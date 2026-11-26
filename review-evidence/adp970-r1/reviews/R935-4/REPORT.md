[R935] POSITIVE - exact head 57f32b28de9602bd239d7686cf4360912638d1f0

# R935-4: internal cleared-context delta review of kebag-logic/milan-fpga PR #1015 (Relates to #970)

- **Head under review:** `57f32b28de9602bd239d7686cf4360912638d1f0`, tree `9cc1e3ca2c1af6992c01ba41256bc617faa717bd`, base `dev-soft-core` `4df125b8c11f0e1706b3c1e489f3e66a5d856b18`.
- **Previously reviewed head (this role):** `701a980b32bf31636811ef831739c9bfd3d6f978` (R935-3, NEGATIVE on one MINOR).
- **Delta:** one commit, `57f32b28d`. It touches `tb/verilator/ctrl_service_budget/model_counts.py` (+54 -28) and `tb/verilator/ctrl_service_budget/README.md` (one line). It changes no firmware, HDL, stack pin or image input (`receipts/delta_scope.log`).
- **Verdict:** POSITIVE.
  - R935-3 F1 (MINOR, Tests and Docs) is **resolved at its cause** by the stronger of its two outcomes. The check now holds all seven published ADP paths, LINK_DOWN and SHUTDOWN included, at every instance, and fails closed.
  - R935-3 RES-A and S1 are resolved by the same rewrite.
  - No new BLOCKER, MAJOR or MINOR. Four RESIDUE items (three retained, one new, all PR text or prose) and five SUGGESTIONs are carried below. None leaves a lens unclean.
- This verdict does not authorize a merge and does not close #970.

## 1. Reconstruction (public state only)

- **Contract:** `AGENTS.md` sections 3 and 6-8 and `CONTRIBUTING.md` (lenses, clean-lens evidence, coverage banked per head, merge only on maintainer authorization), and the owner rules in the review brief (RESIDUE, the comment rule, the token economy).
- **#970 frozen acceptance and rulings:**
  - The issue body's corrected acceptance: the first ENTITY_AVAILABLE within the declared discovery time, with Milan's 0 to 4 s and 0 to 2 s draws, uniform per IEEE 1722.1-2021 6.2.4.2.2.
  - Ruling of 2026-11-22: narrowing the draw is not conformant; the 6.0 s is derived in FR_NFR.
  - Ruling of 2026-11-25 (issuecomment-7174054394): no link hold; the declared 6.0 s stands; the draw change is accepted, with each draw mixing a fresh sample, the entity ID and the interface.
  - Attribution of 2026-11-26: the lost first frames were the test path's, so no ADP change follows.
- **Interface authorities read at this head:**
  - `sw/firmware/ctrl/adp/adp_mbx.h:23-30` (THE DRAW) and `:119-124` (`ADP_MBX_LAT_*`; LINK 12 = 6 + NOW_MS 1 + 3 + 2, "(down, a stop: 9)", SHUTDOWN 29).
  - `sw/firmware/ctrl/adp/adp_mbx.c:51-63` (the clock port; NOW_MS fallback).
  - `sw/firmware/ctrl/plat/ctrl_plat.c:136-140`, `:401` and `:432`: the clock is wired after `compose()` and before `ctrl_app_release_adp`, so the startup draw reads the microsecond clock.
  - Pinned `third_party/tsn-c-stack` `c3bff8f3`: `src/adp.c:53-61` (draw), `:99-110` (`leave_down`), `:256` (startup), `:274` (qualified LINK_UP); `include/adp.h:85-87` (5,000 / 4,000 / 2,000 ms).
  - `docs/reference/FR_NFR.md:200-225` (2.1.1).
- **Public executable evidence:**
  - The signed packet `review-evidence/adp970-r1` at `40ce56ee`: all 14 files match their manifest's published SHA-256. Its receipts cover `0ad0e518` only, not this head. It is used as history only.
  - No author receipt names `701a980b` or `57f32b28`, so this round ran its own focused evidence (section 6).
- **Order kept:** I made my own pass over `4df125b8..57f32b28` and over the delta, and wrote my verdict draft, before reading prior findings. I read this role's own R935-3 before writing the draft, and the other reviewer's round at `701a980b` only after it.

