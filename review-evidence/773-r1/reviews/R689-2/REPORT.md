[R689] NEGATIVE - exact head 1b47a3dcff0cb65cb5cebe1f86327429a76f775d

# R689-2: internal cleared-context review of PR #779 (issue #773), round 2

- **Head:** `1b47a3dcff0cb65cb5cebe1f86327429a76f775d`, tree `f608aefd73bbc007624782653182d0a6f85c8825`. This is the PR head at review time (`receipts/public_state.txt`).
- **Previously reviewed head:** `13d8f1e84920aac1dc3e76fb6406c44a744d8145` (R689-1, R690-1).
- **Base:** dev `a032c6d6e3775f145349d5a495c1e1ad12294936`, which is also live dev.
- **Delta:** two commits, `e85f86a2` and `1b47a3dc`. They touch three files: `docs/design/MEDIA_CLOCK_FOLLOWING.md` (+58/-14), `docs/reference/MILAN_COMPLIANCE_MATRIX.md` (row 191) and `hdl/ieee1722/crf/KL_media_domain_event.sv` (header comment only).
- **Reconstructed from:**
  - AGENTS.md and CONTRIBUTING.md;
  - issue #773's body, ruling (b) (`issuecomment-6380110812`) and the round-2 REVIEW READY (`issuecomment-6384707314`);
  - the round-2 assignment (`issuecomment-6383506324`);
  - my own R689-1 report and R690-1's report (both read for the focus, as the assignment directs);
  - the PR body (`receipts/pr_body_snapshot.md`);
  - `git diff 13d8f1e8..1b47a3dc` and the full `a032c6d6..1b47a3dc` log;
  - the public evidence tree `review-evidence/773-r1` at `1faf10a1`, chiefly `author-r2/receipts/round2/`.
- **Evidence integrity:** all 481 published hashes in `MANIFEST.json` verify. No file is unlisted (`receipts/evidence_manifest_verify.txt`).

**Verdict:** NEGATIVE, on one open MINOR (F1, Docs). One sentence in the corrected page, repeated in the PR body and the REVIEW READY, says the start-up bound is measured "in every 2 ms run". The cited log shows it in 9 of 23 runs. Every figure the delta adds recomputes exactly, and the bounds themselves are correct. Conformance, RTL, Robustness and Tests are clean at this head.

## Answers to the review focus

### 1. R689-1-F1 and R690-1-F1: the two bounds

I rebuilt every figure with my own exact-rational script, `scripts/check_bounds.py`. It is independent of the author's script. It also requires each figure to appear verbatim in the page. Result: 53 checks pass and one page sentence fails (F1). Receipt: `receipts/check_bounds.txt`.

- **Grid live (zero transit, 2 ms):**
  - Earliest hand-over after the frame's instant: 127,991 ns (1x1), from 6 Ps + 131 ns + (86 + 57) cycles. At 8x8 it is 112,275 ns, from 6 Ps - 15,525 ns + (83 + 57) cycles.
  - Arrival lead: 2,038,676 / 2,054,392 ns.
  - Last event after arrival: 2,142,843 / 2,158,559 ns.
  - Margin: 513.3 / 492.4 us.
- **Start-up (base is the live PHC at the first pair):**
  - The hand-over comes at least 5,343 cycles (106,860 ns) after the base: 5,208 (the floor of five 1,041.67-cycle spacings) + 78 (3 x 26) + 57.
  - Arrival lead: 2,059,807 ns at 2 ms and 184,807 ns at 125 us.
  - Last event after arrival: 2,163,974 ns.
  - Margin: 492.1 us (1x1, against 2,656,119 ns) and 487.0 us (8x8, against 2,650,942 ns).
  - This rests on the RTL: `milan_datapath.sv:7230` selects the live PHC whenever `dom_live_w` is low, and `:7212` drops liveness after four frame periods without a marker. The page states both conditions.
  - The 57 cycles for talker 0 and 60 for the others match `KL_aaf_packetizer.sv:237-246`, where E_CRD_S's three CFG reads apply to a talker above 0.
