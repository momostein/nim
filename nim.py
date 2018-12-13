# Project Objectorientatie: NIM - Main program
# Brecht Ooms / 2 ELO-ICT / 2018

import tkinter as tk
from tkinter import messagebox
import os

import player
import gamemodes
import heap

# Mogelijke spelmodi:
# DEFAULT:  Player      vs  Random AI
# NIMSUM:   Player      vs  Hard AI
# PVP:      Player      vs  Player
# AIVAI:    Random AI   vs  Hard AI
# ALL:      Speler      vs  Random AI   vs  Hard AI
PLAYERS = gamemodes.DEFAULT

# Aantal stapels
HEAPS = 3

# Meld de zetten van de AI's
SHOWAIMOVE = True


# TODO: Meer comments


class Main(tk.Tk):
    """Main window"""

    def __init__(self):
        super().__init__()

        # Attributes
        self._spelers = None
        self._curspeler = None

        # Titel en icoontje
        self.title("NIM")
        self.iconbitmap(os.path.realpath('images/nim_icon.ico'))

        # Niet resizable in de verticale richting
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

        # Maak de kolom resizeable
        self.columnconfigure(0, weight=1)

        # Zet de focus op het eerste open naamvak van de speler
        if not self._topFrame.focus():
            # Zet de focus op de nieuwknop als geen naamvakken enabled zijn
            self._botFrame.focus_nieuw()

    def nieuw(self):
        # Start alle frames op
        self._topFrame.start()
        self._midFrame.start()
        self._botFrame.start()

        # Zet de focus op de stapel
        self._midFrame.focus()

        # Maak een generator met de spelers
        self._spelers = self._topFrame.spelers()

        # Zet de eerste speler aan beurt
        self._curspeler = next(self._spelers)

        # Een AI moet automatisch een zet maken
        if not self._curspeler.human:
            self.zet()

    def zet(self):
        # Loop tot een mens aan de beurt is
        # Of totdat iemand verloren is
        while True:
            # als het een mens is
            if self._curspeler.human:

                try:
                    # Vraag de inputs op
                    zet = self._midFrame.get_zet()

                    # Geef de state, speler en zet weer in de CLI
                    print("State: {0}\tPlayer: {1:s}\tMove: {2}".format(self._midFrame.state,
                                                                        str(self._curspeler),
                                                                        zet))

                    # Maak de gegeven zet
                    self._midFrame.zet(zet)

                except ValueError as error:
                    # Laat de error zien in een warning
                    messagebox.showwarning(self._curspeler, error)

                    # Stop de loop zodat de speler opnieuw kan proberen
                    break

            else:
                # Vraag de zet op van de AI
                zet = self._curspeler.get_zet(self._midFrame.state)

                # Geef de state, speler en zet weer in de CLI
                print("State: {0}\tPlayer: {1:s}\tMove: {2}".format(self._midFrame.state,
                                                                    str(self._curspeler),
                                                                    zet))
                try:
                    # Maak de gegeven zet van de AI
                    self._midFrame.zet(zet)

                    # Titel van de betrokken stapel
                    title = self._midFrame.titles[zet[0]]

                    # Meervoud/Enkelvoud van token(s)
                    token = "token"
                    if zet[1] != 1:
                        token += "s"

                    if SHOWAIMOVE:
                        # Bouw het bericht op
                        message = "{:s} neemt {:d} {:s} van {:s}".format(str(self._curspeler),
                                                                         zet[1],
                                                                         token,
                                                                         title)

                        # Geef het aantal tokens en de betrokken stapel weer
                        messagebox.showinfo(self._curspeler, message)

                except ValueError as error:
                    # Laat de error zien in een warning
                    messagebox.showerror(self._curspeler, error)

                    # Stop het spel want een AI kan niet opnieuw proberen
                    self.quit()
                    break

            # Kijk na of alle stapels leeg zijn
            if not any(self._midFrame.state):
                # Incrementeer de zetten één laatste keer
                self._curspeler.zet()

                # Bouw het bericht op
                win_message = '{:s} is verloren...'.format(
                    str(self._curspeler))

                # Geef het bericht weer
                messagebox.showinfo('Verloren', win_message)

                # Stop het spel en breek uit de loop
                self.stop()
                break

            # Zet de volgende speler aan beurt:
            self._curspeler = next(self._spelers)

            # Breek uit de loop als het een mens is:
            if self._curspeler.human:
                # Zet ook de focus terug op de inputs
                self._midFrame.focus()
                break

    def stop(self):
        print("Resetting...")

        # Reset alle frames
        self._topFrame.reset()
        self._midFrame.reset()
        self._botFrame.reset()

        # Zet de focus op het eerste open naamvak van de speler
        if not self._topFrame.focus():
            self._botFrame.focus_nieuw()


class TopFrame(tk.Frame):
    """Bovenste frame met de speler en de AI"""

    def __init__(self, master=None, spelers=gamemodes.DEFAULT):
        super().__init__(master)

        # Maak de labels
        self._lbl_top_naam = tk.Label(self, text="Naam:")
        self._lbl_top_zetten = tk.Label(self, text="Aantal zetten:")

        # Zet ze in de grid
        self._lbl_top_naam.grid(row=1, sticky=tk.W)
        self._lbl_top_zetten.grid(row=2, sticky=tk.W)

        # Verzamel alle spelers uit de gamemode dict
        self._spelers = []
        for i, spelerDict in enumerate(spelers, start=1):
            # Extraheer de data
            name = spelerDict['title']
            speler_class = spelerDict['class']

            # Initializeer het type speler en zet hem in de grid
            speler = speler_class(self, name)
            speler.grid(i)

            # Zet hem in de grid
            self._spelers.append(speler)

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
                    # TODO: Player highlighting
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
            # Maak de kolom resizeable
            self.columnconfigure(x, weight=1)

    def start(self):
        self._btn_zet.config(state=tk.NORMAL)

    def reset(self):
        self._btn_zet.config(state=tk.DISABLED)

    def focus_zet(self):
        self._btn_zet.focus()

    def focus_nieuw(self):
        self._btn_nieuw.focus()

    def focus_stop(self):
        self._btn_stop.focus()


if __name__ == "__main__":
    app = Main()
    app.mainloop()
