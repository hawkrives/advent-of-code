import pathlib
from typing import List

sample = '''
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
'''

TREE = '#'
OPEN = '.'


def run_slope(data: List[str], *, move_right: int, move_down: int):
    tree_count = 0
    width = len(data[0])

    row, col = 0, 0
    while True:
        if data[row][col % width] == TREE:
            tree_count += 1

        row += move_down
        col += move_right

        if row >= len(data):
            break

    return tree_count


def main(data: str) -> None:
    matrix = [row for row in data.splitlines() if row]

    total_trees_product = 1

    paths = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    for i, (right, down) in enumerate(paths):
        path_result = run_slope(matrix, move_right=right, move_down=down)
        print(f"path {i+1}: hit {path_result} trees")
        total_trees_product *= path_result

    print(f"product of all trees hit: {total_trees_product}")


if __name__ == '__main__':
    with pathlib.Path('day03.txt').open('r', encoding='utf-8') as infile:
        content = infile.read()

    main(content)
