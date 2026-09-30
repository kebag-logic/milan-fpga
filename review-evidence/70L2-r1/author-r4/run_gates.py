"""Run the round-4 gate bank at one committed head, never piped, logs outside the packet.

Usage: run_gates.py <logdir> <receipt.json> [--only name ...]
Each gate runs with its stdout and stderr in <logdir>/<name>.log; the receipt
records the command, rc, seconds, log size and SHA-256, and the head before and
after. The two builder banks run one after the other (they share the builder's
outputs and are the heavy pair); every other gate runs in a second chain beside
them. The pinned Verilator wrapper of the manager's consumer bank is first on
PATH and the pinned Markdown environment runs the Markdown gates. `review-runs`
checks the logs R412-3's probe_all.sh and census_mutants_run.sh (run unchanged
from a copy of that review's scripts) and this round's probes wrote at this head.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT = Path('$LANES/70-lane2-pin')
BASE = '79c36963660c10e4c1c11a744fb5bff41a552b8b'
OUT = Path(__file__).parent
PACKET = Path('$VALIDATION_STORAGE/a460-70L2r4/packet')
MD = '$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python'
LITEX = '$WORKSPACE_HOME/litex-milan/venv/bin/python'
ENV = dict(os.environ, PYTHONHASHSEED='0', PYTHONDONTWRITEBYTECODE='1', PYTHONUNBUFFERED='1',
           PATH='$VALIDATION_STORAGE/pp131-manager-9b4da6b5/pinned-tool-bin:$WORKSPACE_HOME/.local/bin:'
                '$WORKSPACE_HOME/Xilinx/2026.1/Vivado/bin:/usr/local/bin:/usr/bin:/bin')

GATES = [
    ('builder-present', [LITEX, '-B', 'sw/builder/test_builder.py', '--require-elaboration', '--require-rv32']),
    ('builder-absent', [LITEX, '-B', str(OUT / 'full-builder-absent.py')]),
    ('review-runs', ['python3', str(OUT / 'check_review_runs.py'), str(ROOT), str(PACKET / 'receipts')]),
    ('firmware-digest', ['python3', str(OUT / 'check_firmware_digest.py'), str(ROOT)]),
    ('check_nvm_capture', ['python3', 'scripts/check_nvm_capture.py']),
    ('fw_service_budget-selftest', ['python3', 'tb/verilator/fw_service_budget/run.py', '--self-test']),
    ('grader-mutants', ['python3', str(OUT / 'check_grader_mutants.py'), str(ROOT), str(PACKET / 'scripts'),
                        str(PACKET / 'scratch' / 'grader')]),
    ('check_py_idiom', ['python3', 'scripts/check_py_idiom.py']),
    ('measure_test_evidence', ['python3', 'scripts/measure_test_evidence.py', '--check']),
    ('diff-check', ['git', 'diff', '--check', BASE, 'HEAD']),
    ('md-docs_check', [MD, 'scripts/docs_check.py']),
    ('md-check_doc_paths', [MD, 'scripts/check_doc_paths.py']),
    ('md-check_doc_style', [MD, 'scripts/check_doc_style.py']),
    ('md-check_archive', [MD, 'scripts/check_archive.py']),
    ('md-gen_toc', [MD, 'scripts/gen_toc.py', '--check']),
    ('md-check_em_dash', [MD, 'scripts/check_em_dash.py', '--base', BASE]),
]

CHAINS = [
    ['builder-present', 'builder-absent'],
    ['review-runs', 'firmware-digest', 'check_nvm_capture', 'fw_service_budget-selftest', 'grader-mutants',
     'check_py_idiom', 'measure_test_evidence', 'diff-check', 'md-docs_check', 'md-check_doc_paths',
     'md-check_doc_style', 'md-check_archive', 'md-gen_toc', 'md-check_em_dash'],
]


def git(*args):
    """stdout of one git command in the lane."""
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def run(name, argv, logdir):
    """Run one gate with its output in its own log; return its receipt entry."""
    log = logdir / f'{name}.log'
    start = time.monotonic()
    with log.open('w') as stream:
        rc = subprocess.run(argv, cwd=ROOT, env=ENV, stdout=stream, stderr=subprocess.STDOUT).returncode
    raw = log.read_bytes()
    return dict(name=name, command=argv, rc=rc, seconds=round(time.monotonic() - start, 1),
                log=str(log), log_bytes=len(raw), log_sha256=hashlib.sha256(raw).hexdigest())


def main():
    """Run every selected gate chain and write the receipt."""
    logdir, receipt = Path(sys.argv[1]), Path(sys.argv[2])
    only = sys.argv[sys.argv.index('--only') + 1:] if '--only' in sys.argv else None
    logdir.mkdir(parents=True, exist_ok=True)
    head = git('rev-parse', 'HEAD')
    tree = git('rev-parse', 'HEAD^{tree}')
    assert not git('status', '--porcelain', '--untracked-files=no'), 'dirty worktree'
    assert git('-C', 'protocol-processor', 'rev-parse', '--show-toplevel') == str(ROOT / 'protocol-processor')
    assert git('ls-tree', 'HEAD', 'protocol-processor').split()[2] == \
        git('-C', 'protocol-processor', 'rev-parse', 'HEAD')
    gates = dict(GATES)
    assert sorted(n for c in CHAINS for n in c) == sorted(gates), 'every gate in exactly one chain'
    chains = [[name for name in chain if only is None or name in only] for chain in CHAINS]
    results = []

    def record(final=None):
        body = dict(head=head, tree=tree, results=results)
        if final:
            body.update(final)
        receipt.write_text(json.dumps(body, indent=2) + '\n')

    def run_chain(chain):
        for name in chain:
            result = run(name, gates[name], logdir)
            results.append(result)
            print(result['name'], result['rc'], result['seconds'], flush=True)
            record()

    with ThreadPoolExecutor(max_workers=len(chains)) as pool:
        list(pool.map(run_chain, chains))
    after = git('rev-parse', 'HEAD')
    clean = not git('status', '--porcelain', '--untracked-files=no')
    record(dict(head_after=after, clean_after=clean))
    print('GATES DONE', head, 'clean' if clean else 'DIRTY',
          'all rc 0' if all(r['rc'] == 0 for r in results) else 'FAILURES', flush=True)


if __name__ == '__main__':
    main()
