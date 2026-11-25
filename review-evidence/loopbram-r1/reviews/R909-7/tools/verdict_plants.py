#!/usr/bin/env python3
"""Plant one fault at a time in the leaf harness's #948 verdict wiring; the unchanged scoreboard must fail.

usage: verdict_plants.py TREE WORK
"""
import concurrent.futures as cf, os, shutil, subprocess, sys
from pathlib import Path
tree, work = Path(sys.argv[1]), Path(sys.argv[2])
OLD = ".pdu_enq_p_i(|accept_w), .pdu_done_p_i(|accept_w), .pdu_done_mask_i(accept_w),"
PL = {
 "control": OLD,
 "no_enqueue": ".pdu_enq_p_i(1'b0), .pdu_done_p_i(|accept_w), .pdu_done_mask_i(accept_w),",
 "no_done": ".pdu_enq_p_i(|accept_w), .pdu_done_p_i(1'b0), .pdu_done_mask_i(accept_w),",
 "mask_zero": ".pdu_enq_p_i(|accept_w), .pdu_done_p_i(|accept_w), .pdu_done_mask_i('0),",
 "mask_stream0_only": ".pdu_enq_p_i(|accept_w), .pdu_done_p_i(|accept_w), .pdu_done_mask_i(N_STREAMS_P'(1)),",
 "mask_all": ".pdu_enq_p_i(|accept_w), .pdu_done_p_i(|accept_w), .pdu_done_mask_i('1),",
 "mask_drops_top": ".pdu_enq_p_i(|accept_w), .pdu_done_p_i(|accept_w), .pdu_done_mask_i({1'b0, accept_w[N_STREAMS_P-2:0]}),",
 "mask_reversed": ".pdu_enq_p_i(|accept_w), .pdu_done_p_i(|accept_w), .pdu_done_mask_i({<<{accept_w}}),",
}
def one(name):
    d = work / name
    shutil.rmtree(d, ignore_errors=True)
    suite = d / "tb/verilator/input_loopback"; suite.mkdir(parents=True)
    src = tree / "tb/verilator/input_loopback"
    for f in src.iterdir():
        if f.is_file(): shutil.copy2(f, suite / f.name)
    w = suite / "loopback_wrap.sv"; t = w.read_text(); assert t.count(OLD) == 1
    w.write_text(t.replace(OLD, PL[name]))
    (d / "hdl").symlink_to(tree / "hdl"); (d / "third_party").symlink_to(tree / "third_party")
    (d / "tb/common").symlink_to(tree / "tb/common") if (tree / "tb/common").exists() else None
    for x in (tree / "tb/verilator").iterdir():
        if x.name != "input_loopback" and not (d / "tb/verilator" / x.name).exists():
            (d / "tb/verilator" / x.name).symlink_to(x)
    r = subprocess.run(["make", "-s", "-C", str(suite), "run", "VERILATOR_JOBS=2", "MDIR=obj",
                        "VERILATOR=" + os.environ["VERILATOR"]], capture_output=True, text=True, errors="replace")
    o = r.stdout + r.stderr
    tail = [l for l in o.splitlines() if l.startswith(("FAIL", "PASS", "%Error"))]
    return name, r.returncode, (tail[0][:110] if tail else "-"), (tail[-1][:110] if tail else "-")
with cf.ThreadPoolExecutor(4) as e:
    bad = 0
    for n, rc, a, b in e.map(one, PL):
        ok = (rc == 0 and "PASS input-loopback" in b) if n == "control" else rc != 0 and "FAIL" in a + b
        bad += not ok
        print(f"{'ok ' if ok else 'ESCAPED'} {n} rc={rc} first={a!r} last={b!r}", flush=True)
sys.exit(bool(bad))
