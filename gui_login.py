import tkinter as tk
import tkinter.messagebox
from gui_game import GameGUI
import pymysql


class LoginGUI:
    def __init__(self, root, db):
        # 数据库
        self.db = db

        # 主界面
        self.root = root
        self.root.title("登录")
        # 窗口居中
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"265x125+{(self.screen_width - 265) // 2}+{(self.screen_height - 125) // 2}")

        # 创建组件
        self.username_label = tk.Label(self.root, text="用户名:")
        self.password_label = tk.Label(self.root, text="密码:")
        self.username_entry = tk.Entry(self.root)
        self.password_entry = tk.Entry(self.root, show="*")
        self.login_button = tk.Button(self.root, text="登录", command=self.login)
        self.register_button = tk.Button(self.root, text="注册", command=self.register)

        # 布局组件
        self.username_label.grid(row=0, column=0, sticky='e', padx='15')
        self.password_label.grid(row=1, column=0, sticky='e', padx='15')
        self.username_entry.grid(row=0, column=1, pady='15')
        self.password_entry.grid(row=1, column=1)
        self.login_button.grid(row=2, column=1, pady='5', sticky='w')
        self.register_button.grid(row=2, column=1, sticky='e')

    def register(self) -> None:
        """注册按钮命令"""
        def register_success() -> None:
            """注册页面提交按钮"""
            username = username_entry.get()
            password = password_entry.get()
            data = {
                'user_name': username,
                'user_password': password
            }
            columns = [
                "id INT AUTO_INCREMENT PRIMARY KEY",
                "word VARCHAR(40) UNIQUE",
                "frequency INT NOT NULL DEFAULT 1",
                # "FOREIGN KEY (word) REFERENCS word_tb(word)"
            ]

            try:
                self.db.insert_data('user_tb', data)
                self.db.create_table(f'{username}_word_tb', columns)
                toplevel.destroy()
                tk.messagebox.showinfo("成功", "注册成功")
            except pymysql.Error:
                tk.messagebox.showerror("错误", "用户名已存在，请重新填写")

        # 弹窗主窗口
        toplevel = tk.Toplevel(self.root)
        toplevel.title("注册")
        toplevel.geometry(f"280x120+{(self.screen_width - 280) // 2}+{(self.screen_height - 120) // 2}")

        # 创建组件
        username_label = tk.Label(toplevel, text="注册用户名:")
        password_label = tk.Label(toplevel, text="注册密码:")
        username_entry = tk.Entry(toplevel)
        password_entry = tk.Entry(toplevel)
        register_button = tk.Button(toplevel, text="注册", command=register_success)

        # 布局组件
        username_label.grid(row=0, column=0, sticky='e', padx='15')
        password_label.grid(row=1, column=0, sticky='e', padx='15')
        username_entry.grid(row=0, column=1, pady='15')
        password_entry.grid(row=1, column=1)
        register_button.grid(row=2, column=1, pady='5')

    def login(self) -> None:
        """登录按钮命令"""
        username_entry = self.username_entry.get()
        password_entry = self.password_entry.get()
        data = self.db.get_data('user_tb', username_entry, 'user_name')
        if data is None:
            tk.messagebox.showerror("错误", "用户名不存在")
        elif data[1] != password_entry:
            tk.messagebox.showerror("错误", "密码错误")
        else:
            self.root.destroy()  # 关闭登录窗口
            game_root = tk.Tk()  # 创建游戏窗口
            GameGUI(game_root, self.db)  # 实例化游戏对象
            game_root.mainloop()  # 运行主窗口
