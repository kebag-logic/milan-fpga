[R757] POSITIVE - exact head 270866ecb95155ef48428ec3a049c357f7eae946

# R757-5: internal cleared-context review of PR #828 (issue #640), round 5

- Head `270866ecb95155ef48428ec3a049c357f7eae946`, tree `6d63bab078834cb3112d3002665f1c2efd9051ca`.
- Round-5 delta: `22f3cedb..270866ec`. Three one-line commits with no bodies or trailers, on two Markdown pages, 75 lines added and 105 removed. The delta has no code, generator, gate, configuration, gitlink or mode change.
- **Reconstructed from:** AGENTS.md and CONTRIBUTING.md, docs/README.md; the #640 body and owner decisions; the manager's ruling as given in the round brief (reduce, do not patch); my R757-4 report; the delta; the live PR body; the author's round-5 packet `review-evidence/640-m9-r1/author-r5` at `cf94dfd2`.
- **Taken as given:** the tu mechanism and its loss figures are open by ruling, and are not findings.

**Order of reading, with one departure from the brief.** The brief requires my verdict and ledger to be written before I read another reviewer's report.

- **What happened:** I composed this report's verdict, findings and ledger first, then issued the write and the fetch of R758-4 in one step. The write failed on a tool precondition, so R758-4 reached me before the report was on disk.
- **What cannot be shown:** no draft digest exists, so the order rests on this statement alone.
- **What changed after the read:** no verdict, finding, severity or ledger result. Four wording corrections, none drawn from R758-4: the PR-body rule sentence in focus item 2, the basis of the case-parameter comparison, the sweep sentence in focus item 3, and the fix wording in S9. I also updated the hosted-run figures and added the section "Prior external findings".

Short names: SE is `docs/design/MARK_II_STREAM_ENGINES.md`; AP is `docs/design/MARK_II_AREA_PLAN.md`; FR is `docs/reference/FR_NFR.md`.

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR is open. Every lens is covered clean at this head.

- **Round-4 findings:** N6, N7, N8 and RR5 to RR7 are all closed.
- **Reduced text:** no touched page, FR or verification row states tu behaviour as fact. None cites a removed register, bit or rule.
- **Clean-copy merge:** built from the page alone, rules 1 to 6 pass every arm of the verification row at 48, 96 and 192 kHz. The row's two named mutations both fail.
- **Register maps:** every offset and bit is defined or reserved, and the figures still sum.
- **TU-1 to TU-5:** each is cited and verifiable. The cases cover every probe in my round-4 report.
- **Gates:** 23 docs-gate commands re-run at this head all exit 0. All 50 of the author's rc files record 0, and their digests verify.
- **Open items:** three RESIDUE items and six SUGGESTIONS. One suggestion, S9, is a real behaviour outside this round's delta and should reach lane 6.

## Findings

No BLOCKER, MAJOR or MINOR.

## RESIDUE (wording only; each changes no figure, verdict, test or gate)

### RR8 RESIDUE - Conformance, Docs - SE:1179; PR body, Round 5 row "R757-4-N7, R758-4-F2" - TU-4 names only an unpaired stream, while its case and test also run a pair

- **Authority and evidence:** TU-4 reads "An unpaired stream that starts with tu still renders." Case G (SE:1199) serves TU-4 and has three arms: unpaired, on both networks, and on both with the secondary faster. TU-4's test says "a stream receiving every packet", so it already fails a pair that renders only isolated packets. R757-4-N7 measured that loss on the pair arms too (21,870 and 21,864 of 24,000 samples). TU-1's exception (SE:1176) reads "an anchor TU-4 states".
- **Why RESIDUE:** the test outcome is already fixed by case G. The fix only aligns the sentence with the test.
- **Impact:** a reader of the requirement column alone could take a pair starting with tu to be outside TU-4.
- **Exact fix:** SE:1179 "A stream that starts with tu, unpaired or on both networks, still renders." In the PR body: "TU-4 requires that a stream starting with tu still renders, unpaired or on both networks, with the lane stating how."
- **Verification:** read SE:1179 against SE:1199.

### RR9 RESIDUE - RTL, Docs - SE:642 - "clears the map" contradicts the map's own definition

