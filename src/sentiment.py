from textblob import TextBlob
from .awards import get_awards_api
from .utils import normalize_text


def __good_vibes(data: dict, hosts: list) -> dict:
    host_scores = {}
    host_vibes = {}
   

    for tweet in data:
        normalized_text = normalize_text(tweet['text'])
        tweet_hosts = [host for host in normalized_text]
        if tweet_hosts:
            for sentence in TextBlob(normalized_text).sentences:
                for host in tweet_hosts:
                    host_scores[host] = host_scores[host] + sentence.sentiment.polarity
    for host, score in host_scores:
        host_vibes[host] = score > 0
    return host_vibes

def get_sentiment_api(data: dict, hosts: list) -> dict:
    """
    Keyword arguments:
    data -- dictionary of hosts
    """

    return __good_vibes(data, hosts)
