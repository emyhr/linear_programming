import numpy as np
import pandas as pd

# input data
PLACES = np.array(['TE', 'ML', 'AT', 'MO', 'JT', 'CA', 'CP',
                   'CN', 'BS', 'SC', 'PC', 'TM', 'AC'])
DURATION = np.array([9 / 2, 3, 1, 2, 3 / 2, 2, 5 / 2, 2, 2, 3 / 2, 3 / 4, 2, 3 / 2])
APPRECIATION = np.array([5, 4, 3, 2, 3, 4, 1, 5, 4, 1, 3, 2, 5])
PRICE = np.array([15.50, 12, 9.50, 11, 0, 10, 10, 5, 8, 8.50, 0, 15, 0])
MAX_HOURS = 12
MAX_EUROS = 65


def distances():
    """Returns matrix of distances between places"""
    dist = pd.read_csv('walking.csv', header=None, index_col=False)
    dist = dist.to_numpy()

    return dist


def preference1(problem, variables):
    """Adds constraints specified in Preference 1"""
    dist = distances()  # matrix of distances
    # indices of nearby places (distance <= 1 km)
    idx_from, idx_to = np.where((dist <= 1) & (dist > 0))
    # names of nearby places
    from_to = zip(PLACES[idx_from], PLACES[idx_to])
    # if 2 places are close then visit both or none
    for from_p, to_p in from_to:
        problem += variables[from_p] == variables[to_p]

    return problem


def preference2(problem, variables):
    """Adds constraints specified in Preference 2"""
    problem += variables['TE'] == 1  # must visit TE
    problem += variables['CA'] == 1  # must visit CA

    return problem


def preference3(problem, variables):
    """Adds constraints specified in Preference 3"""
    # if visited CN then must not visit SC
    problem += variables['CN'] + variables['SC'] <= 1

    return problem


def preference4(problem, variables):
    """Adds constraints specified in Preference 4"""
    # must visit TM
    problem += variables['TM'] == 1

    return problem


def preference5(problem, variables):
    """Adds constraints specified in Preference 5"""
    # if visited ML then must visit CP
    problem += variables['CP'] - variables['ML'] >= 0

    return problem


def equal_lists(list1, list2):
    """Returns True if list1 and list2 have the same elements"""
    if set(list1) == set(list2):
        return True
    else:
        return False


def set_preferences(problem, preferences, variables, return_problem=False):
    """
    Sets given preferences and returns the list
    of places satisfying the preferences.
    if return_problem == True: returns problem as well
    """
    if 1 in preferences:
        problem = preference1(problem, variables)
    if 2 in preferences:
        problem = preference2(problem, variables)
    if 3 in preferences:
        problem = preference3(problem, variables)
    if 4 in preferences:
        problem = preference4(problem, variables)
    if 5 in preferences:
        problem = preference5(problem, variables)
    problem.solve()
    # list of preferred places
    pref_places = [var.name for var in problem.variables() if var.varValue]

    if return_problem:
        return pref_places, problem
    else:
        return pref_places


if __name__ == '__main__':
    pass
