[R264] NEGATIVE - exact head 0abf147f726721f4a323ee6a32095a02363fe2dc

Round R264-1, internal independent review of issue #117 / PR #531 in a cleared context.

- Head `0abf147f726721f4a323ee6a32095a02363fe2dc`, tree `512ce39d485d9af8a8b3d411d6395c511d223135`.
- Two commits on source base `ede8d48ecd7c7f589a14b957951f040d92c99c70`, which is an ancestor. Both commit messages are one line with no trailers.
- Diff: `docs/design/GM_LOSS_RECOVERY.md` (M), `docs/findings/117_GPTP_SILICON_EVIDENCE.md` (A) and `docs/findings/README.md` (M). No HDL, firmware, pin or gitlink change.
- Evidence archive: branch `117-review-evidence`, commit `160debeba11231e2fd38fde26c01c467039603ba`, path `review-evidence/117-r1`.

## Verdict in one paragraph

The bench evidence is strong. Every PASS row I tested re-derives from the raw captures, console transcripts and controller logs in the published archive. That covers the identity gate, the step 2 cadence and turnaround, the step 3 table (every column within 6 ms of my own clock mapping; recovery 0.43 to 1.60 s against the 5 s bound), both halves of step 4, and the step 5 parity and FAIL. The FAIL and NOT RUN rows are honest.

The head still cannot merge. The new findings page trips the repository-wide bare-metal-only gate: REQ-VER-04 requires that gate green, and the required `docs-check` context fails on it at this exact head (F1, BLOCKER). Three MINOR documentation defects are also open:

- observations the page says need issues have none (F2);
- four descriptive statements disagree with the raw artifacts (F3);
- the raw-artifact locator and some tool hashes cannot be traced from the page (F4).

## Reconstruction order and authorities read

