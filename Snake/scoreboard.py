from turtle import Turtle
# форматирование вывода счета
ALIGNMENT = 'center'  # выравнивание
FONT = ('Courier', 24, 'normal')  # шрифт


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.score = 0  # стартовое значение счета
        with open('data.txt') as data:  # открываем файл data.txt
            self.high_score = int(data.read())  # читаем лучший счет
        self.goto(x=0, y=270)  # перемещаем выше
        self.penup()
        self.color('white')  # цвет черепашки белый
        self.update_score()  # стартовый вывод счета
        self.hideturtle()  # делаем черепашку невидимой

    def increase_score(self):
        """Метод, увеличивающиий счет и вызывающий обновление счета на экране."""
        self.score += 1
        self.update_score()

    def update_score(self):
        """Метод, выводящий актуальный счет."""
        self.clear()
        self.write(f"Score: {self.score} High Score: {self.high_score}", align=ALIGNMENT, font=FONT)

    def reset_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open('data.txt', 'w') as file:
                file.write(f'{self.score}')
        self.score = 0
        self.update_score()