#!/usr/bin/env python3
"""Compare protocol_processor_top's parameter and port declarations across revisions.

Reads the module header (from `module protocol_processor_top` to the first
`);` that closes the port list) at each revision with `git show`, strips
comments, and lists parameter names and port names with their declared text.
Reports the set differences: lane round 3 vs head, main vs head, and the
merge identity head == main + (lane3 - base).

usage: top_ports.py <repo>
"""
import re
import subprocess
import sys

F = "hdl/top/protocol_processor_top.sv"
REVS = {"base_3f3ea56b": "3f3ea56ba61829718a6a288600ab4fdac73aa5ba",
        "lane3_9624ef4c": "9624ef4c452d708de68a901d5e645bdfa1f5d6f5",
        "main_03c842a7": "03c842a780064048b0a1a3de29214174a1c13934",
        "head_95a78c0": "95a78c099ee5aa914521975355adc1dfef99d01c"}


def header(repo, rev):
    src = subprocess.run(["git", "-C", repo, "show", f"{rev}:{F}"], check=True,
                         capture_output=True, text=True).stdout
    src = re.sub(r"//[^\n]*", "", src)
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    start = src.index("module protocol_processor_top")
    depth, i = 0, src.index("(", start)
    # parameter list #( ... ) then port list ( ... );
    out = []
    j = start
    while True:
        k = src.index("(", j)
        depth = 0
        for p in range(k, len(src)):
            if src[p] == "(":
                depth += 1
            elif src[p] == ")":
                depth -= 1
                if depth == 0:
                    out.append(src[k + 1:p])
                    j = p + 1
                    break
        if src[j:].lstrip().startswith(";"):
            break
    params_txt = out[0] if len(out) > 1 else ""
    ports_txt = out[-1]
    params = {}
    for m in re.finditer(r"parameter\s+(?:[\w:\[\]\s\-\+\*\(\)']*?\s)?(\w+)\s*=\s*([^,]+)", params_txt):
        params[m.group(1)] = " ".join(m.group(2).split())
    ports = {}
    for m in re.finditer(r"\b(input|output|inout)\b([^;]*?)(?=,\s*\b(?:input|output|inout)\b|$)", ports_txt, flags=re.S):
        decl = " ".join((m.group(1) + m.group(2)).split()).rstrip(",")
        names = re.findall(r"(\w+)\s*(?:\[[^\]]*\]\s*)*(?:,|$)", decl)
        for n in names:
            if n not in ("input", "output", "inout", "logic", "wire", "reg", "signed"):
                ports[n] = decl
    return params, ports


def main():
    repo = sys.argv[1]
    d = {k: header(repo, v) for k, v in REVS.items()}
    for k, (pa, po) in d.items():
        print(f"{k}: {len(pa)} parameters, {len(po)} port names")
    hp, ho = d["head_95a78c0"]
    for k in ("lane3_9624ef4c", "main_03c842a7"):
        pa, po = d[k]
        print(f"\n{k} vs head:")
        print("  params only in head:", sorted(set(hp) - set(pa)))
        print("  params only in", k, ":", sorted(set(pa) - set(hp)))
        print("  params whose default differs:", sorted(n for n in set(hp) & set(pa) if hp[n] != pa[n]))
        print("  ports only in head:", sorted(set(ho) - set(po)))
        print("  ports only in", k, ":", sorted(set(po) - set(ho)))
        print("  ports whose declaration differs:", sorted(n for n in set(ho) & set(po) if ho[n] != po[n]))
    bp, bo = d["base_3f3ea56b"]
    lp, lo = d["lane3_9624ef4c"]
    mp, mo = d["main_03c842a7"]
    print("\nlane's own additions over base: params", sorted(set(lp) - set(bp)), "ports", sorted(set(lo) - set(bo)))
    print("main's additions over base: params", sorted(set(mp) - set(bp)), "ports", sorted(set(mo) - set(bo)))
    exp_p, exp_o = set(mp) | (set(lp) - set(bp)), set(mo) | (set(lo) - set(bo))
    print("head params == main + lane additions:", set(hp) == exp_p, "; ports:", set(ho) == exp_o)


if __name__ == "__main__":
    main()
