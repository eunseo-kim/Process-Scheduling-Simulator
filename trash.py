from itertools import combinations_with_replacement
from CPU import *
from Process import *

c = CPU(7)
print(c.id)
# print(c.id())
print(id(c))
p = Process("p2", 4, 7, 2)
# print(p.id)
# print(p.id())
print(id(p))

# num_list = [x for x in range(1, 25)]
# result = combinations_with_replacement(num_list, 10)

# print(result)
# for arr in result:
#     if len(arr) == 3:
#         print(arr)
