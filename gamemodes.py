# Default gamemodes

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
        'title': 'AI',
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
        'title': 'Nim-sum AI',
        'class': player.NimSumAI
    }

]
