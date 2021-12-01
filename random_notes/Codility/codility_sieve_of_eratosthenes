#codility - lesson 11 - sieve of erastothenes

from collections import Counter 
import math

def solution(A):
    counts = Counter(A) 
    res_dict = {}
    for num in counts:
        divs = 0
        sqrt_num = int(math.sqrt(num))

        """
        this is basically the find divisors function - but adding counts of divisors directly
        here, when using while loop: (while i ** 2 < num) it is a lot slower... 

        1. because range() is implemented in C, where as i += 1 is interpreted...
        2. i += 1 operation is expensive when loop is large b/c ints are immutable in python, 
        it has to create a new object every time, so also consumes a lot of memory. 
        3. the conditional i ** 2 < N is also handled in Python which makes it slow 

        so a part of this solution is to use for loop

        side note:
        in for loops/while loops, when using a variable (ie. N = 1000) vs using the constant 1000 directly,
        the while loop has additional slowdown to repeatedly look up the variable, whereas for loops 
        are not affected

        https://stackoverflow.com/questions/869229/why-is-looping-over-range-in-python-faster-than-using-a-while-loop
        """
        for i in range(1, sqrt_num+1):
            if num%i == 0:
                divs += counts.get(i, 0)
                if num//i != i:
                    divs += counts.get(num//i, 0)
        res_dict.update({num: len(A) - divs})

    return [res_dict[a] for a in A]