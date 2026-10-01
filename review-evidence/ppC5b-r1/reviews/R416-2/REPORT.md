[R416] POSITIVE - exact head 2acd4025782bff4aabbae73252476be34ea8b00d

# R416-2: internal independent review of PR #138 (issue #76, lane C5b, AECP dispatch), round 2

- Exact head `2acd4025782bff4aabbae73252476be34ea8b00d`, tree `f48cee13fd42ee303ec28e488277a3b0f17be65f`. I reviewed it in a detached clone.
- Round-1 head: `54c1e2b1`. Source base for the merge: `d5f73bac158276a9fcf549185bad5c65c0498dae`.
- Assignment: #76 comment 5921225908. Review start: PR #138 comment 5924928384.
- Scope is seven commits on top of 54c1e2b1:
  - the merge a4ba9f7 of main d5f73bac (PRs #136 and #135);
  - b0b30ea, f7fa70b, a91fe0e, 9437b16, 44fda60 and 2acd402.
- Not judged here: processor main has since moved to 3f3ea56b (C4). That merge belongs to a later merge-only round.

## Verdict

**POSITIVE.** There is no open MINOR, MAJOR or BLOCKER at this head, and all five lenses are CLEAN.

Each of the four round-1 MINOR findings is resolved, each with its own evidence:
- SET_CONTROL's out-of-range body;
- the line floor's write past the reservation;
- the undocumented 1008 ceiling;
- `git diff --check`.

All five round-1 suggestions were taken. The only exception is the two non-STREAM short-lane guards, for which the author gives a reachability argument that I accept (see S-R2 below).

Execution evidence (pinned simulator 5.050; at most 8 parallel jobs; all foreground):
- **Suites:** every processor suite rc 0. That is 33 suites, 1,017,973 checks, 0 failures; `tb/pp_top` alone is 8562 checks / 0 failures across its default, fixture and 584-byte line builds.
- **Mutation campaigns:** every arm is KILLED by its named check, and every golden is green:
  - this lane's 35 AECP dispatch arms;
  - the merged #135 adp_engine campaign (30 arm runs);
  - the merged #136 MAAP campaign (29 arm runs);
  - D3 (12/12);
  - the name-write mutant.

## Reconstruction (order followed)

1. AGENTS.md / CONTRIBUTING.md, docs/README, and the issue #76 body with its maintainer and manager comments. That includes the round-2 assignment 5921225908, which lists items (1) to (6) and the parent-visible-list requirement.
2. Authorities:
   - IEEE 1722.1-2021 7.4.25.1 (SET_CONTROL response carries the current value, "the old value if it fails") and 7.3.5.2 (IDENTIFY's step of 255);
   - Milan 5.4.1 (responses above cdl 524);
   - the integrator contract for `RESP_BASE_P` / `DESC_LINE_BYTES_P` (integrator guide section 5, 07 §3.3.1/§3.3.2, F01.5, the top's banner).
3. `git diff d5f73bac..2acd4025` plus each round-2 commit individually, and the merge's combined diff.
4. Public evidence:
   - the milan-fpga `review-evidence/ppC5b-r1` tree at 28314916 (author-r2 HANDOFF, PR-BODY and receipts);
   - the manager's evidence comments;
   - the PR body's "Parent-visible, for the pin-adoption lane" list.
5. Only after the independent pass above: the round-1 public findings of R416-1 and R417-1, each resolved below.

## Item-by-item judgement of the assignment

### (1) Merge a4ba9f7 of main d5f73bac — `receipts/merge-check.txt`

- **Parents and base.** The parents are 54c1e2b1 and d5f73bac, with merge-base 0451d83d.
- **One-sided files.** No file changed on only one side differs from that side at the merge. That holds for 42 main-side files and 50 lane-side files.
- **Both-side files.** Four files changed on both sides:
  - Two are line-multiset equal to each side's own change: `docs/00_MILAN_COMPLIANCE_REVIEW.md` and `tb/pp_top/README.md`. The README tail keeps both sides.
  - Two were resolved by hand, and the combined diff shows both sides kept:
    - In `tb/pp_top/Makefile`, `.PHONY` carries `maap-internal` (main) and `aecp-dispatch` (lane).
    - In `main()` of `tb/pp_top/sim_main.cpp`, `maap_only` and `aecp_only` both join `one_section`, and both section runners are called.
- **Patches.** No patch was re-anchored: the merge touches no `*.patch`. 9437b16 moved the 34 then-existing patches as pure renames (similarity 100%).
- **#135/#136 still passing:**
  - adp_engine suite 1367/0 and its campaign 30/30 KILLED (`adp-engine-mutants.txt`);
  - maap 196/0, rx_validator 497/0, `pp_top maap-internal` 34/0, and the MAAP campaign 29/29 KILLED (`maap-mutants-chunk{A,B}.txt`).

### (2) SET_CONTROL out-of-range (b0b30ea; R416-1 F1 / R417-1 F2)

- **The new arm.** `tb/pp_top/sim_main.cpp:10819` `sctrl_out_of_range_carries_255()` runs while IDENTIFY holds 255:
  - LK3b: the holder, under its own lock, sends SET_CONTROL(IDENTIFY, 128).
  - LK3c: after the unlock, a second controller sends the same command.
- **What each requires.** Each requires BAD_ARGUMENTS byte-exact at cdl 17, carrying 255. The shared `refused()` helper checks that nothing is written, marked or notified. Only the second controller's case waits for an absent unsolicited frame; that is correct, because a notification never goes back to the controller that asked. LK3c also re-reads 255 on GET_CONTROL and on the debug face.
- **Conformance.** The RTL is `gen_ucode.py:1818-1819`, which branches to `SCTRL_EMIT`, the shared tail that carries the value in force. That matches IEEE 1722.1-2021 7.4.25.1. 128 is neither 0 nor 255, so it is out of range under 7.3.5.2's step.
- **Mutation.** `sctrl-badarg-zero-body.patch` (branch to the zero-bodied `E_BADARG1`) is KILLED, with 2 failures, both named LK3b/LK3c (`mutants-chunkA.txt`).
- **Parent-visible list.** The PR body's list names the change: "SET_CONTROL's out-of-range BAD_ARGUMENTS now carries the value in force (before: zero)". Docs 06 §6.8 and 09's Identify row cite LK3b/LK3c.

### (3) Line-size contract (f7fa70b; R416-1 F2 / R417-1 F1), RTL change

- **Buffer size.** `hdl/aecp/KL_aecp_engine.sv:903` sets `RESP_BUF_C = 16 + LINE_BYTES_P`, with no rounding.
- **Write bound.** Every response write is bounded by that value:
  - `KL_aecp_resp_buf.sv:292` drops any byte at or past `RESP_BYTES_P`;
  - the D8 APPEND cap is `RESP_D8_CAP_BYTES_P = RESP_BUF_C` (`:1690`).
- **Refusals.** There are three elaboration refusals (`:927-940`), each naming `DESC_LINE_BYTES_P`:
  - step: `% 8`;
  - floor: `RESP_BUF_C < 24 + 8*71`, i.e. line < 576;
  - ceiling: `RESP_BUF_C > 1024`, the 10-bit cursor, i.e. line > 1008.
- **Range check by derivation.** 24 + 8·71 − 16 = 576, and 1024 − 16 = 1008. The µCPU's own guard (`KL_aecp_ucpu.sv:271-274`, ≤ 1024) is consistent with this, and a legal line now makes the buffer whole 8-byte lanes.
- **Evidence from the bench:**
  - `line-guards` (`pp_top-builds.txt`): 576, 584 and 1008 lint clean; 568, 1016 and 580 are refused, each with a message that names `DESC_LINE_BYTES_P`.
  - AX RB (`sim_main.cpp:11162`) at the 584-byte line build: 218/0.
- **My own probe** at the range ceiling, which the bench does not run: `probe-line-ceiling.txt`, `scripts/probe_line_build.sh`.
  - AX alone at lines 1008 and 1000: 218/0 each.
  - No strobed response byte lands at or past `RESP_BASE_P + 16 + line`.
  - OV1's whole-line read reaches the reservation's last byte.
- **Mutations.** All four line arms are KILLED: `line-floor-rounded`, `line-ceiling-dropped`, `line-buffer-fixed-592` and `rb-rounded-buffer-no-page-cap`.
- **Parent.** The parent's 576 is the floor, so it stays legal, and nothing changes at 576 (592 bytes either way).
- **Docs.** The range appears in:
  - the integrator guide row (`docs/guides/integrator.md:86`, and `:214` for the reservation);
  - F01.5 (`01_overview.md:162`);
  - 07 §3.3.1 (`07_memory_maps.md:288`);
  - the top banner (`protocol_processor_top.sv:118`);
  - the PR's parent-visible list.
- **Disclosure of `$error`.** The parent-visible list says the refusal is an elaboration `$error`, which a `-Wno-fatal` simulation build only warns about. My probe `elab-error-vs-fatal-probe.txt` shows `$fatal` behaves the same under `-Wno-fatal`, so the choice costs nothing and the disclosure is accurate.

### (4) `.gitattributes` exemption (a91fe0e)

- **The line.** `.gitattributes:5` exempts `tb/pp_top/aecp_dispatch_mutations/*.patch` (`-blank-at-eol,-blank-at-eof`), the same way as the srp_top, maap and adp_engine directories.
- **Gate result.** `git diff --check d5f73bac..HEAD` and `0451d83d..HEAD` are both rc 0 (`clone-diff-check.txt`, `clone-integrity.txt`).
- **The exemption is needed.** With the line removed in a scratch clone, `git diff --check 0451d83d HEAD` is rc 2 with 7 trailing-whitespace hits, all in those patches and none elsewhere (`attr-necessity-probe.txt`).
- **Lane C5a is untouched.** The exemption does not reach lane C5a's `tb/pp_top/aecp_mutations/` (check-attr: unspecified).

### (5) Rename (9437b16)

- **New names.** The driver is `tb/pp_top/aecp_dispatch_mutants.py`, its 35 patches are in `aecp_dispatch_mutations/`, and the Makefile target is `aecp-dispatch-mutants` (`tb/pp_top/Makefile:102`, `.PHONY` `:142-143`).
- **No stale references.** `git grep` finds no `aecp_mutants`, `aecp-mutants` or `aecp_mutations/` anywhere in the tree, so `aecp_mutants.py` and `aecp-mutants` are left to lane C5a's PR #140.
- **Arms.** Every arm is still KILLED: 35/35 over two chunks, plus three green controls (`aecp-dispatch`, `aecp-line`, `line-guards`).

### (6) Suggestions taken

**44fda60, `scripts/check_m9_opcodes.py`:**
- It counts every `OP_*_C` localparam in any form. It refuses an unparsed one, and it refuses one opcode carried by two names.
- The docstring's "eight fixtures, six of which must fail" matches the code: a parse check plus seven cases, six of which fail.
- Results:
  - the gate passes with 30 opcodes;
  - the selftest gives 8 of 8;
  - my residual probe (`m9-gate-residual-probe.txt`) shows that a multi-declarator statement fails closed.

**2acd402:**
- **AX RD3** (`sim_main.cpp:11096`): READ_DESCRIPTOR after a power-cycle D3 restore, with no SET since the reset. It covers:
  - AUDIO_UNIT 0, CLOCK_DOMAIN 0, STREAM_INPUT 0 and STREAM_OUTPUT 1, each carrying the restored value;
  - an unset STREAM_OUTPUT 0, which still serves its image.
- **AX RD4** (`:11129`): a configuration-0 STREAM_OUTPUT of 80 bytes with a set row is served as its image whole. `rd-str-short-guard-nop` is KILLED.

## Round-1 public findings: disposition at this head

| Round-1 item | Disposition at 2acd4025 | Evidence |
|---|---|---|
| R416-1 F1 / R417-1 F2 (MINOR): SET_CONTROL out-of-range body is ungraded and not in the parent-visible list | **Resolved** | LK3b/LK3c; `sctrl-badarg-zero-body` KILLED; PR-body list names it |
| R416-1 F2 (MINOR): undocumented 1008 ceiling, refused through an internal parameter | **Resolved** | The engine refuses by `DESC_LINE_BYTES_P`; range in guide/F01.5/07/banner/list; line-guards; my 1000/1008 probe |
| R417-1 F1 (MINOR): a 561..575 line wrote past the `16 + LINE` reservation | **Resolved** | Floor 576, buffer exactly 16 + line; AX RB at 584 and in my 1000/1008 probe; `rb-rounded-buffer-no-page-cap` and `line-buffer-fixed-592` KILLED |
| R416-1 F3 (MINOR): `git diff --check` rc 2 | **Resolved** | `.gitattributes:5`; rc 0; exemption shown necessary (7 hits without it) |
| R416-1 S1: short-lane overlay guards ungraded | **Taken for STREAM** (RD4, KILLED arm); see S-R2 | |
| R416-1 S2 / R417-1 S1: M9 gate robustness and count wording | **Taken** | 44fda60; selftest 8/8; residual probe |
| R417-1 S2: the D3-restore half of the READ_DESCRIPTOR claim | **Taken** | AX RD3 |

## Findings at this head

None at MINOR, MAJOR or BLOCKER.

### S-R2 — SUGGESTION — Tests, Robustness — the AUDIO_UNIT and CLOCK_DOMAIN short-lane guards stay ungraded

- **Where:** `hdl/aecp/ucode/gen_ucode.py`, the READ_DESCRIPTOR overlay guards for AUDIO_UNIT and CLOCK_DOMAIN. These sit alongside the STREAM guard that RD4 grades.
- **Evidence:** 2acd402 and the 06 §6.1 text argue these two are unreachable. A SET_SAMPLING_RATE or SET_CLOCK_SOURCE, and their restore rules, are judged against the descriptor's own list and count, which a descriptor short of the lane does not hold. So no row can be set over one.
- **Assessment:** By inspection the guards use the same COMPARE / BR_STATUS idiom that RD4 kills, and they are defensive only.
- **Impact:** None reachable.
- **Suggested outcome (optional):** state the unreachability next to each guard in `gen_ucode.py`, or record a NOP arm as an expected survivor with that reason.

## Five lenses

- **Conformance — CLEAN.**
  - IEEE 1722.1-2021 7.4.25.1: SET_CONTROL's out-of-range refusal now carries the old value (255), graded byte-exact.
  - Milan 5.4.1: the oversize path is unchanged at the default line, and a 71-record GET_AUDIO_MAP page fits the 576 floor's 592-byte reservation.
  - No AEM behaviour changes at the parent's 576.
- **RTL — CLEAN.**
  - f7fa70b: the buffer is exact; the bound at `resp_buf:292` drops writes past it; the refusals are correctly derived from `GAMAP_PAGE_MAX_C` and the 1024-byte cursor; and they agree with the µCPU's own cap guard.
  - Lint (`lint_hdl.sh`) is OK for every top.
- **Robustness — CLEAN.**
  - Line values outside the legal range are refused at elaboration with an integrator-facing name.
  - The range edges 576, 584, 1000 and 1008 were exercised end to end with no write outside the reservation.
  - The M9 gate fails closed on malformed or duplicated opcode declarations.
  - S-R2 is a defensive-only residual.
- **Tests — CLEAN.**
  - 33 suites rc 0; static and builder gates rc 0 (`static-gates.txt`, `pregates.txt`).
  - 35/35 dispatch arms KILLED, including the three new kinds: zero body, line and buffer, and the short guard.
  - The #135 and #136 campaigns are all KILLED; D3 is 12/12; the name-write mutant is killed.
  - `git diff --check` rc 0.
- **Docs — CLEAN.**
  - The integrator guide, F01.5, 07 §3.3.1/§3.3.2, the top banner, 06 and 09 state the range and the exact reservation.
  - The PR's parent-visible list covers the line range, the exact buffer, the SET_CONTROL body and the rename.
  - `make check` (mermaid, wavedrom, links, matrix, parameters 26/26/26) and `gen_matrix --check` are rc 0.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | gen_ucode.py SET_CONTROL arm (:1807-1832), LK3b/LK3c, IEEE 1722.1-2021 7.4.25.1 / 7.3.5.2, Milan 5.4.1, GAMAP page fit | R416-2 | 2acd4025782bff4aabbae73252476be34ea8b00d |
| RTL | CLEAN | KL_aecp_engine.sv:895-940, :1690, :2005; KL_aecp_resp_buf.sv:292; KL_aecp_ucpu.sv:271-282; ucpu_pkg.sv GAMAP_PAGE_MAX_C; protocol_processor_top.sv:114-170; lint_hdl.sh | R416-2 | 2acd4025782bff4aabbae73252476be34ea8b00d |
| Robustness | CLEAN | line-guards (576/584/1008 pass; 568/580/1016 refused); reviewer probe at 1000/1008; $error vs $fatal probe; M9 gate residual probe; RD4 short STREAM | R416-2 | 2acd4025782bff4aabbae73252476be34ea8b00d |
| Tests | CLEAN | 33 suites (1,017,973 checks); pp_top 8562/0 incl. AX RB/RD3/RD4/LK3b/LK3c; aecp-dispatch-mutants 35/35; adp_engine 30 runs; MAAP 29 runs; D3 12/12; name-write; merge check; git diff --check rc 0; exemption necessity probe | R416-2 | 2acd4025782bff4aabbae73252476be34ea8b00d |
| Docs | CLEAN | integrator.md:86/:214; 01_overview.md:162; 07_memory_maps.md:284-318; 06/09 LK3b/LK3c/RD rows; 00_MILAN_COMPLIANCE_REVIEW.md; tb/pp_top/README.md; PR body parent-visible list; make check; gen_matrix --check | R416-2 | 2acd4025782bff4aabbae73252476be34ea8b00d |

## Commands and receipts

All commands ran in the foreground with at most 8 parallel jobs (the simulator's `-j 0` is capped at 8 by `scripts/verilator-wrapper.sh`). Every receipt is listed in `MANIFEST.sha256`.

- `receipts/toolchain.txt`: the simulator's identity is 5.050, with binary sha256 recorded. The assignment's named wrapper path is absent on this host. I used the same pinned binary through `scripts/verilator-wrapper.sh` and checked its identity by version and hash.
- `receipts/static-gates.txt`, `receipts/pregates.txt`: lint, docs `make check`, matrix, image-generator test, UPC map gate, and the M9 gate with its selftest.
- `receipts/suites-chunk{1,2,3}.txt`, `receipts/suites-chunk4-pp_top.txt`, `receipts/suites-total.txt`, `receipts/pp_top-builds.txt` (via `scripts/suite_chunk.sh`).
- `receipts/mutants-chunk{A,B}.txt` and `receipts/aecp-dispatch-mutants-chunk{A,B}.results.json`: this lane's campaign.
- `receipts/adp-engine-mutants.txt`, `receipts/maap-mutants-chunk{A,B}.txt`, `receipts/d3-mutants-c1.{txt,results.json}`, `receipts/name-wr-mutant.txt`: the merged and neighbouring campaigns.
- `receipts/merge-check.txt`, `receipts/clone-diff-check.txt`, `receipts/attr-necessity-probe.txt` (via `scripts/attr_necessity_probe.sh`).
- `receipts/probe-line-ceiling.txt` (via `scripts/probe_line_build.sh`), `receipts/elab-error-vs-fatal-probe.txt` (via `scripts/elab_error_probe.sv`), `receipts/m9-gate-residual-probe.txt` (via `scripts/m9_gate_residual_probe.py`).
- `receipts/clone-integrity.txt`, re-verified at the end:
  - HEAD, tree and index tree are exact;
  - porcelain status (ignored files included) is empty;
  - 0 tracked files differ in content or mode;
  - the repository has no submodule gitlinks.

Every probe ran in disposable copies under the packet's `scratch/` directory, which is not published. The clone was never modified.

## Real limits

- **Hosted CI.** I did not inspect hosted CI or act results; the manager owns hosted/act acceptance.
- **Banks not run.** I ran no parent, gPTP, Yosys or builder bank and no consumer bank. The parent's 576 and the parent's explicit pass of it rest on the round-1 public record and the PR body, not on a run of mine at dev e4b771f9.
- **Elaboration refusals.** These were exercised under the pinned simulator's lint only, not under a synthesis tool.
- **Hardware.** No physical calibration and no hardware run. Field skips are not hardware proof.
- **Later merge.** The later merge of processor main 3f3ea56b (C4), which conflicts in `tb/pp_top`, is out of scope for this round.
- **Resumed session.** This review resumed after a host session restart. Receipts written before the restart were reused after I checked them against the head, and the clone integrity, `git diff --check`, the M9 gate and the exemption probe were re-run at the end.

## Pending manager duties

- Run the donor bank and the parent consumer bank at dev e4b771f9, and build the final current-dev candidate at the merge turn. Source base is d5f73bac; live dev is e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b.
- Hosted/act acceptance at the exact head, separating executed jobs from skipped contexts.
- The later merge-only round against processor main 3f3ea56b.
- Obtain the second independent positive review (R417-2) before merge.

R416-2 FINISHED
