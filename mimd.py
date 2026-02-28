from multiprocessing import Process, current_process
import os

def tugas_A(data):
    
    result = [x * 3 for x in data]
    print(f"[{current_process().name}] Multiply: {result}")

def tugas_B(data):
    
    result = [x for x in data if x % 2 == 0]
    print(f"[{current_process().name}] Filter: {result}")

def tugas_C(data):
    
    result = sum(data)
    print(f"[{current_process().name}] Sum: {result}")

if __name__ == "__main__":
    data1 = [1, 2, 3, 4]
    data2 = [5, 6, 7, 8]
    data3 = [9, 10, 11, 12]

    # 3 proses, instruksi BERBEDA, data BERBEDA → MIMD
    p1 = Process(target=tugas_A, args=(data1,), name="Process-A")
    p2 = Process(target=tugas_B, args=(data2,), name="Process-B")
    p3 = Process(target=tugas_C, args=(data3,), name="Process-C")

    p1.start(); p2.start(); p3.start()
    p1.join();  p2.join();  p3.join()


# **Output:**
# ```
# [Process-A] Multiply: [3, 6, 9, 12]
# [Process-B] Filter: [6, 8]
# [Process-C] Sum: 42
# ```