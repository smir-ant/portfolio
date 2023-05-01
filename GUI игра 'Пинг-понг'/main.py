from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time

SPEED_CONTROL_START = 0.1  # начальная скорость игры, для функции time(). МЕНЬШЕ - БЫСТРЕЕ

# настройки экрана
screen = Screen()
screen.bgcolor('black')
screen.setup(width=800, height=600)
screen.title('Pong Game')
screen.tracer(0)  # обновление экрана теперь вручную

# создание платформы
l_paddle = Paddle((-350, 0))
r_paddle = Paddle((350, 0))

# инициализация мяча
ball = Ball()

scoreboard = Scoreboard()

# управление
screen.listen()
screen.onkey(key='Up', fun=r_paddle.move_up)
screen.onkey(key='Down', fun=r_paddle.move_down)
screen.onkey(key='w', fun=l_paddle.move_up)
screen.onkey(key='s', fun=l_paddle.move_down)

game_is_on = True
speed_control = SPEED_CONTROL_START
while game_is_on:
    screen.update()  # начинаем обновлять экран только отсюда
    time.sleep(speed_control)
    ball.move_ball()

    # отскок от пола/потолка
    if ball.ycor() >= 290 or ball.ycor() <= -290:
        ball.bounce_y()

    # успешное отбитие
    if ball.distance(r_paddle) <= 50 and ball.xcor() > 320 or ball.distance(l_paddle) <= 50 and ball.xcor() < -320:
        ball.bounce_x()  # мяч отскакивает
        speed_control *= 0.85  # увеличиваем скорость на 15%

    # если мяч пропущен
    if ball.xcor() > 380 or ball.xcor() < -380:
        if ball.xcor() > 380:
            scoreboard.increase_score_l()  # добавляем очков налево

        elif ball.xcor() < -380:
            scoreboard.increase_score_r()  # добавляем очков направо
        # если поставить это перед if-else не сработает)
        ball.goto(0, 0)  # на стартовую позицию
        ball.bounce_x()  # направляем в другую сторону
        speed_control = SPEED_CONTROL_START

screen.exitonclick()
