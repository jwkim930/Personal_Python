# Calculates average from input CSV file, must be in the same directory
# Interactable CLI program
# The CSV file must be formatted so that:
### The first row is ignored
### Each row has 6 columns separated by commas in the following order:
### subject code, course code, final grade, credit units, semester, year.
# The final grade is ignored if it is a text

from typing import *
from tabulate import tabulate


def compute_average(grade: List[str], credit: List[str]) -> float:
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


def get_subjects(sbj: List[str]) -> List[str]:
    """
    Returns a list of unique subjects in the given list of subjects.
    :param sbj: A list of subjects to search through.
    :return: Unique subjects in the given list of subjects.
    """
    result = []
    for sub in sbj:
        if sub not in result:
            result.append(sub)
    return result


def tabulate_database(database: dict) -> None:
    """
    Prints to the console a table showing the content of the database.
    Entries are sorted in alphabetical order by subject name, then by
    the course code.

    :param database: The database dictionary to be printed.
    """
    # Convert database dictionary to list of lists
    table = []
    for i in range(len(database["SBJ"])):
        row = [database["SBJ"][i], database["CRS"][i], database["GRD"][i],
               database["CRD"][i], database["SEM"][i], database["YER"][i]]
        table.append(row)
    # Sort by subject, then course code
    # Done by concatenating the two and sorting normally
    table.sort(key=lambda row: row[0] + row[1])
    print(tabulate(table, headers=["Subject", "Course Code", "Grade", "Credit", "Semester", "Year"]))


def print_credit_average(database: dict) -> None:
    """
    Prints to the console the number of courses taken, the total credits earned,
    and the weighted average.

    :param database: The database dictionary to base the calculation off of.
    """
    print("You have taken {} courses and earned {} credit units so far.".format(len(database["SBJ"]),
                                                                                sum([float(n) for n in database["CRD"]
                                                                                     if n.isnumeric()])))
    print("Your overall weighted average is {}.".format(compute_average(database["GRD"], database["CRD"])))


def take_input_criteria(*criteria: Callable[[str], bool]) -> str:
    """
    Re-prompts the user until a valid input is given based on the criteria.
    If multiple criteria are given, every criterion must be met.
    This function uses short-circuit boolean operation; that is, if the first given criterion fails,
    then the user is re-prompted without evaluating the remaining criteria.

    :param criteria: Callable (such as function) that takes one string as input (which will be the string
                     from input()) and returns True if the input is valid, False if invalid.
    :return: The validated input string.
    """
    return take_input_criteria_run(lambda a: a, *criteria)


def take_input_criteria_run(run: Callable[[str], str], *criteria: Callable[[str], bool]) -> str:
    """
    Re-prompts the user until a valid input is given based on the criteria.
    If multiple criteria are given, every criterion must be met.
    This function uses short-circuit boolean operation; that is, if the first given criterion fails,
    then the user is re-prompted without evaluating the remaining criteria.

    :param criteria: Callable (such as function) that takes one string as input (which will be the string
                     from input()) and returns True if the input is valid, False if invalid.
    :param run: A Callable to be called on the input string before evaluating the string.
                If used, the returned string will also have this applied.
    :return: The validated input string.
    """
    inp = run(input("Your input: "))
    valid = True
    for crit in criteria:
        if not crit(inp):
            valid = False
            break
    while not valid:
        inp = run(input("Invalid input; try again: "))
        for crit in criteria:
            if crit(inp):
                valid = True
            else:
                valid = False
                break
    return inp


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

course_count = len(database["SBJ"])
print_credit_average(database)

while True:
    print()
    print("MAIN MENU: Please select from the options:")
    print("1. List all courses.")
    print("2. List all courses of certain subject(s) and compute the average.")
    print("3. List all courses that are 200-level or above.")
    print("4. Exit Program.")
    user_input = take_input_criteria(lambda inp: inp.isdigit(), lambda inp: int(inp) in range(1, 5))
    i = int(user_input)
    if i == 1:
        tabulate_database(database)
        print_credit_average(database)
    elif i == 2:
        # Take input to select subjects
        subjects = get_subjects(database["SBJ"])
        print("You have taken courses in the following subjects:")
        print(', '.join(subjects).rstrip())
        print("Please enter the subject code(s) to list out, separated by commas.")

        def is_valid_subjects(sub: str) -> bool:
            global subjects
            return set(sub.split(',')).issubset(subjects)
        user_input = take_input_criteria_run(lambda inp: inp.replace(' ', '').upper(), is_valid_subjects)
        targets = user_input.split(',')
        # Filter out the database
        filtered_database = {"SBJ": [], "CRS": [], "GRD": [], "CRD": [], "SEM": [], "YER": []}
        for i in range(course_count):
            if database["SBJ"][i] in targets:
                filtered_database["SBJ"].append(database["SBJ"][i])
                filtered_database["CRS"].append(database["CRS"][i])
                filtered_database["GRD"].append(database["GRD"][i])
                filtered_database["CRD"].append(database["CRD"][i])
                filtered_database["SEM"].append(database["SEM"][i])
                filtered_database["YER"].append(database["YER"][i])
        tabulate_database(filtered_database)
        print_credit_average(filtered_database)
    elif i == 3:
        filtered_database = {"SBJ": [], "CRS": [], "GRD": [], "CRD": [], "SEM": [], "YER": []}
        for i in range(course_count):
            if int(database["CRS"][i][0]) >= 2:
                filtered_database["SBJ"].append(database["SBJ"][i])
                filtered_database["CRS"].append(database["CRS"][i])
                filtered_database["GRD"].append(database["GRD"][i])
                filtered_database["CRD"].append(database["CRD"][i])
                filtered_database["SEM"].append(database["SEM"][i])
                filtered_database["YER"].append(database["YER"][i])
        tabulate_database(filtered_database)
        print_credit_average(filtered_database)
    elif i == 4:
        break
    input("Press enter to return to the main menu...")
print("Program terminated.")
