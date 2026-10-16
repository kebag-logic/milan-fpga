[R588] POSITIVE - exact head b2460b79b399a2c383d8d912c8d017b78e5e4072

# R588-2 internal cleared-context re-review: issue #708 / PR #754

- Head: `b2460b79b399a2c383d8d912c8d017b78e5e4072`, tree `4cc342899bae1253e7e4f63435c4ba2550f1d020`. In the review clone, the index tree, the worktree bytes and modes (1,371 tracked files) and all six gitlinks equal the head (`receipts/clone_integrity.txt`). The live PR head is the same commit.
- Delta under review: `5c6f50ee..b2460b79`, two one-line commits with no trailers (`receipts/delta_commits.txt`):
  - `aa0818b6`: R588-1-R1 and R588-1-R2;
  - `b2460b79`: R588-1-F1.
- Four files change (`receipts/delta_raw.txt`, `receipts/delta.diff`): `docs/design/MAILBOX_SPLIT.md`, `docs/reference/SUBMODULES.md`, `hdl/milan/milan_datapath.sv` (+2 comment lines) and `sw/firmware/ctrl/test/acmp_walk.cpp` (comment only). No record, test body, generated artifact, gitlink or `syn/` file changes. There was no dev merge and no Vivado run.
- Source base: dev `734eb780dc93896a5961cd95180f79475a401650`. Live dev `1f6f2f57177f1dd904654c317009461b43423989` was not merged or validated here.
- Reconstructed from:
  - AGENTS.md and the #708 scope decisions (assignment 6094788195, the 08:46 ruling, flow decision 6100507393, resume 6207474061);
  - the round-2 assignment (PR comment 6219696478) and the REVIEW READY at this head (issue comment 6220369357);
  - the live PR body;
  - the delta and its commits;
  - the processor source at the pinned `2cbed0a9`;
  - the public archive `review-evidence/708-r1` at `34fe4ec1`.
- Prior public findings (R588-1 comment 6219686641, R589-1 comment 6219051857) were read only after my own pass over the delta. Their disposition is given below.
- No open BLOCKER, MAJOR or MINOR. One RESIDUE and one SUGGESTION are recorded. All five lenses are clean at this head.

## Findings

### R588-2-R1 - RESIDUE - Docs - the PR body calls the two-line selector-6 note "a one-line comment"

- Where: the PR body, Round 2 bullet F1 (live body line 52, identical to `review-evidence/708-r1/author-r2/PR-BODY.md`): "`hdl/milan/milan_datapath.sv`'s selector 6 now has a one-line comment like those on selectors 4 and 7."
- Evidence: the note is two `//!` lines, `hdl/milan/milan_datapath.sv:5190-5191`. The selector-4 note it imitates is also two lines (`:5174-5175`). The REVIEW READY comment repeats "a one-line comment".
- Impact: wording only. It changes no measurement, figure, verdict, test, code, generated artifact or clause claim.
- Exact fix: in the PR body, replace "now has a one-line comment like those on selectors 4 and 7" with "now has a two-line comment like those on selectors 4 and 7".
- Verification: read the PR body.

### R588-2-S1 - SUGGESTION - Docs - the selector-6 source note omits the unsettled case

- Where: `hdl/milan/milan_datapath.sv:5190-5191`: "an input's stream_vlan_id [63:48] is unused: the processor replaces it with all 16 received VLAN bits (#708)".
- Evidence: at `2cbed0a9`, `protocol_processor_top.sv:3536-3539` replaces the half-word with `bound_vlan_r[sink]` only while the sink index is in range and probing_status is COMPLETED. Otherwise it replaces it with 16'd0.
  - The note's operative claim, that the parent's half-word is unused, is exact: the only reader of `gsi_data_i` for an input's selector 6 is that arm, which keeps only `[47:0]`.
  - The pin page (`docs/reference/SUBMODULES.md:210-212`) states both cases.
