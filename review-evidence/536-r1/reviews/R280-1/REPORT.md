[R280] NEGATIVE - exact head 612db13c244335b0fa3467d02ebab1c350b01990

# R280-1: internal cleared-context review of issue #536 / PR #543

- Exact head `612db13c244335b0fa3467d02ebab1c350b01990`, tree `80a23ecd3630d054c0062d62ba138494efc44693`.
- Source base and live `dev` at review time: `26d855a9176d63625e6635a029a0c44e3d57ce9a`. The base is an ancestor of the head; there are 2 commits, both one line with no trailers.
- Changed paths (5):
  - `tests/steps/aecp_engine_model.py`
  - `tests/steps/aecp_engine_steps.py`
  - `tests/features/aecp_response_contract.feature`
  - `tests/README.md`
  - `docs/MILAN_V12_ROADMAP.md`
- No HDL, firmware or gitlink change (`receipts/diff_scope.txt`):
  - `protocol-processor` stays at `424c688fa2205b934a7689a58f2aa766420f2326`.
  - `gptp-processor` stays at `c1b617435824929a790739ea8585c3fe1a328cc0`.
- Verdict: **NEGATIVE**. Three MINOR findings are open (F1, F2, F3). No BLOCKER or MAJOR.

## What the round reconstructed, in order

1. `AGENTS.md`, `CONTRIBUTING.md`, `docs/README.md`.
2. Issue #536: body and acceptance criteria 1-3, the executor assignment, TAKEN and REVIEW READY comments (`receipts/issue536_*.txt`).
3. The #510 owner decision (`receipts/issue510_decision.txt`). PR #543 body and the review-start comment (`receipts/pr543_*.txt`).
4. Specification text (the spec text itself is not republished):
   - Milan v1.2 consolidated PDF (sha256 `6bb902be...ba8`): Sections 4.2.4, 5.4.3.1-5.4.3.4, 5.4.4.1-5.4.4.5, Figures 5.2-5.7, Tables 5.18-5.20.
   - IEEE 1722.1-2021 PDF (sha256 `ad7b8220...b9c`): 9.3.5.3.3 and 9.6.
5. The pinned processor at `424c688`:
   - `hdl/aecp/KL_aecp_engine.sv`
   - `hdl/aecp/ucode/gen_ucode.py`
   - `hdl/packet_engine/KL_pp_rx_validator.sv`
   - `tb/pp_top/sim_main.cpp` M1-M9
6. The diff `26d855a9..612db13c` and its two commits.
7. Public executable evidence:
   - Evidence commit `03f757f98886409f97e7cbb647ff3bbd803a588e`, `review-evidence/536-r1`. All five files hash to the manifest's `published_sha256`.
   - Exact-head hosted check runs (`receipts/hosted_check_runs.txt`).

## Independent results at this head

- **Model vs pinned RTL, executed.**
  - Setup: a disposable copy of the pinned `tb/pp_top` was built with Verilator 5.050 (scoped wrapper, identity checked, build capped at 8 jobs). It ran pp_top's own phases up to and including its MVU phase (M1-M9), then 15 extra MVU cases pp_top does not send.
  - Result: **761 checks, 761 PASS, 0 FAIL** (`receipts/rtl_probe_run.txt`).
  - Each RTL frame was compared with the head model's frame for the same command: **15/15 byte-identical** (`receipts/rtl_vs_model.txt`).
  - The extra cases:
    - MVU `0x0001`, `0x0003` and `0x0004` in the Figure 5.3 shape.
    - The 7-octet (cdl 19) GET_MILAN_INFO.
    - A 16-octet (cdl 28) GET_MILAN_INFO, which is served.
    - A junk reserved field, served with reserved 0.
    - SET_SYSTEM_UNIQUE_ID in its Figure 5.5 form (cdl 28).
    - SET_MEDIA_CLOCK_REFERENCE_INFO in its Figure 5.6 form (cdl 92).
    - GET_MEDIA_CLOCK_REFERENCE_INFO in its Figure 5.7 form.
    - Message types 2, 4, 8, 10, 12 and 14 carrying the whole Milan protocol_id.
