import tkinter as tk
from gui_login import LoginGUI
from database import Database

if __name__ == '__main__':
    db = Database()  # 实例化数据库对象
    db.connect_database()  # 连接数据库

    root_login = tk.Tk()  # 创建登录窗口
    login = LoginGUI(root_login, db)  # 实例化登录对象
    root_login.mainloop()  # 运行登录界面

    db.close_database()  # 关闭数据库
