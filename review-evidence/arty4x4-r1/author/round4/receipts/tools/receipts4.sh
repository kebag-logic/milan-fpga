#!/bin/bash
# Copy round 4's receipts into the packet and index them. usage: receipts4.sh
set -eu
G=$VALIDATION_STORAGE/arty4x4-a863/gates4; O=$MANAGEMENT/2026-09-23/arty4x4-a863/round4/receipts
mkdir -p $O/tools $O/docs
cp $G/harness4.rc $O/harness4.rc.txt
for n in ledger-selftest ledger-census4 arty-grade-1x1 arty-grade-4x4 arty-grade-selftest fw-coverage-selftest fw-coverage-check; do gzip -c $G/$n.log > $O/$n.log.gz; done
cp $G/service-selftest.json $O/; for n in 0 1 2 3 4 5 6 7; do gzip -c $G/service-selftest-$n.log > $O/service-selftest-$n.log.gz; done
cp $G/docs/results.json $O/docs/docs-results.json; tar -C $G/docs -czf $O/docs/docs-logs.tar.gz $(cd $G/docs && ls *.log)
cp $G/venv-docs.rc $O/docs/venv-docs.rc.txt; cp $G/venv2-docs.rc $O/docs/venv2-docs.rc.txt
for f in $G/venv-docs-*.log $G/venv2-*.log; do gzip -c $f > $O/docs/$(basename $f).gz; done
cp $G/em-dash.log $O/docs/em-dash.log
cp $G/identity-head2/digests.json $O/identity-head-digests.json
cp $MANAGEMENT/2026-09-23/arty4x4-a863/round3/receipts/identity-base-digests.json $O/identity-base-digests.json
cp $G/p4x4b.log $O/product-4x4.log; cp $G/p4x4b/product/size.json $O/product-4x4-size.json
gzip -c $G/test_builder.log > $O/test_builder.log.gz; cp $G/test_builder.rc $O/test_builder.rc.txt; cp $G/test_builder.head $O/test_builder.head.txt
cp $G/gates-results.json $O/gates-results.json 2>/dev/null || true; cp $G/gates.log $O/gates.log
for f in $G/firmware-*.log $G/boot-*.log $G/region-*.log $G/ctrl-memory.log $G/host-arms.log; do [ -f $f ] && gzip -c $f > $O/gate-$(basename $f).gz; done
T=$VALIDATION_STORAGE/arty4x4-a863/tools
cp $T/docs-gates4.py $T/docs-cmds.txt $T/harness4.sh $T/service-selftest4.py $T/gates4.py $T/builder-suite4.sh $T/identity.py $T/product.py $T/run-env.sh $T/receipts4.sh $O/tools/
cd $MANAGEMENT/2026-09-23/arty4x4-a863/round4
python3 - <<'PY'
import hashlib
from pathlib import Path
r=Path('receipts'); rows=[]
for p in sorted(r.rglob('*')):
    if p.is_file() and p.name!='INDEX.md':
        rows.append(f'| `{p.relative_to(r)}` | {p.stat().st_size} | `{hashlib.sha256(p.read_bytes()).hexdigest()}` |')
head='''# Round 4 receipts

Head `12ab4b189f54439cd126f677b906a19835d7f32a`. Gate logs from `$VALIDATION_STORAGE/arty4x4-a863/gates4`; round 3's receipts (route, censuses, qualification, egress) stand and are not repeated.

- `harness4.rc.txt`, `ledger-*`, `arty-grade-*`, `fw-coverage-*`: the harness gates (`tools/harness4.sh`).
- `service-selftest*`: the service self-test, 8 partitions (`tools/service-selftest4.py`).
- `docs/`: the docs workflow's runner-free checks (`tools/docs-gates4.py`, `tools/docs-cmds.txt`), and their re-runs in the LiteX and Markdown venvs (`venv-docs.rc.txt`, `venv2-docs.rc.txt`, `em-dash.log`).
- `identity-*-digests.json`, `product-4x4*`: byte identity at head against the base `aa53840d9`.
- `test_builder.*`: the builder suite.
- `gates-results.json`, `gates.log`, `gate-*`: firmware, boot, region, memory and host gates (`tools/gates4.py`).

| File | Bytes | sha256 |
|---|---:|---|
'''
Path('receipts/INDEX.md').write_text(head+'\n'.join(rows)+'\n')
print(len(rows),'files')
PY
