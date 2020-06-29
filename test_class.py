class Person:
    def __init__(self, name, age, sex):
        self.__name = name
        self.__age = age
        self.__sex = sex

    def eat(self):
        print(self.__name + " eats")

    def set_name(self, name):
        self.__name = name


class Child(Person):
    def __init__(self, name, age, sex, nickname):
        super().__init__(name, age, sex)
        self.nickname = nickname

    def eat(self):
        Person.eat(self)
        # super().eat()
        print(self.nickname + " eats")


a = Child("Tom", 8, 0, "Tommy")
b = Person("Mary", 25, 1)
a.eat()
b.eat()
