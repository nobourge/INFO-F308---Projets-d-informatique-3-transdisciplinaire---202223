import os
from tkinter import *
from tkinter import ttk


class App:
    def __init__(self):
        self.__root = Tk()
        self.__root.title("3D walking simulator")
        self.setup_tabs()
        self.setup_sim_tab()
        self.setup_vis_tab()

        # XXX DEBUG
        self._add_debug_borders()

    def setup_tabs(self):
        self.__content = ttk.Frame(self.__root, padding="10 10 10 10")
        self.__content.place(relwidth=1, relheight=1)
        self.__content.columnconfigure(0, weight=1)
        self.__content.rowconfigure(1, weight=1)

        self.__win_title = ttk.Label(self.__content, text="3D Walking simulator", padding=" 20 0 20 0")
        self.__win_title.grid(row=0, column=0)

        self.__tabs = ttk.Notebook(self.__content)
        self.__tabs.grid(row=1, column=0, sticky=NSEW)

        self.__sim_tab = ttk.Frame(self.__tabs, relief="ridge", padding="5 5 5 5")
        self.__tabs.add(self.__sim_tab, text="Simulation")

        self.__vis_tab = ttk.Frame(self.__tabs, relief="ridge", padding="5 5 5 5")
        self.__tabs.add(self.__vis_tab, text="Visualisation")

    def setup_sim_tab(self):
        pass

    def setup_vis_tab(self):
        self.__vis_tab.rowconfigure(0, pad="5")
        self.__vis_tab.rowconfigure(2, weight=1)
        self.__vis_tab.rowconfigure(3, pad="5")
        self.__vis_tab.columnconfigure(1, weight=1)

        algo_select_label = ttk.Label(self.__vis_tab, text="Algorithm:")
        algo_select_label.grid(row=0, column=0, padx="0 10")

        algo_var = StringVar()
        algo_select = ttk.Combobox(self.__vis_tab, textvariable=algo_var)
        algo_select["values"] = ("GA", "PPO")
        algo_select.grid(row=0, column=1, sticky=(W,E))

        vis_files_label = ttk.Label(self.__vis_tab, text="Solutions")
        vis_files_label.grid(row=1, column=0, columnspan=2, sticky=(W,E))

        # self.__sol_files_box = Listbox(self.__vis_tab)
        # self.__sol_files_box.grid(column=0, row=0)
        # rootdir = '../solutions/'
        # for i, file in enumerate(os.listdir(rootdir), 0):
        #     d = os.path.join(rootdir, file)
        #     self.__sol_files_box.insert(i, file)

        vis_var = StringVar(value=["20230319-114700", "20230319-150321"])
        vis_files = Listbox(self.__vis_tab, listvariable=vis_var)
        vis_files.grid(row=2, column=0, columnspan=2, sticky=(W,E,N,S))

        vis_btn = ttk.Button(self.__vis_tab, text="Visualize")
        vis_btn.grid(row=3, column=1, sticky=(E,S))

    def _add_debug_borders(self):
        for e in self.__content, self.__win_title:
            e["borderwidth"] = 3
            e["relief"] = "solid" 

    def run(self):
        self.__root.mainloop()


if __name__ == "__main__":
    app = App().run()
