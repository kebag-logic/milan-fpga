#!/usr/bin/env bash
# R222-3: focused runs of required-context gates on the combined tree that
# read the builder and/or avdecc: the wire-accountability job's gate (not in
# the manager's 41-command bank; hosted-only) with a repository-file trace,
# and the REQ-VER-04 source-list and bare-metal gates. Pristine cand2 clone.
# Usage: 14_extra_required_gates.sh <pristine-cand-clone>
set -uo pipefail
d=$1
export PYTHONDONTWRITEBYTECODE=1
fail=0
step() {
  local out rc
  out=$(cd "$d" && "$@" 2>&1); rc=$?
  [ $rc -eq 0 ] || fail=$((fail+1))
  printf 'exit %-3s %s\n' "$rc" "$*"
  printf '%s\n' "$out" | grep -v '^\s*$' | tail -2 | sed 's/^/        | /'
}
echo "head=$(git -C "$d" rev-parse HEAD) tree=$(git -C "$d" rev-parse 'HEAD^{tree}')"
step python3 scripts/check_wire_accountability.py --self-test
step python3 scripts/check_baremetal_only.py --check
step python3 scripts/check_baremetal_only.py --selftest
step python3 scripts/pp_srcs.py --check --selftest
step python3 scripts/check_rtl_source_lists.py
step python3 scripts/check_soc_sources.py
echo "non-zero steps: $fail"
echo "-- repository files the wire-accountability self-test opens (fresh interpreter)"
PYTHONPYCACHEPREFIX=$(mktemp -d) python3 - "$d" <<'EOF'
import os, runpy, sys, io, contextlib
root = os.path.realpath(sys.argv[1])
ISSUE = {"docs/ENDSTATION_BUILDER.md", "sw/builder/endstation_builder.py", "sw/builder/test_builder.py"}
PR513 = {".github/workflows/docs.yml", "avdecc/aem_maps.py", "avdecc/gen_aem_store.py",
         "docs/testing/CI_WORKFLOWS.md", "docs/testing/RUNNING_TESTS.md", "scripts/ci_events.py"}
opened = set()
def hook(ev, args):
    if ev == "open" and args and isinstance(args[0], (str, bytes, os.PathLike)):
        p = os.fsdecode(args[0])
        p = os.path.realpath(p if os.path.isabs(p) else os.path.join(os.getcwd(), p))
        if p.startswith(root + os.sep):
            opened.add(os.path.relpath(p, root))
sys.addaudithook(hook)
os.chdir(root)
sys.path.insert(0, os.path.join(root, "scripts"))
sys.argv = [os.path.join(root, "scripts/check_wire_accountability.py"), "--self-test"]
code = 0
with contextlib.redirect_stdout(io.StringIO()):
    try:
        runpy.run_path(sys.argv[0], run_name="__main__")
    except SystemExit as e:
        code = e.code or 0
print(f"exit {code}; files opened {len(opened)}")
print(f"   issue paths opened: {sorted(opened & ISSUE)}")
print(f"   #513 paths opened:  {sorted(opened & PR513)}")
EOF
echo "clone status lines after run: $(git -C "$d" status --porcelain --untracked-files=all | wc -l)"
