#!/usr/bin/env python3
"""Run S2's round-5 gate set at the S2c checkout's head, one log per gate with its rc on the
last line, and a summary table: the docs workflow's check-mode commands, the bare-metal scope
gate, the harness self-test, whitespace and rtl-fast's bdd-conformance, with S2c's CPU option
test (test_soc_options.py) added beside the end-station builder gate. Copied from S2's
gates_r5.py; this docstring, the added gates (test_soc_options.py; test_ctrl_memory.py, which
reads SPLIT_CONTROL_MEMORY.md; rtl-fast's firmware-boundary and publication-census steps), the
base (the PR's base after round 3's merge, dev-soft-core 1a635a4c) and GATE_SKIP differ.

Usage: gates_s2c.py CHECKOUT PYTHON OUT_DIR SCRATCH [NAME...]
PYTHON is the interpreter with the pinned Markdown renderer (tools/markdown/requirements.txt),
PyYAML and the docs workflow's wavedrom pin. NAME selects gates; default every gate. The gates run
one at a time, and the tree must be clean before and after each (git status --porcelain, every
untracked file and submodule included): several gates plant a defect in the checkout and restore
it, so none may overlap another. Environment: GATE_HDL_PYTHON, the interpreter with
tools/hdl_reference/requirements.txt; GATE_BUILDER_PATH, the PATH prefix with the product LiteX
environment and the pinned RV32 SDK for the end-station builder gate.
"""
import os
import subprocess
import sys
import time
from pathlib import Path

