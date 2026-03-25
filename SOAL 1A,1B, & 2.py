# ============================================================
# Tugas Praktikum - Big Integer ADT
# Soal 1a : Implementasi menggunakan Singly Linked List
# Soal 1b : Implementasi menggunakan Python List
# Soal 2  : Tambahan Assignment Combo Operators
# ============================================================


# ============================================================
# SOAL 1a — Big Integer menggunakan Singly Linked List
# ============================================================

class _Node:
    """Node untuk singly linked list."""
    def __init__(self, digit):
        self.digit = digit   # satu digit (0–9)
        self.next  = None


class BigIntLinkedList:
    """
    Big Integer ADT — penyimpanan digit menggunakan singly linked list.
    Digit disimpan dari least-significant (head) ke most-significant (tail).
    Contoh: 45839  →  head → [9] → [3] → [8] → [5] → [4] → None
    """

    # ----------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------
    def __init__(self, initValue="0"):
        self._head = None
        self._negative = False
        self._parse(str(initValue))

    def _parse(self, s: str):
        """Bangun linked list dari string angka."""
        s = s.strip()
        if s.startswith("-"):
            self._negative = True
            s = s[1:]
        else:
            self._negative = False

        s = s.lstrip("0") or "0"   # hapus leading zero
        self._head = None

        # Simpan digit dari most-significant ke least-significant
        # dengan cara insert di depan (prepend), sehingga:
        # head → least-significant, tail → most-significant
        for ch in s:
            node = _Node(int(ch))
            node.next = self._head
            self._head = node

    # ----------------------------------------------------------
    # toString
    # ----------------------------------------------------------
    def toString(self) -> str:
        digits = []
        cur = self._head
        while cur:
            digits.append(str(cur.digit))
            cur = cur.next
        # digit tersimpan least-significant dulu → balik urutan
        result = "".join(reversed(digits)) or "0"
        result = result.lstrip("0") or "0"
        if self._negative and result != "0":
            return "-" + result
        return result

    def __repr__(self):
        return f"BigIntLinkedList('{self.toString()}')"

    # ----------------------------------------------------------
    # Helper: konversi ke/dari int Python (untuk operasi internal)
    # ----------------------------------------------------------
    def _to_int(self) -> int:
        val = int(self.toString())
        return val

    @classmethod
    def _from_int(cls, n: int) -> "BigIntLinkedList":
        return cls(str(n))

    # ----------------------------------------------------------
    # comparable — mendukung <, <=, >, >=, ==, !=
    # ----------------------------------------------------------
    def comparable(self, other) -> int:
        """
        Kembalikan:  -1  jika self < other
                      0  jika self == other
                      1  jika self > other
        """
        a, b = self._to_int(), other._to_int()
        if a < b:  return -1
        if a > b:  return  1
        return 0

    def __lt__(self, other): return self.comparable(other) == -1
    def __le__(self, other): return self.comparable(other) <= 0
    def __gt__(self, other): return self.comparable(other) == 1
    def __ge__(self, other): return self.comparable(other) >= 0
    def __eq__(self, other): return self.comparable(other) == 0
    def __ne__(self, other): return self.comparable(other) != 0

    # ----------------------------------------------------------
    # arithmetic — +, -, *, //, %, **
    # ----------------------------------------------------------
    def arithmetic(self, rhsInt: "BigIntLinkedList", op: str) -> "BigIntLinkedList":
        a, b = self._to_int(), rhsInt._to_int()
        ops = {
            "+":  lambda x, y: x + y,
            "-":  lambda x, y: x - y,
            "*":  lambda x, y: x * y,
            "//": lambda x, y: x // y,
            "%":  lambda x, y: x %  y,
            "**": lambda x, y: x ** y,
        }
        if op not in ops:
            raise ValueError(f"Operator aritmetika tidak dikenal: {op}")
        return self._from_int(ops[op](a, b))

    def __add__(self, other): return self.arithmetic(other, "+")
    def __sub__(self, other): return self.arithmetic(other, "-")
    def __mul__(self, other): return self.arithmetic(other, "*")
    def __floordiv__(self, other): return self.arithmetic(other, "//")
    def __mod__(self, other): return self.arithmetic(other, "%")
    def __pow__(self, other): return self.arithmetic(other, "**")

    # ----------------------------------------------------------
    # bitwise — |, &, ^, <<, >>
    # ----------------------------------------------------------
    def bitwise_ops(self, rhsInt: "BigIntLinkedList", op: str) -> "BigIntLinkedList":
        a, b = self._to_int(), rhsInt._to_int()
        ops = {
            "|":  lambda x, y: x |  y,
            "&":  lambda x, y: x &  y,
            "^":  lambda x, y: x ^  y,
            "<<": lambda x, y: x << y,
            ">>": lambda x, y: x >> y,
        }
        if op not in ops:
            raise ValueError(f"Operator bitwise tidak dikenal: {op}")
        return self._from_int(ops[op](a, b))

    def __or__ (self, other): return self.bitwise_ops(other, "|")
    def __and__(self, other): return self.bitwise_ops(other, "&")
    def __xor__(self, other): return self.bitwise_ops(other, "^")
    def __lshift__(self, other): return self.bitwise_ops(other, "<<")
    def __rshift__(self, other): return self.bitwise_ops(other, ">>")

    # ----------------------------------------------------------
    # SOAL 2 — Assignment combo operators
    # ----------------------------------------------------------
    def __iadd__(self, other):      return self.arithmetic(other, "+")
    def __isub__(self, other):      return self.arithmetic(other, "-")
    def __imul__(self, other):      return self.arithmetic(other, "*")
    def __ifloordiv__(self, other): return self.arithmetic(other, "//")
    def __imod__(self, other):      return self.arithmetic(other, "%")
    def __ipow__(self, other):      return self.arithmetic(other, "**")
    def __ilshift__(self, other):   return self.bitwise_ops(other, "<<")
    def __irshift__(self, other):   return self.bitwise_ops(other, ">>")
    def __ior__ (self, other):      return self.bitwise_ops(other, "|")
    def __iand__(self, other):      return self.bitwise_ops(other, "&")
    def __ixor__(self, other):      return self.bitwise_ops(other, "^")


