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
    text = get_data_from_api(command)[0]['content']
    soup = BeautifulSoup(text, 'lxml')
    text = soup.get_text()
    text_list = textwrap.wrap(text, 1500)
    return text_list

def get_data_from_api_car_no_HTML(command):
    """
    Функция возвращает либо список словарей для формирования кнопок,
    при условии, что найдено несколько моделей авто подходящих под
    критерий поиска.
    Либо список строк для отправки сообщения.
    """
    car_list = get_data_from_api(command)
    if car_list:
        if len(car_list) > 2:
            return car_list

        soup = BeautifulSoup(car_list[0]['content'], 'lxml')
        text = soup.get_text()
        text_list = textwrap.wrap(text, 2000)
        return text_list
    return car_list



def get_text_messages(command):
    """
    Функция возвращает текст информационного  сообщения из БД,
    согласно команде переданной боту пользователем.
    """
    return Tg_response_msg.objects.filter(command=command).values('content')[0]['content']

def save_mssages_users(user_id, user_name, msg):
    """
    Сохраняет пользователи и сообщение в БД.
    """
    obj, create = Profile.objects.get_or_create(external_id=user_id, name=user_name)
    s = Message.objects.create(profile=obj, text=msg)