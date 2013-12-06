# Need to import path to test/fixtures and test/scripts/
# Ex : export PYTHONPATH='$PATH:/root/test/fixtures/:/root/test/scripts/'
# 
# To run tests, you can do 'python -m testtools.run tests'. To run specific tests,
# You can do 'python -m testtools.run -l tests'
# Set the env variable PARAMS_FILE to point to your ini file. Else it will try to pick params.ini in PWD
# 
from netaddr import IPNetwork

import fixtures
from util import *
from netaddr import *
from time import sleep
import logging as LOG
import re
class DiscoveryVerification(fixtures.Fixture ):
    

    def __init__(self,inputs,api_server_inspect,cn_inspect,agent_inspect,ops_inspect,ds_inspect,logger=LOG):

        self.inputs= inputs 
        self.ops_inspect= ops_inspect 
        self.api_s_inspect= api_server_inspect
        self.agent_inspect= agent_inspect
        self.cn_inspect= cn_inspect
        self.ds_inspect=ds_inspect
        self.logger= logger
#        self.get_all_publishers_by_topology()

    def get_all_control_services_by_topology(self):

        publisher_touple=[]
        services=['xmpp-server']
        for service in services:
            #for ip in self.inputs.bgp_ips:
            for host in self.inputs.bgp_names:
                control_ip = self.inputs.host_data[host]['host_control_ip']
                #t=(ip,service)
                t=(control_ip,service)
                publisher_touple.append(t)
        self.logger.info("Calculated control services as per the testbed file..%s"%(publisher_touple)) 
        return publisher_touple
    
    def get_all_dns_services_by_topology(self):

        publisher_touple=[]
        services=['dns-server']
        for service in services:
            for host in self.inputs.bgp_names:
                control_ip = self.inputs.host_data[host]['host_control_ip']
                #t=(ip,service)
                t=(control_ip,service)
                publisher_touple.append(t)
        self.logger.info("Calculated dns services as per the testbed file..%s"%(publisher_touple)) 
        return publisher_touple
    
    def get_all_api_services_by_topology(self):

        publisher_touple=[]
        self.logger.info("Calculating api services as per the testbed file..") 
        services=['ApiServer']
        for service in services:
            for host in self.inputs.cfgm_names:
                control_ip = self.inputs.host_data[host]['host_control_ip']
                #t=(ip,service)
                t=(control_ip,service)
            publisher_touple.append(t)
        self.logger.info("Calculated api services as per the testbed file..%s"%(publisher_touple)) 
        return publisher_touple
    
    def get_all_ifmap_services_by_topology(self):

        publisher_touple=[]
        self.logger.info("Calculating ifmap services as per the testbed file..") 
        services=['IfmapServer']
        for service in services:
            for host in self.inputs.cfgm_names:
                control_ip = self.inputs.host_data[host]['host_control_ip']
                #t=(ip,service)
                t=(control_ip,service)
            publisher_touple.append(t)
        self.logger.info("Calculated ifmap services as per the testbed file..%s"%(publisher_touple)) 
        return publisher_touple
    
    def get_all_collector_services_by_topology(self):

        publisher_touple=[]
        self.logger.info("Calculating collector services as per the testbed file..") 
        services=['Collector']
        for service in services:
            for host in self.inputs.collector_names:
                control_ip = self.inputs.host_data[host]['host_control_ip']
                #t=(ip,service)
                t=(control_ip,service)
                publisher_touple.append(t)
        self.logger.info("Calculated collector services as per the testbed file..%s"%(publisher_touple)) 
        return publisher_touple

    def get_all_opserver_by_topology(self):

        publisher_touple=[]
        self.logger.info("Calculating opserver services as per the testbed file..") 
        services=['OpServer']
        for service in services:
            for host in self.inputs.collector_names:
                control_ip = self.inputs.host_data[host]['host_control_ip']
                #t=(ip,service)
                t=(control_ip,service)
                publisher_touple.append(t)
        self.logger.info("Calculated opserver as per the testbed file..%s"%(publisher_touple)) 
        return publisher_touple

    def get_all_control_services(self):
        '''http://10.204.216.7:5998/services.json'''

        lst_ip_service_touple=[]
        try:
            obj=self.ds_inspect[self.inputs.cfgm_ip].get_ds_services()
            dct=obj.get_attr('Service',match=('service_type','xmpp-server'))
            for elem in dct:
                ip = elem['info']['ip-address']
                t=(ip,'xmpp-server')
                lst_ip_service_touple.append(t)
        except Exception as e:
            raise
        finally:
            self.logger.info("Registered control services..%s"%(lst_ip_service_touple)) 
            return lst_ip_service_touple

    
    def get_all_collector_services(self):
        '''http://10.204.216.7:5998/services.json'''

        lst_ip_service_touple=[]
        try:
            obj=self.ds_inspect[self.inputs.cfgm_ip].get_ds_services()
            dct=obj.get_attr('Service',match=('service_type','Collector'))
            for elem in dct:
                ip = elem['info']['ip-address']
                t=(ip,'Collector')
                lst_ip_service_touple.append(t)
        except Exception as e:
            print e
            raise
        finally:
            self.logger.info("Registered collector services..%s"%(lst_ip_service_touple)) 
            return lst_ip_service_touple

    def get_all_api_services(self):
        '''http://10.204.216.7:5998/services.json'''

        lst_ip_service_touple=[]
        try:
            obj=self.ds_inspect[self.inputs.cfgm_ip].get_ds_services()
            dct=obj.get_attr('Service',match=('service_type','ApiServer'))
            for elem in dct:
                ip = elem['info']['ip-address']
                t=(ip,'ApiServer')
                lst_ip_service_touple.append(t)
        except Exception as e:
            print e 
        finally:
            self.logger.info("Registered api services..%s"%(lst_ip_service_touple)) 
            return lst_ip_service_touple
    

    def get_all_ifmap_services(self):
        '''http://10.204.216.7:5998/services.json'''

        lst_ip_service_touple=[]
        try:
            obj=self.ds_inspect[self.inputs.cfgm_ip].get_ds_services()
            dct=obj.get_attr('Service',match=('service_type','IfmapServer'))
            for elem in dct:
                ip = elem['info']['ip-address']
                t=(ip,'IfmapServer')
                lst_ip_service_touple.append(t)
        except Exception as e:
            print e 
            raise
        finally:
            self.logger.info("Registered ifmap services..%s"%(lst_ip_service_touple)) 
            return lst_ip_service_touple

    def get_all_dns_services(self):
        '''http://10.204.216.7:5998/services.json'''

        lst_ip_service_touple=[]
        try:
            obj=self.ds_inspect[self.inputs.cfgm_ip].get_ds_services()
            dct=obj.get_attr('Service',match=('service_type','dns-server'))
            for elem in dct:
                ip = elem['info']['ip-address']
                t=(ip,'dns-server')
                lst_ip_service_touple.append(t)
        except Exception as e:
            print e 
            raise
        finally:
            self.logger.info("Registered dns services..%s"%(lst_ip_service_touple)) 
            return lst_ip_service_touple

    def get_all_opserver(self):
        '''http://10.204.216.7:5998/services.json'''

        lst_ip_service_touple=[]
        try:
            obj=self.ds_inspect[self.inputs.cfgm_ip].get_ds_services()
            dct=obj.get_attr('Service',match=('service_type','OpServer'))
            for elem in dct:
