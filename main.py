import math
from typing import Dict, List
from collections import defaultdict


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


def get_intersection_throughput(
    streets: List[Street], cars: List[Car], intersections: List[Intersection], n: int
) -> Dict[int, Dict[int, int]]:
    int_counts: Dict[int, int] = defaultdict(int)
    int_street_counts: Dict[int, Dict[int, int]] = defaultdict(lambda: defaultdict(int))

    for car in cars:
        for street in car.streets:
            street_obj = streets[street]
            int_counts[street_obj.int_end] += 1
            int_street_counts[street_obj.int_end][street] += 1

    int_street_counts = {
        i: {k: math.ceil(n * v / int_counts[i]) for k, v in street_counts.items()}
        for i, street_counts in int_street_counts.items()
    }

    return int_street_counts


def main(path_in: str, path_out: str) -> None:
    # FILE READ
    with open(path_in) as file:
        lines = file.read().strip().split("\n")
        D, I, S, V, F = [int(x) for x in lines[0].split(" ")]

        streets: List[Street] = []
        streets_dict = {}
        streets_dict_inv = {}
        for i, line in enumerate(lines[1 : S + 1]):
            street_data = line.split(" ")
            B = int(street_data[0])
            E = int(street_data[1])
            name = street_data[2]
            L = int(street_data[3])
            street = Street(i, B, E, L)
            streets_dict[name] = i
            streets_dict_inv[i] = name
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

    """
    print("Time Limit:", D)
    print("Car Bonus:", F)

    print("Streets")
    print(streets)

    print("Cars")
    print(cars)

    print("Intersections")
    print(intersections)
    """

    int_street_counts = get_intersection_throughput(streets, cars, intersections, 5)

    # FILE WRITE
    with open(path_out, "w") as file:
        file.write(str(len(int_street_counts.keys())) + "\n")
        for i, int_streets in int_street_counts.items():
            file.write(str(i) + "\n")
            file.write(str(len(int_streets.keys())) + "\n")
            for j, weight in int_streets.items():
                file.write(streets_dict_inv[j] + " " + str(weight) + "\n")


main("data/a.txt", "output/a.txt")
main("data/b.txt", "output/b.txt")
main("data/c.txt", "output/c.txt")
main("data/d.txt", "output/d.txt")
main("data/e.txt", "output/e.txt")
main("data/f.txt", "output/f.txt")
