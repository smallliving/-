import queue
import requests
import threading
import time
import sys

que = '\033[94m[*]\033[0m'
bad = '\033[91m[-]\033[0m'
good = '\033[32m[+]\033[0m'

#定义目录爆破函数
def get_url(path_queue,size):
    while not path_queue.empty():
        try:
            url=path_queue.get()
            r=requests.get(url)
            if size in r.content:
                pass
            else:
                print("%s " % good +"[{}] => {}".format(r.status_code,url))
        except:
            pass


def main():
    url = input("%s 请输入要爆破的url： " % que)
    size = input("%s 请输入异常所包含的关键字： " % que)
    threadNum=int(input("%s 请输入进程：" % que))
    files=""
    language=input("%s 请输入脚本语言(php/jsp/asp/aspx/dir)：" %que)
    if language == "php":
        files="./files/PHP.txt"
    elif language == "jsp":
        files="./files/JSP.txt"
    elif language == "asp":
        files="./files/ASP.txt"
    elif language == "aspx":
        files="./files/ASPX.txt"
    elif language == "dir":
        files="./files/dir.txt"
    else:
        print("%s 输入有误，请重新输入" % bad)
        sys.exit()
    start = time.time()
    #以队列的形式获取要爆破的路径
    path_queue=get_path(url,files)

    #利用多线程爆破
    threads=[]
    for i in range(threadNum):
        t=threading.Thread(target=get_url,args=(path_queue,size))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    end = time.time()
    print("%s 总共耗时 %.2f s" % (good,(end - start)))

#路径获取函数
def get_path(url,files):
    path_queue=queue.Queue()
    f=open(files,"r",encoding='utf-8')
    for i in f.readlines():
        path=url+i.strip()
        path_queue.put(path)
    f.close()
    return path_queue

if __name__ == '__main__':
    main()
