# 2019.5.30
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import redis
import re
import threading
import time
import logging
logging.basicConfig(level=logging.INFO)

redis_cl = None

def thread_test(r, tree):
    # while True:
        x = tree.get_children()
        for i in x:
            tree.delete(i)
        all_keys = r.keys()
        for i in all_keys:
            tree.insert('', 'end', values=(bytes.decode(i), bytes.decode(r.get(i))))
        time.sleep(1)

def exit_button():
    """
    退出按钮方法
    :return:
    """
    exit()

def do_job():
    """
    占位
    :return:
    """
    messagebox.showinfo(message = "myRedisManager Version 0.0.1", title = "myRedisManager")

def detect_ip_input(redis_address):
    """
    用正则表达式检查IP地址输入是否正确
    :param redis_address:
    :return:1：输入正确 0：输入错误
    """
    if re.findall(r'\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b',redis_address):
        return 1
    else:
        return 0

def window_config(window_width, window_height, root_window):
    """
    窗口配置方法
    :param window_width:
    :param window_height:
    :param root_window:
    :return:
    """
    def redis_connect():
        # 获取entry控件内的数据
        redis_address = Entry_address.get()
        redis_port = Entry_port.get()
        redis_password = Entry_password.get()
        redis_DB_num = Entry_DB_num.get()
        # 尝试连接
        if redis_address and redis_port and redis_password and detect_ip_input(redis_address):
            # 清除输入框内容
            Entry_address.delete(0, END)
            Entry_port.delete(0, END)
            Entry_password.delete(0, END)
            Entry_DB_num.delete(0, END)
            try:
                r = redis.StrictRedis(host=redis_address, port=redis_port, password=redis_password, db=redis_DB_num,
                                      socket_connect_timeout=3)
                logging.info(str(r.get('NetStatus')))
                t1 = threading.Thread(target=thread_test, args=(r, tree))
                t1.setDaemon(True)
                t1.start()
            except ConnectionRefusedError as e:
                messagebox.showinfo(message='错误IP地址提示:\n' + str(e), title='提示')
            except redis.exceptions.ConnectionError as e:
                messagebox.showinfo(message='错误端口号提示：\n' + str(e), title='提示')
            except redis.exceptions.ResponseError as e:
                messagebox.showinfo(message='错误连接密码提示：\n' + str(e), title='提示')
            except redis.exceptions.TimeoutError as e:
                messagebox.showinfo(message='连接超时提示：\n' + str(e), title='提示')
        else:
            messagebox.showinfo(message='输入错误，请检查', title='异常提示')
            Entry_address.delete(0, END)
            Entry_port.delete(0, END)
            Entry_password.delete(0, END)
            Entry_DB_num.delete(0, END)

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
    Label_address.grid(row=0, column=0, sticky=W)
    Entry_address = Entry(root_window)
    Entry_address.grid(row=0, column=1, sticky=E)

    Label_port = Label(root_window, text='Redis服务器端口号：')
    Label_port.grid(row=1, column=0, sticky=W)
    Entry_port = Entry(root_window)
    Entry_port.grid(row=1, column=1, sticky=E)

    Label_DB_num = Label(root_window, text='RedisDB号：')
    Label_DB_num.grid(row=2, column=0, sticky=W)
    Entry_DB_num = Entry(root_window)
    Entry_DB_num.grid(row=2, column=1, sticky=E)

    Label_password = Label(root_window, text='Redis服务器密码：')
    Label_password.grid(row=3, column=0, sticky=W)
    Entry_password = Entry(root_window, show='*')
    Entry_password.grid(row=3, column=1, sticky=E)

    button_connect = Button(text='连接', command=redis_connect)
    button_connect.grid(row=4, column=0, sticky=W+E+N+S)
    button_exit = Button(text='退出', command=exit_button)
    button_exit.grid(row=4, column=1, sticky=W + E + N + S)

    # 默认值配置区
    Entry_address.insert(END, '')
    Entry_port.insert(END, '')
    Entry_DB_num.insert(END, '')
    Entry_password.insert(END, '')

    tree = ttk.Treeview(root_window, columns=['1', '2'], show='headings')
    tree.heading('1', text='Key')
    tree.heading('2', text='Value')
    tree.grid(row=5, column=0, columnspan=2, sticky=W+E+N+S)

    # 滚动条控件
    vbar = ttk.Scrollbar(root_window, orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=vbar.set)
    vbar.grid(row=5, column=1, columnspan=3, sticky=S + N + E)

if __name__ == '__main__':
    root_window = tk.Tk()
    window_config(405, 350, root_window)
    root_window.mainloop()