import json
from awards import get_awards


def main():
    file = open('data/gg2013.json')
    data = json.load(file)

    awards = get_awards(data=data)
    print(awards)

if __name__ == '__main__':
    main()