- **Model vs pp_top want frames, offline.** 29 cases, 0 mismatches (`receipts/xcheck_pp_top_mvu.txt`).
  - Method: pp_top's `aecp_frame()` is restated with its identities and its `aem_like` rule.
  - Cases: M1, M3, M4, M5, M5b, M6, all seven M8 octet cases and both M8b cases, plus the engine-source cases above.
  - The M1 frame is `...c001 001b c50ac100 0000 0000 00000001 00000000 00000000` (cdl 32, 60 octets).
- **Suites at head** (`receipts/behave_*_head.txt`):
  - The contract feature: 42 scenarios / 299 steps passed.
  - The full behave suite: 14 features / 326 scenarios / 1600 steps passed.
- **Static gates at head**, all exit 0 (`receipts/static_gates.txt`):
  - `docs_check`: 0 findings.
  - `check_em_dash --base 26d855a9`: 0 findings over 2 added lines.
  - `check_feature_status`: 0 findings.
  - `check_py_idiom`: every ratchet held.
  - `git diff --check`: clean.
- **Review mutation arms**, run on a shadow copy of `tests/` against the contract feature (`receipts/mutations_r280.txt`). The control is green before and after.
  - RED:
    - R6: the length guard at 6 octets.
    - R7: served status set to NOT_IMPLEMENTED.
    - R8: the served answer emitted as an echo.
    - R11: command_type not read. It fails rows `0x0001` to `0x0004` and the r = 1 row.
  - R7, R8 and R11 together independently confirm acceptance criterion 2: all five rows have a failing model arm.
  - SURVIVED: R1-R5 (F1) and R10 (F2).
  - R9 (the MVU arm moved ahead of the AEM arms) survives as an **equivalent** mutant. The arms are disjoint on message_type, so it is not a finding.
- **The clause check requested of this round.**
  - 5.4.3.2.2 is cited correctly everywhere it appears.
  - 5.4.4.1 is cited correctly for:
    - Figures 5.3 and 5.4.
    - The reserved field: "set to 0 by the sender and ignored by the receiver".
    - protocol_version value 1.
    - The two Table 5.20 bits.
    - certification_version 0 for an uncertified PAAD-AE.
  - 5.4.4.2-5.4.4.5 (each "a recommendation"), Table 5.18 and Table 5.19 are cited correctly.
  - Two citations are wrong: see F3.
- **Documentation overlap with PR #537: none** (`receipts/pr537_roadmap_patch.txt`).
  - #537 edits `docs/MILAN_V12_ROADMAP.md` lines 467-477 (the RECOMMENDED table).
  - This PR edits line 539 only (Section 6).
  - The compliance matrix and FR/NFR rows are untouched here.

## Findings

### F1 - MINOR - Tests, Robustness

- **Location.** `tests/features/aecp_response_contract.feature:148-172` (the guard outline), against `tests/steps/aecp_engine_model.py:541-554` (`_mvu_command_type`).
- **Title.** No row asserts the new sub-decode's protocol_id head and middle comparisons or its message_type guard.
- **Authority and evidence.**
  - The claims:
    - The feature says the sub-decode "compares every byte that names the command ... the whole 48-bit protocol_id".
    - The model's docstring says "all 48 bits of the Milan protocol_id (5.4.3.2.1)".
    - The engine keys the match on `PP_PROTO_MVU` (message_type 6/7) and compares four terms (`KL_aecp_engine.sv:1290-1296`).
  - What the rows vary: only @27 (`00-1B-C5-0A-C1-01`), the @28 word and the length.
  - What no row does:
    - Change @22..@26 while keeping the rest of the Milan id.
    - Send a non-6 message_type carrying the Milan protocol_id and word `0x0000`.
  - The file's #83 outlines send the foreign tail `AABBCCDD`, which any single tail comparison rejects.
  - Review arms, one substitution each in the model. The contract feature stayed green (42/42) for every one:
    - R1: @22..@23 not compared.
    - R2: only @27 compared.
    - R3: @24..@26 not compared.
    - R4: message_type guard dropped.
    - R5: ADDRESS_ACCESS also decoded as MVU.
  - The pinned RTL rejects all five:
    - pp_top's per-octet M8 frames catch R1 and R3 (`receipts/xcheck_R1.txt`, `receipts/xcheck_R3.txt`).
    - The engine echoes NOT_IMPLEMENTED for message types 2/4/8/10/12/14 carrying the Milan id, which catches R4 (`receipts/xcheck_R4.txt`, `receipts/rtl_vs_model.txt`).
  - Two sources in the tree make the same point:
    - pp_top M8's own banner (`tb/pp_top/sim_main.cpp:2401-2413`) records that this single last-octet row left 40 of the 48 compared bits unguarded on the RTL.
    - The feature's own lines 212-216 make the same argument for message types.
