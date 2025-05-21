
import logging
import time
from mininet.log import setLogLevel, info
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from emuvim.dcemulator.net import DCNetwork
from emuvim.api.rest.rest_api_endpoint import RestApiEndpoint
from emuvim.api.openstack.openstack_api_endpoint import OpenstackApiEndpoint

from env_config import ENV_CONFIG

logging.basicConfig(level=logging.INFO)
setLogLevel('info')  # set Mininet loglevel
logging.getLogger('werkzeug').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.base').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.compute').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.keystone').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.nova').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.neutron').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.heat').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.heat.parser').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.glance').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.helper').setLevel(logging.DEBUG)


def create_topology():
    net = DCNetwork(monitor=False, enable_learning=True)

    dc1 = net.addDatacenter("dc1")
    # add OpenStack-like APIs to the emulated DC
    api1 = OpenstackApiEndpoint("0.0.0.0", 6001)
    api1.connect_datacenter(dc1)
    api1.start()
    api1.connect_dc_network(net)
    # add the command line interface endpoint to the emulated DC (REST API)
    rapi1 = RestApiEndpoint("0.0.0.0", 5001)
    rapi1.connectDCNetwork(net)
    rapi1.connectDatacenter(dc1)
    rapi1.start()

    # info('*** Adding Ryu controller\n')
    # net.addController('c0', controller= RemoteController, ip='127.0.0.1', port= 6633)

    info('*** Adding switches\n')
    s_zone1 = net.addSwitch('s_zone1')  # zone 1
    s_zone2 = net.addSwitch('s_zone2')  # zone 2   
    s_zone3 = net.addSwitch('s_zone3')  # zone 3
    s4 = net.addSwitch('s4') 
    s5 = net.addSwitch('s5') 

    info('*** Adding Docker containers\n')
    srv = net.addDocker('srv', ip=ENV_CONFIG["srv"]["LOCAL_IP"], dimage='sdci_server_v1', environment=ENV_CONFIG["srv"], tty=True, stdin_open=True, dcmd="/start_server.sh")
    gwi = net.addDocker('gwi', ip=ENV_CONFIG["gwi"]["LOCAL_IP"], dimage='sdci_gateway', environment=ENV_CONFIG["gwi"], dcmd="/start_gw.sh")
    gf1 = net.addDocker('gf1', ip=ENV_CONFIG["gf1"]["LOCAL_IP"], dimage='sdci_gateway', environment=ENV_CONFIG["gf1"], dcmd="/start_gw.sh")
    dev1 = net.addDocker('dev1', ip=ENV_CONFIG["dev1"]["LOCAL_IP"], dimage='sdci_device', environment=ENV_CONFIG["dev1"], dcmd="/start_dev.sh")
    gf2 = net.addDocker('gf2', ip=ENV_CONFIG["gf2"]["LOCAL_IP"], dimage='sdci_gateway', environment=ENV_CONFIG["gf2"], dcmd="/start_gw.sh")
    dev2 = net.addDocker('dev2', ip=ENV_CONFIG["dev2"]["LOCAL_IP"], dimage='sdci_device', environment=ENV_CONFIG["dev2"], dcmd="/start_dev.sh")
    gf3 = net.addDocker('gf3', ip=ENV_CONFIG["gf3"]["LOCAL_IP"], dimage='sdci_gateway', environment=ENV_CONFIG["gf3"], dcmd="/start_gw.sh")      
    dev3 = net.addDocker('dev3', ip=ENV_CONFIG["dev3"]["LOCAL_IP"], dimage='sdci_device', environment=ENV_CONFIG["dev3"], dcmd="/start_dev.sh")

    # Zone 1
    net.addLink(dev1, s_zone1, cls=TCLink)
    net.addLink(gf1, s_zone1, cls=TCLink)
    net.addLink(s_zone1, s4, cls=TCLink)
    # Zone 2
    net.addLink(dev2, s_zone2, cls=TCLink)
    net.addLink(gf2, s_zone2, cls=TCLink)
    net.addLink(s_zone2, s4, cls=TCLink)
    # Zone 3
    net.addLink(dev3, s_zone3, cls=TCLink)
    net.addLink(gf3, s_zone3, cls=TCLink)
    net.addLink(s_zone3, s4, cls=TCLink)
    # Coeur du reseau
    net.addLink(s4, s5, cls= TCLink)
    net.addLink(s5, dc1, cls= TCLink)

    net.addLink(gwi, s5, cls=TCLink)
    net.addLink(srv, s5, cls=TCLink)
    

    info('*** Starting network\n')
    net.start()
    info('*** Testing connectivity\n')
    net.ping([srv, dev1])
    net.ping([srv, dev2])
    net.ping([srv, dev3])
    info('*** Running CLI\n')
    CLI(net)
    info('*** Stopping network')
    net.stop()

def main():
    create_topology()


if __name__ == '__main__':
    main()