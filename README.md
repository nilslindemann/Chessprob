chessprob.py

This script transforms the formulas given in [this answer on Math Stack Overflow](https://math.stackexchange.com/questions/3318378/probability-of-duplicated-games-in-chess/3318496#3318496) to [Python](https://www.python.org/) code.

The chessprob module has six functions, corresponding to the formulas in the above link. They calculate the probability that, in a (idealized) set of games ...

* `identical_any()` - any two games are identical
* `identical_pov_player()` - any of the games played by a specific player is identical to any of the other games played by the other players.
* `identical_pov_game()` - a specific game is identical to any other game
* `identical_these_moves()` - any two games are identical and have a specific move order
* `identical_these_moves_pov_player()` - any of the games played by a specific player is identical to any of the games played by the other players and they have a specific move order
* `identical_these_moves_pov_game()` - a specific game is identical to any other game, and they have a specific move order

There are two formulas for each case, one exact formula and an approximation formula. The exact formula gives a precise result but can not calculate bigger inputs in a reasonable time (See the description for the factorial function in the below glossary for the reason why). The approximation formula (the default) is precise up to around five positions after the comma and can calculate even very big inputs in no time.

See the `example_usage.py` for an example.

You can switch between precision and approximation mode by using `set_options(exact=True)` or `set_options(exact=False)`.

### How to use

_Too long, didn´t read_ – See the `example_usage.py`.

The _chessprob_ module behaves like a class.

If you want other that the default options, first use the `set_options()` function to set them. Use the `print_options()` function to print them.

These are the options you can set with `set_options()`:

* `choices` _int_: The amount of choices in a chess position. Defaults to _3_ <sup>[1]</sup>.
* `depth` _int_: Alias ply. The amount of half moves per game. Defaults to _80_, alias 40 moves <sup>[1]</sup>.
* `players` _int_: The amount of chess players. Defaults to _1.500.000.000_. A guess of the amount of chess players in the history of chess.
* `games` _int_: The amount of games every player plays. Defaults to _2500_. A guess of the average amount of games played by the average chess player in his life.
* `exact` _bool_: If the exact algorithms shall be used to calculate the different probabilities. Defaults to _False_ (recommened).
* `precision` _int_: Sets the amount of numbers after the comma. Defaults to _100_.

[1] [Number of Sensible Chess Games](https://en.wikipedia.org/wiki/Shannon_number#Number_of_sensible_chess_games)

###### Other Tools

The `get_formulas()` function returns the formulas of the specific `identical_*` functions you pass to it, as a list of lists of strings. For each function two formulas. The first is the exact and the second the approximation formula.

The `mathify()` function converts such a formula to math syntax.

The `populate()` function replaces the variables of a formula with the current values you have set (see the `set_options()` function).

The `wolfram_open()` function opens a webbrowser and opens each formula passed to it at [wolframalpha.com](https://www.wolframalpha.com/), populated with the current values, where it will be evaluated. This engine can work with bigger numbers when using the exact formulas.

Again, see the `example_usage.py` for examples.

### Glossary

Meaning of variables, operators and functions used in [Eyeballfrogs Answer](https://math.stackexchange.com/questions/3318378/probability-of-duplicated-games-in-chess/3318496#3318496) and in the _chessprob_ module:

Variables:

* **_N_** = `CHOICES` = the amount of move choices in a chess position.
* **_P_** = `DEPTH` = how many half moves a game lasts. 40 moves = 80 half moves.
* **_N<sub>p</sub>_** = `POSSGAMES` = **_N_** ^ **_P_** = all possible different chess games that can be played, depending on **_N_** and **_P_**.
* **_N<sub>c</sub>_** = `PLAYERS` = The amount of players who play games (originally computers).
* **_N<sub>g</sub>_** = `GAMES` = The amount of games each player plays.
* **_N<sub>a</sub>_** = `ALLGAMES` = **_N<sub>c</sub>_** * **_N<sub>g</sub>_** = all games played by all players.

Operators:

* `+` plus
* `-` minus
* `*` multiplication (left away in math notation, where `A B` means _A * B_)
* `/` division (`÷` in math notation)
* `**` power (`^` in math notation)

Functions:

* `fac(number)` The factorial function, eg. `fac(5)` = _1 * 2 * 3 * 4 * 5_ = 120. Written `(number)!` in math notation. Some of the exact algorithms use it, which is why they are slow on big numbers. Eg. if we assume that 3 ^ 80 is [the amount of all possible different chess games with sensible moves](https://en.wikipedia.org/wiki/Shannon_number#Number_of_sensible_chess_games) (already a number with 38 digits), then `fac(3 ^ 80)` is a number with 5577626172914152352366030303784576483327 digits (you can [calculate the amount of digits](https://stackoverflow.com/a/16326545/1658543) but not the number itself).
* `exp(number)` Returns _e ^ number_, where _e_ is 2.718281... – Euler´s number. Most of the approximation functions use this function.


### Credits

Many thanks go to to Eyeballfrog for [providing the formulas](https://math.stackexchange.com/questions/3318378/probability-of-duplicated-games-in-chess/3318496#3318496).

Written by Nils-Hero Lindemann in 2019.08.12.

### License

public domain
