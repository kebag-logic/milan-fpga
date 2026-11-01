[R758] NEGATIVE - exact head 69fd18f1d8f9d428687c07ede0f9c14597cf2d61

Round R758-3: external independent review of PR #828 (issue #640, with #665 and #823), round-3 delta.
- Head `69fd18f1d8f9d428687c07ede0f9c14597cf2d61`, tree `f7c3f02d8889081b89c7dcb46004d3ffb88623e2`.
- Previous head `f6b3e841646384177584ce75b657fb8dead7727c`.
- Source base `e5b8405db4c1f7cbdafb5df92b15b580142e0232`; live dev `1f29f189279f9fc0132f4918e47342b87d22f33a`.
- Delta: eight one-line commits with no trailers, four Markdown pages, 317 lines added and 85 removed. It
  changes no code, generator, gate, configuration or gitlink.

**Verdict basis.** All six R758-2 findings and the R758-2 residue are closed at their cause. So are the three
R757-2 findings and their two residue items. Round 3 adds three MINOR defects, so the verdict is NEGATIVE and
all five lenses are UNCLEAN:
- two in the new listener-merge rules;
- one in the new compaction save-landing table.

Each is shown on the author's own host model by a short probe. None changes a stated latency, load or save
figure. The 2026-10-31 owner decisions are out of review.

## Findings

### R758-3-F1 MINOR - Robustness, RTL, Tests, Docs - docs/design/MARK_II_STREAM_ENGINES.md:618, :628-631, :654-660, :1109 - tu on both networks drops audio for up to a presentation offset

- **Authority/evidence:**
  - Rule 2 (SE:618) discards a copy with tu set while "the partner holds clean data", that is while the
    partner's `LCTX_CLEAN_PT` is still ahead of the render point. It does not ask whether the partner will
    deliver a clean copy of this packet.
  - Say both networks set tu within one presentation offset of each other. Each context's tu copies are then
    discarded because of the other context's old clean data. That data covers earlier packets, not these ones.
  - The packets between the last clean copy and the first tu copy accepted after both `CLEAN_PT` pass are lost
    from both networks. An unpaired stream applies every rule but rule 2 (SE:654), so it would render them.
  - The round-2 text rendered the first copy when both carried tu. Round 3 removed that sentence and does not
    replace it. The page states a gap only for "Loss plus tu on the other network" (SE:657-660).
  - This design runs one firmware `flexptpd` on one core for both ports. So a single daemon restart or loss of
    sync can set tu on both of a talker's ports at once.
- **Probe** (`scripts/probe_merge_both_tu.py`, `receipts/model/probe_merge_both_tu.out`): the published
  `merge_model.py`'s own `run()` and `judge()`, with tu set on both ports.
  - From packet 100 at the model's latencies (secondary 1.1 to 1.5 ms later), 30 samples are missing:
    5 packets, 625 µs.
  - The same happens with ±5 µs skew, and for tu on both from 100 to 600.
  - With both networks at the primary's latency (`probe_merge_both_tu_equal_latency.out`):
    - 84 samples (14 packets, 1.75 ms) are missing when the onsets coincide;
    - 60 samples (1.25 ms) are missing with onsets 0.5 ms apart.
  - Without rule 2 every case loses nothing. A one-network tu control loses nothing.
  - The model's 15 cases and the verification row (SE:1109) contain no case with tu on both networks.
- **Impact:** with both networks up and carrying every packet, a tu onset on both, which one firmware gPTP
  instance can cause, drops up to about 2 ms of audio. A non-redundant stream would not drop it. Redundancy is
  then worse than a single network for this event, and the guarantee "uncertain time on one network cannot
  disturb the other" says nothing about it.
- **Required outcome:**
  - The rules render a packet that only tu copies carry, once no clean copy of that packet can still come. For
    example, rule 2 discards a tu copy only while the partner's clean data is current: its reference is within
    a packet or two of this packet's counted time, not merely ahead of the render point. Any rule that makes
    both-tu render is acceptable.
  - Otherwise the page states the both-tu gap and its bound as a limit, and lists it beside the Annex D.3 text.
  - The verification row and the model add tu on both networks, with simultaneous and offset onsets.
- **Verification:** the model case "tu on both from packet 100" passes with 0 missing samples, or the stated
  gap equals the model's.

### R758-3-F2 MINOR - Robustness, RTL, Tests, Docs - docs/design/MARK_II_STREAM_ENGINES.md:597-601, :620-623, :632 - a tu copy more than 21 packets from the head by count is written outside the render buffer or counted as a duplicate

