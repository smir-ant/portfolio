from turtle import Turtle
import random
COLORS = ('red', 'orange', 'green', 'blue', 'purple')


class Food(Turtle):
    """Мы можем создать черепашку вызывая Turtle(), но здесь мы меняем сам чертеж, точнее дублируем(наследуем класс),
    изменяем и сохраняем в класс Food(), то бишь, если мы вызовем этот класс, то будет то же самое что и черепашка, но
    модифицированная."""

    def __init__(self):
        super().__init__()
        self.shape('circle')
        self.shapesize(stretch_wid=0.5, stretch_len=0.5)  # изначально черепашку 20х20, мы сделали 10х10
        self.penup()
        self.speed('fastest')  # это скорость как еда появится в центре и дойдет до нужного места
        self.refresh()  # при создании размещаем еду

    def refresh(self):
        """Рандомим место появления, с отступом"""
        self.color(random.choice(COLORS))  # каждый раз разный цвет
        self.goto(random.randint(-280, 280), random.randint(-280, 280))