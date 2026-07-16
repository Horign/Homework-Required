import os
import pandas as pd
from scipy.stats import linregress
from sklearn.ensemble import RandomForestClassifier
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Scatter, HeatMap, Line, Page

datapath = r"processed\bili_clean.csv"
outdir = "output"

def main():
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    df = pd.read_csv(datapath, encoding="utf-8-sig")
    print(f"data loaded: {len(df)} videos, {df['weekly_number'].nunique()} weeks\n")

    feature_cols = ["view", "like", "coin", "favorite", "share", "danmaku", "reply"]
    feature_cn = ["播放量", "点赞数", "投币数", "收藏数", "转发数", "弹幕数", "评论数"]

    # 图1：播放TOP10柱状图
    top = df.sort_values("view", ascending=False).head(10)
    titles = [t[:12] + "…" if len(str(t)) > 12 else str(t) for t in top["title"]]
    bar_view = (
        Bar()
        .add_xaxis(titles)
        .add_yaxis("播放量", [int(v) for v in top["view"]])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="播放量 TOP10 收录视频"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)),
            datazoom_opts=[opts.DataZoomOpts()])
    )
    bar_view.render(os.path.join(outdir, "01_播放量TOP10.html"))
    print("chart1 done: 播放量TOP10")

    # 图2：UP主上榜TOP10柱状图
    up = df.groupby("up_name")["bvid"].nunique().sort_values(ascending=False).head(10)
    bar_up = (
        Bar()
        .add_xaxis(up.index.tolist())
        .add_yaxis("累计上榜视频数", [int(v) for v in up.values])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="UP主累计上榜次数 TOP10"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)))
    )
    bar_up.render(os.path.join(outdir, "02_UP主上榜TOP10.html"))
    print("chart2 done: UP主上榜TOP10")

    # 图3：分区占比饼图
    vc = df["tname"].value_counts().head(8)
    pie = (
        Pie()
        .add("", [list(z) for z in zip(vc.index.tolist(), [int(x) for x in vc.values])])
        .set_global_opts(title_opts=opts.TitleOpts(title="收录视频分区占比 TOP8"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    )
    pie.render(os.path.join(outdir, "03_分区占比.html"))
    print("chart3 done: 分区占比")

    # 图4：播放vs点赞散点图+拟合线
    s = df.sample(min(800, len(df)), random_state=1)
    reg = linregress(s["view"], s["like"])
    x_line = [int(s["view"].min()), int(s["view"].max())]
    y_line = [int(reg.slope * x + reg.intercept) for x in x_line]

    scatter = (
        Scatter()
        .add_xaxis([int(v) for v in s["view"]])
        .add_yaxis("点赞数", [int(v) for v in s["like"]], symbol_size=6,
                   label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="播放量 vs 点赞数 关系散点图"),
            xaxis_opts=opts.AxisOpts(type_="value", name="播放量"),
            yaxis_opts=opts.AxisOpts(type_="value", name="点赞数"),
            visualmap_opts=opts.VisualMapOpts(type_="size", max_=int(s["like"].max()), min_=0))
    )
    # 叠拟合直线
    line_fit = (
        Line()
        .add_xaxis(x_line)
        .add_yaxis("拟合线", y_line, linestyle_opts=opts.LineStyleOpts(color="red", width=2),
                   label_opts=opts.LabelOpts(is_show=False), symbol="none")
    )
    scatter.overlap(line_fit)
    scatter.render(os.path.join(outdir, "04_播放vs点赞散点.html"))
    print("chart4 done: 播放vs点赞散点")

    # 图5：相关系数热力图
    corr = df[feature_cols].corr().round(2)
    n = len(feature_cols)
    hdata = [[j, i, float(corr.iloc[i, j])] for i in range(n) for j in range(n)]
    heat = (
        HeatMap()
        .add_xaxis(feature_cn)
        .add_yaxis("相关系数", feature_cn, hdata,
                   label_opts=opts.LabelOpts(is_show=True, position="inside"))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="核心指标相关系数热力图"),
            visualmap_opts=opts.VisualMapOpts(min_=-1, max_=1, is_calculable=True, pos_left="right"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)))
    )
    heat.render(os.path.join(outdir, "05_相关系数热力图.html"))
    print("chart5 done: 相关系数热力图")

    # 图6：特征重要性条形图
    y = df["rank_in_week"].apply(lambda x: 1 if x <= 10 else 0)
    X = df[feature_cols]
    model = RandomForestClassifier(n_estimators=150, random_state=42)
    model.fit(X, y)
    imp = pd.DataFrame({"name": feature_cn, "value": model.feature_importances_}).sort_values("value")
    bar_imp = (
        Bar()
        .add_xaxis(imp["name"].tolist())
        .add_yaxis("重要性", [round(float(v), 4) for v in imp["value"]])
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts(title="进入前10的关键因素 —— 特征重要性"))
    )
    bar_imp.render(os.path.join(outdir, "06_特征重要性.html"))
    print("chart6 done: 特征重要性")

    # 图7：各期平均播放走势
    trend = df.groupby("weekly_number")["view"].mean().round(0)
    line = (
        Line()
        .add_xaxis([str(x) for x in trend.index.tolist()])
        .add_yaxis("平均播放量", [int(v) for v in trend.values], is_smooth=True,
                   label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="各期收录视频平均播放量走势"),
            xaxis_opts=opts.AxisOpts(name="期数", axislabel_opts=opts.LabelOpts(rotate=45)),
            datazoom_opts=[opts.DataZoomOpts()])
    )
    line.render(os.path.join(outdir, "07_各期平均播放趋势.html"))
    print("chart7 done: 各期平均播放趋势")

    # 图8：发布时长分组对比
    pub_stat = df.groupby("pub_group")[["view", "like", "coin"]].mean().round(0)
    bar_pub = (
        Bar()
        .add_xaxis(pub_stat.index.tolist())
        .add_yaxis("平均播放", [int(v) for v in pub_stat["view"]])
        .add_yaxis("平均点赞", [int(v) for v in pub_stat["like"]])
        .add_yaxis("平均投币", [int(v) for v in pub_stat["coin"]])
        .set_global_opts(title_opts=opts.TitleOpts(title="不同发布时长核心指标对比"))
    )
    bar_pub.render(os.path.join(outdir, "08_发布时长对比.html"))
    print("chart8 done: 发布时长对比")

    # 总看板
    page = Page(layout=Page.SimplePageLayout)
    page.add(bar_view, bar_up, pie, scatter, heat, bar_imp, line, bar_pub)
    page.render(os.path.join(outdir, "dashboard.html"))
    print("\nall charts done, open output/dashboard.html to view")
    input("press enter to exit...")

if __name__ == "__main__":
    main()
#1
    #(2026.7.15series)
# 散点图叠折线查了好久，用overlap就行
# 中文显示一开始有问题，改了环境就好了
