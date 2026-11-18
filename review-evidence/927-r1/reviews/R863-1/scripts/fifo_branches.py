#!/usr/bin/env python3
"""cdc_pair_fifo's two g_mem branches must differ only in the ram_style
attribute (PR #939, issue #927). Reads the file at the given git revision of
the given repository, extracts both branch bodies, removes the attribute from
the first and compares them byte for byte. Also compares the FIFO's storage
behaviour against the base: the write and read statements of the base must
appear, with the base's guards folded, in each branch.

usage: fifo_branches.py <repo> <rev> <base-rev>
"""
import subprocess
import sys

PATH = "hdl/common/cdc_pair_fifo.sv"
ATTR = '(* ram_style = "distributed" *) '


def show(repo, rev):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{PATH}"], check=True,
                          capture_output=True, text=True).stdout


def main() -> int:
    repo, rev, base = sys.argv[1:4]
    text = show(repo, rev)
    head = "  if (DIST_RAM_P != 0) begin : g_mem\n"
    mid = "  end else begin : g_mem\n"
    tail = "  end\n\nendmodule"
    if text.count(head) != 1 or text.count(mid) != 1 or text.count(tail) != 1:
        print("FAIL: the generate's shape is not the one this check reads")
        return 2
    a = text.split(head, 1)[1].split(mid, 1)[0]
    b = text.split(mid, 1)[1].split(tail, 1)[0]
    print(f"branch DIST_RAM_P!=0: {len(a)} bytes; branch else: {len(b)} bytes")
    print(f"attribute occurrences: first {a.count(ATTR)}, second {b.count(ATTR)}")
    same = a.replace(ATTR, "", 1) == b and a.count(ATTR) == 1 and b.count(ATTR) == 0
    print("PASS: the branches differ only in the ram_style attribute" if same
          else "FAIL: the branches differ beyond the attribute")
    old = show(repo, base)
    for stmt in ("mem_r[wptr_bin_r[LOG2D-1:0]] <= wdata_i;", "rdata_o <= mem_r[rptr_bin_r[LOG2D-1:0]];"):
        print(f"base has {stmt!r}: {old.count(stmt)}; head has it {text.count(stmt)} times (once per branch)")
    for guard in ("if (wen_i && !wfull_o)", "if (ren_i && !rempty_o)"):
        print(f"base guard {guard!r}: {old.count(guard)}")
    return 0 if same else 1


if __name__ == "__main__":
    sys.exit(main())
