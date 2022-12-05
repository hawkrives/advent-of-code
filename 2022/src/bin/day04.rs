#![allow(dead_code)]

use std::{fmt::Display, str::FromStr};

use anyhow::anyhow;

const DATA: &str = include_str!("./day04.txt");

const EXAMPLE: &str = r#"2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"#;

#[derive(Debug, Clone, PartialEq, Eq)]
struct Range {
    start: u32,
    end: u32,
}

impl Display for Range {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for _ in 0..=self.start {
            write!(f, ".")?;
        }
        for n in self.start..=self.end {
            write!(f, "{}", n % 10)?;
        }
        for _ in self.end..=100 {
            write!(f, ".")?;
        }
        Ok(())
    }
}

impl FromStr for Range {
    type Err = anyhow::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let Some((start, end)) = s.split_once('-') else {
            return Err(anyhow!("invalid range {s}"));
        };

        Ok(Range {
            start: start.parse()?,
            end: end.parse()?,
        })
    }
}

impl Range {
    fn overlapped(&self, other: &Range) -> bool {
        (other.start >= self.start && other.start <= self.end)
            && (other.end >= self.start && other.end <= self.end)
    }

    fn partial_overlap(&self, other: &Range) -> bool {
        (other.start >= self.start && other.start <= self.end)
            || (other.end >= self.start && other.end <= self.end)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct SectionAssignment(Range, Range);

impl Display for SectionAssignment {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        writeln!(
            f,
            "({}, {}) - ({}, {})",
            self.0.start, self.0.end, self.1.start, self.1.end
        )?;
        writeln!(f, "{}", self.0)?;
        writeln!(f, "{}", self.1)?;
        Ok(())
    }
}

impl FromStr for SectionAssignment {
    type Err = anyhow::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let Some((first, second)) = s.split_once(',') else {
            return Err(anyhow!("invalid section assignment {s}"));
        };

        Ok(SectionAssignment(first.parse()?, second.parse()?))
    }
}

impl SectionAssignment {
    fn overlapped(&self) -> bool {
        self.0.overlapped(&self.1) || self.1.overlapped(&self.0)
    }

    fn partial_overlap(&self) -> bool {
        self.0.partial_overlap(&self.1) || self.1.overlapped(&self.0)
    }
}

fn main() -> anyhow::Result<()> {
    println!("Part 1: {}", part1(EXAMPLE)?);
    println!("Part 1: {}", part1(DATA)?);

    println!("Part 2: {}", part2(EXAMPLE)?);
    println!("Part 2: {}", part2(DATA)?);
    Ok(())
}

fn part1(data: &str) -> anyhow::Result<usize> {
    let ranges = data
        .lines()
        .filter_map(|pair| pair.parse::<SectionAssignment>().ok())
        .collect::<Vec<_>>();

    Ok(ranges.iter().filter(|a| a.overlapped()).count())
}

fn part2(data: &str) -> anyhow::Result<usize> {
    let ranges = data
        .lines()
        .filter_map(|pair| pair.parse::<SectionAssignment>().ok())
        .collect::<Vec<_>>();

    Ok(ranges.iter().filter(|a| a.partial_overlap()).count())
}

#[cfg(test)]
mod test {
    use super::*;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_part1_example() {
        assert_eq!(part1(EXAMPLE).unwrap(), 2);
    }

    #[test]
    fn test_part1_data() {
        assert_eq!(part1(DATA).unwrap(), 657);
    }

    #[test]
    fn test_part2_example() {
        assert_eq!(part2(EXAMPLE).unwrap(), 70);
    }

    #[test]
    fn test_part2_data() {
        assert_eq!(part2(DATA).unwrap(), 938);
    }
}
