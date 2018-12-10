# Project Objectorientatie: NIM - Player classes
# Brecht Ooms / 2 ELO-ICT / 2018

import tkinter as tk


class _BaseColumn():
    """Basisframe voor een speler/AI"""

    def __init__(self, master=None, label='Leeg'):
        self._master = master
        self._lbl_label = tk.Label(master, text=label)

        # StringVar kan niet private zijn
        # Error tijdens sluiten
        self.name = tk.StringVar()
        self.name.set("")
        self._ent_name = tk.Entry(master,
                                  textvariable=self.name)

        self._zetten = tk.IntVar(value=0)
        self._ent_zetten = tk.Entry(master,
                                    textvariable=self._zetten,
                                    state=tk.DISABLED)

    def grid(self, column=0, row=0):
        # Zet alle widgets in de juiste column
        self._lbl_label.grid(row=row,
                             column=column,
                             sticky='nesw')

        self._ent_name.grid(row=row + 1,
                            column=column, padx=2,
                            sticky='nesw')

        self._ent_zetten.grid(row=row + 2,
                              column=column,
                              padx=2, sticky='nesw')

        # Maak de colom resizeable
        self._master.columnconfigure(column, weight=1)

    def zet(self):
        self._zetten.set(self._zetten.get() + 1)

    def start(self):
        pass

    def focus(self):
        self._ent_name.focus_set()


class SpelerColumn(_BaseColumn):
    """Frame voor een speler"""

    def start(self):
        self._ent_name.config(state=tk.DISABLED)


class AIColumn(_BaseColumn):
    """Frame voor een AI"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._ent_name.config(state=tk.DISABLED)

    def start(self):
        self.name.set('Hall')

    def getZet(self, state):
        # TODO: Bereken volgende zet en return (key, amount)
        pass
