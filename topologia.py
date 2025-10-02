from mininet.topo import Topo
from mininet.link import TCLink, Link
from mininet.link import TCIntf
from mininet.net import Mininet
from mininet.node import Host
from mininet.node import Node

class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)

    def terminate(self):
        super(LinuxRouter, self).terminate()

class MyTopo(Topo):
    def build(self):
        # Adiciona hosts (clientes)
        h1 = self.addHost('h1', ip='192.168.10.2/24', defaultRoute='via 192.168.10.1')
        h2 = self.addHost('h2', ip='192.168.20.2/24', defaultRoute='via 192.168.20.1')

        # Adiciona 5 roteadores
        A = self.addHost('A', cls=LinuxRouter)
        B = self.addHost('B', cls=LinuxRouter)
        C = self.addHost('C', cls=LinuxRouter)
        D = self.addHost('D', cls=LinuxRouter)
        E = self.addHost('E', cls=LinuxRouter)

        self.addLink(h1, A)
        self.addLink(h2, E)

        # Conecta os roteadores entre si
        self.addLink(A, B)
        self.addLink(A, C)

        self.addLink(B, D)
        self.addLink(B, E)

        self.addLink(C, D)
        self.addLink(D, E)

# Register topology
topos = {
    'topologia': (lambda: MyTopo())
}
