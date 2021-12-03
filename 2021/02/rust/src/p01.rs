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
pub struct Location {
    pub depth: i64,
    pub horizontal: i64,
}

impl Location {
    pub fn location(&self) -> i64 {
        self.depth * self.horizontal
    }
}

impl PartialEq for Location {
    fn eq(&self, other: &Self) -> bool {
        self.location() == other.location()
    }
}

impl PartialOrd for Location {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        self.location().partial_cmp(&other.location())
    }
}

pub fn navigate(steps: &[Instruction]) -> Location {
    let mut location = Location {horizontal: 0, depth: 0};

    for step in steps {
        match step {
            Instruction::Up(n) => location.depth -= n,
            Instruction::Down(n) => location.depth += n,
            Instruction::Forward(n) => location.horizontal += n,
        }
    }

    location
}
