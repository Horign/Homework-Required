import math
import os
def clear():
    os.system("cls")
def add(a, b):
    return a + b
def sub(a, b):
    return a - b
def mul(a, b):
    return a * b
def div(a, b):
    if b == 0:
        raise ZeroDivisionError("除数不能为0")
    return a / b
def power(a, b):
    return a ** b
def sqrt_num(a):
    if a < 0:
        raise ValueError("负数无法开平方")
    return math.sqrt(a)
def save_record(expr, res):
    with open("calc_history.txt", "a", encoding="utf-8") as f:
        f.write(f"{expr} = {res}\n")
def read_history():
    try:
        with open("calc_history.txt", "r", encoding="utf-8") as f:
            content = f.read()
        if content:
            print(content)
        else:
            print("暂无历史记录")
    except FileNotFoundError:
        print("暂无历史记录文件")
def calculator_main():
    while True:
        clear()
        print("\n数学计算器")
        print("1.加法 2.减法 3.乘法 4.除法")
        print("5.幂运算 6.开平方 7.查看历史 0.退出")
        op = input("请选择功能：")
        if op == "0":
            print("计算器退出")
            break
        try:
            if op in ["1", "2", "3", "4", "5"]:
                num1 = float(input("输入第一个数字："))
                num2 = float(input("输入第二个数字："))
                if op == "1":
                    result = add(num1, num2)
                    exp = f"{num1} + {num2}"
                elif op == "2":
                    result = sub(num1, num2)
                    exp = f"{num1} - {num2}"
                elif op == "3":
                    result = mul(num1, num2)
                    exp = f"{num1} * {num2}"
                elif op == "4":
                    result = div(num1, num2)
                    exp = f"{num1} / {num2}"
                elif op == "5":
                    result = power(num1, num2)
                    exp = f"{num1} ** {num2}"
                print(f"计算结果：{result}")
                save_record(exp, result)
                input("press Enter to continue...")
            elif op == "6":
                num = float(input("输入要开方的数字："))
                result = sqrt_num(num)
                exp = f"sqrt({num})"
                print(f"计算结果：{result}")
                input("press Enter to continue...")
                save_record(exp, result)
            elif op == "7":
                read_history()
            else:
                print("输入序号不存在！")
                input("press Enter to continue...")
        except ValueError as e:
            print(f"输入错误：{e}")
            input("press Enter to continue...")
        except ZeroDivisionError as e:
            print(f"计算错误：{e}")
            input("press Enter to continue...")
if __name__ == "__main__":
    calculator_main()
    input("press Enter to continue...")
