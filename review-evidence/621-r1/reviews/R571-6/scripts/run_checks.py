#!/usr/bin/env python3
"""Run focused checks with joined foreground children and separate raw receipts."""
import argparse, concurrent.futures, json, os, pathlib, subprocess, sys, time
p = argparse.ArgumentParser()
p.add_argument("root", type=pathlib.Path)
p.add_argument("packet", type=pathlib.Path)
p.add_argument("--only", nargs="*")
a = p.parse_args()
a.root = a.root.resolve(); a.packet = a.packet.resolve()
receipts = a.packet / "receipts"
receipts.mkdir(exist_ok=True)
scratch = a.packet / "scratch" / "tmp"
scratch.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE="1")
env["PYTHONPATH"] = str(a.packet / "scratch/markdown-deps") + os.pathsep + env.get("PYTHONPATH", "")
checks = [
("docs-check", ["python3", "scripts/docs_check.py"]),
("em-dash", ["python3", "scripts/check_em_dash.py", "--base", "cfadd767a7ad47aaee68de655e1066cc000fb8a0"]),
("toc-check", ["python3", "scripts/gen_toc.py", "--check"]),
("toc-anchors", ["python3", "scripts/gen_toc.py", "--verify-anchors"]),
("doc-paths", ["python3", "scripts/check_doc_paths.py"]),
("ci-events-check", ["python3", "scripts/ci_events.py", "--check"]),
("ci-events-selftest", ["python3", "scripts/ci_events.py", "--selftest"]),
("test-evidence", ["python3", "scripts/measure_test_evidence.py", "--check"]),
("submodule-docs", ["python3", "scripts/check_submodule_docs.py"]),
("diagram-pngs", ["python3", "scripts/check_diagram_pngs.py"]),
("diagram-pngs-selftest", ["python3", "scripts/check_diagram_pngs.py", "--selftest"]),
("submodule-diagram", ["python3", "docs/diagrams/submodule_boundaries.gen.py", "--check"]),
("timesync-diagram", ["python3", "docs/diagrams/timesync_chain.gen.py", "--check"]),
("suite-shards", ["python3", "scripts/suite_shards.py", "--selftest"]),
("sim-pool", ["python3", "tb/verilator/milan_dp/test_sim_pool.py"]),
("backpressure-fixture", ["python3", str(a.packet / "scripts/backpressure_fixture.py"), str(a.root), str(a.packet)]),
("capture-receipt", ["python3", "scripts/check_nvm_capture.py"]),
]
if a.only:
    checks = [item for item in checks if item[0] in a.only]
def run(item):
    name, command = item
    start = time.monotonic()
    with (receipts / (name + ".log")).open("w") as log:
        result = subprocess.run(command, cwd=a.root, env=env, stdout=log, stderr=subprocess.STDOUT)
    (receipts / (name + ".rc")).write_text(str(result.returncode) + "\n")
    info = dict(name=name, argv=command, rc=result.returncode, seconds=round(time.monotonic()-start, 3))
    print(json.dumps(info), flush=True)
    return info
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(run, checks))
(receipts / ("checks-retry.json" if a.only else "checks.json")).write_text(json.dumps(results, indent=2) + "\n")
sys.exit(int(any(x["rc"] for x in results)))
