# Calculates average from input CSV file, must be in the same directory
# Interactable CLI program
# The CSV file must be formatted so that:
### The first row is ignored
### Each row has 6 columns separated by commas in the following order:
### subject code, course code, final grade, credit units, semester, year.
# The final grade is ignored if it is a text

from typing import List


def compute_average(grade: List[str], credit: List[str]):
    """
    Computes the weighted average of the given grades.
    For example, if you received 80 and 90 with 3 and 6 credits respectively,
    then the weighted average is 86.6667. Any non-numeric grade/credit entry
    will be ignored.

    :param grade: A list of numeric grades.
    :param credit: A list of credit units associated with each grade in the respective order.
    :return: The weighted average of the input grades.
    """
    n = len(grade)
    assert n == len(credit), "List for grades and credits do not agree in length."
    total_grade_weighted = 0
    total_credit = 0
    for i in range(n):
        if grade[i].isnumeric() and credit[i].isnumeric():
            total_grade_weighted += float(grade[i]) * float(credit[i])
            total_credit += float(credit[i])
    return total_grade_weighted / total_credit


# Read file
filename = "John_Transcript.CSV"
file = open(filename, 'r')
database = {"SBJ": [], "CRS": [], "GRD": [], "CRD": [], "SEM": [], "YER": []}
for row in file.readlines()[1:]:
    row_list = row.rstrip().split(',')
    database["SBJ"].append(row_list[0])
    database["CRS"].append(row_list[1])
    database["GRD"].append(row_list[2])
    database["CRD"].append(row_list[3])
    database["SEM"].append(row_list[4])
    database["YER"].append(row_list[5])
file.close()

print("You have taken {} courses and earned {} credit units so far.".format(len(database["CRS"]),
      sum([float(n) for n in database["CRD"] if n.isnumeric()])))
print("Your overall weighted average is {}.".format(compute_average(database["GRD"], database["CRD"])))
print()

while True:
    print("MAIN MENU: Please select from the options:")
    print("1. List all courses of certain subject(s) and compute the average.")
    print("2. Exit Program.")
    user_input = input("Your Input: ")
    while not user_input.isdigit() or int(user_input) not in range(1, 3):
        user_input = input("Invalid input; try again: ")
    i = int(user_input)
    if i == 1:
        # Fill it up
        print()
    elif i == 2:
        break

print("Program terminated.")
