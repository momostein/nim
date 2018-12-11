# Project Objectorientatie: NIM - Main program
# Brecht Ooms / 2 ELO-ICT / 2018

import tkinter as tk
from tkinter import messagebox
import os

import player
import heap

HEAPS = 3

PLAYERS = [
    {
        'title': 'Player',
        'class': player.Speler
    },
    {
        'title': 'AI',
        'class': player.RandomAI
    }
]

# TODO: Vraag naar de juiste handeling van de nieuwknop
#       Als er al een spel bezig is


class Main(tk.Tk):
    """Main window"""

    def __init__(self):
        super().__init__()

        # Titel en icoontje
        self.title("NIM")
        self.iconbitmap(os.path.realpath('images/nim_icon.ico'))

        # Niet resizable in elke richting
        self.resizable(True, False)

        # Bovenste Frame met spelers en hun labels
        self._topFrame = TopFrame(self, PLAYERS)

        # Middenste Frame met alle stapels
        self._midFrame = heap.HeapFrame(self, HEAPS)

        # Onderste Frame met alle knoppen
        self._botFrame = BtnFrame(self, self.zet, self.nieuw, self.stop)

        # Zet de frames in de grid
        self._topFrame.grid(column=0, padx=5, pady=5, sticky="nesw")
        self._midFrame.grid(column=0, padx=5, pady=5, sticky="nesw")
        self._botFrame.grid(column=0, padx=5, pady=5, sticky="nesw")

        # Maak de colom resizeable
        self.columnconfigure(0, weight=1)

        # Zet de focus op de eerste name entry
        self._topFrame.focus()

    def nieuw(self):
        self._topFrame.start()
        self._midFrame.start()
        self._botFrame.start()

        self._midFrame.focus()

        self._spelers = self._topFrame.spelers()

        # Zet de eerste speler aan beurt
        self._curspeler = next(self._spelers)
        if not self._curspeler.human:
            self.zet()

    def zet(self):

        # Loop tot een mens aan de beurt is
        # Of totdat iemand verloren is
        while True:
            # als het een mens is
            if self._curspeler.human:
                try:
                    zet = self._midFrame.getZet()

                    print("State: {0}\tPlayer: {1:s}\tMove: {2}".format(self._midFrame.state,
                                                                        str(self._curspeler),
                                                                        zet))

                    self._midFrame.zet(zet)

                except ValueError as error:
                    # Laat de error zien in een warning
                    messagebox.showwarning(self._curspeler, error)

                    # Stop de loop zodat de speler opnieuw kan proberen
                    break
            else:
                zet = self._curspeler.getZet(self._midFrame.state)

                print("State: {0}\tPlayer: {1:s}\tMove: {2}".format(self._midFrame.state,
                                                                    str(self._curspeler),
                                                                    zet))
                try:
                    self._midFrame.zet(zet)
                    title = self._midFrame.titles[zet[0]]

                    # TODO: Meervoud/enkelvoud tokens
                    message = "{:s} neemt {:d} token(s) van {:s}".format(str(self._curspeler),
                                                                         zet[1],
                                                                         title)
                    messagebox.showinfo(self._curspeler, message)

                except ValueError as error:
                    # Laat de error zien in een warning
                    messagebox.showerror(self._curspeler, error)

                    # Stop het spel want een AI kan niet opnieuw proberen
                    self.quit()

            if not any(self._midFrame.state):
                winMessage = '{:s} is verloren...'.format(
                    str(self._curspeler))
                messagebox.showinfo('Verloren', winMessage)

                # Stop het spel en breek uit de loop
                self.stop()
                break

            # Zet de volgende speler aan beurt:
            self._curspeler = next(self._spelers)

            # Breek uit de loop als het een mens is:
            if self._curspeler.human:
                # TODO: Player highlighting?

                # Zet ook de focus terug op de inputs
                self._midFrame.focus()
                break

    def stop(self):
        print("Resetting...")

        self._topFrame.reset()
        self._midFrame.reset()
        self._botFrame.reset()

        self._topFrame.focus()


class TopFrame(tk.Frame):
    """Bovenste frame met de speler en de AI"""

    def __init__(self, master=None, spelers=None):
        super().__init__(master)

        # Maak de labels
        self._lbl_top_naam = tk.Label(self, text="Naam:")
        self._lbl_top_zetten = tk.Label(self, text="Aantal zetten:")

        # Zet ze in de grid
        self._lbl_top_naam.grid(row=1, sticky=tk.W)
        self._lbl_top_zetten.grid(row=2, sticky=tk.W)

        if not spelers:
            self._spelers = [player.Speler(self, 'Speler'),
                             player.RandomAI(self, 'AI')]

        else:
            self._spelers = []
            for speler in spelers:
                name = speler['title']
                _class = speler['class']

                self._spelers.append(_class(self, name))

        for i, speler in enumerate(self._spelers, start=1):
            speler.grid(i)

    def start(self):
        playercount = len(self._spelers)
        for speler in self._spelers:
            speler.start(playercount)

    def reset(self):
        for speler in self._spelers:
            speler.reset()

    def focus(self, key=0):
        for speler in self._spelers[key:]:
            if speler.enabled:
                speler.focus()
                return True

        return False

    # Eindeloze generator met alle spelers op volgorde
    @property
    def spelers(self):
        def generator():
            while True:
                for speler in self._spelers:
                    # TODO: highlighting here?
                    print('\n{:s} is aan beurt'.format(str(speler)))
                    yield speler
                    speler.zet()

        return generator


class BtnFrame(tk.Frame):
    """Onderste frame met al de knoppen"""

    def __init__(self, master=None, zet=None, nieuw=None, stop=None):
        super().__init__(master)
        self._btn_zet = tk.Button(self,
                                  text="Zet",
                                  command=zet,
                                  state=tk.DISABLED,
                                  width=10)

        self._btn_nieuw = tk.Button(self,
                                    text="Nieuw",
                                    command=nieuw,
                                    width=10)

        self._btn_stop = tk.Button(self,
                                   text="Stop",
                                   command=stop,
                                   width=10)

        self._btn_zet.grid(row=0, column=0, padx=2, pady=2, sticky="nesw")
        self._btn_nieuw.grid(row=0, column=1, padx=2, pady=2, sticky="nesw")
        self._btn_stop.grid(row=0, column=2, padx=2, pady=2, sticky="nesw")

        for x in range(3):
            # Maak de colom resizeable
            self.columnconfigure(x, weight=1)

    def start(self):
        self._btn_zet.config(state=tk.NORMAL)

    def reset(self):
        self._btn_zet.config(state=tk.DISABLED)


if __name__ == "__main__":
    app = Main()

    app.mainloop()
