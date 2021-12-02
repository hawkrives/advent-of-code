mod p01;
mod p02;

const INPUT_DATA: &'static str = include_str!("../input.txt");
const EXAMPLE_DATA: &'static str = include_str!("../input.example.txt");

fn main() {
    println!("Part 1:");

    let expected = 7;
    let actual = p01::analyze_measurements(EXAMPLE_DATA);
    let status = if expected == actual { "ok." } else { "error!" };
    println!("Sample: {} - expected {}, got {}", status, expected, actual);

    let expected = 1692;
    let actual = p01::analyze_measurements(INPUT_DATA);
    let status = if expected == actual { "ok." } else { "error!" };
    println!("Actual: {} - expected {}, got {}", status, expected, actual);

    println!();

    println!("Part 2:");
    let expected = 5;
    let actual = p02::analyze_measurements(EXAMPLE_DATA);
    let status = if expected == actual { "ok." } else { "error!" };
    println!("Sample: {} - expected {}, got {}", status, expected, actual);

    let expected = 1724;
    let actual = p02::analyze_measurements(INPUT_DATA);
    let status = if expected == actual { "ok." } else { "error!" };
    println!("Actual: {} - expected {}, got {}", status, expected, actual);
}
