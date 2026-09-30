[R411] POSITIVE - exact head 616cbdf1e54a56420e35b53cd161116702f7172d

# R411-2: external independent review of processor PR #137 (lane C4, ACMP; closes #45, #47, #48), round 2

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Head `616cbdf1e54a56420e35b53cd161116702f7172d`, tree `d01536e57ea12cfd0f53ab4ff5cbf5178452a5d9`, source base `b2db3a970cedbbff2f8ba813acb96122c442bc58`.
- The round covers six commits on the round-1 head `a9ce0fa2`:
  - `9151e8b`, `f55a25f`, `dbd8624`, `06a84f5`, `bf764ac`
  - `616cbdf`, which reverts `dbd8624`
- The review applies all five lenses to the whole PR diff at this head, with depth on the round-2 delta.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open at this head.

- Every prior finding is resolved or retained with its reason (table below).
- R410-1 F-1, the one open MINOR, is resolved.
- Three new SUGGESTIONs follow. They do not affect the verdict or any lens.

## Reconstruction (order followed)

1. The parent's `AGENTS.md` and `CONTRIBUTING.md`, read at milan-fpga `2650a1e5`, because the processor repository has neither. Then the processor's `README.md` and `docs/README.md`.
2. Issue #45: the body, with its frozen acceptance 1 to 3 and the GAP-15 residue. Then the comments:
   - the lane assignment 5891906554;
   - the round-2 assignment 5903960934, with its rulings on R410-1 F-1, R411-1 S2 and S3;
   - the STOP 5906502273;
   - the ruling 5906539259, option (b).
3. The authorities:
   - 00 §5 GAP-15, the REQ-ACMP-001 row, and F00.2 with its caption `:513-517`;
   - 03 V3 (`:72`) and 09 F09.4 (`:62`);
   - 05's action legend, and the listener's canonical action order (`hdl/acmp/KL_pp_acmp_listener.sv:30-36,597-616`);
   - the F05.3 ROM (`hdl/acmp/rom/gen_ltn_rom.py:57-64`).
4. `git diff b2db3a97..616cbdf` and `a9ce0fa..616cbdf`, the history, and each commit's shape.
5. The public evidence at milan-fpga `2650a1e5` `review-evidence/ppC4-r1/author-r2`: the handoff, the PR body, the parent patches and the AS6 and timeout probes. The PR body at head is the same text as the packet's `PR-BODY.md`.
6. The prior review reports R410-1 and R411-1 (PR comments 5903779541 and 5903956326). I read them only after my own pass over the diff and my probes.

## Findings

No finding at BLOCKER, MAJOR or MINOR.

### S1: SUGGESTION. Lenses: Tests, Docs. AS6 "from the unbind on" does not grade a frame sent before the UNBIND_RX_RESPONSE

- **Where:**
  - `tb/pp_top/sim_main.cpp:9233`: `wait_acmp(9, 0x4815, 400)` pops and drops every non-matching ACMP frame (`:1841-1852`).
  - `tb/pp_top/sim_main.cpp:9223-9225,9257-9261`
  - `tb/pp_top/README.md:1193-1195`
  - the `06a84f5` subject ("so nothing probes the sink from the unbind on")
- **Evidence:**
  - The new check starts at the response. The README's parenthetical states that window exactly, but the headline claim is "from the unbind on".
  - The listener runs its actions in one fixed order, and A13 (the exact-duplicate PROBE_TX) comes before A7 (the UNBIND_RX_RESPONSE) (`KL_pp_acmp_listener.sv:607,613`).
  - Reviewer probe P2 plants A13 in the UNBIND x SETTLED_RSV_OK cell (`gen_ltn_rom.py:64`). The sink then sends a PROBE_TX after the UNBIND_RX but before its response.
  - P2 at head SURVIVES section AC: run rc 0, no check fails.
  - P2 is KILLED in two other places:
    - by `tb/acmp_listener`'s cell walk ("F05.3 UNBIND x SOK: frames got 2 want 1");
    - by a scratch bench copy that reads the unbind response as the next ACMP frame (`h2.wait_any`). The failures there are "AS6: UNBIND_RX_RESPONSE SUCCESS byte-exact" and the new AS6 check. That copy's golden passes: rc 0, no failing check.
  - Receipts: `receipts/probes/A-head.stdout`, `D-head-benchnext.stdout`, `E-head-listener.stdout`.
