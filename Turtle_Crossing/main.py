import time
from turtle import Screen
from player import Player
from scoreboard import Scoreboard
from car_manager import CarManager


# настройки экрана
screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

# инициализации
player = Player()
scoreboard = Scoreboard()
car_manager = CarManager(15)  # делаем машинки в количестве N штук

# управление
screen.listen()
screen.onkey(key='Up', fun=player.move)

game_is_on = True
while game_is_on:

    # проигрыш
    if car_manager.hit(player.ycor()):  # если столковение с машиной
        game_is_on = False  # останавливаем игру
        scoreboard.game_over()  # выводим, что игра закончилась

    # выигрыш
    if player.finish_level():  # если проходим уровень
        player.go_to_start()  # на стартовую позицию
        car_manager.increase_speed()  # скорость +
        scoreboard.increase_score()  # счёт +

    car_manager.move()  # двигаем машинками в такт

    # обновление экрана
    time.sleep(0.1)
    screen.update()

screen.exitonclick()