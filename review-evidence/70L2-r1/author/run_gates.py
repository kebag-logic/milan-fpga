"""Run the lane's gate bank at one committed head, never piped, logs outside the packet.

Usage: run_gates.py <logdir> <receipt.json> [--serial] [--only name ...]
Each gate runs with its stdout and stderr in <logdir>/<name>.log; the receipt
records the command, rc, seconds, log size and SHA-256, and the head before and
after. Gates run in CHAINS: a chain runs its gates one after the other (the two
builder banks share the builder's outputs), and the chains run side by side.
--serial runs the selected gates one after the other in the order --only names
them (the resume after the memory cap: never two heavy builds at once).
The pinned Verilator wrapper of the
manager's consumer bank is first on PATH, Vivado's settings are sourced for
xvlog, and the pinned Markdown environment runs the Markdown gates.
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
MD = '$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python'
LITEX = '$WORKSPACE_HOME/litex-milan/venv/bin/python'
ENV = dict(os.environ, PYTHONHASHSEED='0', PYTHONDONTWRITEBYTECODE='1', PYTHONUNBUFFERED='1',
           PATH='$VALIDATION_STORAGE/pp131-manager-9b4da6b5/pinned-tool-bin:$WORKSPACE_HOME/.local/bin:'
                '$WORKSPACE_HOME/Xilinx/2026.1/Vivado/bin:/usr/local/bin:/usr/bin:/bin')

GATES = [
    ('builder-present', [LITEX, '-B', 'sw/builder/test_builder.py', '--require-elaboration', '--require-rv32']),
    ('builder-absent', [LITEX, '-B', str(OUT / 'full-builder-absent.py')]),
    ('nvm_cosim-full', ['make', '-C', 'tb/verilator/nvm_cosim']),
    ('nvm_cosim-lint', ['make', '-C', 'tb/verilator/nvm_cosim', 'lint']),
    ('pp_shadow', ['make', '-C', 'tb/verilator/pp_shadow', '-j8']),
    ('milan_dp', ['make', '-C', 'tb/verilator/milan_dp', '-j8']),
    ('milan_dp-ax1x1gptp', ['make', '-C', 'tb/verilator/milan_dp', 'ax1x1gptp']),
    ('milan_dp_render', ['make', '-C', 'tb/verilator/milan_dp_render', '-j8']),
    ('host-firmware-selftest', ['python3', 'sw/firmware/nvm_hosttest/test_nvm_firmware.py', '--self-test']),
    ('check_nvm_capture', ['python3', 'scripts/check_nvm_capture.py']),
    ('fw_service_budget-selftest', ['python3', 'tb/verilator/fw_service_budget/run.py', '--self-test']),
    ('yosys-portability', ['bash', 'syn/yosys/run.sh']),
    ('lint_rtl', ['python3', 'scripts/lint_rtl.py', '--check']),
    ('xvlog_gate', ['python3', 'scripts/xvlog_gate.py', '--check']),
    ('check_rtl_source_lists', ['python3', 'scripts/check_rtl_source_lists.py']),
    ('pp_srcs', ['python3', 'scripts/pp_srcs.py', '--check', '--selftest']),
    ('check_port_contracts', ['python3', 'scripts/check_port_contracts.py']),
    ('measure_naming', ['python3', 'scripts/measure_naming.py', '--check']),
    ('measure_test_evidence', ['python3', 'scripts/measure_test_evidence.py', '--check']),
    ('check_cpp_idiom', ['python3', 'scripts/check_cpp_idiom.py']),
    ('check_py_idiom', ['python3', 'scripts/check_py_idiom.py']),
    ('check_feature_status', ['python3', 'scripts/check_feature_status.py']),
    ('check_submodule_docs', ['python3', 'scripts/check_submodule_docs.py']),
    ('submodule_boundaries', ['python3', 'docs/diagrams/submodule_boundaries.gen.py', '--check']),
    ('check_baremetal_only', ['python3', 'scripts/check_baremetal_only.py', '--check']),
    ('ci_scope', ['python3', 'scripts/ci_scope.py', '--selftest']),
    ('integrator_params', ['python3', 'protocol-processor/scripts/check-integrator-params.py']),
    ('diff-check', ['git', 'diff', '--check', BASE, 'HEAD']),
    ('md-docs_check', [MD, 'scripts/docs_check.py']),
    ('md-check_doc_paths', [MD, 'scripts/check_doc_paths.py']),
    ('md-check_doc_style', [MD, 'scripts/check_doc_style.py']),
    ('md-check_archive', [MD, 'scripts/check_archive.py']),
    ('md-gen_toc', [MD, 'scripts/gen_toc.py', '--check']),
    ('md-check_em_dash', [MD, 'scripts/check_em_dash.py', '--base', BASE]),
]

CHAINS = [
    ['builder-present', 'builder-absent', 'host-firmware-selftest', 'check_nvm_capture',
     'fw_service_budget-selftest'],
    ['nvm_cosim-full', 'nvm_cosim-lint', 'pp_shadow', 'milan_dp_render', 'yosys-portability'],
    ['milan_dp', 'milan_dp-ax1x1gptp'],
    ['lint_rtl', 'xvlog_gate', 'check_rtl_source_lists', 'pp_srcs', 'check_port_contracts',
     'measure_naming', 'measure_test_evidence', 'check_cpp_idiom', 'check_py_idiom',
     'check_feature_status', 'check_submodule_docs', 'submodule_boundaries',
     'check_baremetal_only', 'ci_scope', 'integrator_params', 'diff-check',
     'md-docs_check', 'md-check_doc_paths', 'md-check_doc_style', 'md-check_archive',
     'md-gen_toc', 'md-check_em_dash'],
]


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def run(name, argv, logdir):
    log = logdir / f'{name}.log'
    start = time.monotonic()
    with log.open('w') as stream:
        rc = subprocess.run(argv, cwd=ROOT, env=ENV, stdout=stream, stderr=subprocess.STDOUT).returncode
    raw = log.read_bytes()
    return dict(name=name, command=argv, rc=rc, seconds=round(time.monotonic() - start, 1),
                log=str(log), log_bytes=len(raw), log_sha256=hashlib.sha256(raw).hexdigest())


def main():
    logdir, receipt = Path(sys.argv[1]), Path(sys.argv[2])
    only = sys.argv[sys.argv.index('--only') + 1:] if '--only' in sys.argv else None
    logdir.mkdir(parents=True, exist_ok=True)
    head = git('rev-parse', 'HEAD')
    assert not git('status', '--porcelain', '--untracked-files=no'), 'dirty worktree'
    assert git('ls-tree', 'HEAD', 'protocol-processor').split()[2] == \
        git('-C', 'protocol-processor', 'rev-parse', 'HEAD')
    gates = dict(GATES)
    chains = [[name for name in chain if only is None or name in only] for chain in CHAINS]
    assert sorted(n for c in CHAINS for n in c) == sorted(gates), 'every gate in exactly one chain'
    if '--serial' in sys.argv:
        assert only and all(name in gates for name in only), only
        chains = [only]
    results = []

    def run_chain(chain):
        for name in chain:
            result = run(name, gates[name], logdir)
            results.append(result)
            print(result['name'], result['rc'], result['seconds'], flush=True)
            receipt.write_text(json.dumps(dict(head=head, results=results), indent=2) + '\n')

    with ThreadPoolExecutor(max_workers=len(chains)) as pool:
        list(pool.map(run_chain, chains))
    after = git('rev-parse', 'HEAD')
    clean = not git('status', '--porcelain', '--untracked-files=no')
    receipt.write_text(json.dumps(dict(head=head, head_after=after, clean_after=clean,
                                       results=results), indent=2) + '\n')
    print('GATES DONE', head, 'clean' if clean else 'DIRTY',
          'all rc 0' if all(r['rc'] == 0 for r in results) else 'FAILURES', flush=True)


if __name__ == '__main__':
    main()
