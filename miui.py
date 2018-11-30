# -*- coding:utf-8 -*-
import urllib.request
import urllib
import urllib.parse
import re,time,random,json
import sys 
from io import BytesIO
import gzip

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

cookie=''  #add cookie

def reply(purl,ptext,fh):
    url = purl
    postdata = {
        'message':ptext,
        'posttime':time.time(),
        'formhash':fh,
        'usesig':'1',
        'subject':'',
    }
    postdata = urllib.parse.urlencode(postdata).encode('utf-8')

    req = urllib.request.Request(url, headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':cookie,
        'DNT':'1',
        'Host':'www.miui.com',
        'Referer':'http://www.miui.com/gid-14.html',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        
    },data = postdata,
    )

    with urllib.request.urlopen(req,timeout=3000) as oper:
        data = oper.read()
    print(data.decode("utf-8").split(',')[1].split("'")[1]);
    m = re.findall('回复发布成功', data.decode('utf-8'))
    if m==[]:
        raise RuntimeError('回复失败')

def gethtml(url):
    req = urllib.request.Request(url, headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':cookie,
        'DNT':'1',
        'Host':'www.miui.com',
        'Referer':'http://www.miui.com/forum-775-1.html',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        
    })
    with urllib.request.urlopen(req,timeout=3000) as oper:
        data = oper.read()
    return(data.decode("utf-8").translate(non_bmp_map))

def main():

    listurl="http://www.miui.com/forum-775-"+str(random.randint(2, 11))+".html"
    print(listurl)
    listhtml=(gethtml(listurl))
    m = re.findall('<a href="thread-(\d{7,9})-\d-\d\.html" class="xi2">\d\d+</a>', listhtml)
    
    tid=m[random.randint(0, len(m)-1)]
    turl='http://www.miui.com/'+'thread-'+str(tid)+'-1-1.html'
    print('\\__' + turl + '\n')
    thtml=(gethtml(turl))
    
    m = re.findall('<meta name="description" content="(.*?)"', thtml)
    print(m[0])

    # tuling123.com 注册, 申请 api_key
    ptext=gethtml('http://www.tuling123.com/openapi/api?key=[api_key]&info='+urllib.parse.quote(m[0]))
    ptext=json.loads(ptext)['text'] + '\n    --Powered by tuling robot'
    print('\\__' + ptext + '\n')

    m = re.findall('<input type="hidden" name="formhash" value="(.*?)" />', thtml)
    fh=m[0]+':'+m[0][::-1]
    purl="http://www.miui.com/forum.php?mod=post&action=reply&fid=5&tid="+str(tid)+"&extra=page%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1"
    reply(purl,ptext,fh)

if __name__ == "__main__":
    t=0
    wait=161
    errmax=50
    err=0
    
    while(t<50):
        try:
            tm=0
            print('本次已回帖数: ' + str(t) + '\n')
            main()
            t=t+1
            err=0
        except Exception as e:
            print(e)
            tm=int(wait*9/10)+err
            err=err+1

        if(err>errmax):
            raise RuntimeError("错误过多，请稍后再试")

        print('冷却中......')
        while(tm<wait):
            time.sleep(1)
            tm=tm+1
