#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Copy the reviewer's run logs into receipts/ with local roots replaced by
placeholders ($PACKET, $CLONE, $HOME, $SIMROOT), keeping each log's verdict
lines, and summarise the probe campaign. Usage: collect_receipts.py <packet> <review clone>"""
import json
import re
import sys
from pathlib import Path

packet = Path(sys.argv[1])
scratch, receipts = packet / "scratch", packet / "receipts"
receipts.mkdir(exist_ok=True)
CLONE = sys.argv[2] if len(sys.argv) > 2 else "$CLONE"
ROOTS = [(str(packet), "$PACKET"), (CLONE, "$CLONE"),
         (re.compile(re.escape(str(Path.home())) + r"/\.local/share/containers/storage/overlay/[0-9a-f]+/diff"), "$SIMROOT"),
         (str(Path.home()), "$HOME"), ("$VALIDATION_TOOLS", "$TOOLS")]


def clean(text):
    for old, new in ROOTS:
        text = old.sub(new, text) if hasattr(old, "sub") else text.replace(old, new)
    return text


def keep(name, src, pattern=None, tail=None):
    path = scratch / src
    if not path.exists():
        return
    lines = clean(path.read_text(errors="replace")).splitlines()
    if pattern:
        lines = [l for l in lines if re.search(pattern, l)]
    if tail:
        lines = lines[-tail:]
    (receipts / name).write_text("\n".join(lines) + "\n")


verdicts = r"\[(PASS|FAIL|ok|FAIL )\]|RESULT|checks|PASS|FAIL|Error|mutant|LINT GATE|docs_check"
keep("run-render_queue-all.txt", "runs/rq.log", verdicts)
keep("run-chmap_capture.txt", "runs/chmap.log", verdicts, tail=60)
keep("run-capture_coherence-dp.txt", "runs/coh.log", r"RESULT|checks:|FAIL|Error", tail=40)
keep("run-milan_dp_render-ship8.txt", "runs/dpr.log", r"RESULT|checks:|FAIL|Error", tail=60)
keep("run-builder-test_input_loopback.txt", "runs/builder-input-loopback.log")
keep("run-lint.txt", "runs/lint.log", tail=3)
keep("run-docs_check.txt", "runs/docs.log", tail=3)
for rc in ("rq", "chmap", "coh", "dpr", "builder-input-loopback", "lint", "docs"):
    p = scratch / "runs" / f"{rc}.rc"
    if p.exists():
        (receipts / f"run-{rc}.rc").write_text(p.read_text())
# author campaign re-run, unchanged script, pinned simulator
m = scratch / "mutants-head" / "results.json"
if m.exists():
    rows = json.loads(m.read_text())
    for r in rows:
        r["command"] = [clean(c) for c in r["command"]]
    (receipts / "author-mutants-rerun.json").write_text(json.dumps(rows, indent=1) + "\n")
    lines = []
    for r in rows:
        log = scratch / "mutants-head" / f"{r['plant']}.log"
        text = clean(log.read_text(errors="replace")) if log.exists() else ""
        verdict = [l for l in text.splitlines() if "input-loopback streams=" in l]
        first = [l for l in text.splitlines() if l.startswith("FAIL ") and "input-loopback" not in l][:2]
        lines.append(f"{r['plant']}: exit {r['exit']} expectation_met={r['passed']} | "
                     f"{verdict[-1] if verdict else '-'} | {' ; '.join(first)}")
    (receipts / "author-mutants-rerun.txt").write_text("\n".join(lines) + "\n")
# reviewer probes
p = scratch / "probes" / "results.json"
if p.exists():
    rows = json.loads(p.read_text())
    (receipts / "probes-results.json").write_text(clean(json.dumps(rows, indent=1)) + "\n")
    out = []
    for r in rows:
        log = scratch / "probes" / r["probe"] / "run.log"
        first = []
        if log.exists():
            first = [l for l in clean(log.read_text(errors="replace")).splitlines()
                     if l.startswith("FAIL ") and "input-loopback" not in l][:2]
        out.append(f"{r['probe']}: exit {r.get('exit')} expect={r.get('expect')} met={r.get('expectation_met')} | "
                   f"{r.get('verdict')} | {' ; '.join(first)}")
    (receipts / "probes-summary.txt").write_text("\n".join(out) + "\n")
print("collected", sorted(x.name for x in receipts.iterdir()))
