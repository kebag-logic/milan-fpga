#!/usr/bin/env python3
"""Reviewer driver for the #602 gmstep/option-off mutation probes.

Reuses the lane's own gmstep_mutants.py plant/build/verdict functions so a
result means the same thing it means in the suite, but runs controls in
parallel and keeps one log per control. Portable: every path is an argument.

usage: run_mutants.py TREE WORK RECEIPTS --set {author,reviewer} [--only i,j] [--jobs N]
       run_mutants.py TREE WORK RECEIPTS --clean
TREE      checkout whose tb/verilator/milan_dp is used (must be a probe copy)
WORK      disposable directory for planted sources and build dirs
RECEIPTS  directory for per-control logs and results.tsv
"""
import argparse
import concurrent.futures as cf
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tree")
    ap.add_argument("work")
    ap.add_argument("receipts")
    ap.add_argument("--set", choices=["author", "reviewer"])
    ap.add_argument("--only", default="")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--clean", action="store_true")
    a = ap.parse_args()
    here = Path(a.tree).resolve() / "tb/verilator/milan_dp"
    sys.path.insert(0, str(here))
    import gmstep_mutants as gm  # noqa: E402

    work = Path(a.work).resolve()
    rec = Path(a.receipts).resolve()
    work.mkdir(parents=True, exist_ok=True)
    rec.mkdir(parents=True, exist_ok=True)
    trig = gm.RESTART_TRIGGER
    C = gm.Control
    reviewer = [
        C("RV1 restored term gated by CRF selection", "datapath", trig,
          trig[:-1] + " | (crf_clk_selected_r & media_rebase_p_w);",
          "restart: a PHC-only step leaves outgoing mr unchanged", False),
        C("RV2 plane/adjtime strobe alone restored on the gmstep leg", "datapath", trig,
          trig[:-1] + " | eff_ptp_adjust_w;",
          "restart: a PHC-only step leaves outgoing mr unchanged", False),
        C("RV3 GM identity change requests a restart", "datapath", trig,
          trig[:-1] + " | gm_recentre_p_r;",
          "restart: a PHC-only step leaves outgoing mr unchanged", False),
        C("RV4 tu level requests a restart", "datapath", trig,
          trig[:-1] + " | clkv_tu_w;",
          "restart: a PHC-only step leaves outgoing mr unchanged", False),
        C("RV5 a coincident PHC re-base suppresses genuine CRF restarts (gap probe)",
          "datapath", trig,
          "                          & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w)"
          " & ~media_rebase_p_w;",
          "restart:", False),
        C("RV6 full re-base term restored, graded on the option-off leg", "datapath", trig,
          trig[:-1] + " | media_rebase_p_w;",
          "CLKV:", False, "option-off"),
        C("RV7 CRF propagation fires regardless of clock-source selection", "datapath",
          "  wire mcr_restart_p_w = crf_clk_selected_r\n" + trig,
          "  wire mcr_restart_p_w = 1'b1\n" + trig,
          "", False),
    ]
    if a.clean:
        out = []
        for key, leg in gm.LEGS.items():
            exe = gm.build(leg, {}, work / f"obj_clean_{key}")
            rc, log = gm.run_leg(leg, exe) if exe else (-999, "did not compile")
            v = gm.verdict(rc, log, None)
            (rec / f"clean_{key}.log").write_text(log)
            out.append(f"clean\t{key}\t{v}")
        (rec / "results.tsv").open("a").write("\n".join(out) + "\n")
        print("\n".join(out))
        return 0 if all(o.endswith("pass") for o in out) else 1

    pool = gm.CONTROLS if a.set == "author" else reviewer
    idx = [int(i) for i in a.only.split(",")] if a.only else list(range(len(pool)))

    def one(i: int) -> str:
        c = pool[i]
        base = gm.SOURCES[c.source].resolve()
        text = base.read_text()
        n = text.count(c.anchor)
        tag = f"{a.set}{i}"
        if n != 1:
            return f"{tag}\t{c.name}\t{c.leg}\tANCHOR x{n}\t"
        planted = work / f"{tag}_{base.name}"
        planted.write_text(text.replace(c.anchor, c.replacement))
        srcs = {k: p.resolve() for k, p in gm.SOURCES.items()}
        srcs[c.source] = planted
        leg = gm.LEGS[c.leg]
        exe = gm.build(leg, srcs, work / f"obj_{tag}")
        if exe is None:
            return f"{tag}\t{c.name}\t{c.leg}\tDID NOT COMPILE\t"
        rc, log = gm.run_leg(leg, exe)
        (rec / f"{tag}.log").write_text(log)
        v = gm.verdict(rc, log, c.breaks or None)
        broke = "; ".join(gm.failed_checks(log))
        return f"{tag}\t{c.name}\t{c.leg}\t{v}\t{broke}"

    with cf.ThreadPoolExecutor(a.jobs) as ex:
        res = list(ex.map(one, idx))
    with (rec / "results.tsv").open("a") as f:
        f.write("\n".join(res) + "\n")
    print("\n".join(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
