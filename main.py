# This file is a statistics project for Stanford CS 109, Spring 2023
# The dataset used, bundesliga_player.csv, is free to use on Kaggle, accessible
# at https://www.kaggle.com/datasets/oles04/bundesliga-soccer-player

# This program allows the user to experiment and visualize statistics in the dataset through
# rejection sampling. it takes in a set of “given” conditions and a set of “outcome” conditions
# from the user and outputs the experimental probability of the “outcome” conditions being met
# given the “given” conditions. It also allows the user to get the mean, median, or variance of
# the filtered database after the “given” conditions are applied. The program is specifically
# written for the Bundesliga player database but with a bit more time and effort it could be
# generalized for any database, allowing the user to more easily obtain statistics of interest
# from a large database. This makes for a useful tool in parsing through data and comparing certain
# measurements or expected values in specified conditions.

# these dicts are used to read user input as operators and functions
import operator
import numpy
ops = {"==": operator.eq,
       "<": operator.lt,
       "<=": operator.le,
       ">": operator.gt,
       ">=": operator.ge
       }
stats = {"mean": numpy.mean,
         "median": numpy.median,
         "variance": numpy.var
         }

# Structure of dataset of interest
structure = ["AGE", "HEIGHT", "NATION", "CUR_PRICE", "MAX_PRICE", "POS", "P_NO.", "FOOT", "CLUB", "SPONSOR"]

# Indexes of categories that are strings, useful for type conversion
strs = [2, 5, 7, 8, 9]

# Global variable used for testing
player_list = []


# parse_file reads bundesliga_player.csv and sorts the data into a list of lists, with the structure
# presented above
def parse_file():
    # Read file, print categories of interest
    f = open("bundesliga_player.csv")
    lines = f.readlines()
    player_dataset = []
    for i in range(1, len(lines)):
        line = lines[i]
        data = line.strip().split(',')
        player_list.append(data[1])
        player_data = [data[3], data[4], data[5].lower(), data[7], data[8], data[9].lower(),
                       data[10], data[11], data[12].lower(), data[16].lower()]
        player_dataset.append(player_data)
    return player_dataset


# filters dataset with all restrictions in givens and returns filtered sample
def filter_data(dataset, givens):
    passed = []
    for sample in dataset:
        if check_consistent(sample, givens):
            passed.append(sample)
    return passed


# checks whether a single sample complies with conditions in givens
def check_consistent(sample, givens):
    for condition in givens:
        for i in range(len(condition)):
            if sample[i] == "":
                return False
            if condition[i] is not None:
                comp = condition[i][0]
                val = condition[i][1]
                sample_val = sample[i]
                if i not in strs:
                    val = float(val)
                    sample_val = float(sample_val)
                    if not ops[comp](sample_val, val):
                        return False
                elif val not in sample_val:
                    return False
    return True


# Gets a list of conditions or restrictions from user and standardizes them for use
def get_restrictions():
    restriction = " "
    givens = []
    while restriction != "":
        restriction = input()
        cat_val = restriction.split(" ")
        if restriction == "":
            break
        idx = structure.index(cat_val[0])
        if cat_val[1] in ["mean", "median", "variance"]:
            return idx, cat_val[1]
        given = [None] * len(structure)
        given[idx] = cat_val[1], cat_val[2]
        givens.append(given)
    return givens


# Prints the percentage of players that satisfy a set of conditions given a set of restrictions
def satisfies_condition(dataset):
    print("Categories: \n"
          "AGE: (number)\n"
          "HEIGHT: in meters (number)\n"
          "NATION: lowercase, ex. germany, denmark\n"
          "CUR_PRICE: current price in millions of dollars (number)\n"
          "MAX_PRICE: maximum price in millions of dollars (number\n"
          "POS: Position, lowercase {goalkeeper, defender, midfield, attack}\n"
          "P_NO: Player number\n"
          "FOOT: Leading foot {left, right}\n"
          "CLUB: lowercase, ex. bayern munich, dortmund\n"
          "SPONSOR: lowercase, ex. adidas, nike\n"
          "\n"
          "Enter given attributes with format {CATEGORY} {COMPARISON FUNCTION} {VALUE}. \n"
          "EXAMPLES: FOOT == left, AGE < 32, MAX_PRICE >= 2 \n"
          "One per line. End by entering a blank line.")
    givens = get_restrictions()
    filtered = filter_data(dataset, givens)
    print("...\n...\nIn the same format as before, list the conditions you want to be satisfied\n"
          "or enter {CATEGORY} {mean, median, or variance} to see that.")
    conditions = get_restrictions()
    if len(conditions) == 2:
        return do_stats(conditions, filtered)
    filtered_again = filter_data(filtered, conditions)
    print(len(filtered_again) / len(filtered))
    print("\n\n\n")


# do_stats prints the requested statistic from the specified category
def do_stats(conditions, dataset):
    idx = conditions[0]
    stat = stats[conditions[1]]
    category = []
    for player in dataset:
        if player[idx] != "":
            category.append(float(player[idx]))
    print(stat(category))
    print("\n\n\n")


def main():
    # Parse file into categories
    dataset = parse_file()
    while True:
        satisfies_condition(dataset)


if __name__ == "__main__":
    main()
