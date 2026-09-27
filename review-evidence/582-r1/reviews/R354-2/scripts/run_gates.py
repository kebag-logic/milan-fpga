#!/usr/bin/env python3
"""Run focused review gates in a checkout, at most 8 at a time.

Usage: run_gates.py <checkout> <receipt-dir> <python> <base-rev>
Each command writes <receipt-dir>/<nn>-<slug>.log (stdout+stderr) and a
summary line "rc<TAB>seconds<TAB>command" to <receipt-dir>/SUMMARY.tsv.
"""
import concurrent.futures
import re
import subprocess
import sys
import time
from pathlib import Path

CHECKOUT, OUT, PY, BASE = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]

COMMANDS = [
    "{py} scripts/ci_scope.py --selftest",
    "{py} scripts/check_solution_docs.py",
    "{py} scripts/check_solution_docs.py --selftest",
    "{py} scripts/docs_check.py",
    "{py} scripts/docs_check.py --selftest",
    "{py} scripts/check_em_dash.py --base {base}",
    "{py} scripts/check_em_dash.py --selftest",
    "{py} scripts/check_doc_style.py",
    "{py} scripts/check_doc_style.py --selftest",
    "{py} scripts/check_doc_paths.py",
    "{py} docs/DOC_MAP.gen.py --check",
    "{py} scripts/gen_toc.py --check",
    "{py} scripts/gen_toc.py --verify-anchors",
    "{py} scripts/check_baremetal_only.py --check",
    "{py} scripts/check_baremetal_only.py --selftest",
    "{py} scripts/check_entity_shape.py --self-test",
    "{py} scripts/check_deploy_shape.py --self-test",
    "{py} scripts/check_sweep_shape.py --self-test",
    "{py} scripts/check_py_idiom.py",
    "{py} scripts/check_sh_idiom.py",
    "{py} scripts/check_hygiene.py --check",
    "{py} scripts/measure_naming.py --check",
    "{py} scripts/measure_fail_fast.py --check",
    "{py} scripts/measure_test_evidence.py --check",
    "{py} scripts/check_soc_sources.py",
    "{py} scripts/check_nvm_capture.py",
    "{py} sw/builder/test_declarations.py",
    "cd sw/builder && {py} test_clock_contract.py --soc",
    "{py} sw/litex/test_pp_mem_bridge.py",
    "git diff --check {base} HEAD",
]


def run(item):
    index, template = item
    command = template.format(py=PY, base=BASE)
    slug = re.sub(r"[^A-Za-z0-9]+", "-", command.replace(PY, "py"))[:70].strip("-")
    log = OUT / f"{index:02d}-{slug}.log"
    start = time.time()
    with log.open("w") as fh:
        fh.write(f"$ {command}\n")
        fh.flush()
        rc = subprocess.run(["bash", "-c", command], cwd=CHECKOUT, stdout=fh,
                            stderr=subprocess.STDOUT, timeout=3600).returncode
        fh.write(f"\n[rc={rc}]\n")
    return index, rc, time.time() - start, command


OUT.mkdir(parents=True, exist_ok=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results = sorted(pool.map(run, enumerate(COMMANDS)))
with (OUT / "SUMMARY.tsv").open("w") as fh:
    for index, rc, seconds, command in results:
        fh.write(f"{rc}\t{seconds:.1f}\t{command}\n")
        print(f"{rc}\t{seconds:.1f}\t{command}")
sys.exit(1 if any(rc for _, rc, _, _ in results) else 0)