- **Authority/evidence:**
  - A tu copy is placed by its `sequence_num` count from its context's reference (SE:597-601). That count is
    a signed 8-bit difference, so it reaches ±127 packets.
  - Rule 4 re-anchors "a clean copy while `ANCHOR_TU` is set, or more than 21 packets from the head" (SE:620).
    The published model reads the 21-packet clause as clean-only (`merge_model.py:110`,
    `if not tu and (...)`).
  - Rule 1's late and early checks use the copy's own time, which for a tu copy "names no packet" (SE:594).
    So they do not bound the counted k.
  - The author's handoff derives |k| <= 21 from "late and early checks". That holds for clean copies only.
  - A talker sequence discontinuity while tu is set, for example a stream restart during gPTP recovery, gives
    a counted k beyond 21 while the head is still valid.
- **Probe** (`scripts/probe_merge_tu_seq_jump.py`, `receipts/model/probe_merge_tu_seq_jump.out`), on the
  published model's `Pair`:
  - a jump of +40 writes at `head_pos + 240` samples, against a 128-sample render buffer at 48 kHz;
  - a jump of -40 is "not written; counted as duplicate".
- **Impact:**
  - At +40 the write lands past the buffer span. In a ring it overwrites unrendered samples.
  - At -40 `SE_MERGE_DUP` counts a copy whose packet was never written. That contradicts "its packet is already
    written" (SE:623) and "counts each duplicate once" (SE:632).
- **Required outcome:** the rules state what any copy, clean or tu, does when its k lies outside 0 to -21 or
  beyond the buffer span. Re-anchoring, as rule 4 does for clean copies, is one answer; discarding with its own
  count is another. The model then matches the stated rule.
- **Verification:** a model case with a tu copy whose sequence jumps by ±40 while the head is valid. Nothing is
  written outside the span, and `SE_MERGE_DUP` is unchanged.

### R758-3-F3 MINOR - Robustness, Conformance, Tests, Docs - docs/design/MARK_II_STREAM_ENGINES.md:1038, :1041-1046, :932, :1114; docs/reference/FR_NFR.md:476 (NFR-REL-03) - a header that fails its read-back but is stored intact can win at boot over saves made after it

- **Authority/evidence:**
  - The new save-landing row (SE:1038) says that after "a header that fails its read-back" saves append to
    "the old slot, still active". Compaction then "erases the standby and restarts from step 1".
  - Boot picks the valid header with the higher generation (SE:1022, :1046).
  - A read-back can fail while the stored page is correct, for example from a transient read error. The page
    itself treats read-back failures as possible (SE:932).
  - In that case the standby carries an intact header with a higher generation until its erase reaches that
    page. That erase is 12 s of background work, suspended by every save.
  - Saves acknowledged in the old slot in that interval are lost if power is cut before the erase removes the
    header. The power-cut table (SE:1041-1046) has no row for this interval.
  - NFR-REL-03 (FR:476) requires that compaction "loses no saved change, with or without a power cut".
- **Probe** (`scripts/probe_compaction_header_readback.py`, `receipts/model/probe_compaction_header_readback.out`),
  using the published compaction model's `Flash`, `System` and `boot`:
  - steps 2 to 4 run with the header stored intact, and its read-back is treated as failed;
  - one save is acknowledged in the old slot;
  - boot then uses the new standby and returns the pre-save value: `LOST`.
  - The model never fails a read-back, so its 14,831 runs cannot reach this row.
- **Impact:** one listed landing point can lose a durable save across a power cut. That breaks the
  requirement's no-loss claim in exactly the table that round 3 added to prove it.
- **Required outcome:** after a failed header read-back, no save is acknowledged in the old slot while the
  standby's header can still pass its check. Ways to get there include these:
  - invalidate the header first, for example by programming its check field to a value that never checks; NOR
    programming can clear bits without an erase, which costs one page and is inside the compaction-page term;
  - or make the waiting save land where boot will look.
  The power-cut table gains the interval, and the verification row (SE:1114) and NFR-REL-03's test list a
  failed header read-back.
- **Verification:** a host flash-model case. The header is programmed intact and its read-back fails. A save
  is then acknowledged, and power is cut before and after the standby's header sector is erased. Every reboot
  reads the saved value.

### R758-3-R1 RESIDUE - Docs - docs/design/MARK_II_STREAM_ENGINES.md:1143; docs/design/MARK_II_AREA_PLAN.md:313 - two-port gPTP stated as a need and as open

