import tkinter as tk
from gui import WordGuessGame
from database import Database

if __name__ == '__main__':
    root = tk.Tk()  # 实例化主窗口
    db = Database()  # 实例化数据库对象
    game = WordGuessGame(root, db)  # 实例化猜词游戏对象

    db.connect_database()  # 连接数据库
    root.mainloop()  # 运行主窗口
    db.close_database()  # 关闭数据库
