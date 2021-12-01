#!/usr/bin/env ruby

def explore(input)
	floor = 0

	input.each_grapheme_cluster do |thing|
		case thing
		when '('
			floor = floor + 1
		when ')'
			floor = floor - 1
		end
	end

	return floor
end

examples = [
	["(())", 0],
	["()()", 0],
	["(((", 3],
	["(()(()(", 3],
	["))(((((", 3],
	["())", -1],
	["))(", -1],
	[")))", -3],
	[")())())", -3],
]

examples.each do |pair|
	puzzle, expected = pair
	actual = explore(puzzle)
	printf "%d, %d\n" % [expected, actual]
end

puzzle = File.read("input.txt")

puts "actual puzzle"

puts explore(puzzle)
