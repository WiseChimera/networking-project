from mininet.net import Mininet
from mininet.node import Node
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class Router(Node):
    def config(self, **params):
        super().config(**params)
        self.cmd('sysctl -w net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl -w net.ipv4.ip_forward=0')
        super().terminate()


def create_topology():

    net = Mininet(
        controller=None,
        link=TCLink,
        autoSetMacs=True
    )

    info('*** Creating hosts and routers\n')

    h1 = net.addHost('h1', ip='10.0.1.2/24')
    h2 = net.addHost('h2', ip='10.0.4.2/24')

    r1 = net.addHost('r1', cls=Router)
    r2 = net.addHost('r2', cls=Router)


    info('*** Creating network links\n')

    net.addLink(h1, r1,
                intfName1='h1-eth0',
                intfName2='r1-eth0',
                bw=100, delay='1ms')

    net.addLink(r1, r2,
                intfName1='r1-eth1',
                intfName2='r2-eth0',
                bw=10, delay='20ms',
                max_queue_size=20)


    net.addLink(r2, h2,
                intfName1='r2-eth2',
                intfName2='h2-eth0',
                bw=100, delay='1ms')

    info('*** Starting network\n')

    net.start()

    info('*** Configuring IP addresses and routes\n')

    r1.setIP('10.0.12.1/24', intf='r1-eth1')
    r2.setIP('10.0.12.2/24', intf='r2-eth0')

    r1.setIP('10.0.13.1/24', intf='r1-eth2')
    r2.setIP('10.0.32.2/24', intf='r2-eth1')

    r1.setIP('10.0.1.1/24', intf='r1-eth0')
    r2.setIP('10.0.4.1/24', intf='r2-eth2')

    h1.cmd('ip route add default via 10.0.1.1')
    h2.cmd('ip route add default via 10.0.4.1')

    info('*** Starting topology CLI\n')

    CLI(net)

    info('*** Stopping network\n')

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    create_topology()