- **Authority and evidence:** rule 2 "anchors the head and clears the map", and rule 3 re-anchors "as rule 2". SE:820 defines bit k as set "when the packet k intervals before the head is written", so an anchor's bit 0 is set. With bit 0 clear, the partner's copy would pass rule 5 and count no duplicate, and SE:1148's duplicate count would then fail. My probe follows SE:820. The words predate this round, but the delta retyped the row.
- **Impact:** none in behaviour, because SE:820 and the test govern.
- **Exact fix:** "it anchors the head and restarts the map with only bit 0 set".
- **Verification:** read SE:642 against SE:820.

### RR10 RESIDUE - Docs - PR body, Description row `07f8eb91` - a commit row still carries tu text with no round-5 note

- **Authority and evidence:** the row says "a copy with tu set never displaces clean partner data" and "the merge registers". Rows `0f6ab84b` and `2322c6d7` end with a note that their text left in round 5, and the Round 3 and Round 4 intros say the same. This row has no such note. It is a history row, and TU-2 keeps its tu sentence true as a requirement.
- **Impact:** a reader of the row alone could take a removed mechanism as current.
- **Exact fix:** append "The tu text left in round 5." to that row.
- **Verification:** read the row.

## SUGGESTIONS (optional)

- **S8 - Tests, Robustness - SE:1148: name an arm for rule 3 and for a head lapse.** The row says "Simulation of every rule", which still binds. But over all its named arms, rule 3 is reached 0 times, and rule 2 only by each arm's first packet (`receipts/probe_clean_rules_r5.txt`).
  - **Why rule 3 is rare:** a copy past rule 1 and a valid head both lie within the 2.667 ms span, so |k| is at most 21.
  - **What reaches it:** a render point stepping back past the span. A 5 ms step in the probe does. That makes rule 3 a real guard, not dead text.
  - **Fix:** add "a head lapse on both networks; a render-point step beyond the span" to the row.
- **S9 - Robustness, RTL, Tests - SE:642, :624-625, :660, :1148, :1166: clean copies arriving under one packet before their time. Not a round-5 change.**
  - **Behaviour:** rule 1 accepts such a copy. The head lapses before the next packet, so rule 2 re-anchors every packet by its own time. Placement by count then never runs.
  - **Measured:** surviving network only, 48 kHz, margin 20 to 100 µs, time 100 ns past a sample boundary, 160 ns of packet-to-packet jitter: 617 samples missing and 4,524 misplaced of 24,000. At margin 200 to 300 µs the same arm loses none and rule 4 places every packet after the first. At 1 µs past the boundary with 1 µs jitter it also loses none.
  - **Limits of the figure:** this is a page-derived stress arm on a time held at a sample boundary, not a measured rate. It needs a surviving-network latency of about 1.9 ms or more, which is legal but extreme. So it is a one-sample slip risk, and the figures are not a loss bound.
  - **Against the page:** SE:625 says "A new anchor alone uses its own time", which covers this. SE:660 "the pair loses no samples" reads stronger than the behaviour in this regime.
  - **Why it does not count against this round:** rule text, SE:624 and the no-loss statement carry the same meaning at `22f3cedb` (lines 649, 635, 690), and the brief scopes earlier text out unless the delta broke it. The delta did not.
  - **Fix:** lane 6 adds this arm to open design item 1, or keeps the head valid across a one-packet gap so the count still places the copy.
- **S10 - Tests, Docs - SE:1180, :1149, :1167: say which cases run on the bench.** TU-5 says "Every case below, in the model and on the bench". Only cases E, F and J name a bench arm, and SE:1149 says "That item's bench cases". The strict reading is safe, but it asks for bench runs of a 1.5 s skew and a sequence step of 3 on a talker that must be able to produce them.
- **S11 - Tests - SE:1176, :1198: add case F to TU-1.** TU-1's skew test runs cases A to D, and all of them have a partner delivering. Case F is the only skew with no partner, and it serves TU-5 alone. A lane could trust a tu copy's own time only once a partner is lost, pass TU-1, and simply record the loss.
- **S12 - Docs - SE:1184-1186: add a loss row for an unpaired stream.** Cases G, K and L have unpaired arms, but the table's three conditions name only pairs and skew. The per-case report still captures them.
- **S13 - Conformance - SE:633, :830-831: say what a tu copy's time does to the counters.** Round 4's rule 1 applied the late and early check to tu copies, and so counted them. SE:633 now hands those copies to item 2, and TU-1 to TU-5 do not mention `LCTX_LATE_TIMESTAMP` or `LCTX_EARLY_TIMESTAMP`. Those rows still cite Milan v1.2 5.3.8.10, so the duty stands. One clause in TU-1 would make it explicit.

