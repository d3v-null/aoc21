fn calc_pos(movements: &str) -> (i32, i32) {
    let mut pos = (0, 0);
    for line in movements.lines() {
        let (dir, dist) = line.split_once(' ').unwrap();
        let val: i32 = dist.parse().unwrap();
        match dir {
            "forward" => pos.0 += val,
            "up" => pos.1 -= val,
            "down" => pos.1 += val,
            _ => unreachable!()
        }
    }
    pos
}

fn calc_pos2(movements: &str) -> (i32, i32) {
    // aim, pos, depth
    let mut pos = (0, 0, 0);
    for line in movements.lines() {
        let (dir, dist) = line.split_once(' ').unwrap();
        let val: i32 = dist.parse().unwrap();
        match dir {
            "up" => pos.0 -= val,
            "down" => pos.0 += val,
            "forward" => {
                pos.1 += val;
                pos.2 += val * pos.0
            },
            _ => unreachable!()
        }
    }
    (pos.1, pos.2)
}

/// Get the position products for part one and two given movements.
fn calc_pos_combined(movements: &str) -> (i32, i32) {
    let mut pos = (0, 0, 0, 0); // (pos, depth p1, depth p2, aim)
    movements.lines().for_each(|line| {
        let (dir, dist_) = line.split_once(' ').unwrap();
        let dist = dist_.parse::<i32>().unwrap();
        match dir {
            "up" => { pos.1 -= dist; pos.3 -= dist },
            "down" => { pos.1 += dist; pos.3 += dist },
            "forward" => { pos.0 += dist; pos.2 += dist * pos.3 },
            _ => unreachable!()
        }
    });
    (pos.0 * pos.1, pos.0 * pos.2)
}

