# Project Objectorientatie: NIM - Main program
# Brecht Ooms / 2 ELO-ICT / 2018

import tkinter as tk
import os

import player


class Main(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("NIM")
        self.iconbitmap(os.path.realpath('images/nim_icon.ico'))

        self.speler = player.SpelerFrame(self,
                                         label='Banaan')
        self.speler.pack()


if __name__ == "__main__":
    app = Main()

    app.mainloop()