- **Impact:** at top level, the unit suite still catches this defect class. The only gap is that the README and commit claim is wider than what AS6 grades.
- **Suggested outcome:** at a later touch, either read the UNBIND_RX_RESPONSE as the next ACMP frame (a one-line change, which the probe shows passes the golden and kills P2), or narrow the wording to "from the UNBIND_RX_RESPONSE on". Otherwise, add it to the residue checklist.
- **Verification:** P2 under `scripts/r411_2_probes.py` is KILLED in `tb/pp_top`.

### S2: SUGGESTION. Lens: Docs. The F00.2 caption still dates the whole Open residue column to the 2026-09-18 audit

- **Where:** `docs/00_MILAN_COMPLIANCE_REVIEW.md:509` (the GAP-15 cell is now "none found") and `:513` ("The **Open residue** column records the audit of 2026-09-18 at main `6a878f6`").
- **Evidence:**
  - That audit found #45 as GAP-15's residue. The cell now shows the state after this PR.
  - The precedent that the ruling cites, `05fd9e1` (GAP-03), changed its cell and also added a caption sentence naming its later exception (`:517-518`).
  - This PR changes the cell only, as the ruling instructed ("nothing else in 00 changes").
  - The cell itself is right under the caption's rule:
    - GAP-15's category is TOL, and F29 and AL grade the one residue the audit recorded;
    - no other open issue names GAP-15 in its title.
- **Impact:** a reader of the caption would date GAP-15's "none found" to an audit that in fact found a residue. Git history and closed #45 recover the truth.
- **Suggested outcome:** the manager decides whether a one-clause caption note like GAP-03's is added at the next 00 touch. This is not required in this PR, which followed an explicit ruling.

### S3: SUGGESTION. Lenses: Docs, Conformance. This is pre-existing text, outside the item-3 list. A cdl-24 ACMPDU is labelled the "IEEE 2013 short form"

- **Where:**
  - `tb/rx_validator/README.md:37`, in the V3 bullet this PR extends;
  - `tb/rx_validator/sim_main.cpp:463` (F4, "IEEE 2013 short-form ACMPDU, cdl 24").
- **Evidence:** this PR's own edition table and the edited 09 F09.4 row (`:62`) both say the IEEE 1722.1-2013 ACMPDU has cdl 44 (56 bytes). The F4 label names a cdl-24 form as 2013. These lines are unchanged by this PR, and the PR body's "What remains" already lists the related 03 V3 edition gap.
- **Suggested outcome:** add it to the residue checklist, and reword F4's label (for example, "a short ACMPDU, cdl 24") at a later documentation touch.

## Prior findings at this head

| Finding | State at `616cbdf` | Evidence |
|---|---|---|
| R410-1 F-1 (MINOR, Docs/Conformance): the F00.2 GAP-15 cell links #45, which this PR closes | **RESOLVED** (`9151e8b`) | The `b2db3a97..616cbdf` diff of 00 is one line, `:509` becoming "none found"; nothing else in 00 changes. `make check` is rc 0. The cell follows the caption rule (see S2 for the caption's dating). |
| R410-1 S-1 (Tests): AS6's GET_RX_STATE wait drops frames unseen | **ADDRESSED** (`06a84f5`) | `q_acmp` is graded empty before the GET_RX_STATE, and the answer is read as the next frame (`:9257-9261`). Probe P1 (A5 on unbind: a probe after the response) is KILLED at head by the new check alone and SURVIVES at `a9ce0fa`. The window before the response is my S1. |
| R410-1 S-2 (Docs): 09 F09.4 "2013 96-B ACMPDU" | **RESOLVED** (`f55a25f`) | `09_verification.md:62` now reads "96-B IEEE 1722.1-2021 ACMPDU (cdl 84) and 56-B Milan ACMPDU (cdl 44, the IEEE 1722.1-2013 length)". |
| R411-1 S1 (Docs/Conformance): edition of the message_type table | **RESOLVED** (`f55a25f`) | Every message_type and flags citation in the lane and in `tb/acmp_nvm` names its edition: `tb/acmp_listener/README.md:69`, `sim_main.cpp:1209-1210,1221`; `tb/pp_top/README.md:1141`, `sim_main.cpp:8812,8842,8976-8977,9018`; `tb/rx_validator/sim_main.cpp:754`; `tb/acmp_nvm/sim_main.cpp:176-177,185`. The 2021 and 2013 table numbers agree with the PR body's table. The RTL's status citations "IEEE Table 8-3" (`KL_acmp_talker.sv:228,294`) are outside S1 and disclosed. |
| R411-1 S2 (Docs): snapshot reading of F00.2 and the PR body's "per that table's own rule" | **CLOSED** by the ruling on F-1 (5903960934) | The PR body's §1 wording is corrected. |
| R411-1 S3 (Conformance/Robustness, pre-existing): the bound stream identity survives an A8 teardown | **RETAINED**, not attributable to this diff | It is port-visible and on the manager's residue checklist, per 5903960934. `hdl/` is unchanged. |
| R411-1 S4 (Robustness/Tests): no per-run timeout in `acmp_mutants.py` | **RETAINED** under ruling 5906539259, option (b) | The revert is exact: `616cbdf`'s changed lines equal the inverse of `dbd8624`'s. `tb/pp_top/acmp_mutants.py` is blob `cefbbeb5`, mode 100755, identical to `a9ce0fa` and `f55a25f`. `git grep` finds no `--timeout`, `SURVIVED/TIMEOUT` or `RUN_TIMEOUT` at head. `judge()` still counts KILLED only on a completed tally with a non-zero exit and every named check failing, so a hang can never count as a kill. The reason is recorded in PR body §4 and "What remains". |

