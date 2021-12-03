use std::str::FromStr;

pub enum Instruction {
    Forward(i64),
    Down(i64),
    Up(i64),
}

pub struct InvalidCommandStr;

impl FromStr for Instruction {
    type Err = InvalidCommandStr;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.split_ascii_whitespace().collect::<Vec<_>>().as_slice() {
            [command, amount] => {
                let amount = match amount.parse() {
                    Ok(n) => n,
                    Err(_) => return Err(InvalidCommandStr),
                };
                match *command {
                    "forward" => Ok(Instruction::Forward(amount)),
                    "down" => Ok(Instruction::Down(amount)),
                    "up" => Ok(Instruction::Up(amount)),
                    _ => Err(InvalidCommandStr),
                }
            }
            _ => Err(InvalidCommandStr),
        }
    }
}

#[derive(Debug)]
pub struct Position {
    pub depth: i64,
    pub horizontal: i64,
    pub aim: i64,
}

impl Position {
    pub fn location(&self) -> i64 {
        self.depth * self.horizontal
    }
}

impl PartialEq for Position {
    fn eq(&self, other: &Self) -> bool {
        self.location() == other.location()
    }
}

impl PartialOrd for Position {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        self.location().partial_cmp(&other.location())
    }
}

pub fn navigate(steps: &[Instruction]) -> Position {
    let mut location = Position {
        horizontal: 0,
        depth: 0,
        aim: 0,
    };

    for step in steps {
        match step {
            Instruction::Up(n) => location.aim -= n,
            Instruction::Down(n) => location.aim += n,
            Instruction::Forward(n) => {
                location.horizontal += n;
                location.depth += location.aim * n;
            },
        }
    }

    location
}
