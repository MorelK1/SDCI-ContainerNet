from mininet.net import Containernet
from mininet.node import Controller, Docker
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import time

def run():
    setLogLevel('info')
    net = Containernet(controller= Controller)

    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding switches\n')
    s_zone1 = net.addSwitch('s_zone1') #zone 1
    s_zone2 = net.addSwitch('s_zone2') #zone 2
    s_zone3 = net.addSwitch('s_zone3') #zone 3
    s0 = net.addSwitch('s0') # interconnexion vers GI et Server

    info('*** Adding Docker containers\n')
    server = net.addDocker('srv', ip='10.0.0.1', dimage='server')
    gwi = net.addDocker('gwi', ip='10.0.0.2', dimage='gateway', ports=[8181], port_bindings={8181:8181})
    gf1 = net.addDocker('gf1', ip='10.0.0.3', dimage='gateway')
    dev1 = net.addDocker('dev1', ip='10.0.0.4', dimage='device')
    gf2 = net.addDocker('gf2', ip='10.0.0.5', dimage='gateway')
    dev2 = net.addDocker('dev2', ip='10.0.0.6', dimage='device')
    gf3 = net.addDocker('gf3', ip='10.0.0.7', dimage='gateway')
    dev3 = net.addDocker('dev3', ip='10.0.0.8', dimage='device')
    
    gi2 = net.addDocker('gi2', ip='10.0.0.12', dimage='gateway')

    info('*** Creating links with latency\n')
    # Zone 1
    net.addLink(dev1, s_zone1, cls=TCLink, delay='5ms')
    net.addLink(gf1, s_zone1, cls=TCLink, delay='2ms')
    net.addLink(s_zone1, s0, cls=TCLink, delay='1ms')
    # Zone 2
    net.addLink(dev2, s_zone2, cls=TCLink, delay='5ms')
    net.addLink(gf2, s_zone2, cls=TCLink, delay='2ms')
    net.addLink(s_zone2, s0, cls=TCLink, delay='1ms')
    # Zone 3
    net.addLink(dev3, s_zone3, cls=TCLink, delay='5ms')
    net.addLink(gf3, s_zone3, cls=TCLink, delay='2ms')
    net.addLink(s_zone3, s0, cls=TCLink, delay='1ms')
    # Coeur du reseau
    net.addLink(gi2, s0, cls= TCLink, delay='2ms')
    net.addLink(gwi, s0, clSs=TCLink, delay='2ms')
    net.addLink(server, s0, cls=TCLink, delay='1ms')

    info('*** Starting network\n')
    net.start()

    info('*** Lauching process inside container\n')
    server.cmd('node server.js --local_ip 10.0.0.1 --local_port 8080 --local_name srv &')
    gwi.cmd('node gateway.js --local_ip 10.0.0.2 --local_port 8181 --local_name gwi --remote_ip 10.0.0.1 --remote_port 8080 --remote_name srv &')
    gf1.cmd('node gateway.js --local_ip 10.0.0.3 --local_port 8281 --local_name gf1 --remote_ip 10.0.0.2 --remote_port 8181 --remote_name gwi &')
    dev1.cmd('node device.js --local_ip 10.0.0.4 --local_port 9001 --local_name dev1 --remote_ip 10.0.0.3 --remote_port 8281 --remote_name gf1 --send_period 100 &')
    gf2.cmd('node gateway.js --local_ip 10.0.0.5 --local_port 8282 --local_name gf2 --remote_ip 10.0.0.2 --remote_port 8181 --remote_name gwi &')
    dev2.cmd('node device.js --local_ip 10.0.0.6 --local_port 9002 --local_name dev2 --remote_ip 10.0.0.5 --remote_port 8282 --remote_name gf2 --send_period 3000 &')
    gf3.cmd('node gateway.js --local_ip 10.0.0.7 --local_port 8283 --local_name gf3 --remote_ip 10.0.0.2 --remote_port 8181 --remote_name gwi &')
    dev3.cmd('node device.js --local_ip 10.0.0.8 --local_port 9003 --local_name dev3 --remote_ip 10.0.0.7 --remote_port 8283 --remote_name gf3 --send_period 3000 &')

    info('*** Waiting and testing connectivity\n')
    time.sleep(5)
    net.pingAll()

    CLI(net)
    net.stop()

if __name__ == '__main__':
    run()