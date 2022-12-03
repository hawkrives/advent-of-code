//! The Elves begin to set up camp on the beach. To decide whose tent gets
//! to be closest to the snack storage, a giant Rock Paper Scissors tournament
//! is already in progress.
//!
//! Rock Paper Scissors is a game between two players. Each game contains many
//! rounds; in each round, the players each simultaneously choose one of Rock,
//! Paper, or Scissors using a hand shape. Then, a winner for that round is
//! selected: Rock defeats Scissors, Scissors defeats Paper, and Paper defeats
//! Rock. If both players choose the same shape, the round instead ends in a draw.
//!
//! Appreciative of your help yesterday, one Elf gives you an *encrypted strategy
//! guide* (your puzzle input) that they say will be sure to help you win. "The
//! first column is what your opponent is going to play: `A` for Rock, `B` for
//! Paper, and `C` for Scissors. The second column--" Suddenly, the Elf is called
//! away to help with someone's tent.
//!
//! The second column, you reason, must be what you should play in response:` X`
//! for Rock, `Y` for Paper, and `Z` for Scissors. Winning every time would be
//! suspicious, so the responses must have been carefully chosen.
//!
//! The winner of the whole tournament is the player with the highest score.
//! Your *total score* is the sum of your scores for each round. The score for a
//! single round is the score for the *shape you selected* (1 for Rock, 2 for
//! Paper, and 3 for Scissors) plus the score for the *outcome of the round* (0
//! if you lost, 3 if the round was a draw, and 6 if you won).
//!
//! Since you can't be sure if the Elf is trying to help you or trick you, you
//! should calculate the score you would get if you were to follow the strategy
//! guide.
//!
//! For example, suppose you were given the following strategy guide:
//!
//! ```
//! A Y
//! B X
//! C Z
//! ```
//!
//! This strategy guide predicts and recommends the following:
//!
//! - In the first round, your opponent will choose Rock (`A`), and you should
//!   choose Paper (`Y`). This ends in a win for you with a score of **8** (2
//!   because you chose Paper + 6 because you won).
//! - In the second round, your opponent will choose Paper (`B`), and you should
//!   choose Rock (`X`). This ends in a loss for you with a score of **1** (1 + 0).
//! - The third round is a draw with both players choosing Scissors, giving you
//!   a score of 3 + 3 = **6**.
//!
//! In this example, if you were to follow the strategy guide, you would get a
//! total score of *15* (8 + 1 + 6).
//!
//! *What would your total score be if everything goes exactly according to your
//! strategy guide?*

#![allow(dead_code)]

use std::str::FromStr;

use anyhow::anyhow;
use itertools::Itertools;
use num_format::{Locale, ToFormattedString};

const DATA: &str = include_str!("./day02.txt");

pub(crate) fn main() -> anyhow::Result<()> {
    println!("Day 02:");
    // let data = EXAMPLE;
    let data = DATA;
    println!("    Part 2: What would your total score be if everything goes exactly according to your strategy guide?");
    println!(
        "Current output: {}",
        part02(data)?.to_formatted_string(&Locale::en)
    );

    Ok(())
}

#[derive(Debug, PartialEq, Eq, Copy, Clone)]
enum Move {
    Rock,
    Paper,
    Scissors,
}

impl Move {
    const ALL_MOVES: [Move; 3] = [Move::Rock, Move::Paper, Move::Scissors];

    fn winning_move(self) -> Self {
        Self::ALL_MOVES
            .iter()
            .copied()
            .find(|m| m.beats(self))
            .expect("at least one move beats us")
    }

    fn losing_move(self) -> Self {
        Self::ALL_MOVES
            .iter()
            .copied()
            .find(|&m| self.beats(m))
            .expect("at least one move beats us")
    }

    fn drawing_move(self) -> Self {
        self
    }

    /// How many points do we get for picking that move?
    fn inherent_points(self) -> usize {
        match self {
            Move::Rock => 1,
            Move::Paper => 2,
            Move::Scissors => 3,
        }
    }

    fn beats(self, other: Self) -> bool {
        matches!(
            (self, other),
            (Self::Rock, Self::Scissors)
                | (Self::Paper, Self::Rock)
                | (Self::Scissors, Self::Paper)
        )
    }

