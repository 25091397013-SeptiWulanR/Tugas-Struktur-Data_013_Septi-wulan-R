"""
Conway's Game of Life — dengan Menu & Aturan Main
==================================================
Cara menjalankan: python3 game_of_life.py
"""

import sys, time, random, threading


# ══════════════════════════════════════════════════════════════
#  WARNA & KONSTANTA
# ══════════════════════════════════════════════════════════════
R   = "\033[0m"      # reset
G   = "\033[92m"     # hijau
C   = "\033[96m"     # cyan
Y   = "\033[93m"     # kuning
M   = "\033[95m"     # magenta
W   = "\033[97m"     # putih
DIM = "\033[2m"
B   = "\033[1m"      # bold
RED = "\033[91m"

COLS  = 62
ROWS  = 24
ALIVE = "█"
DEAD  = "·"
FPS   = 8

# ══════════════════════════════════════════════════════════════
#  LOGIKA GRID
# ══════════════════════════════════════════════════════════════
def empty_grid():
    return [[0]*COLS for _ in range(ROWS)]

def random_grid(density=0.30):
    return [[1 if random.random()<density else 0 for _ in range(COLS)]
            for _ in range(ROWS)]

def count_neighbors(grid, r, c):
    s = 0
    for dr in (-1,0,1):
        for dc in (-1,0,1):
            if dr==0 and dc==0: continue
            s += grid[(r+dr)%ROWS][(c+dc)%COLS]
    return s

def next_gen(grid):
    new, born, died = empty_grid(), 0, 0
    for r in range(ROWS):
        for c in range(COLS):
            n = count_neighbors(grid, r, c)
            if grid[r][c]:
                if n in (2,3): new[r][c]=1
                else: died+=1
            else:
                if n==3: new[r][c]=1; born+=1
    return new, born, died

def alive_count(grid):
    return sum(sum(row) for row in grid)


# ══════════════════════════════════════════════════════════════
#  POLA PRESET
# ══════════════════════════════════════════════════════════════
PATTERNS = {
    "glider":   [(0,1),(1,2),(2,0),(2,1),(2,2)],
    "beehive":  [(0,1),(0,2),(1,0),(1,3),(2,1),(2,2)],
    "blinker":  [(0,0),(0,1),(0,2)],
    "toad":     [(0,1),(0,2),(0,3),(1,0),(1,1),(1,2)],
    "pulsar":   [
        (0,2),(0,3),(0,4),(0,8),(0,9),(0,10),
        (2,0),(2,5),(2,7),(2,12),(3,0),(3,5),(3,7),(3,12),
        (4,0),(4,5),(4,7),(4,12),(5,2),(5,3),(5,4),(5,8),(5,9),(5,10),
        (7,2),(7,3),(7,4),(7,8),(7,9),(7,10),
        (9,0),(9,5),(9,7),(9,12),(10,0),(10,5),(10,7),(10,12),
        (11,0),(11,5),(11,7),(11,12),(12,2),(12,3),(12,4),(12,8),(12,9),(12,10),
    ],
    "glider_gun": [
        (0,24),(1,22),(1,24),(2,12),(2,13),(2,20),(2,21),(2,34),(2,35),
        (3,11),(3,15),(3,20),(3,21),(3,34),(3,35),(4,0),(4,1),(4,10),(4,16),
        (4,20),(4,21),(5,0),(5,1),(5,10),(5,14),(5,16),(5,17),(5,22),(5,24),
        (6,10),(6,16),(6,24),(7,11),(7,15),(8,12),(8,13),
    ],
}

def place(grid, cells, r0, c0):
    for dr, dc in cells:
        grid[(r0+dr)%ROWS][(c0+dc)%COLS] = 1


# ══════════════════════════════════════════════════════════════
#  UTILITAS TAMPILAN
# ══════════════════════════════════════════════════════════════
def clr():
    print("\033[2J\033[H", end="", flush=True)

def center(text, width, fill=" "):
    raw = strip_ansi(text)
    pad = max(0, width - len(raw))
    l   = pad // 2
    r_  = pad - l
    return fill*l + text + fill*r_

def strip_ansi(s):
    import re
    return re.sub(r'\033\[[0-9;]*m', '', s)

def box_line(content, width):
    raw = strip_ansi(content)
    pad = max(0, width - len(raw))
    return f"{C}{B}║{R}{content}{' '*pad}{C}{B}║{R}"

def sep_line(width, ch="═"):
    return f"{C}{B}╠{ch*width}╣{R}"

def top_line(width):
    return f"{C}{B}╔{'═'*width}╗{R}"

def bot_line(width):
    return f"{C}{B}╚{'═'*width}╝{R}"


