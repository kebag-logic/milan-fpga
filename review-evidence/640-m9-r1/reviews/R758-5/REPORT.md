[R758] NEGATIVE - exact head 270866ecb95155ef48428ec3a049c357f7eae946

Round R758-5: external independent review of PR #828 (issue #640, with #665 and #823), round-5 delta.
- Head `270866ecb95155ef48428ec3a049c357f7eae946`, tree `6d63bab078834cb3112d3002665f1c2efd9051ca`.
- Previous head `22f3cedb420992b7b776c5a842b0b210ac4191d3`. Merge base and live dev `1f29f189279f9fc0132f4918e47342b87d22f33a`.
- Delta: three one-line commits on two Markdown pages (75 lines added, 105 removed). No code, generator, gate, configuration or gitlink.
- SE below is `docs/design/MARK_II_STREAM_ENGINES.md`; AP is `docs/design/MARK_II_AREA_PLAN.md`; FR is `docs/reference/FR_NFR.md`.

**Verdict basis.**
- The reduction did what the ruling asked. Every R758-4 and R757-4 finding and residue item is closed. No touched page, verification row or PR text still states tu behaviour as fact or cites a removed register, bit or rule. TU-1 to TU-5 are correct, cited and verifiable, and they cover my cases. The two save statements are right. The docs workflow passes.
- The verdict is NEGATIVE on one MINOR finding, F1, under focus 3. With the tu text gone, the page's clean-copy rules still contain a case that contradicts SE:624: clean copies on both networks with an arrival margin under one packet interval are each placed by their own time, so conversion error shifts samples.
- F1 needs one corrected sentence and one owned case, with no new mechanism. No stated latency, load, save or area figure moves.
- **F1 is not new behaviour.** The same path is in the round-4 model. My round-4 probe tested this margin only with tu set (R758-4-F1(b)), so I missed it then. It counts now because focus 3 asks whether the clean rules are self-consistent, and because case H now owns this margin for tu copies only, which leaves the clean case with no owner. If the manager rules that F1 falls outside this round's scope, nothing else in this report blocks.

## Findings

### R758-5-F1 MINOR - Conformance, RTL, Robustness, Tests, Docs - SE:624-625, with :642, :654-655, :667-668, :1148, :1166 - clean copies with a short arrival margin on both networks are placed by their own time, so conversion error shifts samples

- **Authority/evidence:**
  - SE:624 says "So conversion error never shifts a sample." SE:625 excepts only "A new anchor".
  - SE:667 treats a time the render point has passed as invalid, and rule 2 (SE:642) anchors at the copy's own time when the head is invalid. If a packet's first copy arrives less than 125 µs before its time, the next packet arrives after the head's time has passed. So every packet is a new anchor, and the exception becomes the normal path.
  - The partner copies differ by up to 2.744 µs (SE:604). When networks with similar latency take turns arriving first, the anchor's own time crosses a sample boundary and the packet lands one sample off.
  - The margin is legal. IEEE 802.1BA-2011 6.5, cited at SE:560, allows class A transit up to 2 ms against the 2 ms default offset. Two networks of one redundant pair are often built alike, so similar margins are the expected case.
  - Probe (`scripts/probe_margin_r5.py`, `receipts/model/probe_margin_r5.out`). It is built from the page's rule table: all copies clean, no frame lost, no time step, both networks 10 to 50 µs before their time, 64 phases of the sample grid, 0.25 s per phase:

    | Rate | Sample period | Phases with a shift | Worst shifts in 2,000 packets | Worst samples left unwritten |
    |---:|---:|---:|---:|---:|
    | 48 kHz | 20.833 µs | 17 of 64 | 766 | 383 |
    | 96 kHz | 10.417 µs | 33 of 64 | 766 | 383 |
    | 192 kHz | 5.208 µs | 64 of 64 | 766 | 383 |

  - No packet is lost and `SE_MERGE_DUP` stays right. The damage is a sample overlap or gap at up to 38 % of packet boundaries.
  - Second implementation: the round-4 model's clean path, unchanged, on the same setup at 1 µs past a boundary: 541 samples missing and 540 rewritten over 4,000 packets. At margins of 150 to 200 µs it shows none.
  - Controls, all 0 shifts in all 64 phases at 48 and 192 kHz: margins of 150 to 200 µs on both; a fast primary; a primary always first (2,000 anchors, all on one time base); one network only. A variant that keeps the head for counting until 1.5 intervals past the render point also gives 0 shifts and one anchor, so the lapse is the cause.
  - No part of the page owns the case. The clean row SE:1148 names no margin, its 12 cases all stay above it, and my rerun of those cases passes. Item 1 (SE:1166) covers the span's edges. Case H (SE:1200) has this margin with tu on both only.
  - SE:655 says the merge keeps Annex D.2's external behaviour for clean copies. Per-network buffers rendering "one or the other" would not read as switching a sample per packet, so that clause claim is unsafe in this case. I did not open the clause text this round; see Real limits.
