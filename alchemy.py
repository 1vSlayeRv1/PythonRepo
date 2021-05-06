import abc


class Alchemy(metaclass=abc.ABCMeta):
    words = {'вода', 'огонь', 'земля', 'воздух'}

    def __add__(self, other):
        if len({self.__class__.__name__, other.__class__.__name__} & {'Fire', 'Water'}) == 2:
            Elements().__call__("пар")
        elif len({self.__class__.__name__, other.__class__.__name__} & {'Par', 'Ground'}) == 2:
            Elements().__call__("гейзер")
        elif self.__class__.__name__ == other.__class__.__name__ == 'Air':
            Elements().__call__("ветер")
        elif len({self.__class__.__name__, other.__class__.__name__} & {'Air', 'Fire'}) == 2:
            Elements().__call__("энергия")
        elif len({self.__class__.__name__, other.__class__.__name__} & {'Air', 'Energy'}) == 2:
            Elements().__call__("буря")
        elif len({self.__class__.__name__, other.__class__.__name__} & {'Water', 'Energy'}) == 2:
            Elements().__call__("спирт")

    @abc.abstractmethod
    def __str__(self):
        print("main abstract class")


class Elements(Alchemy):
    def __str__(self):
        print("Элементы")

    def __call__(self, arg):
        if arg not in self.words:
            self.words.add(arg)
            print("Создается элемент:", end=' ')
            if arg == "пар":
                Par().__str__()
            elif arg == "гейзер":
                Geizer().__str__()
            elif arg == "ветер":
                Wind().__str__()
            elif arg == "энергия":
                Energy().__str__()
            elif arg == "буря":
                Burya().__str__()
            elif arg == "спирт":
                Spirt().__str__()
        else:
            print("Элемент уже был создан!")


class Fire(Elements):

    def __str__(self):
        print("огонь!")


class Air(Elements):
    def __str__(self):
        print("воздух!")


class Wind(Elements):
    def __str__(self):
        print("ветер!")


class Spirt(Elements):
    def __str__(self):
        print("спирт!")


class Water(Elements):
    def __str__(self):
        print("вода!")


class Burya(Elements):
    def __str__(self):
        print("буря!")


class Ground(Elements):
    def __str__(self):
        print("земля!")


class Energy(Elements):
    def __str__(self):
        print("энергия!")


class Geizer(Elements):
    def __str__(self):
        print("гейзер!")


class Par(Elements):
    def __str__(self):
        print("пар!")


class Animals(Alchemy):
    pass


class Materials(Alchemy):

    def hello(self):
        pass


class Food(Alchemy):

    def hello(self):
        pass


class Controller(Alchemy):
    def __init__(self):
        print("Начало игры!")
        self.start_game()

    def add_elems(self, elem1, elem2):
        if elem1 in self.words and elem2 in self.words:
            if len({elem1, elem2} & {'огонь', 'вода'}) == 2:
                Alchemy.__add__(Water(), Fire())
            elif len({elem1, elem2} & {'земля', 'пар'}) == 2:
                Alchemy.__add__(Ground(), Par())
            elif elem1 == elem2 == "воздух":
                Alchemy.__add__(Air(), Air())
            elif len({elem1, elem2} & {'воздух', 'огонь'}) == 2:
                Alchemy.__add__(Air(), Fire())
            elif len({elem1, elem2} & {'воздух', 'энергия'}) == 2:
                Alchemy.__add__(Air(), Energy())
            elif len({elem1, elem2} & {'вода', 'энергия'}) == 2:
                Alchemy.__add__(Water(), Energy())
            else:
                print("Элементы не сочетаются!")
        else:
            print("Вы выбрали несуществующий(-е) элемент(-ы), попробуйте снова!")

    def start_game(self):
        print("Сейчас доступно для сложения: ")
        print(self.words)
        elem1 = input("Введите певый элемент для сложения:")
        elem2 = input("Введите второй элемент для сложения:")
        if elem1 != 'q' or elem2 != 'q':
            self.add_elems(elem1, elem2)
            print()
            self.start_game()
        else:
            pass

    def __str__(self):
        pass


a = Controller()
