# PAGE 3 — Functional Programming + FSM + SymPy
*(Handwrite this on A4 sheet 3 — draw the FSM diagram and tables by hand)*

---

## 1. Functional Programming Concepts Used (5 concepts)

### (a) Higher-order function + closure
`make_bill_calculator()` is a function that **returns another function**
capturing its tariff rates (peak Rs 4/unit, off-peak Rs 2/unit):

```python
def make_bill_calculator(peak_rate=4.0, offpeak_rate=2.0):
    def calculate(peak_units, offpeak_units):        # closure
        return round(peak_units * peak_rate + offpeak_units * offpeak_rate, 2)
    return calculate

TOU_BILL = make_bill_calculator(4.0, 2.0)
# TOU_BILL(8, 4) = 8*4 + 4*2 = Rs 40.0
```

### (b) map — transform every record
```python
billed = list(map(enrich, valid))     # each record -> total_units + tou_bill
```

### (c) filter — select records by condition
```python
valid   = list(filter(is_valid, records))                       # drop bad rows
high    = list(filter(lambda r: r["total_units"] >= 20, billed)) # high usage
```

### (d) reduce — fold records into totals
```python
grand_units = reduce(lambda acc, r: acc + r["total_units"], billed, 0)   # 223.0
grand_bill  = reduce(lambda acc, r: acc + r["tou_bill"],  billed, 0)     # Rs 780
```

### (e) lambda as key in sorted — consumer ranking
```python
ranked = sorted(summaries, key=lambda c: c["total_units"], reverse=True)
```

---

## 2. Finite State Machine (FSM)

**States (4):** `LOW`, `MODERATE`, `HIGH`, `OVERLOAD` — start state: LOW
**Inputs:** daily total consumption band — `LT10` (<10), `B10_19` (10–19),
`B20_29` (20–29), `GE30` (≥30)

```
                    LT10      B10_19        B20_29       GE30
                 ┌────────► LOW ──────► MODERATE ─────► HIGH ──────► OVERLOAD ─┐
                 │          ▲  ◄──────────┴──────────────┴───────────────┘    │
  (start) ───────┘          └──── any lower band moves the state back down ───┘
```

**Complete transition table (4 × 4 = 16 transitions):**

| Current state \ Input | LT10 (<10) | B10_19 (10–19) | B20_29 (20–29) | GE30 (≥30) |
|---|---|---|---|---|
| LOW | LOW | MODERATE | HIGH | OVERLOAD |
| MODERATE | LOW | MODERATE | HIGH | OVERLOAD |
| HIGH | LOW | MODERATE | HIGH | OVERLOAD |
| OVERLOAD | LOW | MODERATE | HIGH | OVERLOAD |

**Worked example — Ramesh (C01):** daily totals 12, 18, 26
FSM path: `LOW →(12) MODERATE →(18) MODERATE →(26) HIGH` → final state **HIGH**
→ recommendation: *"High load — review appliances, consider rooftop solar."*

Final state drives the recommendation: LOW = normal, MODERATE = shift usage to
off-peak, HIGH = review appliances, OVERLOAD = immediate action.

---

## 3. Symbolic Computing with SymPy (3 operations)

### (a) Symbolic slab tariff model
First 50 units @ Rs 3; above 50 @ Rs 5:

```python
x = symbols("x")
bill_expr = Piecewise((3*x, x <= 50), (3*50 + 5*(x - 50), x > 50))
```
Example: Arun's total = 100 units → bill_expr(100) = 150 + 5(50) = **Rs 400**

### (b) Trend line fitted by solving normal equations (least squares)
For Ramesh's daily totals y = (12, 18, 26) at days x = (1, 2, 3):
n=3, Σx=6, Σy=56, Σx²=14, Σxy=126. SymPy solves:

```
14a + 6b = 126          →  a = 7,  b = 14/3 = 4.6667
 6a + 3b =  56
```
**y = 7x + 4.6667** → predicted day-4 consumption = 7(4) + 4.6667 = **32.67 units**

### (c) Budget break-even solve
Monthly budget = Rs 500. SymPy solves `bill_expr(x) − 500 = 0` in each slab
domain and keeps the valid root:

```
3x = 500            → x = 166.67  (rejected: > 50, outside slab 1)
150 + 5(x−50) = 500 → x = 50 + 350/5 = 120 units  ✔ (inside slab 2)
```
**Maximum affordable consumption = 120 units.**
Consumers whose slab bill exceeds Rs 500 are flagged
(over-budget list in the report — e.g. C07 Suresh in test case 2).
