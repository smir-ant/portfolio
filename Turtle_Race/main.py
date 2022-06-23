from turtle import Turtle, Screen
import random


def turtle_race():
    screen = Screen()
    screen.setup(width=500, height=400)  # настройка разрешения окна

    color_list = ['red', 'orange', 'yellow', 'green', 'purple']  # список заранее определенных цветов
    user_bet = ''
    while user_bet not in color_list:
        user_bet = screen.textinput(title='Make your bet',
                                    prompt='Which turtle will win the race? Enter a color: ').lower()
        # всплывашка с названием и сообщением, полученное значение в нижний регистр и в переменную user_bet

    y_first = -100  # нижняя, стартовая точка для черепах
    all_turtles = []  # список со всеми созданными черепахами

    for i in range(0, 5):
        all_turtles.append(Turtle(shape='turtle'))  # закидываем в список черепаху
        all_turtles[i].color(color_list[i])  # меняем у черепашки ее цвет(по ее индексу)
        all_turtles[i].penup()  # убираем чернила
        all_turtles[i].setpos(x=-230, y=y_first)  # сдвигаем
        y_first += 50  # меняем y координату для след. черепахи

    is_game_on = True  # валидность ставки игрока обеспечена выше, потому без проверок запускаем

    while is_game_on:
        for turtle in all_turtles:
            if turtle.xcor() > 230:
                win_color = turtle.pencolor()  # если оставим color, то там два цвета в кортеже
                if user_bet == win_color:
                    print(f'Your bet[{user_bet}] win! The {win_color} is winner of the race!')
                    return  # избегаем двойных победителей
                else:
                    print(f'Your bet[{user_bet}] lose. The {win_color} is winner of the race!')
                    return  # избегаем двойных победителей

        for i in range(len(all_turtles)):
            all_turtles[i].forward(random.randint(0, 10))  # двигаем каждую черепашку рандомно на 0-10 вперед

    screen.exitonclick()


turtle_race()  # функция для вывода только первого(одного!) победителя