- **Both bounds sit inside 4.4.2.1's 2.126 ms.** The 2 ms default still fits with margin, so no STOP condition holds.
- **Measured against the bound:**
  - All 23 of the sweep's 2 ms `[HOLD]` maxima are at or below 2,059,807 ns. All 8 at 125 us are at or below 184,807 ns.
  - Nine 2 ms runs reach 2,059,807. The other 14 read 2,059,787, which is the same bound one cycle later (a 5,209-cycle five-spacing; the script reproduces it). See F1.
- **Equation (1) lead ceiling:** 106,860 + 125,000 = 231,860 ns. The page's "up to 231.8 us" errs on the safe side, and the 166.7 us lead is below it.
- **Supported range, counting this talker's 8 Ps:**
  - The queue's lower and upper limits recompute: 31,119 / 2,656,119 ns (1x1) and 25,942 / 2,650,942 ns (8x8).
  - Transit bounds: 2,135,548 / 2,140,725 ns.
  - First-event offset bounds: 2,489,452 / 2,484,275 ns plus the transit.
  - Whole six-event PDU: 2,385,285 / 2,380,108 ns plus the transit.
  - The direction of each bound is right. The late rule binds the first event (smallest lead), and the queue's depth binds the last event.
- **Drift:** five periods at 1,000 ppm is 104 ns.
- **Compliance matrix row 191:** it states both bounds and both shapes. It names "the `[HOLD]` maximum measured at 1x1", which is true as a maximum over runs.
- **Restatements:** a repository-wide search finds no other stale restatement of 513.3 / 492.4 us, 1,968,881 ns or 237 us.

### 2. R690-1-F2: the full four-shard sweep at this exact head

`author-r2/receipts/round2/sweep/` binds everything the finding asked for:

- per shard, the runner command line and its exit code (0 in all four), in `results.json`;
- each clone's head and tree (`1b47a3dc` / `f608aefd`) and its submodule pins, in `clone_identity.txt`. The pins equal the head's gitlinks;
- each suite's verdict, in `runner.txt`, and a size-and-hash manifest of every suite log;
- the union, in `SUMMARY.txt`: 64 suites run, 64 expected from `run_all_suites.sh --list`, none missing, none run twice, none failing, none timed out;
- check totals: 55,301 + 331,530 + 262,473 + 1,541,583 = 2,190,887.

Spot checks of the excerpts:

- capture_coherence 20,832/0, its dp leg 847/0 and its mutation arm 42/42, with the seven #773 controls each caught;
- aaf-start 34,020/0, with startup mutants 8/8;
- milan_dp, whose excerpt has no non-zero failure count.

Shard 0's clone reports `tracked changes: 2`, collected after the run. That shard holds `tsn_fuzz`, which rewrites the timestamped `hdl/ieee1722/avtp/doc/TEST_RESULTS.md` and `hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md` (`tb/verilator/tsn_fuzz/Makefile:207-218`). `scripts/run_all_suites.sh:86-90` documents that behaviour. So this is expected and not a finding, but the receipt does not name the files (S2).

The PR Status section claims only what ran, each row at the head it names. It says outright that hosted contexts are not claimed. Its rows match the receipts: sweep, behave, lint, the three named docs gates, the docs workflow (41 pass, 2 skipped, em-dash direct with 0 findings), the strip compare, and the carried rows at `13d8f1e8` and `bf2d96f9`. **Resolved.**

### 3. R689-1-R1: the domain event's header comment

`KL_media_domain_event.sv:29-33` now reads exactly the wording I gave.

- My own string-literal-aware stripper finds the file at `13d8f1e8` and at `1b47a3dc` identical once comments are stripped (sha256 prefix `44402151923313a6` both), while the raw bytes differ. The author's receipt agrees.
- The whole `hdl/` delta is those eight comment lines (`receipts/r1_comment_strip.txt`).
- The new comment names only #773 and #632, with no lane label, round or reviewer ID. So no new comment-rule residue. **Resolved.**

### 4. R689-1-S2: the MAC-level figures at 1 Gb/s

Every figure recomputes (`receipts/check_bounds.txt`, MAC section):