- **Impact:** a lane built to the page passes its clean row, then shows clicks on a redundant stream with both networks near the transit bound, at every 192 kHz phase and about a quarter of 48 kHz phases. Nothing tells the owner about this limit. SE:660 and SE:650 hold; only SE:624 and SE:655 overreach.
- **Required outcome:** either of these.
  - Change the rule: the head stays usable for counting across the render point, with a separate bound against wrap.
  - Or state the limit and give it an owner, which adds no mechanism:
    - SE:624 reads "Under a valid head, conversion error never shifts a sample."
    - After SE:625, a new paragraph reads "A margin under 125 µs lapses the head every packet. Interleaved copies can then land one sample apart."
    - SE:655 carries the same condition, or the new paragraph follows it.
    - A new open design item for lane 6, or an added clause in item 1, states the requirement with this verification: clean copies on both networks 10 to 50 µs before their time, first arrival interleaved, 48, 96 and 192 kHz, every grid phase; the test fails on a shift beyond what the lane states.
    - The PR's known limitations gain one line.
- **Verification:** `scripts/probe_margin_r5.py` on the lane's model shows 0 shifts or the stated limit; reread SE:624, :655 and the new item.

### R758-5-R1 RESIDUE - Docs - SE:1179 against SE:1199 - TU-4 names only an unpaired stream, while its case G also runs pairs

- Case G and R757-4-N7's arm B run tu from packet 0 on both networks, and case G "Serves TU-4". Its test ("a stream receiving every packet") already binds a pair, so only the requirement sentence is narrower than its test.
- Exact fix at SE:1179: "An unpaired stream or a pair that starts with tu still renders."

### Suggestions (optional, do not affect coverage)

- **S1, named stimuli on the clean row (SE:1148).**
  - The row says "Simulation of every rule", and that still binds the lane. But the tu cases that moved out were the row's only named stimuli for rule 1 and for a far copy.
  - The row's 12 cases hit rules 2, 4, 5 and 6 only (`receipts/model/probe_clean_r5.out`, section A).
  - The row could name a late copy, an early copy, a format failure clean and with tu, and a backward time-base step of 3 ms.
  - Rule 3 is unreachable on a steady time base, since the largest |k| inside the span is 21 (section D). A -3,000 µs step reaches it once (section C).
- **S2, mirror of case E (SE:1197).** TU-2 says "either network" and case E names "Secondary tu" only. Roles are not symmetric on this page: the even context holds the merge state and one port is the reference port (SE:524, :585). The round-4 model shows no difference between the two directions (`receipts/model/probe_tu_req_r5.out`), so this adds coverage rather than fixing a known failure. Exact change: "tu on either network".
- **S3, sweep cost (SE:674).** "128 cycles per second" was written when the sweep looked after up to three times per context, and the derivation is not stated. It now looks after one time, and only even contexts hold it. No budget reads the figure and the 1 s bound at SE:671 holds, so it could be restated or dropped.
- **S4, TU-1 across lanes (SE:1176, AP:278).** Lever 5 moves the media clock servo into firmware at lane 8, after lane 6. Lane 8's evidence could carry TU-1's free-wheel test so the move cannot drop it.
- **Carried, not taken:** R758-4 S1, S3 and part of S2, R757-4 S4 to S7. The author's reasons in the PR body and handoff are acceptable; this round only reduces.

