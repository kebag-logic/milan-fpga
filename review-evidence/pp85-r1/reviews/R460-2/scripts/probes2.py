#!/usr/bin/env python3
"""Round-2 reviewer probes for tb/adp_engine (disposable), aimed at the follow-up
step the second round adds to the two index > last cells of TK_DISCOVERED.

Same mechanics as probes.py (round 1, rerun unchanged): each probe copies hdl/
and tb/{common,adp_engine} of --root into its own scratch directory, applies
exact string replacements (each must match exactly once), runs
`make -C tb/adp_engine run`, and records rc, the tally and every FAIL line.
Nothing is written to the checkout.

usage: probes2.py --root CHECKOUT --scratch DIR --out RECEIPT_DIR [--jobs N]
       (VERILATOR in the environment names the simulator)
"""
import argparse
import concurrent.futures
import pathlib
import shutil
import subprocess

SV = "hdl/adp/KL_adp_engine.sv"
TB = "tb/adp_engine/sim_main.cpp"

STORE = "            rec_wr_en_w = 1'b1;               // fresh cycle: store + re-arm\n"
NO_STORE = "            // fresh cycle: re-arm only (probe: the index is not noted)\n"
GATED_STORE = "            rec_wr_en_w = gm_dom_ok_w;        // probe: store only on a GM match\n"
FOLLOW = "  if (!notes_fresh_index(row, col)) return;\n"
NOTES = "  return col == D_DISC && (row == V_FRESH || row == V_GMF);\n"

# name: (edits [(file, old, new)], what it breaks, expected outcome)
PROBES = {
    "control": ([], "nothing", "rc 0, 1334 of 1334"),
    "y1-fresh-store-gm-gated": (
        [(SV, STORE, GATED_STORE)],
        "the fresh arc notes the index only when the grandmaster matches "
        "(F04.8's fresh-arc guard reads no grandmaster)",
        "the GM mismatch, index > last x DISCOVERED follow-up only; arc 4 (match cell) stays green"),
    "y2-followup-disabled-vs-r6": (
        [(TB, FOLLOW, "  return;  // probe: no follow-up step\n"), (SV, STORE, NO_STORE)],
        "round 1's r6 fault with the round-2 follow-up step disabled",
        "rc 0: the follow-up step alone catches r6 (round 1's finding)"),
    "y3-followup-fresh-only-vs-y1": (
        [(TB, NOTES, "  return col == D_DISC && row == V_FRESH;  // probe\n"),
         (SV, STORE, GATED_STORE)],
        "y1's fault with the follow-up step on the match cell only",
        "rc 0: the GM mismatch cell's follow-up is what catches y1"),
    "y4-followup-check-inverted": (
        [(TB, "  CHECK(n_rep == 2 && evts[e1].departed", "  CHECK(n_rep != 2 && evts[e1].departed")],
        "the follow-up's own grading line is inverted (head RTL)",
        "both follow-up lines red, arc 4 and the arc count red: the step feeds cell_ok"),
    "y5-noted-literal-drifts": (
        [(TB, "  const uint32_t noted = 700 + 1;", "  const uint32_t noted = 700;  // probe")],
        "the follow-up's literal no longer equals apply_disc's last + 1 (head RTL)",
        "rc 0: a repeat below the noted index is still the restart pair"),
    "y6-noted-literal-drifts-vs-r6": (
        [(TB, "  const uint32_t noted = 700 + 1;", "  const uint32_t noted = 700;  // probe"),
         (SV, STORE, NO_STORE)],
        "y5's drift under round 1's r6 fault",
        "rc 0 would show the follow-up loses its teeth when the literal drifts"),
}


def run_probe(name, spec, root, scratch, out):
    tree = scratch / name
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(root / "hdl", tree / "hdl")
    for sub in ("common", "adp_engine"):
        shutil.copytree(root / "tb" / sub, tree / "tb" / sub,
                        ignore=shutil.ignore_patterns("obj_*", "__pycache__"))
    for rel, old, new in spec[0]:
        path = tree / rel
        text = path.read_text()
        assert text.count(old) == 1, f"{name}: anchor matches {text.count(old)} times"
        path.write_text(text.replace(old, new))
    log = out / f"probe-{name}.log"
    with log.open("w") as stream:
        rc = subprocess.run(["make", "-C", str(tree / "tb" / "adp_engine"), "run"],
                            stdout=stream, stderr=subprocess.STDOUT, check=False).returncode
    text = log.read_text()
    tally = [l for l in text.splitlines() if "checks:" in l and l.endswith(" FAIL")]
    fails = [l for l in text.splitlines() if l.startswith("FAIL:")]
    return name, rc, (tally[-1] if tally else "NO TALLY"), fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=pathlib.Path, required=True)
    ap.add_argument("--scratch", type=pathlib.Path, required=True)
    ap.add_argument("--out", type=pathlib.Path, required=True)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    a.scratch.mkdir(parents=True, exist_ok=True)
    a.out.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as pool:
        futs = [pool.submit(run_probe, n, s, a.root, a.scratch, a.out) for n, s in PROBES.items()]
        results = [f.result() for f in futs]
    with (a.out / "probes-summary.txt").open("w") as summary:
        for name, rc, tally, fails in results:
            _, what, expected = PROBES[name]
            print(f"{name}: rc={rc} {tally} failures={len(fails)}\n  breaks: {what}\n"
                  f"  expected: {expected}", file=summary)
            for line in fails:
                print(f"    {line}", file=summary)
    print((a.out / "probes-summary.txt").read_text())


if __name__ == "__main__":
    main()
