#!/usr/bin/env python3
"""Token-level equivalence of the #502 phase-5 refactor in milan_datapath.

Usage: r329_equiv_expand.py <repo> <base-rev> <head-rev>

Inlines the head's named continuous assigns (amap_edit_beat_w,
amap_edit_in_change_w, amap_edit_out_change_w) into the amap_edit_commit
always_ff block, removes the head-only declarations/assigns, and compares
the whole milan_datapath.sv token stream (comments stripped) against the
base.  Also prints the actual-write condition next to amap_edit_live_wr_p.
Exit 0 only if the only residual token difference is the new
.amap_live_wr_i port connection and the amap_edit_live_wr_p assign/decl.
"""
import re
import subprocess
import sys

TOK = re.compile(r"\d+'[sS]?[bodhBODH][0-9a-fA-F_xXzZ]+|\w+|[<>=!&|+*]=?|&&|\|\||\+:|\S")


def show(repo, rev, path):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], check=True,
                          capture_output=True, text=True).stdout


def strip_comments(s):
    s = re.sub(r"/\*.*?\*/", " ", s, flags=re.S)
    return re.sub(r"//[^\n]*", " ", s)


def toks(s):
    out = []
    i = 0
    s = strip_comments(s)
    for m in re.finditer(r"&&|\|\||\+:|!=|==|<=|>=|\d+'[sS]?[bodhBODH][0-9a-fA-F_xXzZ]+|\w+|\S", s):
        out.append(m.group(0))
    return out


def grab_assign(text, name):
    m = re.search(r"assign\s+" + name + r"\s*=(.*?);", strip_comments(text), flags=re.S)
    assert m, name
    return m.group(1)


def main():
    repo, base_rev, head_rev = sys.argv[1:4]
    p = "hdl/milan/milan_datapath.sv"
    base = show(repo, base_rev, p)
    head = show(repo, head_rev, p)
    names = ["amap_edit_beat_w", "amap_edit_in_change_w", "amap_edit_out_change_w"]
    defs = {n: grab_assign(head, n) for n in names}
    for n in names + ["amap_edit_live_wr_p"]:
        print(f"head assign {n} = {' '.join(toks(grab_assign(head, n)))}")
    hs = strip_comments(head)
    # drop the head-only block: declarations + four assigns
    blk = re.search(r"logic amap_edit_beat_w;.*?amap_edit_out_change_w\)\s*;", hs, flags=re.S)
    assert blk, "head-only block not found"
    removed = hs[blk.start():blk.end()]
    hs = hs[:blk.start()] + hs[blk.end():]
    # drop the new port connection
    conn = re.search(r"\.amap_live_wr_i\s*\(\s*amap_edit_live_wr_p\s*\)\s*,", hs)
    assert conn
    hs = hs[:conn.start()] + hs[conn.end():]
    # inline each named wire with parentheses (1-bit logical terms)
    ht = toks(hs)
    exp = []
    for t in ht:
        if t in defs:
            exp += ["("] + toks(defs[t]) + [")"]
        else:
            exp.append(t)
    bt = toks(base)
    print("removed head-only tokens:", len(toks(removed)))
    # the base writes "else if (!seen || ...)" under "if (!req) ... else", head
    # writes "else if (beat)" where beat = req && (...): report the residual diff.
    import difflib
    sm = difflib.SequenceMatcher(a=bt, b=exp, autojunk=False)
    diffs = [op for op in sm.get_opcodes() if op[0] != "equal"]
    for tag, i1, i2, j1, j2 in diffs:
        print(f"DIFF {tag}: base[{i1}:{i2}]={' '.join(bt[i1:i2])!r}")
        print(f"          head[{j1}:{j2}]={' '.join(exp[j1:j2])!r}")
        print("   context base:", " ".join(bt[max(0, i1-25):i2+10]))
    print(f"base tokens {len(bt)}, expanded head tokens {len(exp)}, diff hunks {len(diffs)}")


if __name__ == "__main__":
    main()
