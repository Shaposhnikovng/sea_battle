from random import randint

# Класс точки на доске, координаты точки
class Dot:
    def __init__(self, x, y):  # координаты точки x и y
        self.x = x
        self.y = y
    def __eq__(self, other): # проверяет равенство точек
        return self.x == other.x and self.y == other.y

    # Вывод в консоль
    def __repr__(self):
        return f"({self.x}, {self.y})"


# d = Dot(1, 1)
# print(d)

class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за пределы доски"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class BoardWrongShipException(BoardException):
    pass

# Класс корабля
class Ship:
    def __init__(self, bow, l, o):  # bow - точка, где находится корабль, l = длина корабля, o - ориентация корабля на карте ( o= 1 - вертикально или o= 0 - горизонтально)
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):  # список точек корабля (которые занимает)
        ship_dots = []
        for i in range(self.l):  # перебираем все точки корабля
            cur_x = self.bow.x  # точки, в которых находимся
            cur_y = self.bow.y  # точки, в которых находимся
            if self.o == 0:  # горизонтальная ориентация
                cur_x += i
            elif self.o == 1:  # вертикальная ориентация
                cur_y += i
            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


# s = Ship(Dot(1, 1), 3, 1)
# d = Dot(1, 2)
# print(d in s.dots)


# Класс игровой доски
class Board:
    def __init__(self, hid=False, size=6): # hid - показаны корабли или нет, size - размер доски
        self.size = size
        self.hid = hid

        self.count = 0 # счётчик, подсчитывает сколько кораблей на доске уничтожено

        self.field = [ ["O"]*size for _ in range(size) ]     # задаём доску размером 6х6 с помощью двумерного спика, изначально везде будет "О"
                                                             # в которых будут размещены "O" - пустая ячейка
                                                             # ■ - в точке находится корабль,
                                                             # Т - куда стреляли,
                                                             # Х - если корабль подбили в этой точке.
        self.busy = []
        self.ships = []

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException() # исключения: выход корабля за границу,либо на заянтую точку
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)
        self.contour(ship)

    def contour(self, ship, verb = False): # область вокруг корабля
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for d in ship.dots: # область в виде точек вокруг расположения корабля
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 | "
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"
        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        return ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()
        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships: # стрельба по кораблям
            if d in ship.dots:
                ship.lives -= 1 # при попадании уменьшаем кол-во жизней на 1
                self.field[d.x][d.y] = "X" # при попадании уменьшаем кол-во жизней на 1 и ставим Х
                if ship.lives == 0: # если у корабля осталось 0 жизней, то увеличиваем счёт на 1
                    self.count += 1 # если у корабля осталось 0 жизней, то увеличиваем счёт на 1
                    self.contour(ship, verb = True) # обведем контуры уничтоженного корабля, так как на этой площади кораблей быть не может
                    print("Корабль уничтожен!")
                    return False # когда False - корабль уничтожен и ход переходит противнику
                else:
                    print("Корабль подбит!")
                    return True # когда корабль подбит, то игром может сделать повторный выстрел (Если True)
        self.field[d.x][d.y] = "." # при промахе ставится "." и надпись "Мимо!"
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []

def random_place(size = 6):
    lens = [3, 2, 2, 1, 1, 1, 1] # создаем список кораблей 1 - трехпалубный
                                                            # 2 - двухпалубных
                                                            # 4 - однопалубных
    # lens = [1, 1, 1, 1, 2, 2, 3]
    board = Board() # создаём игровую доску
    attempts = 0 # создаём счётчик попыток
    for l in lens:
        while True:
            attempts += 1
            if attempts > 2000:
                return None
            ship = Ship(Dot(randint(0, size), randint(0, size)), l, randint(0, 1))
            try:
                board.add_ship(ship)
                break
            except BoardWrongShipException:
                pass
    return board
    # board.begin()
b = random_place()
print(b)
b.begin()
print(b)
b.shot(Dot(1,1))

# b = Board(hid = 0)
# s = Ship(Dot(0, 1), 3, 1)
# b.add_ship(s)
# s = Ship(Dot(2, 3), 3, 1)
# b.add_ship(s)
# print(b)
