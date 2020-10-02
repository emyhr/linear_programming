from mrdoe import *
from pulp import *


def main():

    # problem
    problem = LpProblem("Visiting_places", LpMaximize)
    # variables
    v_places = LpVariable.dicts('v', PLACES, cat='Binary')
    # objective
    problem += lpSum(v_places.values())
    # constraints
    problem += lpDot(v_places.values(), DURATION) <= MAX_HOURS, "Time constraint"
    problem += lpDot(v_places.values(), PRICE) <= MAX_EUROS, "Money constraint"

    # List of recommended PLACES
    problem.solve()
    ListVisit1 = [var.name for var in problem.variables() if var.varValue]

    # preference 1
    problem = preference1(problem, v_places)
    problem.solve()
    pref_list1 = [var.name for var in problem.variables() if var.varValue]
    # preference 2
    problem = preference2(problem, v_places)
    problem.solve()
    pref_list2 = [var.name for var in problem.variables() if var.varValue]
    # preference 3
    problem = preference3(problem, v_places)
    problem.solve()
    pref_list3 = [var.name for var in problem.variables() if var.varValue]
    # preference 4
    problem = preference4(problem, v_places)
    problem.solve()
    pref_list4 = [var.name for var in problem.variables() if var.varValue]
    # preference 5
    problem = preference5(problem, v_places)
    problem.solve()
    pref_list5 = [var.name for var in problem.variables() if var.varValue]

    problem.writeLP("Paris_places.lp")
    print("Status:", LpStatus[problem.status])
    print("Recommended PLACES:\n", ListVisit1)
    print("Total PLACES visited = ", value(problem.objective))


if __name__ == '__main__':
    main()

