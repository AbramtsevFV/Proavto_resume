import re
import time
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from celery.decorators import task
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher, CallbackContext, \
    CallbackQueryHandler
from proproauto.settings import TELEGRAM_TOKEN
from .models import Tg_response_msg
from .utils import get_data_from_api, get_data_from_api_no_HTML, get_text_messages, get_data_from_api_car_no_HTML, \
    save_mssages_users, check_admin, get_user_list


def get_user_data(update):
    """
    Функция получения данных пользователя.
    """
    users ={}
    user_id = update.effective_user.id
    user_name = update.effective_user.name
    if update.callback_query:
        room_id = update.callback_query.message.chat_id
        command = update.callback_query.data
    elif update.message:
        room_id = update.message.chat.id
        command = update.message.text
    users['room_id'] = room_id
    users['command'] = command
    save_mssages_users(user_id, user_name, command)
    return users


def default_keyboard(room_id, command='default_keyboard'):
    """
    Функция отправки навигационного меню.
    """
    default_keyboard = [[InlineKeyboardButton('proproauto.ru', url="http://proproauto.ru/")],
                        [InlineKeyboardButton('Список брендов', callback_data='/brend_list')],
                        [InlineKeyboardButton('Страны', callback_data='/country_list')],
                        [InlineKeyboardButton('Помощь', callback_data='/help'),
                         InlineKeyboardButton('Пуск', callback_data='/start')],
                        ]
    texts = get_text_messages(command)
    reply_markup = InlineKeyboardMarkup(default_keyboard)
    bot.send_message(chat_id=room_id, text=texts, parse_mode='HTML', reply_markup=reply_markup)


def send_msg(room_id, text, reply_markup=None):
    """
    Функция отправки сообщений пользователю.
    """
    bot.send_message(chat_id=room_id, text=text, parse_mode='Markdown', reply_markup=reply_markup)

def send_img(room_id, url):
    bot.send_photo(chat_id=room_id, photo=url)


def start_help(update, context: CallbackContext):
    """
    Отправляет информационное сообщение в зависимости от команды.
    """
    users = get_user_data(update)
    default_keyboard(users['room_id'], users['command'])


def get_keyboard_msg(update, context: CallbackContext):
    """
    Функция отправляет сообщение с клавиатурой выбора
    стран брендов(полученных по API сайта) в зависимости, что на входе.
    """
    users = get_user_data(update)
    value_list = get_data_from_api(users["command"])
    keyboard = []
    for value in value_list:
        keyboard.append([InlineKeyboardButton(f'{value["title"]}', callback_data=f'{users["command"]}/?search={value["slug"]}')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    text = get_text_messages(users["command"])
    send_msg(users['room_id'], text, reply_markup)
    default_keyboard(users['room_id'])

def brend(update, context: CallbackContext):
    users = get_user_data(update)
    photo, brend_list = get_data_from_api_no_HTML(users["command"])
    send_img(users['room_id'], photo)
    for text in brend_list:
         send_msg(users['room_id'], text)
    default_keyboard(users['room_id'])

def get_car(update, context: CallbackContext):
    """
    Функция принимает на входе сообщения пользователя,
    отправляет запрос к API сайта.
    Получает список словарей, список строк, None.
    Список словарей, отправляет клавиатуру с моделями авто которые соответствуют поиск.
    Список строк, отправляет данные по модели авто.
    Пустой список возвращает сообщение об ошибке и навигационную клавиатуру.
    """
    users = get_user_data(update)
    if update.message:
        command = f"/model_auto/?search={users['command']}"
    else:
        command = users['command']
    photo, m_a = get_data_from_api_car_no_HTML(command)

    if m_a:
        if isinstance(m_a[0], dict):
            keyboard = []
            for value in m_a:
                keyboard.append(
                    [InlineKeyboardButton(f'{value["title"]}', callback_data=f'/model_auto/?search={value["slug"]}')])
            reply_markup = InlineKeyboardMarkup(keyboard)
            text = get_text_messages('/car_list')
            send_msg(users['room_id'], text, reply_markup)
        else:

            send_img(users['room_id'], photo)
            for text in m_a:
                send_msg(users['room_id'], text)
    else:
        text = get_text_messages('/error')
        send_msg(users['room_id'], text)
    default_keyboard(users['room_id'])

def admin_info(update, context: CallbackContext):
    users = get_user_data(update)

    if check_admin(users['room_id']):
        user_lst = get_user_list()
        text = get_text_messages('send_info_msg')
        for u in user_lst:
            send_msg(u, text)
        send_msg(users['room_id'], 'Сообщение отправлено')

    else:
        text = get_text_messages('/error_admin')
        send_msg(users['room_id'], text)

def setup_dispatcher(dp):
    """
    Добавление обработчиков событий из Telegram
    """
    dp.add_handler(CommandHandler("start", start_help))
    dp.add_handler(CommandHandler("help", start_help))
    dp.add_handler(CommandHandler("admin_send_info", admin_info))
    dp.add_handler(CommandHandler("brend_list", get_keyboard_msg))
    dp.add_handler(CallbackQueryHandler(get_keyboard_msg, pattern='^/brend_list$'))
    dp.add_handler(CallbackQueryHandler(get_keyboard_msg, pattern='^/country_list$'))
    dp.add_handler(CallbackQueryHandler(start_help, pattern='^/start$'))
    dp.add_handler(CallbackQueryHandler(start_help, pattern='^/help$'))
    dp.add_handler(CallbackQueryHandler(brend, pattern='^/brend_list\S+\w+$'))
    dp.add_handler(CallbackQueryHandler(brend, pattern='^/country_list\S+\w+$'))
    dp.add_handler(CallbackQueryHandler(get_car, pattern='^\Smodel_auto\S\Ssearch=.+$'))
    dp.add_handler(MessageHandler(Filters.text, get_car))
    return dp



@task(ignore_result=True)
def process_telegram_event(update_json):
    update = telegram.Update.de_json(update_json, bot)
    dispatcher.process_update(update)


# Глобальная переменная -  для инициализации Telegram tg_bot
bot = telegram.Bot(token=TELEGRAM_TOKEN)
dispatcher = setup_dispatcher(Dispatcher(bot, None, workers=0, use_context=True))
TELEGRAM_BOT_USERNAME = bot.get_me()["username"]
