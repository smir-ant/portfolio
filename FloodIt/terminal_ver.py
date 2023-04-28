from random import choice, randint
size = 15
moves = round(size * 1.8)  # попыток будет размерность x1.8 с округлением
elements = ("🟥", "🟨", "🟩", "🟦", "🟪", "⬜")

field = {}  # хранение в словаре, чтобы не выходить за пределы списка. {(2, 1): 🟦}
for row in range(size):
    for column in range(size):
        field[(row, column)] = choice(elements)

# Делаем несколько элементов такими же, как соседний.
# В результате получаются группы элементов одинакового цвета/формы.
for i in range(size * 4):
    x = randint(0, size - 2)
    y = randint(0, size - 1)
    field[(x + 1, y)] = field[(x, y)]


def draw():
    "Отрисовка поля"
    print("=" * 15)
    for row in range(size):
        for column in range(size):
            print(field[(row, column)], end="")
        print()

def change_tile(x, y, charToChange):
    "С рекурсивным вызовом"
    if x == 0 and y == 0:
        if field[(x, y)] == charToChange:
            return True  # простой случай: тот же самый элемент

    field[(x, y)] = charToChange  # заменяем цвет

    if x > 0 and field[(x - 1, y)] == previos_color:
        change_tile(x=x-1, y=y, charToChange=charToChange)  # рекурсивно меняем символ СЛЕВА(-x)

    if x < size - 1 and field[(x + 1, y)] == previos_color:
        change_tile(x=x+1, y=y, charToChange=charToChange)  # рекурсивно меняем символ СПРАВА(+x)

    if y > 0 and field[(x, y - 1)] == previos_color:
        change_tile(x=x, y=y-1, charToChange=charToChange)  # рекурсивно меняем символ ВВЕРХ(-y)
    
    if y < size - 1 and field[(x, y+1)] == previos_color:
        change_tile(x=x, y=y+1, charToChange=charToChange)  # рекурсивно меняем символ ВНИЗ(+y)
    
def turn():
    "Спрашиваем цвет и вызываем смену плиток"
    global moves
    choose = input("Введи одну букву для выбора цвета:"
                   "\n(Б)елый,  (Ж)ёлтый, (З)елёный, (К)расный, (С)иний, (Ф)иолетовый"
                   "\n>>> ").upper()
    while choose != "Б" and choose != "Ж" and choose != "З" and choose !="К" and choose != "С" and choose != "Ф":  # ВАЛИДАЦИЯ
        choose = input("(Б)елый,  (Ж)ёлтый, (З)елёный, (К)расный, (С)иний, (Ф)иолетовый"
                       "\n>>> ").upper()
    if choose == "Б":
        if not change_tile(x=0, y=0, charToChange="⬜"):  # если та же клетка
            moves -= 1
    elif choose == "Ж":
        if not change_tile(x=0, y=0, charToChange="🟨"):
            moves -= 1
    elif choose =="З":
        if not change_tile(x=0, y=0, charToChange="🟩"):
            moves -= 1
    elif choose == "К":
        if not change_tile(x=0, y=0, charToChange="🟥"):
            moves -= 1
    elif choose == "С":
        if not change_tile(x=0, y=0, charToChange="🟦"):
            moves -= 1
    else:
        if not change_tile(x=0, y=0, charToChange="🟪"):
            moves -= 1

def is_win():
    global moves
    # првоеряем что клетки заполнены одним цветом
    for row in range(size):
        for column in range(size):
            if field[(row, column)] != field[(0, 0)]:
                return False  # если нашли не подходящую, то выход
    if moves >= 0:  # плюс если ходы ещё остались(равно это в последний ход)
        return True

while True:
    draw()
    previos_color = field[(0, 0)]
    turn()
    if is_win():
        draw()
        print("ТЫ ПОБЕДИЛ")
        quit()
    if moves == 0:
        draw()
        print("ТЫ ПРОИГРАЛ")
        quit()
    print("Ходов осталось:", moves)
