import os
from tkinter import *
from tkinter import messagebox, ttk


class SimView(ttk.Frame):
    def __init__(self, master=None, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._setup()
        self._algo_options_cbs = dict()
        self._algo_options_cbs["Algorithme génétique"] = (self._show_ga_options, self._hide_ga_options)
        self._algo_options_cbs["PPO"] = (self._show_ppo_options, self._hide_ppo_options)

    def _setup(self):
        # Environment selection
        self._env_select_label = ttk.Label(self, text="Environnement")
        #  self._add_debug_borders(self._env_select_label)
        self._env_select_label.grid(row=0, column=0, padx="0 10", sticky=W)
        self.__env_var = StringVar()
        self._env_select_field = ttk.Combobox(
                self, textvariable=self.__env_var
                )
        self._env_select_field["values"] = ["default", "lune", "mars"]
        self._env_select_field.grid(row=0, column=1, sticky=(W, E))
        
        # Creature config
        self._creature_select_lbl = ttk.Label(self, text="Choix de la créature")
        self._creature_select_lbl.grid(row=1, column=0, padx="0 10", sticky=W)
        self.__creature_var = StringVar()
        self._creature_select_field = ttk.Combobox(
            self, textvariable=self.__creature_var
        )
        self._creature_select_field["values"] = ["quadrupède", "bipède"]
        self._creature_select_field.grid(row=1, column=1, sticky=(W, E))

        # Algorithm config
        self._algo_config_lbl = ttk.Label(self, text="Configuration algorithme d'apprentissage")
        self._algo_config_lbl.grid(row=2, column=0, padx="0 10", columnspan=2, sticky=W)
        self._algo_select_lbl = ttk.Label(self, text="Choix de l'algorithme")
        self._algo_select_lbl.grid(row=3, column=0, padx="0 10", sticky=W)
        self.__algo_var = StringVar()
        self._algo_select_field = ttk.Combobox(
            self, textvariable=self.__algo_var
        )
        self._algo_select_field["values"] = ["Algorithme génétique", "PPO"]
        self._algo_select_field.grid(row=3, column=1, sticky=(W, E))
        
        self._algo_select_field.bind(
            "<<ComboboxSelected>>", self._handle_select_algo_field
        )

    def _handle_select_algo_field(self, ev):
        self._algo_options_cbs[self.__algo_var.get()][0]()

    def _show_ga_options(self):
        self._ga_pop_lbl = ttk.Label(self, text="Taille population")
        self._ga_pop_lbl.grid(row=4, column=0, padx="0 10", sticky=W)
        self.__ga_pop_var = StringVar()
        self._ga_pop_field = ttk.Entry(self, textvariable=self.__ga_pop_var)
        self._ga_pop_field.grid(row=4, column=1, sticky=(W, E))

    def _hide_ga_options(self):
        self._ga_pop_lbl.grid_forget()
        self._ga_pop_field.grid_forget()

    def _show_ppo_options(self):
        self._algo_options_cbs[self.__algo_var.get()][1]()

    def _hide_ppo_options(self):
        self._ga_pop_lbl.grid_forget()
        self._ga_pop_field.grid_forget()


    def _add_debug_borders(self, elem):
            elem["borderwidth"] = 3
            elem["relief"] = "solid"
