from turtle import Turtle
import random
COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
DISTANCE_PLUS = 2  # шаг увеличения скорости


class CarManager:
    def __init__(self, cars_count):
        super().__init__()
        self.cars_count = cars_count  # количество машин
        self.move_distance = STARTING_MOVE_DISTANCE  # скорость передвижения
        self.cars = []  # массив с машинками

        # создание машинок
        for i in range(0, self.cars_count):
            self.cars.append(Turtle())
            self.cars[i].penup()
            self.cars[i].shape('square')
            self.cars[i].shapesize(stretch_wid=1, stretch_len=2)
            self.cars[i].color(random.choice(COLORS))  # рандомно выбираем цвет
            self.cars[i].goto(random.randint(-280, 310), random.randint(-230, 260))  # рандомное место на карте

    def increase_speed(self):
        """Увеличение скорости."""
        self.move_distance += DISTANCE_PLUS

    def move(self):
        """Передвижения всех машин."""
        for i in range(0, self.cars_count):  # передвигаем все машинки влево
            self.cars[i].goto(self.cars[i].xcor() - self.move_distance, self.cars[i].ycor())
            if self.cars[i].xcor() <= -320:  # если вышла слева
                self.cars[i].goto(310, random.randint(-230, 260))  # входит справа
                self.cars[i].color(random.choice(COLORS))  # меняет цвет

    def hit(self, player_y):
        """Обнаруживаем столкновение с машиной."""
        for i in range(0, self.cars_count):
            # если машинка находит на Y игрока и машинка находит на X игрока(0), то
            if -20 < (self.cars[i].ycor() - player_y) < 20 and -30 < self.cars[i].xcor() < 30:
                return True