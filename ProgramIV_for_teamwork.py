import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
datapath=r"processed\bili_clean.csv"
def main():
    df = pd.read_csv(datapath, encoding="utf-8-sig")
    print(f"️  sign completed:")
    df["是否前10"]=df["rank_in_week"].apply(lambda x: 1 if x<=10 else 0)
    print(f"   -videos Top10 in number:{df['是否前10'].sum()}")
    print(f"   -videos Top10 out number:{len(df)-df['是否前10'].sum()}")
    print(f"   -ratio video Top10：{df['是否前10'].mean():.2%} \n")
    print("related matrix of core number（皮尔逊系数）")#相关性分析
    feature_cols = ["view", "like", "coin", "favorite", "share", "danmaku", "reply"]
    existing_cols = [col for col in feature_cols if col in df.columns]
    missing_cols = [col for col in feature_cols if col not in df.columns]
    corr_matrix = df[existing_cols].corr().round(3)
    corr_matrix.columns = [
        "播放量", "点赞数", "投币数", "收藏数", "转发数", "弹幕数", "评论数"
    ][:len(existing_cols)]
    corr_matrix.index = corr_matrix.columns
    print(corr_matrix)
    print()
    #机器学习数据准备
    X = df[existing_cols]#所有互动指标
    y = df["是否前10"]#是否进入前10
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)#分层抽样划分
    print(f"   -excercise group:{len(X_train)}number of data (+data number:{y_train.sum()})")
    print(f"   -test group:{len(X_test)}number of data(+data number:{y_test.sum()})\n")
    print("exercise and test of model")#训练随机森林分类模型
    model = RandomForestClassifier(n_estimators=150, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"ratio of accuracy:{accuracy_score(y_test, y_pred):.3f}")#模型效果评估
    print("\nthorough report:")
    print(classification_report(
        y_test, y_pred, 
        target_names=["未进前10", "进入前10"],
        digits=3#保留3位小数
    ))
    #特征重要性排名
    print("feature importance top line(reasons of top10)")
    importance_df = pd.DataFrame({
        "英文列名": existing_cols,
        "中文含义": ["播放量", "点赞数", "投币数", "收藏数", "转发数", "弹幕数", "评论数"][:len(existing_cols)],
        "重要性": model.feature_importances_
    }).sort_values("重要性", ascending=False).reset_index(drop=True)
    #计算重要性占比
    importance_df["重要性占比"] = (importance_df["重要性"] / importance_df["重要性"].sum()).round(3) * 100
    importance_df["重要性占比"] = importance_df["重要性占比"].astype(str) + "%"
    print(importance_df.to_string(index=False))
    input("press enter to exit...")
if __name__ == "__main__":
    main()
