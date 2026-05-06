"""
========================================================================
TUGAS LATIHAN — Advanced Linked Lists
Mata Kuliah : Struktur Data & Algoritma
Topik       : Multi-Linked List, Doubly Linked List, Circular Buffer

SOAL:
    Rancang struktur data untuk aplikasi note-taking yang mendukung:
    (a) Multiple tags per note        -> Multi-Linked List by Tag
    (b) Chronological & Alphabetical  -> Doubly Linked List (sorted)
    (c) Sync status tracking          -> Circular Buffer (recent changes)

PENDEKATAN IMPLEMENTASI:
    - Penamaan pointer menggunakan gaya "sebelum/sesudah" (sebelumWaktu,
      sesudahWaktu, sebelumJudul, sesudahJudul) agar lebih mudah dibaca.
    - Circular Buffer dibangun dari node bertaut (bukan array statis),
      sehingga ilustrasi "circular" lebih eksplisit secara struktur.
    - Setiap skenario pengujian menggunakan konteks catatan mahasiswa.
========================================================================
"""

import time
from datetime import datetime


# ========================================================================
# [A] STATUS SINKRONISASI
# ========================================================================

MENUNGGU  = "MENUNGGU"   # Belum dikirim ke server
TERSIMPAN = "TERSIMPAN"  # Berhasil disinkronkan
GAGAL     = "GAGAL"      # Sinkronisasi gagal


# ========================================================================
# [B] CATATAN (NODE UTAMA — Multi-Linked)
# ========================================================================

class Catatan:
    """
    Satu objek Catatan = satu node yang berpartisipasi dalam
    BANYAK linked list sekaligus tanpa duplikasi data:

        (1) DLL Waktu   : diurutkan berdasarkan waktu_buat (lama → baru)
        (2) DLL Judul   : diurutkan berdasarkan judul (A → Z)
        (3) Rantai Tag  : setiap label/tag membentuk rantai tersendiri
                          lewat pointer label_berikut[nama_label]

    Mengapa multi-linked?
        Kalau kita simpan salinan node di setiap list, kita butuh memori
        3× lebih besar. Dengan multi-linked, 1 node fisik cukup untuk
        semua tampilan (view), pointer-nya saja yang berbeda arah.
    """

    def __init__(self, id_catatan: str, judul: str, isi: str, waktu_buat: datetime):
        # ---------- data isi ----------
        self.id_catatan  = id_catatan
        self.judul       = judul
        self.isi         = isi
        self.waktu_buat  = waktu_buat   # datetime — kunci urutan kronologis

        # ---------- DLL (1): berdasarkan waktu ----------
        self.sebelumWaktu = None   # catatan yang dibuat LEBIH LAMA
        self.sesudahWaktu = None   # catatan yang dibuat LEBIH BARU

        # ---------- DLL (2): berdasarkan judul ----------
        self.sebelumJudul = None   # catatan dengan judul lebih kecil
        self.sesudahJudul = None   # catatan dengan judul lebih besar

        # ---------- Rantai Tag (Multi-Linked) ----------
        # label_berikut["kuliah"] → Catatan berikutnya dlm rantai "kuliah"
        self.label_berikut: dict = {}
        self.daftar_label: list  = []   # label yang dimiliki catatan ini

        # ---------- status sinkronisasi ----------
        self.status_sync = MENUNGGU

    def __str__(self):
        tgl = self.waktu_buat.strftime("%d %b %Y")
        return (f"[{tgl}] {self.judul:<30} "
                f"label={self.daftar_label}  sync={self.status_sync}")

    def __repr__(self):
        return f"Catatan(id={self.id_catatan!r}, judul={self.judul!r})"


# ========================================================================
# [C] RANTAI LABEL (Tag Chain — Partial Multi-Linked List)
# ========================================================================

