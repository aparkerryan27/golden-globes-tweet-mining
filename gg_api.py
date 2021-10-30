import json
from src.awards import get_awards_api
from src.winners import get_winners_api


def get_hosts(year) -> list:
    '''
    Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.
    '''
    with open(f'data/gg{year}.json', 'r') as f:
        data = json.load(f)
        hosts = []
    return hosts

def get_awards(year) -> list:
    '''
    Awards is a list of strings. Do NOT change the name
    of this function or what it returns.
    '''
    with open(f'data/gg{year}.json', 'r') as f:
        data = json.load(f)
        awards = get_awards_api(data=data)
    return awards

def get_nominees(year) -> dict:
    '''
    Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.
    '''
    with open(f'data/gg{year}.json', 'r') as f:
        data = json.load(f)
        nominees = {}
    return nominees

def get_winner(year) -> dict:
    '''
    Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.
    '''
    with open(f'data/gg{year}.json', 'r') as f:
        data = json.load(f)
        winners = get_winners_api(data=data)
    return winners

def get_presenters(year) -> dict:
    '''
    Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.
    '''
    with open(f'data/gg{year}.json', 'r') as f:
        data = json.load(f)
        presenters = {}
    return presenters

def pre_ceremony():
    '''
    This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.
    '''
    print("Pre-ceremony processing complete.")
    return

def main():
    '''
    This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.
    '''
    return

if __name__ == '__main__':
    main()
