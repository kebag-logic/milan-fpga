[R758] NEGATIVE - exact head f6b3e841646384177584ce75b657fb8dead7727c

Round R758-2, external independent review of PR #828 (issue #640, with #665 and #823), round-2 delta.
Head `f6b3e841646384177584ce75b657fb8dead7727c`, tree `4bb54f5edd8e777b1b7c13c045a318474e7e0d80`, previous head
`dfc310fb3dec28f3d06333973e61cde44a4e786d`, source base and live dev `e5b8405db4c1f7cbdafb5df92b15b580142e0232`.
Delta since round 1: twelve commits, six Markdown pages, 575 lines added and 281 removed. It changes no code,
generator, gate or configuration.

Verdict basis: all twelve R758-1 findings and the one residue item are closed at their cause. So are all
thirteen R757-1 findings and three residue items. The round-2 text adds six MINOR defects, so the verdict is
NEGATIVE and all five lenses are UNCLEAN. Four of the six are new design text that is incomplete or
overstated. Two are figures in the analysis evidence that understate the worst case. None changes a stated
met or not-met conclusion. Every case above 65 µs is recorded as not met and listed as an open owner question.
The owner's 2026-10-31 decisions are out of review.

## Findings

### R758-2-F1 MINOR - RTL, Docs - docs/design/MARK_II_STREAM_ENGINES.md:132-138 - the 192 kHz engine load is not the largest legal load

- Authority/evidence: the page says "Each row is the largest load over every legal mix". It gives 92.67 % at
  192 kHz, which is the largest only among exactly 16 streams per port. An enumeration of every mix of 1 to 16
  streams uses the page's own cycle and Table 4.4 reservation formulas (`scripts/load_any_count.py`,
  `receipts/load_any_count.out`). Fourteen eight-channel streams with no CRF reserve 748.160 Mb/s, within the
  75 % default, and load each engine 93.18 %. The author's `load192.py` enumerates exactly 16 streams. The 48 and
  96 kHz rows are unchanged (33.47 % and 58.05 %).
- Impact: the engine-headroom figure that open question 7 rests on is understated by 0.51 points. The page
  presents it as a maximum. The conclusion ("close to full") is unchanged.
- Required outcome: the 192 kHz row gives 93.18 % with 14 eight-channel streams and no CRF, or it states that the
  row covers exactly 16 reservations. Open question 7 (SE:931-933) follows.
- Verification: rerun `load_any_count.py`. The row equals its "any count" line.

### R758-2-F2 MINOR - Conformance, Robustness, Tests, Docs - docs/design/MARK_II_STREAM_ENGINES.md:323-324 - the 192 kHz results do not cover every placement that starts and stops reach

- Authority/evidence: the 192 kHz rows are labelled "Exact occupancy". The model (`exact_192b`,
  `uniform192_crf_first.py`) evaluates three CRF placements: none, tie rank 0 and tie rank 16. Under the page's
  rule (least wire time, a CRF counts, ties in spread order) a start always finds an empty phase at 192 kHz. Each
  start therefore takes the lowest-rank empty phase, the occupied set lies in the first 17 tie ranks, and the CRF
  can start at any of them and can later stop. The probe (`scripts/probe192_placements.py`, using the model's own
  `tandem_192` and window objective, `receipts/probe192_placements.out`) covers all 35 cases. Example sequence:
  start one stream (phase 0), start the CRF (phase 12), start 15 streams, then stop the CRF. The results are:
  - one format: worst 34.861 µs (N = 6), against the page's 32.071 µs;
  - mixed formats: a shaper wait of 57.905 µs, giving at least 75.999 µs before packetizer time, against the
    page's 54.822 and 72.915 µs.
  The author's three placements reproduce exactly (32.071, 54.822, 72.915), so the model is sound but its search
  is incomplete.
- Impact: the analysis evidence for NFR-LAT-03 calls a partial search exact, and it understates both 192 kHz
  figures. The verdicts are unchanged: one format is still met (34.861 < 65) and mixed formats are still not met.
