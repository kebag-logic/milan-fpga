#!/usr/bin/env python3
"""R624-10: gather this review's runs into one path-free receipt.

usage: python3 -I collect_receipts.py <scratch> <review clone> <out.json>

Reads, from <scratch>: the check's run at the head (run0/), the control runners (ctl/), the round 10 helper
tools (r10tools/), the gate logs (gates/), and the published packet copy (pk/, the evidence clone's author-r10).
Records exit statuses, summaries, byte-equality with the author's published files and SHA-256s. Every absolute
path is replaced by a placeholder.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

S, R, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
PATH = re.compile(r"(?:/[\w.+@-]+){2,}")


def clean(s):
    return PATH.sub("<path>", s)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def verdicts(p):
    d = json.loads(Path(p).read_text())
    c = d["controls"] if isinstance(d, dict) and "controls" in d else d
    if isinstance(c, dict):
        return {k: (v if isinstance(v, str) else v.get("verdict")) for k, v in c.items()}
    return {(x.get("control") or x.get("name")): x.get("verdict") for x in c}


A = S / "pk"
out = dict(head=subprocess.run(["git", "-C", str(R), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
           tree=subprocess.run(["git", "-C", str(R), "rev-parse", "HEAD^{tree}"], capture_output=True, text=True).stdout.strip())
out["check_at_head"] = dict(
    check_sha256=sha(A / "tools/check_b16_figures.py"),
    stdout=(S / "run0/stdout").read_text().strip(),
    stdout_equal_published=(S / "run0/stdout").read_bytes() == (A / "r10/figures-check.stdout").read_bytes(),
    rows_sha256=sha(S / "run0/rows.tsv"), rows_equal_published=sha(S / "run0/rows.tsv") == sha(A / "r10/figures-rows.tsv"),
    coverage_sha256=sha(S / "run0/cov.tsv"),
    coverage_equal_published=sha(S / "run0/cov.tsv") == sha(A / "r10/figures-coverage.tsv"))
runners = {}
for mine, auth in [("r3", "r10-rerun-r3-controls"), ("r4", "r10-rerun-r4-controls"), ("r5", "r10-rerun-r5-controls"),
                   ("r6", "r10-rerun-r6-controls"), ("r7", "r10-rerun-r7-controls"), ("r8", "r10-rerun-r8-controls"),
                   ("r9", "r10-rerun-r9-controls"), ("r10", "r10-controls"), ("r10-on-r9b", "r10-controls-on-r9-check")]:
    m, a = verdicts(S / f"ctl/{mine}.json"), verdicts(A / f"controls/{auth}.json")
    runners[mine] = dict(against=auth, passed=sum(v == "PASS" for v in m.values()), total=len(m),
                         failed=sorted(k for k, v in m.items() if v != "PASS") if len(m) - sum(v == "PASS" for v in m.values()) < 5
                         else len(m) - sum(v == "PASS" for v in m.values()),
                         verdicts_equal_published=m == a)
out["control_runners"] = runners
tools = {}
for mine, auth in [("extents.json", "parser-extents.json"), ("layers.json", "layers.json"),
                   ("readerctl.json", "reader-controls.json"), ("selfprobes.json", "self-probes.json"),
                   ("readeron9.json", "reader-on-r9.json"), ("evrcpt.json", "evidence-receipt.json")]:
    tools[auth] = dict(rc=int((S / f"r10tools/{mine.split('.')[0]}.rc").read_text()),
                       sha256=sha(S / f"r10tools/{mine}"),
                       byte_equal_published=(S / f"r10tools/{mine}").read_bytes() == (A / f"r10/{auth}").read_bytes())
tools["r10_figures_build.py"] = dict(rc=int((S / "r10tools/build.rc").read_text()),
                                     regenerated_check_byte_equal=(S / "r10tools/build-check.py").read_bytes()
                                     == (A / "tools/check_b16_figures.py").read_bytes())
out["round10_tools"] = tools
gates = {}
for rc in sorted((S / "gates").glob("*.rc")):
    log = (S / "gates" / (rc.stem + ".log")).read_text().strip().splitlines()
    gates[rc.stem] = dict(rc=int(rc.read_text()), last=clean(log[-1]) if log else "")
out["gates"] = gates
OUT.write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps(dict(check=out["check_at_head"]["stdout_equal_published"],
                      runners={k: (v["passed"], v["total"], v["verdicts_equal_published"]) for k, v in runners.items()},
                      tools={k: v.get("byte_equal_published", v.get("regenerated_check_byte_equal")) for k, v in tools.items()},
                      gates={k: v["rc"] for k, v in gates.items()})))
