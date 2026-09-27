"""Run the documentation and touched-language gates, preserving every status."""
import json
from pathlib import Path
import subprocess
import sys

root = Path.cwd().resolve()
logs = Path("/tmp/582-a370-validation/docs")
logs.mkdir(parents=True, exist_ok=True)
commands = [
    ["scripts/docs_check.py"],
    ["scripts/check_em_dash.py", "--base", "9e9954e96bf55181edb9949ae94c9abd4ab6aaf5"],
    ["scripts/check_doc_style.py"],
    ["scripts/check_doc_paths.py"],
    ["scripts/check_archive.py"],
    ["scripts/check_archive.py", "--selftest"],
    ["scripts/gen_toc.py", "--selftest"],
    ["scripts/gen_toc.py", "--verify-anchors"],
    ["scripts/gen_toc.py", "--check"],
    ["scripts/check_feature_status.py", "--self-test"],
    ["scripts/check_solution_docs.py"],
    ["scripts/check_solution_docs.py", "--selftest"],
    ["scripts/check_submodule_docs.py"],
    ["scripts/check_submodule_docs.py", "--selftest"],
    ["scripts/check_gptp_docs.py", "--with-submodule"],
    ["docs/traceability/gen_module_matrix.py", "--check"],
    ["scripts/check_baremetal_only.py", "--check"],
    ["scripts/check_baremetal_only.py", "--selftest"],
    ["scripts/check_soc_sources.py"],
    ["scripts/check_soc_sources.py", "--selftest"],
    ["scripts/check_rtl_source_lists.py"],
    ["scripts/check_rtl_source_lists.py", "--selftest"],
    ["scripts/check_hygiene.py", "--check"],
    ["scripts/check_hygiene.py", "--selftest"],
    ["scripts/check_py_idiom.py"],
    ["scripts/check_py_idiom.py", "--selftest"],
    ["scripts/check_sh_idiom.py"],
    ["scripts/check_sh_idiom.py", "--selftest"],
    ["scripts/check_sweep_shape.py", "--self-test"],
    ["scripts/check_deploy_shape.py", "--self-test"],
    ["scripts/check_entity_shape.py", "--self-test"],
]
results = []
for index, args in enumerate(commands):
    log = logs / f"{index:02}-{Path(args[0]).stem}.log"
    with log.open("w") as stream:
        result = subprocess.run([sys.executable, *args], cwd=root, stdout=stream,
                                stderr=subprocess.STDOUT, timeout=600)
    results.append({"argv": [sys.executable, *args], "returncode": result.returncode, "log": str(log)})
    print(f"rc {result.returncode}: {' '.join(args)}", flush=True)
    if result.returncode:
        print(log.read_text()[-6000:], flush=True)
Path(__file__).with_name("docs-results.json").write_text(json.dumps(results, indent=2) + "\n")
sys.exit(1 if any(r["returncode"] for r in results) else 0)
