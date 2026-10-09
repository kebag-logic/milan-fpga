[R552] NEGATIVE - exact head 66d1b501f4879402fe76485095aef7c6e07c32af

# R552-2: internal independent review of processor PR #171 (Closes #168), delta 96d3b783..66d1b501

- Subject: Mister-M-alt/protocol-processor-control-plane-avb-milan PR #171, branch `pp168-acmp-fields`.
- Exact head `66d1b501f4879402fe76485095aef7c6e07c32af`, tree `36e735c0d54ceb20f2ca09f4ed07069e575a9717`. Its parent is `96d3b78384f34a630d6056ebd8fa5e30f6836650`, so this round has one commit, with no rebase or amend.
- Source base `ed340b9b85258194247334b85e62cf9c23d4d051`; live dev for the merge candidate `7c1b52bee26b497080ee22b1c1986109f80a5ee7`.
- Review start: PR #171 comment 6086402401. Round assignment: issue #168 comment 6086157264. Author REVIEW READY: 6086365354.
- Role: internal reviewer, cleared context, own detached clone. No repository AGENTS.md or CONTRIBUTING.md exists.

## Verdict summary

The round-3 commit changes only eight Markdown pages and two figures under `docs/`. No `hdl/`, `tb/`, `scripts/`, `syn/`, Makefile or CI file changes. All six prior findings (R552-1 F1 to F4, R553-1 F1 and F2) are **resolved** at this head:

- DISCONNECT_TX validation is consistent across F05.11, the scope table, Δ4, GAP-02, REQ-ACMP-007, the operator guide and figure 24.
- The A5 and A12 legend rows are conditional and match the RTL.
- F07.6 is 16-bit, freshly rendered and bit-exact against `acmp_rec_t`, and the overlay is documented.
- GET_STREAM_INFO selector 6 ownership is stated the same way in 02, 06 and the integrator guide, and the 12-bit top-level port is unchanged.

I checked every new statement against the RTL and drove the claims that matter with disposable probes. All documentation gates pass at both revisions, and each gate's negative control fails as required.

The verdict is NEGATIVE for one new MINOR finding, R552-2-F1. 06 §7, a page this round edits, still describes the STREAM_INPUT notification triggers in terms of the old unconditional status clear that LD2 removed:

- It lists "retry" as a status-compare push. A discovered retry now keeps pbsta/acmpsta, and the PR itself replaced the `RETRY-CLEAR` notification expectation with `RETRY-RETAIN`.
- It says a re-bind from PRB_W_RESP "leaves pbsta/acmpsta at ACTIVE/0". The suite's own LD2 check puts PRB_W_RESP at acmpsta 5.

The assignment's item (1) requires that no claim built on the corrected defects remains, so this is not wording-only. The sentence predates this round and both round-1 reviews missed it.

## Findings

### R552-2-F1 - MINOR - Docs - 06 §7 notification triggers still assume the removed A5/A12 status clear

- **Where:**
  - `docs/architecture/06_aecp_engine.md:1056-1062` (STREAM_INPUT triggers): "the committed pbsta/acmpsta compare ... (bind, unbind, settle, teardown, double probe timeout, retry)" and "a re-bind to another talker from a bound state, which from PRB_W_RESP leaves pbsta/acmpsta at ACTIVE/0 so this is its only push".
  - The same premise appears in two in-code comments: `hdl/top/protocol_processor_top.sv:3551-3553` ("compare (bind, unbind, settle, teardown, double timeout, retry)") and `hdl/acmp/KL_pp_acmp_listener.sv:336-337` ("from PRB_W_RESP the re-bind leaves pbsta/acmpsta at ACTIVE/0, so this pulse is the ONLY notification").
  - All three locations are byte-identical at 96d3b783; the 06 sentence is at lines 1047/1050 there (`receipts/finding-evidence.txt`).