fn main() {
    let input1="forward 2\ndown 4\ndown 1\ndown 4\nforward 3\ndown 6\ndown 5\nforward 3\nforward 8\ndown 2\ndown 3\nup 8\ndown 5\nup 7\ndown 7\nforward 5\nup 2\ndown 6\nforward 7\nforward 1\nforward 2\nforward 7\nup 7\nforward 6\ndown 3\ndown 1\nup 9\ndown 2\nup 1\ndown 1\nup 6\nforward 6\ndown 7\nforward 6\nup 1\ndown 6\nforward 2\nup 7\nforward 4\nforward 8\nforward 7\ndown 7\nforward 8\ndown 1\ndown 6\ndown 7\nforward 4\ndown 3\nup 7\ndown 5\ndown 9\nup 8\nup 4\ndown 2\ndown 3\nup 7\nforward 6\nforward 6\nforward 8\nforward 2\nup 5\ndown 8\ndown 3\ndown 3\ndown 4\ndown 9\ndown 6\nup 6\nforward 4\ndown 6\nforward 3\nforward 3\ndown 4\ndown 8\ndown 2\nup 5\nup 5\nforward 3\nforward 5\ndown 7\nforward 6\nforward 9\nforward 8\nforward 2\ndown 3\ndown 3\ndown 7\ndown 1\ndown 1\ndown 1\ndown 2\ndown 8\ndown 6\nforward 6\nup 1\nup 6\ndown 7\ndown 1\nforward 1\nup 2\nup 8\nup 8\nforward 2\ndown 1\ndown 8\ndown 7\ndown 1\nforward 1\ndown 9\nup 3\ndown 3\nforward 2\ndown 3\nup 6\ndown 2\nforward 7\ndown 9\ndown 6\ndown 1\nforward 6\ndown 4\ndown 1\ndown 3\nforward 3\ndown 5\nforward 9\ndown 5\ndown 7\nup 8\nforward 8\nforward 8\ndown 6\ndown 1\nforward 8\ndown 4\nup 4\nup 4\nup 2\nforward 2\nforward 2\ndown 1\nup 8\ndown 1\ndown 7\nforward 5\ndown 9\ndown 2\nup 3\ndown 1\ndown 5\nforward 6\ndown 7\nup 3\nforward 7\ndown 4\ndown 3\nforward 4\nup 8\ndown 4\nforward 4\nforward 2\nforward 5\ndown 5\nup 2\nforward 4\ndown 4\nforward 6\ndown 4\nforward 1\ndown 5\nforward 2\nforward 2\ndown 8\nforward 4\nforward 7\ndown 3\nup 3\nforward 2\nforward 6\nforward 8\ndown 2\nforward 4\ndown 2\nup 9\ndown 9\ndown 2\nforward 5\nup 4\nforward 2\ndown 2\ndown 3\nforward 1\ndown 2\nforward 8\nforward 8\ndown 4\nforward 6\ndown 3\ndown 3\ndown 5\nforward 8\nforward 4\nforward 1\nup 4\nup 2\nforward 8\ndown 8\nforward 2\nforward 6\nup 1\nup 5\nforward 2\nforward 4\nforward 7\nforward 8\nforward 2\ndown 3\ndown 1\ndown 9\ndown 6\nup 5\nup 6\nforward 6\ndown 3\ndown 2\ndown 1\nforward 5\nforward 2\nforward 7\ndown 8\ndown 7\nforward 7\nup 8\nforward 7\ndown 1\nup 4\nforward 9\nforward 4\nforward 1\ndown 3\ndown 9\ndown 7\nforward 1\ndown 3\nforward 3\ndown 4\ndown 7\nforward 4\nup 6\ndown 8\nup 1\nforward 6\nforward 1\ndown 7\ndown 8\nup 9\nup 4\ndown 3\ndown 7\nforward 8\nup 2\nup 6\nforward 8\ndown 1\nup 4\nup 4\nforward 8\ndown 2\ndown 4\ndown 3\nforward 5\ndown 8\nforward 1\ndown 2\nforward 9\nforward 3\nup 6\ndown 6\nforward 6\nforward 4\ndown 6\ndown 3\ndown 3\nforward 6\ndown 5\nup 4\ndown 9\ndown 3\ndown 6\nup 9\nforward 6\ndown 2\nforward 7\nup 8\ndown 3\ndown 7\ndown 9\nforward 6\ndown 1\nforward 2\ndown 1\ndown 3\ndown 3\nforward 5\nforward 2\nup 5\nforward 4\nup 7\ndown 9\nforward 7\nforward 3\ndown 6\nforward 1\ndown 1\nup 8\ndown 9\nup 3\ndown 7\nup 9\nforward 7\ndown 7\ndown 9\nforward 9\nforward 7\nup 9\ndown 7\ndown 2\ndown 7\nup 2\ndown 3\ndown 9\ndown 6\nforward 7\nforward 8\nforward 8\nforward 6\nforward 9\nforward 4\ndown 4\ndown 5\ndown 7\nforward 6\nforward 2\nforward 4\nforward 9\ndown 4\nforward 6\ndown 7\nup 1\ndown 7\nforward 9\nforward 7\ndown 4\ndown 3\nup 6\nforward 8\nforward 7\ndown 8\nforward 4\nup 6\nup 4\nforward 9\nforward 4\nforward 4\nforward 7\ndown 1\nup 6\nforward 8\nforward 3\nup 6\nforward 4\ndown 1\nup 2\nforward 1\ndown 5\nforward 5\nup 4\ndown 6\ndown 3\nup 8\nforward 9\ndown 2\nforward 4\nforward 8\ndown 9\nforward 5\nforward 2\ndown 9\ndown 8\nforward 8\ndown 7\nup 6\nforward 1\nup 9\nup 3\nforward 9\ndown 6\nforward 9\ndown 3\ndown 3\nforward 7\nforward 5\ndown 8\ndown 9\ndown 3\ndown 6\nup 8\ndown 9\nforward 8\ndown 7\ndown 5\ndown 1\nup 4\ndown 9\nforward 6\nforward 9\nup 6\nup 4\nforward 3\nforward 2\nforward 1\ndown 1\ndown 2\nforward 8\nup 6\nforward 5\nup 4\ndown 1\nforward 5\ndown 3\ndown 6\nup 7\nforward 2\nforward 6\nforward 7\nforward 4\ndown 5\ndown 4\nforward 4\ndown 6\nup 2\nup 2\nforward 7\nforward 3\ndown 8\ndown 1\ndown 8\nforward 7\nforward 7\nup 5\nforward 4\nup 8\ndown 9\ndown 4\ndown 4\nforward 5\ndown 1\nforward 2\ndown 6\nup 4\ndown 8\ndown 1\ndown 9\ndown 5\nup 5\nforward 4\ndown 2\ndown 8\ndown 4\nforward 4\nforward 5\ndown 8\nup 9\nforward 7\nforward 6\ndown 8\ndown 3\nup 7\ndown 7\nforward 2\nforward 5\nforward 7\ndown 9\nup 1\ndown 6\ndown 2\nforward 6\nforward 3\nforward 3\nup 9\nforward 4\ndown 5\ndown 7\nforward 8\nforward 6\nforward 5\ndown 9\ndown 5\ndown 1\ndown 7\nforward 9\nforward 8\ndown 2\ndown 4\ndown 1\nup 5\nup 5\nforward 5\ndown 3\ndown 1\nforward 8\nup 9\nup 3\ndown 3\nup 3\nup 5\nforward 8\ndown 3\nup 3\ndown 9\nup 6\nup 8\nforward 5\nup 2\ndown 6\nforward 3\ndown 2\ndown 4\nforward 9\nforward 6\nforward 3\nup 5\ndown 9\ndown 7\nforward 9\nforward 7\nforward 5\nup 5\nup 1\ndown 6\nforward 4\nforward 4\ndown 7\ndown 1\nup 3\nforward 6\nforward 4\ndown 1\nforward 5\nforward 3\nforward 1\nforward 3\nup 3\nup 9\ndown 7\ndown 4\nforward 8\ndown 8\ndown 3\nup 2\ndown 8\nforward 5\ndown 7\nforward 6\ndown 9\nup 5\nforward 4\ndown 2\nforward 6\ndown 8\ndown 7\nforward 8\nforward 5\ndown 2\nforward 7\nforward 5\nforward 7\ndown 8\nforward 5\ndown 8\ndown 6\ndown 7\ndown 9\nforward 9\ndown 6\nforward 8\nup 6\nup 1\ndown 5\nforward 1\nforward 7\nup 2\nup 5\nup 6\ndown 5\ndown 5\nforward 7\ndown 9\ndown 2\nforward 9\nforward 3\ndown 5\nup 2\nup 8\nforward 5\nforward 8\nup 1\nforward 3\nforward 1\nup 4\nforward 1\ndown 9\ndown 6\nforward 1\ndown 4\ndown 4\nforward 9\ndown 3\nup 6\ndown 3\nforward 6\nforward 6\ndown 3\nforward 6\ndown 3\ndown 1\nforward 3\ndown 7\nup 9\nforward 1\ndown 7\ndown 2\nup 8\ndown 1\ndown 9\ndown 1\ndown 4\ndown 6\ndown 3\ndown 7\ndown 2\ndown 9\ndown 2\nforward 4\nup 3\ndown 4\nup 4\ndown 1\nforward 5\nforward 7\ndown 7\nforward 9\nforward 6\ndown 8\nforward 6\nforward 7\nup 3\ndown 3\nup 6\nforward 7\nup 4\nforward 4\ndown 1\nup 8\nforward 7\ndown 2\nup 6\nforward 1\nforward 3\nup 9\nup 8\nup 5\nforward 7\nup 5\ndown 6\nforward 7\nforward 7\ndown 4\ndown 3\nforward 2\ndown 8\nup 9\nup 6\nforward 7\nforward 5\ndown 9\ndown 2\nup 5\ndown 3\ndown 3\nup 5\ndown 8\nforward 7\ndown 4\ndown 2\nup 9\ndown 5\ndown 8\ndown 5\ndown 6\nforward 9\ndown 3\ndown 8\nforward 3\ndown 1\ndown 9\nforward 1\ndown 3\nup 9\nup 3\nforward 8\nup 2\ndown 4\nup 5\nup 4\ndown 9\ndown 5\nup 3\nforward 2\ndown 8\nforward 8\nforward 7\nup 4\ndown 9\ndown 6\nup 1\nforward 9\nup 8\nforward 4\nup 3\ndown 4\nup 2\nup 7\ndown 2\nforward 3\ndown 8\ndown 9\nup 7\nup 8\nforward 3\nforward 1\nforward 7\nforward 5\nforward 9\nforward 2\nup 1\ndown 1\nup 4\nforward 1\nup 9\nforward 7\nforward 2\ndown 6\ndown 5\nforward 9\nforward 4\ndown 6\ndown 6\nup 8\ndown 3\nup 8\ndown 3\nforward 2\ndown 1\ndown 1\nforward 5\ndown 1\nforward 9\nup 8\nforward 2\ndown 5\nup 8\nup 8\nforward 8\nforward 8\nforward 3\nforward 2\nforward 8\nforward 9\nforward 8\nforward 6\nforward 4\nup 7\nforward 9\nforward 8\nup 7\nforward 6\nforward 9\nforward 8\ndown 7\nforward 9\ndown 4\ndown 1\nup 1\nup 9\nforward 2\ndown 6\ndown 2\ndown 8\ndown 6\nup 8\nforward 7\nup 9\nforward 5\nforward 4\nforward 8\nup 4\nforward 4\nup 6\nforward 7\nforward 1\nup 8\ndown 6\nforward 7\nforward 3\nforward 2\ndown 4\nforward 4\ndown 7\ndown 6\ndown 2\nup 3\nup 5\ndown 7\ndown 9\nup 8\ndown 1\nup 1\ndown 8\nup 8\nforward 8\ndown 6\ndown 1\ndown 6\nforward 3\ndown 9\ndown 5\nup 3\ndown 1\ndown 1\nforward 4\ndown 4\nup 3\nforward 8\nup 4\ndown 3\ndown 5\ndown 3\nforward 6\nforward 3\ndown 2\nforward 9\nforward 3\nforward 2\ndown 2\nforward 6\ndown 1\ndown 1\nforward 5\nforward 4\nforward 6\ndown 7\nforward 7\nforward 3\nforward 1\nup 3\ndown 6\nforward 1\nup 9\nforward 9\nforward 5\nforward 3\nforward 3\ndown 3\nup 8\nforward 5\nup 6\nforward 2\ndown 7\nforward 2\nforward 8\nforward 8\nforward 3\nup 9\ndown 5\ndown 3\nforward 7\nup 9\nforward 4\ndown 1\ndown 3\ndown 5\ndown 2\nforward 9\nup 6\ndown 3\ndown 7\ndown 3\nup 6\nforward 3\ndown 4\nforward 2\ndown 8\ndown 2\nforward 7\ndown 2\ndown 9\nforward 1\ndown 1\ndown 9\ndown 6\nforward 5\ndown 1\nup 1\nforward 5\nforward 4\nforward 9\ndown 3\nforward 3\nforward 5\ndown 9\nforward 9\ndown 8\ndown 2\nforward 1\nup 1\ndown 5\nforward 2\nup 9\nforward 9\nforward 7\nforward 9\nforward 3\ndown 7\nforward 2\ndown 4\nup 3\ndown 7\ndown 6\nforward 2\ndown 2\nforward 8\nup 9\ndown 1\nforward 7\ndown 8\nforward 3\ndown 2\ndown 5\ndown 5\ndown 3\nforward 1\nup 9\nup 9\ndown 8\ndown 6\nup 7\nforward 7\ndown 4\nforward 6\ndown 9\nup 5\nup 6\nforward 4\nforward 1\nforward 1\ndown 7\ndown 8\ndown 2\ndown 4\ndown 3\nup 8\ndown 3\nforward 3\nforward 8\nup 3\ndown 2\nforward 4\ndown 3\nforward 5\nup 1\ndown 9\ndown 1\ndown 4\nforward 3\nforward 6\nforward 7\nforward 2\nforward 9\nforward 1\nforward 6\nforward 7\nforward 2\nup 1\ndown 6\ndown 1\nforward 6\ndown 6\ndown 5\nforward 1";
    println!("{:?}", calc_pos(input1));
    let pos = calc_pos2(input1);
    println!("{:?}, {}", pos, pos.0 * pos.1);
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_calc_pos_example() {
        assert_eq!(
            calc_pos(
                "forward 5\ndown 5\nforward 8\nup 3\ndown 8\nforward 2"),
            (15, 10)
        );
    }
    #[test]
    fn test_calc_pos2_example() {
        assert_eq!(
            calc_pos2(
                "forward 5\ndown 5\nforward 8\nup 3\ndown 8\nforward 2"),
            (15, 60)
        );
    }
    #[test]
    fn test_calc_pos_combined_example() {
        assert_eq!(
            calc_pos_combined(
                "forward 5\ndown 5\nforward 8\nup 3\ndown 8\nforward 2"),
            (150, 900)
        );
    }
}