#                ip = elem['info']['ip-address']
#Work around for bug [Bug 1692] New: Discovery-Service:http://nodea11:5998/services.json shows opserver ip-address as cfgm ip address
                ip = elem['remote']
                t=(ip,'OpServer')
                lst_ip_service_touple.append(t)
        except Exception as e:
            print e 
            raise
        finally:
            self.logger.info("Registered OpServers..%s"%(lst_ip_service_touple)) 
            return lst_ip_service_touple

    def get_all_services_by_service_name(self,service=None):
        '''http://10.204.216.7:5998/services.json'''

        lst_ip_service_touple=[]
        try:
            obj=self.ds_inspect[self.inputs.cfgm_ip].get_ds_services()
            dct=obj.get_attr('Service',match=('service_type',service))
            for elem in dct:
                ip = elem['info']['ip-address']
                t=(ip,service)
                lst_ip_service_touple.append(t)
        except Exception as e:
            print e 
            raise
        finally:
            self.logger.info("Registered %s..%s"%(service,lst_ip_service_touple)) 
            return lst_ip_service_touple

    def publish_service_to_discovery(self,service=None,ip=None,port=20003):
        '''http://discovery-server-ip:5998/publish'''

        obj=None
        try:
            obj=self.ds_inspect[self.inputs.cfgm_ip].publish_service(service=service,ip=ip,port=port)
        except Exception as e:
            print e 
            raise
        finally:
            return obj

    def subscribe_service_from_discovery(self,service=None,instances=None,client_id=None):
        '''http://discovery-server-ip:5998/subscribe'''

        obj=None
        try:
            obj=self.ds_inspect[self.inputs.cfgm_ip].subscribe_service(service=service,instances=instances,client_id=client_id)
        except Exception as e:
            print e 
            raise
        finally:
            return obj

    def cleanup_service_from_discovery(self):
        '''http://discovery-server-ip:5998/cleanup'''

        obj=None
        try:
            obj=self.ds_inspect[self.inputs.cfgm_ip].cleanup_service()
        except Exception as e:
            print e 
            raise
        finally:
            return obj

    def get_service_status(self,service_touple=()):

        ip=service_touple[0]
        svc=service_touple[1]
        status=None
        try:
            obj=self.ds_inspect[self.inputs.cfgm_ip].get_ds_services()
            dct=obj.get_attr('Service',match=('service_type',svc))
            for elem in dct:
                if ip in elem['info']['ip-address']:
                    status=elem['status']
                    self.logger.info("dct:%s"%(elem))
        except Exception as e:
            raise
        finally:
            return status

    def get_service_admin_state(self,service_touple=()):

        ip=service_touple[0]
        svc=service_touple[1]
        status=None
        try:
            obj=self.ds_inspect[self.inputs.cfgm_ip].get_ds_services()
            dct=obj.get_attr('Service',match=('service_type',svc))
            for elem in dct:
                if ip in elem['info']['ip-address']:
                    status=elem['admin_state']
        except Exception as e:
            raise
        finally:
            return status

    def get_service_id(self,service_touple=()):

        ip=service_touple[0]
        svc=service_touple[1]
        status=None
        try:
            obj=self.ds_inspect[self.inputs.cfgm_ip].get_ds_services()
            dct=obj.get_attr('Service',match=('service_type',svc))
            for elem in dct:
                if ip in elem['info']['ip-address']:
                    status=elem['service_id']
        except Exception as e:
            raise
        finally:
            return status

    def get_service_in_use(self,service_touple=()):

        ip=service_touple[0]
        svc=service_touple[1]
        status=None
        try:
            obj=self.ds_inspect[self.inputs.cfgm_ip].get_ds_services()
            dct=obj.get_attr('Service',match=('service_type',svc))
            for elem in dct:
                if ip in elem['info']['ip-address']:
                    status=elem['in_use']
        except Exception as e:
            print e
        finally:
            return status

    def get_service_prov_state(self,service_touple=()):

        ip=service_touple[0]
        svc=service_touple[1]
        status=None
        try:
            obj=self.ds_inspect[self.inputs.cfgm_ip].get_ds_services()
            dct=obj.get_attr('Service',match=('service_type',svc))
            for elem in dct:
                if ip in elem['info']['ip-address']:
                    status=elem['prov_state']
        except Exception as e:
            print e
        finally:
            return status

    def get_service_endpoint_by_service_id(self,service_id=None):

        t2=()
        try:
            obj=self.ds_inspect[self.inputs.cfgm_ip].get_ds_services()
            dct=obj.get_attr('Service',match=('service_id',service_id))
            for elem in dct:
                t1=(elem['info']['ip-address'],elem['info']['port'])
                t2=(t1,elem['service_type'])
        except Exception as e:
            print e
        finally:
            return t2

    def get_service_id_by_service_end_point(self,service_touple=()):

        '''Returns service id of a (service type,ip)'''

        ip=service_touple[0]
        service=service_touple[1]
        t2=None
        try:
            obj=self.ds_inspect[self.inputs.cfgm_ip].get_ds_services()
            dct=obj.get_attr('Service',match=('service_type',service))
            for elem in dct:
