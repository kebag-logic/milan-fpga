#!/usr/bin/env python3
"""Reviewer driver: run a chosen subset of the engine mutation arm, plus
reviewer-planted probes, in parallel workers, using the arm's own code
(mutants.stage / build / generate_image / run_harness / named_verdict).

usage: arm_subset.py <engine dir of a probe copy> <out dir>
                     [--jobs N] [--p100 | --rest | --all] [--names "a|b"]
                     [--probes]

Every job writes <out>/<NNN>.log (all it printed) and <out>/<NNN>.json.
The unmutated control is job 000. Nothing is written to the probe copy.
"""
import argparse
import concurrent.futures as cf
import contextlib
import importlib.util
import io
import json
import sys
import time
from pathlib import Path

ENGINE = "top/KL_gptp_engine.sv"
GENERATOR = "ucode/gen_gptp_ucode.py"

#: reviewer probes: (name, file, pattern, replacement, breaks). "breaks"
#: is informational; for probes the verdict is caught / survived only.
PROBES = [
    ("R1 floor becomes truncation toward zero", ENGINE,
     "      if (tlv_mul_r) tlv_freq_r <= 32'(tlv_prod_w >>> 16);\n",
     "      if (tlv_mul_r) tlv_freq_r <= 32'(tlv_prod_w / 64'sd65536);\n",
     "(probe) scaledLastGmFreqChange floor"),
    ("R2 the frequency multiply zero-extends the delta", ENGINE,
     "  wire signed [63:0] tlv_prod_w = 64'(tlv_dlt_r) *\n",
     "  wire signed [63:0] tlv_prod_w = $signed({39'd0, tlv_dlt_r}) *\n",
     "(probe) multiply sign"),
    ("R5 the watch is not due in its deadline's millisecond", ENGINE,
     "  wire        w2_due_w  = w2_armed_r && ($signed(ms_now_w - w2_dl_r) >= 0);\n",
     "  wire        w2_due_w  = w2_armed_r && ($signed(ms_now_w - w2_dl_r) > 0);\n",
     "(probe) expiry due at the instant"),
    ("R7 the interval is taken from any frame's word 0", ENGINE,
     "      if (bank_we_w && (bank_addr_w == 5'd0) && ann_frame_capture_r)\n",
     "      if (bank_we_w && (bank_addr_w == 5'd0))\n",
     "(probe) interval capture guard"),
    ("R9 any PHC write counts as a mastership", ENGINE,
     "                              (st_addr_w[19:16] == 4'd4) &&\n"
     "                              (st_addr_w[1:0] == 2'd3);\n",
     "                              (st_addr_w[19:16] == 4'd4);\n",
     "(probe) mastership mark"),
]


def load(engine: Path):
    sys.path.insert(0, str(engine))
    spec = importlib.util.spec_from_file_location("mutants",
                                                  engine / "mutants.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def job(engine: str, work: str, kind: str, index: int, entry) -> dict:
    m = load(Path(engine))
    w = Path(work) / f"j{index:03d}"
    w.mkdir(parents=True, exist_ok=True)
    clean = Path(work) / "clean" / "obj_clean" / "Vengine_clean"
    t0 = time.time()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        if kind == "control":
            src = m.stage(w, "clean")
            run = w / "run_clean"
            exe = m.build(src, w, "clean")
            ok = exe is not None and m.generate_image(src, run)
            ans = m.verdict(*m.run_harness(exe, run)) if ok else "no build"
            print(f"control verdict: {ans}")
            out = ans == "pass"
        else:
            out = m.run_mutant(w, clean, tuple(entry))
    return {"index": index, "kind": kind, "name": entry[0] if entry else
            "control", "ok": out, "seconds": round(time.time() - t0, 1),
            "log": buf.getvalue()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("engine")
    ap.add_argument("out")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--p100", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--rest", action="store_true",
                    help="every arm mutant that is not a #100 control")
    ap.add_argument("--probes", action="store_true")
    ap.add_argument("--names", default="")
    a = ap.parse_args()
    engine = Path(a.engine).resolve()
    out = Path(a.out).resolve()
    work = out / "work"
    work.mkdir(parents=True, exist_ok=True)
    m = load(engine)
    from_p100 = {e[0] for e in m.P100_MUTATIONS}
    want = set(filter(None, a.names.split("|")))
    sel = [e for e in m.MUTATIONS
           if a.all or (a.p100 and e[0] in from_p100) or e[0] in want
           or (a.rest and e[0] not in from_p100)]
    jobs = [("control", 0, None)]
    jobs += [("arm", i + 1, e) for i, e in enumerate(sel)]
    if a.probes:
        jobs += [("probe", 900 + i, e) for i, e in enumerate(PROBES)]
    # the clean exe every generator mutant reuses, built first
    m.build(m.stage(work / "clean", "clean"), work / "clean", "clean")
    res = []
    with cf.ProcessPoolExecutor(max_workers=a.jobs) as ex:
        futs = [ex.submit(job, str(engine), str(work), k, i, e)
                for k, i, e in jobs]
        for f in cf.as_completed(futs):
            r = f.result()
            res.append(r)
            (out / f"{r['index']:03d}.log").write_text(r["log"])
            (out / f"{r['index']:03d}.json").write_text(
                json.dumps({k: v for k, v in r.items() if k != "log"}))
            print(f"{r['index']:03d} {r['kind']} "
                  f"{'ok' if r['ok'] else 'NOT-OK'} {r['seconds']}s "
                  f"{r['name']}", flush=True)
    res.sort(key=lambda r: r["index"])
    arm = [r for r in res if r["kind"] != "probe"]
    good = sum(r["ok"] for r in arm)
    with open(out / "SUMMARY.md", "w") as f:
        f.write(f"arm jobs: {len(arm)}, ok {good}, not ok {len(arm)-good}\n")
        for r in res:
            f.write(f"- {r['index']:03d} {r['kind']} "
                    f"{'ok' if r['ok'] else 'NOT-OK'} {r['seconds']}s "
                    f"{r['name']}\n")
    print(f"arm jobs: {len(arm)}, ok {good}")
    return 0 if good == len(arm) else 1


if __name__ == "__main__":
    sys.exit(main())
