use itertools::Itertools;

pub fn analyze_measurements(measurements: &str) -> usize {
    measurements
        .split_ascii_whitespace()
        .filter_map(|m| m.parse::<u64>().ok())
        // group into 2-tuples,
        .tuple_windows::<(_, _)>()
        // and count only the ones that directly increase in size
        .filter(|(a, b)| a < b)
        .count()
}
