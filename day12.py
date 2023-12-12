with open('./input12.txt') as f:
    data = f.read()

import operator as op
from functools import reduce


def ncr(n, r):
    if r > n:
        return 0
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom  # or / in Python 2

# data = '''???.### 1,1,3
# .??..??...?##. 1,1,3
# ?#?#?#?#?#?#?#? 1,3,1,6
# ????.#...#... 4,1,1
# ????.######..#####. 1,6,5
# ?###???????? 3,2,1
# '''

lines = data.split('\n')[:-1]
print(len(lines))

def count_configurations(row, nums):
    if not nums:
        result = 0 if '#' in row else 1
    else:
        if nums[0] > len(row):
            result = 0
        elif all(char == '?' for char in row):
            result = ncr(len(row) - sum(nums) + 1, len(nums))
        elif sum(nums) + len(nums) - 1 > len(row):
            result = 0
        elif row[0] == '#':
            if all(
                char in '#?' for char in row[:nums[0]]
                ) and ((len(row) == nums[0]) or (row[nums[0]] in '.?')):
                result = count_configurations(row[nums[0] + 1:], nums[1:])
            else:
                result = 0
        elif row[0] == '.':
            result = count_configurations(row[1:], nums)
        else:
            result = count_configurations(
                '#' + row[1:], nums
            ) + count_configurations(
                '.' + row[1:], nums
            )
    #print(row, nums, result)
    return result

result = 0
for line in lines:
    row, nums = line.split(' ')
    nums = [int(i) for i in nums.split(',')]
    result += (count_configurations(row, nums))

print(result)





def count_configurations_smarter(row, nums):
    if not nums:
        return 0 if '#' in row else 1
    elif sum(nums) + len(nums) - 1 > len(row):
        return 0
    else:
        index = 0
        while index < len(row) and row[index] == '?':
            index += 1
        if index == len(row):
            return ncr(len(row) - sum(nums) + 1, len(nums))
        elif row[index] == '.':
            result, k = 0, 0
            while k <= len(nums) and sum(nums[:k]) + k - 1 <= index:
                result += ncr(
                    index - sum(nums[:k]) + 1, k
                    ) * count_configurations_smarter(
                        row[index + 1:], nums[k:]
                    )
                k += 1
            return result
        else:
            result, k = 0, 0
            while k < len(nums) and sum(nums[:k]) + k - 1 <= index - 1:
                for s in range(nums[k]):
                    if index - s >= 0 and (
                        index - s + nums[k] <= len(row)
                    ) and all(
                        row[index - s + l] in '#?' for l in range(nums[k])
                    ) and (
                        index - s + nums[k] == len(row) or row[index - s + nums[k]] in '.?'
                    ):
                        result += ncr(
                            index - s - sum(nums[:k]), k
                        ) * count_configurations_smarter(
                            row[index - s + nums[k] + 1:], nums[k+1:]
                        )
                k += 1
            return result


resulta, resultb = 0, 0
for rn, line in enumerate(lines):
    row, nums = line.split(' ')
    nums = [int(i) for i in nums.split(',')]
    a, b = count_configurations(
        row, nums), count_configurations_smarter(row, nums)
    if a != b:
        print('mistake on row ', rn, ':', row, nums)
        print(a, 'vs.', b)
    resulta += a
    resultb += b

print(resulta, 'vs.', resultb)

print(count_configurations('??#????.', [5, 1]))
print(count_configurations_smarter('??#????.', [5,1]))

print(count_configurations('?.', [1]))
print(count_configurations_smarter('?.', [1]))

# result = 0
# for i,line in enumerate(lines):
#     row, nums = line.split(' ')
#     nums = [int(i) for i in nums.split(',')]
#     addend = count_configurations_smarter('?'.join(row for _ in range(5)), 5*nums)
#     # print(i, addend)
#     result += addend
#     if i % 50 == 0:
#         print(i)

# print(result)


# maybe faster with dynamic programming?
#

def count_configs_dp(vals, row, nums):
    if (row, ) + tuple(nums) in vals:
        return vals[(row, ) + tuple(nums)]
    else:
        if not nums:
            result = 0 if '#' in row else 1
        elif sum(nums) + len(nums) - 1 > len(row):
            result = 0
        else:
            index = 0
            while index < len(row) and row[index] == '?':
                index += 1
            if index == len(row):
                return ncr(len(row) - sum(nums) + 1, len(nums))
            elif row[index] == '.':
                result, k = 0, 0
                while k <= len(nums) and sum(nums[:k]) + k - 1 <= index:
                    result += ncr(
                        index - sum(nums[:k]) + 1, k
                    ) * count_configs_dp(
                        vals, row[index + 1:], nums[k:]
                    )
                    k += 1
            else:
                result, k = 0, 0
                while k < len(nums) and sum(nums[:k]) + k - 1 <= index - 1:
                    for s in range(nums[k]):
                        if index - s >= 0 and (
                            index - s + nums[k] <= len(row)
                        ) and all(
                            row[index - s + l] in '#?' for l in range(nums[k])
                        ) and (
                            index - s +
                                nums[k] == len(row) or row[index -
                                                        s + nums[k]] in '.?'
                        ):
                            result += ncr(
                                index - s - sum(nums[:k]), k
                            ) * count_configs_dp(
                                vals, row[index - s + nums[k] + 1:], nums[k+1:]
                            )
                    k += 1
    vals[(row, ) + tuple(nums)] = result
    return result


result = 0
for i, line in enumerate(lines):
    vals = dict()
    row, nums = line.split(' ')
    nums = [int(i) for i in nums.split(',')]
    addend = count_configs_dp(
        vals, '?'.join(row for _ in range(5)), 5*nums)
    result += addend
    if i % 50 == 0:
        print(i)

print(result)


def count_configurations_dp(vals, row, nums):
    if (row,) + tuple(nums) in vals:
        return vals[(row,) + tuple(nums)]
    if not nums:
        result = 0 if '#' in row else 1
    else:
        if nums[0] > len(row):
            result = 0
        elif all(char == '?' for char in row):
            result = ncr(len(row) - sum(nums) + 1, len(nums))
        elif sum(nums) + len(nums) - 1 > len(row):
            result = 0
        elif row[0] == '#':
            if all(
                char in '#?' for char in row[:nums[0]]
            ) and ((len(row) == nums[0]) or (row[nums[0]] in '.?')):
                result = count_configurations_dp(vals, row[nums[0] + 1:], nums[1:])
            else:
                result = 0
        elif row[0] == '.':
            result = count_configurations_dp(vals, row[1:], nums)
        else:
            result = count_configurations_dp(vals,
                '#' + row[1:], nums
            ) + count_configurations_dp(vals,
                '.' + row[1:], nums
            )
    vals[(row,) + tuple(nums)] = result
    return result


result = 0
for i, line in enumerate(lines):
    vals = dict()
    row, nums = line.split(' ')
    nums = [int(i) for i in nums.split(',')]
    addend = count_configurations_dp(
        vals, '?'.join(row for _ in range(5)), 5*nums)
    result += addend
    if i % 50 == 0:
        print(i)

print(result)
