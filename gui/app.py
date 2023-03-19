import os
from tkinter import *
from tkinter import ttk


class App:
    def __init__(self):
        self.__root = Tk()
        self.__root.title("3D walking simulator")
        self.center(500, 400)
        self.setup_tabs()
        self.setup_sim_tab()
        self.setup_vis_tab()

        # XXX DEBUG
        self._add_debug_borders()

    def center(self, width, height):
        x = int((self.__root.winfo_screenwidth() / 2) - (width / 2))
        y = int((self.__root.winfo_screenheight() / 2) - (height / 2))
        self.__root.geometry(f"{width}x{height}+{x}+{y}")

    def setup_tabs(self):
        self.__content = ttk.Frame(self.__root, padding="10 10 10 10")
        self.__content.place(relwidth=1, relheight=1)
        self.__content.columnconfigure(0, weight=1)
        self.__content.rowconfigure(1, weight=1)

        self.__win_title = ttk.Label(
            self.__content, text="3D Walking simulator", padding=" 20 0 20 0"
        )
        self.__win_title.grid(row=0, column=0)

        self.__tabs = ttk.Notebook(self.__content)
        self.__tabs.grid(row=1, column=0, sticky=NSEW)

        self.__sim_tab = ttk.Frame(
            self.__tabs, relief="ridge", padding="5 5 5 5"
        )
        self.__tabs.add(self.__sim_tab, text="Simulation")

        self.__vis_tab = ttk.Frame(
            self.__tabs, relief="ridge", padding="5 5 5 5"
        )
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

        self.__vis_algo_var = StringVar()
        algo_select = ttk.Combobox(
            self.__vis_tab, textvariable=self.__vis_algo_var
        )
        algo_select["values"] = ("GA", "PPO")
        algo_select.grid(row=0, column=1, sticky=(W, E))
        algo_select.bind(
            "<<ComboboxSelected>>", self._vis_tab_handle_algo_select
        )

        vis_files_label = ttk.Label(self.__vis_tab, text="Solutions")
        vis_files_label.grid(row=1, column=0, columnspan=2, sticky=(W, E))

        self.__vis_files_var = StringVar()
        self.__vis_files = Listbox(
            self.__vis_tab, listvariable=self.__vis_files_var
        )
        self.__vis_files.grid(
            row=2, column=0, columnspan=2, sticky=(W, E, N, S)
        )
        self.__vis_files.bind(
            "<<ListboxSelect>>", self._vis_tab_handle_files_select
        )

        self.__vis_btn = ttk.Button(
            self.__vis_tab,
            text="Visualize",
            command=self._vis_tab_visualize,
            state="disabled",
        )
        self.__vis_btn.grid(row=3, column=1, sticky=(E, S))

    def _add_debug_borders(self):
        for e in self.__content, self.__win_title:
            e["borderwidth"] = 3
            e["relief"] = "solid"

    def _vis_tab_handle_algo_select(self, ev):
        algo = self.__vis_algo_var.get().lower()
        rootdir = os.path.join("solutions", algo)
        self.__vis_btn.state(["disabled"])

        files = []
        for file in os.listdir(rootdir):
            files.append(file)

        self.__vis_files_var.set(files)

    def _vis_tab_handle_files_select(self, ev):
        if len(self.__vis_files.curselection()) > 0:
            self.__vis_btn.state(["!disabled"])

    def _vis_tab_visualize(self):
        print(self.__vis_files.curselection())

    def run(self):
        self.__root.mainloop()


if __name__ == "__main__":
    app = App().run()
