import os
import re
import glob
import json
import pandas as pd
from datetime import datetime
basedir = os.path.dirname(os.path.abspath(__file__))
rawdir = os.path.join(basedir, "bilibili_weekly")
proc_dir = os.path.join(basedir, "processed")
os.makedirs(proc_dir, exist_ok=True)
base_date = datetime(2026, 7, 15)
def load_raw():
    files = (glob.glob(os.path.join(rawdir, "weekly_*.json")) +
             glob.glob(os.path.join(rawdir, "weekly_*.txt")))
    if not files:
        raise FileNotFoundError(f"{rawdir}里没找到weekly开头的数据文件")
        input("按回车继续...")
    records = []
    for fp in files:
        m = re.search(r"weekly_(\d+)", os.path.basename(fp))
        number = int(m.group(1)) if m else -1
        try:
            data = json.load(open(fp, encoding="utf-8"))
        except Exception as e:
            print(f"[跳过] {fp} 解析失败：{e}")
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
            rr = v.get("rcmd_reason")
            if isinstance(rr, dict):
                rcmd = rr.get("content", "")
            elif isinstance(rr, str):
                rcmd = rr
            else:
                rcmd = ""
            records.append({
                "weekly_number": number,
                "weekly_name": week_name,
                "rank_in_week": rank,
                "bvid": v.get("bvid"),
                "title": v.get("title"),
                "tname": v.get("tname"),
                "duration": v.get("duration"),
                "pubdate": v.get("pubdate"),
                "up_mid": owner.get("mid"),
                "up_name": owner.get("name"),
                "view": stat.get("view"),
                "danmaku": stat.get("danmaku"),
                "reply": stat.get("reply"),
                "favorite": stat.get("favorite"),
                "coin": stat.get("coin"),
                "share": stat.get("share"),
                "like": stat.get("like"),
                "his_rank": stat.get("his_rank"),
                "rcmd_reason": rcmd,
            })
    df = pd.DataFrame(records)
    print(f"[读取] 载入{len(files)}期，共{len(df)}条视频记录")
    return df
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.strip()
    text = re.sub(r"[\x00-\x1f\x7f]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text
def clean_data(df):
    print(f"清洗前共{len(df)}条记录")
    keep = ["weekly_number", "weekly_name", "rank_in_week", "bvid", "title",
            "tname", "duration", "pubdate", "up_mid", "up_name",
            "view", "danmaku", "reply", "favorite", "coin", "share", "like",
            "his_rank", "rcmd_reason"]
    df = df[[c for c in keep if c in df.columns]].copy()
    print(f"保留{df.shape[1]}个字段")
    for col in ["title", "up_name", "tname", "rcmd_reason", "weekly_name"]:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
    print("文本字段清洗完成")
    num_cols = ["view", "danmaku", "reply", "favorite", "coin", "share",
                "like", "duration", "his_rank"]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    n0 = len(df)
    df = df.dropna(subset=["bvid", "view", "like"])
    n1 = len(df)
    df = df[df["view"] > 0]
    n2 = len(df)
    df = df[df["duration"].fillna(0) >= 0]
    n3 = len(df)
    df = df.drop_duplicates(subset=["bvid", "weekly_number"])
    n4 = len(df)
    print(f"    关键字段缺失   删除{n0 - n1}条")
    print(f"    播放量<=0      删除{n1 - n2}条")
    print(f"    时长异常       删除{n2 - n3}条")
    print(f"    同期重复       删除{n3 - n4}条")
    # 四分位法剔异常值，极端值太影响相关性结果
    iqr_cols = ["view", "like", "coin", "favorite", "share", "reply", "danmaku"]
    for col in iqr_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        df = df[(df[col] >= Q1 - 1.5*IQR) & (df[col] <= Q3 + 1.5*IQR)]
    n5 = len(df)
    print(f"    异常值剔除     删除{n4 - n5}条")
    print(f"    合计删除{n0 - n5}条，剩余{n5}条")
    # 派生字段
    df["pubdate"] = pd.to_datetime(df["pubdate"], unit="s", errors="coerce")
    df["pub_days"] = (base_date - df["pubdate"]).dt.days
    def get_pub_group(days):
        if days <= 7:
            return "7天内"
        elif 7 < days <= 30:
            return "7-30天"
        else:
            return "30天以上"
    df["pub_group"] = df["pub_days"].apply(get_pub_group)
    # 互动总量和各类比率，统一保留4位小数
    df["interaction"] = (df["like"].fillna(0) + df["coin"].fillna(0) +
                         df["favorite"].fillna(0) + df["share"].fillna(0) +
                         df["reply"].fillna(0) + df["danmaku"].fillna(0))
    df["interaction_rate"] = (df["interaction"] / df["view"]).round(4)
    df["like_rate"] = (df["like"].fillna(0) / df["view"]).round(4)
    df["coin_rate"] = (df["coin"].fillna(0) / df["view"]).round(4)
    df["duration_min"] = (df["duration"] / 60).round(2)
    
    # 标记是否进过热榜前十
    df["his_rank"] = df["his_rank"].fillna(0)
    df["top10"] = ((df["his_rank"] > 0) & (df["his_rank"] <= 10)).astype(int)
    print("派生字段计算完成")
    # 保存结果
    path = os.path.join(proc_dir, "bili_clean.csv")
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"\n清洗后数据已保存至：{path}")
    return df
if __name__ == "__main__":
    raw = load_raw()
    clean = clean_data(raw)
    print("\n清洗后数据预览：")
    cols = ["weekly_number", "title", "tname", "pub_group",
            "view", "like", "coin", "interaction"]
    print(clean[cols].head().to_string(index=False))
    print("\n字段信息：")
    print(clean.info())
#1
    #(2026.7.15series)
#更新记录：
    #datetime相减得到的是timedelta，取.days
    #分组之后样本量差得还挺多，30天以上的视频占了大半，算发布天数，按时间分组，新老视频分开分析更准
