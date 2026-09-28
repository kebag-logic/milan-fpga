"""Gate receipts at one committed head; every log and output stays under physical data storage.

Modes:
  pins     the hosted elaborate bank in the pins-only environment (pins_env.sh)
  builder  bench builder banks, RV32 compiler present and absent
  hooks    the #607 shipping-hook/constraint entry and the #395 timing-grade entry, run directly
  live     planted wrong-name control against the read-only shipping checkpoint
  docs     the hosted docs-check job's gates. The Markdown environment's interpreter is first
           on PATH, so `python3` and sys.executable are both that pinned interpreter.
Each command runs directly with stdout/stderr to its own log; nothing is piped.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path('$LANES/607-xdc-clock-names')
out = Path(__file__).resolve().parent
work = Path('$VALIDATION_STORAGE/607-a427')
bench = '$WORKSPACE_HOME/litex-milan/venv/bin/python'
md = Path('$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin')
base = '7390b43627032c71c470e2aa8d0845eb5b740663'  # the merge's dev parent
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
logs = work / ('gates-' + head[:9])
logs.mkdir(parents=True, exist_ok=True)
(work / 'tmp').mkdir(exist_ok=True)
git_env = dict(GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='core.commitGraph', GIT_CONFIG_VALUE_0='false')
clean = {k: v for k, v in os.environ.items() if k not in ('PYTHONPATH', 'MILAN_LITEX_PYTHON', 'VIRTUAL_ENV')}
bench_env = dict(clean, TMPDIR=str(work / 'tmp'), MILAN_LITEX_PYTHON=bench, PYTHONHASHSEED='0', **git_env)
md_env = dict(bench_env, PATH=str(md) + ':' + clean['PATH'])
pins_env = dict(clean, **git_env)
mode = sys.argv[1]
commands = []
if mode == 'pins':
    # Exactly the hosted step: `python3 sw/builder/test_builder.py --require-elaboration --require-rv32`.
    commands = [('pins-bank', ['sh', str(out / 'pins_env.sh'), str(root), str(work), 'python3',
                               'sw/builder/test_builder.py', '--require-elaboration', '--require-rv32'], pins_env)]
elif mode == 'builder':
    commands = [('builder-present', ['python3', '-B', 'sw/builder/test_builder.py', '--require-rv32',
                                     '--require-elaboration'], bench_env),
                ('builder-absent', ['python3', '-B', str(out / 'run_builder_absent.py')], bench_env)]
elif mode == 'hooks':
    commands = [('shipping-hook-bench', [bench, '-B', 'sw/builder/test_clock_constraints.py'], bench_env),
                ('shipping-hook-pins', ['sh', str(out / 'pins_env.sh'), str(root), str(work), 'python3', '-B',
                                        'sw/builder/test_clock_constraints.py'], pins_env),
                ('timing-grade-bench', ['python3', '-B', 'sw/builder/test_timing_grade.py', bench], bench_env),
                ('timing-grade-pins', ['sh', str(out / 'pins_env.sh'), str(root), str(work), 'python3', '-B',
                                       'sw/builder/test_timing_grade.py', 'python3'], pins_env)]
elif mode == 'hdlref':
    # Not Markdown gates: the HDL reference needs the pinned pyslang (tools/hdl_reference/requirements.txt),
    # which the Markdown environment lacks. Rounds 1 and 3 took it from this read-only dependency directory.
    hdl_env = dict(bench_env, PYTHONPATH='$VALIDATION_STORAGE/607-a408-work/docdeps')
    commands = [('gen_hdl_reference-selftest', ['python3', '-B', 'scripts/gen_hdl_reference.py', '--selftest'],
                 hdl_env),
                ('gen_hdl_reference-output', ['python3', '-B', 'scripts/gen_hdl_reference.py', '--output',
                                              str(work / ('hdl-reference-' + head[:9]))], hdl_env)]
elif mode == 'live':
    evidence = work / ('live-plant-' + head[:9])
    commands = [('live-plant', [bench, '-B', 'sw/builder/test_clock_constraints.py',
                                '--vivado', '$WORKSPACE_HOME/Xilinx2/2026.1/Vivado/bin/vivado', '--checkpoint',
                                '$WORKSPACE_HOME/litex-milan/work/build_ax7101_eto_tdm8dev9e9954e9/gateware/'
                                'alinx_ax7101_route.dcp', '--evidence-dir', str(evidence)], bench_env)]
elif mode == 'docs':
    rows = [
        ('scripts/gen_hdl_reference.py', '--selftest'),
        ('scripts/gen_hdl_reference.py', '--output ' + str(work / ('hdl-reference-' + head[:9]))),
        ('scripts/docs_check.py', ''),
        ('scripts/check_em_dash.py', '--base ' + base),
        ('scripts/check_em_dash.py', '--selftest'),
        ('scripts/check_doc_style.py', ''),
        ('scripts/check_doc_style.py', '--selftest'),
        ('scripts/check_gptp_docs.py', ''),
        ('scripts/check_gptp_docs.py', '--selftest'),
        ('docs/DOC_MAP.gen.py', '--check'),
        ('docs/DOC_MAP.gen.py', '--selftest'),
        ('docs/diagrams/timesync_chain.gen.py', '--check'),
        ('docs/diagrams/timesync_chain.gen.py', '--selftest'),
        ('scripts/check_solution_docs.py', ''),
        ('scripts/check_solution_docs.py', '--selftest'),
        ('docs/diagrams/submodule_boundaries.gen.py', '--check'),
        ('docs/diagrams/submodule_boundaries.gen.py', '--selftest'),
        ('scripts/check_submodule_docs.py', ''),
        ('scripts/check_submodule_docs.py', '--selftest'),
        ('scripts/gen_wavedrom.py', '--selftest'),
        ('scripts/gen_wavedrom.py', 'docs/diagrams/wd_axis_backpressure.json --background=white --check'),
        ('scripts/gen_wavedrom.py', 'docs/diagrams/wd_cdc_handshake.json --background=white --check'),
        ('scripts/gen_wavedrom.py', 'docs/diagrams/wd_gptp_pdelay.json --background=white --check'),
        ('scripts/check_diagram_pngs.py', ''),
        ('scripts/check_diagram_pngs.py', '--selftest'),
        ('scripts/check_feature_status.py', '--self-test'),
        ('scripts/check_feature_status.py', ''),
        ('docs/traceability/gen_module_matrix.py', '--check'),
        ('scripts/check_gptp_docs.py', '--with-submodule'),
        ('scripts/measure_control_flow.py', '--selftest'),
        ('scripts/measure_cohesion.py', '--selftest'),
        ('scripts/check_baremetal_only.py', '--check'),
        ('scripts/check_baremetal_only.py', '--selftest'),
        ('sw/builder/test_firmware_compiler.py', '--selftest'),
        ('sw/builder/test_firmware_compiler.py', '--absent --audit ' + str(work / ('firmware-absent-' + head[:9]
                                                                                  + '.jsonl'))),
        ('scripts/check_nvm_record_space.py', ''),
        ('scripts/check_nvm_record_space.py', '--self-test'),
        ('scripts/check_nvm_capture.py', ''),
        ('sw/firmware/nvm_hosttest/test_nvm_firmware.py', '--self-test'),
        ('scripts/check_soc_sources.py', ''),
        ('scripts/check_soc_sources.py', '--selftest'),
        ('sw/litex/iob_pack_selftest.py', ''),
        ('scripts/check_rtl_source_lists.py', ''),
        ('scripts/check_rtl_source_lists.py', '--selftest'),
        ('scripts/measure_naming.py', '--check'),
        ('scripts/measure_naming.py', '--selftest'),
        ('scripts/check_port_contracts.py', ''),
        ('scripts/check_port_contracts.py', '--selftest'),
        ('scripts/measure_fail_fast.py', '--check'),
        ('scripts/measure_fail_fast.py', '--selftest'),
        ('scripts/check_todo_ownership.py', ''),
        ('scripts/check_todo_ownership.py', '--selftest'),
        ('scripts/measure_test_evidence.py', '--check'),
        ('scripts/measure_test_evidence.py', '--selftest'),
        ('scripts/check_hygiene.py', '--check'),
        ('scripts/check_hygiene.py', '--selftest'),
        ('scripts/check_sv_idiom.py', ''),
        ('scripts/check_sv_idiom.py', '--selftest'),
        ('scripts/check_cpp_idiom.py', ''),
        ('scripts/check_cpp_idiom.py', '--selftest'),
        ('scripts/check_py_idiom.py', ''),
        ('scripts/check_py_idiom.py', '--selftest'),
        ('scripts/check_sh_idiom.py', ''),
        ('scripts/check_sh_idiom.py', '--selftest'),
        ('scripts/ci_events.py', '--check'),
        ('scripts/ci_events.py', '--selftest'),
        ('scripts/check_doc_paths.py', ''),
        ('scripts/check_archive.py', ''),
        ('scripts/check_archive.py', '--selftest'),
        ('scripts/gen_toc.py', '--selftest'),
        ('scripts/gen_toc.py', '--verify-anchors'),
        ('scripts/gen_toc.py', '--check'),
        ('avdecc/gen_aem_store.py', '--self-test'),
        ('scripts/check_sweep_shape.py', '--self-test'),
        ('scripts/check_deploy_shape.py', '--self-test'),
        ('scripts/check_entity_shape.py', '--self-test'),
        ('scripts/check_wire_accountability.py', '--self-test'),
    ]
    seen = set()
    for path, args in rows:
        label = Path(path).stem + ('-' + Path(args.split()[0]).name.lstrip('-') if args else '')
        assert label not in seen, label
        seen.add(label)
        commands.append((label, ['python3', '-B', path, *args.split()], md_env))
    commands += [('gptp-docs', ['make', '-C', 'gptp-processor', 'docs'], md_env),
                 ('git-diff-worktree', ['git', 'diff', '--check'], md_env),
                 ('git-diff-committed', ['git', 'diff', '--check', base, 'HEAD'], md_env)]
receipt = out / ('gate-results-' + head[:9] + '-' + mode + '.json')
results = json.loads(receipt.read_text()) if receipt.exists() else []
# Resume after an interruption: keep only verified rc-0 receipts from this head.
results = [row for row in results if row['head'] == head and row['rc'] == 0 and Path(row['log']).exists()
           and hashlib.sha256(Path(row['log']).read_bytes()).hexdigest() == row['sha256']]
done = {row['name'] for row in results}
failed = False
for label, command, env in commands:
    if label in done:
        print('KEEP', label, flush=True)
        continue
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip() == head
    log = logs / (label + '.log')
    start = time.monotonic()
    print('START', label, time.strftime('%H:%M:%S'), flush=True)
    with log.open('w') as stream:
        result = subprocess.run(command, cwd=root, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=7200)
    row = dict(name=label, head=head, command=command, rc=result.returncode,
               elapsed_s=round(time.monotonic() - start, 2), log=str(log), size=log.stat().st_size,
               sha256=hashlib.sha256(log.read_bytes()).hexdigest())
    results.append(row)
    receipt.write_text(json.dumps(results, indent=2) + '\n')
    print('FINISH', label, 'rc=' + str(result.returncode), 'seconds=' + str(row['elapsed_s']), flush=True)
    failed |= result.returncode != 0
status = subprocess.run(['git', 'status', '--porcelain'], cwd=root, capture_output=True, text=True,
                        env=dict(clean, **git_env)).stdout
print('WORKTREE', 'clean' if not status.strip() else status, flush=True)
print('MODE', mode, 'rc=' + str(int(failed)), flush=True)
sys.exit(int(failed))