## Round-4 findings at this head

| ID | Status | Evidence at 270866ec |
|---|---|---|
| R758-4-F1(a) own-time skew | Closed | SE:711 and the claim list are gone; SE:632-635 takes tu copies past the format check out of the rules; TU-1 plus cases B and C. Each probe row is named: +1,000, -1,900, -2,500 µs; 1 ms either sign at the default latencies. Case B's "60 to 180 µs" equals the model's primary latency |
| R758-4-F1(b) arrival margin | Closed for tu | Case H carries all four margin bands, serving TU-5. The clean-copy counterpart is F1 above |
| R758-4-F1(c) networks clearing apart | Closed | SE:721 is gone; case I has -200, -300, -500 µs, slower first, faster up to 80 packets later |
| R758-4-F2 | Closed | The sentence is gone with the reference; TU-4 and case G. The page now has no reference to contradict |
| R758-4-R1 | Closed | PR body Round 4 row reads "removing rule 4 fails 7"; the receipt prints 7 (`author-r5/evidence/model/mutation_count.txt`, my rerun identical). The round-4 handoff stays as published, which is right for a historical packet |
| R758-4-R2 | Closed | SE:650 as written. Its second sentence named rules that no longer exist; TU-2 replaces it |
| R757-4-N6 | Closed | Every probe row is named: case A (+700, +800, +850, -2,000), B (+1,000 period), D (fast primary), F (cut, 250 ms, +2,500). Arm A's -1,900 is in B |
| R757-4-N7 | Closed | Arm B's three starts are in case G; see R1 for the sentence |
| R757-4-N8 | Closed | As R758-4-R1 |
| R757-4 RR5 | Closed | The corrected sentences are gone; case K has "on both networks" |
| R757-4 RR6, RR7 | Closed | SE:975 and SE:937 as written |

The internal round-4 report was read after my draft verdict and ledger. The draft's sha256 is in `receipts/draft_sha256.txt`; the draft is not published. The one change since the draft is that this ledger adds Conformance to F1, for SE:655, instead of leaving it clean. The round-5 internal report was not read.

## Per focus item

**Focus 2, no surviving claim** (`receipts/claims_grep.txt`).
- `tu` on SE appears only at :580, :611-617, :632-635, :1149, :1167, :1169-1204. Each is a pointer, a requirement or a case. `TIMESTAMP_UNCERTAIN` in the counter rows is the Milan counter and is untouched.
- `SE_MERGE_TU`, `LAST_TU`, `ANCHOR_TU`, `SEQ_VALID`, `CLEAN_VALID`, `LCTX_SEQ_PT`, `LCTX_CLEAN_PT` and the removed anchors `#tu-on-both-networks` and `#reference-upkeep` have 0 hits over docs, REQUIREMENTS.md and scripts. The receipt's hits for "names no packet", "rule 7" and "rule 8" are on unrelated pages and in a gate script, none in this delta.
- FR has no merge or tu claim. The split page's and REQUIREMENTS.md's `tu` lines are about the talker and did not change in this delta.
- The live PR body equals the packet's apart from a trailing newline (`receipts/pr_body_diff.txt`). The Round 2 to Round 4 merge text is introduced as history that Round 5 removed; commit-table rows `0f6ab84b` and `2322c6d7` say so; `07f8eb91`'s "never displaces clean partner data" still holds as TU-2. Known limitations and the models line state no tu figure.

