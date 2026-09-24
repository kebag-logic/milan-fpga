[R276] POSITIVE - exact head 021b2e07b009158bcb0ce19529126eb1d330bba5

Round R276-2 is the internal independent re-review of PR #540 (Relates to #387, partial). It reviews the exact head `021b2e07b009158bcb0ce19529126eb1d330bba5`, tree `a7ffb35beea95d5bba593029f382e8c0ab0b1c27`, from a cleared context. The source base is `759da623072358afdb0e9d570a7b4b6a788492c9`. The head descends linearly from it through six one-line commits with no trailers and no merges, so the source candidate tree is the head tree.

All five lenses were applied at this head, and all five are clean. Every finding of R276-1 and R277-1 is resolved at this head, each checked with independent evidence. Two SUGGESTIONs are raised; they do not affect coverage. The verdict is POSITIVE.

## Reconstructed from

I read these in the contract's order:

- AGENTS.md, CONTRIBUTING.md and docs/README.md.
- The #387 body and its frozen acceptance.
- The decisions: 5606198212 (part b), 5794731090, the assignment 5800693336, the rulings 5802264260 and the correction assignment 5804878668.
- The author's REVIEW READY comments, 5802234836 (A214) and 5805175917 (A224), and the PR body.
- REQ-PTP-05/07/08/09 and NFR-REL-01.
- #539.
- The diff and history `759da623..021b2e07`, and the correction delta `44bf0891..021b2e07`.
- The public evidence tree `review-evidence/387-r1` at `37d91083`, limited to the published proposed patch and the edited datapath copies.

I did my own pass over the diff, probes, verdict and ledger before reading any review report. After that I read R276-1 (5804105668) and R277-1 (5804873088) and disposed of each item below.

## Verdict basis

Everything below was verified at this head.

**The gmstep leg.**
- At the head it scores 48 checks and 4 failures, at feed delays 0 and 12, and through the Makefile's own `gmstep GMSTEP_FEED_DELAY=12` target (receipts 30, 31, 32).
- The four failures are exactly the declared ones:
  - "render: the GM change is one counted re-base event" (2);
  - "render: every counted re-base lands at a PDU end right after the step" (the identity re-base at -160118 cycles);
  - "restart: the outgoing mr toggles exactly once" (0);
  - "restart: the talker's MEDIA_RESET counts exactly one" (0).

