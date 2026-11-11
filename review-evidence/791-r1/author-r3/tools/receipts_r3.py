#!/usr/bin/env python3
"""receipts_r3.py: copy round 3's cited logs (head c7e4badb) into receipts/r3/ with host paths replaced, then rewrite
receipts/INDEX.md from every file present (receipts.py's scrub and index)."""
import receipts as r

S, R3 = r.S, r.R / 'r3'
F = S / 'r3'
J = S / 'ci/c7e4badb4caf/jobs'
COPIES = {
    **{f'tcm/run.{x}': F / f'tcm.{x}' for x in ('log', 'rc')},
    **{f'region-decode/self-test.{x}': F / f'region-self-test.{x}' for x in ('log', 'rc')},
    **{f'probes/{n}.{x}': F / f'{m}.{x}' for n, m in (('guard_probe', 'guard-probe'), ('guard_probe2', 'guard-probe2'),
                                                       ('cpupatches_probe', 'cpupatches-probe')) for x in ('log', 'rc')},
    **{f'decode/product-decode.{x}': F / f'product-decode.{x}' for x in ('log', 'rc')},
    **{f'decode/{s}.txt': F / f'decode/{s}.txt' for s in ('endstation_ax7101_1x1_tdm8', 'endstation_ax7101_8x8')},
    **{f'allfabric/allfabric.{x}': F / f'allfabric.{x}' for x in ('log', 'rc')},
    'allfabric/allfabric-compare.txt': F / 'allfabric-receipt/allfabric-compare.txt',
    **{f'gates/{g}.{x}': F / f'{g}.{x}' for g in ('diff-check', 'netlist-identity') for x in ('log', 'rc')},
    **{f'gates/chain-{c}.txt': F / f'chain-{c}.log' for c in ('a', 'b', 'c')},
    'ci/docs-chain.txt': F / 'docs-chain.log', 'ci/docs-chain-attempt1.txt': F / 'docs-chain-attempt1.log',
    'ci/docs-replay-table.md': F / 'docs-table.md', 'ci/docs-not_run.json': F / 'docs-not_run.json',
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
print(f'{sum(1 for q in R3.rglob("*") if q.is_file())} files under receipts/r3/')
