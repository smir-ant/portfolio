import tkinter
from quiz_brain import GameMaster


class QuizInterface:
    def __init__(self):
        self.quiz = GameMaster()
        self.quiz.new_data()

        self.window = tkinter.Tk()
        self.window.title('Кто хочет сосать у миллионера')
        self.window.minsize(width=400, height=400)
        self.window.config(padx=20, pady=20, bg='#375362')  # паддинг в окне = 20px(отступ по краям от рамок)
        # self.switch_timer = self.window.after(ms=20, func=self.quiz.new_data)

        # ТЕКСТ
        self.canvas = tkinter.Canvas(width=400,  # квадратный холст
                                     height=400,
                                     highlightthickness=0)  # отключить обводку

        self.question_text = self.canvas.create_text(200,
                                                     200,
                                                     text='',
                                                     width=400,
                                                     font=("Arial", 30, "bold"),
                                                     fill="black")
        self.canvas.grid(row=1, column=0, columnspan=2, pady=8)

        # КНОПКИ
        # лямбда функция используется так как мне нужен аргумент
        self.button_A = tkinter.Button(text='',  # текст кнопки
                                       padx=20,  # отступ от границ до содержимого по горизонтали
                                       width=18,
                                       pady=8,  # отступ от границ до содержимого по вертикали
                                       font=16,  # высота шрифта
                                       highlightthickness=0,  # отключаем обводку белым
                                       command=lambda: self.check_answer(0)  # передаем ответ А=0
                                       )
        self.button_A.grid(column=0, row=2, pady=7, padx=7)

        self.button_B = tkinter.Button(text='',  # текст кнопки
                                       padx=20,  # отступ от границ до содержимого по горизонтали
                                       width=18,
                                       pady=8,  # отступ от границ до содержимого по вертикали
                                       font=16,  # высота шрифта
                                       highlightthickness=0,  # отключаем обводку белым
                                       command=lambda: self.check_answer(1)  # передаем ответ B=1
                                       )
        self.button_B.grid(column=1, row=2)

        self.button_C = tkinter.Button(text='',  # текст кнопки
                                       padx=20,  # отступ от границ до содержимого по горизонтали
                                       width=18,
                                       pady=8,  # отступ от границ до содержимого по вертикали
                                       font=16,  # высота шрифта
                                       highlightthickness=0,  # отключаем обводку белым
                                       command=lambda: self.check_answer(2)  # передаем ответ C=2
                                       )
        self.button_C.grid(column=0, row=3)

        self.button_D = tkinter.Button(text='',  # текст кнопки
                                       padx=20,  # отступ от границ до содержимого по горизонтали
                                       width=18,
                                       pady=8,  # отступ от границ до содержимого по вертикали
                                       font=16,  # высота шрифта
                                       highlightthickness=0,  # отключаем обводку белым
                                       command=lambda: self.check_answer(3)  # передаем ответ D=3
                                       )
        self.button_D.grid(column=1, row=3)

        self.button_difficult = tkinter.Button(text="ПРИМИТИВНО",  # текст кнопки
                                               fg='green',
                                               padx=20,  # отступ от границ до содержимого по горизонтали
                                               width=10,
                                               pady=8,  # отступ от границ до содержимого по вертикали
                                               font=16,  # высота шрифта
                                               highlightthickness=0,  # отключаем обводку белым
                                               command=self.switch_difficult
                                               )
        self.button_difficult.grid(column=0, row=0, columnspan=2)

        self.draw_question_answers()  # ЗАПУСКАЕМ

        self.window.mainloop()

    def check_answer(self, player_answer):
        """
        Узнаем правильный ли дан был ответ, красим фон в зеленый если правильный и красный если нет.
        :param player_answer: цифра нажатой кнопки передается из функции нажатия на ответ
        """
        if self.quiz.is_answer_right(player_answer=player_answer):
            self.green_bg()
            print('RIGHT')
        elif not self.quiz.is_answer_right(player_answer):
            self.red_bg()
            print('WRONG')
        # через секунду паузы(чтобы был фон отрисован) запускаем след. вопрос-ответ
        self.window.after(ms=1000, func=self.next_question_answer)  # p.s. работает без таймеров

    def next_question_answer(self):
        """
        Формируем новые данные(вопрос-ответ-пр.ответ)
        """
        # меняем вопрос-ответ
        self.quiz.new_data()  # берем паузу в 2 секунды перед новым вопросом
        self.draw_question_answers()

    def red_bg(self):  # функция, что окрашивает фон в красный, если ответ был неправильным
        """
        Отрисовывает на фоне холста красный цвет
        """
        self.canvas.config(bg='red')

    def green_bg(self):
        """
        Отрисовывает на фоне холста зеленый цвет
        """
        self.canvas.config(bg='green')

    def switch_difficult(self):
        """
        Смена сложности, обновление данных под сложность новую и отрисовка новых вопрос-ответов
        """
        # сперва меняем сложность
        difficult = self.quiz.switch_difficult()  # меняю сложность и получаю ее в return
        if difficult == 1:  # ЛЕГКАЯ СЛОЖНОСТЬ
            self.button_difficult.config(text="ПРИМИТИВНО", fg='green')
        elif difficult == 2:  # НОРМАЛЬНАЯ СЛОЖНОСТЬ
            self.button_difficult.config(text="НОРМАЛЬНО", fg='dark orange')
        elif difficult == 3:  # ВЫСОКАЯ СЛОЖНОСТЬ
            self.button_difficult.config(text="СЛОЖНО", fg='red')

        # затем обновляем данные
        self.quiz.new_data()

        # следом переписовываю новые вопрос и ответы
        self.draw_question_answers()

    def draw_question_answers(self):
        """
        - Получаю вопрос и ответы;
        - Раскидываю ответы по кнопкам;
        - Скидываю задний цвет холста. Меняю текст вопроса;
        :return:
        """

        # скидываю цвет фона
        self.canvas.config(bg='white')

        # получаем вопрос и меняем текст на холсте
        next_questions = self.quiz.get_question()
        self.canvas.itemconfig(self.question_text, text=next_questions)

        # получаем ответы и меняем кнопки
        answers = self.quiz.get_answers()
        print(answers)
        self.button_A.config(text=f'A. {answers[0]}')
        self.button_B.config(text=f'B. {answers[1]}')
        self.button_C.config(text=f'C. {answers[2]}')
        self.button_D.config(text=f'D. {answers[3]}')