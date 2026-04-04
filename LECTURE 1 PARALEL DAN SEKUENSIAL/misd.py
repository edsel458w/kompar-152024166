from multiprocessing import Process

# SATU DATA yang sama
data = 100

def instruksi_A(x):
    hasil = x + 50
    print(f"[Instruksi A] {x} + 50 = {hasil}")

def instruksi_B(x):
    hasil = x * 2
    print(f"[Instruksi B] {x} * 2 = {hasil}")

def instruksi_C(x):
    hasil = x ** 2
    print(f"[Instruksi C] {x} ** 2 = {hasil}")

def instruksi_D(x):
    hasil = x - 30
    print(f"[Instruksi D] {x} - 30 = {hasil}")

if __name__ == "__main__":
    # Banyak instruksi BERBEDA → data SAMA (100)
    proses = [
        Process(target=instruksi_A, args=(data,)),
        Process(target=instruksi_B, args=(data,)),
        Process(target=instruksi_C, args=(data,)),
        Process(target=instruksi_D, args=(data,)),
    ]

    for p in proses:
        p.start()
    for p in proses:
        p.join()
# ```

# **Output:**
# ```
# [Instruksi A] 100 + 50 = 150
# [Instruksi B] 100 * 2 = 200
# [Instruksi C] 100 ** 2 = 10000
# [Instruksi D] 100 - 30 = 70