- **Impact.**
  - The model could stop comparing 40 of the 48 protocol_id bits, and the suite would stay green.
  - It could also serve GET_MILAN_INFO to an ADDRESS_ACCESS, AV/C or other message carrying the Milan id, and the suite would stay green.
  - Either way the model contradicts the pinned engine. That is the #536 failure (model and RTL diverging unobserved), reintroduced for the new arm.
  - The feature's stated claim is not enforced.
- **Required outcome.**
  - Add rows expecting the NOT_IMPLEMENTED echo:
    - Rows differing from `00-1B-C5-0A-C1-00` in @22..@23 and in @24..@26, keeping the rest of the Milan id. Per octet, as pp_top M8 does, is the stronger form.
    - Rows carrying the whole Milan protocol_id and word `0x0000` under a message_type other than 6: at least 2 and 4.
  - Alternatively, narrow the claims to what the rows prove. This is not preferred, because the model's docstring claims 48 bits.
- **Verification.**
  - `scripts/r280_mutations.py` arms R1-R5 turn RED at the corrected head, and the control stays green.
  - `scripts/xcheck_pp_top_mvu.py` stays at 0 mismatches.

### F2 - MINOR - Conformance, Tests, Robustness

- **Location.** `tests/features/aecp_response_contract.feature:127-132` (rows `0x0001` and `0x0003`) with `tests/steps/aecp_engine_steps.py:378-381` (`step_send_mvu`, "One Figure 5.3 Milan MVU command").
- **Title.** Two #510 RECOMMENDED rows send a truncated form of the command whose clause they cite, so no row grades an MVU echo longer than eight octets.
- **Authority and evidence.**
  - Milan v1.2 command formats:
    - Figure 5.3 is "GET_MILAN_INFO command and GET_SYSTEM_UNIQUE_ID command format".
    - SET_SYSTEM_UNIQUE_ID (5.4.4.2) is Figure 5.5. It adds the 64-bit `system_unique_id` at @32: 16 payload octets, cdl 28.
    - SET_MEDIA_CLOCK_REFERENCE_INFO (5.4.4.4) is Figure 5.6: 80 payload octets, cdl 92.
      - `clock_domain_index` at @30.
      - flags, reserved, default_mcr_prio and user_mcr_prio at @32..@35.
      - reserved at @36..@39.
      - the 64-octet `media_clock_domain_name` at @40..@103.
    - Rows `0x0002` (Figure 5.3) and `0x0004` (Figure 5.7: 8 octets, `clock_domain_index` at @30) are correctly shaped.
  - The mismatch:
    - The rows labelled 5.4.4.2 and 5.4.4.4 send the 8-octet Figure 5.3 frame and assert cdl 20.
    - The outline comment (lines 103-106) says each is echoed "at the command's own length".
  - What the RTL does: it echoes the real Figure 5.5 form at cdl 28 and the real Figure 5.6 form at cdl 92, NOT_IMPLEMENTED. The head model agrees byte for byte (`receipts/rtl_vs_model.txt`).
  - Review arm R10 makes the model walk and echo an MVU command only to the Figure 5.3 8 octets:
    - It survives the contract feature, 42/42 (`receipts/mutations_r280.txt`).
    - It disagrees with the RTL on exactly the two real SET frames (`receipts/rtl_vs_model_R10.txt`).
- **Impact.**
  - Two of the four RECOMMENDED rows exercise commands that are malformed under their own clause.
  - The table records cdl 20 for commands whose conformant exchange is cdl 28 and cdl 92.
  - No row grades the echo length of an MVU command longer than 8 octets, including both real SET forms. A model that truncated it would pass while contradicting the engine.
