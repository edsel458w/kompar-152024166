import multiprocessing
import time

# resepsionis daftarin pasien trus kirim ke dokter
def resepsionis(q_dokter):
    pasien = ["Budi", "Siti", "Andi", "Rina"]
    for nama in pasien:
        print(f"  [resepsionis] daftarin {nama}, kirim ke dokter...")
        time.sleep(0.4)
        q_dokter.put(nama)
    q_dokter.put(None)  # kasih tau dokter udah ga ada pasien lagi

# dokter terima dari resepsionis, periksa, trus kirim resep ke apoteker
def dokter(q_dokter, q_apoteker):
    while True:
        nama = q_dokter.get()
        if nama is None:
            q_apoteker.put(None)
            break
        print(f"  [dokter] lagi meriksa {nama}...")
        time.sleep(1.0)
        q_apoteker.put(f"resep_{nama}")

# apoteker siapain obat berdasarkan resep yang masuk
def apoteker(q_apoteker):
    while True:
        resep = q_apoteker.get()
        if resep is None:
            break
        print(f"  [apoteker] nyiapin obat: {resep}")
        time.sleep(0.5)
    print("  [apoteker] semua resep beres")

if __name__ == "__main__":
    # 2 queue buat komunikasi antar proses (konsepnya kayak MPI)
    q1 = multiprocessing.Queue()
    q2 = multiprocessing.Queue()

    print("=== pipeline: resepsionis -> dokter -> apoteker ===\n")
    t = time.time()

    p1 = multiprocessing.Process(target=resepsionis, args=(q1,))
    p2 = multiprocessing.Process(target=dokter, args=(q1, q2))
    p3 = multiprocessing.Process(target=apoteker, args=(q2,))

    p1.start(); p2.start(); p3.start()
    p1.join();  p2.join();  p3.join()

    print(f"\nselesai semua, waktu: {time.time()-t:.2f}s")