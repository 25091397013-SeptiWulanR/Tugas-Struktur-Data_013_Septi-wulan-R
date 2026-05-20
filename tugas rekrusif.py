"""
====================================================
  TUGAS REKURSIF - ALGORITMA BACKTRACKING
  1. N-Queens  (N-Ratu)
  2. Knight's Tour  (Tur Kuda)
  3. Knapsack  (Masalah Tas)
====================================================
"""

# ─────────────────────────────────────────────────
#  BAGIAN 1 : N-QUEENS
# ─────────────────────────────────────────────────

def solve_nqueens(n):
    """
    Menyelesaikan masalah N-Queens menggunakan backtracking rekursif.
    Menempatkan N ratu di papan N×N sehingga tidak ada yang saling menyerang.

    Parameter:
        n (int): ukuran papan dan jumlah ratu

    Return:
        list[list[str]]: semua solusi papan yang valid
    """
    board = [['.' ] * n for _ in range(n)]
    solutions = []

    def is_safe(row, col):
        # Cek kolom yang sama di baris atas
        for r in range(row):
            if board[r][col] == 'Q':
                return False

        # Cek diagonal kiri-atas
        r, c = row - 1, col - 1
        while r >= 0 and c >= 0:
            if board[r][c] == 'Q':
                return False
            r -= 1
            c -= 1

        # Cek diagonal kanan-atas
        r, c = row - 1, col + 1
        while r >= 0 and c < n:
            if board[r][c] == 'Q':
                return False
            r -= 1
            c += 1

        return True

    def backtrack(row):
        # Basis rekursi: semua baris sudah terisi -> simpan solusi
        if row == n:
            solutions.append([row[:] for row in board])
            return

        for col in range(n):
            if is_safe(row, col):
                board[row][col] = 'Q'   # tempatkan ratu
                backtrack(row + 1)      # rekursi ke baris berikutnya
                board[row][col] = '.'   # backtrack

    backtrack(0)
    return solutions


def print_queens_board(board):
    """Mencetak satu solusi papan N-Queens."""
    n = len(board)
    separator = '+' + ('---+' * n)
    print(separator)
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print(separator)


def run_nqueens():
    print("=" * 50)
    print("       MASALAH N-QUEENS (N-RATU)")
    print("=" * 50)
    try:
        n = int(input("Masukkan ukuran papan (N, disarankan 4-10): "))
        if n < 1:
            print("N harus lebih dari 0.")
            return
    except ValueError:
        print("Input tidak valid.")
        return

    print(f"\nMencari solusi untuk {n}-Queens...\n")
    solutions = solve_nqueens(n)

    if not solutions:
        print(f"Tidak ada solusi untuk {n}-Queens.")
        return

    print(f"Ditemukan {len(solutions)} solusi.\n")

    # Tampilkan semua solusi atau pilih berapa yang ingin ditampilkan
    try:
        tampil = int(input(f"Tampilkan berapa solusi? (1-{len(solutions)}): "))
        tampil = max(1, min(tampil, len(solutions)))
    except ValueError:
        tampil = 1

    for i, sol in enumerate(solutions[:tampil], 1):
        print(f"\n--- Solusi {i} ---")
        print_queens_board(sol)
        print("Posisi kolom ratu per baris:", [row.index('Q') for row in sol])


# ─────────────────────────────────────────────────
#  BAGIAN 2 : KNIGHT'S TOUR (TUR KUDA)
# ─────────────────────────────────────────────────

