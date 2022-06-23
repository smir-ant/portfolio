from turtle import Turtle
STEP = 10  # шаг нашего мяча, на кратности 10 всё повязано


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('circle')
        self.penup()
        self.speed(1)
        self.color('white')
        self.y_step = STEP
        self.x_step = STEP

    def move_ball(self):
        self.goto(x=self.xcor() + self.x_step, y=self.ycor() + self.y_step)

    def bounce_y(self):
        """Метод отскока от верх-нижней рамки."""
        self.y_step *= -1  # меняем знак по Y на обратный

    def bounce_x(self):
        """Метод отскока от верх-нижней рамки."""
        self.x_step *= -1  # меняем знак по Y на обратный