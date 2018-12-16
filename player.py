# Project Objectorientatie: NIM - Player klassen
# Brecht Ooms / 2 ELO-ICT / 2018

import random
import tkinter as tk

DEFAULTCOLOR = 'SystemButtonFace'
DEFAULTRELIEF = 'flat'

HIGHLIGHTCOLOR = 'lawn green'
HIGHLIGHTRELIEF = 'raised'


# TODO: Meer comments


class _BaseColumn:
    """Basisframe voor een speler/AI."""

    def __init__(self, master=None, title='Leeg'):
        # Attributes
        self._master = master
        self._title = title
        self._playercount = -1

        # True: wacht voor user input (Speler)
        # False: Speel automatisch (AI)
        self._human = False

        # Label bovenaan
        self._lbl_title = tk.Label(master, text=self._title)
        self.highlight(False)

        # Naamvariabele voor het naamvak
        self._name = tk.StringVar()
        self._name.set("")

        # Naamvak (disabled by default in het begin)
        self._ent_name = tk.Entry(master,
                                  textvariable=self._name,
                                  state=tk.DISABLED)

        self._enabled = False

        # Aantal zetten
        self._zetten = tk.IntVar(value=0)
        self._ent_zetten = tk.Entry(master,
                                    textvariable=self._zetten,
                                    state="readonly",
                                    takefocus=False)

    def __str__(self):
        """De titel en de naam van deze speler."""
        return "{0.title:s}: {0.name:s}".format(self)

    def grid(self, column=0, row=0):
        """Zet alle widgets van deze speler in de gegeven kolom vanaf
        de gegeven rij."""

        # Zet alle widgets in de juiste column
        self._lbl_title.grid(row=row,
                             column=column,
                             padx=2, pady=2,
                             sticky='nesw')

        self._ent_name.grid(row=row + 1,
                            column=column,
                            padx=2,
                            sticky='nesw')

        self._ent_zetten.grid(row=row + 2,
                              column=column,
                              padx=2,
                              sticky='nesw')

        # Maak de kolom resizeable
        self._master.columnconfigure(column, weight=1)

    def get_zet(self, state):
        """Calculeer de volgende zet uit de huidige staat van het spel."""
        return None

    def zet(self):
        """Incrementeer het aantal zetten van deze speler."""
        self._zetten.set(self._zetten.get() + 1)

    def start(self, playercount=-1):
        """Configerueer de naam en reset het aantal zettenself.
        Sla ook het aantal spelers op."""
        # Verander de naam (als een subklasse deze functie overridden heeft)
        self._set_name()

        # Zet het naamvak op readonly en disable de tab-focus
        self._ent_name.config(state="readonly", takefocus=False)
        self._enabled = False

        # Zet het aantal zetten op 0
        self._zetten.set(0)

        # Sla het aantal spelers op
        self._playercount = playercount

        # Zet de highlight uit
        self.highlight(False)

    def reset(self):
        """Reset de naam en het aantal zetten."""

        # Reset aantal zetten en de naam
        self._zetten.set(0)
        self._name.set("")

        # Zet de highlight uit
        self.highlight(False)

    def focus(self):
        """Zet de focus op het naamvak van deze speler."""
        self._ent_name.focus_set()

    def highlight(self, flag=True):
        """Zet de highlight aan (True) of uit (False)."""

        if flag:
            # Verander de acthergrondkleur en de stijl van de rand
            self._lbl_title.config(bg=HIGHLIGHTCOLOR, relief=HIGHLIGHTRELIEF)
        else:
            # Verander de acthergrondkleur en de stijl van de rand
            self._lbl_title.config(bg=DEFAULTCOLOR, relief=DEFAULTRELIEF)

    @property
    def human(self):
        """True: Speler waarvan men de zet ingeeft via de inputs van de stapels
        False: AI die de zet bepaalt met de functie get_zet(state)."""
        return self._human

    @property
    def name(self):
        """Naam van de speler."""
        return self._name.get()

    @property
    def title(self):
        """Titel boven de speler."""
        return self._title

    @property
    def enabled(self):
        """Of het naamvak enabled is"""
        return self._enabled

    def _set_name(self):
        """Private functie die de naam eventueel veranderd als men deze override"""
        pass


