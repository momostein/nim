# Project Objectorientatie: NIM - Player classes
# Brecht Ooms / 2 ELO-ICT / 2018

import tkinter as tk
import random


class _BaseColumn():
    """Basisframe voor een speler/AI"""

    def __init__(self, master=None, title='Leeg'):
        self._master = master
        self._title = title

        # True: wacht voor user input (Speler)
        # False: Speel automatisch (AI)
        self._human = False

        # Label bovenaan
        self._lbl_label = tk.Label(master, text=self._title)

        self._name = tk.StringVar()
        self._name.set("")
        self._ent_name = tk.Entry(master,
                                  textvariable=self._name,
                                  state="readonly",
                                  takefocus=False)

        self._enabled = False

        # Aantal zetten
        self._zetten = tk.IntVar(value=0)
        self._ent_zetten = tk.Entry(master,
                                    textvariable=self._zetten,
                                    state="readonly",
                                    takefocus=False)

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

        self._ent_name.config(state="readonly", takefocus=False)
        self._enabled = False

        self._zetten.set(0)
        self._playercount = playercount

    def reset(self):
        self._zetten.set(0)
        self._name.set("")

    def focus(self):
        self._ent_name.focus_set()

    def __str__(self):
        return "{0.title:s}: {0.name:s}".format(self)

    @property
    def human(self):
        return self._human

    @property
    def name(self):
        return self._name.get()

    @property
    def title(self):
        return self._title

    @property
    def enabled(self):
        return self._enabled

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
        self._ent_name.config(state=tk.NORMAL, takefocus=True)
        self._enabled = True

    def reset(self):
        super().reset()
        self._ent_name.config(state=tk.NORMAL, takefocus=True)
        self._enabled = True


class RandomAI(_BaseColumn):
    """Een AI die willekeurige zetten doet"""

    def _setName(self):
        self._name.set('Hall')

    def getZet(self, state):
        heaps = []

        for heap in enumerate(state):

            # Als de stapel niet leeg is
            if heap[1] > 0:
                heaps.append(heap)

        if len(heaps) == 0:
            raise ValueError("Alle stapels zijn leeg!")

        index, tokens = random.choice(heaps)

        return index, random.randint(1, tokens)


class NimSumAI(_BaseColumn):
    """Een AI die de zoegenoemde nim sum gebruikt om te winnen.
    Werkt wel alleen maar met 2 spelers..."""

    def _setName(self):
        with open('aiNames.txt') as f:
            names = list(f)

        self._name.set(random.choice(names).strip())

    def start(self, playercount=-1):
        if playercount != 2:
            print("Warning!: NimSumAI may only work with 2 players!")

        super().start(playercount)

    def getZet(self, state):

        # Kijk of we in de end-game zijn (max 1 stapel met 2+ tokens)
        if sum((1 for x in state if x > 1)) <= 1:
            print("End game")
            return self._endGame(state)

        nimSum = 0
        for heap in state:
            # Bereken nim sum (bitwise XOR)
            nimSum = nimSum ^ heap

        print(nimSum)

        if nimSum == 0:
            # kan normaal niet winnen, neem van random stapel
            return self._randomZet(state)

        for index, heap in enumerate(state):
            target = heap ^ nimSum

            if target < heap:
                amount = heap - target
                return index, amount

    def _endGame(self, state):
        # 1 if odd, 0 if even
        odd = sum(1 for x in state if x > 0) % 2

        bigHeap = max(state)
        bigIndex = state.index(bigHeap)

        # Remove whole stack if even, leave 1 if odd
        amount = bigHeap - odd

        # Can't take 0
        if amount < 1:
            amount = 1

        return (bigIndex, amount)

    def _randomZet(self, state):
        # Neem één token van een willekeurige stapel
        heaps = []

        for index, heap in enumerate(state):

            # Als de stapel niet leeg is
            if heap > 0:
                heaps.append(index)

        if len(heaps) == 0:
            raise ValueError("Alle stapels zijn leeg!")

        index = random.choice(heaps)

        return index, 1
