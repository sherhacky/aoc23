with open('./input01.txt') as f:
    data = f.read()

# data = '''1abc2
# pqr3stu8vwx
# a1b2c3d4e5f
# treb7uchet
# '''

lines = data.split('\n')[:-1]

sum_of_vals = 0
for line in lines:
    nums = [c for c in line if c in '0123456789']
    sum_of_vals += 10*int(nums[0]) + int(nums[-1])
  
print(sum_of_vals)


# data = '''two1nine
# eightwothree
# abcone2threexyz
# xtwone3four
# 4nineeightseven2
# zoneight234
# 7pqrstsixteen
# '''
# lines = data.split('\n')[:-1]

sum_of_vals = 0
for line in lines:
    mapping = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
    }
    for (index, incr, factor) in [(0, 1, 10), (-1, -1, 1)]:
        while not any(line[index:].startswith(num) for num in mapping.keys() + mapping.values()):
            index += incr
        for word in mapping:
            if line[index:].startswith(word):
                sum_of_vals += int(mapping[word])*factor
        for char in '0123456789':
            if line[index] == char:
                sum_of_vals += int(char)*factor
    print(line)

print(sum_of_vals)