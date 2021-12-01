import sqlite3
import pathlib
from typing import List, Dict, Iterable


def init_db(conn: sqlite3.Connection):
    conn.execute('drop table if exists passports')
    conn.execute('''
        create table passports (
            byr text,
            iyr text,
            eyr text,
            hgt text,
            hcl text,
            ecl text,
            pid text,
            cid text
        )
    ''')


def parse_passports(buffer: Iterable[str]) -> List[Dict[str, str]]:
    blank_passport = dict(byr=None, iyr=None, eyr=None, hgt=None, hcl=None, ecl=None, pid=None, cid=None)
    current_passport = dict(**blank_passport)

    previous_line = None
    for line in buffer:
        line = line.strip()

        if previous_line == "":
            if current_passport:
                yield current_passport

            current_passport = dict(**blank_passport)

        for kv_pair in line.split():
            key, value = kv_pair.split(':')
            current_passport[key] = value

        previous_line = line

    yield current_passport


def insert_passports(conn: sqlite3.Connection, passports: List[Dict[str, str]]):
    with conn:
        conn.execute('DELETE FROM passports')

        for passport in passports:
            conn.execute('''
                INSERT INTO passports (byr, iyr, eyr, hgt, hcl, ecl, pid, cid) 
                VALUES (:byr, :iyr, :eyr, :hgt, :hcl, :ecl, :pid, :cid) 
            ''', passport)


def main():
    conn = sqlite3.connect('day04p1.sqlite3')
    init_db(conn)

    sample = pathlib.Path('day04_sample.txt')
    drew_data = pathlib.Path('day04_drew.txt')
    data = pathlib.Path('day04.txt')

    with data.open('r', encoding='utf-8') as infile:
        passports = parse_passports(infile)
        insert_passports(conn, passports)


if __name__ == '__main__':
    main()
