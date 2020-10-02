from mrdoe import *
from pulp import *
from scipy.stats import kendalltau, spearmanr


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

    # List of recommended places
    problem.solve()
    ListVisit1 = [var.name for var in problem.variables() if var.varValue]

    # preferences
    preferences = [1, 2, 3, 4, 5]
    preferred_places = set_preferences(problem, preferences, v_places)

    # correlations of rankings
    ken_dur_app, _ = kendalltau(DURATION, APPRECIATION)
    spearman_dur_app, _ = spearmanr(DURATION, APPRECIATION)
    ken_dur_price, _ = kendalltau(DURATION, PRICE)
    spearman_dur_price, _ = spearmanr(DURATION, PRICE)
    ken_price_app, _ = kendalltau(PRICE, APPRECIATION)
    spearman_price_app, _ = spearmanr(PRICE, APPRECIATION)

    problem.writeLP("Paris_places.lp")
    print("Status:", LpStatus[problem.status])
    print("Recommended places:\n", ListVisit1)
    print("Total places visited = ", value(problem.objective))
    print(equal_lists(preferred_places, ListVisit1))
    print(preferred_places)

    print("Kendall correlation between duration and appreciation: ", ken_dur_app)
    print("Spearman correlation between duration and appreciation: ", spearman_dur_app)
    print("Kendall correlation between duration and price: ", ken_dur_price)
    print("Spearman correlation between duration and price: ", spearman_dur_price)
    print("Kendall correlation between price and appreciation: ", ken_price_app)
    print("Spearman correlation between price and appreciation: ", spearman_price_app)


if __name__ == '__main__':
    main()

