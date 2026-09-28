"""Run committed-head parent validation commands in the foreground."""
from pathlib import Path
import subprocess
import sys

out = Path(__file__).resolve().parent
md_python = "$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python"
commands = [
    ("final-cpp", ["python3", "scripts/check_cpp_idiom.py"]),
    ("final-py", ["python3", "scripts/check_py_idiom.py"]),
    ("final-xvlog", ["python3", "scripts/xvlog_gate.py", "--check"]),
    ("final-source-lists", ["python3", "scripts/check_rtl_source_lists.py"]),
    ("final-pp-sources", ["python3", "scripts/pp_srcs.py", "--check", "--selftest"]),
    ("final-builder", ["python3", "sw/builder/test_builder.py", "--require-elaboration", "--require-rv32"]),
    ("final-shadow", ["make", "-C", "tb/verilator/pp_shadow", "-j8"]),
    ("final-port-contracts", ["python3", "scripts/check_port_contracts.py"]),
    ("final-naming", ["python3", "scripts/measure_naming.py", "--check"]),
    ("final-evidence", ["python3", "scripts/measure_test_evidence.py", "--check"]),
    ("final-docs", [md_python, "scripts/docs_check.py"]),
    ("final-soc-import", ["python3", "-c", "import sys; sys.path.insert(0, 'sw/litex'); import milan_soc"]),
    ("final-aem", ["python3", "avdecc/gen_aem_store.py", "--self-test"]),
    ("final-soc-sources", ["python3", "scripts/check_soc_sources.py"]),
    ("final-sweep-shape", ["python3", "scripts/check_sweep_shape.py", "--self-test"]),
    ("final-deploy-shape", ["python3", "scripts/check_deploy_shape.py", "--selftest"]),
    ("final-iob", ["python3", "sw/litex/iob_pack_selftest.py"]),
    ("final-capture", ["python3", "scripts/check_nvm_capture.py"]),
    ("final-submodule-docs", ["python3", "scripts/check_submodule_docs.py"]),
    ("final-boundary-diagram", ["python3", "docs/diagrams/submodule_boundaries.gen.py", "--check"]),
    ("final-toc", [md_python, "scripts/gen_toc.py", "--check"]),
    ("final-first", ["make", "-C", "tb/verilator/pp_shadow", "run-crf", "SIM_ARGS=--first-probe-only", "-j8"]),
    ("final-crf", ["make", "-C", "tb/verilator/pp_shadow", "run-crf", "SIM_ARGS=--crf-stop-only", "-j8"]),
]
failed = []
for name, command in commands:
    print("START " + name, flush=True)
    result = subprocess.run([sys.executable, str(out / "run_gate.py"), name, *command],
                            timeout=15000, check=False)
    if result.returncode:
        failed.append(name)
print("FAILED: " + repr(failed), flush=True)
raise SystemExit(bool(failed))