    fn outcome(self, theirs: Self) -> Outcome {
        if self.beats(theirs) {
            Outcome::Win
        } else if theirs.beats(self) {
            Outcome::Loss
        } else {
            Outcome::Draw
        }
    }
}

impl FromStr for Move {
    type Err = anyhow::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "A" => Ok(Move::Rock),
            "B" => Ok(Move::Paper),
            "C" => Ok(Move::Scissors),
            _ => Err(anyhow!("invalid move: {s}")),
        }
    }
}

#[derive(Debug, PartialEq, Eq, Copy, Clone)]
enum Outcome {
    Loss,
    Draw,
    Win,
}

impl FromStr for Outcome {
    type Err = anyhow::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "X" => Ok(Outcome::Loss),
            "Y" => Ok(Outcome::Draw),
            "Z" => Ok(Outcome::Win),
            _ => Err(anyhow!("invalid outcome: {s}")),
        }
    }
}

impl Outcome {
    fn inherent_points(self) -> usize {
        match self {
            Outcome::Win => 6,
            Outcome::Draw => 3,
            Outcome::Loss => 0,
        }
    }

    fn matching_move(self, theirs: Move) -> Move {
        match self {
            Outcome::Win => theirs.winning_move(),
            Outcome::Draw => theirs.drawing_move(),
            Outcome::Loss => theirs.losing_move(),
        }
    }
}

#[derive(Debug, PartialEq, Eq, Copy, Clone)]
struct Round {
    theirs: Move,
    ours: Move,
}

impl FromStr for Round {
    type Err = anyhow::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let Some((theirs, outcome)) = s.split_whitespace().collect_tuple() else {
            return Err(anyhow!("invalid round {}", s));
        };

        let theirs: Move = theirs.parse()?;
        let outcome: Outcome = outcome.parse()?;
        let ours: Move = outcome.matching_move(theirs);

        Ok(Round { theirs, ours })
    }
}

impl Round {
    fn outcome(self) -> Outcome {
        self.ours.outcome(self.theirs)
    }

    fn our_score(self) -> usize {
        self.ours.inherent_points() + self.outcome().inherent_points()
    }
}

fn parse(data: &str) -> anyhow::Result<Vec<Round>> {
    let lines: Vec<_> = data.lines().collect();
    let filtered: Vec<_> = lines
        .iter()
        .filter_map(|l| match l.trim() {
            "" => None,
            s => Some(s),
        })
        .collect();

    filtered.iter().map(|l| l.parse()).collect()
}

fn part02(data: &str) -> anyhow::Result<usize> {
    Ok(parse(data)?.iter().map(|r| r.our_score()).sum())
}

const EXAMPLE: &str = r#"
A Y
B X
C Z
"#;

#[cfg(test)]
mod test {
    use super::*;
    use pretty_assertions::assert_eq;

    impl Move {
        fn a() -> Self {
            "A".parse().unwrap()
        }
        fn b() -> Self {
            "B".parse().unwrap()
        }
        fn c() -> Self {
            "C".parse().unwrap()
        }
    }

    #[test]
    fn test_parse() {
        let (a, b, c) = (Move::a(), Move::b(), Move::c());

        let actual = parse(EXAMPLE).unwrap();
        let expected = vec![
            Round { theirs: a, ours: a },
            Round { theirs: b, ours: a },
            Round { theirs: c, ours: a },
        ];

        assert_eq!(actual, expected);
    }

    #[test]
    fn test_judge() {
        let (a, b, c) = (Move::a(), Move::b(), Move::c());

        assert_eq!(Round { theirs: a, ours: a }.outcome(), Outcome::Draw);
        assert_eq!(Round { theirs: b, ours: a }.outcome(), Outcome::Loss);
        assert_eq!(Round { theirs: c, ours: a }.outcome(), Outcome::Win);
    }

    #[test]
    fn test_score() {
        let (a, b, c) = (Move::a(), Move::b(), Move::c());

        assert_eq!(Round { theirs: a, ours: a }.our_score(), 4);
        assert_eq!(Round { theirs: b, ours: b }.our_score(), 1);
        assert_eq!(Round { theirs: c, ours: c }.our_score(), 7);
    }

    #[test]
    fn part02_example() {
        assert_eq!(part02(EXAMPLE).unwrap(), 45_000);
    }

    #[test]
    fn part02_personalized() {
        assert_eq!(part02(DATA).unwrap(), 212_489);
    }
}
