import json
from src.awards import get_awards_api
from src.hosts import get_hosts_api
from src.presenters import get_presenters_api
from src.winners import get_winners_api
from src.nominees import get_nominees_api


# IMPORTANT: DO NOT CHANGE ANY OF THE FUNCTION NAMES OR
# WHAT THEY RETURN. THESE ARE NEEDED FOR THE AUTOGRADER.

def get_hosts(year) -> list:
    """
    Hosts is a list of one or more strings.
    """
    with open(f'data/gg{year}.json', 'r') as f:
        data = json.load(f)
        hosts = get_hosts_api(data=data)
    return hosts

def get_awards(year) -> list:
    """
    Awards is a list of strings.
    """
    with open(f'data/gg{year}.json', 'r') as f:
        data = json.load(f)
        awards = get_awards_api(data=data)
    return awards

def get_nominees(year) -> dict:
    """
    Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings.
    """
    with open(f'data/gg{year}.json', 'r') as f:
        data = json.load(f)
        nominees = get_nominees_api(data=data)
    return nominees

def get_winner(year) -> dict:
    """
    Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    """
    with open(f'data/gg{year}.json', 'r') as f:
        data = json.load(f)
        winners = get_winners_api(data=data)
    return winners

def get_presenters(year) -> dict:
    """
    Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings.
    """
    with open(f'data/gg{year}.json', 'r') as f:
        data = json.load(f)
        presenters = get_presenters_api(data=data)
    return presenters

def pre_ceremony():
    """
    This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    """
    return

def main():
    """
    This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading.
    """
    print("Testing all functions")
    year = 2013
    #print(get_nominees(2013))

    return

if __name__ == '__main__':
    main()
