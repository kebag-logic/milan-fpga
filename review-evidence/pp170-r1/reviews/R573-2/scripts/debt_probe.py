#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer debt probe for PR #172 N9 (issue #170).

Copies the four bench source directories into NEWDIR/<arm>/source, optionally
plants the debt-protection defect (the writer leaves the roll-back after its
two-cycle minimum regardless of the descriptor debt), and instruments N9 to
print, separately, how many table entries and how many GET_NAME answers differ
from the image defaults, whether READ_DESCRIPTOR serves the image ENTITY
names, and the restore terminal flags. Runs the N9 arm alone ("debt") in the
1x1 population at 39 entries and the 8x8 population at 107 entries.

usage: debt_probe.py --root CLONE --output NEWDIR --verilator PATH
"""
import argparse, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

WRITER = "hdl/aecp/KL_aecp_nvm_writer.sv"
DEFECT = ("          if (rb_min_r && !desc_debt_i) ws_r <= W_RELOC;\n",
          "          if (rb_min_r) ws_r <= W_RELOC;\n")
HOOK_OLD = "    CHECK(entries && gets,\n"
HOOK_NEW = ("    { unsigned be = 0, bg = 0;\n"
            "      for (const auto& n : named) { be += table_entry(n.ordinal) != defaults[n.ordinal];\n"
            "        bg += !get_reads(n, defaults[n.ordinal]); }\n"
            "      printf(\"PROBE N9 entries_differing=%u gets_differing=%u of %zu; entity_ok=%d; \"\n"
            "             \"done=%ld closed=%ld rb=%u cause=%u owed=%ld img_valid=%u\\n\", be, bg, named.size(),\n"
            "             int(entity_reads(defaults[0], defaults[1])), b.done, b.closed,\n"
            "             unsigned(x.d->restore_rb_o), unsigned(x.d->rs_cause_o), owed,\n"
            "             unsigned(x.d->dbg_img_valid_o)); }\n"
            "    CHECK(entries && gets,\n")


def arm(name, defect, root, out, vl):
    tree = out / name / "source"
    for d in ("hdl", "tb/common", "tb/pp_top", "tb/name_state"):
        shutil.copytree(root / d, tree / d, ignore=shutil.ignore_patterns("obj*", "__pycache__"))
    edits = [("tb/name_state/sim_main.cpp", HOOK_OLD, HOOK_NEW)]
    if defect:
        edits.append((WRITER,) + DEFECT)
    for f, old, new in edits:
        p = tree / f
        t = p.read_text()
        assert t.count(old) == 1, (f, old)
        p.write_text(t.replace(old, new))
    sys.path.insert(0, str(tree / "tb/name_state"))
    import run as bench  # noqa: E402  (the copied tree's own run.py)
    import fixture  # noqa: E402
    logs = []
    for population, names in bench.NAMES.items():
        where = out / name / f"names-{population}"
        where.mkdir()
        binary = bench.build(tree, where, vl, bench.capacity(names))
        image = where / "image.bin"
        image.write_bytes(fixture.packer(tree).build(fixture.fixture(population), lint=False)[0])
        r = subprocess.run([str(binary), str(image), str(population), "debt"], cwd=where,
                           text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logs.append(f"== {name} population {population} at {names} entries rc={r.returncode}\n{r.stdout}")
    return "".join(logs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--verilator", required=True)
    a = ap.parse_args()
    a.output.mkdir(parents=True)
    root = a.root.resolve()
    for name, defect in (("intact", False), ("rollback_ignores_debt", True)):
        print(arm(name, defect, root, a.output.resolve(), a.verilator), end="", flush=True)


if __name__ == "__main__":
    main()
