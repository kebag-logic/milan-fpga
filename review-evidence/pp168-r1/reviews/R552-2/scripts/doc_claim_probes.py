#!/usr/bin/env python3
"""Disposable RTL probes for claims the round-3 documentation makes.

Each probe copies hdl/, tb/common/ and one suite from a clean tree into its own
scratch directory, applies exact edits (each old text must occur exactly once),
builds and runs that suite, and records rc, tally and FAIL lines. The source
tree is never written.

  E1 overlay_mask_removed   F07.6: the published record view masks the private
                            controller word to zero outside SNR/SOK.
                            Expect: the listener suite FAILS (claim enforced).
  E2 a12_clear_removed      05 legend: A12's other callers already have
                            acmpsta = 0. Removing A12's clear entirely should be
                            unobservable. Expect: PASS (equivalence evidence).
  E3 a5_clear_removed       05 §6.4: a new binding clears acmpsta at A5.
                            Expect: FAIL if a check reaches A5 from a nonzero
                            status through a new binding.
  E4 a10_erases_overlay     07: A10 need not erase the private word.
                            Expect: PASS (equivalence evidence).
  E5 disconnect_index_only  05 §6bis: DISCONNECT_TX validation includes the
                            source being enabled in the current configuration.
                            Expect: FAIL if a check grades a disabled source.

usage: doc_claim_probes.py --root TREE --scratch DIR --out DIR --verilator V
                           [--jobs N] [--only NAME ...]
"""
import argparse
import concurrent.futures
import json
import re
import shutil
import subprocess
from pathlib import Path

LST = "hdl/acmp/KL_pp_acmp_listener.sv"
TKR = "hdl/acmp/KL_acmp_talker.sv"

PROBES = {
    "E1_overlay_mask_removed": ("tb/acmp_listener", [(
        LST,
        "      published_rec_w.settled_stream_id = 64'd0;\n",
        "      published_rec_w.settled_stream_id = published_rec_w.settled_stream_id;\n")]),
    "E2_a12_clear_removed": ("tb/acmp_listener", [(
        LST,
        "                if (evt_r != LEV_TMR_RETRY) rec_r.acmpsta <= 5'd0;\n",
        "")]),
    "E3_a5_clear_removed": ("tb/acmp_listener", [(
        LST,
        "                if (evt_r != LEV_TMR_DELAY) rec_r.acmpsta <= 5'd0;\n",
        "")]),
    "E4_a10_erases_overlay": ("tb/acmp_listener", [(
        LST,
        "                rec_r.probe_seq     <= 16'd0;\n",
        "                rec_r.probe_seq     <= 16'd0;\n"
        "                rec_r.settled_stream_id <= 64'd0;\n")]),
    "E5_disconnect_index_only": ("tb/acmp_talker", [(
        TKR,
        "resp_status_o       = uid_valid_w ? ST_SUCCESS_C : ST_TALKER_UNKNOWN_C;",
        "resp_status_o       = (uid16_w < 16'(N_STREAM_OUT_P)) ? ST_SUCCESS_C"
        " : ST_TALKER_UNKNOWN_C;")]),
    "G_listener_golden": ("tb/acmp_listener", []),
    "G_talker_golden": ("tb/acmp_talker", []),
}
TALLY = re.compile(r"^.*\d+ checks.*$", re.M)


def probe(name, root, scratch, out, verilator):
    suite, edits = PROBES[name]
    tree = scratch / name
    if tree.exists():
        shutil.rmtree(tree)
    skip = shutil.ignore_patterns("obj*", "*.hex", "__pycache__")
    for d in ("hdl", "tb/common", suite):
        shutil.copytree(root / d, tree / d, ignore=skip)
    for path, old, new in edits:
        f = tree / path
        text = f.read_text()
        n = text.count(old)
        if n != 1:
            return {"probe": name, "verdict": "REFUSED", "occurrences": n}
        f.write_text(text.replace(old, new))
    log = out / f"{name}.log"
    with log.open("w") as s:
        rc = subprocess.run(["make", "run", "VERILATOR=" + verilator], cwd=tree / suite,
                            stdout=s, stderr=subprocess.STDOUT, check=False).returncode
    text = log.read_text(errors="replace")
    fails = [l[6:] for l in text.splitlines() if l.startswith("FAIL: ")]
    tally = TALLY.findall(text)
    shutil.rmtree(tree)
    return {"probe": name, "suite": suite, "rc": rc, "tally": tally[-1] if tally else None,
            "fail_count": len(fails), "first_fails": fails[:8],
            "verdict": "PASS" if rc == 0 and not fails else "FAIL"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--scratch", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    a.scratch.mkdir(parents=True, exist_ok=True)
    a.out.mkdir(parents=True, exist_ok=True)
    names = a.only or list(PROBES)
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as pool:
        res = list(pool.map(lambda n: probe(n, a.root.resolve(), a.scratch.resolve(),
                                            a.out.resolve(), a.verilator), names))
    (a.out / "doc_claim_probes.json").write_text(json.dumps(res, indent=1) + "\n")
    for r in res:
        print(json.dumps({k: r.get(k) for k in ("probe", "rc", "tally", "fail_count", "verdict")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
