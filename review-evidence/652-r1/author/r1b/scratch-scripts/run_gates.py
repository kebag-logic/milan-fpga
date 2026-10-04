"""Run named gates one after another, each unpiped into its own log, recording rc and seconds."""
import json, os, subprocess, sys, time
from pathlib import Path
LANE = "$LANES/652-builder-names"
MDPY = "$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3"
PY = sys.executable
SETS = {
 "readonly": [
  ("docs_check", [PY, "scripts/docs_check.py"]),
  ("em_dash", [MDPY, "scripts/check_em_dash.py", "--base", "6c22d3ca"]),
  ("doc_style", [PY, "scripts/check_doc_style.py"]),
  ("doc_style_self", [PY, "scripts/check_doc_style.py", "--selftest"]),
  ("toc_self", [MDPY, "scripts/gen_toc.py", "--selftest"]),
  ("toc_anchors", [MDPY, "scripts/gen_toc.py", "--verify-anchors"]),
  ("toc_check", [MDPY, "scripts/gen_toc.py", "--check"]),
  ("doc_paths", [PY, "scripts/check_doc_paths.py"]),
  ("archive", [PY, "scripts/check_archive.py"]),
  ("feature_status", [PY, "scripts/check_feature_status.py", "--self-test"]),
  ("module_matrix", [PY, "docs/traceability/gen_module_matrix.py", "--check"]),
  ("solution_docs", [PY, "scripts/check_solution_docs.py"]),
  ("solution_docs_self", [PY, "scripts/check_solution_docs.py", "--selftest"]),
  ("doc_map", [PY, "docs/DOC_MAP.gen.py", "--check"]),
  ("baremetal_only", [PY, "scripts/check_baremetal_only.py", "--check"]),
  ("py_idiom", [PY, "scripts/check_py_idiom.py"]),
  ("py_idiom_self", [PY, "scripts/check_py_idiom.py", "--selftest"]),
  ("sv_idiom", [PY, "scripts/check_sv_idiom.py"]),
  ("hygiene", [PY, "scripts/check_hygiene.py", "--check"]),
  ("fail_fast", [PY, "scripts/measure_fail_fast.py", "--check"]),
  ("port_contracts", [PY, "scripts/check_port_contracts.py"]),
  ("naming", [PY, "scripts/measure_naming.py", "--check"]),
  ("todo", [PY, "scripts/check_todo_ownership.py"]),
  ("test_evidence", [PY, "scripts/measure_test_evidence.py", "--check"]),
  ("lint_rtl", [PY, "scripts/lint_rtl.py", "--check"]),
  ("soc_sources", [PY, "scripts/check_soc_sources.py"]),
  ("soc_sources_self", [PY, "scripts/check_soc_sources.py", "--selftest"]),
  ("rtl_lists", [PY, "scripts/check_rtl_source_lists.py"]),
  ("resmap_sweep_self", [PY, "syn/resmap/yosys_sweep.py", "--selftest"]),
  ("resmap_models_self", [PY, "syn/resmap/resmap_models.py", "--selftest"]),
  ("resmap_tables_self", [PY, "syn/resmap/resmap_tables.py", "--selftest"]),
  ("resmap_map_self", [PY, "syn/resmap/resmap_map.py", "--selftest"]),
  ("resmap_soc_self", [PY, "syn/resmap/soc_sweep.py", "--selftest"]),
 ],
 "bank": [
  ("builder_bank", [PY, "sw/builder/test_builder.py", "--require-rv32"]),
 ],
 "builder_consumers": [
  ("nvm_space", [PY, "scripts/check_nvm_record_space.py"]),
  ("nvm_space_self", [PY, "scripts/check_nvm_record_space.py", "--self-test"]),
  ("nvm_capture", [PY, "scripts/check_nvm_capture.py"]),
  ("nvm_fw_self", [PY, "sw/firmware/nvm_hosttest/test_nvm_firmware.py", "--self-test"]),
  ("entity_shape", [PY, "scripts/check_entity_shape.py", "--self-test"]),
  ("sweep_shape", [PY, "scripts/check_sweep_shape.py", "--self-test"]),
  ("deploy_shape", [PY, "scripts/check_deploy_shape.py", "--self-test"]),
  ("wire_acc", [PY, "scripts/check_wire_accountability.py", "--self-test"]),
  ("aem_store_self", [PY, "avdecc/gen_aem_store.py", "--self-test"]),
 ],
 "suites": [(s, ["make", "-j16", "-C", f"tb/verilator/{s}"]) for s in
            ("nvm_backend", "nvm_cosim", "nvm_capture_cpu", "fw_service_budget")],
}
which = sys.argv[1]
out = Path(f"/tmp/652-a533/r1b/final/{which}")
out.mkdir(parents=True, exist_ok=True)
env = {**os.environ, "PATH": "$VALIDATION_TOOLS/pinned-verilator-5.050:" + os.environ["PATH"],
       "PYTHONDONTWRITEBYTECODE": "1"}
head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=LANE, capture_output=True, text=True).stdout.strip()
results = []
for name, argv in SETS[which]:
    t = time.time()
    with open(out / f"{name}.log", "w") as log:
        rc = subprocess.run(argv, cwd=LANE, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
    secs = round(time.time() - t, 1)
    (out / f"{name}.rc").write_text(f"{rc}\n")
    results.append({"gate": name, "argv": argv, "rc": rc, "seconds": secs})
    print(f"{name}: rc={rc} {secs}s", flush=True)
(out / "results.json").write_text(json.dumps({"head": head, "results": results}, indent=1) + "\n")
print(f"{which}: {sum(r['rc'] == 0 for r in results)}/{len(results)} rc 0 at {head}")
