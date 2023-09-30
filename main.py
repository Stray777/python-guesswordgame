import tkinter as tk
from gui import WordGuessGame


if __name__ == '__main__':
    root = tk.Tk()
    game = WordGuessGame(root)
    root.mainloop()
