[R902] NEGATIVE - exact head 66b4def34dcbc0d371ce4eb339d3d0226875befa

Internal cleared-context review R902-1 of issue #983 / PR #986. Tree `b5bba478993ff213d953aa73ca5fecc8d5476c8a`; source base `854bd7236792ce1adbd10c43b13a6a5002ad3bb6`; two commits (`677d605f`, `66b4def3`), five files. All five lenses were applied. One BLOCKER is open (Conformance, RTL, Tests). Robustness and Docs are clean. There are two RESIDUE items and two SUGGESTIONs. This is a source-head review. It does not validate the current-dev merge candidate.

## Authorities and independence

I reconstructed the task from these sources: AGENTS.md; CONTRIBUTING.md (sections 6 and 6.1); docs/README.md; the frozen body of issue #983 and its two public REVIEW READY comments; the manager's scope ruling (ti-sitara-am65x-bsp#29 issuecomment-7096504049); the authorities named by the diff (ENDSTATION_BUILDER sections 3 and 6, `ctrl_loop.h` THE SHAPES, and the shape-table contract `tb/verilator/ctrl_service_budget/shape_costs.py` with its README); then `git diff 854bd723..66b4def3` and its history; then the published author packet's file listing at `7095fc64`. I did not read any private author material, any lane scratchpad, or the handoff file in the packet. I read prior public findings on the PR (R900-1, R900-2) only after writing my own draft verdict and ledger. No other reviewer's packet was read.

## Findings

### R902-1-F1 BLOCKER - Conformance, RTL, Tests

**Where:** `sw/firmware/ctrl/loop/ctrl_loop.h:396-422`, the host comment block and the `#elif defined(CTRL_HOST_PLATFORM) && CTRL_LOOP_SHAPE(1u, 1u, 2u)` row inside THE SHAPES chain. The reader it breaks is `tb/verilator/ctrl_service_budget/shape_costs.py:102-137` (`listed()`).

**Title:** The host row breaks the tree's own reader of THE SHAPES. The load gate, the flip check, the shape-table check and self-test, and the budget self-test all crash at the head.

**Requirement and evidence.**

- Issue #983 freezes two things: "The FPGA scheduler-shape guard and its rows are untouched" and "FPGA profile validation is unchanged".
- `shape_costs.listed()` is the tree's reader of the table. Its documented contract is "a table that is not one #if chain of CTRL_LOOP_SHAPE tests, each stating NAMES and BOUNDS once as plain numbers ... is refused".
- At the head, the reader stops inside the (2, 9, 9) row on the first new comment line: `ValueError: ctrl_loop.h states "// THE HOST PLATFORM's shape (#983), ..." for the shape (2, 9, 9)`. If the comment were moved, the `#elif defined(...) && ...` line would still fail its head regex.
- Results at base and head, each run in a disposable tree extracted from the revision with the pinned submodules linked:

| Command | Base `854bd723` | Head `66b4def3` |
|---|---|---|
| `shape_costs.py --check` | PASS, rc 0 | ValueError, rc 1 |
| `shape_costs.py --selftest` | 25/25 controls refused, rc 0 | ValueError, rc 1 |
| `load_grade.py --check` | PASS, rc 0 | ValueError, rc 1 |
| `flip_grade.py --check --point 1x1/1if` | PASS, rc 0 | ValueError, rc 1 |
| `flip_grade.py --check` (all points) | grades and FAILs 8x8/2if, rc 1 (the documented base state, a check apart from the merge gates) | ValueError before any grading, rc 1 |
| `run.py --self-test` | still grading controls at the 560 s bound, rc 124 | ValueError at start, rc 1 |

- `probe_shape_costs.py` reads each revision's `ctrl_loop.h`. `listed()` succeeds at base and raises at `677d605f` and at `66b4def3`, so the defect has been present since round 1.
- The budget README (line 212) says the load gate holds 1x1/1if "for merge". `docs/design/SPLIT_CONTROL_MEMORY.md:2471-2473` and `:2550` record `load_grade.py --check` and `flip_grade.py --check` as merge legs.
- The compiler view really is unchanged. `preproc_shapes.sh` compares 12 points (no shape header, 1x1, 8x8 and the three Arty configs, at MBX_N_IF 1 and 2): the macros are identical, and the only diagnostic difference is the `#error` line number, 397 to 424. But the tree reads this table as text, and neither gate 41 nor any hosted workflow (`.github/workflows/*.yml` has no reference to `ctrl_service_budget`) runs that reader. The PR's evidence ("the arms that read THE SHAPES ... passed") therefore misses the reader that refuses it.

**Impact:**

