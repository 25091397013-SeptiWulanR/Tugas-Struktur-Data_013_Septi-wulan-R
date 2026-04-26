import tkinter as tk
from tkinter import ttk, messagebox
import random
from collections import deque
from dataclasses import dataclass
from datetime import datetime
import threading
import time

# ===== PRINTER QUEUE =====
class PrinterQueue:
    def __init__(self):
        self.queue = deque()
        self.printed = []
    
    def enqueue(self, doc):
        self.queue.append(doc)
    
    def dequeue(self):
        if len(self.queue) > 0:
            doc = self.queue.popleft()
            self.printed.append(doc)
            return doc
        return None
    
    def get_queue(self):
        return list(self.queue)
    
    def get_printed(self):
        return self.printed
    
    def reset(self):
        self.queue = deque()
        self.printed = []


# ===== HOT POTATO =====
class HotPotatoGame:
    def __init__(self, num_players):
        self.players = [{"name": f"P{i+1}", "eliminated": False} for i in range(num_players)]
        self.current_idx = 0
        self.logs = []
    
    def play_round(self, oper_count):
        remaining = sum(1 for p in self.players if not p["eliminated"])
        if remaining <= 1:
            return None
        
        # Oper
        for _ in range(oper_count):
            while True:
                self.current_idx = (self.current_idx + 1) % len(self.players)
                if not self.players[self.current_idx]["eliminated"]:
                    break
        
        # Tersingkir
        self.players[self.current_idx]["eliminated"] = True
        self.logs.append(f"{self.players[self.current_idx]['name']} tersingkir!")
        
        # Cek pemenang
        remaining = sum(1 for p in self.players if not p["eliminated"])
        if remaining == 1:
            winner = next(p for p in self.players if not p["eliminated"])
            self.logs.append(f"🎉 Pemenang: {winner['name']}")
            return winner["name"]
        
        # Lanjut ke pemain berikutnya
        while True:
            self.current_idx = (self.current_idx + 1) % len(self.players)
            if not self.players[self.current_idx]["eliminated"]:
                break
        
        return None
    
    def get_state(self):
        return {
            "players": self.players,
            "current_idx": self.current_idx,
            "logs": self.logs
        }
    
    def reset(self):
        self.players = []
        self.current_idx = 0
        self.logs = []


# ===== HOSPITAL PRIORITY QUEUE =====
@dataclass
class Patient:
    name: str
    priority: int
    time: str

class HospitalQueue:
    def __init__(self):
        self.queues = [deque() for _ in range(4)]
        self.served = []
    
    def add_patient(self, name, priority):
        patient = Patient(name, priority, datetime.now().strftime("%H:%M:%S"))
        self.queues[priority].append(patient)
    
    def serve_patient(self):
        for i in range(4):
            if len(self.queues[i]) > 0:
                patient = self.queues[i].popleft()
                self.served.append(patient)
                return patient
        return None
    
    def get_all_waiting(self):
        all_patients = []
        for priority in range(4):
            for patient in self.queues[priority]:
                all_patients.append((patient, priority))
        return all_patients
    
    def get_served(self):
        return self.served
    
    def reset(self):
        self.queues = [deque() for _ in range(4)]
        self.served = []


# ===== BFS GRAPH =====
class BFSGraph:
    def __init__(self):
        self.graph = {
            'A': ['B', 'C'],
            'B': ['A', 'D', 'E'],
            'C': ['A', 'F'],
            'D': ['B'],
            'E': ['B', 'F'],
            'F': ['C', 'E']
        }
        self.visited = set()
        self.queue = deque()
        self.order = []
        self.started = False
    
    def init_bfs(self):
        self.visited = set()
        self.queue = deque()
        self.order = []
        self.started = True
        
        self.queue.append('A')
        self.visited.add('A')
    
    def step_bfs(self):
        if not self.started:
            self.init_bfs()
        
        if len(self.queue) == 0:
            return False
        
        node = self.queue.popleft()
        self.order.append(node)
        
        for neighbor in self.graph[node]:
            if neighbor not in self.visited:
                self.visited.add(neighbor)
                self.queue.append(neighbor)
        
        return True
    
    def get_state(self):
        levels = {
            0: ['A'],
            1: ['B', 'C'],
            2: ['D', 'E', 'F']
        }
        
        state = {}
        for level, nodes in levels.items():
            state[level] = []
            for node in nodes:
                if node in self.order:
                    state[level].append((node, 'visited'))
                elif node in self.queue:
                    state[level].append((node, 'queued'))
                elif node in self.visited:
                    state[level].append((node, 'queued'))
                else:
                    state[level].append((node, 'unvisited'))
        
        return state
    
    def reset(self):
        self.visited = set()
        self.queue = deque()
        self.order = []
        self.started = False