- **Authority and evidence:**
  - Milan 5.5.3.5.30 step 2 and 5.5.3.5.10 (the LD2 correction) keep the status through a discovered retry and the following delay expiry. Milan Table 5.22 notifies GET_STREAM_INFO only on a field change.
  - The RTL keeps acmpsta in A12 on T-ACMP-RETRY (`KL_pp_acmp_listener.sv:1273`) and in A5 on T-ACMP-DELAY (`:1345`). The compare term fires only when the committed `{pbsta, acmpsta}` byte changes (`protocol_processor_top.sv:3488-3491`).
  - The suite's LD2 check asserts `sm == S_PWR && acmpsta == 5` after the retry probe (`tb/acmp_listener/field_cases.hpp:136-138`), so PRB_W_RESP is reachable with a retained non-zero status.
  - This PR replaced `pair("RETRY-CLEAR", ..., true, 5000)`, which waited for the status-clear notification at retry, with `RETRY-RETAIN`. The new check has no notification wait, and the suite README gives the reason: "Table 5.22 does not notify a status value that did not change" (`tb/pp_top/gsi_internal.hpp:424-428`, `tb/pp_top/README.md:2839-2842`).
  - The 05 legend now states the retention rule correctly (05:290, :297, :337-340). 06 §7 contradicts it.
- **Impact:**
  - 06 §7 is the place that enumerates which Milan Table 5.22 pushes the processor raises for a Stream Input. A verifier who builds expectations from it expects an unsolicited GET_STREAM_INFO at every discovered retry. That is the old RETRY-CLEAR behaviour, which LD2 removed and this PR's tests no longer expect.
  - The "only push" rationale for `act_strt_chg_o` is also false once a status is retained. In that case both terms fire on the same X_WB write; the OR still sends one frame, so the hardware is correct and only the description is wrong.
  - This is a claim built on a corrected defect, which the round's acceptance item (1) excludes. It changes a behavioural claim in an architecture document, so it is not RESIDUE.
- **Required outcome:**
  - In 06 §7, state that the pbsta/acmpsta compare pushes only on a committed change. A discovered retry (A12, then the A5 delay expiry) keeps the status and pushes nothing (Milan 5.5.3.5.30 step 2, .10, Table 5.22). A retry with the talker gone (A17) pushes. A repeated double timeout that leaves the status unchanged pushes nothing.
  - Qualify the re-bind sentence: from PRB_W_RESP with no retained status the byte stays ACTIVE/0, so `act_strt_chg_o` is then the only push. With a retained status, both terms fire on the same write and one frame is sent.
  - The two RTL comments carry the same premise. Correct them with the same change, or, because this round forbids `hdl/` edits, have the manager record them for the next change that touches those files.
- **Verification:** read 06 §7 against `KL_pp_acmp_listener.sv:1273/1345`, `protocol_processor_top.sv:3488-3491` and `tb/pp_top/gsi_internal.hpp:424-428`; then `make -j16 check` and `python3 scripts/gen_matrix.py --check` return 0.

### RESIDUE

None.

### Suggestions (do not affect the verdict)

- **R552-2-S1 (Tests; retained from R552-1 S3).** The new 05 §6bis text says DISCONNECT_TX "source validation includes both the index range and whether the source is enabled in the current configuration". The RTL implements that through `uid_valid_w` (`KL_acmp_talker.sv:656-657`, `:1304`), but no check covers the enabled half for DISCONNECT_TX. Probe E5 (index-only validation for DISCONNECT_TX) survives the talker suite: 1376/1376 PASS (`receipts/probes/E5_disconnect_index_only.log`). The bench already toggles `cfg_src_en_i` (`tb/acmp_talker/sim_main.cpp:798`, `:873`, `:967`). Adding a DISCONNECT_TX to a disabled, in-range source in one of those windows would grade the claim.
- **R552-2-S2 (Tests; carried from R552-1 S2, not re-probed).** The SRP service VID slice `lstn_act_settle_vlan_w[11:0]` is still graded only with VLAN values below 0x100. Sources are unchanged since R552-1.