- The two lines read "Redundancy needs one instance per port (#665 F6)". In the same delta, split :51 says
  "one instance per AVB interface is an open owner question", and AP:254 says "one instance per port is open
  decision 3". #665 F6 says "`flexptpd` ported to the core ... for both ports"; it does not fix the instance
  count.
- Exact fix, at both places: "Redundancy needs gPTP on both ports (#665 F6); one instance per port is one way."

### Suggestions (optional, do not affect coverage)

- **S1:** SE:1016-1017 could say why the check plus header is atomic in practice. The check is a cursor
  compare with no flash access, so "one step" means no save is dequeued between them. The model's `split`
  mutation already shows the failure if it is not.
- **S2:** the error bound (SE:550-555) books four PHC reads. Both the talker's capture stamp and the listener's
  render point also read a PHC. They need no term only because the same reading serves both copies or both
  sides of a compare. One sentence would say so.
- **S3 (carried from R758-2 S4, not taken):** the author's reason is recorded (REQUIREMENTS.md text needs
  owner approval). That is acceptable as an optional item.

## R758-2 findings at this head

| ID | Status | Evidence at 69fd18f1 |
|---|---|---|
| F1 192 kHz engine load | Closed | SE:136 93.18 %, 14 eight-channel streams, no CRF, 748.160 Mb/s. SE:138-142 every mix of 1 to 16 streams, and 92.67 % at 16 reservations. Open question 7 at SE:1149-1152. `load_any.py` rerun equals the author's output and my round-2 `load_any_count.out` |
| F2 every 192 kHz placement | Closed | SE:353-354 and :362-377. `p192.py` rerun: 1,245,183 reachable states, of which 34 hold 16 AAF streams, exactly ranks 0..16 minus one with the CRF there or absent. My round-2 count of 35 counted "no CRF" and "CRF stopped at rank 16" twice, so 34 is right. One format 34.861 µs (N = 6), met; mixed 57.905 µs shaper wait, 84.319 µs reached, 100.825 µs at most, not met. 75.999 µs equals my round-2 probe |
| F3 compaction window | Closed at its cause | SE:1003-1020 strict priority and check plus header as one step; tables SE:1030-1046; SE:1114; FR:476. Model rerun: 14,831 runs, 0 losses; mutation `split` 733 and `no_replay` 2,704 losses. T_worst holds with a save waiting on the header: the header is one page (program plus read-back, 5.35 ms), which is the "compaction page in flight" term, and strict priority stops any second compaction page ahead of the save. 359.75 ms re-derived. A narrower hole in the new read-back row is R758-3-F3 |
| F4 merge with a tu copy | Closed at its cause | SE:530-623. Both R758-2 cases (secondary tu, skew below and above 125 µs, arriving first) are now discarded by rule 2. Model cases at ±30 µs, ±200 µs and +1 ms pass, and the `no_rule2` mutation fails them. New defects in the new rules: R758-3-F1 and F2 |
| F5 tap time base | Closed | SE:415-430: both PHCs are stamped on one edge, and each copy's interval uses its own port's PHC at both ends. SE:728-731 and :778 name the PHC. SE:1106 is a verification row for an odd context with a drifting offset |
| F6 flexPTP adoption | Closed | Split :79-80 keeps only the owner's 17:04 words ("Its source and licence get confirmed before adoption", checked against comment 6545820658). Split :93-101 records the survey as "not an owner decision". AP:254 reads "Not decided"; AP:279; AP:308-314 open decision 3; SE:1141-1144. No "adopted fork" or "adopted revision" remains. The two-port wording is R758-3-R1 |
| R1 counter rule | Closed | SE:704 "Every Milan counter is 32 bits and wraps to zero." |
| S1 to S4 | S1 to S3 taken; S4 not taken, with a reason | S1 SE:957 5.344 ms; S2 SE:171 114 µs (15 x 2,064 / 270.848 = 114.31); S3 SE:395-402 totals: 102.584, 123.337, 81.750 and 40.325 = wait + 40.325, all re-added |

## Prior public findings of the internal round (R757-2, issuecomment-6553028166) at this head

I read these after my independent pass, my draft verdict and my ledger. The draft's sha256 is
bc30882d9cce445418ebfdd4eed2aa9b1a0a16cd1290b0b0f4e360af126083f0; it is not published.