class RantaiLabel:
    """
    RantaiLabel merepresentasikan satu partial linked list
    untuk SATU label/tag tertentu.

    "Partial" karena tidak semua Catatan masuk di sini —
    hanya catatan yang memiliki label ini.

    Catatan-catatan terhubung lewat:
        catatan.label_berikut["nama_label"] → Catatan_berikutnya

    Sisipan baru selalu di DEPAN → O(1).
    Traversal seluruh rantai      → O(k), k = jumlah catatan berlabel ini.
    """

    def __init__(self, nama: str):
        self.nama   = nama    # e.g. "kuliah", "tugas"
        self.kepala = None    # Catatan pertama di rantai ini
        self.total  = 0

    def tambah(self, catatan: Catatan):
        """Sisipkan di depan rantai — O(1)."""
        catatan.label_berikut[self.nama] = self.kepala
        self.kepala = catatan
        self.total += 1
        if self.nama not in catatan.daftar_label:
            catatan.daftar_label.append(self.nama)

    def hapus(self, target: Catatan):
        """
        Cari dan putuskan target dari rantai ini — O(k).
        Pointer label_berikut target dibersihkan setelah dilepas.
        """
        sebelum = None
        kini    = self.kepala
        while kini is not None and kini is not target:
            sebelum = kini
            kini    = kini.label_berikut.get(self.nama)

        if kini is None:
            return  # tidak ada di rantai ini

        berikut = kini.label_berikut.pop(self.nama, None)
        if sebelum is None:
            self.kepala = berikut
        else:
            sebelum.label_berikut[self.nama] = berikut

        if self.nama in kini.daftar_label:
            kini.daftar_label.remove(self.nama)
        self.total -= 1

    def iterasi(self):
        """Generator: kunjungi semua Catatan dalam rantai ini."""
        kini = self.kepala
        while kini is not None:
            yield kini
            kini = kini.label_berikut.get(self.nama)

    def __repr__(self):
        return f"RantaiLabel(nama={self.nama!r}, total={self.total})"


# ========================================================================
# [D] BUFFER MELINGKAR (Circular Buffer — Sync Tracking)
#     Implementasi menggunakan NODE bertaut agar struktur "circular"
#     terlihat eksplisit, bukan sekadar array dengan modulo.
# ========================================================================

class NodeBuffer:
    """Node kecil khusus untuk Circular Buffer."""
    def __init__(self):
        self.rekaman  = None   # dict berisi info event sync
        self.berikut  = None   # pointer ke NodeBuffer berikutnya


