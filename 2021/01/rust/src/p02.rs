use itertools::izip;

pub fn analyze_measurements(measurements: &str) -> u64 {
    let measurements = measurements
        .split_ascii_whitespace()
        .filter_map(|m| m.parse::<u64>().ok())
        .collect::<Vec<_>>();

    let offset0 = measurements.iter();
    let mut offset1 = measurements.iter();
    offset1.next();
    let mut offset2 = measurements.iter();
    offset2.next();
    offset2.next();

    let mut combined = izip!(offset0, offset1, offset2);

    let first = combined.next().expect("no measurements found?");

    let mut prior = first.0 + first.1 + first.2;
    let mut increase_count: u64 = 0;
    for depth in combined {
        let summed_depth = depth.0 + depth.1 + depth.2;
        if let std::cmp::Ordering::Greater = summed_depth.cmp(&prior) {
            increase_count += 1;
        }
        prior = summed_depth;
    }

    return increase_count;
}