- **Required outcome.** One of:
  - Rows `0x0001` and `0x0003` send their own Figure 5.5 / 5.6 forms and assert the NOT_IMPLEMENTED echo at that length (cdl 28, cdl 92). A Figure 5.3-shaped command_type sweep may stay as a separate, honestly labelled partition row.
  - The rows and the step docstring say plainly that only the command_type is carried, in a Figure 5.3-shaped frame. A separate row then grades an MVU echo longer than 8 octets.
- **Verification.**
  - R10 turns RED at the corrected head.
  - The RTL probe cases `set_suid_fig5.5_cdl28` and `set_mcri_fig5.6_cdl92` still equal the model.

### F3 - MINOR - Conformance, Docs

- **Location.**
  - `tests/features/aecp_response_contract.feature:105-106`.
  - `tests/steps/aecp_engine_model.py:81-83`.
  - The same IEEE citation appears in the PR body's "Authoritative references".
- **Title.** Two clause citations in the new MVU text are wrong.
- **(a) The IEEE clause cited for the MVU echo.** The MVU block cites "IEEE 9.3.5.3.3" for the NOT_IMPLEMENTED echo of MVU `0x0001`-`0x0004`.
  - IEEE 1722.1-2021 9.3.5.3.3 is processCommand of the **AEM** Entity state machine: "used to handle the receipt, processing and respond to an AEM Command other than ACQUIRE_ENTITY and LOCK_ENTITY". Its "correctly sized response" sentence is scoped to AEM.
  - VENDOR_UNIQUE commands are governed by 9.6:
    - 9.6.5.3.1 asks only for "an appropriate status code".
    - Table 9-6 gives status 1.
  - Milan v1.2 5.4.3.3 Table 5.19 gives NOT_IMPLEMENTED no size rule either.
  - The pinned engine's own MVU banner cites "Milan Table 5.19 = IEEE Table 9-6", not 9.3.5.3.3 (`KL_aecp_engine.sv:166-171`).
  - The command-length echo for MVU is the engine's design choice. Read literally, 9.3.5.3.3's "correctly sized" would point to the Figure 5.5 response form for GET_SYSTEM_UNIQUE_ID, not to the echo.
- **(b) The section cited for the protocol_version quote.** The model quotes "A PAAD shall set the value of the protocol_version field in the GET_MILAN_INFO response to 1" under a heading citing 5.4.4.1.
  - That sentence is Milan v1.2 **Section 4.2.4**, verbatim.
  - 5.4.4.1 words it: "The protocol_version field shall be set to the Milan protocol version supported by the PAAD-AE. The value of this field is 1."
  - The pinned `gen_ucode.py` cites "§4.2.4 and §5.4.4.1", and pp_top M2 cites §4.2.4.
- **Impact.**
  - Committed conformance text sends a reader to a clause that does not govern the behaviour (a).
  - It gives the wrong section for a quoted SHALL (b).
  - `CONTRIBUTING.md` section 6 requires compliance references to cite the specification clause.
- **Required outcome.**
  - (a) Cite Milan v1.2 Table 5.19 and IEEE 1722.1-2021 9.6 / Table 9-6 for the MVU NOT_IMPLEMENTED status, and state that the command-length echo is the engine's choice. Or remove 9.3.5.3.3 from the MVU text.
  - (b) Attribute the quote to Section 4.2.4, optionally beside 5.4.4.1's own wording.
- **Verification.**
  - Re-read against the Milan v1.2 and IEEE 1722.1-2021 text at the corrected head.
  - `docs_check` and `check_em_dash` stay at 0 findings.

### Suggestions (optional, no effect on coverage)

- **S1 - SUGGESTION - Tests - `tests/steps/aecp_engine_steps.py:864-866`.**
  - The MVU RTL gate parses only `localparam logic [15:0] MVU_(GET|SET)_*_C = 16'hXXXX;`.
  - Suppose a later pin declares a served command at the 15-bit command_type width Milan 5.4.3.2 gives it (`[14:0]`), or with a `16'd` literal. The gate would not parse it, and would stay green while GET_MILAN_INFO still parses.
  - Suggest failing closed on any `MVU_(GET|SET)_` localparam the pattern cannot parse.
