# Project Objectorientatie: NIM -  Heap classes
# Brecht Ooms / 2 ELO-ICT / 2018

import random
import tkinter as tk

MIN = 1
MAX = 9


# TODO: Meer comments


class HeapFrame(tk.Frame):
    """Frame met meerdere stapels"""

    def __init__(self, master=None, heaps=3):
        super().__init__(master)

        # Maak een lijst en vul hem met stapels
        self._heaps = []

        # Registreer de validatiefunctie
        vcmd = (self.register(validate),
                '%d', '%P', '%S')

        for i in range(heaps):
            # Maak een nieuwe stapel
            heap = Heap(self, "Stapel {:d}".format(i + 1), vcmd)

            # Zet hem in de grid
            heap.grid(column=i, row=0, padx=2, pady=2, sticky='nesw')

            # Maak de colom resizeable
            self.columnconfigure(i, weight=1)

            # Voeg hem toe aan de lijst
            self._heaps.append(heap)

    def start(self):
        for heap in self._heaps:
            heap.start()

    def reset(self):
        for heap in self._heaps:
            heap.reset()

    def get_zet(self):
        more_than_zero = 0

        heap_key = -1
        amount = -1

        # Get the input of every heap
        for i, heap in enumerate(self._heaps):
            # Kijk na of de input een positieve integer is
            try:
                val = int(heap.input)

                if val > 0:
                    more_than_zero += 1

                    heap_key = i
                    amount = val

            except ValueError:
                heap.focus()
                raise ValueError('U moet geldige getallen ingeven!')

        if more_than_zero == 0:
            self.focus()
            raise ValueError('U moet minstens één token nemen!')

        if more_than_zero > 1:
            self.focus()
            raise ValueError('U mag maar van één stapel nemen!')

        return heap_key, amount

    def zet(self, zet):
        self._heaps[zet[0]].zet(zet[1])

    def focus(self, key=0):

        # Focus the first enabled heap starting from key
        for heap in self._heaps[key:]:
            if heap.enabled:
                heap.focus()
                return True
        else:
            # Return false if none are enabled starting from key
            return False

    def get_title(self, key):
        """Verkrijg de titel van de stapel met index key"""
        return self._heaps[key].title

    @property
    def state(self):
        return [heap.tokens for heap in self._heaps]

    @property
    def titles(self):
        return [heap.title for heap in self._heaps]


class Heap(tk.Frame):
    """Een frame voor een stapel"""

    def __init__(self, master=None, title="Stapel", vcmd=None):
        super().__init__(master)

        self._title = title
        self._enabled = False

        # Titel van de stapel
        self._lbl_title = tk.Label(self,
                                   text=self._title)

        # Aantal Balletjes
        self._tokens = tk.IntVar()
        self._ent_tokens = tk.Entry(self,
                                    textvariable=self._tokens,
                                    state="readonly",
                                    takefocus=False)

        # Inputveld
        self._strInput = tk.StringVar()
        self._ent_input = tk.Entry(self,
                                   textvariable=self._strInput,
                                   state=tk.DISABLED,
                                   validate="key",
                                   validatecommand=vcmd)

        # Voeg ze toe aan de grid
        self._lbl_title.grid(row=0, sticky='nesw')
        self._ent_tokens.grid(row=1, sticky='nesw')
        self._ent_input.grid(row=2, sticky='nesw')

        # Maak de colom resizeable
        self.columnconfigure(0, weight=1)

    def start(self):
        # Vul een willekeurige hoeveelheid tokens in
        self._tokens.set(random.randint(MIN, MAX))

        # Reset the input
        self._strInput.set(0)

        self.enable()

    def reset(self):
        self._tokens.set(0)
        self._strInput.set("")
        self.disable()

    def zet(self, amount):
        if amount <= 0:
            self.focus()
            raise ValueError("U moet minstens 1 nemen!")

        if amount > self.tokens:
            self.focus()
            raise ValueError("U kunt maximaal {:d} tokens van {:s} nemen".format(
                self.tokens,
                self._title))

        else:
            self._tokens.set(self.tokens - amount)
            self.input = 0
            if self.tokens == 0:
                self.disable()

    def focus(self):
        self._ent_input.focus_set()

    def disable(self):
        self._ent_input.config(state=tk.DISABLED)
        self._enabled = False

    def enable(self):
        self._ent_input.config(state=tk.NORMAL)
        self._enabled = True

    @property
    def tokens(self):
        return self._tokens.get()

    @property
    def title(self):
        return self._title

    @property
    def enabled(self):
        return self._enabled

    @property
    def input(self):
        return self._strInput.get()

    @input.setter
    def input(self, val):
        self._strInput.set(int(val))


def validate(action, edited, change):
    """validatiefunctie om alleen nummers toe te laten"""

    # action : Type of action (1=insert, 0=delete, -1 for others)
    # edited : Value of the entry if the edit is allowed
    # change : The text string being inserted or deleted, if any

    # Validate als het een insert action is
    if action == "1":
        # Kijk na of de verandering bestaat uit digits
        if not change.isdigit():
            # Verwerp de verandering
            return False

        # Kijk na of we de hele input een integer is
        try:
            int(edited)

        except ValueError:
            # Verwerp de verandering
            return False

    # Accepteer de verandering
    return True