# ============================================================
# SOAL 1b — Big Integer menggunakan Python List
# ============================================================

class BigIntList:
    """
    Big Integer ADT — penyimpanan digit menggunakan Python list.
    Digit disimpan dari least-significant (index 0) ke most-significant.
    Contoh: 45839  →  [9, 3, 8, 5, 4]
    """

    # ----------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------
    def __init__(self, initValue="0"):
        self._digits   = []
        self._negative = False
        self._parse(str(initValue))

    def _parse(self, s: str):
        s = s.strip()
        if s.startswith("-"):
            self._negative = True
            s = s[1:]
        else:
            self._negative = False

        s = s.lstrip("0") or "0"
        # simpan dari least-significant ke most-significant
        self._digits = [int(ch) for ch in reversed(s)]

    # ----------------------------------------------------------
    # toString
    # ----------------------------------------------------------
    def toString(self) -> str:
        result = "".join(str(d) for d in reversed(self._digits)).lstrip("0") or "0"
        if self._negative and result != "0":
            return "-" + result
        return result

    def __repr__(self):
        return f"BigIntList('{self.toString()}')"

    # ----------------------------------------------------------
    # Helper
    # ----------------------------------------------------------
    def _to_int(self) -> int:
        return int(self.toString())

    @classmethod
    def _from_int(cls, n: int) -> "BigIntList":
        return cls(str(n))

    # ----------------------------------------------------------
    # comparable
    # ----------------------------------------------------------
    def comparable(self, other) -> int:
        a, b = self._to_int(), other._to_int()
        if a < b:  return -1
        if a > b:  return  1
        return 0

    def __lt__(self, other): return self.comparable(other) == -1
    def __le__(self, other): return self.comparable(other) <= 0
    def __gt__(self, other): return self.comparable(other) == 1
    def __ge__(self, other): return self.comparable(other) >= 0
    def __eq__(self, other): return self.comparable(other) == 0
    def __ne__(self, other): return self.comparable(other) != 0

    # ----------------------------------------------------------
    # arithmetic
    # ----------------------------------------------------------
    def arithmetic(self, rhsInt: "BigIntList", op: str) -> "BigIntList":
        a, b = self._to_int(), rhsInt._to_int()
        ops = {
            "+":  lambda x, y: x + y,
            "-":  lambda x, y: x - y,
            "*":  lambda x, y: x * y,
            "//": lambda x, y: x // y,
            "%":  lambda x, y: x %  y,
            "**": lambda x, y: x ** y,
        }
        if op not in ops:
            raise ValueError(f"Operator aritmetika tidak dikenal: {op}")
        return self._from_int(ops[op](a, b))

    def __add__(self, other): return self.arithmetic(other, "+")
    def __sub__(self, other): return self.arithmetic(other, "-")
    def __mul__(self, other): return self.arithmetic(other, "*")
    def __floordiv__(self, other): return self.arithmetic(other, "//")
    def __mod__(self, other): return self.arithmetic(other, "%")
    def __pow__(self, other): return self.arithmetic(other, "**")

    # ----------------------------------------------------------
    # bitwise
    # ----------------------------------------------------------
    def bitwise_ops(self, rhsInt: "BigIntList", op: str) -> "BigIntList":
        a, b = self._to_int(), rhsInt._to_int()
        ops = {
            "|":  lambda x, y: x |  y,
            "&":  lambda x, y: x &  y,
            "^":  lambda x, y: x ^  y,
            "<<": lambda x, y: x << y,
            ">>": lambda x, y: x >> y,
        }
        if op not in ops:
            raise ValueError(f"Operator bitwise tidak dikenal: {op}")
        return self._from_int(ops[op](a, b))

    def __or__ (self, other): return self.bitwise_ops(other, "|")
    def __and__(self, other): return self.bitwise_ops(other, "&")
    def __xor__(self, other): return self.bitwise_ops(other, "^")
    def __lshift__(self, other): return self.bitwise_ops(other, "<<")
    def __rshift__(self, other): return self.bitwise_ops(other, ">>")

    # ----------------------------------------------------------
    # SOAL 2 — Assignment combo operators
    # ----------------------------------------------------------
    def __iadd__(self, other):      return self.arithmetic(other, "+")
    def __isub__(self, other):      return self.arithmetic(other, "-")
    def __imul__(self, other):      return self.arithmetic(other, "*")
    def __ifloordiv__(self, other): return self.arithmetic(other, "//")
    def __imod__(self, other):      return self.arithmetic(other, "%")
    def __ipow__(self, other):      return self.arithmetic(other, "**")
    def __ilshift__(self, other):   return self.bitwise_ops(other, "<<")
    def __irshift__(self, other):   return self.bitwise_ops(other, ">>")
    def __ior__ (self, other):      return self.bitwise_ops(other, "|")
    def __iand__(self, other):      return self.bitwise_ops(other, "&")
    def __ixor__(self, other):      return self.bitwise_ops(other, "^")


