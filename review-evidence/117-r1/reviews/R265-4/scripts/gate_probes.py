#!/usr/bin/env python3
"""Disposable mutation probes: can the documentation gates fail on the #117 findings page?

usage: gate_probes.py <repo> [<private-token-file>]
Each probe rewrites docs/findings/117_GPTP_SILICON_EVIDENCE.md in the working tree, runs one
gate, records its exit status and summary line, then restores the exact HEAD bytes and checks
them against the HEAD blob before the next probe. Private tokens come from the repository's own
assembled constants (scripts/docs_check.py) or from a private file that is never published.
"""
import hashlib
import importlib.util
import json
import subprocess
import sys

repo = sys.argv[1]
priv = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else {}
PAGE = 'docs/findings/117_GPTP_SILICON_EVIDENCE.md'
spec = importlib.util.spec_from_file_location('dc', repo + '/scripts/docs_check.py')
dc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dc)


def git(*a):
    return subprocess.run(['git', '-C', repo, *a], capture_output=True).stdout


orig = git('show', 'HEAD:' + PAGE)
head_blob = git('rev-parse', 'HEAD:' + PAGE).decode().strip()


def blob_of(b):
    return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()


assert blob_of(orig) == head_blob


def run(cmd):
    r = subprocess.run(cmd, cwd=repo, capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip().splitlines()
    return r.returncode, out


def probe(name, mutate, cmd, expect_fail, grep=None):
    txt = orig.decode('utf-8')
    new = mutate(txt)
    assert new != txt, name
    open(f'{repo}/{PAGE}', 'w', encoding='utf-8').write(new)
    try:
        rc, out = run(cmd)
    finally:
        open(f'{repo}/{PAGE}', 'wb').write(orig)
    restored = open(f'{repo}/{PAGE}', 'rb').read()
    ok_restore = blob_of(restored) == head_blob
    hit = [l for l in out if grep and grep in l]
    verdict = ('FIRES' if rc != 0 else 'SILENT')
    good = (rc != 0) == expect_fail
    print(f'{name}: gate rc={rc} {verdict} (expected {"fail" if expect_fail else "pass"}: {"as expected" if good else "UNEXPECTED"}); '
          f'matching lines {len(hit)}; restored-bytes-equal-HEAD-blob={ok_restore}')
    for l in (hit or out[-2:])[:3]:
        print('    |', l[:160])
    return good and ok_restore


results = []
tail = '\n'
host = dc._BENCH_HOST_TOKEN + '-' + 'pw' + '1'
results.append(probe('P1 bench-host-prefix line', lambda t: t + tail + f'The controller host is {host}.\n',
                     ['python3', 'scripts/docs_check.py'], True, 'bench host prefix'))
results.append(probe('P2 peer product name', lambda t: t + tail + f'The reference peer is a {dc._PEER_TOKEN}D.\n',
                     ['python3', 'scripts/docs_check.py'], True, 'peer product name'))
results.append(probe('P3 retired bare-metal phrase restored',
                     lambda t: t.replace('reports 0 dropped packets', 'reports 0 kernel drops', 1),
                     ['python3', 'scripts/check_baremetal_only.py', '--check'], True, '117_GPTP'))
# Anchor and link probes. Expectations record the observed gate scope: only
# gen_toc.py --verify-anchors checks cross-page fragments, docs_check.py checks
# relative-link targets, and no gate checks in-page
# fragments (so the review resolves those directly).
for gate, exp5, exp6 in ((['python3', 'scripts/gen_toc.py', '--verify-anchors'], False, True),
                         (['python3', 'scripts/check_doc_paths.py'], False, False),
                         (['python3', 'scripts/gen_toc.py', '--check'], False, False),
                         (['python3', 'scripts/docs_check.py'], False, False)):
    results.append(probe('P5 broken in-page anchor via ' + gate[1] + ' ' + ' '.join(gate[2:]), lambda t: t.replace('(#grandmaster-change-across-the-loss-and-return)', '(#grandmaster-change-across-the-loss-and-returns)', 1),
                         gate, exp5, '117_GPTP'))
    results.append(probe('P6 broken cross-page anchor via ' + gate[1] + ' ' + ' '.join(gate[2:]), lambda t: t.replace('GM_LOSS_RECOVERY.md#recovery-bound)', 'GM_LOSS_RECOVERY.md#recovery-bounds)', 1),
                         gate, exp6, '117_GPTP'))
    results.append(probe('P6b broken relative link target via ' + gate[1] + ' ' + ' '.join(gate[2:]), lambda t: t.replace('(../design/GM_LOSS_RECOVERY.md#recovery-bound)', '(../design/GM_LOSS_RECOVERYX.md#recovery-bound)', 1),
                         gate, gate[-1].endswith('docs_check.py'), 'GM_LOSS_RECOVERYX'))
results.append(probe('P7 home path', lambda t: t + tail + 'Scripts ran from /home/' + 'someone/bench.\n',
                     ['python3', 'scripts/docs_check.py'], True, 'home path'))
PROBE_CLASS = 'capture server machine host name'  # the F1 residual class; other classes are covered by P1/P2
for i, (cls, toks) in enumerate((k, v) for k, v in priv.items() if k == PROBE_CLASS):
    results.append(probe(f'P{8 + i} private token class "{cls}" (the redaction residual class)',
                         lambda t, tok=toks[0]: t + tail + f'The capture server answers as {tok}.\n',
                         ['python3', 'scripts/docs_check.py'], False, None))
print('probes as expected and restored:', sum(results), 'of', len(results))
