docker run -it --rm --privileged -e DISPLAY              -v /tmp/.X11-unix:/tmp/.X11-unix              -v /lib/modules:/lib/modules              iwaseyusuke/mininet

sudo apt update
sudo apt install openvswitch-testcontroller
sudo apt install frr

sudo ln /usr/bin/ovs-testcontroller /usr/bin/controller

sudo python3 executa_topologia.py


Para abrir em mais de um terminal:
dump
sudo mnexec -a [PID] bash
