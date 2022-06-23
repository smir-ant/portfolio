from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import time

# настройка экрана
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor('black')  # цвет заливки фона
screen.title('My Snake Game')  # заголовок(сверху) окна
screen.tracer(0)  # обновление экрана теперь только вручную

# инициализация наших классов
snake = Snake()  # инициализация змейки(создаются и настраиваются три сегмента)
food = Food()
scoreboard = Scoreboard()

game_is_on = True

while game_is_on:
    screen.update()  # обновляем экран вручную
    time.sleep(0.1)  # таймер в 0.1 секунду, чтобы она не улетала

    snake.move()  # каждый тик змея двигается и "слушает" повороты

    # Столкновение с едой.
    if snake.segments[0].distance(food) < 15:  # если дистанция между головой змейки и едой < 15
        # p.s. 15 потому что половина змейки(10) + половинка еды(5) ((их границы))
        scoreboard.increase_score()  # увеличиваем счет
        food.refresh()  # генерируем новый хавчик
        snake.extend()  # расширяем змейку

    # Столкновение со стеной.
    if snake.segments[0].xcor() > 290 or snake.segments[0].xcor() < -290 or snake.segments[0].ycor() > 290 or \
            snake.segments[0].ycor() < -290:  # если голова сталкивается с границами
        scoreboard.reset_score()  # обновление счета(сброс и лучший счет)
        snake.reset()  # старую змейку на кладбище, новую создаем

    # Столкновение с хвостом.
    for segment in snake.segments[1:]:  # для каждого сегмента змейки, кроме головы
        if snake.segments[0].distance(segment) < 10:  # если дистанция до другого сегмент < 10(столкновение)
            scoreboard.reset()  # обновление счета(сброс и лучший счет)
            snake.reset()  # старую змейку на кладбище, новую создаем

screen.exitonclick()