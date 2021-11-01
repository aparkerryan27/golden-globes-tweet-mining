from queue import PriorityQueue
from .utils import normalize_text
import textdistance


def __get_award(awards: dict, normalized_text: str):
    words = normalized_text.split(' ')
    for i, word in enumerate(words):
        if word == 'wins' or word == 'earns' or word == 'won' or word == 'recieves' or word == 'awarded' or word == 'named':
            for j in range(i+2, len(words)+1):
                award = ' '.join(words[i+1:j])
                awards[award] = awards.get(award, 0) + 1
        elif word == 'won':
            for j in range(i+2, len(words)+1):
                award = ' '.join(words[i+1:j])
                awards[award] = awards.get(award, 0) + 1
        elif word == 'goes':
            if i == len(words)-1 or words[i+1] != 'to':
                continue
            for j in range(i):
                award = ' '.join(words[j:i])
                awards[award] = awards.get(award, 0) + 1

def __get_possible_awards(data: dict) -> dict:
    awards = {}

    for tweet in data:
        __get_award(awards, normalize_text(tweet['text']))

    return awards

def __is_valid_award(award: str) -> bool:
    award_words = award.split(' ')
    if len(award_words) <= 3: return False
    if "award" not in award_words and award_words[0] != 'best': return False # awards should start with the word 'best' except for the awards
    blacklist = ['a', 'at', 'am', 'an', 'in', 'it', 'or', 'to', 'tv', 'and', 'are', 'the', 'for', 'best', 'next', 'year', 'years', 'host', 'hosts', 'than', 'then', 'today', 'tonight', 'motion', 'original', 'globe', 'globes', 'goldenglobe']
    ultimate_blacklist = ["for", "golden", "goldenglobes", "congrats", "congratulations", "cast", "crew", "rt"]
    for item in ultimate_blacklist:
        if item in award_words:
            return False
    return award_words[-1] not in blacklist

def get_awards_api(data: dict, n: int=30) -> list:
    """
    Keyword arguments:
    data -- dictionary of tweets
    n -- number of awards to return (default 30)
    """

    awards = []

    possible_awards = __get_possible_awards(data)

    freqs = {}
    max_heap = PriorityQueue()
    for award, freq in possible_awards.items():
        if freq not in freqs:
            freqs[freq] = []
            max_heap.put(-freq)
        freqs[freq].append(award)

    while not max_heap.empty() and len(awards) < n:
        top = -max_heap.get()
        for award in freqs[top]:
            if __is_valid_award(award):
                if len(awards) > 0:
                    for item in awards:
                        if item in award or award in item or textdistance.jaccard(award, item) > 0.87: #if award substring matches or words are just switched around
                            break
                    else:
                        awards.append(award)
                else:
                    awards.append(award)


    return awards
