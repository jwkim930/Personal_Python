import numpy as np


def enter(row: int, col: int) -> np.ndarray:
  """
  Takes console input from user to get a matrix.
  Input is taken by each row.
  
  :param col: the number of columns of the matrix
  :param row: the number of rows of the matrix
  :return: a numpy array representing the entered matrix
  """

  assert type(row) is int and type(col) is int, "row/col must be integers"
  assert row > 0 and col > 0, "row/col must be positive"

  mx = np.zeros((row, col), int)
  # build the visual representation
  # The matrix would look something like this (3 by 4 for example):
  # 0 0 0 0
  # 1 1 * -
  # - - - -

  visual = "*"   # this is the visual representation
  r = 0   # row-coordinate for iteration
  c = 0   # col-coordinate for iteration
  # insert whitespace appropriately
  if c == col - 1:  # end of row reached
    r += 1
    c = 0
    visual += "\n"
  else:
    c += 1
    visual += " "

  # add '-' to the rest
  while r != row:
    visual += "-"
    if c == col - 1:  # end of row reached
      r += 1
      c = 0
      visual += "\n"
    else:
      c += 1
      visual += " "
  visual = visual.rstrip()
  
  # take input and fill up
  def replace(s:str, i:int, r:str) -> str:
    """
    Returns the string with the character at given index replaced with r.
    :param s: string to have the replacement happen
    :param i: index of the target character
    :param r: string to be used for replacement
    :return: string after the replacement
    """

    return s[0:i] + r + s[i+1:]

  def locate(vis:str, width:int, row:int, col:int) -> int:
    """
    Determines the string-index of the visual representation of the matrix
    for a particular entry.

    :param vis: the visual representation of the matrix
    :param width: the number of columns of the matrix
    :param row: which row the entry is at
    :param col: which column the entry is at
    :return: the string-index of the entry
    """

    # each entry is separated by one whitespace, either ' ' or '\n'
    # the first entry never follows a whitespace, and the last entry is never followed by a whitespace
    # determine what-th entry the entry of interest is by left to right and top to bottom,
    # then count string-index towards it linearly

    th = (row * width) + col
    # th is what-th entry it is, calculated by (# of entries for the rows above) + (# of entries in current row)
    # th == 0 for the first entry

    i = 0   # string-index to be returned
    entry = 0   # entry being inspected
    while entry != th:
      if vis[i] == " " or vis[i] == "\n":
        entry += 1
      i += 1

    return i

  r = 0   # reset r for new iteration, c should've been reset from the first loop
  while r != row:
    print(visual)
    new = input("Replace * with: ")
    mx[r, c] = int(new)
    visual = replace(visual, locate(visual, col, r, c), new)

    if c == col - 1:  # end of row reached
      r += 1
      c = 0
      visual += "\n"
    else:
      c += 1
      visual += " "

  return mx
