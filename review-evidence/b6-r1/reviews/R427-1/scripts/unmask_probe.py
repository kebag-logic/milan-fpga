#!/usr/bin/env python3
"""Try to reproduce the page-cited (unmasked) hash of a label-masked evidence file by
substituting small integers for the capture-layout labels. Prints only MATCH/NO MATCH,
never the substituted values (they are the masked capture layout).

usage: unmask_probe.py <masked file> <target sha256> <mode: tool|events>
"""
import hashlib, itertools, sys
path, target, mode = sys.argv[1], sys.argv[2], sys.argv[3]
src = open(path, "rb").read()
def h(b): return hashlib.sha256(b).hexdigest()
found = False
if mode == "tool":
    # <capture-channel-count> and <n> -> N (or f-string forms); indices -> L, R
    cnt = src.count(b"<capture-channel-index>")
    nforms = [None, b"{NCH}", b"{nch}"]
    for n in range(1, 65):
        for nf in nforms:
            base = src.replace(b"<capture-channel-count>", str(n).encode())
            base = base.replace(b"<n>", str(n).encode() if nf is None else nf)
            if cnt == 0:
                if h(base) == target: found = True; break
                continue
            for L, R in itertools.product(range(n), repeat=2):
                b = base
                for v in ([L, R] if cnt == 2 else [L, L, R][:cnt] if cnt == 3 else [L]):
                    b = b.replace(b"<capture-channel-index>", str(v).encode(), 1)
                if h(b) == target: found = True; break
                if cnt == 3:
                    # line 14 may carry a pair "L and R"/"L/R"
                    for sep in (b" and ", b"/", b", ", b" + "):
                        b2 = base.replace(b"<capture-channel-index>", str(L).encode() + sep + str(R).encode(), 1)
                        b2 = b2.replace(b"<capture-channel-index>", str(L).encode(), 1).replace(b"<capture-channel-index>", str(R).encode(), 1)
                        if h(b2) == target: found = True; break
                if found: break
            if found: break
        if found: break
elif mode == "events":
    for n in range(1, 65):
        b0 = src.replace(b"<n>", str(n).encode())
        for secs in list(range(1, 700)):
            for frames in (48000 * secs,):
                nb = frames * 3 * n
                b = b0.replace(b'"<withheld>"', str(nb).encode())
                if h(b) == target: found = True; break
            if found: break
        if found: break
print(path.split("author/")[-1], "MATCH" if found else "NO MATCH")
