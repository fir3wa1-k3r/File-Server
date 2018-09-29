import socket
import os
import subprocess

#ip = "127.0.0.1"
port = 3333

def service(conn):
    conn.send(b'Thank you for connecting\n')
    conn.send(b'Available commands:\n')
    conn.send(b'LIST GET EXIT\n')
    conn.send(b'-----------------------------\n')
    conn.send(b'usage for GET command: GET <filename>\n')
    choice = b''
    choice = conn.recv(1024)
    string_data = choice.decode('utf-8')
    while True:
        if("EXIT" in choice.decode('utf-8').upper()):
            conn.send(b'Thanks for connecting...!!!')
            conn.close()
            exit(0)
        elif("LIST" in choice.decode('utf-8').upper()):
            #conn.send(b'You are using LIST\n')
            command = 'ls -la'
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            conn.send(p.stdout.read())
            choice = conn.recv(1024)
        else:
            #conn.send(b'You are using GET\n')
            command = choice.decode('utf-8')
            filename = command[4:].strip()
            path = ('/tmp/ftp/'+filename).strip()
            #fh = open(path,'r')
            try:
                fh = open(path,'r')
                conn.send(fh.read().encode())
            except FileNotFoundError:
                conn.send(b'File not found..!!!!\n')
            choice = conn.recv(1024)
            
def setup():
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("[+]SETTING UP THE SOCKETS")
    except:
        print("[!]SOCKET ERROR..!! PLEASE TRY AGAIN")
    sock.bind(('',port))
    print("[+]SOCKET BINDED TO PORT "+str(port))
    sock.listen(1)   #Accepts only 1 connection request, Change it to accept more connections
    print("[+]LISTENING FOR INCOMING REQUESTS")
    while True:
        conn, addr = sock.accept()
        print("[+]INCOMING CONNECTION FROM "+ str(addr[0]) + ":" + str(addr[1]))
        service(conn)

        
def main():
    setup()

main()
