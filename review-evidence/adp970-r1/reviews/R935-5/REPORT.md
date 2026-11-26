[R935] POSITIVE - exact head 35d29eb71d2cc76717a4550787ef53ff2b72181f

# R935-5: internal cleared-context delta review of kebag-logic/milan-fpga PR #1015 (Relates to #970)

- **Head under review:** `35d29eb71d2cc76717a4550787ef53ff2b72181f`, tree `28780c953fc6d1f0df218ab5f692756020f78d24`, base `dev-soft-core` `4df125b8c11f0e1706b3c1e489f3e66a5d856b18`.
- **Previously reviewed head (this role):** `57f32b28de9602bd239d7686cf4360912638d1f0` (R935-4, POSITIVE).
- **Delta:** one commit, `35d29eb71`. It adds two lines to `sw/firmware/ctrl/test/ctrl_configs.py:313-314`: an `OUTSIDE` entry for `tb/verilator/ctrl_service_budget/model_counts.py`. It changes no firmware, HDL, stack pin, image input, harness, document or test case.
- **Verdict:** POSITIVE.
  - The delta fixes a real gate failure at the parent head. At `57f32b28d` the hosted `firmware-boundary` job refused `model_counts.py`, and gave only that reason: the file names the firmware's tree, is a program, and was in none of the gate's tables. The delta lists the file, and its stated reason is true. My probe of the gate's own cross-check gives REFUSED 1 with the parent's table and CLEAN at this head.
  - All prior findings stay resolved. No new BLOCKER, MAJOR or MINOR. Four RESIDUE items are retained (PR text and one prose line), one of them extended. Eight SUGGESTIONs are carried, one of them new. None leaves a lens unclean.
- This verdict does not authorize a merge and does not close #970.

## 1. Reconstruction (public state only)

- **Contract:** `AGENTS.md` sections 3 and 6 to 8, and `CONTRIBUTING.md` (five lenses, evidence for clean lenses, coverage banked per head, merge only on maintainer authorization). Also the owner rules in the review brief: RESIDUE, the comment rule, and the token economy.
- **#970 frozen acceptance and rulings:**
  - The issue body's corrected acceptance: the first ENTITY_AVAILABLE within the declared discovery time, with Milan's 0 to 4 s and 0 to 2 s draws, uniform per IEEE 1722.1-2021 6.2.4.2.2.
  - 2026-11-22: narrowing the draw is not conformant, and the 6.0 s is derived in FR_NFR.
  - 2026-11-25: no link hold, and the declared 6.0 s stands. The draw change is accepted, with each draw mixing a fresh sample, the entity ID and the interface.
  - 2026-11-26: the lost first frames were the test path's, so no ADP change follows.
- **Gate authority for the delta:**
  - `ctrl_configs.py:15-40`: the builder cross-check by text. A Python program that names the firmware's tree must be one of BUILDERS, PART_OF, OUTSIDE or SUITES.
  - `ctrl_configs.py:452-487` (`held`): the refusal, which joins every reason before it raises.
  - `docs/testing/CI_WORKFLOWS.md:3747`: `ctrl_boundary.py --require-rv32 --selftest` is one of the documented local firmware commands. Hosted, it is `rtl-fast` `firmware-boundary`, after `firmware-boundary-capture`.
- **Public executable evidence:**
  - The signed packet `review-evidence/adp970-r1` at `40ce56ee` has 14 manifest entries. I re-hashed two files against the manifest's published SHA-256 and both match (`receipts/packet_manifest_spotcheck.txt`). The packet's receipts cover `0ad0e518` only, so I used it as history.
  - No author receipt names `35d29eb71`, so this round ran its own focused evidence (section 8). No manager source bank is claimed or inferred.
- **Order kept:** I did my own pass over the delta, its gate and the hosted history (section 2) before reading the prior public findings. The prior reports read afterwards were R935-4, R935-3 and R936-3.

## 2. Independent pass over the delta

