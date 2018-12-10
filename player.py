# Project Objectorientatie: NIM - Player classes
# Brecht Ooms / 2 ELO-ICT / 2018

import tkinter as tk


class _BaseColumn():
    """Basisframe voor een speler/AI"""

    def __init__(self, master=None, label='Leeg'):
        self._master = master

        # True: wacht voor user input (Speler)
        # False: Speel automatisch (AI)
        self._human = False

        # Label bovenaan
        self._lbl_label = tk.Label(master, text=label)

        self._name = tk.StringVar()
        self._name.set("")
        self._ent_name = tk.Entry(master,
                                  textvariable=self._name,
                                  state=tk.DISABLED)

        # Aantal zetten
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

    def getZet(self, state):
        return None

    def zet(self):
        self._zetten.set(self._zetten.get() + 1)

    def start(self, playercount=-1):
        self._setName()

        self._ent_name.config(state=tk.DISABLED)
        self._playercount = playercount

    def focus(self):
        self._ent_name.focus_set()

    @property
    def human(self):
        return self._human

    @property
    def name(self):
        return self._name.get()

    # Private functie die de naam eventueel veranderd
    def _setName(self):
        pass


class Speler(_BaseColumn):
    """Frame voor een speler"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Een speler is weldegelijk een mens en zal dus wachten op user input
        self._human = True

        # Enable de name entry
        self._ent_name.config(state=tk.NORMAL)


class RandomAI(_BaseColumn):
    """Een AI die willekeurige zetten doet"""

    def _setName(self):
        self._name.set('Hall')

    def getZet(self, state):
        # TODO: Program AI
        # Test zet (kan errors creëren)
        return (0, 1)
