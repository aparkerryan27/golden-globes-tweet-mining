import json
import time
from src.awards import get_awards_api
from src.hosts import get_hosts_api
from src.presenters import get_presenters_api
from src.winners import get_winners_api
from src.nominees import get_nominees_api
#from src.sentiment import get_sentiment_api


# IMPORTANT: DO NOT CHANGE ANY OF THE FUNCTION NAMES OR
# WHAT THEY RETURN. THESE ARE NEEDED FOR THE AUTOGRADER.

def get_hosts(year) -> list:
    #takes about 1 minute for 2013, 5 minutes for 2015 (slow, but this works.)
    """
    Hosts is a list of one or more strings.
    """
    print("started open")
    with open(f'data/gg{year}.json', 'r') as f:
        data = json.load(f)
        print("finished open")
        hosts = get_hosts_api(data=data)
        print(hosts)


    return hosts

def get_awards(year) -> list:
    #Takes about 30 seconds for 2013, 2 minutes for 2015 (this gets ~20% completeness ~80% spelling, not sure if that's sufficient)
    """
    Awards is a list of strings.
    """
    with open(f'data/gg{year}.json', 'r') as f:
        data = json.load(f)
        awards = get_awards_api(data=data)
        print(awards)
    return awards

def get_nominees(year) -> dict:
    """
    Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings.
    """
    with open('gg%sanswers.json' % year, 'r') as f:
        answers = json.load(f)

    answers['awards'] = list(answers['award_data'].keys())

    with open(f'data/gg{year}.json', 'r') as f:
        data = json.load(f)
        nominees = get_nominees_api(data=data,awards=answers['awards'])
    return nominees

def get_winner(year) -> dict:
    #gets about a 20% and takes some time, but this technically works well enough and gets most correct it looks like
    """
    Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    """
    with open('gg%sanswers.json' % year, 'r') as f:
        answers = json.load(f)

    answers['awards'] = list(answers['award_data'].keys())

    with open(f'data/gg{year}.json', 'r') as f:
        data = json.load(f)
        winners = get_winners_api(data=data,awards=answers['awards'])
        print(winners)
    return winners

def get_presenters(year) -> dict:
    """
    Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings.
    """
    with open('gg%sanswers.json' % year, 'r') as f:
        answers = json.load(f)

    answers['awards'] = list(answers['award_data'].keys())
    count = 0

    with open(f'data/gg{year}.json', 'r') as f:
        data = json.load(f)
        presenters = get_presenters_api(data=data,awards=answers['awards'])
        print(presenters)
        for award in answers['awards']:
            if presenters[award] == answers['award_data'][award]: count += 1
        print('SCORE')
        print(count/len(answers['awards']))
    return presenters


def get_host_sentiment(year) -> list:
    """
    Gets the overall feelings on the golden globes and its participants
    """
    with open(f'data/gg{year}.json', 'r') as f:
        data = json.load(f)
        vibes = get_sentiment_api(data, get_hosts_api(data))

    sentiment =  "good vibes" if vibes else "bad vibes"
    print(sentiment)
    return sentiment

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
    #print("Testing all functions")
    #year = '2013'
    #with open('gg%sanswers.json' % year, 'r') as f:
    #    answers = json.load(f)

    #answers['awards'] = list(answers['award_data'].keys())
    #print(answers['awards'])

    starttime = time.time()
    presenters = get_presenters(2013)
    print('That took {} seconds'.format(time.time() - starttime))


    return

if __name__ == '__main__':
    main()
