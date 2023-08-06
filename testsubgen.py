import random as rand
import os

VFORMATH = "[Legit] Video Name - "   # First part of the video name desired
VFORMATT = " (1920x1080 AAC).mkv"   # Last part of the video name desired
SFORMATH = "[Not-Legit] Subtitle Name - "   # First part of the subtitle name desired
SFORMATT = " (1920x1080 AAC).ass"   # Last part of the subtitle name desired
VNUM = "01"   # Video numbering
SNUM = "01"   # Subtitle numbering
TNUM = 12   # Number of files
RANDOMIZE_SUB = True   # If true, add a randomized string to the beginning of SFORMATT
RANDOMIZE_VID = True   # If true, add a randomized string to the beginning of VFORMATT
INCLUDE_OVA = True   # If true, add a video + subtitle pair with the episode number "OVA"


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


if os.path.isdir("Test"):
    files = os.listdir("Test")
    for f in files:
        os.remove("Test\\" + f)
else:
    os.mkdir(os.getcwd() + "\\Test")

for i in range(TNUM):
    sub_tail = " [" + str(rand.randint(100000, 999999)) + "]" + SFORMATT if RANDOMIZE_SUB else SFORMATT
    vid_tail = " [" + str(rand.randint(100000, 999999)) + "]" + VFORMATT if RANDOMIZE_VID else VFORMATT
    vname = os.getcwd() + "\\Test\\" + VFORMATH + VNUM + vid_tail
    sname = os.getcwd() + "\\Test\\" + SFORMATH + SNUM + sub_tail
    open(vname, 'x').close()
    open(sname, 'x').close()
    VNUM = add1(VNUM)
    SNUM = add1(SNUM)
if INCLUDE_OVA:
    sub_tail = " [" + str(rand.randint(100000, 999999)) + "]" + SFORMATT if RANDOMIZE_SUB else SFORMATT
    vid_tail = " [" + str(rand.randint(100000, 999999)) + "]" + VFORMATT if RANDOMIZE_VID else VFORMATT
    vname = os.getcwd() + "\\Test\\" + VFORMATH + "OVA" + vid_tail
    sname = os.getcwd() + "\\Test\\" + SFORMATH + "OVA" + sub_tail
    open(vname, 'x').close()
    open(sname, 'x').close()