## Prior public review findings at this head

I read these only after my own pass and the probes above were complete.

| Prior item | Status at 66d1b501 | Evidence |
|---|---|---|
| R552-1 F1 / R553-1 F1 (DISCONNECT_TX "always SUCCESS") | **Resolved** | 05:13 scope table, F05.11 (05:403-405) plus the 05:412-416 paragraph, Δ4 (01:139), GAP-02 (00:94-98), REQ-ACMP-007 (00:393) and operator.md:52 all state invalid → TALKER_UNKNOWN_ID, valid → SUCCESS, no state change in either case. Figure 24 (line 116) was corrected and its render inspected. A repository-wide search finds no unconditional-SUCCESS claim for DISCONNECT_TX; the only hit is the historical concept sketch, which is marked superseded. The RTL matches (`KL_acmp_talker.sv:1301-1307`). |
| R552-1 F2 / R553-1 F1 (A5/A12 legend) | **Resolved** | A5 (05:290) keeps acmpsta on T-ACMP-DELAY and A12 (05:297) keeps it on T-ACMP-RETRY; both clear otherwise. This matches `KL_pp_acmp_listener.sv:1273`/`:1345`. The legend note's claim that A12's other callers already have acmpsta 0 is supported by the matrix walk and by probe E2: removing A12's clear entirely leaves the listener suite at 3167/3167 PASS. The statement that a new binding clears it at A5 is enforced: probe E3 fails `F05.3 BIND_NEW x PWT: pbsta/acmpsta got 2/5 want 2/0`. |
| R552-1 F3 / R553-1 F2 (F07.6 layout, overlay) | **Resolved** | F07.6 has a 16-bit `settled vlan_id` and no reserved nibble. `scripts/sinkrec_layout_check.py` maps every lane bit-exactly onto `acmp_rec_t`, including the prose ranges [319:304] and [255:192] and the flag order from bit 11 (`receipts/sinkrec-layout-check.log`, rc 0). The SVG is fresh and the render was inspected. 05 §5 says 16 bits. The overlay paragraph (07:515-526) matches the RTL: A5 capture (`:1340`), the guard (`:531-535`), A13 retry bytes (`:736-738`), A15 replace (`:1298`), and the published/NVM-shadow mask (`:790-797`, consumed at top `:2819`). Probe E1 shows the mask is load-bearing (97 listener failures). Probe E4 shows that A10 erasing the word is unobservable, which matches "A10 need not erase". |
| R552-1 F4 / R553-1 F2 (selector-6 ownership) | **Resolved** | 06 §6.2 (06:335-341), the F06.13 rows and reads paragraph (06:421-433), 02 §4.4 (02:413, :416-424) and integrator.md:547 and :570-581 now agree with the RTL (`protocol_processor_top.sv:3508-3513`, `:3536-3539`, `:1042`, `:2714`): <ul><li>input selector 6 [63:48] is the settled 16-bit VLAN while PROBING_COMPLETED, otherwise zero (also zero for an out-of-range index);</li><li>[47:0] and the `gsi_req_o`/`gsi_wait_i` handshake stay external;</li><li>output selector 6 is unchanged;</li><li>`acmp_bound_vlan_o` stays 12 bits, carrying [11:0], and the SRP request uses [11:0].</li></ul> |
| R552-1 S1 (dead A12 clear) | **Resolved as documented** | The legend note gives the reason the clear stays; probe E2 confirms it is equivalent. |
| R552-1 S2, S3 | **Retained** as R552-2-S2 and R552-2-S1 | No tests changed in this round. |
| R552-1 S4 (OOC timing variance) | Informational, unchanged | Sources are unchanged. |
| RESIDUE in either round-1 review | None existed | — |

## Judgement against the review focus

