# The naming scheme of both the subtitle and video must be
# consistent, differing only in the number.
# Every consecutive number must be present.
# This script never modifies the video name.

import os

files = os.listdir()
subName = input("Name of first subtitle (including extension): ")
assert subName in files, "File with such name could not be found in local directory."
vidName = input("Name of first video (including extension): ")
assert vidName in files, "File with such name could not be found in local directory."


def nameExtract(name:str) -> list[str]:
    """
    Extract elements of name from the input filename.
    The parts are as follows:
    1. The characters before the episode count
    2. The characters representing the episode number
    3. The characters after the episode count, before file extension
    4. File extension, including '.'

    This function prompts the user to confirm the position of the episode number.

    :param name: The file name to be split
    :return: A list of 4 strings as described above
    """
    ext = ''   # file extension
    for i in range(len(name)-1, -1, -1):
        # separate file extension from name
        if name[i] == '.':
            ext = name[i:]
            name = name[0:i]
            break
    epis = ''   # episode number
    pre = ''   # characters before epis
    post = ''   # characters after epis
    i = 0   # index of beginning of episode name
    j = 0   # index of end of episode name
    while epis == '':
        while i < len(name):
            if name[i].isnumeric():
                j = i
                while name[j+1].isnumeric() and j+1 < len(name):
                    j += 1
                break
            else:
                i += 1
        assert i < len(name), "No number could be found in the filename: " + name + ext
        resp = ''
        while resp != 'y' and resp != 'n':
            print()
            print(name[0:i] + '***' + name[i:j+1] + '***' + name[j+1:])
            print("Are the characters marked like ***num*** the episode number?")
            resp = input("Enter Y or N: ").lower()
        if resp == 'y':
            pre = name[0:i]
            epis = name[i:j+1]
            post = name[j+1:]
        else:
            i = j + 1
    return [pre, epis, post, ext]


def add1(num:str):
    """
    Adds 1 to the episode number while retaining its general format.

    :param num: episode number
    :return: episode number + 1
    """
    n = int(num) + 1
    nxt = str(n)
    if len(nxt) < len(num):
        # missing leading zeros, such as going from 01 to 2
        diff = len(num) - len(nxt)
        nxt = diff * '0' + nxt
    return nxt


subElem = nameExtract(subName)
vidElem = nameExtract(vidName)

while subElem[0] + subElem[1] + subElem[2] + subElem[3] in files:
    old_subName = subElem[0] + subElem[1] + subElem[2] + subElem[3]
    new_subName = vidElem[0] + vidElem[1] + vidElem[2] + subElem[3]
    if vidElem[0] + vidElem[1] + vidElem[2] + vidElem[3] in files:
        os.rename(old_subName, new_subName)
        print(old_subName)
        print("->", new_subName)
    subElem[1] = add1(subElem[1])
    vidElem[1] = add1(vidElem[1])

print("The script ran successfully.")
