
"""
@ print_success: 定义 print_success 函数
  1.该函数接受两个参数传入，分别为 msg 和 end
  2.msg 表示需要打印的消息
  3.end 表示消息以什么结尾，这里是换行符
"""


def print_success(msg, end="\n"):  # 构造一个函数，参数为输出信息和尾部字符串（一般使用换行实现）
    print(f"[+] {msg}", end=end)  # 输出 [+] XXX 并且设置end参数也就是尾部字符串


if __name__ == "__main__":
    print_success("Fuck v1.0")  # 使用print_success输出一个字符串
    # Command = [] # 构造列表
    # Command.append("Apache ") # 列表加入参数字符串
    # 针对上述代码的优化
    Command = ["Apache"]

    while True:
        # 这是一个死循环，因为循环条件写死了，当列表中元素为10个时，break被运行并退出循环
        if len(Command)==10:
            break
        # 如果列表长度为2或4 ，那么列表追加字符串"NULL\"
        elif len(Command) == 2 or len(Command) == 4:
            Command.append("NULL\\")
            # 跳出本次循环，从while判断语句开始执行
            continue
        # 列表Command长度不为2、4、10，列表追加“N与当前列表长度\”作为新字符串，如“N3\”
        Command.append("N%d\\" % len(Command))

    # while循环结束后，任意加入一个字符串作为演示
    Command.append("etc\passwd")
    # 打印列表中的元素
    for i in Command:
        print("Index:%s" % i)

    # 使用字符串的join方法对列表中的元素进行合并输出
    print("COMMAND:%s" % (":".join(Command)))
    # 调用 print_success 函数输出消息
    print_success("MAKE Command Successfully.") # 输出成功

    # 如果列表长度大于10并且i的值为..\，该条件不会成立
    if len(Command) > 10 and i== "..\\":
        print_success("Verify String:", end="")
        print(i)
    # 否则打印 Fuck
    else:
        print_success("Fuck")








