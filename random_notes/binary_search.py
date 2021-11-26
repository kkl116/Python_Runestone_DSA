"""binary search
https://stackoverflow.com/questions/35256433/binary-search-terminating-condition#:~:text=The%20two%20termination%20conditions%20you,low%20%E2%89%A4%20high%20is%20appropriate
^ good example showing why terminating condition should be <= and < in different cases
"""

def binary_search(sorted_list, target):
    left = 0 
    right = len(sorted_list) - 1
    res = None 
    #when bounds are INCLUSIVE (i.e. left and right == upper and lower bounds, then use <= 
    # else if bounds are EXCLUSIVE, (i.e. when right == len(list) b/c it's an invalid index), use < )
    while left <= right:
        mid = (left+right)//2
        if sorted_list[mid] > target:
            right = mid - 1
        else:
            left = mid + 1
            if sorted_list[mid] == target:
                return mid
    
    return -1 
