# SISD: proses satu data per satu waktu
numbers = [10, 20, 30, 40, 50]
result = []

for num in numbers:
    result.append(num * 2)  # Satu instruksi, satu data

print(result)  # [20, 40, 60, 80, 100]