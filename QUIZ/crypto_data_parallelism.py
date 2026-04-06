from multiprocessing import Pool
import time
import random
import os
from datetime import datetime, timedelta

# buat simulasi data harga kripto, 
# pakai random walk biar gerakannya natural naik turun
def buat_data_harga(coin, jumlah_hari=120, seed=42):
    random.seed(seed)
    harga_awal = 45000 if coin == "BTC" else 2500
    data = []
    harga_sekarang = harga_awal
    tgl_mulai = datetime(2024, 1, 1)

    for i in range(jumlah_hari):
        perubahan = random.uniform(-0.05, 0.055)
        open_h  = harga_sekarang
        close_h = round(open_h * (1 + perubahan), 2)
        high_h  = round(max(open_h, close_h) * random.uniform(1.001, 1.02), 2)
        low_h   = round(min(open_h, close_h) * random.uniform(0.98, 0.999), 2)
        vol     = round(random.uniform(10000, 80000), 2)

        data.append({
            "tanggal": (tgl_mulai + timedelta(days=i)).strftime("%Y-%m-%d"),
            "coin":    coin,
            "open":    open_h,
            "high":    high_h,
            "low":     low_h,
            "close":   close_h,
            "volume":  vol
        })
        harga_sekarang = close_h

    return data


# ini fungsi yang dijalankan tiap worker secara paralel
# masing-masing worker nerima potongan data yang beda
def proses_chunk(args):
    chunk_id, data = args
    pid = os.getpid()

    print(f"[PID {pid}] Chunk-{chunk_id} mulai | {data[0]['coin']} | {data[0]['tanggal']} - {data[-1]['tanggal']}")
    time.sleep(0.5)  # simulasi proses berat

    closes  = [d["close"]  for d in data]
    opens   = [d["open"]   for d in data]
    highs   = [d["high"]   for d in data]
    lows    = [d["low"]    for d in data]
    volumes = [d["volume"] for d in data]

    # hitung moving average 5 hari
    ma5 = []
    for i in range(len(closes)):
        window = closes[max(0, i-4): i+1]
        ma5.append(round(sum(window) / len(window), 2))

    # volatilitas = selisih high-low dibagi open, kali 100
    volatilitas = [round((h - l) / o * 100, 4) for h, l, o in zip(highs, lows, opens)]

    # persentase perubahan harga tiap hari
    pct_change = [round((c - o) / o * 100, 4) for c, o in zip(closes, opens)]

    hasil = {
        "chunk_id":    chunk_id,
        "pid":         pid,
        "coin":        data[0]["coin"],
        "tgl_mulai":   data[0]["tanggal"],
        "tgl_akhir":   data[-1]["tanggal"],
        "n_hari":      len(data),
        "avg_ma5":     round(sum(ma5) / len(ma5), 2),
        "avg_volatil": round(sum(volatilitas) / len(volatilitas), 4),
        "avg_pct":     round(sum(pct_change) / len(pct_change), 4),
        "harga_max":   max(highs),
        "harga_min":   min(lows),
        "avg_volume":  round(sum(volumes) / len(volumes), 2),
        "naik":        sum(1 for p in pct_change if p > 0),
        "turun":       sum(1 for p in pct_change if p <= 0),
    }

    print(f"[PID {pid}] Chunk-{chunk_id} selesai | MA5: {hasil['avg_ma5']:,.2f} | max: {hasil['harga_max']:,.2f} | min: {hasil['harga_min']:,.2f}")
    return hasil

# gabungin semua hasil dari tiap worker jadi satu ringkasan
def gabung_hasil(semua_hasil):
    return {
        "coin":       semua_hasil[0]["coin"],
        "total_hari": sum(r["n_hari"] for r in semua_hasil),
        "max":        max(r["harga_max"] for r in semua_hasil),
        "min":        min(r["harga_min"] for r in semua_hasil),
        "avg_ma5":    round(sum(r["avg_ma5"] for r in semua_hasil) / len(semua_hasil), 2),
        "avg_vol":    round(sum(r["avg_volatil"] for r in semua_hasil) / len(semua_hasil), 4),
        "avg_pct":    round(sum(r["avg_pct"] for r in semua_hasil) / len(semua_hasil), 4),
        "naik":       sum(r["naik"] for r in semua_hasil),
        "turun":      sum(r["turun"] for r in semua_hasil),
    }

if __name__ == "__main__":
    N_WORKER = 4
    N_HARI   = 120

    print("  Data Parallelism - Analisis Harga Kripto")
    print(f"  Worker: {N_WORKER} | Data: {N_HARI} hari per koin\n")

    for coin, seed in [("BTC", 42), ("ETH", 99)]:
        print(f"\n--- {coin} ---")

        # buat data dulu
        data_harga = buat_data_harga(coin, N_HARI, seed)

        # bagi data jadi N_WORKER bagian
        ukuran = N_HARI // N_WORKER
        chunks = []
        for i in range(N_WORKER):
            mulai = i * ukuran
            akhir = mulai + ukuran if i < N_WORKER - 1 else N_HARI
            chunks.append((i + 1, data_harga[mulai:akhir]))

        print(f"Data dibagi jadi {N_WORKER} chunk, masing-masing ~{ukuran} hari")
        print(f"Setiap chunk diproses worker berbeda secara paralel:\n")

        # jalankan paralel
        t_mulai = time.time()
        with Pool(processes=N_WORKER) as pool:
            hasil_chunks = pool.map(proses_chunk, chunks)
        t_selesai = time.time()

        print(f"\nWaktu eksekusi: {round(t_selesai - t_mulai, 3)} detik")

        # agregasi semua hasil
        ringkasan = gabung_hasil(hasil_chunks)

        print(f"\nRingkasan {coin}:")
        print(f"  Harga tertinggi : ${ringkasan['max']:,.2f}")
        print(f"  Harga terendah  : ${ringkasan['min']:,.2f}")
        print(f"  Rata-rata MA5   : ${ringkasan['avg_ma5']:,.2f}")
        print(f"  Avg volatilitas : {ringkasan['avg_vol']}%")
        print(f"  Hari naik/turun : {ringkasan['naik']} / {ringkasan['turun']}")

    print("  Selesai.")
    