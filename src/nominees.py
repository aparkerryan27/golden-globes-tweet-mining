from .awards import get_awards_api
from .utils import normalize_text


def __get_nominee(nominees: dict, normalized_text: str):
    words = normalized_text.split(' ')
    for i, word in enumerate(words):
        if word == 'nominee': #does this work backwards and forwards?
            for j in range(i):
                nominee = ' '.join(words[j:i])
                nominees[nominee] = nominees.get(nominee, 0) + 1
        elif word == 'nominated':
            for j in range(i):
                nominee = ' '.join(words[j:i])
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
    blacklist = ['golden', 'globe', 'globes', 'goldenglobe', 'goldenglobes']
    return nominee_words[-1] not in blacklist

def get_nominees_api(data: dict, n: int=30) -> dict:
    """
    Keyword arguments:
    data -- dictionary of tweets
    n -- number of awards to return (default 30)
    """
    all_nominees = {}

    awards = get_awards_api(data=data, n=n)

    for award in awards:
        potential_nominees = __get_potential_nominees(data, award)

        valid_noms = {}
        for nom, freq in potential_nominees.items():
            if __is_valid_nominee(nom):
                valid_noms[nom] = freq
        valid_noms = sorted(valid_noms.items(), key=lambda x: x[1], reverse=False)
        
        all_nominees[award] = valid_noms[:5]
        

    return all_nominees
