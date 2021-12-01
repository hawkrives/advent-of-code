use itertools::Itertools;

pub fn analyze_measurements(measurements: &str) -> usize {
    measurements
        .split_ascii_whitespace()
        .filter_map(|m| m.parse::<u64>().ok())
        // group into 3-tuples
        .tuple_windows::<(_, _, _)>()
        // and sum each 3-tuple
        .map(|(a, b, c)| a + b + c)
        // now group those summed 3-tuples into 2-tuples,
        .tuple_windows::<(_, _)>()
        // and count only the ones that directly increase in size
        .filter(|(a, b)| a < b)
        .count()
}
