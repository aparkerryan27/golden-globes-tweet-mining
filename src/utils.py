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
