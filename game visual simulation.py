import sys
import time
import os
from collections import deque

# ─────────────────────────────────────────────
#  MAZE  (# = wall, S = start, E = exit)
# ─────────────────────────────────────────────
RAW_MAZE = [
    "####################",
    "#S  #     #        #",
    "# ## # ## # ##### ##",
    "# #  #  # #     #  #",
    "# # ## ## ##### # ##",
    "#   #  #     #  #  #",
    "### # ### ## # ### #",
    "#   #   # #  #   # #",
    "# ### # # # ### # ##",
    "# #   # # #   # #  #",
    "# # ### # ### # ## #",
    "#   #   #   # #    #",
    "# ### ####### # ## #",
    "#   #         #  # #",
    "### ########### # ##",
    "#   #       #   #  #",
    "# ### ##### # ###  #",
    "#     #     #   #  #",
    "####### ######### ##",
    "#                 E#",
    "####################",
]

ROWS = len(RAW_MAZE)
COLS = len(RAW_MAZE[0])
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# ─────────────────────────────────────────────
#  WARNA TERMINAL (ANSI)
# ─────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"

BG_WALL    = "\033[48;5;17m"
BG_OPEN    = "\033[48;5;255m"
BG_VISITED = "\033[48;5;117m"
BG_PATH    = "\033[48;5;85m"
BG_CURRENT = "\033[48;5;33m"
BG_START   = "\033[48;5;35m"
BG_END     = "\033[48;5;214m"

FG_WHITE   = "\033[97m"
FG_DARK    = "\033[30m"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


# ─────────────────────────────────────────────
#  PARSE MAZE
# ─────────────────────────────────────────────
def parse_maze():
    grid = []
    start = end = None
    for r, row in enumerate(RAW_MAZE):
        line = list(row.ljust(COLS, "#"))
        grid.append(line)
        for c, ch in enumerate(line):
            if ch == "S":
                start = (r, c)
            elif ch == "E":
                end = (r, c)
    return grid, start, end


# ─────────────────────────────────────────────
#  SOLVER : BFS
# ─────────────────────────────────────────────
def bfs(grid, start, end):
    visited = {start}
    prev = {start: None}
    queue = deque([start])
    steps = []

    while queue:
        cur = queue.popleft()
        steps.append((frozenset(visited), cur, None))
        if cur == end:
            break
        r, c = cur
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            nk = (nr, nc)
            if 0 <= nr < ROWS and 0 <= nc < COLS \
               and nk not in visited and grid[nr][nc] != "#":
                visited.add(nk)
                prev[nk] = cur
                queue.append(nk)

    path = []
    node = end
    while node:
        path.append(node)
        node = prev.get(node)
    steps.append((frozenset(visited), None, frozenset(path)))
    return steps


# ─────────────────────────────────────────────
#  SOLVER : DFS
# ─────────────────────────────────────────────
def dfs(grid, start, end):
    visited = set()
    prev = {start: None}
    stack = [start]
    steps = []

    while stack:
        cur = stack.pop()
        if cur in visited:
            continue
        visited.add(cur)
        steps.append((frozenset(visited), cur, None))
        if cur == end:
            break
        r, c = cur
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            nk = (nr, nc)
            if 0 <= nr < ROWS and 0 <= nc < COLS \
               and nk not in visited and grid[nr][nc] != "#":
                if nk not in prev:
                    prev[nk] = cur
                stack.append(nk)

    path = []
    node = end
    while node:
        path.append(node)
        node = prev.get(node)
    steps.append((frozenset(visited), None, frozenset(path)))
    return steps


