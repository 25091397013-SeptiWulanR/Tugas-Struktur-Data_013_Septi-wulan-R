# ============================================================
# SOLUSI LENGKAP - 5 PROGRAM PYTHON
# ============================================================

# ============================================================
# 1. REMOVE DUPLICATES (Hapus Duplikat, Pertahankan Urutan)
# ============================================================
def remove_duplicates(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

print("=" * 50)
print("1. REMOVE DUPLICATES")
print("=" * 50)
contoh1 = [1, 3, 2, 1, 5, 3, 4, 2, 6]
print(f"Input  : {contoh1}")
print(f"Output : {remove_duplicates(contoh1)}")

contoh2 = ["apple", "banana", "apple", "cherry", "banana", "date"]
print(f"Input  : {contoh2}")
print(f"Output : {remove_duplicates(contoh2)}")


# ============================================================
# 2. INTERSECTION DUA ARRAY
# ============================================================
def intersection(list1, list2):
    set2 = set(list2)
    seen = set()
    result = []
    for item in list1:
        if item in set2 and item not in seen:
            seen.add(item)
            result.append(item)
    return result

print("\n" + "=" * 50)
print("2. INTERSECTION DUA ARRAY")
print("=" * 50)
a = [1, 2, 3, 4, 5]
b = [3, 4, 5, 6, 7]
print(f"List 1 : {a}")
print(f"List 2 : {b}")
print(f"Irisan : {intersection(a, b)}")

c = ["dog", "cat", "bird", "fish"]
d = ["cat", "fish", "snake", "dog"]
print(f"List 1 : {c}")
print(f"List 2 : {d}")
print(f"Irisan : {intersection(c, d)}")


# ============================================================
# 3. ANAGRAM CHECK
# ============================================================
def is_anagram(str1, str2):
    str1 = str1.replace(" ", "").lower()
    str2 = str2.replace(" ", "").lower()
    
    if len(str1) != len(str2):
        return False
    
    count = {}
    for char in str1:
        count[char] = count.get(char, 0) + 1
    for char in str2:
        count[char] = count.get(char, 0) - 1
        if count[char] < 0:
            return False
    return True

print("\n" + "=" * 50)
print("3. ANAGRAM CHECK")
print("=" * 50)
pasangan = [
    ("listen", "silent"),
    ("hello", "world"),
    ("Astronomer", "Moon starer"),
    ("python", "typhon"),
]
for s1, s2 in pasangan:
    hasil = is_anagram(s1, s2)
    status = "✓ ANAGRAM" if hasil else "✗ BUKAN Anagram"
    print(f'"{s1}" vs "{s2}" → {status}')


# ============================================================
# 4. FIRST RECURRING CHARACTER
# ============================================================
def first_recurring_char(s):
    seen = set()
    for char in s:
        if char in seen:
            return char
        seen.add(char)
    return None

print("\n" + "=" * 50)
print("4. FIRST RECURRING CHARACTER")
print("=" * 50)
strings = ["ABCDCA", "BCFGHBCD", "abcdef", "aabbcc"]
for s in strings:
    result = first_recurring_char(s)
    if result:
        print(f'String "{s}" → Karakter pertama berulang: "{result}"')
    else:
        print(f'String "{s}" → Tidak ada karakter berulang')


# ============================================================
# 5. SIMULASI BUKU TELEPON
# ============================================================
def phone_book():
    contacts = {}
    
    print("\n" + "=" * 50)
    print("5. SIMULASI BUKU TELEPON")
    print("=" * 50)
    
    # Pre-load beberapa kontak contoh
    contacts["Budi"] = "08123456789"
    contacts["Sari"] = "08234567890"
    contacts["Ahmad"] = "08345678901"
    
    while True:
        print("\n--- MENU BUKU TELEPON ---")
        print("1. Tambah Kontak")
        print("2. Cari Kontak")
        print("3. Tampilkan Semua Kontak")
        print("4. Keluar")
        
        pilihan = input("\nPilih menu (1-4): ").strip()
        
        if pilihan == "1":
            nama = input("Masukkan nama  : ").strip()
            nomor = input("Masukkan nomor : ").strip()
            if nama and nomor:
                contacts[nama] = nomor
                print(f"✓ Kontak '{nama}' berhasil ditambahkan!")
            else:
                print("✗ Nama dan nomor tidak boleh kosong!")
        
        elif pilihan == "2":
            nama = input("Masukkan nama yang dicari: ").strip()
            if nama in contacts:
                print(f"✓ Ditemukan! {nama}: {contacts[nama]}")
            else:
                # Cari partial match
                hasil = {k: v for k, v in contacts.items() 
                        if nama.lower() in k.lower()}
                if hasil:
                    print(f"Hasil pencarian untuk '{nama}':")
                    for k, v in hasil.items():
                        print(f"  • {k}: {v}")
                else:
                    print(f"✗ Kontak '{nama}' tidak ditemukan.")
        
        elif pilihan == "3":
            if contacts:
                print(f"\n{'No.':<5} {'Nama':<20} {'Nomor':<15}")
                print("-" * 40)
                for i, (nama, nomor) in enumerate(sorted(contacts.items()), 1):
                    print(f"{i:<5} {nama:<20} {nomor:<15}")
                print(f"\nTotal: {len(contacts)} kontak")
            else:
                print("Buku telepon masih kosong.")
        
        elif pilihan == "4":
            print("Terima kasih! Program selesai.")
            break
        
        else:
            print("✗ Pilihan tidak valid! Masukkan angka 1-4.")

# Jalankan Phone Book
phone_book()