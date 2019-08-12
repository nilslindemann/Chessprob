from chessprob import *


print_options()
#~ print_options(verbose=True)

print('\nCalculate the probabilities with standard settings')
print(
    identical_any(),
    identical_pov_player(),
    identical_pov_game(),
    identical_these_moves(),
    identical_these_moves_pov_player(),
    identical_these_moves_pov_game(),
    sep='\n'
)


# Use raw=True to get the raw number
#~ print(identical_any())
#~ print(identical_any(raw=True))


print()

# Use small numbers with exact=True, otherwise it will run forever (and it may
# overflow, did not test). eg. try setting depth=9 in the below line and it
# will need around 3 seconds. This time span will grow exponentially.
set_options(exact=True, choices=3, depth=8, players=10, games=10, precision=100)

print_options()


print('\nCalculate the probabilities with the exact formula')
print(
    identical_any(),
    identical_pov_player(),
    identical_pov_game(),
    identical_these_moves(),
    identical_these_moves_pov_player(),
    identical_these_moves_pov_game(),
    sep='\n'
)


print('\nThe same with the approximation formula, for comparision')
set_options(exact=False)
print(
    identical_any(),
    identical_pov_player(),
    identical_pov_game(),
    identical_these_moves(),
    identical_these_moves_pov_player(),
    identical_these_moves_pov_game(),
    sep='\n'
)


print('\n------------------------------------------------\n')

print('Formulas (See the glossary in the README.md for an explanation of these variables)')

for exact, fast in get_formulas(
    identical_any,
    identical_pov_player,
    identical_pov_game,
    identical_these_moves,
    identical_these_moves_pov_player,
    identical_these_moves_pov_game
):
    print(exact, fast, sep='\n')
    # print(mathify(exact), mathify(fast), sep='\n')
    # print(populate(exact), populate(fast), sep='\n')


# open and execute formulas at https://www.wolframalpha.com/
# for exact, fast in get_formulas(identical_any):
#     wolfram_open(exact, fast)


# This should result in a bad approximation, because ( POSSGAMES - (GAMES ** 2) * (PLAYERS ** 2) == 0 ), but it doesnt, why?
# set_options(choices=10, depth=4, players=10, games=10)
# print_options(short=False)
# print(identical_any())
# set_options(exact=True)
# print(identical_any())
