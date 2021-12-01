# each group's answers are separated by blank lines
# and each person's answer is on a single line

from typing import Iterable, Iterator
from pathlib import Path
import sqlite3


def split_into_lines(text: Iterable[str]) -> Iterator[str]:
    for line in text:
        yield line.strip()


def split_into_groups(lines: Iterable[str]) -> Iterator[str]:
    lines = (l.strip() for l in lines)

    previous = None
    current_group = []

    for line in lines:
        if previous == '':
            # omit blank groups
            if current_group:
                yield current_group
            current_group = []

        # omit blank lines
        if line:
            current_group.append(line)

        previous = line

    # return the last one too
    yield current_group


if __name__ == '__main__':
    conn = sqlite3.connect('./day06.sqlite3')

    conn.execute('DROP TABLE IF EXISTS answer')
    conn.execute('''
        CREATE TABLE answer (
            group_id int,
            person_id text,
            question text
        )
    ''')
    conn.execute('''
        create index answer_group_question ON answer(group_id, question)
    ''')
    # conn.execute('''
    #     create index answer_group_question ON answer(group_id, question)
    # ''')

    sample = Path('./day06_sample.txt')
    data = Path('./day06.txt')
    with data.open('r', encoding='utf-8') as infile:
        groups = split_into_groups(split_into_lines(infile))
        groups = list(groups)

        with conn:
            for group_id, group in enumerate(groups):
                for person_id, person in enumerate(group):
                    for question in person:
                        conn.execute('''
                            INSERT INTO answer(group_id, person_id, question)
                            VALUES (?, ?, ?)
                        ''', [group_id, f"{group_id}-{person_id}", question])
