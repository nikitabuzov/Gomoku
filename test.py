import re
import string
import random
import numpy as np
import operator


# some_scores = [0,1,2,3,4]
# score = random.choice(some_scores)
# heuristic = {'quintet': [20000000, ['xxxxx']],
# 'quartet2opens': [400000, ['exxxxe']],
# 'quartet1open': [50000, ['nxxxxe', 'exxxxn']],
# 'triplet2opens': [30000, ['exxxe']]}
# y1 = np.array([[1, 2, 3, 4], [1, 3, 5, 7], [1, 2, 4, 6], [2, 2, 3, 2]])
# y2 = np.array([[100, 200], [100,300], [100, 200], [200, 200]])
# z = np.array([1, 2])
# b = np.random.randint(5, size=(10, 10))
#
# dig1 = [b.diagonal(i) for i in range(b.shape[1]-5, -b.shape[1]+4, -1)]
# dig2 = [b[::-1, :].diagonal(i) for i in range(b.shape[1]-5, -b.shape[1]+4, -1)]

# a = 'aababa'
# b = 'aba'
# dig1 = len(re.findall(b,a))


a = {'a5':1, 'b5':2}
best = max(a.items(), key=operator.itemgetter(1))[0]
print(best)
# print(b)





# print(threatMoves)
# print(dig2)
# print(np.where(y1==z))
# count = len(np.where(y1==z))
# print(strlist)