| ID | Status at 69fd18f1 |
|---|---|
| N1 save between the last replay and the header | Closed: option (a) taken (SE:1016-1020), and the table row "Impossible" (SE:1036). The model's `split` mutation is the failing sequence, with no power cut |
| N2 exact time compare | Closed: the tolerance window (SE:576-587), the stated bound 2.210 µs (SE:530-558), and verification with jittered ±2.210 µs (SE:1109). The `exact` mutation fails all 15 cases |
| N3 16-reservation condition | Closed: SE:19, :379, AP:60, :255 and FR:306 each carry "16 reservations"; a grep over all docs finds no "one format ... meets" line without it (focus item 5) |
| RR1 PR body | Closed: the live PR body reads "(open questions 1 and 7)". It equals the packet's PR-BODY.md except for a trailing newline |
| RR2 only valid copy | Closed: SE:628 |
| S1 to S5 | Taken: S1 SE:395-402; S2 SE:309-334 (re-derived below); S3 SE:1064-1080 (re-derived below); S4 as R758-2-F6; S5 SE:957 |

## Independently verified at this head (no finding)

- **Signed packet** (`receipts/packet_verify.txt`): evidence commit `1a5f9f3a`, author-r3.
  - 129 manifest entries, 0 published-hash mismatches, 0 unlisted files.
  - SHA256SUMS: 126 lines, all equal to the manifest's original hashes. The 13 SHA256SUMS mismatches are
    exactly the path-redacted files.
  - Gate logs name source revision 69fd18f1.
- **Models rerun** (`receipts/model/`, all rc 0): `merge_model`, `compaction_model`, `load_any` and `p192`,
  run concurrently. Each output is byte-equal to the author's (`rerun_compare.txt`); p192 took 158 s.
- **Conversion error bound** (focus item 3) re-derived:
  - The talker's odd stamp adds its latched offset, and the listener subtracts its own. Their difference is
    (PHC1_T - PHC1_L) - (PHC0_T - PHC0_L), at most 2 x 1 µs by IEEE 802.1AS-2020 B.3 (six or fewer
    intermediate instances, seven hops).
  - Each offset is up to 125 µs old against grandmasters within ±100 ppm (B.1.1): 2 x 25 ns.
  - Four latched reads at the 40 ns granule (B.1.2): 160 ns.
  - Total 2.210 µs. Adding 0.55 µs of drift over 22 packets gives 2.76 µs, far below 62.5 µs, which is far
    below 125 µs less that.
  - Map: 2.667 ms / 125 µs = 21.3, so 22 bits. HEAD_POS is 9 bits for a 512-deep buffer.
  - The new LCTX words 0x48 and 0x4C and `LCTX_MERGE` fill 32 bits; 0x50-0x7C are reserved; SE_MERGE_TU is at
    0x038. All are contiguous.
- **Packetizer term for mixed formats** (SE:309-334):
  - Cycles per bit, (16 + 6N) / (192N + 528), rise with N, so eight-channel frames are the worst AAF case.
  - At 48 kHz: 3 + 5 x 3 + 1 = 19 > 17. At 96 kHz: 12 x 2 + 1 = 25 > 17.
  - (192 + 22) x 2 x 20 ns = 8.560 µs; (224 + 22) x 2 x 20 ns = 9.840 µs; each fits its phase.
  - A CRF's 22 cycles over 704 bits is a higher ratio, but it is added on top, so the bound is conservative.
- **Replay bound:**
  - 0.9t/p - 33 < 273 + 0.1t/p gives t < 382.5 p = 2.046 s; A <= 70.25.
  - Next trigger after 289 p / 0.1 = 15.46 s, with 13.42 s free for the 12 s erase. All re-derived.
- **Latency figures:**
  - 18.093 = 4.557 + 0.200 + 1.000 + 12.336, and 100.825 = 57.905 + 24.827 + 18.093.
  - Every case above 65 µs is stated as not met and is in open question 1.
  - The 34.861 µs one-format result is under the "Results at 16 reservations per port" heading.
- **Docs gates** (clean clone, pinned renderer; `receipts/gates/`, `gates_summary.txt`): 27 of 29 rc 0.
  - `docs_check`: 0 findings over 211 pages and 1,427 scrubbed files.
  - `check_em_dash --base e5b8405d`: 0 over 1,658 added lines in 7 pages.
  - `check_baremetal_only --check`: 0 over 1,425 files, plus its self-test.
  - `check_doc_style` and its self-test; `gen_toc --check` (150 pages), `--verify-anchors` and `--selftest`.
  - `DOC_MAP --check` and `--selftest`; the feature-status, doc-path, gPTP, solution, submodule and archive
    gates with their self-tests.
  - The diagram-PNG check, module matrix, `ci_events --check` and `ci_gate_workflows --check`.
  - `git diff --check e5b8405d HEAD`: rc 0.
  - `check_hygiene` and `check_todo_ownership` refuse because submodules are not initialised (rc 2), as in
    round 2. Neither reads Markdown. The author's receipts at 69fd18f1 show both at rc 0 with submodules, and
    every docs-workflow step at rc 0, the builder legs included.