- **Frame sizes.**
  - A maximum tagged frame is 1,522 + 8 + 12 octets, which is 12,336 ns at 1 Gb/s and 123,360 ns at 100 Mb/s.
  - The CRF PDU, with one timestamp, is a minimum 64-octet frame: 672 ns on the wire.
  - The 8-channel AAF PDU is 238 octets: 2,064 ns on the wire.
  - The gasket is 512 cycles, 10,240 ns, shorter than one maximum frame on the wire.
- **One frame ahead at the MAC.** The spare less 12,336 ns leaves 5,480 / 6,576 ns (AAF) and 8,167 / 2,990 ns (CRF).
- **Store-and-forward.** The maximum frame takes the arbiters first (190 beats), then the other output's PDU, then this PDU.
  - The egress shift against uncontended egress is 3,800 + 12,336 + 672 - 600 = 16,208 ns for AAF, and 3,800 + 12,336 + 2,064 - 160 = 18,040 ns for CRF.
  - That leaves 1,608 / 2,704 ns (AAF) and 2,463 ns (1x1 CRF), and puts the 8x8 CRF PDU 2,714 ns past stamp - offset.
  - Under round-robin `crf_dp_mux`, a second AAF PDU cannot pass a pending CRF PDU. I checked whether an 8x8 AAF burst backlogged in the MAC FIFO behind the frame could be worse. It is not: the CRF PDU's own uncontended baseline moves later by the same amount. So 18,040 ns is the worst case for one maximum frame.
- **Judgement on the 8x8 CRF corner: not a Conformance finding. It lies outside the ruled boundary.**
  - IEEE 1722-2016 4.3.3 Equation (1) constrains TT, the transfer of the AVTPDU to the network interface. Ruling (b) and the page fix that point at the datapath's MAC transmit port. There the 8x8 CRF PDU is handed over with 15,326 ns of spare, against an arbiter wait of at most 4,400 ns.
  - The MAC's store-and-forward FIFO and its line-rate egress come after TT. A maximum interfering frame on the talker's own port is part of the transit that Max Transit Time and the stream's reserved latency carry. Equation (1)'s TT bound does not.
  - The shipping shape is 1x1, where the corner leaves 2,463 ns.
  - The page states the corner, and its "Not covered" list names the cases left open. I add only a wording SUGGESTION (S1) and a manager duty: decide whether the second 8x8 TC period the REVIEW READY mentions gets its own Issue.
- The assignment's three S2 asks are all present: 12.3 us of the spare, what remains for each output and shape, and that 100 Mb/s is not covered. **S2 taken.**

### 5. Gates at this head

These ran in a disposable clean clone of this head (`receipts/gate_clone_identity.txt`; tracked changes 0 before and after):

- **lint:** `python3 scripts/lint_rtl.py --check` gives 89 <= 89, PASS, rc 0 (`receipts/gates/lint.*`), with the verified pinned Verilator 5.050 (`receipts/gates/tool_versions.txt`).
- **behave:** `cd tests && behave --no-capture -f plain` gives 14 features, 406 scenarios and 1,977 steps passed, rc 0.
- **docs_check.py:** 0 findings, rc 0.
- **check_doc_style.py:** OK, rc 0.
- **gen_toc.py --check:** OK (149 pages), rc 0. It ran under a private venv with the hash-pinned `tools/markdown/requirements.txt` renderer. The first attempt, without that renderer, refused with rc 2; that receipt is kept as `*.no_renderer.*`.
- **check_em_dash.py --base a032c6d6:** 0 findings over 198 added lines, rc 0.

These are my runs under GNU Make 4.4.1. The author's receipts under GNU Make 4.3 also show rc 0, and their 44-step docs workflow shows 41 pass, 2 skipped by rule and the em-dash step run directly. I accept those as the make 4.3 evidence.

**Round-1 code coverage carries over.** `git diff 13d8f1e8..1b47a3dc -- hdl tb sw scripts configs` is the comment edit alone. The full sweep re-ran at this head anyway.

## Findings

### F1 — MINOR — Docs — "in every 2 ms run" misstates the measured `[HOLD]` maxima

