import json
from awards import get_awards


def main():
    file = open('data/gg2013.json')
    data = json.load(file)
    awards = get_awards(data=data)
    print(f'2013 Awards: {awards}\n')

    file = open('data/gg2015.json')
    data = json.load(file)
    awards = get_awards(data=data)
    print(f'2015 Awards: {awards}\n')

if __name__ == '__main__':
    main()
