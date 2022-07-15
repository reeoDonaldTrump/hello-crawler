
import multiprocessing
import random
import os
import time

def hello(num:int)->int:
    print(f"num:{num}, processId: {os.getpid()}")
    time.sleep(random.randint(1,10))
    return random.randint(1,100)

def processcallback(result:int):
    print(f"result:{result}, processId: {os.getpid()}")

if __name__ == "__main__":
    pass