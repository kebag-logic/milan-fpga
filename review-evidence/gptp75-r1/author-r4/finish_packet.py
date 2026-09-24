"""Write the handoff only after all assigned gates and comparisons pass."""
import hashlib
import json
from pathlib import Path
import subprocess

out = Path(__file__).resolve().parent
commits = json.loads((out / "commits.json").read_text())
source = commits["source"]["head"]
consumer = commits["consumer"]["head"]
comparisons = json.loads((out / "comparisons.json").read_text())
assert comparisons and all(row["identical"] for row in comparisons)
labels = ["before-engine", "before-mutants", "before-source-evidence", "before-source-selftest",
          "after-source-evidence", "after-source-selftest", "after-make", "after-mutants",
          "parent-cpp", "parent-python", "parent-xvlog", "parent-source-lists", "parent-builder", "parent-shadow"]
receipts = {label: json.loads((out / (label + ".receipt.json")).read_text()) for label in labels}
assert all(receipt["returncode"] == 0 for receipt in receipts.values())
rows = ["gate\tcommand\trc\tseconds"]
for label, receipt in receipts.items():
    rows.append("\t".join((label, " ".join(receipt["command"]), str(receipt["returncode"]), str(receipt["elapsed_seconds"]))))
(out / "gate-results.tsv").write_text("\n".join(rows) + "\n")
for name, before, after in [
    ("engine-checks", "before-engine-checks.txt", "after-engine-checks.txt"),
    ("mutant-verdicts", "before-mutant-verdicts.tsv", "after-mutant-verdicts.tsv"),
    ("mutant-gate", "before-mutant-gate-table.txt", "after-mutant-gate-table.txt"),
    ("source-evidence", "before-source-evidence.stdout.log", "after-source-evidence.stdout.log"),
    ("source-selftest", "before-source-selftest.stdout.log", "after-source-selftest.stdout.log")]:
    with (out / (name + ".diff")).open("w") as diff:
        result = subprocess.run(["diff", "-u", str(out / before), str(out / after)], stdout=diff, stderr=subprocess.STDOUT, timeout=60)
    assert result.returncode == 0, name
