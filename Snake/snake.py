from turtle import Turtle, Screen

STARTING_POS = [(0, 0), (-20, 0), (-40, 0)]  # стартовые координаты + кол-во стартовых сегментов. константа
MOVE_DISTANCE = 20
RIGHT, UP, LEFT, DOWN = 0, 90, 180, 270  # направления(угол) взгляда в turtle


class Snake:
    def __init__(self):
        self.segments = []  # сегменты змейки
        self.screen = Screen()
        self.create_snake()  # создаем змейку

    def create_snake(self):
        """Создание массива черепашек(змейки). Просто обращаемся к методу создания ячейки 3 раза."""
        for position in STARTING_POS:
            self.add_segment(position)

    def add_segment(self, position):
        new_segment = Turtle('square')
        new_segment.color('white')
        new_segment.penup()
        new_segment.setpos(position)  # каждому задаем его позицию
        self.segments.append(new_segment)

    def reset(self):
        for seg in self.segments:
            seg.goto(1000, 1000)  # выбрасываем на кладбище кажыдй сегмент
        self.segments.clear()  # очищаем его(визуально он остается)
        self.create_snake()  # создаем новую змейку

    def extend(self):
        """Просто обращаемся к методу создания ячейки 1 раз."""
        self.add_segment(self.segments[-1].position())

    def move(self):
        """Метод передвижения: голова бесконечно шагает вперед и может поворачивать, тело повторяет за головой."""
        def left():  # вложенный метод, без self, ибо он создан локально (не просто в классе, а в его методе)
            if self.segments[0].heading() != RIGHT:
                self.segments[0].setheading(LEFT)

        def right():
            if self.segments[0].heading() != LEFT:
                self.segments[0].setheading(RIGHT)

        def up():
            if self.segments[0].heading() != DOWN:
                self.segments[0].setheading(UP)

        def down():
            if self.segments[0].heading() != UP:
                self.segments[0].setheading(DOWN)

        # ниже перемещаем все с хвоста ближе к голове
        for seg in range(len(self.segments) - 1, 0, -1):  # идем от хвоста к голове(0 не включается, потому до 1.
            new_xy = (self.segments[seg - 1].xcor(), self.segments[seg - 1].ycor())
            # записываем координаты, где находится сегмент ближе к голове

            self.segments[seg].goto(new_xy)  # перемещаем задний сегмент на впереди идущий сегмент

        # ниже перемещаем голову
        self.screen.listen()
        self.screen.onkey(key='a', fun=left)  # если бы left() был просто одним из методов класса, то мы бы обращались
        # к нему как self.left, а так как он создан локально, то left
        self.screen.onkey(key='d', fun=right)
        self.screen.onkey(key='w', fun=up)
        self.screen.onkey(key='s', fun=down)
        self.segments[0].forward(MOVE_DISTANCE)  # бесконечно шагаем вперед