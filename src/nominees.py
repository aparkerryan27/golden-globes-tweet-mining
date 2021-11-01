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

        #TODO: way to select the right number of nominees for each category, maybe a ratio of highest frequencies or a spread size
        
        nominees = []
        lowest_freq = 0
        lowest_nominee = ''
        potential_nominees = [nom for nom in potential_nominees if __is_valid_nominee(nom)]
        for potential_nominee, freq in potential_nominees.items():
            if __is_valid_nominee(potential_nominees):
                if len(potential_nominees) < 5:
                    nominees.append(potential_nominee)
                    lowest_freq = freq
                    lowest_nominee = potential_nominee
                elif freq > lowest_freq:
                    lowest_freq = freq
                    nominees.replace()
                    lowest_nominee = potential_nominee
        nominees.sort
        all_nominees[award] = nominees
        

    return all_nominees
