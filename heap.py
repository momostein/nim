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

        for i in range(heaps):
            # Maak een nieuwe stapel
            heap = Heap(self, "Stapel {:d}".format(i + 1))

            # Zet hem in de grid
            heap.grid(column=i, row=0)

            # Voeg hem toe aan de lijst
            self._heaps.append(heap)

    def start(self):
        for heap in self._heaps:
            heap.start()

    def focus(self, key=0):
        self._heaps[key].focus()

    @property
    def state(self):
        return [heap.tokens for heap in self._heaps]


class Heap(tk.Frame):
    """Een frame voor een stapel"""

    def __init__(self, master=None, title="Stapel"):
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
        self._input = tk.IntVar()
        self._ent_input = tk.Entry(self,
                                   textvariable=self._input,
                                   state=tk.DISABLED)

        # Voeg ze toe aan de grid
        self._lbl_title.grid(row=0)
        self._ent_tokens.grid(row=1)
        self._ent_input.grid(row=2)

    def start(self):
        self._tokens.set(random.randint(MIN, MAX))
        self._input.set(0)
        self._ent_input.config(state=tk.NORMAL)

    def focus(self):
        self._ent_input.focus_set()

    @property
    def tokens(self):
        return self._tokens.get()
