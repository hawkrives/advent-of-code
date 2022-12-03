use itertools::Itertools;
use num_format::{Locale, ToFormattedString};
use std::collections::BTreeSet;

const DATA: &str = include_str!("./day03.txt");

const EXAMPLE: &str = r#"vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"#;

#[derive(Debug, Clone, Copy, PartialEq, PartialOrd, Eq, Ord)]
struct Item(char);

impl Item {
    fn priority(self) -> u32 {
        match self.0 {
            'a'..='z' => self.0.to_digit(36).unwrap() - 9,
            'A'..='Z' => self.0.to_ascii_lowercase().to_digit(36).unwrap() - 9 + 26,
            _ => unreachable!(),
        }
    }
}

fn main() -> anyhow::Result<()> {
    println!(
        "Part 1 (example): {}",
        part1(EXAMPLE).to_formatted_string(&Locale::en)
    );
    println!("Part 1: {}", part1(DATA).to_formatted_string(&Locale::en));

    println!(
        "Part 2 (example): {}",
        part2(EXAMPLE).to_formatted_string(&Locale::en)
    );
    println!("Part 2: {}", part2(DATA).to_formatted_string(&Locale::en));
    Ok(())
}

fn part1(data: &str) -> u32 {
    let mut sum: u32 = 0;
    for line in data.lines() {
        let (a, b) = line.split_at(line.len() / 2);
        let a = BTreeSet::from_iter(a.chars().map(Item));
        let b = BTreeSet::from_iter(b.chars().map(Item));
        let common_items: BTreeSet<_> = a.intersection(&b).collect();
        sum += common_items.iter().map(|item| item.priority()).sum::<u32>();
    }
    sum
}

fn part2(data: &str) -> u32 {
    let mut sum: u32 = 0;
    let lines: Vec<_> = data.lines().collect();
    for chunks in lines.chunks_exact(3) {
        let a = BTreeSet::from_iter(chunks.first().unwrap().chars().map(Item));
        let b = BTreeSet::from_iter(chunks.get(1).unwrap().chars().map(Item));
        let c = BTreeSet::from_iter(chunks.get(2).unwrap().chars().map(Item));

        let a_and_b: BTreeSet<_> = a.intersection(&b).cloned().collect();
        let and_c: BTreeSet<_> = a_and_b.intersection(&c).cloned().collect();

        sum += and_c.iter().map(|item| item.priority()).sum::<u32>();
    }
    sum
}

#[cfg(test)]
mod test {
    use super::*;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_item_priority() {
        assert_eq!(Item('a').priority(), 1);
        assert_eq!(Item('p').priority(), 16);
        assert_eq!(Item('L').priority(), 38);
        assert_eq!(Item('P').priority(), 42);
        assert_eq!(Item('v').priority(), 22);
        assert_eq!(Item('t').priority(), 20);
        assert_eq!(Item('s').priority(), 19);
        assert_eq!(Item('Z').priority(), 52);
    }

    #[test]
    fn test_part1_example() {
        assert_eq!(part1(EXAMPLE), 157);
    }

    #[test]
    fn test_part1_data() {
        assert_eq!(part1(DATA), 7737);
    }

    #[test]
    fn test_part2_example() {
        assert_eq!(part2(EXAMPLE), 70);
    }
}