- Optional wording: "... the processor replaces it with all 16 received VLAN bits while settled, 0 otherwise (#708)". Taking it would need the comment-only RTL gates run again. Not taking it is acceptable.

### Comment-rule scan of the delta

The added source comment lines carry only `#708`, `#665` and `processor issue #168`. They contain no lane label, lane name, review round, reviewer ID or issue-comment ID. The one comment ID that was there (`comment 6030067436`) was removed. No RESIDUE under the owner's comment rule.

## Disposition of prior public findings at this head

| Finding | Status at `b2460b79` | Evidence |
|---|---|---|
| R588-1-F1 (MINOR, Docs) | **Resolved** | See the verification under F1 below |
| R588-1-R1 (RESIDUE) and R589-1-R1 (RESIDUE), the same defect | **Resolved** | `sw/firmware/ctrl/test/acmp_walk.cpp:65` reads "first, so it governs (#665)." No `comment <id>` remains in the file |
| R588-1-R2 (RESIDUE) | **Resolved, with the exact prescribed text** | `acmp_walk.cpp:43-44`: "this walk normalised LD1 and LD2 in the walk, and LD3's status byte in its scenario, before comparing". `docs/design/MAILBOX_SPLIT.md:784-785`: "normalised the first two in the walk and the third's status byte in its scenario before comparing". Checked against base `734eb780`: the walk zeroed LD1's talker fields and restored LD2's `acmpsta`, and `ListenerScenario.LD3TheLockRefusalStatus` rewrote `e.frames[0].b[2]`, the status byte, before its `memcmp` |
| R588-1-S1 (SUGGESTION, Tests) | Not taken; it is optional | Unchanged: walk the two other #168 convergences |
| R588-1-S2 (SUGGESTION, Tests) | Belongs to the manager | sv2v 0.0.12 nvm_port guard issue |

**F1 verification.** I read each new statement against the processor at `2cbed0a9` (gitlink verified):

