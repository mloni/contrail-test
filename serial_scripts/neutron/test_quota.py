import random
from vn_test import MultipleVNFixture
from floating_ip import FloatingIPFixture
from connections import ContrailConnections
from tcutils.wrappers import preposttest_wrapper
from user_test import UserFixture
from project_test import ProjectFixture
from base import BaseNeutronTest
import test
from tcutils.util import *


class TestQuotaUpdate(BaseNeutronTest):

    @classmethod
    def setUpClass(cls):
        super(TestQuotaUpdate, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(TestQuotaUpdate, cls).tearDownClass()

    @preposttest_wrapper
    def test_update_default_quota_for_admin_tenant(self):
        result = True
        self.update_default_quota_list(
            subnet=3,
            virtual_network=3,
            floating_ip=10,
            logical_router=10,
            security_group_rule=10,
            virtual_machine_interface=5,
            security_group=5)

        resource_dict = self.create_quota_test_resources(
            self.admin_inputs,
            self.admin_connections,
            vn_count=3,
            router_count=10,
            secgrp_count=4,
            secgep_rule_count=9,
            fip_count=10,
            port_count=5)

        for item in resource_dict.keys():
            if item != 'vn_fix':
                if None in resource_dict[item]:
                    result = False
                    self.logger.error(
                        "Error while creating resource within quota limit for %s please check logs " %
                        (item))

        (vn_name, vn_fix) = resource_dict['vn_fix']._vn_fixtures[1]
        sg_objs = resource_dict['sg_grps']
        response_dict = self.verify_quota_limit(
            self.admin_inputs,
            self.admin_connections,
            vn_fix,
            sg_objs[0])
        for item in response_dict.keys():
            if response_dict[item]:
                result = False
                self.logger.error("Quota limit not followed for %s " % (item))

        assert result, 'Quota tests failed'

    @preposttest_wrapper
    def test_update_default_quota_for_new_tenant(self):
        result = True
        self.update_default_quota_list(
            subnet=3,
            virtual_network=3,
            floating_ip=10,
            logical_router=10,
            security_group_rule=10,
            virtual_machine_interface=5,
            security_group=5)

        resource_dict = self.create_quota_test_resources(
            self.inputs,
            self.connections,
            vn_count=3,
            router_count=10,
            secgrp_count=4,
            secgep_rule_count=9,
            fip_count=10,
            port_count=5)

        for item in resource_dict.keys():
            if item != 'vn_fix':
                if None in resource_dict[item]:
                    result = False
                    self.logger.error(
                        "Error while creating resource within quota limit for %s please check logs " %
                        (item))

        (vn_name, vn_fix) = resource_dict['vn_fix']._vn_fixtures[1]
        sg_objs = resource_dict['sg_grps']

        response_dict = self.verify_quota_limit(
            self.inputs,
            self.connections,
            vn_fix,
            sg_objs[0])
        for item in response_dict.keys():
            if response_dict[item]:
                result = False
                self.logger.error("Quota limit not followed for %s " % (item))

        assert result, 'Quota tests failed'

    def create_quota_test_resources(
            self,
            inputs,
            connections,
            vn_count=1,
            vm_count=1,
            router_count=1,
            secgrp_count=1,
            secgep_rule_count=1,
            fip_count=1,
            port_count=1):
        resource_dict = {}
        self.inputs = inputs
        self.connections = connections
        vn_s = self.create_random_vn_list(vn_count)
        multi_vn_fixture = self.create_multiple_vn(inputs, connections, vn_s)
        assert multi_vn_fixture.verify_on_setup()
        vn_objs = multi_vn_fixture.get_all_fixture_obj()
        (self.vn1_name, self.vn1_fix) = multi_vn_fixture._vn_fixtures[0]
        assert self.vn1_fix.verify_on_setup()
        fip_list = self.create_multiple_floatingip(
            inputs,
            connections,
            fip_count,
            self.vn1_fix)
        router_objs = self.create_multiple_router(connections, router_count)
        secgrp_objs = self.create_multiple_secgrp(connections, secgrp_count)
        sg_rule_objs = self.create_multiple_secgrp_rule(
            connections,
            secgrp_objs[
                :1],
            secgep_rule_count)
        port_objs = self.create_multiple_ports(
            connections, [
                self.vn1_fix], port_count)
        resource_dict['vn_fix'] = multi_vn_fixture
        resource_dict['sg_grps'] = secgrp_objs
        resource_dict['fips'] = fip_list
        resource_dict['routers'] = router_objs
        resource_dict['sg_rules'] = sg_rule_objs
        resource_dict['ports'] = port_objs

        return resource_dict

    def verify_quota_limit(self, inputs, connections, vn_fix, sg_obj):

        response_dict = {}
        vn1_name = get_random_name('vn_test_quota')
        vn1_obj = connections.quantum_fixture.create_network(vn1_name)
        if vn1_obj:
            self.addCleanup(
                connections.quantum_fixture.delete_vn,
                vn1_obj['id'])
        response_dict['network'] = vn1_obj
        subnet_cidr = get_random_cidr()
        subnet_rsp = connections.quantum_fixture.create_subnet(
            {'cidr': subnet_cidr}, vn_fix.vn_id)
        response_dict['subnet'] = subnet_rsp
        secgrp_obj = self.create_security_group(
            get_random_name('sec_grp'),
            connections.quantum_fixture)
        response_dict['secgrp'] = secgrp_obj
        router_obj = self.create_router(
            get_random_name('router'),
            connections.project_id)
        response_dict['router'] = router_obj
        sg_rule_obj = connections.quantum_fixture.create_security_group_rule(
            sg_obj['id'],
            protocol='tcp')
        response_dict['sg_rule'] = sg_rule_obj
        port_obj = connections.quantum_fixture.create_port(
            vn_fix.vn_id)
        response_dict['port'] = port_obj
        fip_obj = self.create_multiple_floatingip(
            inputs,
            connections,
            1,
            vn_fix)
        response_dict['fip'] = fip_obj

        return response_dict

    def create_multiple_vn(self, inputs, connections, vn_s, subnet_count=1):
        multi_vn_fixture = self.useFixture(MultipleVNFixture(
            connections=connections, inputs=inputs, subnet_count=subnet_count,
            vn_name_net=vn_s, project_name=self.inputs.project_name))
        return multi_vn_fixture

    def create_random_vn_list(self, count):
        vn_s = {}
        for i in range(count):
            vn_s[get_random_name('vn')] = [get_random_cidr()]
        return vn_s

    def create_multiple_router(self, connections, count=1):
        router_objs = []
        for i in range(count):
            router_obj = self.create_router(
                get_random_name('router'),
                connections.project_id)
            router_objs.append(router_obj)
        return router_objs

    def create_multiple_floatingip(
            self,
            inputs,
            connections,
            count,
            fvn_fixture):
        self.inputs = inputs
        self.connections = connections
        body = {'router:external': 'True'}
        net_dict = {'network': body}
        net_rsp = connections.quantum_fixture.update_network(
            fvn_fixture.vn_id,
            net_dict)
        assert net_rsp['network'][
            'router:external'] == True, 'Failed to update router:external to True'      
        self.fip_fixture = self.useFixture(
            FloatingIPFixture(
                project_name=self.inputs.project_name,
                inputs=self.inputs,
                connections=self.connections,
                pool_name='',
                vn_id=fvn_fixture.vn_id, option='neutron'))
        assert self.fip_fixture.verify_on_setup()
        if count == 1:
            fip_resp = connections.quantum_fixture.create_floatingip(
                fvn_fixture.vn_id,
                connections.project_id)
            if fip_resp:
                self.addCleanup(
                    self.fip_fixture.delete_floatingip,
                    fip_resp['floatingip']['id'])
        else:
            fip_resp = self.fip_fixture.create_floatingips(
                fvn_fixture.vn_id,
                count)
            self.addCleanup(self.fip_fixture.delete_floatingips, fip_resp)
        return fip_resp

    def create_multiple_secgrp(self, connections, count=1):
        secgrp_objs = []
        for i in range(count):
            secgrp_obj = self.create_security_group(
                get_random_name('sec_grp'),
                connections.quantum_fixture)
            secgrp_objs.append(secgrp_obj)
        return secgrp_objs

    def create_multiple_secgrp_rule(self, connections, sg_obj_list, count=1):
        proto_list = ['udp', 'tcp', 'icmp']
        sg_rule_objs = []
        for sg_obj in sg_obj_list:
            for i in range(count):
                sg_rule_obj = connections.quantum_fixture.create_security_group_rule(
                    sg_obj['id'],
                    protocol=random.choice(proto_list))
                sg_rule_objs.append(sg_rule_obj)

        return sg_rule_objs

    def create_multiple_ports(self, connections, vn_fix_list, count=1):
        port_obj_list = []
        for vn_fix in vn_fix_list:
            for i in range(count):
                port_obj = connections.quantum_fixture.create_port(
                    vn_fix.vn_id)
                if port_obj:
                    self.addCleanup(
                        connections.quantum_fixture.delete_port,
                        port_obj['id'])
                port_obj_list.append(port_obj)
        return port_obj_list