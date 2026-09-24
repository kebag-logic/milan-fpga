[R281] POSITIVE - exact head fb84de54ee9c1e3a2b51d2a239efbc04e4a22bad

# R281-2: external cleared-context re-review of issue #536 / PR #543 (correction round 1)

- Exact head `fb84de54ee9c1e3a2b51d2a239efbc04e4a22bad`, tree `24a2b1c9bd657d2d14b5e814f18ec349108ffc1f`, verified in the detached review clone.
- Source base `26d855a9176d63625e6635a029a0c44e3d57ce9a`, an ancestor of the head. 6 commits in total: the 2 of the first head plus the 4 of correction round 1 (`8179587ee`, `3753b5749`, `bfe2e5c79`, `fb84de54e`). Every commit is one line with no trailers.
- Diff base..head: 5 files, +405/-26:
  - `tests/steps/aecp_engine_model.py`
  - `tests/steps/aecp_engine_steps.py`
  - `tests/features/aecp_response_contract.feature`
  - `tests/README.md`
  - `docs/MILAN_V12_ROADMAP.md`
- No HDL, firmware or gitlink change. `protocol-processor` stays at `424c688fa2205b934a7689a58f2aa766420f2326` and `gptp-processor` at `c1b617435824929a790739ea8585c3fe1a328cc0`. Live dev `615b5a5d` carries the same two pins.
- **Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR is open. The prior findings R280-F1 to F3 and R281-F1 to F3 are all resolved at this head (see "Prior public findings"). Five SUGGESTIONs are recorded, and none affects coverage.
- All five lenses were applied at this head: Conformance, RTL, Robustness, Tests and Docs. All five are CLEAN.

## Reconstruction order

1. `AGENTS.md`, `CONTRIBUTING.md`, `docs/README.md`.
2. Issue #536: its body (acceptance 1-3) and the public comments. Those are the assignment, the first TAKEN and REVIEW READY, the correction-round assignment and the A230 REVIEW READY.
3. The #510 owner decision (issuecomment-5789766089: SYSTEM_UNIQUE_ID and MEDIA_CLOCK_REFERENCE_INFO held at RECOMMENDED), plus the PR body and the R281-2 review-start comment.
4. Specification text, from local plain-text renderings identified by sha256 in `receipts/spec_citation_check.txt`:
   - Milan v1.2: 4.2.4, 5.4.3.1 to 5.4.3.4, 5.4.4.1 to 5.4.4.5, Figures 5.2 to 5.7, Tables 5.18 to 5.21.
   - IEEE 1722.1-2021: Table 9-1, 9.3.5.3.3, 9.6.2 to 9.6.5.3.1 (Table 9-6), and Table 7-140 for 0x001B.
5. The pinned processor at `424c688`:
   - `hdl/aecp/KL_aecp_engine.sv`: MVU constants :697-719, the pop decode :1133-1150, `mvu_get_milan_info_w` :1284-1296, and the @26/@27 captures :3193-3197.
   - `hdl/packet_engine/KL_pp_rx_validator.sv:545-550`: 6/7 go to MVU, 2/3 to AA, everything else to the AEM bucket.
   - `hdl/top/protocol_processor_top.sv:83`: `RX_SLOT_BYTES_P = 576`.
   - `tb/pp_top/sim_main.cpp` M1 to M9.
6. The diff `26d855a9..fb84de54` and its commit history.
7. Executable evidence:
   - The published tree `765cb958.../review-evidence/536-r1`, author and correction packets.
   - The exact-head hosted check runs.
   - This round's own probes, below.
8. Only after this round's verdict and ledger were written (an interim draft of this file recorded them first): the prior public reviews R280-1 (PR comment 5806086835) and R281-1 (PR comment 5806267441), and the prior rounds' scripts in the evidence tree.

## Independent results at this head