- At the head, every FPGA service-budget figure that THE SHAPES governs can no longer be checked: the 1x1/1if load ceiling, the flip rows and the table's own rules. So the guard's rows are no longer held, even though their text is unchanged.
- The break is silent in hosted CI, so it would merge unseen. Any later change to an FPGA row would then also go ungraded.

**Required outcome:**

- At the corrected head, `shape_costs.py --check` and `--selftest`, `load_grade.py --check` and `flip_grade.py --check --point 1x1/1if` reach the base verdicts with the four FPGA rows read unchanged. `flip_grade.py --check` and `run.py --self-test` must grade as at base rather than raise.
- The host row stays selectable only under `CTRL_HOST_PLATFORM`, and no reader may take it as an FPGA shape.
- A check in this PR's gates must fail on this defect.
- If the fix needs the shape-table reader itself to change, that file sits under the frozen "guard untouched" scope. Publish the question and get the manager's decision before choosing (AGENTS.md section 2).

**Verification:**

- Re-run `scripts/probe_shape_costs.py` and the five commands above at the corrected head and compare them with the base receipts.
- Mutation: restore the `66b4def3` placement of the row. The new check must fail and `listed()` must raise again.
- Gate 41 must stay green.

### R902-1-R1 RESIDUE - Docs

**Where:** `docs/ENDSTATION_BUILDER.md:1233-1241`, and the row 5d reference at `:1031`.

**Title:** Section 6's key rows are labelled `6a` to `6i`, which collides with section 3's rows `6` and `6a`.

**Evidence:** Section 3 row `6a` (line 1033) is `platform.mac_address`, and row 3 (line 1021) cites "row 6a's MAC". Section 6 row `6a` (line 1233) is `board.target`. Gate 32 and gate 41 read keys from the second cell, not labels (`test_builder.py:28807-28828`), so this changes no test.

**Impact:** Wording only. A reader can resolve "row 6a" to the wrong table.

**Exact fix:** Give the section 6 rows labels that cannot collide with section 3 (for example `H1` to `H9`), and change row 5d's "(section 6, row 6b)" to the new label of `board.gptp_owner`.

**Verification:** `grep -n '^| 6[a-i] |' docs/ENDSTATION_BUILDER.md` lists only section 3 rows. Gates 32 and 41 still pass.

### R902-1-R2 RESIDUE - PR body (retains R900-2-R1)

**Where:** PR #986 body, the Status paragraph and the checkout command comment.

**Evidence:** The live PR head is `66b4def34dcbc0d371ce4eb339d3d0226875befa`, yet the body says "Published head: `677d605f...`" and "Round 2's head ... becomes the published head when it is pushed". The checkout comment still says "once pushed".

**Impact:** Stale publication prose only.

**Exact fix:** Replace the Status paragraph that begins "Published head:" with: "Published head: `66b4def34dcbc0d371ce4eb339d3d0226875befa`. The evidence below is local source-head evidence; hosted acceptance is tracked separately." Then remove "once pushed" from the checkout comment. Keep the incomplete-gate disclosures.

**Verification:** Compare the body with the PR head.

### R902-1-S1 SUGGESTION - Tests

**Where:** `sw/builder/test_builder.py:30691-30699`.

**Point:** Gate 41 checks "the macro moves no FPGA row" only at the contract's MBX_N_IF 1, so the two-interface rows are not exercised. `preproc_shapes.sh` shows them identical at MBX_N_IF 2. An MBX_N_IF 2 case in the gate would cover all four rows.

### R902-1-S2 SUGGESTION - Robustness

**Where:** `_gptp_clock_accuracy_key`, which the host path reuses.

**Point:** `gptp.clock_accuracy: 'x'` raises ValueError rather than ConfigError. This is also the base behaviour on an FPGA config (`fpga_parity_probe.txt`), so it is not new here. It could join the disclosed `board: null` / integer TypeError follow-up as a separate Issue.

## Prior public findings at this head

| Prior ID | Severity and lenses | Disposition at 66b4def3 |
|---|---|---|
| R900-1-F1 | MINOR; Conformance, Robustness, Tests | RESOLVED. `endstation_builder.py:4802` reads the target with `_req`. `prior_f1_probe.txt` shows ConfigError "board: missing required key 'target'" for `[]`, `""` and `["ax7101"]` at base and head. Gate 42 passes 31/31 and carries the three rows. |
| R900-1-F2 | MINOR; Docs | RESOLVED. ENDSTATION_BUILDER section 6 (lines 1245-1265) and the `load_config` comment (`endstation_builder.py:4813-4818`) state the widest advertised `channels_per_frame`, shared at `clocking.sampling_rate_hz`, matching `framer_declared_channels`. Gate 41 holds 217 against 73. |
| R900-1-R1 / R900-2-R1 | RESIDUE; Docs | RETAINED as R902-1-R2. |