- Required outcome: the 192 kHz rows either cover every reachable placement (all 17 CRF ranks, plus the CRF
  stopped after any of them) or drop "exact". The figures follow, and so does any other place that repeats
  32.071 µs.
- Verification: rerun the model's 192 kHz section over all 35 placements. Its maxima equal the table.

### R758-2-F3 MINOR - Robustness, Conformance, Tests, Docs - docs/design/MARK_II_STREAM_ENGINES.md:834-851 and :799; docs/reference/FR_NFR.md:476 (NFR-REL-03) - the compaction order leaves a window between its last check and the header

- Authority/evidence: step 4 repeats the replay "until no record is dirty or unreplayed". Step 5 then writes the
  header, and "until its commit, saves keep appending to the active slot". The page also says "Compaction
  yields to saves only between pages" and "Steps 2 to 4 run between saves". It does not say that a save cannot
  run between step 4's final check and step 5's header page.
- If a save runs there, it appends a change to the old slot, and the save reports it durable. The header then
  commits the new slot without that record, and step 7 erases the old slot. The change is lost without a power
  cut, which is the R758-1-F3 failure in a smaller window. NFR-REL-03 now states "loses no saved change, with
  or without a power cut".
- The planned host-model test (SE:897, FR:476) changes a record "after its copy". It does not place a save
  between the last check and the header.
- Impact: a straightforward implementation of the written order (check, yield, header) can drop a durable save.
- Required outcome: the page states that the final check and the header write run with no save between them. A
  save that arrives then waits for the header and appends to the new slot. Alternatively, the header write
  re-checks for unreplayed records. The verification row adds a save placed in that window.
- Verification: a host flash-model case. A save completes between the last replay page and the header. After
  the commit, the erase and a reboot, the new value is read back.

### R758-2-F4 MINOR - Robustness, RTL, Tests, Docs - docs/design/MARK_II_STREAM_ENGINES.md:471-492 and :893 - the listener merge can render a time-uncertain copy at a wrong position while its clean partner is valid

- Authority/evidence: merge rule 2 renders "a copy later than the last written time". It does this whether or
  not the copy carries tu. Rule 3 says "a clean copy replaces the last packet's tu copy". The page names no key
  that matches a clean copy to "the last packet's" tu copy, and replacing a write cannot erase samples the tu
  copy wrote outside the clean copy's span.
- tu marks uncertain time (IEEE 1722-2016 4.4.4.7). Two cases follow when the secondary copy carries tu and its
  converted time is off by δ:
  - It arrives first with 0 < -δ < 125 µs. Rule 2 renders it over the tail of the previous packet. The clean
    primary copy is then written at its own time, and the shifted samples in that tail stay.
  - It arrives first with δ > 0 and the merge key is matched by time. Rule 2 moves the last written time ahead
    by δ. Rule 4 then discards every clean primary copy until real time passes it.
- The verification row covers both copies with tu set and a grandmaster change on a surviving single network.
  It does not cover one tu copy with a skewed time beside a valid partner.
- Impact: with both networks up, uncertain time on one network can corrupt or block audio that the clean
  network carries correctly. Redundancy exists to prevent this.
- Required outcome: the rules state how a clean copy and a tu copy of one packet are matched (for example by
  sequence or the expected packet time). They also guarantee that a tu copy never advances the merge key past,
  or overwrites samples outside, what the clean copy of the same packet would write. Holding a paired tu copy
  until its partner is due is one way.
- Verification: a merge simulation with the secondary copy tu-flagged, its time skewed by ±δ (δ below and above
  125 µs), arriving before the primary. The rendered samples equal the clean stream's.

### R758-2-F5 MINOR - RTL, Tests, Docs - docs/design/MARK_II_STREAM_ENGINES.md:359-377, :563-566 and :612 - the latency instrument does not state the time base of port-1 copies