# ============================================================
# DEMO / TEST
# ============================================================

def run_tests():
    print("=" * 60)
    print("SOAL 1a — BigIntLinkedList")
    print("=" * 60)

    a = BigIntLinkedList("45839")
    b = BigIntLinkedList("12345")

    print(f"a = {a.toString()}")
    print(f"b = {b.toString()}")

    # toString
    print(f"\n--- toString ---")
    print(f"a.toString() = {a.toString()}")

    # comparable
    print(f"\n--- comparable ---")
    print(f"a > b  : {a > b}")
    print(f"a < b  : {a < b}")
    print(f"a == b : {a == b}")
    print(f"a != b : {a != b}")

    # arithmetic
    print(f"\n--- arithmetic ---")
    print(f"a + b  = {a.arithmetic(b, '+').toString()}")
    print(f"a - b  = {a.arithmetic(b, '-').toString()}")
    print(f"a * b  = {a.arithmetic(b, '*').toString()}")
    print(f"a // b = {a.arithmetic(b, '//').toString()}")
    print(f"a % b  = {a.arithmetic(b, '%').toString()}")
    print(f"a ** 2 = {a.arithmetic(BigIntLinkedList('2'), '**').toString()}")

    # bitwise
    print(f"\n--- bitwise ---")
    x = BigIntLinkedList("60")   # 0b111100
    y = BigIntLinkedList("13")   # 0b001101
    print(f"x = {x.toString()}, y = {y.toString()}")
    print(f"x | y  = {x.bitwise_ops(y, '|').toString()}")
    print(f"x & y  = {x.bitwise_ops(y, '&').toString()}")
    print(f"x ^ y  = {x.bitwise_ops(y, '^').toString()}")
    print(f"x << 2 = {x.bitwise_ops(BigIntLinkedList('2'), '<<').toString()}")
    print(f"x >> 2 = {x.bitwise_ops(BigIntLinkedList('2'), '>>').toString()}")

    # SOAL 2 — assignment combo operators
    print(f"\n--- Soal 2: assignment combo operators (Linked List) ---")
    c = BigIntLinkedList("100")
    d = BigIntLinkedList("30")
    c += d;  print(f"c += d  → {c.toString()}")   # 130
    c -= d;  print(f"c -= d  → {c.toString()}")   # 100
    c *= d;  print(f"c *= d  → {c.toString()}")   # 3000
    c //= d; print(f"c //= d → {c.toString()}")   # 100
    c %= d;  print(f"c %= d  → {c.toString()}")   # 10
    c **= BigIntLinkedList("3"); print(f"c **= 3 → {c.toString()}")  # 1000
    e = BigIntLinkedList("60")
    e <<= BigIntLinkedList("2"); print(f"60 <<= 2 → {e.toString()}")  # 240
    e >>= BigIntLinkedList("1"); print(f"240 >>= 1 → {e.toString()}") # 120
    e |=  BigIntLinkedList("15"); print(f"120 |= 15  → {e.toString()}")
    e &=  BigIntLinkedList("127"); print(f"... &= 127 → {e.toString()}")
    e ^=  BigIntLinkedList("10"); print(f"... ^= 10  → {e.toString()}")

    print()
    print("=" * 60)
    print("SOAL 1b — BigIntList (Python list)")
    print("=" * 60)

    p = BigIntList("45839")
    q = BigIntList("12345")

    print(f"p = {p.toString()}")
    print(f"q = {q.toString()}")
    print(f"Digit list (LSB first): {p._digits}")

    # comparable
    print(f"\n--- comparable ---")
    print(f"p > q  : {p > q}")
    print(f"p < q  : {p < q}")
    print(f"p == q : {p == q}")

    # arithmetic
    print(f"\n--- arithmetic ---")
    print(f"p + q  = {p.arithmetic(q, '+').toString()}")
    print(f"p - q  = {p.arithmetic(q, '-').toString()}")
    print(f"p * q  = {p.arithmetic(q, '*').toString()}")
    print(f"p // q = {p.arithmetic(q, '//').toString()}")
    print(f"p % q  = {p.arithmetic(q, '%').toString()}")
    print(f"p ** 2 = {p.arithmetic(BigIntList('2'), '**').toString()}")

    # bitwise
    print(f"\n--- bitwise ---")
    u = BigIntList("60")
    v = BigIntList("13")
    print(f"u | v  = {u.bitwise_ops(v, '|').toString()}")
    print(f"u & v  = {u.bitwise_ops(v, '&').toString()}")
    print(f"u ^ v  = {u.bitwise_ops(v, '^').toString()}")
    print(f"u << 2 = {u.bitwise_ops(BigIntList('2'), '<<').toString()}")
    print(f"u >> 2 = {u.bitwise_ops(BigIntList('2'), '>>').toString()}")

    # SOAL 2 — assignment combo operators
    print(f"\n--- Soal 2: assignment combo operators (Python List) ---")
    r = BigIntList("100")
    s = BigIntList("30")
    r += s;  print(f"r += s  → {r.toString()}")   # 130
    r -= s;  print(f"r -= s  → {r.toString()}")   # 100
    r *= s;  print(f"r *= s  → {r.toString()}")   # 3000
    r //= s; print(f"r //= s → {r.toString()}")   # 100
    r %= s;  print(f"r %= s  → {r.toString()}")   # 10
    r **= BigIntList("3"); print(f"r **= 3 → {r.toString()}")  # 1000
    t = BigIntList("60")
    t <<= BigIntList("2"); print(f"60 <<= 2 → {t.toString()}")   # 240
    t >>= BigIntList("1"); print(f"240 >>= 1 → {t.toString()}")  # 120
    t |=  BigIntList("15"); print(f"... |= 15  → {t.toString()}")
    t &=  BigIntList("127"); print(f"... &= 127 → {t.toString()}")
    t ^=  BigIntList("10"); print(f"... ^= 10  → {t.toString()}")

    print("\nSemua test selesai!")


if __name__ == "__main__":
    run_tests()