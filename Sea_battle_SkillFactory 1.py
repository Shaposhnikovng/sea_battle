from random import randint


# Класс точки на доске, координаты точки
class Dot:
    def __init__(self, x, y):  # координаты точки x и y
        self.x = x
        self.y = y

    def __eq__(self, other):  # проверяет равенство точек
        return self.x == other.x and self.y == other.y

    # Вывод в консоль
    def __repr__(self):
        return f"({self.x}, {self.y})"


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
    def __init__(self, bow, l,
                 o):  # bow - точка, где находится корабль, l = длина корабля, o - ориентация корабля на карте ( o= 1 - вертикально или o= 0 - горизонтально)
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


# Класс игровой доски
class Board:
    def __init__(self, hid=False, size=6):  # hid - показаны корабли или нет, size - размер доски
        self.size = size
        self.hid = hid

        self.count = 0  # счётчик, подсчитывает сколько кораблей на доске уничтожено

        self.field = [["О"] * size for _ in
                      range(size)]  # задаём доску размером 6х6 с помощью двумерного спика, изначально везде будет "О"
        # в которых будут размещены "O" - пустая ячейка
        # ■ - в точке находится корабль,
        # Т - куда стреляли,
        # Х - если корабль подбили в этой точке.
        self.busy = []
        self.ships = []

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()  # исключения: выход корабля за границу,либо на заянтую точку
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):  # область вокруг корабля
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:  # область в виде точек вокруг расположения корабля
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 | "
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "О")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):  # возвращает нужно ли повторять ход
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:  # стрельба по кораблям
            if d in ship.dots:
                ship.lives -= 1  # при попадании уменьшаем кол-во жизней на 1
                self.field[d.x][d.y] = "X"  # при попадании уменьшаем кол-во жизней на 1 и ставим Х
                if ship.lives == 0:  # если у корабля осталось 0 жизней, то увеличиваем счёт на 1
                    self.count += 1  # если у корабля осталось 0 жизней, то увеличиваем счёт на 1
                    self.contour(ship,
                                 verb=True)  # обведем контуры уничтоженного корабля, так как на этой площади кораблей быть не может
                    print("Корабль уничтожен!")
                    return False  # когда False - корабль уничтожен и ход переходит противнику
                else:
                    print("Корабль подбит!")
                    return True  # когда корабль подбит, то игром может сделать повторный выстрел (Если True)
        self.field[d.x][d.y] = "."  # при промахе ставится "." и надпись "Мимо!"
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):  # метод хода
        while True:
            try:
                target = self.ask()  # спрашивается точка куда стрелять
                repeat = self.enemy.shot(target)  # выполняется выстрел
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1}{d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()  # запрашиваются координады, разбиваем с помощью split

            if len(cords) != 2:
                print("Введите 2 кооринаты")  # если введено больше 2х координат, то потребуется ввести заново
                continue  # если введены верно 2 координаты, то цикл продолжится

            x, y = cords  # распаковка координат

            if not (x.isdigit()) or not (y.isdigit()):  # проверка, что вводятся числа
                print("Введите числа")
                continue

            x, y = int(x), int(y)  # преобразование х и у к числу

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("------------------")
        print(" Приветствуем Вас ")
        print("      в игре      ")
        print("   Морской бой!   ")
        print("------------------")
        print("Формат ввода: x, y")
        print(" X - номер строки ")
        print(" Y - номер столбца")
        print("------------------")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска игрока: ")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера: ")
            print(self.ai.board)
            print("-" * 20)
            if num % 2 == 0:
                print("-"*20)
                print("Ход игрока")
                repeat = self.us.move()
            else:
                print("-"*20)
                print("Ход компьютера")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Игрок одержал победу!")
                break
            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьтер одержал победу!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
