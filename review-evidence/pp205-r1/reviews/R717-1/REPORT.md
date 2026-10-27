[R717] POSITIVE - exact head 7bad3943c6dc3a86814faa43aee53a1e8aab4a4f

# R717-1: independent review of issue #205 / PR #207

**Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open, and all five lenses are CLEAN. There is one SUGGESTION (R717-1-S1) and no RESIDUE.

- **The fix is correct.** A GET_TX_STATE_COMMAND whose `talker_unique_id` is invalid now gets a TALKER_UNKNOWN_ID response that echoes the command's `listener_entity_id` and `listener_unique_id`. Every other field of that response follows Milan v1.2 Table 5.46. The SUCCESS response keeps Table 5.47's zeros.
- **No other response changed.** PROBE_TX, DISCONNECT_TX and GET_TX_CONNECTION behave as before. There is no change to any port, parameter or register map.
- **Reproduced here.** The talker suite passes 1561 of 1561 at head. On the base talker RTL it fails exactly the four new listener-field checks. The three new mutant arms are KILLED by their named checks.
- **New reviewer evidence.** I added a disposable wire-level probe to `tb/pp_top`. It fails only on the base RTL (RV1, listener bytes 0) and passes at head. I also ran ten reviewer mutant arms. Every one behaved as predicted: eight KILLED, one equivalence control and one informational arm.

## 1. Identity and scope

| Item | Value |
|---|---|
| Exact head | `7bad3943c6dc3a86814faa43aee53a1e8aab4a4f`, tree `317c13456cdceac6cdcda6e7b40992c40e300b5f` (verified in the clone) |
| Source base | processor main `097a7987` |
| Merge-candidate base (manager, not built here) | live dev `97aab1d0f28bd753a3e11df6278d5cac54f964dd` |
| Delta | `097a7987..7bad3943`, 2 commits (`c7250d65` the change, `7bad3943` the talker README re-measure). 6 files: `hdl/acmp/KL_acmp_talker.sv` +26/-8, `tb/acmp_talker/sim_main.cpp` +22/-6, `tb/pp_top/acmp_mutants.py` +35/-3, `tb/acmp_talker/README.md` +40/-8, `docs/architecture/05_acmp_engine.md` +11/-2, `docs/00_MILAN_COMPLIANCE_REVIEW.md` +1/-1 |
| Authorities | Milan v1.2 5.5.4.3 and Tables 5.40, 5.44, 5.46, 5.47. IEEE 1722.1-2021 8.2.5.2.3, 8.2.5.2.5 and Figure 8-4. The issue cites 8.2.4: in 1722.1-2021 that is the listener state machine, whose `txResponse` has the same wording. |
| Scope sources read | the issue body; the assignment comment (issuecomment-6434658917); the PR body; the review-start comment (issuecomment-6436912806); the docs README conventions. The repo has no AGENTS.md or CONTRIBUTING.md. |
| Public evidence | `kebag-logic/milan-fpga@d96469cc…/review-evidence/pp205-r1` (118 files, downloaded as data; receipts and spec extracts inspected) |

## 2. Lens results

### Conformance — CLEAN

Table 5.46, field by field, against the `respond` block at `hdl/acmp/KL_acmp_talker.sv:1580-1639`:

| Field | Table 5.46 | Head |
|---|---|---|
| message_type | GET_TX_STATE_RESPONSE | `txn_r.msg_type \| 1` (:1581) |
| status | TALKER_UNKNOWN_ID | `ST_TALKER_UNKNOWN_C` = 2 (:1635) |
| controller_entity_id | the command's | `txn_r.controller_eid` (:1582) |
| talker_entity_id | the command's | `own_entity_id_i` (:1583). A talker command requires `target_eid == own_entity_id_i` (:789-790), so the two values are equal. |
| listener_entity_id | the command's | `pdu_leid_r` (:1636), fetched from RX-slot bytes 28..35 because `needs_pdu_w` now covers this case (:809) |
| talker_unique_id | the command's | `uid16_w` (:1584) |
| listener_unique_id | the command's | `pdu_luid_r` (:1637), RX-slot bytes 38..39 |
| sequence_id | the command's | `txn_r.sequence_id` (:1585) |
| connection_count, the three flags, stream_id, stream_dest_mac, stream_vlan_id | Undefined | 0 (defaults :1565-1577). Milan wins over IEEE's `response = rcvdCmdResp` (Milan 5.5.2.1). |