| Question | Result | Evidence |
|---|---|---|
| Does the parent head fail without the entry? | Yes. Hosted `firmware-boundary` at `57f32b28d` concluded `failure` with one reason (288 characters, no `;` separator): "`tb/verilator/ctrl_service_budget/model_counts.py` names the firmware's tree and is a program, and is neither a known builder ... (OUTSIDE) or compiles only in a suite (SUITES)". | `receipts/hosted_parent_firmware_boundary_refusal.txt`, `receipts/hosted_firmware_checks_parent.txt` |
| Does the entry clear it, and nothing else? | Yes. `probe_outside.py` runs the gate's own `builder_texts()`, `program()`, `rel()` and tables over every candidate in the checkout. It gives CLEAN at this head, and REFUSED 1 (exactly `model_counts.py`) with the entry removed. The parent's blob equals this head's with the two lines removed. | `receipts/probe_outside.txt` |
| Is the stated reason true ("reads `adp_mbx.h` as text; compiles nothing")? | Yes. `model_counts.py:40,95` reads `sw/firmware/ctrl/adp/adp_mbx.h` with `read_text`. Neither it nor its imports (`datapath_window`, `held`, `kept_window`, `scenario`) has a subprocess, compiler or `ctrl_build` reference. `scenario.py` is itself in OUTSIDE. | `receipts/delta_static_checks.txt` |
| Is OUTSIDE the right table, rather than PART_OF? | Yes. PART_OF is for a program that runs under another builder and compiles in its capture (`ctrl_configs.py:24-26`). `model_counts.py` compiles nothing, which is OUTSIDE's case, as for its siblings `scenario.py`, `selftest.py` and `share.py`. | `ctrl_configs.py:24-28,313-320` |
| Does anything else the boundary gate judges differ from a head where it passed? | No. Hosted `firmware-boundary` passed at `f4833e16a`. Since then, `f4833e16a..HEAD` touches `SUBMODULES.md`, one comment line in `adp_first_mutants.py`, and the budget harness's `README.md`, `model_counts.py`, `run.py` and `scenario.py`. Of these, only `model_counts.py` is a new builder found by text, and it is now listed. At `701a980b` the hosted boundary jobs were cancelled, not run. | `receipts/hosted_boundary_history.txt`, `receipts/delta_scope_and_spotchecks.txt` |
| Does the check the entry names still pass? | Yes. `model_counts.py` rc 0: 0 stale counts, and every path's one-short plant is found at every instance, at 1 and 2 interfaces. | `receipts/model_counts_head.txt` |
| Commit and comment rules | The commit message is one line with no trailer, and the range has no trailers. The added text names no bench lane label, lane name, review round, reviewer ID or comment ID. | `receipts/delta_static_checks.txt` |

**An observation on the prior round, not a finding at this head.** R935-4 banked `Tests` at `57f32b28d` on a local `test_ctrl_firmware.py` run. That gate does not run the boundary cross-check, and the hosted boundary job failed at that head. R935-4 claimed no hosted pass, so its report was not wrong, but its `Tests` coverage did not include this gate. The delta touches `Tests` scope, and this round covers that lens again at the exact head.

## 3. Prior findings, resolved or retained