# ══════════════════════════════════════════════════════════════
#  LAYAR: SPLASH / LOGO
# ══════════════════════════════════════════════════════════════
LOGO = [
    r"   ██████╗  ██████╗ ██╗      ",
    r"  ██╔════╝ ██╔═══██╗██║      ",
    r"  ██║  ███╗██║   ██║██║      ",
    r"  ██║   ██║██║   ██║██║      ",
    r"  ╚██████╔╝╚██████╔╝███████╗ ",
    r"   ╚═════╝  ╚═════╝ ╚══════╝ ",
]

def show_splash():
    clr()
    W_ = COLS
    print(top_line(W_))
    print(box_line("", W_))
    for line in LOGO:
        colored = f"{G}{B}{line}{R}"
        pad = max(0, W_ - len(line))
        l = pad//2
        print(f"{C}{B}║{R}{' '*l}{colored}{' '*(pad-l)}{C}{B}║{R}")
    print(box_line("", W_))

    sub = f"{Y}{B}Conway's Game of Life{R}"
    print(box_line(center(sub, W_), W_))
    ver = f"{DIM}Simulasi Kehidupan Seluler — v2.0{R}"
    print(box_line(center(ver, W_), W_))
    print(box_line("", W_))
    print(bot_line(W_))
    print()
    print(f"  {DIM}Tekan{R} {W}{B}Enter{R} {DIM}untuk melanjutkan...{R}")
    input()


# ══════════════════════════════════════════════════════════════
#  LAYAR: ATURAN MAIN
# ══════════════════════════════════════════════════════════════
def show_rules():
    clr()
    W_ = COLS
    print(top_line(W_))
    title = f"{Y}{B}  📖  ATURAN MAIN — GAME OF LIFE  📖{R}"
    print(box_line(center(title, W_), W_))
    print(sep_line(W_))

    sections = [
        ("APA ITU GAME OF LIFE?", [
            "Game of Life adalah simulasi sel yang diciptakan oleh",
            "matematikawan John Horton Conway pada tahun 1970.",
            "Bukan permainan biasa — tidak ada menang/kalah.",
            "Ini adalah 'zero-player game' yang berjalan sendiri.",
        ]),
        ("CARA KERJA GRID", [
            f"Grid terdiri dari sel {G}{B}{ALIVE}{R} (hidup) dan {DIM}{DEAD}{R} (mati).",
            "Setiap sel memiliki 8 tetangga di sekitarnya.",
            f"Grid bersifat TOROIDAL: tepi kiri = tepi kanan.",
        ]),
        ("4 ATURAN INTI", [
            f"{Y}1. Underpopulation{R}  : Sel hidup < 2 tetangga → MATI",
            f"{G}2. Survival{R}         : Sel hidup 2-3 tetangga → HIDUP",
            f"{M}3. Overpopulation{R}   : Sel hidup > 3 tetangga → MATI",
            f"{C}4. Reproduction{R}     : Sel mati = 3 tetangga → LAHIR",
        ]),
        ("POLA TERKENAL", [
            f"{G}Still Life{R}   : Pola diam tidak berubah (Beehive)",
            f"{Y}Oscillator{R}   : Pola berulang periodik (Blinker, Pulsar)",
            f"{C}Spaceship{R}    : Pola bergerak melintasi grid (Glider)",
            f"{M}Glider Gun{R}   : Terus menerus menghasilkan Glider baru",
        ]),
    ]

    for heading, lines_ in sections:
        print(box_line("", W_))
        h = f"  {C}{B}▶ {heading}{R}"
        print(box_line(h, W_))
        for ln in lines_:
            print(box_line(f"    {ln}", W_))

    print(box_line("", W_))
    print(sep_line(W_))
    hint = f"{DIM}Tekan{R} {W}{B}Enter{R} {DIM}untuk kembali ke menu...{R}"
    print(box_line(center(hint, W_), W_))
    print(bot_line(W_))
    input()


