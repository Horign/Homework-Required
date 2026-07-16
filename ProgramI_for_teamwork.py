import requests
import json
import time
import random
import os
from fake_useragent import UserAgent as ua
buvid3="71A877BB-A716-2ED9-2FD4-D288B666D72249754infoc"
if not os.path.exists("bilibili_weekly"):
    os.makedirs("bilibili_weekly")
def crawl(series):
    url=f"https://api.bilibili.com/x/web-interface/popular/series/one?number={series}"
    headers={
        "referer":"https://www.bilibili.com/v/popular/weekly",
        "user-agent":ua().random,
        "origin":"https://m.bilibili.com",
        "accept":"application/json,text/plain,*/*",
        "acceptLanguage":"zh-CN,zh;q=0.9",
        "cookie":f"buvid3={buvid3};"
    }
    maxretry=3
    for i in range(maxretry):
        try:
            resp=requests.get(url,headers=headers,timeout=15)
            resp.raise_for_status()
            data=resp.json()
            if data["code"]==0:
                return data["data"]
            elif data["code"]==-352:
                print(f"series No.{series} in risk-control,please wait.")
                time.sleep(random.uniform(60,120))
            else:
                print(f"第{series}期请求出错：{data['message']}")
                return None
        except Exception as e:
            print(f"第{series}期第{i+1}次请求失败：{str(e)}")
            time.sleep(random.uniform(8,12))
    return None
def main():
    start=1
    end=381
    success=0
    fail=0
    for num in range(start,end+1):
        filepath=f"bilibili_weekly/weekly_{num}.json"
        if os.path.exists(filepath):
            print(f"{num} exist,skip")
            success+=1
            continue
        weekda=crawl(num)
        if weekda:
            with open(f"bilibili_weekly/weekly_{num}.json","w",encoding="utf-8") as f:
                json.dump(weekda,f,ensure_ascii=False,indent=2)
                print(f"finish No.{num}")
                success+=1
            time.sleep(random.uniform(12,18))
        else:
            print(f"fail No.{num}")
            fail+=1
    print(f"\nsuccess:{success},fail:{fail}")
    file_count = len([f for f in os.listdir("bilibili_weekly") if f.startswith("weekly_")])
    print(f"{file_count} files now")
    input("press enter to continue...")
    if fail > 0:
        print("run again")
        main()

if __name__=="__main__":
    main()
#1
    #(2026.7.15series)
#更新记录：
    #拉长全量跑的时候间隔
    #完善文件完整度检查
