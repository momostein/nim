# Project Objectorientatie: NIM - Main program
# Brecht Ooms / 2 ELO-ICT / 2018

import tkinter as tk
import os

import player


class Main(tk.Tk):

    def __init__(self):
        super().__init__()

        # Titel en icoontje
        self.title("NIM")
        self.iconbitmap(os.path.realpath('images/nim_icon.ico'))

        # Niet resizable
        self.resizable(False, False)

        # Bovenste Frame met spelers en hun labels
        self._topFrame = TopFrame(self)
        self._topFrame.grid(column=0, padx=5, pady=5)

        startbutton = tk.Button(self,
                                text="Start",
                                command=self.start)
        startbutton.grid(column=0)

        button = tk.Button(self, text="Zet",
                           command=self._topFrame.spelers[0].zet)

        button.grid(column=0)

    def start(self):
        self._topFrame.start()



class TopFrame(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)

        # Maak de labels
        self._lbl_top_naam = tk.Label(self, text="Naam:")
        self._lbl_top_zetten = tk.Label(self, text="Aantal zetten:")

        self._lbl_top_naam.grid(row=1, sticky=tk.W)
        self._lbl_top_zetten.grid(row=2, sticky=tk.W)

        self._spelers = [player.SpelerColumn(self, 1, 'Speler'),
                         player.AIColumn(self, 2, 'AI')]

    def start(self):
        for speler in self._spelers:
            speler.start()

    @property
    def spelers(self):
        return self._spelers.copy()


if __name__ == "__main__":
    app = Main()

    app.mainloop()
