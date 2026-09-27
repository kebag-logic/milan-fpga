[R329] POSITIVE - exact head 90ab4a3da5b676f90b768b4f22b77ce7d0bd911d

Round R329-5 is an external independent review of PR #579 for issue #502.

- Head: `90ab4a3da5b676f90b768b4f22b77ce7d0bd911d`, tree `34132a7625cf046e17a00c6a4b8130ef56999e04`.
- Delta judged: `92c6154a17d1f1192f20a3a642e6a01b616afb67..90ab4a3d`, one commit.
- Source base of the whole change: `831f94f4146cc45ec476f8c8dcf5afac7cd8eacf`.

**Summary.** R329-4 F1 is closed. Section 13 of the ownership contract now gives the pending composition the RTL has, and both design pages agree with `hdl/milan/KL_pp_shadow.sv:945-957`. I read both pages end to end and swept the whole tree. No current-state statement of the pending sources, the `pend_i` composition, the trigger or the D2 bit contradicts the RTL at this head. The only code changes are label-only: I compared every check position against the parent build and the verdicts and values are identical. The CSR edit is a comment rewrap. The focused targets and the docs gates pass locally. No MINOR, MAJOR or BLOCKER finding is open. There are four optional suggestions.

## Findings

None at MINOR or above.

### Complete list of remaining stale or loose pending/trigger/composition wording in the tree

This is the one list the assignment asked for. Every item is non-blocking. None is a current-state statement that contradicts the RTL. The per-hit and per-section dispositions are in `receipts/sweep_disposition.md`.

- **S1 - SUGGESTION - Docs - `docs/design/SAVED_STATE_MATERIALIZATION.md:1697-1698` - the stage table omits the direct pulse term.**
  - Evidence: this round added the direct pulse `aecp_live_wr_w` to the documented composition. The section 10 prose (:1710-1712) and 5.2 (:494-495) now retire both the pulse and `aecp_live_pend_r`. The table cells in the same section still say only that "the sticky pending source stops taking live name writes" (stage 2) and that "the sticky live-name/map bit is deleted" (stage 3). The PR body line "Proposed stage retirement accounts for both the direct pulse and sticky history" is true of the prose, not of the table.
  - Impact: none on the shipped behaviour. This is proposed D3 text. The final composition (:493) and the prose 13 lines below are complete, and an extra one-cycle pulse after stage 3 could not produce a false durable reading.
  - Suggested outcome: name both terms in the two cells, for example "stops feeding names to the live pulse and its sticky history" and "the live pulse and sticky history leave `pend_i`".
- **S2 - SUGGESTION - Tests - `tb/verilator/pp_shadow/sim_main.cpp:1447` - one check in the preload helper is still untagged.**
  - Evidence: `pending_preload_map` now takes a tag and passes it to its GET_AUDIO_MAP diagnostics. Its own `K12 preloaded baseline durable` check prints the same label four times, for the duplicate and remove cases in both directions (`receipts/pp_shadow_pending_leg_head.log`, lines 132, 154, 253, 275).
  - Suggested outcome: prefix that label with `tag`, as the round did for the exact-record check.
- **S3 - SUGGESTION - Docs - `docs/design/SAVED_STATE_FASTCONNECT.md:1380` - "That manager" has lost its antecedent.**
  - Evidence: this PR rewrote section 12.2 (:1371-1378). The sentence that ended with "the missing manager's job" is gone, so "That manager is proposed in ..." now follows "Neither group has a record writer yet", which is a different noun.
  - Suggested outcome: "That record writer is proposed in ..." or equivalent.