**Focus 3, clean-copy rules** (`scripts/probe_clean_r5.py`, `scripts/check_regmaps.py`), built from the page's rule table without the earlier model's code.
- **Rules:** k is exhaustive across rules 3 to 6; the table's "first matching rule" holds. All 12 named row cases: 0 wrong, 0 missing, 0 outside the buffer.
- **Duplicates:** 4,000 of 4,000 second copies counted at both latencies, 1,500 on a cut, and the counts match under loss.
- **Row's mutations:** `exact` fails 12 of the 12 cases and `own_time` fails 2, so the row's claim holds on clean cases alone.
- **Sums:** 62.5 µs window, 2.744 + 0.550 = 3.294 µs, 59.206 µs spare, neighbours 121.706 µs apart. The 2.744 µs arithmetic at SE:571-577 is unchanged. Span is 21.333 intervals against a 22-bit map; `HEAD_POS` is 9 bits against 512 samples.
- **Registers:** the three tables sum with 0 problems: every offset once to 0x2000, 0x40 and 0x80, every word's bits 31:0, each reset's width fits. `LCTX_STATE` 31:9 and 0x48-0x7C reserved; 56 octets at SE:1172 is 128 - 72. `SE_MERGE_DUP` cites rule 6 and `SE_MERGE_SEC` rules 2 to 5, both correct.
- **Rule references:** SE:550, :643, :1177 are all right after renumbering. The ledger's 32 x 128 octets is unchanged.
- **Moved text:** SE:657-663 reads correctly, and SE:660's condition holds in my probes, including a cut at each latency. F1 is the one inconsistency.

**Focus 4, TU-1 to TU-5.**
- **Correct and cited:**
  - TU-1 matches this repo's records of IEEE 1722-2016 4.4.4.7 and Milan v1.2 4.4.2.3 (`docs/design/MEDIA_CLOCK_FOLLOWING.md:132`, :666, "for an appropriate amount of time" after tu resets).
  - TU-5's 1.5 s is at `docs/design/GM_LOSS_RECOVERY.md:218` and :333, inside the linked section for :218; case F's 250 ms is :190.
- **Verifiable, not vacuous** (`scripts/probe_tu_req_r5.py`): TU-1's differential test over cases A to D fails the round-4 model in 11 of 16 runs, and a disposable counted check passes all 16 with 0 missing. So the test can fail and the requirement can be met. This is feasibility evidence, not a proposed mechanism.
- **Coverage:** all my round-4 cases are named, see the table above. S2 of round 4 is in case L. Twelve cases, A to L; each serves at least TU-5; TU-1 to TU-4 each have a case. The loss table reads "To be set by lane 6". The model and probe links resolve at commit `b250a616`, an ancestor of the evidence tip, and their labels are neutral.
- **TU-2 after the third commit:** "as the rules above place it" correctly stops a discarded duplicate from reading as a break. Its test holds on packets with a clean copy past rule 1.

**Focus 5, the two save statements.**
- SE:975 is right. SE:1052 adds one page for a failed header (365.10 ms), and a compaction retry yields at the next page boundary (SE:1008-1009), so "fault-free" is the correct and conservative condition.
- SE:937 is right for copy, replay and record pages. Each page holds checked records, so a failed page fails its check or duplicates an identical value, and sequence order resolves the rest (SE:943-944, :1058-1064). The header keeps its own path (SE:1030-1054). SE:938's reported-fault wording matches SE:1044. Nothing in NFR-REL-03 contradicts either.

**Focus 6, docs workflow** (`receipts/gates/`).
- My clean clone with the four submodules and the pinned renderer: 33 of 33 docs-relevant gates rc 0, including `docs_check` (0 findings, 213 pages), `check_em_dash` (0 over 1,748 added lines in 7 pages), `check_doc_style`, `check_doc_paths` (1,084 paths), `gen_toc` all three modes (580 links), `check_baremetal_only`, hygiene and TODO ownership. `git diff --check` rc 0.
- Author receipts for the steps I did not run (both builder legs, RV32 SDK, ratchets): all 50 rc files read 0.

