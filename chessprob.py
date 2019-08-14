from decimal import Decimal as D, getcontext

__doc__ = """chessprob.py
See the README and example_usage.py"""

__all__ = [
    'set_options', 'print_options', 'identical_any', 'identical_pov_player',
    'identical_pov_game', 'identical_these_moves', 'identical_these_moves_pov_player',
    'identical_these_moves_pov_game', 'get_formulas', 'mathify', 'populate', 'wolfram_open'
]


#region Options

def set_options(
    choices=None, depth=None,
    players=None, games=None,
    exact=None, precision=None
):
    """ Use this function to set global options """
    global CHOICES, DEPTH, POSSGAMES, PLAYERS, GAMES, ALLGAMES, EXACT, PRECISION, _NUMBERFORMAT

    if players is not None:
        if players % 2 == 1:
            raise Exception(f'Please choose an even amount of players, not {players}.')
        PLAYERS = D(int(players))
    if games is not None: GAMES = D(int(games))
    ALLGAMES = D(int(PLAYERS * GAMES / 2))

    if choices is not None: CHOICES = D(choices)
    if depth is not None: DEPTH = D(depth)
    POSSGAMES = D(int(CHOICES ** DEPTH))

    if exact is not None: EXACT = bool(exact)

    if precision is not None: PRECISION = int(precision)
    getcontext().prec = PRECISION
    _NUMBERFORMAT = '{0:.' + str(PRECISION) + 'f}'


def print_options(verbose=False):
    """ output the current global options """
    if verbose:
        print(f'choices per move:{CHOICES}, game depth:{DEPTH} --> Number of possible games:{POSSGAMES}')
        print(f'players:{PLAYERS}, games per player:{GAMES} --> Number of games: {ALLGAMES}')
        print(f'use exact algorithms:{EXACT}, precision={PRECISION}')
    else:
        print(f'choices:{CHOICES}, depth:{DEPTH}, players:{PLAYERS}, games:{GAMES}')


# set these variables using the set_options() function

EXACT = False

CHOICES = D(3)
DEPTH = D(80)
POSSGAMES = D(int(CHOICES ** DEPTH))

PLAYERS = D(1_500_000_000)
GAMES = D(2_500)
ALLGAMES = D(int(PLAYERS * GAMES / 2))

PRECISION = 100
getcontext().prec = PRECISION
_NUMBERFORMAT = '{0:.' + str(PRECISION) + 'f}'


#endregion

#region Algorithms

def identical_any(raw=False):
    """
    1 - ( fac( Np ) / ( N ** ( P * Na ) * fac( Np - Na) ) )
    1 - exp( -( ( Na * ( Na - 1 ) ) / ( 2 * Np ) ) )
    """

    if EXACT:
        result = 1 - (fac(POSSGAMES) / (CHOICES ** (DEPTH * ALLGAMES) * fac(POSSGAMES - ALLGAMES)))
    else:
        result = 1 - exp(((ALLGAMES * (ALLGAMES - 1)) / (2 * POSSGAMES)) * D(-1))

    return pretty(result, raw=raw)


def identical_pov_player(raw=False):
    """
    1 - ( 1 - N ** -P ) ** ( Ng ** 2 * ( Nc - 1 ) )
    1 - exp( -( ( Ng ** 2 * ( Nc - 1 ) ) / Np ) )
    """

    if EXACT:
        result = 1 - (1 - CHOICES ** -DEPTH) ** (GAMES ** 2 * (PLAYERS - 1))
    else:
        result = 1 - exp(((GAMES ** 2 * (PLAYERS - 1)) / POSSGAMES) * D(-1))

    return pretty(result, raw=raw)


def identical_pov_game(raw=False):
    """
    1 - ( 1 - N ** -P ) ** ( Na - 1 )
    1 - exp( -( ( Na - 1 ) / Np ) )
    """

    if EXACT:
        result = 1 - (1 - CHOICES ** -DEPTH) ** (ALLGAMES - 1)
    else:
        result = 1 - exp(((ALLGAMES - 1) / POSSGAMES) * D(-1))

    return pretty(result, raw=raw)


