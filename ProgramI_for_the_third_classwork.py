import numpy as np
student_names = []
score_array = np.array([])
def show_menu():
    """打印系统主菜单"""
    print("=" * 35)
    print("        成绩分析系统")
    print("=" * 35)
    print("1. 输入成绩数据")
    print("2. 查看成绩统计")
    print("3. 查看成绩排名")
    print("4. 查看成绩分布")
    print("5. 查询学生成绩")
    print("6. 退出系统")
    print("=" * 35)
def input_scores():
    global student_names, score_array
    student_names.clear()
    while True:
        try:
            count = int(input("请输入学生人数："))
            if count > 0:
                break
            else:
                print("请重新输入！")
        except ValueError:
            print("请输入数字！")
            input("press enter key to continue...")
    temp_scores = []
    for i in range(count):
        name = input(f"\n请输入第{i+1}个学生姓名：")
        student_names.append(name)
        while True:
            try:
                score = float(input("请输入成绩："))
                if 0 <= score <= 100:
                    temp_scores.append(score)
                    break
                else:
                    print("请重新输入！")
                    input("press enter key to continue...")
            except ValueError:
                print("请输入数字！")
                input("press enter to continue...")
    score_array = np.array(temp_scores)
    print("\n成绩录入完成！")
def calc_statistics():
    if len(score_array) == 0:
        print("无数据，请先录入！")
        return
    print("\n成绩统计信息")
    print(f"总人数：{len(score_array)}")
    print(f"平均分：{np.mean(score_array):.2f}")
    print(f"最高分：{np.max(score_array)}")
    print(f"最低分：{np.min(score_array)}")
    print(f"中位数：{np.median(score_array):.2f}")
    print(f"方差：{np.var(score_array):.2f}")
    print(f"标准差：{np.std(score_array):.2f}")
def show_ranking():
    if len(score_array) == 0:
        print("无数据，请先录入！")
        return
    stu_data = list(zip(student_names, score_array))
    stu_data.sort(key=lambda x: x[1], reverse=True)
    print("\n 成绩排名\n")
    print(f"{'排名':<6}{'姓名':<8}{'分数':<6}")
    for idx, (name, score) in enumerate(stu_data, start=1):
        print(f"{idx:<6}{name:<8}{score:<6}")
def show_score_distribution():
    if len(score_array) == 0:
        print("暂无成绩数据，请先录入！")
        return
    excellent = np.sum((score_array >= 90) & (score_array <= 100)) 
    good = np.sum((score_array >= 80) & (score_array < 90))      
    pass_ = np.sum((score_array >= 60) & (score_array < 80))
    fail = np.sum(score_array < 60)                              
    total = len(score_array)
    print("\n成绩等级分布")
    print(f"优秀(90-100)：{excellent}人，占比{excellent/total*100:.1f}%")
    print(f"良好(80-89) ：{good}人，占比{good/total*100:.1f}%")
    print(f"及格(60-79) ：{pass_}人，占比{pass_/total*100:.1f}%")
    print(f"不及格(0-59)：{fail}人，占比{fail/total*100:.1f}%")
def query_student():
    if len(score_array) == 0:
        print("无数据，请先录入！")
        return
    target_name = input("请输入要查询的学生姓名：")
    if target_name in student_names:
        idx = student_names.index(target_name)
        score = score_array[idx]
        if score >= 90:
            level = "优秀"
        elif score >= 80:
            level = "良好"
        elif score >= 60:
            level = "及格"
        else:
            level = "不及格"
        print(f"\n学生：{target_name}，分数：{score}，等级：{level}")
    else:
        print(f"未找到名为【{target_name}】的学生！")
def main():
    while True:
        show_menu()
        select = input("请选择：")
        if select == "1":
            input_scores()
        elif select == "2":
            calc_statistics()
        elif select == "3":
            show_ranking()
        elif select == "4":
            show_score_distribution()
        elif select == "5":
            query_student()
        elif select == "6":
            print("感谢使用！")
            break
        else:
            print("输入无效！")
        # 分隔线，区分每次操作
        input("\npress enter to continue...")
        print("\n" * 2)
if __name__ == "__main__":
    main()