## Lens results

### Conformance: CLEAN

- **#45 (REQ-ACMP-001, Milan v1.2 §5.5.2.2; 03 V3; F09.4):**
  - **F29** (`tb/rx_validator/sim_main.cpp:754-797`) drives the cdl-84 form with a patterned 40-byte tail, as a BIND_RX and as a PROBE_TX. The frame is committed whole: the slot holds 96 bytes, `rx_length` does not move, and the header beat is field-exact and equal to the 56-B form's apart from cdl.
  - **AL1 to AL4** (`tb/pp_top/sim_main.cpp:9024-9072`): long UNBIND_RX, BIND_RX and PROBE_TX commands get byte-exact 56-B cdl-44 responses. The probe regenerated from the long BIND_RX's record is byte-exact.
  - **Acceptance 3:** `cdl_not_44_rejected` is KILLED (27 of 495; 19 of 43) and recorded as M5 in `tb/rx_validator/README.md`.
- **#47 (REQ-ACMP-012, §5.5.3.1):**
  - B13 and B14 (`tb/acmp_listener/sim_main.cpp:1207-1294`): types 3, 5, 7, 9, 11, 13, 14 and 15, each shaped as the perfect probe answer, are fully inert. The guard is graded term by term, with a positive control.
  - AI1 to AI3 (`tb/pp_top/sim_main.cpp:8984-9016`).
- **#48 (REQ-ACMP-016):**
  - AS1 to AS6 (`:9082-9274`) follow §5.5.3.5.18, .36, .42 and .45, and §5.3.8.5 and .9.
  - The AS6 unbind grades the ROM cell UNBIND x SOK = `A1 A11 A8 A9 A10 A7` (`gen_ltn_rom.py:64`): response, Lv, bound view cleared, unbound GET_RX_STATE.
- **Edition labels** (round 2): internally consistent. The 2021 set is §8.2.1.4/Table 8-2, §8.2.1.6 (cdl 84) and §8.2.1.16/Table 8-4. The 2013 set is §8.2.1.5/Table 8.1, §8.2.1.7 (cdl 44) and §8.2.1.17/Table 8.3.
- **F00.2 GAP-15 cell:** follows the caption's rule (S2 concerns only the caption's date).

### RTL: CLEAN

- `git diff --quiet b2db3a97 616cbdf -- hdl scripts Makefile .github syn` is rc 0, so no RTL, port, parameter, register or ROM changes.
- The only non-suite source is `tb/pp_top/pp_top_wrap.sv:253-260,666-669`. It connects the top's existing `acmp_bound_eid/sid/dmac/vlan_o` at 8x64, 8x64, 8x48 and 8x12 bits, which matches the lane-slicing helper `view()` (`sim_main.cpp:8860-8875`). Both builds (default and VID fixture) elaborate and pass.
- I checked the listener's canonical action order (`KL_pp_acmp_listener.sv:597-616`) to judge the AS6 claim (S1). The order is design-intended and unchanged.

### Robustness: CLEAN

