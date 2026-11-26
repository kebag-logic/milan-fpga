[R935] NEGATIVE - exact head 701a980b32bf31636811ef831739c9bfd3d6f978

# R935-3: internal cleared-context delta review of kebag-logic/milan-fpga PR #1015 (Relates to #970)

- **Head:** `701a980b32bf31636811ef831739c9bfd3d6f978`, tree `03e2a77c669704aa8b42207ff0e99163d925e304` (verified in the clone; worktree clean, index and gitlinks unchanged, `third_party/tsn-c-stack` at `c3bff8f3`).
- **Delta judged:** `f4833e16..701a980b`, one commit, 6 files (+100 / -9). R935-2 was POSITIVE at `f4833e16`. Code the delta does not touch keeps its R935-2 lens verdict.
- **Scope:** R936-2-F1 only: LINK_UP's published model-access count, the new `model_counts.py` check with its planted stale count, the README and PR-body distinction from the platform's wired-clock path (11), and that no verdict or timing changed.
- **Verdict:** NEGATIVE. R936-2-F1 is **resolved at its cause**: both scenario literals are 12, every emitted LINK_UP instance carries 12 at both CPU points, and the field feeds no verdict. One **MINOR** remains (F1, Tests and Docs). The new check's text says it holds *every* ADP probe's count to the adapter's `ADP_MBX_LAT_*`, but it holds five of seven ADP paths. A stale SHUTDOWN count, whose bound `ADP_MBX_LAT_SHUTDOWN` the header states, and a stale LINK_DOWN count both pass it unseen. There are also two RESIDUE items and three SUGGESTIONs.

## 1. Reconstruction

- Contract: AGENTS.md sections 6-8 (lenses, clean-lens evidence, coverage banked per head); the owner rules quoted in the review brief (RESIDUE, the comment rule, the token economy).
- The finding under re-review, R936-2-F1 (PR comment 7187819678), required three things. Both emitted model counts must agree with the exercised fallback composition (12), with affected generated evidence refreshed. The distinction from the wired platform path must be kept. A consistency check must remain that detects stale count metadata.
- Interface authorities read at this head:
  - `sw/firmware/ctrl/adp/adp_mbx.h:119-124` (the `ADP_MBX_LAT_*` bounds; `LINK` 12 = 6 + NOW_MS 1 + 3 + 2, "down, a stop: 9").
  - `sw/firmware/ctrl/adp/adp_mbx.c:50-64`: `port_seed` returns `clock_fn(...)` when a clock is wired, else `mbx_now_ms()`, which is one mailbox access.
  - `sw/firmware/ctrl/plat/ctrl_plat.c:136-140,401`: the platform wires `adp_clock`, which reads `flash->now_us`, not a mailbox access, so the platform's pass is 11.
  - `sw/firmware/ctrl/test/test_adp.cpp:152` (C0 bounded by `ADP_MBX_LAT_LINK`).
  - `docs/design/MAILBOX_SPLIT.md:697` (LINK_UP / LINK_DOWN 12 / 9).
- `adp_mbx_set_clock` has exactly one non-test caller, `ctrl_plat.c:401`. The budget image is the size fixture (`build.py` scratch copies of `ctrl_aecp_image.c`), which wires no clock. So 12 is the correct count for this harness.

## 2. Prior findings, resolved or retained

