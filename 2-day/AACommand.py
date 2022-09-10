

# 别问为什么这么做，问就是好家伙
def print_success(msg,end="\n"):  # 构造一个函数 参数为 输出信息   尾部字符串（一般使用换行实现）
    print(f"[+] {msg}",end=end) #输出 [+] XXX 并且设置end参数也就是尾部字符串

if __name__ == "__main__":
    print_success("Fuck v1.0") #使用print_success输出一个字符串
    Command = []  #构造列表
    Command.append("Apache ") # 列表加入参数字符串
    while True: #这是一个死循环，因为循环条件写死了 只能break才能退出
        if len(Command)==10: # 判断列表长度是否等于10 如果是跳出循环
            break #跳出循环
        elif len(Command) == 2 or len(Command) == 4: # 判断长度为2 或（or） 4 ，如果是那么加入NULL
            Command.append("NNULL\\")
            continue # 跳出本次循环 跳出本次循环   代码不会继续运行17行 但是循环没有跳出
        Command.append("N%d\\"%len(Command)) #加入N和长度的字符串   %d 为整数   并且 使用 % 作为格式化传递 该代码类似于f"N{len(Command)}\\"

    Command.append("etc\passwd") # 随便加入一个字符串作为演示
    for i in Command: # 取出列表里的字符串，并且每次都会传递给i 递归
        print("Index:%s" %  i) # %s为 字符串类型    类似于f"Index:{i}"
    print("COMMAND:%s" % (":".join(Command)))  # 使用字符串的join方法对列表进行合并，并且传递给格式化 （） 括起来 是优先级 也可以理解为优先运行
    print_success("MAKE Command Successfully.") # 输出成功
    if len(Command) > 10 and i== "..\\": #判断长度（没啥意义 ） 条件是识别内容和 （and）长度
        print_success("Verify String:",end="")
        print(i)
    else:
        print_success("Fuck")