- AGENTS.md, then CONTRIBUTING.md (sections 2.1, 2.2, 3 and 6, including the dev merge bar's seven contexts and the em-dash rule), then docs/README.md.
- Issue #117: body, frozen acceptance, and the scope decisions:
  - 2026-09-06 one-DUT decision (comment 5561827955), applied 2026-09-07 (5565246390);
  - 2026-09-15 audio deferral (body preface, 5674663121);
  - 2026-09-23 owner decisions 5789767491, 5794146393 and 5795898094;
  - build and flash records 5794859125 and 5794950660;
  - bench operator evidence 5794274143, 5795658105 and 5796668867.
- Requirements: REQUIREMENTS.md REQ-PTP-07, REQ-PTP-08, REQ-VER-04 and REQ-VER-05.
- Interface and reference docs:
  - docs/reference/REGISTER_MAP.md rows 0x624/0x628, 0x62C, 0x644, 0x6E4, 0x6F4, 0x720, 0x730/0x734, 0x750, 0x764, 0x774, 0x77C, 0x780, 0x7E4, 0x7E8, 0x7EC and 0x7F0;
  - docs/reference/MILAN_COMPLIANCE_MATRIX.md rows 4.2.6.1.1, 4.2.6.2.2 and 4.2.6.2.6;
  - docs/testing/TESTING.md section 6c (the counters-probe parity bar);
  - docs/integration/BUILDING.md 4.1 and docs/testing/RUNNING_TESTS.md (the one-DUT topology);
  - docs/findings/README.md (the rule for new findings).
- The diff, then commit history.
- Evidence:
  - the archive (both packets and MANIFEST.json);
  - the issue #358 record of 2026-09-20 (comment 5751909357);
  - issues #529 and #530;
  - exact-head hosted check runs.
- Prior public review findings on PR #531: there are none. The PR carries only two review-start comments and no review or review comment. The reviewer rounds on the issue thread (R155 to R158) reviewed the separate read-only peer reader archives, not this diff, so none is carried here.

## Findings

### F1 - BLOCKER - Conformance, Tests, Docs

`[R264] BLOCKER Conformance, Tests, Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:125, :149, :401 - the new page fails the repository-wide bare-metal-only gate, so the required docs-check context is red at the exact head`

- **Requirement/evidence:**
  - REQUIREMENTS.md REQ-VER-04: the repository-wide bare-metal-only gate must be green with zero policy findings.
  - CONTRIBUTING.md section 2.1 (lines 55-58) lists `docs-check` among the seven required contexts.
  - `python3 scripts/check_baremetal_only.py --check` at this head reports `FAIL (3 finding(s))` on three page lines:
    - line 125, deny-listed term `kernel`, in "0 kernel drops";
    - line 149, `host capture`, in "controller-host capture and watcher";
    - line 401, `software gPTP owner`, in "No software gPTP owner exists on the image".
  - At base `ede8d48e` the same gate reports `OK (0 findings)`. At c3eb95fa it reports 2 findings.
  - Hosted `docs-check` concluded `failure` at both c3eb95fa and 0abf147f. At 0abf147f, job 107227198488 failed at step 21 "Bare-metal scope gate", and steps 22 to 45 were skipped: the builder gates, doc cited-path gate, per-page contents gate, hygiene and idiom ratchets, and others.
  - The recorded validation (`bench-a200/gates-c3eb95fa.txt`, `bench-a202/gates-0abf147f.txt`, and both REVIEW READY comments) lists only four docs gates and omits this one.
- **Impact:**
  - A required merge context is failing, and a normative requirement is violated by the change.
  - Twenty-four later docs-check steps have no hosted result at this head.
  - The claim that validation passed is incomplete.
- **Required change:**
  - The page's wording passes `check_baremetal_only.py --check` with zero findings; the gate has no allowance to add.
  - The recorded validation includes that gate.
  - The complete hosted `docs-check` job succeeds at the new head.
  - The disposable probe `receipts/gates/probe_reworded.diff` shows that rewording only those three lines yields `OK (0 findings)`. It demonstrates feasibility and is not prescribed wording.
- **Verification:**
  - `python3 scripts/check_baremetal_only.py --check` exits 0 at the new head.
  - Hosted `docs-check` shows every step executed and successful.
  - The four existing docs gates stay green.

### F2 - MINOR - Docs

`[R264] MINOR Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:448-449, :458-461; PR #531 body - observations the page says need their own issue have none, and the PR states they are filed`

- **Requirement/evidence:**
  - AGENTS.md section 4: newly discovered work becomes a public Issue.
  - The page says "Items 1 to 6 each need their own issue" and "Items 8 to 10 concern the DUT and each need their own issue".
  - The PR body says "Observations outside the boxes are filed as #529 and #530."
  - Actual tracking (`receipts/observation-tracking.txt`):
    - #530 carries items 1 to 3, and its lane cites item 9;
    - #529 is the step 5 Milan downgrade, which is not an observation item;
    - items 4, 5, 6, 8 and 10 have no issue; items 8 and 10 are DUT observations (LINK_UP/LINK_DOWN counters not moving over seven outages; no self-identity ADPDU).
  - The observation list links neither issue.
  - Items 5 and 6 (bench-switch facts) and item 4 ("the documented design") are classed as needing issues, unlike the bench facts 7, 11 and 12.
- **Impact:** once merged, DUT observations 8 and 10 have no owner, and the PR record misstates the tracking.
- **Required change:**
  - Every observation the page says needs an issue has a public issue, linked from its item.
  - Otherwise the page says the item needs none, and why.
  - The PR text matches.
- **Verification:** each item 1 to 12 either links an open or closed issue or states that no issue is needed.

### F3 - MINOR - Docs

`[R264] MINOR Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:305, :320, :47, :375, :125 - four descriptive statements disagree with the raw artifacts`

Requirement/evidence: brief and CONTRIBUTING section 3: no claim beyond what was measured. Details and counts are in `receipts/step3-text-discrepancies.txt`.

| Item | Page line | Page says | Raw artifacts show |
|---|---|---|---|
| A | 320 | "nothing in either direction from 1.03 to 1.71 s" | In cycle 2 the tap recorded a DUT Pdelay_Req at 1.75 s (1.748 to 1.753 s under two independent clock fits), so the range is 1.03 to 1.75 s. |
| B | 305 | holdover (CLKV_STAT bit 3) "for 0.3 s" at the sync loss | The console shows spans of 0.30, 0.30, 0.50, 0.31, 0.41 and 0.41 s. The packet's own cycle analyses agree. |
| C | 47 and 375 | "no operator action reached the DUT beyond read-only AECP queries"; "The DUT received read-only AECP queries only" | The page's own methodology also polls the DUT console every 0.1 s: all 38,954 console commands in 15 transcripts are reads (`receipts/console-command-census.txt`). Cycles 4 to 6 bind and unbind the listener around each outage. The automatic-recovery conclusion stands. |
| D | 125 | envelope-less records "76 in Run A, none elsewhere" | The step 3 captures exclude 38, 0, 38, 45, 0 and 37, and the step 3 final capture 18. The packet's analyses agree. |

- **Impact:** the durable record carries numbers the artifacts contradict. No acceptance result changes.
- **Required change:** each of the four statements matches the artifacts.
- **Verification:** re-derive with `r264_step3.py`, `r264_step3_console.py` and `r264_console.py` against the corrected text.

### F4 - MINOR - Conformance, Docs

`[R264] MINOR Conformance, Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:32, :58, :120, :200-201, :209-210, :503-505, :80, :82 - box 5 PASS relies on raw artifacts and hashes a cold reader cannot trace from the page`

- **Requirement/evidence:**
  - Issue #117 acceptance box 5: findings include raw artifacts, exact hashes and tool revisions.
  - The page says the raw artifacts are in "two private bench packets" and gives no locator.
  - The packets are in fact published on branch `117-review-evidence` at `160debeb`. Every one of the 74 quoted full hashes that name archive files matches a published file (`receipts/packet-integrity.txt`). A committed page can link such an archive; docs/testing/ASSERTIONS.md:153 already links a pinned review-evidence tree.
  - Line 120 says the peer firmware string "stays in the private packet", but the published `bench-a200/bench/peer-aem-1.jsonl` carries the raw ENTITY descriptor bytes. I re-derived the quoted field hash from them (`receipts/hash-corroboration.txt`).
  - Lines 209-210 say "Full hashes are in the packet manifests". That is not true for:
    - the la_avdecc libraries `95d64fd5...` and `8ef4b008...`, the probe `ad579e18...` and its source `0e9faf30...`: three of these have full hashes only on the issue's 2026-09-08 comments, and `8ef4b008...` has none anywhere public;
    - `bios.bin` and `csr.csv`, whose hashes (lines 80 and 82) have no public corroboration.
- **Impact:**
  - After merge, box 5's PASS cannot be checked from the page.
  - The page's privacy statements disagree with what has been published.
- **Required change:**
  - The page names a pinned public locator for the raw artifacts, or says precisely which remain private.
  - Its privacy statements match what is published.
  - Every abbreviated tool hash has a public full value, or the "full hashes" sentence is narrowed.
- **Verification:**
  - Follow the locator.
  - `r264_packet_check.py` maps every quoted hash.
  - The narrowed sentence is true.

### F5 - SUGGESTION - Conformance, Docs

`[R264] SUGGESTION Conformance, Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:42, :182-188, :219-222, :233, :400 - cite the limits and records the PASS rows use`

Suggested citations:

- the clause behind the "within 30 %" interval check (matrix row 4.2.6.2.2 exists);
- row 4.2.6.1.1 for the 800 ns bound;
- the 2026-09-20 record (issue #358 comment 5751909357, which does carry 391 and 392 ns);
- the firmware lines showing that the publication words are only read (`sw/firmware/milan_baremetal/milan_baremetal.c:1472-1479`, with no `milan_write` to them).

The claim that the turnaround script is "unchanged from the 2026-09-20 record" cannot be checked publicly: that record does not publish the script hash. Optional.

### F6 - SUGGESTION - Conformance, Docs

`[R264] SUGGESTION Conformance, Docs - docs/design/GM_LOSS_RECOVERY.md:96; docs/findings/README.md:11 - mark the lane's reading of "the grandmaster's return", and give the index row's full state`

- The owner fixed the bound as 5 s "from the grandmaster's return" (comment 5795898094). The row "its first Announce or Sync on the link" is the lane's operational reading, presented under "The owner fixed this bound".
- A power-on reading would give 19.18 to 20.32 s, which the page honestly reports at line 300. The first-frame reading gives 1.82 to 2.60 s, still inside the bound.
- The findings index row's state names only the PASS and omits the step 5 FAIL and the NOT RUN rows. Optional.

## Per-lens results (every lens applied at 0abf147f)

`[R264] PASS RTL - git diff --raw ede8d48e..0abf147f; REGISTER_MAP.md:731, :770, :875, :880, :942-944, :1347, :1363-1364, :1392; sw/firmware/milan_baremetal/milan_baremetal.c:1472-1479 - docs-only diff with gitlinks identical to base; the page's register-level readings checked against the register map and matched against the decoded console words`

The readings checked:

- CLKV_STAT `0x00010002` bit layout;
- ASP_CMD `0x11`;
- GPTP_LAT `0x029000DB` = 656/219 ns;
- CRFT_COUNT `0x850D` = 34,061;
- CRFT_CTRL `0x3002E3`;
- LINKG_STAT `0x83`/`0x03` against the 2^27-cycle activity window.

The firmware reads the publication words and never writes them.

`[R264] PASS Robustness - archive 160debeb bench-a202/bench/attempt1-aborted/*, cycle1-6/*, all tcpdump logs; receipts/step3-cycles*.jsonl - failure and fault paths of the method checked`

- The aborted attempt is excluded, recorded, and its records match the page.
- The guard and pre-flight fix are shown.
- Recovery is insensitive to the clock mapping: two independent fits give 0.43 to 1.60 s, versus the page's 0.43 to 1.60 s, with more than 3 s margin to the bound.
- The announce-phase split (0.43 to 0.52 s against 1.46 to 1.60 s) is explained by the raw data. The first Announce is ignored when it arrives before asCapable, and the next is accepted 1.007 s later.
- Bound and unbound cycles are both exercised.
- Every capture reports 0 kernel drops.
- Envelope-less host records are classified as IPv4/IPv6 host traffic. The count statement is F3-D, filed under Docs.
- The FAIL and NOT RUN rows are honest: reach, the peer's recovery time, Hive, behave, latency and audio.

Conformance is covered and UNCLEAN (F1, F4). It was judged against the frozen acceptance and the owner decisions:

- **Identity gate: CONFIRMED.**
  - On-board ROM `f6afa4ec`, QSPI `02036e95` and AEM `93742dd2` equal the `asl` row of `expected-crc.txt`, which is byte-identical in both packets.
  - They exclude seeds `eppo` and `eto` and the replaced `f6b31625` image.
  - VERSION `00020060`; grader 10/10 at all four runs; dev tree `ff9950bc`.
  - The grader hash `bc41ab03...` equals `git show ede8d48e:scripts/baremetal_uart_smoke.py`.
  - The running configuration was not read back, as the page states.
- **Box 1: CONFIRMED.**
  - asCapable retained in 116/116 console samples and 60/60 GET_AVB_INFO polls.
  - Peer delay 380 to 391 ns.
  - Intervals: 4,556 Sync, 565 Announce, 564 and 566 Pdelay_Req, none outside 30 %. The DUT's Pdelay_Req interval is 1000.002 ms every time.
  - Turnaround 10,984 to 11,009 ns over 568/568 exchanges; 570/570 exchanges in the other direction, including 18.33 and 18.36 ms.
  - The DUT sends only Pdelay messages.
  - The asCapable partner being the bench switch is consistent with the documented one-DUT topology through the bench AVB switch (BUILDING.md 4.1, owner decisions of 2026-09-06 and 2026-09-23). The page publishes that interpretation and keeps "reaches" NOT RUN.
- **Box 2: CONFIRMED.**
  - All ten columns of the six-cycle table re-derive within 6 ms under at least one fit.
  - The loss-declaration offsets re-derive: 0.40 to 0.46 s, 3.01 to 3.08 s and 5.0 to 5.1 s.
  - The PHC steps equal the on-to-on intervals within 0.04 s.
  - TUCNT rose by 40, 39, 41, 40, 40 and 41.
  - GPTP_GM_CHANGED rose by 2 per cycle on both entities.
  - Stream: first `tu=1` PDUs at 1.08, 1.07 and 1.00 s; post-return first PDUs at 41.28, 42.96 and 41.46 s, all `tu=0`; listener MEDIA_LOCKED at the stated polls.
  - Peer table and attempt 1: confirmed.
- **Box 3: CONFIRMED.**
  - Steady-state words agree with the wire and with AECP.
  - Run B: 34,061 CRF PDUs, all `tu=0`, continuous sequence numbers, PCP 3 / VID 2, bursts of 19.67, 18.45, 15.00 and 15.00 s.
  - Every transition edge falls within one console sample of its wire cause.
- **Box 4: CONFIRMED.**
  - The two counters-probe transcripts are identical line for line: CLEAN, rc 0, 0 complaints.
  - The enumeration log shows the Milan-to-IEEE 1722.1 downgrade over "5.3.8.10", enumeration in 164 ms, and 0 retries or timeouts.
  - The NOT RUN rows are honest.
- **Box 5:** overstated in part (F4).

Tests is covered and UNCLEAN (F1). For a findings PR this lens is the validation evidence:

- The recorded gate set omits a required gate that is red.
- Locally at this head, the four recorded docs gates, `gen_toc.py --verify-anchors` and seven further docs-workflow gates pass (`receipts/gates/`).
- Every numeric claim I sampled has a re-derivation that could fail, and each is recorded in `receipts/`.

Docs is covered and UNCLEAN (F1 to F4). Also checked:

- the em-dash rule (0 findings over 630 added lines);
- the GM_LOSS_RECOVERY derivation, which matches the owner's text (3 × 1 s + 3 × 125 ms + margin);
- the Contents separator switch, which the em-dash rule prescribes;
- the index row;
- privacy: roles only, no host names.

## Reviewer ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 BLOCKER, F4 MINOR) | #117 acceptance and decisions; REQUIREMENTS REQ-PTP-07/08, REQ-VER-04/05; the page's box table against archive 160debeb (identity, runA/B/C/final, cycle1-6, attempt1); compliance matrix rows | R264-1 | 0abf147f726721f4a323ee6a32095a02363fe2dc |
| RTL | CLEAN | diff --raw (docs only; gitlinks equal base); REGISTER_MAP rows cited above; firmware milan_baremetal.c:1472-1479 | R264-1 | 0abf147f726721f4a323ee6a32095a02363fe2dc |
| Robustness | CLEAN | attempt1-aborted, cycle1-6, tcpdump logs, two clock fits, NOT RUN/FAIL rows | R264-1 | 0abf147f726721f4a323ee6a32095a02363fe2dc |
| Tests | UNCLEAN (F1 BLOCKER) | recorded gate transcripts in both packets; local gates and hosted check runs at c3eb95fa and 0abf147f; reviewer re-derivations | R264-1 | 0abf147f726721f4a323ee6a32095a02363fe2dc |
| Docs | UNCLEAN (F1 BLOCKER; F2, F3, F4 MINOR) | 117_GPTP_SILICON_EVIDENCE.md, GM_LOSS_RECOVERY.md, findings/README.md, PR body, issues #529/#530 | R264-1 | 0abf147f726721f4a323ee6a32095a02363fe2dc |

F5 and F6 are SUGGESTIONs and do not affect coverage. Any later commit that touches the page or the design doc un-covers Conformance, Tests and Docs, and they must be covered again at that head.

## Real limits

- I read only the published archive. The 11 path-redacted files differ from their originals only as MANIFEST.json declares, and I did not see the originals.
- The build directories are not public. The `.bit`, payload and AEM hashes are corroborated by the CRC table and the build record. The `bios.bin` and `csr.csv` hashes are not corroborated (F4).
- Timing re-derivations rest on the recorded host-offset brackets and power-strip log times. The tap-to-host mapping is my own lower-envelope fit, in two variants.
- The peer's own recovery time, the reach transition, Hive, behave, latency and audio are NOT RUN, as the page states. Physical calibration is NOT RUN. No field skip or hosted skip is hardware proof.
- Two local gates, `check_hygiene.py --check` and `check_todo_ownership.py`, refused to run because the submodules are not initialized in this clone. I did not run them, and they count as no evidence.
- No bank, builder, Verilator, Yosys, act or hardware step was run.
- The clone was restored and verified afterwards:
  - all 865 tracked files are byte-exact with their modes;
  - the index equals the HEAD tree;
  - the 4 gitlinks are at their pins and uninitialized, as found;
  - the porcelain status, ignored files included, is empty.

## Pending manager duties

- Reconcile the review-start statement that the source static banks passed with the failing `check_baremetal_only.py --check` and hosted `docs-check` at this head. I found no public bank transcript.
- After the fix, obtain exact-head hosted `docs-check` with every step executed, plus the other required contexts, and run act and the candidate merge against live dev `07d85dac` at the merge turn.
- Decide whether the public archive at `160debeb` meets CONTRIBUTING section 6. Some files carry raw peer descriptor bytes, bench host names and capture interface names. This is outside this PR's diff.
- File or decline, publicly, the observation issues in F2.
- Obtain the second, external review. This round is the internal one.

## Receipts (listed in MANIFEST.sha256)

Scripts:

- `r264_wire.py`: tap decoder;
- `r264_console.py`: console parser;
- `r264_step3.py`: cycle re-derivation, with `--robust`;
- `r264_watch.py`: controller log decoder;
- `r264_step3_console.py`: console-only step 3 checks;
- `r264_compare_step3.py`: page against reviewer;
- `r264_packet_check.py`: archive integrity;
- `r264_run_all.sh`: regenerates the receipts. A rerun reproduced every generated receipt byte for byte.

Receipts: `receipts/*.json*`, `receipts/*.txt`, `receipts/gates/*` (gate transcripts at head, base and c3eb95fa, plus the reworded-line probe and its diff), and `receipts/hosted-*` (exact-head check runs and docs-check job steps).

R264-1 FINISHED