| Prior ID | Disposition at this head | Evidence |
|---|---|---|
| R936-2-F1 MINOR (RTL, Tests, Docs): LINK_UP published 11 after the fallback grew to 12 | **RESOLVED** at the cause | `scenario.py:266` and `:944` now publish `accesses=12`. `receipts/probe_emitted_counts.log`: every LINK_UP instance emits 12 at 1x1-1if and at 8x8-1if (6 instances each), alongside discover 31, gm 11, tmr_delay 39, tmr_advertise 11, link_down 9 and shutdown 29. `grade.py:638-639` copies the field to `model_accesses` and `run.py:568` prints it, so regenerated report columns carry 12. The planted 11 is found 6 times at 1 interface and 11 at 2 (`receipts/model_counts.log`). The distinction is kept in `README.md:1326` and `model_counts.py:10-12`. In the PR body it is kept only partially (RES-B). The coverage claim of the new check is F1 below, a new defect of the fix, not a retention of R936-2-F1. |
| R936-2-R1 RESIDUE (`adp_first_mutants.py:121` names review activity) | **RESOLVED** | The line is now exactly the stated fix: `# #970: each qualified rise samples through the adapter and platform (IEEE 1722.1-2021 6.2.4.2.2).` |
| R936-2-R2 RESIDUE (`SUBMODULES.md` splits "accept 57 to 2047" from "They refuse 0 and 55.") | **RESOLVED** | `SUBMODULES.md:1198-1202`: "Parent tests accept 57 to 2047." / "They refuse 0 and 55." / "Parent adapter tests ..." now precede the #970 block. Numbers verbatim. |
| R936-2-S1 SUGGESTION (PR body: duplicate `[A847]` opening, "to be assigned" roles) | Not addressed (optional) | The live PR body still has `[A847]` twice and three "to be assigned" lines. Carried as S3. |
| R935-2 RES1 (the same SUBMODULES split) | **RESOLVED** | As R936-2-R2. |
| R935-2 RES3 (the same mutants comment) | **RESOLVED** | As R936-2-R1. The replacement text meets the comment rule. |
| R935-2 RES2 (`SPLIT_CONTROL_MEMORY.md:755` "this change's own base `c34e7d8b`") | Retained (RESIDUE, untouched by the delta) | The line is unchanged. The manager carries it to the residue checklist with R935-2's exact fix. |
| R935-2 RES4 (the PR body's CPU-leg base described inexactly) | Retained (RESIDUE, PR text) | Not in this delta. Carried. |
| R935-2 S1-S3 | Optional, not addressed | No lens effect. |

## 3. New findings at this head

### F1 - MINOR - Tests, Docs - `tb/verilator/ctrl_service_budget/README.md:1326`, `model_counts.py:3`, `model_counts.py:32-34`, `model_counts.py:61-63` - the check claims every ADP count and holds five of seven

- **Authority/evidence:**
  - What the text claims:
    - The README's checks list says `model_counts.py` "holds each ADP probe's published model count ... to the adapter's `ADP_MBX_LAT_*`".
    - The module docstring says the counts "the scenario publishes for ADP's paths" are "held to the adapter's own bounds".
    - The comment on `PATHS` says "Each ADP path the scenario probes".
    - The commit subject says "hold every ADP count to the adapter's bounds".
  - What the code does:
    - `PATHS` lists five paths: link_up, gm_change, discover, tmr_delay and tmr_advertise.
    - `groups_at()` omits `shutdown_groups()`.
  - The scenario publishes counts for two more ADP paths:
    - `adp.link_down` (9; `scenario.py:283`, `:968`), whose 9 the header states in `ADP_MBX_LAT_LINK`'s comment.
    - `adp.shutdown` (29; `scenario.py:919-920`), whose bound `ADP_MBX_LAT_SHUTDOWN 29u` (`adp_mbx.h:124`) the header states and `bounds()` parses.
  - Disposable in-memory probes (`probe_model_counts.py`, no file edited; `receipts/probe_model_counts.log`), at 1 and 2 interfaces:

    | Planted value | Result |
    |---|---|
    | LINK_UP 11, GM 12, DISCOVER 30, TMR_DELAY 40, TMR_ADVERTISE 10 | **DETECTED** |
    | header LINK=11 against the real scenario | **DETECTED** |
    | LINK_DOWN 8 | **MISSED** (0 findings) |
    | SHUTDOWN 28 | **MISSED** (0 findings) |
    | header SHUTDOWN=30 against the real scenario | **MISSED** (0 findings) |

- **Impact:** The README's checks list is the harness's test contract. It promises stale-count detection that does not exist for two published ADP rows. A future change to the shutdown or link-down mailbox path, R936-2-F1's failure mode, would publish a stale model count with the check reporting `0 stale count(s)`. The current counts are correct (29 = 29; 9 equals the header's stated stop), so no figure is wrong today. But the statement is a test-coverage claim, so the RESIDUE exception does not apply.
- **Required outcome:** One of:
  - (a) The check holds every ADP probe that publishes a count:
    - `adp.shutdown` against `ADP_MBX_LAT_SHUTDOWN`, with the shutdown groups in its set;
    - `adp.link_down` against a bound the adapter states in a form the check reads;
    - a planted stale value for each that must be found.
  - (b) README:1326, the docstring and the `PATHS` comment name exactly the five paths held, and say that LINK_DOWN and SHUTDOWN are not held.

  Either resolves F1. (a) is the stronger answer to R936-2-F1's "retain a consistency check that detects stale count metadata".
- **Verification:**
  - For (a): rerun `probe_model_counts.py <root>`; LINK_DOWN 8, SHUTDOWN 28 and header SHUTDOWN=30 must read DETECTED, and `python3 -I tb/verilator/ctrl_service_budget/model_counts.py` must exit 0.
  - For (b): read the three texts against `PATHS` and `groups_at()`.

