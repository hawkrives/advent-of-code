import pathlib
import dataclasses
import enum
import typing
import copy


PocketDimension = typing.Dict[int, typing.Dict[int, typing.Dict[int, bool]]]


def get_neighbors(dimension, *, z: int, x: int, y: int) -> typing.Iterator[bool]:
    for z_index in [z - 1, z, z + 1]:
        layer = dimension.get(z_index, dict())

        for x_index in [x - 1, x, x + 1]:
            row = layer.get(x_index, dict())

            for y_index in [y - 1, y, y + 1]:
                if z_index == z and x_index == x and y_index == y:
                    continue

                cell = row.get(y_index, False)
                yield cell


def count_active_cells(dimension) -> int:
    counter = 0

    for layer in dimension.values():
        for row in layer.values():
            for cell in row.values():
                if cell:
                    counter += 1

    return counter


def count_active_neighbors(dimension, *, z: int, x: int, y: int) -> int:
    return sum(1 for cell in get_neighbors(dimension, z=z, x=x, y=y) if cell is True)


def simulate(dimension: PocketDimension) -> PocketDimension:
    original = copy.deepcopy(dimension)

    dimension[min(dimension.keys()) - 2] = dict()
    dimension[min(dimension.keys()) - 1] = dict()
    dimension[max(dimension.keys()) + 1] = dict()
    dimension[max(dimension.keys()) + 2] = dict()

    dimension_size = [k for k in dimension.keys()]

    for z_index in dimension_size:
        layer = dimension.setdefault(z_index, dict())

        for x_index in dimension_size:
            row = layer.setdefault(x_index, dict())

            for y_index in dimension_size:
                cell = row.setdefault(y_index, False)

                active_neighbors = count_active_neighbors(original, z=z_index, x=x_index, y=y_index)

                if cell is False:
                    if active_neighbors == 3:
                        # becomes active
                        row[y_index] = True
                    else:
                        # remains inactive
                        row[y_index] = False
                elif cell is True:
                    if active_neighbors in (2, 3):
                        # remains active
                        row[y_index] = True
                    else:
                        # becomes inactive
                        row[y_index] = False

    return dimension


def parse(data: typing.Iterable[str]) -> PocketDimension:
    dimension = dict()

    for x, line in enumerate(data):
        row = dict()

        for y, cell in enumerate(line):
            if cell == "#":
                # active
                row[y] = True
            elif cell == ".":
                # inactive
                row[y] = False

        dimension[x] = row

    return {0: dimension}


def print_dimension(dimension: PocketDimension):
    for z, layer in sorted(dimension.items()):
        print(f'z={z}')
        for x, row in sorted(layer.items()):
            for y, col in sorted(row.items()):
                print('#' if col else '.', end='')

            print()
        print()


def main():
    # load the data
    dimension = parse([
        '.#.',
        '..#',
        '###',
    ])

    print('Before any cycles:')
    print_dimension(dimension)

    for cycle in range(1):
        print(f'After {cycle+1:,} cycle{"" if cycle+1 == 1 else "s"}')

        dimension = simulate(dimension)
        print_dimension(dimension)


    # print(count_active_neighbors(dimension, z=0, x=1, y=1))
    # print(count_active_neighbors(dimension, z=0, x=0, y=1))


if __name__ == "__main__":
    main()