- "the processor serves STREAM_INPUT GET_STREAM_INFO selector 6's `stream_vlan_id`; a settled input reports all 16 received bits; an unsettled input reports 0" (`SUBMODULES.md:199,208-212`, PR body lines 49-50 and the #168 Scope row at line 96).
  - In `protocol_processor_top.sv:3508-3509`, `gsi_input_w` is kind 0 with descriptor type 0x0005.
  - At `:3536-3539`, the arm gives `[63:48] = (index < N_STREAM_IN_P && status[7:5] == PB_COMPLETED_C) ? bound_vlan_r[sink] : 16'd0`.
  - `bound_vlan_r` is `[15:0]` per sink (`:1021`). It is latched from the A15 settle (`:1921`) and cleared on disarm (`:1933`).
  - True.
- "GET_RX_STATE_RESPONSE also carries the full 16 bits" (`:214`). `KL_pp_acmp_listener.sv:698` sets `b_vlan_w = settled_w ? rec_r.settled_vlan : 16'd0`, and `pp_acmp_pkg.sv:152` declares `settled_vlan` as `[15:0]`. True.
- "The parent's selector-6 input VLAN halfword is no longer used" (`:216`).
  - The parent's `gsi_ans_raw_w` goes to `gsi_data_r` (`milan_datapath.sv:4900`), then to `pp_gsi_data_w` (`:5230`), then to the processor's `gsi_data_i` (`:8163`).
  - Inside the processor, `gsi_data_i` is read only at `:3530`, `:3533` and `:3539`. For an input's selector 6 only `[47:0]` survives.
  - True.
- "`acmp_bound_vlan_o` keeps 12 bits per sink" (`:218`). `protocol_processor_top.sv:692` declares `[N_STREAM_IN_P*12-1:0]`, and `:1042` drives it from `bound_vlan_r[v][11:0]`. True.
- No other current page contradicts these statements. A search of every first-party `*.md` outside `docs/history` for `stream_vlan`, `bound_vlan`, input VLAN ownership and 12-bit VLAN claims finds only the pin page itself.
- The required outcome is met.

## Lens coverage at this head

| Lens | Result | Artifact | What was checked and against what |
|---|---|---|---|
| Conformance | PASS | `docs/reference/SUBMODULES.md:199,208-218`; PR body lines 49-53 and 96; processor `hdl/top/protocol_processor_top.sv:1021,1042,3508-3539` and `hdl/acmp/KL_pp_acmp_listener.sv:698` at `2cbed0a9` | The new interface statements match the pinned RTL, which cites Milan 5.3.8.9 and 5.4.2.10 at `:3535`. The LD1-LD3 history and TD1 text that R588-1 graded against Milan v1.2 and IEEE 1722.1-2021 is unchanged apart from R1 and R2, which changes no clause claim. #708 acceptance is unchanged from round 1. The delta adds no requirement or interface change, and it documents the one that R588-1 found undocumented |
| RTL | PASS | `hdl/milan/milan_datapath.sv:5160-5205` at head vs `5c6f50ee`; `receipts/strip_compare_delta.log`; `receipts/lint_rtl_check.log` | Comment-stripped token streams of `milan_datapath.sv` and `acmp_walk.cpp` are identical between `5c6f50ee` and `b2460b79`, and no `//` line ends in a backslash. The same probe reports DIFFERENT on the walk across `734eb780..HEAD` (`receipts/strip_compare_control.log`), so it can fail. `lint_rtl.py --check --self-test --jobs 16` with Verilator 5.050 (identity in `receipts/verilator_wrapper.txt`) gives PASS, 90 <= 90, 18 waived. No RTL behaviour changes. R588-1's RTL coverage at `5c6f50ee` stands for everything else |
| Robustness | PASS | processor `protocol_processor_top.sv:1903-1935,3519-3539` | The boundary and state cases the new text claims were checked against RTL. An out-of-range input index answers 0. An unsettled (not COMPLETED) input answers 0. Unbind clears `bound_vlan_r` to 0, so a stale VLAN is never served. Reset zeroes it. The delta changes no executable path, so R588-1's Robustness evidence (pp_shadow, milan_dp, processor ACMP suites) still applies to identical code |
| Tests | PASS | `sw/firmware/ctrl/test/acmp_walk.cpp` (delta comment-only, token-identical); `receipts/delta.diff` | No test body, expectation, message string or mutant-referenced prefix changed, because only lines 43-47 and 65 changed and both are comments. The walk's 127/127 result and its old-pin controls from R588-1 still hold for identical code. The author's pp_shadow (317/0) and milan_dp (13 PASS) runs at this head are consistent with a comment-only RTL change, and I did not re-run them: the token-identity proof leaves nothing for them to detect. R588-1-S1 stays optional |
| Docs | PASS (R588-2-R1 RESIDUE, R588-2-S1 SUGGESTION) | `docs/reference/SUBMODULES.md:180-232`; `docs/design/MAILBOX_SPLIT.md:776-800`; `acmp_walk.cpp:42-66`; PR body; `review-evidence/708-r1/author-r2/{HANDOFF,PR-BODY}.md`; `receipts/*.log`, `receipts/gates_rc.txt` | F1, R1 and R2 are resolved as shown above. Gates at the head, all rc 0: `docs_check.py` (0 findings, 208 md); `check_em_dash.py --base 734eb780` (0 over 201 added lines) and `--base 5c6f50ee` (0 over 16); `gen_toc.py --check` and `--verify-anchors` (515 links); `check_submodule_docs.py`; `check_doc_style.py`; `check_doc_paths.py`; `check_port_contracts.py`; `measure_naming.py --check`; `submodule_boundaries.gen.py --check`. The first em-dash and TOC attempts exited 2 only because the pinned renderer was not on the default interpreter. They were re-run with the pinned lock (cmarkgfm 2025.10.22, html5lib 1.1) and passed. Both rows are kept in `gates_rc.txt`. The published `author-r2/HANDOFF.md` and `PR-BODY.md` re-hash to their `MANIFEST.json` `published_sha256`, and the archived PR body equals the live body apart from a trailing blank line |

## Reviewer ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | pin page and PR body VLAN statements vs processor top `:3508-3539` and listener `:698`; R1/R2 text vs base walk | R588-2 (delta); R588-1 for scope untouched since | `b2460b79b399a2c383d8d912c8d017b78e5e4072` (R588-1 at ancestor `5c6f50eefa4c5545f052ec843363ace5e7936e8a`; nothing in this lens's executable scope changed since) |
| RTL | CLEAN | `milan_datapath.sv` comment-only delta (token-identical), lint 90 <= 90 | R588-2 | `b2460b79b399a2c383d8d912c8d017b78e5e4072` |
| Robustness | CLEAN | processor out-of-range, unsettled, unbind and reset paths behind the new claims; no executable delta | R588-2; R588-1 for executable scope | `b2460b79b399a2c383d8d912c8d017b78e5e4072` (R588-1 at `5c6f50eefa4c5545f052ec843363ace5e7936e8a`, code identical) |
| Tests | CLEAN | `acmp_walk.cpp` comment-only delta (token-identical); no test change | R588-2; R588-1 for walk execution | `b2460b79b399a2c383d8d912c8d017b78e5e4072` (R588-1 at `5c6f50eefa4c5545f052ec843363ace5e7936e8a`, code identical) |
| Docs | CLEAN (one RESIDUE, one SUGGESTION) | pin page, MAILBOX_SPLIT, walk comments, PR body, archived handoff and body, docs gates | R588-2 | `b2460b79b399a2c383d8d912c8d017b78e5e4072` |

## Commands and probes (receipts under `receipts/`)

- `strip_compare.py <repo> 5c6f50ee b2460b79 hdl/milan/milan_datapath.sv sw/firmware/ctrl/test/acmp_walk.cpp` gives IDENTICAL, rc 0. The negative control `734eb780..b2460b79` on the walk gives DIFFERENT, rc 1.
- Docs gates as listed in the Docs row. `lint_rtl.py --check --self-test --jobs 16 --verilator <pinned 5.050>` passes.
- Read-only queries:
  - the PR body and comments;
  - the issue comments;
  - the archive tree at `34fe4ec1`, where `author-r2` differs from `author` only in HANDOFF.md and PR-BODY.md;
  - the exact-head check runs (`receipts/hosted_checks_snapshot.txt`).
- The review clone was only read. After lint, `git status --untracked-files=all` is empty (ignored paths excluded). The clone ends equal to the head: 0 byte and 0 mode mismatches over 1,371 tracked files, every gitlink exact, and submodule worktrees clean.

## Real limits

- Not re-run here: `tb/verilator/pp_shadow`, `tb/verilator/milan_dp`, the walk, any processor or gPTP suite, Yosys, `xvlog`, the builder bank, or Vivado. The comment-only proof makes them non-discriminating for this delta. Their evidence at this head is the author's published claims, and for identical code it is R588-1's runs at `5c6f50ee`.
- No manager source bank ran at this head, and none is claimed. The current-dev candidate (source base `734eb780`, live dev `1f6f2f57`) was not built or validated here.
- Hosted contexts at the exact head were mostly queued or in progress at the snapshot (2026-10-16T16:56:21Z): 8 success, 20 in progress, 16 queued. `Physical gPTP (nightly and manual)` is a skipped context, not execution evidence. This round claims no hosted or act acceptance.
- Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Current-dev merge-candidate validation (builder and native banks) at the merge turn, with receipts linked on the PR.
- Hosted `rtl-fast`, `verilator-suites` and `yosys-portability` evidence at the exact head.
- Carry R588-2-R1 to the residue checklist. R588-1-S2 (sv2v 0.0.12 nvm_port guard) still wants its own issue.
- Acceptance 5 (post-merge flash and soak), including the round-1 note on grading the shipping-launcher image's corners if it differs from the measured route's bitstream.

R588-2 FINISHED
