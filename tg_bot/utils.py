# pip install beautifulsoup4
# pip install lxml
import textwrap

import requests
from bs4 import BeautifulSoup

from proproauto.settings import API_URL
from tg_bot.models import Tg_response_msg, Profile, Message


def get_data_from_api(command):
    """ запрос к серверу API."""
    url = API_URL + command
    session = requests.Session()
    r = session.get(url).json()
    if r:
        return r
    return None

def get_data_from_api_no_HTML(command):
    """
    Функция возвращает список строк, без HTML тегов т.к.
    в БД храниться данные с форматирование HTML.
    """
    info = get_data_from_api(command)

    photo = info[0]['previewImg']
    text = info[0]['content']
    soup = BeautifulSoup(text, 'lxml')
    text = soup.get_text()
    text_list = textwrap.wrap(text, 1500)
    return photo, text_list

def get_data_from_api_car_no_HTML(command):
    """
    Функция возвращает либо список словарей для формирования кнопок,
    при условии, что найдено несколько моделей авто подходящих под
    критерий поиска.
    Либо список строк для отправки сообщения.
    """
    photo = None
    car_list = get_data_from_api(command)
    if car_list:
        if len(car_list) > 2:
            return photo, car_list
        photo = car_list[0]['previewImg']
        soup = BeautifulSoup(car_list[0]['content'], 'lxml')
        text = soup.get_text()
        text_list = textwrap.wrap(text, 2000)
        return photo, text_list
    return photo, car_list



def get_text_messages(command):
    """
    Функция возвращает текст информационного  сообщения из БД,
    согласно команде переданной боту пользователем.
    """

    return  Tg_response_msg.objects.filter(command=command).values('content')[0]['content']



def save_mssages_users(user_id, user_name, msg):
    """
    Сохраняет пользователи и сообщение в БД.
    """
    obj, create = Profile.objects.get_or_create(external_id=user_id, name=user_name)
    s = Message.objects.create(profile=obj, text=msg)

def check_admin(user_id):
    """
    Функция проверянт наличие роли bot_admin
    """
    chek = Profile.objects.filter(external_id=user_id).values('bot_admin')[0]['bot_admin']
    return chek

def get_user_list():
    """
    Полчам список по
    """
    qs = Profile.objects.all().values('external_id')
    if qs:
        user_list = [x['external_id'] for x in qs]
        return user_list
    return None
