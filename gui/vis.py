import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk

from gui.shell import ShellCommandDialog

from loguru import logger

class VisView(ttk.Frame):
    def __init__(self, master=None, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._setup_configuration()

    def _setup_configuration(self):
        self.rowconfigure(0, pad="5")
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, pad="5")
        self.columnconfigure(1, weight=1)

        # Algo Select
        ttk.Label(self, text="Algorithm:").grid(row=0, column=0, padx="0 10")
        self._selected_algo_var = tk.StringVar()
        self._select_algo_field = ttk.Combobox(
            self, textvariable=self._selected_algo_var
        )
        self._select_algo_field["values"] = ("GA", "PPO")
        self._select_algo_field.bind(
            "<<ComboboxSelected>>", self._handle_select_algo_field
        )
        self._select_algo_field.grid(row=0, column=1, sticky=tk.EW)

        # Solutions Files
        ttk.Label(self, text="Solutions").grid(
            row=1, column=0, columnspan=2, sticky=tk.EW
        )
        self._solutions_var = tk.StringVar()
        logger.debug(f"self._solutions_var: {self._solutions_var.get()}")
        logger.debug(f"self._solutions_var: {self._solutions_var}")
        self._solutions_lbox = tk.Listbox(
            self, listvariable=self._solutions_var
        )
        self._solutions_lbox.bind(
            "<<ListboxSelect>>", self._handle_selected_solution
        )
        self._solutions_lbox.grid(
            row=2, column=0, columnspan=2, sticky=tk.NSEW
        )

        # Vis Button
        self._vis_btn = ttk.Button(
            self,
            text="Visualize",
            command=self._handle_vis_btn,
            state="disabled",
        )
        self._vis_btn.grid(row=3, column=1, sticky=tk.SE)

    @property
    def selected_algo(self):
        return self._selected_algo_var.get().lower()

    @property
    def selected_solution(self):
        indexes = self._solutions_lbox.curselection()
        if len(indexes) == 0:
            return None

        return self._solutions_lbox.get(indexes[0])

    @property
    def walkingsim_command(self):
        logger.debug("walkingsim_command()")
        # NOTE: -u is important for showing the output in the dialog
        cmd = [sys.executable, "-u", "-m", "walkingsim", "visualize"]
        if self.selected_algo is not None:
            cmd += ["--algorithm", self.selected_algo]

        if self.selected_solution is not None:
            cmd += [self.selected_solution]

        logger.debug(f"cmd: {cmd}")

        return cmd

    def _handle_select_algo_field(self, ev):
        logger.debug("handle_select_algo_field()")
        # os.path is the path to the python file that is running this
        # code (in this case, vis.py) so we need to go up one level
        # to get to the solutions directory
        logger.debug(f"os.path: {os.path}")
        # <module 'ntpath' from 'C:\\Users\\bourg\\anaconda3\\envs\\infof308-chrono\\lib\\ntpath.py'>
        # this means that we are on windows and that the path is a
        # module from the standard library (ntpath) and not a file
        # from the project (solutions)
        # the current path is the path to the python file that is
        # running this code (in this case, vis.py)
        # for the current path to be the project root path, we should
        # have a __main__.py file in the project root directory and
        # run the project with python -m project_name

        rootdir = os.path.join("solutions", self.selected_algo)

        #relative path :
        # relative_path_to_solutions = "../solutions"
        # rootdir = os.path.join(relative_path_to_solutions, self.selected_algo)

        logger.debug(f"rootdir: {rootdir}")
        if os.path.exists(rootdir):
            self._solutions_var.set(os.listdir(rootdir))
            logger.debug(f"os.listdir(rootdir): {os.listdir(rootdir)}")
            logger.debug(f"self._solutions_var: {self._solutions_var.get()}")
        else:
            logger.debug(f"rootdir: {rootdir} does not exist")
            logger.info(f"No solution for {self.selected_algo} found")
            self._solutions_var.set([])

        self._vis_btn.state(["disabled"])

    def _handle_selected_solution(self, ev):
        if len(self._solutions_lbox.curselection()) > 0:
            self._vis_btn.state(["!disabled"])

    def _handle_vis_btn(self):
        if self.selected_solution is None:
            messagebox.showwarning(
                title="No Solution", message="You must select a solution"
            )
        else:
            ShellCommandDialog(self, self.walkingsim_command)
