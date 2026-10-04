[R482] NEGATIVE - exact head 6f76d612a3191b77ac8a1fe2b9c66da42aeb405a

# R482-1: internal independent review of PR #659 (Refs #653), lane B11 bench findings

- Head: `6f76d612a3191b77ac8a1fe2b9c66da42aeb405a`, tree `0023180fd4bde56446cb6a50b5344d4ecc3b1cd4`, one commit on dev `6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5`.
- Diff: `docs/findings/653_DISCONNECT_ORDER_BENCH.md` (new, 356 lines) and one row in `docs/findings/README.md:16`. No other file.
- Reconstructed from: AGENTS.md, CONTRIBUTING.md (sections 2, 3, 4 and 6), docs/README.md, the #653 body and acceptance, the lane comments on #653 (STOP 5980272602, ruling 5980290102, B11 assignment 5983239639, TAKEN 5983278802, REVIEW READY 5983553123), the PR body, the diff and commit, and the public evidence tree `review-evidence/653-b11-r1` at `980c578474ce63614e214152d87de058079c0033`.
- Prior public review findings on PR #659: none. At review start the PR had no reviews, no review comments and two review-start notices. Nothing to resolve or retain.

## Verdict

The page's central result holds up under independent re-derivation. It is the UNBIND_RX response leaving the DUT's port before the unlock's unsolicited GET_COUNTERS, in 23 of 23 captures. The figures are 7.5 µs for command to response, 114.2 to 116.8 µs for response to push on AAF input 0, and 99,346.2 and 99,731.4 µs on CRF input 1. I rebuilt every order and interval from the provided decoder's published output, independently of the lane grader, and all 23 match.

The verdict is NEGATIVE because of two MINOR findings:

- **F1:** the page presents the controller library's silence as evidence about the reported defect. The library's only stream-input counters check cannot detect that defect.
- **F2:** one interval in the control-capture section is attributed to the wrong frame.

Both are page fixes. Neither changes a capture, a measured order or the wire-order conclusion.

## Findings

### F1 - MINOR - Conformance, Tests, Docs - the library's "no counter error" result cannot fail for the reported defect or for the CRF 1/0 window, and the page does not say so

- **Where:**
  - `docs/findings/653_DISCONNECT_ORDER_BENCH.md:36-37`: the headline, "flagged nothing in any of them".
  - `:44`: acceptance 4, "Held for the library".
  - `:224-226`: the library's check, quoted.
  - `:252-254`: the CRF window, "It flagged nothing then".
  - `:285-287`: Limits.
  - `docs/findings/README.md:16`: "The library flagged nothing".
- **Evidence:** I fetched the controller library's public source at the tag the probe was built against (`v4.3.1.1`, commit `6d61a92e7f264c69f23cdc38f50d31114e567aa0`; `runs/build/build-3.txt` records the same tag). It has one stream-input counters check, at `src/controller/avdeccControllerImpl.cpp:1611`.
  - It removes the Milan flag only when `lockedValue != unlockedValue && lockedValue != (unlockedValue + 1)`.
  - The input's connection state is not an input to that check.
  - No other use of MEDIA_UNLOCKED exists in the library's `src/` or `include/`.
  - So both pairs that matter here pass in any connection state: 1/1, whichever of the response and the push arrives first, and 1/0, the pre-#655 CRF window.
  - The check could not have fired in either order (receipt `receipts/library_check.txt`).
  - Also, no counters update reached the library inside either CRF window: one update after each unbind, and none before the 1/1 one (`receipts/rederive_library.txt`, R01 and R02). So "It flagged nothing then" had nothing to judge even in principle.
  - The page quotes the check's message and clause and says it "raised no event in any cycle". It does not state its condition.
- **Impact:**
  - A reader takes the library's silence as evidence that a real controller tolerates the reported order and the CRF 1/0 window. It is not evidence of either.
  - The negative result has a consequence the page does not draw: the owner's reported flag cannot come from this library check, so it must come from a layer above it. That makes "the Hive application was not run" the decisive gap for acceptance 4, not a side limit.
  - Two kinds of evidence remain sound and should stay: the wire order, and the library's processing order (NotConnected before the counters update, 51 to 113 µs on AAF).
- **Required outcome:**
  - The page states the library check's condition: MEDIA_LOCKED equal to MEDIA_UNLOCKED or one more, independent of connection state.
  - It states that the check therefore could not flag either order or the 1/0 window.
  - The acceptance-4 row and the README row qualify "no counter error" accordingly.
  - The CRF section notes that no counters update arrived inside the window.
  - Limits names the layer above the library as the only remaining source of the reported flag.
- **Verification:** re-read the page and README row at the new head against `avdeccControllerImpl.cpp:1611` at `v4.3.1.1`, and re-run `library_check.py` and `rederive_library.py`.

