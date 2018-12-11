# Project Objectorientatie: NIM - Main program
# Brecht Ooms / 2 ELO-ICT / 2018

import tkinter as tk
from tkinter import messagebox
import os

import player
import heap

HEAPS = 3


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
        self._topFrame = TopFrame(self)

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

    def zet(self):

        # Loop tot een mens aan de beurt is
        # Of totdat iemand verloren is
        while True:
            print(self._curspeler.name, 'is aan beurt')

            # Haal de gamestate binnen

            # als het een mens is
            if self._curspeler.human:
                try:
                    zet = self._midFrame.getZet()
                    self._midFrame.zet(zet)

                except ValueError as error:
                    # Laat de error zien in een warning
                    messagebox.showwarning(self._curspeler.name, error)

                    # Stop de loop zodat de speler opnieuw kan proberen
                    break
            else:
                # TODO: Better error handling and traceback printing
                zet = self._curspeler.getZet(self._midFrame.state)

                try:
                    self._midFrame.zet(zet)

                except ValueError as error:
                    # Laat de error zien in een warning
                    messagebox.showerror(self._curspeler.name, error)

                    # Stop het spel want een AI kan niet opnieuw proberen
                    self.quit()

            if not any(self._midFrame.state):
                winMessage = '{:s} is verloren...'.format(
                    self._curspeler.name)
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
        print("Stoppen...")

        # TODO: Don't quit the program, but reset it to the initial state

        self.quit()


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

        # TODO: Splits Speler en AI arrays
        if not spelers:
            self._spelers = [player.Speler(self, 'Speler'),
                             player.RandomAI(self, 'AI')]
        else:
            self._spelers = spelers

        for i, speler in enumerate(self._spelers, start=1):
            speler.grid(i)

    def start(self):
        playercount = len(self._spelers)
        for speler in self._spelers:
            speler.start(playercount)

    def focus(self, key=0):
        self._spelers[key].focus()

    # Eindeloze generator met alle spelers op volgorde
    @property
    def spelers(self):
        def generator():
            while True:
                for speler in self._spelers:
                    yield speler

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


if __name__ == "__main__":
    app = Main()

    app.mainloop()
