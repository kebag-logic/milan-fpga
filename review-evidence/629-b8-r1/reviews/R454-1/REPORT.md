[R454] NEGATIVE - exact head 4fb5125a2e43997384839deeb1fe4742a5b2dca8

R454-1, internal cleared-context review of issue #629 / PR #646 (bench lane B8, docs only).
Head `4fb5125a2e43997384839deeb1fe4742a5b2dca8`, tree `4d4dc37d39e0cea16f2c9f38ba380de8f1ef66a8`,
diff `40714c1bd166c2a05f9607a861e8550c705d183a..4fb5125a` (two commits: `c17997fb`, `4fb5125a`;
547 added lines in `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, one changed row in
`docs/findings/README.md`; submodule gitlinks unchanged). Published evidence: branch
`629-b8-review-evidence`, commit `5bad6a43aaf9b398eca4535d3ff86a01477e132d`,
`review-evidence/629-b8-r1/author/`.

Verdict: NEGATIVE. Every bench verdict the section states re-derives from the published
evidence, and the four measured items and the STOP hold. Four findings stay open, all under
`Docs`:

- **F1 (MAJOR).** A published tool states the external capture's channel count.
- **F2 (MINOR).** Two published tools still give away the capture's sample layout.
- **F3 (MINOR).** The CRF window's capture loss is reported as 19.0 s; it is 18.7 s.
- **F4 (MINOR).** The section does not say where the B8 packet is published.

`Conformance`, `RTL`, `Robustness` and `Tests` are clean.

## Sources read

Read in order:

1. AGENTS.md and CONTRIBUTING.md (sections 4 to 6) and docs/README.md.
2. Issue #629: its body, and the [A10] assignments and rulings for lanes B7 and B8
   (issuecomment-5969106115, -5970119417, -5970598673, -5970760794 and -5970994127), the
   [A521] TAKEN, STOP and REVIEW READY, and #645 (OPEN).
3. The PR #646 body.
4. Authorities:
   - `docs/design/MEDIA_CLOCK_FOLLOWING.md`: Switching sources :1035-1052, Lock loss
     :1054-1077, `mr` :1079-1117, CLOCK_DOMAIN C1 :1146-1195, Bench :1354-1372;
   - `docs/design/TIME_SYNC.md:384-385`;
   - `docs/reference/REGISTER_MAP.md:1843-1868` and `:2006-2035`;
   - `hdl/ieee1722/aaf/KL_render_setpoint.sv`;
   - `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:572-588`;
   - `hdl/milan/milan_datapath.sv:6253-6278`.
5. The diff and its history.
6. The published packet at `5bad6a43`, and lane B7's at `c6ad37e7` for comparison only.

Prior public review findings on PR #646: none. The PR carries only the two
review-start notices, so there is nothing to resolve or retain.

## Verdicts re-derived from the published evidence

All the receipts named below are in this packet.

- **AAF to CRF and CRF to AAF switches (item 2): PASS holds.** The source is
  `summary/sw/switches.json`, together with my own decode of the raw GET_COUNTERS payloads
  in `runs/sw/events.jsonl` (`receipts/decoded-counters.txt`).
  - **MEDIA_RESET.** The DUT talker counts 0/1/2/3, and the peer counts the same as
    received. The restore makes it 4. That is one per source change, as `mr` :1081 declares.
  - **CLOCK_DOMAIN.** 6/5, then 7/6, 8/7 and 9/8: one C1 pair per switch, with the
    5.3.11.2 invariant kept.
  - **Stream Inputs.** Both of the DUT's Stream Inputs stay at 0 disruption counts.
  - **Relock times.**
    - AAF to CRF: LOCKED 2.616 to 3.116 s, ACQUIRE by 0.094 s, trim -6.0625 carried.
    - CRF to AAF: LOCKED 5.959 to 6.476 s, the meter's rate valid 3.932 to 4.439 s, 0
      history restarts.
    - Both match W2's "about 3 s / about 6 s" and E8's 4.096 s.
  - **SLIP_LB, SLIP_TDM and render.** SLIP_LB stays at 422/0 through both holds, SLIP_TDM at
    0/0 and the rail count at 31. The DUT's word reads at the run's start and end agree:
    `0x8D4` reads 414 before the binds and 422 at the end.
  - **Tone path.** The span is 417.3 s and 20,030,400 frames, with 0 net steps. 416 of 417
    blocks are at the floor; the other block holds one 108-frame (48·2+12) capture-path loss
    with a 1.95 ms read rise. Timed ratio -0.018 ± 0.569 ppm.
- **INTERNAL to AAF and #645: the data is recorded.** SLIP_LB reads 414 at the binds, then 416,
  418, 420 in ACQUIRE, and 422 between 9.151 and 9.652 s. The first LOCKED poll ended at
  7.136 s, so the slip falls 2.0 to 3.0 s after the lock instant. The ring then held to the
  restore at 437.3 s. #645 is OPEN, and the lane did not post there; carrying the data there
  is a manager duty.
- **B-CRF repeated: PASS holds.**
  - 797 polls LOCKED, trim -6.06 to -5.94, 0 net steps in 19,261,920 frames.
  - The C1 counters read 10/9 at both window marks. That covers the stall span the polls
    and the capture cannot see.
  - The stalls change no verdict, but the page misreports their size (F3).
- **CRF lock loss (item 3): as declared.**
  - **Holdover.** HOLDOVER is first seen 0.054 to 0.555 s after the unbind and lasts all
    19 polls at trim -6.00. GET_CLOCK_SOURCE reads 1 throughout and the hold is 11.041 s.
  - **`mr`.** The DUT talker's MEDIA_RESET goes 1, then 2, then stays 2: one toggle at the
    loss and none at the return (`mr` :1081-1117 and Lock loss step 3; IEEE 1722-2016
    4.4.4.3 as the design applies it). The peer receives the same.
  - **CLOCK_DOMAIN.** 10/9, then 10/10, then 11/10.
  - **STREAM_INPUT 1.** MEDIA_UNLOCKED reads 0, then 1, then 0 after the bind's bank reset.
  - **Relock.** The CRF sink locks by 0.143 s, the servo is in ACQUIRE at 0.143 to 0.643 s
    and LOCKED at 2.66 to 3.162 s.
  - **Tone segment.** 25.77 s with every block at the floor and 0 events; its longest read
    gap is 16.9 ms.
- **Saved selection across the one power cycle (item 4): PASS holds.** Sources:
  `runs/pc/*`, `runs/pc-cycle-lock.txt` and `summary/pc/pc.json`.
  - **Before the cycle.** The set 2 is read back as 2. The NVM goes from 30 commits (image
    seq 30) to 31 (image seq 31, slot A), with `dirty=0` and `commit_busy=0`.
  - **The cycle.** It runs 18:49:50.9 to 18:49:59.7. The boot console takes slot A seq 31,
    `VD_OK`, `rolled_back=0`, and the grader reads 10/10 at 18:51:19.
  - **After the boot.** The first AECP command is GET_CLOCK_SOURCE (`ctl-post.jsonl`), and it
    reads 2.
  - **Relock.** The servo state is 4 (LOCKED) at the first poll, and the C1 counters read
    1/0 since the boot.
  - **Identity.** The identity verdict after the boot is byte-equal to lane B7's.
  - **Discrimination.** The as-found index was 0, so a read of 2 tells "saved" from "reset".
- **Item 1 STOP: well founded.** Sources: `summary/proof/proof.json` and `runs/proof/*`.
  - Mapped channels 0 to 3 sit at -141.1 to -141.5 dBFS and -2 to +1 LSB, with about half
    their samples non-zero. The unmapped channels 4 to 7 are exactly zero. So the DUT
    rendered the peer's idle samples; its path was not muted.
  - In my decode, STREAM_INPUT 0 reads MEDIA_LOCKED 1 with no disruption counts, and
    FRAMES_RX (index 11) rises by 103,998 over 12.61 s.
  - The detector is not blind (`receipts/probe-b8-proof.txt`). Planted -20 dBFS tones on
    two channels read TONE PRESENT. The observed floor shape, a -50 dBFS pair and a single
    tone each read TONE ABSENT.
  - The page states where the tone was not examined and does not speculate.
- **#629 acceptance as re-judged: correct.** The page (:1704-1717) and the PR body give
  "Refs #629", not Closes:
  - Direction B THD+N is not met.
  - INTERNAL to AAF keeps #645 open.
  - Lock loss is met for both sources.
  - The saved selection is met at the bench.
- **Shorter windows and the three host stalls: disclosed, no verdict changed.** The method
  (:1441-1442), the CRF paragraph (:1605-1610), the limits (:1728-1731) and the PR body
  disclose them. The figures are wrong, though (F3).
- **Identity three times, and the tool controls.** All three `identity*/identity-verdict.txt`
  files hash `ff817aca…`, which is lane B7's row. `controls.json` is `7bbefc71…` and
  `b6_thdn.py` is `d4673f55…`, both equal to the B6 and B7 rows.
  - `grade_b8.py` differs from B7's `grade_b7.py` in four ways: the segment arguments, the
    private-environment layout, poll-sourced words and `lock_timing` from events. The
    attribution core is unchanged.
- **Hash rows.** All 46 B8 rows match the published packet (`receipts/b8-hash-rows.txt`):
  - every evidence row matches the published file's bytes, its SHA-256 and `published_sha256`
    in `MANIFEST.json`;
  - every raw row matches `RAW-ARTIFACTS.json`;
  - the `run_b8.py` "as run" prefix matches `redaction.json`.
- **Docs gates at the head, all rc 0** (`receipts/gates/`): `docs_check`, `check_doc_style`,
  `gen_toc --check`, `gen_toc --verify-anchors`, `check_em_dash --base 40714c1b`,
  `check_doc_paths`, `check_feature_status --self-test` and `git diff --check`. All 34
  in-page anchors resolve.

## Findings

```text
[R454] MAJOR Docs - 629-b8-review-evidence@5bad6a43 review-evidence/629-b8-r1/author/tools/grade_b8.py:39 (and the page row docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1794) - F1: the external capture's channel count is published in a tool docstring
Requirement/evidence: the manager's privacy ruling on #629 (issuecomment-5970598673) makes the
  external capture's channel count private. CONTRIBUTING section 6 applies the privacy rules
  to scripts. Lane B7's packet masks the same docstring line as `<capture-channels>`
  (c6ad37e7 grade_b7.py:26), but B8's grade_b8.py:39 states the number as a literal.
  grade_b8.py is not in redaction.json, and the page lists it unmasked (hash 330c14cd...).
  receipts/findings-evidence.txt locates the line without restating the value.
Impact: a value the owner ruled private is public on the evidence branch. It is the same
  leak that d36de704 had to mask after lane B7's publication.
Required change: mask the value on the evidence branch, top-only (no force-push), as
  d36de704 did. Record grade_b8.py in redaction.json with its as-run hash. Update the page
  row for tools/grade_b8.py to the retained hash, with "(masked; as run 330c14cd...)". Sweep
  every other B8 tool and record the same way for the channel count and the tone-pair channels.
Verification: a value-blind scan of the republished packet finds no literal channel count;
  the page's tools/grade_b8.py row equals the published file, and its as-run prefix equals
  redaction.json's original_sha256.
```

```text
[R454] MINOR Docs - 629-b8-review-evidence@5bad6a43 author/tools/run_b8.py:224,228,237,240 and author/tools/grade_b8.py:104-106; page docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1765-1767 - F2: the capture's sample layout is still readable in published code, and the page says it was masked at one line
Requirement/evidence: the same ruling makes the external capture's sample format private.
  The redaction masked one line of run_b8.py (`<capture-format-check>`, :64), and the page
  says run_b8.py is masked "at one line that would state the capture's sample layout". But
  the capture reader still decodes with a literal per-sample byte width and byte order: in
  run_b8.py at :224, :237 and :240, and in grade_b8.py's words24() at :104-106. Those lines
  determine the format. Lane B7's published run_b7.py:198-214 and run_b6.py:157-173 at
  c6ad37e7 carry the same decode, so the earlier packets have it too.
Impact: anyone reading the published tools can work out the private format, and the page's
  account of the masking is incomplete.
Required change: the manager rules whether code that decodes the format falls under the
  format rule.
  - If it does: mask the decode in B8's tools, and B6's and B7's if the ruling reaches them,
    top-only, and update the page's hash rows and masking sentence.
  - If it does not: record that ruling publicly, and reword :1765-1767 so it does not claim
    the layout is hidden.
Verification: the republished tools state no byte width or byte order for the external
  capture, or the ruling is linked and the page sentence matches it.
```

```text
[R454] MINOR Docs - docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1605-1610 and :1730; PR #646 body ("hid 19.0 s") - F3: the CRF window's stall loss and the stall clusters' signature are misreported
Requirement/evidence: summary/crfll/grade.json (5bad6a43) gives 19,261,920 frames captured
  (401.29 s) and 899,009 frames lost on the capture path, which is 18.73 s. The window events
  span 420.026 s. The three stall clusters (1, 2 and 3) lose 18.69 s. The page and the PR
  body say 19.0 s, which does not even match the page's own 420 - 401.3. The page also says
  "The three stall clusters are off the 48 n + 12 signature". The grade marks cluster 2 as
  on the signature: its only skip, 2,172 frames, is 48 n + 12. That cluster also carries a
  23,776-frame capture-path repeat that the page does not mention.
Impact: a measurement on the page disagrees with its own evidence. No verdict changes: the
  B-CRF PASS rests on the counted ratio and on the C1 counters, which read 10/9 at both
  marks, and both cover the stall span.
Required change: state the loss as about 18.7 s (899,009 frames) in all three places. Say
  that two of the three stall clusters are off the signature, and that the third holds a
  23,776-frame capture-path repeat.
Verification: the figures equal grade.json's capture_lost_frames / 48,000 and its
  skip_clusters[].size_signature (receipts/findings-evidence.txt reproduces both).
```

```text
[R454] MINOR Docs - docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1306-1308, :1761-1770 (B8: artifact hashes); PR #646 body "Evidence" - F4: the section does not say where its evidence is published
Requirement/evidence: AGENTS.md section 6 Docs asks for enough evidence for another cold
  reviewer. The section cites packet paths ("Paths such as runs/sw/events.jsonl are in the
  lane packet; B8: artifact hashes names it"), but B8: artifact hashes names only the label
  `629-b8-a521`. It gives no branch, pin or path mapping. Lane B7's section does
  (:1213-1219), and the same gap was a finding there (R451-1 F2). The PR body still says
  "The packet is not yet published", although it is now on `629-b8-review-evidence` at
  5bad6a43, under `review-evidence/629-b8-r1/author/`.
Impact: a cold reader cannot get from the page to the files its hash table certifies.
Required change: name the published branch, the final pin (after the F1/F2 masking) and the
  label-to-path mapping, as lane B7 does. Update the PR body's Evidence paragraph.
Verification: every hash row resolves at the named pin under the named path.
```

## Residue (wording only; does not make the verdict negative)

- **R1, `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1417-1418`.** The link labels
  `SLIP_TDM` as `[0x8D4]`, but `SLIP_TDM` is the word at `0x8D8` (`REGISTER_MAP.md:1868`);
  `0x8D4` is `SLIP_LB`, and the anchor is the section that holds both words. Exact fix: replace
  the parenthesis with ``(`0x8D8`, in [the media-boundary slip counters](../reference/REGISTER_MAP.md#0x8d4-----media-boundary-slip-counters--slip-kl_chan_map_capture))``.
- **R2, `:1739-1741`.** "Each run's `events.jsonl` records the size and SHA-256 of its run's
  raw files" is not quite right. The tone proof's `events.jsonl` records only the recording's
  size, and the full grades and `boot-console.jsonl` are recorded only in
  `RAW-ARTIFACTS.json`. Every hash still verifies there. Exact fix: "The SW and CRFLL runs'
  `events.jsonl` record the size and SHA-256 of their capture files; the packet's
  `RAW-ARTIFACTS.json` records every raw file by run directory, and is the only record of the
  tone proof's recording hash, the full grades and the boot record."
- **R3, `:1303` and `:1661`.** "with no command sent" contradicts the same table, where
  GET_CLOCK_SOURCE, the format, the RX state, the counters and the NVM were read first. Exact
  fix: "with no state-changing command sent (only the reads above)" at `:1661`, and "with no
  state-changing command sent" at `:1303`.

## Suggestions (optional)

- **S1, `:1531-1536` and `:1557-1558`.** Say "consistent with the declared recentre". An
  underrun in `KL_render_setpoint` (`:567-572`) leaves the same prefill and converged trace,
  and RENDER_STAT does not expose `underruns_o`, so the bench cannot tell the two apart.
- **S2, `:1697-1700`.** The 6 SLIP_LB dups after the boot are 3 ring slips while the DUT
  followed AAF from a cold start. They are already 6 at the first poll after the boot. Offer
  them to #645 as untimed data.
- **S3, `restore/host-*.txt:13` (evidence).** These lines carry a container `veth…`
  interface name. It is random and not bench-identifying, and `docs_check` targets only
  MAC-derived names. Mask it for consistency with `<host-if>`.
- **S4, `:1601`.** Disclose that one CRF-window poll (618) missed a word: the grade counts
  798 reads, and `b8_events.py` uses the 797 decoded ones.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Page :1267-1717 against MEDIA_CLOCK_FOLLOWING.md :1035-1117, :1146-1195 and :1354-1372, TIME_SYNC.md :384-385, issue #629's frozen acceptance and the [A10] B8 assignment and ruling; evidence `switches.json`, `lockloss.json`, `pc.json`, raw GET_COUNTERS (`receipts/decoded-counters.txt`) | R454-1 | 4fb5125a2e43997384839deeb1fe4742a5b2dca8 (evidence 5bad6a43) |
| RTL | CLEAN | No HDL in the diff (`git diff --stat`, gitlinks unchanged). The page's RTL claims were checked against `KL_render_setpoint.sv` :50-97 and :545-614 (recentre, prefill, converged, CONV_DWELL_C=100), `KL_mmcm_drp_servo.sv` :572-588 (HOLDOVER and ACQUIRE), `milan_datapath.sv` :6253-6278 (settle 2048 / 32768 ticks) and `REGISTER_MAP.md` :1867-1868 and :2030-2034 (SLIP and RENDER_STAT fields); R1 is wording only | R454-1 | 4fb5125a2e43997384839deeb1fe4742a5b2dca8 |
| Robustness | CLEAN | Lock loss and return (`lockloss.json`, `grade-lockloss.json`), the cold power cycle and boot (`runs/pc/*`, `pc-cycle-lock.txt`, `boot-console.txt`, NVM records), the host capture stalls and their effect on each verdict (`summary/crfll/grade.json` clusters; C1 counters across the stall span), restore and census (`restore/census-compare*.txt`, `dut-end2.txt`), the bench-lock incident (:1392-1398) | R454-1 | 4fb5125a2e43997384839deeb1fe4742a5b2dca8 (evidence 5bad6a43) |
| Tests | CLEAN | Detector probe of `b8_proof.py` with planted captures (`receipts/probe-b8-proof.txt`); controls and `b6_thdn.py` byte-equal to B6/B7; `grade_b8.py` against B7's `grade_b7.py` (only the attribution inputs changed); 46 hash rows (`receipts/b8-hash-rows.txt`); my own counter decode against the lane's summaries | R454-1 | 4fb5125a2e43997384839deeb1fe4742a5b2dca8 (evidence 5bad6a43) |
| Docs | UNCLEAN (F1 MAJOR; F2, F3, F4 MINOR) | Page section :1267-1807, the README row, PR body, published packet (privacy and pointer); docs gates (`receipts/gates/`) | R454-1 | 4fb5125a2e43997384839deeb1fe4742a5b2dca8 (evidence 5bad6a43) |

```text
[R454] PASS Conformance - docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1484-1717 at 4fb5125a; evidence 5bad6a43 summary/sw/switches.json, summary/crfll/lockloss.json, summary/pc/pc.json, runs/*/events.jsonl - item 2/3/4 verdicts re-derived against MEDIA_CLOCK_FOLLOWING.md W2, mr, C1 and Bench rows; Refs #629 matches #629's frozen acceptance and the 5970994127 ruling
[R454] PASS RTL - hdl/ieee1722/aaf/KL_render_setpoint.sv:545-614, hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:572-588, hdl/milan/milan_datapath.sv:6253-6278, docs/reference/REGISTER_MAP.md:1867-1868 - every RTL behaviour the page attributes (recentre trace, HOLDOVER/ACQUIRE, settle bounds, slip and render words) matches the RTL; no HDL in the diff
[R454] PASS Robustness - evidence 5bad6a43 summary/crfll/grade.json, grade-lockloss.json, runs/pc/*, restore/* - lock loss, cold power cycle, capture stalls and restore re-derived; stalls change no verdict (C1 counters cover the span)
[R454] PASS Tests - receipts/probe-b8-proof.txt, receipts/b8-hash-rows.txt, receipts/decoded-counters.txt - the STOP detector fails and passes on planted captures as claimed; controls byte-equal; all 46 hash rows hold; independent counter decode equals the page
```

## Real limits

- **The raw bench files are not published, by the lane's design.** They are kept on the
  bench host: the console polls, the captures and the boot console's timed record. So I
  verified the following only against the lane's own derived summaries (`b8_events.py`,
  `grade_b8.py`):
  - the poll-derived servo states, SLIP_LB timing and render bits;
  - the boot timings (0.3 s, 8.4 s);
  - the tone grades.
  The endpoints were cross-checked against the published DUT word reads, GET_COUNTERS
  payloads and NVM and console records. I did not re-run the grades from raw data.
- **No hardware, and no full banks.** I ran no hardware, no full parent, PP, gPTP, Yosys or
  builder bank, no act, and no RTL simulation. The diff touches no RTL.
- **Hosted checks at the exact head, read at review time.** `rtl-fast`, `changes`,
  `elaborate`, `wire-accountability`, `bdd-conformance`, `docs-check-no-git` and
  `full-ci-gate` reported success. `docs-check` was still in progress. `verilator-suites`,
  `yosys-portability`, the shards, `verilator-lint`, `yosys-elaboration` and
  "Physical gPTP" were skipped and not executed, which is consistent with a docs-only scope.
  The manager owns hosted and act acceptance.
- **Calibration.** No physical calibration was run. Printed precision is not accuracy.
- **Privacy checks.** The scan is value-blind on structure (`scripts/privacy_scan.py`), plus
  an unpublished vendor-name sweep of the page diff and the PR body (0 hits) and a read of
  every structural hit.

## Pending manager duties

1. **F1 and F2.** Mask the evidence branch top-only, rule on F2, update the page's hash
   rows, then pin the final evidence commit on the page (F4).
2. **F3.** Correct the figure in the page and the PR body.
3. **Residue.** Put R1 to R3 on the residue checklist.
4. **#645.** Carry the INTERNAL-to-AAF slip data to #645: page :1561-1593, plus S2 if
   taken. The lane posted nothing there.
5. **Merge order.** Merge PR #644 (lane B7) first, since this branch stacks on `40714c1b`.
   Then build and validate the current-dev candidate against live dev `546437243e87`, finish
   `docs-check`, and get the second independent review (R455).
6. **Re-review.** A new head un-covers `Docs`, and the other lenses wherever the change
   touches their scope.

R454-1 FINISHED
