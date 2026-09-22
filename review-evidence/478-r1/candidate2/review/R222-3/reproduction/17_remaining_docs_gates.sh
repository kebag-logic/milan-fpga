#!/usr/bin/env bash
# R222-3: the runnable docs-check gate lines that neither the manager's bank
# nor receipts 08-15 exercised on the combined tree, each traced for issue/#513
# path reads. NOT run by design: scripts/act_ci.py --selftest (candidate copy
# must not execute on the host), the HDL reference build (pinned pyslang wheel
# not installed) and gen_wavedrom (wavedrom not installed; no installs).
# Usage: 17_remaining_docs_gates.sh <pristine-cand-clone>
set -uo pipefail
d=$1
export PYTHONDONTWRITEBYTECODE=1
echo "head=$(git -C "$d" rev-parse HEAD) tree=$(git -C "$d" rev-parse 'HEAD^{tree}')"
trace() {
  PYTHONPYCACHEPREFIX=$(mktemp -d) python3 - "$d" "$@" <<'EOF'
import os, runpy, sys, io, contextlib
root = os.path.realpath(sys.argv[1]); script = sys.argv[2]; args = sys.argv[3:]
ISSUE = {"docs/ENDSTATION_BUILDER.md", "sw/builder/endstation_builder.py", "sw/builder/test_builder.py"}
PR513 = {".github/workflows/docs.yml", "avdecc/aem_maps.py", "avdecc/gen_aem_store.py",
         "docs/testing/CI_WORKFLOWS.md", "docs/testing/RUNNING_TESTS.md", "scripts/ci_events.py"}
opened = set()
def hook(ev, a):
    if ev == "open" and a and isinstance(a[0], (str, bytes, os.PathLike)):
        p = os.fsdecode(a[0])
        p = os.path.realpath(p if os.path.isabs(p) else os.path.join(os.getcwd(), p))
        if p.startswith(root + os.sep):
            opened.add(os.path.relpath(p, root))
sys.addaudithook(hook)
os.chdir(root)
path = os.path.join(root, script)
sys.path.insert(0, os.path.dirname(path))
sys.argv = [path, *args]
out = io.StringIO(); code = 0
with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
    try:
        runpy.run_path(path, run_name="__main__")
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
tail = [l.strip() for l in out.getvalue().splitlines() if l.strip()][-1:]
print(f"exit {code:<3} {script} {' '.join(args)} | {tail}")
print(f"        issue paths read: {sorted(opened & ISSUE)}; #513 paths read: {sorted(opened & PR513)}")
EOF
}
trace scripts/check_gptp_docs.py --with-submodule
trace scripts/check_nvm_record_space.py --self-test
trace scripts/check_soc_sources.py --selftest
trace scripts/measure_naming.py --selftest
trace scripts/check_port_contracts.py --selftest
trace scripts/measure_fail_fast.py --selftest
trace scripts/check_todo_ownership.py --selftest
trace scripts/measure_test_evidence.py --selftest
trace scripts/check_hygiene.py --selftest
trace scripts/check_sv_idiom.py --selftest
trace scripts/check_cpp_idiom.py --selftest
trace scripts/check_py_idiom.py --selftest
trace scripts/check_sh_idiom.py --selftest
trace scripts/check_archive.py --selftest
out=$(make -C "$d/gptp-processor" docs 2>&1); rc=$?
echo "exit $rc   make -C gptp-processor docs | $(printf '%s\n' "$out" | grep -v '^\s*$' | tail -1)"
echo "clone status lines after run: $(git -C "$d" status --porcelain --untracked-files=all | wc -l)"
echo "gptp-processor status lines after run: $(git -C "$d/gptp-processor" status --porcelain --untracked-files=all | wc -l)"
