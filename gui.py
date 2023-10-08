import tkinter as tk
import random
from database import Database


class WordGuessGame:
    def __init__(self, root):
        # 初始主窗口
        self.root = root
        self.root.title("猜词游戏")
        # 窗口居中
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"600x250+{(self.screen_width - 600) // 2}+{(self.screen_height - 250) // 2}")

        # 容器
        self.frame1 = tk.Frame(self.root)
        self.frame1.pack()
        self.frame2 = tk.Frame(self.root)
        self.frame2.pack(pady='30')

        # 容器1
        self.button2 = tk.Button(self.frame1, text='获取单词/跳过单词', command=self.get_word)
        self.button2.pack(pady='10')
        self.label1 = tk.Label(self.frame1)
        self.label1.pack()

        # 容器2
        self.label2 = tk.Label(self.frame2, text="请输入你猜的单词:")
        self.label2.pack()
        self.entry1 = tk.Entry(self.frame2)
        self.entry1.pack()
        self.button1 = tk.Button(self.frame2, text="提交", command=self.compare_word)
        self.button1.pack(pady='5')

        # 变量
        self.word = None

    def get_word(self):
        """获取单词"""
        with open('word.txt', 'r') as file:
            # 判断有多少单词行
            lines = file.readlines()
            line_count = len(lines)

            # 读取随机一行的单词
            file.seek(0)
            line = random.randint(1, line_count)
            for i in range(line - 1):
                file.readline()
            self.word = file.readline().strip()

            # label1显示乱序单词
            wordlist = list(self.word)
            random.shuffle(wordlist)
            word_out_of_order = "".join(wordlist)
            self.label1.config(text=f"乱序单词为: {word_out_of_order}")

    def compare_word(self):
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

    def pop_up_window(self, title='', label_text='', button_text=''):
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