- **AS6 stray-frame accounting:** the queue is checked, then cleared, so a stray frame counts once, and the answer is the next frame (`:9257-9261`).
- **`wait_frame` discard semantics** (`:1841-1857`) were checked for every AS window. The only residual is S1.
- **Section AC** runs on a fresh model (`:8821-8826`), so the main timeline is unaffected. The full suite at head still totals 7931.
- **Mutation driver grading rule** (`acmp_mutants.py` `judge`): a refused edit, a failed build, a crash or a missing tally never counts as a kill. So S4's retention leaves no false-KILLED path.

### Tests: CLEAN (S1 is a suggestion)

- **Changed suites at head, Verilator 5.050:**

  | Suite | Result |
  |---|---|
  | `tb/rx_validator` | 495/495 |
  | `tb/acmp_listener` | 2988/2988 |
  | `tb/acmp_nvm` | 360/360 |
  | `tb/pp_top` | 7931/7931, both builds (AC 43 checks, 0 failures) |

- **`acmp_mutants.py` at head:** 19 of 19 KILLED, and all four goldens PASS. Every failing count equals the recorded table:
  - `tb/acmp_listener`: 93/2988, 50/2984, 40/2984, 30/2984;
  - `tb/rx_validator`: 27/495;
  - section AC: 1, 19, 7, 1, 7, 7, 7, 6, 2, 2, 2, 1, 5 and 5 of 43.
- **Round-2 check has teeth:** probe P1 is KILLED at head by the new AS6 check alone and SURVIVES at `a9ce0fa`.
- **Untouched entry points** that build this lane's changed suite: `name_wr_mutant.py` rc 0 (decode killed; golden and restored PASS), and `gsi_mutants.py` rc 0 (20 detected; golden and restored PASS).

### Docs: CLEAN (S2 and S3 are suggestions)

- **Suite READMEs agree with the measured tallies and tables:**
  - `tb/acmp_listener/README.md:7,83-91`
  - `tb/rx_validator/README.md:5,38-43,81`
  - `tb/pp_top/README.md:1141-1145,1190-1196,1204-1232`: the date is 2026-09-30, the denominators are 43, and the usage text is identical to round 1's.
- **Documentation edits:** 09 F09.4 `:62` and 00 F00.2 `:509`.
- **PR body:**
  - the round-2 table, §§1-5 and the validation tables;
  - the disposition line for `protocol-processor/tb/pp_top/acmp_mutants.py`. It matches the published `parent-adaptation-132-c1-c4.patch` and describes the driver accurately: listener, validator, top SRP-service, bound-view and SRP-matcher edits, and every named check failing in a completed run.
- **Gates:** `make check` rc 0 (links 976, matrix 115 REQ / 17 GAP, modmatrix 94 rows 0 untested, params 26). `gen_matrix.py --check` rc 0. `git diff --check` rc 0 for base..head and for r1..head.
- **Commits:** all 12 have one-line messages with no body or trailers, and there are no merges.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #45 acceptance 1-3 (F29 `tb/rx_validator/sim_main.cpp:754-797`, AL `tb/pp_top/sim_main.cpp:9024-9072`, M5); #47 B13/B14 `tb/acmp_listener/sim_main.cpp:1207-1294`, AI `:8984-9016`; #48 AS1-AS6 `:9082-9274` against the ROM cell `gen_ltn_rom.py:64`; edition citations (list above); 09 F09.4 `:62`; 00 F00.2 `:509` against the caption `:513-517` | R411-2 | 616cbdf1e54a56420e35b53cd161116702f7172d |
| RTL | CLEAN | `hdl/` diff empty (rc 0); `tb/pp_top/pp_top_wrap.sv:253-260,666-669` widths against `view()` `:8860-8875`; listener canonical order `KL_pp_acmp_listener.sv:597-616` | R411-2 | 616cbdf1e54a56420e35b53cd161116702f7172d |
| Robustness | CLEAN | AS6 queue check `:9257-9261`; `wait_frame` `:1841-1857`; fresh-model AC `:8821-8826`; `acmp_mutants.py` `judge()`; S4 revert exactness | R411-2 | 616cbdf1e54a56420e35b53cd161116702f7172d |
| Tests | CLEAN (S1 suggestion) | four changed suites at 5.050; `acmp_mutants.py` 19/19 with counts; probes P1/P2 plus the bench-next and listener variants; `name_wr_mutant.py`; `gsi_mutants.py` | R411-2 | 616cbdf1e54a56420e35b53cd161116702f7172d |
| Docs | CLEAN (S2, S3 suggestions) | three suite READMEs; 00 F00.2; 09 F09.4; PR body and disposition line against the published patch; `make check`; `gen_matrix --check`; `git diff --check`; commit shape | R411-2 | 616cbdf1e54a56420e35b53cd161116702f7172d |