R902-1-F1 is new. It contradicts the RTL and Tests PASS results of R900-1 (at `677d605f`, where the defect was already present) and of R900-2 (at this head). Neither of those rounds ran the shape-table reader.

## Five-lens results

- **Conformance: UNCLEAN, F1.**
  - What holds: the host example generates through the unchanged AEM checks (gate 41 passes). The three firmware generators run with rc 0 and give ADP sources 1 and sinks 2, talker capabilities 0x4001 (no MEDIA_CLOCK_SOURCE, since there is no CRF output), listener capabilities 0x4801 and entity capabilities 0xC588 (as the FPGA 1x1); `CTRL_SRP_SOURCES 1u` and `CTRL_SRP_SINKS 2u`; and 2 STREAM_INPUTs, 1 STREAM_OUTPUT, 1 AVB_INTERFACE and 1 CLOCK_DOMAIN (`receipts/host_*.h`). `build()` refuses the profile by name (rc 1, `host_generators_head.txt`). This matches the issue's inventory and the manager ruling (Milan v1.2 7.2.2 and 7.2.3).
  - What fails: "guard and its rows untouched" and "FPGA profile validation unchanged" do not hold in effect, because the tree's checks of those rows refuse the head (F1).

- **RTL: UNCLEAN, F1.**
  - What holds: the diff touches no HDL, no SoC source and no firmware C. It changes no file mode (all 100644) and moves no submodule gitlink (`integrity.txt`). `ctrl_loop.h` is macro-identical at 12 points (`preproc_shapes.txt`). The (1, 1, 2) row is reachable only with `CTRL_HOST_PLATFORM`, and no build input names that macro (gate 41; mutant m1 drops the guard and gate 41 fails).
  - What fails: the firmware's interface contract for THE SHAPES, as `shape_costs.listed()` and its README line 147 define it, is broken (F1).

- **Robustness: CLEAN.**
  - `host_robustness_probe.txt` runs 46 one-key edits. Every host fabric declaration, every unstated or out-of-range gPTP field, wrong types (bool, float, list), the link rate, queue count, width and word length, role pools, the all-fabric placement and a `soc:` section are refused through ConfigError. The CRF-input (7.2.2) and CRF-output (7.2.3) rules and the domain-0 rule fire on the host profile. An FPGA config still refuses a gptp_owner, `fabric_gptp: false`, a missing `gptp:`, retargeting to host, and `usb_audio`.
  - The only crashes (`board: null` or an integer, and a non-integer `clock_accuracy`) are byte-for-byte base behaviour on the FPGA path (`fpga_parity_probe.txt`). They are disclosed or recorded as S2.
  - Mutant m2 removes the FPGA gptp_owner refusal, and gate 42 fails.

- **Tests: UNCLEAN, F1.**
  - What holds: gates 32, 41 and 42 pass in the clone (116 == 116 keys; 31/31 plants), and `test_bad_configs_rejected` passes. Mutants m1 and m2 are each killed by their gate.
  - What fails: existing regressions in the budget harness are no longer green at the head, and the new gate does not cover the reader that breaks (F1).

- **Docs: CLEAN; one RESIDUE (R1); R2 is PR-body residue.**
  - ENDSTATION_BUILDER section 6 describes the profile, what it feeds, what is unchanged, the keys that differ, the TSpec rule and its clause, the duty to substitute the MAC, and the host-only shape row. Row 5d documents the new FPGA refusal. The section 3 counts read 75 rows and 116 keys (68 keyed rows plus 7 derived or generator-owned rows, as gate 32 reports).
  - These gates pass: `docs_check` (0 findings over 223 md and 1911 scrubbed files), `check_em_dash --base 854bd723` (0 findings, 339/339 arms), `gen_toc --check`, `check_baremetal_only --check` (0 over 1909 files) and `--selftest` (867 arms), and `check_py_idiom`.
  - Naming against #259: none of the 807 added lines contains the banned retired-stack term, and the profile uses the tree's existing `host`-program vocabulary. The bare-metal scope gate passes, and the manager's ruling authorizes a descriptor-only host profile. I see no conflict with #259's intent.
  - The comment rule: the 807 added lines contain no bench lane label, review round, reviewer ID, lane name or issue-comment ID (`residue_scan.txt`; the only hit is the technical term "render-lane").

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1 | issue #983 body and REVIEW READY comments; ruling 7096504049; `configs/host/endstation_host_example.yaml`; `receipts/host_{adp,srp,aecp}_entity.h`; `host_generators_head.txt`; `gates_32_41_42_head.txt`; `shape_costs_check_*`, `load_grade_check_*` | R902-1 | 66b4def34dcbc0d371ce4eb339d3d0226875befa |
| RTL | UNCLEAN: F1 | `git diff --raw 854bd723..66b4def3`; `ctrl_loop.h:353-425`; `shape_costs.py:102-137`; `preproc_shapes.txt`; `probe_shape_costs.txt`; `identity_probe.txt` (240/240); `integrity.txt` | R902-1 | 66b4def34dcbc0d371ce4eb339d3d0226875befa |
| Robustness | CLEAN | `endstation_builder.py:4123-4170, 4420-4464, 4552-4598, 4787-4830`; `host_robustness_probe.txt` (46 rows); `fpga_parity_probe.txt`; `prior_f1_probe.txt`; `mutant_m2.txt` | R902-1 | 66b4def34dcbc0d371ce4eb339d3d0226875befa |
| Tests | UNCLEAN: F1 | `test_builder.py:28807-28828, 30630-30935`; `gates_32_41_42_head.txt`; `gate_bad_configs_head.txt`; `mutant_m1.txt`; `mutant_m2.txt`; `flip_grade_check_*`; `shape_costs_selftest_*`; `budget_run_selftest_*` | R902-1 | 66b4def34dcbc0d371ce4eb339d3d0226875befa |
| Docs | CLEAN (R1 residue) | `docs/ENDSTATION_BUILDER.md:1-8, 78-86, 1021-1033, 1193-1283`; `docs_*.txt`; `residue_scan.txt`; PR body | R902-1 | 66b4def34dcbc0d371ce4eb339d3d0226875befa |

