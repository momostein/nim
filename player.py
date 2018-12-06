# Project Objectorientatie: NIM - Player classes
# Brecht Ooms / 2 ELO-ICT / 2018

import tkinter as tk


class SpelerFrame(tk.Frame):
    """Basisframe voor een speler/AI"""

    def __init__(self, master=None, label='Leeg'):
        super().__init__(master)

        self._lbl_label = tk.Label(self, text=label)

        # StringVar kan niet private zijn
        # Error tijdens sluiten
        self.name = tk.StringVar()
        self.name.set("")
        self._ent_name = tk.Entry(self,
                                  textvariable=self.name)

        self._zetten = tk.IntVar(value=0)
        self._ent_zetten = tk.Entry(self,
                                    textvariable=self._zetten,
                                    state=tk.DISABLED)

        self._lbl_label.grid(row=0)
        self._ent_name.grid(row=1)
        self._ent_zetten.grid(row=2)

    def zet(self):
        print("zet")
        self._zetten.set(self._zetten.get() + 1)
