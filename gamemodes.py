# Project Objectorientatie: NIM - Game Modes
# Brecht Ooms / 2 ELO-ICT / 2018

import player

# Speler vs Random AI
DEFAULT = [
    {
        'title': 'Player',
        'class': player.Speler
    },
    {
        'title': 'AI',
        'class': player.RandomAI
    }
]

# Speler vs Speler
PVP = [
    {
        'title': 'Player 1',
        'class': player.Speler
    },
    {
        'title': 'Player 2',
        'class': player.Speler
    }
]

# Speler vs Hard AI
NIMSUM = [
    {
        'title': 'Player',
        'class': player.Speler
    },
    {
        'title': 'Hard AI',
        'class': player.NimSumAI
    }
]

# Random AI vs Hard AI
AIVAI = [
    {
        'title': 'Random AI',
        'class': player.RandomAI
    },
    {
        'title': 'Hard AI',
        'class': player.NimSumAI
    }

]

# Speler vs Random AI vs Hard AI
ALL = [
    {
        'title': 'Player',
        'class': player.Speler
    },
    {
        'title': 'AI',
        'class': player.RandomAI
    },
    {
        'title': 'Hard AI',
        'class': player.NimSumAI
    }

]