## Gate 1b and the firmware shards

Neither of these completing would change this verdict: F1 makes it NEGATIVE on its own. On their own merits, they cannot be judged at this head, and they are owed to the candidate.

- **Gate 1b** (`test_baremetal_profile_contract`) reads the builder, which this PR changes.
- **The firmware gate's four shards and mutation campaigns** have not run at any head of this PR. F1 shows that the author's substitute evidence ("the arms that read THE SHAPES") was not complete.
- **The budget harness** (`shape_costs`, `load_grade`, `flip_grade` and `run.py --self-test`) is not in the builder or firmware banks. The manager should add it explicitly to the candidate validation.

## Real limits and pending manager duties

- No manager source bank ran at this head, and none is inferred. I ran no full builder, firmware, parent, PP, gPTP or Yosys bank, and I did not use the scoped simulator.
- Exact-head hosted checks: 9 check runs, 8 queued and 1 in progress, none completed (`hosted_checks_66b4def3.tsv`). No executed or skipped context is credited.
- I built no current-dev candidate. The manager owes the candidate from live dev `e275d7950ef3385753e6a15d2e191ba855b171ed` (source base `854bd723`): the builder and native banks, the budget harness above, and its receipts.
- Physical calibration was NOT RUN. Field skips and desk checks are not hardware proof. Host scheduling bounds, preemption, daemon behaviour and board integration were not tested. The host shape row is a stated profile, not a measurement, and its comment says so.
- The base run of `run.py --self-test` hit the 560 s bound (rc 124) while still grading controls, so the base self-test verdict is not established. The head result (it raises at start) does not depend on that.
- Probes ran in disposable extracted trees under `scratch/`, with the clone's pinned submodules linked read-only. Gates 32, 41 and 42 and the docs gates ran in the clone, which they need for `git grep`.
- One reviewer-created ignored cache (`tb/verilator/ctrl_service_budget/__pycache__`) was removed afterwards.
- Final integrity (`integrity.txt`): HEAD and tree are exact; the status is clean with 0 ignored files; worktree, index and HEAD all match; 1936 tracked blobs match by raw bytes with 0 mismatches; there are no skip or assume flags and no non-zero stages; modes match; the five pinned submodules are at their gitlinks and clean; `external` is still uninitialised.
- No source fixes, commits, pushes, GitHub writes, author contact, Docker or act, or shared installs. The pinned Markdown renderer went into a disposable venv under `scratch/`.

## Reproduction

The scripts are in `scripts/` and take explicit paths:

- `probe_shape_costs.py REPO REV...`
- `identity_probe.sh BASE HEAD OUT`
- `preproc_shapes.sh BASE HEAD IDENTITY_OUT WORK`
- `host_robustness_probe.py TREE WORK`
- `fpga_parity_probe.py TREE WORK`
- `prior_f1_probe.py TREE WORK`

The mutants are described in `scripts/mutant_note.txt`. Base and head trees come from `git archive` with the pinned submodules linked in. Run the budget commands from each tree root with `python3 -B`. Receipts use `<PACKET>` and `<REPO>` in place of local paths. Check them with `sha256sum -c MANIFEST.sha256` from the packet directory.

R902-1 FINISHED