- **Comment rule:** the delta has no source file, so it adds no source-comment instance. **Privacy:** the
  docs_check scrub is clean.
- **Clone restored** (`receipts/clone_restore_check.txt`, `gitlinks_at_head.txt`):
  - HEAD and tree as above, 0 untracked or ignored entries, index tree equal to HEAD's tree;
  - the six gitlinks are unchanged, and the delta touches none.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F3) | NFR-LAT-03 and NFR-REL-03 (FR:306, :476); IEEE 802.1AS-2020 B.1.1, B.1.2, B.3 as cited at SE:535-558; IEEE 1722-2016 4.4.4.6, 4.4.4.7, 4.4.4.9 at SE:589-651; owner comments 6545820658, #665 body F6; survey 6551164172; every "65 µs" line in docs and the PR body | R758-3 | 69fd18f1d8f9d428687c07ede0f9c14597cf2d61 |
| RTL | UNCLEAN (F1, F2) | Merge state, rules 1 to 7, reference upkeep and sweep (SE:560-660); merge and tap registers (SE:728-736, :778, :806-828); engine load table (SE:132-142); packetizer term (SE:309-334); instrument (SE:410-436) | R758-3 | 69fd18f1d8f9d428687c07ede0f9c14597cf2d61 |
| Robustness | UNCLEAN (F1, F2, F3) | Both-tu, tu sequence jumps, one-network tu and loss; compaction save-landing and power-cut tables (SE:1030-1049); header read-back path; replay bound (SE:1054-1098) | R758-3 | 69fd18f1d8f9d428687c07ede0f9c14597cf2d61 |
| Tests | UNCLEAN (F1, F2, F3) | Author models `merge_model.py` (15 cases, 3 mutations), `compaction_model.py` (14,831 runs, 2 mutations), `p192.py`, `load_any.py`, rerun; own probes `probe_merge_both_tu*.py`, `probe_merge_tu_seq_jump.py`, `probe_compaction_header_readback.py`; verification rows SE:1104-1114; docs gates at the head; author gate receipts | R758-3 | 69fd18f1d8f9d428687c07ede0f9c14597cf2d61 |
| Docs | UNCLEAN (F1, F2, F3; R1 residue) | All four touched pages at the head (SE, split, AP, FR); diff f6b3e841..69fd18f1 and its eight commits; author HANDOFF and live PR body; contents and anchors | R758-3 | 69fd18f1d8f9d428687c07ede0f9c14597cf2d61 |

## Real limits

- I did not re-read the standards this round. The IEEE 802.1AS-2020 B.1.1 (±100 ppm), B.1.2 (40 ns) and B.3
  (1 µs within seven hops) values match my reading of those clauses, and I did not open the clause text again.
  Clauses whose cited text is unchanged since round 2 keep their round-2 readings.
- The latency, merge and compaction results come from the author's models, which I reran, and from my own small
  probes on those models. They are not from an implementation. F1 to F3 are design-level defects shown in those
  models.
- **Hosted evidence at this head**, at 06:36 UTC (`receipts/gh/hosted_check_runs.tsv`):
  - 19 completed success, 22 skipped, and 3 still in progress (docs-gates-0, docs-gates-2 and one fail-fast
    context).
  - docs-check-no-git, docs-gates-1, rtl-fast, wire-accountability and full-ci-gate passed.
  - This is not acceptance evidence.
- No physical calibration, bench or hardware run took place. No manager source bank runs at this head, and none
  is claimed or inferred.

## Pending manager duties

- Hosted and act acceptance of the exact head, including the docs-gates-0 and docs-gates-2 results.
- Builder and native banks on the current-dev merge candidate at the merge turn. The source base is e5b8405d,
  and live dev is 1f29f189; the author's trial merge is information only.
- Owner approval of the requirement text and of the open owner decisions:
  - latency with mixed formats or fewer reservations;
  - save bursts, Block RAM and the commit timeout;
  - lever 5 against media ownership, and lever 2 after lever 3;
  - `flexptpd` on two ports and its surveyed source.
- Carry R758-3-R1 to the residue checklist.

R758-3 FINISHED
