#!/usr/bin/env python3
"""Disposable composition probes for PR #543 on the merge-train candidate.

Usage: probes.py <candidate-checkout> <parent-rev> <scratch-dir>

Every arm works on a copy under <scratch-dir>; the candidate checkout is only
read. Behave arms copy tests/ and protocol-processor/hdl into a probe tree and
run the contract feature there, then compare the failing scenario lines to the
expected set. The em-dash arm makes a shared local clone at HEAD, commits one
edited line of the composed roadmap row there and runs the candidate's own
check_em_dash.py against the parent revision.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
PARENT = sys.argv[2]
SCRATCH = Path(sys.argv[3]).resolve()
FEATURE = "features/aecp_response_contract.feature"


def sub(path, old, new):
    text = path.read_text(encoding="utf-8")
    assert text.count(old) == 1, f"{path}: anchor count {text.count(old)}: {old!r}"
    path.write_text(text.replace(old, new), encoding="utf-8")


def probe_tree(name):
    root = SCRATCH / f"probe_{name}"
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(REPO / "tests", root / "tests")
    shutil.copytree(REPO / "protocol-processor" / "hdl",
                    root / "protocol-processor" / "hdl")
    # everything else the step modules import or read is linked, read-only
    for top, copied in ((REPO, {"tests", "protocol-processor", ".git"}),
                        (REPO / "protocol-processor", {"hdl", ".git"})):
        dest = root if top == REPO else root / "protocol-processor"
        for entry in top.iterdir():
            if entry.name not in copied:
                (dest / entry.name).symlink_to(entry)
    return root


def failing_lines(root):
    out = subprocess.run(["behave", "--no-capture", "-f", "plain", FEATURE],
                         cwd=root / "tests", capture_output=True, text=True)
    fails = sorted(set(int(m) for m in re.findall(
        r"aecp_response_contract\.feature:(\d+)\s", out.stdout.split(
            "Failing scenarios:")[-1]))) if "Failing scenarios:" in out.stdout else []
    tally = [l for l in out.stdout.splitlines() if " passed, " in l]
    return out.returncode, fails, tally


def row_line(text_lines, needle):
    hits = [i + 1 for i, l in enumerate(text_lines) if needle in l]
    assert len(hits) == 1, (needle, hits)
    return hits[0]


feat = (REPO / "tests" / FEATURE).read_text(encoding="utf-8").splitlines()
L = {
    "row0000": row_line(feat, "| 0x0000       | GET_MILAN_INFO | 5.4.4.1 |"),
    "row0002": row_line(feat, "| 0x0002       | GET_SYSTEM_UNIQUE_ID "),
    "quadlets": row_line(feat, "Scenario: GET_MILAN_INFO reports protocol_version 1"),
    "junk": row_line(feat, "| 0xDEAD   | 20     | 0      | 32 "),
    "cdl24": row_line(feat, "| 24     | 0      | 32 "),
    "cdl112": row_line(feat, "| 112    | 0      | 32 "),
    "gate": row_line(feat, "Scenario: the served MVU command types are the ones"),
}

ARMS = []


def arm(name, expected):
    def deco(fn):
        ARMS.append((name, fn, sorted(expected)))
        return fn
    return deco


@arm("control_unmodified", [])
def _(root):
    pass


@arm("served_mvu_adds_0x0002", [L["row0002"], L["gate"]])
def _(root):
    sub(root / "tests/steps/aecp_engine_steps.py",
        '    0x0000: dict(name="GET_MILAN_INFO", clause="Milan 5.4.4.1"),\n',
        '    0x0000: dict(name="GET_MILAN_INFO", clause="Milan 5.4.4.1"),\n'
        '    0x0002: dict(name="GET_SYSTEM_UNIQUE_ID", clause="Milan 5.4.4.3"),\n')


@arm("mvu_dispatch_unreachable",
     [L["row0000"], L["quadlets"], L["junk"], L["cdl24"], L["cdl112"]])
def _(root):
    sub(root / "tests/steps/aecp_engine_model.py",
        "cmd_payload) in self.mvu_served:",
        "cmd_payload) in ():")


@arm("engine_copy_declares_system_unique_id", [L["gate"]])
def _(root):
    sub(root / "protocol-processor/hdl/aecp/KL_aecp_engine.sv",
        "  localparam logic [15:0] MVU_GET_MILAN_INFO_C = 16'h0000;\n",
        "  localparam logic [15:0] MVU_GET_MILAN_INFO_C = 16'h0000;\n"
        "  localparam logic [15:0] MVU_GET_SYSTEM_UNIQUE_ID_C = 16'h0002;\n")


results = []
for name, fn, expected in ARMS:
    root = probe_tree(name)
    fn(root)
    rc, fails, tally = failing_lines(root)
    ok = (fails == expected) and ((rc == 0) == (not expected))
    results.append(ok)
    print(f"ARM {name}: rc={rc} failing={fails} expected={expected} "
          f"{'EXACT' if ok else 'MISMATCH'} | {' ; '.join(tally)}")
    shutil.rmtree(root)

# em-dash arm on the composed roadmap row
clone = SCRATCH / "probe_emdash"
if clone.exists():
    shutil.rmtree(clone)
head = subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"],
                      capture_output=True, text=True, check=True).stdout.strip()
subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", str(REPO),
                str(clone)], check=True)
subprocess.run(["git", "-C", str(clone), "checkout", "-q", "--detach", head],
               check=True)
road = clone / "docs/MILAN_V12_ROADMAP.md"
for label, edit in (("control", False), ("emdash_in_composed_row", True)):
    if edit:
        sub(road, "so the suite cannot go stale |\n",
            "so the suite cannot go stale — probe |\n")
        subprocess.run(["git", "-C", str(clone), "-c", "user.name=probe",
                        "-c", "user.email=probe@invalid", "commit", "-q", "-am",
                        "probe"], check=True)
    out = subprocess.run([sys.executable, "-B", "scripts/check_em_dash.py",
                          "--base", PARENT], cwd=clone, capture_output=True,
                         text=True)
    first = (out.stdout + out.stderr).strip().splitlines()
    summary = [l for l in first if "finding" in l][-1:] or first[-1:]
    want_fail = edit
    ok = (out.returncode != 0) == want_fail
    results.append(ok)
    print(f"ARM em_dash_{label}: rc={out.returncode} {'EXACT' if ok else 'MISMATCH'}"
          f" | {' '.join(summary)}")
shutil.rmtree(clone)

print(f"SUMMARY {sum(results)}/{len(results)} arms exact")
sys.exit(0 if all(results) else 1)