- Authority/evidence: "Capture stamps each TDM frame end in PHC time". The end is "the launch observer's
  first-bit time". Each port has its own PHC (SE:511) and its own timestamp unit, and odd copies launch on
  port 1. The page does not say which PHC the capture stamp uses. It also does not say whether port 1's
  launch time is converted with the latched PHC offset, as the talker timestamp is (SE:456-463). Without that,
  `SE_TLAT_MAX1`, `SE_TLAT_OVER` COUNT1 and `TCTX_TLAT_MAX` of every odd context measure the interval plus
  the offset between the two PHCs. NFR-LAT-03 names these taps as its test ("which measure this pin-to-wire
  interval itself").
- Impact: the requirement's test instrument is under-specified for half of the talker streams. A literal
  implementation reports a value that is off by the PHC offset.
- Required outcome: the instrument names the capture time base and converts port 1's launch stamps into it (or
  stamps the capture in each port's time). The verification adds a check on a port-1 copy.
- Verification: the instrument text, and a simulation of an odd context with a non-zero PHC offset whose
  recorded interval matches the pin-to-wire time.

### R758-2-F6 MINOR - Conformance, Docs - docs/ARCHITECTURE_HW_SW_SPLIT.md:75, :79-82 and :51; docs/design/MARK_II_STREAM_ENGINES.md:925 - a survey's recommended flexPTP revision is presented as an owner decision

- Authority/evidence: the split page opens the list with "These decisions are final; this page restates them".
  It then states "The adopted revision is branch `gptp` at `d116d3d`", linking 6551164172. That comment is the
  survey lane's report, which recommends "adopt kebag-logic/flexPTP gptp d116d3d". It is not an owner decision.
  The owner's 17:04 decision is "`flexptpd` ... Its source and licence get confirmed before adoption". Round 1
  recorded that condition ("Its source and licence are confirmed before adoption"), and round 2 removed it.
  The row at :51 and SE:925 also say "the adopted fork".
- The public facts the delta cites are correct (`receipts/gh/flexptp_repo.json`, `flexptp_gptp_branch.json`):
  `kebag-logic/flexPTP` is public and MIT (LICENSE.txt on `gptp`), a fork of `epagris/flexPTP`, and branch
  `gptp` is at `d116d3dfe8e6`. One port per image stays an open item (SE:924-926, split :82, plan D13). Neither
  is in question.
- Impact: a lane recommendation, the pinned revision and its adoption, sits in a list of final owner decisions,
  ahead of the confirmation the owner asked for.
- Required outcome: the revision and the adoption are stated as the survey's proposal, with the source and
  licence findings recorded for the owner's confirmation (or the owner's confirmation is cited). Naming
  `flexptpd` and its public source stays.
- Verification: the three places read against the 17:04 comment and the survey comment.

### R758-2-R1 RESIDUE - Docs - docs/design/MARK_II_STREAM_ENGINES.md:539-540 - the counter rule contradicts SE_TLAT_OVER

- "Every counter is 32 bits and wraps to zero. Milan's Tables 5.4 and 5.6 require that." `SE_TLAT_OVER`
  (SE:565-566) holds two 16-bit counts that saturate. Its row is explicit, so no width or behaviour is in doubt.
- Exact fix: "Every Milan counter is 32 bits and wraps to zero."

### Suggestions (optional, do not affect coverage)

- S1: SE:785 prints t_page as 5.343 ms. The terms sum to 5.3438 ms, which rounds to 5.344 ms. The 5.35 ms used
  in T_worst covers both.
- S2: SE:168 says "about 117 µs". Under the page's rule (CRF last in its phase) the sixteenth frame starts
  30,960 bits / 270.848 Mb/s = 114.3 µs after the release. 117 µs assumes the CRF goes first.
- S3: the fewer-reservations table (SE:346-351) adds only interference. Adding the fixed terms gives the
  comparable total, for example 83.012 + 40.325 = 123.3 µs for three co-phased streams. Light mixed streams
  co-phased alone can approach 125 µs of shaper wait.
- S4: REQUIREMENTS.md:58-59 scopes "preserve wire behavior ... ordering and normative timeouts" to "until the
  switch-over". After the switch-over that obligation rests only on NFR-SCOUT-03. One clause ("after it, the
  firmware placement preserves them") would keep it explicit.

