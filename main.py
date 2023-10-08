import tkinter as tk
from gui import WordGuessGame
from database import Database

if __name__ == '__main__':
    db = Database()  # 实例化数据库对象
    db.connect_database()  # 运行数据库

    root = tk.Tk()  # 实例化主窗口
    game = WordGuessGame(root)  # 实例化猜词游戏对象
    root.mainloop()  # 运行主窗口

    db.close_database()  # 关闭数据库
