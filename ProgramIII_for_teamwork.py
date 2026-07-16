import os
import pandas as pd
base_dir = os.path.dirname(os.path.abspath(__file__))
proc_dir = os.path.join(base_dir, "processed")
os.makedirs(proc_dir, exist_ok=True)
pd.set_option("display.unicode.east_asian_width", True)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
def load_clean():
    path = os.path.join(proc_dir, "bili_clean.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"未找到 {path}")
    df = pd.read_csv(path, encoding="utf-8-sig")
    print(f"[read] 载入清洗后数据 {len(df)} 条，共 {df['weekly_number'].nunique()} 期")
    return df
def analyze_videos(df):#描述统计（计数/均值/标准差/最小/分位数/最大）
    stat_cols = ["view", "like", "coin", "favorite", "share",
                 "reply", "danmaku", "interaction", "duration_min"]
    desc = df[stat_cols].describe().round(1)
    print("\n各指标描述统计")
    print(desc)
    desc.to_csv(os.path.join(proc_dir, "video_desc.csv"), encoding="utf-8-sig")
    top_view = df.sort_values("view", ascending=False).head(10)[#播放TOP10
        ["title", "up_name", "view", "like", "interaction"]]
    print("\n播放TOP10")
    print(top_view.to_string(index=False))
    top_like = df.sort_values("like", ascending=False).head(10)[
        ["title", "up_name", "like", "view", "like_rate"]]#点赞TOP10
    print("\n点赞TOP10")
    print(top_like.to_string(index=False))
    tname_count = df["tname"].value_counts()#各分区收录视频数
    print("\n收录数量 TOP10")
    print(tname_count.head(10))
    tname_count.to_csv(os.path.join(proc_dir, "tname_count.csv"),
                       encoding="utf-8-sig", header=["count"])
    ratio = df["top10"].mean()#进热榜前十占比
    print(f"\n[热榜前十占比]收录视频中进入过热榜前10的比例：{ratio:.2%}")
    return desc, top_view, tname_count
def analyze_up(df):
    up = df.groupby(["up_mid", "up_name"]).agg(
        video_count=("bvid", "nunique"),#上榜视频数
        total_view=("view", "sum"),#播放量
        total_like=("like", "sum"),#点赞
        total_coin=("coin", "sum"),#投币
        total_interaction=("interaction", "sum"),#互动热度
        avg_view=("view", "mean"),#平均单视频播放量
        top10_count=("top10", "sum"),#上过热榜前十的视频数
    ).reset_index()
    up["avg_view"] = up["avg_view"].round(0)
    up = up.sort_values(["video_count", "total_view"],
                        ascending=[False, False]).reset_index(drop=True)#按上榜次数降序，次数相同再按播放量降序
    print("\nUP主TOP10")
    print(up.head(10)[["up_name", "video_count", "total_view",
                       "total_like", "top10_count"]].to_string(index=False))
    print("\n累计播放量最高的 UP主 TOP10")
    print(up.sort_values("total_view", ascending=False).head(10)[
        ["up_name", "total_view", "video_count", "avg_view"]].to_string(index=False))
    print(f"\nUP主总体情况共 {len(up)} 位 UP主上榜；"#汇总信息
          f"人均上榜 {up['video_count'].mean():.2f} 次；"
          f"上榜 2 次及以上的 UP主 {int((up['video_count'] >= 2).sum())} 位")
    up.to_csv(os.path.join(proc_dir, "up_summary.csv"),
              index=False, encoding="utf-8-sig")
    print(f"\nUP主累计数据已保存至：{os.path.join(proc_dir, 'up_summary.csv')}")
    return up
if __name__ == "__main__":
    print("Question III")
    df = load_clean()
    analyze_videos(df)#视频基本播放情况
    analyze_up(df)#UP主数据
    print("\n结果已打印并保存到processed/目录。")
