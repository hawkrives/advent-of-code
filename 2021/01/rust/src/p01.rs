pub fn analyze_measurements(measurements: &str) -> u64 {
    let measurements = measurements
        .split_ascii_whitespace()
        .filter_map(|m| m.parse::<u64>().ok())
        .collect::<Vec<_>>();

    let (first, remaining) = measurements.split_first().expect("no measurements found?");

    let mut prior = first;
    let mut increase_count: u64 = 0;
    for depth in remaining {
        if let std::cmp::Ordering::Greater = depth.cmp(prior) {
            increase_count += 1;
        }
        prior = depth;
    }

    return increase_count;
}