- **Table 5.47 (success).** The listener fields are set to 0 explicitly (:1629-1631). connection_count is 0 and the flags carry REGISTERING_FAILED, live (:1625). The stream fields are the current ones (:1626-1628). These are the same values as at base.
- **Wire-level check.** My `tb/pp_top` probe (`receipts/pptop-probe-head.log`) asserts the whole 70-byte response frame:
  - RV1 unknown GET_TX_STATE: listener fields echoed, everything else as above.
  - RV2 success with non-zero listener fields in the command: zeros.
  - RV3/RV4 PROBE_TX and DISCONNECT_TX unknown: echo.
  - RV5 GET_TX_CONNECTION NOT_SUPPORTED: echo.

  All five pass at head. On the base talker RTL only RV1 fails (`receipts/pptop-probe-basertl.log`), so check (3) holds at the wire as well.
- **Spec text.** The clause text in the author's spec extracts (`receipts/spec/*.txt` in the public evidence) agrees with the issue's quotation of 5.5.4.3 and Table 5.46. No spec PDF was available here (see limits).

### RTL — CLEAN

- **The change is small.** It touches one fetch-gate term (`:809`, `(msg_type == MT_GTX_ST_C) && !uid_valid_w`), two listener assignments in each GET_TX_STATE arm (`:1629-1637`) and comments. The PROBE, DISCONNECT and GET_TX_CONNECTION arms and their fetch terms are unchanged (`git diff`, and reviewer arms 7-9 below).
- **No interface change (check 7).** The module header (`module` through `);`, 182 lines) is byte-identical between base and head: sha256 `07504cdc…01bef5` (`receipts/interface-check.txt`). No `parameter`, `localparam`, `input` or `output` line changed. No other file under `hdl/` changed, and neither did 01/02/07 or the guides.
- **The top passes the fields through.** It latches every talker response field unchanged into one 56-byte ACMPDU (`hdl/top/protocol_processor_top.sv:3376-3418`).
- **Lint.** `scripts/lint_hdl.sh` passes, 41 modules LINT OK with no warning (`receipts/lint-hdl-head.log`). The talker `make lint` is clean.
- **Latency.** The fetch adds the 13-clock S_TXN_PDU walk (`fetch_ix_r` 0..12, `:1131-1160`) to the refusal only. A successful GET_TX_STATE still goes S_TXN_REC to S_TXN_ACT, so the success-path figure in 08 is unaffected.

### Robustness — CLEAN

- **No stale echo.** `pdu_leid_r`, `pdu_luid_r` and `pdu_flags_r` are cleared at every dispatch (`:1115-1117`), so a refusal can never echo an earlier command's fields.
  - Reviewer arm `rv_no_clear_on_dispatch` removes that clear and survives with 0 failing checks (informational). No suite pins the clear, but at head the response arms read the registers only after a fetch, so it is not needed for correctness. The clear is pre-existing and outside this delta.
- **Truncated PDUs.** For a short PDU, bytes beyond `slot_len_r` read as 0 (`:1137-1139`), the same rule as the existing C6 case.
- **Out-of-range RX slot.** If `rx_slot` is out of range (`slot_ok_w` false) there is no fetch and the echo is 0, the same as the pre-existing PROBE_TX and DISCONNECT_TX paths.
- **`uid_valid_w` is evaluated twice.** It is read combinationally in S_TXN_REC (fetch decision) and again in S_TXN_ACT (arm select), from the live `cfg_src_en_i`. If a source were disabled between those two cycles, the response would be a TALKER_UNKNOWN_ID with listener fields 0, never stale data. PROBE_TX has the same pre-existing pattern. I did not probe whether the top's hazard scoreboard keeps configuration changes out of that window (see limits). It is not a finding: the result is the base behaviour in a single-cycle window, never garbage.

### Tests — CLEAN