#                if (service == 'Apiservice' or service == 'Ifmapservice'):
#                    if (ip == elem['info']['ip_addr']):
#                        t2=elem['service_id']
#                else:
#                if (ip == elem['info']['ip-address']):
                if (ip == elem['remote']):
                    t2=elem['service_id']
        except Exception as e:
            print e 
        finally:
            return t2

    
    def get_service_status_by_service_id(self,service_id=None):

        t2={}
        try:
            obj=self.ds_inspect[self.inputs.cfgm_ip].get_ds_services()
            dct=obj.get_attr('Service',match=('service_id',service_id))
            for elem in dct:
                t1={}
                t1['prov_state']=elem['prov_state']
                t2.update(t1)
                t1['admin_state']=elem['admin_state']
                t2.update(t1)
                t1['status']=elem['status']
                t2.update(t1)
                t1['in_use']=elem['in_use']
                t2.update(t1)
                t1['ts_use']=elem['ts_use']
                t2.update(t1)
        except Exception as e:
            print e 
        finally:
            return t2
    

    def get_subscribed_service_id(self,client=(),service=None):

        '''Returns service id subscribed by a client'''

        client_ip=client[0]
        client_svc=client[1]
        service_id=[]
        try:
            obj=self.ds_inspect[self.inputs.cfgm_ip].get_ds_clients()
            dct=obj.get_attr('Clients',match=('remote',client_ip))
            for elem in dct:
                if service in elem['service_type']:
                    client_type=elem['client_type']
                    if re.search(client_svc,client_type):
                        service_id.append(elem['service_id'])
                        self.logger.info("dct: %s "%(elem))
        except Exception as e:
            print e 
        finally:
            return service_id

    def get_xmpp_server_of_agent(self,agent_ip=None):

        control_nodes=[]
        try:
            lst_service_id=self.get_subscribed_service_id(client=(agent_ip,'VRouterAgent'),service='xmpp-server')
            for id in lst_service_id:
                node=self.get_service_endpoint_by_service_id(service_id=id)
                control_nodes.append(node)
        except Exception as e:
            print e
        finally:
            return control_nodes
    
    def get_all_clients_subscribed_to_a_service(self,service_touple=()):

        clients=[]
        ip=service_touple[0]
        service=service_touple[1]
        try:
            service_id=self.get_service_id(service_touple=service_touple)
            obj=self.ds_inspect[self.inputs.cfgm_ip].get_ds_clients()
            dct=obj.get_attr('Clients',match=('service_id',service_id))
            for elem in dct:
                client_ip=elem['remote']
                clients.append(client_ip)
        except Exception as e:
            print e
        finally:
            return clients

                
    def verify_registered_services_to_discovery_service(self):

        result=True

        expected_control_services=self.get_all_control_services_by_topology()
        expected_collector_services=self.get_all_collector_services_by_topology()
        expected_api_services=self.get_all_api_services_by_topology()
        expected_ifmap_services=self.get_all_ifmap_services_by_topology()
        expected_opserver=self.get_all_opserver_by_topology()
        expected_dns_services=self.get_all_dns_services_by_topology()
        registered_control_services=self.get_all_control_services()         
        registered_api_services=self.get_all_api_services()         
        registered_ifmap_services=self.get_all_ifmap_services()         
        registered_collector_services=self.get_all_collector_services()
        registered_opserver=self.get_all_opserver()
        registered_dns_services=self.get_all_dns_services()
        #checking for missing registered service
        diff=set(expected_control_services) ^ set (registered_control_services)
        if diff:
            self.logger.warn("Inconsistency in registerd services %s"%(diff))
            result=result and False
        else:
            self.logger.info("%s registered to discover service"%(expected_control_services))
            result=result and True
        #checking for missing registered service
        diff=set(expected_collector_services) ^ set (registered_collector_services)
        if diff:
            self.logger.warn("Inconsistency in registerd services %s"%(diff))
            result=result and False
        else:
            self.logger.info("%s registered to discover service"%(expected_collector_services))
            result=result and True
        #checking for missing registered service
        diff=set(expected_api_services) ^ set (registered_api_services)
        if diff:
            self.logger.warn("Inconsistency in registerd services %s"%(diff))
            result=result and False
        else:
            self.logger.info("%s registered to discover service"%(expected_api_services))
            result=result and True
        #checking for missing registered service
        diff=set(expected_ifmap_services) ^ set (registered_ifmap_services)
        if diff:
            self.logger.warn("Inconsistency in registerd services %s"%(diff))
            result=result and False
        else:
            self.logger.info("%s registered to discover service"%(expected_ifmap_services))
            result=result and True

        #checking for missing registered service
        diff=set(expected_opserver) ^ set (registered_opserver)
        if diff:
            self.logger.warn("Inconsistency in registerd services %s"%(diff))
            result=result and False
        else:
            self.logger.info("%s registered to discover service"%(registered_opserver))
            result=result and True

        #checking for missing registered service
        diff=set(expected_dns_services) ^ set (registered_dns_services)
        if diff:
            self.logger.warn("Inconsistency in registerd services %s"%(diff))
            result=result and False
        else:
            self.logger.info("%s registered to discover service"%(registered_dns_services))
            result=result and True

        #Verifying the service provision state/status/admin state
        self.logger.info("Checking for control node service")
        for service in registered_control_services:
            t={}
            service_id=self.get_service_id_by_service_end_point(service_touple=service)
            t=self.get_service_status_by_service_id(service_id=service_id)
            self.logger.info("Service health: %s"%(t)) 
            if (t['admin_state'] == 'up'and t['status'] == 'up'):
                self.logger.info("%s service is up"%(service,))
                result = result and True
            else:
                self.logger.warn("%s service not up"%(service,))
                result = result and False
        
        self.logger.info("Checking for api service")
        for service in registered_api_services:
            t={}
            service_id=self.get_service_id_by_service_end_point(service_touple=service)
            t=self.get_service_status_by_service_id(service_id=service_id)
            self.logger.info("Service health: %s"%(t)) 
            if (t['admin_state'] == 'up'and t['status'] == 'up'):
                self.logger.info("%s service is up"%(service,))
                result = result and True
            else:
                self.logger.warn("%s service not up"%(service,))
                result = result and False
        
        self.logger.info("Checking for ifmap service")
        for service in registered_ifmap_services:
            t={}
            service_id=self.get_service_id_by_service_end_point(service_touple=service)
            t=self.get_service_status_by_service_id(service_id=service_id)
            self.logger.info("Service health: %s"%(t)) 
            if (t['admin_state'] == 'up'and t['status'] == 'up'):
                self.logger.info("%s service is up"%(service,))
                result = result and True
            else:
                self.logger.warn("%s service not up"%(service,))
                result = result and False
        
        self.logger.info("Checking for collector service")
        for service in registered_collector_services:
            t={}
            service_id=self.get_service_id_by_service_end_point(service_touple=service)
            t=self.get_service_status_by_service_id(service_id=service_id)
            self.logger.info("Service health: %s"%(t)) 
            if (t['admin_state'] == 'up'and t['status'] == 'up'):
                self.logger.info("%s service is up"%(service,))
                result = result and True
            else:
                self.logger.warn("%s service not up"%(service,))
                result = result and False
        
        self.logger.info("Checking for dns service")
        for service in registered_dns_services:
            t={}
            service_id=self.get_service_id_by_service_end_point(service_touple=service)
            t=self.get_service_status_by_service_id(service_id=service_id)
            self.logger.info("Service health: %s"%(t)) 
            if (t['admin_state'] == 'up'and t['status'] == 'up'):
                self.logger.info("%s service is up"%(service,))
                result = result and True
            else:
                self.logger.warn("%s service not up"%(service,))
                result = result and False
        
        self.logger.info("Checking for opserver")
        for service in registered_opserver:
            t={}
            service_id=self.get_service_id_by_service_end_point(service_touple=service)
            t=self.get_service_status_by_service_id(service_id=service_id)
            self.logger.info("Service health: %s"%(t)) 
            if (t['admin_state'] == 'up'and t['status'] == 'up'):
                self.logger.info("%s service is up"%(service,))
                result = result and True
            else:
                self.logger.warn("%s service not up"%(service,))
                result = result and False

        return result

    def verify_bgp_connection(self):
        
        result=True
        for host in self.inputs.bgp_names:
            control_ip = self.inputs.host_data[host]['host_control_ip']
            username= self.inputs.host_data[host]['username']
            password= self.inputs.host_data[host]['password']
            if host in self.inputs.compute_names:
                host_ip = self.inputs.host_data[host]['host_ip']
                # Verify the connection between compute to all control nodes 
                inspect_h= self.agent_inspect[host_ip]
                agent_xmpp_status= inspect_h.get_vna_xmpp_connection_status()

                # Calculating the the expected list of bgp peer
                expected_bgp_peer = []
                bgp_peer_touple_from_discovery=self.get_xmpp_server_of_agent(agent_ip=control_ip)
                for t in bgp_peer_touple_from_discovery:
                    ip=t[0][0]
                    expected_bgp_peer.append(ip)
                self.logger.info("%s compute is subscribed to %s bgp nodes"%(host,expected_bgp_peer))
                expected_bgp_peer_by_addr = []
                actual_bgp_peer = []
