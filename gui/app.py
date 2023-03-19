from tkinter import *
from tkinter import ttk


class App:
    def __init__(self):
        self.__root = Tk()        
        # Widget creation
        self.__content = ttk.Frame(self.__root, padding="3 3 12 12")
        self.__win_title = ttk.Label(self.__content, text="Walking simulator")
        self.__main_tabs = ttk.Notebook(self.__root)
        self.__sim_tab = ttk.Frame(self.__main_tabs)
        self.__vis_tab = ttk.Frame(self.__main_tabs)
        self.__main_tabs.add(self.__sim_tab, text='Simulation')
        self.__main_tabs.add(self.__vis_tab, text='Visualisation')
        #  self.__mainframe = ttk.Frame(self.__content,)
        # Widget grid placement
        self.__content.grid(column=0, row=0)
        self.__win_title.grid(column=0, row=0)
        self.__main_tabs.grid(column=0, row=1, columnspan=2, rowspan=1)

    def run(self):
        self.__root.mainloop()


if __name__ == "__main__":
    app = App().run()
