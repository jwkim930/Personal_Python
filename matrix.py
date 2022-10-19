import numpy as np
from typing import Union


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


def mult(*matrices:np.ndarray) -> np.ndarray:
  """
  Returns the product of the matrices.
  At least 2 matrices are required.

  :param matrices: any number of matrices to be multiplied together.
  the matrix multiplication must be defined.
  :return: the product of matrices used as argument
  """
  assert len(matrices) >= 2, "at least 2 matrices are required"

  prod = np.dot(matrices[0], matrices[1])   # product to be returned
  for i in range(2, len(matrices)):
    prod = np.dot(prod, matrices[i])

  return prod


def add(*matrices:np.ndarray) -> np.ndarray:
  """
  Returns the sum of the matrices.
  At least 2 matrices are required.

  :param matrices: any number of matrices to be added together.
  all matrices must have the same dimension.
  :return: the sum of the matrices used as argument
  """
  assert len(matrices) >= 2, "at least 2 matrices are required"

  msum = np.add(matrices[0], matrices[1])   # sum to be returned
  for i in range(2, len(matrices)):
    msum = np.add(msum, matrices[i])

  return msum


def smul(c:Union[int, float], m:np.ndarray) -> np.ndarray:
  """
  Returns the scalar multiple of the matrix.

  :param c: the scalar to be multiplied to
  :param m: the matrix to be multiplied
  :return: the resulting matrix
  """
  return c * m


def subt(m1:np.ndarray, m2:np.ndarray) -> np.ndarray:
  """
  Returns the difference of two matrices, m1 - m2.
  m1 and m2 must have the same dimension.

  :param m1: matrix to be subtracted from
  :param m2: matrix to subtract
  :return: the matrix resulting from subtraction
  """
  return add(m1, smul(-1, m2))


def det(m:np.ndarray) -> Union[int, float]:
  """
  Returns the determinant of the matrix.
  The input matrix must be a 2-dimensional square matrix.

  :param m: a 2-dimensional square matrix
  :return: the determinant of the matrix
  """
  
  assert m.ndim == 2, "matrix must be 2-dimensional"
  assert m.shape[0] == m.shape[1], "matrix must be square"

  l = m.shape[0]   # length
  if l == 1:
    return m[0,0]
  elif l == 2:
    return (m[0,0] * m[1,1]) - (m[0,1] * m[1,0])
  else:
    result = 0
    for col in range(l):
      # expand matrix along the first row
      left_piece = m[1:l, 0:col]
      right_piece = m[1:l, col+1:l]
      piece = np.hstack((left_piece, right_piece))

      result += (-1)**(col) * m[0, col] * det(piece)
    
    return result
    