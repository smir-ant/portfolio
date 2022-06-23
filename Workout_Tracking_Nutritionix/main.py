import os
import requests
from datetime import datetime


# ================= Заранее мы внесли следующие переменные в окружение =================
print('API_KEY =', os.environ['NUT_API_KEY'])
print('APP_ID =', os.environ['NUT_APP_ID'])


# ================= sheety API =================
SHEETY_ENDPOINT = 'https://api.sheety.co/9b1e1e562d8091e2514889f5aa55068a/yoga/workouts'
SHEETY_HEADER = {'Authorization': os.environ['SHEETY_KEY']}


# ================= nutritionix API =================
NUTRITIONIX_ENDPOINT = 'https://trackapi.nutritionix.com'
"""Авторизация в запросах всегда идет по схеме 'x-...'. Пробелов нет - вместо них тире. 
Upper-case или lower-case - неважно"""
NUTRITIONIX_HEADER = {'Content-Type': 'application/json',
                      'X-APP-ID': os.environ['NUT_APP_ID'],
                      'x-app-key': os.environ['NUT_API_KEY']}


# ================= ВВОД =================
print('\n')
print('Пример ввода: Ran 2 km and walked for 3km')
user_input = input('[Ввод]: Чем сегодня похвалишься(на пиндоском)? -> ').title()  # заглавная большая


# ================= ФИКСИРУЕМ ДАТУ И ВРЕМЯ =================
moment_now = datetime.now()
moment_time = moment_now.time().strftime('%X')
moment_day = moment_now.date().strftime('%x')

print()
print('[Время]:', moment_time)
print('[Дата]:', moment_day)


# ================= обращаемся по API nutritionix =================
params = {'query': user_input,  # обязательно
          'gender': 'male',  # необзятально
          'weight_kg': 61,  # необзятально
          'height_cm': 175,  # необзятально
          'age': 21}  # необзятально

response = requests.post(url=f'{NUTRITIONIX_ENDPOINT}/v2/natural/exercise',
                         json=params,
                         headers=NUTRITIONIX_HEADER)

# print(response.json())  # одинаковый ответ, лол..?)
# print(response.text)  # одинаковый ответ, лол..?)
result = response.json()

for exercise in result['exercises']:
    print('-----')
    print('[Упражнения]:', exercise['name'])
    print('[Длительность]:', exercise['duration_min'], 'мин')
    print('[Cженные каллории]:', exercise['nf_calories'], 'кал')

    """
    dic_of_result[exercise['name']] = {'Duration': exercise['duration_min'],
                                       'Callories': exercise['nf_calories']}
    # если добавляем, то надо добавить и dic_of_result = {}
    # --> {'yoga': {'Duration': 30, 'Callories': 100.65}, 'running': {'Duration': 30, 'Callories': 298.9}}
    """


    # ================= обращаемся по API sheety =================
    # долго не получалось потому что хоть поля в гугл таблице с большой буквы, тут они с маленькой)
    params = {'workout': {'date': moment_day,
                          'time': moment_time,
                          'exercise': exercise['name'].title(),  # с большой буквы
                          'duration': exercise['duration_min'],
                          'calories': exercise['nf_calories']}
              }

    response = requests.post(url=SHEETY_ENDPOINT, json=params, headers=SHEETY_HEADER)
    print(response.text)