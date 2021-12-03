mod p01;
mod p02;

const INPUT_DATA: &'static str = include_str!("../input.txt");
const EXAMPLE_DATA: &'static str = include_str!("../input.example.txt");

fn main() {
    println!("Part 1:");

    let expected = 150;
    let parsed = EXAMPLE_DATA
        .lines()
        .filter_map(|s| s.parse().ok())
        .collect::<Vec<_>>();
    let actual = p01::navigate(&parsed).location();
    let status = if expected == actual { "ok." } else { "error!" };
    println!("Sample: {} - expected {}, got {}", status, expected, actual);

    let expected = 1_746_616;
    let parsed = INPUT_DATA
        .lines()
        .filter_map(|s| s.parse().ok())
        .collect::<Vec<_>>();
    let actual = p01::navigate(&parsed).location();
    let status = if expected == actual { "ok." } else { "error!" };
    println!("Actual: {} - expected {}, got {}", status, expected, actual);

    println!();
    
    println!("Part 2:");

    let expected = 900;
    let parsed = EXAMPLE_DATA
        .lines()
        .filter_map(|s| s.parse().ok())
        .collect::<Vec<_>>();
    let actual = p02::navigate(&parsed).location();
    let status = if expected == actual { "ok." } else { "error!" };
    println!("Sample: {} - expected {}, got {}", status, expected, actual);

    let expected = 1_741_971_043;
    let parsed = INPUT_DATA
        .lines()
        .filter_map(|s| s.parse().ok())
        .collect::<Vec<_>>();
    let actual = p02::navigate(&parsed).location();
    let status = if expected == actual { "ok." } else { "error!" };
    println!("Sample: {} - expected {}, got {}", status, expected, actual);
}