### RES-A - RESIDUE - Docs - `tb/verilator/ctrl_service_budget/model_counts.py:15` - "(one finding a point)" misstates the planted check

- **Evidence:** The planted LINK_UP 11 yields 6 findings at 1 interface and 11 at 2 (`receipts/model_counts.log`). The pass condition is `len(planted) >= interfaces` (`:80`), not one finding per point.
- **Impact:** Wording in a docstring only. It changes no measurement or verdict.
- **Exact fix:** replace "(one finding a point)" with "(at least one finding at each point)". If S1 is taken, use "(a finding for each LINK_UP instance)".

### RES-B - RESIDUE - Docs - live PR body, `sw/firmware/ctrl/adp/` bullet and "Harness waits" bullet - the harness's 12 and the new check are not stated

- **Evidence:** The body says `ADP_MBX_LAT_LINK` is 12 where no clock is wired and that "The platform wires a clock, and its LINK_UP row stays at 11". It does not say that the CPU budget harness, whose image wires no clock, now publishes LINK_UP's model count as 12. It does not mention `model_counts.py` or its planted stale count.
- **Impact:** PR text only. A cold reader cannot tell from the body which "row" is 11 and which is 12.
- **Exact fix:** append to the "Harness waits" bullet: "The budget harness's image wires no clock, so it publishes LINK_UP's model count as 12 (the platform's LINK_UP is 11). `model_counts.py`, run first by `run.py --self-test`, holds the scenario's ADP counts to `ADP_MBX_LAT_*` and must find LINK_UP planted at 11." Narrow the "holds" wording to match F1's outcome.

### S1 - SUGGESTION - Tests - `model_counts.py:80` - the planted threshold is loose

`len(planted) >= interfaces` passes with 1 of the 6 LINK_UP instances at 1 interface, or 2 of 11 at 2. A refactor that dropped most ADP groups from `groups_at()` would still pass. Require `len(planted)` to equal the number of LINK_UP instances in the set.

### S2 - SUGGESTION - Docs - `tb/verilator/ctrl_service_budget/README.md:642` - the Results table's LINK_UP model column reads 11

The Results section states that its figures were measured on `e76a755a` and not again (`README.md:547-551`), so "(11)" is correct for that firmware and is not a stale figure of this head. The new line at `README.md:1326` says the harness's count is 12. Consider one clause under the ADP table: "the model bound is 12 at this head (`ADP_MBX_LAT_LINK`); 11 was the bound at `e76a755a`".

### S3 - SUGGESTION - Docs - live PR body opening and roles (R936-2-S1, carried)

Keep one `[A847]` opening and replace the three "to be assigned" lines with the recorded role identities.

### Comment rule

The delta adds no bench lane label, lane name, review round, reviewer ID or comment ID in source. It removes one ("the reviews of PR #1015"). `model_counts.py` names test cases (C0 to C6) and authorities only. No new RESIDUE under the rule.

## 4. Per-lens results

| Lens | Result | Artifact and what was checked |
|---|---|---|
| Conformance | **PASS** | `adp_mbx.h:119-124`, `adp_mbx.c:50-64`, `ctrl_plat.c:136-140,401`, `test_adp.cpp:152`, `MAILBOX_SPLIT.md:697`. 12 is the fallback composition's exact LINK_UP count (6 + NOW_MS 1 + 3 + 2). The platform's clock read is not a mailbox access, so its 11 is correct. The delta changes no ADP behaviour, clause citation, wire field or timeout. The IEEE 1722.1-2021 6.2.4.2.2 citation added in `adp_first_mutants.py:121` matches the header's THE DRAW clause. |
| RTL | **PASS** | Diff stat `f4833e16..701a980b`: no file under `hdl/`; no firmware C/H change. `grade.py:638-639` and `run.py:568`: `accesses` feeds only `model_accesses` and its display column, never `within_budget`, a bound or a share. So no probe's budget, CPU verdict or timing can change. `run.py:898-899` chains `model_counts.main() or selftest.main([])` and adds no build or simulation input. R936-2-F1's RTL part is resolved. |
| Robustness | **PASS** | `model_counts.py:37-90`. A renamed or reformatted header macro makes `counts[name]` raise, so the self-test exits nonzero: it fails closed. `stale()` mutates only freshly built groups (`groups_at` is called again). A failing count check returns 1 before the main self-test, and a passing one falls through to it. Both interface counts (1, 2) are exercised. The check reads only repo-relative paths (`HERE.parents[2]`). |
| Tests | **FAIL** (F1) | `receipts/probe_model_counts.log`: planted LINK_DOWN and SHUTDOWN stale counts are missed while the README claims every ADP probe. The LINK_UP plant, the other four paths and a header-side plant are DETECTED. `receipts/model_counts.log` rc 0. |
| Docs | **FAIL** (F1) | `README.md:1326`, `model_counts.py:3,32` overstate the check (F1). RES-A and RES-B are wording only. `SUBMODULES.md:1198-1202` is fixed. |