class BufferMelingkar:
    """
    Circular Buffer berbasis linked nodes.

    Cara kerja:
      - Sejumlah N NodeBuffer dibuat saat inisialisasi dan
        disambung menjadi lingkaran: node[0]→node[1]→…→node[N-1]→node[0].
      - 'penulis' menunjuk posisi tempat menulis berikutnya.
      - 'pembaca' menunjuk entry paling lama (oldest).
      - Ketika buffer penuh, pembaca maju (oldest tertimpa).

    Keunggulan vs array:
      Tidak perlu operasi modulo karena pointer next sudah "wrap" sendiri.

    Kompleksitas: tulis O(1), baca-semua O(N).
    """

    def __init__(self, kapasitas: int = 8):
        self.kapasitas = kapasitas
        self.isi       = 0

        # Buat N node dan sambung melingkar
        nodes = [NodeBuffer() for _ in range(kapasitas)]
        for i in range(kapasitas):
            nodes[i].berikut = nodes[(i + 1) % kapasitas]

        self.penulis = nodes[0]   # posisi tulis berikutnya
        self.pembaca = nodes[0]   # posisi baca (oldest)

    def catat(self, catatan: Catatan, status: str):
        """
        Tulis satu event sync ke buffer.
        Jika penuh, entry terlama tertimpa & pembaca maju.
        Kompleksitas: O(1).
        """
        self.penulis.rekaman = {
            "id"        : catatan.id_catatan,
            "judul"     : catatan.judul,
            "status"    : status,
            "waktu"     : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.penulis = self.penulis.berikut   # maju ke slot berikut

        if self.isi < self.kapasitas:
            self.isi += 1
        else:
            # Buffer penuh: oldest tertimpa, geser pembaca
            self.pembaca = self.pembaca.berikut

    def baca_semua(self) -> list:
        """
        Kembalikan semua rekaman dari oldest ke newest.
        Kompleksitas: O(N).
        """
        hasil = []
        kini  = self.pembaca
        for _ in range(self.isi):
            if kini.rekaman:
                hasil.append(kini.rekaman)
            kini = kini.berikut
        return hasil

    def kosong(self) -> bool:
        return self.isi == 0

    def __repr__(self):
        return f"BufferMelingkar(kapasitas={self.kapasitas}, isi={self.isi})"


# ========================================================================
# [E] BUKU CATATAN (Controller Utama)
# ========================================================================

class BukuCatatan:
    """
    BukuCatatan mengelola seluruh struktur data:

      DLL Waktu  : kepalaWaktu ↔ … ↔ ekorWaktu
                   (sorted waktu_buat ascending)
      DLL Judul  : kepalaJudul ↔ … ↔ ekorJudul
                   (sorted judul ascending, A-Z)
      Rantai     : dict {nama_label → RantaiLabel}
      Buffer     : BufferMelingkar untuk N perubahan sync terakhir

    Aturan utama (dari materi):
      - Setiap insert harus memperbarui SEMUA chain.
      - Setiap delete harus melepas dari SEMUA chain sebelum node dibuang.
    """

    def __init__(self, ukuran_buffer: int = 6):
        # DLL Waktu
        self.kepalaWaktu = None
        self.ekorWaktu   = None

        # DLL Judul
        self.kepalaJudul = None
        self.ekorJudul   = None

        # Registry label
        self.rantai: dict = {}       # {nama_label: RantaiLabel}

        # Circular Buffer
        self.buffer = BufferMelingkar(kapasitas=ukuran_buffer)

        self._jumlah = 0

    # ────────────────────────────────────────────────────────────────────
    # INSERT
    # ────────────────────────────────────────────────────────────────────

    def tambah_catatan(self, id_catatan, judul, isi, waktu_buat,
                       labels=None) -> Catatan:
        """
        Tambah catatan baru ke semua chain.
        Insert ke DLL sorted: O(n).
        """
        if labels is None:
            labels = []

        baru = Catatan(id_catatan, judul, isi, waktu_buat)
        self._jumlah += 1

        self._sisip_waktu(baru)   # masuk ke DLL Waktu
        self._sisip_judul(baru)   # masuk ke DLL Judul

        for lb in labels:         # masuk ke setiap rantai label
            if lb not in self.rantai:
                self.rantai[lb] = RantaiLabel(lb)
            self.rantai[lb].tambah(baru)

        self.buffer.catat(baru, MENUNGGU)   # catat sebagai MENUNGGU
        return baru

    def _sisip_waktu(self, baru: Catatan):
        """
        Sisipkan ke DLL Waktu secara sorted ascending (waktu_buat).
        Tiga kasus: kosong, kepala, ekor, atau tengah.
        """
        if self.kepalaWaktu is None:
            self.kepalaWaktu = self.ekorWaktu = baru
            return

        if baru.waktu_buat <= self.kepalaWaktu.waktu_buat:
            baru.sesudahWaktu            = self.kepalaWaktu
            self.kepalaWaktu.sebelumWaktu = baru
            self.kepalaWaktu             = baru
            return

        if baru.waktu_buat >= self.ekorWaktu.waktu_buat:
            baru.sebelumWaktu           = self.ekorWaktu
            self.ekorWaktu.sesudahWaktu = baru
            self.ekorWaktu              = baru
            return

        # Sisip di tengah: cari posisi yang tepat
        pos = self.kepalaWaktu
        while pos is not None and pos.waktu_buat < baru.waktu_buat:
            pos = pos.sesudahWaktu

        # Sisipkan baru sebelum pos
        baru.sesudahWaktu              = pos
        baru.sebelumWaktu              = pos.sebelumWaktu
        pos.sebelumWaktu.sesudahWaktu  = baru
        pos.sebelumWaktu               = baru

    def _sisip_judul(self, baru: Catatan):
        """
        Sisipkan ke DLL Judul secara sorted ascending (judul A-Z).
        Logika identik dengan _sisip_waktu namun kunci = judul.
        """
        if self.kepalaJudul is None:
            self.kepalaJudul = self.ekorJudul = baru
            return

        if baru.judul <= self.kepalaJudul.judul:
            baru.sesudahJudul              = self.kepalaJudul
            self.kepalaJudul.sebelumJudul  = baru
            self.kepalaJudul               = baru
            return

        if baru.judul >= self.ekorJudul.judul:
            baru.sebelumJudul              = self.ekorJudul
            self.ekorJudul.sesudahJudul    = baru
            self.ekorJudul                 = baru
            return

        pos = self.kepalaJudul
        while pos is not None and pos.judul < baru.judul:
            pos = pos.sesudahJudul

        baru.sesudahJudul              = pos
        baru.sebelumJudul              = pos.sebelumJudul
        pos.sebelumJudul.sesudahJudul  = baru
        pos.sebelumJudul               = baru

    # ────────────────────────────────────────────────────────────────────
    # DELETE
    # ────────────────────────────────────────────────────────────────────

    def hapus_catatan(self, catatan: Catatan):
        """
        Lepas catatan dari SEMUA chain lalu kurangi counter.
        DLL: O(1) karena punya pointer sebelum & sesudah.
        Rantai label: O(k) per label.
        """
        # --- lepas dari DLL Waktu ---
        if catatan.sebelumWaktu:
            catatan.sebelumWaktu.sesudahWaktu = catatan.sesudahWaktu
        else:
            self.kepalaWaktu = catatan.sesudahWaktu

        if catatan.sesudahWaktu:
            catatan.sesudahWaktu.sebelumWaktu = catatan.sebelumWaktu
        else:
            self.ekorWaktu = catatan.sebelumWaktu

        # --- lepas dari DLL Judul ---
        if catatan.sebelumJudul:
            catatan.sebelumJudul.sesudahJudul = catatan.sesudahJudul
        else:
            self.kepalaJudul = catatan.sesudahJudul

        if catatan.sesudahJudul:
            catatan.sesudahJudul.sebelumJudul = catatan.sebelumJudul
        else:
            self.ekorJudul = catatan.sebelumJudul

        # --- lepas dari setiap rantai label ---
        salinan_label = list(catatan.daftar_label)
        for lb in salinan_label:
            if lb in self.rantai:
                self.rantai[lb].hapus(catatan)

        self._jumlah -= 1
        print(f"  >> HAPUS: '{catatan.judul}' dilepas dari semua chain.")

    # ────────────────────────────────────────────────────────────────────
    # UPDATE SYNC
    # ────────────────────────────────────────────────────────────────────

    def perbarui_sync(self, catatan: Catatan, status: str):
        """
        Ubah status sinkronisasi catatan dan catat ke buffer.
        Kompleksitas: O(1).
        """
        catatan.status_sync = status
        self.buffer.catat(catatan, status)
        ikon = {"TERSIMPAN": "✓", "GAGAL": "✗", "MENUNGGU": "…"}.get(status, "?")
        print(f"  {ikon} SYNC '{catatan.judul}' → {status}")

    # ────────────────────────────────────────────────────────────────────
    # TRAVERSAL / VIEW
    # ────────────────────────────────────────────────────────────────────

    def urutkan_waktu(self, terbalik: bool = False) -> list:
        """
        Traversal DLL Waktu.
        terbalik=False → lama ke baru (forward, via sesudahWaktu)
        terbalik=True  → baru ke lama (reverse, via sebelumWaktu)
        Kompleksitas: O(n).
        """
        hasil = []
        if not terbalik:
            pos = self.kepalaWaktu
            while pos:
                hasil.append(pos)
                pos = pos.sesudahWaktu
        else:
            pos = self.ekorWaktu
            while pos:
                hasil.append(pos)
                pos = pos.sebelumWaktu
        return hasil

    def urutkan_judul(self, terbalik: bool = False) -> list:
        """
        Traversal DLL Judul.
        terbalik=False → A-Z (forward)
        terbalik=True  → Z-A (reverse, via sebelumJudul)
        Kompleksitas: O(n).
        """
        hasil = []
        if not terbalik:
            pos = self.kepalaJudul
            while pos:
                hasil.append(pos)
                pos = pos.sesudahJudul
        else:
            pos = self.ekorJudul
            while pos:
                hasil.append(pos)
                pos = pos.sebelumJudul
        return hasil

    def cari_per_label(self, nama_label: str) -> list:
        """
        Kembalikan semua catatan dengan label tertentu.
        Kompleksitas: O(k), k = catatan berlabel ini.
        """
        if nama_label not in self.rantai:
            return []
        return list(self.rantai[nama_label].iterasi())

    def riwayat_sync(self) -> list:
        """Baca seluruh isi buffer (oldest → newest)."""
        return self.buffer.baca_semua()

    @property
    def jumlah(self) -> int:
        return self._jumlah

    def __repr__(self):
        return (f"BukuCatatan(jumlah={self._jumlah}, "
                f"label={list(self.rantai.keys())}, "
                f"buffer={self.buffer})")


# ========================================================================
# [F] HELPER CETAK
# ========================================================================

def garis(judul: str = ""):
    print("\n" + "─" * 62)
    if judul:
        print(f"  ▶  {judul}")
        print("─" * 62)

def cetak_daftar(daftar: list, keterangan: str = ""):
    if keterangan:
        print(f"\n  {keterangan}")
    if not daftar:
        print("    (tidak ada catatan)")
        return
    for c in daftar:
        tgl = c.waktu_buat.strftime("%d/%m/%Y")
        print(f"    {tgl}  {c.judul:<32} [{', '.join(c.daftar_label)}]  {c.status_sync}")

def cetak_riwayat(rekaman: list):
    print("\n  Riwayat sinkronisasi (oldest → newest):")
    if not rekaman:
        print("    (buffer masih kosong)")
        return
    for i, r in enumerate(rekaman, 1):
        print(f"    {i:>2}. [{r['waktu']}]  {r['judul']:<30}  {r['status']}")


# ========================================================================
# [G] MAIN — SKENARIO PENGUJIAN (Konteks Catatan Mahasiswa)
# ========================================================================

if __name__ == "__main__":

    garis("APLIKASI CATATAN MAHASISWA — Advanced Linked Lists")

    # ── Inisialisasi ────────────────────────────────────────────────────
    buku = BukuCatatan(ukuran_buffer=6)

    # ── (1) Tambah Catatan ───────────────────────────────────────────────
    garis("1. MENAMBAHKAN CATATAN")

    c1 = buku.tambah_catatan(
        "C001", "Rangkuman Struktur Data",
        "Array, Stack, Queue, Linked List, Tree, Graph",
        datetime(2024, 3, 10, 8, 0),
        labels=["kuliah", "ds", "rangkuman"]
    )
    c2 = buku.tambah_catatan(
        "C002", "Tugas Basis Data ER-Diagram",
        "Buat ER-Diagram untuk sistem perpustakaan kampus",
        datetime(2024, 3, 5, 13, 0),
        labels=["tugas", "basis-data"]
    )
    c3 = buku.tambah_catatan(
        "C003", "Catatan OOP Python",
        "Class, inheritance, encapsulation, polymorphism",
        datetime(2024, 3, 8, 9, 30),
        labels=["kuliah", "python", "oop"]
    )
    c4 = buku.tambah_catatan(
        "C004", "Proyek Akhir Semester",
        "Aplikasi manajemen inventaris toko kelontong",
        datetime(2024, 3, 15, 17, 0),
        labels=["proyek", "tugas", "python"]
    )
    c5 = buku.tambah_catatan(
        "C005", "Jadwal UTS 2024",
        "DS: 20 Mar | BD: 22 Mar | OOP: 25 Mar",
        datetime(2024, 3, 1, 7, 0),
        labels=["jadwal", "penting"]
    )
    c6 = buku.tambah_catatan(
        "C006", "Belajar Algoritma Greedy",
        "Knapsack, Dijkstra, Prim, Kruskal",
        datetime(2024, 3, 12, 10, 0),
        labels=["kuliah", "ds", "algoritma"]
    )

    print(f"\n  Total catatan tersimpan: {buku.jumlah}")

    # ── (2) View Kronologis ──────────────────────────────────────────────
    garis("2. VIEW KRONOLOGIS (DLL sorted by waktu_buat)")

    cetak_daftar(buku.urutkan_waktu(terbalik=False),
                 "Lama → Baru (forward via sesudahWaktu):")
    cetak_daftar(buku.urutkan_waktu(terbalik=True),
                 "Baru → Lama (reverse via sebelumWaktu):")

    # ── (3) View Alfabetis ───────────────────────────────────────────────
    garis("3. VIEW ALFABETIS (DLL sorted by judul)")

    cetak_daftar(buku.urutkan_judul(terbalik=False),
                 "A → Z (forward via sesudahJudul):")
    cetak_daftar(buku.urutkan_judul(terbalik=True),
                 "Z → A (reverse via sebelumJudul):")

    # ── (4) Filter per Label ─────────────────────────────────────────────
    garis("4. FILTER PER LABEL (Multi-Linked Rantai Tag)")

    print()
    for lb in ["kuliah", "tugas", "python", "ds", "jadwal"]:
        catatan_lb = buku.cari_per_label(lb)
        judul_lb   = [c.judul for c in catatan_lb]
        print(f"  #{lb:<12} ({len(judul_lb)} catatan) → {judul_lb}")

    # ── (5) Sinkronisasi & Circular Buffer ──────────────────────────────
    garis("5. SINKRONISASI & CIRCULAR BUFFER")

    print("\n  Proses sinkronisasi catatan ke server:")
    buku.perbarui_sync(c5, TERSIMPAN)
    buku.perbarui_sync(c2, TERSIMPAN)
    buku.perbarui_sync(c3, GAGAL)      # gagal, akan di-retry
    buku.perbarui_sync(c1, TERSIMPAN)
    buku.perbarui_sync(c6, TERSIMPAN)  # buffer hampir penuh
    buku.perbarui_sync(c3, TERSIMPAN)  # retry c3 yang gagal
    buku.perbarui_sync(c4, MENUNGGU)   # entry ke-7, oldest tertimpa

    cetak_riwayat(buku.riwayat_sync())

    # ── (6) Hapus Catatan ────────────────────────────────────────────────
    garis("6. HAPUS CATATAN (lepas dari semua chain)")

    print(f"\n  Sebelum hapus: {buku.jumlah} catatan")
    buku.hapus_catatan(c2)   # hapus "Tugas Basis Data ER-Diagram"
    print(f"  Sesudah hapus: {buku.jumlah} catatan")

    cetak_daftar(buku.urutkan_waktu(),
                 "Daftar kronologis setelah hapus:")

    print(f"\n  Label #tugas setelah hapus c2: "
          f"{[c.judul for c in buku.cari_per_label('tugas')]}")

    # ── (7) Verifikasi Struktur Circular Buffer ──────────────────────────
    garis("7. VERIFIKASI STRUKTUR CIRCULAR BUFFER (NODE BERTAUT)")

    buf = buku.buffer
    print(f"\n  Kapasitas buffer : {buf.kapasitas}")
    print(f"  Slot terisi      : {buf.isi}")

    # Telusuri lingkaran node buffer secara manual
    print("\n  Traversal manual seluruh slot buffer (melingkar):")
    pos = buf.pembaca
    for i in range(buf.kapasitas):
        isi_slot = pos.rekaman["judul"] if pos.rekaman else "(kosong)"
        penanda  = " ← pembaca (oldest)" if (i == 0) else ""
        print(f"    slot {i}: {isi_slot}{penanda}")
        pos = pos.berikut   # maju ke node berikutnya dalam lingkaran

    # ── (8) Ringkasan Kompleksitas ───────────────────────────────────────
    garis("8. TABEL KOMPLEKSITAS OPERASI")

    tabel = [
        ("tambah_catatan (insert sorted 2 DLL)", "O(n)",      "n = total catatan"),
        ("hapus_catatan  (lepas dari 2 DLL)",    "O(1)",      "punya pointer prev & next"),
        ("hapus dari T rantai label",            "O(k·T)",    "k = pjg rantai, T = jml label"),
        ("urutkan_waktu / urutkan_judul",        "O(n)",      "traversal DLL penuh"),
        ("Reverse view (via sebelum* pointer)",  "O(n)",      "tanpa rebuild list"),
        ("cari_per_label (satu rantai)",         "O(k)",      "k = catatan berlabel itu"),
        ("buffer.catat (circular buffer)",       "O(1)",      "pointer langsung, no modulo"),
        ("buffer.baca_semua",                    "O(N_buf)",  "N_buf = kapasitas buffer"),
        ("Memori total",                         "O(N·L)",    "N = catatan, L = label unik"),
    ]
    print()
    print(f"  {'OPERASI':<42} {'WAKTU':<12} KETERANGAN")
    print(f"  {'─'*41} {'─'*10} {'─'*25}")
    for op, t, ket in tabel:
        print(f"  {op:<42} {t:<12} {ket}")

    garis("SELESAI")
    print("  Semua fitur berhasil diuji:")
    print("  ✓ (a) Multi-Linked by Tag  → RantaiLabel")
    print("  ✓ (b) Doubly Linked sorted → DLL Waktu & DLL Judul")
    print("  ✓ (c) Circular Buffer      → BufferMelingkar (node bertaut)")
    print()