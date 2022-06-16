"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    for x in paragraphs:
        if select(x):
            if k == 0:
                return x
            else:
                k = k - 1
    return ''

    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def func(str):
        for x in topic:
            if x in split(lower(remove_punctuation(str))):
                return True
        return False

    return func


    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    correct = 0
    wrong = 0

    for x in range(0,len(typed_words)):
        if x >= len(reference_words):
            wrong += 1
        elif typed_words[x] == reference_words[x]:
            correct += 1
        else:
            wrong += 1

    if typed == '':
        return 0.0

    return (correct / (correct + wrong)) * 100
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'

    # BEGIN PROBLEM 4

    min = elapsed/60
    return (len(typed)/5)/min

    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    diff = ''
    limit_st = limit

    for x in valid_words:
        if x == user_word:
            return x
        elif diff_function(user_word,x,limit) <= limit_st:
            diff = x
            limit_st = diff_function(user_word,x,limit) - 1

    if diff == '':
        return user_word
    else:
        return diff
    # END PROBLEM 5


def sphinx_swap(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    if limit < 0:
        return 100

    if start == '':
        return len(goal)
    elif goal == '':
        return len(start)

    if start[0] == goal[0]:
        return sphinx_swap(start[1:],goal[1:],limit)
    else:
        return sphinx_swap(start[1:],goal[1:],(limit-1)) + 1

    # END PROBLEM 6


def feline_fixes(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""

    if limit < 0:
        return 100

    if start == '':
        return len(goal)
    elif goal == '':
        return len(start)
        # END

    elif start[0] == goal[0]: # Feel free to remove or add additional cases
        # BEGIN
        return feline_fixes(start[1:],goal[1:],limit)
        # END

    else:
        add_diff = feline_fixes(goal[0] + start,goal,(limit-1))
        remove_diff = feline_fixes(start[1:], goal, (limit-1))
        substitute_diff = feline_fixes(goal[0] + start[1:], goal, (limit-1))
        return min(add_diff,remove_diff,substitute_diff) + 1



def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    correct = 0
    i = 0
    while i <len(prompt) and i<len(typed):
        if typed[i] == prompt[i]:
            correct += 1
            i += 1
        else:
            correct += 0
            i = len(prompt)

    send = {}
    send["ID:"] = id
    send["Progress:"] = correct/len(prompt)

    print("ID:", send["ID:"],"Progress:", send["Progress:"])
    print(correct/len(prompt))

    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    timediff1 = []
    timediff2 = []

    i = 0
    k = 0

    while k < len(times_per_player):
        i = 0
        while i < len(words):
            timediff1.append(times_per_player[k][i+1] - times_per_player[k][i])
            i += 1
        timediff2.append(timediff1)
        timediff1 = []
        k += 1
    return game(words, timediff2)
    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    players = range(len(all_times(game)))  # An index for each player
    words = range(len(all_words(game)))    # An index for each word
    # BEGIN PROBLEM 10
    times = all_times(game)
    winners = []
    for i in range(len(times)):
        winners.append([])
    w = []
    for i in range(len(times[0])):
        temp = times[0][i]
        winner = 0
        for j in range(len(times)):
            if times[j][i] < temp:
                temp = times[j][i]
                winner = j
        winners[winner].append(all_words(game)[i])
    return winners
    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = False  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