## Round-1 findings (R758-1) at this head

| ID | Status | Evidence at f6b3e841 |
|---|---|---|
| F1 bare-metal gate | Closed | AP:159 "the host tools", AP:273 "host-tool"; `check_baremetal_only.py --check` rc 0, 0 findings over 1425 files; `--selftest` rc 0 (`receipts/gates/baremetal_only*`) |
| F2 mixed formats | Closed at its cause | SE:179-214 rule and reached mix; SE:312-336 results at 16 reservations for 48, 96 and 192 kHz; FR:306 records met for one format and not met for mixed formats or fewer reservations; open question 1 (SE:904-913). The 192 kHz figures are understated (R758-2-F2), but the conclusions hold |
| F3 compaction loses changes | Closed at its cause | SE:828-861 replay ordering and power-cut table; FR:476. A narrower window remains (R758-2-F3) |
| F4 a-d requirement contradictions | Closed | RQ:25-37, :41-47, :58-59, :110, :156-159; FR:75-85, :305, :320, :327, :456-457, :477, :517; OV:3-19. Own search `receipts/scope_search.txt`: every hit is scoped. Lever 5 conflict published (FR:328, AP:291-300) |
| F5 "Mark I bound" | Closed | FR:473 matches the #234 ruling (`receipts/gh/c5967924270.json`: "The target stays at 60 %... How it is met: a redesign ... #640 ... Until then: the #638 resource gate holds every resource at its recorded value"); AP:65-71 |
| F6 a, b clause claims | Closed | SE:51, :590, :630 N in {1, 2, 4, 6, 8}; SE:229-233 Milan cites 802.1Q-2014 34.6.1, which is 2022's 34.6.1.1 |
| F7 a CDC, b "any order" | Closed | SE:297 "(0.080 µs), rounded up to 0.200 µs"; the order claim is replaced by the reachable-state model (SE:197, :207-214) |
| F8 render buffer per rate | Closed | SE:393-417: depth 128, 256, 512 = 2.667 ms at 48, 96, 192 kHz (>= 2.25 ms >= 2.126 ms, Milan v1.2 4.4.2.1); 1, 2, 4 RAMB36; ledger 4.0 (SE:677); fabric 27.0, total 144.5 against 121.5, recorded open (SE:690, :917-919; AP:238-242) |
| F9 a talker time base, b tu rule | Closed at its cause | SE:448-469 each copy in its own port's time (Milan v1.2 8.3.4, 1722-2016 4.4.4.9); SE:476-492 no rule drops the only copy, both-tu stated. New merge defect: R758-2-F4 |
| F10 register maps | Closed | Every register's fields sum to 32 bits and every offset is defined or reserved (checked row by row; see below); PORT reset by parity; TCTX_MAP 15 = not mapped; VID 12 bits |
| F11 flexptpd | Closed as asked (named as decided); see R758-2-F6 for the adoption wording |
| F12 lane order | Closed | AP:257 D16 row, AP:288-289, AP:301-307 open decision 2, marked as a proposal |
| R1 paragraph length | Closed | The 20-to-30 rule is an upper bound; `check_doc_style.py` rc 0 at the head, and the author's changed-block run shows 0 findings |
| S1 to S6 | Taken | S1 SE:239-244 (model `per_stream_spacing_ok`: largest ratio 125.000 µs, the CRF); S2 SE:393; S3 FR:613; S4 SE:760-764; S5 SE:185, :196; S6 FR:328, SP:79 link 16:51 |

## Prior public findings of the internal round (R757-1, issuecomment-6551340614) at this head

Read after this round's independent pass, draft verdict and ledger were written.

