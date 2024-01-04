# Calculates average from input CSV file, must be in the same directory
# Interactable CLI program
# The CSV file must be formatted so that:
### The first row is ignored
### Each row has 6 columns separated by commas in the following order:
### subject code, course code, final grade, credit units, semester, year.
# The final grade is ignored if it is a text

from typing import *
from tabulate import tabulate
from copy import deepcopy


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


def tabulate_database(data: dict) -> None:
    """
    Prints to the console a table showing the content of the database.
    Entries are sorted in alphabetical order by subject name, then by
    the course code.

    :param data: The database dictionary to be printed.
    """
    # Convert database dictionary to list of lists
    table = []
    for i in range(len(data["SBJ"])):
        row = [data["SBJ"][i], data["CRS"][i], data["GRD"][i],
               data["CRD"][i], data["SEM"][i], data["YER"][i]]
        table.append(row)
    # Sort by subject, then course code
    # Done by concatenating the two and sorting normally
    table.sort(key=lambda row: row[0] + row[1])
    print(tabulate(table, headers=["Subject", "Course Code", "Grade", "Credit", "Semester", "Year"]))


def print_credit_average(data: dict) -> None:
    """
    Prints to the console the number of courses taken, the total credits earned,
    and the weighted average.

    :param data: The database dictionary to base the calculation off of.
    """
    print("You have taken {} courses and earned {} credit units so far.".format(len(data["SBJ"]),
                                                                                sum([float(n) for n in data["CRD"]
                                                                                     if n.isnumeric()])))
    print("Your overall weighted average is {}.".format(compute_average(data["GRD"], data["CRD"])))


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

    :param run: A Callable to be called on the input string before evaluating the string.
                If used, the returned string will also have this applied.
    :param criteria: Callable (such as function) that takes one string as input (which will be the string
                     from input()) and returns True if the input is valid, False if invalid.
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


def filter_database(data: Dict[str, List[str]],
                    *criteria: Callable[[str, str, str, str, str, str], bool]) -> Dict[str, List[str]]:
    """
    Returns a database dictionary only with entries that satisfy the given criteria.

    :param data: The database to filter from.
    :param criteria: The Callable(s) to be called on each entry. This must take 6 strings as arguments,
                     each representing the keys SBJ, CRS, GRD, CRD, SEM, YER in the respective order.
                     It should return True if this entry should be included, False otherwise.
    :return: The filtered database dictionary.
    """
    result = {"SBJ": [], "CRS": [], "GRD": [], "CRD": [], "SEM": [], "YER": []}
    for i in range(len(data["SBJ"])):
        valid = True
        for crit in criteria:
            if not crit(data["SBJ"][i], data["CRS"][i], data["GRD"][i], data["CRD"][i], data["SEM"][i], data["YER"][i]):
                valid = False
                break
        if valid:
            result["SBJ"].append(data["SBJ"][i])
            result["CRS"].append(data["CRS"][i])
            result["GRD"].append(data["GRD"][i])
            result["CRD"].append(data["CRD"][i])
            result["SEM"].append(data["SEM"][i])
            result["YER"].append(data["YER"][i])
    return result


def filter_builder(criteria_simplified: Callable[..., bool],
                   *keys_to_be_used: str) -> Callable[[str, str, str, str, str, str], bool]:
    """
    Helper function to expedite building filter function for filter_database().

    :param criteria_simplified: The Callable to be called on each entry.
                                The number of its arguments should agree with the number of keys_to_be_used.
    :param keys_to_be_used: Some or all of SBJ, CRS, GRD, CRD, SEM, YER, representing the keys to be considered
                            in the filter Callable in the respective order for the positional argument.
    :return: The filtering function(s) to be passed into filter_database().
    """
    order = ["SBJ", "CRS", "GRD", "CRD", "SEM", "YER"]

    def filter_function(SBJ: str, CRS: str, GRD: str, CRD: str, SEM: str, YER: str) -> bool:
        original_arguments = [SBJ, CRS, GRD, CRD, SEM, YER]
        arguments = []
        for key in keys_to_be_used:
            j = order.index(key)
            arguments.append(original_arguments[j])
        return criteria_simplified(*tuple(arguments))
    return filter_function


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

# Main loop
while True:
    print()
    print("MAIN MENU: Please select from the options:")
    print("1. List all courses.")
    print("2. List all courses of certain subject(s) and compute the average.")
    print("3. List all courses that are 200-level or above.")
    print("4. Simulate the overall credit & average with additional courses.")
    print("5. Exit Program.")
    user_input = take_input_criteria(lambda inp: inp.isdigit(), lambda inp: int(inp) in range(1, 6))
    input_int = int(user_input)
    if input_int == 1:
        tabulate_database(database)
        print_credit_average(database)
    elif input_int == 2:
        # Take input to select subjects
        subjects = get_subjects(database["SBJ"])
        print("You have taken courses in the following subjects:")
        print(', '.join(subjects).rstrip())
        print("Please enter the subject code(s) to list out, separated by commas.")
        user_input = take_input_criteria_run(lambda inp: inp.replace(' ', '').upper(),
                                             lambda inp: set(inp.split(',')).issubset(subjects))
        targets = user_input.split(',')
        # Filter and print
        filtered_database = filter_database(database, filter_builder(lambda s: s in targets, "SBJ"))
        tabulate_database(filtered_database)
        print_credit_average(filtered_database)
    elif input_int == 3:
        filtered_database = filter_database(database, filter_builder(lambda c: int(c[0]) >= 2, "CRS"))
        tabulate_database(filtered_database)
        print_credit_average(filtered_database)
    elif input_int == 4:
        simulated_database = deepcopy(database)
        print("Please enter the grade and credit of the course to be added, separated by a comma.")
        print("To enter multiple, separate each pair using a semicolon.")
        print("For example, if you want to add one course with the grade 80 and 3 credits and another with the",
              "grade 78 and 6 credits, then you can enter '80,3;78,6' without the quotation marks.")

        def valid_input(inp):
            pairs = inp.split(';')
            for p in pairs:
                if ',' not in p:
                    return False
                pair = p.split(',')
                if len(pair) != 2:
                    return False
                for n in pair:
                    if not n.isdigit():
                        return False
            return True
        user_input = take_input_criteria_run(lambda inp: inp.replace(' ', ''), valid_input)
        to_add = [pair.split(',') for pair in user_input.split(';')]
        for i in range(len(to_add)):
            simulated_database["SBJ"].append("SIMU")
            simulated_database["CRS"].append(str(i))
            simulated_database["GRD"].append(to_add[i][0])
            simulated_database["CRD"].append(to_add[i][1])
            simulated_database["SEM"].append("NA")
            simulated_database["YER"].append("NA")
        print_credit_average(simulated_database)
    elif input_int == 5:
        break
    input("Press enter to return to the main menu...")
print("Program terminated.")
