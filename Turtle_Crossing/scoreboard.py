from turtle import Turtle
ALIGNMENT = 'center'
FONT = ("Courier", 24, "normal")
START_POSITION = (-230, 270)


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.goto(START_POSITION)
        self.score = 0
        self.update_score()  # выводим счет

    def update_score(self):
        """Обновление счета."""
        self.clear()
        self.write(arg=f'Score: {self.score}', align=ALIGNMENT, font=FONT)

    def increase_score(self):
        """Увеличение счета."""
        self.score += 1
        self.update_score()

    def game_over(self):
        """Вывод 'Game Over'."""
        self.goto(x=0, y=0)
        self.write(arg='ПОТРАЧЕНО', align=ALIGNMENT, font=FONT)