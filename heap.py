# Project Objectorientatie: NIM -  Heap classes
# Brecht Ooms / 2 ELO-ICT / 2018

import tkinter as tk
import random

MIN = 1
MAX = 9


class HeapFrame(tk.Frame):
    """Frame met meerdere stapels"""

    def __init__(self, master=None, heaps=3):
        super().__init__(master)

        # Maak een lijst en vul hem met stapels
        self._heaps = []

        vcmd = (self.register(self.onValidate),
                '%d', '%P', '%S')

        for i in range(heaps):
            # Maak een nieuwe stapel
            heap = Heap(self, "Stapel {:d}".format(i + 1), vcmd)

            # Zet hem in de grid
            heap.grid(column=i, row=0, padx=2, pady=2, sticky='nesw')
            self.columnconfigure(i, weight=1)

            # Voeg hem toe aan de lijst
            self._heaps.append(heap)

    def start(self):
        for heap in self._heaps:
            heap.start()

    def focus(self, key=0):
        self._heaps[key].focus()

    def onValidate(self, d, P, S):
        # %d = Type of action (1=insert, 0=delete, -1 for others)
        # %P = value of the entry if the edit is allowed
        # %S = the text string being inserted or deleted, if any

        # Validate als het een insert action is
        if d == "1":
            # Kijk na of de verandering bestaat uit digits
            if not S.isdigit():
                # Verwerp de verandering
                return False

            # Kijk na of we de hele input een integer is
            try:
                int(P)

            except ValueError:
                # Verwerp de verandering
                return False

        # Accepteer de verandering
        return True

    @property
    def state(self):
        return [heap.tokens for heap in self._heaps]


class Heap(tk.Frame):
    """Een frame voor een stapel"""

    def __init__(self, master=None, title="Stapel", vcmd=None):
        super().__init__(master)

        # Titel van de stapel
        self._lbl_title = tk.Label(self,
                                   text=title)

        # Aantal Balletjes
        self._tokens = tk.IntVar()
        self._ent_tokens = tk.Entry(self,
                                    textvariable=self._tokens,
                                    state=tk.DISABLED)

        # Inputveld
        self.strInput = tk.StringVar()
        self._ent_input = tk.Entry(self,
                                   textvariable=self.strInput,
                                   state=tk.DISABLED,
                                   validate="key",
                                   validatecommand=vcmd)

        # Voeg ze toe aan de grid
        self._lbl_title.grid(row=0, sticky='nesw')
        self._ent_tokens.grid(row=1, sticky='nesw')
        self._ent_input.grid(row=2, sticky='nesw')

    def start(self):
        self._tokens.set(random.randint(MIN, MAX))
        self.strInput.set(0)
        self._ent_input.config(state=tk.NORMAL)

    def focus(self):
        self._ent_input.focus_set()

    def disable(self):
        self._ent_input.config(state=tk.DISABLED)

    def enable(self):
        self._ent_input.config(state=tk.NORMAL)

    @property
    def tokens(self):
        return self._tokens.get()

    @property
    def input(self):
        return self.strInput.get()

    @input.setter
    def input(self, val):
        self.strInput.set(int(val))
