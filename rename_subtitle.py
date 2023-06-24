# The naming scheme of both the subtitle and video must be
# consistent, differing only in the number.
# It's okay for characters after the episode number to differ.
# The file extensions for subtitles must be the same,
# same for videos.
# Every consecutive number must be present.
# This script never modifies the video name
# as long as the initial setup is done properly.

import os

import natsort


def nameExtract(name:str, elem=None) -> list[str]:
    """
    Extract elements of name from the input filename.
    The parts are as follows:
    1. The characters before the episode count
    2. The characters representing the episode number
    3. The characters after the episode count, before file extension
    4. File extension, including '.'

    This function prompts the user to confirm the position of the episode number.
    If the list of element is given, then it assumes that the overall layout are the same
    (and thus doesn't prompt the user for input).

    :param name: The file name to be split
    :param elem: A list produced from running nameExtract() on a name.
    :return: A list of 4 strings as described above
    """
    if elem is None:
        # no elem given
        return nameExtractInitial(name)
    elif len(elem) == 4:
        # elem given
        result = [elem[0]]   # first part shouldn't have changed
        epsStartIndex = len(elem[0])
        epsEndIndex = epsStartIndex
        while name[epsEndIndex + 1].isnumeric() and epsEndIndex + 1 < len(name):
            epsEndIndex += 1
        result.append(name[epsStartIndex : epsEndIndex + 1])   # episode number
        result.append(name[epsEndIndex + 1 : len(name) - len(elem[3])])   # after episode number
        result.append(name[len(name) - len(elem[3]):])   # extension
        return result
    else:
        assert True, "Invalid argument; list elem must have 4 strings."


def nameExtractInitial(name:str) -> list[str]:
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
                while j+1 < len(name) and name[j+1].isnumeric():
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


def filterbyepisode(filenames:list[str], elem:list[str]) -> list[str]:
    """
    Returns a list of filenames for same or later episodes.

    :param filenames: The list of subtitle/video file names.
    :param elem: The list created by running nameExtract() on the earliest episode.
    :return: The sorted list of subtitle/video file names.
    """
    result = []
    for file in filenames:
        eps = int(nameExtract(file, elem)[1])
        if eps >= int(elem[1]):
            result.append(file)
    return result


files = os.listdir()
files = natsort.natsorted(files)

subName = input("Name of first subtitle (including extension): ")
assert subName in files, "File with such name could not be found in local directory."
vidName = input("Name of first video (including extension): ")
assert vidName in files, "File with such name could not be found in local directory."

subElem = nameExtract(subName)
subList = []
vidElem = nameExtract(vidName)
vidList = []
sub_vid_episode_delta = int(subElem[1]) - int(vidElem[1])
if sub_vid_episode_delta != 0:
    response = input("The episode names do not seem to match. Are you sure this is correct? (Y/N): ").lower()
    if response != "y":
        print("Terminating script with no name change.")
        exit(0)

# separate subtitles and videos
# filter each by comparing only the first part
for name in files:
    ext = ''  # file extension
    for i in range(len(name) - 1, -1, -1):
        # separate file extension from name
        if name[i] == '.':
            ext = name[i:]
            break
    # both extension and first part of the name must match
    if ext == subElem[3] and name[:len(subElem[0])] == subElem[0]:
        subList.append(name)
    elif ext == vidElem[3] and name[:len(vidElem[0])] == vidElem[0]:
        vidList.append(name)

# exclude subtitles/videos beyond the first one given
subList = filterbyepisode(subList, subElem)
vidList = filterbyepisode(vidList, vidElem)

# change name
while len(vidList) > 0 and len(subList) > 0:
    # create new name
    vidname = vidList.pop(0)
    vid_elements = nameExtract(vidname, vidElem)
    old_subname = subList.pop(0)
    sub_elements = nameExtract(old_subname, subElem)
    if int(sub_elements[1]) != int(vid_elements[1]) + sub_vid_episode_delta:
        break   # some episode number is missing
    new_subname = vid_elements[0] + vid_elements[1] + vid_elements[2] + sub_elements[3]

    # change name
    os.rename(old_subname, new_subname)
    print(old_subname)
    print("->", new_subname)

print("The script ran successfully.")
