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
            resp=requests.get(url,headers=headers,timeout=10)
            resp.raise_for_status()
            data=resp.json()
            if data["code"]==0:
                return data["data"]
            elif data["code"]==-352:
                print(f"error on the entrance No.{series}:{data['message']}")
                time.sleep(random.uniform(60,100))
            else:
                print(f"error on the entrance No.{series}:{data['message']}")
                return None
        except Exception as e:
            print(f"failed on request No.{i+1} in series No.{series}:{str(e)}")
            time.sleep(random.uniform(6,10))
    return None
def main():
 #   testda=crawl(200)
 #   if testda:
    start=1
    end=381
    count=0
    for num in range(start,end+1):
        filepath=f"bilibili_weekly/weekly_{num}.json"
        if os.path.exists(filepath):
            print(f"series No.{num} exists,skip")
            count+=1
            continue
        weekda=crawl(num)
        if weekda:
            with open(f"bilibili_weekly/weekly_{num}.json","w",encoding="utf-8") as f:
                json.dump(weekda,f,ensure_ascii=False,indent=2)
                print(f"Series No.{num} finish crawling successfully.")
                count+=1
            time.sleep(random.uniform(10,15))
    print("All data collection Accepted.")
    input("press enter to continue...")
  #     else:
  #         print("failed to crawl,add login situation")
  #         input("press enter to continue")
    if int(count)!=381:
        main()
if __name__=="__main__":
    main()
#1:352(请求非法-Too many cookie cause URL):20（buvid3）
#2:ac(成功爬虫获取数据):2 352:18（请求非法-Too frequent）
#3:ac:16 352:4（almost accepted,try again）
#4:wa(Error):20（Disturbed by test data）
#5:ac:15 352:5（请求非法-Too frequent that cause control）
#6:ac:20（Successful temporarily）
#7:database change-ac:26 352:355（请求非法-Too large amount）
#8:ac:322 352:12 skip（文件已存在跳过）:47
#9:ac:12 skip:368 NaN:1(Data No.105 Not Found)
#10:352:1 skip:380
#11:skip:380 NaN:1（Data No.105 Not Found）
    #(2026.7.11 series)