- **S4 - SUGGESTION - Docs - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1280-1281` - the present-tense cause is historical.**
  - Evidence: the text reads "The channel-map and name rows are now REPORTED, because donor scope D2 landed. Issue #502 makes accepted live writes sticky instead." Read together, the two sentences are accurate. Read alone, the first gives D2's marks as the current cause, but at head the marks end on `unused_aecp_marks_w` (`KL_pp_shadow.sv:942-943`). The row table above it (:1273-1274) is correct.
  - Suggested outcome: "were first reported when donor scope D2 landed; since #502 they are reported from accepted live writes".

Checked by hand and **not** a finding: the `PP_STAT[11]` row in `docs/reference/REGISTER_MAP.md:2239`. It describes the pending sources generically ("a change the producer still holds"), this PR does not change it, and it is not stale against #502.

## Round-4 findings

| Item | State at 90ab4a3d | Evidence |
|---|---|---|
| R329-4 F1 (MINOR; Docs, Conformance): ownership :1354-1355 gave the pre-#502 `pend_i` as current | **CLOSED** | Now at :1361-1365, "Current parent use", `pend_i = aecp_dyn_dirty_o \| (\|nvm_unflushed_w) \| aecp_live_wr_w \| aecp_live_pend_r` and `aecp_live_wr_w = aecp_name_wr_w \| amap_live_wr_i`. This is byte-for-byte the RTL at `KL_pp_shadow.sv:945-946, 956-957`, and it points to 6.1. D2's use is labelled "Original parent use" at :1388. The materialization page states the same equation at :130-135. A whole-tree `pend_i *=` search at head returns only these two current equations, the two proposed D3 equations (:493, :614) and two harness input drives (`receipts/tree_grep_head.txt`). |
| R329-4 S1 (SUGGESTION): `K12 GET_AUDIO_MAP exact record` untagged | **CLOSED** | `sim_main.cpp:1429-1432` uses `"%s GET_AUDIO_MAP exact record"`. In the head log it prints `K12 input/output`, `K12 duplicate input/output` and `K12 remove input/output` (`receipts/compare_run-pending.txt`). |
| R329-4 S2 (SUGGESTION): `milan_csr.sv:197` "No CSR" alone on a line | **CLOSED** | Rewrapped at :197-199. The code tokens are identical to the parent (`receipts/code_token_check.txt`). |

## Earlier public findings on this PR, rechecked at this head

I read these only after my own pass and the ledger below were complete.

| Finding | State | Evidence at 90ab4a3d |
|---|---|---|
| R328-1 F1 = R329-1 F2 (refused-at-validation control) | CLOSED | `K12 refused record input/output` passes: status 7, count 0, pending clear. Values are identical to the parent (`receipts/compare_run-pending.txt`). |
| R328-1 F2 (materialization section 1 and 5.2) | CLOSED | :130-141 and :490-496, reconciled this round (see the full read). |
| R328-1 F3 (TESTING campaign table) | CLOSED | `docs/testing/TESTING.md:268` |
| R328-1 S1 = R329-1 F3 (an unchanged duplicate set pending) | CLOSED | `milan_datapath.sv:4269-4271` requires an actual change. The duplicate controls pass with pending clear. "Conservative duplicate" has zero hits in the tree. |
| R328-1 S2 (observer anchored on triggers) | CLOSED | The storage-based observer is unchanged. The delta is label-only. |
| R329-1 F1 (REMOVE from a durable baseline) | CLOSED | `K12 remove input/output` passes. The late-mark mutant fails both remove pairs (`receipts/pending_mutant_head.log`). |
| R329-2 F1 = R328-2 F1 (CHANGELOG and SUBMODULES trigger text) | CLOSED | `CHANGELOG.md:38-40`, `docs/reference/SUBMODULES.md:59-62` |
| R329-2 S1 = R328-2 S2 (PR body "prepared locally") | CLOSED | Absent from the live body (`receipts/pr579_body_live.md`). |
| R328-2 S1 (P4 survived) | CLOSED | The partial-refusal controls are unchanged in value (`receipts/compare_run-pending.txt`). |
| R328-2 S2 (ownership "first accepted write") | CLOSED | :1273 reads "from the first actual write". |
| R329-3 F1 and S1, R328-3 S1 | CLOSED | :2097-2103 reads "RESOLVED by #502"; :1731 and :2086 are labelled historical; the refusal tags are present in the head log. |

## What was verified

1. **The only code change is a label refactor with no behaviour change.**
   - `git diff --raw 92c6154a 90ab4a3d` touches four files: the two design pages, `milan_csr.sv` and `tb/verilator/pp_shadow/sim_main.cpp`. No gitlink changed (`receipts/delta_stat.txt`).
   - `code_token_check.py` strips comments and compares code tokens. It reports `milan_csr.sv` as changed bytes with identical tokens, and `KL_pp_shadow.sv`, `milan_datapath.sv` and `KL_nvm_backend.sv` as blob-identical (`receipts/code_token_check.txt`).
   - I built all four pp_shadow legs at the parent and at head in scratch exports, using the same submodules. `compare_legs.py` matched every check position: the PASS/FAIL state, `got` and `exp` are identical at every one of 591/591/591/295 positions, and only labels differ. There are 14 relabels in each 591 leg (the pending cases run there too) and 28 in the pending leg, all tag additions (`receipts/compare_run-*.txt`, `receipts/per_leg_counts.txt`).
2. **pp_shadow at head** with Verilator 5.050: `make -j4 -C tb/verilator/pp_shadow` returned rc 0, with 591 + 591 + 591 + 295 checks and 0 failures (`receipts/pp_shadow_default_summary.txt`).
3. **The late-mark mutant** (`make -C tb/verilator/pp_shadow pending-mutant`, run from a head export) returned rc 0. The clean control passed 295/0. The mutant failed 12 named checks: K10, K10 repeat, K12 input, K12 (output), K12 remove input and K12 remove output, each on `no_durable_claim_over_unsaved` and `pending_from_accepting_edge` (`receipts/pending_mutant_head.log`).
4. **Docs gates at head, all rc 0**, with the hash-locked Markdown environment (`receipts/docs_gates.txt`):
   - `docs_check.py` in Git mode, and with `GIT_DIR=/dev/null` (0 findings; the no-Git mode skips inventory parity);
   - `check_em_dash.py --base 831f94f4…` and `--base 92c6154a…`;
   - `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_doc_paths.py`;
   - `git diff --check` over both ranges;
   - `lint_rtl.py --check`: PASS, 90 of the ratchet's 90.
5. **Full read of both pages.** I read `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` (1938 lines) and `SAVED_STATE_MATERIALIZATION.md` (2249 lines) in full. The section-by-section disposition is in `receipts/sweep_disposition.md`, sections 3 and 4. I checked each new claim of the round against RTL:
   - A refused RELOAD leaves ownership unchanged: `KL_nvm_backend.sv:1128-1133`.
   - The reset row: records open at reset, and a whole-record WRITE or an accepted RELOAD closes them (`:1128-1133`).
   - `nvm_pend = pend_r | unres`: `:786, 790`.
   - Pending falls in the no-load terminal state once nothing is open and no producer work remains, while committable work and writer retirement still refuse the durable reading. This is consistent with the W4 text at :793-808.
   - The accepting-edge claim holds: the pulse enters `pend_i` combinationally and the backend registers it on the write edge.
   - The unchanged map program skips `NVM_MARK`: processor `gen_ucode.py:1789-1791`.
6. **Whole-tree sweep** (`sweep.sh`): 27 pattern hits and 39 name/map-pending hits, each disposed in `receipts/sweep_disposition.md`. The zero-hit patterns are `aecp_mark_pend`, "conservative duplicate", "every commit beat", "D2 sticky" and "D2 bit".
7. **PR body** (`receipts/pr579_body_live.md`, live at the head). It has no stale lines. Its round-5 claims all hold: the equation, byte-identical shadow, datapath and backend, unchanged CSR tokens, and unchanged stimuli, expected values and check counts. The one overstatement is the stage-retirement sentence, covered by S1.
8. **The RTL, re-read at head.** The pending latch uses the same `clk_i` and the synchronous `rst_n` style as the backend's registers (`KL_nvm_backend.sv:754-786`). No CDC is involved. The lint ratchet is unchanged at head.

## Reviewer-owned lens ledger

| Lens | Result | Examined artifacts (at head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #502 acceptance and decisions (comments 5844866872, 5846418959, 5848417938, 5854533678 items 1-3) against `KL_pp_shadow.sv:925-957`, `milan_datapath.sv:4245-4271` and processor `gen_ucode.py:1765-1795`. K10/K12 on the shipping glue: `receipts/pp_shadow_pending_leg_head.log` and `receipts/pending_mutant_head.log`. Ownership 6.1 and 13, materialization 1 and 2 against RTL | R329-5 | 90ab4a3da5b676f90b768b4f22b77ce7d0bd911d |
| RTL | CLEAN | `receipts/code_token_check.txt`: `milan_csr.sv` comment-only; shadow, datapath and backend blob-identical to 92c6154a. The pending glue `KL_pp_shadow.sv:925-957` (one clock, synchronous reset matching `KL_nvm_backend.sv:754-786`, no CDC, sticky until reset). The qualified map pulse `milan_datapath.sv:4269-4271`. `lint_rtl.py --check` PASS (`receipts/docs_gates.txt`) | R329-5 | 90ab4a3da5b676f90b768b4f22b77ce7d0bd911d |
| Robustness | CLEAN | `sim_main.cpp:1449-1505`: zero-record, refused-at-validation (status 7), two-record partial refusal (status 7), static-output refusal, duplicate, REMOVE, and reset through `pending_boot`, in both directions. All pass at head with values identical to the parent (`receipts/compare_run-pending.txt`) | R329-5 | 90ab4a3da5b676f90b768b4f22b77ce7d0bd911d |
| Tests | CLEAN (S2 optional) | `sim_main.cpp:1418-1505`: the delta is label-only, proved position by position across all four legs (`receipts/compare_run-*.txt`). Counts 591/591/591/295 (`receipts/per_leg_counts.txt`). The late-mark mutant is killed by 12 named checks (`receipts/pending_mutant_head.log`) | R329-5 | 90ab4a3da5b676f90b768b4f22b77ce7d0bd911d |
| Docs | CLEAN (S1, S3, S4 optional) | Both design pages read end to end (`receipts/sweep_disposition.md` sections 3-4). Whole-tree sweep (`receipts/tree_grep_head.txt`, `receipts/tree_grep_namemap_pending.txt`). `CHANGELOG.md:35-45, 254-281`, `SAVED_STATE_FASTCONNECT.md:1371-1380`, `SUBMODULES.md:57-62`, `KL_nvm_backend.sv:196-204`, `milan_csr.sv:180-199`, `pp_shadow/README.md:50-102`. Docs gates (`receipts/docs_gates.txt`). Live PR body (`receipts/pr579_body_live.md`) | R329-5 | 90ab4a3da5b676f90b768b4f22b77ce7d0bd911d |

All five lenses are covered clean at the exact head. The other internal review, R328-3, is POSITIVE at `867a2e38`. RTL and test artifacts have changed since then only as proved above: comments in the CSR file, and labels in the harness.

## Real limits

- Physical calibration was NOT RUN. The field and freshness skips are not hardware evidence. This PR makes no materialization, flash-persistence or hardware claim, and I tested none.
- I ran only focused targets: pp_shadow (all four legs at both commits), pending-mutant, the docs gates and lint. I did not run the full parent, processor, gPTP, Yosys or builder banks, `milan_dp`, `nvm_cosim` or `nvm_backend`. The delta does not touch their sources, apart from the comment-only CSR file.
- The assigned simulator path (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`) does not exist on this host. I used a copy of the round-5 manager wrapper for the same 5.050 package. Its `verilator_bin` sha256 `44898b22…` matches the identity recorded in R329-4 (`receipts/tool_identity.txt`).
- **Hosted evidence at the head is not accepted here.** A read-only snapshot (`receipts/hosted_check_runs_head.tsv`) showed:
  - `docs-check` as **failure**. The job failed in its "Install the pinned sv2v release" step on an HTTP 500 download error, before any gate ran (`receipts/hosted_docs_check_failed_step.txt`). That is an infrastructure failure, not a content verdict; the same gates pass locally.
  - `rtl-fast`, `elaborate` and Verilator shards 1, 2 and 4 of 5 in progress.
  - Physical gPTP skipped. A skipped context is not an executed job.