# ══════════════════════════════════════════════════════════════
#  LAYAR: MENU PILIH POLA
# ══════════════════════════════════════════════════════════════
def show_pattern_menu():
    clr()
    W_ = COLS
    print(top_line(W_))
    title = f"{Y}{B}  🔬  PILIH POLA AWAL  🔬{R}"
    print(box_line(center(title, W_), W_))
    print(sep_line(W_))

    items = [
        ("1", "Acak (Random)",    f"{DIM}Sel hidup tersebar acak ~30% grid{R}"),
        ("2", "Glider",           f"Pola {C}bergerak{R} diagonal (5 sel)"),
        ("3", "Blinker",          f"{Y}Oscillator{R} paling sederhana, period-2"),
        ("4", "Toad",             f"{Y}Oscillator{R} period-2, 6 sel"),
        ("5", "Beehive",          f"{G}Still life{R} berbentuk sarang lebah"),
        ("6", "Pulsar",           f"{Y}Oscillator{R} besar period-3, simetris"),
        ("7", "Glider Gun",       f"{M}Menghasilkan{R} Glider tanpa henti"),
        ("8", "Grid Kosong",      f"{DIM}Mulai dari nol, tambah pola manual{R}"),
    ]

    print(box_line("", W_))
    for key, name, desc in items:
        row = f"  {W}{B}[{key}]{R}  {B}{name:<20}{R}  {desc}"
        print(box_line(row, W_))
        print(box_line("", W_))

    print(sep_line(W_))
    hint = f"{DIM}Masukkan pilihan (1-8) lalu tekan Enter:{R}"
    print(box_line(f"  {hint}", W_))
    print(bot_line(W_))

    while True:
        choice = input(f"\n  {B}Pilihan > {R}").strip()
        if choice in [str(i) for i in range(1,9)]:
            return int(choice)
        print(f"  {RED}Pilihan tidak valid. Masukkan 1-8.{R}")


# ══════════════════════════════════════════════════════════════
#  LAYAR: MENU UTAMA
# ══════════════════════════════════════════════════════════════
def show_main_menu():
    clr()
    W_ = COLS
    print(top_line(W_))
    title = f"{C}{B}  🌱  MENU UTAMA — GAME OF LIFE  🌱{R}"
    print(box_line(center(title, W_), W_))
    print(sep_line(W_))
    print(box_line("", W_))

    menu = [
        ("1", "▶  Mulai Simulasi",     f"{G}Pilih pola & jalankan simulasi{R}"),
        ("2", "📖  Aturan Main",        f"{Y}Baca cara kerja Game of Life{R}"),
        ("3", "🎲  Simulasi Cepat",     f"{C}Langsung mulai dengan pola acak{R}"),
        ("4", "❌  Keluar",             f"{DIM}Tutup program{R}"),
    ]

    for key, name, desc in menu:
        row = f"  {W}{B}[{key}]{R}  {B}{name:<25}{R}  {desc}"
        print(box_line(row, W_))
        print(box_line("", W_))

    print(sep_line(W_))
    hint = f"{DIM}Masukkan pilihan (1-4) lalu tekan Enter:{R}"
    print(box_line(f"  {hint}", W_))
    print(bot_line(W_))

    while True:
        choice = input(f"\n  {B}Pilihan > {R}").strip()
        if choice in ("1","2","3","4"):
            return choice
        print(f"  {RED}Pilihan tidak valid. Masukkan 1-4.{R}")


# ══════════════════════════════════════════════════════════════
#  LAYAR: SIMULASI
# ══════════════════════════════════════════════════════════════
def render_sim(grid, gen, alive, born, died, fps, total_born, total_died, paused):
    W_ = COLS
    lines = []
    lines.append(top_line(W_))

    # Judul + status pause
    pause_tag = f" {RED}{B}[ PAUSED ]{R}" if paused else ""
    title_raw = f"Game of Life{pause_tag}"
    title_col = f"{Y}{B}Game of Life{R}{pause_tag}"
    lines.append(box_line(center(title_col, W_), W_))

    # Statistik
    raw = f"Gen:{gen:5}  Hidup:{alive:5}  Lahir:{born:4}  Mati:{died:4}  FPS:{fps}"
    col = (f"Gen:{Y}{gen:5}{R}  Hidup:{G}{alive:5}{R}  "
           f"Lahir:{G}{born:4}{R}  Mati:{M}{died:4}{R}  FPS:{Y}{fps}{R}")
    p2  = (W_ - len(raw)) // 2
    lines.append(box_line(" "*p2 + col, W_))
    lines.append(sep_line(W_))

    grad = [G, C, C, M, M, C]
    for r_, row in enumerate(grid):
        color = grad[r_ % len(grad)]
        line  = "".join(f"{color}{ALIVE}{R}" if cell else f"{DIM}{DEAD}{R}" for cell in row)
        lines.append(f"{C}{B}║{R}{line}{C}{B}║{R}")

    lines.append(sep_line(W_))
    ctrl = "[SPACE]Pause [r]Acak [c]Hapus [g]Glider [p]Pulsar [+/-]Speed [q]Menu"
    lines.append(box_line(f"{DIM}{center(ctrl,W_)}{R}", W_))
    raw2 = f"Total lahir:{total_born:6}   Total mati:{total_died:6}"
    col2 = f"Total lahir:{G}{total_born:6}{R}   Total mati:{M}{total_died:6}{R}"
    lines.append(box_line(center(col2, W_), W_))
    lines.append(bot_line(W_))
    lines.append(f"\n{B}Perintah > {R}")

    clr()
    print("\n".join(lines), end="", flush=True)


