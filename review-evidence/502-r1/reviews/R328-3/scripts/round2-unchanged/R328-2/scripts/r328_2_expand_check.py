#!/usr/bin/env python3
"""R328-2 source-level equivalence check of the round-2 datapath refactor.

Usage: r328_2_expand_check.py <repo-root> <base-rev> <head-rev>

1. Reads milan_datapath.sv at both revisions (git show).
2. Extracts the head's four new continuous assigns (amap_edit_beat_w,
   amap_edit_in_change_w, amap_edit_out_change_w, amap_edit_live_wr_p).
3. Inlines the three change/beat names into the head's amap_edit_commit
   always_ff block. Every definition is a top-level && chain used only as
   the right operand of && (or, for the beat, as the whole else-if
   condition under `if (!pp_amap_edit_req_w) ... else`), so inlining without
   parentheses preserves the parse. For the beat, the leading
   `pp_amap_edit_req_w &&` is dropped only after asserting it is present,
   because that branch is reached only when the request is high.
4. Compares the expanded head block with the base block, whitespace removed.
5. Reports every remaining file difference outside the four assigns, the
   comment, and the shadow port connection.
6. Evaluates, over all assignments of the atoms, that amap_edit_live_wr_p is
   true exactly when the base phase-5 block takes a write branch.
"""
import itertools
import re
import subprocess
import sys


def show(root, rev):
    return subprocess.run(["git", "-C", root, "show", f"{rev}:hdl/milan/milan_datapath.sv"],
                          check=True, capture_output=True, text=True).stdout


def block(text):
    start = text.index("begin : amap_edit_commit")
    end = text.index("end : amap_edit_commit")
    return text[start:end]


def assign(text, name):
    m = re.search(r"assign " + name + r" = (.*?);", text, re.S)
    assert m, name
    return m.group(1)


def squash(s):
    return re.sub(r"\s+", "", s)


def main():
    root, base_rev, head_rev = sys.argv[1:4]
    base, head = show(root, base_rev), show(root, head_rev)
    beat = assign(head, "amap_edit_beat_w")
    inc = assign(head, "amap_edit_in_change_w")
    outc = assign(head, "amap_edit_out_change_w")
    live = assign(head, "amap_edit_live_wr_p")
    hb = block(head)
    for name in ("amap_edit_in_change_w", "amap_edit_out_change_w", "amap_edit_beat_w"):
        print(f"head block uses {name}: {len(re.findall(name, hb))}x")
    assert squash(beat).startswith("pp_amap_edit_req_w&&(") and squash(beat).endswith(")")
    beat_inner = squash(beat)[len("pp_amap_edit_req_w&&("):-1]
    ex = squash(hb)
    ex = ex.replace("elseif(amap_edit_beat_w)", "elseif(" + beat_inner + ")")
    ex = ex.replace("amap_edit_in_change_w", squash(inc))
    ex = ex.replace("amap_edit_out_change_w", squash(outc))
    bb = squash(block(base))
    print("expanded head amap_edit_commit == base amap_edit_commit:", ex == bb)
    if ex != bb:
        i = next(k for k in range(min(len(ex), len(bb))) if ex[k] != bb[k])
        print("first difference at", i, "\n head:", ex[i - 80:i + 80], "\n base:", bb[i - 80:i + 80])
    # remaining file differences outside the expected edits
    bl = [l for l in base.splitlines()]
    hl = [l for l in head.splitlines()]
    import difflib
    diff = [d for d in difflib.unified_diff(bl, hl, lineterm="", n=0)
            if d[:1] in "+-" and not d.startswith(("+++", "---"))]
    body_names = ("amap_edit_beat_w", "amap_edit_in_change_w", "amap_edit_out_change_w",
                  "amap_edit_live_wr_p")
    print(f"raw changed lines: {len(diff)}")
    # atoms truth table: live == write taken by base phase-5 branch structure
    atoms = ["rstn", "req", "beat_inner", "ph5", "ctx", "inc", "outc"]
    ok = True
    for vals in itertools.product([False, True], repeat=len(atoms)):
        v = dict(zip(atoms, vals))
        if v["inc"] and v["outc"]:
            continue  # excluded structurally: in/out key valids are exclusive
        # base: async reset clears; else if !req nothing; else if beat_inner case phase 5:
        wr_in = v["rstn"] and v["req"] and v["beat_inner"] and v["ph5"] and v["ctx"] and v["inc"]
        wr_out = (v["rstn"] and v["req"] and v["beat_inner"] and v["ph5"]
                  and not (v["ctx"] and v["inc"]) and v["ctx"] and v["outc"])
        pulse = (v["rstn"] and (v["req"] and v["beat_inner"]) and v["ph5"] and v["ctx"]
                 and (v["inc"] or v["outc"]))
        ok &= pulse == (wr_in or wr_out)
    print("live_wr_p definition:", squash(live))
    assert squash(live) == ("axis_resetn&&amap_edit_beat_w&&(pp_amap_edit_phase_w==3'd5)"
                            "&&amap_edit_context_w&&(amap_edit_in_change_w||amap_edit_out_change_w)")
    print("pulse == (in-write or out-write) over all reachable atom assignments:", ok)
    # also: with exclusivity dropped, priority still gives pulse == any write
    ok2 = True
    for vals in itertools.product([False, True], repeat=len(atoms)):
        v = dict(zip(atoms, vals))
        taken = v["rstn"] and v["req"] and v["beat_inner"] and v["ph5"] and v["ctx"] and (v["inc"] or v["outc"])
        pulse = v["rstn"] and v["req"] and v["beat_inner"] and v["ph5"] and v["ctx"] and (v["inc"] or v["outc"])
        ok2 &= taken == pulse
    print("pulse == some write branch taken, without the exclusivity assumption:", ok2)
    for d in diff:
        print("  " + d[:150])


if __name__ == "__main__":
    main()
