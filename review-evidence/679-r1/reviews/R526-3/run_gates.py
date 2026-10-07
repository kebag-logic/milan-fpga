#!/usr/bin/env python3
"""Run independent focused gates concurrently, joining all foreground commands."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

packet = Path(__file__).resolve().parent
repo = Path(sys.argv[1]).resolve()
python = sys.executable
gates = {
    'docs_check': ['scripts/docs_check.py'],
    'toc_check': ['scripts/gen_toc.py', '--check'],
    'toc_anchors': ['scripts/gen_toc.py', '--verify-anchors'],
    'em_dash': ['scripts/check_em_dash.py', '--base', '72d3780d23a0b96362f8ae64059311b866ff5776'],
    'ci_events_check': ['scripts/ci_events.py', '--check'],
    'ci_events_selftest': ['scripts/ci_events.py', '--selftest'],
    'ci_scope': ['scripts/ci_scope.py', '--selftest'],
    'doc_style': ['scripts/check_doc_style.py'],
    'doc_paths': ['scripts/check_doc_paths.py'],
    'feature_status': ['scripts/check_feature_status.py'],
    'test_evidence_check': ['scripts/measure_test_evidence.py', '--check'],
    'test_evidence_selftest': ['scripts/measure_test_evidence.py', '--selftest'],
    'nvm_record_space': ['scripts/check_nvm_record_space.py'],
    'suite_shards': ['scripts/suite_shards.py', '--selftest'],
    'submodule_docs': ['scripts/check_submodule_docs.py'],
}

def run(item):
    name, args = item
    command = [python, str(packet / 'run_receipt.py'), '--repo', str(repo), '--name', name, '--', python, *args]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    print(result.stdout, flush=True)
    return name, result.returncode

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    results = list(pool.map(run, gates.items()))
print('Focused gate results:', results, flush=True)
raise SystemExit(int(any(rc for _, rc in results)))
