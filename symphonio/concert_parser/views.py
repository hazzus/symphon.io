import requests
from bs4 import BeautifulSoup
import datetime


class Concert():
    def __init__(self, time, place, url, composer):
        self.time = time
        self.place = place
        self.url = url
        self.composer = composer


def f(r):
    for i in parse():
        print(i.time, i.composer, i.place, i.url, sep='\n')


def get_html():
    try:
        return requests.get('https://www.meloman.ru/calendar/')
    except:
        print("Error while getting data form the Internet")


def parse_concert(url):
    concertr = requests.get('https://www.meloman.ru' + url)
    return BeautifulSoup(concertr.text, features='html.parser').find_all('h5', {'class': 'caps'})


def parse():
    res = []
    month = BeautifulSoup(get_html().text, features='html.parser').findAll('div',
                                                                           {'class': 'calendar-day'})
    res = []
    for day in month:
        concerts = day.find_all('li', {'class': 'hall-entry'})
        dayo = int(day.find('p', {'class': 'day'}).text)
        date = day.find('p', {'class': 'month'}).text
        if date == 'Января':
            month = 1
        elif date == 'Февраля':
            month = 2
        elif date == 'Марта':
            month = 3
        elif date == 'Апреля':
            month = 4
        elif date == 'Мая':
            month = 5
        elif date == 'Июня':
            month = 6
        elif date == 'Июля':
            month = 7
        elif date == 'Августа':
            month = 8
        elif date == 'Сентября':
            month = 9
        elif date == 'Октября':
            month = 10
        elif date == 'Ноября':
            month = 11
        elif date == 'Декабря':
            month = 12
        for c in concerts:
            d = c.find('span', {'class': 'sans'}).text
            hour = int(d[:2])
            minute = int(d[-2:])
            place = c.find('div', {'class': 'hall-entry-head'}).text.strip()
            link = c.attrs['data-link']
            url = 'https://www.meloman.ru' + link
            for comp in parse_concert(link):
                if comp.parent.find('h6', {'class': 'gray'}) is not None:
                    composer = comp.find('a')
                    if composer is not None:
                        res.append(Concert(datetime.datetime(2018, month, dayo, hour, minute), place, url,
                                           "".join(composer.text.strip().split())))
                        return res
    return res