**Where:**
- `docs/design/MEDIA_CLOCK_FOLLOWING.md:1885-1886`: "`capture_coherence`'s datapath leg measures that `[HOLD]` maximum in every 2 ms run."
- The PR body's Round 2 section: "That bound is 2,059,807 ns at both shapes, the `[HOLD]` maximum measured in every 2 ms run."
- The REVIEW READY `issuecomment-6384707314`: "2,059,807 ns is the `[HOLD]` maximum in every 2 ms run."

**Authority:** AGENTS.md section 6, Docs (the docs must reflect the contract, and the PR and Issue must carry accurate evidence for a cold reviewer). The evidence is the published sweep excerpt `author-r2/receipts/round2/sweep/excerpts/capture_coherence.txt`.

**Evidence:**
- The 2 ms `[HOLD]` maximum is 2,059,807 ns in 9 of 23 runs: DP-INT-slow, DP-INT-fast, DP-CRF-0, -1, -2, -3 and -5, and DP-band-true+2 and +4.
- It is 2,059,787 ns in the other 14 runs: DP-CRF-4, -6 and -7, and DP-band-true-20 through +0.
- At 125 us it is 184,807 ns in 5 of 8 runs.
- The difference is the start-up PDU's five tick spacings falling at 5,209 cycles rather than 5,208. That agrees with the page's "at least 5,343 cycles".
- My own R689-1-F1 text ("The cited leg measures `[HOLD]` at 2,059,807 ns in every 2 ms run") made the same misstatement. That is where this sentence came from, and I correct it here.

**Impact:** the bound and every figure are right. The sentence still states a test result the log contradicts for 14 of 23 runs. It is the page's only measured anchor for the start-up bound, so a cold reviewer reconciling the page with the log (R690-1-F1's own verification method) finds a false measurement claim.

**Why MINOR and not RESIDUE:** it misstates a measurement, which is outside the wording-only rule.

**Required outcome:** the page, the PR body and the REVIEW READY's restatement say what the log shows. For example, at the page: "`capture_coherence`'s datapath leg reaches that bound: its largest 2 ms `[HOLD]` maximum is 2,059,807 ns (9 of its 23 runs; the others 2,059,787 ns, a cycle later)." The REVIEW READY needs a correcting comment, because the original text is history.

**Verification:**
- `python3 -I scripts/check_bounds.py <checkout> <capture_coherence log>` passes 54/54 at the corrected head, including its sentence check.
- `docs_check.py`, `check_doc_style.py` and `gen_toc.py --check` pass.
- Only the Docs lens needs re-review.

### S1 — SUGGESTION — Conformance, Docs — name the 8x8 CRF corner's reference and its boundary

**Where:** `MEDIA_CLOCK_FOLLOWING.md:1858`, "The 8x8 CRF output's PDU leaves up to 2,714 ns late."

**Suggestion:** say "late" against what, and why it is no Equation (1) failure. For example: "...leaves up to 2,714 ns after its timestamp less the applied offset. That is after the hand-over, Equation (1)'s TT, so it is transit the stream's latency budget carries."

**Optional follow-up:** a separate Issue for a second 8x8 TC period, as the REVIEW READY proposes.

### S2 — SUGGESTION — Tests — name the files behind a shard's tracked-change count

**Where:** `author-r2/receipts/round2/sweep/shard-0/clone_identity.txt:3` (`tracked changes: 2`) and `author-r2/scripts/sweep_receipts.py:45`.

**Suggestion:** record the paths, and a pre-run count. A reader could then confirm that the two files are `tsn_fuzz`'s timestamped TEST_RESULTS rewrites (`run_all_suites.sh:86-90`) and not a dirty tree under test.

### S3 — SUGGESTION — Tests — R689-1-S3 stays open as an option

R689-1-S3 (measure the contended path in one dp scenario) was not taken. It is still optional. A measured contended case would now also anchor the MAC-level figures.

### RES1 — RESIDUE — PR body roles are stale

**Where:** the PR body's "Linked Issue / roles" section, "Internal cleared-context reviewer: `[R<n>]` (to be assigned)" and "External reviewer: `[R<n>]` (to be assigned)".

**Exact fix:** "Internal cleared-context reviewer: `[R689]`" and "External reviewer: `[R690]`".

## Prior public findings at this head

