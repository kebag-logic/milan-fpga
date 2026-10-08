import argparse
import concurrent.futures
import importlib.util
import json
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("--repo", type=Path, required=True)
p.add_argument("--exe", type=Path, required=True)
p.add_argument("--out", type=Path, required=True)
p.add_argument("--jobs", type=int, required=True)
a = p.parse_args()
s = importlib.util.spec_from_file_location("sweep", a.repo / "tb/verilator/follow_ring/sweep.py")
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
runs = []
for k in range(16):
    for sign, ppm, dwell in [("slow", "-11.02", "1"), ("fast", "0.82", "45")]:
        for envelope, jitter, tail, probability in [("none", "0", "0", "0"),
                ("uniform5", "5", "0", "0"), ("tail24", "2", "24", "1e-4"),
                ("uniform60", "60", "0", "0")]:
            directory = a.out / (sign + "-" + envelope)
            directory.mkdir(parents=True, exist_ok=True)
            name = f"b8_j{jitter}_p{k:02d}"
            argv = ["--case", "b8", "--set-phase", f"{k/16:.6f}", "--jitter-us", jitter,
                    "--tail-us", tail, "--tail-p", probability, "--hold-s", "40",
                    "--switch-hold-s", "20", "--latency-us", "200", "--seed", str(645+k),
                    "--allow-ungradable", "--peer-ppm", ppm, "--dwell-s", dwell]
            runs.append((directory, name, argv))
results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:
    futures = {pool.submit(m.run, a.exe, directory, name, argv): directory.name
               for directory, name, argv in runs}
    for future in concurrent.futures.as_completed(futures):
        name, rc, lines = future.result()
        row = {"group": futures[future], "name": name, "rc": rc, "results": lines}
        results.append(row)
        (a.out / "results.json").write_text(json.dumps(results, indent=2) + "\n")
        print(f"{len(results)}/128 {futures[future]}/{name}: rc {rc}", flush=True)
rc = int(any(r["rc"] or not r["results"] for r in results))
(a.out / "all.rc").write_text(f"{rc}\n")
raise SystemExit(rc)