### F2 - MINOR - Tests, Docs - the control's 1,629.8 µs is the UNBIND_RX command's interval, not the response's

- **Where:** `docs/findings/653_DISCONNECT_ORDER_BENCH.md:237-238`: "The response came 1,629.8 µs after the probe's own GET_COUNTERS answer."
- **Evidence:**
  - The grader's field is `own_rsp_to_cmd_us = cmd - own` (`tools/o653_grade.py`; `o653-grade.json` `s0b/C0`).
  - Rebuilt independently from the decoder's C0 output: own answer to UNBIND_RX command 1,629.8 µs, own answer to UNBIND_RX response 1,637.3 µs (`receipts/control_interval.txt`).
- **Impact:** a stated interval in the control evidence is false as written. It is off by 7.5 µs, and the order is unaffected.
- **Required outcome:** the sentence names the UNBIND_RX command with 1,629.8 µs, or states 1,637.3 µs for the response.
- **Verification:** re-run `control_interval.py` against the new wording.

### S1 - SUGGESTION - Docs - name the identity tool's aggregate FAIL

The published `identity/identity-verdict.txt` ends "IDENTITY GATE: FAIL".

- Its three FAIL lines are exactly the live fields the page lists at `:65-67`: STREAM_INPUT 0 offset 78 (current_format), CLOCK_DOMAIN 0 offset 71 (clock_source_index) and GET_CLOCK_SOURCE.
- The lane's STOP gate, the four ATDECC entity facts, passes (`receipts/restore_check.txt`).

A clause saying that the tool's aggregate line reads FAIL on those three fields only would save a cold reader the reconciliation. This is optional.

### S2 - SUGGESTION - Tests - the control does not exercise the unlock-push selection

The C0 control proves that the comparator can read COUNTERS_FIRST, using the probe's solicited answer. It does not exercise the selection of the unlock push itself.

A disposable reviewer probe covered that path (`receipts/synth_probe.txt`). It built synthetic captures in the documented tap layout and ran the published grader and decoder on them:

| Capture | Grader and decoder read |
|---|---|
| Push moved ahead of the response | COUNTERS_FIRST |
| Push removed | NO_UNLOCK_PUSH |
| Response first | RESPONSE_FIRST |

The page could mention this limit of the control. This is optional.

## Evidence examined, per lens

**Conformance.**
- Acceptance 1 to 4 against the page's table at `:39-44`.
- All 23 rows at `:161-185`, recomputed from `o653-grade.json`: 195 checks, 0 fail (`receipts/verify_page.txt`).
- Order and both intervals rebuilt from the decoder's published outputs, independent of the grader. The decoder output is S = lo·2^32 + hi, so the true interval is round(ΔS/2^32) ns. All 23 match (`receipts/rederive_decoder.txt`).
- The AAF talker was still streaming at each unbind: 303 to 1,562 frames after the command, and the last one 37.8 to 195.2 ms after it, long after the unlock push at about 0.12 ms. So the unlock came from the unbind.
- CRF: the push came 99.3 and 99.7 ms after the response. This is consistent with the 100 ms silence timeout at the image's RTL.
- The finding is F1.

**RTL.**
- The diff touches no HDL (`git diff --name-status`: two docs files).
- I checked the page's RTL-derived statements against the image's source, dev `bbf704ec`, an ancestor of the base. `KL_crf_rx.sv`, `KL_avtp_rx_monitor_ctx.sv` and `milan_datapath.sv` are unchanged from `bbf704ec` to the base.
  - CRF unlock only at the 100 ms timeout: `bbf704ec:hdl/ieee1722/crf/KL_crf_rx.sv:529-537`.
  - AAF unlock at the bind fall: `bbf704ec:hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:857`.
- PR #655 is open, and the image does not contain it, as the page says.
- Clean.

**Robustness.**
- The grader fails closed: NO_UNBIND, NO_UNLOCK_PUSH, the decoder's NO_LINES, the VLAN-tag path, and the tap timestamp monotonic in all 23 captures.
- Every unbind came at least 2.000 s after the input's last counters update (`receipts/check_cadence.txt`).
- Restore and census (`receipts/restore_check.txt`):
  - Census 45 of 46; the one difference is the GET_AVB_INFO propagation delay, 381 to 387 ns.
  - NVM image seq 51 to 98 and commits 20 to 67: 47.
  - CLOCK_DOMAIN 0 counters 3/3 to 6/6.
  - Servo trim `0xffa40035`, then `0x00000020` after the SET 0 / SET 1 release, each read back.
- Library and session state:
  - Deregistration: SUCCESS from both entities in both sessions.
  - No flag-type library event in either session.
  - The Milan flag is present on every update.
- The limits on push cadence and on a single registered controller are stated.
- Clean.

