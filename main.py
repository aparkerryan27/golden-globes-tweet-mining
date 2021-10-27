import json
from src.awards import get_awards
from src.winners import get_winners


def main():
    file = open('data/gg2013.json')
    data = json.load(file)
    awards = get_awards(data=data)
    winners = get_winners(data=data)
    print(f'2013 Awards: {awards}\n')
    print(f'2013 Winners: {winners}\n')

    file = open('data/gg2015.json')
    data = json.load(file)
    awards = get_awards(data=data)
    winners = get_winners(data=data)
    print(f'2015 Awards: {awards}\n')
    print(f'2015 Winners: {winners}\n')


if __name__ == '__main__':
    main()
