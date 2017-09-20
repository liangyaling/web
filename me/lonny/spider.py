# -*- coding:utf-8 -*-
'''def is_plaindrome(n):
    return str(n)==str(n)[ : :-1]
output=filter(is_plaindrome,range(1,10000))
print(list(output))'''

L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
def by_score(t):
    return t[1]
L2=sorted(L,key=by_score,reverse=True)
print(L2)