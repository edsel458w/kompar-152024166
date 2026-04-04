from multiprocessing import Pool, cpu_count
import time

# simulasi dokter periksa pasien, tiap pasien butuh waktu 1.5 detik
def periksa_pasien(id_pasien):
    print(f"  lagi meriksa pasien ke-{id_pasien}...")
    time.sleep(1.5)
    return f"diagnosa_{id_pasien}"

if __name__ == "__main__":
    pasien = [1, 2, 3, 4, 5, 6]

    # cara biasa dulu (sequential)
    print(f"--- sequential (1 dokter) ---")
    mulai = time.time()
    hasil = []
    for p in pasien:
        hasil.append(periksa_pasien(p))
    selesai = time.time() - mulai
    print("hasil:", hasil)
    print(f"waktu sequential: {selesai:.2f}s\n")

    # sekarang pake multiprocessing
    print(f"--- paralel ({cpu_count()} core) ---")
    mulai2 = time.time()
    with Pool(cpu_count()) as pool:
        hasil2 = pool.map(periksa_pasien, pasien)
    selesai2 = time.time() - mulai2
    print("hasil:", hasil2)
    print(f"waktu paralel: {selesai2:.2f}s")

    print(f"\nspeedup: {selesai/selesai2:.2f}x")