#
                # Get the actual list of controller IP
                for i in xrange(len(agent_xmpp_status)): actual_bgp_peer.append(agent_xmpp_status[i]['controller_ip'])

                # Matching the expected and actual bgp contreoller
                # sort the value for list match
                actual_bgp_peer.sort()
                expected_bgp_peer.sort()
                self.logger.info("Actual XmppServer for %s : %s"%(host,actual_bgp_peer))
                self.logger.info("Expected XmppServer for %s : %s"%(host,expected_bgp_peer))

                if actual_bgp_peer != expected_bgp_peer :
                    result = result and False
                    self.logger.error('All the required BGP controller has not found in agent introspect for %s' %(host))
                for entry in agent_xmpp_status:
                    if entry['state'] != 'Established':
                        result = result and False
                        self.logger.info('From agent %s connection to control node %s is not Established' %(host , entry['controller_ip']))
            if host in self.inputs.bgp_names:
                host_ip = self.inputs.host_data[host]['host_ip']
                # Verify the connection between all control nodes
                cn_bgp_entry=self.cn_inspect[host_ip].get_cn_bgp_neigh_entry()
                control_node_bgp_peer_list = []
                control_node_bgp_xmpp_peer_list = []
                if type(cn_bgp_entry) == type(dict()):
                    if cn_bgp_entry['peer_address'] in self.inputs.bgp_ips:
                        if cn_bgp_entry['state'] != 'Established':
                            self.logger.error('For control node %s, with peer %s peering is not Established. Current State %s ' %(host, cn_bgp_entry['peer_address'] , cn_bgp_entry['state']))
                    if cn_bgp_entry['encoding']== 'BGP':
                        control_node_bgp_peer_list= [cn_bgp_entry['peer_address']]
                    else:
                        control_node_bgp_xmpp_peer_list= [cn_bgp_entry['peer_address']]
                else:
                    for entry in cn_bgp_entry:
                        if entry ['peer_address'] in self.inputs.bgp_ips:
                            if entry ['state'] != 'Established':
                                result = result and False
                                self.logger.error('For control node %s, with peer %s peering is not Established. Current State %s ' %(host, entry ['peer'] , entry['state']) )
                        if entry['encoding']== 'BGP':
                            control_node_bgp_peer_list.append(entry['peer_address'])
                        else:
                            control_node_bgp_xmpp_peer_list.append(entry['peer_address'])

                # Verify all required xmpp entry is present in control node
                #Get computes subscribed to this control node
                computes=self.get_all_clients_subscribed_to_a_service(service_touple=(control_ip,'xmpp-server'))
                self.logger.info("%s bgp node subscribed by %s xmpp-clients"%(control_ip,computes))
                computes.sort()
                control_node_bgp_xmpp_peer_list.sort()
                self.logger.info("From control node introspect, xmpp-clients: %s"%(control_node_bgp_xmpp_peer_list))
                if computes != control_node_bgp_xmpp_peer_list :
                   result = result and False
                   self.logger.error('All the required XMPP entry not present in control node introspect for %s' %(host))
                # Verify all required BGP entry is present in control node
                control_node_bgp_peer_list.append(control_ip)


                # sort the value for list match
                control_node_bgp_peer_list.sort()
                self.inputs.bgp_control_ips.sort()
                if not set(self.inputs.bgp_control_ips).issubset(control_node_bgp_peer_list) :
                    result = result and False
                    self.logger.error('All the required BGP entry not present in control node introspect for %s' %(host))
        if not result :
            self.logger.error('One or more process-states are not correct on nodes')
        return result
    #end verify_control_connection 

    def verify_agents_connected_to_dns_service(self): 

        '''Verifies that agents connected to dns service''' 
        
        result=True
        for ip in self.inputs.compute_ips:
            dns_nodes=[]
            try:
                lst_service_id=self.get_subscribed_service_id(client=(ip,'VRouterAgent'),service='dns-server')
                for id in lst_service_id:
                    node=self.get_service_endpoint_by_service_id(service_id=id)
                    dns_nodes.append(node)
            except Exception as e:
                print e
            if dns_nodes:
                self.logger.info("Agent %s connected to dns-service %s"%(ip,dns_nodes))
                result=result and True
            else:
                self.logger.warn("Agent %s not connected to any dns-servicet"%(ip))
                return False
            self.logger.info("Verifying that dns-servers belongs to this test bed")
            dns_ips=[]
            for t in dns_nodes:
                dns_ip=t[0][0]
                dns_ips.append(dns_ip)
            dns_ips.sort()
            self.inputs.bgp_ips.sort()
            if (set(dns_ips).issubset(self.inputs.bgp_ips)):
                self.logger.info("Agent %s is connected to proper dns-servers %s"%(ip,dns_ips))
                result=result and True
            else:
                self.logger.warn("Agent %s is not connected to proper dns-servers %s"%(ip,dns_ips))
                self.logger.info("Proper dns servers should be %s"%(self.inputs.bgp_ips))
                result = result and False
        return result
                
                
            
    def verify_agents_connected_to_collector_service(self): 

        '''Verifies that agents connected to collector service''' 
        
        result=True
        for ip in self.inputs.compute_control_ips:
            collector_nodes=[]
            try:
                lst_service_id=self.get_subscribed_service_id(client=(ip,'VRouterAgent'),service='Collector')
                for id in lst_service_id:
                    node=self.get_service_endpoint_by_service_id(service_id=id)
                    collector_nodes.append(node)
            except Exception as e:
                print e
            if collector_nodes:
                self.logger.info("Agent %s connected to collector-service %s"%(ip,collector_nodes))
                result=result and True
            else:
                self.logger.warn("Agent %s not connected to any collector-servicet"%(ip))
                return False
            self.logger.info("Verifying that collectors belongs to this test bed")
            collector_ips=[]
            for t in collector_nodes:
                collector_ip=t[0][0]
                collector_ips.append(collector_ip)
            collector_ips.sort()
            self.inputs.collector_control_ips.sort()
            if (set(collector_ips).issubset(self.inputs.collector_control_ips)):
                self.logger.info("Agent %s is connected to proper collectors %s"%(ip,collector_ips))
                result=result and True
            else:
                self.logger.warn("Agent %s is not connected to proper collectors %s"%(ip,collector_ips))
                self.logger.info("Proper collectors should be %s"%(self.inputs.collector_ips))
                result = result and False
        return result
    
    def verify_dns_agent_connected_to_collector_service(self): 

        '''Verifies that dns agents connected to collector service''' 
        
        result=True
        for ip in self.inputs.bgp_control_ips:
            collector_nodes=[]
            try:
                lst_service_id=self.get_subscribed_service_id(client=(ip,'DnsAgent'),service='Collector')
                for id in lst_service_id:
                    node=self.get_service_endpoint_by_service_id(service_id=id)
                    collector_nodes.append(node)
            except Exception as e:
                print e
            if collector_nodes:
                self.logger.info("DnsAgent %s connected to collector-service %s"%(ip,collector_nodes))
                result=result and True
            else:
                self.logger.warn("DnsAgent %s not connected to any collector-servicet"%(ip))
                return False
            self.logger.info("Verifying that collectors belongs to this test bed")
            collector_ips=[]
            for t in collector_nodes:
                collector_ip=t[0][0]
                collector_ips.append(collector_ip)
            collector_ips.sort()
            self.inputs.collector_control_ips.sort()
            if (set(collector_ips).issubset(self.inputs.collector_control_ips)):
                self.logger.info("DnsAgent %s is connected to proper collectors %s"%(ip,collector_ips))
                result=result and True
            else:
                self.logger.warn("DnsAgent %s is not connected to proper collectors %s"%(ip,collector_ips))
                self.logger.info("Proper collectors should be %s"%(self.inputs.collector_ips))
                result = result and False
        return result
    
    def verify_control_nodes_connected_to_collector_service(self): 

        '''Verifies that dns agents connected to collector service''' 
        
        result=True
        for ip in self.inputs.bgp_control_ips:
            collector_nodes=[]
            try:
                lst_service_id=self.get_subscribed_service_id(client=(ip,'ControlNode'),service='Collector')
                for id in lst_service_id:
                    node=self.get_service_endpoint_by_service_id(service_id=id)
                    collector_nodes.append(node)
            except Exception as e:
                print e
            if collector_nodes:
                self.logger.info("ControlNode %s connected to collector-service %s"%(ip,collector_nodes))
                result=result and True
            else:
                self.logger.warn("ControlNode %s not connected to any collector-servicet"%(ip))
                return False
            self.logger.info("Verifying that collectors belongs to this test bed")
            collector_ips=[]
            for t in collector_nodes:
                collector_ip=t[0][0]
                collector_ips.append(collector_ip)
            collector_ips.sort()
            self.inputs.collector_control_ips.sort()
            if (set(collector_ips).issubset(self.inputs.collector_control_ips)):
                self.logger.info("ControlNode %s is connected to proper collectors %s"%(ip,collector_ips))
                result=result and True
            else:
                self.logger.warn("ControlNode %s is not connected to proper collectors %s"%(ip,collector_ips))
                self.logger.info("Proper collectors should be %s"%(self.inputs.collector_ips))
                result = result and False
        return result
    
    def verify_control_nodes_subscribed_to_ifmap_service(self): 

        '''Verifies that control nodes subscribed to ifmap service''' 
        
        result=True
        for host in self.inputs.bgp_names:
            host_ip = self.inputs.host_data[host]['host_ip']
            control_ip = self.inputs.host_data[host]['host_control_ip']
            subscribed_ifmap_nodes_from_discovery=[]
            subscribed_ifmap_nodes_from_cn_introspect=[]
            try:
                lst_service_id=self.get_subscribed_service_id(client=(control_ip,'ControlNode'),service='IfmapServer')
                for id in lst_service_id:
