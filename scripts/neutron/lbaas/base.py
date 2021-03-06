from common.neutron.base import BaseNeutronTest
from tcutils.commands import ssh, execute_cmd, execute_cmd_out
from fabric.context_managers import settings, hide
from tcutils.util import run_fab_cmd_on_node
import re
from time import sleep

class BaseTestLbaas(BaseNeutronTest):

    @classmethod
    def setUpClass(cls):
        super(BaseTestLbaas, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(BaseTestLbaas, cls).tearDownClass()


    def verify_active_standby(self, compute_ips, pool_uuid):
        cmd1 = 'ip netns list | grep %s' % pool_uuid
        cmd2 = 'ps -aux | grep loadbalancer | grep %s' % pool_uuid
        netns_list = {}
        haproxy_pid = {}
        result = True
        errmsg = []
        for compute_ip in compute_ips:
            out = self.inputs.run_cmd_on_server(
                                       compute_ip, cmd1,
                                       self.inputs.host_data[compute_ip]['username'],
                                       self.inputs.host_data[compute_ip]['password'])
            output = out.strip().split('\n')
            if len(output) != 1:
                return False, ('Found more than one NETNS (%s) while'
                               'expecting one with pool ID (%s)' % (output, pool_uuid))

            netns_list[compute_ip] = output[0]
            out = self.inputs.run_cmd_on_server(
                                       compute_ip, cmd2,
                                       self.inputs.host_data[compute_ip]['username'],
                                       self.inputs.host_data[compute_ip]['password'])
            pid = []
            output = out.split('\n')
            for out in output:
                match = re.search("nobody\s+(\d+)\s+",out)
                if match:
                    pid.append(match.group(1))
            if len(pid) != 1:
                 return False, ('Found more than one instance of haproxy running while'
                                ' expecting one with pool ID (%s)' % (pool_uuid))
            haproxy_pid[compute_ip] = pid

        self.logger.info("Created net ns: %s" % (netns_list.values()))
        if len(self.inputs.compute_ips) >= 2:
            if len(netns_list.values()) == 2:
                self.logger.info('More than 1 compute in setup: Active and Standby nets got'
                                 ' created on compute nodes: (%s)' % (netns_list.keys()))
            else:
                errmsg.append("2 netns did not get created for Active and Standby")
                result = False
            if len(haproxy_pid.values()) == 2:
                self.logger.info('More than 1 compute in setup: Active and Standby haproxy running on'
                                 ' compute node: (%s)' % (haproxy_pid.keys()))
            else:
                errmsg.append("Haproxy not running in 2 computes for Active and Standby")
                result = False
        else:
            if(netns_list.values()):
                self.logger.info('one compute in setup, sinlge netns got created'
                                 ' on compute:(%s)' % (netns_list.keys()))
            else:
                errmsg.append("NET NS didnot get created")
                result = False
            if(haproxy_pid.values()):
                self.logger.info('one compute in setup,  haproxy running on'
                                  ' compute:(%s)' % (haproxy_pid.keys()))
            else:
                errmsg.append("haproxy not running on compute node")
                result = False

        return (result,errmsg)

    def start_simpleHTTPserver(self, servers):
        output = ''
        for server in servers:
            with hide('everything'):
                with settings(host_string='%s@%s' % (self.inputs.username,server.vm_node_ip),
                              password=self.inputs.password, warn_only=True,abort_on_prompts= False):
                    cmd1 = 'sudo hostname > index.html'
                    cmd2 = 'sudo python -m SimpleHTTPServer 80 & sleep 600'
                    output = run_fab_cmd_on_node(host_string = '%s@%s'%(server.vm_username,server.local_ip),
                                            password = server.vm_password, cmd = cmd1, as_sudo=False)
                    output = run_fab_cmd_on_node(host_string = '%s@%s'%(server.vm_username,server.local_ip),
                                        password = server.vm_password, cmd = cmd2, as_sudo=False, timeout=2)
        return

    def run_wget(self, vm, vip):
        response = ''
        out = ''
        result = False
        with hide('everything'):
            with settings(host_string='%s@%s' % (self.inputs.username,vm.vm_node_ip),
                             password=self.inputs.password, warn_only=True,abort_on_prompts= False):
                cmd1 = 'sudo wget http://%s' % vip
                cmd2 = 'cat index.html'
                cmd3 = 'rm -rf index.html'
                result = run_fab_cmd_on_node(host_string = '%s@%s'%(vm.vm_username,vm.local_ip),
                                        password = vm.vm_password, cmd = cmd1, as_sudo=False)
                if result.count('200 OK'):
                    result = True
                    self.logger.info("connections to vip %s successful" % (vip))
                    response = run_fab_cmd_on_node(host_string = '%s@%s'%(vm.vm_username,vm.local_ip),
                                                  password = vm.vm_password, cmd = cmd2, as_sudo=False)
                    out = run_fab_cmd_on_node(host_string = '%s@%s'%(vm.vm_username,vm.local_ip),
                                              password = vm.vm_password, cmd = cmd3, as_sudo=False)
                    self.logger.info("Request went to server: %s" % (response))
                else:
                    self.logger.error("Error in response on connecting to vip %s. Error is %s" % (vip, result))
                    result = False
                return (result,response)
    #end run_wget

    def get_netns_left_intf(self, server_ip, pool_uuid):
        cmd = 'ip netns list | grep %s' % pool_uuid
        left_int = ''
        out = self.inputs.run_cmd_on_server(
                                       server_ip, cmd,
                                       self.inputs.host_data[server_ip]['username'],
                                       self.inputs.host_data[server_ip]['password'])
        pattern = "vrouter-((\w+-)+\w+):"
        match = re.match(pattern, out)
        if match:
            netns = match.group(1)
            inspect_h = self.agent_inspect[server_ip]
            for tapint in inspect_h.get_vna_tap_interface_by_vm(netns):
                if 'left interface' in tapint['vm_name']:
                    left_int = tapint['name']
        return left_int

    def start_tcpdump(self, server_ip, tap_intf):
        session = ssh(server_ip,self.inputs.host_data[server_ip]['username'],self.inputs.host_data[server_ip]['password'])
        pcap = '/tmp/%s.pcap' % tap_intf
        cmd = "tcpdump -nei %s tcp -w %s" % (tap_intf, pcap)
        self.logger.info("Staring tcpdump to capture the packets on server %s" % (server_ip))
        execute_cmd(session, cmd, self.logger)
        return pcap, session

    def stop_tcpdump(self,session, pcap):
        self.logger.info("Waiting for the tcpdump write to complete.")
        sleep(30)
        cmd = 'kill $(pidof tcpdump)'
        execute_cmd(session, cmd, self.logger)
        cmd = 'tcpdump -r %s | wc -l' % pcap
        out, err = execute_cmd_out(session, cmd, self.logger)
        count = int(out.strip('\n'))
        cmd = 'rm -f %s' % pcap
        execute_cmd(session, cmd, self.logger)
        return count

    def start_stop_service(self, server_ip, service, action):
        cmd =  "service %s %s" % (service, action)
        out = self.inputs.run_cmd_on_server(
                                   server_ip, cmd,
                                   self.inputs.host_data[server_ip]['username'],
                                   self.inputs.host_data[server_ip]['password'])
        cmd = "service %s status" % (service)
        output = self.inputs.run_cmd_on_server(
                                   server_ip, cmd,
                                   self.inputs.host_data[server_ip]['username'],
                                   self.inputs.host_data[server_ip]['password'])
        if action == 'stop' and 'STOPPED' in output:
                self.logger.info("%s service stopped in server %s" % (service, server_ip))
        elif action == 'start' and 'RUNNING' in output:
                self.logger.info("%s service running in server %s" % (service, server_ip))
        else:
            self.logger.warn("requested action is %s for service %s, but current staus is %s" % (action, service, output))
        return
