import json
from queue import PriorityQueue
from utils import normalize_text


file = open('data/gg2013.json')
data = json.load(file)

def __get_award_name(award_names: dict, text: list):
    for i, word in enumerate(text):
        if word == 'wins':
            for j in range(i+2, len(text)+1):
                award_name = ' '.join(text[i+1:j])
                award_names[award_name] = award_names.get(award_name, 0) + 1
        elif word == 'won':
            for j in range(i+2, len(text)+1):
                award_name = ' '.join(text[i+1:j])
                award_names[award_name] = award_names.get(award_name, 0) + 1
        elif word == 'goes':
            if i == len(text)-1 or text[i+1] != 'to':
                continue
            for j in range(i):
                award_name = ' '.join(text[j:i])
                award_names[award_name] = award_names.get(award_name, 0) + 1

def __get_possible_award_names() -> dict:
    award_names = {}

    for tweet in data:
        text = tweet['text']
        normalized_text = normalize_text(text)
        __get_award_name(award_names, normalized_text)

    return award_names

def __is_valid_award_name(award_name: str) -> bool:
    award_name_words = award_name.split(' ')
    if len(award_name_words) <= 1: return False
    if award_name_words[0] != 'best': return False # award names should start with 'best'
    blacklist = ['a', 'am', 'an', 'in', 'it', 'or', 'rt', 'to', 'and', 'the', 'for', 'best', 'than', 'then', 'today', 'tonight', 'motion', 'original', 'golden', 'globe', 'globes', 'goldenglobe', 'goldenglobes']
    return award_name_words[-1] not in blacklist

def get_award_names(n: int=10) -> list:
    award_names = []

    possible_award_names = __get_possible_award_names()

    freqs = {}
    max_heap = PriorityQueue()
    for award_name, freq in possible_award_names.items():
        if freq not in freqs:
            freqs[freq] = []
            max_heap.put(-freq)
        freqs[freq].append(award_name)

    while not max_heap.empty() and len(award_names) < n:
        top = -max_heap.get()
        for award_name in freqs[top]:
            if __is_valid_award_name(award_name):
                award_names.append(award_name)

    return award_names

print(get_award_names(20))
