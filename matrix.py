import numpy as np


def enter(row: int, col: int) -> np.ndarray:
  """
  Takes console input from user to get a matrix.
  Input is taken by each row.
  
  :param col: the number of columns of the matrix
  :param row: the number of rows of the matrix
  :return: a numpy array representing the entered matrix
  """

  mx = np.zeros((row, col), int)

  def show_mx(mx:np.ndarray, row:int, col:int) -> str:
    """
    Gives the visual representation of the array being built.
    '*' represents the entry being entered,
    and '-' represents entries not entered yet.

    :param mx: the matrix to be shown
    :param col: the column currently being entered
    :param row; the row currently being entered
    :return: the visual representation of the matrix
    """

    # The matrix would look something like this (3 by 4 for example):
    # 0 0 0 0
    # 1 1 * -
    # - - - -

    visual = ""   # this is the visualized matrix

    # fill up the ones already entered
    r = 0
    c = 0
    height = mx.shape[0]
    width = mx.shape[1]
    while not(r == row and c == col):
      visual += str(mx[r, c])
      if c == width - 1:  # end of row reached
        r += 1
        c = 0
        visual += "\n"
      else:
        c += 1
        visual += " "

    # add * to where the new entry should go
    visual += "*"
    if c == width - 1:  # end of row reached
      r += 1
      c = 0
      visual += "\n"
    else:
      c += 1
      visual += " "

    # add - to the rest
    while r != height:
      visual += "-"
      if c == width - 1:  # end of row reached
        r += 1
        c = 0
        visual += "\n"
      else:
        c += 1
        visual += " "

    return visual
  
  for r in range(row):
    for c in range(col):
      print(show_mx(mx, r, c))
      mx[r, c] = input("Replace * with: ")
    
  return mx


print(enter(3,4))
