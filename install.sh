#!/bin/bash
apt-get install apache2
apt install dnsmasq hostapd

pip3 install -r requirements.txt			# install depencies
mkdir temp
cd temp
git clone https://github.com/r4ma050/wireless.git
cd wireless
cp Wireless.py /usr/local/lib/python3.5/dist-packages/wireless
cd ..

git clone https://github.com/prasathmani/tinyfilemanager.git
mkdir /var/www/html
cd tinyfilemanager
cp tinyfilemanager.php /var/www/html/index.php
cp translation.php /var/www/html
mkdir /shared
chmod -R 777 /shared
sed -i 's/$root_path = '';/$root_path = '\/shared';/g' /var/www/html/index.html

systemctl disable hostapd
systemctl disable apache2

systemctl stop dnsmasq
systemctl stop hostapd

cp /etc/dhcpcd.conf /etc/dhcpcd.conf.bak
cp /etc/dhcpcd.conf /etc/dhcpcd.conf.desactivate
echo 'interface wlan0' >> /etc/dhcpcd.conf
echo 'static ip_address=192.168.100.1/24' >> /etc/dhcpcd.conf
echo 'nohook wpa_supplicant' >> /etc/dhcpcd.conf
cp /etc/dhcpcd.conf /etc/dhcpcd.conf.activate
cp /etc/dhcpcd.bak /etc/dhcpcd.conf

mv /etc/dnsmasq.conf /etc/dnsmasq.conf.bak
nano /etc/dnsmasq.conf
echo 'interface=wlan0' >> /etc/dnsmasq.conf
echo 'dhcp-range=192.168.100.2,192.168.100.254,255.255.255.0,24h' >> /etc/dnsmasq.conf

echo 'interface=wlan0' >> /etc/hostapd/hostapd.conf
echo 'driver=nl80211' >> /etc/hostapd/hostapd.conf
echo 'ssid=SecretHat' >> /etc/hostapd/hostapd.conf
echo 'hw_mode=g' >> /etc/hostapd/hostapd.conf
echo 'channel=7' >> /etc/hostapd/hostapd.conf
echo 'wmm_enabled=0' >> /etc/hostapd/hostapd.conf
echo 'macaddr_acl=0' >> /etc/hostapd/hostapd.conf
echo 'auth_algs=1' >> /etc/hostapd/hostapd.conf
echo 'ignore_broadcast_ssid=0' >> /etc/hostapd/hostapd.conf
echo 'wpa=2' >> /etc/hostapd/hostapd.conf
echo 'wpa_passphrase=SecretHat' >> /etc/hostapd/hostapd.conf
echo 'wpa_key_mgmt=WPA-PSK' >> /etc/hostapd/hostapd.conf
echo 'wpa_pairwise=TKIP' >> /etc/hostapd/hostapd.conf
echo 'rsn_pairwise=CCMP' >> /etc/hostapd/hostapd.conf
sed -i 's/#DAEMON_CONF/DAEMON_CONF="\/etc\/hostapd\/hostapd.conf"/g' /etc/default/hostapd

sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/g' /etc/default/hostapd
iptables -t nat -A  POSTROUTING -o eth0 -j MASQUERADE
sh -c "iptables-save > /etc/iptables.ipv4.nat"

echo 'iptables-restore < /etc/iptables.ipv4.nat' >> /etc/rc.local

sudo systemctl unmask hostapd
sudo systemctl enable hostapd
#sudo systemctl start hostapd
sudo reboot

echo Please install Dataplicy for the backdoor : https://www.dataplicity.com/
