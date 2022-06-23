import requests
from datetime import datetime

# https://pixe.la/ - трекер, обращаться с ним исключительно по API
PIXELA_ENDPOINT = 'https://pixe.la/v1/users'
PIXELA_HEADER = {'X-USER-TOKEN': 'secret'}
PIXELA_USERNAME = 'secret'


def signup():

    params = {
        'token': PIXELA_HEADER['X-USER-TOKEN'],
        'username': PIXELA_USERNAME,
        'agreeTermsOfService': 'yes',
        'notMinor': 'yes'  # 18+
    }

    response = requests.post(url=PIXELA_ENDPOINT, json=params)
    # response = response.json()  # как мы делали раньше и как работало и работает сейчас
    print(response.text)  # как можно сделать сейчас


def create_graph():
    pixela_graph_endpoint = f'{PIXELA_ENDPOINT}/{PIXELA_USERNAME}/graphs'
    params = {
        'id': 'graph1',
        'name': 'Minutes of yoga',
        'unit': 'min',
        'type': 'int',
        'color': 'shibafu',
    }

    response = requests.post(url=pixela_graph_endpoint, json=params, headers=PIXELA_HEADER)
    # response = response.json()  # как мы делали раньше и как работало и работает сейчас
    print(response.text)  # как можно сделать сейчас


def add_point():
    """
    Добавляем точку
    :return:
    """
    # ======== ЗАПРАШИВАЕМ СПИСОК ВСЕХ ГРАФОВ ПОЛЬЗОВАТЕЛЯ ========
    #
    response = requests.get(url=f'{PIXELA_ENDPOINT}/{PIXELA_USERNAME}/graphs', headers=PIXELA_HEADER)
    graph_dic = {}  # массив для будущих значений ID графов
    for i in response.json()['graphs']:  # пробегаемся по всем графам
        print(i)
        graph_dic[i['id']] = i['name']  # выносим в словарь связку id  и название графа

    # ======== ВЫБИРАЕМ ГРАФ ========
    print('\nВсе графы:')
    for i in graph_dic:
        print(f'    – {i}')  # выбираем по ключу в словаре
    choice = input('Введите ID графа для выбора -> ')

    # ======== СТАВИМ ТОЧКУ ========
    yoga_min = input('Сколько сегодня ты позанимался йогой? -> ')
    params = {
        'date': datetime.now().strftime('%Y%m%d'),  # дата где ставить точку
        'quantity': yoga_min  # он суммирует стринги, боже??
    }

    print(params)
    response = requests.post(url=f'{PIXELA_ENDPOINT}/{PIXELA_USERNAME}/graphs/{choice}',
                             headers=PIXELA_HEADER, json=params)
    print(response.text)


def update_point():
    """
    Используем метод put чтобы обновить данные.
    """
    params = {'quantity': '20'}  # значение на которое мы изменим
    date = '20211201'
    response = requests.put(url=f'{PIXELA_ENDPOINT}/{PIXELA_USERNAME}/graphs/graph1/{date}',
                            json=params,  # передаем значение, собственно
                            headers=PIXELA_HEADER)
    print(response.text)


def delete_point():
    """
    Удалить точку. Метод delete.
    """
    params = {'quantity': '20'}  # значение на которое мы изменим
    date = '20211201'
    response = requests.delete(url=f'{PIXELA_ENDPOINT}/{PIXELA_USERNAME}/graphs/graph1/{date}', headers=PIXELA_HEADER)
    print(response.text)

# signup()  # регистрация пользователя
# create_graph()  # создаем таблицу
# add_point()  # добавляем точку в нашем графе
# update_point()  # изменить значение точки
delete_point()  # удаление метки