mod p01;
mod p02;

const INPUT_DATA: &'static str = include_str!("../input.txt");
const EXAMPLE_DATA: &'static str = include_str!("../input.example.txt");

fn main() {
    println!("Part 1:");
    let sample_1 = p01::analyze_measurements(EXAMPLE_DATA);
    println!("Sample: expected {}, got {}", 7, sample_1);
    let actual_1 = p01::analyze_measurements(INPUT_DATA);
    println!("Actual: expected {}, got {}", 1692, actual_1);
    println!();

    println!("Part 2:");
    let sample_2 = p02::analyze_measurements(EXAMPLE_DATA);
    println!("Sample: expected {}, got {}", 5, sample_2);
    let actual_2 = p02::analyze_measurements(INPUT_DATA);
    println!("Actual: expected {}, got {}", 1724, actual_2);
}
