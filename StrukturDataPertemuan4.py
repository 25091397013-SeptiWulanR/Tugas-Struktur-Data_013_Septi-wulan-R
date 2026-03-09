# ==============================================================
# SOAL 1 — Modified Binary Search: countOccurrences
# ==============================================================
print("=" * 60)
print("SOAL 1 — Modified Binary Search: countOccurrences")
print("=" * 60)

def countOccurrences(sortedList, target):
    """
    Menghitung berapa kali target muncul dalam sortedList.
    Menggunakan dua binary search untuk menemukan:
      - leftBound  : indeks pertama kemunculan target
      - rightBound : indeks terakhir kemunculan target
    Kompleksitas: O(log n)
    """
    def findLeft(arr, target):
        """Cari indeks paling kiri di mana target berada."""
        low, high, result = 0, len(arr) - 1, -1
        while low <= high:
            mid = (low + high) // 2
            if arr[mid] == target:
                result = mid      # simpan kandidat, terus cari ke kiri
                high = mid - 1
            elif arr[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return result

    def findRight(arr, target):
        """Cari indeks paling kanan di mana target berada."""
        low, high, result = 0, len(arr) - 1, -1
        while low <= high:
            mid = (low + high) // 2
            if arr[mid] == target:
                result = mid      # simpan kandidat, terus cari ke kanan
                low = mid + 1
            elif arr[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return result

    left  = findLeft(sortedList, target)
    if left == -1:
        return 0          # target tidak ditemukan sama sekali
    right = findRight(sortedList, target)
    return right - left + 1


# --- Pengujian Soal 1 ---
list1 = [1, 2, 4, 4, 4, 4, 7, 9, 12]
print(f"\ncountOccurrences({list1}, 4) → {countOccurrences(list1, 4)}")   # expected: 4
print(f"countOccurrences({list1}, 5) → {countOccurrences(list1, 5)}")   # expected: 0
print(f"countOccurrences({list1}, 1) → {countOccurrences(list1, 1)}")   # expected: 1
print(f"countOccurrences({list1}, 9) → {countOccurrences(list1, 9)}")   # expected: 1

# ==============================================================
# SOAL 2 — Bubble Sort dengan Analisis Langkah
# ==============================================================
print("\n" + "=" * 60)
print("SOAL 2 — Bubble Sort dengan Analisis Langkah")
print("=" * 60)

def bubbleSort(theSeq):
    """
    Modifikasi bubbleSort yang:
      - Mengembalikan tuple (sorted_list, total_comparisons, total_swaps, passes_used)
      - Mengimplementasikan early termination
      - Mencetak state array setelah setiap pass
    """
    seq = list(theSeq)          # salin agar list asli tidak berubah
    n = len(seq)
    total_comparisons = 0
    total_swaps = 0
    passes_used = 0

    for i in range(n - 1):
        swapped = False
        passes_used += 1

        for j in range(n - 1 - i):
            total_comparisons += 1
            if seq[j] > seq[j + 1]:
                seq[j], seq[j + 1] = seq[j + 1], seq[j]
                total_swaps += 1
                swapped = True

        print(f"  Pass {passes_used}: {seq}")

        # Early termination — tidak ada pertukaran berarti sudah terurut
        if not swapped:
            break

    return (seq, total_comparisons, total_swaps, passes_used)


# --- Pengujian Soal 2 ---
def uji_bubble(data):
    print(f"\nInput : {data}")
    result, comps, swaps, passes = bubbleSort(data)
    print(f"Output: {result}")
    print(f"  Total comparisons : {comps}")
    print(f"  Total swaps       : {swaps}")
    print(f"  Passes digunakan  : {passes}")

uji_bubble([5, 1, 4, 2, 8])
uji_bubble([1, 2, 3, 4, 5])

print("""
Penjelasan perbedaan jumlah pass:
  [5, 1, 4, 2, 8] → perlu beberapa pass karena banyak elemen yang
                    belum terurut, sehingga pertukaran terus terjadi.
  [1, 2, 3, 4, 5] → sudah terurut, pass pertama tidak menghasilkan
                    swap sama sekali → early termination langsung aktif
                    hanya butuh 1 pass untuk konfirmasi.
""")

# ==============================================================
# SOAL 3 — Hybrid Sort
# ==============================================================
print("=" * 60)
print("SOAL 3 — Hybrid Sort")
print("=" * 60)

def insertionSortCount(seq):
    """Insertion sort yang mengembalikan (sorted_list, comparisons, swaps)."""
    arr = list(seq)
    comps, swaps = 0, 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0:
            comps += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                swaps += 1
                j -= 1
            else:
                break
        arr[j + 1] = key
    return arr, comps, swaps

def selectionSortCount(seq):
    """Selection sort yang mengembalikan (sorted_list, comparisons, swaps)."""
    arr = list(seq)
    n = len(arr)
    comps, swaps = 0, 0
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            comps += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
    return arr, comps, swaps

def hybridSort(theSeq, threshold=10):
    """
    Menggunakan insertion sort jika len(sub-array) <= threshold,
    selection sort jika lebih besar.
    Mengembalikan (sorted_list, total_ops) di mana total_ops = comps + swaps.
    """
    arr = list(theSeq)
    total_comps, total_swaps = 0, 0

    # Gunakan insertion sort untuk blok kecil (divide array ke blok threshold)
    n = len(arr)
    for start in range(0, n, threshold):
        end = min(start + threshold, n)
        sub = arr[start:end]
        if len(sub) <= threshold:
            sorted_sub, c, s = insertionSortCount(sub)
        else:
            sorted_sub, c, s = selectionSortCount(sub)
        arr[start:end] = sorted_sub
        total_comps += c
        total_swaps += s

    # Merge blok-blok yang sudah terurut (selection sort untuk sisa)
    # Untuk simplisitas, lakukan final selection sort pada seluruh array
    # yang sudah hampir terurut (blok sudah terurut, tinggal gabungkan)
    final, c2, s2 = selectionSortCount(arr)
    total_comps += c2
    total_swaps += s2

    return final, total_comps + total_swaps


# --- Pengujian Soal 3 ---
print(f"\n{'Ukuran':<10} {'Hybrid':>12} {'Pure Insertion':>16} {'Pure Selection':>16}")
print("-" * 56)

import random
for size in [50, 100, 500]:
    random.seed(42)
    data = [random.randint(1, 1000) for _ in range(size)]

    _, hybrid_ops   = hybridSort(data, threshold=10)
    _, ins_comps, ins_swaps = insertionSortCount(data)
    _, sel_comps, sel_swaps = selectionSortCount(data)

    ins_ops = ins_comps + ins_swaps
    sel_ops = sel_comps + sel_swaps

    print(f"{size:<10} {hybrid_ops:>12,} {ins_ops:>16,} {sel_ops:>16,}")

print("\n(Nilai = total comparisons + swaps)")

# ==============================================================
# SOAL 4 — Merge Tiga Sorted Lists
# ==============================================================
print("=" * 60)
print("SOAL 4 — Merge Tiga Sorted Lists")
print("=" * 60)

def mergeThreeSortedLists(listA, listB, listC):
    """
    Menggabungkan tiga sorted list menjadi satu sorted list dalam O(n).
    Menggunakan TIGA POINTER (i, j, k) dalam SATU PASS.
    Tidak memanggil fungsi merge dua list secara bertahap.

    Setiap iterasi: ambil nilai terdepan dari tiap pointer
    (gunakan inf jika list sudah habis), pilih yang terkecil,
    tambahkan ke result, lalu majukan pointer yang dipilih.
    """
    result = []
    i, j, k = 0, 0, 0
    lenA, lenB, lenC = len(listA), len(listB), len(listC)

    while i < lenA or j < lenB or k < lenC:
        a = listA[i] if i < lenA else float('inf')
        b = listB[j] if j < lenB else float('inf')
        c = listC[k] if k < lenC else float('inf')

        minimum = min(a, b, c)
        result.append(minimum)

        if minimum == a:
            i += 1
        elif minimum == b:
            j += 1
        else:
            k += 1

    return result


# --- Pengujian Soal 4 ---
A, B, C = [1, 5, 9], [2, 6, 10], [3, 4, 7]
print(f"\nlistA = {A}")
print(f"listB = {B}")
print(f"listC = {C}")
print(f"Hasil → {mergeThreeSortedLists(A, B, C)}")
# expected: [1, 2, 3, 4, 5, 6, 7, 9, 10]

A2, B2, C2 = [1, 4, 7], [2, 5, 8], [3, 6, 9]
print(f"\nlistA = {A2}, listB = {B2}, listC = {C2}")
print(f"Hasil → {mergeThreeSortedLists(A2, B2, C2)}")

A3, B3, C3 = [], [1, 3], [2]
print(f"\nlistA = {A3}, listB = {B3}, listC = {C3}")
print(f"Hasil → {mergeThreeSortedLists(A3, B3, C3)}")

"""
SOAL 5 — Inversions Counter
Data Structures & Algorithms - Chapter 5
"""

import random
import time


def countInversionsNaive(arr):
    """
    Brute force O(n²).
    Inversion: pasangan (i, j) di mana i < j tapi arr[i] > arr[j].
    Periksa semua kemungkinan pasangan.
    """
    count = 0
    n = len(arr)
    for i in range(n - 1):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count


def countInversionsSmart(arr):
    """
    Modifikasi Merge Sort O(n log n).
    Saat merge dua sub-array terurut: jika right[j] < left[i],
    maka right[j] lebih kecil dari SEMUA elemen tersisa di kiri
    → tambahkan (len(left) - i) inversion sekaligus.
    """
    def mergeAndCount(left, right):
        merged = []
        inversions = 0
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                inversions += len(left) - i   # semua left[i:] > right[j]
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, inversions

    def sortAndCount(arr):
        if len(arr) <= 1:
            return arr, 0
        mid = len(arr) // 2
        left,  inv_left  = sortAndCount(arr[:mid])
        right, inv_right = sortAndCount(arr[mid:])
        merged, inv_split = mergeAndCount(left, right)
        return merged, inv_left + inv_right + inv_split

    _, total = sortAndCount(list(arr))
    return total


# --- Pengujian kebenaran ---
print("=" * 60)
print("SOAL 5 — Inversions Counter")
print("=" * 60)

contoh = [3, 1, 2, 5, 4]
print(f"\nContoh arr = {contoh}")
print(f"  Naive  : {countInversionsNaive(contoh)} inversions")
print(f"  Smart  : {countInversionsSmart(contoh)} inversions")
print(f"  Sama   : {countInversionsNaive(contoh) == countInversionsSmart(contoh)}")

contoh2 = [5, 4, 3, 2, 1]   # fully reversed → 10 inversions
print(f"\nArr fully reversed {contoh2}")
print(f"  Naive  : {countInversionsNaive(contoh2)}")
print(f"  Smart  : {countInversionsSmart(contoh2)}")

contoh3 = [1, 2, 3, 4, 5]   # already sorted → 0 inversions
print(f"\nArr already sorted {contoh3}")
print(f"  Naive  : {countInversionsNaive(contoh3)}")
print(f"  Smart  : {countInversionsSmart(contoh3)}")

# --- Pengukuran waktu eksekusi ---
print(f"\n{'Ukuran':<10} {'Naive (ms)':>12} {'Smart (ms)':>12} {'Hasil Sama':>12}")
print("-" * 48)

for size in [1000, 5000, 10000]:
    random.seed(0)
    data = [random.randint(1, 10000) for _ in range(size)]

    t0 = time.time()
    res_naive = countInversionsNaive(data)
    t1 = time.time()
    res_smart = countInversionsSmart(data)
    t2 = time.time()

    naive_ms = (t1 - t0) * 1000
    smart_ms = (t2 - t1) * 1000

    print(f"{size:<10} {naive_ms:>11.2f} {smart_ms:>11.2f} "
          f"{'Ya' if res_naive == res_smart else 'TIDAK':>12}")

print("""
Penjelasan mengapa Merge Sort lebih cepat:
  - countInversionsNaive → O(n²): membandingkan SEMUA pasangan (i, j).
    Untuk n=10.000 ada ~50 juta perbandingan.

  - countInversionsSmart → O(n log n): saat merge dua sub-array terurut,
    ketika right[j] < left[i], kita langsung tahu bahwa right[j] membentuk
    inversion dengan SEMUA elemen tersisa di kiri (len(left) - i) sekaligus,
    tanpa loop tambahan. Untuk n=10.000 hanya ~130.000 operasi —
    ratusan kali lebih efisien.
""")

