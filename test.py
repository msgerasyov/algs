import numpy as np
import re
import string
import tracemalloc
from hash_table import HashTable

sample_text = \
"""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
    tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
    quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
    commodo consequat. Duis aute irure dolor in reprehenderit in
    voluptate velit esse cillum dolore eu fugiat nulla pariatur.
    Excepteur sint occaecat cupidatat non proident,
    sunt in culpa qui officia deserunt mollit anim id est laborum.
"""

def generate_test(filename, size=100, p_insert=0.6, p_remove=0.1, p_get=0.3,
                  text=sample_text, max_key=2**16):
    """
    Generates a text file with insert, remove and get commands for
    testing the developed hash table container.

    Parameters
    ----------
    filename : str
        The name of the output file
    size : int, optional
        The number of actions to generate
    p_insert, p_remove, p_get : int, optional
        Probabilities of generating respected actions
    text : str, optional
        Text used for sampling values for insertion
    max_key : int, optimal
        Maximum value for generated keys
    """
    words = [word.strip(",.") for word in text.split() if word != ""]
    actions = ["insert", "remove", "get"]
    chosen_actions = []
    keys = [0]
    for _ in range(size):
        action = np.random.choice(actions, p=(p_insert, p_remove, p_get))
        chosen_actions.append(action)
    with open(filename, "w") as f:
        for action in chosen_actions:
            if action == "insert":
                key = np.random.randint(max_key)
                value = np.random.choice(words)
                f.write("{0}({1}, {2})\n".format(action, key, value))
                keys.append(key)
            else:
                key = np.random.choice(keys)
                f.write("{0}({1})\n".format(action, key))

def test(container, filename):
    with open(filename, "r") as f:
        for line in f:
            m=re.match("^\s*(\w+)\s*\((.*)\)", line)
            action = m.group(1)
            params = m.group(2).split(', ')
            params[0] = int(params[0])
            if action == "insert":
                container.insert(*params)
            elif action == "remove":
                container.remove(*params)
            else:
                print(container.get(*params))
    return container


if __name__ == "__main__":

    tracemalloc.start()

    container = HashTable()
    #basic tests
    container.insert(123494893, "second")
    container.insert(123494893, "first")
    print(container.get(123494893))
    container.remove(123494893)
    print(container.get(123494893))
    container.insert(10, "ten")

    #large-scale test
    #generate_test("sample_test.txt", 2000)
    container = test(container, "sample_test.txt")

    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
    tracemalloc.stop()
    print("Elements:", len(container))