## 2. Prior findings, resolved or retained

| Prior ID | Disposition at this head | Evidence |
|---|---|---|
| R935-3 F1 MINOR (Tests, Docs): the check claims every ADP count and holds five of seven | **RESOLVED** at the cause, outcome (a) | See the table after this one. |
| R935-3 RES-A RESIDUE: "(one finding a point)" | **RESOLVED** | The docstring (`model_counts.py:23-25`) now reads "plants each path's count one short, and every instance of that path must be found". That matches `:102-104`. |
| R935-3 S1 SUGGESTION: the planted threshold is loose | **RESOLVED** | `:104` now requires `caught[path] == instances[path]` and `instances[path]` non-zero for each of the seven paths. |
| R935-3 RES-B RESIDUE: the PR body does not state the harness's 12 or the check | **RETAINED** (PR text) | The live PR body's adapter bullet still says only "its LINK_UP row stays at 11" and does not mention `model_counts.py`. Exact fix in section 3. |
| R935-3 S2 SUGGESTION: `README.md:642` Results table reads LINK_UP model "(11)" | Retained, optional | Unchanged. That table is a dated measurement at `e76a755a`. |
| R935-3 S3 / R936-2-S1 SUGGESTION: duplicate `[A847]` opening and "to be assigned" roles in the PR body | Retained, optional | The body still has two `[A847]` and three "to be assigned". |
| R935-2 RES2 RESIDUE: `SPLIT_CONTROL_MEMORY.md:755` "this change's own base `c34e7d8b`" | **RETAINED** | The line is unchanged. The PR now sits on `4df125b8`. Carry R935-2's exact fix. |
| R935-2 RES4 RESIDUE: the PR body's CPU-leg base described inexactly | **RETAINED** (PR text) | Not in this delta. Carried. |
| R935-2 S1 (H10's floor of 600 against 915 observed), S2 (`adp_mbx.h:23` wraps after "and seeds its"), S3 (16-bit multiply-shift quantization in pinned `draw_ms`) | Retained, optional | Unchanged at this head. `adp_mbx.h:23-25` still breaks after "and seeds its". |
| R935-1-S4 SUGGESTION: generator-order reproducibility (`PYTHONHASHSEED=0`) | Retained, optional | Still disclosed in the PR's Known limitations. |
| R935-1 F1-F4, R935-1 R1, R936-1-F1, R936-2-F1, R936-2-R1/R2 | Remain RESOLVED | The delta touches none of their artifacts. Firmware, stack pin and image inputs are byte-identical to `701a980b` and `f4833e16`, apart from one test-table comment at `f4833e16..701a980b` (`receipts/delta_scope.log`). |

The evidence for R935-3 F1 follows. Each row is one of R935-3's verification items or one of my own probes.

| R935-3 verification item | Result at this head |
|---|---|
| `adp.link_down` held, against a bound the header states in a form the check reads | Held. `PATHS` (`:43`) maps it to `LINK_DOWN`. `bounds()` (`:51-55`) reads 9 from `ADP_MBX_LAT_LINK`'s comment "(down, a stop: 9)" (`adp_mbx.h:123`). `test_adp.cpp:181` (C5) bounds it by `ADP_MBX_LAT_LINK`, as the docstring says. |
| `adp.shutdown` against `ADP_MBX_LAT_SHUTDOWN`, with the shutdown groups in the set | Held. `SETS` (`:46-48`) includes `scenario.shutdown_groups`. |
| A planted stale value for each path must be found | Found at every instance. `receipts/model_counts.log`, rc 0. At 1 interface: link_up 6/6, link_down 2/2, gm_change 1/1, discover 2/2, tmr_delay 5/5, tmr_advertise 1/1, shutdown 2/2. At 2 interfaces: 11/11, 3/3, 2/2, 3/3, 10/10, 2/2, 3/3. |
| LINK_DOWN 8, SHUTDOWN 28, header SHUTDOWN=30 must be DETECTED | My probes (`probe_model_counts.py`, in memory, no file edited; `receipts/probe_model_counts.log`, 54 of 54 as expected, rc 0) at 1 and 2 interfaces. DETECTED: header SHUTDOWN 30, header LINK_DOWN comment 10, each of the six other header macros +1, each path +1, a single stale instance of each path, and an ADP count on an unheld path. |
| The check fails closed | My probes: an unreadable LINK_DOWN comment and a removed SHUTDOWN macro both RAISE (KeyError). A weakened check also FAILS `main()`: dropping `adp.shutdown` or `adp.link_down` from `PATHS`, or `shutdown_groups` or `adp_groups` from `SETS`. |
| The build-dependent sets publish no count, as the docstring claims | Static check. `save_window.py:208`'s probe is family `disc`, not `adp`. `aecp_groups` and `aecp_fanout_groups` call no `advertised()` and carry no ADP `accesses`. `reboot_group.py` and `long_notice.py` construct no ADP probe. |

## 3. Findings at this head

No BLOCKER, MAJOR or MINOR.

### RES-B (retained from R935-3) - RESIDUE - Docs - live PR body, `sw/firmware/ctrl/adp/` bullet and "Harness waits" bullet

- **Evidence:** The body says `ADP_MBX_LAT_LINK` is 12 where no clock is wired, and that "The platform wires a clock, and its LINK_UP row stays at 11". It does not say that the budget harness, whose image wires no clock, publishes 12. It does not mention `model_counts.py`.
- **Impact:** PR text only. It changes no figure or verdict.
- **Exact fix:** append to the "Harness waits" bullet: "The budget harness's image wires no clock, so it publishes LINK_UP's model count as 12 (the platform's LINK_UP is 11). `model_counts.py`, run first by `run.py --self-test`, holds the published counts of all seven ADP paths to `adp_mbx.h` and must find each path planted one short at every instance."

### RES-C (new) - RESIDUE - Docs - live PR body, "Status" list

- **Evidence:** "Since the reviewed head `0ad0e518`" lists five steps ending at the `c3bff8f3` pin (`f4833e16`). It omits `701a980b` (LINK_UP's harness count 12 and the new count check) and `57f32b28` (all seven paths held).
- **Impact:** PR text only. A cold reader of the body cannot see the last two commits.
- **Exact fix:** add the following two items:
  - "6. `701a980b`: the budget harness publishes LINK_UP's model count as 12 (no clock wired), and `model_counts.py` holds the published ADP counts to `adp_mbx.h`."
  - "7. `57f32b28`: that check holds all seven ADP paths, LINK_DOWN and SHUTDOWN included, at every instance."

### RES-D (R935-2 RES2, retained) - RESIDUE - Docs - `docs/design/SPLIT_CONTROL_MEMORY.md:755`

- "against this change's own base `c34e7d8b`": the PR's base is now `4df125b8`.
- **Exact fix (as R935-2):** "against `c34e7d8b`, the `dev-soft-core` base this was measured on (`4df125b8` adds no `rom` at these points)". Use this only if the manager confirms the second clause from the merge-candidate ledger; otherwise drop "this change's own base".

### RES-E (R935-2 RES4, retained) - RESIDUE - Docs - live PR body, the CPU budget rows

- The base the CPU legs were paired against is not named exactly.
- **Exact fix (as R935-2):** name the base commit the legs were paired against in the two CPU rows.

### Suggestions (optional, no lens effect)

- **S2:** under the `README.md:636-644` ADP table, add "the model bound is 12 at this head (`ADP_MBX_LAT_LINK`); 11 was the bound at `e76a755a`".
- **S3:** keep one `[A847]` opening in the PR body and fill the three roles.
- **R935-2 S1:** raise H10's distinct-delay floor (`test_adp.cpp:1052` onward) nearer the 915 observed.
- **R935-2 S2:** reflow `adp_mbx.h:23-25`.
- **R935-2 S3:** investigate the 16-bit quantization of `draw_ms`, separately.
- **R935-1-S4:** remove the generator-order dependence, separately.
- **New S4 (Tests):** `model_counts.py:102` counts every finding a plant produces, not only those on the planted path. This is sound today, because `:104` also requires zero findings on the real scenario. A filter on `path_of(probe) == path` would make the equality independent of that guard.

### Comment rule

The delta's source text (`model_counts.py` docstring, comments and messages) names test cases (C0 to C6, C5), header macros and the adapter header only. It adds no bench lane label, lane name, review round, reviewer ID or comment ID. No new RESIDUE under the rule.

## 4. Per-lens results

| Lens | Result | Artifact and what was checked |
|---|---|---|
| Conformance | **PASS** | Pinned `src/adp.c:99-110,256,274`: one sample at each transition out of DOWN; the seed is the least significant 32 bits of MAC + sample (6.2.4.2.2), mixed with the entity ID and the interface. `include/adp.h:85-87`: 4,000 / 2,000 ms unchanged (Milan v1.2 5.6.3.5.2 and 5.6.3.5.3, Table 5.50). `ctrl_plat.c:136-140,401,432`: wired before the release, no hold, settle or debounce added. `git diff 4df125b8..HEAD -- sw/firmware/ctrl/plat` adds only the clock and its wiring. `FR_NFR.md:200-225`: 6.0 s and the 4,311 ms sum unchanged. The diff only adds the uniformity paragraph. The delta `701a980b..57f32b28` changes no behaviour, wire field, timeout or clause citation. |
| RTL | **PASS** | `receipts/delta_scope.log`: no `hdl/`, firmware, stack-pin or image-input change in `f4833e16..57f32b28` apart from one test-table comment. `accesses` feeds only the report's model column, not a budget, share or verdict (`grade.py`, `run.py`). `run.py:898-899` adds no build or simulation input. CPU legs and memory ledger keep their reviewed results at the byte-identical firmware. |
| Robustness | **PASS** | `model_counts.py:51-55,93-110` with my probes: header drift raises; weakened `PATHS` or `SETS` fail `main()`; a foreign ADP path is a finding; `groups_at()` rebuilds fresh groups for every plant. At this head the firmware's duplicate and disabled LINK_UP take no sample: `AdpDraw.H9` passed in `receipts/firmware_gate.log`. |
| Tests | **PASS** | `receipts/model_counts.log` (rc 0); `receipts/probe_model_counts.log` (54/54); `receipts/run_selftest.log` (rc 0, "self-test: 0 failures", no MUTANT ESCAPED); `receipts/firmware_gate.log` (rc 0, 85 of 85 suite verdicts PASS). H4-H6, H8 and H10 chi-square 8.2 to 25.5 against 30.6, and H10 915 distinct of 1,024; platform boot 59 checks at if1 and 60 at if2 (B25-B27). R935-3 F1's Tests part is resolved. |
| Docs | **PASS** | `tb/verilator/ctrl_service_budget/README.md:1326` and `model_counts.py:1-26` state exactly what `:43-110` does: the seven paths, LINK_DOWN from the LINK comment, "every instance", raise on a missing count. `test_adp.cpp:181` confirms "C5 bounds it by `ADP_MBX_LAT_LINK`". `check_py_idiom.py` rc 0. RES-B to RES-E are wording only. R935-3 F1's Docs part is resolved. |

## 5. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | pinned `src/adp.c:53-61,99-110,256,274`; `include/adp.h:85-87`; `adp_mbx.h:23-30,119-124`; `adp_mbx.c:51-63`; `ctrl_plat.c:136-140,401,432`; `FR_NFR.md:200-225`; #970 rulings | R935-4 | `57f32b28de9602bd239d7686cf4360912638d1f0` |
| RTL | CLEAN | `receipts/delta_scope.log`; `run.py:895-900`; `grade.py` model column; no `hdl/` in `4df125b8..57f32b28` | R935-4 | `57f32b28de9602bd239d7686cf4360912638d1f0` |
| Robustness | CLEAN | `model_counts.py:43-110`; `receipts/probe_model_counts.log`; `AdpDraw.H9` in `receipts/firmware_gate.log` | R935-4 | `57f32b28de9602bd239d7686cf4360912638d1f0` |
| Tests | CLEAN | `model_counts.py`; `scenario.py` (`advertised`, `adp_groups`, `control_groups`, `fixture_groups`, `shutdown_groups`); `receipts/model_counts.log`; `receipts/probe_model_counts.log`; `receipts/run_selftest.log`; `receipts/firmware_gate.log`; `test_adp.cpp:934-1075`; `test_plat_boot.cpp:1346-1412` | R935-4 | `57f32b28de9602bd239d7686cf4360912638d1f0` |
| Docs | CLEAN | `tb/verilator/ctrl_service_budget/README.md:636-644,1326`; `model_counts.py:1-26`; `SPLIT_CONTROL_MEMORY.md:755`; `FR_NFR.md:217-221`; `CHANGELOG.md`; live PR body; `receipts/check_py_idiom.log` | R935-4 | `57f32b28de9602bd239d7686cf4360912638d1f0` |

## 6. Executed evidence (this round, at the exact head)

| Command | Result | Receipt |
|---|---|---|
| `python3 -I -B model_counts.py` (in `tb/verilator/ctrl_service_budget`) | rc 0; 0 stale; all seven paths found at every instance, at 1 and 2 interfaces | `receipts/model_counts.log`, `.rc` |
| `python3 -I -B probe_model_counts.py <clone>` | rc 0; 54 of 54 probes as expected | `receipts/probe_model_counts.log`, `.rc` |
| `python3 -B run.py --self-test` (budget harness) | rc 0; `model_counts` first, then "self-test: 0 failures" | `receipts/run_selftest.log`, `.rc` |
| `python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --jobs 4` (no `--self-test`) | rc 0; `test_ctrl_firmware: PASS`; 85 suite verdicts PASS | `receipts/firmware_gate.log`, `.rc` |
| `python3 -B scripts/check_py_idiom.py` | rc 0 | `receipts/check_py_idiom.log`, `.rc` |
| `python3 -B scripts/gen_toc.py --check` | **Not run**: rc 2, the pinned Markdown renderer is not installed here | `receipts/gen_toc_check.log`, `.rc` |
| `plat_ledger.py --build-dir ...` | **Not run**: rc 1, `ModuleNotFoundError: litex` in this environment | `receipts/plat_ledger_not_run.log`, `.rc` |
| Hosted check runs at the head (read-only snapshot, 12:46 UTC) | 30 success, 1 skipped, 14 in progress, 24 queued. Nothing is claimed as a pass. | `receipts/hosted_check_runs_snapshot.tsv` |
| Clone state after the runs | HEAD, tree and index tree are `9cc1e3ca...`; porcelain empty; all submodule worktrees clean. Gitlinks: `tsn-c-stack c3bff8f3`, `gptp-processor 3ce71b76`, `protocol-processor 801ef228`, `lwSRP d1bb4f4e`, `verilog-axis 48ff7a7e`, `external efeb541a` (not initialized). | `receipts/tree_restore_check.log` |

`run_r935_4.sh <clone> <packet>` reproduces these commands. No repository file was edited, and no probe wrote into the clone.

## 7. Real limits and pending manager duties

- **Limits:**
  - The firmware gate ran without `--self-test`. The 28 ADP plants (`adp_first_mutants.py`) and the control campaign were not re-run this round. Their sources and targets are unchanged since the heads where they were reviewed, apart from one comment line.
  - The memory ledger and the TOC check could not run here (LiteX and the pinned Markdown renderer are absent). The `rom` figures at `SPLIT_CONTROL_MEMORY.md:755` rest on firmware byte-identical to `f4833e16`, not on a fresh build. The `+344 to +384 B` in the review brief matches no published figure at any head of this PR. The doc states +264 / +272 / +264 / +256 B against `c34e7d8b`.
  - No CPU budget legs, boot simulation, twin, reboot or co-simulation ran this round. They depend on firmware the delta does not touch.
  - Neither the 33 s co-simulation's frame count ("fourteen frames (five ADP, nine ACMP)", `tb/verilator/mbx/README.md`) nor the reboot row was re-executed. They carry their prior rounds' verdicts.
  - Hosted contexts were still running at the snapshot. Physical calibration was NOT RUN, and field skips are not hardware proof. No manager source bank is claimed or inferred.
- **Pending manager duties:**
  - Build and validate the current-dev merge candidate (source base `4df125b8`, live dev `e275d795`) with the builder and native banks, the memory ledger and the TOC check. Link the receipts.
  - Own hosted and act acceptance at the exact head.
  - Carry RES-B, RES-C, RES-D and RES-E to the residue checklist.
  - The second positive and the external review per CONTRIBUTING.
  - Maintainer merge authorization.
  - #972 and the bench re-run of the discovery scenarios stay open on #970.

R935-4 FINISHED
