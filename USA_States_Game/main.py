import turtle
import pandas

states = pandas.read_csv('50_states.csv')
print(states.to_dict())
screen = turtle.Screen()
screen.title('U.S. States Game')
BG = 'blank_states_img.gif'
screen.addshape(BG)  # добавляем овую форму(типа как круг, квадрат или черепашка
turtle.shape(BG)  # создаем черепашку в центре с формой фотографии

"""
// Получаем координаты клика
def coordinates(x, y):
    print(x, y)


screen.onclick(coordinates)  # выполняем действие на клик

screen.mainloop()  # зацикливание бесконечное
"""
states_to_learn = {}
all_answers_player = []


def correct_answer(name):
    timmy = turtle.Turtle()
    timmy.penup()
    timmy.shape('circle')
    timmy.goto(int(states.x[states.state == name]), int(states.y[states.state == name]))  # двигаемся в координаты
    timmy.hideturtle()
    timmy.write(name)


while len(all_answers_player) < 50:
    answer_player = screen.textinput(title=f'{len(all_answers_player)} / 50 Guess the state',
                                     prompt='What\'s another state\'s name?').title()  # красиво получаем ответ игрока
    if answer_player == 'Exit':
        missing_states = []
        for i in states.state:  # пробегаемся по всем штатам
            if i not in all_answers_player:  # элемент из списка не числится отгаданным
                missing_states.append(i)
        print(missing_states)
        states_to_learn_df = pandas.DataFrame(missing_states)
        states_to_learn_df.to_csv('states_to_learn.csv')
        break
    if answer_player in states.state.values and answer_player not in all_answers_player:  # если ответ верный и впервые
        # альтернативный вариант проверки наличия ответа в списках:
        # all_states = states.state.to_list()  # приводим штаты к массиву
        # if answer_player in all_states and ..
        correct_answer(answer_player)  # выводим штат
        all_answers_player.append(answer_player)  # дополняем массив с ответами


# states_to_learn.csv =

screen.exitonclick()