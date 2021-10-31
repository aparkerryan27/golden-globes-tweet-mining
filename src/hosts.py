from queue import PriorityQueue
from .utils import normalize_text

def __get_host(hosts: dict, normalized_text: str):
    words = normalized_text.split(' ')
    if 'should' in words: return
    if 'wish' in words: return
    if 'hope' in words: return
    if 'next' in words: return
    for i, word in enumerate(words):
        if word == 'host':
            for j in range(i):
                host = ' '.join(words[j:i])
                hosts[host] = hosts.get(host, 0) + 1
            for j in range(i+2, len(words)+1):
                host = ' '.join(words[i+1:j])
                hosts[host] = hosts.get(host, 0) + 1
        if word == 'hosting':
            for j in range(i):
                host = ' '.join(words[j:i])
                hosts[host] = hosts.get(host, 0) + 1
            for j in range(i+2, len(words)+1):
                host = ' '.join(words[i+1:j])
                hosts[host] = hosts.get(host, 0) + 1

def __get_potential_hosts(data: dict) -> dict:
    potential_hosts = {}

    for tweet in data:
        text = tweet['text']
        normalized_text = normalize_text(text)
        __get_host(potential_hosts, normalized_text)

    return potential_hosts

def __is_valid_host(host: str) -> bool:
    host_words = host.split(' ')
    if len(host_words) <= 1 or len(host_words) > 2: return False
    blacklist = ['a', 'am', 'an', 'as', 'any', 'be', 'can', 'in', 'it', 'of', 'on', 'or', 'my', 'no', 'not', 'rt', 'to', 'tv', 'he', 'she', 'him', 'his', 'her', 'and', 'are', 'the', 'this', 'that', 'there', 'their', 'they', 'show', 'for', 'from', 'your', 'yours', 'will', 'was', 'were', 'best', 'next', 'year', 'years', 'host', 'hosts', 'than', 'then', 'what', 'when', 'why', 'how', 'award', 'awards', 'ever', 'every', 'everything', 'today', 'tonight', 'motion', 'original', 'person', 'people', 'golden', 'globe', 'globes', 'goldenglobe', 'goldenglobes']
    return host_words[0] not in blacklist and host_words[-1] not in blacklist

def get_hosts_api(data: dict) -> list:
    """
    Keyword arguments:
    data -- dictionary of tweets
    """
    hosts = []

    potential_hosts = __get_potential_hosts(data=data)

    freqs = {}
    max_heap = PriorityQueue()
    for host, freq in potential_hosts.items():
        if freq not in freqs:
            freqs[freq] = []
            max_heap.put(-freq)
        freqs[freq].append(host)

    while not max_heap.empty() and len(hosts) < 2:
        top = -max_heap.get()
        for host in freqs[top]:
            if __is_valid_host(host):
                hosts.append(host)

    return hosts
