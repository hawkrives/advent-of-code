// use itertools::Itertools;

const DATA: &str = include_str!("./day01.txt");

pub(crate) fn main() -> anyhow::Result<()> {
    println!("Day 01:");
    println!(
        "    Part 1: How many calories is the elf with the most calories carrying? {}",
        part01(DATA)?
    );
    println!(
        "    Part 2: How many calories total are the three elves with the most calories carrying? {}",
        part02(DATA)?
    );

    Ok(())
}

fn parse(data: &str) -> anyhow::Result<Vec<u64>> {
    let lines = data
        .lines()
        .map(|v| v.trim().parse::<u64>().ok())
        .collect::<Vec<_>>();
    
    let groups = lines
        .split(|line| line.is_none())
        .map(|group| group.iter().map(|v| v.unwrap()).sum::<u64>())
        .collect::<Vec<_>>();

    Ok(groups)
}

fn part01(data: &str) -> anyhow::Result<u64> {
    Ok(parse(data)?.into_iter().max().unwrap())
}

fn part02(data: &str) -> anyhow::Result<u64> {
    let by_calories = {
        let mut x = parse(data)?;
        x.sort_unstable();
        x.reverse();
        x
    };

    Ok(by_calories.iter().take(3).sum())
}

#[cfg(test)]
mod test {
    use super::*;
    use pretty_assertions::assert_eq;

    const EXAMPLE: &str = r#"1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"#;

    #[test]
    fn test_parse() {
        assert_eq!(
            parse(EXAMPLE).unwrap(),
            vec![6000, 4000, 11000, 24000, 10000]
        );
    }

    #[test]
    fn part01_example() {
        assert_eq!(part01(EXAMPLE).unwrap(), 24_000);
    }

    #[test]
    fn part01_personalized() {
        assert_eq!(part01(DATA).unwrap(), 71_780);
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
