[R483] NEGATIVE - exact head 6f76d612a3191b77ac8a1fe2b9c66da42aeb405a

# R483-1: external review of PR #659 (Refs #653, bench lane B11)

- **Head:** `6f76d612a3191b77ac8a1fe2b9c66da42aeb405a`, tree `0023180fd4bde56446cb6a50b5344d4ecc3b1cd4`, one commit on dev `6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5`.
- **Diff:** `docs/findings/653_DISCONNECT_ORDER_BENCH.md` (new, 356 lines) and one row in `docs/findings/README.md`. No other file.
- **Public evidence judged:** the packet at `980c578474ce63614e214152d87de058079c0033:review-evidence/653-b11-r1`, the #653 issue body and comments, and the PR body.
- **Role:** cleared-context external reviewer. No author contact, and no GitHub write.

## Verdict

**NEGATIVE.** Two MINOR findings are open, under Conformance, Tests and Docs.

The bench result itself holds on independent recomputation. In all 23 disconnects the UNBIND_RX response leaves first, and every figure in the per-cycle table matches the evidence.

The two findings are about how the page reports two parts of that evidence:
- **F1:** one interval in the control section names the wrong event.
- **F2:** the controller-library result is offered without a receipt. It is also offered without stating that the library's only counter check can never fire on the order defect #653 reports.

There are also two RESIDUE items (wording only) and two SUGGESTIONs.

## Findings

### F1: MINOR | Tests, Docs | `docs/findings/653_DISCONNECT_ORDER_BENCH.md:237-238` | The control's 1,629.8 µs is measured to the UNBIND_RX command, not to the response

- **Authority/evidence:**
  - The page says: "The response came 1,629.8 µs after the probe's own GET_COUNTERS answer." In that paragraph "the response" is the UNBIND_RX response.
  - The figure is the grader's `own_rsp_to_cmd_us`, computed as `cmd["tns"] - own["tns"]` (`tools/o653_grade.py:132`). That is the interval to the UNBIND_RX **command**.
  - An independent recomputation from the provided decoder's C0 output gives 1,629.8 µs from the probe's GET_COUNTERS answer to the UNBIND_RX command, and **1,637.3 µs** to the UNBIND_RX response (`receipts/control_c0_interval.txt`).
- **Impact:** The control section is the evidence for #653 acceptance 2, and it misstates a measured interval. The order verdict is unaffected.
- **Required outcome:** The sentence pairs each figure with the event it was measured to. For example: "The UNBIND_RX command left 1,629.8 µs after the probe's own GET_COUNTERS answer, and its response 1,637.3 µs after it."
- **Verification:** Re-read the corrected line against `own_rsp_to_cmd_us` in `summary/o653-grade.json` and against `receipts/control_c0_interval.txt`.

### F2: MINOR | Conformance, Tests, Docs | `docs/findings/653_DISCONNECT_ORDER_BENCH.md:44`, `:224-226`, `:252-254` | The library's counter check is cited without a receipt, and it cannot detect the reported defect

- **Authority/evidence:**
  - Lines 224-226 state that the library "carries a compatibility check worded 'Invalid MEDIA_LOCKED / MEDIA_UNLOCKED counters value on STREAM_INPUT', cited to Milan 1.3 clause 5.3.8.10. It raised no event in any cycle."
  - No file in the published packet contains that string or any receipt for it. A search of all 207 files found nothing.
  - I checked the open-source library at the tag the build receipts name (`v4.3.1.1`, `receipts/library_stream_input_counter_check.txt`). The string and clause are real, at `src/controller/avdeccControllerImpl.cpp:1613`.
  - The check's condition (`:1611`) is `lockedValue != unlockedValue && lockedValue != unlockedValue + 1`. It is the library's only STREAM_INPUT counter-value check, and it ignores connection state.
  - So the check accepts 1/0 and 1/1 whether the input is bound or not. It **cannot** fire on either wire order of the UNBIND_RX response and the unlock push. It also cannot fire on the CRF input's 1/0 NotConnected window.
  - The page's "It flagged nothing then" (`:254`) and acceptance 4's "Held for the library" (`:44`) are therefore true by construction for any order the DUT could produce. The page does not say so. Placed after the CRF 1/0 discussion, the citation (`:224-226`) implies the check was a live test of that window.
  - Under AGENTS.md section 6, the Tests lens asks that each test can fail for the defect it claims to detect.
- **Impact:**
  - A reader, or the owner, can take "the library flagged nothing" as evidence that a controller tolerates the order or the 1/0 window. The library's code cannot tell either way.
  - The same code shows the owner's flag cannot have come from this library's counter check. That is the useful conclusion for #653's open question, and the page leaves it unstated. Its Limits entry only says Hive "may apply counter checks of its own".
