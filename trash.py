from itertools import combinations_with_replacement

num_list = [x for x in range(1, 25)]
result = combinations_with_replacement(num_list, 10)

print(result)
# for arr in result:
#     if len(arr) == 3:
#         print(arr)