#                    uid = (id,'IfmapServer')
                    endpoint=self.get_service_endpoint_by_service_id(service_id=id)
                    node = endpoint
                    subscribed_ifmap_nodes_from_discovery.append(node)
                l = self.cn_inspect[host_ip].get_if_map_peer_server_info(match = 'ds_peer_info')
                for elem in subscribed_ifmap_nodes_from_discovery:
                    result1 = True 
                    for elem1 in l['IFMapDSPeerInfo']['ds_peer_list']:
                        if (elem[0][0] == elem1['host'] and elem[0][1] == elem1['port'] and elem1['in_use'] == 'true' ):
                            self.logger.info("ControlNode %s connected to ifmapservice %s"%(control_ip,elem1))
                            result=result and True
                            result1 = True
                            break
                        else:
                            result1 = False
                            continue
#                            self.logger.warn("ControlNode %s not connected to any ifmapservice"%(ip))
#                            result = result and  False
                    if not result1:
                        self.logger.warn("ControlNode %s not connected to any ifmapservice"%(control_ip))
                        result = result and  False
            except Exception as e:
                result = result and  False
                self.logger.warn("Got exception as %s" %e)
        return result

    def verify_dns_agent_subscribed_to_ifmap_service(self): 

        '''Verifies that dns agent subscribed to ifmap service''' 
        
        result=True
        result1=True
        for ip in self.inputs.bgp_control_ips:
            subscribed_ifmap_nodes_from_discovery=[]
            subscribed_ifmap_nodes_from_cn_introspect=[]
            try:
                lst_service_id=self.get_subscribed_service_id(client=(ip,'DnsAgent'),service='IfmapServer')
                for id in lst_service_id:
                    node=self.get_service_endpoint_by_service_id(service_id=id)
                    subscribed_ifmap_nodes_from_discovery.append(node)
                for elem in subscribed_ifmap_nodes_from_discovery:
                    if (self.inputs.cfgm_control_ip in elem[0][0]):
                        self.logger.info("Dns agent %s connected to ifmapservice %s"%(ip,subscribed_ifmap_nodes_from_discovery))
                        result=result and True
                        result1=True
                        break
                    else:
                        result1=False
                if not result1:
                    self.logger.warn("Dns agent %s not connected to any ifmapservice"%(ip))
                    result = result and  False

            except Exception as e:
                self.logger.warn("Got exception as %s"%(e))
                result = result and False
        return result 


    def verify_ApiServer_subscribed_to_collector_service(self): 

        '''Verifies that ApiServer subscribed to collector service''' 
        
        result=True