# ===== SIMULATION =====
class TicketSimulation:
    def __init__(self):
        self.events = []
        self.stats = {}
    
    def run(self, num_agents):
        num_minutes = 480
        between_time = 10
        service_time = 3
        
        customer_queue = deque()
        agents = [{'free_at': 0, 'customer_id': None} for _ in range(num_agents)]
        total_wait = 0
        customers_served = 0
        self.events = []
        
        customer_count = 0
        
        for minute in range(num_minutes + 1):
            # Arrival
            if random.random() < 1 / between_time:
                customer_count += 1
                customer_queue.append({'id': customer_count, 'arrive_time': minute})
                self.events.append(f"T={minute:3d}: Customer {customer_count} tiba")
            
            # Begin service
            for idx, agent in enumerate(agents):
                if agent['free_at'] <= minute and len(customer_queue) > 0:
                    customer = customer_queue.popleft()
                    wait = minute - customer['arrive_time']
                    total_wait += wait
                    agent['customer_id'] = customer['id']
                    agent['free_at'] = minute + service_time
                    customers_served += 1
                    self.events.append(f"T={minute:3d}: Agen {idx+1} layani customer {customer['id']} (tunggu {wait}min)")
        
        avg_wait = total_wait / customers_served if customers_served > 0 else 0
        
        self.stats = {
            'customers_served': customers_served,
            'avg_wait': round(avg_wait, 2),
            'remaining': len(customer_queue),
            'num_agents': num_agents
        }
    
    def get_events(self):
        return self.events[-25:]
    
    def get_stats(self):
        return self.stats
    
    def reset(self):
        self.events = []
        self.stats = {}


