from tkinter import *
import GUI

if __name__ == '__main__':
    root = Tk()
    root.resizable(0, 0)
    root.geometry("800x800")
    serverr = GUI.GUI(root)
    root.mainloop()
