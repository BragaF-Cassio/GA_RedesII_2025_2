 #!/usr/bin/env python3
from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.topo import Topo

# Importa a topologia do arquivo
from topologia import MyTopo   # Arquivo deve conter a classe MyTopo

def run():
    net = Mininet(topo=MyTopo(), controller=Controller, link=TCLink, switch=OVSSwitch)
    net.start()

    # Get routers
    routers = [net.get('A'), net.get('B'), net.get('C'), net.get('D'), net.get('E')]

    A = net.get('A')
    A.intf('A-eth0').setIP('192.168.10.1/24')
    A.intf('A-eth1').setIP('192.168.0.1/24')
    A.intf('A-eth2').setIP('192.168.1.1/24')

    B = net.get('B')
    B.intf('B-eth0').setIP('192.168.0.2/24')
    B.intf('B-eth1').setIP('192.168.3.1/24')
    B.intf('B-eth2').setIP('192.168.4.1/24')

    C = net.get('C')
    C.intf('C-eth0').setIP('192.168.1.2/24')
    C.intf('C-eth1').setIP('192.168.2.1/24')

    D = net.get('D')
    D.intf('D-eth1').setIP('192.168.2.2/24')
    D.intf('D-eth0').setIP('192.168.3.2/24')
    D.intf('D-eth2').setIP('192.168.5.1/24')

    E = net.get('E')
    E.intf('E-eth0').setIP('192.168.20.1/24')
    E.intf('E-eth1').setIP('192.168.4.2/24')
    E.intf('E-eth2').setIP('192.168.5.2/24')

    # Executa o algoritmo de roteamento em cada roteador
    for r in routers:
        info(f"*** Executando codigo de roteamento no roteador {r.name}\n")
        info(r.cmd(f"/usr/lib/frr/frrinit.sh start '{r.name}'"))
        #r.cmd('python3 ./roteamento.py &')

    # Mantem o minitet CLI aberto para testes
    from mininet.cli import CLI
    CLI(net)

    for r in routers:
        info(f"*** Finalizando codigo de roteamento no roteador {r.name}\n")
        info(r.cmd(f"/usr/lib/frr/frrinit.sh stop '{r.name}'"))

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
