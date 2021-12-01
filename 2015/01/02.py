floor = 0

with open('input.txt', 'r', encoding='utf-8') as infile:
	for line in infile:
		line = line.strip()
		if not line:
			continue

		for index, char in enumerate(line):
			if char == '(':
				floor += 1
			elif char == ')':
				floor -= 1

			if floor < 0:
				print(index + 1)
				break

print(floor)
