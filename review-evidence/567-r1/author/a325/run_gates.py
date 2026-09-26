from pathlib import Path
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time

root = Path("$LANES/567-pp-pin-0922e434")
out = Path(__file__).resolve().parent
mode = sys.argv[1]
env = dict(os.environ)
env["PATH"] = "/tmp/567-a325-venv/bin:" + env["PATH"]
groups = {
 "builder": [
  ("builder-sdk", ["python3", str(out / "builder_modes.py"), "sdk"]),
  ("builder-absent", ["python3", str(out / "builder_modes.py"), "absent"]),
 ],
 "gates": [
  ("parameter-inventory", ["python3", "protocol-processor/scripts/check-integrator-params.py"]),
  ("nvm-firmware", ["python3", "sw/firmware/nvm_hosttest/test_nvm_firmware.py", "--self-test"]),
  ("nvm-capture", ["python3", "scripts/check_nvm_capture.py"]),
  ("baremetal-only", ["python3", "scripts/check_baremetal_only.py", "--check"]),
  ("docs-check", ["python3", "-B", "scripts/docs_check.py"]),
  ("ci-events-check", ["python3", "scripts/ci_events.py", "--check"]),
  ("ci-events-selftest", ["python3", "scripts/ci_events.py", "--selftest"]),
  ("em-dash", ["python3", "scripts/check_em_dash.py", "--base", "7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a"]),
  ("doc-style", ["python3", "scripts/check_doc_style.py"]),
  ("toc-check", ["python3", "scripts/gen_toc.py", "--check"]),
  ("toc-anchors", ["python3", "scripts/gen_toc.py", "--verify-anchors"]),
  ("doc-paths", ["python3", "scripts/check_doc_paths.py"]),
  ("module-matrix", ["python3", "docs/traceability/gen_module_matrix.py", "--check"]),
  ("xvlog", ["python3", "scripts/xvlog_gate.py", "--check"]),
  ("rtl-source-lists", ["python3", "scripts/check_rtl_source_lists.py"]),
  ("sv-idiom", ["python3", "scripts/check_sv_idiom.py"]),
  ("rtl-lint", ["python3", "scripts/lint_rtl.py", "--check"]),
  ("cpp-idiom", ["python3", "scripts/check_cpp_idiom.py"]),
  ("py-idiom", ["python3", "scripts/check_py_idiom.py"]),
  ("port-contracts", ["python3", "scripts/check_port_contracts.py"]),
  ("naming", ["python3", "scripts/measure_naming.py", "--check"]),
  ("test-evidence", ["python3", "scripts/measure_test_evidence.py", "--check"]),
  ("behave", ["behave", "--no-capture", "-f", "plain"]),
  ("diff-check", ["git", "diff", "--check"]),
  ("submodule-docs", ["python3", "scripts/check_submodule_docs.py"]),
  ("submodule-diagram", ["python3", "docs/diagrams/submodule_boundaries.gen.py", "--check"]),
  ("diagram-pngs", ["python3", "scripts/check_diagram_pngs.py"]),
 ],
 "no-git": [("docs-check-no-git", ["python3", "-B", "scripts/docs_check.py"])],
}
groups["docs-final"] = [(gate, command) for gate, command in groups["gates"] if gate in {"docs-check", "em-dash", "doc-style", "toc-check", "toc-anchors", "doc-paths", "diff-check", "submodule-docs"}]
results = []
with tempfile.TemporaryDirectory(prefix="567-a325-docs-no-git-") as temp:
    base = root
    if mode == "no-git":
        base = Path(temp)
        listing = subprocess.run(["rtk", "proxy", "git", "ls-files", "-z"], cwd=root, check=True, capture_output=True).stdout
        for name in listing.decode().split("\0"):
            if not name:
                continue
            source = root / name
            if source.is_file():
                target = base / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
            elif source.is_dir():
                (base / name).mkdir(parents=True, exist_ok=True)
        assert not (base / ".git").exists()
    for gate, command in groups[mode]:
        print("START", gate, flush=True)
        start = time.monotonic()
        cwd = base / "tests" if gate == "behave" else base
        with (out / (gate + ".log")).open("w") as log:
            try:
                result = subprocess.run(["rtk", "proxy", *command], cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=14400)
                rc = result.returncode
            except subprocess.TimeoutExpired:
                rc = 124
        row = dict(gate=gate, command=shlex.join(command), rc=rc, seconds=round(time.monotonic()-start, 2), log=gate + ".log")
        results.append(row)
        (out / (mode + "-results.json")).write_text(json.dumps(results, indent=2) + "\n")
        print("END", gate, "rc=" + str(rc), flush=True)
        with (out / "HANDOFF.md").open("a") as handoff:
            handoff.write("\nGate update: `" + gate + "` rc " + str(rc) + "; evidence `" + gate + ".log`.\n")
raise SystemExit(1 if any(row["rc"] != 0 for row in results) else 0)
