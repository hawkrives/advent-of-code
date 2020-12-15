import pathlib

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


def main(data):
    slope_r = 3
    slope_d = 1

    matrix = [row for row in data.splitlines() if row]

    tree_count = 0
    width = len(matrix[0])

    row, col = 0, 0
    while True:
        if matrix[row][col % width] == TREE:
            tree_count += 1

        row += slope_d
        col += slope_r

        if row >= len(matrix):
            break

    print(f'hit {tree_count} trees')


if __name__ == '__main__':
    with pathlib.Path('day03.txt').open('r', encoding='utf-8') as infile:
        content = infile.read()

    main(content)
