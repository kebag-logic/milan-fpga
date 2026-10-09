[R580] POSITIVE - exact head 6904af6b79aae0566e6e47979223f54b8ba0eb6f

Round R580-3, internal cleared-context review of PR #702 (issue #640, lane M0s step 2). This is a delta review, d10aee62 to 6904af6b (one commit), answering round-3 assignment [6089650427](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6089650427). Tree `c0e859f0fccbb7af27f75d14e321f9a3e27e361f`. Earlier rounds stand for files the delta does not touch.

All five lenses were applied and are CLEAN at this head. No BLOCKER, MAJOR, MINOR or RESIDUE is open. One optional SUGGESTION is recorded. Both prior findings are RESOLVED: R580-2-F1 = R581-2-F1 and R580-2-R1 = R581-2-R1.

## Scope reconstructed

- **Authorities:**
  - AGENTS.md sections 6-7.
  - Issue #640: body, M0s step assignment 6086604096, round-2 assignment 6087671877, P2 ruling 6089329720, round-3 assignment 6089650427.
  - Author REVIEW READY 6089897327.
  - Gate documented usage `syn/ooc/pp_resource_gate.py:48-49`.
  - Hosted step `.github/workflows/rtl-fast.yml:200-216`.
- **Delta (`git diff --name-only d10aee62..6904af6b`):**
  - `syn/ooc/pp_placement_selftest.py` (+10/-5).
  - `syn/ooc/pp_resource_gate_mutants.py` (+2).
  - No product code, documentation, HDL, firmware or gitlink changed.
- **What the delta does:**
  - `pp_placement_selftest.py:244-260` calls the gate as `check <directory> --endpoint ...` and `record <directory> --endpoint ... --write`. This is the documented order.
  - `:254-255` adds a printed-`record` arm: each wrong population except an absent wrapper exits 0 and prints the record.
  - `pp_resource_gate_mutants.py:288-289` adds the mutant "all-fabric population judged in a printed record".

## Evidence (receipts in this packet; commands in `scripts/run_r580_3.sh`)

Interpreters:
- CPython 3.12.3 at `$VALIDATION_TOOLS/uvpy/cpython-3.12.3-linux-x86_64-gnu/bin/python3.12`, the hosted ubuntu-24.04 system interpreter.
- Host CPython 3.14.7.

Every row below exited 0 on both interpreters unless stated.

| Check | 3.12.3 | 3.14.7 | Receipt |
|---|---|---|---|
| `pp_resource_gate.py --selftest` | rc 0, 138 `placement gate` lines, 21 of them `printed record` | same | `receipts/gates/gate_selftest_{py3123,host}.log` |
| `pp_resource_gate_mutants.py` | control passes, 192 of 192 fail | same | `receipts/gates/gate_mutants_*.log` |
| `pp_baseline_mutants.py` | control passes, 45 of 45 fail | same | `receipts/gates/baseline_mutants_*.log` |
| `check-baseline` | `baseline PASS: 3 endpoints` | same | `receipts/gates/check_baseline_*.log` |
| `pp_baseline.py --selftest`, `pp_baseline_reports_selftest.py`, `ooc_tcl_selftest.py`, `dp_srcs.py --selftest` plus both tops | rc 0 | rc 0 | `receipts/gates/*_{py3123,host}.log` |
| P1, R580-1 `probe_mutants.py`, unmodified (sha256 `41bcca25...`, R580-1 manifest) | 29 of 34; survivors G1, G3, G8, G13, B9, unchanged | same | `receipts/gates/P1_probe_mutants_*.log` |
| P4, R580-2 `probe_default_population.py`, unmodified (sha256 `34c7074a...`), with the published route-1x1 hierarchy report (blob `61e2c63c`, 645-review-evidence `b17c8f88`) | 0 unexpected | 0 unexpected | `receipts/gates/P4_default_population_*.log` |
| P10, R580-2 `probe_cli_order.py`, unmodified | documented order exits 2 naming roles; option-first order exits through argparse | both orders exit 2 naming roles | `receipts/gates/P10_cli_order_*.log` |
| P11, this round's `probe_order_plants.py` | 11 variants, 0 unexpected | 11 variants, 0 unexpected | `receipts/gates/P11_order_plants_*.log` |
| Order scan, `order_scan.py` (AST walk of `syn/**` and `scripts/**`) | 24 command-word sites. The single flagged site is the `judged` tuple at `pp_placement_selftest.py:244`, which `:249` and `:259` reassemble directory-first. | - | `receipts/order_scan.log` |
| Legacy self-test lines, `git archive` base, d10aee62 and head | 212 non-placement, non-fuzz lines; digest `063d1e8b7d097ce8` at base and head. d10aee62 rc 1; its 212 lines are present, interleaved with the argparse usage and traceback. | same digest at all three | `receipts/legacy_lines.txt` |
| Docs, TOC, anchors, em-dash vs base, idiom, hygiene, fail-fast, naming, test-evidence, `git diff --check` | - | rc 0 | `receipts/gates/*.log` |
| Tree after probes | bytes, modes and index equal HEAD; 0 untracked; required gitlinks protocol-processor, gptp-processor and verilog-axis match | - | `receipts/tree_integrity.txt` |

