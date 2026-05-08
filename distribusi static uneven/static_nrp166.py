import threading
import time

# NRP: 166
# digit genap dari NRP = 6, 6
# total proses = 6 + 6 = 12
# distribusi static uneven ke 3 thread: 6, 4, 2 (total 12, tidak merata)

# jumlah task per thread udah ditentuin dari awal (static)
tugas_thread = [6, 4, 2]  # thread 0 dapet 6, thread 1 dapet 4, thread 2 dapet 2

waktu_selesai = [0, 0, 0]

def kerjain(id_thread, jumlah_tugas):
    print(f"thread-{id_thread} mulai, kebagian {jumlah_tugas} tugas")
    
    total = 0
    for i in range(jumlah_tugas):
        # simulasi kerja, tiap tugas butuh waktu 0.5 detik
        time.sleep(0.5)
        total += 1
        print(f"  thread-{id_thread} selesai tugas ke-{i+1}")
    
    waktu_selesai[id_thread] = total * 0.5
    print(f"thread-{id_thread} beres semua, total waktu estimasi: {waktu_selesai[id_thread]}s")

# bikin thread-nya
t0 = threading.Thread(target=kerjain, args=(0, tugas_thread[0]))
t1 = threading.Thread(target=kerjain, args=(1, tugas_thread[1]))
t2 = threading.Thread(target=kerjain, args=(2, tugas_thread[2]))

mulai = time.time()

t0.start()
t1.start()
t2.start()

t0.join()
t1.join()
t2.join()

selesai = time.time()
total_waktu = round(selesai - mulai, 2)

print()
print("=== HASIL ===")
print(f"distribusi tugas  : {tugas_thread}")
print(f"waktu tiap thread : {[f'{t}s' for t in waktu_selesai]}")
print(f"wall clock time   : {total_waktu}s")

# cek apakah distribusi udah ideal
# ideal = semua thread selesai barengan (selisih < 0.1s)
maks = max(waktu_selesai)
mini = min(waktu_selesai)
selisih = round(maks - mini, 2)

print(f"selisih waktu     : {selisih}s")

if selisih <= 0.1:
    print("distribusi IDEAL tercapai! semua thread selesai hampir bersamaan")
else:
    print(f"distribusi belum ideal, selisih {selisih}s (harusnya <= 0.1s)")
    print("thread-0 kebagian paling banyak karena digit NRP pertama = 6")
