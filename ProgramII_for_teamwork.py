import os
import re
import glob
import json
import pandas as pd
basedir = os.path.dirname(os.path.abspath(__file__))
rawdir = os.path.join(basedir, "bilibili_weekly")#I的输出目录
proc_dir = os.path.join(basedir, "processed")
os.makedirs(proc_dir, exist_ok=True)
def load_raw():
    files = (glob.glob(os.path.join(rawdir, "weekly_*.json")) +
             glob.glob(os.path.join(rawdir, "weekly_*.txt")))
    if not files:
        raise FileNotFoundError(f"{rawdir}没找到 weekly_* 数据文件")
        input("press enter to continue...")
    records = []
    for fp in files:
        m = re.search(r"weekly_(\d+)", os.path.basename(fp))#期数
        number = int(m.group(1)) if m else -1
        try:
            data = json.load(open(fp, encoding="utf-8"))
        except Exception as e:
            print(f"[skip] {fp} 解析失败：{e}")
            continue
        video_list = data.get("list", []) if isinstance(data, dict) else []
        week_name = ""
        if isinstance(data.get("config"), dict):
            week_name = data["config"].get("name", "")
        for rank, v in enumerate(video_list, start=1):
            if not isinstance(v, dict):
                continue
            stat = v.get("stat", {}) or {}
            owner = v.get("owner", {}) or {}
            #rcmd_reason统一取文本
            rr = v.get("rcmd_reason")
            if isinstance(rr, dict):
                rcmd = rr.get("content", "")
            elif isinstance(rr, str):
                rcmd = rr
            else:
                rcmd = ""
            records.append({
                "weekly_number": number,#期数
                "weekly_name": week_name,#期名
                "rank_in_week": rank,#位次
                "bvid": v.get("bvid"),
                "title": v.get("title"),
                "tname": v.get("tname"),#分区
                "duration": v.get("duration"),#时长(秒)
                "pubdate": v.get("pubdate"),#发布时间戳
                "up_mid": owner.get("mid"),#id
                "up_name": owner.get("name"),#名
                "view": stat.get("view"),#播放量
                "danmaku": stat.get("danmaku"),#弹幕
                "reply": stat.get("reply"),#评论
                "favorite": stat.get("favorite"),#收藏
                "coin": stat.get("coin"),#投币
                "share": stat.get("share"),#分享
                "like": stat.get("like"),#点赞
                "his_rank": stat.get("his_rank"),#热榜排名
                "rcmd_reason": rcmd,#推荐语
            })
    df = pd.DataFrame(records)
    print(f"[read] 载入 {len(files)} 期，共 {len(df)} 条原视频记录")
    return df
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.strip()
    text = re.sub(r"[\x00-\x1f\x7f]", "", text)#去控制字符
    text = re.sub(r"\s+", " ", text)#合并空白
    return text
def clean_data(df):
    print(f"清洗前共{len(df)}记录")
    #选择
    keep = ["weekly_number", "weekly_name", "rank_in_week", "bvid", "title",
            "tname", "duration", "pubdate", "up_mid", "up_name",
            "view", "danmaku", "reply", "favorite", "coin", "share", "like",
            "his_rank", "rcmd_reason"]
    df = df[[c for c in keep if c in df.columns]].copy()
    print(f"留{df.shape[1]}个有价值字段")
    #修正
    for col in ["title", "up_name", "tname", "rcmd_reason", "weekly_name"]:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
    print("文本修正")
    #删除
    num_cols = ["view", "danmaku", "reply", "favorite", "coin", "share",
                "like", "duration", "his_rank"]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")#非法值转 NaN
    n0 = len(df)
    df = df.dropna(subset=["bvid", "view", "like"])#缺失
    n1 = len(df)
    df = df[df["view"] > 0]#非正
    n2 = len(df)
    df = df[df["duration"].fillna(0) >= 0]#非正
    n3 = len(df)
    df = df.drop_duplicates(subset=["bvid", "weekly_number"])#同期重复
    n4 = len(df)
    print(f"    关键字段缺失   删除 {n0 - n1} 条")
    print(f"    播放量<=0      删除 {n1 - n2} 条")
    print(f"    时长异常       删除 {n2 - n3} 条")
    print(f"    同期重复       删除 {n3 - n4} 条")
    print(f"    合计删除 {n0 - n4} 条，剩余 {n4} 条")
    #派生字段
    df["pubdate"] = pd.to_datetime(df["pubdate"], unit="s", errors="coerce")
    #互动热度=点赞+投币+收藏+分享+评论+弹幕
    df["interaction"] = (df["like"].fillna(0) + df["coin"].fillna(0) +
                         df["favorite"].fillna(0) + df["share"].fillna(0) +
                         df["reply"].fillna(0) + df["danmaku"].fillna(0))
    df["interaction_rate"] = (df["interaction"] / df["view"]).round(4)#互动率
    df["like_rate"] = (df["like"].fillna(0) / df["view"]).round(4)#点赞率
    df["coin_rate"] = (df["coin"].fillna(0) / df["view"]).round(4)#投币率
    df["duration_min"] = (df["duration"] / 60).round(2)#时长(分)
    #目标标签：0<his_rank<=10 记为进入热搜榜前十
    df["his_rank"] = df["his_rank"].fillna(0)
    df["top10"] = ((df["his_rank"] > 0) & (df["his_rank"] <= 10)).astype(int)
    print("派生字段")
    #保存
    path = os.path.join(proc_dir, "bili_clean.csv")
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"\n清洗后数据已保存至：{path}")
    return df
if __name__ == "__main__":
    raw = load_raw()
    clean = clean_data(raw)
    print("\n清洗后数据预览（部分）：")
    cols = ["weekly_number", "title", "up_name", "tname",
            "view", "like", "interaction", "top10"]
    print(clean[cols].head().to_string(index=False))
    print("\n字段与缺失情况：")
    print(clean.info())
