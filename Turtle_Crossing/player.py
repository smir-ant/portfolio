from turtle import Turtle
STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.left(90)
        self.penup()
        self.condition = ''
        self.shape('turtle')
        self.go_to_start()

    def move(self):
        """Продвижение вперед."""
        self.forward(MOVE_DISTANCE)

    def go_to_start(self):
        """Возврат на стартовую позицию."""
        self.goto(STARTING_POSITION)

    def finish_level(self):
        """Прохождение уровня"""
        if self.ycor() == FINISH_LINE_Y:
            return True