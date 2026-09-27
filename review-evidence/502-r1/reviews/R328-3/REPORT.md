[R328] POSITIVE - exact head 867a2e38a4e3231545a0a24b97d1e5612a6659fe

Round R328-3: internal independent review of PR #579 for issue #502 (tree `d0c5cc45362c34d2db66d61bc051659da50df2a1`, parent `5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e`).

- Assignment: issue 502 comment 5854008765.
- Review type: a DELTA review of `5d4cf33e..867a2e38`. Round R328-2 covered `5d4cf33e` in full.
- The delta is one commit. It changes five files: `CHANGELOG.md`, `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md`, `docs/reference/SUBMODULES.md`, `tb/verilator/pp_shadow/README.md` and `tb/verilator/pp_shadow/sim_main.cpp`.
- No RTL, firmware, configuration or gitlink changes (`receipts/delta_scope.txt`).

## Summary

The verdict is POSITIVE. No BLOCKER, MAJOR or MINOR finding is open at this head, and every lens is covered clean. One optional SUGGESTION is recorded (S1).

- **R328-2 F1 = R329-2 F1 is CLOSED.** `CHANGELOG.md:39-40` now reads "Actual parent phase-5 map writes raise the same sticky source." / "Unchanged map records raise nothing." `docs/reference/SUBMODULES.md:61` now reads "The parent's actual-write enable supplies the map trigger." Neither line says every commit beat raises pending, and neither names the processor's phase-5 export. Both match `milan_datapath.sv:4269-4271`, which feeds `KL_pp_shadow.sv:388,945-946` through `milan_datapath.sv:7498`.
- **R328-2 S1 is CLOSED.** The committed control `sim_main.cpp:1459-1469` uses the same record layout as my round-2 probe; only the sequence numbers differ. My unchanged `r328_2_dp_mutants.py` now kills P4 in both legs, by name:
  - static leg: `K12 partial refusal input sticky_pending_PP_STAT` and `sticky_pending_PP_NVM_STAT` (2 failures);
  - dynamic leg: the same two checks for input and for output (4 failures).
- **R328-2 S2 is CLOSED** for both parts:
  - `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1263` now reads "from the first actual write". This matches its own change-indication column.
  - The live PR body no longer contains the "prepared locally / has not been applied" sentence.
- **R329-2 S1 is CLOSED.** It is the same PR-body sentence, and it is gone.

## What was checked (assignment items)

### (1) Documentation now describes the delivered trigger