**Tests.**
- The decoder defects the page states are confirmed:
  - The time words are swapped: the synthetic capture shows it, and the real decoder outputs reconcile to 7.5 µs only under the swap.
  - The ACMP columns are wrong: the decoder prints the talker's ID as the listener, `luid=255` (bytes 2-3 of the DUT's entity ID) and cc from the destination MAC. The grader reads 0001/1/3 on the same frame (`receipts/synth_probe.txt`).
- The control C0 reads COUNTERS_FIRST against the probe's own answer, and RESPONSE_FIRST against the push.
- Probe build hashes match `runs/build/build-2.txt` (s0b: source `3821d3d5…`, binary `305884f6…`) and `build-3.txt` (s1: source `2d8079e3…`, binary `eafd3eb5…`, header `3d09fa69…`), and the published `o653_probe.cpp`, `o653_grade.py` and `tap_order_decode.py` hash to the page's values.
- The findings are F1 and F2.

**Docs.**
- Capture names, bytes and SHA-256 at `:305-329`, and the 12-hex prefixes in the per-cycle table, equal `RAW-ARTIFACTS.json`: 23 of 23 (`receipts/cmp_hashes.txt`).
- The publication `MANIFEST.json` matches all 206 files. The four author-manifest mismatches are exactly the publication's content redactions.
- Docs gates at the head are all rc 0 in a scratch environment with the pinned Markdown lock (`receipts/docs_gates.txt`):
  - `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`.
  - `check_em_dash.py --base 6c22d3ca`, `check_doc_paths.py`, `check_feature_status.py --self-test`, `ci_scope.py --selftest`.
  - `check_baremetal_only.py --check` and `--selftest`. In the scratch environment, which has no pyyaml, these refuse with rc 2; they pass rc 0 under the system interpreter.
  - `git diff --check`.
- Privacy: the page names no reference peer, instrument, host, subnet, interface or probe directory, and equipment appears by role.
- The commit is one line with no trailers.
- The findings are F1 and F2.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | page `:34-49`, `:153-199`, `:228-254`; #653 acceptance 1-4; `o653-grade.json`; `summary/decode/*.decode.txt`; probe logs s0b/s1; library `v4.3.1.1` `avdeccControllerImpl.cpp:1611` | R482-1 | `6f76d612a3191b77ac8a1fe2b9c66da42aeb405a` |
| RTL | CLEAN | diff name-status (no HDL); `bbf704ec:hdl/ieee1722/crf/KL_crf_rx.sv:529-537`; `bbf704ec:hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:857`; no change to either file, or to `milan_datapath.sv`, from `bbf704ec` to base | R482-1 | `6f76d612a3191b77ac8a1fe2b9c66da42aeb405a` |
| Robustness | CLEAN | `tools/o653_grade.py` fail-closed paths and synthetic captures; `restore/*` (census, counters, NVM, servo, clock release); probe logs (cadence, deregistration, flags) | R482-1 | `6f76d612a3191b77ac8a1fe2b9c66da42aeb405a` |
| Tests | UNCLEAN (F1, F2) | control C0 (grader and decoder); `tap_order_decode.py` vs `o653_grade.py` on synthetic captures; build records 1-3 vs page hashes; library check condition | R482-1 | `6f76d612a3191b77ac8a1fe2b9c66da42aeb405a` |
| Docs | UNCLEAN (F1, F2) | page whole; `docs/findings/README.md:16`; `RAW-ARTIFACTS.json`; `MANIFEST.json`; docs gates at head; privacy scan | R482-1 | `6f76d612a3191b77ac8a1fe2b9c66da42aeb405a` |

## Real limits of this review

- The 23 captures are not public; only their hashes and the decoder outputs are. Hashes were compared with the author's raw-artifact record, not recomputed from capture bytes. The independent re-derivation of order and timing uses the decoder's published text, so it depends on that text being the decoder's real output for those captures.
- The 28-byte tap record layout was not checked against the tap's own documentation. It is supported by consistency: under the grader's reading the 23 command-to-response intervals all come out 7.5 µs, and the timestamps are monotonic.
- No hardware, controller host or tap was touched. The Hive application's own checks are unknown to this review as well.
- Physical calibration was NOT RUN. Hosted skips are not hardware proof.

## Pending manager duties

- Hosted acceptance at this head. When read, the check runs showed 7 success and 7 skipped, and `docs-check` was in progress (`receipts/hosted_checks.txt`).
- Act and candidate-merge validation against live dev (`6c22d3ca`).
- Carry F1 and F2 to the lane. Both are page edits, so a new head needs a re-review of Conformance, Tests and Docs.
- Acceptance 4 on #653 remains open at the Hive layer whatever this PR's outcome.

R482-1 FINISHED
