#!/usr/bin/env python3
"""Re-execute the published unchanged phase probe with bounded concurrency."""
import concurrent.futures
import json
import pathlib
import subprocess
import sys

packet = pathlib.Path(sys.argv[1])
def run(pair):
    shape, shift = pair
    log = packet / "receipts" / f"shift-{shape}-{shift}.log"
    command = ["sh", str(packet / "scripts/run_shift.sh"),
               str(packet / "scratch" / f"clean-{shape}"), str(shift), str(log)]
    launcher_rc = subprocess.run(command, check=False).returncode
    output = log.read_text()
    ok = launcher_rc == 0 and output.rstrip().endswith("rc=0") and "RESULT: PASS" in output
    result = {"shape": shape, "shift_cycles": shift, "launcher_rc": launcher_rc,
              "child_rc": int(output.rstrip().rsplit("rc=", 1)[1]), "pass": ok}
    print(json.dumps(result), flush=True)
    return result

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, [(s, v) for s in (1, 8)
                                 for v in (0, 200, 300, 800, 900, 1000000)]))
(packet / "receipts/shift-results.json").write_text(json.dumps(results, indent=2) + "\n")
raise SystemExit(not all(r["pass"] for r in results))
