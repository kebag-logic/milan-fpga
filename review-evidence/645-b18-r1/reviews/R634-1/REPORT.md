[R634] POSITIVE - exact head 480c5e916f8bf711c47e1985ba3efe2b2471bdda

# R634-1: internal independent review of PR #747 (issue #645, bench lane B18)

- Exact head `480c5e916f8bf711c47e1985ba3efe2b2471bdda`, tree `5841131ff2c6d46a1c96ebfcc0ff9445e62825e7`, one commit on dev `9ef717727e6fdac11ee7f01672fefae948452343`. The commit message is one line with no trailers.
- Delta: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` only, +315 lines. This is the Contents entry at `:93` and the section "Dev 9ef71772, 2026-10-15: lane B18" at `:4982-5294`. No source, test, gitlink or other document changes. The diff is in `receipts/diff.patch`.
- Reconstructed from:
  - AGENTS.md, CONTRIBUTING.md (sections 2, 3 and 6), docs/README.md;
  - issue #645's body and the public decisions on it: ruling [6099627217](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6099627217), the B17 assignment 6186729424 and its answer 6186940255, the PR #742 round-2 decision 6193474559, and the B18 assignment [6199691564](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6199691564);
  - the operator's TAKEN 6199781988 and REVIEW READY 6200209744;
  - the design's settle-recentre table and "A bind at INTERNAL" (`docs/design/MEDIA_CLOCK_FOLLOWING.md:1088-1096`, `:1264-1370`), `SLIP_LB`/`RENDER_STAT` in `docs/reference/REGISTER_MAP.md:1878` and `:2017-2045`, and `hdl/milan/milan_datapath.sv` at this head;
  - the public evidence packet `review-evidence/645-b18-r1` at `2e9135196430eb73fb9c2ca414a17f111d61028d`, and B17's published packet `review-evidence/645-b17-r1/{author,author-r2,author-r3}` at `bdb96b6685751a424fbbdc952726f33efd17282a`.
- Before this verdict there were no review findings on PR #747: 0 reviews, 0 review comments, and only the two review-start notices. So no earlier finding needed resolving or carrying forward.
- No bench access. The review is proved from the packets' receipts, with offline recomputation and disposable probes under this packet's `scratch/`.

## Verdict basis, by focus item

1. **Identity binds the run to the dev 9ef71772 image: PASS.**
   - `identity/identity-verdict.txt` is 11 of 11 PASS. Over ATDECC it reads entity_id `020000fffe000001`, "Milan FPGA 1x1 TDM8", `2.96.0` and `AX7101-0001`, which equal B17's identity row (`:4656` vs `:5027`).
   - The console reads `ID=4d494c4e VERSION=00020060`, the AEM CRC is `5ba355eb` over 7,512 B, the live ENTITY and CONFIGURATION are byte-equal to QSPI, and the clock-source set is as for #629. The UART grader is 10 of 10, inside the 18:50:11.845Z to 18:50:17.651Z lock window.
   - No read on this image separates `9ef71772` from `5603c353`. VERSION, the AEM CRC and the QSPI AEM dump are equal to B17's (`receipts/identity_compare.txt`). The page says so and rests the image identity on the manager's flash record (`:5035-5038`). That record is the manager's public statement in the B18 assignment: `FLASH_RC=0`, `POWERCYCLE_RC=0`, and the boot line `CSR ID=4d494c4e VERSION=00020060`, AEM 7512 B, CRC `5ba355eb`.
   - The as-found state is consistent with a fresh cold boot: `SLIP_LB` 0 against B17's 208, NVM `commits ok=0`, `pend=0`.
   - The ATDECC identity strings are the project's own AEM constants (`avdecc/aem_specs.py:44`), not bench identity.
2. **B17's method ran unchanged: PASS.**
   - `console_poll_b8.py` (`1912837a…`), `ana_b17.py` (`299d4f55…`) and `peer_gap_b17.py` (`93c62e30…`) are byte-identical to B17's packet copies. They also equal B17's page hashes (`:4946-4980`) and the poller hash every B17 cycle recorded at run time.
   - `cyc_b18.py` (`d41d0480…`) differs from B17's run-time `cyc_b17.py` (`12ec02fe…`) in 8 diff lines: 2 added comment lines, and `RAW`, `CTL_DIR` and the capture name. Nothing else changed.
   - Every B18 cycle's start event records `tool_sha256=d41d0480…` and `poller_sha256=1912837a…` (`receipts/cycle_tools_timebase.txt`). `run_locked_b18.sh` and `baseline_b18.sh` differ from B17's only in their environment name, staging path and comments.
   - Each cycle ran the same schedule: unbind at +2 s, format rule, bind 6 s later, 32 s hold, 80 polls at 0.5 s, a 50 s / 96 B tap capture, all ten.
   - The polls covered -8.00 s to +31.70..+31.88 s from the bind, against B17's -8.01..-7.99 to +31.75..+31.93 (recomputed for both lanes). The tail in c01 and c10 is 0.05 s shorter than B17's shortest; see S1. Every gap between cycles and the end baseline are covered by the cumulative counter.
   - Tap and host agree on the unbind-to-bind interval within 0.1 ms in every cycle.
3. **The per-cycle table equals the raw counter logs, and every cycle is graded correctly: PASS.**
   - `summary/counter-logs.sha256` verifies all ten `poll.jsonl`, and its own SHA-256 is the page's `2c5e8d6f…`. The author `MANIFEST.sha256` verifies all 89 entries, and all 13 page evidence rows match in bytes and SHA-256. All ten capture rows equal `RAW-ARTIFACTS.json`, with 0 kernel drops.
   - An independent recompute (`scripts/recompute_b18.py`, `receipts/recompute_b18.txt`) reproduces every cell from raw:
     - every bind UTC, 80 polls, the first and last poll offset, and 800 of 800 readable;
     - `SLIP_LB` 0 in all 800 polls, and 0 at both baselines (`restore/dut-{start,end}.txt` `0x900008d4`), with `SLIP_TDM` 0;
     - `MCSRV_STAT` `0x20` (IDLE) throughout, and the AAFM/CRF words 0;
     - `RENDER_STAT`: prefill with fill 0 through the unbound span, prefill cleared by 0.11-0.67 s, converged by 0.59-0.67 s, fill 8-14 after, rails 0;
     - CLOCK_SOURCE 0/1 at the start and end of every cycle, and every cycle ending bound with flags `0x0002`.
   - With no change there is nothing to grade as the #743 residual or as class (c), so "Held" is correct for all ten under the assignment's rule (`SLIP_LB` unchanged).
   - The tap cells were checked against the graded summaries (`scripts/check_tap_figures.py`, `receipts/check_tap_figures.txt`, 0 mismatches): first PDU, first burst s/peak, bursts and peak to the last poll, and delta_ppm.
     - The first burst over 20 us is also the first PDU over 10 us in every cycle (`over_10us_before_arm` empty).
     - Its offset after the design firing time is 32.735 to 4,557.171 ms, so the page's "32.7 ms to 4.56 s" holds.
     - The capture-end counts (12-22), peaks (28.0-32.0 us), p99.9 (4.5-5.9 us) and peer rate (+4.87 to +4.92 ppm) match.
   - B17's columns of the comparison table equal B17's own section (bind UTC and slip interval). B17's first bursts and its 30.3 us maximum, recomputed from B17's `late_pdus` with the stated rule, match (`receipts/b17_bursts.txt`).
   - The c01 capture explanation reproduces: the peer's AAF continued 4.951 s after the unbind against 0.002-0.181 s for the other nine, and B17's c08 shows 4.875 s (`receipts/peer_gap_check.txt`).
   - The decoded GET_COUNTERS payloads (`receipts/decode_counters.txt`) show exactly the moves the page lists. MEDIA_LOCKED reads 1 static, every other DUT STREAM_INPUT counter is 0 static, and the end values match the page's ranges.
4. **Restore read-back equals the as-found state: PASS.**
   - An independent census diff ignores only the seq and timestamp fields. 45 of 46 entries are equal, and entry 8 differs only in the GET_AVB_INFO propagation delay, `0x17e` against `0x184` (382 and 388 ns).
   - The DUT binding is flags `0x0002` at `0205022001006000`. The peer is `0x0082` on its CLOCK_SOURCE 1, and all formats and maps are equal.
   - The NVM residual is seq 315→335 with commits 0→20, `pend=0` and `VD_OK`.
   - The controller staging was removed, no lane process is left, and both baseline lock windows returned rc 0.
5. **Close condition and limits: PASS.**
   - The ruling as the B18 assignment restates it is met: "every bind at INTERNAL holds, apart from the #743 residual". It held 10 of 10, with no residual.
   - The stated limits are honest:
     - `recentres_o` reaches no CSR. `RENDER_STAT` is `{rails, 6'd0, converged, prefill, fill}` at `hdl/milan/milan_datapath.sv:6835-6838`, and `rsp_recentres_w` is a simulator tap only (`:6833`, `:6877`).
     - The arming window was not exercised. Every first late burst came at or after the design firing time plus 32.7 ms, and the page claims nothing about that window.
   - See S2 on the firing time being the earliest.
6. **No private device, host or instrument is named: PASS.**
   - A scan of the 315 added lines finds no address, MAC, host, path, interface, vendor or product name. The equipment is named by role.
   - `docs_check.py` (identity scrub) is rc 0.
   - Lane and operator labels appear only in findings-page prose and PR text, which the comment rule allows. There is no source delta, so the comment rule has no new instance.

## Findings

No BLOCKER, MAJOR or MINOR. One RESIDUE and three SUGGESTIONs.

```text
[R634] RESIDUE Docs: PR #747 body, "Counters that moved" bullet: "the rest stayed at 0" over-reaches
ID: R634-1-RS1
Requirement/evidence: The body says "Nothing else moved: MEDIA_UNLOCKED, STREAM_INTERRUPTED, SEQ_NUM_MISMATCH, MEDIA_RESET, LATE_TIMESTAMP and the rest stayed at 0."
  The decoded payloads show the DUT's STREAM_INPUT 0 MEDIA_LOCKED at 1 and AVB_INTERFACE 0 LINK_UP at 1, both static (receipts/decode_counters.txt).
  The page itself is exact: MEDIA_LOCKED "1 at both reads" at docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:5218.
Impact: Wording only. Read as "the rest of the error counters", it is true. It changes no figure, grade or claim on the page.
Required change (exact fix): replace "and the rest stayed at 0." with "and the other error counters stayed at 0; MEDIA_LOCKED read 1 at both reads."
Verification: The PR body text.
```

```text
[R634] SUGGESTION Conformance: docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:5010 and :5121-5122: the realised poll tail against B17's
ID: R634-1-S1
Requirement/evidence: The assignment says "poll ... for at least as long as B17 did". The TAKEN plan says "to at least 31.75 s after it".
  B18's last poll ended at +31.70 s in c01 and c10. B17's shortest was +31.75 (c03).
  Total spans are 39.70 s against B17's minimum of 39.74 s. Same poller, 80 polls, same schedule.
  Every inter-cycle gap and the tail are covered by the cumulative counter: all reads are 0 through the end baseline.
Impact: None on any grade. The window where B17's slips fell (0.07-5.67 s) is covered with more than 26 s to spare.
Suggested change: one clause saying that the tail fell 0.05 s short of B17's shortest in two cycles from poll timing, with the counter cumulative over it.
Verification: receipts/recompute_b18.txt, the "last" columns for both lanes.
```

```text
[R634] SUGGESTION Robustness, Docs: docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:5102-5103, :5136 and :5252-5254: the 42.7 ms firing time is the earliest
ID: R634-1-S2
Requirement/evidence: "Fires at INTERNAL" needs 2,048 settled or disengaged ticks running, and an excursion restarts the run.
  Sources: docs/design/MEDIA_CLOCK_FOLLOWING.md:1092, and hdl/milan/milan_datapath.sv:6645-6676 (settle_run_ticks_r reset when !settle_steady_w or settle_exc_w).
  The aligner state has no CSR, so the silicon firing time is first PDU + 42.7 ms at the earliest.
  The page labels the figure "the design's", which follows the design's own sentence at MEDIA_CLOCK_FOLLOWING.md:1300.
Impact: None on the verdict. A later firing would only put a burst inside the arming window, and the binds held anyway. The page's "does not test that window" stays conservative.
Suggested change: "the design's earliest firing time".
Verification: The page text.
```

```text
[R634] SUGGESTION Docs: docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:5019-5021: point at the published packet
ID: R634-1-S3
Requirement/evidence: The page says the packet "645-b18-a622" is held by the manager. It is now public as review-evidence/645-b18-r1 at 2e913519, but the PR and issue do not yet link it. B17's section names its published location (:4644-4648).
Impact: A cold reader needs the PR or issue thread to find the receipts.
Suggested change: Publish the evidence link on the PR and issue (manager duty). Optionally name the location on the page in a later findings round.
Verification: Link present.
```

## Lens results

```text
[R634] PASS Conformance: docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:4982-5294 against issue #645 ruling 6099627217 and B18 assignment 6199691564 items 1-5
  Checked: identity receipts (identity-verdict, console-identity, grader, lock window) against B17's identity row and the manager's flash statement.
  Checked: tool byte-identity against B17's packet.
  Checked: the per-cycle table and the comparison against the raw logs and both lanes' summaries.
  Checked: grading against PR #742's stated behaviour; the restore read-back against the as-found census; the close condition; and the privacy rule.
  S1 recorded.
[R634] PASS RTL: hdl/milan/milan_datapath.sv:6634-6676 and :6824-6839, docs/design/MEDIA_CLOCK_FOLLOWING.md:1088-1096 and :1296-1309, docs/reference/REGISTER_MAP.md:1878 and :2041-2045
  There is no RTL in the delta. The page's RTL-derived claims were checked at this head:
  - the bind arm is the first PDU at INTERNAL only (settle_bind_arm_w = !follow_sel_r && ...);
  - the firing rule;
  - the recentre count reaches no CSR (RENDER_STAT field packing);
  - the recentre counts in neither SLIP_LB half, so "held" means no slip.
[R634] PASS Robustness: review-evidence/645-b18-r1 cycles c01-c10, restore/, RAW-ARTIFACTS.json, summary/peer-gap.json
  Checked: the unbound span; the c01 4.95 s peer-tail anomaly (DUT in prefill with fill 0, no counter move); inter-cycle and tail gaps (cumulative counter joins); 0 unreadable polls; 0 kernel drops; 0 sequence gaps.
  Checked: the honest scope limits: arming window untested; the residual rule never exercised on silicon; following-mode binds out of scope.
  S2 recorded.
[R634] PASS Tests: scratch rerun of tools/summ_b18.py (byte-identical outputs), scripts/recompute_b18.py, scripts/check_tap_figures.py, scripts/b17_bursts.py, scripts/decode_counters.py, scripts/mutation_probe.sh, receipts/gates.txt
  Checked: the packet's summary tool reproduces cycles.json, table.md, compare.md, counters.md, counter-logs.sha256 and its stdout byte-for-byte from the published inputs (receipts/summ_b18_rerun.txt).
  Checked: three planted faults in c10's raw log plus the end baseline are each detected (exit 1, lane held 9; receipts/mutation_probe.txt):
    - +2 at the first burst is graded "B17 class (c)", largest lateness 25.313 us;
    - +1 whose interval holds the first PDU is graded "#743 residual";
    - +1 at +20 s is graded "other / not held".
  My independent recompute flags each one.
  Checked: the seven Markdown/hygiene gates are rc 0 at the head with the pinned markdown lock.
[R634] PASS Docs: docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:93 and :4982-5294; PR #747 body (byte-equal to the packet's PR-BODY.md)
  Checked: docs_check (0 findings, scrub self-test 23/23), check_doc_style, gen_toc --check, check_em_dash --base 9ef71772 (0 over 315 added lines), check_doc_paths, check_baremetal_only and git diff --check, all rc 0.
  Checked: every intra-page anchor and both cross-page anchors resolve to existing headings.
  Checked: the limits section states what the lane cannot show.
  RS1 (wording only), S2 and S3 recorded. None leaves the lens unclean.
```

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Findings page `:4982-5294`; issue #645 rulings 6099627217, 6186940255, 6199691564; B18 packet identity/, tools/, cycles/, summary/, restore/; B17 packet and page section `:4613-4980` | R634-1 | `480c5e916f8bf711c47e1985ba3efe2b2471bdda` |
| RTL | CLEAN | `hdl/milan/milan_datapath.sv:6634-6676`, `:6824-6839`, `:6877`; design `:1088-1096`, `:1264-1370`; register map `:1878`, `:2017-2045` (claims checked; no RTL in delta) | R634-1 | `480c5e916f8bf711c47e1985ba3efe2b2471bdda` |
| Robustness | CLEAN | Raw poll and event logs c01-c10; restore baselines and census; peer-gap and capture records; limits `:5246-5259` | R634-1 | `480c5e916f8bf711c47e1985ba3efe2b2471bdda` |
| Tests | CLEAN | Byte-identical rerun of `summ_b18.py`; independent recompute; 3 mutation probes; gate receipts | R634-1 | `480c5e916f8bf711c47e1985ba3efe2b2471bdda` |
| Docs | CLEAN | Page `:93`, `:4982-5294`; PR #747 body; seven doc and hygiene gates; anchors; privacy scan | R634-1 | `480c5e916f8bf711c47e1985ba3efe2b2471bdda` |

The RESIDUE RS1 does not un-clean Docs, by the owner's residue rule. The SUGGESTIONs do not affect coverage.

## Real limits

- **Tap figures.** The raw captures are not published; only their SHA-256 and byte counts are recorded. Every tap figure was checked against the operator's graded summaries (`summary/cNN.json`, from the byte-identical `ana_b17.py`). They were not re-derived from the captures, and `ana_b17.py` was not re-run.
- **Image identity.** It rests on the manager's public flash statement plus behavioural consistency, as the page states. No device read distinguishes the two images, and I examined no flash receipt itself.
- **The recentre is unobserved.** "Held" is the counter's result. The arming window and the #743 residual were not exercised on silicon. #743 remains open.
- **Switch cases on this image.** #645 acceptance 3 (the INTERNAL→AAF and AAF→CRF switch repeats) was ruled met by lane B14 on the pre-#742 image `5603c353` (6099627217). No bench lane re-ran those switches on `9ef71772`. The B18 assignment set the close condition to the bind repeat only. Recorded for the manager; it is not a finding against this PR's scope.
- **No physical claims.** Physical calibration NOT RUN. Printed precision is not calibrated accuracy, and field skips are not hardware proof.
- **Validation runs not made.** No manager source bank ran at this head, and none is claimed or inferred. Source-head execution evidence is the operator's gate receipts, and I reproduced the seven doc/hygiene gates myself. No Docker, act, builder or full banks were run.
- **Hosted checks.** At exact head, the read-only snapshot was 18 success, 21 skipped and 4 in progress (`docs-gates-0..2`, "Fail fast across this head"), in `receipts/hosted_checks.txt`. Skipped contexts are not executed evidence. The manager owns hosted and act acceptance.
- **Clone integrity.** The clone was restored and verified: HEAD and tree are exact, the worktree and index are clean, and index modes and blobs equal the tree. The six gitlinks (`external`, `gptp-processor`, `protocol-processor`, `third_party/{lwSRP,tsn-c-stack,verilog-axis}`) are unchanged against the base. The ignored `scripts/__pycache__` created by the gate run was removed.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base and live dev `9ef717727e6fdac11ee7f01672fefae948452343`). Link its builder and native-bank receipts, and complete the hosted and act acceptance at the merge turn.
- Publish the evidence-packet link (`review-evidence/645-b18-r1` at `2e913519`) on the PR and the issue (S3).
- Carry R634-1-RS1 to the residue checklist, and decide S1 and S2.
- Obtain the second, external positive review and the maintainer's merge authorisation. "Closes #645" then closes the issue, with #743 left open for the in-window residual.

R634-1 FINISHED