def identical_these_moves(raw=False):
    """
    1 - ( 1 + Na / ( Np - 1 ) ) * ( 1 - N ** -P ) ** Na
    1 - exp( -( Na * ( Na - 1 ) / ( 2 * N ** ( 2 * P ) ) ) )
    """

    if EXACT:
        result = 1 - (1 + ALLGAMES / (POSSGAMES - 1)) * (1 - CHOICES ** -DEPTH) ** ALLGAMES
    else:
        result = 1 - exp((ALLGAMES * (ALLGAMES - 1) / (2 * CHOICES ** (2 * DEPTH))) * D(-1))

    return pretty(result, raw=raw)


def identical_these_moves_pov_player(raw=False):
    """
    ( 1 - ( 1 - N ** -P ) ** Ng ) * ( 1 - ( 1 - N ** -P ) ** ( Ng * ( Nc - 1 ) ) )
    1 - exp( -( Ng ** 2 * ( Nc - 1 ) / ( N ** ( 2 * P ) ) ) )
    """

    matchmoves = CHOICES ** -DEPTH
    if EXACT:
        result = (1 - (1 - matchmoves) ** GAMES) * (1 - (1 - matchmoves) ** (GAMES * (PLAYERS - 1)))
    else:
        result = 1 - exp((GAMES ** 2 * (PLAYERS - 1) / (CHOICES ** (2 * DEPTH))) * D(-1))

    return pretty(result, raw=raw)


def identical_these_moves_pov_game(raw=False):
    """
    N ** -P * ( 1 - ( 1 - N ** -P ) ** ( Na - 1 ) )
    N ** -P * ( 1 - exp( -( ( Na - 1 ) / Np ) ) )
    """

    matchmoves = CHOICES ** -DEPTH
    if EXACT:
        result = matchmoves * (1 - (1 - matchmoves) ** (ALLGAMES - 1))
    else:
        result = matchmoves * (1 - exp(((ALLGAMES - 1) / POSSGAMES) * D(-1)))

    return pretty(result, raw=raw)


#region Helper functions

def pretty(number, raw=False):
    """ formats floating numbers so that they look pretty when printed """
    if raw:
        return number
    else:
        return _NUMBERFORMAT.format(number)


from math import factorial


# this module internally works with decimal.Decimal instances instead of raw numbers
# because of precision issues. These two functions do with Decimals what math.factorial
# and math.exp do with raw numbers.

def exp(n: D):
    return n.exp()


def fac(n):
    return D(factorial(n))


#endregion

#endregion

#region Tools

from webbrowser import open as openbrowser
from time import sleep


def get_formulas(*funcs):
    """ extract the formulas from the functions docstring """
    result = []
    for func in funcs:
        result.append([f for f in (
            f.strip() for f in func.__doc__.splitlines()
        ) if f])
    return result


def mathify(formula):
    """ convert the formula from python to math syntax """
    return formula.replace('/', '÷').replace('**', '^').replace(' * ', ' ')


def populate(formula):
    """ populate the formula with the current options """
    formula = formula. \
        replace('Np', '{possgames}').replace('Na', '{allgames}'). \
        replace('Ng', '{games}').replace('Nc', '{players}'). \
        replace('N', '{choices}').replace('P', '{depth}')
    return formula.format(
        choices=CHOICES, depth=DEPTH, possgames=POSSGAMES,
        games=GAMES, players=PLAYERS, allgames=ALLGAMES
    )


def wolfram_open(*formulas, new=2):
    """ open the formula on wolframalpha.com """
    wait = .3
    for f in formulas:
        f = populate(f)
        f = f.replace('/', '%2F').replace('+', '%2B').replace(' ', '+')
        f = f'https://www.wolframalpha.com/input/?i={f}'
        openbrowser(f, new=new)
        sleep(wait)


#endregion


if __name__ == '__main__':
    print(__doc__)
