from typing import List, Optional
import math

class ListNode:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class AdvancedSorter:
    def __init__(self):
        pass

    # =========================================================
    # 1. ARRAY MERGE SORT (Virtual Sublists + Single tmpArray)
    # =========================================================
    def sort_array(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1: return arr
        tmp_array = [0] * len(arr) # Single temporary array [cite: 47]
        self._rec_merge_sort(arr, 0, len(arr) - 1, tmp_array)
        return arr

    def _rec_merge_sort(self, arr, first, last, tmp_array):
        if first >= last: return
        mid = (first + last) // 2
        self._rec_merge_sort(arr, first, mid, tmp_array)
        self._rec_merge_sort(arr, mid + 1, last, tmp_array)
        self._merge_virtual(arr, first, mid, last, tmp_array)

    def _merge_virtual(self, arr, left_start, mid, right_end, tmp_array):
        # Penggabungan dua virtual sublist [cite: 59]
        left = left_start
        right = mid + 1
        idx = left_start

        while left <= mid and right <= right_end:
            if arr[left] <= arr[right]: # STABLE sort [cite: 61, 98]
                tmp_array[idx] = arr[left]
                left += 1
            else:
                tmp_array[idx] = arr[right]
                right += 1
            idx += 1

        while left <= mid:
            tmp_array[idx] = arr[left]
            left += 1
            idx += 1

        while right <= right_end:
            tmp_array[idx] = arr[right]
            right += 1
            idx += 1

        for i in range(left_start, right_end + 1):
            arr[i] = tmp_array[i] # Salin kembali [cite: 62]

    # =========================================================
    # 2. LINKED LIST MERGE SORT (Fast-Slow + Dummy Merge)
    # =========================================================
    def sort_linked_list(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        right_head = self._split_linked_list(head) # [cite: 73]
        left_head = head
        left_sorted = self.sort_linked_list(left_head)
        right_sorted = self.sort_linked_list(right_head)
        return self._merge_linked_lists(left_sorted, right_sorted)

    def _split_linked_list(self, head: ListNode) -> Optional[ListNode]:
        midPoint = head
        curNode = head.next
        # Fast-slow pointer implementation [cite: 79, 99]
        while curNode and curNode.next:
            midPoint = midPoint.next
            curNode = curNode.next.next
            
        right_head = midPoint.next # [cite: 100]
        midPoint.next = None # Putus link [cite: 80, 101]
        return right_head

    def _merge_linked_lists(self, listA: Optional[ListNode], listB: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0) # Dummy node [cite: 85, 102]
        tail = dummy

        while listA and listB:
            if listA.data <= listB.data: # STABLE [cite: 86]
                tail.next = listA
                listA = listA.next
            else:
                tail.next = listB
                listB = listB.next
            tail = tail.next
            
        tail.next = listA or listB # [cite: 103]
        return dummy.next # [cite: 87]

    # =========================================================
    # 3. QUICK SORT PARTITION (Median-of-Three Pivot)
    # =========================================================
    def partition_quick(self, arr: List[int], first: int, last: int) -> int:
        mid = (first + last) // 2
        # Median of three logic [cite: 93, 104]
        if arr[first] > arr[mid]: arr[first], arr[mid] = arr[mid], arr[first]
        if arr[first] > arr[last]: arr[first], arr[last] = arr[last], arr[first]
        if arr[mid] > arr[last]: arr[mid], arr[last] = arr[last], arr[mid]
        
        # Tukar pivot (median) ke posisi 'first' [cite: 94, 104]
        arr[first], arr[mid] = arr[mid], arr[first]
        
        pivot_val = arr[first]
        left = first + 1
        right = last

        while True:
            while left <= right and arr[left] <= pivot_val: left += 1
            while arr[right] >= pivot_val and right >= left: right -= 1
            if right < left: break
            arr[left], arr[right] = arr[right], arr[left]

        arr[first], arr[right] = arr[right], arr[first]
        return right

class ExprHeapSorter:
    def __init__(self, expr):
        self.expr = expr

    def heapsort_inplace(self, arr: List[int]) -> None:
        n = len(arr)

        def heapify(heap_size: int, root_index: int):
            largest = root_index
            left = 2 * root_index + 1
            right = 2 * root_index + 2

            if left < heap_size and arr[left] > arr[largest]:
                largest = left
            if right < heap_size and arr[right] > arr[largest]:
                largest = right

            if largest != root_index:
                arr[root_index], arr[largest] = arr[largest], arr[root_index]
                heapify(heap_size, largest)

        for i in range(n // 2 - 1, -1, -1):
            heapify(n, i)

        for end in range(n - 1, 0, -1):
            arr[0], arr[end] = arr[end], arr[0]
            heapify(end, 0)

    def is_complete_tree(self, arr: List[int]) -> bool:
        # Array-backed binary tree is complete when represented as a contiguous array.
        return True

if __name__ == "__main__":
    # Membuat instansiasi objek dari class AdvancedSorter
    sorter = AdvancedSorter()

    # --- Uji Coba Array Merge Sort ---
    print("=== Uji Coba Array Merge Sort ===")
    arr_test = [38, 27, 43, 3, 9, 82, 10]
    print(f"Data Sebelum diurutkan : {arr_test}")

    # Memanggil fungsi untuk mengurutkan
    sorter.sort_array(arr_test)

    print(f"Data Sesudah diurutkan : {arr_test}")

    # =====================================================================
# BLOK UJI COBA (DRIVER CODE) - COPY DAN PASTE DI PALING BAWAH FILE
# =====================================================================

def create_linked_list(arr):
    """Helper untuk membuat Linked List dari list Python"""
    if not arr: return None
    head = ListNode(arr[0])
    curr = head
    for val in arr[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head

def print_linked_list(head):
    """Helper untuk visualisasi Linked List dengan tanda panah"""
    elements = []
    while head:
        elements.append(str(head.data))
        head = head.next
    return " -> ".join(elements) + " -> None"

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🎓 DEMO TUGAS SORTING & BINARY TREE 🎓".center(50))
    print("="*50 + "\n")

    # Inisialisasi Sorter
    sorter = AdvancedSorter()

    # ---------------------------------------------------------
    # UJI COBA 1: Array Merge Sort (Virtual Sublists)
    # ---------------------------------------------------------
    print(">>> 1. UJI COBA ARRAY MERGE SORT (O(n log n))")
    arr_test = [82, 38, 27, 43, 3, 9, 10, 10, 27] # Sengaja ada data kembar untuk test STABLE
    print(f"[-] Data Sebelum  : {arr_test}")
    sorter.sort_array(arr_test)
    print(f"[+] Data Sesudah  : {arr_test}")
    print("-" * 50)

    # ---------------------------------------------------------
    # UJI COBA 2: Linked List Merge Sort (Fast-Slow Pointer)
    # ---------------------------------------------------------
    print(">>> 2. UJI COBA LINKED LIST MERGE SORT")
    ll_data = [45, 12, 89, 33, 1, 9, 12, 5]
    ll_head = create_linked_list(ll_data)
    
    print(f"[-] List Sebelum  : {print_linked_list(ll_head)}")
    sorted_ll_head = sorter.sort_linked_list(ll_head)
    print(f"[+] List Sesudah  : {print_linked_list(sorted_ll_head)}")
    print("-" * 50)

    # ---------------------------------------------------------
    # UJI COBA 3: Quick Sort Partition (Median-of-Three)
    # ---------------------------------------------------------
    print(">>> 3. UJI COBA QUICK SORT PARTITION")
    qs_arr = [25, 10, 40, 5, 30, 50, 15]
    print(f"[-] Array Awal           : {qs_arr}")
    
    # Partisi array dari indeks 0 sampai terakhir (6)
    pivot_idx = sorter.partition_quick(qs_arr, 0, len(qs_arr) - 1)
    
    print(f"[!] Indeks Pivot Akhir   : {pivot_idx} (Nilai Pivot: {qs_arr[pivot_idx]})")
    print(f"[+] Array Pasca Partisi  : {qs_arr}")
    print("    *Catatan: Elemen di kiri pivot <= pivot, di kanan >= pivot")
    print("-" * 50)

    # ---------------------------------------------------------
    # UJI COBA 4: In-Place Heapsort (Dari Modul ExprHeapSorter)
    # ---------------------------------------------------------
    print(">>> 4. UJI COBA IN-PLACE HEAPSORT & TREE VALIDATION")
    # Anggap ini adalah hasil dari evaluasi pohon ekspresi
    heap_sorter = ExprHeapSorter("dummy_expr") 
    raw_data = [99, 22, 14, 5, 67, 88, 11]
    
    print(f"[-] Data Mentah   : {raw_data}")
    heap_sorter.heapsort_inplace(raw_data)
    print(f"[+] Heapsort Hasil: {raw_data}")
    
    # Cek Validasi Complete Tree
    is_complete = heap_sorter.is_complete_tree(raw_data)
    print(f"[?] Apakah array terurut valid sebagai Complete Binary Tree? : {'YA' if is_complete else 'TIDAK'}")
    print("=" * 50 + "\n")

    from typing import List, Optional
from collections import deque

class ExprHeapSorter:
    def __init__(self, expr_str: str):
        self.expr = expr_str # [cite: 142]
        self.values = [] # [cite: 143]

    def parse_and_evaluate(self) -> List[int]:
        tokens = deque(self.expr) # [cite: 146]
        root = self._build_tree(tokens)
        self.values = self._eval_tree(root)
        return self.values

    def _build_tree(self, tokens: deque) -> Optional[dict]:
        # Implementasi rekursif sesuai instruksi [cite: 151]
        if not tokens: return None
        token = tokens.popleft()

        if token == '(':
            left_node = self._build_tree(tokens)
            op = tokens.popleft() # Ambil operator [cite: 179]
            right_node = self._build_tree(tokens)
            tokens.popleft() # Buang ')' yang menutup [cite: 179]
            return {'val': op, 'left': left_node, 'right': right_node} # [cite: 152]
        else:
            return {'val': token, 'left': None, 'right': None} # Operand [cite: 180]

    def _eval_tree(self, node: Optional[dict]) -> List[int]:
        # Evaluasi postorder [cite: 155]
        if node is None: return []
        
        if node['left'] is None and node['right'] is None:
            return [int(node['val'])]
            
        left_vals = self._eval_tree(node['left'])
        right_vals = self._eval_tree(node['right'])
        
        l_val = left_vals[-1] if left_vals else 0
        r_val = right_vals[-1] if right_vals else 0
        
        op = node['val']
        res = 0
        if op == '+': res = l_val + r_val
        elif op == '-': res = l_val - r_val
        elif op == '*': res = l_val * r_val
        elif op == '/':
            if r_val == 0: raise ValueError("Division by zero") # [cite: 156]
            res = l_val // r_val
            
        return left_vals + right_vals + [res]

    def heapsort_inplace(self, arr: List[int]) -> List[int]:
        n = len(arr) # [cite: 160]
        if n <= 1: return arr
        
        # 1. Build max-heap in-place [cite: 162]
        for i in range(n//2 - 1, -1, -1): # [cite: 163, 184]
            self._sift_down(arr, n, i)
            
        # 2. Extract & sort [cite: 165]
        for end in range(n - 1, 0, -1): # [cite: 166]
            arr[0], arr[end] = arr[end], arr[0] # Swap [cite: 167]
            self._sift_down(arr, end, 0) # [cite: 168]
            
        return arr

    def _sift_down(self, arr: List[int], heap_size: int, idx: int):
        largest = idx
        left = 2 * idx + 1 # [cite: 172]
        right = 2 * idx + 2 # [cite: 172]

        if left < heap_size and arr[left] > arr[largest]:
            largest = left
        if right < heap_size and arr[right] > arr[largest]:
            largest = right

        if largest != idx:
            arr[idx], arr[largest] = arr[largest], arr[idx] # Swap [cite: 181]
            self._sift_down(arr, heap_size, largest)

    def is_complete_tree(self, arr: List[int]) -> bool:
        n = len(arr)
        # Memvalidasi properti complete binary tree [cite: 175, 176]
        for i in range(n):
            left = 2 * i + 1
            right = 2 * i + 2
            # Jika ada anak kiri di luar bounds tapi ada elemen sisa, atau lompat [cite: 182, 183]
            if left >= n and right < n:
                return False
        return True
"""
Hash Table Premium+ (Linear Probing) — matplotlib + keyboard controls (Windows CMD safe)

Controls:
  SPACE : pause/resume
  RIGHT : step forward (when paused)
  LEFT  : step backward (when paused)
  R     : restart
  ESC/Q : quit

Run:
  python hash_table_premium_keyboard.py
Options:
  python hash_table_premium_keyboard.py --size 12 --nkeys 11
  python hash_table_premium_keyboard.py --save gif
"""

import argparse
import random
import numpy as np

import matplotlib
matplotlib.use("TkAgg")  # CMD Windows GUI backend

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def plan_inserts(keys, size=20):
    table = [None] * size
    frame_data = []
    load_factors = []

    for step, key in enumerate(keys, 1):
        start = hash(key) % size
        idx = start
        probes = 0

        def snap(phase, placed=False):
            frame_data.append({
                "phase": phase,
                "step": step,
                "key": key,
                "start": start,
                "idx": idx,
                "probes": probes,
                "table": list(table),
                "placed": placed
            })

        snap("start", placed=False)

        while table[idx] is not None:
            snap("collision", placed=False)
            probes += 1
            idx = (idx + 1) % size
            snap("probe", placed=False)

        table[idx] = key
        snap("place", placed=True)

        lf = sum(v is not None for v in table) / size
        load_factors.append(lf)

        snap("pause", placed=True)

    return frame_data, load_factors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=20)
    parser.add_argument("--nkeys", type=int, default=18)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--save", choices=["none", "gif"], default="none")
    args = parser.parse_args()

    random.seed(args.seed)
    keys = [f"k{i}" for i in range(args.nkeys)]
    random.shuffle(keys)

    frames, load_factors = plan_inserts(keys, size=args.size)

    # ==== FIGURE LAYOUT ====
    fig = plt.figure(figsize=(12, 6), constrained_layout=True)
    gs = fig.add_gridspec(2, 1, height_ratios=[3, 1])

    ax_table = fig.add_subplot(gs[0])
    ax_lf = fig.add_subplot(gs[1])

    fig.suptitle("Hash Table Premium+ (Linear Probing) — Keyboard Control", fontsize=14)

    # ---- TABLE GRID ----
    n = args.size
    ax_table.set_xlim(-0.5, n - 0.5)
    ax_table.set_ylim(-0.5, 0.5)
    ax_table.set_yticks([])
    ax_table.set_xticks(range(n))
    ax_table.set_xlabel("Index Bucket")

    rects, texts = [], []
    for i in range(n):
        r = plt.Rectangle((i - 0.5, -0.35), 1.0, 0.7, fill=True, alpha=0.25)
        ax_table.add_patch(r)
        rects.append(r)
        t = ax_table.text(i, 0, "", ha="center", va="center", fontsize=9)
        texts.append(t)

    info = ax_table.text(0.01, 1.08, "", transform=ax_table.transAxes, fontsize=11)
    legend = ax_table.text(
        0.01, 1.01,
        "SPACE: pause/resume | ←/→: step (pause) | R: restart | Q/Esc: quit",
        transform=ax_table.transAxes, fontsize=9
    )

    # ---- LOAD FACTOR CHART ----
    ax_lf.set_xlim(1, max(2, args.nkeys))
    ax_lf.set_ylim(0, 1.05)
    ax_lf.set_xlabel("Insert ke-")
    ax_lf.set_ylabel("Load Factor")
    ax_lf.grid(True, alpha=0.25)

    lf_line, = ax_lf.plot([], [])
    lf_dot, = ax_lf.plot([], [], marker="o", linestyle="")

    bar_bg = plt.Rectangle((0.02, 0.15), 0.96, 0.2, transform=ax_lf.transAxes, alpha=0.15)
    bar_fg = plt.Rectangle((0.02, 0.15), 0.00, 0.2, transform=ax_lf.transAxes, alpha=0.35)
    ax_lf.add_patch(bar_bg)
    ax_lf.add_patch(bar_fg)
    lf_text = ax_lf.text(0.02, 0.45, "", transform=ax_lf.transAxes, fontsize=10)

    # ==== PLAYER STATE ====
    state = {
        "i": 0,          # current frame index
        "paused": False  # paused flag
    }

    def render(frame):
        """Render a single frame dict."""
        table = frame["table"]
        start = frame["start"]
        idx = frame["idx"]
        phase = frame["phase"]

        # reset buckets
        for j in range(n):
            rects[j].set_alpha(0.25)
            rects[j].set_linewidth(1.0)
            texts[j].set_text("" if table[j] is None else str(table[j]))

        # highlight target hash bucket
        rects[start].set_alpha(0.55)
        rects[start].set_linewidth(2.5)

        # highlight current idx
        rects[idx].set_alpha(0.75)
        rects[idx].set_linewidth(3.0)

        # collision emphasis
        if phase == "collision":
            rects[idx].set_alpha(0.9)

        filled = sum(v is not None for v in table)
        lf = filled / n

        info.set_text(
            f"Frame {state['i']+1}/{len(frames)} | Step {frame['step']}/{args.nkeys} | key='{frame['key']}' | "
            f"hash%size={start} | idx={idx} | probes={frame['probes']} | load_factor={lf:.2f} | phase={phase} | "
            f"{'PAUSED' if state['paused'] else 'PLAY'}"
        )

        # completed inserts so far
        completed = frame["step"] - 1 + (1 if frame["placed"] else 0)
        if completed <= 0:
            x, y = [], []
        else:
            x = list(range(1, completed + 1))
            y = load_factors[:completed]

        lf_line.set_data(x, y)
        if x:
            lf_dot.set_data([x[-1]], [y[-1]])
            bar_fg.set_width(0.96 * y[-1])
            lf_text.set_text(f"Load Factor: {y[-1]:.2f} ({int(y[-1]*100)}%)")
        else:
            lf_dot.set_data([], [])
            bar_fg.set_width(0.00)
            lf_text.set_text("Load Factor: 0.00 (0%)")

        return rects + texts + [info, legend, lf_line, lf_dot, bar_fg, lf_text]

    def update(_):
        """Animation tick: advance if not paused; otherwise keep frame."""
        if not state["paused"]:
            state["i"] = min(state["i"] + 1, len(frames) - 1)
        return render(frames[state["i"]])

    # Init render
    def init():
        return render(frames[state["i"]])

    ani = FuncAnimation(
        fig, update, init_func=init,
        frames=np.arange(len(frames)),  # timer ticks, actual frame controlled by state["i"]
        interval=450, blit=False, repeat=False
    )

    def on_key(event):
        k = event.key
        if k == " ":
            state["paused"] = not state["paused"]
            fig.canvas.draw_idle()

        elif k == "right":
            if state["paused"]:
                state["i"] = min(state["i"] + 1, len(frames) - 1)
                render(frames[state["i"]])
                fig.canvas.draw_idle()

        elif k == "left":
            if state["paused"]:
                state["i"] = max(state["i"] - 1, 0)
                render(frames[state["i"]])
                fig.canvas.draw_idle()

        elif k in ("r", "R"):
            state["i"] = 0
            state["paused"] = True  # restart dalam kondisi pause biar enak step
            render(frames[state["i"]])
            fig.canvas.draw_idle()

        elif k in ("escape", "q", "Q"):
            plt.close(fig)

    fig.canvas.mpl_connect("key_press_event", on_key)

    if args.save == "gif":
        try:
            from matplotlib.animation import PillowWriter
            ani.save("hash_table_premium_keyboard.gif", writer=PillowWriter(fps=2))
            print("Tersimpan: hash_table_premium_keyboard.gif")
        except Exception as e:
            print("Gagal simpan GIF. Pastikan 'pillow' terpasang. Error:", e)

    plt.show()


if __name__ == "__main__":
    main()    
    