R757-4 S4 to S7 were declined with stated reasons. They were optional, so nothing is retained.

## Round-4 findings (R757-4) at this head

| Item | Evidence at this head | Result |
|---|---|---|
| N6 MINOR, tu's own time and the no-loss claims | Rule 1's time check now applies to clean copies only (SE:632-635). Round-4 SE:711, :695, :1219's tu arms and the PR-body claim are gone. TU-1 forbids trusting a tu copy's own time, TU-5 makes loss lane 6's output, and SE:1184-1186 read "To be set by lane 6". Cases A, B, D and F carry each probe row | **Closed** by the reduced text |
| N7 MINOR, "cannot make one" | The sentence is gone (0 hits). TU-4 requires the render and the lane states how. Case G names all three of my starts | **Closed**; RR8 is wording |
| N8 MINOR, mutation count | PR body line 137 reads "removing rule 4 fails 7". The author's re-run prints `no_rule4: caught by 7`, as the published output does | **Closed** |
| RR5 | Its sentences are gone. Case K names a jump on both networks | **Closed** |
| RR6 | SE:975 is the exact fix | **Closed** |
| RR7 | SE:937 is the exact fix | **Closed** |

### My round-4 probes against the named cases

| Probe | Case |
|---|---|
| Both networks 60 to 180 µs; skews up to +700, +800, +850, -2,000 µs | A |
| tu for packets 100 to 600, skew +1,000 µs; -1,900 µs with wrong positions | B |
| Fast primary +1,000 µs, slow secondary 0 | D |
| Primary cut, secondary tu 250 ms, skew +2,500 µs | F |
| tu from packet 0: unpaired, both, both with the secondary faster | G |
| Jump on both networks, and on one with the partner clean or tu | K |
| Restart inside the span (round 4's open design item 2) | L |

No probe of mine is uncovered. The case parameters match the tables in my R757-4 report; I did not re-read the probe scripts.

## What was checked, per focus item

1. **Round-4 findings:** see the tables above.
2. **Residual claims:**
   - **Removed names:** `SE_MERGE_TU`, `ANCHOR_TU`, `SEQ_VALID`, `CLEAN_VALID`, `LAST_TU`, `LCTX_SEQ_PT` and `LCTX_CLEAN_PT` have 0 hits under `docs`, `scripts`, `tests` and `tb`, and in REQUIREMENTS.md. In the PR body they appear only in the Round 5 list of what left, and `LAST_TU` in commit row `0f6ab84b`, which notes its text left in round 5.
   - **Rule numbers:** every remaining reference on the five pages resolves to the new numbering (SE:550, :633, :643, :650, :744, :745, :1177). Rules named in the PR body sit in rows stated as history, or in the Round 5 section.
   - **FR:** no tu or merge claim. Its redundancy lines (FR:331, :473, :577-587, :617) state shape and scope only.
   - **AP:** one changed row (AP:276), which is right; SE:1161 names lane 6, and AP:276 is the lane 6 row. AP:177 says only "merge".
   - **SE tu mentions:** SE:580 (no such bound), SE:611-617, SE:633-635, and item 2. The counters `TCTX_TIMESTAMP_UNCERTAIN` and `LCTX_TIMESTAMP_UNCERTAIN` are Milan counters, not the mechanism.
   - **Verification rows:** SE:1148 has no tu arm, and its bench claim is the cable pull only. SE:1149 points to item 2.
   - **Other pages:** the split page and REQUIREMENTS.md mention `tu` only for the talker-side fabric decision, and the delta does not touch them.
3. **Clean-copy merge:**
   - **Rules:** rules 1 to 6 are ordered and complete. k = 0 to -21 with a 22-bit map; |k| > 21 goes to rule 3. Counters: `SE_MERGE_DUP` is rule 6 and `SE_MERGE_SEC` is rules 2 to 5, matching the table.
   - **Probe** (`scripts/probe_clean_rules_r5.py`, `receipts/probe_clean_rules_r5.txt`, built from the page alone): 9 arms at 3 rates, 27 runs, all PASS. Each has 0 samples missing, misplaced or extra, and exact duplicate and secondary counts. Arms: jitter up to 2.744 µs; 1.5 ms apart either way; 1 µs past a sample boundary; a cut on either network, and with the survivor slower; 1 % loss filled by the later copy.
   - **Mutations:** exact compare fails 9 of 9 arms; own-time placement fails 8 of 9.
   - **Figures** (`receipts/regmap_r5.txt`): 2.917 ms latch to latch and 2.744 µs still hold, with drift rounded up (2.7434). Window margin 59.206 µs, neighbours 121.706 µs apart. Span 21.33 packets, under 22.
   - **Register maps** (`scripts/check_regmap_r5.py`): engine block ends at 0x2000, talker context at 0x40, listener context at 0x80. There are no gaps or overlaps, every word fills 32 bits, and each reset fits its field. `LCTX_MERGE` is 22 + 9 + 1 bits, and `HEAD_POS` addresses the 512-sample depth. Reserved 0x48-0x7C is the stated 56 octets. The ledger's 32 x 128 octets is unchanged.
   - **Sweep:** 32 contexts per second at 4 cycles each is 128. The page does not derive the 4 cycles. The sweep now clears one kind of bit, not three, so its work did not grow.
   - **Pairing and render span:** SE:489-505 and SE:449-485 are outside the diff.
4. **TU-1 to TU-5:**
   - **TU-1:** matches the repository's records of IEEE 1722-2016 4.4.4.7 (`docs/design/MEDIA_CLOCK_FOLLOWING.md:132`) and of Milan v1.2 4.4.2.3, "for an appropriate amount of time" after `tu` resets (same page, :666). The skew test compares two runs, so it is verifiable, and it holds at ±1.5 s. The exception for an anchor is needed, because a stream starting with tu has no other time.
   - **TU-2:** "as the rules above place it" resolves the duplicate. Rule 6 discards a second clean copy, and the test checks the rendered samples. It is consistent with SE:650.
   - **TU-3:** checkable at every write, and leaves the restart signal to the lane, as ruled.
   - **TU-4:** see RR8.
   - **TU-5:** the 1.5 s figure and link are right. `docs/design/GM_LOSS_RECOVERY.md:218` lies inside the linked section (:156-:308), and :333 grades the same step. The bound is left open by ruling. See S10 and S12.
   - **Starting-point links:** SE:1206-1207 all resolve at `b250a616`, an ancestor of the evidence tip (0 behind), and four paths list 9, 9, 4 and 5 entries. The same link form exists at `docs/testing/ASSERTIONS.md:153`.
5. **Two other statements:**
   - **SE:975 "Fault-free, a save waits for at most one compaction page.":** right. Compaction yields only between pages (SE:976), and SE:1052 adds the one faulted page. 10 + 5.35 + 2 + 2 x 171.2 = 359.75 ms, and +5.35 = 365.10 ms. Neither FR nor AP restates it.
   - **SE:937 "Any non-header page failing read-back is rewritten further on.":** consistent. A copy or replay page failing is retried further on in the standby, and a save still has priority at the next page boundary (SE:1008-1009). A copy or replay retry therefore does not lengthen a save's wait, and SE:938's "outside the bound" over-covers it harmlessly. A header takes the separate path at SE:1030-1054, and the zeroing is that path's own page.
6. **Docs workflow:**
   - **My runs** (`receipts/gates/`, `receipts/gates_summary.tsv`): 23 commands in a pinned-renderer venv (cmarkgfm 2025.10.22, html5lib 1.1, PyYAML 6.0.3), all rc 0: `docs_check.py` 0 findings over 213 pages; `check_em_dash.py --base 1f29f189` 0 over 1,748 added lines in 7 pages; `check_baremetal_only.py --check` 0 over 1,434 files; `check_doc_paths.py` 1,084 paths; `gen_toc.py --selftest`, `--verify-anchors` (580 links) and `--check`; the doc style, gPTP, DOC_MAP, time-sync, solution, submodule, feature-status, traceability and archive gates; `git diff --check 1f29f189 HEAD`. Each count matches the PR body.
   - **Style on changed blocks** (`receipts/style_touched.txt`): 0 findings over the 7 pages.
   - **Author receipts:** all 50 rc files record 0, including both builder legs, the RV32 SDK, CI events and the act-runner contract. I did not re-run the submodule, SDK or builder steps, because the delta has no file they scan.

### Commit shape, comment rule and privacy

- **Commits:** three one-line subjects, no bodies or trailers. The first-parent count from `e5b8405d` is 34, as the PR body says.
- **Comment rule:** no source file is in the delta, so no new instance is possible. SE:1207's link targets carry review labels in their paths, on a design page rather than a source comment, in the existing link form.
- **Privacy:** a search of the added lines finds no private path or host.

### Evidence integrity (`receipts/evidence_integrity.txt`)

- **Manifest:** `MANIFEST.json` at `cf94dfd2` lists 113 `author-r5` files. All match their published digests, with none missing and none unlisted.
- **SHA256SUMS:** 98 of 110 entries verify. The 12 that do not are exactly the path-redacted evidence files the manifest flags. The receipt's "not path-redacted" line lists them only because of a `./` prefix in my comparison; its last line lists the redacted set.
- **Live PR body:** equals the packet's PR-BODY.md apart from a trailing newline.
- **Signature:** the hosting service reports evidence commit `cf94dfd2` as unsigned. I verified the packet by its digests, not by a commit signature.

## Lens results

```text
[R757] PASS Conformance - SE:611-617, :632-635, :654-660, :1176-1180 and FR at this head - TU-1 to TU-5 and the clean-copy statements against the repository's records of IEEE 1722-2016 4.4.4.6, 4.4.4.7 and Milan v1.2 4.4.2.3, 5.3.8.10, Annex D; no tu claim in FR
[R757] PASS RTL - SE:637-674, :744-746, :816-822, :833 at this head - rules against the map, head, counters and register tables, by scripts/check_regmap_r5.py and scripts/probe_clean_rules_r5.py
[R757] PASS Robustness - SE:1176-1204, :937, :975, :1030-1054 at this head - malformed-time, loss, jump, restart and start cases against the round-4 probes; save and read-back paths against their tables; S8 and S9 recorded
[R757] PASS Tests - SE:1148-1149, :1167, :1176-1204 at this head - each failing condition is checkable; receipts/probe_clean_rules_r5.txt fails both named mutations; receipts/gates_summary.tsv; author-r5 rc files and digests
[R757] PASS Docs - SE, AP:276, the live PR body at this head - receipts/gates/, receipts/style_touched.txt; removed names and rule numbers searched; residue RR8 to RR10 recorded
```

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | SE:611-617, :632-635, :654-660, :1176-1180; FR redundancy and traceability lines; `docs/design/MEDIA_CLOCK_FOLLOWING.md:132`, :666; `docs/design/GM_LOSS_RECOVERY.md:156-308`, :333 | R757-5 | 270866ecb95155ef48428ec3a049c357f7eae946 |
| RTL | CLEAN | SE:596-674, :744-746, :816-822, :833, :851-852; `receipts/regmap_r5.txt`; `receipts/probe_clean_rules_r5.txt`. Registers and logic the delta does not touch keep their R757-3 result | R757-5 | 270866ecb95155ef48428ec3a049c357f7eae946 |
| Robustness | CLEAN | SE:1176-1204 against each R757-4 probe; SE:937-938, :975-976, :1008-1009, :1030-1054, :1066-1085; `receipts/probe_clean_rules_r5.txt` (S8, S9) | R757-5 | 270866ecb95155ef48428ec3a049c357f7eae946 |
| Tests | CLEAN | SE:1148-1149, :1166-1167, :1176-1204; the row's mutations re-derived in the probe; 23 gates re-run (`receipts/gates/`); author gate receipts and digests (`receipts/evidence_integrity.txt`); hosted check snapshot (`receipts/hosted_checks.tsv`) | R757-5 | 270866ecb95155ef48428ec3a049c357f7eae946 |
| Docs | CLEAN | SE delta; AP:276; live PR body, Round 3 to Round 5 and known limitations; `receipts/style_touched.txt`; em dash, TOC, anchor, path and bare-metal gates; RR8 to RR10 | R757-5 | 270866ecb95155ef48428ec3a049c357f7eae946 |

## Prior external findings (R758-4), resolved at this head

See "Order of reading" above for when I read these (issuecomment-6555558017).

| R758-4 item | At this head |
|---|---|
| F1 MINOR, tu on both | **Resolved by the reduced text.** SE:711, :721 and :723-738 are gone. (a) Own-time skew is cases A, B and C, with its -2.5 ms and -1.9 ms and its ±1 ms at the default latencies. (b) Arrival margin is case H, with its four margins. (c) Networks clearing apart is case I, with its three steps and 80 packets. TU-5 makes each size lane 6's output |
| F2 MINOR, "cannot make one" | **Resolved.** The sentence is gone. TU-4 and case G carry the start, and case K's unpaired arm carries its -40 jump |
| R1 RESIDUE, mutation count | **Resolved** in the PR body (line 137). The round-4 handoff stays as published, which is acceptable for a published packet; the round-5 handoff records the correct count |
| R2 RESIDUE, "the only valid copy" | **Resolved.** SE:650 is its first sentence exactly. Its second sentence names rules that are gone. Its 318-sample case is in case E |
| S1 | **Not taken, with a stated reason:** requirement text waits for owner approval. Optional, so nothing is retained |
| S2 | **Partly taken:** case L has the clean partner losing frames. The restart signal stays with the lane under TU-3 |
| S3 | **Not taken, with a stated reason.** Optional, so nothing is retained |
| Carried R757-3 S1, R758-3 S3 | **Not taken** in earlier rounds, for reasons already accepted |

One link to my own findings: F1(b) found the lapse for tu references, and S9 is the same lapse on clean copies. Case H has only tu arms, which is why S9 points at item 1.

Earlier rounds' findings were recorded as closed in R757-4 and R758-4, and this delta does not reopen them.

## Real limits

- **Not re-run:** the submodule-dependent docs-workflow steps (HDL reference, RV32 SDK, builder legs, code ratchets, NVM, CI events, act contract). The clone has no submodules checked out. The author's published receipts at this head are the source-head evidence for them.
- **Hosted runs** (`receipts/hosted_checks.tsv`, 2026-11-01 09:45 UTC): 19 completed successfully, 22 skipped, 3 in progress (`docs-gates-0`, `docs-gates-2` and one fail-fast context). `docs-gates-1`, `docs-check-no-git`, `wire-accountability`, `rtl-fast`, `elaborate`, `bdd-conformance` and `full-ci-gate` had succeeded. Skipped contexts are not executed evidence.
- **Standards:** no clause text was opened this round. IEEE 1722-2016 and Milan v1.2 are checked against the repository's own records of them and the quotations in the author's handoff.
- **Probes:** every result comes from a page-derived model, not an implementation. S9's figures come from a chosen stress arm and measure no real talker. The exact-compare mutation is a crude form of that mistake.
- **Not used:** hardware, bench, act, a hosted re-run and the builder bank. Physical calibration was not run, and field skips are not hardware proof.
- **Manager bank:** no manager source bank ran at this head, and this round claims none.
- **Clone state:** the clone equals HEAD. The index tree is `6d63bab0`, the worktree is clean, and the six gitlinks are unchanged. One ignored `scripts/__pycache__/`, created by this round's style check, was removed (`receipts/clone_integrity.txt`).

## Pending manager duties

- Accept the hosted `docs-check` at this head, once `docs-gates-0` and `docs-gates-2` complete with all three legs executed.
- Accept `verilator-suites` and `yosys-portability` as skipped contexts for a documentation-only head.
- Validate the current-dev merge candidate at the merge turn, with the builder and native banks. Source base and live dev are both `1f29f189`.
- Get owner approval of the requirement text, and of the open owner decisions in the area plan.
- Carry RR8, RR9 and RR10 to the residue checklist, and S9 to lane 6.

R757-5 FINISHED
