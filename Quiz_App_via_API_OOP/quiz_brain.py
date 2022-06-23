from data import MakeData

"""Обращается к данным и является логикой"""


class GameMaster:
    def __init__(self):
        self.data_process = MakeData()  # инициализируем data.py

    def is_answer_right(self, player_answer):
        """
        Проверяем правильный ли ответ дал пользователь сравнивая нужный от полученного
        :param player_answer: ответ пользователя(1=A, 2=B, 3=C, 4=D)
        :return: Верный ответ(True) или ответ неправильный(False)
        """
        print('-' * 8)
        print('player', player_answer)
        print('right', self.get_right_answer())
        if player_answer != self.get_right_answer():
            return False
        elif player_answer == self.get_right_answer():
            return True

    def switch_difficult(self):
        self.data_process.switch_difficult()  # меняю qType(сложность)
        return self.data_process.get_difficult()  # передаю в ui цифру сложности

    def new_data(self):
        """
        Обращаемся к data.py и тамошнему методу new_data(), что новый запрос API сделает
        """
        self.data_process.new_data()

    def get_right_answer(self):
        """
        :return: правильный ответ из data.py
        """
        return self.data_process.right_answer

    def get_answers(self):
        """
        :return: ответы из data.py
        """
        return self.data_process.answers

    def get_question(self):
        """
        :return: вопрос из data.py
        """
        return self.data_process.question