- **S2 - SUGGESTION - Tests, Docs.**
  - `SERVED_MVU` is not gated against the ledger's `served_mvu_operations`. Both are `["GET_MILAN_INFO"]` today.
  - This is the author's recorded limitation. A follow-up could tie them in `scripts/check_feature_status.py`.

## Clean-lens result

```text
[R280] PASS RTL - protocol-processor gitlink 424c688 (unchanged base..head, receipts/diff_scope.txt); hdl/aecp/KL_aecp_engine.sv:697-719 (MVU_PID_*_C, MVU_GET_MILAN_INFO_C, MVU_CMD_PLD_C, UPC_MVUINFO_C), :1133-1160 (aem_w pop decode; every A_PLD-exit flag is AEM-guarded), :1284-1296 (mvu_get_milan_info_w), :1307-1312 (pld_cap/pld_trim), :2815-2826 (A_PLD-exit re-dispatch), :3181-3200 (walk captures, pid_lo_r), :2100-2127 (@22 header echo, no u-bit mask on VU); hdl/aecp/ucode/gen_ucode.py:98-118, :683-718 (E_MVUINFO); hdl/packet_engine/KL_pp_rx_validator.sv:545-550 (6/7 -> PP_PROTO_MVU) - the model's sub-decode terms, guard order, 8-octet boundary, 16-bit r+command_type word, echo length and 20-octet restated body agree with the pinned RTL; executed: pinned pp_top through M1-M9 plus 15 review cases 761/761 PASS, model == RTL frame 15/15, model == pp_top want frame 29/29. No HDL, processor or gitlink change in the diff.
```

## Per-lens coverage, this round

- **Conformance**: applied; UNCLEAN by F2 and F3.
  - AC1 is met: 0x0000 is served with the Figure 5.4 body, and 0x0001-0x0004 are answered as the engine does (`receipts/rtl_vs_model.txt`, `receipts/xcheck_pp_top_mvu.txt`).
  - AC2 is met: every row has a failing model arm (R7/R8 for 0x0000, R11 for 0x0001-0x0004).
  - AC3 is met: behave and the docs gates are green.
  - Clause interpretation was checked against the Milan v1.2 and IEEE 1722.1-2021 text.
- **RTL**: applied; CLEAN. See the PASS line above.
- **Robustness**: applied; UNCLEAN by F1 and F2.
  - Examined: truncated input (the cdl 19 row, M6), the 7/8-octet length boundary, an over-long GET_MILAN_INFO (cdl 28, served), r = 1, a junk reserved field, message-type confusion, and the maximum-length MVU echo.
  - Examined with no finding: an unloaded image (E_MVUINFO reads no store in either the engine or the model), and responses as input and other-entity drops (pre-existing arms).
- **Tests**: applied; UNCLEAN by F1 and F2.
  - Read the author's 21-arm mutation log.
  - Ran 11 independent review arms.
  - Inspected the RTL gate (S1).
  - Regressions are green at 326 scenarios.
- **Docs**: applied; UNCLEAN by F3.
  - `tests/README.md:90` (count 42 verified) and `docs/MILAN_V12_ROADMAP.md:539` are accurate.
  - There is no #537 overlap.
  - The model, steps and feature headers were read against the clauses.
  - The static docs gates are green.

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2, F3 open) | issue #536 AC1-3; #510 decision; Milan v1.2 4.2.4, 5.4.3.2-5.4.3.3, 5.4.4.1-5.4.4.5, Figs 5.2-5.7, Tables 5.18-5.20; IEEE 1722.1-2021 9.3.5.3.3, 9.6; `aecp_engine_model.py`, `aecp_engine_steps.py`, contract feature at head; `receipts/rtl_vs_model.txt`, `receipts/xcheck_pp_top_mvu.txt` | R280-1 | `612db13c244335b0fa3467d02ebab1c350b01990` |
| RTL | CLEAN | pinned `KL_aecp_engine.sv`, `gen_ucode.py`, `KL_pp_rx_validator.sv`, `tb/pp_top/sim_main.cpp` M1-M9 at `424c688`; gitlinks unchanged; executed probe `receipts/rtl_probe_run.txt` (761/761) | R280-1 | `612db13c244335b0fa3467d02ebab1c350b01990` |
| Robustness | UNCLEAN (F1, F2 open) | guard outline rows; review cases cdl 19/20/28, r = 1, reserved junk, message types 2-14, Figure 5.5/5.6 lengths; `receipts/mutations_r280.txt` R1-R5, R10 | R280-1 | `612db13c244335b0fa3467d02ebab1c350b01990` |
| Tests | UNCLEAN (F1, F2 open) | contract feature (42), full behave (326), author `mutations.log`/`mutations.py` (published evidence), review arms R1-R11, `step_mvu_inventory_matches_rtl` | R280-1 | `612db13c244335b0fa3467d02ebab1c350b01990` |
| Docs | UNCLEAN (F3 open) | `tests/README.md:90`, `docs/MILAN_V12_ROADMAP.md:539`, new header/comment text in the three test files, PR #537 roadmap hunks, `receipts/static_gates.txt` | R280-1 | `612db13c244335b0fa3467d02ebab1c350b01990` |

