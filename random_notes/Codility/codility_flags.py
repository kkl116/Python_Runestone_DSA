# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

def check_flags(x, peaks):
    planted = 1
    prev_planted = peaks[0]
    i = 0
    while planted < x:
        i += 1
        if i == len(peaks):
            return False 

        next_pos = peaks[i]
        if next_pos - prev_planted >= x:
            prev_planted = next_pos 
            planted += 1
    return True 

def solution(A):
    # write your code in Python 3.6
    #find peaks
    peaks = []
    for i in range(1, len(A)-1):
        if A[i-1] < A[i] > A[i+1]:
            peaks.append(i)  
    if len(peaks):
        #first flag is always 1
        #use binary search here to search for the right n
        lower = 0
        higher = len(A)
        #if lower = higher - 1, we know that we've found the boundary between check == True and check == False, 
        # so return the final value of check == True which is left 
        while lower < higher-1:
            mid = (lower + higher) // 2
            if check_flags(mid, peaks):
                lower = mid
            else:
                higher = mid
        return lower
    else:
        return 0 
