def count_configurations_dp(vals, row, nums):
    if (row,) + tuple(nums) in vals:
        return vals[(row,) + tuple(nums)]
    elif not nums:
        result = 0 if '#' in row else 1
    elif nums[0] > len(row):
        result = 0
    elif row[0] == '.':
        result = count_configurations_dp(vals, row[1:], nums)
    elif row[0] == '#':
        if all(
            char in '#?' for char in row[:nums[0]]
        ) and ((len(row) == nums[0]) or (row[nums[0]] in '.?')):
            result = count_configurations_dp(vals, row[nums[0] + 1:], nums[1:])
        else:
            result = 0
    else:
        result = count_configurations_dp(
            vals, '#' + row[1:], nums
        ) + count_configurations_dp(
            vals, '.' + row[1:], nums
        )
    vals[(row,) + tuple(nums)] = result
    return result


with open('./input12.txt') as f:
    data = f.read()
lines = data.split('\n')[:-1]

part_1_result = 0
part_2_result = 0
for i, line in enumerate(lines):
    row, nums = line.split(' ')
    nums = [int(i) for i in nums.split(',')]
    part_1_result += count_configurations_dp(dict(), row, nums)
    part_2_result += count_configurations_dp(
        dict(), '?'.join(row for _ in range(5)), 5*nums
    )
print(part_1_result)
print(part_2_result)