#        for ip in self.inputs.cfgm_ip:
#            import pdb;pdb.set_trace()
        ip = self.inputs.cfgm_control_ip
        collector_nodes=[]
        try:
            lst_service_id=self.get_subscribed_service_id(client=(ip,'ApiServer'),service='Collector')
            for id in lst_service_id:
                node=self.get_service_endpoint_by_service_id(service_id=id)
                collector_nodes.append(node)
        except Exception as e:
            print e
        if collector_nodes:
            self.logger.info("ApiServer %s connected to collector-service %s"%(ip,collector_nodes))
            result=result and True
        else:
            self.logger.warn("ApiServer %s not connected to any collector-servicet"%(ip))
            return False
        self.logger.info("Verifying that collectors belongs to this test bed")
        collector_ips=[]
        for t in collector_nodes:
            collector_ip=t[0][0]
            collector_ips.append(collector_ip)
        collector_ips.sort()
        self.inputs.collector_control_ips.sort()
        if (set(collector_ips).issubset(self.inputs.collector_control_ips)):
            self.logger.info("ApiServer %s is connected to proper collectors %s"%(ip,collector_ips))
            result=result and True
        else:
            self.logger.warn("ApiServer %s is not connected to proper collectors %s"%(ip,collector_ips))
            self.logger.info("Proper collectors should be %s"%(self.inputs.collector_ips))
            result = result and False
        return result
    
    def verify_Schema_subscribed_to_collector_service(self): 

        '''Verifies that Schema subscribed to collector service''' 
        
        result=True
        ip = self.inputs.cfgm_control_ip