# ─────────────────────────────────────────────
#  RENDER MAZE KE TERMINAL
# ─────────────────────────────────────────────
def render(grid, visited, current, path, step_num, total, algo_name, done):
    lines = []
    lines.append(BOLD + "=" * 46 + RESET)
    lines.append(BOLD + "   MAZE SOLVER  —  " + algo_name + RESET)
    lines.append(BOLD + "=" * 46 + RESET)

    for r in range(ROWS):
        row_str = ""
        for c in range(COLS):
            ch = grid[r][c]
            pos = (r, c)
            if ch == "S":
                row_str += BG_START + FG_WHITE + BOLD + " S" + RESET
            elif ch == "E":
                row_str += BG_END + FG_DARK + BOLD + " E" + RESET
            elif ch == "#":
                row_str += BG_WALL + FG_WHITE + "██" + RESET
            elif path and pos in path:
                row_str += BG_PATH + FG_DARK + " *" + RESET
            elif current and pos == current:
                row_str += BG_CURRENT + FG_WHITE + " @" + RESET
            elif visited and pos in visited:
                row_str += BG_VISITED + FG_DARK + " ." + RESET
            else:
                row_str += BG_OPEN + FG_DARK + "  " + RESET
        lines.append(row_str)

    lines.append("")
    bar_len = 40
    filled = int(bar_len * min(step_num / max(total, 1), 1.0))
    bar = "█" * filled + "░" * (bar_len - filled)
    pct = int(100 * min(step_num / max(total, 1), 1.0))
    lines.append(f"  Langkah : {step_num:>4} / {total}   [{bar}] {pct}%")

    if done:
        path_len = len(path) if path else 0
        lines.append(f"\n  Selesai! Panjang jalur: {path_len} sel | Dijelajahi: {len(visited)} sel")
    else:
        lines.append(f"\n  Menjelajahi... (Ctrl+C untuk berhenti)")

    lines.append("")
    lines.append(
        "  LEGENDA: " +
        BG_START   + " S " + RESET + " Start  " +
        BG_END     + " E " + RESET + " Exit  " +
        BG_CURRENT + " @ " + RESET + " Saat ini  " +
        BG_VISITED + " . " + RESET + " Dijelajahi  " +
        BG_PATH    + " * " + RESET + " Jalur  " +
        BG_WALL    + "██" + RESET + " Dinding"
    )
    lines.append("")

    sys.stdout.write("\033[H")
    sys.stdout.write("\n".join(lines))
    sys.stdout.flush()


# ─────────────────────────────────────────────
#  MENU
# ─────────────────────────────────────────────
def menu():
    clear()
    print(BOLD + "=" * 46 + RESET)
    print(BOLD + "      MAZE SOLVER — PILIH ALGORITMA" + RESET)
    print(BOLD + "=" * 46 + RESET)
    print()
    print("  [1]  BFS  — Breadth-First Search (jalur terpendek)")
    print("  [2]  DFS  — Depth-First Search")
    print()
    while True:
        choice = input("  Pilihan (1/2): ").strip()
        if choice in ("1", "2"):
            break
        print("  Masukkan 1 atau 2.")

    print()
    print("  Kecepatan animasi:")
    print("  [1] Lambat   [2] Normal   [3] Cepat   [4] Turbo (tanpa animasi)")
    while True:
        spd = input("  Pilihan (1-4): ").strip()
        if spd in ("1", "2", "3", "4"):
            break
        print("  Masukkan 1, 2, 3, atau 4.")

    algo = "BFS" if choice == "1" else "DFS"
    delays = [0.08, 0.03, 0.008, 0]
    delay = delays[int(spd) - 1]
    return algo, delay


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    # aktifkan warna ANSI di Windows
    if os.name == "nt":
        os.system("color")
        try:
            import ctypes
            kernel = ctypes.windll.kernel32
            kernel.SetConsoleMode(kernel.GetStdHandle(-11), 7)
        except Exception:
            pass

    grid, start, end = parse_maze()

    while True:
        algo, delay = menu()

        print("\033[2J\033[H", end="")

        steps = bfs(grid, start, end) if algo == "BFS" else dfs(grid, start, end)
        total = len(steps)

        try:
            for i, (vis, cur, pth) in enumerate(steps):
                done = (pth is not None)
                render(grid, vis, cur, pth, i + 1, total, algo, done)
                if delay > 0:
                    time.sleep(delay)
        except KeyboardInterrupt:
            pass

        print()
        again = input("  Jalankan lagi? (y/n): ").strip().lower()
        if again != "y":
            print()
            print("  Terima kasih! Program selesai.")
            print()
            break


if __name__ == "__main__":
    main()