- **Every new or changed MVU row was executed on the pinned RTL, and the model matched it byte for byte** (`receipts/rtl_vs_model.txt`).
  - **Setup.** A disposable copy of the pinned `tb/pp_top` was made, and all 52 of its source files equal the pinned blobs except the two noted in `receipts/probe_copy_integrity.txt`. It was built with the scoped Verilator 5.050 (identity in `receipts/toolchain.txt`) at 8 jobs. The only additions are a frame-injection probe placed after the harness's own MilanInfoPhase (`receipts/pp_top_probe.diff`) and a Makefile run step (`receipts/pp_top_makefile.diff`).
  - **The pinned suite still passes.** Its own checks through MilanInfoPhase (M1 to M9 included) ran first: 731 checks, 0 FAIL.
  - **How frames were built.** `scripts/rtl_vs_model.py` parses all 26 rows of the three MVU outlines out of the head feature. It builds each frame by calling that row's **own When step** from the head steps module. Only the envelope is rewritten to the pp_top identity: MACs, entity ids and a unique sequence_id.
  - **How frames were compared.** Each frame went through the RTL and through the head model, and the answers were compared on every octet, together with the RTL command and response counter deltas.
  - **Result: 26 of 26 rows are byte-exact, each with cmd+1 and rsp+1.** The 26 rows are:
    - the five Table 5.18 rows in their own figures (cdl 20, 28, 20, 92, 20; the cdl 92 echo is a 118-octet frame)
    - every protocol_id octet @22 to @27
    - both @26 nibbles
    - `C1-01`
    - r = 1
    - cdl 19
    - the junk reserved field
    - cdl 24 and cdl 112, both served (SUCCESS, cdl 32)
    - message types 0, 2, 4, 8, 10, 12 and 14, each echoed NOT_IMPLEMENTED under its own type plus one
  - **This closes the three rows the author could only reason about from the RTL.** The @26 high-nibble row `00-1B-C5-0A-D1-00`, the @26 low-nibble row `00-1B-C5-0A-C2-00` and the cdl 24 row now each have an executed RTL frame, and the model equals it.
  - **Extra frames I chose myself: 24 of 26 match.** They cover six more @26 values, @25 and @27 variants, served commands at cdl 21 to 500 with non-zero fill, command words 0x0001, 0x0005, 0x7FFF, 0xFFFF and 0x0100, the Figure 5.5 and 5.6 forms under a foreign protocol_id, and a junk tail after Figure 5.3. The two mismatches are cdl 592 and cdl 600: the RTL is silent and the model answers. That gap already existed before this PR (see S2).
- **Suites at head.**
  - Contract feature: 59 scenarios / 435 steps passed (`receipts/behave_contract_head.txt`).
  - Full behave suite: 14 features / 343 scenarios / 1736 steps passed (`receipts/behave_full_head.txt`).
  - Both tallies match the PR body and the README row.
- **Static gates at head**, all exit 0 (`receipts/static_gates.txt`):
  - `check_py_idiom`: every ratchet held.
  - `docs_check`: 0 findings.
  - `check_em_dash --base 26d855a9`: 0 findings over 2 added lines.
  - `check_feature_status`: 0 findings.
  - `git diff --check`: clean.