- **Required outcome:**
  - The page cites a receipt for the library check, for example the upstream file and line at `v4.3.1.1`, or the bench source tree's copy.
  - The page states the check's condition: it accepts LOCKED = UNLOCKED or UNLOCKED + 1, in any connection state. It also states that the condition can flag neither the reported order nor the CRF 1/0 window.
  - Acceptance row 4 and the CRF section carry that qualification. So the "held for the library" result reads as "no miscount flagged", not as evidence about the order.
- **Verification:** Re-read the revised page against the cited source lines and against `receipts/library_stream_input_counter_check.txt`.

### R1: RESIDUE | Docs | `docs/findings/653_DISCONNECT_ORDER_BENCH.md:62` | The identity table says the descriptor bytes are equal; the scripted gate reports three live-state differences

- **Evidence:**
  - `identity/identity-verdict.txt` prints `IDENTITY GATE: FAIL` on three checks:
    - `aecp-STREAM_INPUT 0`, differing offset 78 (current_format);
    - `aecp-CLOCK_DOMAIN 0`, differing offset 71 (clock_source_index);
    - `get-clock-source` (1).
  - These are exactly the three live-state values the page discloses at `:65-67`. Every CRC, the version and the ATDECC entity facts pass, so the image identity is established. The defect is wording only.
- **Exact fix:** `:62` reads "Equal to the build's AEM image, except the three live-state fields below; the scripted gate reports FAIL on exactly those three".

### R2: RESIDUE | Docs | PR #659 body | The PR body does not follow the PR template

- **Evidence:** CONTRIBUTING.md:405 and `.github/PULL_REQUEST_TEMPLATE.md` require these sections: Status, Linked Issue / roles (executor and both reviewers), Authoritative references, How to get into the same state, How to validate, Known limitations, and Definition of Done. The body has its own sections instead: What this adds, Result, Method, Validation, Limits.
- **Exact fix:** Restructure the body into the template sections, and keep the current content under them:
  - `Refs #653` and the roles go under Linked Issue / roles.
  - The gate table goes under How to validate, with its commands.
  - The Limits go under Known limitations.

### S1: SUGGESTION | Tests | `docs/findings/653_DISCONNECT_ORDER_BENCH.md:240-243`; `tools/o653_grade.py:105-111`

The bench control exercises only the comparison step, against a solicited GET_COUNTERS answer. It does not exercise the unlock-push selection.

I fed synthetic captures in the tap record format through the published grader, unchanged (`receipts/grader_fault_probe.txt`):
- With the unlock push placed between the command and the response, the full check reads COUNTERS_FIRST.
- With the unlock pushed before the command, it reads NO_UNLOCK_PUSH, not a pass.
- A push for another input index is ignored.
- A low-word wrap still gives 7.5 µs.

A sentence citing such an offline control, or a committed copy of it, would show the full check can fail. No change is required.

### S2: SUGGESTION | Tests | `tools/o653_grade.py:140`

The decoder-based order takes the first `UNBIND_RX_RESP` line without filtering by input. A capture holding a second unbind, for another input, would read RESPONSE_FIRST wrongly (fault probe case `unbind_other_input_first`).

Every real capture holds exactly one UNBIND_RX command and one response (`receipts/decode_structure.txt`), so the page's "the two agree on all 23" stands. Worth a note if the grader is reused.

## What was checked and held (artifact-specific)

**Per-cycle table:** `scripts/recompute.py`, `receipts/recompute.txt`, rc 0.
- All 23 rows match the grade JSON field by field: input, lock ms, hold, both intervals, order, pushed triple, frames after the command, library state, flags, pair after, and the short hash.
- The intervals were recomputed independently from the provided decoder's text. Its time column is the 64-bit LE read of the tap's two words, swapped; the low (ns) word is recovered as dX / 2^32. They agree with the grader within 0.06 µs.
- Command to response is 7.496 to 7.512 µs in all 23.
- Response to the unlock push is 114.232 to 116.840 µs on AAF, and 99,346.2 and 99,731.4 µs on CRF.
- The wire shape is response, then unsolicited GET_STREAM_INFO, then GET_COUNTERS. R01 also has a GET_AVB_INFO.
- Ports: the command goes switch to DUT, the response DUT to switch.

**Talker streaming at the unbind:**
- 303 to 1,562 AAF frames reached the DUT after the command.
- The last AAF frame came 37.8 to 195.2 ms after the command; the last CRF frame 35.7 and 63.3 ms after.
- The unlock push follows the response by about 115 µs, so the AAF unlock came from the bind fall and not from silence.
- Tap time is monotonic in file order in all 23 captures (grader flag).