def knights_tour(start_row, start_col, n=8):
    """
    Menyelesaikan Knight's Tour menggunakan backtracking rekursif
    dengan heuristik Warnsdorff (pilih kotak dengan degree terkecil).

    Parameter:
        start_row (int): baris awal kuda (0-indexed)
        start_col (int): kolom awal kuda (0-indexed)
        n        (int): ukuran papan (default 8x8)

    Return:
        list[list[int]] | None: papan berisi urutan langkah, atau None jika gagal
    """
    # 8 kemungkinan gerakan kuda
    moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
             ( 1, -2), ( 1, 2), ( 2, -1), ( 2,  1)]

    # Inisialisasi papan dengan -1 (belum dikunjungi)
    board = [[-1] * n for _ in range(n)]
    board[start_row][start_col] = 0   # langkah pertama = 0

    def valid(r, c):
        return 0 <= r < n and 0 <= c < n and board[r][c] == -1

    def degree(r, c):
        """Hitung berapa banyak langkah valid dari posisi (r, c) — heuristik Warnsdorff."""
        return sum(1 for dr, dc in moves if valid(r + dr, c + dc))

    def backtrack(r, c, step):
        # Basis rekursi: semua petak sudah dikunjungi
        if step == n * n:
            return True

        # Urutkan langkah berikutnya berdasarkan degree (Warnsdorff)
        next_moves = [(dr, dc) for dr, dc in moves if valid(r + dr, c + dc)]
        next_moves.sort(key=lambda x: degree(r + x[0], c + x[1]))

        for dr, dc in next_moves:
            nr, nc = r + dr, c + dc
            board[nr][nc] = step          # kunjungi petak
            if backtrack(nr, nc, step + 1):
                return True
            board[nr][nc] = -1            # backtrack

        return False

    success = backtrack(start_row, start_col, 1)
    return board if success else None


def print_knight_board(board):
    """Mencetak papan Knight's Tour dengan urutan langkah."""
    n = len(board)
    separator = '+' + ('----+' * n)
    print(separator)
    for row in board:
        print('|' + ''.join(f' {v+1:2d} |' if v >= 0 else '  . |' for v in row))
        print(separator)


def print_knight_path(board):
    """Mencetak urutan langkah kuda secara berurutan."""
    n = len(board)
    path = [None] * (n * n)
    for r in range(n):
        for c in range(n):
            if board[r][c] >= 0:
                path[board[r][c]] = (r, c)

    print("\nUrutan langkah kuda:")
    for i, pos in enumerate(path):
        if pos:
            arrow = f" → {path[i+1]}" if i + 1 < len(path) and path[i+1] else ""
            print(f"  Langkah {i+1:2d}: baris={pos[0]}, kolom={pos[1]}{arrow}")


def run_knights_tour():
    print("=" * 50)
    print("     MASALAH TUR KUDA (KNIGHT'S TOUR)")
    print("=" * 50)
    try:
        n = int(input("Ukuran papan (default 8): ") or "8")
        r = int(input(f"Baris awal kuda (0-{n-1}): "))
        c = int(input(f"Kolom awal kuda (0-{n-1}): "))
        if not (0 <= r < n and 0 <= c < n):
            print(f"Posisi harus antara 0 dan {n-1}.")
            return
    except ValueError:
        print("Input tidak valid.")
        return

    print(f"\nMencari Tur Kuda dari posisi ({r}, {c}) di papan {n}×{n}...\n")
    board = knights_tour(r, c, n)

    if board is None:
        print("Tidak ditemukan solusi dari posisi tersebut.")
        return

    print(f"Tur Kuda berhasil! Semua {n*n} petak dikunjungi.\n")
    print("Papan (angka = urutan kunjungan):")
    print_knight_board(board)
    print_knight_path(board)


# ─────────────────────────────────────────────────
#  BAGIAN 3 : KNAPSACK (MASALAH TAS)
# ─────────────────────────────────────────────────

def knapsack_all(weights, target):
    """
    Mencari SEMUA kombinasi barang yang totalnya tepat sama dengan target
    menggunakan algoritma rekursif backtracking.

    Parameter:
        weights (list[int]): daftar berat barang
        target  (int)      : berat target yang ingin dicapai

    Return:
        list[list[int]]: semua kombinasi yang valid
    """
    solutions = []

    def backtrack(idx, remaining, chosen):
        # Basis rekursi: target tercapai
        if remaining == 0:
            solutions.append(list(chosen))
            return

        # Prune: tidak mungkin mencapai target
        if remaining < 0 or idx >= len(weights):
            return

        # Pilihan 1: ambil barang ke-idx
        chosen.append(weights[idx])
        backtrack(idx + 1, remaining - weights[idx], chosen)
        chosen.pop()  # backtrack

        # Pilihan 2: lewati barang ke-idx
        backtrack(idx + 1, remaining, chosen)

    backtrack(0, target, [])
    return solutions


