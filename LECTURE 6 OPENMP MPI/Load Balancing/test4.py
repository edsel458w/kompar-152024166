from multiprocessing import Pool, cpu_count
import time

def tangani_pasien(info):
    id_p, tipe, durasi = info
    print(f"  [IGD] pasien {id_p} ({tipe}) butuh {durasi}s...")
    time.sleep(durasi)
    return f"pasien {id_p} selesai"

if __name__ == "__main__":
    # pasien 3 sama 5 kritis, sisanya ringan
    # nanti keliatan bedanya static vs dynamic
    pasien = [
        (1, "ringan",  0.5),
        (2, "ringan",  0.5),
        (3, "kritis",  4.0),
        (4, "ringan",  0.5),
        (5, "kritis",  3.5),
        (6, "ringan",  0.5),
    ]

    # static: worker 1 dapet pasien 1,2,3 — worker 2 dapet 4,5,6
    # masalahnya kalo kebetulan dapet yang kritis semua ya lama
    print("--- static scheduling (chunksize=3) ---")
    t1 = time.time()
    with Pool(2) as p:
        p.map(tangani_pasien, pasien, chunksize=3)
    w1 = time.time() - t1
    print(f"waktu static: {w1:.2f}s\n")

    # dynamic: worker yang nganggur langsung ambil tugas baru
    # lebih fleksibel, ga ada yang nunggu nganggur
    print("--- dynamic scheduling (chunksize=1) ---")
    t2 = time.time()
    with Pool(2) as p:
        p.map(tangani_pasien, pasien, chunksize=1)
    w2 = time.time() - t2
    print(f"waktu dynamic: {w2:.2f}s")

    print(f"\nselisih: {abs(w1-w2):.2f}s -> dynamic lebih efisien kalo beban ga merata")