from .awards import get_awards_api
from .utils import normalize_text
from .utils import find_names

def __get_time(data: dict, award: str) -> int:
    timestamps = []
    for tweet in data:
        normalized_text = normalize_text(tweet['text'])
        award_normalized = normalize_text(award)
        award_words = award_normalized.split(" ")

        if all([word in normalized_text for word in award_words]):
            timestamps += [tweet['timestamp_ms']]

    if len(timestamps) == 0:
        print('NO         '+award)
        return -1
    else:
        print('yes ' + award)
        print(sum(timestamps)/len(timestamps))
        return sum(timestamps)/len(timestamps)

def __get_potential_presenters(data: dict, award: str,avgtime) -> dict:
    potential_presenters = {}
    minus_time = 2*1000*60
    plus_time = 0*1000*60

    for tweet in data:
        if (tweet['timestamp_ms'] < avgtime - minus_time) | (tweet['timestamp_ms'] > avgtime + plus_time): continue

        names = find_names(tweet['text'])
        for name in names:
            potential_presenters[name] = potential_presenters.get(name, 0) + 1

    return potential_presenters

def __is_valid_presenter(presenter: str) -> bool:
    presenter_words = presenter.split(' ')
    if len(presenter_words) <= 1: return False
    blacklist = ['a', 'am', 'an', 'as', 'any', 'be', 'can', 'in', 'it', 'of', 'on', 'or', 'my', 'no', 'not', 'rt', 'to', 'tv', 'he', 'she', 'him', 'his', 'her', 'and', 'are', 'the', 'this', 'that', 'there', 'their', 'they', 'show', 'for', 'from', 'your', 'yours', 'will', 'was', 'were', 'best', 'next', 'year', 'years', 'host', 'hosts', 'than', 'then', 'what', 'when', 'why', 'how', 'award', 'awards', 'ever', 'every', 'everything', 'today', 'tonight', 'motion', 'original', 'person', 'people', 'golden', 'globe', 'globes', 'goldenglobe', 'goldenglobes']
    return presenter_words[0] not in blacklist and presenter_words[-1] not in blacklist

def get_presenters_api(data: dict, awards=None, n: int=30) -> dict:
    """
    Keyword arguments:
    data -- dictionary of tweets
    n -- number of presenters to return (default 30)
    """
    presenters = {}

    if awards is None: awards = get_awards_api(data=data, n=n)

    #organize awards by length so that the substring awards dont catch names first
    awards.sort(key=len)
    awards.reverse()

    for award in awards:
        avgtime = __get_time(data,award)
        if avgtime == -1:
            presenters[award] = ''
            continue
        potential_presenters = __get_potential_presenters(data, award,avgtime)

        max_freq = 0
        presenter = ''
        for potential_presenter, freq in potential_presenters.items(): #this only allows for one presenter, probably the best way to do this
            if freq > max_freq and __is_valid_presenter(potential_presenter):
                max_freq = freq
                presenter = potential_presenter

        presenters[award] = presenter

    return presenters
