# each group's answers are separated by blank lines
# and each person's answer is on a single line

from typing import Iterable, Iterator, Collection
from pathlib import Path


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


def collect_unique_questions(group: Collection[str]) -> int:
    unique_questions = set()

    for person in group:
        for answer in person:
            unique_questions.add(answer)

    return unique_questions


if __name__ == '__main__':
    sample = Path('./day06_sample.txt')
    data = Path('./day06.txt')
    with data.open('r', encoding='utf-8') as infile:
        groups = split_into_groups(split_into_lines(infile))
        groups = list(groups)

    total_distinct_questions_answered = 0

    for group in groups:
        answered_questions = collect_unique_questions(group)
        total_distinct_questions_answered += len(answered_questions)

    print(total_distinct_questions_answered)