make_log = (out / "after-make.stdout.log").read_text()
assert "SKIP" not in make_log
phase_lengths = json.loads((out / "scope-verification.json").read_text())["phase_lines"]
phase_table = "\n".join("| `" + name + "` | " + str(length) + " |" for name, length in phase_lengths.items())
parent_table = "\n".join("| `" + " ".join(receipts[name]["command"]) + "` | 0 | [receipt](" + name + ".receipt.json) |" for name in labels if name.startswith("parent-"))
check_hash = hashlib.sha256((out / "before-engine-checks.txt").read_bytes()).hexdigest()
mutant_hash = hashlib.sha256((out / "before-mutant-verdicts.tsv").read_bytes()).hexdigest()
body = (out / "PR-BODY.md").read_text()
assert "ROUND4_RESULTS_PENDING" in body
round4 = f"""- Split `exercise_the_slew_level_contract()` into eight named phases. The coordinator is 10 lines; the phases are 13–30 lines. Expanding their bodies in call order reproduces every original statement, with no changes to checks, stimuli or expected values.
- Annotated `check`, `selftest` and `main` in `scripts/check_source_evidence.py`, and added the `main` docstring. The ledger still reports 20 exact anchors and 0 findings; its seven-arm self-test and all output bytes are unchanged.
- Recorded the complete engine check list before and after: 1,613 checks on each of three images, with all 4,839 names and their order byte-identical. Both complete mutation runs catch all 33 mutants on the same checks. Their verdict tables, return codes and full ordered failure lists are identical, including all six required slew checks.
- `make -j8` and the separate `make -C tb/verilator/engine mutants` return 0. All repository suites execute, with no skips.
- Fetched local candidate `{source}` into the parent consumer and committed only its gitlink as `{consumer}`. The consumer is based on `dev` `573f0052` plus the supplied local pin commit. All six assigned checks return 0: C++ idioms, Python idioms, source parsing, source lists, builder, and the shadow suite with its mutation controls. The builder reports one calibration arm not run because its expected utilization report is absent; that arm is not covered by this result.

Round 4 changes only the two assigned source files. RTL, microcode, ROM images, mutation definitions and documentation claims are unchanged. The candidate and consumer pin are local; the parent connection work remains with #545."""
body = body.replace("ROUND4_RESULTS_PENDING", round4)
body = body.replace("Validation: every required local gate returns 0, with no skipped suites.", "Validation: the repository's default gate set and all six assigned parent consumer gates return 0. The repository suite bank has no skipped suites.")
(out / "PR-BODY.md").write_text(body)
handoff = f"""[A281] Round 4 handoff for FPGA-gPTP #75 / PR #76

Head: `{source}` on `75-slew-active`.
Baseline: `3face0914efd9d5e71f36da7e30108cfe09c837d`.
Commit: `{commits['source']['subject']}`. One line, no body or trailers.

The [assignment](https://github.com/Mister-M-alt/FPGA-gPTP/issues/75#issuecomment-5821534416) is implemented in exactly two files. [The patch](round4.patch) splits the lifecycle scenario into named phases and adds the requested Python signatures and main docstring. All other 102 tracked files match the baseline, including RTL, the generator, ROM images, mutation definitions and documentation. [Scope verification](scope-verification.json) also proves that expanding the phases reproduces the original statements in order.

## Phase sizes

| Function | Lines, including declaration and closing brace |
|---|---:|
{phase_table}

## Before and after

| Evidence | Before | After | Comparison |
|---|---|---|---|
| Whole engine suite, each of three images | 1,613 PASS, 0 FAIL | 1,613 PASS, 0 FAIL | All 4,839 names and order identical |
| Engine mutation campaign | 33 caught; positive control passes | 33 caught; positive control passes | Same killing checks, return codes and full ordered failure lists |
| Required slew controls | 6 caught at their required named checks | 6 caught at their required named checks | Identical |
| Source-evidence ledger | 20 exact, 0 findings | 20 exact, 0 findings | stdout and stderr byte-identical |
| Ledger self-test | PASS, 7 arms | PASS, 7 arms | stdout and stderr byte-identical |

- Engine lists: [before](before-engine-checks.txt), [after](after-engine-checks.txt). Shared SHA-256: `{check_hash}`.
- Mutant verdict tables: [before](before-mutant-verdicts.tsv), [after](after-mutant-verdicts.tsv). Shared SHA-256: `{mutant_hash}`.
- The shipped campaign tables are [before](before-mutant-gate-table.txt) and [after](after-mutant-gate-table.txt); each has 34 PASS, 0 FAIL including the positive control.
- [All comparisons](comparisons.json) pass. The five comparison diffs for engine checks, mutant verdicts, shipped mutant output, ledger output and self-test output are empty; each direct comparison returns 0. The Python executable syntax trees match after excluding annotations and the new docstring.

The production harness prints only failures and its tally. [The trace script](trace_checks.py) therefore adds one check-name print in `expect()` in a temporary source export, then runs all three images. It changes no stimulus, expectation, counter or simulated clock operation. Both ordinary engine runs also pass. Source exports and builds stay outside this packet.

[The observer](observer/sitecustomize.py) copies the mutation campaign's already-captured output, preserving each subprocess result and the shipped verdict logic. Both observed campaigns invoke the unchanged `make -C tb/verilator/engine mutants`. The separate unobserved `make -j8` also runs the full campaign. The baseline's last 22 generator mutations reuse its already-built control executable; the live C++ edit occurred only after the final baseline C++ variant had finished, as recorded in [the reuse boundary receipt](baseline-reuse-boundary.json).

## Repository gates

`make -j8` returns 0 with no skipped suites. It runs the contract check; arithmetic, parser, engine, adapter, packet-generator and timestamp-tag suites; engine, adapter and packet-generator mutation controls; both lint targets; and documentation, diagram and source-evidence checks and self-tests. The candidate tracks no CI workflow files. The separate `make -C tb/verilator/engine mutants` also returns 0.

[Gate inventory](gate-inventory.json), [all commands and return codes](gate-results.tsv), [main gate receipt](after-make.receipt.json), [mutation gate receipt](after-mutants.receipt.json), and their adjacent stdout/stderr logs record the results. Each command runs as a foreground subprocess, without a shell pipeline, with a three-hour deadline. Existing dependencies are identified in [environment.json](environment.json).

## Parent consumer

The supplied parent was `584a8c17d67d9c86df3e18913e34e237f58cacc7`, on `dev` `573f0052a0e4412e81f0845438fcec2086ce5d55` plus one local gitlink commit. The new source head was fetched locally into `gptp-processor`, checked out there, and pinned by local parent commit `{consumer}`. That commit changes only the gitlink and has a one-line message. [Commit details](commits.json).

| Command from the consumer | rc | Evidence |
|---|---:|---|
{parent_table}

The shadow suite passes 309 checks and all 9 mutation controls. Its existing missing-port warnings include `phc_slew_active_o`; connecting that port remains #545 work. The C++ gate reports zero long functions. The Python gate reports zero unannotated and zero undocumented public functions. The source parser matches its four existing findings in the other processor; it reports no new findings. The builder returns 0 but declares gate 11 not run: its calibration comparison needs the absent mf48 utilization report. This result does not cover that arm.

## Review handoff

The updated [PR body](PR-BODY.md) starts with `[A281]`, retains `Closes #75`, and includes Round 4. The assignment calls for R304's delta review at the new head; R305-3 remains the recorded positive review of the ancestor `3face091`. This handoff supplies author evidence, not a review verdict.

The parent #545 connection, timing-policy decisions and hardware validation remain separate work. No push, PR edit, merge or hardware operation was performed.
"""
(out / "HANDOFF.md").write_text(handoff)
for name in ("HANDOFF.md", "PR-BODY.md"):
    text = (out / name).read_text()
    assert text.startswith("[A281]") and "/home/" not in text and "PENDING" not in text
print("Wrote HANDOFF.md, PR-BODY.md, gate-results.tsv and five empty diffs.")
