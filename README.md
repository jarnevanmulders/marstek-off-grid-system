# Marstek Off-grid System Firmware (Based on LibreVNA hardware)

### 0️⃣ Boot without USB-C adapter PSU
This configuration change is necessary because the Raspberry Pi 5 has a higher power requirement, and setting PSU_MAX_CURRENT=5000 ensures that the Pi recognizes that the connected power supply can deliver up to 5A. This can help resolve issues where the Pi fails to boot properly due to insufficient power, especially when using power-hungry USB devices or when booting from USB. Do the following:
- `sudo rpi-eeprom-config --edit`
- Add the following line --> `PSU_MAX_CURRENT=5000`

### 1️⃣ Enable DHCP server
- `sudo apt update`
- `sudo apt install dnsmasq`
- `sudo nano /etc/dnsmasq.conf`

interface=eth0
dhcp-range=192.168.10.50,192.168.10.150,255.255.255.0,24h

- `systemctl status NetworkManager`
- `nmcli con show`
- `sudo nmcli con mod "netplan-eth0" ipv4.addresses 192.168.10.1/24`
- `sudo nmcli con mod "netplan-eth0" ipv4.method manual`
- `sudo nmcli con mod "netplan-eth0" ipv6.method ignore`
- `sudo nmcli con up "netplan-eth0"`
- `ip a show eth0`
- `ifconfig`
- `arp -a`



### 2️⃣ Create SSH Key to clone this repository
- On the raspberry pi
	```
	ssh-keygen -t ed25519 -C "jarne.vanmulders@kuleuven.be"
	cat ~/.ssh/id_ed25519.pub
	```
- ENTER 3x
- Add key to github account [online] --> settings --> SSH Key
- Clone repo via SSH

### 3️⃣ Get custom firmware ready
1. Install git
	```
	sudo apt update
	sudo apt install git -y
	```
2. Git clone via SSH KEY on rpi in home dir: `git clone git@github.com:jarnevanmulders/marstek-off-grid-system.git`

### 4️⃣ 

### 5️⃣ Connection with temperature sensors DS18B20
1. Connect D to GPIO4
2. Enable w1-gpio: add `dtoverlay=w1-gpio` with `sudo nano /boot/firmware/config.txt`
3. Reboot `sudo reboot`
4. Activate and test onewire:
	``` 
	sudo modprobe w1-gpio
	sudo modprobe w1-therm
	cd /sys/bus/w1/devices
	ls
	``` 
	If you see the sensor's ID as dir here, all is well. 

### 6️⃣ Install required python packages
Install pip `sudo apt install python3-pip`
```
sudo python3 -m pip install pyyaml --break-system-packages
sudo python3 -m pip install filelock --break-system-packages
sudo python3 -m pip install influxdb_client --break-system-packages
sudo python3 -m pip install flask --break-system-packages
sudo python3 -m pip install psutil --break-system-packages
``` 

### 7️⃣ Test all individual scripts
1. Test `system.py`
2. Test `librevna.py`
3. Test `controller.py`
4. Test `app.py`
5. Run services
	1. Copy service files to systemd:
	```
	sudo cp ~/Radar-LibreVNA-Firmware/app.service /lib/systemd/system/
	sudo cp ~/Radar-LibreVNA-Firmware/controller.service /lib/systemd/system/
 	```
 	2. Enable and start services
  	```
	sudo systemctl enable app.service
   	sudo systemctl enable controller.service
   	sudo systemctl start app.service
   	sudo systemctl start controller.service
  	```   

### 8️⃣ Test system data script
1. Download following packages
	`sudo python3 -m pip install psutil --break-system-packages`
2. Test `system.py`

### 9️⃣ Other features
1. Tailscale
	```
	curl -fsSL https://tailscale.com/install.sh | sh
	sudo apt update
	sudo apt install tailscale
	sudo tailscale up
	```
3. Samba (For debugging)
	1. Change <<<PASSWORD>>> and execute following commands
	   ```
	   curl -sSL https://get.docker.com | sh
	   sudo docker run -itd --name samba --restart=unless-stopped -p 139:139 -p 445:445 -v /home/pi:/mount dperson/samba -u "pi;<<<PASSWORD>>>" -s "pi;/mount;yes;no;no;pi"
	   sudo chmod 755 /home/pi
	   sudo chown pi:pi /home/pi
	   ```
    	2. Map network drive \\\IP_ADDRESS\pi and fill in credentials
