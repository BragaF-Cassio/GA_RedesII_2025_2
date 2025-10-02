# Passos para a execução

## OPCIONAL: Executar uma VM com o mininet instalado
docker run -it --rm --privileged -e DISPLAY              -v /tmp/.X11-unix:/tmp/.X11-unix              -v /lib/modules:/lib/modules              iwaseyusuke/mininet

## Necessário para a instalação
sudo apt update
sudo apt install openvswitch-testcontroller
sudo apt install frr

### Adicionar ao PATH
sudo ln /usr/bin/ovs-testcontroller /usr/bin/controller

### Executar
./config_frr.sh
sudo python3 executa_topologia.py

## Passos adicionais
Para abrir em mais de um terminal:
- dump

No dump você pega o PID de cada VM, e para acessar o terminal separado, utilize:
- sudo mnexec -a [PID] bash