| Run (pinned simulator v5.050, = CI `VERILATOR_VERSION`) | Result | Receipt |
|---|---|---|
| `tb/acmp_talker` at head | rc 0, `1561 checks: 1561 PASS, 0 FAIL` | `talker-head.log` |
| `tb/acmp_talker` at base `097a7987` | rc 0, `1545 checks: 1545 PASS, 0 FAIL` | `talker-base.log` |
| head tests on the base talker RTL | rc 2, `1561 checks: 1557 PASS, 4 FAIL`. The failures are exactly C2 listener_eid/uid and H3 listener_eid/uid, each answered 0: the reported defect, as the PR claims (check 4) | `talker-basertl.log` |
| `acmp_mutants.py --only` the three new arms, `--jobs 3` | rc 0. Golden PASS. `tx_state_unknown_zeroes_listener` KILLED, 4 failing; `tx_state_unknown_not_fetched` KILLED, 4; `tx_state_success_echoes_listener` KILLED, 2 (B2 listener_eid/uid). These match the README and PR tables. | `acmp-mutants-new.log`, `acmp-mutants-new/results.json` |
| static plant check of all ACMP arms at head | 101 arms, 0 refused: the talker edit breaks no existing arm's planted text | `plant-check-head.log` |
| reviewer arms (`scripts/rv_mutants.py`, the head's own `judge`) | rc 0, golden PASS, all ten behaved as predicted (table below) | `rv-mutants.log`, `rv-mutants/results.json` |
| `tb/pp_top` main build plus reviewer probe RV1-RV5, head | rc 0, `[build default …] 10203 checks, 0 failures` (10198 existing + 5 probe) | `pptop-probe-head.log` |
| the same, base talker RTL | rc 2, `10203 checks, 1 failures`, only RV1 | `pptop-probe-basertl.log` |

The reviewer arms:

| Arm | Expectation | Result |
|---|---|---|
| `rv_unknown_uid_zeroed` | KILL | KILLED: C2 and H3 `listener_uid` |
| `rv_unknown_eid_zeroed` | KILL | KILLED: C2 and H3 `listener_eid` |
| `rv_unknown_eid_halves_swapped` | KILL | KILLED: `got b5a69788f1e2d3c4`. The distinct-byte `L_DIST` value pays off here: `L1` = `0x1111222233334444` would also catch this swap, but not a swap within a repeated byte pair. |
| `rv_fetch_inverted` | KILL | KILLED: all four C2/H3 listener checks |
| `rv_unknown_echoes_flags` | KILL | KILLED: C2 and H3 `flags got ffff`. Flags are Undefined in Table 5.46; the suite pins the chosen 0. |
| `rv_success_explicit_zero_removed` | EQUIVALENT | 0 failing checks. As expected, a successful GET_TX_STATE fetches nothing, so the defaults already give 0. |
| `rv_probe_unknown_zeroed` | KILL | KILLED: C1, H2, L1 |
| `rv_disconnect_eid_zeroed` | KILL | KILLED: C4, TD1 |
| `rv_gtx_connection_eid_zeroed` | KILL | KILLED: C5 |
| `rv_no_clear_on_dispatch` | INFO | 0 failing checks (see Robustness) |

- **Test design.** C2 uses an out-of-range source and H3 a disabled one, both through 5.5.4.3 step 1's validity check (`uid_valid_w`, `:787-788`). Each checks all 14 response fields through `expect_resp` (`tb/acmp_talker/sim_main.cpp:389-405`). B2 keeps a success case with non-zero listener fields in the command, so the zeros are graded, not inherited.
- **Parent consumer gate (check 6).** I re-ran the two idiom gates the assignment names in a scratch clone of milan-fpga dev `97aab1d0`, with the `protocol-processor` gitlink set to this head and populated at this head. Both gave rc 0 (`parent-cpp-idiom.log`, `parent-py-idiom.log`): C++ ratchets all `0 <= 0`; Python ratchets at budget. I did not have the #202 wiring patch (`ff5068d2…1275`) locally. The populations differ from the author's receipt by exactly what that patch adds: 348 versus 349 translation units (the patch adds `sim_sid_move.cpp`) and 262,442 versus 262,461 Python lines. The patch touches only parent files, so it does not change what these two gates measure in the processor delta.
- **The rest of the gate.** For the other fifteen consumer commands I inspected the author's published receipts (`receipts/parent/consumer-gate/results.json`: 17 of 17 exit 0; `PARENT-STATE.txt`: gitlink `7bad3943`, patch commit identical to the patch). I did not re-run them (not allowed here).

### Docs — CLEAN

- **No description of the old behaviour is left (check 5).** I grepped the whole tree for GET_TX_STATE and listener-field wording. Every hit at head states the new behaviour:
  - the talker banner (`KL_acmp_talker.sv:24-30`), the fetch-gate comment (`:800-804`), the compose comment (`:1553-1558`) and the arm comments (`:1569`, `:1629`, `:1633-1634`);
  - F05.11's two GET_TX_STATE leaves and the new paragraph (`docs/architecture/05_acmp_engine.md:420-421`, `:431-438`);
  - REQ-ACMP-008 (`docs/00_MILAN_COMPLIANCE_REVIEW.md:405`);
  - the talker README case list and its #205 section (`tb/acmp_talker/README.md:22-28`, `:367-392`);
  - the harness banner (`sim_main.cpp:9-11`).

  The base wording "GET_TX_STATE zeroes the listener fields" is gone from every file.
- **Counts.** `1561` appears only in the README, and matches my run. The re-measured retry counts (`no_command_ready` 782, `no_get_tx_state_response` 144) match the author's retry receipts, where baseline and restored both pass 1561.
- **Comment rule.** I scanned every added line for lane labels, reviewer or round IDs and comment IDs (`receipts/comment-scan.txt`). The only hit is the existing retry-case ID `R16` in a README table row, a test-case ID. The added source comments state behaviour with Milan table numbers, issue #205 and REQ-ACMP-008. The C2/H3 references in harness comments are that suite's own case IDs. No RESIDUE.
- **Doc gates.** `make check` passes in a local clone at head (rc 0: lint, wavedrom, links, matrix, req-tags selftest, aecp commands, ids, figures). `scripts/gen_matrix.py --check` passes (94 rows, 0 untested).
- **Line references.** The PR body's line references (`:809`, `:1569-1572`, `:1629-1631`, `:1632-1637`, `:24-30`, `:800-804`, `:1553-1558`) all match the head.

## 3. Findings

| ID | Severity | Lenses | Where | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R717-1-S1 | SUGGESTION | Tests | `tb/pp_top/sim_main.cpp` section T (`:9065-9196`); the PR body's "Not changed" paragraph | The qualification failure was seen on the wire. `tb/pp_top` has no TALKER_UNKNOWN_ID case for any talker command. My disposable RV1 probe catches the base defect at the top: at base the listener bytes are `00…` where `f1 e2 d3 c4 b5 a6 97 88` / `8c 17` were expected. | None today: the top passes the response through unchanged, and the talker suite plus the mutant arms grade it. A future change in the top's talker-response latch or ACMPDU packer that dropped the listener fields of a refusal would only be caught by the top's existing success-path byte-exact cases. | Optional: add a byte-exact pp_top case for GET_TX_STATE (and optionally PROBE_TX/DISCONNECT_TX) with an unknown `talker_unique_id` and distinct non-zero listener fields, like RV1-RV4 in `scripts/pp_top_probe.py`. | The case passes at head and fails on the base talker RTL. |

No BLOCKER, MAJOR, MINOR or RESIDUE.

## 4. Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_acmp_talker.sv:787-810, 1552-1649`; Milan 5.5.4.3 and Tables 5.40/5.44/5.46/5.47; IEEE 1722.1-2021 8.2.5 extracts; `protocol_processor_top.sv:3376-3418`; pp_top RV1-RV5 at head and base RTL | R717-1 | `7bad3943c6dc3a86814faa43aee53a1e8aab4a4f` |
| RTL | CLEAN | full talker diff; module header hash base/head; `lint_hdl.sh`; talker lint; walker states `:1104-1233` | R717-1 | `7bad3943c6dc3a86814faa43aee53a1e8aab4a4f` |
| Robustness | CLEAN | per-dispatch clear, truncated PDU, slot guard, single-cycle `cfg_src_en_i` window (by inspection); reviewer arms incl. `rv_no_clear_on_dispatch` | R717-1 | `7bad3943c6dc3a86814faa43aee53a1e8aab4a4f` |
| Tests | CLEAN | talker suite head/base/base-RTL; 3 new arms; 101-arm plant check; 10 reviewer arms; pp_top main build plus probe at head and base RTL; parent cpp/py idiom gates; author consumer-gate and retry receipts | R717-1 | `7bad3943c6dc3a86814faa43aee53a1e8aab4a4f` |
| Docs | CLEAN | 05 F05.11 and §6bis paragraph; 00 REQ-ACMP-008; talker README; harness and HDL comments; `acmp_mutants.py` docstring; comment-rule scan; `make check`; `gen_matrix.py --check`; PR body | R717-1 | `7bad3943c6dc3a86814faa43aee53a1e8aab4a4f` |

## 5. Limits (real) and pending manager duties

**Limits:**

- **No full banks.** I did not run any full parent, processor, gPTP, Yosys or builder bank. In particular I did not run:
  - `scripts/run_suites.sh`;
  - the other six `tb/pp_top` builds (I ran the default build only, plus probe);
  - the full 101-arm ACMP campaign (only the three new arms run, plus the static plant check of all 101);
  - `tb/acmp_talker/retry_mutants.py`;
  - `check-req-tags.py` with suite evidence;
  - fifteen of the seventeen parent consumer commands.

  For those, the source-head execution evidence is the author's published receipts, which I inspected but did not reproduce. There is no manager source bank at this head, and none is claimed or inferred.
- **No wiring patch.** I ran the two parent idiom gates without the #202 wiring patch, which was not available to me (population difference explained above).
- **Spec text.** No Milan or IEEE PDF was available here. Clause text comes from the issue, the PR body and the author's published extracts, which agree with each other.
- **Single-cycle window not probed.** I did not test whether the top's hazard scoreboard keeps `cfg_src_en_i` changes out of the S_TXN_REC to S_TXN_ACT window. That analysis is by inspection only.
- **How the probe receipts were recorded.** The two pp_top probe runs were launched detached. They completed normally (08:34:53Z and 08:35:09Z), but their logs had been moved aside while the runs were still writing, so I restored those complete logs as the receipts and re-recorded each rc file from its log's make outcome: rc 0 at head, rc 2 at base RTL, `make: *** … Error 1`. A redundant second launch was stopped and is not a receipt.
- **Disposable copies.** Disposable copies built with a capped Verilator `-j` (`--build -j 2`, 4 or 12 instead of 0) to stay within 16 jobs. That changes build parallelism only.
- **Redacted paths.** In the published receipts, the simulator's install root is redacted to `<pinned-tool>` and the home directory to `<home>`. That is the only post-run edit to any receipt, and `MANIFEST.sha256` hashes the redacted files.
- **No hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof.

**Pending manager duties:**

- **Hosted CI.** At the exact head, `docs-gates` and `portability` show success in runs 40471787565 and 40471782134. Both `suites` jobs were still in progress when last read. Hosted/act acceptance is the manager's.
- **Merge candidate.** The manager builds and validates the current-dev merge candidate (source base `097a7987`, live dev `97aab1d0`) with the builder and native banks at the merge turn, with the #202 wiring patch until the sixth pin adoption lands. The manager also links the receipts.
- **Second review.** The merge still needs the second independent positive review and the full completion bar.

## 6. Prior public review findings on this PR

I read this section only after the verdict and ledger above were written. At the time of reading, PR #207 carries no prior review findings: no PR review, no inline review comment, and only two comments, both manager review-start notices (R717-1 issuecomment-6436912806, R718-1 issuecomment-6437054335). Issue #205 carries the assignment, TAKEN and REVIEW READY comments only. **There is nothing to resolve or retain.** The parallel R718-1 review was in progress and unpublished; I did not read it.

## 7. Clone state after probes

All builds and probes ran in `git archive` copies or local clones under `scratch/`. The review clone was never built in or edited. After the run, `receipts/clone-integrity.txt` shows:

- HEAD is `7bad3943…`, detached, with tree and `write-tree` both `317c1345…`.
- `git status --porcelain --untracked-files=all` prints 0 lines, and the worktree-vs-index and index-vs-HEAD diffs are both empty.
- The index entries (modes, blob ids, paths) hash identically to `git ls-tree -r HEAD`.
- The worktree blob hashes (no filters) equal the index blob ids.

This repository has no gitlinks. In the scratch parent, the `protocol-processor` gitlink was `7bad3943…` with a clean submodule tree (`receipts/parent-state.txt`).

R717-1 FINISHED
