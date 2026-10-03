[R455] NEGATIVE - exact head 4fb5125a2e43997384839deeb1fe4742a5b2dca8

Round R455-1, external independent review of PR #646 (issue #629, bench lane B8), docs only.
Head `4fb5125a2e43997384839deeb1fe4742a5b2dca8`, tree `4d4dc37d39e0cea16f2c9f38ba380de8f1ef66a8`,
diff `40714c1bd166c2a05f9607a861e8550c705d183a..4fb5125a` (stacked on PR #644): the dated section
"Dev bbf704ec, 2026-10-03: lane B8" in `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`
(+546 lines; lines 1267-1806 plus the page introduction and Contents) and its row in
`docs/findings/README.md`.
Evidence: branch `629-b8-review-evidence` at `5bad6a43aaf9b398eca4535d3ff86a01477e132d`,
`review-evidence/629-b8-r1/`.

Verdict basis: four open MINOR findings (F1 to F4) leave the Docs, Tests and Robustness lenses unclean.
No finding changes an item verdict on the page. Every item verdict (item 2 PASS for AAF to CRF and CRF to AAF;
#645 repeated for INTERNAL to AAF; item 3 as declared; item 4 PASS; item 1 NOT RUN) re-derives from the
published packet. "Refs #629" is correct.

## Independent re-derivation (receipts/rederive-b8.txt, scripts/rederive_b8.py)

The published packet verifies. MANIFEST.json has 252 entries, 0 missing, 0 mismatched and 0 unlisted;
8 files carry a publication-time redaction recorded as original vs published. All 33 evidence rows of the
page's "B8: artifact hashes" table match the packet in size and SHA-256 (receipts/packet-verify.txt).

**Item 2, switches** (`summary/sw/switches.json`, `runs/sw/events.jsonl`). The three sets answered SUCCESS
and read back 2, 1 and 2. LOCKED came at 6.636-7.136, 2.616-3.116 and 5.959-6.476 s after each set,
against the design's about 6 s onto AAF and about 3 s onto CRF (MEDIA_CLOCK_FOLLOWING.md Switching sources).
GET_CLOCK_SOURCE held the set index at all three marks. Every hold poll read LOCKED (238/298/298).

- **Trim:** carried across both stream-to-stream switches (-6.0625 / -6.0 in ACQUIRE).
- **MEDIA_RESET:** DUT STREAM_OUTPUT 0 went 0, 1, 2, 3 and the peer STREAM_INPUT 0 received 0, 1, 2, 3.
  That is exactly 1 per change, against the declared one `mr` toggle per source change.
- **CLOCK_DOMAIN:** LOCKED/UNLOCKED moved (1,1) per change and LOCKED-UNLOCKED stayed in {0,1} (C1).
  The locked, mid and end marks are identical in each phase.
- **Receive path:** both DUT Stream Inputs show 0 disruption counters.
- **Ring and render words:** `SLIP_LB` held 422/0 static, `SLIP_TDM` 0/0 static and the render rails 31
  static across both stream-to-stream switches. The converged bit fell by 0.105 s and 0.094 s and was high
  again by 0.61 s and 0.60 s. It was never low after CRF to AAF. That matches the RTL claim the page makes:
  a recentre on a short queue re-enters prefill and clears converged, and one on a full queue snaps the
  read pointer with no trace (`hdl/ieee1722/aaf/KL_render_setpoint.sv:584-610`).
- **Tone path:** the span runs 417.31 s of wall time from 20 s after the first set. Both stream-to-stream
  switches fall inside it, at +107.3 s and +260.6 s. Result: 1 event, a 108-frame capture-path skip with a
  matching read-time rise; 0 non-capture steps in 20,030,400 frames; timed -0.018 +-0.569 ppm. 416 of 417
  blocks sit at the floor.
- **Independent counter decode:** I decoded all 144 GET_COUNTERS payloads in `runs/{sw,crfll}/events.jsonl`
  independently. They match the lane's decoded summaries with 0 mismatches. A planted MEDIA_RESET mutation
  is caught, so the check can fail (receipts/counters-decode*.txt).

**#645 data.** The page records the INTERNAL-to-AAF `SLIP_LB` sequence: 414, then 416 and 418 before the
set, 420 in ACQUIRE, and 422 at 2.015-3.016 s after the first LOCKED read. The ring then held for 428 s.
The data is recorded for #645, and the lane did not post on #645 (stated at
`629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1589-1593`). See F3 for the attribution of the pre-set slips.

**B-CRF repeated** (`summary/crfll/{lockloss,grade}.json`). All 797 polls read LOCKED with trim -6.0625 to
-5.9375; set to LOCKED was 2.663-3.169 s. Counted ratio: 0 non-capture steps in 19,261,920 frames.
Every one of the nine capture-path clusters passes the rise-vs-loss rule. The timed ratio is -4.67 +-24.96 ppm:
the halves are +0.01 and -45.35, distorted by the stalls, as the page says. 391 of 401 blocks sit at the floor.
The figure for lost time is wrong (F1).

**Item 3, CRF lock loss.** The stream was unbound for 11.041 s:

- HOLDOVER within 0.054-0.555 s, with the trim at -6.0 at all 19 polls.
- GET_CLOCK_SOURCE read 1 at all six reads.
- The CRF sink relocked by 0.143 s after the rebind; ACQUIRE at 0.143-0.643 s; LOCKED at 2.66-3.162 s.
- DUT STREAM_OUTPUT 0 MEDIA_RESET went 1, 2, 2, and the peer received the same. That is one toggle at the
  loss and none at the return, as declared under IEEE 1722-2016 4.4.4.3 in the design's `mr` section.
- CLOCK_DOMAIN went 10/9, 10/10, 11/10 (C1). STREAM_INPUT 1 MEDIA_UNLOCKED went 0, then 1 (the bank resets
  at the bind).
- The lock-loss segment (25.77 s) has 0 events and 0 steps, and its largest read gap is 16.9 ms.

**Item 4, saved selection** (`summary/pc/pc.json`, `runs/pc-cycle-lock.txt`, `runs/pc/boot-console.txt`):

- CLOCK_SOURCE 2 was set and read back, and committed: image seq 31, 31 commits.
- One power cycle, under the lock: CYCLE_BEGIN appears once in the packet. The boot verdict passed at the
  first grader run.
- The firmware took NVM slot A seq 31 with nothing rolled back. GET_CLOCK_SOURCE read 2 at the first command.
- Since the boot: CLOCK_DOMAIN 1/0, and the servo LOCKED at the first poll with no command.
- The restore read back 0. The identity gate after the boot is byte-equal to the start's
  (`ff817aca...` for all three verdicts).

**Item 1, STOP evidence** (`summary/proof/proof.json`, `runs/proof/*`). Channels 0-3 read -141.1 to
-141.5 dBFS with a -2..+1 LSB range, and 0.03-0.04 % of their power within 5 Hz of either tone. Unmapped
channels 4-7 are exactly zero. The verdict is TONE ABSENT. Between the reads 12.61 s apart, STREAM_INPUT 0
read MEDIA_LOCKED 1 and MEDIA_UNLOCKED 0, and FRAMES_RX rose by 103,998.

The mapped-vs-unmapped contrast shows that the DUT's render path was live on this image. So "the stream
carried no tone" is supported, and the page does not speculate about where the tone was lost (lines 1385-1390).
The tone stop is recorded (`runs/tone-stop.txt`).

**Acceptance.** The section 1704-1717 table is consistent with B7's (lines 1128-1148) and with the evidence:
Direction B's THD+N is NOT met, and INTERNAL to AAF keeps #645 open. So "Refs #629", not "Closes", in the
PR body; it is correct.

**Shorter windows and stalls.** Both are disclosed: the method (lines 1441-1442), the CRF window paragraph
(1605-1610), the limits (1728-1731), the PR body and REVIEW READY. Neither changes a verdict. The switch
criteria are counts and lock times, and a 120 to 150 s hold covers B7's 15 to 45 s post-lock slip interval.
The B-CRF criteria are length-independent and pass on the counted ratio. The 18.7 s hidden by the stalls could
hide at most a listener event inside them, which the page states (lines 1609-1610).

**Binding rule** (receipts/binding-rule.txt). Every bind in the proof, SW, CRFLL and PC runs is preceded
by an ok format check. A format was set only on the listener, and only to the talker's format. Every clock
set was on the DUT, answered SUCCESS and read back. Every restore read back as found. 0 violations.

**Privacy** (receipts/privacy-scrub.txt, receipts/privacy-capture-channel-count.txt). The repository's
identity and local-info scrub finds nothing in the page, the PR body or the packet's 252 files. The
SoC-side TDM format on the page and in the logs is already public (`docs/findings/451_TDM8_FIRST_LIGHT.md:175`).
One packet file states the external capture's channel count: F4.

**Gates** (receipts/gates.txt and gate-*.log, pinned Markdown environment at this head). All 11 commands
are rc 0: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `gen_toc.py --verify-anchors`,
`check_em_dash.py --base 40714c1b` and `--selftest`, `check_doc_paths.py`, `check_feature_status.py --self-test`,
`ci_scope.py --selftest`, `check_baremetal_only.py --check`, and `git diff --check`.

## Findings

**F1 - MINOR - Docs, Tests**
- Location: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1605-1607` and `:1730`; PR body row
  "B-CRF repeated"; REVIEW READY "Open risks" (the same figure).
- Title: the CRF window's lost time, "19.0 s", has no basis in the evidence.
- Authority/evidence: AGENTS.md section 6 Docs (claims must match their evidence); Tests (the bench record
  of a graded window).
  - `runs/crfll/events.jsonl`: window-start to window-end is 420.026 s of wall time; 401.29 s were captured.
  - `summary/crfll/lockloss.json`: capture-lost frames 899,009 = 18.73 s over the nine clusters; the three
    stall clusters lost 18.69 s; the three read gaps sum to 18.26 s.
  - No file in the packet derives 19.0 s. The page's own 401.3 + 19.0 = 420.3 does not close on its 420 s.
  - The "271 to 286 s into the window" are captured-audio positions (270.9, 284.1 and 285.5 s). In wall
    time the third stall begins near 295 s, and the page does not say which basis it uses.
- Impact: a measured figure in the graded window's record is misstated on the page and in the PR body. The
  verdict is unchanged.
- Required outcome: the lost time states the evidence's value and its basis (18.7 s), or the derivation of
  19.0 s is published. The stall positions name their time basis.
- Verification: rerun `scripts/rederive_b8.py` on the packet; the page figure equals the "wall-captured" or
  "capture-lost frames" line.

**F2 - MINOR - Docs**
- Location: `629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1306-1308` and `:1761-1770`; PR body "Evidence".
- Title: the B8 section never says where its packet is published, and the PR body says "The packet is not
  yet published".
- Authority/evidence: AGENTS.md section 6 Docs ("enough evidence for another cold reviewer") and section 2
  (reconstructable from GitHub and the repository).
  - The B6 and B7 sections each pin a branch and commit and map the label to a path (lines 625-633 and
    1213-1218). B7 added this in answer to its round-1 findings.
  - B8 names only the label `629-b8-a521`. The packet now exists on `629-b8-review-evidence` at `5bad6a43`.
  - That publication added path redaction to 8 files, recorded only in its MANIFEST.json.
- Impact: a cold reader cannot locate or verify the 33 hashed evidence rows from the page. The PR body's
  statement is now false.
- Required outcome: the section states the branch, the pinned commit, the label-to-path mapping
  (`review-evidence/629-b8-r1/author/`) and where the original vs published hashes live. The PR body's
  evidence paragraph matches.
- Verification: open the named commit and path; `scripts/verify_packet.py` reports 0 bad.

**F3 - MINOR - Robustness, Docs**
- Location: `629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1578-1581`.
- Title: the two slips before the set are attributed to the 5.92 ppm INTERNAL offset, but that offset cannot
  produce them that close together.
- Authority/evidence: `summary/sw/switches.json` `from_binds` and the aaf1 changes.
  - `SLIP_LB` read 414 at the binds, 416 by 1.107 s and 418 by 1.939 s after the binds ended.
  - Two slipped frames came within 1.94 s of the bind, at most 1.33 s apart.
  - At 5.92 ppm one frame slips every 1 / (48,000 x 5.92e-6) = 3.52 s, so drift gives at most one slip in
    that span. No skips were counted, which rules out dither.
  - REGISTER_MAP.md's reading (lines 1999-2003) is a rate row ("climbing"), not an explanation for a burst
    right after priming.
- Impact: the data handed to #645, an open ring-slip defect, carries a cause the numbers contradict. It could
  steer #645 away from a start-up or priming mechanism.
- Required outcome: the page does not assert a cause the data excludes. Either state the two slips, their
  interval and the 3.5 s drift period as recorded but not analysed, or support the attribution with evidence.
- Verification: the sentence at 1578-1581 matches `from_binds`; a reviewer re-derives the interval from
  switches.json.

**F4 - MINOR - Docs (privacy)**
- Location: published packet `review-evidence/629-b8-r1/author/tools/grade_b8.py:39` (SHA-256 `330c14cd...`,
  the page row at `629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1794`).
- Title: the published evidence states the external capture's channel count.
- Authority/evidence: the assignment's privacy rule (no capture channel count in the evidence) and
  CONTRIBUTING.md section 6.
  - Line 39 reads "which of the <N> capture channels carry the tone", with a literal number; it is masked
    in this report.
  - The same tool moves the count to the private environment (`CAP_NCH`, lines 12 and 94), and
    `RAW-ARTIFACTS.json` withholds sizes "because it would state the capture's layout".
  - B7's packet masked the same docstring line as `<capture-channels>` (receipts/privacy-capture-channel-count.txt).
- Impact: a private instrument property is published in this lane's evidence. That is a privacy rule
  breach, not wording.
- Required outcome: the retained `grade_b8.py` masks the count. `redaction.json` records its original and
  retained hashes, the page row at line 1794 carries the retained hash, and the packet is republished.
- Verification: scan the republished packet for the count's literal in tool text; the page's hash row
  verifies against the republished file.

**Suggestions** (they affect no lens):
- **S1:** line 1656 says "nothing dirty or in flight". `runs/pc/nvm-pre-pre-saved-0.txt` reads `pend=1`
  (`nvm_pend`, accepted work no slot holds; `docs/design/SAVED_STATE_FASTCONNECT.md:1067`). It reads 1 in
  every steady state of this run, and the post-boot readback of 2 settles item 4. Record the bit so the row
  does not read as complete durability.
- **S2:** lines 1374-1383 could state why the idle floor indicts the peer's talker rather than the DUT's
  render path: mapped channels 0-3 carry a nonzero few-LSB floor while unmapped 4-7 are exactly zero.
- **S3:** B7's limit "`mr` toggles counted at both ends (GET_COUNTERS), not captured on the wire"
  (line 1157) applies equally to B8 and is absent from lines 1719-1735.

**Prior public review findings on PR #646.** None existed before this round. At my independent pass the PR
carried only the two review-start notices (5971548315, 5971548837) and no review objects. B7's round-1 and
round-2 findings belong to PR #644 and are outside this diff.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Page lines 1267-1806 against the B8 assignment (issue comment 5970760794), the STOP ruling (5970994127), the issue's acceptance list and `MEDIA_CLOCK_FOLLOWING.md` Switching sources, Lock loss, `mr`, CLOCK_DOMAIN LOCKED/UNLOCKED (C1) and Bench rows. Re-derived from `summary/{sw,crfll,pc,proof}`, `runs/*/events.jsonl` and `runs/pc-cycle-lock.txt` (receipts/rederive-b8.txt, binding-rule.txt, counters-decode.txt). Acceptance table 1704-1717 against B7's 1128-1148; "Refs #629" | R455-1 | 4fb5125a2e43997384839deeb1fe4742a5b2dca8 |
| RTL | CLEAN | No RTL in the diff (`git diff --stat 40714c1b..4fb5125a`: two Markdown files). The page's RTL claims checked against `hdl/ieee1722/aaf/KL_render_setpoint.sv:584-617` (recentre and converged) and `docs/reference/REGISTER_MAP.md:1867-2003` (`SLIP_LB` unit and readings, 2 dups per frame for a 2-pair stream); TIME_SYNC.md:385 (settle bound) | R455-1 | 4fb5125a2e43997384839deeb1fe4742a5b2dca8 |
| Robustness | UNCLEAN (F3) | INTERNAL-to-AAF and pre-set ring behaviour (`switches.json` `from_binds`); capture stalls and lost frames (`lockloss.json` clusters, read gaps); lock-loss holdover, rebind and restore; power cycle and boot; restore read-backs and census (`restore/census-compare-r2.txt`) | R455-1 | 4fb5125a2e43997384839deeb1fe4742a5b2dca8 |
| Tests | UNCLEAN (F1) | Tool controls (`controls/controls.json` byte-equal to B6/B7, `7bbefc71...`); the `grade_b7.py` to `grade_b8.py` diff (input plumbing only; the detector `b6_thdn.py` is unchanged, `d4673f55...`); `b8_proof.py` logic; independent counter decode with a planted negative control; capture-loss arithmetic | R455-1 | 4fb5125a2e43997384839deeb1fe4742a5b2dca8 |
| Docs | UNCLEAN (F1, F2, F3, F4) | Page section, introduction and Contents; `docs/findings/README.md` row; PR body; the packet's MANIFEST.json, redaction.json, RAW-ARTIFACTS.json and the 33 hashed rows (receipts/packet-verify.txt); privacy scrub of page, PR body and packet; 11 docs gates rc 0 (receipts/gates.txt) | R455-1 | 4fb5125a2e43997384839deeb1fe4742a5b2dca8 |

## Real limits

- No bench access. Every verdict is re-derived from the reduced summaries, the event logs and the logs the
  packet publishes.
- The raw files (`cap-*.raw`, `poll-run.jsonl`, `grade-full.json`) are not published. So the tone grading and
  the per-poll decode were not re-run from raw; their hashes are recorded only. F1 could have a basis in an
  unpublished file, but none is cited.
- IEEE 1722-2016 4.4.4.3 and the Milan clauses were not re-read from the standards. Conformance is judged
  against the merged design's clause findings and its declarations.
- Physical calibration NOT RUN; printed precision is not calibrated accuracy. Field and hosted skips are not
  hardware proof.
- Hosted contexts at the exact head, when queried (receipts/hosted-checks.txt):
  - SUCCESS: rtl-fast, bdd-conformance, changes, full-ci-gate, elaborate, docs-check-no-git and
    wire-accountability.
  - docs-check: in progress.
  - SKIPPED, not executed: verilator-suites, yosys-portability, Verilator and Yosys shards, verilator-lint,
    yosys-elaboration and Physical gPTP.
- After the probes the clone was restored to the head: 0 untracked, ignored or modified entries, index tree
  equal to `4d4dc37d...`, and the submodule gitlinks and checkouts clean (receipts/clone-integrity.txt).

## Pending manager duties

- Publish this round. Carry F1 to F4 to the lane and re-review the corrected head.
- After F4 is fixed, republish the B8 packet with `grade_b8.py` masked and re-pin it on the page (F2).
- The B7 packet (`629-b7-review-evidence` at `c6ad37e7`, `tools/grade_b7.py:101` and `:104`) states the same
  channel count as a literal. It predates this PR and is outside this diff, so it needs its own redaction or
  issue.
- Post, or have posted, the INTERNAL-to-AAF data pointer on #645. The lane did not post there.
- Hosted acceptance at the exact head: docs-check was in progress, and the long gates were skipped by scope.
- The final current-dev candidate build and merge validation against live dev
  `546437243e87eb5a78783a9e3cd5d1badcc3423e`.

R455-1 FINISHED