# ===== GUI APPLICATION =====
class QueueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Queue - 5 Kasus Implementasi")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize data models
        self.printer = PrinterQueue()
        self.potato = HotPotatoGame(0)
        self.hospital = HospitalQueue()
        self.bfs = BFSGraph()
        self.simulation = TicketSimulation()
        
        self.current_case = 0
        
        # Create header
        self.create_header()
        
        # Create tabs
        self.create_tabs()
        
        # Create case containers
        self.containers = []
        self.create_case1()  # Printer
        self.create_case2()  # Hot Potato
        self.create_case3()  # Hospital
        self.create_case4()  # BFS
        self.create_case5()  # Simulation
        
        # Show first case
        self.switch_case(0)
    
    def create_header(self):
        header_frame = tk.Frame(self.root, bg="#667eea", height=80)
        header_frame.pack(fill=tk.X)
        
        title = tk.Label(
            header_frame,
            text="📊 Queue - 5 Kasus Implementasi",
            font=("Helvetica", 24, "bold"),
            bg="#667eea",
            fg="white"
        )
        title.pack(pady=20)
    
    def create_tabs(self):
        tab_frame = tk.Frame(self.root, bg="#f0f0f0")
        tab_frame.pack(fill=tk.X, padx=10, pady=10)
        
        buttons = [
            ("🖨️ Printer", 0),
            ("🥔 Hot Potato", 1),
            ("🏥 Rumah Sakit", 2),
            ("📈 BFS Graph", 3),
            ("✈️ Tiket Bandara", 4)
        ]
        
        self.tab_buttons = []
        for text, idx in buttons:
            btn = tk.Button(
                tab_frame,
                text=text,
                command=lambda i=idx: self.switch_case(i),
                bg="white",
                fg="#667eea",
                font=("Helvetica", 10, "bold"),
                padx=20,
                pady=10,
                relief=tk.FLAT,
                bd=2
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.tab_buttons.append(btn)
    
    def create_case1(self):
        """PRINTER QUEUE"""
        container = tk.Frame(self.root, bg="white")
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title = tk.Label(
            container,
            text="🖨️ Kasus 1: Antrian Printer Bersama",
            font=("Helvetica", 16, "bold"),
            bg="white",
            fg="#667eea"
        )
        title.pack(pady=10)
        
        desc = tk.Label(
            container,
            text="Dokumen dicetak sesuai urutan kedatangan (FIFO).",
            font=("Helvetica", 10),
            bg="white",
            fg="#666"
        )
        desc.pack(pady=5)
        
        # Control panel
        control = tk.Frame(container, bg="#f8f9fa", relief=tk.SUNKEN, bd=1)
        control.pack(fill=tk.X, padx=20, pady=10)
        
        ctrl_title = tk.Label(control, text="Kontrol:", font=("Helvetica", 10, "bold"), bg="#f8f9fa")
        ctrl_title.pack(anchor=tk.W, padx=10, pady=5)
        
        input_frame = tk.Frame(control, bg="#f8f9fa")
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(input_frame, text="Nama Dokumen:", bg="#f8f9fa").pack(side=tk.LEFT, padx=5)
        self.printer_input = tk.Entry(input_frame, width=20)
        self.printer_input.pack(side=tk.LEFT, padx=5)
        self.printer_input.insert(0, "laporan.pdf")
        
        tk.Button(input_frame, text="+ Tambah", command=self.printer_enqueue, bg="#667eea", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(input_frame, text="🖨️ Cetak", command=self.printer_dequeue, bg="#667eea", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(input_frame, text="Reset", command=self.printer_reset, bg="#6c757d", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Visualization
        viz_frame = tk.Frame(container, bg="#f8f9fa", relief=tk.SUNKEN, bd=1, height=150)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(viz_frame, text="Antrian Printer:", font=("Helvetica", 10, "bold"), bg="#f8f9fa").pack(anchor=tk.W, padx=10, pady=5)
        self.printer_display = tk.Label(viz_frame, text="(kosong)", font=("Helvetica", 12, "bold"), bg="#f8f9fa", fg="#667eea")
        self.printer_display.pack(pady=20, expand=True)
        
        # Log
        log_frame = tk.Frame(container, bg="#e7f3ff", relief=tk.SUNKEN, bd=1)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(log_frame, text="Dokumen Yang Dicetak:", font=("Helvetica", 10, "bold"), bg="#e7f3ff").pack(anchor=tk.W, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.printer_log = tk.Text(log_frame, height=6, yscrollcommand=scrollbar.set, font=("Courier", 9))
        self.printer_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        scrollbar.config(command=self.printer_log.yview)
        
        self.containers.append(container)
    
    def create_case2(self):
        """HOT POTATO"""
        container = tk.Frame(self.root, bg="white")
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title = tk.Label(
            container,
            text="🥔 Kasus 2: Permainan Hot Potato",
            font=("Helvetica", 16, "bold"),
            bg="white",
            fg="#667eea"
        )
        title.pack(pady=10)
        
        desc = tk.Label(
            container,
            text="Pemain melingkar mengoper benda. Setelah N kali oper, pemain yang pegang tersingkir.",
            font=("Helvetica", 10),
            bg="white",
            fg="#666"
        )
        desc.pack(pady=5)
        
        # Control panel
        control = tk.Frame(container, bg="#f8f9fa", relief=tk.SUNKEN, bd=1)
        control.pack(fill=tk.X, padx=20, pady=10)
        
        ctrl_title = tk.Label(control, text="Kontrol:", font=("Helvetica", 10, "bold"), bg="#f8f9fa")
        ctrl_title.pack(anchor=tk.W, padx=10, pady=5)
        
        input_frame = tk.Frame(control, bg="#f8f9fa")
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(input_frame, text="Jumlah Pemain:", bg="#f8f9fa").pack(side=tk.LEFT, padx=5)
        self.potato_players = tk.Spinbox(input_frame, from_=3, to=10, width=5)
        self.potato_players.pack(side=tk.LEFT, padx=5)
        self.potato_players.delete(0, tk.END)
        self.potato_players.insert(0, "6")
        
        tk.Button(input_frame, text="🎮 Mulai", command=self.potato_init, bg="#667eea", fg="white").pack(side=tk.LEFT, padx=5)
        
        tk.Label(input_frame, text="Oper (kali):", bg="#f8f9fa").pack(side=tk.LEFT, padx=5)
        self.potato_oper = tk.Spinbox(input_frame, from_=1, to=10, width=5)
        self.potato_oper.pack(side=tk.LEFT, padx=5)
        self.potato_oper.delete(0, tk.END)
        self.potato_oper.insert(0, "3")
        
        tk.Button(input_frame, text="▶️ Ronde", command=self.potato_play, bg="#667eea", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(input_frame, text="Reset", command=self.potato_reset, bg="#6c757d", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Visualization
        viz_frame = tk.Frame(container, bg="#f8f9fa", relief=tk.SUNKEN, bd=1, height=200)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.potato_canvas = tk.Canvas(viz_frame, bg="#f8f9fa", highlightthickness=0, height=200)
        self.potato_canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Log
        log_frame = tk.Frame(container, bg="#e7f3ff", relief=tk.SUNKEN, bd=1)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(log_frame, text="Log Permainan:", font=("Helvetica", 10, "bold"), bg="#e7f3ff").pack(anchor=tk.W, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.potato_log = tk.Text(log_frame, height=6, yscrollcommand=scrollbar.set, font=("Courier", 9))
        self.potato_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        scrollbar.config(command=self.potato_log.yview)
        
        self.containers.append(container)
    
    def create_case3(self):
        """HOSPITAL QUEUE"""
        container = tk.Frame(self.root, bg="white")
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title = tk.Label(
            container,
            text="🏥 Kasus 3: Antrian Rumah Sakit (Priority Queue)",
            font=("Helvetica", 16, "bold"),
            bg="white",
            fg="#667eea"
        )
        title.pack(pady=10)
        
        desc = tk.Label(
            container,
            text="Pasien darurat didahulukan berdasarkan prioritas. 0=Kritis, 1=Darurat, 2=Menengah, 3=Ringan.",
            font=("Helvetica", 10),
            bg="white",
            fg="#666"
        )
        desc.pack(pady=5)
        
        # Control panel
        control = tk.Frame(container, bg="#f8f9fa", relief=tk.SUNKEN, bd=1)
        control.pack(fill=tk.X, padx=20, pady=10)
        
        ctrl_title = tk.Label(control, text="Kontrol:", font=("Helvetica", 10, "bold"), bg="#f8f9fa")
        ctrl_title.pack(anchor=tk.W, padx=10, pady=5)
        
        input_frame = tk.Frame(control, bg="#f8f9fa")
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(input_frame, text="Nama Pasien:", bg="#f8f9fa").pack(side=tk.LEFT, padx=5)
        self.hospital_name = tk.Entry(input_frame, width=15)
        self.hospital_name.pack(side=tk.LEFT, padx=5)
        self.hospital_name.insert(0, "Pasien")
        
        tk.Label(input_frame, text="Prioritas:", bg="#f8f9fa").pack(side=tk.LEFT, padx=5)
        self.hospital_priority = ttk.Combobox(input_frame, values=["🔴 Kritis (0)", "🟠 Darurat (1)", "🟡 Menengah (2)", "🟢 Ringan (3)"], width=15, state="readonly")
        self.hospital_priority.pack(side=tk.LEFT, padx=5)
        self.hospital_priority.current(0)
        
        tk.Button(input_frame, text="+ Pasien Datang", command=self.hospital_add, bg="#667eea", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(input_frame, text="✓ Layani", command=self.hospital_serve, bg="#667eea", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(input_frame, text="Reset", command=self.hospital_reset, bg="#6c757d", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Visualization
        viz_frame = tk.Frame(container, bg="#f8f9fa", relief=tk.SUNKEN, bd=1)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(viz_frame, text="Antrian Tunggu:", font=("Helvetica", 10, "bold"), bg="#f8f9fa").pack(anchor=tk.W, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(viz_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.hospital_display = tk.Text(viz_frame, height=8, yscrollcommand=scrollbar.set, font=("Courier", 9))
        self.hospital_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        scrollbar.config(command=self.hospital_display.yview)
        
        # Log
        log_frame = tk.Frame(container, bg="#e7f3ff", relief=tk.SUNKEN, bd=1)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(log_frame, text="Pasien Yang Dilayani:", font=("Helvetica", 10, "bold"), bg="#e7f3ff").pack(anchor=tk.W, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.hospital_log = tk.Text(log_frame, height=5, yscrollcommand=scrollbar.set, font=("Courier", 9))
        self.hospital_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        scrollbar.config(command=self.hospital_log.yview)
        
        self.containers.append(container)
    
    def create_case4(self):
        """BFS GRAPH"""
        container = tk.Frame(self.root, bg="white")
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title = tk.Label(
            container,
            text="📈 Kasus 4: BFS (Breadth-First Search)",
            font=("Helvetica", 16, "bold"),
            bg="white",
            fg="#667eea"
        )
        title.pack(pady=10)
        
        desc = tk.Label(
            container,
            text="Pencarian jalur terpendek pada graf menggunakan queue. Menjelajahi node level demi level.",
            font=("Helvetica", 10),
            bg="white",
            fg="#666"
        )
        desc.pack(pady=5)
        
        # Control panel
        control = tk.Frame(container, bg="#f8f9fa", relief=tk.SUNKEN, bd=1)
        control.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(control, text="🚀 Mulai BFS", command=self.bfs_init, bg="#667eea", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(control, text="⏭️ Langkah", command=self.bfs_step, bg="#667eea", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(control, text="Reset", command=self.bfs_reset, bg="#6c757d", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10, pady=10)
        
        # Visualization
        viz_frame = tk.Frame(container, bg="#f8f9fa", relief=tk.SUNKEN, bd=1, height=150)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(viz_frame, text="Status Graf:", font=("Helvetica", 10, "bold"), bg="#f8f9fa").pack(anchor=tk.W, padx=10, pady=5)
        self.bfs_display = tk.Label(viz_frame, text="Tekan 'Mulai BFS'", font=("Helvetica", 11, "bold"), bg="#f8f9fa", fg="#667eea")
        self.bfs_display.pack(pady=30, expand=True)
        
        # Log
        log_frame = tk.Frame(container, bg="#e7f3ff", relief=tk.SUNKEN, bd=1)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(log_frame, text="Urutan Kunjungan:", font=("Helvetica", 10, "bold"), bg="#e7f3ff").pack(anchor=tk.W, padx=10, pady=5)
        self.bfs_log = tk.Label(log_frame, text="Belum dimulai", font=("Courier", 11, "bold"), bg="#e7f3ff", fg="#667eea", pady=10)
        self.bfs_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.containers.append(container)
    
    def create_case5(self):
        """SIMULATION"""
        container = tk.Frame(self.root, bg="white")
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title = tk.Label(
            container,
            text="✈️ Kasus 5: Simulasi Loket Tiket Bandara",
            font=("Helvetica", 16, "bold"),
            bg="white",
            fg="#667eea"
        )
        title.pack(pady=10)
        
        desc = tk.Label(
            container,
            text="Discrete event simulation untuk menghitung rata-rata waktu tunggu dengan berbagai jumlah agen.",
            font=("Helvetica", 10),
            bg="white",
            fg="#666"
        )
        desc.pack(pady=5)
        
        # Control panel
        control = tk.Frame(container, bg="#f8f9fa", relief=tk.SUNKEN, bd=1)
        control.pack(fill=tk.X, padx=20, pady=10)
        
        ctrl_title = tk.Label(control, text="Kontrol:", font=("Helvetica", 10, "bold"), bg="#f8f9fa")
        ctrl_title.pack(anchor=tk.W, padx=10, pady=5)
        
        input_frame = tk.Frame(control, bg="#f8f9fa")
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(input_frame, text="Jumlah Agen:", bg="#f8f9fa").pack(side=tk.LEFT, padx=5)
        self.sim_agents = tk.Scale(input_frame, from_=1, to=5, orient=tk.HORIZONTAL, bg="#f8f9fa", length=150)
        self.sim_agents.set(2)
        self.sim_agents.pack(side=tk.LEFT, padx=5)
        
        tk.Button(input_frame, text="▶️ Jalankan", command=self.sim_run, bg="#667eea", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(input_frame, text="Reset", command=self.sim_reset, bg="#6c757d", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Stats
        self.sim_stats_frame = tk.Frame(container, bg="white")
        self.sim_stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Timeline
        log_frame = tk.Frame(container, bg="#e7f3ff", relief=tk.SUNKEN, bd=1)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(log_frame, text="Timeline Kejadian (25 terakhir):", font=("Helvetica", 10, "bold"), bg="#e7f3ff").pack(anchor=tk.W, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.sim_log = tk.Text(log_frame, height=8, yscrollcommand=scrollbar.set, font=("Courier", 8))
        self.sim_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        scrollbar.config(command=self.sim_log.yview)
        
        self.containers.append(container)
    
    def switch_case(self, case_idx):
        self.current_case = case_idx
        
        for i, container in enumerate(self.containers):
            if i == case_idx:
                container.tkraise()
            else:
                container.pack_forget()
        
        self.containers[case_idx].pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for i, btn in enumerate(self.tab_buttons):
            if i == case_idx:
                btn.config(bg="#764ba2", fg="white")
            else:
                btn.config(bg="white", fg="#667eea")
    
    # ===== PRINTER METHODS =====
    def printer_enqueue(self):
        doc = self.printer_input.get().strip()
        if doc:
            self.printer.enqueue(doc)
            self.printer_input.delete(0, tk.END)
            self.printer_input.insert(0, "laporan.pdf")
            self.update_printer_display()
    
    def printer_dequeue(self):
        doc = self.printer.dequeue()
        if doc:
            self.update_printer_display()
    
    def printer_reset(self):
        self.printer.reset()
        self.printer_input.delete(0, tk.END)
        self.printer_input.insert(0, "laporan.pdf")
        self.update_printer_display()
    
    def update_printer_display(self):
        queue = self.printer.get_queue()
        display_text = " → ".join([f"[{doc[:6]}...]" for doc in queue]) if queue else "(kosong)"
        self.printer_display.config(text=display_text)
        
        printed = self.printer.get_printed()
        self.printer_log.config(state=tk.NORMAL)
        self.printer_log.delete(1.0, tk.END)
        if printed:
            for i, doc in enumerate(printed):
                self.printer_log.insert(tk.END, f"✓ {i+1}. {doc}\n")
        else:
            self.printer_log.insert(tk.END, "Belum ada dokumen yang dicetak")
        self.printer_log.config(state=tk.DISABLED)
    
    # ===== HOT POTATO METHODS =====
    def potato_init(self):
        num = int(self.potato_players.get())
        self.potato = HotPotatoGame(num)
        self.update_potato_display()
    
    def potato_play(self):
        if len(self.potato.players) == 0:
            messagebox.showwarning("Info", "Mulai permainan terlebih dahulu!")
            return
        
        oper = int(self.potato_oper.get())
        winner = self.potato.play_round(oper)
        self.update_potato_display()
    
    def potato_reset(self):
        self.potato = HotPotatoGame(0)
        self.update_potato_display()
    
    def update_potato_display(self):
        self.potato_canvas.delete("all")
        
        if len(self.potato.players) == 0:
            self.potato_canvas.create_text(150, 100, text="Klik 'Mulai' untuk memulai", font=("Helvetica", 12))
        else:
            width = self.potato_canvas.winfo_width()
            height = self.potato_canvas.winfo_height()
            if width == 1:
                width = 400
            if height == 1:
                height = 200
            
            cx, cy = width // 2, height // 2
            radius = min(width, height) // 2 - 30
            
            angle_slice = 2 * 3.14159 / len(self.potato.players)
            
            for i, player in enumerate(self.potato.players):
                angle = angle_slice * i - 3.14159 / 2
                x = cx + radius * __import__('math').cos(angle)
                y = cy + radius * __import__('math').sin(angle)
                
                if player["eliminated"]:
                    color = "#ccc"
                elif i == self.potato.current_idx:
                    color = "#ff6b6b"
                else:
                    color = "#667eea"
                
                self.potato_canvas.create_oval(x-25, y-25, x+25, y+25, fill=color)
                self.potato_canvas.create_text(x, y, text=player["name"], font=("Helvetica", 10, "bold"), fill="white")
            
            self.potato_canvas.create_oval(cx-15, cy-15, cx+15, cy+15, fill="#ff8c00")
        
        self.potato_log.config(state=tk.NORMAL)
        self.potato_log.delete(1.0, tk.END)
        for log in self.potato.logs:
            self.potato_log.insert(tk.END, f"• {log}\n")
        self.potato_log.config(state=tk.DISABLED)
    
    # ===== HOSPITAL METHODS =====
    def hospital_add(self):
        name = self.hospital_name.get().strip()
        priority_text = self.hospital_priority.get()
        priority = int(priority_text.split("(")[1].split(")")[0])
        
        if name:
            self.hospital.add_patient(name, priority)
            self.hospital_name.delete(0, tk.END)
            self.hospital_name.insert(0, "Pasien")
            self.update_hospital_display()
    
    def hospital_serve(self):
        patient = self.hospital.serve_patient()
        if patient:
            self.update_hospital_display()
    
    def hospital_reset(self):
        self.hospital = HospitalQueue()
        self.update_hospital_display()
    
    def update_hospital_display(self):
        self.hospital_display.config(state=tk.NORMAL)
        self.hospital_display.delete(1.0, tk.END)
        
        all_patients = self.hospital.get_all_waiting()
        if not all_patients:
            self.hospital_display.insert(tk.END, "Queue kosong")
        else:
            priority_labels = ["🔴 Kritis", "🟠 Darurat", "🟡 Menengah", "🟢 Ringan"]
            for patient, priority in all_patients:
                self.hospital_display.insert(tk.END, f"{priority_labels[priority]} - {patient.name} ({patient.time})\n")
        
        self.hospital_display.config(state=tk.DISABLED)
        
        self.hospital_log.config(state=tk.NORMAL)
        self.hospital_log.delete(1.0, tk.END)
        
        served = self.hospital.get_served()
        if served:
            priority_labels = ["Kritis", "Darurat", "Menengah", "Ringan"]
            for i, patient in enumerate(served):
                self.hospital_log.insert(tk.END, f"✓ {i+1}. {patient.name} ({priority_labels[patient.priority]})\n")
        else:
            self.hospital_log.insert(tk.END, "Belum ada pasien yang dilayani")
        
        self.hospital_log.config(state=tk.DISABLED)
    
    # ===== BFS METHODS =====
    def bfs_init(self):
        self.bfs.init_bfs()
        self.update_bfs_display()
    
    def bfs_step(self):
        if not self.bfs.started:
            self.bfs_init()
        
        has_more = self.bfs.step_bfs()
        if not has_more and len(self.bfs.queue) == 0:
            messagebox.showinfo("BFS", "BFS selesai!")
        
        self.update_bfs_display()
    
    def bfs_reset(self):
        self.bfs = BFSGraph()
        self.bfs_log.config(text="Belum dimulai")
        self.update_bfs_display()
    
    def update_bfs_display(self):
        state = self.bfs.get_state()
        
        display_text = ""
        for level in sorted(state.keys()):
            display_text += f"Level {level}: "
            for node, node_state in state[level]:
                if node_state == "visited":
                    display_text += f"[{node}✓] "
                elif node_state == "queued":
                    display_text += f"[{node}◈] "
                else:
                    display_text += f"[{node}] "
            display_text += "\n"
        
        self.bfs_display.config(text=display_text)
        
        if self.bfs.order:
            self.bfs_log.config(text=" → ".join(self.bfs.order))
        else:
            self.bfs_log.config(text="Belum dimulai")
    
    # ===== SIMULATION METHODS =====
    def sim_run(self):
        num_agents = self.sim_agents.get()
        self.simulation.run(num_agents)
        self.update_sim_display()
    
    def sim_reset(self):
        self.simulation.reset()
        self.sim_stats_frame.destroy()
        self.sim_stats_frame = tk.Frame(self.containers[4], bg="white")
        self.sim_stats_frame.pack(fill=tk.X, padx=20, pady=10)
        self.sim_log.config(state=tk.NORMAL)
        self.sim_log.delete(1.0, tk.END)
        self.sim_log.config(state=tk.DISABLED)
    
    def update_sim_display(self):
        # Clear old stats frame
        for widget in self.sim_stats_frame.winfo_children():
            widget.destroy()
        
        stats = self.simulation.get_stats()
        
        stat_labels = [
            ("Customers Dilayani", stats.get('customers_served', 0)),
            ("Avg Waktu Tunggu (min)", stats.get('avg_wait', 0)),
            ("Sisa di Queue", stats.get('remaining', 0)),
            ("Jumlah Agen", stats.get('num_agents', 0))
        ]
        
        for label, value in stat_labels:
            stat_card = tk.Frame(self.sim_stats_frame, bg="#667eea", relief=tk.RAISED, bd=1)
            stat_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            tk.Label(stat_card, text=str(value), font=("Helvetica", 18, "bold"), bg="#667eea", fg="white").pack(pady=10)
            tk.Label(stat_card, text=label, font=("Helvetica", 9), bg="#667eea", fg="white").pack()
        
        self.sim_log.config(state=tk.NORMAL)
        self.sim_log.delete(1.0, tk.END)
        
        events = self.simulation.get_events()
        for event in events:
            self.sim_log.insert(tk.END, event + "\n")
        
        self.sim_log.config(state=tk.DISABLED)


# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = QueueApp(root)
    root.mainloop()