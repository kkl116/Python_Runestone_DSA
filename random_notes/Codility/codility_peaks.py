def check_blocks(x, peaks, A):
    #generate ranges for each "block"
    size = len(A)//x
    block_ranges = [(i*size, i*size + size-1) for i in range(len(A)//size)]  
    curr_block = 0
    i = 0
    while curr_block < x:
        curr_peak = peaks[i]
        if block_ranges[curr_block][0] <= curr_peak <= block_ranges[curr_block][1]:
            curr_block += 1
        i += 1
        if i == len(peaks) and curr_block < x:
            return False 
    return True 

def get_divisors(len_a):
    i = 1
    result = []
    while i**2 < len_a:
        if len_a%i == 0:
            result.append(i)
            result.append(len_a//i)
        i += 1
    if i**2 == len_a:
        result.append(i)
    return result

def solution(A):
    # write your code in Python 3.6
    #find peaks
    peaks = []
    for i in range(1, len(A)-1):
        if A[i-1] < A[i] > A[i+1]:
            peaks.append(i)

    if len(peaks) >= 1:
        #for number of divisors for len(A) up to sqrt(A)
        #binary search the correct divisor 
        divisors = get_divisors(len(A))
        divisors = [d for d in divisors if d <= len(peaks)]
        i = 0
        divisors.sort(reverse=True) 
        for d in divisors:
            if check_blocks(d, peaks, A):
                return d

    else:
        return 0