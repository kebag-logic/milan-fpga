[R758] POSITIVE - exact head 20933ef48a9b174e58a9d17ddd59078a072024af

Round R758-8, issue #640 / PR #828, documentation only. Tree `2299420e70cea4ce2dcb0450c5ff0fbb56bbf9f0`. Delta reviewed: `e7310e94..20933ef4`, two commits, three pages, +45/-7. Authority for the delta: the owner decisions of 2026-11-01 (#640 comment 6558021030), the manager's ruling on R757-7-F1 as assigned to this round, R757-7-F1 and R758-7-R1.

Result: no BLOCKER, MAJOR or MINOR. Two new RESIDUE items and two SUGGESTIONS. One prior RESIDUE item (RR13, the manager's) is retained. That the fewer-reservations maximum is not derived here is by ruling and is not a finding.

File keys: FR = `docs/reference/FR_NFR.md`, SE = `docs/design/MARK_II_STREAM_ENGINES.md`, AP = `docs/design/MARK_II_AREA_PLAN.md`. Line numbers are at the exact head.

## Findings

### R758-8-R1 RESIDUE - Docs - SE:450-451 - "may be low" understates what is public and gives only part of the reason

- **Authority/evidence:** the page says "Its 192 kHz search left out eight-channel streams. So that row may be low." The row is low, not possibly low. Three cases reach more, each through the model's queue recursion and 8.6.8.2 simulation:
  - R758-7 S1, eight-channel in phase 3, one-channel in phase 6: 106.927 µs before the packetizer term.
  - This round, with no eight-channel stream at all: six-channel in phase 0, one-channel in phase 1, wait 94.357 µs, 112.450 µs before the packetizer term. So the omission of eight-channel streams is not the whole reason. That search was also a random walk.
  - This round, eight-channel in phases 0 and 1, one-channel in phase 2: wait 103.331 µs, 121.424 µs before the packetizer term.
- **Why RESIDUE:** the row's own figure is correct and reached. SE:438-439 already says no row is a maximum, and open design item 4 covers the case. No figure, grade or claim changes, and the sentence is true as far as it goes.
- **Impact:** a reader may take the 192 kHz row as near the rate's largest case when it is about 19 µs below a known one.
- **Exact fix, adding no figure:** replace SE:450-451 with "Its 192 kHz search was a random walk." "It left out eight-channel streams." "Larger cases exist, so that row is low."
- **Verification:** read the lines; `receipts/probe_r8_delta.out` parts C and E.

### R758-8-R2 RESIDUE - Docs - AP:60, AP:255, PR body line 27 - fewer reservations read as never meeting 65 µs

- **Authority/evidence:** AP:60 says "not met with fewer reservations", AP:255 says "exceeded by fewer reservations", and the PR body says "With fewer reservations it does not either". SE:400 says "some cases exceed it", and SE:418 has a fewer-reservations row at 40.325 µs marked Met.
- **Why RESIDUE:** the delta carried the wording forward. It changes no figure or grade, and FR:306 does not repeat it.
- **Impact:** none on a measurement. A bench reader could expect every fewer-reservations case above 65 µs.
- **Exact fix:** AP:60 "not met by some cases with fewer reservations"; AP:255 "exceeded by some cases with fewer reservations"; PR body line 27 "With fewer reservations some cases exceed it, and no maximum is derived".
- **Verification:** read the three lines against SE:400 and SE:418.

### R758-8-S1 SUGGESTION - Tests, Docs - SE:1221 - item 4 could name the other port at 192 kHz

Item 4 speaks of reservations "on a port", but at 192 kHz the packetizer is a shared queue, so the total depends on the other port's placement. Under the model's queue, phases 2, 3 and 4 give 129.745 µs with the same placement on both ports and 125.584 µs with the other port at 14 eight-channel streams (`receipts/probe_r8_delta.out` part C). "Every placement" can be read to include this, so nothing is wrong. Adding "on both ports" would settle it.

### R758-8-S2 SUGGESTION - Docs - SE:1221, FR:306 - "16 reservations" counts AAF streams, which the sentence does not say

The derivation means 16 AAF reservations with an optional CRF as the 17th stream (SE:80, SE:331, SE:384). A port with 15 AAF streams and a CRF has 16 reservations by plain count, but no table row was derived for it. Item 4 says "with and without a CRF", so the case is owned. "Fewer than 16 AAF reservations" would stop a lane grading it against the 16-reservation table.

## Assigned checks

| # | Check | Result | Evidence |
|---|---|---:|---|
| 1 | NFR-LAT-03 reads as ruled and applies to every case | Holds | FR:306: SHOULD, priority S, 65 µs a target; "The bench measures every case against the target and reports it; a case above 65 µs is reported, not failed"; graded "only where one is derived, which is the 16-reservation table"; a measurement above it "is a finding"; no maximum derived for fewer reservations; the lane owes it; 143.347 µs "quoted as reached, not as a limit"; no connection refused. Case walk: 16 AAF with one format or mixed at 48, 96 and 192 kHz has a table row to grade against. Sixteen eight-channel streams at 192 kHz exceed 75 % (SE:84-88), so that case falls in the fewer-reservations class or in the mixed row. Every other case is reported and ungraded. No case is undecided. SE:230-243 says the same. `SE_TLAT_OVER` (SE:479, SE:793-794) counts frames at or above 65 µs and fails nothing |
| 2 | New table: each case and witness reproduces; none called a maximum | Holds | All four rows replayed from the page's own words under the page's rule, in an implementation independent of the model: placements, waits and totals match to three decimals, and the model's recursion and 8.6.8.2 simulation agree (`probe_r8_delta.out` part A). Peak 16, 3, 15 and 6 streams. The fixed terms at SE:444-445 match SE:322 and SE:393-394. SE:438-439 "The rows of both tables are examples. None is a maximum." The linked probe and output are pinned, resolve, and match the published files byte for byte. The output lists all four totals. The search does omit eight-channel streams at 192 kHz. Wording: R758-8-R1 |
| 3 | Open design item 4 verifiable | Holds | SE:1221 names the rates, every reachable placement and base format, with and without a CRF, and eight-channel at 192 kHz. It requires a stated method, exact or superset. Its failing condition is any table case exceeding the result, in the recursion or the simulation, and both exist in the model. It adds a bench case at the largest placement and a citation back into NFR-LAT-03. AP:276 carries the open design items as lane 6's evidence. Feasibility: this round scanned all three rates in minutes. Suggestions: R758-8-S1, R758-8-S2 |
| 4 | 123.337 µs not worst case; no "published bound" for a class without one | Holds | Only SE:416 carries 123.337 µs in the repository, a row now under "None is a maximum". The PR body names it only as the figure the owner saw. "Published bound" appears in no PR page. The PR body has it only where it quotes round 7's replaced sentence (lines 192, 201). FR:306, SE:230-231, SE:398, AP:60 and AP:255 limit "accepted" to 16-reservation or mixed-format bounds |
| 5 | R758-7-R1 applied; area plan and PR body agree | Holds | AP:276 "Talker latency taps on all talker streams, measured against the 65 µs target". The wording differs from R1's exact text ("reported against") but closes its impact, and the sentence's other half is at FR:306. AP:60, AP:255, PR body lines 27, 98, 205-212 and the known limitation agree with FR:306. Wording: R758-8-R2 |
| 6 | Nothing else changed; docs gates pass | Holds | Three pages, modes unchanged, gitlinks unchanged, one-line subjects with no trailers. The first fewer-reservations table and the 16-reservation table hash the same at both heads. Own gate runs, all rc 0: doc links (0 findings, 213 pages), doc style, cited paths (1084), feature status, contents self-test, contents check and anchors, em dash (0 over 1792 added lines), style on the touched pages' changed blocks. `git diff --check` from the base: rc 0. Author's 50 gate rc files all read 0, as listed in the published packet |

### Is 143.347 µs still the largest figure reached?

FR:306 says it is, so this round tried to falsify it. It survives. These are not ceilings.

| Rate | Largest case found | Wait | Total | Largest row on the page |
|---|---|---:|---:|---:|
| 48 kHz | Six one-channel in phase 0 | 103.022 µs | 143.347 µs | 143.347 µs |
| 96 kHz | Two eight-channel in phase 0, four one-channel in phase 1 | 103.570 µs | 136.061 µs | 125.426 µs |
| 192 kHz | Eight-channel in phases 0 and 1, one-channel in phase 2 | 103.331 µs | 121.424 µs before the packetizer; 129.745 µs in the model's queue | at least 102.034 µs |

- Each case passed an operation-level replay of starts and stops under the rule, with at most 16 AAF streams and one CRF.
- The 192 kHz case needs the CRF as a scaffold. Its witness is: start eight-channel, seven one-channel, eight-channel, six one-channel, a CRF, one one-channel; stop all but phases 0, 1 and 2.
- Scan coverage is in the limits below. The rows on the page remain correct as examples, and the higher cases are item 4's business. They are offered as starting cases for lane 6, not as a request to add figures.

## Prior findings

Read after this round's own verdict and ledger were recorded in the report file.

| Finding | State at this head | Evidence |
|---|---|---|
| R757-7-F1 MINOR | Resolved, outcome (b) | FR:306 and SE:230-243 state no fewer-reservations bound is derived and name who derives it; rows are examples (SE:438-439); a case above 65 µs with no bound is reported, not failed; no connection refused. The form at SE:423-426 names equal frames, no largest k. Its re-run probes match the published outputs byte for byte and each witness falls under the stated rule. The owner notice it asks for is recorded in #640 comment 6559636145 |
| R758-7-R1 RESIDUE, R757-7 RR12 | Resolved | AP:276 |
| R757-7 RR13 RESIDUE, issue body | Retained, the manager's | Issue body lines 30 and 36 still read "the 65 µs target" as binding |
| R757-7-S1 | Resolved | SE:1221 names the bench case |
| R757-7-S2 | Retained, optional | Out of the delta |
| R758-7 S1 | Resolved by ruling | FR:306 covers the case; SE:1221 owes the ceiling. Its statement that its search does not exceed 123.337 µs is superseded by 143.347 µs |
| R758-7 S2 | Resolved | FR:306's last sentence |
| R758-7 S3 | Retained, optional | AP:270 unchanged |
| R757-6 S14 to S16, R758-6 S1 to S4 | Retained, optional | Delta does not touch them |
| Findings of earlier rounds | As R758-7 recorded them | Delta does not touch their text |

## Lens results

```text
[R758] PASS Conformance - FR:306; SE:227-243; AP:60, 255, 276 - read against the owner decision and the ruling's six rules; every case classed as graded or reported
[R758] PASS RTL - git diff --raw e7310e94 20933ef4: three Markdown pages, no RTL, generator or register change; SE:793-794 still only counts; earlier RTL lens verdicts keep their standing
[R758] PASS Robustness - SE:431-436, SE:1221; receipts/probe_r8_delta.out - boundary cases: 16-stream cap, 75 % cap, CRF as scaffold, largest reached at each rate, no case above the quoted figure
[R758] PASS Tests - receipts/probe_r8_delta.out; rerun_*.out; gate_*.rc - each row replayed independently and through both model calculations; published probes re-run byte-identical; item 4's failing condition checked against what the model can compute
[R758] PASS Docs - FR:306; SE:227-243, SE:405-451, SE:1221; AP:60, 255, 276; PR body; gate_*.log - stale-figure and stale-phrase search over all PR pages, anchors and pinned links; residue R758-8-R1 and R2 recorded with exact fixes
```

## Ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | FR:306; SE:227-243; AP:60, 255, 276; #640 comments 6558021030, 6559636145 | R758-8 | 20933ef48a9b174e58a9d17ddd59078a072024af |
| RTL | CLEAN | `git diff --raw e7310e94 20933ef4`; SE:479, SE:793-794; docs only, no RTL in the PR diff | R758-8 | 20933ef48a9b174e58a9d17ddd59078a072024af |
| Robustness | CLEAN | SE:431-436, SE:1221; `receipts/probe_r8_delta.out` | R758-8 | 20933ef48a9b174e58a9d17ddd59078a072024af |
| Tests | CLEAN | `scripts/probe_r8_delta.py`; `receipts/rerun_*.out`; `receipts/gate_*`; published packet receipts | R758-8 | 20933ef48a9b174e58a9d17ddd59078a072024af |
| Docs | CLEAN, residue R758-8-R1 and R2, RR13 retained | FR:306; SE:405-451, SE:1221; AP; PR body; `receipts/gate_*` | R758-8 | 20933ef48a9b174e58a9d17ddd59078a072024af |

## Real limits

- **Delta review.** By the assignment, only the delta and the author's round 8 packet were judged. Earlier rounds were not re-opened, and nothing in the delta broke them.
- **The search is not a proof of a ceiling.**
  - 48 kHz: phase contents up to 6,192 bits (the page's limit) were scanned over windows of one and two phases, CRF included. Three or more phases stay under 83.333 µs of wait.
  - 96 kHz: contents up to 7,200 bits over one and two phases. Three phases were limited to seven streams. Three or more phases stay under 104.167 µs, below the 110.856 µs needed to pass 143.347 µs.
  - 192 kHz: one stream per phase within the first 17 tie phases, windows up to seven phases. The other port was tried in only two placements: the same placement, and 14 eight-channel streams.
  - The reach test uses eight-channel scaffolds, which is sufficient to show reach. A failure to reach is not a proof of unreachability.
- **"Reached" totals add the page's fixed terms in full, estimates included**, as SE:441-442 discloses. A case's own packetizer load can be less than the term. The wait is what is reached under the rule. Nothing here is a measurement.
- **Gate evidence.** Own runs cover the Markdown gates only. The remaining steps rest on the author's published receipts, for the head named in the packet. No manager source bank runs at this head and none is claimed or inferred.
- **Packet digests.** `author-r8/evidence/SHA256SUMS` digests the originals. Sixteen published copies differ from it because publication redacted local paths. The publication manifest's published digest matches all 119 published files, and its original digest equals SHA256SUMS for all 116 listed files.
- **Independence.** The R757-7 probe and output are linked from the page under review, and the author's packet quotes R758-7 S1; both were read during this round's own pass. The two reports were read only after the verdict and ledger were recorded.
- **Hosted evidence.** At the time of reading, 20 contexts passed, 2 were pending and 22 were skipped. Skipped contexts are not execution. No acceptance is inferred.
- **Hardware.** Physical calibration NOT RUN. No bench, no hardware, no field evidence.
- **Comment rule.** The delta touches no source comment, so it has no instance to judge.

## Pending manager duties

- Carry R758-8-R1, R758-8-R2 and RR13 to the residue checklist.
- The owner has not answered the 14:52 notice recorded in #640 comment 6559636145, and the decision can still be revisited.
- The owner's decision text still accepts bounds "for fewer reservations", and the owner's approval of the requirement text was given as reviewed at `3f5fea24`. NFR-LAT-03 has since changed under that decision and under the ruling. Whether the approval needs restating for the row as it now reads is the manager's call.
- Hosted and local-replica acceptance at the exact head, the merge-turn candidate build and its banks, and post-merge containment.

## Probes

Disposable and repeatable: `python3 -I scripts/probe_r8_delta.py <mixed_stagger.py>`. The model is `review-evidence/640-m9-r1/author-r3/evidence/model/mixed_stagger.py` at `f1215a16b6dc2da15a89ec377931cf89d1e77a33`, digest in `receipts/model_sha256.txt`. The clone stayed at exact head: clean status, tree `2299420e`, tracked blobs and modes unchanged, gitlinks in `receipts/gitlinks.txt`. No source edit, commit, push or GitHub write was made.

R758-8 FINISHED
