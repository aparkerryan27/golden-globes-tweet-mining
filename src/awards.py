from queue import PriorityQueue
from .utils import normalize_text


def __get_award(awards: dict, normalized_text: str):
    words = normalized_text.split(' ')
    for i, word in enumerate(words):
        if word == 'wins':
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
        text = tweet['text']
        normalized_text = normalize_text(text)
        __get_award(awards, normalized_text)

    return awards

def __is_valid_award(award: str) -> bool:
    award_words = award.split(' ')
    if len(award) <= 1: return False
    if award_words[0] != 'best': return False # awards should start with the word 'best'
    blacklist = ['a', 'am', 'an', 'in', 'it', 'or', 'rt', 'to', 'tv', 'and', 'the', 'for', 'best', 'than', 'then', 'today', 'tonight', 'motion', 'original', 'golden', 'globe', 'globes', 'goldenglobe', 'goldenglobes']
    return award_words[-1] not in blacklist

def get_awards(data: dict, n: int=10) -> list:
    """
        data: dictionary of tweets
        n: number of awards to return
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
                awards.append(award)

    return awards