**Library reports:** `runs/s0*/s1-probe.jsonl`.
- Sessions s0, s0b and s1 recorded no `compat_changed`, `diagnostics`, `query_error`, `unsol_loss`, `aecp_timeout`, `aecp_unexpected`, `transport_error` or `offline` event.
- Both entities were IEEE17221|Milan, Milan 0x01020000, and subscribed.
- The session-end event lists are empty, and deregistration returned SUCCESS from an entity whose ID equals the session's.
- The input went NotConnected before the unlock update in every cycle: 51 to 113 µs before it on AAF, 0.9 to 5.2 ms after the unbind.
- The CRF 1/0 hold lasted 95.0 and 100.0 ms.
- The library version label `4.3.1-beta1` matches the upstream `CMakeLists.txt` for `4.3.1.1`.
- The JSON-feature omission gates only free functions (`include/la/avdecc/internals/jsonSerialization.hpp:149-155`), so the probe and the library agree on class layout.

**Control capture:** the probe's GET_COUNTERS command and answer (ML 1, MU 0) precede the UNBIND_RX in the capture; `order_vs_own` reads COUNTERS_FIRST. The one figure defect is F1.

**Decoder defects:** confirmed from `tap_order_decode.py:11` and `:21-22`.
- The time column is a single LE64 read of the tap's two 32-bit words.
- The ACMP "listener" column reads the talker ID (`a[20:28]`), "luid" reads bytes 2-3 of the listener ID (`a[30:32]`), and "cc" reads into the destination MAC (`a[44:46]`).
- The grader uses the IEEE 1722.1 offsets (`a[28:36]`, `a[38:40]`, `a[46:48]`; AEM counters at `a[32:]`).

**Probe build hashes:** `scripts/check_hashes.py`, `receipts/check_hashes.txt`, rc 0.
- All 23 capture names, byte counts and SHA-256 values match `RAW-ARTIFACTS.json`, and the 23 short hashes match their full hashes.
- The s1 probe source, driver, grader and decoder hash equal to the packet files.
- The s0b source and binary, the s1 binary and the copied header equal `runs/build/build-2.txt` and `build-3.txt`.

**Identity, restore and residuals:**
- The CRCs `5ba355eb`, `2144df1c`, `e6b8febc` equal the build's, VERSION is `0x00020060`, the entity facts pass, and the UART grader reads 10/10.
- The census is 45 of 46. The 46th is DUT GET_AVB_INFO propagation delay `0x17d` to `0x183` (381 to 387 ns).
- NVM went from image seq 51 / 20 commits to 98 / 67 commits. 66 commits were reached after the 23 binds and 23 unbinds, and the clock-source SET 0 then SET 1 added one more.
- CLOCK_DOMAIN 0 counters went from 3/3 to 6/6, and STREAM_INPUT 0 and 1 stayed at 1/1.
- The servo trim went from `0xffa40035` to `0x00000020` after the release.
- The controller staging was removed and no probe process remained. The SoC bridge PIDs are equal at start and end.

**RTL claims:**
- At `bbf704ec`, the only MEDIA_UNLOCKED increment in `hdl/ieee1722/crf/KL_crf_rx.sv` outside reset is the 100 ms timeout (`:530-537`). The file and `KL_avtp_rx_monitor_ctx.sv` are unchanged from `bbf704ec` to the head.
- PR #655 is OPEN (not merged), so "the image predates PR #655" holds.

**Docs gates at head** (`receipts/docs_gates.txt`), all rc 0:
- `docs_check.py`
- `check_doc_style.py`
- `gen_toc.py --check` and `--verify-anchors`
- `check_em_dash.py --base 6c22d3ca`
- `check_doc_paths.py`
- `check_feature_status.py --self-test`
- `check_baremetal_only.py --check` and `--selftest`
- `ci_scope.py --selftest`
- `git diff --check`

The Markdown gates ran in a scratch venv built from the pinned lock. `check_baremetal_only.py` returned rc 2 in that venv only because pyyaml was missing there, and rc 0 under the system interpreter.

**Privacy:** `receipts/privacy_scan.txt`.
- No path, address, MAC, interface or host shape appears in the added lines or the PR body; the only matches are version and clause numbers.
- The reference peer, instruments and hosts are named by role, and the probe's staging directory is not named.
- The library and the Hive application are already named across living docs, for example `docs/findings/117_GPTP_SILICON_EVIDENCE.md`.

**Commit:** one line, no trailers (`git cat-file -p HEAD`).

