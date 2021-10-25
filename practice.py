from os import name
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

import json

from collections import Counter

import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_sm')


'''
{
"text": "JLo's dress! #eredcarpet #GoldenGlobes", 
"user": {"screen_name": "Dozaaa_xo", "id": 557374298}, 
"id": 290620657987887104, "timestamp_ms": 1358124338000}
'''
file = open("gg2013.json")
data = json.load(file)
tweets_text = [item["text"] for item in data]
portion_tweets_text = tweets_text[:10000] #first 10,000 tweets // most common names [('Amy Poehler', 359), ('Anne Hathaway', 238), ('James Cameron', 164), ('Kate Hudson', 113), ('Adele', 109)]
large_portion_tweets_text = tweets_text[:100000] #first 100,000 tweets 
#host_tweets = [text for text in tweets_text if "host" in text.lower()]
all_names = []
#NLTK Method (struggles to get names correct, and only gets first names)
#processed_tweets = [pos_tag(word_tokenize(tweet)) for tweet in host_tweets]
#names = [data[0] for data in tweet in processed_tweets if data[1] == "NNP"]

total = len(large_portion_tweets_text)
counter = 0

for tweet in large_portion_tweets_text:
    
    #Spacey Method (trained on a larger entity recognizer )
    names = [str(ent) for ent in nlp(tweet).ents  if "Globes" not in ent.text] #if ent.label_ == "PERSON" prevents Tina Fey from being recognized (she is an ORG lol)
    print(counter/total)
    counter = counter + 1
    all_names = all_names + names

'''
name_counts = {'Sample Name': 1}
for name in all_names:
    for existing_name in name_counts:
        if name in existing_name:
            name_counts[existing_name] += 1 #add to the supername and ignore the subname
            print("added subname")
            break
        elif existing_name in name and name.count(" ") == 1 and name.count("@") == 0 and name.count("’") == 0: #make sure its a legal full name
            name_counts[name] = name_counts[existing_name] #set the supername to the sum of the subname
            name_counts[existing_name] = 0 # remove the subname from the running
            print("added supername")
            break
    else:
        if name in name_counts:
            name_counts[name] += 1
            print("added fullname") 
        elif name.count(" ") <= 1 and name.count("@") == 0 and name.count("’") == 0: #avoid declaring large bad names (checks ’ but not ')
            name_counts[name] = 0
            print("added newname")

sorted_counts = sorted(name_counts.items(), key=lambda x: x[1], reverse=True)
print(sorted_counts)
'''
counter_names = Counter(all_names)
print(counter_names.most_common(200))