## Prior public review findings on this PR

- None existed at round start. The only PR comment was the review-start notice, and there were no PR reviews or inline review comments.
- Nothing is carried forward.

## Out-of-scope observations (present at base `26d855a9`, not counted against this head)

- **O1.** `aecp_response_contract.feature:32-36` ("NOTE ON THE DECODE") still says the dispatch arms read @22..@23 "without consulting the protocol".
  - This has been stale since #83. The model's `aem` guard (`aecp_engine_model.py:370`) and the same feature's lines 183-186 say otherwise.
  - Candidate for a new Issue.
- **O2.** `tests/README.md:80` and `:128` carry a dated total of 312 scenarios. It was 316 at base and is 326 at this head.
- **O3.** Milan v1.2 5.4.4.1's NOTE recommends that a PAAD-AE whose active Configuration is not compliant not reply to GET_MILAN_INFO.
  - The pinned engine always replies, and `docs/README.md` states the implementation is not fully Milan-compliant.
  - This is an owner/processor decision, and the PR already lists it as a limitation. It is not this PR's change.

## Real limits of this round

- The RTL probe ran a **copy** of `tb/pp_top` with a spliced probe and an early return.
  - It is not the processor's full pp_top run and does not replace the processor's own suites.
  - Phases after the MVU phase were not run.
- No full parent, processor, gPTP, Yosys or builder bank was run.
- No `act`, no Docker, no hardware. Physical calibration NOT RUN; field skips are not hardware proof.
- Hosted runs were inspected read-only (`receipts/hosted_check_runs.txt`).
  - Every required context at the exact head concluded success.
  - `Physical gPTP (nightly and manual)` is **skipped**, not executed.
- The spec PDFs are local reference copies identified by sha256. Their text is quoted only where a finding needs it.
- The clone was verified after all probes (`receipts/clone_restore_verify.txt`):
  - HEAD and tree are exact.
  - The worktree is clean, including ignored files.
  - The index is identical to HEAD.
  - No skip-worktree or assume-unchanged flag is set.
  - Every tracked blob re-hashes to its index id with the expected mode, in the superproject and in 222 processor files.
  - The gitlinks are unchanged.
  - The byte-cache directories created by this round's test runs were removed.

## Pending manager duties

- Publish this report and the files listed in `MANIFEST.sha256`.
- Route F1-F3 to the executor. Re-review is needed at the corrected head, and each lens un-covered by a changed artifact must be covered again.
- The external review is still outstanding.
- Hosted and `act` acceptance for the final head.
- Candidate merge validation against live `dev` at the merge turn.
- Post-merge containment.
- The merge needs explicit maintainer authorization.

## Reproduce

Each command runs from the packet root. `$REPO` is the reviewed head's checkout, with `protocol-processor` initialized at its pin.

- `python3 -B scripts/xcheck_pp_top_mvu.py "$REPO"`
- `sh scripts/build_rtl_probe.sh "$REPO" scratch <verilator-5.050>`, then `python3 -B scripts/r280_rtl_vs_model.py "$REPO" receipts/rtl_probe_run.txt`
- `PYTHONDONTWRITEBYTECODE=1 python3 -B scripts/r280_mutations.py "$REPO" scratch`

R280-1 FINISHED