| Prior ID | Disposition at this head | Evidence |
|---|---|---|
| R935-1 F1 to F4, R935-1 R1, R936-1-F1, R936-2-F1, R936-2-R1/R2, R935-3 F1, R935-3 RES-A, R935-3 S1 | Remain **RESOLVED** | The delta touches none of their artifacts. Firmware, stack pin (`c3bff8f3`) and image inputs are byte-identical to `57f32b28d` (`receipts/delta_scope_and_spotchecks.txt`). |
| R935-3 RES-B / R935-4 RES-B, RESIDUE (PR body does not state the harness's 12 or the count check) | **RETAINED** | The live body still says only "its LINK_UP row stays at 11" and does not name `model_counts.py`. |
| R935-4 RES-C, RESIDUE (PR body "Status" list stops at `f4833e16`) | **RETAINED and extended** | The list still has five items. It now also omits `35d29eb71`. |
| R935-2 RES2 / R935-4 RES-D, RESIDUE (`SPLIT_CONTROL_MEMORY.md:755`, "this change's own base `c34e7d8b`") | **RETAINED** | Line unchanged. The PR's base is `4df125b8`. |
| R935-2 RES4 / R935-4 RES-E, RESIDUE (PR body CPU-leg base described inexactly) | **RETAINED** | Not in the delta. |
| R935-3 S2, R935-3 S3 / R936-2-S1, R935-2 S1-S3, R935-1-S4, R935-4 S4, all SUGGESTION | Retained, optional | Unchanged. The body still has two `[A847]` openings and three "to be assigned" roles. |

## 4. Findings at this head

No BLOCKER, MAJOR or MINOR.

### RES-B (retained) - RESIDUE - Docs - live PR body, `sw/firmware/ctrl/adp/` and "Harness waits" bullets

- **Evidence:** The body states 12 accesses where no clock is wired, and 11 for the platform. It does not say that the budget harness publishes 12, and it does not mention `model_counts.py`.
- **Impact:** PR text only. No figure or verdict changes.
- **Exact fix:** append to "Harness waits": "The budget harness's image wires no clock, so it publishes LINK_UP's model count as 12 (the platform's LINK_UP is 11). `model_counts.py`, run first by `run.py --self-test`, holds the published counts of all seven ADP paths to `adp_mbx.h` and must find each path planted one short at every instance."

### RES-C (retained, extended) - RESIDUE - Docs - live PR body, "Status" list

- **Evidence:** "Since the reviewed head `0ad0e518`" lists five items, ending at the `c3bff8f3` pin (`f4833e16`).
- **Impact:** PR text only. A cold reader of the body cannot see the last three commits.
- **Exact fix:** add three items:
  - "6. `701a980b`: the budget harness publishes LINK_UP's model count as 12 (no clock wired), and `model_counts.py` holds the published ADP counts to `adp_mbx.h`."
  - "7. `57f32b28`: that check holds all seven ADP paths, LINK_DOWN and SHUTDOWN included, at every instance."
  - "8. `35d29eb7`: `ctrl_configs.OUTSIDE` lists `model_counts.py`, which reads `adp_mbx.h` as text and compiles nothing. The TSN stack boundary gate's builder cross-check refused it at `57f32b28`."

### RES-D (retained) - RESIDUE - Docs - `docs/design/SPLIT_CONTROL_MEMORY.md:755`

- "against this change's own base `c34e7d8b`": the PR now sits on `4df125b8`.
- **Exact fix (as R935-2):** "against `c34e7d8b`, the `dev-soft-core` base this was measured on (`4df125b8` adds no `rom` at these points)". Use this only if the manager confirms the second clause from the merge-candidate ledger; otherwise drop "this change's own base".

### RES-E (retained) - RESIDUE - Docs - live PR body, the two CPU budget rows

- **Exact fix (as R935-2):** name the base commit the legs were paired against in both rows.

### Suggestions (optional, no lens effect)

- **New S5 (Tests, Docs): add the boundary gate to "How to validate".** The PR body's list and table do not include `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest`. That is one of the documented local firmware commands (`docs/testing/CI_WORKFLOWS.md:3747`), and it is the gate this lane's last commit answers. Add the command, and a row with its result at the head, so the "Required local verification passes" box rests on a named receipt.
  - **Why not MINOR:** the code is correct at this head. My probe shows that, and the boundary gate's other inputs are unchanged since `f4833e16a`, where it passed. The exact-head hosted `firmware-boundary` result is a completion-bar item the manager accepts in any case.
- **S2:** under the `tb/verilator/ctrl_service_budget/README.md:636-644` ADP table, note that the model bound is 12 at this head and was 11 at `e76a755a`.
- **S3:** keep one `[A847]` opening in the PR body and fill the three roles.
- **R935-2 S1:** raise H10's distinct-delay floor nearer the 915 observed.
- **R935-2 S2:** reflow `adp_mbx.h:23-25`.
- **R935-2 S3:** investigate the 16-bit quantization of `draw_ms`, separately.
- **R935-1-S4:** remove the generator-order dependence (`PYTHONHASHSEED=0`), separately.
- **R935-4 S4:** filter `model_counts.py:102`'s plant count to the planted path.

### Comment rule

The delta's one string names a harness file, a header and its behaviour only. **No new RESIDUE under the rule.**

## 5. The brief's focus points at this head

The delta touches none of these. Each keeps its prior verdict, with a spot-check.

- **No hold or delay of LINK_UP:** no added line in `git diff 4df125b8..HEAD -- sw/firmware/ctrl` contains hold, settle, debounce or 2000. No `hdl/` change in the range.
- **Discovery time unchanged:** `FR_NFR.md:201,212,214` still give 6.0 s, the 4,311 ms sum and the 1,689 ms margin.
- **Draw ranges unchanged:** pinned `include/adp.h:85-87` still has 5,000, 4,000 and 2,000 ms.
- **Uniformity tests, plants, adapter writes no stack state, CPU legs, boot simulations:** their sources and the firmware are byte-identical to `57f32b28d`. They keep R935-4's verdicts, and the evidence named there.
- **Ledger:** the brief's "+344 to +384 B rom" matches no published figure at any head of this PR, as R935-4 also found. The document states +264 / +272 / +264 / +256 B against `c34e7d8b`. Not re-measured here.

## 6. Per-lens results

| Lens | Result | Artifact and what was checked |
|---|---|---|
| Conformance | **PASS** | `ctrl_configs.py:313-314` against #970's acceptance and rulings. The delta changes no behaviour, wire field, timeout, draw range or clause citation. `FR_NFR.md:201-214` and pinned `include/adp.h:85-87` are unchanged (`receipts/delta_scope_and_spotchecks.txt`). Untouched scope keeps R935-4's evidence at ancestor `57f32b28d`. |
| RTL | **PASS** | `git diff --stat 57f32b28d HEAD`: one gate-table file. There is no `hdl/` change in `4df125b8..HEAD`, and the submodule gitlinks are unchanged (`receipts/tree_restore_check.txt`). `OUTSIDE` feeds only the boundary gate's classification, not any build, image or simulation input. |
| Robustness | **PASS** | `ctrl_configs.py:452-487` with `receipts/probe_outside.txt`. Removing the entry makes the gate refuse by name, and with it every candidate is classified. The reason's claim, compiles nothing, is checked against the file and its imports (`receipts/delta_static_checks.txt`). An OUTSIDE entry's standing exemption is the table's design, shared by its siblings. |
| Tests | **PASS** | `receipts/probe_outside.txt` (parent REFUSED 1, head CLEAN); `receipts/hosted_parent_firmware_boundary_refusal.txt`; `receipts/hosted_boundary_history.txt` (`f4833e16a` success); `receipts/model_counts_head.txt` (rc 0, every plant found). |
| Docs | **PASS** | `ctrl_configs.py:15-40` documents the table the entry joins. No document enumerates OUTSIDE entries, and `tb/verilator/ctrl_service_budget/README.md:1326` already describes `model_counts.py`. RES-B to RES-E are wording only. |

## 7. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `ctrl_configs.py:313-314`; `FR_NFR.md:201-214`; pinned `include/adp.h:85-87`; #970 rulings; R935-4's Conformance artifacts at ancestor `57f32b28d`, untouched since | R935-5 | `35d29eb71d2cc76717a4550787ef53ff2b72181f` |
| RTL | CLEAN | delta diff stat; `4df125b8..HEAD` without `hdl/`; gitlinks in `receipts/tree_restore_check.txt` | R935-5 | `35d29eb71d2cc76717a4550787ef53ff2b72181f` |
| Robustness | CLEAN | `ctrl_configs.py:24-28,452-487`; `model_counts.py:36-41,95`; `receipts/probe_outside.txt`; `receipts/delta_static_checks.txt` | R935-5 | `35d29eb71d2cc76717a4550787ef53ff2b72181f` |
| Tests | CLEAN | `receipts/probe_outside.txt`; `receipts/model_counts_head.txt`; hosted `firmware-boundary` at `57f32b28d` (failure, one reason) and `f4833e16a` (success); R935-4's firmware-gate and plant evidence for untouched sources | R935-5 | `35d29eb71d2cc76717a4550787ef53ff2b72181f` |
| Docs | CLEAN | `ctrl_configs.py:15-40`; `tb/verilator/ctrl_service_budget/README.md:1326`; `SPLIT_CONTROL_MEMORY.md:755`; live PR body | R935-5 | `35d29eb71d2cc76717a4550787ef53ff2b72181f` |

## 8. Executed evidence (this round)

| Command | Result | Receipt |
|---|---|---|
| `python3 -I -B probe_outside.py <clone>` and `... <clone> tb/verilator/ctrl_service_budget/model_counts.py` | head CLEAN; parent table REFUSED 1 (`model_counts.py`); parent blob = head minus the two lines | `receipts/probe_outside.txt` |
| `python3 -B model_counts.py` (in `tb/verilator/ctrl_service_budget`) | rc 0 | `receipts/model_counts_head.txt` |
| `python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --jobs 4` (host, no RV32 compiler on this host) | **Not completed**: stopped at the 585 s foreground limit while still building (rc 124). Not claimed. | `receipts/fw_gate_head.log`, `.rc` |
| Hosted check runs at the head (read-only snapshot, about 17:35 UTC) | 14 success, 1 skipped, 20 in progress, 37 queued; `firmware-boundary` not yet listed. Nothing is claimed as a pass. | `receipts/hosted_checks_head.txt` |
| Hosted history, read-only | `57f32b28d` `firmware-boundary` failure, one reason; `f4833e16a` success; `701a980b` cancelled | `receipts/hosted_firmware_checks_parent.txt`, `receipts/hosted_parent_firmware_boundary_refusal.txt`, `receipts/hosted_boundary_history.txt` |
| Packet re-hash | 2 of 2 match | `receipts/packet_manifest_spotcheck.txt` |
| Clone state after the runs | HEAD, tree and index tree `28780c95...`; porcelain empty, ignored entries none; submodule worktrees clean; gitlinks `tsn-c-stack c3bff8f3`, `gptp-processor 3ce71b76`, `protocol-processor 801ef228`, `lwSRP d1bb4f4e`, `verilog-axis 48ff7a7e`, `external efeb541a` (not initialized) | `receipts/tree_restore_check.txt` |

`run_r935_5.sh <clone> <packet>` reproduces the local steps. No repository file was edited.

## 9. Real limits and pending manager duties

- **Limits:**
  - The boundary gate (`ctrl_boundary.py --require-rv32 --selftest`) was not run end to end. This host has no RV32 SDK, and a capture exceeds the foreground limit. The changed classification is proven by the gate's own functions over the real checkout. The gate's other inputs are bounded by its hosted pass at `f4833e16a`.
  - The host firmware gate did not complete within the foreground limit. The firmware it builds is byte-identical to `57f32b28d`, where R935-4 recorded rc 0.
  - No plant campaign, CPU leg, boot simulation, twin, reboot, co-simulation, memory ledger or TOC check ran this round. Their inputs are unchanged by the delta.
  - Hosted contexts were still running at the snapshot. Physical calibration was NOT RUN, and field skips are not hardware proof. No manager source bank is claimed or inferred.
- **Pending manager duties:**
  - Accept the hosted and act results at the exact head, in particular `firmware-boundary` and `firmware-boundary-capture`.
  - Build and validate the current-dev merge candidate (source base `4df125b8`, live dev `e275d795`) with the builder and native banks, the memory ledger and the TOC check, and link the receipts.
  - Carry RES-B, RES-C (now three items), RES-D and RES-E to the residue checklist.
  - The second positive and the external review, per CONTRIBUTING.
  - Maintainer merge authorization.
  - #972 and the bench re-run of the discovery scenarios stay open on #970.

R935-5 FINISHED
