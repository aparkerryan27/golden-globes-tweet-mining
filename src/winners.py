from .awards import get_awards
from .utils import normalize_text


def __get_winner(winners: dict, normalized_text: str):
    words = normalized_text.split(' ')
    for i, word in enumerate(words):
        if word == 'wins':
            for j in range(i):
                winner = ' '.join(words[j:i])
                winners[winner] = winners.get(winner, 0) + 1
        elif word == 'won':
            for j in range(i):
                winner = ' '.join(words[j:i])
                winners[winner] = winners.get(winner, 0) + 1
        elif word == 'goes':
            if i == len(words)-1 or words[i+1] != 'to':
                continue
            for j in range(i+3, len(words)+1):
                winner = ' '.join(words[i+2:j])
                winners[winner] = winners.get(winner, 0) + 1

def __get_potential_winners(data: dict, award: str) -> dict:
    potential_winners = {}

    for tweet in data:
        text = tweet['text']
        normalized_text = normalize_text(text)
        if award in normalized_text:
            __get_winner(potential_winners, normalized_text)

    return potential_winners

def __is_valid_winner(winner: str) -> bool:
    winner_words = winner.split(' ')
    if len(winner_words) <= 1: return False
    blacklist = ['golden', 'globe', 'globes', 'goldenglobe', 'goldenglobes']
    return winner_words[-1] not in blacklist

def get_winners(data: dict, n: int=10) -> dict:
    """
        data: dictionary of tweets
        n: number of awards to return
    """
    winners = {}

    awards = get_awards(data=data, n=n)

    for award in awards:
        potential_winners = __get_potential_winners(data, award)

        max_freq = 0
        winner = ''
        for potential_winner, freq in potential_winners.items():
            if freq > max_freq and __is_valid_winner(potential_winner):
                max_freq = freq
                winner = potential_winner

        winners[award] = winner

    return winners
