"""Rebuild round 4's gate table with this round's rc and last log line.
Usage: python3 -I gate_table.py <r4 HANDOFF.md> <logs dir> <old scratch> <new scratch>"""
import sys
from pathlib import Path

r4, logs, old, new = sys.argv[1:5]
ids = ["wire_accountability", "nogit_docs_check", "gate_1_hdl_reference", "gate_7_docs_check",
       "gate_8_em_dash", "gate_9_style", "gate_10_diagram_nodrift", "gate_11_solution",
       "gate_12_submodule_docs", "gate_13_wavedrom", "gate_14_pngs", "gate_15_feature",
       "gate_16_traceability", "gate_18_gptp_submodule", "gate_19_measure_selftests",
       "gate_21_baremetal", "rv32_sdk_ci", "gate_24_fw_compiler_sdk", "gate_26_nvm_record_space",
       "gate_27_nvm_capture", "gate_28_nvm_writer", "gate_29_soc_sources", "gate_30_rtl_source_lists",
       "gate_31_naming", "gate_32_port_contracts", "gate_33_fail_fast", "gate_34_todo",
       "gate_35_test_evidence", "gate_36_hygiene", "gate_37_sv_idiom", "gate_38_cpp_idiom",
       "gate_39_py_idiom", "gate_40_sh_idiom", "gate_43_doc_paths", "gate_44_archive", "gate_45_toc",
       "gate_46_aem_store", "gate_47_sweep_shape", "gate_48_deploy_shape", "gate_49_entity_shape",
       "gate_50_ci_controls", "gate_25_0_builder", "gate_25_1_builder", "gate_41_ci_events",
       "gate_42_act_runner", "md818_docs_check", "md818_em_dash", "md818_doc_style", "md818_toc",
       "diff_check", "style_touched", "reader_check_baseline", "reader_service_bounds",
       "census_coverage", "census_coverage_control"]
text = Path(r4).read_text(encoding="utf-8").splitlines()
start = text.index("| Job | Step | Command | rc | Last line |")
rows = []
for line in text[start + 2:]:
    if not line.startswith("|"):
        break
    rows.append(line)
assert len(rows) == len(ids), (len(rows), len(ids))
print(text[start]); print(text[start + 1])
bad = 0
for row, i in zip(rows, ids):
    cells = row.split(" | ")
    rc = Path(logs, i + ".rc").read_text().strip()
    bad += rc != "0"
    log = Path(logs, i + ".log").read_text(encoding="utf-8", errors="replace").splitlines()
    last = log[-1].replace("|", "/") if log else ""
    if i == "reader_service_bounds" and not log:
        last = "rc 0"
    if i == "style_touched":
        cells = [c.replace("d52e966b", "545ac9cb") for c in cells]
    last = last.replace(old, new)
    print(" | ".join(cells[:3] + [rc, last + " |"]))
print(f"\n{len(ids)} rc files; non-zero: {bad}", file=sys.stderr)
