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

    datafile = Path('./sample2.txt')
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

    for ticket_id, ticket in enumerate(nearby):
        values = [int(n) for n in ticket.split(',')]

        is_ticket_valid = True
        for v in values:
            is_value_valid = False

            for f in all_fields:
                if (f[1][0] <= v <= f[1][1]):
                    is_value_valid = True

                if (f[2][0] <= v <= f[2][1]):
                    is_value_valid = True

                # if is_value_valid:
                #     print(f"{ticket} passed check {f}")

            is_ticket_valid = is_ticket_valid and is_value_valid

        if is_ticket_valid:
            nearby_tickets.append(values)

    # print(nearby_tickets)

    indices_to_fields = dict()

    for potential_field_index in range(len(all_fields)):
        for f in all_fields:
            if f[0] in indices_to_fields.values():
                continue

            f1 = f[1]
            f2 = f[2]

            all_tickets_valid_for_field = True
            for ticket in nearby_tickets:
                # is_ticket_valid = True
                v = ticket[potential_field_index]
                # for v in ticket:
                is_value_valid = (f1[0] <= v <= f1[1]) or (f2[0] <= v <= f2[1])

                # if not is_value_valid:
                #     print(f'{v} in {ticket} invalid for {f}')
                # is_ticket_valid = is_ticket_valid and is_value_valid
                all_tickets_valid_for_field = all_tickets_valid_for_field and is_value_valid

            if all_tickets_valid_for_field:
                indices_to_fields[potential_field_index] = f[0]

    print(indices_to_fields)

    mine_dict = dict()
    for field_index, field_value in enumerate(mine.split(',')):
        # print(field_index)
        mine_dict[indices_to_fields[field_index]] = field_value

    print(mine_dict)

    interesting_values = [v for k, v in mine_dict if k.startswith('departure')]
    print(interesting_values)
    print(product(interesting_values))


def product(iter):
    acc = 1
    for n in iter:
        acc *= n
    return acc


if __name__ == '__main__':
    with timed():
        main()
