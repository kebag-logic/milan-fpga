#!/usr/bin/env python3
"""Reviewer probes for PR #913 round 2 (#911): baseline gates and single-point
mutants, each planted alone in its own clone of the head so they run at once.

usage: r841_2_probes.py <source repo> <head sha> <work dir> <litex python> [jobs]

For each case: clone <source repo> at <head sha> into <work dir>/<case>, plant
the one edit (anchor must occur exactly once), run the named gates, record rc
and the last failing line, restore the file and check the clone is clean.
Exit 0 when every baseline gate passes and every mutant's expectation holds.
"""
import concurrent.futures
import os
import subprocess
import sys
from pathlib import Path

SRC, HEAD, WORK, LITEX_PY = sys.argv[1], sys.argv[2], Path(sys.argv[3]), sys.argv[4]
JOBS = int(sys.argv[5]) if len(sys.argv) > 5 else 8

G1E = ("gate 1e", ["python3", "-B", "sw/builder/test_builder.py", "--gates",
                   "test_qspi_owner_transition_completed_write_prefixes"])
TG = ("test_timing_grade.py", ["python3", "-B", "sw/builder/test_timing_grade.py", LITEX_PY])
TGG = ("gate test_commercial_timing_grade",
       ["python3", "-B", "sw/builder/test_builder.py", "--gates", "test_commercial_timing_grade"])
QT = "sw/litex/qspi_owner_transition.py"
# Submodules the gates read, filled from the source repo's own checkouts at
# the head's gitlinks (no network).
SUBMODULES = ("protocol-processor", "gptp-processor", "third_party/lwSRP",
              "third_party/tsn-c-stack", "third_party/verilog-axis")

# (case, file, anchor, replacement, gates, expect: "red" | "green")
CASES = [
    ("BASE", None, None, None, [G1E, TG, TGG], "green"),
    ("K3", QT, "    if len(ids) != 1:", "    if not ids:", [G1E], "red"),
    ("K4", QT, "    if len(models) != 1:", "    if not models:", [G1E], "red"),
    ("K7", "sw/litex/layout_from_soch.py", '"addr": 0x0, "budget": aem["offset"]})',
     '"addr": 0x0, "budget": 0x40_0000})', [TG, TGG], "red"),
    ("K9", QT, '    budget = bit_rows[0].get("budget", bit_rows[0].get("size"))\n',
     '    budget = min(bit_rows[0].get("budget", bit_rows[0].get("size")), 0x40_0000)\n',
     [G1E, TG, TGG], "red"),
    # The round's new rule: a chain of two equal dies. Counting distinct
    # models again must turn gate 1e red.
    ("R1-distinct-models", QT, "    if len(models) != 1:", "    if len(set(models)) != 1:",
     [G1E], "red"),
    # The deploy write offset of the AEM image pinned to the AX7101's 4 MiB:
    # the 200T arm must see the AEM land somewhere other than 0xA00000.
    ("R2-aem-offset-pinned", "sw/litex/deploy.sh",
     '    print("%s\\t%d\\t%d" % (row["name"], off, top))',
     '    print("%s\\t%d\\t%d" % (row["name"], 0x400000 if row["name"] == "aem" else off, top))',
     [G1E], "red"),
    # The die slot table loses the 200T entry: layout_for() keeps the AX7101
    # map for the 200T, so the soc.h rebuild test must go red.
    ("R3-slot-table-empty", "sw/litex/milan_soc.py",
     'FLASHBOOT_BITSTREAM_SLOT = {"xc7a200t-fbg484-2": 0xA0_0000}',
     'FLASHBOOT_BITSTREAM_SLOT = {}', [TG, TGG], "red"),
    # The 200T arm's own map edit removed: the 9,730,652-B payload on the
    # AX7101 map must be refused, so the arm depends on the 0xA00000 map.
    ("R4-arm-on-4MiB-map", "sw/builder/test_builder.py",
     '            rows["bitstream"]["budget"] = rows["aem"]["offset"] = 0xA00000\n', '', [G1E], "red"),
    # The first refusal line's wording reverted: no gate reads that line, so
    # the gate stays green (recorded as the absence of a control).
    ("R5-first-message-reverted", "sw/litex/deploy.sh",
     "the image set's layout or the FPGA on the cable fails the board check.",
     "the FPGA on the cable is not the image set's part.", [G1E], "green"),
]


def sh(argv, cwd, env=None, timeout=1500):
    return subprocess.run(argv, cwd=cwd, text=True, capture_output=True, env=env, timeout=timeout)


def one(case):
    name, rel, old, new, gates, expect = case
    tree = WORK / name
    if not tree.exists():
        sh(["git", "clone", "-q", "--no-checkout", SRC, str(tree)], WORK)
        sh(["git", "checkout", "-q", HEAD], tree)
    for sub in SUBMODULES:
        if not (tree / sub / ".git").exists():
            sh(["git", "config", f"submodule.{sub}.url", str(Path(SRC) / sub)], tree)
            sh(["git", "-c", "protocol.file.allow=always", "submodule", "update", "--init", sub], tree)
    head = sh(["git", "rev-parse", "HEAD"], tree).stdout.strip()
    out = [f"== {name} at {head}, expect {expect}"]
    env = dict(os.environ, MILAN_LITEX_PYTHON=LITEX_PY, TMPDIR=str(WORK / f"tmp-{name}"))
    Path(env["TMPDIR"]).mkdir(exist_ok=True)
    original = None
    if rel:
        path = tree / rel
        original = path.read_text(encoding="utf-8")
        if original.count(old) != 1:
            return False, "\n".join(out + [f"SETUP-ERROR anchor occurs {original.count(old)} times"])
        path.write_text(original.replace(old, new), encoding="utf-8")
    rcs = []
    try:
        for gname, argv in gates:
            r = sh(argv, tree, env)
            lines = [ln for ln in (r.stdout + r.stderr).splitlines() if ln.strip()]
            hit = [ln for ln in lines if "AssertionError" in ln or "Error" in ln or "REFUSED" in ln
                   or "FAIL" in ln]
            last = (hit or lines or [""])[-1][:500]
            out.append(f"   {gname} rc={r.returncode}: {last}")
            (WORK / f"{name}-{gname.replace(' ', '_')}.log").write_text(r.stdout + r.stderr)
            rcs.append(r.returncode)
    finally:
        if rel:
            (tree / rel).write_text(original, encoding="utf-8")
    clean = sh(["git", "status", "--porcelain", "--untracked-files=no"], tree).stdout == ""
    red = any(rcs)
    ok = (red if expect == "red" else not red) and clean
    out.append(f"   {'RED' if red else 'GREEN'}; expectation {'met' if ok else 'NOT met'}; "
               f"restored clean: {clean}")
    return ok, "\n".join(out)


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(JOBS) as pool:
        results = list(pool.map(one, CASES))
    for _, text in results:
        print(text)
    bad = [c[0] for c, (ok, _) in zip(CASES, results) if not ok]
    print(f"{len(CASES) - len(bad)}/{len(CASES)} expectations met; not met: {bad or 'none'}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
