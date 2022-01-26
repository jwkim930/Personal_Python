import random as rand
import numpy as np
import sorter as srt


def diceest(face, dice, trial):
    """
    Simulates a given number of dice throws to estimate the probability of getting a number in %.
    Prints the progress to the console in percentage.
    Returns the result as a dictionary,
    where the keys are the numbers (int) and the values are the probabilities in % (float).
    :param face: the number (int) of faces of the dice. For example, enter 6 for D6's.
    :param dice: the number (int) of dices to roll.
    :param trial: the number of dice throws to be made for estimation. Higher the more accurate but takes longer.
    :return: a dictionary mapping the possible numbers to the probability of getting it
    """

    count = {}
    for n in range(dice, face * dice + 1):   # min == # of dice * lowest number (1), max == # of dice * highest number
        count[n] = 0

    for iteration in range(trial):   # repeated (trial) times
        num = 0
        for n in range(dice):   # roll a (face)-sided die (dice) times
            num += rand.randint(1, face)   # randint() IS inclusive!
        count[num] += 1
        print(str(iteration / trial * 100) + "% of the simulations completed")

    for number, occur in count.items():   # convert the counts to %
        count[number] = occur / trial * 100

    print("\n------------------------------------------\n")

    return count


def dicecalc(face, dice):
    """
    Calculates the probability of getting a number by rolling dice, in %.
    Prints the progress to the console in percentage.
    Returns the result as a dictionary,
    where the keys are the numbers (int) and the values are the probabilities in % (float).
    :param face: the number (int) of faces of the dice. For example, enter 6 for D6's.
    :param dice: the number (int) of dices to roll.
    """

    grid = np.zeros([face for i in range(dice)], dtype=int)   # (dice)-D grid with length (face), the result of the list comprehension is [6, 6, 6] for 3D6
    i = np.zeros(dice, dtype=int)   # the index of each dimension as a 1D array, array used for array arithmetic below
    track = 0   # used to track progress (to be printed as %)
    while (i < face - 1).any():   # repeated until i == [face-1 face-1]
        grid[tuple(i)] = (i + 1).sum()
        sat = -1   # checks the index of the last dimension, working upward one by one if "saturated"
        while i[sat] == face - 1:
            i[sat] = 0
            sat -= 1
        i[sat] += 1   # proceed to the next box
        track += 1
        print(str(track / grid.size * 100) + "% of the calculation completed.")
    grid[tuple(i)] = (i + 1).sum()   # the loop terminates just before the last box is filled in, so do this manually

    print("\n-------------------------------------------------\n")
    count = {}
    for n in range(dice, face * dice + 1):   # min == # of dice * lowest number (1), max == # of dice * highest number
        count[n] = grid[grid == n].size / grid.size * 100

    return count


def printresult(ascending, count, limit, bynum):
    """
    Sorts a dictionary based on its values in descending order and prints its contents to the console.
    :param ascending: When set to True, prints the result in ascending order instead.
    :param count: the dictionary to be printed
    :param limit: When set to a positive integer, it will only print that number of the top probabilities.
    If ascending is also set to True, it will only print the lowest probabilities.
    :param bynum: When set to True, sorts the result by the number instead of the probability.
    When used with limit, the items to be displayed are still determined by the probability, not by the number.
    """

    if type(limit) == int:
        csorted = srt.sortdict(count, descend=not ascending)   # first sort by probability
        csorted = srt.sortdict(dict(csorted[0:limit]), bykey=bynum, descend=not ascending)    # slice to length, then (potentially) sort by number

    else:
        csorted = srt.sortdict(count, descend=not ascending, bykey=bynum)

    for item in csorted:
        print(str(item[0]) + ": " + str(item[1]) + "%")


def est(face, dice, trial, limit=None, ascending=False, bynum=False):
    """
    Simulates a given number of dice throws to estimate the probability of getting a number in %.
    Prints the result to the console in descending order based on the probability.
    :param face: the number (int) of faces of the dice. For example, enter 6 for D6's.
    :param dice: the number (int) of dices to roll.
    :param trial: the number of dice throws to be made for estimation. Higher the more accurate but takes longer.
    :param limit: When set to a positive integer, it will only display that number of the top probabilities.
    If ascending is also set to True, it will only print the lowest probabilities.
    :param ascending: When set to True, prints the result in ascending order instead.
    :param bynum: When set to True, sorts the result by the number instead of the probability.
    When used with limit, the items to be displayed are still determined by the probability, not by the number.
    """

    count = diceest(face, dice, trial)

    print("Having thrown " + str(dice) + "D" + str(face) + " " + str(trial) + " times, here are the estimated")
    print("probabilities of getting each number:\n")

    printresult(ascending, count, limit, bynum)


def calc(face, dice, limit=None, ascending=False, bynum=False):
    """
    Calculates the probability of getting a number by rolling dice, in %.
    Prints the result to the console in descending order based on the probability.
    :param face: the number (int) of faces of the dice. For example, enter 6 for D6's.
    :param dice: the number (int) of dices to roll.
    :param limit: When set to a positive integer, it will only display that number of the top probabilities.
    If ascending is also set to True, it will only print the lowest probabilities.
    :param ascending: When set to True, prints the result in ascending order instead.
    :param bynum: When set to True, sorts the result by the number instead of the probability.
    When used with limit, the items to be displayed are still determined by the probability, not by the number.
    """

    count = dicecalc(face, dice)

    print("Here are the probabilities of getting each number when throwing " + str(dice) + "D" + str(face) + ":")

    printresult(ascending, count, limit, bynum)


def rangechance(face, dice, lower, upper, est=False, trial=1000000):
    """
    Prints to the console the probability of getting a number between the lower and the upper bound.
    :param face: the number (int) of faces of the dice. For example, enter 6 for D6's.
    :param dice: the number (int) of dices to roll.
    :param lower: the lower bound (inclusive) of the range, integer
    :param upper: the upper bound (inclusive) of the range, integer
    :param est: When set to True, use estimated values from simulations instead of calculated ones.
    Intended for throws that are too big for to be calculated.
    :param trial: the number of dice throws to be made for estimation. Higher the more accurate but takes longer.
    Only used when est == True. The default is 1 000 000 throws.
    """

    if est:
        count = diceest(face, dice, trial)
    else:
        count = dicecalc(face, dice)

    for num in count.copy().keys():   # remove all numbers not in the range
        if num < lower or num > upper:
            del count[num]

    prob = sum(count.values())

    print("The probability of getting a number between " + str(lower) + " and " + str(upper) + " by throwing " + str(dice) + "D" + str(face) + " is:")
    print(str(prob) + "%")

# This is a test to see if GitHub syncing is working properly. Delete once you see it works.