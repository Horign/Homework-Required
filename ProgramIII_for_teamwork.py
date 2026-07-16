import os
import pandas as pd
base_dir = os.path.dirname(os.path.abspath(__file__))
proc_dir = os.path.join(base_dir, "processed")
os.makedirs(proc_dir, exist_ok=True)
pd.set_option("display.unicode.east_asian_width", True)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
pd.set_option("display.precision", 3)
def load_clean():
    path = os.path.join(proc_dir, "bili_clean.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"找不到{path}文件")
    df = pd.read_csv(path, encoding="utf-8-sig")
    print(f"[读取] 载入清洗后数据{len(df)}条，共{df['weekly_number'].nunique()}期")
    return df
def analyze_videos(df):
    #全样本基础描述统计，统一保留1位小数
    stat_cols = ["view", "like", "coin", "favorite", "share",
                 "reply", "danmaku", "interaction", "duration_min"]
    desc = df[stat_cols].describe().round(1)
    print("\n=== 全样本指标描述统计 ===")
    print(desc)
    desc.to_csv(os.path.join(proc_dir, "video_desc.csv"), encoding="utf-8-sig")
    #播放量TOP10
    top_view = df.sort_values("view", ascending=False).head(10)[
        ["title", "up_name", "view", "like", "interaction"]]
    print("\n=== 播放量TOP10视频 ===")
    print(top_view.to_string(index=False))
    #点赞量TOP10
    top_like = df.sort_values("like", ascending=False).head(10)[
        ["title", "up_name", "like", "view", "like_rate"]]
    print("\n=== 点赞量TOP10视频 ===")
    print(top_like.to_string(index=False))
    #各分区收录数量
    tname_count = df["tname"].value_counts()
    print("\n=== 分区收录数量TOP10 ===")
    print(tname_count.head(10))
    tname_count.to_csv(os.path.join(proc_dir, "tname_count.csv"),
                       encoding="utf-8-sig", header=["count"])
    #热榜前十占比
    ratio = df["top10"].mean()
    print(f"\n收录视频里进过热榜前10的比例：{ratio:.2%}")
    #各分区平均指标对比
    print("\n=== 各分区平均指标对比 ===")
    tname_stat = df.groupby("tname")[stat_cols].mean().round(1).sort_values("view", ascending=False)
    print(tname_stat.head(8))
    tname_stat.to_csv(os.path.join(proc_dir, "tname_mean.csv"), encoding="utf-8-sig")
    #按发布时长分组统计，看看新老视频的差异
    print("\n=== 不同发布时长分组指标对比 ===")
    pub_stat = df.groupby("pub_group")[stat_cols].mean().round(1)
    print(pub_stat)
    pub_stat.to_csv(os.path.join(proc_dir, "pub_group_mean.csv"), encoding="utf-8-sig")
    return desc, top_view, tname_count
def analyze_up(df):
    #UP主维度聚合统计
    up = df.groupby(["up_mid", "up_name"]).agg(
        video_count=("bvid", "nunique"),
        total_view=("view", "sum"),
        total_like=("like", "sum"),
        total_coin=("coin", "sum"),
        total_interaction=("interaction", "sum"),
        avg_view=("view", "mean"),
        avg_like_rate=("like_rate", "mean"),
        top10_count=("top10", "sum"),
    ).reset_index()
    up["avg_view"] = up["avg_view"].round(0)
    up["avg_like_rate"] = up["avg_like_rate"].round(4)
    #按上榜次数排序
    up = up.sort_values(["video_count", "total_view"],
                        ascending=[False, False]).reset_index(drop=True)
    print("\n=== UP主上榜次数TOP10 ===")
    print(up.head(10)[["up_name", "video_count", "total_view",
                       "avg_like_rate", "top10_count"]].to_string(index=False))
    #按总播放量排序
    print("\n=== 累计播放量最高UP主TOP10 ===")
    print(up.sort_values("total_view", ascending=False).head(10)[
        ["up_name", "total_view", "video_count", "avg_view"]].to_string(index=False))
    #整体情况汇总
    print(f"\n一共有{len(up)}位UP主上过榜；"
          f"平均每位上榜{up['video_count'].mean():.2f}次；"
          f"上榜2次及以上的有{int((up['video_count'] >= 2).sum())}位")
    up.to_csv(os.path.join(proc_dir, "up_summary.csv"),
              index=False, encoding="utf-8-sig")
    print(f"\nUP主统计结果存在：{os.path.join(proc_dir, 'up_summary.csv')}")
    return up
if __name__ == "__main__":
    print("开始基础统计分析")
    df = load_clean()
    analyze_videos(df)
    analyze_up(df)
    print("\n所有结果都已保存到processed文件夹。")
