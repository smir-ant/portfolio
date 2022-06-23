import requests  # для работы с API
from datetime import datetime  # из модуля datetime импортируем класс datetime, для узнавания текущего времени
import smtplib  # для отправления письма
import time  # для задержки в минуту

MY_LAT = 55.014673
MY_LNG = 82.942240
UTC = 7

smtp_host = 'smtp.gmail.com'
MY_MAIL_LOGIN = 'ivanovich.py@gmail.com'
MY_MAIL_PASS = 'SuperSecret'
SEND_MAIL = 'Your_Email@email.here'


def is_iss_overhead():  # получили словарь
    """
    если iss рядом с разницей в 5 градусов, то возвращает True, иначе  False
    """
    response = requests.get(url='http://api.open-notify.org/iss-now.json')  # получаем ответ отправляя запров на url api
    response.raise_for_status()  # чекаем есть ли ошибка при получении
    iss_data = response.json()['iss_position']

    # если разница с позицией iss в 5градусов по длине или ширине, то
    if abs(MY_LAT - float(iss_data['latitude'])) <= 5 and abs(MY_LNG - float(iss_data['longitude'])) <= 5:
        return True


def is_dark_now():
    """
    возвращает True если сейчас темно, иначе False
    """
    parameters = {
        'lat': MY_LAT,
        'lng': MY_LNG,
        'formatted': 0,  # говорим ему, что мы не хотим форматирования
    }

    # получаем ответик по времени рассвета и заката формата:
    response = requests.get('https://api.sunrise-sunset.org/json', params=parameters)
    # либо можно просто в ссылку воткнуть параметры >> https://api.sunrise-sunset.org/json?lat=55.014673&lng=82.942240
    response.raise_for_status()  # чекаем есть ли ошибка при получении
    sun_sun_data = response.json()['results']  # получаем словарь json и входим сразу в 'results'

    # ЗАКАТ
    time_sunset = sun_sun_data['sunset'].split('T')[1].split('+')[0]
    time_sunset = int(time_sunset.split(":")[0]) + UTC
    # часы + 7  // все это из 10:28:59

    # РАССВЕТ
    time_sunrise = sun_sun_data['sunrise'].split('T')[1].split('+')[0]
    time_sunrise = int(time_sunrise.split(":")[0]) + UTC
    # часы + 7  // все это из 01:56:19

    # если сейчас время после заката или перед рассветом
    if time_sunset <= datetime.now().hour or datetime.now().hour <= time_sunrise:
        return True


def send_mail():
    with smtplib.SMTP(smtp_host) as connection:
        connection.starttls()
        connection.login(MY_MAIL_LOGIN, MY_MAIL_PASS)
        connection.sendmail(MY_MAIL_LOGIN, SEND_MAIL, 'Subject:Look up!👆\n\nISS is near. Overhead.')


while True:
    print(is_dark_now())  # ОТЛАДКА
    print(is_iss_overhead())  # ОТЛАДКА
    print('-' * 8)

    # если сейчас и темно iss рядом
    if is_dark_now() and is_iss_overhead():
        send_mail()

    time.sleep(60)  # ожидание минута