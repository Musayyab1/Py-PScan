
# Port Scanning using Multi-threading
# Unnecessarily open ports = potential security gaps. Only scan stuff if allowed to.

# Try to connect to each port using sockets. If connects, it's open. If not, then either closed or ignoring


import socket
import threading
from queue import Queue 
from tqdm import tqdm #for progress bar


target = "127.0.0.1" #set target ip to scan
port_list = range(6900, 8500) # Set Range of ports to scan here
threads = 100 #set number of threads

# Queue to store ports and a list to keep track of open ports
queue = Queue()
open_ports = []


def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #creating socket, firstParam-InternetSocket IPv4 , secondParam-TCP
        sock.connect((target, port)) 
        sock.close()
        return True
    
    except:
        return False

'''    
without threading sequentially scan, checks each port one by one, slow for large port ranges
for ports in range(1, 500):
    result = portscan(ports)
    if result:
        print("Port {} is open!".format(ports))
    else:
        print("{} port is not open.".format(ports))
'''

# Add each port to the queue for threads to process
def fill_queue(port_list):
    for port in port_list:
        queue.put(port)


fill_queue(port_list)  # Fill the queue with ports to scan

thread_list = []  # Store thread objects so can be started later

progress_bar = tqdm(total=len(port_list), desc="Scanning Ports... ", ncols=100)  # Progress bar with number of ports to scan


def worker(progress_bar):
    while not queue.empty():  
        port = queue.get()   #queue.get() automatically locks for thread safety, so multiple threads can safely pull ports one by one without race conditions.
        if portscan(port):
            print("Port {} is open!".format(port))
            open_ports.append(port)  
        progress_bar.update(1)  




for t in range(threads):     
    thread = threading.Thread(target=worker, args=(progress_bar,))    # Each thread runs the worker() function
    thread_list.append(thread)  # Save thread for later

for thread in thread_list: # Threads race to pull ports from the queue and scan them.
    thread.start()              # Start each

for thread in thread_list:
    thread.join()     #Waits / Blocks main thread until the worker thread completes / finishes

progress_bar.close()

print("opne ports are ", open_ports)

