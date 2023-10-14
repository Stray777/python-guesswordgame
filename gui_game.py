import tkinter as tk
import random
import pymysql
from tkinter import messagebox
from database import DelError


class GameGUI:
    def __init__(self, root, db):
        # 数据库
        self.db = db
        # 单词
        self.word = None

        # 初始主窗口
        self.root = root
        self.root.title("猜词游戏")
        # 窗口居中
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"600x250+{(self.screen_width - 600) // 2}+{(self.screen_height - 250) // 2}")

        # 容器1
        self.frame1 = tk.Frame(self.root)
        self.frame1.pack()
        self.button2 = tk.Button(self.frame1, text='获取单词/跳过单词', command=self.get_word)
        self.button2.pack(pady='10')
        self.label1 = tk.Label(self.frame1)
        self.label1.pack()

        # 容器2
        self.frame2 = tk.Frame(self.root)
        self.frame2.pack(pady='30')
        self.label2 = tk.Label(self.frame2, text="请输入你猜的单词:")
        self.label2.pack()
        self.entry1 = tk.Entry(self.frame2)
        self.entry1.pack()
        self.button1 = tk.Button(self.frame2, text="提交", command=self.compare_word)
        self.button1.pack(pady='5')

        # 容器3
        self.frame3 = tk.Frame(self.root)
        self.frame3.pack(side="left")
        self.changeword_button = tk.Button(self.frame3, text="更改单词库", command=self.change_word)
        self.changeword_button.pack(padx='5')

    def change_word(self) -> None:
        """更改单词库按钮"""
        def add_word() -> None:
            """添加单词"""
            word = add_entry.get()
            if word == '':
                tk.messagebox.showerror("添加单词失败", "输入框为空")
                return None
            data = {
                "word": word
            }
            try:
                self.db.insert_data("word_tb", data)
                add_entry.delete(0, tk.END)
                self.pop_up_window("成功", f"已添加单词:{word}", "返回")
            except pymysql.Error as e:
                tk.messagebox.showerror("添加单词失败", str(e))

        def del_word() -> None:
            """删除单词"""
            word = del_entry.get()
            try:
                self.db.del_data("word_tb", word, "word")
                del_entry.delete(0, tk.END)
                self.pop_up_window("成功", f"已删除单词:{word}", "返回")
            except DelError as e:
                messagebox.showerror(str(e), "不存在此数据")

        def check_word() -> None:
            """查看单词库"""
            # 弹窗
            popup = tk.Toplevel(toplevel)
            popup.title("单词库")
            popup.geometry(f"240x350+{(self.screen_width - 240) // 2}+{(self.screen_height - 350) // 2}")

            # 获取单词
            word_tuple_list = list(self.db.get_data_all("word_tb"))

            # 创建组件
            word_txt = tk.Text(popup)
            for oneword_tuple in word_tuple_list:
                word_txt.insert(tk.END, f"{oneword_tuple[0]}\n")
            txt_label = tk.Label(popup, text="滑轮滚动向下继续查看")

            # 组件布局
            word_txt.pack()
            txt_label.pack(pady='5')

        toplevel = tk.Toplevel(self.root)
        toplevel.title("单词库")
        toplevel.geometry(f"300x120+{(self.screen_width - 300) // 2}+{(self.screen_height - 120) // 2}")

        # 创建组件
        add_label = tk.Label(toplevel, text="输入要添加的单词:")
        add_entry = tk.Entry(toplevel)
        add_button = tk.Button(toplevel, text="添加", command=add_word)
        del_label = tk.Label(toplevel, text="输入要删除的单词:")
        del_entry = tk.Entry(toplevel)
        del_button = tk.Button(toplevel, text="删除", command=del_word)
        check_word_button = tk.Button(toplevel, text="查看单词库", command=check_word)

        # 组件布局
        add_label.grid(row=0, column=0, pady="10")
        add_entry.grid(row=0, column=1)
        add_button.grid(row=0, column=2)
        del_label.grid(row=1, column=0)
        del_entry.grid(row=1, column=1)
        del_button.grid(row=1, column=2)
        check_word_button.grid(row=2, column=1, pady='5')

    def get_word(self) -> None:
        """获取单词"""
        self.word = self.db.get_data_random('word_tb')

        # label1显示乱序单词
        wordlist = list(self.word)
        random.shuffle(wordlist)
        word_out_of_order = "".join(wordlist)
        self.label1.config(text=f"乱序单词为: {word_out_of_order}")

    def compare_word(self) -> None:
        if self.word is None:
            self.pop_up_window('错误', '尚未获取单词！', '返回')
        input_word = self.entry1.get().lower()
        if input_word == '':
            pass
        elif input_word == '0':
            pass
        elif input_word == '1':
            pass
        elif input_word == self.word:
            self.entry1.delete(0, tk.END)
            self.pop_up_window('答对啦', '恭喜你！答对啦！', '下一个')
            self.get_word()
        else:
            self.entry1.delete(0, tk.END)
            self.pop_up_window('答错了', '真遗憾...答错了', '重新作答')

    def pop_up_window(self, title='', label_text='', button_text='') -> None:
        """弹窗"""
        # 弹窗主窗口
        toplevel = tk.Toplevel(self.root)
        toplevel.title(title)
        toplevel.geometry(f"240x90+{(self.screen_width - 240) // 2}+{(self.screen_height - 90) // 2}")

        # 组件
        label = tk.Label(toplevel, text=label_text)
        label.pack(pady='5')  # title高度为32，也就是90-32=58，因此要距离上下各58/2=29
        button = tk.Button(toplevel, text=button_text, command=toplevel.destroy)
        button.pack()
