# Project Objectorientatie: NIM - Main program
# Brecht Ooms / 2 ELO-ICT / 2018

import tkinter as tk
import os

import player


class Main(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)

        self.winfo_toplevel().title("NIM")
        self.winfo_toplevel().iconbitmap(os.path.realpath('images/nim_icon.ico'))

        spelerNaam = tk.StringVar()
        speler = player.SpelerFrame(self,
                                    label='Banaan',
                                    naamvariable=spelerNaam)
        speler.pack()


if __name__ == "__main__":
    root = tk.Tk()

    mainFrame = Main(root)

    mainFrame.pack()
    root.mainloop()
