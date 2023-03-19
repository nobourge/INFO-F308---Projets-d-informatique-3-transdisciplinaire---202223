from tkinter import *
from tkinter import ttk


class App:
    def __init__(self):
        self.__root = Tk()        
        self.__mainframe = ttk.Frame(self.__root, padding="3 3 12 12")

    def run(self):
        self.__root.mainloop()


if __name__ == "__main__":
    app = App().run()
