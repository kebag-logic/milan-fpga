#!/usr/bin/env python3
"""Fetch selected round-4 author receipts from the immutable public evidence commit and check each
against the evidence packet's MANIFEST.json (published_sha256). Read-only GitHub API use via `gh`.

Usage: python3 -I verify_public.py OUTDIR
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO, REF, BASE = 'kebag-logic/milan-fpga', 'efd9f61c563776a3db0306e5abc4ff6537df695e', 'review-evidence/665s4-r1'
WANT = [
    'author-r4/PR-BODY.md', 'author-r4/receipts/INDEX.md', 'author-r4/receipts/gates-long-summary.md',
    'author-r4/receipts/gates-short/summary.md', 'author-r4/receipts/gates-short/HEAD.txt',
    'author-r4/receipts/gates-long/HEAD.txt', 'author-r4/receipts/gates-long-rest/HEAD.txt',
    'author-r4/receipts/gates-short/nvm_target_selftest.log', 'author-r4/receipts/gates-short/nvm_capture.log',
    'author-r4/receipts/probes/real-refusal-1x1.log', 'author-r4/receipts/probes/real-refusal-8x8.log',
    'author-r4/receipts/probes/reuse-mutant-failures.txt', 'author-r4/receipts/probes/reuse-probe.log',
    'author-r4/receipts/probes/round3-identity.txt', 'author-r4/receipts/scope/HEAD.txt',
    'author-r4/receipts/scope/commits.txt', 'author-r4/receipts/scope/rtl-unchanged.txt',
    'author-r4/receipts/scope/runs-head.txt', 'author-r4/receipts/scope/merge-check.txt',
    'author-r4/receipts/scope/diffstat-round4.txt', 'author-r4/receipts/d5-plant/plant_d5_removed.log',
    'author-r4/receipts/target-1x1/run-tail.log', 'author-r4/receipts/target-1x1/results.json',
    'author-r4/receipts/target-1x1/table.md', 'author-r4/receipts/target-1x1/build-clocks.txt',
    'author-r4/receipts/target-8x8/run-tail.log', 'author-r4/receipts/target-8x8/results.json',
    'author-r4/receipts/target-8x8/table.md', 'author-r4/receipts/target-8x8/build-clocks.txt',
]


def raw(path: str) -> bytes:
    return subprocess.run(['gh', 'api', '-H', 'Accept: application/vnd.github.raw',
                           f'repos/{REPO}/contents/{BASE}/{path}?ref={REF}'], check=True, capture_output=True).stdout


def main() -> int:
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    manifest = {e['file']: e for e in json.loads(raw('MANIFEST.json'))}
    bad = 0
    for path in WANT:
        data = raw(path)
        (out / path).parent.mkdir(parents=True, exist_ok=True)
        (out / path).write_bytes(data)
        got = hashlib.sha256(data).hexdigest()
        want = manifest.get(path, {}).get('published_sha256')
        ok = got == want
        bad += not ok
        print(f"{'MATCH' if ok else 'MISMATCH'} {path} {got} manifest={want}")
    print(f'files: {len(WANT)}   mismatches: {bad}')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
