mod p01;
mod p02;

const INPUT_DATA: &'static str = include_str!("../input.txt");
const EXAMPLE_DATA: &'static str = include_str!("../input.example.txt");

fn main() {
    println!("Part 1:");
    println!("Sample: {}", p01::analyze_measurements(EXAMPLE_DATA));
    println!("Actual: {}", p01::analyze_measurements(INPUT_DATA));
    println!();
    println!("Part 2:");
    println!("Sample: {}", p02::analyze_measurements(EXAMPLE_DATA));
    println!("Actual: {}", p02::analyze_measurements(INPUT_DATA));
}