checkout, python, out, scratch = (Path(a) for a in sys.argv[1:5])
wanted = set(sys.argv[5:])
#: Gates skipped by name (GATE_SKIP, space-separated); the summary names them.
skip = set(os.environ.get('GATE_SKIP', '').split())
BASE = '1a635a4cf9dce5095be624f0265fc1002a60ec59'
P = str(python)
GATES = [
    ('harness_selftest', [P, '-B', 'tb/verilator/ctrl_service_budget/run.py', '--self-test'], '.'),
    ('baremetal_check', [P, 'scripts/check_baremetal_only.py', '--check'], '.'),
    ('baremetal_selftest', [P, 'scripts/check_baremetal_only.py', '--selftest'], '.'),
    ('wire_accountability_selftest', [P, 'scripts/check_wire_accountability.py', '--self-test'], '.'),
    ('docs_check', [P, 'scripts/docs_check.py'], '.'),
    ('feature_status', [P, 'scripts/check_feature_status.py'], '.'),
    ('feature_status_selftest', [P, 'scripts/check_feature_status.py', '--self-test'], '.'),
    ('traceability_matrix', [P, 'docs/traceability/gen_module_matrix.py', '--check'], '.'),
    ('em_dash', [P, 'scripts/check_em_dash.py', '--base', BASE], '.'),
    ('em_dash_selftest', [P, 'scripts/check_em_dash.py', '--selftest'], '.'),
    ('doc_style', [P, 'scripts/check_doc_style.py'], '.'),
    ('doc_style_selftest', [P, 'scripts/check_doc_style.py', '--selftest'], '.'),
    ('gptp_docs', [P, 'scripts/check_gptp_docs.py'], '.'),
    ('gptp_docs_selftest', [P, 'scripts/check_gptp_docs.py', '--selftest'], '.'),
    ('gptp_docs_with_submodule', [P, 'scripts/check_gptp_docs.py', '--with-submodule'], '.'),
    ('gptp_processor_docs', ['make', '-C', 'gptp-processor', 'docs', f'PYTHON={P}'], '.'),
    ('doc_map', [P, 'docs/DOC_MAP.gen.py', '--check'], '.'),
    ('doc_map_selftest', [P, 'docs/DOC_MAP.gen.py', '--selftest'], '.'),
    ('timesync_chain', [P, 'docs/diagrams/timesync_chain.gen.py', '--check'], '.'),
    ('timesync_chain_selftest', [P, 'docs/diagrams/timesync_chain.gen.py', '--selftest'], '.'),
    ('solution_docs', [P, 'scripts/check_solution_docs.py'], '.'),
    ('solution_docs_selftest', [P, 'scripts/check_solution_docs.py', '--selftest'], '.'),
    ('submodule_boundaries', [P, 'docs/diagrams/submodule_boundaries.gen.py', '--check'], '.'),
    ('submodule_boundaries_selftest', [P, 'docs/diagrams/submodule_boundaries.gen.py', '--selftest'], '.'),
    ('submodule_docs', [P, 'scripts/check_submodule_docs.py'], '.'),
    ('submodule_docs_selftest', [P, 'scripts/check_submodule_docs.py', '--selftest'], '.'),
    ('wavedrom_selftest', [P, 'scripts/gen_wavedrom.py', '--selftest'], '.'),
    *[(f'wavedrom_{d}', [P, 'scripts/gen_wavedrom.py', f'docs/diagrams/wd_{d}.json', '--background=white', '--check'],
       '.') for d in ('axis_backpressure', 'cdc_handshake', 'gptp_pdelay')],
    ('diagram_pngs', [P, 'scripts/check_diagram_pngs.py'], '.'),
    ('diagram_pngs_selftest', [P, 'scripts/check_diagram_pngs.py', '--selftest'], '.'),
    ('control_flow_selftest', [P, 'scripts/measure_control_flow.py', '--selftest'], '.'),
    ('cohesion_selftest', [P, 'scripts/measure_cohesion.py', '--selftest'], '.'),
    ('rv32_sdk_selftest', [P, 'scripts/ci_rv32_sdk_selftest.py'], '.'),
    ('firmware_compiler_selftest', [P, 'sw/builder/test_firmware_compiler.py', '--selftest'], '.'),
    ('firmware_compiler_absent', [P, 'sw/builder/test_firmware_compiler.py', '--absent', '--audit',
                                  str(scratch / 'rv32-absent.jsonl')], '.'),
    ('nvm_record_space', [P, 'scripts/check_nvm_record_space.py'], '.'),
    ('nvm_record_space_selftest', [P, 'scripts/check_nvm_record_space.py', '--self-test'], '.'),
    ('nvm_capture', [P, 'scripts/check_nvm_capture.py'], '.'),
    ('nvm_firmware_selftest', [P, 'sw/firmware/nvm_hosttest/test_nvm_firmware.py', '--self-test'], '.'),
    ('soc_sources', [P, 'scripts/check_soc_sources.py'], '.'),
    ('soc_sources_selftest', [P, 'scripts/check_soc_sources.py', '--selftest'], '.'),
    ('iob_pack_selftest', [P, 'sw/litex/iob_pack_selftest.py'], '.'),
    ('rtl_source_lists', [P, 'scripts/check_rtl_source_lists.py'], '.'),
    ('rtl_source_lists_selftest', [P, 'scripts/check_rtl_source_lists.py', '--selftest'], '.'),
    ('naming', [P, 'scripts/measure_naming.py', '--check'], '.'),
    ('naming_selftest', [P, 'scripts/measure_naming.py', '--selftest'], '.'),
    ('port_contracts', [P, 'scripts/check_port_contracts.py'], '.'),
    ('port_contracts_selftest', [P, 'scripts/check_port_contracts.py', '--selftest'], '.'),
    ('fail_fast', [P, 'scripts/measure_fail_fast.py', '--check'], '.'),
    ('fail_fast_selftest', [P, 'scripts/measure_fail_fast.py', '--selftest'], '.'),
    ('todo_ownership', [P, 'scripts/check_todo_ownership.py'], '.'),
    ('todo_ownership_selftest', [P, 'scripts/check_todo_ownership.py', '--selftest'], '.'),
    ('test_evidence', [P, 'scripts/measure_test_evidence.py', '--check'], '.'),
    ('test_evidence_selftest', [P, 'scripts/measure_test_evidence.py', '--selftest'], '.'),
    ('hygiene', [P, 'scripts/check_hygiene.py', '--check'], '.'),
    ('hygiene_selftest', [P, 'scripts/check_hygiene.py', '--selftest'], '.'),
    ('sv_idiom', [P, 'scripts/check_sv_idiom.py'], '.'),
    ('sv_idiom_selftest', [P, 'scripts/check_sv_idiom.py', '--selftest'], '.'),
    ('cpp_idiom', [P, 'scripts/check_cpp_idiom.py'], '.'),
    ('cpp_idiom_selftest', [P, 'scripts/check_cpp_idiom.py', '--selftest'], '.'),
    ('py_idiom', [P, 'scripts/check_py_idiom.py'], '.'),
    ('py_idiom_selftest', [P, 'scripts/check_py_idiom.py', '--selftest'], '.'),
    ('sh_idiom', [P, 'scripts/check_sh_idiom.py'], '.'),
    ('sh_idiom_selftest', [P, 'scripts/check_sh_idiom.py', '--selftest'], '.'),
    ('doc_paths', [P, 'scripts/check_doc_paths.py'], '.'),
    ('archive', [P, 'scripts/check_archive.py'], '.'),
    ('archive_selftest', [P, 'scripts/check_archive.py', '--selftest'], '.'),
    ('toc_selftest', [P, 'scripts/gen_toc.py', '--selftest'], '.'),
    ('toc_verify_anchors', [P, 'scripts/gen_toc.py', '--verify-anchors'], '.'),
    ('toc_check', [P, 'scripts/gen_toc.py', '--check'], '.'),
    ('aem_store_selftest', [P, 'avdecc/gen_aem_store.py', '--self-test'], '.'),
    ('sweep_shape_selftest', [P, 'scripts/check_sweep_shape.py', '--self-test'], '.'),
    ('deploy_shape_selftest', [P, 'scripts/check_deploy_shape.py', '--self-test'], '.'),
    ('entity_shape_selftest', [P, 'scripts/check_entity_shape.py', '--self-test'], '.'),
    ('gate_workflows', [P, 'scripts/ci_gate_workflows.py', '--check'], '.'),
    *[(name.replace('ci_', '').replace('_selftest', '') + '_selftest', [P, f'scripts/{name}.py'], '.')
      for name in ('ci_gate_workflows_selftest', 'ci_case_receipts_selftest', 'ci_make_cases_selftest',
                   'ci_maap_cases_selftest', 'ci_capture_cases_selftest', 'ci_suite_pieces_selftest',
                   'ci_suite_collect_selftest', 'ci_fail_fast_selftest', 'ci_install_cache_selftest',
                   'ci_workflow_plan_selftest', 'ci_manifest_selftest')],
    ('evidence_pins', [P, 'scripts/generate_ci_evidence_pins.py', '--check'], '.'),
    ('ci_events', [P, 'scripts/ci_events.py', '--check'], '.'),
    ('ci_events_selftest', [P, 'scripts/ci_events.py', '--selftest'], '.'),
    ('git_diff_check', ['git', 'diff', '--check', BASE, 'HEAD'], '.'),
    ('bdd_conformance', ['behave'], 'tests'),
    ('hdl_reference_selftest', [os.environ['GATE_HDL_PYTHON'], 'scripts/gen_hdl_reference.py', '--selftest'], '.'),
    ('hdl_reference', [os.environ['GATE_HDL_PYTHON'], 'scripts/gen_hdl_reference.py', '--output',
                       str(scratch / 'milan-hdl-reference')], '.'),
    ('soc_options', ['python3', 'sw/builder/test_soc_options.py'], '.'),
    ('ctrl_memory', ['python3', 'sw/litex/test_ctrl_memory.py'], '.'),
    ('builder_require_rv32', ['python3', 'sw/builder/test_builder.py', '--require-rv32'], '.'),
    # rtl-fast's firmware-boundary step, with the product LiteX pins and the pinned RV32 SDK
    ('firmware_boundary', ['python3', 'sw/firmware/ctrl/test/ctrl_boundary.py', '--require-rv32', '--selftest',
                           '--without', 'verilator'], '.'),
    # rtl-fast's publication-census step, with the pinned Yosys and sv2v 0.0.12
    ('publication_census', [P, 'sw/mailbox/publication_census.py', '--check', '--selftest', '--jobs',
                            os.environ.get('GATE_CENSUS_JOBS', '4')], '.'),
]
#: The end-station builder gate runs python3 from the product LiteX environment, with the SDK.
_BUILDER = dict(os.environ, PATH=os.environ['GATE_BUILDER_PATH'] + ':' + os.environ['PATH'], PYTHONUNBUFFERED='1')
#: The census runs sv2v from GATE_SV2V_DIR (the pinned 0.0.12) ahead of any other.
_CENSUS = dict(os.environ, PATH=os.environ.get('GATE_SV2V_DIR', '') + ':' + os.environ['PATH'])
ENV = {'builder_require_rv32': _BUILDER, 'soc_options': _BUILDER, 'ctrl_memory': _BUILDER,
       'firmware_boundary': _BUILDER, 'publication_census': _CENSUS}


