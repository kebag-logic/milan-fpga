#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Writes COMMAND_RESULTS.md from what run.py recorded: every command of
every phase with its exit code, every case run's exit code, and the SHA-256
of every evidence source and of every production file examined. The session
narrative (which invocations ran, in what order, and why) is SESSION below.

    python3 -B proposal-evidence/make_command_results.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

#: production files read or searched for this proposal beyond run.py's own
#: PRODUCTION list (which results.json hashes before and after the run)
EXAMINED_EXTRA = [
    "AGENTS.md", "CONTRIBUTING.md",
    "docs/reference/REGISTER_MAP.md",
    "sw/litex/milan_soc.py",
    "configs/endstation_ax7101_1x1_tdm8.yaml", "configs/endstation_ax7101_8x8.yaml",
    "tb/verilator/nvm_backend/Makefile", "tb/verilator/nvm_backend/sim_main.cpp",
    "tb/verilator/nvm_backend/mutate.py",
    "protocol-processor/hdl/aecp/KL_aecp_engine.sv",
    "protocol-processor/hdl/aecp/KL_aecp_desc_store.sv",
    "protocol-processor/hdl/aecp/ucode/gen_ucode.py",
    "protocol-processor/docs/architecture/02_interfaces.md",
]

SESSION = """\
## Session narrative

Every command below ran in the foreground from the checkout root with rtk in
front; compiling and simulating steps also ran under taskset -c 16-31 with at
most 8 workers (run.py adds both to every command it spawns).

State found at the start: the previous session's results.txt and
results.json predated its own last edits to harness/cosim_cases.cpp and
run.py and its last build and run phases, and no grade followed them, so
they did not describe the sources on disk. They are kept unmodified in
proposal-evidence/prior-session/ (results.txt sha256
16fce8e6b916f9ee479bceeb18d3240fb24f33f3920725e9a1484b4fe90c4fdf). Two draft
files the prototype never included (control_section.svh,
ownership_section.svh) were moved from prototype/ to
prior-session/unused-drafts/, and the empty mutants/ directory was removed
(mutants are defined in run.py).

| Step | Command | Exit | Result |
|---|---|---|---|
| 1 | remove build/, runs/, logs/, tmp/, results.* (clean state) | 0 | - |
| 2 | python3 -B proposal-evidence/run.py --phase build --jobs 8 | 0 | 50 s |
| 3 | python3 -B proposal-evidence/run.py --phase run --jobs 8 | 0 | 1110 runs, 6 min 45 s |
| 4 | python3 -B proposal-evidence/run.py --phase grade --jobs 8 | 1 | DIFFERS from prior-session/results.txt: two findings, C1r deferred_until_certificate:0x21:port and C2r hold_bounded:0x21:port. Cause: the check selected the FIRST port ERASE of record 0x21, which is the base binding flushed before any capture, not the request made inside the hold. Resolved in run.py (held_op: the first request made while a capture is open and uncertified); the request inside the hold was deferred correctly (requested 8 cycles after the arm, granted after the certificate) |
| 5 | python3 -B proposal-evidence/run.py --phase grade --skip-area | 0 | no findings; mutant M06 now fails both real-port checks (the checks are live) |
| 6 | cases added in harness/cosim_cases.cpp and run.py: C2e (real port, erased span under a stale mask), a first gap case, mutants M18 (pending bit stuck) and F06 (ACK after a failed slot), convergence now requires the durable status reading | - | - |
| 7 | clean state, then run.py --phase build, --phase run, --phase grade | 0, 0, 0 | 1252 runs, no findings. The first gap case landed the ARM on the WRITE's request edge, so M02 survived it (B5 still killed M02) |
| 8 | the gap case split into C1a (ARM after ERASE done, on the WRITE request edge) and C1g (copy taken inside the ERASE-to-WRITE gap, ERASE granted before the arm, WRITE held) | - | - |
| 9 | clean state, then run.py --phase build, --phase run, --phase grade | 0, 0, 0 | FINAL: 1278 runs, no findings |
| 10 | M02's named killer changed from B5 to the real-port C1g in run.py; run.py --phase grade | 0 | no findings |
| 11 | the rejected composite-bit alternative added as build mut-A01_composite_durable_bit; run.py --phase build --builds 'mut-A01*', --phase run --builds 'mut-A01*', --phase grade | 0, 0, 0 | FINAL results.txt: 1326 runs, NO FINDINGS |
| 12 | python3 -B proposal-evidence/make_command_results.py | 0 | this file |

Stopped steps: NONE. No tool call or step was refused or stopped by an
automatic safety filter in this session. No compiler-callback or binary
instrumentation was used; the only source adaptation is run.py's counted
textual seams (the firmware's two CSR primitives and its fences, and the
single counted replacement of each mutant).
"""


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git(*a, cwd=ROOT) -> str:
    return subprocess.check_output(["rtk", "proxy", "git", *a], cwd=cwd, text=True).strip()


