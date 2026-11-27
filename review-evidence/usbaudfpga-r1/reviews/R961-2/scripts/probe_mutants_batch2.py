#!/usr/bin/env python3
"""Reviewer falsification probes for the usbaudio epoch fence and the
playback frame-preservation boundary.  Each probe copies the audio RTL,
applies one exact textual edit (which must match exactly once), builds the
named unchanged testbench with the pinned simulator, runs it, and records
which named CHECK fired.  A probe whose build fails is BUILD_FAILED, never a
detection.  A clean control per testbench must pass first.

usage: probe_mutants.py TREE ENGINE OUT WORKERS"""
import concurrent.futures as cf, json, shutil, subprocess, sys, re
from pathlib import Path
TREE, ENGINE, OUT, WORKERS = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), int(sys.argv[4])
RTL = TREE / "hdl/milan/usbaudio"
TB = TREE / "tb/verilator/usbaudio"
FIFO = TREE / "third_party/verilog-axis/rtl/axis_async_fifo.v"
# name, testbench, rtl leaf, old, new
PROBES = [
    ("p2m_no_trailing_discard", "media", "media",
     "render_discard_r <= !render_tick_i && !render_last_i", "render_discard_r <= 1'b0 && !render_last_i"),
    ("p3m_capture_valid_ignores_change", "media", "media",
     "&& flags_r[2] && flags_r[1] && !capture_changed_w && !render_fenced_r;",
     "&& flags_r[2] && flags_r[1] && !render_fenced_r;"),
    ("p8e_playback_consumed_during_pending_change", "epochs", "media",
     "assign playback_ready_o = !playback_changed_w &&", "assign playback_ready_o = 1'b1 &&"),
    ("p9e_ack_before_boundary", "epochs", "media",
     "assign ack_valid_o = state_valid_i && state_boundary_w;", "assign ack_valid_o = state_valid_i;"),
]
def sources(test, rtl):
    if test == "media":
        return [rtl / "KL_usbaudio_media.sv"]
    files = [rtl / "KL_usbaudio_bridge.sv"] + sorted(p for p in rtl.glob("*.sv") if p.name != "KL_usbaudio_bridge.sv")
    return files + [FIFO]
def run(probe):
    name, test, leaf, old, new = probe
    case = OUT / name
    shutil.rmtree(case, ignore_errors=True)
    rtl = case / "rtl"
    shutil.copytree(RTL, rtl)
    if leaf:
        f = rtl / f"KL_usbaudio_{leaf}.sv"
        text = f.read_text()
        if text.count(old) != 1:
            return {"probe": name, "result": "EDIT_NOT_UNIQUE", "count": text.count(old)}
        f.write_text(text.replace(old, new))
    obj = case / "obj"
    cmd = [ENGINE, "--binary", "--timing", "--top-module", f"{test}_tb", "-Wall", "-Wno-fatal",
           "-Werror-USERERROR", "-Wno-TIMESCALEMOD", "--build-jobs", "2", "--Mdir", str(obj),
           *map(str, sources(test, rtl)), str(TB / f"{test}_tb.sv")]
    b = subprocess.run(cmd, capture_output=True, text=True)
    (case / "build.log").write_text(b.stdout + b.stderr)
    if b.returncode:
        return {"probe": name, "test": test, "result": "BUILD_FAILED"}
    try:
        r = subprocess.run([str(obj / f"V{test}_tb")], capture_output=True, text=True, timeout=1500, cwd=case)
        out, rc = r.stdout + r.stderr, r.returncode
    except subprocess.TimeoutExpired as e:
        out, rc = (e.stdout or b"").decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or ""), "TIMEOUT"
    (case / "run.log").write_text(out)
    checks = re.findall(r"CHECK (\w+)", out)
    shutil.rmtree(obj, ignore_errors=True)
    result = "PASS" if rc == 0 else ("TIMEOUT" if rc == "TIMEOUT" else "FAILED")
    return {"probe": name, "test": test, "rc": rc, "result": result, "checks": checks[:3]}
OUT.mkdir(parents=True, exist_ok=True)
with cf.ThreadPoolExecutor(WORKERS) as ex:
    results = list(ex.map(run, PROBES))
for r in results:
    print(json.dumps(r))
(OUT / "probe-results.json").write_text(json.dumps(results, indent=1) + "\n")
