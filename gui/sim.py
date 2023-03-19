import os
from tkinter import *
from tkinter import messagebox, ttk


class SimView(ttk.Frame):
    def __init__(self, master=None, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._setup()

    def _setup(self):
        # Environment selection
        env_select_label = ttk.Label(self, text="Environnement")
        env_select_label.grid(row=0, column=0, padx="0 10")
        self.__env_var = StringVar()
        env_select = ttk.Combobox(
            self, textvariable=self.__env_var
        )
        env_select["values"] = ["default", "lune", "mars"]
        env_select.grid(row=0, column=1, sticky=(W, E))
        
        # Creature config
        creature_select_lbl = ttk.Label(self, text="Choix de la créature")
        creature_select_lbl.grid(row=1, column=0, padx="0 10")
        self.__creature_var = StringVar()
        creature_select = ttk.Combobox(
            self, textvariable=self.__creature_var
        )
        creature_select["values"] = ["quadrupède", "bipède"]
        creature_select.grid(row=1, column=1, sticky=(W, E))

