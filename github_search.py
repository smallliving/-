import requests
import json
def main():
    key=input("[*] 请输入要github搜索的关键词：")
    token='54164d17051cdc5861981b483c4558aef69abefd'
    url="https://api.github.com/search/code?q=%s" % key
    headers={"Authorization":"token %s" % token}
    params={"per_page" : 10 , "page" : 0}
    r=requests.get(url,headers=headers,params=params)
    d=r.json()
    print (json.dumps(d,indent=4))
if __name__ == '__main__':
    main()