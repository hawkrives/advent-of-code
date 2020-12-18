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
    all_fields = []
    nearby_tickets = []

    datafile = Path('./sample.txt')
    datafile = Path('./data.txt')

    groups = list(parse(datafile))
    fields, mine, nearby = groups

    # remove the headers
    mine = mine[1]
    nearby = nearby[1:]

    for field_index, field in enumerate(fields):
        field_name, ranges = field.split(': ')
        range1, range2 = ranges.split(' or ')
        range1start, range1end = range1.split('-')
        range2start, range2end = range2.split('-')

        all_fields.append((field_name, (int(range1start), int(range1end)), (int(range2start), int(range2end))))

    # values that are not valid for any field
    invalid_values = []

    for ticket_id, ticket in enumerate(nearby):
        values = [int(n) for n in ticket.split(',')]

        for v in values:
            valid = False

            for f in all_fields:
                if (f[1][0] <= v <= f[1][1]):
                    valid = True

                if (f[2][0] <= v <= f[2][1]):
                    valid = True

            if not valid:
                invalid_values.append(v)
                print(f"ticket {ticket}, value {v}: violates {f}")
                break

        # if valid:
        #     nearby_tickets.append(ticket)

    print(invalid_values)
    print(sum(invalid_values))


if __name__ == '__main__':
    with timed():
        main()
