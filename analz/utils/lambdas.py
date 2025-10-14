from functools import reduce

class Lambdas:
    @staticmethod
    def simple1(a, b):
        sum = lambda a, b: a + b
        print(sum(5, 3))

        # lambda as filter func

        numbers = [1, 2, 3, 4, 5, 6]
        even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
        print(even_numbers)
        # Output: [2, 4, 6]

        # lambdas with map
        numbers2 = [1, 2, 3, 4, 5]
        squared_numbers = list(map(lambda x: x ** 2, numbers2))
        print(squared_numbers)

        # Output: [1, 4, 9, 16, 25]

        #  lambdas with reduce (functool)

        numbers3 = [1, 2, 3, 4, 5]
        sum3 = reduce(lambda x, y: x + y, numbers3)
        print(sum3)
    @staticmethod
    def lambdas_listcomp():
        # list comprension with lambdas
        numbers = [1, 2, 3, 4, 5]
        squared = [(lambda x: x ** 2)(x) for x in numbers]
        print(squared)

        # Output: [1, 4, 9, 16, 25]
    @staticmethod
    def lambdas_sort_dic():

        # Sorting a list of dictionaries by a specific key
        people = [{'name': 'John', 'age': 45}, {'name': 'Diane', 'age': 35}]
        sorted_people = sorted(people, key=lambda x: x['age'])
        print(sorted_people)

        # Output: [{'name': 'Diane', 'age': 35}, {'name': 'John', 'age': 45}]

    @staticmethod
    def lambdas_nested():
        # A lambda function that returns another lambda function
        make_incrementor = lambda n: lambda x: x + n
        add_five = make_incrementor(5)
        print(add_five(10))

        # Output: 15

    @staticmethod
    def lambdas_decorator():
        decorator = lambda func: lambda *args, **kwargs: func(*args, **kwargs)

        @decorator
        def greet(name):
            return f"Hello, {name}!"

        print(greet("World"))



