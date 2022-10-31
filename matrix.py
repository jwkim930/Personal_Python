import numpy as np
from typing import Union


class matrixer(object):
  def __init__(self, mx:np.ndarray):
    """
    TO USERS: Please use ienter() or enter() instead of initializing directly.
    """
    self.__matrix = mx
    self.dim = mx.shape
    self.dtype = mx.dtype

  def __repr__(self):
    mx = self.__matrix
    return str(mx)

  def __str__(self):
    mx = self.__matrix
    return str(mx)

  def __add__(self, b):
    assert type(b) is matrixer, "addition must be between matrices"
    return matrixer(np.add(self.__matrix, b.__matrix))

  def __mul__(self, b):
    assert type(b) in (matrixer, int, float), "can only multiply number or matrix"
    if type(b) is matrixer:
      return matrixer(np.dot(self.__matrix, b.__matrix))
    else:
      return matrixer(np.dot(self.__matrix, b))

  def __sub__(self, b):
    assert type(b) is matrixer, "subtraction must be between matrices"
    return self + (b * (-1))

  def det(self) -> Union[int, float]:
    """
    Returns the determinant of the matrix.
    The matrix must be a non-empty 2-dimensional square matrix.
    The determinant of an empty matrix is 1.

    :return: the determinant of the matrix
    """

    assert self.dim[0] == self.dim[1], "matrix must be square"

    l = self.dim[0]  # length
    m = self.__matrix

    def de(m, l):
      if l == 0:
        return 1
      if l == 1:
        return m[0, 0]
      elif l == 2:
        return (m[0, 0] * m[1, 1]) - (m[0, 1] * m[1, 0])
      else:
        result = 0
        for col in range(l):
          # expand matrix along the first row
          left_piece = m[1:l, 0:col]
          right_piece = m[1:l, col + 1:l]
          piece = np.hstack((left_piece, right_piece))

          result += (-1) ** (col) * m[0, col] * de(piece, l - 1)

        return result

    return de(m, l)


def ienter(row: int, col: int) -> matrixer:
  """
  Takes console input from user to get a matrix of integers.
  The input values must all be integers.
  Use enter() for a matrix of floats.

  :param col: the number of columns of the matrix
  :param row: the number of rows of the matrix
  :return: a matrix object representing the entered matrix
  """
  assert type(row) is int and type(col) is int, "row/col must be integers"
  assert row > 0 and col > 0, "row/col must be positive"

  mx = np.zeros((row, col), int)
  # build the visual representation
  # The matrix would look something like this (3 by 4 for example):
  # 0 0 0 0
  # 1 1 * -
  # - - - -

  visual = "*"  # this is the visual representation
  r = 0  # row-coordinate for iteration
  c = 0  # col-coordinate for iteration
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
  r = 0  # reset r for new iteration, c should've been reset from the first loop
  vis_i = 0  # this is the index of '*' in visual
  while r != row:
    print(visual)
    new = input("Replace * with: ")
    while not new.lstrip('-').isnumeric():
      new = input("Non-integer input, try again: ")
    mx[r, c] = int(new)

    visual = replace(visual, vis_i, new)
    if c == col - 1:  # end of row reached
      r += 1
      c = 0
      visual += "\n"
    else:
      c += 1
      visual += " "

    vis_i += (len(new) + 1)  # new entry + 1 whitespace
    visual = replace(visual, vis_i, "*")

  return matrixer(mx)


def enter(row:int, col:int, showto:int=2, sci:bool=False) -> matrixer:
  """
  Takes console input from user to get a matrix of floats.
  Use ienter() for an integer matrix.

  :param col: the number of columns of the matrix
  :param row: the number of rows of the matrix
  :param showto: the decimal place of entry to be shown during entering, default is 2.
                 it does not affect the actual value being entered in.
  :param sci: when set to True, entries are entered/shown in scientific notation
              it does not affect the actual value being entered in.
  :return: a matrix object representing the entered matrix
  """
  mx = np.zeros((row, col))
  # build the visual representation
  # For sci == False, the matrix would look something like this (3 by 4 and showto == 2 for example):
  # 0.00 0.00 0.00 0.00
  # 1.00 1.00 **** ----
  # ---- ---- ---- ----
  if not sci:
    keylen = 2 + showto  # number of */- to use, 2 for '0.'
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

  def isfloat(s: str) -> bool:
    """
    Returns true if string can be converted to float, false otherwise.

    :param s: string to be checked
    :return: true/false
    """
    try:
      float(s)
      return True
    except ValueError:
      return False

  while r != row:
    print(visual)
    if not sci:
      new = input("Replace * with: ")

      while not isfloat(new):
        new = input("Non-float input, try again: ")
      newf = float(new)
    else:
      new = input("Replace * with (in scientific notation, like 2.34E7): ").upper()

      def issci(s:str) -> bool:
        """
        Returns true is string is in proper scientific notation, false otherwise.

        :param s: string to be checked
        :return: true/false
        """
        s = s.lstrip('-')   # negative is irrelevant for this
        # shortest string denoting scientific notation is 3 characters long (e.g. 3e0)
        if isfloat(s) and len(s) >= 3:
          # s[1] must be either '.' (e.g. 3.00e8) or 'E' (e.g. 2e8) for positive
          return 'E' in s and s[1] in ('.', 'E')

        return False

      while not issci(new):
        new = input("Invalid scientific notation, try again: ").upper()

      newf = float(new)   # actual value to go into matrix
      newn = new.split("E")   # used for displaying values
      newn[0] = float(newn[0])
      newn[1] = int(newn[1])

    mx[r, c] = newf

    if not sci:
      new = format(round(newf, showto), "." + str(showto) + "f")  # round to showto-th place
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

    vis_i += len(new) + 1  # new entry + 1 whitespace
    visual = replace(visual, (vis_i, vis_i + keylen), "*" * keylen)

  return matrixer(mx)


def zero(row:int, col:int, dtype:type=float) -> matrixer:
  """
  Returns a zero matrix of the given size. Entries are in float by default.

  :param row: number of rows
  :param col: number of columns
  :param dtype: set to int or float to control data type
  :return: the row by col zero matrix
  """
  return matrixer(np.zeros((row, col), dtype))


def identity(n:int, dtype:type=float) -> matrixer:
  """
  Returns an identity matrix of the given size. Entries are in float by default.

  :param n: the size of the identity matrix
  :param dtype: set to int or float to control data type
  :return: the n by n identity matrix
  """
  return matrixer(np.identity(n, dtype))
