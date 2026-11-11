#!/usr/bin/env python3
"""receipts_r4.py: copy round 4's cited logs (head 6a5acf06) into receipts/r4/ with host paths replaced, then rewrite
receipts/INDEX.md from every file present (receipts.py's scrub and index)."""
import receipts as r

S, R3 = r.S, r.R / 'r4'
F = S / 'r4'
J = S / 'ci/6a5acf06c80c/jobs'
COPIES = {
    **{f'tcm/run.{x}': F / f'tcm.{x}' for x in ('log', 'rc')},
    **{f'region-decode/self-test.{x}': F / f'region-self-test.{x}' for x in ('log', 'rc')},
    **{f'allfabric/allfabric.{x}': F / f'allfabric.{x}' for x in ('log', 'rc')},
    'allfabric/allfabric-compare.txt': F / 'allfabric-receipt/allfabric-compare.txt',
    **{f'gates/{g}.{x}': F / f'{g}.{x}' for g in ('py-idiom', 'py-idiom-selftest', 'diff-check') for x in ('log', 'rc')},
    **{f'gates/chain-{c}.txt': F / f'chain-{c}.log' for c in ('a', 'b', 'c')},
    'ci/docs-chain.txt': F / 'docs-chain.log',
    'ci/docs-replay-table.md': F / 'docs-table.md', 'ci/docs-not_run.json': F / 'docs-not_run.json',
    'ci/superseded-14a0c538-py-idiom.log': S / 'superseded/r4-14a0c538/py-idiom.log',
    **{f'ci/results/{j}.json': J / j / 'result.json' for j in (
        'docs__wire-accountability', 'docs__docs-check-no-git', 'docs__docs-gates-0', 'docs__docs-gates-1',
        'docs__docs-gates-2', 'docs__docs-check', 'docs__ci-manifest', 'docs__ci-fail-fast', 'docs__ci-cancel-tail')},
}
for name, src in COPIES.items():
    if src.exists():
        out = R3 / name
        out.parent.mkdir(parents=True, exist_ok=True)
        data = src.read_bytes()
        assert len(data) <= r.LIMIT, f'{name}: {len(data)} bytes'
        out.write_bytes(r.scrub(data))
r.index()
print(f'{sum(1 for q in R3.rglob("*") if q.is_file())} files under receipts/r4/')