On PR #779 there are no PR reviews and no inline threads. The only findings are those in R689-1 and R690-1 (`receipts/public_state.txt`).

| Finding | Status at 1b47a3dc | Evidence |
|---|---|---|
| R689-1-F1 (MINOR, Docs) | Resolved: both bounds and margins are stated, the range counts the 8 Ps, and the REVIEW READY correction is posted. Its own verification test (stated maximum >= every 2 ms `[HOLD]` maximum) passes. The new sentence defect is F1 above. | `receipts/check_bounds.txt` |
| R690-1-F1 (MINOR, Conformance, Docs) | Resolved in my assessment: grid-live and start-up bounds are derived for both shapes, the matrix is updated, and the margins are recomputed. Its reviewer owns its own re-review. | `MEDIA_CLOCK_FOLLOWING.md:1864-1896`, `MILAN_COMPLIANCE_MATRIX.md:191` |
| R690-1-F2 (MINOR, Conformance, Tests, Docs) | Resolved: a complete four-shard sweep at this exact head, 64/64, with receipts binding commands, head, tree, return codes and results. The PR Status claims nothing beyond. | `author-r2/receipts/round2/sweep/*` |
| R689-1-R1 (RESIDUE) | Resolved: exact wording, and identical after comment stripping. | `receipts/r1_comment_strip.txt` |
| R689-1-S1 (SUGGESTION) | Not taken. It stays optional and does not affect coverage. | — |
| R689-1-S2 (SUGGESTION) | Taken, and the figures are correct. | `receipts/check_bounds.txt` |
| R689-1-S3 (SUGGESTION) | Not taken; carried as S3. | — |

## Clean-lens results

- `[R689] PASS Conformance — MILAN_COMPLIANCE_MATRIX.md:191; MEDIA_CLOCK_FOLLOWING.md:1846-1896,2038-2048; milan_datapath.sv:7212,7230; receipts/check_bounds.txt`.
  - Checked against Milan v1.2 4.4.2.1 (2.126 ms) and 5.3.7.6, IEEE 1722-2016 4.3.3 Equation (1), and ruling (b).
  - Both bounds lie inside 2.126 ms at both shapes.
  - The lead stays below the 231.86 us Equation (1) lower-bound ceiling.
  - The 8x8 CRF MAC corner lies after TT, outside the ruled hand-over boundary.
  - R690-1-F2's sweep is complete.
  - No stamp or RTL behaviour changed since R689-1 covered this lens at 13d8f1e8.
- `[R689] PASS RTL — git diff 13d8f1e8..1b47a3dc -- hdl tb sw scripts configs (KL_media_domain_event.sv:26-33 only); receipts/r1_comment_strip.txt`.
  - The only RTL-file change is comment-only, with the stripped text identical.
  - R689-1's RTL coverage (packetizer, CRF, latency package, datapath #773 block, elaboration probes) therefore stands unchanged at this head.
  - The full sweep at this head passes 64/64.
- `[R689] PASS Robustness — MEDIA_CLOCK_FOLLOWING.md:1879-1896 against KL_media_domain_event.sv:47-52,93-105, milan_datapath.sv:7212,7230; sweep excerpt capture_coherence.txt`.
  - The start-up base (live PHC) and the re-entry condition (four frames without a marker) match the RTL.
  - Both offsets' start-up PDUs stay within Equation (1) and 2.126 ms.
  - The page bounds media-clock drift and the one-cycle tick-spacing variation.
  - There is no behaviour change to re-probe.
- `[R689] PASS Tests — author-r2/receipts/round2/sweep/{spec.json,SUMMARY.txt,shard-*/*,excerpts/*}; receipts/evidence_manifest_verify.txt; receipts/gates/behave.*, lint.*`.
  - The 64/64 sweep at this exact head and tree is verified through its hash envelope.
  - The capture_coherence dp leg 847/0 and mutation arm 42/42 are verified, and the aaf startup mutants are 8/8.
  - behave 406/406 and lint 89 <= 89 are my own runs.
  - No test changed in the delta.
