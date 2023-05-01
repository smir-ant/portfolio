from turtle import Turtle
STEP = 20  # шаг наших платформ


class Paddle(Turtle):
    def __init__(self, coordinates):
        super().__init__()
        self.shape('square')
        self.color('white')
        self.penup()
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.goto(coordinates)  # отправляем на точку

    def move_up(self):
        self.goto(x=self.xcor(), y=self.ycor() + STEP)

    def move_down(self):
        self.goto(x=self.xcor(), y=self.ycor() - STEP)