| ID | Status at f6b3e841 |
|---|---|
| F1 bare-metal gate | Closed (as R758-1-F1) |
| F2 60 % presented as decided | Closed (as R758-1-F5) |
| F3 requirement contradictions | Closed (as R758-1-F4) |
| F4 mixed-format worst case | Closed at its cause. The author's model reproduces 42.765 µs (`receipts/model/checks.out`). The 192 kHz figures stay open as R758-2-F2 |
| F5 flexPTP lineage | Retained in narrower form as R758-2-F6 (adoption and revision presented as decided) |
| F6 interference assumptions | Closed: SE:263-290 states A1, A2, L.3.1.1 a), the 802.1BA 6.3 correction and the 16.160 µs figure for 2000-octet frames |
| F7 a-d citations | Closed: a SE:229-233; b SE:571-574 (5.3.10.1) and SE:594 (5.3.9.1); c SE:51; d FR:613 adds 5.3.8.1, 5.3.8.3, 5.3.10.1, 5.3.11.1 and 5.5.2.4 |
| F8 instrument interval | Closed: pin-referenced (SE:359-377, :563-566, :612; FR:306). The time base is still unstated (R758-2-F5) |
| F9 rates | Closed (as R758-1-F8; per-rate wire table SE:80-88, engine load SE:132-138, see R758-2-F1) |
| F10 save terms and timeout | Closed: SE:789-792 359.75 ms; SE:804-805 and open question 6 |
| F11 register bits and counter resets | Closed: bits as above; reset events SE:607-611 (5.3.7.7) and SE:628, :646-658 (5.3.8.10) |
| F12 lever 6 credit | Closed: AP:175 +0.25k; 21.45k central (17.8k to 25.45k) re-derived |
| F13 lane order | Closed (as R758-1-F12) |
| R1, R2, R3 | Closed: SE:297; SE:921-922; AP:226 heading, anchor unchanged, `gen_toc.py --check` rc 0 |
| S1 to S4 | Taken (SE:239-244; SE:489-491; FR:500; SE:185, :196) |

## Independently verified at this head (no finding)

- Signed packet: every author-r2 file matches `MANIFEST.json` (107 entries, 0 mismatches) and
  `evidence/SHA256SUMS` (8 of 8 OK). The model digest matches the REVIEW READY digest (bfebe546...).
- Docs gates (clean clone, pinned renderer; `receipts/gates/`, `gates_summary.txt`), all rc 0:
  - `check_baremetal_only.py --check` (0 findings over 1425 files) and `--selftest`;
  - `check_doc_style.py` and `--selftest`;
  - `docs_check.py` (0 findings, 211 pages, 1427 scrubbed files);
  - `gen_toc.py --check` (150 pages), `--verify-anchors` and `--selftest`;
  - `check_em_dash.py --base e5b8405d` (0 over 1426 added lines in 7 pages) and its self-test;
  - `check_feature_status` and its self-test, `check_doc_paths`;
  - `check_gptp_docs`, `check_solution_docs`, `check_submodule_docs` and `check_archive`, each with its self-test;
  - `DOC_MAP --check` and `--selftest`, `check_diagram_pngs`, `gen_module_matrix --check`;
  - `ci_events --check` and `ci_gate_workflows --check`.
  `check_hygiene` and `check_todo_ownership` refuse because the submodules are not initialised (rc 2). Neither
  reads Markdown. The author's receipts show both at rc 0 with submodules.
- Shaper model (`receipts/model/`, all rc 0, each under 5 min; `run_times.txt`):
  - `checks`: F1 equals the 8.6.8.2 simulation at every rate, and F2 adds at most 12.335 µs against 12.336. The
    per-stream level never holds a frame. Fixed terms: 18.229, 9.115 and 4.557 pin, 0.200 CDC, 8.560, 9.840 and
    9.200 packetizer. Both reviewer cases reproduce (42.875 and 42.765 µs).
  - `uniform`: 48 kHz, 17,658 states, worst 23.106 µs (8 ch, no CRF), so 63.431 = 23.106 + 40.325. 96 kHz,
    351,488 states, worst 18.802 µs (1 ch, CRF in phase 2), so 51.293 = 18.802 + 32.491.
  - The optional `s48 ahead` and `s96 ahead` give superset maxima of 55.542 and 60.725 µs, so 95.867 and
    93.216 µs.
  - Reached totals re-derive: 92.530 = 53.085 + 18.229 + 0.2 + 7.680 + 12.336 + 1.0, and 74.826 likewise.
  - The 48 kHz witness (3 x 8 ch, 5 x 2 ch, 8 x 1 ch; idleSlope 133.120 Mb/s; 9,840 bits / 133.120 - 20.833 =
    53.085 µs) was reached by hand under the rule. Start 13 eight-channel streams so phase 0 holds three, stop
    the others, interleave two-channel streams into phase 1 against eight-channel fillers, stop the fillers,
    then start the one-channel streams.