## Commands and receipts

All commands ran in the foreground. Builds used a head export (`git archive`, with every file hash checked against the tree) under `scratch/`, with the simulator's `-j 0` capped by `scripts/verilator-capped.sh` so that at most 8 compile jobs ran at once.

| Receipt | What |
|---|---|
| `receipts/tool_identity.txt` | simulator identity, versions and hashes |
| `receipts/suite_{rx_validator,acmp_listener,acmp_nvm,pp_top}_v5050.log` | the four changed suites, rc 0 |
| `receipts/acmp_mutants/c1`, `c2` (`results.json`, logs, `.stdout`), `summary.txt` | `python3 tb/pp_top/acmp_mutants.py --jobs 4 --only ...`, in two chunks, rc 0 |
| `receipts/probes/*` | `scripts/r411_2_probes.py`: P1/P2 at head and at `a9ce0fa`, the bench-next variant, and the `tb/acmp_listener` variant |
| `receipts/name_wr.stdout`, `receipts/name_wr/`, `receipts/gsi.stdout`, `receipts/gsi/` | the two untouched drivers, rc 0 |
| `receipts/make_check.log`, `receipts/gen_matrix_check.log`, `receipts/diff_check.txt` | documentation and diff gates |
| `receipts/hosted_checks.txt` | exact-head hosted contexts at two times |
| `receipts/clone_integrity.txt` | the clone at exact head: index modes and blobs equal the tree, worktree blobs equal the index, no status lines, no gitlinks (the repository has no `.gitmodules`) |

A note on judging the bench-next golden: its only edit is the bench edit, so `judge()` grades it by its mutant rule. Its PASS therefore reads as `SURVIVED` with run_rc 0 and no failing check.

## Real limits

- **Simulator.** The simulator path named in the brief (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`) is absent on this host. Every receipt used the standalone Verilator 5.050 build at `$VALIDATION_TOOLS/verilator-v5.050` (identity in `receipts/tool_identity.txt`), the version the hosted workflow pins. The author's 5.052 was not used.
- **Full processor sweep not run** (outside the allowance): `run_suites.sh` over 33 suites, and `lint_hdl.sh`, since `hdl/` is unchanged. I ran only the four suites this PR changes.
- **`d3_mutants.py` (83 controls) not run.** Its `tb/pp_top` mode is `--d3-only`, which does not run section AC. Its other suites' round-2 changes are comments only (`acmp_nvm`) or one comment line (`rx_validator`). The goldens of all three pass in my runs.
- **Parent consumer set not run** (outside the allowance). I checked the disposition line only statically, against the driver and the published patch.
- **Spec texts.** IEEE 1722.1-2013/2021 and Milan v1.2 are not distributed and were not available here. The edition and table labels are checked for consistency with each other and with the PR's table.
- **Manager's exact-head banks.** I found no public manager bank result at `616cbdf`: the PR and issue threads hold only the `a9ce0fa2` bank (5903837095), and evidence commit `2650a1e5` holds the author and round-1 material. I relied on my own runs.
- **Hosted, at 12:32 UTC.** One push-event run, 36711587963, at the exact head:
  - `docs-gates`: success;
  - `portability`: success;
  - `suites`: still in progress.
  No pull_request-event run exists for this head.
- **Hardware.** None was used. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Merge composition.** Not judged. Processor main is at `0451d83d`, and C2 lands next.

## Pending manager duties

- Post the parent consumer bank at dev `ccdd07b5`: the combined #132 + C1 adaptation plus the `acmp_mutants.py` disposition line, 16 commands.
- Accept the hosted `suites` context at the exact head once it completes, and the hosted/act result.
- Rule on S2 (caption note), and optionally add S1 and S3 to the residue checklist. R411-1 S3 and S4 stay recorded as retained.
- After C2 lands: the main merge, the delta review, and the final current-dev candidate (source base `b2db3a97`, live dev `ccdd07b5`).
- Merge requires two independent positives and the full completion bar. The internal round R410-2 is in flight.

R411-2 FINISHED
