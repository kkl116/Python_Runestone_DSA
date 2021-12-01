#Codility - Ladder 

#100%
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