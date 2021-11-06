import re
import string
import unidecode


def normalize_text(text: str) -> str:
    # remove extra whitespace
    res = re.sub(' +', ' ', text)

    # make all ASCII
    res = unidecode.unidecode(res)

    # remove punctuation
    punctuation_table = res.maketrans('', '', string.punctuation)
    res = res.translate(punctuation_table)

    # make lowercase
    res = res.lower()

    return res

def find_names(text:str) -> str:
    names = []
    continuation = ''

    res = re.sub(' +', ' ', text)

    # make all ASCII
    res = unidecode.unidecode(res)

    # remove punctuation
    punctuation_table = res.maketrans('', '', string.punctuation)
    res = res.translate(punctuation_table)

    res = res.split(' ')

    for word in res:
        if len(word) > 1:
            if (word[0].upper() + word[1:].lower()) == word:
                continuation += ' ' + word
            else:
                names += [continuation]
                continuation = ''
        elif word.upper() == word:
            if word not in ['A','I']:
                continuation += ' ' + word
            else:
                names += [continuation]
                continuation = ''
        else:
            names += [continuation.lower()]
            continuation = ''

    return names
