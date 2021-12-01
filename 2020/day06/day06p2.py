# each group's answers are separated by blank lines
# and each person's answer is on a single line

from typing import Iterable, Iterator, Collection, List
from pathlib import Path
import collections


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


def collect_unanimous_questions(group: List[str]) -> List[str]:
    questions = collections.Counter(''.join(p for p in group))

    print(questions)

    group_size = len(group)
    return [q for q, count in questions.items() if count == group_size]


if __name__ == '__main__':
    sample = Path('./day06_sample.txt')
    data = Path('./day06.txt')
    with data.open('r', encoding='utf-8') as infile:
        groups = split_into_groups(split_into_lines(infile))
        groups = list(groups)

    total_unanimous_questions_answered = 0

    for group in groups:
        unanimous_questions = collect_unanimous_questions(group)
        total_unanimous_questions_answered += len(unanimous_questions)

    print(total_unanimous_questions_answered)
