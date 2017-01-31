sudo ifdown wlan0
sudo /usr/sbin/hostapd /etc/hostapd/hostapd.conf -B
sudo python robot/testmotor.py