def run_simulation(start_grid):
    grid       = [row[:] for row in start_grid]
    gen        = 0
    fps        = FPS
    total_born = 0
    total_died = 0
    born = died = 0
    paused     = False
    stop       = threading.Event()
    lock       = threading.Lock()

    def sim_loop():
        nonlocal grid, gen, total_born, total_died, born, died, fps, paused
        while not stop.is_set():
            if not paused:
                with lock:
                    grid, born, died = next_gen(grid)
                    gen        += 1
                    total_born += born
                    total_died += died
                    a = alive_count(grid)
                render_sim(grid, gen, a, born, died, fps,
                           total_born, total_died, paused)
            else:
                render_sim(grid, gen, alive_count(grid), born, died, fps,
                           total_born, total_died, paused)
            time.sleep(1.0/fps)

    t = threading.Thread(target=sim_loop, daemon=True)
    t.start()

    try:
        while True:
            cmd = sys.stdin.readline().strip().lower()
            if cmd == 'q':
                break
            elif cmd == ' ' or cmd == 'space':
                paused = not paused
            elif cmd == 'r':
                with lock:
                    grid = random_grid()
                    gen = total_born = total_died = 0
            elif cmd == 'c':
                with lock:
                    grid = empty_grid()
                    gen = total_born = total_died = 0
            elif cmd == 'g':
                with lock:
                    place(grid, PATTERNS["glider"],
                          random.randint(0,ROWS-5), random.randint(0,COLS-5))
            elif cmd == 'p':
                with lock:
                    place(grid, PATTERNS["pulsar"],
                          random.randint(0,ROWS-14), random.randint(0,COLS-14))
            elif cmd == '+':
                fps = min(30, fps+2)
            elif cmd == '-':
                fps = max(1, fps-2)
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        stop.set()


# ══════════════════════════════════════════════════════════════
#  DEMO (non-interaktif / pipe)
# ══════════════════════════════════════════════════════════════
def run_demo():
    print(f"{C}{B}Conway's Game of Life — Mode Demo{R}\n")
    grid = random_grid()
    tb = td = 0
    for gen in range(1, 51):
        grid, b, d = next_gen(grid)
        tb += b; td += d
        if gen % 5 == 0:
            print(f"  Gen {gen:>3} | Hidup:{G}{alive_count(grid):>5}{R} | "
                  f"Lahir:{G}{tb:>5}{R} | Mati:{M}{td:>5}{R}")
        time.sleep(0.04)
    print(f"\n{C}Jalankan di terminal untuk tampilan & menu lengkap!{R}")


# ══════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════
def build_start_grid(choice):
    if choice == 1:   # Acak
        return random_grid()
    elif choice == 2: # Glider
        g = empty_grid()
        place(g, PATTERNS["glider"], ROWS//2, COLS//2)
        return g
    elif choice == 3: # Blinker
        g = empty_grid()
        for _ in range(12):
            place(g, PATTERNS["blinker"],
                  random.randint(0,ROWS-3), random.randint(0,COLS-5))
        return g
    elif choice == 4: # Toad
        g = empty_grid()
        for _ in range(8):
            place(g, PATTERNS["toad"],
                  random.randint(0,ROWS-3), random.randint(0,COLS-6))
        return g
    elif choice == 5: # Beehive
        g = empty_grid()
        for _ in range(10):
            place(g, PATTERNS["beehive"],
                  random.randint(0,ROWS-4), random.randint(0,COLS-6))
        return g
    elif choice == 6: # Pulsar
        g = empty_grid()
        place(g, PATTERNS["pulsar"], 4, 20)
        return g
    elif choice == 7: # Glider Gun
        g = empty_grid()
        place(g, PATTERNS["glider_gun"], 2, 1)
        return g
    elif choice == 8: # Kosong
        return empty_grid()

def main():
    if not sys.stdin.isatty():
        run_demo()
        return

    show_splash()

    while True:
        choice = show_main_menu()

        if choice == "1":
            pat = show_pattern_menu()
            grid = build_start_grid(pat)
            run_simulation(grid)

        elif choice == "2":
            show_rules()

        elif choice == "3":
            run_simulation(random_grid())

        elif choice == "4":
            clr()
            print(f"\n  {C}{B}Terima kasih telah bermain Game of Life! 👋{R}\n")
            break

if __name__ == "__main__":
    main()
    
    