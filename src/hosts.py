from queue import PriorityQueue
import time
from .utils import normalize_text

def __get_host(hosts: dict, normalized_text: str):
    words = normalized_text.split(' ')
    if 'should' in words: return #eliminate future or previous hosts
    if 'wish' in words: return
    if 'hope' in words: return
    if 'next' in words: return
    if 'pre' in words: return #eliminate pre-show host (attempts to remove Natalie Morales but doesn't work)
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
    #starttime = time.time()
    for tweet in data:
        __get_host(potential_hosts, normalize_text(tweet['text']))

        
    #print('That took {} seconds'.format(time.time() - starttime))
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

    while not max_heap.empty() and len(hosts) < 2: #TODO: will always get two hosts! don't know how to solve that for exception years
        top = -max_heap.get()
        for host in freqs[top]:
            if __is_valid_host(host):
                hosts.append(host)

    return hosts
