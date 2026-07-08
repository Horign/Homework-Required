#鉴于此代码文件仅作练习使用，部分输入输出处理相对较为粗糙，敬请谅解！
import os
student_list=[]
def clear_screen():
    os.system("cls")
def get_valid_score(prompt_text):
    while True:
        try:
            user_input = input(prompt_text)
            score = float(user_input)
            if 0 <= score <= 150:
                return score
            else:
                print("Error: Score must be between 0 and 150!")
                input("press Enter to continue...")
        except ValueError:
            print(f"Error: '{user_input}' is not a valid number!")
            input("press Enter to continue...")
def get_valid_score2(prompt_text):
    while True:
        try:
            user_input = input(prompt_text)
            score = float(user_input)
            if 0 <= score <= 100:
                return score
            else:
                print("Error: Score must be between 0 and 100!")
                input("press Enter to continue...")
        except ValueError:
            print(f"Error: '{user_input}' is not a valid number!")
            input("press Enter to continue...")
def add():
    name_student=input("Student name,please:")
    while True:
        id_student=input("Student id,please:")
        repeat=False
        for stu in student_list:
            if stu["ID"]==id_student:
                repeat=True
                break
        if repeat:
            print(f"Error: Student ID {id_student} already exists!")
            input("press Enter to continue...")
        else:
            break
    Chinese=get_valid_score("His or Her Chinese grade:")
    Math=get_valid_score("His or Her Math grade:")
    Foreign_Language=get_valid_score("His or Her Foreign Language grade:")
    Physics=get_valid_score2("His or Her Physics grade:")
    Chemistry=get_valid_score2("His or Her Chemistry grade:")
    Politics=get_valid_score2("His or Her Politics grade:")
    History=get_valid_score2("His or Her History grade:")
    Biology=get_valid_score2("His or Her Biologty grade:")
    Geography=get_valid_score2("His or Her Geography grade:")
    stu_dict={
        "Name":name_student,
        "ID":id_student,
        "Chinese":Chinese,
        "Math":Math,
        "Foreign Language":Foreign_Language,
        "Physics":Physics,
        "Chemistry":Chemistry,
        "Politics":Politics,
        "History":History,
        "Biology":Biology,
        "Geography":Geography,
    }
    student_list.append(stu_dict)
    input("press enter to continue...")
def search():
    if not student_list:
        print("Sorry,but there is nothing about what you want to search for.")
        input("Press Enter to continue...")
        return
    lookup_id=input("Insert(Input) student id you want to look up:")
    find=False
    for stu in student_list:
        if stu["ID"]==lookup_id:
            find=True
            print(f"Name:{stu['Name']}")
            print(f"ID:{stu['ID']}")
            print(f"Chinese:{stu['Chinese']}")
            print(f"Math:{stu['Math']}")
            print(f"Foreign Language:{stu['Foreign Language']}")
            if stu["Physics"]!=0:
                print(f"Physics:{stu['Physics']}")
            if stu["Chemistry"]!=0:
                print(f"Chemistry:{stu['Chemistry']}")
            if stu["Politics"]!=0:
                print(f"Politics:{stu['Politics']}")
            if stu["History"]!=0:
                print(f"History:{stu['History']}")
            if stu["Biology"]!=0:
                print(f"Biology:{stu['Biology']}")
            if stu["Geography"]!=0:
                print(f"Geography:{stu['Geography']}")
            total_individual=stu["Chinese"]+stu["Math"]+stu["Foreign Language"]+stu["Physics"]+stu["Chemistry"]+stu["Biology"]+stu["History"]+stu["Politics"]+stu["Geography"]
            print(f"Total:{total_individual:.2f}")
            input("press Enter to continue..,")
    if not find:
        print("Sorry,but we cannot find the data of the student you search for.")
        input("press Enter to continue...")
def stat():
    if not student_list:
        print("Sorry,but there is nothing about what you want to search for.")
        input("Press Enter to continue...")
        return
    subject_data = {
        "Chinese": [],
        "Math": [],
        "Foreign Language": [],
        "Physics": [],
        "Chemistry": [],
        "Politics": [],
        "History": [],
        "Biology": [],
        "Geography": []
    }
    student_standard_total = []
    for stu in student_list:
        chi = stu["Chinese"]
        mat = stu["Math"]
        eng = stu["Foreign Language"]
        phy = stu["Physics"]
        che = stu["Chemistry"]
        pol = stu["Politics"]
        his = stu["History"]
        bio = stu["Biology"]
        geo = stu["Geography"]
        subject_data["Chinese"].append(chi)
        subject_data["Math"].append(mat)
        subject_data["Foreign Language"].append(eng)
        subject_data["Physics"].append(phy)
        subject_data["Chemistry"].append(che)
        subject_data["Politics"].append(pol)
        subject_data["History"].append(his)
        subject_data["Biology"].append(bio)
        subject_data["Geography"].append(geo)
        std_chi = chi * 100 / 150
        std_mat = mat * 100 / 150
        std_eng = eng * 100 / 150
        total_std = std_chi + std_mat + std_eng + phy + che + pol + his + bio + geo
        student_standard_total.append(total_std)
    print(f"Average standard total score of each student: {sum(student_standard_total)/len(student_standard_total):.2f}\n")
    for sub in ["Chinese", "Math", "Foreign Language"]:
        score_list = subject_data[sub]
        avg_raw = sum(score_list) / len(score_list)
        avg_std = avg_raw * 100 / 150
        sub_max = max(score_list)
        sub_min = min(score_list)
        print(f"【{sub}】(Full mark:150)")
        print(f"    Original average: {avg_raw:.2f} | Standard 100-point average: {avg_std:.2f}")
        print(f"    Highest score in this subject: {sub_max}")
        print(f"    Lowest score in this subject: {sub_min}\n")
    for sub in ["Physics", "Chemistry", "Politics", "History", "Biology", "Geography"]:
        score_list = subject_data[sub]
        avg_raw = sum(score_list) / len(score_list)
        sub_max = max(score_list)
        sub_min = min(score_list)
        print(f"【{sub}】(Full mark:100)")
        print(f"    Average: {avg_raw:.2f}")
        print(f"    Highest score in this subject: {sub_max}")
        print(f"    Lowest score in this subject: {sub_min}\n")
    input("Press Enter to continue...")
while True:
    clear_screen()
    print("Welcome to student grade points manager server!All rights reserved.")
    print("1.Input students' grades(Teachers)")
    print("2.Look up grade data points on pointed student by one's id.")
    print("3.The statistics of the whole class students' grades.(Your grade points will be transferred to 100-grade standard.)")
    print("(Other numbers or Texts).Log out the system.")
    choice=input("Input the number before the texts,please:")
    if choice=="1":
        add()
    elif choice=="2":
        search()
    elif choice=="3":
        stat()
    else:
        print("Thanks for using!Goodbye!")
        input("Press Enter to continue...")
        break