**The edited datapath (the leg's passing reference, not part of this PR).**
- The tree's `milan_datapath.sv` plus the published patch equals both published copies byte for byte (sha256 `45ac96c0...`, receipt 12).
- With it the leg passes 48/48 at all 125 feed delays, 0 to 124 (receipt 40). That is the whole 125-cycle period of the 2 MHz media-tick pattern, a superset of the 42 the author claims.
- The fill after every push is 14 at every delay. The fill at accept is 9 (106 delays), 10 (16) or alternates (3), and that is not graded.
- The margins at every delay (receipt 41):
  - The counted re-base lands at +132 cycles against its 500-cycle window.
  - The first `mr` toggle lands at +22 to +663 cycles against its 1284-cycle window (two intervals of 642).
  - The longest talker pause is 653 to 830 cycles against its 2568 limit.

**My own mutants.** I wrote seven, independently of the author's control runner. Each one is built through the tree's recipe with `DP_SRC`/`RSP_SRC` (receipts 50, 51, 52), and each is caught by the named check it targets:

| Mutant | Failing checks |
|---|---|
| D1: the `mr` restart keyed to the grandmaster identity, not the step | "every mr toggle is first sent right after the step" and "MEDIA_RESET does not move between the commit and the step" (delays 0, 29) |
| D2: the restart on both the identity and the step | those two, plus "toggles exactly once" (2) and "MEDIA_RESET counts exactly one" (2) |
| D3: the step's restart 4000 cycles late | only the toggle-window check |
| D4: the step's render re-centre 1000 cycles late | only "every counted re-base lands at a PDU end right after the step" |
| D5: the recentre snap (not the prefill release or the rail) one event short | only "every PDU push leaves the target fill across the event" (2660 or 2661 pushes off target), at all ten delays tried: 0, 7, 12, 20, 29, 41, 55, 83, 100, 124 |
| D6 and D7: the talker silenced for good 300000 or 600000 cycles after the step, admission gate untouched | "never pauses beyond four of its intervals" and "keeps its baseline rate within 1%" |

**The pin and the ROM (receipt 11).**
- The gitlink `e5dcea6e` is donor main (compare: identical), the merge of FPGA-gPTP PR #74.
- Its parents are `c1b61743` and `ba926810`, and its tree `5a02fa35` equals `ba926810`'s.
- The default-argument image regenerates to `4afe436d...`, which equals `syn/yosys/rom_digests.tsv` at the pin.
- The donor constants are `STEP_LINKUP_NS_C = 20000`, `STEP_LOCKED_NS_C = 100000` and `RATE_PPM_C = 200`.

**Consumer suites at this head (receipt 60).**
- `milan_dp gptp`: 181/181.
- `gptp_shadow run`: 309/309.
- `clkvalid`: 22 + 19 + 14 checks, 0 failures.

**Static gates at this head (receipt 10).** All 12 exit 0:
- `docs_check`;
- `check_em_dash --base 759da623`;
- `check_gptp_docs`, with and without the submodule;
- `gen_toc --check`, `check_doc_style` and `check_cpp_idiom`;
- `check_feature_status`, `check_submodule_docs` and `check_diagram_pngs`;
- `measure_test_evidence --check`;
- `git diff --check 759da623 HEAD`.

The C++ build of `sim_gmstep.cpp` raised no compiler warning.

**Hosted contexts at this head (receipt 20).**
- 21 executed jobs concluded `success`. They include all five Verilator shards, all four Yosys shards, and the `verilator-suites` and `yosys-portability` aggregates.
- `Physical gPTP (nightly and manual)` is a skipped context and is not hardware evidence.
- The gmstep leg is not in any hosted sweep.

**Scope.**
- The hot files `milan_datapath.sv`, `sim_nxn.cpp` and `CHANGELOG.md` are untouched.
- No parent RTL is in the diff.
- The PR says "Relates to #387" and states that acceptance 3 is not met. That matches ruling 5802264260's partial-PR scope.

## Focus items of correction round 1

| Item | Result at this head | Evidence |
|---|---|---|
| The grid-aligner row quotes decision part (b) verbatim in the Decided column | Met. `docs/design/GM_LOSS_RECOVERY.md:119` is a verbatim substring of 5606198212 (b) | text comparison |
| The tree column records the observed gap, and the page does not settle it | Met. `KL_media_grid_align.sv:97-106` has no PHC or step input (ports read). Its reference chain is CRF, then the servo, then the physical grid, then the aligner (`:26-33`), so "a step reaches it only through the CRF-steered grid (#539)" is accurate. The question is published to the owner on #387 (5805175917, question 1) | RTL read; #539 body |
| Ruling 5802264260 item 2 is recorded | Met. `GM_LOSS_RECOVERY.md:124` restates the ruling's three clauses. Its tree state, "Not yet", matches `KL_media_clock_restart.sv:167` (`tgt_r <= ~tgt_r` once per request, adopted only after the hold) | RTL read |
| The gmstep claims are narrowed to what it grades | Met. Each item in `GM_LOSS_RECOVERY.md:139-143` maps to named checks: `sim_gmstep.cpp:886-911` (tu), `:963-990` (render re-base and law), `:996-1024` (mr and MEDIA_RESET), `:916-960` (streams). The ungraded list (`:147-151`), the verification row (`:179`), `tb/verilator/milan_dp/README.md:385-392` and the banner (`sim_gmstep.cpp:15-19`) agree | code read; head run |
| The counted re-base event is tied to the step | Met. The re-base window is `sim_gmstep.cpp:115-117,966-972,977`, the toggle window `:118-121,1002-1013`, and the mid-event MEDIA_RESET read `:844-846,872-873,1020-1021`. The head's identity re-base fails the window. D1, D3 and D4 each fail only through these arms | receipts 30, 50 |
| The licence check sees a talker that stops for good | Met. The trailing silence is counted (`:923-925`), and more than 100 PDUs are required after `tu` clears (`:909`). D6 and D7 are caught | receipt 50 |
| The render-law arms are independent of start phase | Met. The law is read as the post-push peak (`:437-447`) against TARGET_C = 14 (`:110-112`), which matches the stage's own law (`KL_render_setpoint.sv:54-59,220,536`). The clean edited leg passes at 125/125 delays, and D5 is caught at 10/10 | receipts 40, 41, 50 |

`docs/design/TIME_SYNC.md:95-97` is also correct:
- The donor microcode clamps the trim (`RATE_PPM_C = 200` and the integrator clamp in `gen_gptp_ucode.py`).
- `KL_gptp_txret.sv:303-305` derives `PHC_ADJ_MAX_C` from `RECON_REL_PPM_P = 200`.
- `KL_gptp_txret.sv:434-436` refuses eligibility while `|adj|` exceeds it.

## Prior public review findings

Each item was re-checked at this head with the evidence named.

| Prior item | Lenses as filed | Disposition at 021b2e07 | Evidence |
|---|---|---|---|
| R276-1 F1 MINOR: the aligner's Decided cell contradicts part (b) | Conformance, Docs | RESOLVED | `GM_LOSS_RECOVERY.md:119` quotes (b) verbatim. The tree gap is in the tree column, and the question is with the owner (5805175917). The required outcome ("until that ruling exists, the Decided column carries part (b)'s wording and the tree column carries the observation") is met |
| R276-1 F2 MINOR: ruling 5802264260 item 2 missing | Conformance, Docs | RESOLVED | `GM_LOSS_RECOVERY.md:124` |
| R276-1 F3 MINOR: "measures all of this" | Docs | RESOLVED | `GM_LOSS_RECOVERY.md:135-151,179`; every graded item maps to a named check |
| R276-1 F4 MINOR: the counted event is not tied to the step | Tests | RESOLVED | D1 (restart on the identity) fails 2 checks, D3 fails the toggle window, D4 fails the re-base window; the head's identity re-base fails the window |
| R276-1 F5 MINOR: a talker that stops for good passes | Tests, Robustness | RESOLVED | D6 and D7 fail the pause and rate checks |
| R276-1 S1: the Makefile names an untracked runner | Docs | RESOLVED | `tb/verilator/milan_dp/Makefile:99-101,275-282` name no file |
| R276-1 S2: no counters_valid guard | Tests | RESOLVED | `sim_gmstep.cpp:953-955` (both Stream Input answers) and `:1014-1019` (all three Stream Output answers). FRAMES_RX is graded against the accepts (`:956-957`) |
| R276-1 S3: cite #539 on the CRF-servo row | Docs | RESOLVED | `GM_LOSS_RECOVERY.md:121` |
| R277-1 finding 1 MINOR: the aligner row | Conformance, Docs | RESOLVED | as R276-1 F1 |
| R277-1 finding 2 MINOR: the overclaim | Docs, Tests | RESOLVED | as R276-1 F3 |
| R277-1 finding 3 MINOR: the render arms depend on the start phase | Tests, Robustness, Docs | RESOLVED | 125/125 phases pass on the edited copy, and D5 is caught at 10/10. The banner (`sim_gmstep.cpp:46-53`) and README (`:363-374`) no longer state a fixed at-accept constant |
| R277-1 suggestion 1: the Makefile runner name | Docs, Tests | RESOLVED | as R276-1 S1 |
| R277-1 suggestion 2: Stream Input validity and FRAMES_RX | Tests, Robustness | RESOLVED | as R276-1 S2 |
| R277-1 suggestion 3: TIME_SYNC.md:95 wording | Docs | RESOLVED | `TIME_SYNC.md:95-97`, checked against the sources above |

No prior item is retained.

## Findings of this round

No BLOCKER, MAJOR or MINOR finding is open.

```text
[R276] SUGGESTION Docs - docs/design/GM_LOSS_RECOVERY.md:118 - the render row's tree column opens "Yes" for a case the tree does not yet meet
Requirement/evidence: the row's decided reaction is "one bounded, counted event". For a grandmaster change that steps, the tree counts two re-bases (receipt 30: counted at -160118 and +132 cycles against the step pulse). The same cell's qualifier and :131-133 disclose this, so nothing is hidden.
Impact: a reader scanning the column sees "Yes" beside a decided count the tree meets for a lone step but not for the scenario this section is about.
Required outcome (optional): word the cell as partial, or turn it together with the #387 datapath edit.
Verification: the cell agrees with the gmstep result at the head that carries it.
```

```text
[R276] SUGGESTION Docs - docs/design/GM_LOSS_RECOVERY.md:118-119,124 - the decision and ruling are cited by bare identifier
Requirement/evidence: the cells cite "decision part b" and "ruling 5802264260 item 2" without links. The page names #387 once (:113), while TIME_SYNC.md:103-107 links its sources.
Impact: a cold reader must know that both are #387 comments.
Required outcome (optional): link issuecomment-5606198212 and issuecomment-5802264260.
Verification: docs_check passes and the links resolve.
```

## Per-lens results

```text
[R276] PASS Conformance - #387 acceptance 1-5 against the PR body; docs/design/GM_LOSS_RECOVERY.md:109-153 against 5606198212(b), 5794731090 and 5802264260 items 1-3; docs/design/TIME_SYNC.md:75-107 against 5794731090, FPGA-gPTP#68 5798089412 and the donor constants at e5dcea6e; REQ-PTP-08 against the licence and tu arms - the aligner row quotes (b) and leaves the question with the owner, the merge ruling is recorded as decided with its true tree state, acceptance 3 is truthfully declared not met, and the scope matches the partial-PR ruling
[R276] PASS RTL - gptp-processor gitlink e5dcea6e (donor main, tree 5a02fa35 = ba926810); syn/yosys/rom_digests.tsv row 4afe436d reproduced; hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv:303-305,434-436; hdl/milan/milan_datapath.sv:1935-1936,2743,3091-3092,5965-5967 (step consumers, unchanged); KL_media_grid_align.sv:97-106, KL_media_nco.sv:89-112, KL_media_clock_restart.sv:167, KL_mmcm_drp_servo.sv guard; milan_dp gptp 181/181, gptp_shadow 309/309, clkvalid 55/55 - no parent RTL in the diff, and every RTL fact the pages state matches the source
[R276] PASS Robustness - tb/verilator/milan_dp/sim_gmstep.cpp:916-960 (trailing silence, rate, counter validity), :963-1024 (event windows), :1045-1061 (feed-delay argument; receipt 70), transport bounds :660-698; 125 feed delays on the edited copy; mutants D3, D4, D6, D7 - the arms fail on late, silent and stopped behaviour and pass a correct datapath at every start phase, with margins of about 2x on every window
[R276] PASS Tests - sim_gmstep.cpp 48 checks at head (44/48, the four declared failures) and on the edited copy (48/48 x 125 delays); seven reviewer mutants D1-D7 each caught by the named check they target; Makefile:275-293 recipe exercised with GMSTEP_FEED_DELAY=12 - every new arm can fail for its defect, and none fails a correct datapath
[R276] PASS Docs - GM_LOSS_RECOVERY.md:109-153,179; TIME_SYNC.md:75-107; tb/verilator/milan_dp/README.md:340-398; Makefile:99-101,275-293; sim_gmstep.cpp:1-62 banner; 12 static docs and code gates at head - every stated fact was checked against code, run output or decision text; two SUGGESTIONs only
```

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #387 acceptance, decisions 5606198212(b) and 5794731090, rulings 5802264260 and 5798089412, assignment 5804878668; PR body; GM_LOSS_RECOVERY.md:109-153; TIME_SYNC.md:75-107; REQ-PTP-05/07/08/09 | R276-2 | 021b2e07b009158bcb0ce19529126eb1d330bba5 |
| RTL | CLEAN | gitlink e5dcea6e and donor ancestry; ROM digest reproduction; KL_gptp_txret envelope; datapath step consumers; aligner, NCO, restart and servo interfaces; milan_dp gptp, gptp_shadow and clkvalid runs | R276-2 | 021b2e07b009158bcb0ce19529126eb1d330bba5 |
| Robustness | CLEAN | sim_gmstep.cpp licence, event-window and argument paths; 125-delay sweep with margins; mutants D3, D4, D6, D7 | R276-2 | 021b2e07b009158bcb0ce19529126eb1d330bba5 |
| Tests | CLEAN | sim_gmstep.cpp at head and on the edited copy; Makefile gmstep recipe; mutants D1-D7; phase sweep | R276-2 | 021b2e07b009158bcb0ce19529126eb1d330bba5 |
| Docs | CLEAN (two SUGGESTIONs) | GM_LOSS_RECOVERY.md; TIME_SYNC.md; milan_dp README and Makefile comments; sim_gmstep.cpp banner; static docs and code gates | R276-2 | 021b2e07b009158bcb0ce19529126eb1d330bba5 |

## Limits

**Banks not run.** No full parent, protocol-processor, gPTP, Yosys or builder bank was run, and neither were act, host act_ci or hardware. Also not run here:
- the `milan_dp` `run` recipe;
- `gptp_shadow` lifecycle and mutants;
- `gptp_plane`, `gptp_txts`, `media_grid_align` and `tsn_fuzz`;
- `test_builder.py`, `lint_rtl`, `xvlog_gate` and the donor suites.

The manager's source banks are the evidence for those. The assignment states that they passed at this head. I found no separate manager-bank comment at this head on #387 or #540; the public evidence tree at `37d91083` archives the author packets and the round-1 reviews.

**No physical evidence.** Physical calibration was NOT RUN, and acceptance 4 (the #117 bench) was not attempted. The skipped physical nightly context is not hardware proof.

**The probes judge the harness, not a shipped fix.** They run on scratch copies of the published proposed patch, which belongs to the follow-up lane. Some of its design is not reviewed here: the restart is no longer gated by clock source, and the ruling-2 merge is not implemented.

**The author's own ten controls were not re-run.** Seven independent mutants stand in for them.

**One step phase only.** The counted re-base landed at +132 cycles at every feed delay, because the Sync carrying the step is scheduled into the AAF gaps. The 500-cycle window is therefore exercised at a single step-to-PDU phase. Its bound, one PDU period plus the pipeline, keeps it safe, and D4 shows that the window can fail.

**The gmstep model is limited.** It runs a 2 MHz compressed fabric with the TDM clocks held and the DRP answering zero, and the talker is opened by the escape bit. It grades the AAF talker's `mr` and Stream Output 0's MEDIA_RESET, not the CRF output's. The CRF output shares the engine-wide target in `KL_media_clock_restart`.

**Outside this diff.** `sim_aclk.cpp:141` and `milan_dp_render/sim_tdm8_render.cpp:165` also grade at-accept "registration slack". They are not examined here.

**The live-dev candidate was not built.** Live dev `50e78097` touches `docs/design/TIME_SYNC.md` (base line 111) and `tb/verilator/milan_dp/README.md` (base line 499), away from this PR's hunks.

## Pending manager duties

- Build and gate the current-dev candidate at the merge turn. The source base is `759da623` and live dev is `50e78097`, which overlaps this PR in `TIME_SYNC.md` and the milan_dp README. After the merge, re-run the docs gates on the candidate.
- Own hosted and act acceptance at the exact head.
- Obtain the external re-review (R277).
- Obtain the owner's ruling on the grid aligner's re-centre (#387, 5805175917 question 1).
- In the follow-up after #529:
  - apply the datapath edit, with ruling 2's merge arm;
  - wire `gmstep` and its negative-control runner into the sweep;
  - turn the "Not yet" rows;
  - add the CHANGELOG entry.
- Keep #539 open.
- Run the #117 bench (acceptance 4).

## Clone state after the probes

`receipts/90-clone-final.txt` is a PASS:
- HEAD, the tree and the index tree equal the exact head.
- All 873 tracked blobs of the superproject match HEAD's bytes and modes, and no index entry carries a hide flag.
- The three required submodules match their gitlinks blob for blob: `gptp-processor` 103, `protocol-processor` 222, `third_party/verilog-axis` 213 blobs plus one symlink.
- `external` is uninitialised by design.
- `git status --ignored` is empty in the superproject and in all three submodules. Every build output this session created in the clone was removed.
- Probe trees live only under the packet's `scratch/`.

## Receipts

Listed in `MANIFEST.sha256`.

**Clone and tools:**
- `receipts/00-clone-baseline.txt`, `receipts/90-clone-final.txt`: the clone before and after.
- `receipts/01-tool-identity.txt`: the pinned Verilator 5.050 wrapper and binary digests.

**Static gates, pin and edited copy:**
- `receipts/10-static-gates.txt`
- `receipts/11-pin-and-rom.txt`
- `receipts/12-edited-copy-provenance.txt`

**Hosted contexts:**
- `receipts/20-hosted-check-runs.tsv`

**The gmstep leg at head:**
- `receipts/30-gmstep-head-delay0.log`
- `receipts/31-gmstep-head-delay12.log`
- `receipts/32-make-gmstep-delay12-run.log`

**The phase sweep on the edited copy:**
- `receipts/40-edit-sweep-summary.txt`
- `receipts/41-edit-sweep-margins.txt`
- `receipts/42-edit-sweep-logs.tar.gz`

**The reviewer mutants:**
- `receipts/50-mutants-summary.txt`
- `receipts/51-mutant-diffs.txt`
- `receipts/52-mutant-logs.tar.gz`

**Consumer suites and the feed-delay argument:**
- `receipts/60-consumer-suites.txt`
- `receipts/70-feed-delay-argument.txt`

**Scripts:**
- `scripts/verify_clone.sh` and `scripts/verify_blobs.py`: clone and blob verification.
- `scripts/build_gmstep.sh`, `scripts/run_gmstep.sh`, `scripts/sweep_delays.sh` and `scripts/run_matrix.sh`: build and run.
- `scripts/make_mutants.py`: the mutants.
- `scripts/sweep_margins.py`: the margins.

Reproduce the mutants in three steps:
1. `make_mutants.py <edited datapath> <tree KL_render_setpoint.sv> <outdir>`.
2. `build_gmstep.sh <clone> <verilator> <mdir> DP_SRC=... [RSP_SRC=...]`.
3. `run_matrix.sh <clone> <logdir>`, fed `name mdir delay` lines.

R276-2 FINISHED