**P11 plants (both interpreters):**
- **Old order restored.** Restoring the old order in either arm or both fails the gate self-test on 3.12.3 with the hosted assertion (`got (2, ['exited through argparse'])`). It passes on 3.14.7. This reproduces the defect class and shows it depends on the interpreter.
- **`--write` dropped from the record arm.** This fails on both interpreters, because the record prints with exit 0 where exit 2 is required. So the `record --write` refusal is still judged.
- **Gate ignores `record --write` population.** Detected.
- **Gate judges a printed record.** Detected.
- **Printed-record arm removed together with that gate mutant.** The mutant survives, so the new arm is its only detector.
- **Printed-record arm extended to `wrapper absent`.** This fails with the root refusal. So the `:254` exclusion is required and accurate, and it does not hide a passing case.

**Hosted, exact head `6904af6b`:**
- The pull_request event checks out merge `6c2fa69` of the head into dev `8b61b709`.
- Run 37996307323 `rtl-fast` is completed/success. Its jobs `yosys-elaboration` 114043347540, `firmware-unit`, `verilator-lint`, `bdd-conformance`, `changes` and the aggregate `rtl-fast` 114052372284 all succeeded.
- The `yosys-elaboration` log (`receipts/hosted/yosys-elaboration_114043347540.log`, image ubuntu-24.04) executed:
  - 138 placement-gate lines, 21 of them printed-record;
  - `placement gate: unchanged acceptance schema, record and policy PASS`;
  - `resource gate mutants: control passes, all 192 mutants fail`;
  - `baseline PASS: 3 endpoints`;
  - the later `ooc_selftest`, `guard_selftest` and `cache_selftest` steps.
- `docs` and `elaborate` succeeded.
- In `rtl-full` run 37996307246, Verilator shards 1, 2 and 4 were still pending at 22:26Z. `Physical gPTP` was skipped, which is a skipped context and not a result (`receipts/hosted/hosted_checks.tsv`).
- The hosted interpreter version is not printed in the log. It is inferred from the image.

## Findings

### R580-3-S1 - SUGGESTION - Tests - the order class is caught only by an older-parser interpreter

- **Where:** `syn/ooc/pp_resource_gate_selftest.py:569-584` (`cli()`), and its use at `syn/ooc/pp_placement_selftest.py:249,259`.
- **Evidence:** P11 "old order" variants pass on CPython 3.14.7 and fail only on 3.12.3. The author records the same limit.
- **Impact:** low. Hosted `yosys-elaboration` catches the class. A local run on a newer interpreter does not.
- **Optional change:** a self-test-only check in `cli()` that refuses an option word between the command word and the directory. This would make the class fail on every interpreter. It is not required by the assignment, and the author declined it with a reason.

No other finding.

## Prior findings at this head

| Finding | State at 6904af6b | Evidence |
|---|---|---|
| R580-2-F1 (BLOCKER, Tests) = R581-2-F1 (MAJOR, Tests, Robustness): self-test option-before-directory order fails on the hosted interpreter | **RESOLVED** | `pp_placement_selftest.py:244-260` is directory-first. 3.12.3: self-test rc 0 with 138 placement lines; campaign 192/192 with control; `check-baseline`; P1 and P4 unmodified. Hosted `yosys-elaboration` and `rtl-fast` succeeded. No assertion weakened: P11 "record arm without --write" and "gate ignores record --write" both fail; baseline-byte checks at `:252-253,262-263`. The order scan finds no other option-first site. |
| R580-2-R1 = R581-2-R1 (RESIDUE): PR body still requested the P2 decision | **RESOLVED** | The PR body's Known-limitations bullet reads "The manager ruled this difference expected (#640 comment 6089329720); see Round 2." The Round 2 lead reads "**P2 `fuzz` and self-test line prefix (ruled expected in #640 comment 6089329720).**" (`receipts/pr702_body.md`). |
| R580-2-S1 (SUGGESTION): printed record unjudged with no control | **Adopted** | `:254-255` and mutant `pp_resource_gate_mutants.py:288`. P11 shows the arm is that mutant's detector. |
| R580-1-S2 (SUGGESTION): census breadth | Optional, not adopted, with reason; not a finding | Unchanged |
| R581-1-R1, R580-1-F1, R580-1-F2 | Resolved in earlier rounds; files unchanged by this delta except the self-test arms reviewed above | R580-2 and R581-2 tables |