def dirty() -> str:
    """The checkout's changes, untracked files and submodule changes included; '' when clean."""
    return subprocess.run(['git', 'status', '--porcelain', '--untracked-files=all', '--ignore-submodules=none'],
                          cwd=checkout, capture_output=True, text=True, check=True).stdout

out.mkdir(parents=True, exist_ok=True)
head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=checkout, capture_output=True, text=True).stdout.strip()
(out / 'HEAD.txt').write_text(head + '\n')
rows = []
if dirty():
    raise SystemExit(f'the checkout is not clean before the gates:\n{dirty()}')
for name, argv, cwd in GATES:
    if (wanted and name not in wanted) or name in skip:
        continue
    log = out / f'{name}.log'
    t0 = time.monotonic()
    with log.open('w') as sink:
        sink.write(f'$ (cd {cwd}) {" ".join(a if a != P else "python3" for a in argv)}\n')
        sink.flush()
        rc = subprocess.run(argv, cwd=checkout / cwd, stdout=sink, stderr=subprocess.STDOUT,
                            env=ENV.get(name)).returncode
    left = dirty()
    with log.open('a') as sink:
        sink.write(f'rc={rc}\n' + (f'TREE LEFT DIRTY:\n{left}' if left else 'tree clean after the gate\n'))
    rows.append((name, rc, time.monotonic() - t0, 'clean' if not left else 'DIRTY'))
    print(f'{name} rc={rc} ({rows[-1][2]:.1f} s) tree {rows[-1][3]}', flush=True)
    if left:
        break
lines = [f'head {head}', '', '| Gate | rc | s | Tree after |', '|---|---:|---:|---|',
         *[f'| {n} | {rc} | {s:.1f} | {c} |' for n, rc, s, c in rows],
         *([f'', f'skipped by name: {" ".join(sorted(skip))}'] if skip else []),
         '', f'{sum(1 for _, rc, _, c in rows if rc or c != "clean")} of {len(rows)} gates nonzero or left the tree dirty']
(out / ('summary.md' if not wanted else 'summary-partial.md')).write_text('\n'.join(lines) + '\n')
print(lines[-1])
