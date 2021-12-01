pub fn analyze_measurements(measurements: &str) -> usize {
    let measurements = measurements
        .split_ascii_whitespace()
        .filter_map(|m| m.parse::<u64>().ok())
        .collect::<Vec<_>>();

    let m2 = measurements
        .windows(3)
        .map(|set| set.iter().sum::<u64>())
        .collect::<Vec<_>>();

    m2.windows(2)
        .filter(|pair| match pair {
            [a, b] => a < b,
            _ => panic!("expected a two-element array"),
        })
        .count()
}
