#Codility - Ladder 

#100% my solution - 
def solution(A, B):
    # write your code in Python 3.6
    #get fib sequence up to L
    L = len(A) + 1
    fibs = [0] * (L+2)
    fibs[1] = 1
    for i in range(2, L+1):
        fibs[i] = fibs[i-1] + fibs[i-2]
    #get pows
    pows = [0, 2]
    for _ in range(2, 30+1):
        pows.append(pows[-1]*2)
    #get dict to store already computed stuff - modolo is expensive!
    done = {}
    res = []
    for a, b in zip(A,B):
        if (a,b) in done:
            res.append(done[(a,b)])
        else:
            c = fibs[a+1] % pows[b]
            done.update({(a,b): c})
            res.append(c)
    return res

#another solution - key concept here is that taking modulo 2^n is actually equal to stripping 
#places in the number in BINARY FORM (think % 10^n in base 10)
    # write your code in Python 3.6
    #get fib sequence up to L
def solution(A,B):
    L = len(A) + 1
    fibs = [0] * (L+2)
    fibs[1] = 1
    for i in range(2, L+1):
        fibs[i] = fibs[i-1] + fibs[i-2]
    #get pows
    pows = [0, 2]
    for _ in range(2, 30+1):
        pows.append(pows[-1]*2)

    res = []
    for  a,b in zip(A,B):
        res.append(fibs[a+1] & (pows[b] - 1))
        #& operator converts both numbers to binary, then compares each digit-
        #if both digits == 1, then resulting digit in final number is 1 etc 
        #pows[b] - 1's binary string is ALL 1s (b/c pows[b] binary is 1000, 10000, etc)
        #so pows[b] - 1 = 111, 1111 etc for the prev corresponding strings
        """
        e.g. 
        1010    100111
         |          |
        0100    000101
        0000       101
        """

        """
        another way to get pows is bitwise operator >> and << 
        essentially first converts original int into binary e.g. 3 -> 11
        then 3 << 5 in python would be 1100000 converted to int (96)
        """
    return res