- Falsification attempt of the 48 kHz bound: an independent random start/stop search with my own rule and
  recursion (`scripts/churn48.py`, 8 seeds, about 4.75 M 16-stream states). The top states were re-scored with
  the round-1 event-level simulator, and both agree exactly. The best reached was 42.485 µs, so nothing came
  near 55.542.
- Every case above 65 µs is stated as not met and is in open question 1 or the fewer-reservations text, never
  as met. That covers the mixed results at 48, 96 and 192 kHz and the 74.6 to 95.3 µs fewer-reservation rows
  (SE:317-357, FR:306, AP:59, AP:255, SE:904-913).
- Save worst case: 10 + 5.35 + 2 x 1 + 32 x 5.35 + 32 x 5.35 = 359.75 ms, margin 140.25 ms (28.05 %). The
  N25Q128 inputs are unchanged from round 1: Table 32 tPP 5 ms, tSE 3 s, tSSE 2 s; Table 17 suspend latency
  15 µs typical with no maximum; 9.1.20. The new term is Table 17's 40 µs resume-to-suspend, covered by the 1 ms
  allowance. Compaction table: 1,024 pages per slot, 784 append pages, 1.28 s, 12 s and 168 ms all re-derive.
- Render buffer and ledger: 108, 216 and 432 samples for 2.25 ms; 32,768, 65,536 and 131,072 bits. Fabric rows
  sum to 27.0. Total 27.0 + 113.0 - 11.5 + 16.0 = 144.5, which is 23 over 121.5. Firmware extrapolation 461,240 B
  (112.6, so 113 tiles) and stage 47,275 B both re-derive.
- Register maps: each field range sums to 32 bits in SE_ID, SE_CAP, SE_CTRL, SE_TLAT_OVER, SE_RMAP, TCTX_CTRL,
  TCTX_MAP, TCTX_DA_HI, TCTX_PTO, TCTX_STATE, LCTX_CTRL, LCTX_DA_HI and LCTX_STATE. Engine offsets
  0x000-0x05C are contiguous, then reserved to 0x7FC. Contexts sit at 0x800 + 64n (16 words) and 0x1000 + 128n
  (32 words). PTO reset 0x001E_8480 = 2,000,000 ns. The five 5.3.7.7 talker counters and ten 5.3.8.10 listener
  counters are present, each with its reset event.
- Redundancy: per-port PHC and gPTP (Milan v1.2 8.3.4), each copy stamped in its own port's time (1722-2016
  4.4.4.9), the listener converts with the latched offset, and wrap-aware comparison holds. See R758-2-F4 for the
  merge.
- Requirement scoping: REQUIREMENTS.md, FR_NFR.md and the overview change scope only ("until the switch-over",
  "until F6", "after F6"). NFR-RES-01, NFR-SCOUT-02 and the plan record only the decisions and the open items
  (lever 5 against media ownership, lever 2 after lever 3, BRAM, latency, save bursts, flexptpd two-port).
  The flexPTP adoption is the exception (R758-2-F6).
- Area: lever 6 nets 5,194 - 218 - 32 = 4,944. Central 21.45k, low 17.8k, high 25.45k.
- Comment rule: the delta has no source file, so it adds no source-comment instance. Privacy: docs_check scrub
  clean.
