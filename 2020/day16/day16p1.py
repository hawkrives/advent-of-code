from pathlib import Path
from contextlib import contextmanager
import time
import typing
import sqlite3
from collections import namedtuple


Field = namedtuple('Field', ['name', 'range1', 'range2'])


@contextmanager
def timed():
    start = time.perf_counter()
    yield
    end = time.perf_counter()
    print(f"Runtime: {end - start:.3f}s")


def parse(datafile):
    with datafile.open('r', encoding='utf-8') as infile:
        group = []

        for line in infile:
            line = line.strip()

            if not line:
                yield group
                group = []
                continue

            group.append(line)

        yield group


def main():
    conn = sqlite3.connect('./day16p1.sqlite3', isolation_level=None)
    conn.row_factory = sqlite3.Row

    conn.execute('pragma foreign_keys = on;')

    conn.execute('''drop table if exists ticket''')
    conn.execute('''drop table if exists field''')

    conn.execute('''
        create table field (
            field_index int primary key,
            label text not null,
            range1start int not null,
            range1end int not null,
            range2start int not null,
            range2end int not null
        )
    ''')

    conn.execute('''
        create table ticket (
            ticket_id int not null,
            field_index int not null references field(field_index),
            value int not null
        )
    ''')

    datafile = Path('./sample.txt')
    # datafile = Path('./data.txt')

    groups = list(parse(datafile))
    fields, mine, nearby = groups

    # remove the headers
    mine = mine[1]
    nearby = nearby[1:]

    conn.execute('BEGIN;')

    for field_index, field in enumerate(fields):
        field_name, ranges = field.split(': ')
        range1, range2 = ranges.split(' or ')
        range1start, range1end = range1.split('-')
        range2start, range2end = range2.split('-')

        conn.execute('''
            INSERT INTO field (label, field_index, range1start, range1end, range2start, range2end)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (field_name, field_index, int(range1start), int(range1end), int(range2start), int(range2end)))

    for field_index, field_value in enumerate(mine.split(',')):
        conn.execute('''
            INSERT INTO ticket (ticket_id, field_index, value)
            VALUES (1, ?, ?)
        ''', (field_index, field_value))

    for ticket_id, ticket in enumerate(nearby):
        for field_index, field_value in enumerate(ticket.split(',')):
            conn.execute('''
                INSERT INTO ticket (ticket_id, field_index, value)
                VALUES (?, ?, ?)
            ''', (ticket_id + 10, field_index, field_value))

    conn.commit()


if __name__ == '__main__':
    with timed():
        main()
