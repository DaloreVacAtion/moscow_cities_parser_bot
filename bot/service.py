import logging
import unicodedata

import pandas as pd
import requests
from bs4 import BeautifulSoup as BS
from django.http import HttpResponse

from cities.models import City

logger = logging.getLogger('telebot')


def send_mess(bot, message, text: str, keyboard=None):
    if keyboard:
        bot.send_message(message.chat.id, text, reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, text)
    return HttpResponse(200)


def update_database(df, city_type: str, pgt=0):
    for i, row in df.iterrows():
        try:
            city, _ = City.objects.update_or_create(
                city_name=row[city_type],
                defaults={'population': unicodedata.normalize("NFKD", row['население,чел.'][1:]).replace(' ', ''),
                          'type': pgt}
            )
        except Exception as e:
            logger.debug('find some exception: %s', e)


def parse_wiki(url):
    response = requests.get(url)
    lxml_r = BS(response.text, 'lxml')
    tables = lxml_r.find_all('table', class_='standard sortable')

    cities_headers = []
    for i in tables[0].find_all('th'):
        title = i.text
        cities_headers.append(title)
    logger.debug(cities_headers)

    cities = pd.DataFrame(columns=cities_headers)
    logger.debug(cities)

    for city in tables[0].find_all('tr')[1:]:
        city_row = city.find_all('td')
        row = [j.text.partition('[4]')[0] for j in city_row]
        length = len(cities)
        cities.loc[length] = row
    logger.debug(cities)

    cities = cities.drop('герб', axis=1)
    logger.debug(cities)

    pgt_headers = []
    for i in tables[1].find_all('th'):
        title = i.text
        pgt_headers.append(title)
    logger.debug(pgt_headers)

    pgts = pd.DataFrame(columns=pgt_headers)
    logger.debug(pgts)

    for pgt in tables[1].find_all('tr')[1:]:
        pgt_row = pgt.find_all('td')
        row = [j.text.partition('[4]')[0] for j in pgt_row]
        length = len(pgts)
        pgts.loc[length] = row
    logger.debug('PGT  = %s', pgts)

    update_database(cities, 'город')
    update_database(pgts, 'пгт', 1)
