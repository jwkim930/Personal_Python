import numpy as np


def ienter(row: int, col: int) -> np.ndarray:
  """
  Takes console input from user to get a matrix of integers.
  The input values must all be integers.
  Use enter() for a matrix of floats.

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

  def replace(s: str, i: int, r: str) -> str:
    """
    Returns the string with the character at given index replaced with r.
    :param s: string to have the replacement happen
    :param i: index of the target character
    :param r: string to be used for replacement
    :return: string after the replacement
    """

    return s[0:i] + r + s[i + 1:]

  # take input and fill up
  r = 0   # reset r for new iteration, c should've been reset from the first loop
  vis_i = 0   # this is the index of '*' in visual
  while r != row:
    print(visual)
    new = input("Replace * with: ")
    mx[r, c] = int(new)
    visual = replace(visual, vis_i, new)

    if c == col - 1:  # end of row reached
      r += 1
      c = 0
      visual += "\n"
    else:
      c += 1
      visual += " "

    vis_i += (len(new) + 1)   # new entry + 1 whitespace
    visual = replace(visual, vis_i, "*")

  return mx


def enter(row:int, col:int, showto:int=2, sci:bool=False) -> np.ndarray:
  """
  Takes console input from user to get a matrix of floats.
  Use ienter() for an integer matrix.

  :param col: the number of columns of the matrix
  :param row: the number of rows of the matrix
  :param showto: the decimal place of entry to be shown during entering, default is 2.
  it does not affect the actual value being entered in.
  :param sci: when set to True, entries are entered/shown in scientific notation
  it does not affect the actual value being entered in.
  :return: a numpy array representing the entered matrix
  """

  assert type(row) is int and type(col) is int, "row/col must be integers"
  assert row > 0 and col > 0, "row/col must be positive"

  mx = np.zeros((row, col))
  # build the visual representation

  # For sci == False, the matrix would look something like this (3 by 4 and showto == 2 for example):
  # 0.00 0.00 0.00 0.00
  # 1.00 1.00 **** ----
  # ---- ---- ---- ----
  if not sci:
    keylen = 2 + showto   # number of */- to use, 2 for '0.'
    visual = "*" * keylen
    r = 0
    c = 0
    # insert whitespace appropriately
    if c == col - 1:  # end of row reached
      r += 1
      c = 0
      visual += "\n"
    else:
      c += 1
      visual += " "

    # add '-'s to the rest
    while r != row:
      visual += "-" * keylen
      if c == col - 1:  # end of row reached
        r += 1
        c = 0
        visual += "\n"
      else:
        c += 1
        visual += " "

  # For sci == True:
  # 0.00E0 2.13E6 0.00E0 3.00E8
  # 0.00E0 6.66E6 7.64E2 ******
  # ------ ------ ------ ------
  else:
    keylen = 4 + showto  # 4 for '0.' and 'E0"
    visual = "*" * keylen
    r = 0
    c = 0
    # insert whitespace appropriately
    if c == col - 1:  # end of row reached
      r += 1
      c = 0
      visual += "\n"
    else:
      c += 1
      visual += " "

    # add '-'s to the rest
    while r != row:
      visual += "-" * keylen
      if c == col - 1:  # end of row reached
        r += 1
        c = 0
        visual += "\n"
      else:
        c += 1
        visual += " "

  visual = visual.rstrip()

  def replace(s: str, i: tuple, r: str) -> str:
    """
    Returns the string with the characters at given index range replaced with r.
    :param s: string to have the replacement happen
    :param i: index range (inclusive lower bound, exclusive upper bound) of the characters to be replaced
    :param r: string to be used for replacement
    :return: string after the replacement
    """

    return s[0:i[0]] + r + s[i[1]:]

  # take input and fill up
  r = 0  # reset r for new iteration, c should've been reset from the first loop
  vis_i = 0  # this is the index of the first '*' among '*'s in visual
  while r != row:
    print(visual)
    if not sci:
      new = input("Replace * with: ")
      newf = float(new)
    else:
      new = input("Replace * with (in scientific notation, like 2.34E7): ").upper()
      assert "E" in new, "invalid scientific notation"

      newn = new.split("E")
      newn[0] = float(newn[0])
      newn[1] = int(newn[1])
      newf = newn[0] * (10 ** newn[1])

    mx[r, c] = newf

    if not sci:
      new = format(round(newf, showto), "." + str(showto) + "f")   # round to showto-th place
    else:
      new = format(round(newn[0], showto), "." + str(showto) + "f") + "E" + str(newn[1])

    visual = replace(visual, (vis_i, vis_i + keylen), new)
    if c == col - 1:  # end of row reached
      r += 1
      c = 0
      visual += "\n"
    else:
      c += 1
      visual += " "

    vis_i += len(new) + 1   # new entry + 1 whitespace
    visual = replace(visual, (vis_i, vis_i + keylen), "*" * keylen)

  return mx