- The public evidence tree named in the assignment (`dc9d0928…/review-evidence/502-r1`) is the round-1 author packet archived on 2026-09-26, not a bank run at this head. I found no head-specific manager bank evidence published on the issue or the PR.
- Every probe ran in scratch exports under the packet. After the runs I removed the in-clone build residue: `pp_shadow` object directories, generated hex files and `__pycache__`, all created after the clone at 11:23:46. Then I verified the clone: HEAD `90ab4a3d`, `write-tree` = tree `34132a76`, index equal to the head tree, 911 tracked files hash-identical, four gitlinks unchanged, and zero untracked or ignored entries in the parent and in the three initialised submodules (`receipts/integrity_after.txt`).
- I made no GitHub writes, source edits, commits or pushes, and did not use Docker, act or hardware. Host paths in receipts are abbreviated as `$CLONE`, `$PACKET`, `$VALIDATION_STORAGE`, `$PINNED_TOOL_ROOT` and `$MD_VENV`.

## Pending manager duties

- Re-run and accept the hosted contexts at this head. `docs-check` needs a rerun after its sv2v download failure. Also finish `rtl-fast`, `elaborate`, the Verilator shards and the act replica.
- Publish head-specific bank evidence, if the claimed static, builder and native banks are to be cited for `90ab4a3d`.
- Build and validate the candidate merge on live dev `e0920d77162284d8da52ffaf13a973e451e44f90` (source base `831f94f4`), then run post-merge containment.
- Optionally route S1-S4. None affects coverage.
- Obtain maintainer merge authorization.

R329-5 FINISHED
