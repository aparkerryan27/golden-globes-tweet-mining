from .awards import get_awards_api
from .utils import normalize_text


def __get_presenter(presenters: dict, normalized_text: str):
    words = normalized_text.split(' ')
    if 'should' in words: return
    if 'wish' in words: return
    if 'hope' in words: return
    for i, word in enumerate(words):
        if word == 'presents':
            for j in range(i):
                presenter = ' '.join(words[j:i])
                presenters[presenter] = presenters.get(presenter, 0) + 1
        if word == 'presenter':
            for j in range(i):
                presenter = ' '.join(words[j:i])
                presenters[presenter] = presenters.get(presenter, 0) + 1
            for j in range(i+1, len(words)+1):
                presenter = ' '.join(words[i+2:j])
                presenters[presenter] = presenters.get(presenter, 0) + 1
        if word == 'presenters':
            for j in range(i):
                presenter = ' '.join(words[j:i])
                presenters[presenter] = presenters.get(presenter, 0) + 1
            for j in range(i+1, len(words)+1):
                presenter = ' '.join(words[i+2:j])
                presenters[presenter] = presenters.get(presenter, 0) + 1
        elif word == 'presenting':
            for j in range(i):
                presenter = ' '.join(words[j:i])
                presenters[presenter] = presenters.get(presenter, 0) + 1
            for j in range(i+1, len(words)+1):
                presenter = ' '.join(words[i+2:j])
                presenters[presenter] = presenters.get(presenter, 0) + 1

def __get_potential_presenters(data: dict, award: str) -> dict:
    potential_presenters = {}

    for tweet in data:
        text = tweet['text']
        normalized_text = normalize_text(text)
        if award in normalized_text:
            __get_presenter(potential_presenters, normalized_text)

    return potential_presenters

def __is_valid_presenter(presenter: str) -> bool:
    presenter_words = presenter.split(' ')
    if len(presenter_words) <= 1: return False
    blacklist = ['a', 'am', 'an', 'as', 'any', 'be', 'can', 'in', 'it', 'of', 'on', 'or', 'my', 'no', 'not', 'rt', 'to', 'tv', 'he', 'she', 'him', 'his', 'her', 'and', 'are', 'the', 'this', 'that', 'there', 'their', 'they', 'show', 'for', 'from', 'your', 'yours', 'will', 'was', 'were', 'best', 'next', 'year', 'years', 'host', 'hosts', 'than', 'then', 'what', 'when', 'why', 'how', 'award', 'awards', 'ever', 'every', 'everything', 'today', 'tonight', 'motion', 'original', 'person', 'people', 'golden', 'globe', 'globes', 'goldenglobe', 'goldenglobes']
    return presenter_words[0] not in blacklist and presenter_words[-1] not in blacklist

def get_presenters_api(data: dict, n: int=30) -> dict:
    """
    Keyword arguments:
    data -- dictionary of tweets
    n -- number of presenters to return (default 30)
    """
    presenters = {}

    awards = get_awards_api(data=data, n=n)

    for award in awards:
        potential_presenters = __get_potential_presenters(data, award)

        max_freq = 0
        presenter = ''
        for potential_presenter, freq in potential_presenters.items():
            if freq > max_freq and __is_valid_presenter(potential_presenter):
                max_freq = freq
                presenter = potential_presenter

        presenters[award] = presenter

    return presenters
