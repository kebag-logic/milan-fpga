#!/usr/bin/env python3
"""R490-1 reviewer mutation probes for #658 / PR #670 (exact head fb4953bd).

Independent of the lane's dynmap_mutants.py: each probe plants ONE edit in a
copy of hdl/milan/milan_datapath.sv, rebuilds the [DYNMAP] leg through the
suite's own recipe (make dynmap-build, DP_SRC and DYNMAP_MDIR overridden) and
runs it. A probe is KILLED when the leg reports a [FAIL] line or a failing
tally, SURVIVED when the leg passes, and NOT-EVIDENCE otherwise (build error,
crash). Nothing in the checkout is modified; mutants and objdirs live under
--work.

Usage:
  python3 r490_mutants.py --repo <checkout at fb4953bd> --work <dir>
      --verilator <verilator> [--jobs N] [--vjobs M] [IDS...]
"""
import argparse
import concurrent.futures as cf
import json
import re
import subprocess
import sys
from pathlib import Path

CSR_GATE = "!amap_boot_busy_w && !aecp_locked"
PROBES = {
    "P1-no-csr-hold": ("CSR 0x900 writer not held while the boot writer is busy",
                       [(CSR_GATE, "!aecp_locked", 4)]),
    "P2-no-edit-wait": ("edit face never waits for the boot writer",
                        [("assign pp_amap_edit_wait_w = amap_boot_busy_w;",
                          "assign pp_amap_edit_wait_w = 1'b0;", 1)]),
    "P3-no-final-sweep": ("no sweep after the restore terminal",
                          [("        amap_boot_last_r <= 1'b1;\n",
                            "        amap_boot_last_r <= 1'b0;\n", 1)]),
    "P4-clip-off-by-one": ("input clip keeps stream channel == channel count",
                           [("&& (32'(AMAP_IN_IMAGE_C[k*8 +: 3]) < 32'(amap_in_ch_w[s])))",
                             "&& (32'(AMAP_IN_IMAGE_C[k*8 +: 3]) <= 32'(amap_in_ch_w[s])))", 1)]),
    "P5-no-closed-terminal": ("boot window ignores the CLOSED terminal",
                              [("if (amap_boot_r && (pp_restore_done_w || pp_restore_closed_w)) begin",
                                "if (amap_boot_r && pp_restore_done_w) begin", 1)]),
    "P6-window-ends-at-busy": ("boot window ends when the restore starts, before formats apply",
                               [("if (amap_boot_r && (pp_restore_done_w || pp_restore_closed_w)) begin",
                                 "if (amap_boot_r && (pp_restore_busy_w || pp_restore_done_w || pp_restore_closed_w)) begin", 1)]),
    "P7-writer-writes-image": ("render RAM written from the unclipped image, not the store",
                               [("        amap_boot_iword_w = amap_in_store_r[k*8 +: 8];",
                                 "        amap_boot_iword_w = AMAP_IN_IMAGE_C[k*8 +: 8];", 1)]),
    "P8-out-cluster-zero": ("output cluster registers reset to 0 instead of k%8",
                            [("      r[k*16 +: 16] = v_i[k] ? 16'(k % 8) : 16'd0;",
                              "      r[k*16 +: 16] = 16'd0;", 1)]),
    "P9-no-drain": ("busy drops the cycle the last boot write is still in flight",
                    [("      amap_boot_drain_r <= amap_boot_last_r && amap_boot_wrap_w;",
                      "      amap_boot_drain_r <= 1'b0;", 1)]),
    "P10-writer-final-sweep-only": ("crossbar RAMs written only in the final sweep, not in the window",
                                    [("  wire amap_boot_wr_w   = amap_boot_r || amap_boot_last_r;",
                                      "  wire amap_boot_wr_w   = amap_boot_last_r;", 1)]),
    "P11-in-image-ignores-format": ("input image not bounded by the declared default format",
                                    [("            && (c < 32'(amap_decl_ch(1'b0, p)))\n", "", 1)]),
    "P12-clip-forever": ("store clip keeps running after the terminal (run-time re-add)",
                         [("      if (amap_boot_r) begin\n        amap_in_store_r <= amap_in_boot_w;",
                           "      if (1'b1) begin\n        amap_in_store_r <= amap_in_boot_w;", 1)]),
}


def plant(src: str, edits, out: Path) -> str | None:
    text = src
    for pat, rep, n in edits:
        c = text.count(pat)
        if c != n:
            return f"pattern count {c} != {n}: {pat[:60]!r}"
        text = text.replace(pat, rep)
    out.write_text(text)
    return None


def run_probe(pid, repo: Path, work: Path, verilator: str, vjobs: int):
    desc, edits = PROBES[pid]
    pdir = work / pid
    pdir.mkdir(parents=True, exist_ok=True)
    src = (repo / "hdl/milan/milan_datapath.sv").read_text()
    dp = pdir / "milan_datapath.sv"
    err = plant(src, edits, dp)
    rec = {"id": pid, "desc": desc}
    if err:
        rec.update(verdict="NOT-EVIDENCE", why=err)
        return rec
    suite = repo / "tb/verilator/milan_dp"
    mdir = pdir / "obj"
    b = subprocess.run(["make", "-s", "-C", str(suite), "-o", "ltn_rom.hex", "-o", "ucode.hex",
                        "dynmap-build", f"DP_SRC={dp}", f"DYNMAP_MDIR={mdir}",
                        f"VERILATOR={verilator}", f"VERILATOR_JOBS={vjobs}"],
                       capture_output=True, text=True)
    (pdir / "build.log").write_text(b.stdout + b.stderr)
    exe = mdir / "Vmilan_dp_dynmap"
    if b.returncode != 0 or not exe.is_file():
        rec.update(verdict="NOT-EVIDENCE", why=f"build rc {b.returncode}")
        return rec
    r = subprocess.run([str(exe)], cwd=str(suite), capture_output=True, text=True)
    out = r.stdout + r.stderr
    (pdir / "run.log").write_text(out)
    fails = [l.strip() for l in out.splitlines() if l.strip().startswith("[FAIL]")]
    m = re.search(r"checks:\s*(\d+)\s+failures:\s*(\d+)", out)
    tally = (int(m.group(1)), int(m.group(2))) if m else None
    rec.update(rc=r.returncode, tally=tally, first_fails=fails[:6], n_fail_lines=len(fails))
    if fails or (tally and tally[1] > 0):
        rec["verdict"] = "KILLED"
    elif r.returncode == 0 and tally and tally[1] == 0:
        rec["verdict"] = "SURVIVED"
    else:
        rec["verdict"] = f"NOT-EVIDENCE (rc {r.returncode}, no verdict)"
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, type=Path)
    ap.add_argument("--work", required=True, type=Path)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--vjobs", type=int, default=4)
    ap.add_argument("ids", nargs="*")
    a = ap.parse_args()
    ids = a.ids or list(PROBES)
    a.work.mkdir(parents=True, exist_ok=True)
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        res = list(ex.map(lambda i: run_probe(i, a.repo.resolve(), a.work.resolve(),
                                              a.verilator, a.vjobs), ids))
    for r in res:
        print(f"{r['id']}: {r['verdict']}  tally={r.get('tally')}  {r['desc']}")
        for f in r.get("first_fails", []):
            print(f"    {f}")
    print(json.dumps(res, indent=1), file=open(a.work / "results.json", "w"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
