#!/usr/bin/env python3
"""Gate 36b mutation probes for PR #663 (issue #661), run against disposable worktrees.

Usage: probe_36b.py <superproject clone> <scratch dir> <out dir>
Creates one detached worktree per arm at the clone's HEAD (with the three pinned
submodules as worktrees at their gitlinks), plants one source mutation, runs the
named gate-36b functions of sw/builder/test_builder.py, records rc and log, then
removes every worktree it created. The control arm plants nothing and must pass;
every mutant arm must fail.
"""
import subprocess, sys, os, json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

clone, scratch, out = (Path(a).resolve() for a in sys.argv[1:4])
out.mkdir(parents=True, exist_ok=True)
head = subprocess.check_output(["git", "-C", clone, "rev-parse", "HEAD"], text=True).strip()
TESTS = ["test_shipping_image_contract", "test_soc_shipping_image_contract",
         "test_shipping_image_contract_presence"]
ARMS = {
    "control": None,
    "builder_lint_off": ("sw/builder/endstation_builder.py",
                         "_join.identity_from_overlay(overlay)),\n        576)",
                         "_join.identity_from_overlay(overlay)),\n        576, lint=False)"),
    "soc_lint_off": ("sw/litex/milan_soc.py",
                     "_join.identity_from_overlay(ovl)), 576)",
                     "_join.identity_from_overlay(ovl)), 576, lint=False)"),
    "overlay_drops_waiver": ("sw/builder/endstation_builder.py",
                             "if cfg.get(\"model_lint_waivers\") else {}),",
                             "if False else {}),"),
    "spec_drops_waiver": ("avdecc/aem_specs.py",
                          "lint_waivers=list(ovl.get(\"model_lint_waivers\", [])),",
                          "lint_waivers=[],"),
    "document_drops_waiver": ("avdecc/gen_aemi_image.py",
                              "**({\"lint_waivers\": M[\"LINT_WAIVERS\"]} if M.get(\"LINT_WAIVERS\") else {}),",
                              "**({}),"),
}
DRIVER = (
    "import sys, os, traceback\n"
    "sys.path.insert(0, 'sw/builder'); sys.argv = ['test_builder.py']\n"
    "import runpy\n"
    "ns = runpy.run_path('sw/builder/test_builder.py', run_name='probe')\n"
    "bad = 0\n"
    "for name in %r:\n"
    "    try:\n"
    "        ns[name](); print('PROBE-PASS', name)\n"
    "    except BaseException as exc:\n"
    "        bad += 1; print('PROBE-FAIL', name, type(exc).__name__, str(exc).splitlines()[0][:300] if str(exc) else '')\n"
    "sys.exit(1 if bad else 0)\n" % (TESTS,))

def run(arm):
    wt = scratch / f"probe36b-{arm}"
    subs = ("protocol-processor", "gptp-processor", "third_party/verilog-axis")
    subprocess.run(["git", "-C", clone, "worktree", "add", "-q", "--detach", wt, head], check=True)
    for sub in subs:
        pin = subprocess.check_output(["git", "-C", wt, "rev-parse", f"HEAD:{sub}"], text=True).strip()
        subprocess.run(["git", "-C", clone / sub, "worktree", "add", "-q", "--detach", wt / sub, pin], check=True)
    try:
        spec = ARMS[arm]
        if spec:
            path, old, new = spec
            text = (wt / path).read_text()
            assert text.count(old) == 1, f"{arm}: site not unique ({text.count(old)})"
            (wt / path).write_text(text.replace(old, new))
        r = subprocess.run([sys.executable, "-c", DRIVER], cwd=wt, capture_output=True, text=True, timeout=1500)
        (out / f"{arm}.log").write_text(r.stdout + r.stderr)
        verdicts = [l for l in r.stdout.splitlines() if l.startswith("PROBE-")]
        return arm, r.returncode, verdicts
    finally:
        for sub in subs:
            subprocess.run(["git", "-C", clone / sub, "worktree", "remove", "--force", wt / sub])
        subprocess.run(["git", "-C", clone, "worktree", "remove", "--force", wt])

with ThreadPoolExecutor(max_workers=len(ARMS)) as pool:
    results = list(pool.map(run, ARMS))
ok = True
summary = []
for arm, rc, verdicts in results:
    expect = 0 if arm == "control" else "nonzero"
    good = (rc == 0) if arm == "control" else (rc != 0)
    ok &= good
    summary.append({"arm": arm, "rc": rc, "expected": expect, "as_expected": good, "verdicts": verdicts})
    print(f"{arm}: rc {rc} -> {'OK' if good else 'UNEXPECTED'}")
    for v in verdicts: print("   ", v)
(out / "summary.json").write_text(json.dumps({"head": head, "arms": summary}, indent=1) + "\n")
sys.exit(0 if ok else 1)
