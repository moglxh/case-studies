import sys

brand = sys.argv[1]

# a tiny "nearby key / similar sound" map used for substitution
neighbors = {"a": "s", "o": "p", "v": "b", "b": "v", "n": "m", "t": "r"}

def omission(w):
    return [w[:i] + w[i+1:] for i in range(len(w))]

def duplication(w):
    return [w[:i+1] + w[i] + w[i+1:] for i in range(len(w))]

def transposition(w):
    out = []
    for i in range(len(w) - 1):
        if w[i] != w[i+1]:
            out.append(w[:i] + w[i+1] + w[i] + w[i+2:])
    return out

def substitution(w):
    out = []
    for i, ch in enumerate(w):
        if ch in neighbors:
            out.append(w[:i] + neighbors[ch] + w[i+1:])
    return out

def lookalike(w):
    out = []
    for i, ch in enumerate(w):
        if ch == "o":
            out.append(w[:i] + "0" + w[i+1:])
    return out

classes = [
    ("omission", omission),
    ("duplication", duplication),
    ("transposition", transposition),
    ("substitution", substitution),
    ("lookalike", lookalike),
]

everything = []
for name, fn in classes:
    results = fn(brand)
    print(f"{name} ({len(results)})")
    for r in results:
        print("  " + r)
    everything += results

with open("typos.txt", "w") as f:
    for r in everything:
        f.write(r + "\n")

print(f"total: {len(everything)}")
