import requests
from random import shuffle


class MakeData:
    def __init__(self):

        self.params = {'qType': 1,  # УРОВЕНЬ СЛОЖНОСТИ, 1-3: 1-легко, 3-сложные
                       'count': 1}  # получаем одну связку вопрос-ответ

        # первоопределение
        self.question = ''
        self.answers = []
        self.right_answer = 5

    def new_data(self):
        """
        Отправляем API запрос, считываем ответ, меняем:
        - question = вопрос
        - answers = 4 вопроса на него, перемешанные
        - right_answers = правильный ответ, число
        """
        response = requests.get('https://engine.lifeis.porn/api/millionaire.php',
                                params=self.params)  # обращаемся по API
        response.raise_for_status()  # ловим ошибки если есть
        api_response = response.json()  # читаем ответ

        self.question = api_response['data'][0]['question']  # забираем вопрос                           <----------
        self.answers = api_response['data'][0]['answers']  # забираем ответы                             <----------
        self.right_answer = self.answers[0]  # фиксируем правльный ответ string
        # Перемешиваем ответы
        shuffle(self.answers)

        # Находим какой ответ правильный
        self.right_answer = self.answers.index(self.right_answer)  # индекс правильного ответа. 1=A, 2=B, 3=C, 4=D <---
        print('[Номер правильного ответа]:', self.right_answer)  # индекс правильного ответа. 1=A, 2=B, 3=C, 4=D

    def switch_difficult(self):
        """
        Меняем qType - параметр для запроса API.
        УРОВЕНЬ СЛОЖНОСТИ, 1-3: 1-легко, 3-сложно
        """
        if self.params['qType'] < 3:  # если 1 или 2, то плюсуем
            self.params['qType'] += 1
        else:
            self.params['qType'] = 1

    def get_difficult(self):
        """
        :return: значение qType(сложности текущей)
        """
        return self.params['qType']