- **My mutation arms: 21 of 21 behave exactly as predicted** (`scripts/mutate_r281_2.py`, `receipts/mutation_arms_r281_2.txt`).
  - Method: one substitution per arm, each in its own disposable copy of `tests/`. The prediction is the exact set of failing feature lines, not just red or green.
  - Killed, each failing exactly its row or rows:
    - length floor lowered by one
    - length ceiling at 99 payload octets
    - reserved field forwarded into the body
    - @22..@23 not compared
    - @26 compared on its high nibble only
    - @26 compared on its low nibble only
    - message_type 14 decoded as MVU
    - r bit masked
    - every whole MVU command served
    - VU echo capped at 20 octets
    - Figure 5.4 body one quadlet long
    - Figure 5.6 name cut to 32 octets
    - Figure 5.5 id dropped
    - guard step ignoring its protocol_id cell
    - guard step without the extra octets (only the cdl 112 row fails; the cdl 24 case is equivalent because the 60-octet Ethernet pad carries the 4 claimed octets)
    - other-type step leaving message_type at 6
    - u-bit mask applied to message_type 6 (the two older issue #83 rows also fail)
    - MVU arm made unreachable
  - Predicted survivors: the control; a length ceiling at 100 payload octets (see S1); and the gate regex narrowed to `GET_`, which is equivalent at this pin.
  - Gate arm (`receipts/gate_arm.txt`): a copy of the pinned engine that adds `MVU_GET_SYSTEM_UNIQUE_ID_C = 16'h0002` fails exactly the RTL-gate scenario (feature:233).
- **The prior rounds' own scripts, run unmodified at this head.**
  - R280-1 `r280_mutations.py` (`receipts/prior_r280_arms_at_head.txt`): R1 to R8, R10 and R11 are RED and the control is green before and after. R9 survives, and R280-1 had already classified it as an equivalent mutant: the arms are disjoint on message_type.
  - R281-1 `mutate_model.py` (`receipts/prior_r281_arms_at_head.txt`): all nine arms are KILLED, including `mt_guard_dropped`, `len_exact_20`, `pid_head_22_23_dropped`, `pid_24_25_dropped`, `pid_26_dropped`, `pid_only_27` and `pid_27_dropped`. The baseline is green.
- **Citations.** Checked against the Milan v1.2 and IEEE 1722.1-2021 text, and every citation in the diff is correct (`receipts/spec_citation_check.txt`):
  - Figure 5.5 gives cdl 28 and Figure 5.6 gives cdl 92: @30 clock_domain_index; @32 flags, reserved and two priorities; @36 reserved; @40 a 64-octet name.
  - The 5.4.4.1 sentence "The value of this field is 1" and the Section 4.2.4 SHALL are each quoted verbatim, each under its own clause.
  - Table 5.19 and IEEE Table 9-6 both give NOT_IMPLEMENTED the value 1, and the 9.6.5.3.1 quotation is verbatim.
  - 9.3.5.3.3 is correctly scoped to AEM.
  - The Table 9-1 labels are correct, and 0x001B is DECREMENT_CONTROL (Table 7-140), which is not served.
- **Hosted, exact head, inspected read-only** (`receipts/hosted_check_runs.tsv`):
  - 22 check runs. 21 completed success: `changes`, `full-ci-gate`, `rtl-fast`, `verilator-lint`, `verilator-suites`, `yosys-elaboration`, `yosys-portability`, `bdd-conformance`, `docs-check`, `docs-check-no-git`, `wire-accountability`, `elaborate`, the 5 Verilator shards and the 4 Yosys shards.
  - `Physical gPTP (nightly and manual)` was **skipped**. It was not executed, and it is not hardware proof.
- **Candidate outlook** (read-only; the manager owns the candidate). `git merge-tree` of the head onto live dev `615b5a5d` is clean. The only overlapping path is `docs/MILAN_V12_ROADMAP.md`, and live dev keeps both processor pins, so the RTL evidence above applies to the candidate's pin.

## Findings

No BLOCKER, MAJOR or MINOR finding. The suggestions below are optional, and none of them affects lens coverage.

### S1 - SUGGESTION - Tests, Robustness

- **Location.** `tests/steps/aecp_engine_steps.py:421` (the guard step's fill `bytes(range(max(cdl - 20, 0)))`) and `tests/features/aecp_response_contract.feature:197-198`.
- **Title.** The over-length rows cannot reach the largest command the RTL accepts.
- **Authority and evidence.**
  - The engine's sub-decode has no ceiling. Its only upper bound is the 576-octet RX slot, which means cdl 564. `receipts/rx_slot_boundary_head.txt` shows the RTL serving GET_MILAN_INFO at cdl 564.
  - The rows stop at cdl 112. The step raises `ValueError` for any cdl above 276, because its fill counts up without wrapping.
  - Arm A02, a model ceiling at 100 payload octets, survives (`receipts/mutation_arms_r281_2.txt`). Arm A03, a ceiling at 99, is killed.
- **Impact.** A model that grew a ceiling between 101 and 552 payload octets would stay green while diverging from the RTL. No realistic regression of that shape is known. The exact-length and "Figure 5.3 plus one quadlet" regressions are both killed.
- **Suggested outcome.** Use a wrapping fill in the step, and add a served row at cdl 564, the RX-slot maximum.
- **Verification.** A02 turns red, and the row equals the RTL frame.

### S2 - SUGGESTION - Robustness, Tests (out of scope, predates this PR; recommend a new Issue)

- **Location.** `tests/steps/aecp_engine_model.py:342-345` (`deliver`: the payload is capped by the slot the frame carries, but an AVTPDU larger than the RX slot is not dropped).
- **Title.** The model answers AECP commands the RTL drops silently because they overflow the 576-octet RX slot.
- **Authority and evidence.**
  - `receipts/rx_slot_boundary_head.txt` and `receipts/rx_slot_boundary_base.txt`, run on the RTL probe. At cdl 565 and cdl 600 (AVTPDU 577 and 612 octets) the RTL is silent, with cmd+0, for GET_MILAN_INFO and for an unserved AEM opcode alike.
  - The head model answers both. The **base** model already answers the AEM case the same way.
  - `RX_SLOT_BYTES_P = 576` (`protocol-processor/hdl/top/protocol_processor_top.sv:83`).
- **Impact.** The model contradicts the engine above the slot size for every message type. No feature row sends such a frame, and this PR neither introduced the gap nor asserts anything there.
- **Suggested outcome.** A separate Issue: either model the RX-slot drop, or state the model's input bound.
- **Verification.** A row at cdl 565 expecting no frame, graded against the RTL.

### S3 - SUGGESTION - Docs (predates this PR; retained from R280-O1 / R281-1 S1)

- **Location.** `tests/features/aecp_response_contract.feature:32-36`, "NOTE ON THE DECODE".
- **Problem.** The note still says the dispatch arms read @22..@23 "without consulting the protocol". It has been stale since #83: the model's `aem` guard (`aecp_engine_model.py:371`) and the same file's #83 outline contradict it.
- **Status.** The diff does not touch it, and the PR body lists it for its own Issue.

### S4 - SUGGESTION - Tests (retained from R280-S1)

- **Location.** `tests/steps/aecp_engine_steps.py:907`.
- **Problem.** The MVU gate parses only `localparam logic [15:0] MVU_(GET|SET)_*_C = 16'hXXXX;`. A later pin that declares a served command at another width or radix would not be parsed, and the gate would stay green.
- **Suggested outcome.** Fail closed on any `MVU_(GET|SET)_` localparam the pattern cannot parse.
- **Status.** Still present at this head. At the current pin, arm A19 shows it is equivalent.

### S5 - SUGGESTION - Tests, Docs (retained from R280-S2)

- **Problem.** `SERVED_MVU` (`tests/steps/aecp_engine_steps.py:276`) is not tied to the ledger's `served_mvu_operations` (`docs/reference/milan_feature_status.json:37`). Both hold only GET_MILAN_INFO today.
- **Status.** This is the author's own recorded limitation.

## Clean-lens results (one line per lens, at the exact head)

```text
[R281] PASS Conformance - issue #536 AC1-3; #510 decision; tests/features/aecp_response_contract.feature:98-139 (MVU outline, Figures 5.3/5.5/5.3/5.6/5.7, cdl 32/28/20/92/20), :141-155, :156-199, :200-233; tests/steps/aecp_engine_model.py:74-91, :542-555, :678-696 (MVU_COMMAND_FORMS); receipts/spec_citation_check.txt; receipts/rtl_vs_model.txt - AC1: 0x0000 served with the Figure 5.4 body (status 0, cdl 32, protocol_version 1, flags 0, certification 0) and 0x0001-0x0004 answered NOT_IMPLEMENTED exactly as the pinned engine answers them, each in its own Milan figure; AC2: every row has a failing arm (A10/A11/A13/A14/A20, prior R7/R8/R11); AC3: behave and docs gates green; every Milan and IEEE citation in the diff checked against the text
[R281] PASS RTL - protocol-processor@424c688 hdl/aecp/KL_aecp_engine.sv:697-719, :1133-1150, :1284-1296, :3193-3197; hdl/packet_engine/KL_pp_rx_validator.sv:545-550; hdl/top/protocol_processor_top.sv:83; tb/pp_top/sim_main.cpp:2198-2437 - no RTL, processor pin or gitlink change (base, head and live dev all at 424c688 / c1b6174); the model's sub-decode terms (message_type 6, pld >= 8, @22..@23, @24..@25, @26, @27, whole @28 word), echo length and restated 20-octet body agree with the pinned RTL, executed: the pinned suite's 731 checks through MilanInfoPhase pass, then 26/26 head rows and 24/26 extra frames byte-exact (the 2 exceptions are the S2 pre-existing over-slot case)
[R281] PASS Robustness - tests/features/aecp_response_contract.feature:181-199 (per-octet and per-nibble protocol_id, r = 1, cdl 19 truncated, junk reserved, cdl 24/112 over-length), :208-225 (message types 0/2/4/8/10/12/14), :136-139 (maximum-length echo at cdl 92); receipts/rtl_vs_model.txt, receipts/rx_slot_boundary_*.txt - malformed/truncated input, min/max values, invalid ordering by message type and repeated independent commands all match the RTL; reset/backpressure are out of an offline model's scope and not claimed; the over-slot gap predates this PR and is S2
[R281] PASS Tests - tests/steps/aecp_engine_steps.py:390-441 (MVU, guard and other-type steps), :848-915 (protocol_id, body, quadlet and RTL-gate steps); receipts/mutation_arms_r281_2.txt (21/21 exact), receipts/gate_arm.txt, receipts/prior_r280_arms_at_head.txt (R1-R8, R10, R11 red; R9 equivalent), receipts/prior_r281_arms_at_head.txt (9/9 killed), receipts/behave_*_head.txt (59/435 and 343/1736) - each new row can fail for the defect it claims, arms fail exactly the predicted rows, the step refuses a figure mismatch, expectations are graded against the RTL rather than restated from the model; the ceiling mutant A02 survives (S1, optional)
[R281] PASS Docs - tests/README.md:90 (59, verified by run); docs/MILAN_V12_ROADMAP.md:539; comment/header text in the three test files (model :74-91, :283-302, :447-467, :542-555, :678-696; steps :36-98, :259-277; feature :14-15, :98-117, :141-168, :200-233); docs/reference/MILAN_COMPLIANCE_MATRIX.md:95-105, :130-136 and docs/reference/FR_NFR.md:143 (consistent, untouched, #537's rows); PR body; receipts/static_gates.txt - changed contracts are reflected, nothing obsolete restored, the PR and issue carry enough evidence for a cold reviewer; the stale pre-existing NOTE is S3
```

## Prior public findings on this PR

Each item was read only after this round's own verdict and ledger were written. The disposition is judged at `fb84de54ee9c1e3a2b51d2a239efbc04e4a22bad`.

| Prior item | Severity; lenses | Disposition at this head | Evidence |
|---|---|---|---|
| R280-F1 = R281-F1: the sub-decode outline pinned 3 of its guards | MINOR; Tests, Robustness | **RESOLVED** | Rows per octet @22 to @27, per @26 nibble, over-length at cdl 24 and 112, and message types 0, 2, 4, 8, 10, 12 and 14 (feature:181-199, :208-225). R280 R1 to R5 are RED and R281 `mt_guard_dropped`, `len_exact_20` and all the `pid_*` arms are KILLED. My A05 to A08 and A17 fail exactly their rows. All 26 rows equal the executed RTL frames. |
| R280-F2 = R281-F2: rows `0x0001` and `0x0003` sent a truncated Figure 5.3 frame | MINOR; Conformance, Tests, Robustness | **RESOLVED** | `MVU_COMMAND_FORMS` sends Figures 5.5, 5.3, 5.6 and 5.7, and the rows assert cdl 28, 20, 92 and 20. Those lengths match the Milan figures and the RTL (118-octet echo at cdl 92). R280 R10 is RED, my A11, A13 and A14 are killed, and the step refuses a mismatched figure. |
| R280-F3(a), retained by R281-1: IEEE 9.3.5.3.3 cited for the MVU echo | MINOR; Conformance, Docs | **RESOLVED** | The feature (:104-110) and the steps header (:91-98) now cite Milan Table 5.19, IEEE Table 9-6 and 9.6.5.3.1 (a verbatim quotation), call the command-length echo the engine's choice, and scope 9.3.5.3.3 to AEM. All of this was checked against the text. |
| R280-F3(b) = R281-F3: a Section 4.2.4 quotation under a 5.4.4.1 heading | MINOR; Docs, Conformance | **RESOLVED** | `aecp_engine_model.py:82-85` quotes 5.4.4.1's own sentence and attributes the SHALL to Section 4.2.4. Both are verbatim. |
| R280-S1: the MVU gate regex parses only `[15:0]` / `16'h` | SUGGESTION; Tests | Retained as S4 | Unchanged. It is optional. |
| R280-S2: `SERVED_MVU` is not tied to the ledger | SUGGESTION; Tests, Docs | Retained as S5 | Unchanged. It is optional. |
| R280-O1 = R281-1 S1: the stale "NOTE ON THE DECODE" | out of scope / SUGGESTION | Retained as S3 | Predates this PR and is untouched by it. |
| R280-O2: the dated behave total in `tests/README.md:80,128` | out of scope | Agreed, not a finding | The prose is explicitly dated and defers to the run's own tally. The per-feature row (59) is correct. |
| R280-O3: the 5.4.4.1 NOTE on not replying from a non-compliant configuration | out of scope | Agreed | Owner or processor decision. It is listed in the PR limitations. |

No prior BLOCKER, MAJOR or MINOR remains open. No finding was moved to another Issue in place of a fix.

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #536 AC1-3; #510 decision; Milan v1.2 4.2.4, 5.4.3.2-5.4.3.4, 5.4.4.1-5.4.4.5, Figs 5.2-5.7, Tables 5.18-5.21; IEEE 1722.1-2021 Table 9-1, 9.3.5.3.3, 9.6 (Table 9-6, 9.6.5.3.1), Table 7-140; model, steps and feature MVU text; `receipts/spec_citation_check.txt`, `receipts/rtl_vs_model.txt` | R281-2 | `fb84de54ee9c1e3a2b51d2a239efbc04e4a22bad` |
| RTL | CLEAN | pinned `KL_aecp_engine.sv`, `KL_pp_rx_validator.sv`, `protocol_processor_top.sv`, `tb/pp_top` M1-M9 at `424c688`; gitlinks unchanged base/head/live dev; executed probe: 731 pinned checks + 26/26 rows + 24/26 extras byte-exact (`receipts/rtl_vs_model.txt`, `receipts/probe_copy_integrity.txt`) | R281-2 | `fb84de54ee9c1e3a2b51d2a239efbc04e4a22bad` |
| Robustness | CLEAN | truncated, over-length (cdl 21-564), per-octet and per-nibble protocol_id, r bit, command words, message types 0-14, junk reserved and tail, RX-slot boundary; `receipts/rtl_vs_model.txt`, `receipts/rx_slot_boundary_*.txt` | R281-2 | `fb84de54ee9c1e3a2b51d2a239efbc04e4a22bad` |
| Tests | CLEAN | contract 59/435 and full 343/1736; 21 reviewer arms (21/21 exact), gate arm, prior R280 and R281 scripts rerun unmodified; step and gate code at head | R281-2 | `fb84de54ee9c1e3a2b51d2a239efbc04e4a22bad` |
| Docs | CLEAN | `tests/README.md:90`, `docs/MILAN_V12_ROADMAP.md:539`, compliance matrix 1.3/1.4 and FR_NFR (consistent, untouched), comment/header text in three test files, PR body, `receipts/static_gates.txt` | R281-2 | `fb84de54ee9c1e3a2b51d2a239efbc04e4a22bad` |

Every covering head is the merge candidate's source head itself. A later commit that changes any artifact within a lens's scope un-covers that lens.

## Real limits

- **The RTL evidence comes from a probe, not the full suites.** The probe ran a **copy** of `tb/pp_top`: the pinned phases through MilanInfoPhase, then an early exit. Later pp_top phases, the full processor, parent and gPTP banks, Yosys, the builder, `act` and Docker were not run, as this round's rules require.
- **Each frame was sent on its own, into an idle engine.** That says nothing about MVU under backpressure, concurrent traffic or reset during activity. The offline model does not claim those either.
- **No hardware.** Physical calibration NOT RUN. Field and physical skips (including the hosted `Physical gPTP` context) are not hardware proof.
- **The specification was read from plain-text renderings.** Figure offsets were read from those renderings and cross-checked against the executed RTL answers. The IEEE Table 7-140 rendering shifts the hex letter by one (`B16` is SET_VIDEO_FORMAT 0x000A), and 0x001B was confirmed from the table order.
- **#537's documentation rows were deliberately not reviewed**, to respect the lane split.
- **Clone restoration** (`receipts/clone_restore_verify.txt`, `scripts/verify_clone.sh`), checked after all probes:
  - HEAD and tree are exact.
  - The worktree is clean, including ignored and untracked files.
  - The index equals HEAD, and no skip-worktree or assume-unchanged flag is set.
  - All 872 tracked blobs re-hash to HEAD with their HEAD modes.
  - `protocol-processor` (222 blobs) and `gptp-processor` (103 blobs) are at their pins, re-hash byte for byte and are clean.
  - All four gitlinks are unchanged.
  - Six bytecode-cache directories that this round's runs created in the clone were removed before the check. No source in the clone was edited. Every probe ran in disposable copies under the packet's unpublished `scratch/`.

## Pending manager duties

- Publish this report and the files listed in `MANIFEST.sha256`.
- Own hosted and `act` acceptance at the final head.
- Build and validate the final current-dev candidate at the merge turn: source base `26d855a9`, live dev `615b5a5d`, with `docs/MILAN_V12_ROADMAP.md` touched on both sides.
- Confirm the internal review (R280-2) independently. Merging needs two independent positives, explicit maintainer authorization, and then post-merge containment.
- Optional: open Issues for S2 (the model's RX-slot drop) and S3 (the stale NOTE). S1, S4 and S5 are at the lane's discretion.

## Reproduce (from the packet root; `$REPO` is the head checkout with `protocol-processor` at its pin)

- Probe build: copy the pinned `hdl`, `tb/pp_top` and `tb/common` into `scratch/pp`. Run `python3 scripts/patch_pp_top_probe.py scratch/pp/tb/pp_top/sim_main.cpp`. Apply `receipts/pp_top_makefile.diff`, then run `make run` there with the scoped Verilator 5.050 first on PATH.
- `python3 -B scripts/rtl_vs_model.py --repo "$REPO" --sim scratch/pp/tb/pp_top --out receipts/rtl_vs_model.txt`
- `python3 -B scripts/rx_slot_boundary.py --repo "$REPO" --sim scratch/pp/tb/pp_top --out receipts/rx_slot_boundary_head.txt`. For the base comparison, pass `--repo` a git-archive of `26d855a9`'s `tests/`.
- `python3 -B scripts/mutate_r281_2.py --repo "$REPO" --work scratch/mut`
- `sh scripts/verify_clone.sh "$REPO" fb84de54ee9c1e3a2b51d2a239efbc04e4a22bad 24a2b1c9bd657d2d14b5e814f18ec349108ffc1f`

R281-2 FINISHED
