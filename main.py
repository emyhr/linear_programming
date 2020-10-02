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

    # preferences
    preferences = [1, 2, 3, 4]
    preferred_places = set_preferences(problem, preferences, v_places)

    problem.writeLP("Paris_places.lp")
    print("Status:", LpStatus[problem.status])
    print("Recommended PLACES:\n", ListVisit1)
    print("Total PLACES visited = ", value(problem.objective))
    print(equal_lists(ListVisit1, preferred_places))


if __name__ == '__main__':
    main()

