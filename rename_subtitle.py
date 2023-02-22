# The naming scheme of both the subtitle and video must be
# consistent, differing only in the number.
# Both the subtitle and video must be numbered the same way.
# Every consecutive number must be present.
# The first episode must be numbered 0 or 1 (or 00 or 01).
# This script never modifies the video name.

import os

files = os.listdir()
subName = input("Name of first subtitle (including extension): ")
assert subName in files, "File with such name could not be found in local directory."
vidName = input("Name of first video (including extension): ")
assert vidName in files, "File with such name could not be found in local directory."


def nameExtract(name:str) -> tuple[list[str], str]:
    bPassed = False   # marks whether the index is past the first open bracket
    ePassed = False   # marks whether the index is past the file extension
    # iterate backward, the first 1 or 0 after open bracket is episode number
    for i in range(len(name) - 1, -1, -1):
        if ePassed:
            if name[i] == '(' and i != 0:
                # i == 0 implies RAW-name encased in open brackets, ignore this
                bPassed = True
            elif bPassed and (name[i] == '0' or name[i] == '1'):
                if name[i - 1] == '0':
                    # episode number is 00 or 01
                    lst = [name[0:i - 1], name[i + 1:exti], ext]
                    num = name[i - 1:i + 1]
                else:
                    # episode number is 0 or 1
                    lst = [name[0:i], name[i + 1:exti], ext]
                    num = name[i]
                break
        elif name[i] == '.':
            ext = name[i:]
            exti = i
            ePassed = True
    if not bPassed:
        # open bracket missing, ignore it
        for i in range(len(name) - 1, -1, -1):
            if name[i] == '0' or name[i] == '1':
                if name[i - 1] == '0':
                    # 00 or 01
                    lst = [name[0:i - 1], name[i + 1:exti], ext]
                    num = name[i - 1:i + 1]
                else:
                    # 0 or 1
                    lst = [name[0:i], name[i + 1:exti], ext]
                    num = name[i]
                break
    return lst, num


subList, subNum = nameExtract(subName)
vidList, vidNum = nameExtract(vidName)
assert int(subNum) == int(vidNum), "Subtitle and video start with different numbers."

while subList[0] + subNum + subList[1] + subList[2] in files:
    old_subName = subList[0] + subNum + subList[1] + subList[2]
    new_subName = vidList[0] + vidNum + vidList[1] + subList[2]
    if vidList[0] + vidNum + vidList[1] + vidList[2] in files:
        os.rename(old_subName, new_subName)
        print(old_subName)
        print("->", new_subName)

    if len(vidNum) == 1 or int(vidNum) >= 9:
        # 1, 09, etc., no 0 in front for next number
        vidNum = str(int(vidNum) + 1)
    else:
        # 00, 01, etc., 0 in front for next number
        vidNum = '0' + str(int(vidNum) + 1)

    if len(subNum) == 1 or int(subNum) >= 9:
        # 1, 09, etc., no 0 in front for next number
        subNum = str(int(subNum) + 1)
    else:
        # 00, 01, etc., 0 in front for next number
        subNum = '0' + str(int(subNum) + 1)

print("The script ran successfully.")
