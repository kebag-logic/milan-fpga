#!/usr/bin/env python3
"""Plant stricter L6 readings in disposable copies and run the packer gate.

Usage: l6_plants.py <clean clone at the head> <clean clone at the merge> <work dir>

Each plant inserts one refusal into hdl/aecp/desc/model_rules.py of a copy of
each clone (only hdl/aecp/desc and tb/desc_store are copied), then runs the
whole gate (test_gen_desc_image.py). A plant is KILLED by a tree's gate when
the gate fails. The head clone carries the round-4 positive case; the merge
clone does not, so the pair shows what the new test adds.
"""
import shutil
import subprocess
import sys
from pathlib import Path

ANCHOR_SRC = "        if ctx.of(cfg, D.STREAM_OUTPUT) and not any(k[0] == INTERNAL for k in kinds.values()):\n"
ANCHOR_DOM = ('            if count == 0:\n'
              '                ctx.bad("domain-source-count", where, "clock_sources_count 0")\n')
BAD_SRC = '            ctx.bad("aaf-input-source", (cfg, D.CLOCK_SOURCE, None), "PLANT")\n'
BAD_DOM = '                ctx.bad("domain-source-count", where, "PLANT")\n'

# name -> (anchor, inserted condition line, refusal line, expectation note)
PLANTS = {
    "aaf-at-most-one-beside-crf": (ANCHOR_SRC,
        "        if crf_in and sum(at_input[k] for k in aaf_in) > 1:\n", BAD_SRC),
    "aaf-none-beside-crf": (ANCHOR_SRC,
        "        if crf_in and sum(at_input[k] for k in aaf_in) > 0:\n", BAD_SRC),
    "domain-count-cap-8": (ANCHOR_DOM, "            if count > 8:\n", BAD_DOM),
    "domain-count-cap-9": (ANCHOR_DOM, "            if count > 9:\n", BAD_DOM),
    "input-stream-sources-at-most-two": (ANCHOR_SRC,
        "        if sum(at_input.values()) > 2:\n", BAD_SRC),
    # the reviewer's own readings
    "aaf-source-only-below-input-2": (ANCHOR_SRC,
        "        if crf_in and any(at_input[k] for k in aaf_in if k >= 2):\n", BAD_SRC),
    "sources-at-most-stream-inputs": (ANCHOR_SRC,
        "        if len(kinds) > len(ctx.of(cfg, D.STREAM_INPUT)):\n", BAD_SRC),
    "one-aaf-input-with-a-source": (ANCHOR_SRC,
        "        if len([k for k in aaf_in if at_input[k]]) > 1:\n", BAD_SRC),
    "crf-source-after-aaf-sources": (ANCHOR_SRC,
        "        if any(q[0] == INPUT_STREAM and q[2] in crf_in and any(r[0] == INPUT_STREAM "
        "and r[2] in aaf_in and j > i for j, r in kinds.items()) for i, q in kinds.items()):\n",
        BAD_SRC),
    "clock-source-descriptors-cap-9": (ANCHOR_SRC, "        if len(kinds) > 9:\n", BAD_SRC),
    # order readings: main's L6 lets the consumer order the list; the lint
    # claims to read no order. These refuse orders other than D1's, so the D1
    # positive case is expected to pack under them (informational).
    "order-internal-first": (ANCHOR_SRC,
        "        if kinds and kinds.get(0, (None,))[0] != INTERNAL:\n", BAD_SRC),
    "domain-count-cap-215": (ANCHOR_DOM, "            if count > 215:\n", BAD_DOM),
}


def plant_tree(src: Path, dst: Path, anchor: str, cond: str, bad: str) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    for rel in ("hdl/aecp/desc", "tb/desc_store"):
        shutil.copytree(src / rel, dst / rel, ignore=shutil.ignore_patterns("obj_dir", "__pycache__"))
    rules = dst / "hdl/aecp/desc/model_rules.py"
    text = rules.read_text(encoding="utf-8")
    assert text.count(anchor) == 1, f"anchor not unique in {src}"
    rules.write_text(text.replace(anchor, cond + bad + anchor), encoding="utf-8")


def gate(tree: Path) -> tuple[int, list[str]]:
    run = subprocess.run([sys.executable, "-B", "test_gen_desc_image.py"],
                         cwd=tree / "tb/desc_store", capture_output=True, text=True)
    failing = sorted({line.split(" (")[0].split(": ", 1)[1] + " " + line.split("(")[1].split(")")[0]
                      for line in run.stderr.splitlines()
                      if line.startswith(("FAIL: ", "ERROR: "))})
    return run.returncode, failing


def main() -> int:
    head, merge, work = (Path(a) for a in sys.argv[1:4])
    for tree in (head, merge):
        rc, failing = gate(tree)
        print(f"control {tree.name}: rc={rc} {'PASS' if rc == 0 else 'FAIL ' + str(failing)}")
        if rc:
            return 2
    for name, (anchor, cond, bad) in PLANTS.items():
        res = {}
        for label, tree in (("head", head), ("merge", merge)):
            dst = work / f"{name}.{label}"
            plant_tree(tree, dst, anchor, cond, bad)
            res[label] = gate(dst)
            shutil.rmtree(dst)
        verdict = {k: ("KILLED" if v[0] else "SURVIVED") for k, v in res.items()}
        print(f"{name}: head {verdict['head']} {res['head'][1]}; "
              f"merge {verdict['merge']} {res['merge'][1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
