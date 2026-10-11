"""Compare two sv2v outputs module by module. Usage: modcmp.py <a.v> <b.v> <label-a> <label-b>"""
import hashlib, re, sys
def split(path):
    text = open(path).read()
    mods, rest, pos = {}, [], 0
    for m in re.finditer(r"^module\s+(\w+).*?^endmodule\b", text, re.M | re.S):
        rest.append(text[pos:m.start()]); pos = m.end()
        mods[m.group(1)] = m.group(0)
    rest.append(text[pos:])
    return mods, "".join(rest)
(a, ra), (b, rb) = split(sys.argv[1]), split(sys.argv[2])
h = lambda s: hashlib.sha256(s.encode()).hexdigest()[:16]
print(f"module\t{sys.argv[3]} sha256[:16]\t{sys.argv[4]} sha256[:16]\tidentical")
for name in sorted(set(a) | set(b)):
    x, y = a.get(name, ""), b.get(name, "")
    print(f"{name}\t{h(x)}\t{h(y)}\t{'yes' if x == y else 'NO'}")
print("text outside modules identical:", ra == rb)