1. **Normative ACMP behaviour no longer specifies the corrected defects.**
   - DISCONNECT_TX is no longer documented as always SUCCESS anywhere in `docs/` or figure 24.
   - LD1: the UNBIND talker fields appear in no normative table.
   - LD3: A1 and REQ-ACMP-020 name CONTROLLER_NOT_AUTHORIZED.
   - VLAN: 05 §5, F07.6, 02 and 06 give 16 bits.
   - Probe guard: A5, A13 and the F07.6 overlay describe the sent controller.
   - **One claim built on LD2 remains**, in 06 §7 (R552-2-F1). The focus item is therefore not fully met.
2. **Listener legend, A5 and A12.** Resolved; the legend matches the RTL and is supported by probes E2 and E3.
3. **F07.6 layout and private overlay.** Resolved; the layout is bit-exact against the struct, the figure is fresh and inspected, and the overlay description is enforced by probe E1.
4. **Selector-6 ownership, VLAN layout and GSI contract.** Resolved; the widened internal path is documented, and the 12-bit `acmp_bound_vlan_o[N_STREAM_IN_P*12-1:0]` (`protocol_processor_top.sv:692`) is unchanged.
5. **Scope and gates.**
   - `git diff 96d3b783..66d1b501` touches only `docs/` and no `hdl/` file (`receipts/scope-check-*.log`).
   - `make -j16 check` and `gen_matrix.py --check` return 0 at both 96d3b783 and 66d1b501 (`receipts/gates/`).
   - The issue-168 mutation subset gives 18/18 KILLED with three goldens passing at exact-head bytes.

## Executed evidence (this review, exact head unless stated)

| Run | rc | Result | Receipt |
|---|---|---|---|
| `make -j16 check` at head / at 96d3b783 | 0 / 0 | All targets: lint (41 mermaid + 18 WaveDrom), wavedrom-check, links (1186), matrix, modmatrix, params, ids (+ selftest), figures (+ selftest), stale | `receipts/gates/{head,base}.make-check.*` |
| `python3 scripts/gen_matrix.py --check` at head / base | 0 / 0 | 94 rows, 0 untested | `receipts/gates/{head,base}.gen-matrix.*` |
| Gate negative controls N1 (stale F07.6 SVG), N2 (deleted `sec-02-avtp` anchor), N3 (12-bit source, 16-bit SVG) | 2 / 2 / 2 | Each gate fails as required: WAVEDROM STALE; 3 LINK FAILs (05, 07, integrator); WAVEDROM STALE | `receipts/negative/` |
| F07.6 against `acmp_rec_t` | 0 | 21/21 PASS | `receipts/sinkrec-layout-check.log` |
| Issue-168 mutation subset (`tb/pp_top/acmp_mutants.py --only` with the 16 FIELDS names, `--jobs 2`) | 0 | 18/18 KILLED by every named check; goldens acmp_listener, acmp_talker and pp_top `--gsi-internal-only` PASS | `receipts/acmp-fields-campaign/` |
| Doc-claim probes E1 to E5 plus two goldens | 0 | Goldens 3167 and 1376 PASS. E1 FAIL (97), E3 FAIL (1): claims enforced. E2 PASS, E4 PASS: equivalence evidence for the documented rationale. E5 PASS: unexercised claim (S1). | `receipts/probes/` |
| Clone integrity before and after probes | — | Head and tree exact; worktree clean; index equals HEAD; every tracked blob's bytes and mode match; identical index/tree hashes before and after; no gitlinks exist or are expected | `receipts/scope-check-{before,after}-probes.log` |
| Figure renders (scratch only) | — | Figure 24 line 116 and F07.6 render without overlap or truncation | inspected; rasters not published |

