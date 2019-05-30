import tkinter as tk
from tkinter import messagebox
from tkinter import *

def do_job():
    messagebox.showinfo(message = "myRedisManager Version 0.0.1", title = "myRedisManager")

def window_config(window_width, window_height, root_window):
    def redis_connect():
        # 异常处理
        redis_address = Entry_address.get()
        redis_port = Entry_port.get()
        redis_password = Entry_password.get()
        if redis_address and redis_port and redis_password:
            messagebox.showinfo(message=(redis_address + redis_port + redis_password), title='输入正常')
            Entry_address.delete(0, END)
            Entry_port.delete(0, END)
            Entry_password.delete(0, END)
        else:
            messagebox.showinfo(message='输入不能为空', title='异常提示')
            Entry_address.delete(0, END)
            Entry_port.delete(0, END)
            Entry_password.delete(0, END)
        # message = 'redis_address:' + redis_address + '\n' + 'port' + redis_port + 'password' + redis_password

        # messagebox.showinfo(message=message, title="myRedisManager")

    # 配置窗口为居中
    width_screen = root_window.winfo_screenwidth()
    height_screen = root_window.winfo_screenheight()
    window_x = (width_screen/2) - (window_width/2)
    window_y = (height_screen/2) - (window_height/2)
    root_window.geometry('%dx%d+%d+%d' % (window_width, window_height, window_x, window_y))

    # 配置菜单栏
    menu_bar = tk.Menu(root_window)
    root_window['menu'] = menu_bar
    # tearoff = False选项一定要加上，否则菜单会撕裂出去
    menu_son_1 = tk.Menu(menu_bar, tearoff = False)
    menu_son_2 = tk.Menu(menu_bar, tearoff = False)

    menu_son_1.add_command(label='打开')
    menu_son_1.add_command(label='保存')
    menu_son_2.add_command(label='复制')
    menu_son_2.add_command(label='删除')

    menu_bar.add_cascade(label='文件', menu=menu_son_1)
    menu_bar.add_cascade(label='编辑', menu=menu_son_2)
    menu_bar.add_cascade(label='关于', command=do_job)

    # 窗口标题
    root_window.title('myRedisManager')
    # root_window.configure(background='white')

    # 界面布局
    Label_address = Label(root_window, text='Redis服务器地址：')
    Label_address.grid(row=0,column=0)
    Entry_address = Entry(root_window)
    Entry_address.grid(row=0,column=1)
    Label_port = Label(root_window, text='Redis服务器端口号：')
    Label_port.grid(row=1, column=0)
    Entry_port = Entry(root_window)
    Entry_port.grid(row=1, column=1)
    Label_password = Label(root_window, text='Redis服务器密码：')
    Label_password.grid(row=2, column=0)
    Entry_password = Entry(root_window, show='*')
    Entry_password.grid(row=2, column=1)
    button_connect = Button(text='连接', command=redis_connect)
    button_connect.grid(row=3, column=0)

root_window = tk.Tk()
window_config(500, 300, root_window)
root_window.mainloop()