## Reviewer-owned lens ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2) | #653 acceptance 1-4 against page `:39-44`; per-cycle table `:161-185` against `summary/o653-grade.json` and the decoder texts; ACMP/AECP offsets in `tools/o653_grade.py:65-83` against IEEE 1722.1; library check at upstream `avdeccControllerImpl.cpp:1605-1615` | R483-1 | `6f76d612a3191b77ac8a1fe2b9c66da42aeb405a` |
| RTL | CLEAN | No HDL in the diff (`git diff --name-only`); page RTL claims against `hdl/ieee1722/crf/KL_crf_rx.sv:530-537`, unchanged from `bbf704ec` to head; PR #655 state OPEN | R483-1 | `6f76d612a3191b77ac8a1fe2b9c66da42aeb405a` |
| Robustness | CLEAN | `receipts/grader_fault_probe.txt` (reversal, push before command, other index, low-word wrap); `receipts/decode_structure.txt` (one unbind per capture, single controller); s0 failure handling (`runs/s0/s0-probe.jsonl`: FORMAT_READ_FAILED, nothing bound); HOLDOVER release `restore/clock-release.jsonl`, `servo-*-release.txt`; residuals `restore/dut-*.txt`, `counters-*.jsonl`, `census-compare.txt` | R483-1 | `6f76d612a3191b77ac8a1fe2b9c66da42aeb405a` |
| Tests | UNCLEAN (F1, F2) | Control C0 (`summary/o653-grade.json` `s0b/C0.control`, decoder C0 text, `receipts/control_c0_interval.txt`); grader `tools/o653_grade.py` and its fault probe; library sensitivity (`receipts/library_stream_input_counter_check.txt`) | R483-1 | `6f76d612a3191b77ac8a1fe2b9c66da42aeb405a` |
| Docs | UNCLEAN (F1, F2) | `docs/findings/653_DISCONNECT_ORDER_BENCH.md` (all sections), `docs/findings/README.md:16`; `receipts/docs_gates.txt`; `receipts/privacy_scan.txt`; `receipts/check_hashes.txt`; PR body | R483-1 | `6f76d612a3191b77ac8a1fe2b9c66da42aeb405a` |

## Prior public review findings on this PR

There are none to resolve or retain.

I read PR #659's public state after this verdict and ledger were written:
- 2 issue comments, both from the manager: the R482-1 and R483-1 start markers.
- 0 review bodies.
- 0 review comments.
- The PR head is still `6f76d612a3191b77ac8a1fe2b9c66da42aeb405a`.

No other reviewer's report was read.

## Real limits

- **Captures not re-read:** the raw captures stay off the packet, so they were not re-read. The per-cycle figures were re-derived from the provided decoder's published text and checked against the grader JSON. Stream-frame counts and the tap's monotonic-time flag rest on the grader's reading of the captures. The grader logic was read and fault-probed, but its run on the real files is not reproduced.
- **Library checked upstream, not on the bench:** the library-check facts in F2 come from the upstream source at the tag the build receipt names. The bench host's install was not inspected.
- **No hardware run:** no hardware, bench lock, act or hosted run was used. The hosted contexts were not inspected; the manager owns hosted and act acceptance. Physical calibration was not run, and field skips are not hardware proof.
- **Hive not run:** as the page states, the Hive application was not run. The owner's layer is untested.

## Pending manager duties

- Carry R1 and R2 to the residue checklist.
- Route F1 and F2 to the lane for a corrected head, then re-review that head under Conformance, Tests and Docs.
- Build and validate the final current-dev candidate at the merge turn (source base and live dev `6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5`).
- Own the hosted and act evidence for the exact head.
- Merge only with explicit maintainer authorization.

## Receipts

All under this packet; hashes are in `MANIFEST.sha256`.

- `scripts/check_hashes.py`, `receipts/check_hashes.txt`: capture, build and tool hashes.
- `scripts/recompute.py`, `receipts/recompute.txt`: independent per-cycle recomputation and comparison with the page.
- `receipts/control_c0_interval.txt`: control intervals (F1).
- `receipts/library_stream_input_counter_check.txt`: upstream library check and version (F2).
- `scripts/grader_fault_probe.py`, `receipts/grader_fault_probe.txt`: grader and decoder fault probe (S1, S2).
- `receipts/decode_structure.txt`: one unbind and one controller per capture.
- `scripts/privacy_scan.py`, `receipts/privacy_scan.txt`.
- `receipts/docs_gates.txt`.
- `receipts/clone_integrity.txt`: the clone at exact head, with index, modes, blobs and gitlinks verified.

R483-1 FINISHED
