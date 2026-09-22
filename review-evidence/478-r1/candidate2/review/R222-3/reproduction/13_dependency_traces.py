#!/usr/bin/env python3
"""R222-3: complete repository-file dependency lists (audit-hook 'open'
events, fresh interpreter, empty bytecode cache) for each gate 36a arm and for
the AEM store self-test, on a pristine candidate clone. Each opened file is
tagged ISSUE (the #478 patch), PR513 (the #513 patch) or unchanged.
Usage: 13_dependency_traces.py <pristine-candidate-clone>
"""
import json
import os
import subprocess
import sys
import tempfile

root = os.path.realpath(sys.argv[1])
ISSUE = {"docs/ENDSTATION_BUILDER.md", "sw/builder/endstation_builder.py",
         "sw/builder/test_builder.py"}
PR513 = {".github/workflows/docs.yml", "avdecc/aem_maps.py", "avdecc/gen_aem_store.py",
         "docs/testing/CI_WORKFLOWS.md", "docs/testing/RUNNING_TESTS.md",
         "scripts/ci_events.py"}
DRIVER = r'''
import json, os, sys, io, contextlib, runpy
root = os.path.realpath(sys.argv[1]); target = sys.argv[2]
opened = set()
def hook(event, args):
    if event == "open" and args and isinstance(args[0], (str, bytes, os.PathLike)):
        p = os.fsdecode(args[0])
        if not os.path.isabs(p):
            p = os.path.join(os.getcwd(), p)
        p = os.path.realpath(p)
        if p.startswith(root + os.sep):
            opened.add(os.path.relpath(p, root))
sys.addaudithook(hook)
status = "PASS"
with contextlib.redirect_stdout(io.StringIO()):
    try:
        if target == "selftest":
            sys.path.insert(0, os.path.join(root, "avdecc"))
            sys.argv = [os.path.join(root, "avdecc/gen_aem_store.py"), "--self-test"]
            try:
                runpy.run_path(sys.argv[0], run_name="__main__")
            except SystemExit as e:
                status = "PASS" if e.code in (0, None) else "FAIL"
        else:
            sys.path.insert(0, os.path.join(root, "sw/builder"))
            import test_builder as tb
            getattr(tb, target)()
    except BaseException:
        status = "FAIL"
print(json.dumps({"status": status, "opened": sorted(opened)}))
'''
for target in ("test_audio_unit_rates_loader_contract", "test_audio_unit_shipping_rates",
               "test_pp_shadow_audio_unit_rates_match_config", "selftest"):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1",
               PYTHONPYCACHEPREFIX=tempfile.mkdtemp(prefix="r222-r3-pyc-"))
    env.pop("PYTHONPATH", None)
    p = subprocess.run([sys.executable, "-c", DRIVER, root, target], cwd=root, env=env,
                       capture_output=True, text=True, timeout=900)
    r = json.loads(p.stdout.strip().splitlines()[-1])
    print(f"== {target}: {r['status']}, {len(r['opened'])} repository files opened")
    for f in r["opened"]:
        tag = "ISSUE" if f in ISSUE else ("PR513" if f in PR513 else "")
        print(f"   {tag:<5} {f}")
st = subprocess.run(["git", "-C", root, "status", "--porcelain", "--untracked-files=all"],
                    capture_output=True, text=True).stdout
print(f"clone status lines after traces: {len(st.splitlines())}")
