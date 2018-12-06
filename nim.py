# Project Objectorientatie: NIM - Main program
# Brecht Ooms / 2 ELO-ICT / 2018

import tkinter as tk
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
        self.resizable(False, False)

        # Bovenste Frame met spelers en hun labels
        self._topFrame = TopFrame(self)

        # Middenste Frame met alle stapels
        self._midFrame = heap.HeapFrame(self, HEAPS)

        # Onderste Frame met alle knoppen
        self._botFrame = BotFrame(self, self.zet, self.nieuw, self.stop)

        # Zet de frames in de grid
        self._topFrame.grid(column=0, padx=5, pady=5, sticky="nesw")
        self._midFrame.grid(column=0, padx=5, pady=5, sticky="nesw")
        self._botFrame.grid(column=0, padx=5, pady=5, sticky="nesw")

        # Zet de focus op de eerste name entry
        self._topFrame.focus()

    def nieuw(self):
        self._topFrame.start()
        self._midFrame.start()
        self._botFrame.start()

        self._midFrame.focus()

    def zet(self):
        print(self._midFrame.state)
        self._topFrame.spelers[0].zet()

    def stop(self):
        print("Stoppen...")
        self.quit()


class TopFrame(tk.Frame):
    """Bovenste frame met de speler en de AI"""

    def __init__(self, master=None):
        super().__init__(master)

        # Maak de labels
        self._lbl_top_naam = tk.Label(self, text="Naam:")
        self._lbl_top_zetten = tk.Label(self, text="Aantal zetten:")

        # Zet ze in de grid
        self._lbl_top_naam.grid(row=1, sticky=tk.W)
        self._lbl_top_zetten.grid(row=2, sticky=tk.W)

        # Misschien later opsplitsen in Spelers en AI
        # om meerdere Spelers of AI mogelijk te maken...
        self._spelers = [player.SpelerColumn(self, 1, 'Speler'),
                         player.AIColumn(self, 2, 'AI')]

    def start(self):
        for speler in self._spelers:
            speler.start()

    def focus(self, key=0):
        self._spelers[key].focus()

    @property
    def spelers(self):
        return self._spelers.copy()


class BotFrame(tk.Frame):
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
            self.columnconfigure(x, weight=1)

    def start(self):
        self._btn_zet.config(state=tk.NORMAL)


if __name__ == "__main__":
    app = Main()

    app.mainloop()
