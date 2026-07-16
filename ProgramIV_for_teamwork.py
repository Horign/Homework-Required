import pandas as pd
from scipy.stats import linregress
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
datapath=r"processed\bili_clean.csv"
def main():
    df = pd.read_csv(datapath, encoding="utf-8-sig")
    print(f"  sign completed:")
    df["是否前10"]=df["rank_in_week"].apply(lambda x: 1 if x<=10 else 0)
    print(f"   -videos Top10 in number:{df['是否前10'].sum()}")
    print(f"   -videos Top10 out number:{len(df)-df['是否前10'].sum()}")
    print(f"   -ratio video Top10：{df['是否前10'].mean():.2%} \n")

    print("related matrix of core number（皮尔逊系数）")
    feature_cols = ["view", "like", "coin", "favorite", "share", "danmaku", "reply"]
    existing_cols = [col for col in feature_cols if col in df.columns]
    corr_matrix = df[existing_cols].corr().round(3)
    corr_matrix.columns = [
        "播放量", "点赞数", "投币数", "收藏数", "转发数", "弹幕数", "评论数"
    ][:len(existing_cols)]
    corr_matrix.index = corr_matrix.columns
    print(corr_matrix)
    print()
    #一元线性回归
    print("一元线性回归（播放量为自变量）")
    reg_like = linregress(df["view"], df["like"])
    print(f"  点赞：y={reg_like.slope:.3f}x+{reg_like.intercept:.3f}  R²={reg_like.rvalue**2:.3f}  p={reg_like.pvalue:.3e}")
    reg_coin = linregress(df["view"], df["coin"])
    print(f"  投币：y={reg_coin.slope:.3f}x+{reg_coin.intercept:.3f}  R²={reg_coin.rvalue**2:.3f}  p={reg_coin.pvalue:.3e}")
    print()
    #分分区回归
    print("分分区回归对比（播放→点赞）")
    for tname in df["tname"].value_counts().head(8).index:
        sub = df[df["tname"] == tname]
        if len(sub) < 30:
            continue
        r = linregress(sub["view"], sub["like"])
        print(f"  {tname}：r={r.rvalue:.3f}  R²={r.rvalue**2:.3f}")
    print()
    #分发布时长回归
    print("分发布时长回归对比（播放→点赞）")
    for g in ["7天内", "7-30天", "30天以上"]:
        sub = df[df["pub_group"] == g]
        if len(sub) < 30:
            continue
        r = linregress(sub["view"], sub["like"])
        print(f"  {g}：r={r.rvalue:.3f}  R²={r.rvalue**2:.3f}  样本数={len(sub)}")
    print()
    #随机森林分类
    print("exercise and test of model")
    X = df[existing_cols]
    y = df["是否前10"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"   -excercise group:{len(X_train)}number of data (+data number:{y_train.sum()})")
    print(f"   -test group:{len(X_test)}number of data(+data number:{y_test.sum()})\n")

    model = RandomForestClassifier(n_estimators=150, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"ratio of accuracy:{accuracy_score(y_test, y_pred):.3f}")
    print("\nthorough report:")
    print(classification_report(
        y_test, y_pred, 
        target_names=["未进前10", "进入前10"],
        digits=3
    ))
    #特征重要性
    print("feature importance top line(reasons of top10)")
    importance_df = pd.DataFrame({
        "英文列名": existing_cols,
        "中文含义": ["播放量", "点赞数", "投币数", "收藏数", "转发数", "弹幕数", "评论数"][:len(existing_cols)],
        "重要性": model.feature_importances_
    }).sort_values("重要性", ascending=False).reset_index(drop=True)
    importance_df["重要性占比"] = (importance_df["重要性"] / importance_df["重要性"].sum()).round(3) * 100
    importance_df["重要性占比"] = importance_df["重要性占比"].astype(str) + "%"
    print(importance_df.to_string(index=False))

    input("press enter to exit...")

if __name__ == "__main__":
    main()
#1
    #(2026.7.15series)
# polyfit算不了R²，换scipy的linregress方便多了
# 老视频R²确实比新视频高，符合之前的猜想
