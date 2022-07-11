import logging

from django.conf import settings
from django.views import View
from django.http import JsonResponse

from telebot import TeleBot
from telebot.types import Update
from time import sleep
import requests

from bot.keyboards import cities_keyboard
from bot.service import parse_wiki, send_mess
from cities.models import City

logger = logging.getLogger('telebot')

bot_url = 'https://6a7f-80-234-59-108.ngrok.io' if settings.DEBUG else ''
bot_token = '5361810013:AAEbLU0FMOrY5ZcMDJAkB5DMKw_Eu7HZZoc'  # токен бота
bot_webhook_url = f'{bot_url}/telebot/'  # url сайта для вебхуков
api_url = 'https://api.telegram.org/bot{}/sendMessage'.format(bot_token)
headers = {
    'Content-Type': 'application/json'
}

bot = TeleBot(bot_token)
sleep(2)
r = requests.post('https://api.telegram.org/bot{}/deleteWebhook'.format(bot_token))
r = requests.post('https://api.telegram.org/bot{}/setWebhook?url={}'.format(bot_token, bot_webhook_url))

parse_url = 'https://ru.wikipedia.org/wiki/Городские_населённые_пункты_Московской_области'


class WebhookBotView(View):

    def get(self, request):
        return JsonResponse({'status': 200})

    def post(self, request):
        bot.process_new_updates([Update.de_json(request.body.decode('utf-8'))])
        return JsonResponse({'status': 200})


@bot.message_handler(commands=['start', 'parse'])
def start(message):
    send_mess(bot, message, 'Загружаю/Обновляю информацию с сайта Wikipedia...\n Пожалуйста, подождите.')
    parse_wiki(parse_url)
    send_mess(bot, message, 'Для того, чтобы воспользоваться моими возможностями, введите в чат часть или '
                            'полное название одного из городов/ПГТ Московской области.')


@bot.message_handler(content_types=['text'])
def find_cities(message):
    send_mess(bot, message, f'Вы ввели "{message.text}"')
    cities = City.objects.filter(city_name__icontains=message.text)
    if cities:
        cities_keyboard(message, bot, cities)
    else:
        send_mess(bot, message, 'К сожалению, мы не нашли ни одного города по Вашему запросу.')


@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data
    if data.startswith('city-'):
        get_city_callback(query)


def get_city_callback(query):
    bot.answer_callback_query(query.id)
    send_city_result(query.message, query.data[5:])


def send_city_result(message, city_id):
    try:
        city = City.objects.get(id=int(city_id))
    except City.DoesNotExist:
        logger.debug('city does not found')
        send_mess(bot, message, 'Извините, по техническим причинам мы не можем предоставить информацию о выбранном '
                                'Вами городе. Пожалуйста, попробуйте позднее.')
        return
    text = 'Численность в городе %s составляет %s человек. \n Ссылка: %s' % (city.city_name,
                                                                             city.population,
                                                                             city.city_url)
    logger.debug('info about city %s' % (city.city_name, ))
    send_mess(bot, message, text)