#        for ip in self.inputs.cfgm_ip:
        collector_nodes=[]
        try:
            lst_service_id=self.get_subscribed_service_id(client=(ip,'Schema'),service='Collector')
            for id in lst_service_id:
                node=self.get_service_endpoint_by_service_id(service_id=id)
                collector_nodes.append(node)
        except Exception as e:
            print e
        if collector_nodes:
            self.logger.info("Schema %s connected to collector-service %s"%(ip,collector_nodes))
            result=result and True
        else:
            self.logger.warn("Schema %s not connected to any collector-servicet"%(ip))
            return False
        self.logger.info("Verifying that collectors belongs to this test bed")
        collector_ips=[]
        for t in collector_nodes:
            collector_ip=t[0][0]
            collector_ips.append(collector_ip)
        collector_ips.sort()
        self.inputs.collector_control_ips.sort()
        if (set(collector_ips).issubset(self.inputs.collector_control_ips)):
            self.logger.info("Schema %s is connected to proper collectors %s"%(ip,collector_ips))
            result=result and True
        else:
           self.logger.warn("Schema %s is not connected to proper collectors %s"%(ip,collector_ips))
           self.logger.info("Proper collectors should be %s"%(self.inputs.collector_ips))
           result = result and False
        return result
    
    def verify_ServiceMonitor_subscribed_to_collector_service(self): 

        '''Verifies that ServiceMonitor subscribed to collector service''' 
        
        result=True
        ip = self.inputs.cfgm_control_ip
