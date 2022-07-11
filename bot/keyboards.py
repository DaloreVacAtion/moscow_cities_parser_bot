from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.service import send_mess


def cities_keyboard(message, bot, cities):
    keyboard = InlineKeyboardMarkup()
    for i in range(0, len(cities), 2):
        if not len(cities) % 2:
            button_1 = InlineKeyboardButton(cities[i].city_name, callback_data='city-' + str(cities[i].id))
            button_2 = InlineKeyboardButton(cities[i + 1].city_name, callback_data='city-' + str(cities[i + 1].id))
            keyboard.row(button_1, button_2)
        else:
            try:
                button_1 = InlineKeyboardButton(cities[i].city_name, callback_data='city-' + str(cities[i].id))
                button_2 = InlineKeyboardButton(cities[i + 1].city_name, callback_data='city-' + str(cities[i + 1].id))
                keyboard.row(button_1, button_2)
            except:
                button = InlineKeyboardButton(cities[len(cities) - 1].city_name, callback_data='city-' + str(cities[len(cities) - 1].id))
                keyboard.row(button)
    send_mess(bot, message, 'О каком городе Вам рассказать?', keyboard)
