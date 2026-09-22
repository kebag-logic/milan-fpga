#!/usr/bin/env python3
"""R235 independent workflow/record plants for the new docs-check step.

Each plant is a hard-linked copy of the head extract (cp -al) in which the
edited file is UNLINKED before being rewritten, so no shared inode changes.
Every textual edit must match exactly `count` times or the plant is INVALID.
`scripts/ci_events.py --check` (and, where listed, `--selftest`) then runs in
the copy, with PyYAML from the system interpreter.
expect: "refuse" (--check must exit non-zero), "accept" (--check must exit 0),
"selftest-refuse" (--check 0 but --selftest must exit non-zero).
Usage: workflow_mutations.py <head-extract> <work-root> <receipt-dir>
"""
import concurrent.futures as cf
import os
import shutil
import subprocess
import sys
from pathlib import Path

HEAD, WORK, OUT = (Path(a) for a in sys.argv[1:4])
PY = "/usr/bin/python3.14"
WF, CE = ".github/workflows/docs.yml", "scripts/ci_events.py"
STEP = ("      - name: AEM store generator self-test\n"
        "        run: python3 avdecc/gen_aem_store.py --self-test\n")
SWEEP = ("      - name: Sweep/build shape gate\n"
         "        run: python3 scripts/check_sweep_shape.py --self-test\n")
RECORD = ('        {"name": "AEM store generator self-test",\n'
          '         "run": (\n'
          "             'python3 avdecc/gen_aem_store.py --self-test',\n"
          "         )},\n")
E = lambda f, o, n, c=1: (f, o, n, c)  # noqa: E731
PLANTS = [
    ("W00", "pristine hard-linked copy", "accept", []),
    ("W01", "new step removed (record kept)", "refuse", [E(WF, STEP, "")]),
    ("W02", "new step moved after the sweep shape gate", "refuse",
     [E(WF, STEP + "\n", ""), E(WF, SWEEP, SWEEP + "\n" + STEP)]),
    ("W03", "new step renamed", "refuse",
     [E(WF, "- name: AEM store generator self-test\n", "- name: AEM store self-test\n")]),
    ("W04", "new step gains if: false", "refuse",
     [E(WF, STEP, STEP.replace("        run:", "        if: false\n        run:"))]),
    ("W05", "new step gains continue-on-error: true", "refuse",
     [E(WF, STEP, STEP + "        continue-on-error: true\n")]),
    ("W06", "--self-test flag dropped (store would be regenerated instead)", "refuse",
     [E(WF, "run: python3 avdecc/gen_aem_store.py --self-test\n",
        "run: python3 avdecc/gen_aem_store.py\n")]),
    ("W07", "call swallowed with || true", "refuse",
     [E(WF, "run: python3 avdecc/gen_aem_store.py --self-test\n",
        "run: python3 avdecc/gen_aem_store.py --self-test || true\n")]),
    ("W08", "working-directory redirect", "refuse",
     [E(WF, STEP, "      - name: AEM store generator self-test\n"
                  "        working-directory: avdecc\n"
                  "        run: python3 gen_aem_store.py --self-test\n")]),
    ("W09", "step env PYTHONPATH added", "refuse",
     [E(WF, STEP, STEP + "        env:\n          PYTHONPATH: avdecc\n")]),
    ("W10", "step shell override", "refuse",
     [E(WF, STEP, STEP + "        shell: bash {0}\n")]),
    ("W11", "whitespace-only reformat to a block scalar", "accept",
     [E(WF, STEP, "      - name: AEM store generator self-test\n"
                  "        run: |\n"
                  "          python3   avdecc/gen_aem_store.py   --self-test\n")]),
    ("W12", "trailing '; true' appended on the same line", "refuse",
     [E(WF, "run: python3 avdecc/gen_aem_store.py --self-test\n",
        "run: python3 avdecc/gen_aem_store.py --self-test; true\n")]),
    ("W13", "step AND record removed together (step-count arms still say 44)",
     "selftest-refuse", [E(WF, STEP, ""), E(CE, RECORD, "")]),
    ("W14", "record removed, step kept", "refuse", [E(CE, RECORD, "")]),
    ("W15", "step duplicated", "refuse", [E(WF, STEP, STEP + STEP)]),
    ("W16", "third-party action inserted before the step", "refuse",
     [E(WF, STEP, "      - uses: actions/setup-python@v5\n" + STEP)]),
    ("W17", "record's script altered (workflow unchanged)", "refuse",
     [E(CE, "             'python3 avdecc/gen_aem_store.py --self-test',\n",
        "             'python3 avdecc/gen_aem_store.py --self-test --x',\n")]),
]


def plant(pid, edits):
    d = WORK / pid
    if d.exists():
        shutil.rmtree(d)
    subprocess.run(["cp", "-al", str(HEAD), str(d)], check=True)
    for f, old, new, count in edits:
        p = d / f
        text = p.read_text()
        n = text.count(old)
        if n != count:
            return d, f"INVALID: {f} has {n} x {old!r}"
        p.unlink()                      # never write through a shared hard link
        p.write_text(text.replace(old, new))
    return d, None


def run(pid, desc, expect, edits):
    d, invalid = plant(pid, edits)
    if invalid:
        return f"{pid} {expect:15s} INVALID {desc}: {invalid}"
    env = {"PATH": os.environ["PATH"], "HOME": os.environ["HOME"]}
    chk = subprocess.run([PY, "-B", "-E", "-s", CE, "--check"], cwd=d,
                         capture_output=True, text=True, env=env)
    (OUT / f"{pid}-check.log").write_text(chk.stdout + chk.stderr)
    rc_s = None
    if expect == "selftest-refuse":
        st = subprocess.run([PY, "-B", "-E", "-s", CE, "--selftest"], cwd=d,
                            capture_output=True, text=True, env=env)
        (OUT / f"{pid}-selftest.log").write_text(st.stdout + st.stderr)
        rc_s = st.returncode
    lines = (chk.stdout + chk.stderr).splitlines()
    hit = next((l.strip() for l in lines if ("AEM store" in l or "step 41" in l
                                             or "step 42" in l or "44 steps" in l)
                and ("must" in l or "FAIL" in l or "not" in l)), "")
    if expect == "refuse":
        ok = chk.returncode != 0
    elif expect == "accept":
        ok = chk.returncode == 0
    else:
        ok = chk.returncode == 0 and rc_s not in (0, None)
    return (f"{pid} {expect:15s} {'MET' if ok else 'NOT-MET':7s} {desc}\n"
            f"     --check rc={chk.returncode}"
            + (f" --selftest rc={rc_s}" if rc_s is not None else "")
            + (f"\n     finding: {hit[:210]}" if hit else ""))


OUT.mkdir(parents=True, exist_ok=True)
WORK.mkdir(parents=True, exist_ok=True)
with cf.ThreadPoolExecutor(max_workers=8) as ex:
    rows = list(ex.map(lambda p: run(*p), PLANTS))
text = "\n".join(rows)
text += (f"\n\nTALLY: MET={sum(' MET ' in r for r in rows)} "
         f"NOT-MET={sum('NOT-MET' in r for r in rows)} "
         f"INVALID={sum('INVALID' in r for r in rows)} plants={len(rows)}\n")
(OUT / "SUMMARY.txt").write_text(text)
print(text)