class Speler(_BaseColumn):
    """Frame voor een speler."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Een speler is weldegelijk een mens en zal dus wachten op user input
        self._human = True

        # Enable de name entry
        self._ent_name.config(state=tk.NORMAL, takefocus=True)
        self._enabled = True

    def reset(self):
        """Reset de naam en het aantal zetten."""
        super().reset()

        # Enable het naamvak
        self._ent_name.config(state=tk.NORMAL, takefocus=True)
        self._enabled = True


class RandomAI(_BaseColumn):
    """Een AI die willekeurige zetten doet."""

    def _set_name(self):
        """Zet de naam op 'Hall'."""
        self._name.set('Hall')

    def get_zet(self, state):
        """Neem een willekeurig aantal van een willekeurige stapel."""
        return _random_zet(state)


class NimSumAI(_BaseColumn):
    """Een AI die de zoegenoemde nim sum gebruikt om te winnen.
    Werkt het beste met 2 spelers.
    """

    def _set_name(self):
        """Zet de naam op een willekeurige naam uit 'aiNames.txt'."""
        # Open de file en zet alle lijnen in een list
        with open('aiNames.txt') as f:
            names = list(f)

        # Kies een willekeurige lijn en strip alle whitespace
        name = random.choice(names).strip()

        # Zet vul de gekozen naam in
        self._name.set(name)

    def start(self, playercount=-1):
        """Configerueer de naam en reset het aantal zettenself.
        Sla ook het aantal spelers op.

        Geeft een waarschuwing als het aantal spelers niet gelijk is aan 2.
        """

        # Kijk na of er twee spelers in het spel zijn
        if playercount != 2:
            print("Warning!: NimSumAI works best with 2 players!")

        super().start(playercount)

    def get_zet(self, state):
        """Bepaal de volgende zet volgens de wiskundige regels ivm de nim sum."""

        # Kijk of we in de endgame zijn (max 1 stapel met 2+ tokens)
        if sum((1 for x in state if x > 1)) <= 1:
            print("End game")
            return _endgame(state)

        nim_sum = 0
        for heap in state:
            # Bereken nim sum (bitwise XOR van alle stapels)
            nim_sum = nim_sum ^ heap

        print(nim_sum)  # Ter controle

        # Als de nim_sum 0 is en de tegenstander perfect speelt kan deze AI niet winnen
        if nim_sum == 0:
            # Neem een willekeurig zet omdat het niet uit maakt
            return _random_zet(state)

        # Neem het grootste aantal tokens zodat de nim_sum 0 is na deze beurt
        for index, heap in enumerate(state):
            # De gewilde hoeveelheid in deze stapel
            target = heap ^ nim_sum

            # Als target kleiner is dan de stapel
            if target < heap:
                # Hoeveel men van deze stapel moet nemen om target te bekomen
                amount = heap - target

                return index, amount


def _endgame(state):
    """Bepaalt de beste zet tijdens de endgame."""

    # 1 bij een oneven aantal niet-lege stapels
    # 0 bij een even aantal niet-lege stapels
    odd = sum(1 for x in state if x > 0) % 2

    # Aantal tokens en de index van de grootste stapel
    big_heap = max(state)
    big_index = state.index(big_heap)

    # Laat 1 token achter bij een oneven aantal niet-lege stapels
    # Neem de hele stapel bij een even aantal niet-lege stapels
    amount = big_heap - odd

    # Je moet minstens 1 token nemen
    if amount < 1:
        amount = 1

    return big_index, amount


def _random_zet(state):
    """Neem een willekeurig aantal van een willekeurige stapel."""

    # Verzamel de index en het aantal tokens van alle niet-lege stapels
    heaps = []
    for heap in enumerate(state):
        # Als de stapel niet leeg is
        if heap[1] > 0:
            heaps.append(heap)

    # Kijk na of er niet-lege stapels zijn
    if len(heaps) == 0:
        raise ValueError("Alle stapels zijn leeg!")

    # kies een willekeurige stapel
    index, tokens = random.choice(heaps)

    # Neem een willekeurig aantal tokens uit de stapel
    return index, random.randint(1, tokens)
