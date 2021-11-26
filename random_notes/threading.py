"""
Threading is good for stuff that is I/O bound - speed of tasks limited by input and output 
Threading not so good for CPU bound stuff - intense calculations 
- cost of creating and destroying threads likely outweight benefits
Multiprocessing better for CPU bound stuff

https://www.youtube.com/watch?v=IEEhzQoKtQU&ab_channel=CoreySchafer - Threading
Threading - cpu is waiting for I/O, 
moves onto next task to do other stuff first 
"""