- Clone restored: HEAD and tree as above, no untracked or ignored files, index identical to HEAD's tree, and
  gitlinks unchanged (`receipts/clone_restore_check.txt`, `gitlinks_at_head.txt`).

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2, F3, F6) | FR_NFR.md NFR-LAT-02/03, NFR-RES-01, NFR-REL-03, NFR-SCOUT-01/02/03, NFR-OBS-01, sections 1.2, 4.2, 6; REQUIREMENTS.md sections 1 and 4; overview; split page; stream-engine page (stagger, latency, render buffer, redundancy, maps, save path, open questions); area plan Target, decisions and lanes; #640 owner comments 16:39 to 17:21, survey 6551164172, #234 ruling 5967924270 | R758-2 | f6b3e841646384177584ce75b657fb8dead7727c |
| RTL | UNCLEAN (F1, F4, F5) | Engine throughput and load per rate; capture ring; depacketizer match; render buffer and clock crossing; per-port units and PHCs; time-base conversion; merge state words; all register maps bit by bit; Block RAM ledger | R758-2 | f6b3e841646384177584ce75b657fb8dead7727c |
| Robustness | UNCLEAN (F2, F3, F4) | Start/stop reachability at 48, 96, 192 kHz; fewer reservations; compaction interleaving and power-cut table; tu, grandmaster change and single-network paths; ERR handling of invalid NCH/NSR/PHASE/SLOT | R758-2 | f6b3e841646384177584ce75b657fb8dead7727c |
| Tests | UNCLEAN (F2, F3, F4, F5) | Author model `mixed_stagger.py` (checks, uniform, e192, s48/s96 ahead) and its 192 kHz search; own probes `load_any_count.py`, `probe192_placements.py`, `churn48.py`; docs gates at the head; author gate receipts; verification tables of SE, NFR-LAT-03 and NFR-REL-03; hosted check runs | R758-2 | f6b3e841646384177584ce75b657fb8dead7727c |
| Docs | UNCLEAN (F1, F2, F3, F4, F5, F6; R1 residue) | All six touched pages at the head; diff dfc310fb..f6b3e841 and its twelve commits; author HANDOFF and PR body; contents and anchors | R758-2 | f6b3e841646384177584ce75b657fb8dead7727c |

## Real limits

- The standards were not re-read this round for clauses whose cited text is unchanged since round 1. These are
  the N25Q128 Tables 32 and 17, Milan v1.2 4.4.2.1, 5.3.7.7 and 5.3.8.10, and IEEE 802.1Q-2022 L.3.1.1. Their
  values match the round-1 readings. The new citation of IEEE 802.1BA-2011 6.1 options a) and b) (30 µs wake) is
  accepted on the internal round's reading; I did not re-read it.
- The latency figures are analysis from the author's class-level model and my independent recursion and event
  simulator, not from an implementation. The 48 and 96 kHz superset maxima are taken from the author's search,
  which I re-ran but did not re-implement. My random search only probes the 48 kHz bound from below.
- Hosted evidence at this head, at review time: 20 completed success and 22 skipped. docs-check-no-git,
  docs-gates-1, docs-gates-2, rtl-fast and wire-accountability passed. docs-gates-0 and one fail-fast context were
  still in progress, so the docs-check aggregate had not reported (`receipts/gh/hosted_check_runs.tsv`). This
  is not acceptance evidence.
- No physical calibration, bench or hardware run took place. No manager source bank runs at this head, and none
  is claimed or inferred.

## Pending manager duties

- Hosted and act acceptance of the exact head, including the docs-gates-0 and docs-check results.
- Builder and native banks on the current-dev merge candidate at the merge turn (source base and live dev both
  e5b8405db4c1f7cbdafb5df92b15b580142e0232 at review time).
- Owner approval of the requirement text and the open owner decisions: lever 5 against media ownership, lever 2
  after lever 3, latency with mixed formats or fewer reservations, save bursts, Block RAM, the commit timeout
  and the flexptpd two-port item. The flexPTP revision's adoption is added by R758-2-F6.
- Carry R758-2-R1 to the residue checklist.

R758-2 FINISHED