**Evidence and shape.**
- **Packet** (`receipts/packet_verify.txt`): evidence commit `cf94dfd2`, author-r5, 113 manifest entries, 0 published-digest mismatches, 0 unlisted. SHA256SUMS has 110 lines, all equal to the manifest's originals; the 12 that differ from the published bytes are exactly the path-redacted files. One large log is listed by digest and not published. The host reports the commit as unsigned, so this is digest integrity only, not a signature.
- **Model:** merge model sha256 `2d857169...` rerun: ALL PASS, byte-equal to the author's rerun, and the mutation counts are the published ones.
- **Commits:** three one-line subjects with no trailers; 34 first-parent commits as the PR body says.
- **Comment rule:** the delta has no source file, so no instance. SE:1207's URLs contain review directory names; a design page is not a source comment, and the link labels are neutral.
- **Clone** (`receipts/clone_restore_check.txt`): HEAD, tree and index as above, 0 untracked or ignored entries, worktree equal to HEAD, six gitlinks unchanged. All probes ran under the packet directory; nothing ran in the clone.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, SE:655 only) | TU-1 to TU-5 sources SE:1176-1180 against the repo's records of IEEE 1722-2016 4.4.4.6, 4.4.4.7 and Milan v1.2 4.4.2.3; SE:654-660 against Annex D.2, D.3 as quoted; rule 1 SE:641 against Milan v1.2 4.4.2.2, 5.3.8.10; NFR-REL-03 at FR:476 | R758-5 | 270866ecb95155ef48428ec3a049c357f7eae946 |
| RTL | UNCLEAN (F1) | Rules and head upkeep SE:619-674; register tables SE:723-833 summed by `check_regmaps.py`; `probe_clean_r5.py` and `probe_margin_r5.py` | R758-5 | 270866ecb95155ef48428ec3a049c357f7eae946 |
| Robustness | UNCLEAN (F1) | Margins, cuts, loss, boundary times, time-base steps in `probe_clean_r5.py`, `probe_margin_r5.py`; save statements SE:937, :975 with SE:1008-1054 | R758-5 | 270866ecb95155ef48428ec3a049c357f7eae946 |
| Tests | UNCLEAN (F1) | Rows SE:1148-1149, cases SE:1193-1204; row mutations rerun on clean cases; TU-1 differential in `probe_tu_req_r5.py`; round-4 model rerun; 33 gates; author receipts | R758-5 | 270866ecb95155ef48428ec3a049c357f7eae946 |
| Docs | UNCLEAN (F1; R1 residue) | SE and AP:276 delta and history `22f3cedb..270866ec`; FR; live PR body; author-r5 HANDOFF; TOC, anchors and evidence links | R758-5 | 270866ecb95155ef48428ec3a049c357f7eae946 |

## Real limits

- I did not open the standards' text; no copy is in the repository. Clause readings rest on the repository's records, the author's quotations and my earlier rounds. That includes Annex D.2, on which F1's Conformance attribution rests.
- The manager's ruling is known to me from my assignment and from its public statements in the author's TAKEN comment and the PR body.
- F1 and everything else here come from my probes and the author's model, not an implementation. The probe holds each network's time free of B.3 jitter apart from the conversion error, and assumes overlapping arrival windows on the two networks. A primary always first shows no shift.
- I did not run the builder legs, the RV32 SDK steps or the ratchet gates. For those I rely on the author's receipts, and they are not manager evidence.
- **Hosted evidence at this head, snapshot** (`receipts/hosted_check_runs.tsv`): 19 completed success, 22 skipped, 3 in progress (docs-gates-0, docs-gates-2 and one fail-fast context), 0 failed. docs-check-no-git, docs-gates-1, rtl-fast, wire-accountability and full-ci-gate passed. This is not acceptance evidence.
- No physical calibration, bench or hardware run took place. No manager source bank ran at this head, and none is claimed or inferred.

## Pending manager duties

- Hosted and act acceptance of the exact head, including docs-gates-0 and docs-gates-2.
- Builder and native banks on the current-dev merge candidate at the merge turn (source base and live dev `1f29f189` at this review).
- Owner approval of the requirement text and of the open owner decisions.
- Rule whether F1 is in scope. If it is, one more round on that text; if not, record why it is left open.
- Carry R758-5-R1 to the residue checklist.

R758-5 FINISHED
