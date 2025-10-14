import PIL
import os
from functools import reduce
import operator
from heapq import heappush, heappop


class Reduce:
   @staticmethod
   def factorial(x: int, y: int):
       a = reduce(lambda x, y: y * x, range(1, 6), 1)
       b = reduce(operator.mul, range(x, y))
       # c = (((((1 * 1) * 2) * 3) * 4) * 5)
       return a, b

   @staticmethod
   def various():
        _sum = lambda d: reduce(operator.add, d, 0)  # sum()

        f = str
        _map = lambda d: reduce(lambda x, y: x + [f(y)], d, [])  # map()

        is_prime = lambda n: all(n % j for j in range(2, int(n ** 0.5) + 1)) and n > 1
        _filter = lambda d: reduce(lambda x, y: x + [y] if is_prime(y) else x, d, [])  # filter(is_prime, range(10))

        _reversed = lambda d: reduce(lambda x, y: [y] + x, d, [])  # reversed(data)

        _min = lambda d: reduce(lambda x, y: x if x < y else y, d)  # min(data)

        _max = lambda d: reduce(lambda x, y: x if x > y else y, d)  # max(data)



class MediumUtils:

    # Boltons
    @staticmethod
    def im_remap(source = None):
        from boltons.iterutils import remap

        if source is None:
            source = {'x': 1, 'child': {'y': 2}}

        # source = {'x': 1, 'child': {'y': 2}}
        result = remap(source, visit=lambda path, key, value: (key.upper(), value))
        print(result)

        # {'X': 1, 'CHILD': {'Y': 2}}

    @staticmethod
    def do_pydash():
        import pydash

        people = [{'name': 'Ana'}, {'name': 'Dev'}, {'name': 'Jo'}]
        names = pydash.map_(people, 'name')

        print(names)
        # ['Ana', 'Dev', 'Jo']

    @staticmethod
    def do_funcy():
        from funcy import select

        stuff = {'a': 1, 'b': 0, 'c': 3}
        filtered = select(lambda item: item[1] > 1, stuff)

        print(filtered)
        # {'c': 3}

    @staticmethod
    def do_glom():
        from glom import glom

        input_data = {'meta': {'info': {'version': 3}}}
        version = glom(input_data, 'meta.info.version')

        print(version)
        # 3


    @staticmethod
    def do_furl():
        from furl import furl

        url = furl('https://endpoint.com/api')
        url.args['sort'] = 'desc'

        print(url.url)
        # https://endpoint.com/api?sort=desc

    @staticmethod
    def do_cachier():
        from cachier import cachier

        @cachier(stale_after=3600)
        def expensive():
            print("Running...")
            return 42

        expensive()
        expensive()  # uses cache

    @staticmethod
    def do_levenshtein_distance():
        import Levenshtein

        score = Levenshtein.distance("kitten", "sitting")
        print(score)
         # 3


    # world news api
    @staticmethod
    def world_news():
        # World News Fetcher
        # pip install requests
        import requests
        ApiKey = "4710850799214474b3bc727039cfe2dc"
        url = f"https://api.worldnewsapi.com/search-news?text=hurricane&api-key={ApiKey}"
        headers = {
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        print("News: ", response.json())



class PendulumUtil:
    # import library
    import pendulum

    dt = pendulum.datetime(2023, 1, 31)
    print(dt)

    # local() creates datetime instance with local timezone

    local = pendulum.local(2023, 1, 31)
    print("Local Time:", local)
    print("Local Time Zone:", local.timezone.name)

    # Printing UTC time
    utc = pendulum.now('UTC')
    print("Current UTC time:", utc)

    # Converting UTC timezone into Europe/Paris time

    europe = utc.in_timezone('Europe/Paris')
    print("Current time in Paris:", europe)

class TimerDecorator:
    @staticmethod
    def timer(func):
        import time
        def wrapper(*args, **kwargs):
            # start the timer
            start_time = time.time()
            # call the decorated function
            result = func(*args, **kwargs)
            # remeasure the time
            end_time = time.time()
            # compute the elapsed time and print it
            execution_time = end_time - start_time
            print(f"Execution time: {execution_time} seconds")
            # return the result of the decorated function execution
            return result

        # return reference to the wrapper function
        return wrapper

    @staticmethod
    @timer
    def train_model():
        import time
        print("Starting the model training function...")
        # simulate a function execution by pausing the program for 5 seconds
        time.sleep(5)
        print("Model training completed!")

    # train_model()

    #  simple decorator with args
    @staticmethod
    def debug(func):  # decorator
        def wrapper(*args, **kwargs):
            # print the fucntion name and arguments
            print(f"Calling {func.__name__} with args: {args} kwargs: {kwargs}")
            # call the function
            result = func(*args, **kwargs)
            # print the results
            print(f"{func.__name__} returned: {result}")
            return result

        return wrapper

    @staticmethod
    @debug
    def add_numbers(x, y):
        return x + y

    # add_numbers(7, y=5, )
    #        Output: Calling add_numbers with args: (7) kwargs: {'y': 5} \n add_numbers returned: 12

    # Exception handler decorator

    @staticmethod
    def exception_handler(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Handle the exception
                print(f"An exception occurred: {str(e)}")
                # Optionally, perform additional error handling or logging
                # Reraise the exception if needed

        return wrapper


    @staticmethod
    @exception_handler
    def divide(x, y):
        result = x / y
        return result

    # divide(10, 0)  # Output: An exception occurred: division by zero

    # validation decorator
    @staticmethod
    def validate_input(*validations):
        def decorator(func):
            def wrapper(*args, **kwargs):
                for i, val in enumerate(args):
                    if i < len(validations):
                        if not validations[i](val):
                            raise ValueError(f"Invalid argument: {val}")
                for key, val in kwargs.items():
                    if key in validations[len(args):]:
                        if not validations[len(args):][key](val):
                            raise ValueError(f"Invalid argument: {key}={val}")
                return func(*args, **kwargs)

            return wrapper

        return decorator


    @staticmethod
    @validate_input(lambda x: x > 0, lambda y: isinstance(y, str))
    def divide_and_print(x, message):
        print(message)
        return 1 / x

    # divide_and_print(5, "Hello!")  # Output: Hello! 1.0

    # retry decorator
    @staticmethod
    def retry(max_attempts, delay=1):
        import time
        def decorator(func):
            def wrapper(*args, **kwargs):
                attempts = 0
                while attempts < max_attempts:
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        attempts += 1
                        print(f"Attempt {attempts} failed: {e}")
                        time.sleep(delay)
                print(f"Function failed after {max_attempts} attempts")

            return wrapper
        return decorator


    @staticmethod
    @retry(max_attempts=3, delay=2)
    def fetch_data(url):
        print("Fetching the data..")
        # raise timeout error to simulate a server not responding..
        raise TimeoutError("Server is not responding.")

    # fetch_data("https://example.com/data")  # Retries 3 times with a 2-second delay between attempts


class ShortPath:
    graph = {
        "A": ["B", "C"],
        "B": ["A", "D"],
        "C": ["A", "D"],
        "D": ["B", "C", "E"],
        "E": ["D"]
    }
    source = "https://medium.com/@kanishks772/move-over-dijkstra-the-new-algorithm-that-just-rewrote-70-years-of-computer-science-d670696c440d"


    @classmethod
    def find_influential_nodes(cls, layer:list, distances: dict):
        pass

    @classmethod
    def partition_into_layers(cls, graph, source):
        pass

    @classmethod
    def relax_from_node(cls, node, distances):
        pass

    @classmethod
    def process_remaining_cluster(cls, layer, distances):
        pass

    @classmethod
    def dijkstra(cls, graph:dict, source):
        distances = {vertex: float('infinity') for vertex in graph}
        distances[source] = 0
        priority_queue = [(0, source)]
        visited = set()

        while priority_queue:
            current_distance, current_vertex = heappop(priority_queue)

            if current_vertex in visited:
                continue

            visited.add(current_vertex)

            for neighbor, weight in graph[current_vertex].items():
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heappush(priority_queue, (distance, neighbor))

        return distances

    @classmethod
    def new_shortest_path(cls, graph: dict, source):
        # Simplified conceptual version
        layers = cls.partition_into_layers(graph, source)
        distances = {source: 0}

        for layer in layers:
            # Use Bellman-Ford to identify influential nodes
            influential = cls.find_influential_nodes(layer, distances)

            # Process influential nodes first
            for node in influential:
                cls.relax_from_node(node, distances)

            # Handle remaining nodes without sorting
            cls.process_remaining_cluster(layer, distances)

        return distances