## 5. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `adp_mbx.h:119-124`; `adp_mbx.c:50-64`; `ctrl_plat.c:136-140,401`; `test_adp.cpp:152`; `MAILBOX_SPLIT.md:697`; `adp_first_mutants.py:121` | R935-3 | `701a980b32bf31636811ef831739c9bfd3d6f978` |
| RTL | CLEAN | delta diff stat (no HDL, no firmware source); `grade.py:630-645`; `run.py:560-570,895-900` | R935-3 | `701a980b32bf31636811ef831739c9bfd3d6f978` |
| Robustness | CLEAN | `model_counts.py:37-90`; `run.py:898-899` | R935-3 | `701a980b32bf31636811ef831739c9bfd3d6f978` |
| Tests | UNCLEAN (F1) | `model_counts.py`; `scenario.py:262-305,889-975`; `receipts/probe_model_counts.log`; `receipts/probe_emitted_counts.log`; `receipts/model_counts.log` | R935-3 | `701a980b32bf31636811ef831739c9bfd3d6f978` |
| Docs | UNCLEAN (F1) | `README.md:545-551,634-644,1326`; `model_counts.py:1-34`; `SUBMODULES.md:1190-1212`; live PR body | R935-3 | `701a980b32bf31636811ef831739c9bfd3d6f978` |

## 6. Executed evidence (this round, at the exact head)

| Command | Result | Receipt |
|---|---|---|
| `python3 -I tb/verilator/ctrl_service_budget/model_counts.py` | rc 0. 0 stale counts at 1 and 2 interfaces; planted 11 found 6 and 11 times | `receipts/model_counts.log`, `.rc` |
| `python3 -I probe_model_counts.py <root>` (in-memory plants) | rc 0. 5 path plants and header LINK DETECTED; LINK_DOWN, SHUTDOWN and header SHUTDOWN MISSED | `receipts/probe_model_counts.log`, `.rc` |
| `python3 -I probe_emitted_counts.py <root>` (build-free constructors and the shutdown-entry set, 1x1-1if and 8x8-1if) | rc 0. All 6 LINK_UP instances emit 12 at each point; checker 0 findings | `receipts/probe_emitted_counts.log`, `.rc` |
| `python3 -I run.py --self-test` | **Partial, not completed.** It exceeded this session's 10-minute foreground limit. Its first stage (`model_counts`) passed. The partial log shows 0 FAIL, 0 escaped mutants and 54 caught. | `receipts/run_selftest.log`, `receipts/run_selftest.NOTE` |
| Hosted check runs at the head (read-only snapshot) | Mostly queued or in progress. `elaborate-gates-2` success. Nothing here is claimed as a pass. | `receipts/hosted_check_runs_snapshot.tsv` |

After the probes: `git status --porcelain` is empty and `HEAD^{tree}` is `03e2a77c...`. Gitlinks: `tsn-c-stack c3bff8f3`, `gptp-processor 3ce71b76`, `protocol-processor 801ef228`, `lwSRP d1bb4f4e`, `verilog-axis 48ff7a7e`, `external efeb541a`. No repository file was edited.

## 7. Real limits and pending manager duties

- Limits:
  - I did not complete the full budget self-test (`run.py --self-test`) at this head. The executor's PR table states "hooks and budget harness self-tests ... PASS", but I found no executor receipt naming `701a980b`.
  - The delta adds only `model_counts` ahead of `selftest.main`, and `accesses` affects no verdict. Even so, a completed self-test at this head is source evidence the manager should obtain or link.
  - No CPU budget legs were rerun. Unchanged timing follows from the code path (`accesses` is display-only), not from a fresh measurement.
  - The `review-evidence/adp970-r1` tree belongs to an earlier round and was not re-verified for this one-commit delta.
- Not claimed: a manager source bank at this head; hosted or act acceptance; physical calibration (NOT RUN); any hardware proof from field skips.
- Pending manager duties:
  - At the merge turn, build and validate the current-dev candidate (source base `4df125b8`, live dev `e275d795`) with builder and native banks, and link its receipts.
  - Own hosted acceptance at the exact head.
  - Carry RES-A, RES-B, R935-2 RES2 and RES4 to the residue checklist.
  - Re-review F1's fix at its new head (Tests and Docs).

R935-3 FINISHED