def knapsack_first(weights, target):
    """
    Mencari SATU solusi pertama menggunakan rekursi dengan memoization.

    Parameter:
        weights (list[int]): daftar berat barang
        target  (int)      : berat target

    Return:
        list[int] | None: kombinasi pertama yang valid, atau None
    """
    memo = {}

    def can_fill(idx, remaining):
        if remaining == 0:
            return []
        if remaining < 0 or idx >= len(weights):
            return None

        key = (idx, remaining)
        if key in memo:
            return memo[key]

        # Ambil barang ke-idx (rekursi)
        take = can_fill(idx + 1, remaining - weights[idx])
        if take is not None:
            result = [weights[idx]] + take
            memo[key] = result
            return result

        # Lewati barang ke-idx (rekursi)
        skip = can_fill(idx + 1, remaining)
        memo[key] = skip
        return skip

    return can_fill(0, target)


def run_knapsack():
    print("=" * 50)
    print("        MASALAH KNAPSACK (TAS)")
    print("=" * 50)
    try:
        raw = input("Masukkan berat barang (pisahkan dengan koma, contoh: 2,5,6,9,12,14,20): ")
        weights = [int(x.strip()) for x in raw.split(',') if x.strip()]
        if not weights:
            print("Tidak ada barang yang valid.")
            return
        target = int(input("Masukkan berat target: "))
        if target <= 0:
            print("Target harus lebih dari 0.")
            return
    except ValueError:
        print("Input tidak valid.")
        return

    print(f"\nBarang tersedia : {weights}")
    print(f"Target berat    : {target}\n")

    # Cari solusi pertama dengan memoization (cepat)
    first = knapsack_first(weights, target)
    if first:
        print(f"Solusi pertama  : {first}")
        print(f"Total berat     : {sum(first)}\n")
    else:
        print("Tidak ada kombinasi yang mencapai target persis.\n")
        return

    # Tanya apakah ingin melihat semua solusi
    lihat_semua = input("Tampilkan semua solusi? (y/n): ").strip().lower()
    if lihat_semua == 'y':
        semua = knapsack_all(weights, target)
        print(f"\nTotal solusi ditemukan: {len(semua)}")
        for i, sol in enumerate(semua, 1):
            print(f"  Solusi {i:3d}: {sol} = {sum(sol)}")


# ─────────────────────────────────────────────────
#  MENU UTAMA
# ─────────────────────────────────────────────────

def main():
    print("\n" + "=" * 50)
    print("   TUGAS REKURSIF & BACKTRACKING")
    print("=" * 50)
    print("  1. N-Queens  (N-Ratu)")
    print("  2. Knight's Tour  (Tur Kuda)")
    print("  3. Knapsack  (Masalah Tas)")
    print("  4. Jalankan semua (demo otomatis)")
    print("  0. Keluar")
    print("=" * 50)

    pilihan = input("Pilih menu (0-4): ").strip()

    if pilihan == '1':
        print()
        run_nqueens()

    elif pilihan == '2':
        print()
        run_knights_tour()

    elif pilihan == '3':
        print()
        run_knapsack()

    elif pilihan == '4':
        # Demo otomatis dengan nilai default
        print("\n" + "─" * 50)
        print("DEMO 1: 6-Queens")
        print("─" * 50)
        sols = solve_nqueens(6)
        print(f"Jumlah solusi 6-Queens: {len(sols)}")
        print("Solusi pertama:")
        print_queens_board(sols[0])

        print("\n" + "─" * 50)
        print("DEMO 2: Knight's Tour dari (0, 0) di papan 8x8")
        print("─" * 50)
        board = knights_tour(0, 0, 8)
        if board:
            print("Berhasil! Papan urutan kunjungan:")
            print_knight_board(board)
        else:
            print("Gagal menemukan solusi.")

        print("\n" + "─" * 50)
        print("DEMO 3: Knapsack - barang [2,5,6,9,12,14,20], target 30")
        print("─" * 50)
        weights = [2, 5, 6, 9, 12, 14, 20]
        target  = 30
        semua   = knapsack_all(weights, target)
        print(f"Semua solusi (total {len(semua)}):")
        for i, s in enumerate(semua, 1):
            print(f"  Solusi {i}: {s} = {sum(s)}")

    elif pilihan == '0':
        print("Keluar. Sampai jumpa!")
        return

    else:
        print("Pilihan tidak valid.")

    # Tanya apakah ingin kembali ke menu
    print()
    lagi = input("Kembali ke menu utama? (y/n): ").strip().lower()
    if lagi == 'y':
        main()


if __name__ == "__main__":
    main()