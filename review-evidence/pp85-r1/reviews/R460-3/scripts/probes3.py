#!/usr/bin/env python3
"""Reviewer fault probes for tb/adp_engine, round 3 (disposable, scratch only).

Each probe copies hdl/ and tb/{common,adp_engine} of the tree given by --root
into a scratch directory of its own, applies one or more exact string
replacements (each must match exactly once), runs `make -C tb/adp_engine run`
and records rc, the tally and every FAIL line. A control with no edit runs
first. Nothing is written to --root.

usage: probes3.py --root TREE --scratch DIR --out RECEIPT_DIR [--jobs N]
       (VERILATOR in the environment names the simulator)
"""
import argparse
import concurrent.futures
import pathlib
import shutil
import subprocess

SV = "hdl/adp/KL_adp_engine.sv"
TB = "tb/adp_engine/sim_main.cpp"

FRESH = "            rec_wr_en_w = 1'b1;               // fresh cycle: store + re-arm\n"
RESTART = ("            ev_disc_w   = 1'b1;\n"
           "            rec_wr_en_w = 1'b1;\n"
           "            iter_arm_w  = 1'b1;\n"
           "          end else begin\n")


def fresh_store(expr):
    return (FRESH, "            rec_wr_en_w = 1'b1;\n"
                   f"            rec_wr_data_w = {{rx_ifx_r, {expr}}};\n")


def restart_store(expr):
    return (RESTART, "            ev_disc_w   = 1'b1;\n"
                     "            rec_wr_en_w = 1'b1;\n"
                     f"            rec_wr_data_w = {{rx_ifx_r, {expr}}};\n"
                     "            iter_arm_w  = 1'b1;\n"
                     "          end else begin\n")


ARC4 = "P13 F04.3 arc DISCOVERED -> DISCOVERED (index > last)"
ARC5 = "P13 F04.3 arc DISCOVERED -> DISCOVERED (index <= last, GM matches: restart pair)"
GMF = "P13 F04.3 AVAILABLE(GM mismatch, index > last) x TK_DISCOVERED"

UPPER_CHECK = "  CHECK(n_up == 0,\n"
LOWER_CHECK = "  CHECK(n_rep == 2 && evts[e1].departed && evts[e1].sink == s\n"

# name: ([(file, old, new), ...], what it breaks, the check that must (or must not) go red)
PROBES = {
    "control": None,
    # ---- RTL: the restart arc's noted index (assignment item 2)
    "s1-restart-no-store": (
        [(SV, RESTART, "            ev_disc_w   = 1'b1;\n"
                       "            iter_arm_w  = 1'b1;\n"
                       "          end else begin\n")],
        "the restart pair notes nothing (the r7 / q4 edit)", "red: " + ARC5),
    "s2-restart-store-plus-one": (
        [(SV,) + restart_store("rx_aidx_r + 32'd1")],
        "the restart pair notes the received index + 1", "red: " + ARC5),
    "s3-restart-store-minus-one": (
        [(SV,) + restart_store("rx_aidx_r - 32'd1")],
        "the restart pair notes the received index - 1", "red: " + ARC5),
    "s4-restart-store-max": (
        [(SV,) + restart_store("32'hFFFF_FFFF")],
        "the restart pair notes the maximum index", "red: " + ARC5),
    # ---- RTL: the fresh arc's noted index, other exact-value faults
    "s5-fresh-store-minus-one": (
        [(SV,) + fresh_store("rx_aidx_r - 32'd1")],
        "the fresh arc notes the received index - 1", "red: " + ARC4),
    "s6-fresh-store-low-byte": (
        [(SV,) + fresh_store("{24'd0, rx_aidx_r[7:0]}")],
        "the fresh arc notes only the low byte of the index", "red: " + ARC4),
    "s7-fresh-store-gm-only": (
        [(SV, FRESH, "            rec_wr_en_w = gm_dom_ok_w;\n")],
        "the fresh arc notes only on a grandmaster and domain match", "red: " + GMF),
    # ---- testbench: each side of the two-sided follow-up is load-bearing
    "t1-no-upper-vs-plus-one": (
        [(TB, UPPER_CHECK, "  CHECK(true || n_up == 0,\n"),
         (SV,) + fresh_store("rx_aidx_r + 32'd1")],
        "upper side neutralised, fresh arc notes + 1", "survives: " + ARC4),
    "t2-no-lower-vs-no-store": (
        [(TB, LOWER_CHECK, "  CHECK(true || n_rep == 2 && evts[e1].departed && evts[e1].sink == s\n"),
         (SV, FRESH, "            // probe: the fresh index is not noted\n")],
        "lower side neutralised, fresh arc notes nothing", "survives: " + ARC4),
    "t3-no-upper-vs-restart-no-store": (
        [(TB, UPPER_CHECK, "  CHECK(true || n_up == 0,\n"),
         (SV, RESTART, "            ev_disc_w   = 1'b1;\n"
                       "            iter_arm_w  = 1'b1;\n"
                       "          end else begin\n")],
        "upper side neutralised, restart notes nothing", "survives: " + ARC5),
    # ---- testbench: the named constant drives all three sites (item 3)
    "t4-disc-last-moved": (
        [(TB, "constexpr uint32_t DISC_LAST = 700;\n", "constexpr uint32_t DISC_LAST = 9000;\n")],
        "the discovered column's last index moved to 9000 at its one definition",
        "nothing: every site follows, the walk passes"),
    "t5-disc-last-moved-vs-plus-one": (
        [(TB, "constexpr uint32_t DISC_LAST = 700;\n", "constexpr uint32_t DISC_LAST = 9000;\n"),
         (SV,) + fresh_store("rx_aidx_r + 32'd1")],
        "DISC_LAST 9000 and the fresh arc notes + 1", "red: " + ARC4),
}


def run_probe(name, spec, root, scratch, out):
    tree = scratch / name
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(root / "hdl", tree / "hdl")
    for sub in ("common", "adp_engine"):
        shutil.copytree(root / "tb" / sub, tree / "tb" / sub,
                        ignore=shutil.ignore_patterns("obj_*", "__pycache__"))
    for rel, old, new in (spec[0] if spec else []):
        path = tree / rel
        text = path.read_text()
        assert text.count(old) == 1, f"{name}: anchor matches {text.count(old)} times"
        path.write_text(text.replace(old, new))
    log = out / f"probe-{name}.log"
    with log.open("w") as stream:
        rc = subprocess.run(["make", "-C", str(tree / "tb" / "adp_engine"), "run"],
                            stdout=stream, stderr=subprocess.STDOUT, check=False).returncode
    text = log.read_text()
    tally = [l for l in text.splitlines() if l.endswith(" FAIL") and "checks:" in l]
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
    with (a.out / "probes3-summary.txt").open("w") as summary:
        for name, rc, tally, fails in results:
            spec = PROBES[name]
            arc4 = sum(f[len("FAIL: "):].startswith(ARC4) for f in fails)
            arc5 = sum(f[len("FAIL: "):].startswith(ARC5) for f in fails)
            head = f"{name}: rc={rc} {tally} failures={len(fails)} arc4={arc4} arc5={arc5}"
            if spec:
                head += f"\n  breaks: {spec[1]}\n  expected: {spec[2]}"
            print(head, file=summary)
            for line in fails:
                print(f"    {line}", file=summary)
    print((a.out / "probes3-summary.txt").read_text())


if __name__ == "__main__":
    main()
