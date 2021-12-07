#!/bin/sh
export c=session=53616c7465645f5fdc6a11fbbd01401e02c6c87c265298a2dc797ae1813a4f64597eb39b7be080e24b4e34c0df02f73e
curl -b$c https://adventofcode.com/2021/day/$1/input > input.txt
