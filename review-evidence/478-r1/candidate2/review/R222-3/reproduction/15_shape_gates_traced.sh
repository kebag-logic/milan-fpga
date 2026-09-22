#!/usr/bin/env bash
# R222-3: docs-check steps outside the manager's 41-command bank that sit on
# the builder/avdecc path, each run on the pristine combined tree in a fresh
# interpreter with a repository-file trace (issue/#513 paths tagged).
# Usage: 15_shape_gates_traced.sh <pristine-cand-clone>
set -uo pipefail
d=$1
export PYTHONDONTWRITEBYTECODE=1
echo "head=$(git -C "$d" rev-parse HEAD) tree=$(git -C "$d" rev-parse 'HEAD^{tree}')"
for spec in "scripts/check_deploy_shape.py --self-test" \
            "scripts/check_entity_shape.py --self-test" \
            "scripts/check_rtl_source_lists.py --selftest" \
            "sw/litex/iob_pack_selftest.py"; do
  PYTHONPYCACHEPREFIX=$(mktemp -d) python3 - "$d" $spec <<'EOF'
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
buf = io.StringIO(); code = 0
with contextlib.redirect_stdout(buf):
    try:
        runpy.run_path(path, run_name="__main__")
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
tail = [l for l in buf.getvalue().splitlines() if l.strip()][-1:]
print(f"exit {code:<3} {script} {' '.join(args)}\n        | {tail}")
print(f"        issue paths opened: {sorted(opened & ISSUE)}; #513 paths opened: {sorted(opened & PR513)}; files {len(opened)}")
EOF
done
echo "clone status lines after run: $(git -C "$d" status --porcelain --untracked-files=all | wc -l)"
