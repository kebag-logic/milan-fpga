"""Run foreground #577 gates with bounded retained logs and exact return codes."""
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import time

ROOT = Path('$LANES/577-image-l6-l10')
OUT = Path(__file__).resolve().parent
PYTHON = '/tmp/milan-577-venv/bin/python'
BASE = '54ce877371ee6e8878cf67294e86c2a8481b62f6'
GROUPS = {
    'builder': [
        ['sw/builder/test_builder.py', '--require-rv32'],
        ['sw/builder/test_firmware_compiler.py', '--selftest'],
        ['sw/builder/test_firmware_compiler.py', '--absent', '--audit', '/tmp/milan-577-absent.jsonl'],
    ],
    'docs': [
        ['scripts/docs_check.py'],
        ['scripts/docs_check.py', 'NO_GIT_MODE'],
        ['scripts/check_em_dash.py', '--base', BASE],
        ['scripts/check_doc_style.py'], ['scripts/check_doc_style.py', '--selftest'],
        ['scripts/gen_toc.py', '--check'], ['scripts/gen_toc.py', '--verify-anchors'],
        ['scripts/gen_toc.py', '--selftest'],
        ['scripts/check_doc_paths.py'],
        ['scripts/check_feature_status.py', '--self-test'],
        ['docs/traceability/gen_module_matrix.py', '--check'],
        ['scripts/check_gptp_docs.py', '--with-submodule'], ['scripts/check_gptp_docs.py', '--selftest'],
        ['scripts/check_solution_docs.py'], ['scripts/check_solution_docs.py', '--selftest'],
        ['scripts/check_submodule_docs.py'], ['scripts/check_submodule_docs.py', '--selftest'],
        ['scripts/check_archive.py'], ['scripts/check_archive.py', '--selftest'],
        ['scripts/ci_events.py', '--check'], ['scripts/ci_events.py', '--selftest'],
        ['scripts/check_py_idiom.py'], ['scripts/check_py_idiom.py', '--selftest'],
        ['scripts/check_baremetal_only.py', '--check'], ['scripts/check_baremetal_only.py', '--selftest'],
        ['scripts/check_rtl_source_lists.py'], ['scripts/check_rtl_source_lists.py', '--selftest'],
        ['scripts/check_port_contracts.py'], ['scripts/check_port_contracts.py', '--selftest'],
        ['scripts/measure_naming.py', '--check'], ['scripts/measure_naming.py', '--selftest'],
        ['scripts/measure_fail_fast.py', '--check'], ['scripts/measure_fail_fast.py', '--selftest'],
        ['scripts/check_todo_ownership.py'], ['scripts/check_todo_ownership.py', '--selftest'],
        ['scripts/measure_test_evidence.py', '--check'], ['scripts/measure_test_evidence.py', '--selftest'],
        ['scripts/check_hygiene.py', '--check'], ['scripts/check_hygiene.py', '--selftest'],
        ['scripts/check_sv_idiom.py'], ['scripts/check_sv_idiom.py', '--selftest'],
        ['scripts/check_cpp_idiom.py'], ['scripts/check_cpp_idiom.py', '--selftest'],
        ['scripts/measure_control_flow.py', '--selftest'], ['scripts/measure_cohesion.py', '--selftest'],
        ['avdecc/gen_aem_store.py', '--self-test'],
        ['scripts/check_entity_shape.py', '--self-test'],
        ['scripts/check_wire_accountability.py', '--self-test'],
    ],
    'diagrams': [
        ['docs/DOC_MAP.gen.py', '--check'], ['docs/DOC_MAP.gen.py', '--selftest'],
        ['docs/diagrams/timesync_chain.gen.py', '--check'], ['docs/diagrams/timesync_chain.gen.py', '--selftest'],
        ['docs/diagrams/submodule_boundaries.gen.py', '--check'],
        ['docs/diagrams/submodule_boundaries.gen.py', '--selftest'],
        ['scripts/gen_wavedrom.py', '--selftest'],
        ['scripts/gen_wavedrom.py', 'docs/diagrams/wd_axis_backpressure.json', '--background=white', '--check'],
        ['scripts/gen_wavedrom.py', 'docs/diagrams/wd_cdc_handshake.json', '--background=white', '--check'],
        ['scripts/gen_wavedrom.py', 'docs/diagrams/wd_gptp_pdelay.json', '--background=white', '--check'],
        ['scripts/check_diagram_pngs.py'], ['scripts/check_diagram_pngs.py', '--selftest'],
        ['scripts/gen_hdl_reference.py', '--selftest'],
        ['scripts/check_sh_idiom.py'], ['scripts/check_sh_idiom.py', '--selftest'],
    ],
    'parser': [
        ['scripts/gen_hdl_reference.py', '--selftest'],
        ['scripts/gen_hdl_reference.py', '--output', '/tmp/milan-577-hdl-reference'],
    ],
    'reference': [['scripts/gen_hdl_reference.py', '--output', '/tmp/milan-577-hdl-reference']],
    'focused': [[str(OUT / 'check_mutants.py')], [str(OUT / 'check_images.py')]],
}

def main():
    group = sys.argv[1]
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    results = []
    failure = False
    for number, args in enumerate(GROUPS[group], 1):
        env = dict(os.environ)
        args = list(args)
        prefix = ''
        if group == 'reference':
            env.update(GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='core.commitGraph', GIT_CONFIG_VALUE_0='false')
            prefix = 'GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.commitGraph GIT_CONFIG_VALUE_0=false '
        if args[-1] == 'NO_GIT_MODE':
            args.pop()
            env['GIT_DIR'] = '/dev/null'
            prefix = 'GIT_DIR=/dev/null '
        argv = [PYTHON, '-u', *args]
        label = f'{group}-{number:02d}'
        print(f'START {label}: {prefix}{shlex.join(argv)}', flush=True)
        start = time.monotonic()
        with tempfile.TemporaryDirectory(prefix='milan-577-gate-') as tmp:
            log = Path(tmp) / 'stdout.log'
            with log.open('wb') as stream:
                result = subprocess.run(argv, cwd=ROOT, env=env, stdout=stream,
                                        stderr=subprocess.STDOUT, timeout=7200)
            size = log.stat().st_size
            content = log.read_bytes()
            digest = hashlib.sha256(content).hexdigest()
            saved = None
            if size <= 200000:
                saved = label + '.log'
                (OUT / saved).write_bytes(content)
            else:
                tail = content[-12000:].decode(errors='replace')
                (OUT / (label + '-tail.txt')).write_text(tail)
            record = dict(label=label, command=prefix + shlex.join(argv), cwd=str(ROOT),
                          head=head, rc=result.returncode, seconds=round(time.monotonic()-start, 2),
                          bytes=size, sha256=digest, log=saved)
            results.append(record)
            (OUT / (group + '-gates.json')).write_text(json.dumps(results, indent=2) + '\n')
            print(json.dumps(record), flush=True)
            if result.returncode:
                failure = True
                print(content[-8000:].decode(errors='replace'), flush=True)
    return int(failure)

if __name__ == '__main__':
    sys.exit(main())
