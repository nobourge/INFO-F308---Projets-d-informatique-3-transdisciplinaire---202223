import os
from tkinter import *
from tkinter import messagebox, ttk


class SimView(ttk.Frame):
    def __init__(self, master=None, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._setup()

    def _setup(self):
        env_select_label = ttk.Label(self, text="Environment")
        env_select_label.grid(row=0, column=0, padx="0 10")

        self.__train_algo_var = StringVar()
        env_select = ttk.Combobox(
            self, textvariable=self.__train_algo_var
        )
        env_select["values"] = ["default", "moon", "mars"]
        env_select.grid(row=0, column=1, sticky=(W, E))