Simulator identity: pinned 5.050 (`receipts/verilator-identity.txt`, with the binary's sha256). Its internal build parallelism was capped at 8 by `scripts/verilator-j8.sh`. Unit memory peaked at 4,559,073,280 bytes against the 12,884,901,888-byte cap, with zero out-of-memory events (`receipts/memory-unit.txt`). No jobs from this review are left running.

## Lens evidence

- **Conformance - CLEAN.** The DISCONNECT_TX statements now follow the TD1 ruling (Milan 5.5.4.2 step 1, Tables 5.44/5.45 govern the 5.5.2.7 overview) everywhere, including Δ4 and REQ-ACMP-007. The A5/A12 rule cites 5.5.3.5.10 and 5.5.3.5.30 step 2. The VLAN statements cite 5.3.8.9, Table 5.38 and 5.4.2.10. The out-of-range VID remains a parent-side item, per ruling 6050554601. No conformance or compliance-matrix claim at this head contradicts the corrected RTL. R552-2-F1 is an architecture description of notification triggers, and the hardware behind it is conformant (one frame, change-only); I attribute it to Docs.
- **RTL - CLEAN.** There is no `hdl/` change in this round, so the RTL is byte-identical to 96d3b783, which R552-1 and R553-1 found sound. I re-traced every RTL fact the new documents assert: the A5/A12 conditions, overlay lifetime and mask, selector-6 gating and handshake, the 12-bit projection and DISCONNECT_TX validation. The two stale in-code comments are part of F1 under Docs.
- **Robustness - CLEAN.** The documented masking of the private controller word on the published and NVM-shadow view is load-bearing and enforced (E1). Erasing it at A10 is unobservable, as documented (E4). Selector 6 is index- and PROBING_COMPLETED-gated, so a stale `bound_vlan_r` after A8 cannot be read. The 12-bit public port is unchanged.
- **Tests - CLEAN.** No test changed in this round. At exact-head bytes all 18 issue-168 controls are killed by their named witnesses and the three goldens pass. The probes show which new documentation claims are test-enforced (E1, E3) and which are equivalence rationale (E2, E4). One claim is unexercised (E5 → S1, SUGGESTION).
- **Docs - UNCLEAN (R552-2-F1).** All four R552-1 and both R553-1 documentation findings are resolved, the figures are fresh and inspected, and the gates and negative controls pass. 06 §7 still carries the pre-LD2 notification premise.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #168 table, TD1 ruling and VLAN ruling 6050554601; Δ4 (01 F01.4); GAP-02 and REQ-ACMP-007/015/016/017/020/023 (00); 05 scope table, F05.3 legend, F05.4 note, F05.11, F05.14; 02 §4.4; `KL_acmp_talker.sv` DISCONNECT path; listener A5/A12/A15/A17 | R552-2 | 66d1b501f4879402fe76485095aef7c6e07c32af |
| RTL | CLEAN | Empty `hdl/` diff for 96d3b783..66d1b501; `pp_acmp_pkg.sv` `acmp_rec_t`; listener classify, guard, PDU builder, published view, A5/A6/A8/A10/A12/A13/A14/A15/A17; top binding view, GSI owner read and answer, status compare, NVM capture; talker `uid_valid_w` and responder | R552-2 | 66d1b501f4879402fe76485095aef7c6e07c32af |
| Robustness | CLEAN | Overlay lifetime and mask (E1, E4); selector-6 gating and out-of-range index; 12-bit port projection; no-state-change DISCONNECT path (`disconnect_changes_gate` killed) | R552-2 | 66d1b501f4879402fe76485095aef7c6e07c32af |
| Tests | CLEAN | Issue-168 mutation subset (18/18 killed, 3 goldens); doc-claim probes E1 to E5; `tb/acmp_listener/field_cases.hpp`, `tb/pp_top/gsi_internal.hpp`, `tb/pp_top/README.md` RETRY-RETAIN; gate negative controls N1 to N3 | R552-2 | 66d1b501f4879402fe76485095aef7c6e07c32af |
| Docs | UNCLEAN (R552-2-F1) | Every changed page: 00, 01, 02, 05, 06, 07, integrator.md, operator.md; figure 24 and F07.6 (renders inspected); `docs/README.md` rules; repository-wide searches for the corrected claims; 06 §7; PR body Round 3 section | R552-2 | 66d1b501f4879402fe76485095aef7c6e07c32af |

## Hosted CI at the exact head (observed, not accepted; the manager owns hosted acceptance)

From `receipts/hosted-ci-jobs.txt`, observed 2026-10-09T18:10:39Z; both runs report head_sha 66d1b501:

| Run | docs-gates | portability | suites |
|---|---|---|---|
| pull_request 37969844803 | success; the `make check` step executed | success; the elaborate step executed | **in progress**: lint and suites running; campaign, matrix and nvm_port steps pending |
| push 37969840642 | success; `make check` executed | success | **in progress**, same state |

Neither suites job is counted as passed. Both "Build Verilator" steps are skipped because the cache hit; that is not a skipped check.

## Real limits

- The Milan v1.2 and IEEE 1722.1-2021 texts were not available to this review. Clause judgements rest on:
  - the issue's frozen table and the manager's rulings;
  - the clause citations already accepted by both round-1 reviews (R553-1 read the standards directly);
  - the RTL and its clause tests.
- I re-ran only the issue-168 subset of the ACMP campaign, plus the gates and probes above. The full 33-suite bank, the other campaigns, lint, the off-vendor flow and OOC area were not re-run, because sources are byte-identical to 96d3b783, where R552-1 executed them. The area result (+29 LUT / +14 FF) is carried, not re-measured.
- The public evidence tree `kebag-logic/milan-fpga@1570e003` (`review-evidence/pp168-r1`) was committed before round 3 and contains no round-3 receipts. The author's round-3 gate results are stated in REVIEW READY 6086365354. My own head and base gate runs cover the same commands.
- No manager source bank ran at this exact head, and none is claimed or inferred. Physical calibration was NOT RUN. Field skips, simulation and documentation gates are not hardware proof.
- The sub-case of R552-2-F1 in which a retained status makes both notification terms fire on one write rests on RTL reading (`protocol_processor_top.sv:3488-3491`, `:3554-3556`) and the suite's PRB_W_RESP/acmpsta-5 check. I did not simulate it end to end.

## Pending manager duties

- Route R552-2-F1: a docs correction to 06 §7 on this branch. The two in-code comments go into the same change if `hdl/` comment edits are authorised; otherwise record them for the next change that touches those files.
- Donor bank (9) and parent consumer bank (17) at this head on dev 7c1b52be. Build the current-dev merge candidate (builder and native banks; source base ed340b9b, live dev 7c1b52be) at the merge turn and link its receipts on the PR.
- Hosted CI acceptance: both suites jobs were still in progress at observation.
- Carry the parent-side handling of a stream_vlan_id that is not a valid VID (out of scope by ruling 6050554601), and the optional coverage suggestions S1 and S2.

## Receipts

Paths are relative to this packet; every published file is listed in `MANIFEST.sha256`.

- `scripts/`:
  - `mkclone.sh`, `gates.sh`, `negative-gates.sh`, `launch.sh`, `wait_rc.sh` (campaign driver and poller);
  - `doc_claim_probes.py`, `sinkrec_layout_check.py`, `scope_check.sh`;
  - `verilator-j8.sh`: the pinned-simulator wrapper that caps build parallelism.
- `receipts/gates/`, `receipts/negative/`, `receipts/probes/`, `receipts/acmp-fields-campaign/` (per-arm logs and `results.json`), with per-campaign `*.out`/`*.rc`.
- `receipts/sinkrec-layout-check.*`, `receipts/scope-check-{before,after}-probes.log`, `receipts/finding-evidence.txt`, `receipts/hosted-ci-jobs.txt`, `receipts/verilator-identity.txt`, `receipts/memory-unit.txt`.

R552-2 FINISHED
