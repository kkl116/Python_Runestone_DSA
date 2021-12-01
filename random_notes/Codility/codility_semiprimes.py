import math
import bisect
def get_primes(num):
    sieve = [True] * (num+1)
    sieve[0] = sieve[1] = False 
    sqrt_num = int(math.sqrt(num))
    for i in range(2, sqrt_num+1):
        if sieve[i]:
            k = i**2 
            while (k <= num):
                sieve[k] = False 
                k += i
    primes = [i for i,bool_ in enumerate(sieve) if bool_]
    return primes

def get_semiprimes(N):
    primes = get_primes(N)
    semiprimes = []
    for i in range(len(primes)):
        for j in range(i,len(primes)):
            val = primes[i] * primes[j]
            if val <= N:
                semiprimes.append(val)
            if val > N:
                break
    return semiprimes

def solution(N, P, Q):
    # write your code in Python 3.6
    res = []
    semiprimes = get_semiprimes(N)
    semiprimes.sort()
    for p,q in zip(P,Q):
        p_idx = bisect.bisect_left(semiprimes, p) 
        q_idx = bisect.bisect_right(semiprimes, q) 

        res.append(q_idx - p_idx)
    return res