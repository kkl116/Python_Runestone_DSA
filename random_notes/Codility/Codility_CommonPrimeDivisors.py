#http://codility-lessons.blogspot.com/2015/03/lesson-10-commonprimedivisors.html

def gcd(a,b):
    if a%b == 0:
        return b 
    else:
        return gcd(b, a%b)    

def primeReduce(n, gcd_):
    n_a = n//gcd_
    ngcd = gcd(n_a, gcd_)
    if n_a == 1:
        #if n_a == 1, it means that 
        return True 
    elif ngcd == 1:
        return False 
    return primeReduce(n_a, ngcd)

def solution(A, B):
    # write your code in Python 3.6
    res = 0
    for a,b in zip(A,B):
        if a == b:
            res += 1
        else:
            gcd_ = gcd(a,b)
            if primeReduce(a, gcd_) and primeReduce(b, gcd_):
                res += 1
    return res

"""
A key concept is to consider NUMBERS, as a collection of factors... 
so keeping that in mind. Let's walk through it for a sample case.
a = 15, b = 75 
First, we can find the GCD of the 2 numbers, which happens to be 15.
Think of it is up to the GCD, the two numbers must share the same prime factors -- 
so a = GCD * 1, and b = GCD * 5 
for the remaining quotient of each number, again need ot consider it as A COLLECTION OF FACTORS. 
(another important thing to rmb is either a number is prime, or a composite number which can be built 
from prime * other factors)
so, from GCD, the set of prime factors currently is {3, 5}
TWO THINGS.
We need to see if prime factors in the respective quotients EXIST in the current set.
So for each quotient, we almost start PEELING prime factors off of it.

GOOD CASE - 
so for 75, 
gcd = 15 
GCD_FACTOR_SET = {3, 5}
75/15 = 5 (quotient)
gcd(5, 15) = 5 --> exists in GCD_FACTOR_SET
quotient / 5 = 1  - success b/c no more prime factors that need to be accounted for

for 15,
gcd = 15
15/15 = 1 (quotient) - do nothing b/c no more factors unaccounted for

BASE CASE - 
a, b = 10, 30
gcd = 10 
GCD_FACTOR_SET = {2, 5}
GCD

10/10 = 1 (quotient) - do nothing (meaning quotient does not have additional prime factors)

30/10 = 3 (quotient)
gcd(3, 10) = 1 -> FAILED
because it means 3 is an additional prime factor that does not exist in prime factor set within gcd!
"""