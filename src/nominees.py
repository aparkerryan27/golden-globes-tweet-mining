from queue import PriorityQueue
from .awards import get_awards_api
from .utils import normalize_text


def __get_nominee(nominees: dict, normalized_text: str):
    words = normalized_text.split(' ')
    if 'should' in words: return
    if 'wish' in words: return
    if 'hope' in words: return
    for i, word in enumerate(words):
        if word == 'nominee':
            for j in range(i):
                nominee = ' '.join(words[j:i])
                nominees[nominee] = nominees.get(nominee, 0) + 1
            for j in range(i+1, len(words)+1):
                nominee = ' '.join(words[i+2:j])
                nominees[nominee] = nominees.get(nominee, 0) + 1
        if word == 'nominees':
            for j in range(i):
                nominee = ' '.join(words[j:i])
                nominees[nominee] = nominees.get(nominee, 0) + 1
            for j in range(i+1, len(words)+1):
                nominee = ' '.join(words[i+2:j])
                nominees[nominee] = nominees.get(nominee, 0) + 1
        elif word == 'nominated':
            for j in range(i):
                nominee = ' '.join(words[j:i])
                nominees[nominee] = nominees.get(nominee, 0) + 1
            for j in range(i+1, len(words)+1):
                nominee = ' '.join(words[i+2:j])
                nominees[nominee] = nominees.get(nominee, 0) + 1

def __get_potential_nominees(data: dict, award: str) -> dict:
    potential_nominees = {}

    for tweet in data:
        text = tweet['text']
        normalized_text = normalize_text(text)
        if award in normalized_text:
            __get_nominee(potential_nominees, normalized_text)

    return potential_nominees

def __is_valid_nominee(nominee: str) -> bool:
    nominee_words = nominee.split(' ')
    if len(nominee_words) <= 1: return False
    blacklist = ['a', 'am', 'an', 'as', 'any', 'be', 'can', 'in', 'it', 'of', 'on', 'or', 'my', 'no', 'not', 'rt', 'to', 'tv', 'he', 'she', 'him', 'his', 'her', 'and', 'are', 'the', 'this', 'that', 'there', 'their', 'they', 'show', 'for', 'from', 'your', 'yours', 'will', 'was', 'were', 'best', 'next', 'year', 'years', 'host', 'hosts', 'than', 'then', 'what', 'when', 'why', 'how', 'award', 'awards', 'ever', 'every', 'everything', 'today', 'tonight', 'motion', 'original', 'person', 'people', 'golden', 'globe', 'globes', 'goldenglobe', 'goldenglobes']
    return nominee_words[0] not in blacklist and nominee_words[-1] not in blacklist

def get_nominees_api(data: dict, awards=None, n: int=30) -> dict:
    """
    Keyword arguments:
    data -- dictionary of tweets
    n -- number of nominees to return (default 30)
    """
    nominees = {}

    if awards is None: awards = get_awards_api(data=data, n=n)

    for award in awards:
        potential_nominees = __get_potential_nominees(data, award)

        nominees_lst = []
        max_heap = PriorityQueue()
        freqs = {}
        for potential_nominee, freq in potential_nominees.items():
            if freq not in freqs:
                freqs[freq] = []
                max_heap.put(-freq)
            freqs[freq].append(potential_nominee)

        while not max_heap.empty() and len(nominees_lst) < 5:
            top = -max_heap.get()
            for nominee in freqs[top]:
                if len(nominees_lst) < n and __is_valid_nominee(nominee):
                    nominees_lst.append(nominee)

        nominees[award] = nominees_lst

    return nominees