## Lens results

```text
[R580] PASS Conformance - syn/ooc/pp_placement_selftest.py:242-260 against pp_resource_gate.py:48-49 and assignment 6089650427 items 1-2; receipts/order_scan.log; receipts/pr702_body.md - documented order in both arms, every other driver checked, ruling stated as decided, 3.12.3 runs as required
[R580] PASS RTL - git diff --name-only d10aee62..6904af6b (two Python test/driver files; no hdl/, firmware, gitlink or gate product change); pp_resource_gate.py:715-727 parser and :743-764 printing guard unchanged; receipts/tree_integrity.txt - tooling interface contract unchanged
[R580] PASS Robustness - receipts/gates/P11_order_plants_{py3123,host}.log, P4_*, P10_*, gate_selftest_py3123.log - interpreter-dependent parsing now avoided; wrapper-absent exclusion required and accurate; baseline bytes unchanged on every refusal; real route report 0 unexpected
[R580] PASS Tests - pp_placement_selftest.py:244-260, pp_resource_gate_mutants.py:288-289; receipts/gates/gate_mutants_*.log (192/192 + control on both), P1_* (29/34 unchanged), P11_* (11/11), legacy_lines.txt; hosted yosys-elaboration log - new arm can fail for the defect it targets; no assertion weakened
[R580] PASS Docs - docs/testing/PP_SHADOW_BASELINE_RECIPE.md:234-238, syn/ooc/pp_resource_gate.py:21-23, pp_placement_selftest.py:242-243,254 comments, receipts/pr702_body.md Round 3; docs gates rc 0 - the printed-record rule the new arm pins was already documented; PR body counts (138, 192, 212) reproduced
```

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `pp_placement_selftest.py:242-260`; `pp_resource_gate.py:48-49`; issue #640 6089650427, 6089329720; PR body; order scan | R580-3 | `6904af6b79aae0566e6e47979223f54b8ba0eb6f` |
| RTL | CLEAN | delta file list (no HDL/firmware/gitlink/product change); parser `pp_resource_gate.py:715-727`; required gitlinks | R580-3 | `6904af6b79aae0566e6e47979223f54b8ba0eb6f` |
| Robustness | CLEAN | P11, P4 (real route-1x1 report), P10 on 3.12.3 and 3.14.7; baseline-byte checks `:252-253,262-263` | R580-3 | `6904af6b79aae0566e6e47979223f54b8ba0eb6f` |
| Tests | CLEAN (S1 optional) | gate campaign 192/192 on both interpreters and hosted; recipe campaign 45/45; P1; P11; legacy lines | R580-3 | `6904af6b79aae0566e6e47979223f54b8ba0eb6f` |
| Docs | CLEAN | recipe page `:234-238`; gate docstring `:21-23`; PR body Known limitations, Round 2 lead, Round 3; docs gates | R580-3 | `6904af6b79aae0566e6e47979223f54b8ba0eb6f` |

## Real limits

- **Hosted provenance.** Hosted execution ran on the pull_request merge ref `6c2fa69` (head into dev `8b61b709`), not on the source head alone. The hosted Python version is inferred from the ubuntu-24.04 image and is not printed.
- **Older parsers.** No CPython 3.11 was available locally. The older-parser case was exercised only on 3.12.3, which is the hosted interpreter.
- **Probes not rerun.** P2 and P3 were not rerun. In their place, the 212 legacy non-fuzz self-test lines were compared base to head on both interpreters. The gate product code is unchanged since d10aee62.
- **Hosted-only steps.** `syn/yosys/ooc_selftest.py` and `cache_selftest.py` were not run locally; they are hosted-green only.
- **Not run.** No Vivado route, no selected-placement measurement and no re-record were performed. Physical calibration was NOT RUN, and skipped field contexts are not hardware proof.
- **No manager bank.** No manager source bank exists at this head, and none is claimed.

## Pending manager duties

- Hosted/act acceptance at the exact head, including the `rtl-full` Verilator shards 1, 2 and 4 that were still pending at 22:26Z.
- The current-dev merge candidate (source base `7c1b52be`, live dev `8b61b709`) with builder and native banks, linked on the PR when published.
- The external review R581-3. Its result is unread here and independent.
- Residue checklist: nothing new from this round. R580-2-R1 is resolved in the body.
- R580-3-S1 is optional.

R580-3 FINISHED
