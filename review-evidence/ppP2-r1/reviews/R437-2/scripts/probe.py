#!/usr/bin/env python3
"""R437-2 reviewer probe driver for tb/nvm_port (portable).

Each job = (probe, model, tmo). A job exports the exact head's tracked bytes
(git archive) of hdl/packet_engine, tb/nvm_port and tb/common into its own
scratch directory, applies the probe's text edits and the model's edits (each
anchor must occur exactly once), builds the suite with the same Verilator flags
as tb/nvm_port/Makefile's `suite` recipe at -GMEM_TIMEOUT_CYC_P=<tmo> and
-DNVM_PORT_TMO=<tmo> (only the Verilator build parallelism is lowered to -j 2),
runs it, and records the tally and the names of the failing checks.

The model edits are imported from the head's own measure_figures.py, remapped
onto the job's copy, so the models are byte-for-byte the figures gate's.

usage: probe.py --repo R --scratch S --out O --jobs N --verilator V SPEC.py
SPEC.py defines PROBES = {name: [(file_tag, old, new), ...]} with file_tag
'RTL' or 'SIM', and RUNS = [(probe, model, tmo), ...].
"""
import argparse
import concurrent.futures as cf
import importlib.util
import io
import json
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

HEAD = "c0715410418b47ffaccf5feed55b71617fcfaf82"
TALLY = re.compile(r"(\d+) checks: (\d+) PASS, (\d+) FAIL")


def load_models(repo: Path):
    sys.path.insert(0, str(repo / "tb" / "nvm_port"))
    spec = importlib.util.spec_from_file_location("mf", repo / "tb/nvm_port/measure_figures.py")
    mf = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mf)
    models = {}
    for name, _claims, edits in mf.MODELS:
        flat = []
        for e in edits:
            # MODELS entries are lists of edits, except _HALFPAGE (a bare tuple)
            if isinstance(e, tuple) and len(e) == 3 and isinstance(e[1], str):
                flat.append(e)
            else:
                flat.extend(e)
        models[name] = [("RTL" if p.name.endswith(".sv") else "SIM", o, n) for p, o, n in flat]
    return models


def export(repo: Path, dst: Path):
    tar = subprocess.run(["git", "-C", str(repo), "archive", HEAD, "hdl/packet_engine",
                          "tb/nvm_port", "tb/common"], check=True, capture_output=True).stdout
    with tarfile.open(fileobj=io.BytesIO(tar)) as t:
        t.extractall(dst)


def run_job(args, models, probes, probe, model, tmo):
    tag = f"{probe}__{model.replace(' ', '_').replace('+', 'p')}__{tmo}"
    jd = Path(args.scratch) / "jobs" / tag
    if jd.exists():
        shutil.rmtree(jd)
    jd.mkdir(parents=True)
    export(Path(args.repo), jd)
    files = {"RTL": jd / "hdl/packet_engine/KL_pp_nvm_port.sv", "SIM": jd / "tb/nvm_port/sim_main.cpp"}
    for ftag, old, new in probes[probe] + models[model]:
        txt = files[ftag].read_text()
        n = txt.count(old)
        if n != 1:
            return {"job": tag, "error": f"anchor occurs {n} times: {old[:80]!r}"}
        files[ftag].write_text(txt.replace(old, new, 1))
    tb = jd / "tb/nvm_port"
    (tb / "obj_dir").mkdir()
    cmd = [args.verilator, "--cc", "--exe", "--build", "-j", "2", "--top-module", "KL_pp_nvm_port",
           "-Wall", "-Wno-fatal", "-Wno-DECLFILENAME", "-Wno-UNUSEDSIGNAL", "-Wno-WIDTHEXPAND",
           "-Wno-WIDTHTRUNC", "-Wno-UNUSEDPARAM", "-GMAX_PAYLOAD_P=1024",
           "-CFLAGS", f"-std=c++17 -O2 -I{tb} -Wall -Wextra",
           f"-GMEM_TIMEOUT_CYC_P={tmo}", "-CFLAGS", f"-DNVM_PORT_TMO={tmo} -Wall -Wextra",
           "--Mdir", "obj_dir", "../../hdl/packet_engine/KL_pp_nvm_port.sv", "sim_main.cpp",
           "-o", "Vnvm_port_sim"]
    b = subprocess.run(cmd, cwd=tb, capture_output=True, text=True)
    if b.returncode != 0:
        return {"job": tag, "error": "build failed", "log": (b.stdout + b.stderr)[-3000:]}
    try:
        r = subprocess.run(["./obj_dir/Vnvm_port_sim"], cwd=tb, capture_output=True, text=True,
                           timeout=args.run_timeout)
        out, rc = r.stdout + r.stderr, r.returncode
    except subprocess.TimeoutExpired as e:
        out, rc = (e.stdout or b"").decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or ""), "timeout"
    m = TALLY.search(out)
    fails = [l[6:] for l in out.splitlines() if l.startswith("FAIL: ")]
    (Path(args.out) / "logs").mkdir(parents=True, exist_ok=True)
    (Path(args.out) / "logs" / f"{tag}.log").write_text(out)
    shutil.rmtree(jd / "tb/nvm_port/obj_dir", ignore_errors=True)
    res = {"job": tag, "probe": probe, "model": model, "tmo": tmo, "rc": rc,
           "total": int(m.group(1)) if m else None, "fail": int(m.group(3)) if m else None,
           "fail_names": [f[:110] for f in fails]}
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("--run-timeout", type=int, default=900)
    ap.add_argument("spec")
    a = ap.parse_args()
    ns = {}
    exec(Path(a.spec).read_text(), ns)
    probes, runs = ns["PROBES"], ns["RUNS"]
    models = load_models(Path(a.repo))
    models["pristine"] = []
    results = []
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        futs = [ex.submit(run_job, a, models, probes, p, m, t) for p, m, t in runs]
        for f in cf.as_completed(futs):
            r = f.result()
            results.append(r)
            print(json.dumps({k: r.get(k) for k in ("job", "rc", "total", "fail", "error")}), flush=True)
    results.sort(key=lambda r: r["job"])
    Path(a.out).mkdir(parents=True, exist_ok=True)
    name = Path(a.spec).stem
    (Path(a.out) / f"{name}.json").write_text(json.dumps(results, indent=1))
    with open(Path(a.out) / f"{name}.txt", "w") as fh:
        for r in results:
            if "error" in r:
                fh.write(f"{r['job']}: ERROR {r['error']}\n")
                continue
            fh.write(f"{r['job']}: rc={r['rc']} {r['total']} checks, {r['fail']} FAIL\n")
            for n in r["fail_names"]:
                fh.write(f"    FAIL: {n}\n")
    print(Path(a.out) / f"{name}.txt")


if __name__ == "__main__":
    main()
