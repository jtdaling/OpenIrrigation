import os
import time
import subprocess
import urllib

# check if the wlan is configured by checking if a SSID is configured
file = open("/etc/network/interfaces")
strings = file.read()
search_word = "ssid"
file.close()
if(search_word in strings):
	print("network configured")
	time.sleep(30)
	# test network connection and check if wunderground is available
	try :
	    stri = "http://api.wunderground.com"
	    data = urllib.urlopen(stri)
        print("Connected")
        text = open("internet.txt", "w")
	    text.write("internetok")
	    text.close()
	except:
	    print("not connected")
internet=open('/home/pi/internet.txt')
	    internetcheck = internet.read()
	    search_word = 'nointernet'
	    if(search_word in internetcheck):
	    	os.system('0> network.txt')
	    	os.system('cp /etc/network/interfaces.old /etc/network/interfaces')
	    	os.system('reboot')
	    else:
	    	text = open("internet.txt", "w")
	    	text.write("nointernet")
	    	text.close()
	    	exit()

else:
    print("network not configured")
    time.sleep(10)
    # create netwerk configuration page for index.html
    os.system('cp /var/www/html/networksetup.html /var/www/html/index.html')
    os.system('cp /etc/dnsmasq.conf.ap /etc/dnsmasq.conf')
    os.system('systemctl start dnsmasq hostapd dhcpcd')
    # wait untill the network details are entered
    while True:
    	print('waiting')
    	if os.path.getsize('/home/pi/network.txt') < 1:
    		print('.')
    		time.sleep(1)
    		True
    	else:
            print('Network configured')
            # create new index.html page
            os.system('cp /var/www/html/index.html.networkconfigured /var/www/html/index.html')
            # empty the network.txt page, write network settings to /etc/network/inferfaces
            file = open('/etc/network/interfaces',"w")
            file.write('# Include files from /etc/network/interfaces.d:\n')
            file.write('source-directory /etc/network/interfaces.d\n')
            file.write('\n')
            file.write('auto wlan0\n')
            # read the new settings from network.txt
            settings=open('/home/pi/network.txt')
            strings = settings.read()
            search_word = 'static'
            if(search_word in strings):
				file.write('iface wlan0 inet static\n')
				# read lines from network.txt
				#settings = ('/home/pi/network.txt','r')
				data=open('/home/pi/network.txt')
				lines=data.readlines()
				ip = lines[3]
				file.write('address ' +ip.strip()+ '\n')
				file.write('netmask 255.255.255.0\n')
				ipr = lines[4]
				network = ipr
				file.write('gateway ' +ipr+'\n')
				ssid = lines[1]
				file.write('wpa-ssid ' +ssid.strip()+'\n')
				password = lines[2]
				key="wpa_passphrase " "\""+ssid.strip()+"\""  " " "\""+password.strip()+"\""" |grep -E 'psk' |grep -v \"#psk\" |cut -d '=' -f 2"
				passkey = subprocess.check_output(key, shell=True)
				file.write('wpa-psk ' +passkey.strip()+'\n')
				file.write('\n')
				file.write('auto eth0\n')
				file.write('iface eth0 inet dhcp\n')
				file.close()
				time.sleep(1)
				os.system('systemctl disable dnsmasq')
				os.system('systemctl disable hostapd')
				os.system('systemctl disable dhcpcd')
				os.system('cp /etc/dnsmasq.conf.noap /etc/dnsmasq.conf')
				os.system('systemctl enable networking')
            time.sleep(1)
            os.system('0> network.txt')
            print('rebooting now')
            os.system('reboot')
            break
exit()