- `CHANGELOG.md:36-44` (the #502 entry):
  - Line 39 names the parent's actual phase-5 write as the source.
  - Line 40 says unchanged records raise nothing. This matches the committed `K12 duplicate input/output` controls and the round-2 P3 result.
  - The entry no longer claims that every accepted commit beat raises pending.
- `docs/reference/SUBMODULES.md:57-62`: the map trigger is the parent's actual-write enable, not the processor's phase-5 export. The name line (PR 121 export) is unchanged and correct.
- Stale wording search across the repository, excluding submodules and `docs/history`: no remaining claim of the superseded trigger in delivered-behaviour text. Three hits remain in `SAVED_STATE_MATERIALIZATION.md`:
  - lines 1658, 2061 and 2117 describe the proposed D3 record-writer trigger and its limits;
  - none of them describes the #502 pending source;
  - none was touched by this PR.
  The PR's own section 1 text (`:128-134,145`) and section 2 addendum (`:224-248`) name `amap_edit_live_wr_p` as the actual phase-5 write enable.

### (2) Committed K12 partial-refusal control

Setup, `sim_main.cpp:1459-1469`:
- `pending_boot(6)` starts durable. The harness itself checks "K control: reset/load permits durable status" at 0x40 with backend pending 0.
- The command is a two-record ADD. Record 0 claims key 0.
- Input: record 1 changes the stream channel under the same cluster key.
- Output: record 1 changes the cluster under the same stream/channel key.
- The control runs in both map directions under the dynamic fixture, and for input under the static fixture.

Grading:
- Refusal status 7 (`pending_command(..., 7)`).
- Unchanged, empty map (`pending_map_value(type, 0, ...)`).
- Zero phase-5 records, marks and storage changes.
- No durable claim over unsaved state.
- Both sticky pending bits clear at the end. The bits are sticky, so any transient rise during the abort is still caught.

Receipts:
- Shipping, `receipts/pp_shadow_make.log`: 591 + 591 + 591 + 295 checks, zero failures. This includes every `K12 partial refusal input/output` check.
- P4, unchanged `r328_2_dp_mutants.py` (`receipts/r328_dp_mutants/summary.txt`, `fails/P4_no_phase5.*`): killed in both legs by the named checks listed in the summary.
- The other mutant results are the same as the round-2 published results, except P4, which now dies:
  - killed: P1 (dynamic), P2, P3, P6, S1;
  - survive, as the source-level equivalence argument predicts: E1, E2, P5;
  - P1 survives in the static leg, which has no output map.
- Unchanged `r328_2_multirec_probe.py` (`receipts/r328_multirec/`):
  - shipping: 327 checks, 0 failures;
  - P4 datapath: the committed `K12 partial refusal input/output sticky_pending_*` checks fail, and so do the probe's own Q1/Q2 checks (8 failures).
- Reviewer harness mutant `scripts/r328_3_harness_mutant.py` (`receipts/harness_no_conflict_summary.txt`). It deletes only the record-1 conflict line, so both records are identical. The control then fails on:
  - response status (0, expected 7);
  - GET_AUDIO_MAP count (1, expected 0);
  - phase-5 records (2);
  - `K12 partial refusal input/output live_state_changed` and both sticky pending checks.
  So the status, map and pending grading can each fail.

### (3) Scope, other reviewer's scripts, PR body

- **Scope:**
  - `git diff --name-status 5d4cf33e..867a2e38` lists only the five files above.
  - The gitlinks are identical.
  - Zero paths changed under `hdl`, `sw`, `syn` or configuration.
  - The commit message is a single line with no trailers.
- **The other reviewer's round-2 scripts, run unchanged:**
  - `r329_campaign.sh` (`receipts/r329_campaign/results.txt`):
    - The unchanged round-1 script refuses its stale round-1 anchors (M1, M2, M4 to M6, M8 to M10). The script prints these as REFUSED by design, and they are not kills.
    - Its live mutants M3 and M7 are killed.
    - The adapter's thirteen mutants are killed by named checks in every leg that can observe them. U8 input-only passes the static leg, which has no output map, and is killed in the dynamic leg.
    - M5, M9 and U5 now also fail the new `K12 partial refusal *` checks.
    - The control passes 295 dynamic and 189 static checks.
  - `r329_dp_mutants.py` (`receipts/r329_dp_mutants/RESULTS.txt`):
    - D1 is killed in the dynamic leg and survives the static leg, which has no output.
    - D2 and D3 are killed in both legs.
    - The shipping datapath is unchanged after the campaign.
  - `r329_equiv_expand.py 104c8a54 867a2e38` returns rc 0 (`receipts/r329_equiv_expand_head.txt`).
  - `r329_probe.py` on shipping: 327 checks, 0 failures (`receipts/r329_probe/`).
- **PR body** (`receipts/pr579_view.json`):
  - Live head `867a2e38`, not a draft.
  - The stale publication sentence is gone.
  - The round-3 section's numbers match my reruns: P4 kills with 2 static and 4 dynamic failures, 24 parent-pulse mutation legs (18 + 6) with no build failures or refused anchors, and a 327-check probe.
  - The body correctly labels its sweep, builder and OOC numbers as round-2 evidence that was not repeated.
  - No stale line remains.

### (4) Gates

`scripts/r328_3_gates.sh` is the round-2 gate script with only the head SHA changed and one extra delta range. Summary is in `receipts/gates_summary.txt`; every gate returned rc 0:

- `git diff --check` over three ranges: `831f94f4..`, `104c8a54..` and `5d4cf33e..867a2e38`;
- RTL lint;
- em dash, doc style, TOC, anchors and doc paths;
- submodule docs, diagram generator and PNGs;
- test evidence;
- port contracts, SV/C++/Python idiom and RTL source lists;
- naming;
- `docs_check`, wire accountability, feature status and module matrix;
- `xvlog_gate`, `ci_events`, NVM capture and bare-metal-only;
- NVM firmware self-test and `nvm_backend`;
- no-Git `docs_check` plus feature status.

`make -C tb/verilator/pp_shadow` returned rc 0 (above). `make -C tb/verilator/pp_shadow pending-mutant` returned rc 0: "PASS: late-mark mutant killed by K10 and K12; clean control passes" (`receipts/pending_mutant.log`).

## Findings

No BLOCKER, MAJOR or MINOR finding.

### S1 - SUGGESTION - Tests - tb/verilator/pp_shadow/sim_main.cpp:1369,1421 - status and map-count checks in the refusal controls carry no case tag

- **Evidence:** in `receipts/harness_no_conflict.log` the status and map-count failures print as the generic `K command: response status` and `K12 GET_AUDIO_MAP record count`. Only the log position ties them to the partial-refusal case. The same applies to the existing `K12 refused record *` controls. The sticky-pending, durable and storage checks are tag-qualified, and those are the checks that kill P4.
- **Impact:** diagnosis only. A regression still fails the suite.
- **Optional:** pass the case tag into these two labels.
- **Verification:** the no-conflict harness mutant would name the case in all of its failures.

## Round-2 findings at this head

| Finding | Severity | Status | Evidence at 867a2e38 |
|---|---|---|---|
| R328-2 F1 = R329-2 F1 (changelog and pin-history trigger text) | MINOR | CLOSED | `CHANGELOG.md:39-40`; `docs/reference/SUBMODULES.md:61`; against `milan_datapath.sv:4269-4271,7498` and `KL_pp_shadow.sv:388,945-946` |
| R328-2 S1 (P4 phase-5 term unguarded) | SUGGESTION | CLOSED | `sim_main.cpp:1459-1469`; P4 killed by `K12 partial refusal input/output sticky_pending_PP_STAT/_PP_NVM_STAT` in both legs |
| R328-2 S2 (ownership row "accepted"; PR body sentence) | SUGGESTION | CLOSED | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1263`; live PR body |
| R329-2 S1 (PR body sentence) | SUGGESTION | CLOSED | live PR body |
| Round-1 findings (closed in round 2) | - | remain CLOSED | the committed checks still kill M5, M6 and U11, and my P3 mutant, at this head (`receipts/r329_campaign/results.txt`, `receipts/r328_dp_mutants/summary.txt`) |

## Lens results

```text
[R328] PASS Conformance - CHANGELOG.md:36-44; docs/reference/SUBMODULES.md:57-62; hdl/milan/milan_datapath.sv:4269-4271,7498; hdl/milan/KL_pp_shadow.sv:388,945-946 at 867a2e38; receipts/delta_scope.txt - the delivered map source is still the parent's actual phase-5 write (option (a), decision 5848417938), RTL byte-identical to 5d4cf33e, and the published description now states that trigger and that unchanged records raise nothing; issue #502 acceptance (name and map pending from the first live write through mark and commit, with unchanged, reset and group controls) still holds on the 591/591/591/295 run.
[R328] PASS RTL - receipts/delta_scope.txt (zero hdl/sw/syn/config paths in 5d4cf33e..867a2e38, identical gitlinks); receipts/r329_equiv_expand_head.txt (rc 0 against 104c8a54); receipts/gates/lint_rtl.log, port_contracts.log, sv_idiom.log, wire_acct.log - no RTL change in the delta. The round-2 RTL result, covered clean at 5d4cf33e, carries to 867a2e38 because nothing in RTL scope changed.
[R328] PASS Robustness - tb/verilator/pp_shadow/sim_main.cpp:1459-1469 at 867a2e38; receipts/pp_shadow_make.log, r328_multirec/, harness_no_conflict_summary.txt - the malformed multi-record case (refused at record 1 after record 0 claimed a key) is now committed from a durable baseline in both directions: status 7, empty map, no storage change, both pending bits clear. The harness mutant shows each of those gradings can fail. Existing refusal, duplicate, REMOVE, zero-record, static-refusal, repeat, ACK and reset controls pass.
[R328] PASS Tests - tb/verilator/pp_shadow/{sim_main.cpp,README.md} at 867a2e38; receipts/r328_dp_mutants/, r329_campaign/results.txt, r329_dp_mutants/RESULTS.txt, pending_mutant.log, r329_probe/ - the new control kills P4 by name in both legs, and M5, M9 and U5 now also hit it. The equivalence controls (E1, E2, P5) still survive, the other mutants are killed where observable, and pending-mutant passes. S1 is optional.
[R328] PASS Docs - CHANGELOG.md:39-40; docs/reference/SUBMODULES.md:61; docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1263; tb/verilator/pp_shadow/README.md:91-94; SAVED_STATE_MATERIALIZATION.md:128-146,224-248 (unchanged, re-read); live PR #579 body; receipts/gates_summary.txt - every changed line describes the head, the README states the new control exactly as coded, no superseded trigger claim remains in delivered-behaviour text, the PR body has no stale line, and all documentation gates pass with and without Git.
```

## Completion ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | CHANGELOG #502 entry; SUBMODULES pin history; datapath pulse and shadow input; issue #502 acceptance; full pp_shadow run | R328-3 | 867a2e38a4e3231545a0a24b97d1e5612a6659fe |
| RTL | CLEAN | delta scope (no RTL, firmware, config or gitlink change); equivalence expansion; lint, port-contract, idiom and wire gates. Full RTL review at 5d4cf33e, whose RTL scope 867a2e38 leaves untouched | R328-2 (full) and R328-3 (delta) | 5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e (RTL bytes identical at 867a2e38a4e3231545a0a24b97d1e5612a6659fe) |
| Robustness | CLEAN | `sim_main.cpp:1459-1469`; multirec probe; harness no-conflict mutant; full pp_shadow run | R328-3 | 867a2e38a4e3231545a0a24b97d1e5612a6659fe |
| Tests | CLEAN | `sim_main.cpp`, `README.md`; R328-2 and R329-2 mutant scripts unchanged; pending-mutant; probes | R328-3 | 867a2e38a4e3231545a0a24b97d1e5612a6659fe |
| Docs | CLEAN | CHANGELOG; SUBMODULES; SNAPSHOT_OWNERSHIP:1263; pp_shadow README; MATERIALIZATION sections 1 and 2; live PR body; docs gates (Git and no-Git) | R328-3 | 867a2e38a4e3231545a0a24b97d1e5612a6659fe |

## Real limits

- **Tool path substitution.** The assigned simulator path (`.../372-manager-candidate1/pinned-tool-bin/verilator`) did not exist at run time. I used the issue-502 pinned wrapper instead (`$VALIDATION_STORAGE/502-manager-r1/pinned-tool-bin/verilator`), which reports version 5.050 rev v5.050. Its binary hashes are in `receipts/tool_identity.txt`. It is the same wrapper my round-2 receipts used. Build parallelism was capped at 8, or at 2 per job for the other reviewer's four-way campaign (`scripts/env/`).
- **Not rerun.** The full parent, PP, gPTP and Yosys banks, the builder, OOC synthesis and the 55-suite sweep were not rerun (out of scope for this round). No timing, hardware, physical-calibration or field claim is made. Declared field skips are not hardware proof.
- **Isolation.** All probes ran in disposable copies under the packet's scratch directory. The review clone was never modified: `receipts/restore_check.txt` shows exact HEAD and tree, index equals HEAD, a clean worktree with zero untracked or ignored entries, every tracked blob rehashed with zero mismatches, and all three required gitlinks at their recorded commits with clean checkouts.
- **Order of reading.** Prior public round-2 findings were read only after the independent pass over the delta. No other round-3 report was read. The round-2 scripts were taken unchanged from `502-review-evidence` commit `15178bd9d4ae2b6e6b31c162c6d379ffbe9bb025` (`scripts/round2-unchanged/`).

## Pending manager duties

- **Hosted evidence at 867a2e38** (`receipts/hosted_check_runs.tsv`, sampled during this round):
  - completed with success: `rtl-fast`, Verilator shards 0/5 and 3/5, Yosys shards 0/4 to 3/4, `yosys-elaboration`, `verilator-lint`, docs checks and `full-ci-gate`;
  - still running: Verilator shards 1/5, 2/5 and 4/5;
  - skipped context: Physical gPTP.
  Exact-head `verilator-suites` completion, act acceptance and the hosted verdict belong to the manager.
- **Merge candidate.** Build and validate the current-dev candidate: source base `831f94f4`, live dev `e0920d77`. Then perform post-merge containment.
- **Final confirmation.** Confirm the second positive review for this round. Merge only with explicit maintainer authorization.

R328-3 FINISHED