def main() -> None:
    res = json.loads((HERE / "results.json").read_text())
    out = ["# Command results for the issue 419 round-3 proposal", "",
           "Paths are relative to the checkout root; <CHECKOUT> in a recorded "
           "command stands for it.", "", "## Source", ""]
    out.append(f"- dev {git('rev-parse', 'HEAD')}")
    for sub in ("protocol-processor", "gptp-processor", "third_party/verilog-axis"):
        out.append(f"- {sub} {git('rev-parse', 'HEAD', cwd=ROOT / sub)}")
    out.append(f"- tracked changes: {'none' if not git('status', '--porcelain', '--untracked-files=no') else 'PRESENT'}")
    out += ["", SESSION, "## Final results (proposal-evidence/results.txt)", ""]
    txt = (HERE / "results.txt").read_text().splitlines()
    out += ["```"] + [ln for ln in txt if not ln.startswith(("prod-", "proto-", "mut-", "mix-"))] + ["```", ""]
    # totals
    runs = res["runs"]
    tot = collections.Counter()
    per = collections.defaultdict(collections.Counter)
    exits = collections.Counter()
    for r in runs:
        b = r["build"]
        k = "mutants and alternative" if b.startswith("mut-") else b
        exits[r["exit"]] += 1
        for v in r["checks"].values():
            tot[v[0]] += 1
            per[k][v[0]] += 1
    out += ["## Graded checks", "",
            f"{len(runs)} case runs over {len({r['build'] for r in runs})} builds; "
            f"{sum(tot.values())} graded checks: {tot['pass']} pass, {tot['fail']} fail, "
            f"{tot['n/a']} not expressible.", "",
            "| Build class | pass | fail | n/a |", "|---|---|---|---|"]
    for k, v in sorted(per.items()):
        out.append(f"| {k} | {v['pass']} | {v['fail']} | {v['n/a']} |")
    out += ["", "Case-run exit codes: " + ", ".join(f"{n} runs exit {e}" for e, n in sorted(exits.items()))
            + ". A non-zero exit occurs only on a mutant (its harness aborts, graded as a "
            "failing check):", ""]
    for r in runs:
        if r["exit"] != 0:
            out.append(f"- {r['build']} {r['case']}: exit {r['exit']}")
    out.append("")
    # every recorded command
    out += ["## Every recorded command, with its exit code", "",
            "The case runs themselves are the 'runs' of results.json (exit codes "
            "above); every other command run.py spawned is below, from its "
            "manifests.", ""]
    mans = sorted((HERE / "logs").glob("manifest-*.json"))
    blocks = [(m.name, json.loads(m.read_text())) for m in mans] + [("results.json (grade phase)", res["manifest"])]
    for name, entries in blocks:
        ex = collections.Counter(e["exit"] for e in entries)
        out += [f"### {name}: {len(entries)} commands, exit codes {dict(sorted(ex.items()))}", "",
                "| Exit | Wall s | Command |", "|---|---|---|"]
        for e in entries:
            cmdline = " ".join(e["argv"]).replace("|", "\\|")
            if len(cmdline) > 400:
                cmdline = cmdline[:400] + " ..."
            out.append(f"| {e['exit']} | {e['wall_s']} | `{cmdline}` |")
        out.append("")
    out += ["The two grade-phase commands that exit 1 are the build-time refusals, "
            "which MUST fail (REFUSAL lines above).", ""]
    # hashes
    out += ["## SHA-256 of every evidence source", "", "| sha256 | file |", "|---|---|"]
    skip = {"build", "runs", "logs", "tmp", "console", "__pycache__"}
    for p in sorted(HERE.rglob("*")):
        if p.is_file() and not (set(p.relative_to(HERE).parts[:1]) & skip) \
                and p.name not in ("results.txt", "results.json"):
            out.append(f"| {sha(p)} | proposal-evidence/{p.relative_to(HERE)} |")
    out += ["", "## SHA-256 of the evidence outputs", "", "| sha256 | file |", "|---|---|"]
    for p in [HERE / "results.txt", HERE / "results.json", *sorted((HERE / "console").glob("*.log")),
              *mans]:
        out.append(f"| {sha(p)} | proposal-evidence/{p.relative_to(HERE)} |")
    out += ["", "## SHA-256 of every production file examined", "",
            f"run.py's PRODUCTION list is hashed before and after the run; unchanged: "
            f"{res['production_unchanged']}.", "", "| sha256 | file |", "|---|---|"]
    prod = dict(res["production_sha256"])
    for p in EXAMINED_EXTRA:
        prod[p] = sha(ROOT / p)
    for p in sorted(prod):
        now = sha(ROOT / p)
        flag = "" if now == prod[p] else " (CHANGED SINCE THE RUN)"
        out.append(f"| {now} | {p}{flag} |")
    out.append("")
    (ROOT / "COMMAND_RESULTS.md").write_text("\n".join(out))
    print(f"wrote COMMAND_RESULTS.md: {len(out)} lines")


if __name__ == "__main__":
    main()
