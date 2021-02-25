from typing import List


class Car:
    def __init__(self, id: int, streets: List[int]):
        self.id = id
        self.streets = streets

        self.curr_index = 0

    def next_street(self) -> int:
        self.curr_index += 1
        return self.streets[self.curr_index]

    def __str__(self) -> str:
        return str(self.id) + ": [" + ", ".join([str(x) for x in self.streets]) + "]"

    def __repr__(self) -> str:
        return self.__str__()


class Street:
    def __init__(self, id: int, int_start: int, int_end: int, length: int):
        self.id = id
        self.int_start = int_start
        self.int_end = int_end
        self.length = length

    def __str__(self) -> str:
        return (
            str(self.id)
            + " ("
            + str(self.int_start)
            + ", "
            + str(self.int_end)
            + "): "
            + str(self.length)
        )

    def __repr__(self) -> str:
        return self.__str__()


class Intersection:
    def __init__(self, id: int):
        self.id = id
        self.incoming: List[int] = []
        self.outgoing: List[int] = []

    def add_incoming(self, i: int):
        self.incoming.append(i)

    def add_outgoing(self, i: int):
        self.outgoing.append(i)

    def __str__(self) -> str:
        return (
            str(self.id)
            + ": ["
            + ", ".join(str(x) for x in self.incoming)
            + "]: ["
            + ", ".join(str(x) for x in self.outgoing)
            + "]"
        )

    def __repr__(self) -> str:
        return self.__str__()


def main(path: str) -> None:
    with open(path) as file:
        lines = file.read().strip().split("\n")
        D, I, S, V, F = [int(x) for x in lines[0].split(" ")]

        streets: List[Street] = []
        streets_dict = {}
        for i, line in enumerate(lines[1 : S + 1]):
            street_data = line.split(" ")
            B = int(street_data[0])
            E = int(street_data[1])
            name = street_data[2]
            L = int(street_data[3])
            street = Street(i, B, E, L)
            streets_dict[name] = i
            streets.append(street)

        cars: List[Car] = []
        for i, line in enumerate(lines[S + 1 : S + V + 1]):
            car_streets = [streets_dict[x] for x in line.split(" ")[1:]]
            car = Car(i, car_streets)
            cars.append(car)

        intersections: List[Intersection] = [Intersection(i) for i in range(I)]
        for street in streets:
            intersections[street.int_start].add_outgoing(street.id)
            intersections[street.int_end].add_incoming(street.id)

    print("Time Limit:", D)
    print("Car Bonus:", F)

    print("Streets")
    print(streets)

    print("Cars")
    print(cars)

    print("Intersections")
    print(intersections)


main("data/a.txt")