#        for ip in self.inputs.cfgm_ip:
        collector_nodes=[]
        try:
            lst_service_id=self.get_subscribed_service_id(client=(ip,'Service Monitor'),service='Collector')
            for id in lst_service_id:
                node=self.get_service_endpoint_by_service_id(service_id=id)
                collector_nodes.append(node)
        except Exception as e:
            print e
        if collector_nodes:
            self.logger.info("Service Monitor %s connected to collector-service %s"%(ip,collector_nodes))
            result=result and True
        else:
            self.logger.warn("ServiceMonitor %s not connected to any collector-servicet"%(ip))
            return False
        self.logger.info("Verifying that collectors belongs to this test bed")
        collector_ips=[]
        for t in collector_nodes:
            collector_ip=t[0][0]
            collector_ips.append(collector_ip)
        collector_ips.sort()
        self.inputs.collector_control_ips.sort()
        if (set(collector_ips).issubset(self.inputs.collector_control_ips)):
            self.logger.info("ServiceMonitor %s is connected to proper collectors %s"%(ip,collector_ips))
            result=result and True
        else:
            self.logger.warn("ServiceMonitor %s is not connected to proper collectors %s"%(ip,collector_ips))
            self.logger.info("Proper collectors should be %s"%(self.inputs.collector_ips))
            result = result and False
        return result