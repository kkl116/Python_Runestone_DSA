#Codility FibFrog

# My original attempt - 100%
# fails last efficiency test all 1s   
"""
Basically first calculate every pos == 1's possible next positions, 
and then traverse all possible routes, and on the way record the minimum steps 
to the end 
important optimizations:
- precomputing fib seq to reduce repeated calculations
- precomputing next positions to reduce repeated calcs (helps only a little bit)
- using dict to store visited steps (memoization):
if pos already seen, then only try it if stored steps at least +3 over curr step 
(b/c +1 is current step, plus 2 would mean we visited this route already and has gone to next step,
but plus 3 gives room for improvement)
^ this memoization needs to be put to PREVENT traverse function call, which massively improves efficiency,
because function calls are expensive 

- path searching from each i starts from largest next step to smallest next step:
this helps allow filtering of paths with more steps later on 


solution = brute force + memoization to filter out routes that already have been considered 

I think it's good first try to implementing recursion to traverse all the solutions! :)

"""
t_max_n = 27
def get_fibs(n):
    fib = [0] * (n+2)
    fib[1] = 1
    for i in range(2, n+1):
        fib[i] = fib[i-1] + fib[i-2]
    return fib

def find_nexts(i, nexts, targ, fibs, A):
    for n in range(1, t_max_n):
        next_pos = i + fibs[n]
        if next_pos <= targ:
            if next_pos == targ:
                nexts[i+1] = [targ]
                return nexts
            elif A[next_pos]:
                nexts[i+1].append(next_pos)
        else:
            nexts[i+1].reverse()
            break
    return nexts

def solution(A):
    #another approach - for all 1s find the next possible steps, then traverse?
    nexts = [[]]
    targ = len(A)
    fibs = get_fibs(t_max_n)
    done = {}
    #add for n == -1
    nexts = find_nexts(-1, nexts, targ, fibs, A)

    fibs = get_fibs(t_max_n)
    targ = len(A)
    for i,a in enumerate(A):
        nexts.append([])
        if a:
            #find the next possible dests 
            nexts = find_nexts(i, nexts, targ, fibs, A)
        else:
            pass
    
    poss_steps = []
    def traverse(pos, nexts, poss_steps, curr_steps, done, targ):
        #starting pos = -1 
        curr_nexts = nexts[pos+1]
        for nex in curr_nexts:
            if nex == targ:
                #reached the end 
                if poss_steps:
                    if curr_steps+1 < min(poss_steps):
                        poss_steps.append(curr_steps + 1)
                else:
                    poss_steps.append(curr_steps+1)
            else:
                #put filtering conditions here to prevent function calls
                if (nex not in done or done[nex] > curr_steps + 2):
                        done.update({nex: curr_steps+1})
                        traverse(nex, nexts, poss_steps, curr_steps+1, done, targ)

    
    traverse(-1, nexts, poss_steps, 0, done, targ) 
    if len(A):
        if poss_steps:
            return min(poss_steps)
        else:
            return -1
    else:
        return 1

#Better solution - dynamic programming
"""
global problem: find the min steps to get to N, and frog is allowed to step on 1s within the array
subproblems: find the min steps to each step 1! if these are found then we can easily find the 
most optimal path to N...

from a less formal persepctive, the redundancy is reduced because there are no repeat computations --
at each pos == 1 we are LOOKING BACKWARDS at the array to find best possible steps to current pos == 1, 
and at the later 1s by revisiting this best result we prevent the need to think about all the other possible routes

simple comparison with my brute force from an estimate operations persepctive..
input = [1] * 100,000
dynamic programming: 
    MAX operations = t_max_n * len(input) = 2,600,000 (real = 2,378,658)
    ^ and this is an overestimation b/c at earlier i's the for loop will break earlier if prev < 0,
    and each for loop's operations are simple - calc prev, if prev > 0, replace value of i if smaller

brute force:
    find_nexts = MAX t_max_n * len(input) = 2,600,000 (real = 2,403,609)
    ^ cant reduce, be

    traverse function calls:
        1,051,595
    actual function calls:
        1,051,754 - in this scenario memoization barely filters any routes

n operations are around the same order of magnitude, but fewer function calls in dp algorithm makes things
a lot faster!
    

"""

n_for_loops = 0
t_max_n = 26
def get_fibs(n):
    fib = [0] * (n+2)
    fib[1] = 1
    for i in range(2, n+1):
        fib[i] = fib[i-1] + fib[i-2]
    return fib

def get_max_n(pos, targ, fibs):
    for n in range(t_max_n+1):
        if fibs[n] > (targ-pos):
            return n

def solution(A):
    global n_for_loops
    n_for_loops = 0
    # Approach: for each position == 1 in A, find the MINIMUM steps to that point. - dp solution
    fibs = get_fibs(t_max_n)
    #get global max_n ie. max steps for A
    g_max_n = get_max_n(-1, len(A), fibs)
    #insert pos = -1's step into steps (which is 0) and into A
    #insert N as 1 into A to include destination
    A.insert(0, 1)
    A.append(1)

    #set up steps array - assume for each position it takes max = len(A) to get there (if all 1s for example)
    #!!!!IMPORTNAT!!!! max steps is len(A) and not g_max_n. because depending on pattern of 1s the step
    #increments can be very small.
    steps = [len(A)] * len(A)
    steps[0] = 0

    for i,a in enumerate(A):
        if a:
            for n in range(1, g_max_n):
                n_for_loops += 1
                prev = i - fibs[n]
                if prev >= 0:
                    if steps[prev] + 1 < steps[i]:
                        steps[i] = steps[prev] + 1
                else:
                    #this previous step goes too far back so break
                    break

    print('n_for_loops: ', n_for_loops)
    if steps[-1] == len(A):
        return -1 
    else:
        return steps[-1]