- Docs is UNCLEAN: F1 is open. S1, RES1 and the clean results above are recorded.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | compliance row 191; design page :1846-1896, :2038-2048; Equation (1) ceiling; 8x8 CRF MAC corner against TT; sweep completeness; `check_bounds.txt` | R689-2 | 1b47a3dcff0cb65cb5cebe1f86327429a76f775d |
| RTL | CLEAN | delta `hdl/` (comment-only, strip-identical); R689-1's RTL coverage, unchanged since | R689-2 (delta), on R689-1 at 13d8f1e8 | 1b47a3dcff0cb65cb5cebe1f86327429a76f775d |
| Robustness | CLEAN | start-up/timeout base against `KL_media_domain_event.sv`, `milan_datapath.sv:7212,7230`; per-run `[HOLD]`/`[WIRE]` at 2 ms and 125 us; drift statement | R689-2 | 1b47a3dcff0cb65cb5cebe1f86327429a76f775d |
| Tests | CLEAN | four-shard sweep receipts at head (64/64, hash-verified); dp leg, mutation arm, aaf startup mutants; own behave and lint | R689-2 | 1b47a3dcff0cb65cb5cebe1f86327429a76f775d |
| Docs | UNCLEAN (F1) | `MEDIA_CLOCK_FOLLOWING.md` delta; `MILAN_COMPLIANCE_MATRIX.md:191`; `KL_media_domain_event.sv` header; PR body; REVIEW READY; own docs gates rc 0 | R689-2 | 1b47a3dcff0cb65cb5cebe1f86327429a76f775d |

## Real limits

- **Not re-run by me:**
  - the full Verilator sweep (the author's exact-head receipts, verified by hash);
  - Yosys (60/60 at `bf2d96f9`);
  - the Vivado front end, route-1x1, ooc-1x1 and ooc-8x8 (all at `13d8f1e8`);
  - the tdm8render-mutants, pull-in and gmstep-mutants campaigns (at `bf2d96f9`);
  - the 44-step docs workflow and the builder legs.

  No RTL, test or script byte changed since those heads.
- **Docs gates:** my runs used GNU Make 4.4.1, not 4.3. The make 4.3 evidence is the author's receipts.
- **Derived only:** the 8x8 TDM32 figures and every MAC-level figure. No harness runs 8x8 at its clocks or models the MAC at line rate.
- **Reading order:** I read the round-1 reports (R689-1, R690-1) before the delta pass, because the assignment's focus is defined by them. No other reviewer's round-2 report was read.
- **Hosted:** at 2026-10-24T13:32Z, 8 checks had succeeded, 1 was skipped, 20 were in progress and 16 queued (`receipts/hosted_check_runs.tsv`). Skipped or unfinished contexts are not executed evidence.
- **No manager source bank** exists at this head, and none is inferred.
- **No hardware:** physical calibration NOT RUN. Field skips and desk passes are not hardware proof.

## Pending manager duties

- Carry F1 to the author and re-review the Docs lens at the corrected head. A docs-only correction leaves the other four lenses' scope untouched.
- Carry RES1 to the residue checklist.
- Decide on S1's optional Issue: a second 8x8 TC period, or a measured contended-path scenario (S3).
- Own hosted and act acceptance at the exact head.
- Build and validate the current-dev merge candidate with the builder and native banks, and link its receipts.
- Decide how #773 closes. The PR says "Relates to #773", and AGENTS.md section 7 needs the Issue closed at merge or by hand.
- Obtain both independent positive reviews before any authorized merge. This report authorizes no merge.

## Packet

- **Scripts** (portable; run with `python3 -I`):
  - `scripts/check_bounds.py <checkout> <capture_coherence log>`
  - `scripts/strip_sv.py <repo> <rev-a> <rev-b> <path>`
  - `scripts/verify_manifest.py <evidence root>`
  - `scripts/make_clone.sh <src> <dest> <rev>`
- **Raw receipts:** under `receipts/`.
- **Publication set:** only `REPORT.md` and the files listed in `MANIFEST.sha256` are published.
- **Clone integrity:** after review, the review clone's tracked bytes, modes, index (write-tree = `f608aefd`) and all six submodule gitlinks match the head exactly (`receipts/clone_integrity.txt`).

R689-2 FINISHED
