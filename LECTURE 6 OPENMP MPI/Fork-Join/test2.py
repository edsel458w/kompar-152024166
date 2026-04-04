from multiprocessing import Pool, cpu_count
import time
import random

# tiap worker analisis sampel lab, butuh waktu random antara 1-3 detik
def cek_lab(data):
    id_pasien, nama = data
    lama = random.uniform(1.0, 3.0)
    print(f"  ngecek sampel {nama}, kira2 {lama:.1f}s...")
    time.sleep(lama)
    kondisi = random.choice(["normal", "perlu observasi", "kritis"])
    return f"{nama} -> {kondisi}"

if __name__ == "__main__":
    daftar = [(1,"Budi"),(2,"Siti"),(3,"Andi"),(4,"Rina"),(5,"Doni")]

    # fork: bagi ke semua worker
    print(f"=== FORK: bagi tugas ke {cpu_count()} worker ===")
    t = time.time()
    with Pool(cpu_count()) as p:
        hasil = p.map(cek_lab, daftar)
    elapsed = time.time() - t

    # join: kumpulin semua hasil
    print("\n=== JOIN: semua hasil masuk ===")
    for h in hasil:
        print(" ", h)
    print(f"\ntotal: {elapsed:.2f}s")