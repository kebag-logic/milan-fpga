[R634] POSITIVE - exact head c2243f791ced37dd2288dbf870758d93c5aa5325

# R634-2: internal independent delta review of PR #751 (issue #117, #387, #621; bench lane B19, round 2)

Head `c2243f791ced37dd2288dbf870758d93c5aa5325`, tree `ece348805565c8c0b12bd6c90eccf512ef46c222`, detached clone, cleared context. Source base `734eb780dc93896a5961cd95180f79475a401650`. The delta under review is the six one-line commits `d812a604..c2243f79` on the manager's privacy amend `d812a604` of `18b98bbc`, all in `docs/findings/117_GPTP_SILICON_EVIDENCE.md` and `docs/findings/387_SOFTWARE_GM_STEP.md` (+131/-47). They were made under the round-2 assignment (PR #751 comment 6208623939). No bench, hardware, Docker/act, or GitHub write was used in this review. Physical calibration was NOT RUN.

Verdict basis: every round-1 finding (R635-1-F1, F2, F3, R1, R2 and R634-1-F1 to F5, R1, R2, S1) is resolved at this head (table below). This round found no BLOCKER, MAJOR or MINOR. It records two SUGGESTIONs and one RESIDUE. All five lenses are covered clean at this head.

## Reconstruction

- Read AGENTS.md and the #117 issue body (frozen acceptance, boxes 1 to 5). Read the manager comments: the B19 assignment 6207451080, the round-2 assignment 6208623939 (items 1 to 8), the privacy amend 6208484697, the raw-retention receipt 6208612856, the author's REVIEW READY 6217741415 and the review start 6217817979. Also read the PR #751 body.
- Authorities checked against the delta's claims:
  - `docs/design/GM_LOSS_RECOVERY.md:105-106`: announce receipt timeout 3 s, sync receipt timeout 0.375 s.
  - `sw/firmware/milan_baremetal/milan_baremetal.c:1896-1938`: `milan_status_handler` reads the CSRs, prints two lines, then reads the PHC.
  - `configs/endstation_ax7101_1x1_tdm8.yaml:43,51`: 100 MHz system clock, 115,200 baud.
  - The pinned LiteX `a1e1c3652ec2` (`sw/litex/litex_pins.txt:53`), read-only:
    - `soc/software/libbase/uart.c:13-29,93-118`: `UART_POLLING` is not defined, and the TX ring has 128 entries, 127 usable.
    - `soc/software/libc/stdio.c` `litex_putc`: each `\n` goes out as `\n\r`.
    - `soc/integration/soc.py`: `add_uart` `fifo_depth=16`. The repository sets no override.
- Evidence:
  - The published packet at evidence commit `633b6e33`, sub-tree `author-r2`.
  - The 151 raws, read-only in the cold archive.
  - PR #747's provenance record at `bbc53aab` and its comment 6200503436.

My independent pass over the diff and the evidence came first. I read the two round-1 reports (R634-1, R635-1) only after it, to settle their findings.

## Evidence verified (receipts in this packet)

| Check | Result | Receipt |
|---|---|---|
| Published evidence tree against its publication manifest | 582 of 582 files equal; 85 path-redacted entries consistent; 0 unlisted. The 42 `author-r2/MANIFEST.sha256` mismatches are all publication path redactions, plus one file never published. Every round-2 tool and output is unredacted and equals the author manifest | `receipts/publication-check.txt`, `receipts/author-r2-manifest-check.txt` |
| 151 raws in the cold archive against `RAW-ARTIFACTS.json` | 151 equal, 0 differ, 0 missing (agrees with manager receipt 6208612856) | `receipts/raw-rehash.txt` |
| Round-1 `corr_analyze.py` re-run on the archive (raw root only changed) | all six `bench/cycleNN/correlation.json` byte-identical to the published ones | `receipts/correlation-regen.txt` |
| Round-2 tools re-run on the archive | `box3-model.json`, `box3-grade.json`, `box3-grade.md`, `gm-steps-r2.json`, `gm-steps-r2.md` and `box4-derivations.json` are byte-identical to the published outputs, and their SHA-256 and sizes equal the page tables (`117:1099-1104`, `387:522-523`). Box 3 selftest 13 of 13 and GM selftest 9 of 9, also byte-identical | `receipts/rerun/` |
| Independent GM-step re-derivation (own parser) | 2,399 samples with 0 asCapable 0. 600 DUT GET_AVB_INFO polls, all answered, 0 asCapable 0; 36 per takeover window and 83 per release window. Peer delay 373 to 392 ns in both arms. Every `tu` set and steady-clear time equals `387:447-456`, including the four corrected set rows. Steady after set 0.25 to 0.75 s. Exactly two edges have a single `tu=1` sample | `receipts/probe_gm.txt` |
| Independent box 4 figures (decoded from GET_COUNTERS payload bytes) | Peer Stream Input 8 FRAMES_RX +149,513 over 300 polls, 499.99/s. DUT CRF FRAMES_TX +149,514. 26 first and last reads, lag 167 to 7,925. 1,495 polls, lag 0 to 7,925, 0 negative. 0 payload/decoded mismatches | `receipts/probe_box4.txt` |
| Independent box 3 closest edges (own pcap and console parsing, unrounded) | Cycle 1 GM loss: -10.26 ms at d = 0, lower margin 0.65 ms with the measured placement error, 0.60 ms with the model's full u. Cycle 3 GM return: -9.03 ms at d = 0, 1.83 ms. Cycle 5 GM return: -3.71 ms, 7.15 ms. Cycle 4 GM return: 15.84 ms. Each agrees with the grader within the 0.1 ms input rounding | `receipts/probe_box3.txt`, `receipts/probe_c1_margin.txt` |
| DUT PHC against the tap clock | 78 consecutive neighbours per cycle at 7.36 to 8.36 ppm. The only other intervals are the dark gap (no step) and one grandmaster-return step of -125 s to -1,362,194 s per cycle. That step is far beyond the 3 s PHC pairing distance and the 0.2 s coarse check, so no sample is placed across it, and the stated 0.075 ms PHC placement error holds | `receipts/probe_phc_steps.txt` |
| End-to-end mutations of both graders through their main paths | One gm03 DUT poll set to as_capable 0: `r2_gm.py` rc 1, that edge FAIL. Cycle 3 last Sync +8 ms: `r2_box3_grade.py` rc 1, sync loss FAIL. d_lo reduced by 8 byte times (a store 8 bytes larger): rc 1, cycle 1 GM loss FAIL, confirming the page's "more than 7 bytes" sensitivity | `receipts/gm-mut.out`, `receipts/grade-mut.out`, `receipts/grade-mut3.out` |
| Host clock identity: the takeover Announce's priority1-240 identity, found in the gm01 to gm05 tap captures and never printed | 0 hits under `docs/` at HEAD in five spellings. 0 hits in the PR body, comments 6217741415, 6208623939 and 6208612856, and all 183 text files of the published `author-r2` packet | `receipts/probe_host_identity.txt`, `receipts/probe_identity_text.txt` |
| Image provenance | `provenance.json` at `bbc53aab`: dev merge `9ef71772`, bitstream SHA-256 `4b5a391a...4ffcca`, 3,825,992 B; AEM `4fc8d615...db396d`, 7,512 B; cold boot `VERSION=00020060`, CRC `5ba355eb`. Comment 6200503436 item 5 gives the B18 end, 18:59:53 UTC, as the page states | `receipts/provenance-bbc53aab.json` |
| Documentation gates at the exact head | `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base 734eb780` (0 findings over 509 added lines), `check_doc_paths.py`, `gen_toc.py --verify-anchors`, `git diff --check`, `git diff --check 734eb780 HEAD`: all rc 0 | `receipts/gates/` |
| Hosted contexts at the exact head (inspected, not owned) | `rtl-fast`, `changes`, `docs-check-no-git`, `elaborate*`, `bdd-conformance`, `wire-accountability` and `full-ci-gate` succeeded. `docs-gates-0/1/2` were in progress at inspection. Verilator, Yosys, firmware and union contexts were skipped by scope (docs-only), so they are not executed evidence | `receipts/hosted-checks-c2243f79.txt` |
| Clone integrity after probes | HEAD, tree and index equal `ece34880`; worktree clean; six gitlinks unchanged | `receipts/clone-integrity.txt` |

## Round-1 findings: disposition at this head

| Finding | Required outcome | Evidence at `c2243f79` | Status |
|---|---|---|---|
| R635-1-F1 (MAJOR, Docs) / R634-1-F5 (MINOR, Docs): controller host clock identity | Role label; no equivalent representation in the delta or PR text | `387:474` reads "the controller host's clock identity, priority1 240, stepsRemoved 1". The value, derived from the raws, has 0 hits under `docs/`, in the PR body and comments, and in the packet | RESOLVED |
| R635-1-F2 (MAJOR) + R634-1-F2 (MINOR), all five lenses: box 3 time base and criterion | Stated criterion, time base with read-to-PHC offset bounded from line bytes and baud, tolerance; a mechanical grader over every `correlation.json` that can fail; near-boundary edges with margins; verdict follows the grader | `117:866-873` state the offset (N = 271/272, S = 144, 86.8 us per byte, Q ≤ 14, per-record idle, 1 ms CPU), the placement error and the criterion. I verified the byte-store model against firmware and pinned LiteX source. My own round-1 estimate of 20 to 23.5 ms assumed a 16-byte store and is superseded: the 128-entry software ring is compiled in. `r2_box3_grade.py` grades all 27 edges and fails on breach (13 planted controls, plus my three end-to-end mutations). `117:984-1016` give the verdict, the 11 near-boundary rows (all equal to the grader) and the store sensitivity. The three round-1 counterexamples are reconciled: -10.2, -9.1 and -3.7 ms at d = 0, inside at d ≥ 10.9 ms. The loss spans at `117:950` and the table at `117:976-982` equal the grader's `ranges` | RESOLVED (SUGGESTIONs R634-2-S1 and S2 below) |
| R635-1-F3 (MINOR, Conformance/Tests/Docs): `tu` set and clear times | Full transition history, one convention with uncertainty, regenerated rows and durations, boundary control, wire, console and completion kept distinct | `387:425-441` give the convention, interval ≤ 0.282 s and round-1 defect. `:447-456` rows equal my independent history. `:458-460` give 0.25 to 0.75 s, wire 0.376 to 0.684 s, and console 0 to 0.53 s at the single-sample edges. `:484` is the contract row. The control keeps the first asserted sample and shows the round-1 search drops it. Wire and console stay on separate clocks: one wire last `tu=1` PDU (run 5 takeover) falls 24 ms before its console clear interval, inside the coarse cross-host error, and the page makes no cross-clock claim | RESOLVED |
| R634-1-F1 (MINOR, Conformance/Docs): image identity | Provenance link, bitstream and AEM SHA-256, reads stated non-distinguishing, continuity basis | `117:835-838`, `387:374-381`: link to the `bbc53aab` record; both hashes equal `provenance.json`; reads stated non-distinguishing; continuity from item 8 of 6208623939 | RESOLVED |
| R634-1-F3 (MINOR, Conformance/Tests/Docs): poll arm and underived figures | Poll arm with a mutation control; each figure derived by published tool output or removed | `r2_gm.py` `poll_arm`; a planted poll FAILs, in the selftest and in my end-to-end mutation. 600/0, 373 to 392 ns, 149,513, the 26-read lag 167 to 7,925 and 1,495 polls 0 to 7,925 are all in `gm-steps-r2.json` / `box4-derivations.json`, and my own parsers reproduce them. `387:386,415,461,482`, `117:1024,1029` | RESOLVED |
| R634-1-F4 (MINOR, Conformance/Docs): raw retention | Durable retention receipt cited on both pages | `117:1071-1077` and `387:503-507` cite 6208612856; my re-hash in the archive: 151 equal | RESOLVED |
| R635-1-R1 / R634-1-R1 (RESIDUE): PR body Status | wording | PR body Status: "Published for independent review; PR open against `dev`; reviewers R634 (internal) and R635 (external)" | RESOLVED |
| R635-1-R2 (RESIDUE): probe parity wording | wording | `117:822`, `:1023` and the PR body: "identical result lines; the target-identity line differs" | RESOLVED |
| R634-1-R2 (RESIDUE): base GM_CHANGED count | wording | `387:391-392` "rise of 3 at nine of the ten edges", which agrees with `387:211,241` | RESOLVED |
| R634-1-S1 (SUGGESTION): servo observable line | optional | `387:400` added; the PR body's limitations repeat it | RESOLVED |

## Findings (this round)

### R634-2-S1: SUGGESTION (Tests, Robustness): the grader's rounding allowance covers one of two rounded inputs

- **Where:** `review-evidence/117-b19-r1/author-r2/tools/r2_box3_model.py:41,108` (`ROUND = 0.05e-3`, added once to u) and `tools/r2_box3_grade.py:41-42`, applied to `bench/cycleNN/correlation.json`. That file rounds both the sample brackets and the wire causes to 0.1 ms.
- **Evidence:** The model's docstring says the 0.05 ms covers "the 0.1 ms rounding of the published times". Each margin, though, subtracts two rounded times (cause and sample), so the combined rounding error can reach 0.1 ms. On the closest edge my unrounded computation gives -10.261 ms at d = 0 against the grader's -10.2 (`receipts/probe_c1_margin.txt`). Its lower margin is 0.65 ms with the measured placement error, against the published 0.66 ms. The store sensitivity is unchanged: 8 bytes breach and 7 do not, as `117:1013-1016` state.
- **Impact:** None on any verdict or quoted figure at this head. The tool could overstate a margin by up to 0.05 ms beyond its stated allowance on a future edge within 0.1 ms of a boundary.
- **Optional change:** Grade from unrounded times, or set the allowance to cover both rounded operands.

### R634-2-S2: SUGGESTION (Tests): `excluded_steps: 0` in `box3-model.json` hides the one PHC step per cycle

- **Where:** `tools/r2_box3_model.py:84-93`; `round2/box3-model.json` `phc_vs_tap.excluded_steps`.
- **Evidence:** Each box 3 cycle has a grandmaster-return PHC step of -125 s to -1,362,194 s (`receipts/probe_phc_steps.txt`). The tool drops that interval through its 0.5 to 3.5 s window before the step test, so it reports 0 steps, and the dark gap is dropped silently the same way. The placement is unaffected: the 3 s pairing distance and the 0.2 s coarse check keep every sample on its own side of the step.
- **Optional change:** Report window-excluded intervals (the gap and the step, with sizes) beside `excluded_steps`.

### R634-2-R1: RESIDUE (Docs): `docs/findings/117_GPTP_SILICON_EVIDENCE.md:872`, placement-error sentence

- "The DUT PHC ran 7.4 to 8.4 ppm from the tap clock over every pair of its Pdelay responses" overstates the set. Two of the 80 neighbour intervals per cycle, the dark interval and the grandmaster-return step, are not rates. The figure stands.
- **Exact fix:** replace "over every pair of its Pdelay responses," with "over every pair of consecutive Pdelay responses on one PHC time base (78 per cycle; the dark interval and the grandmaster-return step of 125 s or more are excluded, and no sample is placed across that step),".
- This changes no measurement, figure, verdict, test, code, artifact or privacy claim. It does not leave a lens unclean.

Comment rule: the delta changes no source file, so it has no source comment to judge. Lane names appear only in findings pages and PR text, where they are allowed.

## Lens coverage (each with its artifact)

- `[R634] PASS Conformance` (`117:821,835-838,866-873,950,976-1016`; `387:374-392,412-460,482-484`):
  - The box 3 criterion was checked against the `GM_LOSS_RECOVERY.md:105-106` timeouts and REQ-PTP-07 publication.
  - #621 item 3 holds through both asCapable arms (0 of 2,399 samples, 0 of 600 polls).
  - #387 item 4 holds: one `tu` episode per edge, wire holdover ≥ 0.376 s ≥ 0.25 s.
  - Image identity rests on provenance `bbc53aab` and receipt item 8, and the #117 box 5 hashes were re-verified.
- `[R634] PASS RTL` (`milan_baremetal.c:1896-1938`; pinned LiteX `uart.c:13-29,93-118`, `stdio.c` `litex_putc`, `soc.py` `add_uart fifo_depth=16`; config `:43,51`):
  - The delta changes no RTL, firmware or interface. Its stated read-then-print-then-PHC ordering and the 144-byte TX store are true of the shipped source.
  - Under interrupts disabled the bound still holds, because the measured per-record idle term absorbs any stall.
- `[R634] PASS Robustness` (`117:866-873,984-1016`; `receipts/probe_phc_steps.txt`, `probe_c1_margin.txt`, `grade-mut3.out`):
  - The near-boundary edges are listed.
  - The 0.66 ms margin's dependence on the store size is stated and confirmed by mutation.
  - Cross-step placement is excluded.
  - The rounding effect is ≤ 0.05 ms (S1).
- `[R634] PASS Tests` (`tools/r2_box3_model.py`, `r2_box3_grade.py`, `r2_gm.py`, `r2_box4.py`; `receipts/rerun/`, `correlation-regen.txt`, mutation receipts):
  - The chain from raws to `correlation.json` to grade reproduces byte for byte, and both selftests pass.
  - Three end-to-end mutations fail as required, and the independent parsers reproduce every quoted figure.
- `[R634] PASS Docs` (both pages' B19 sections, PR #751 body; `receipts/gates/`):
  - All round-1 wording items are applied.
  - The hash and size tables equal the files.
  - No private identifier is present.
  - Gates rc 0. One RESIDUE (R634-2-R1).

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `117_GPTP_SILICON_EVIDENCE.md` B19 sections; `387_SOFTWARE_GM_STEP.md` B19 sections; `GM_LOSS_RECOVERY.md:105-106`; provenance `bbc53aab`; receipts 6208612856, 6208623939 | R634-2 | `c2243f791ced37dd2288dbf870758d93c5aa5325` |
| RTL | CLEAN | `milan_baremetal.c:1896-1938`; pinned LiteX TX path (ring, FIFO, newline expansion); `endstation_ax7101_1x1_tdm8.yaml:43,51`; the diff touches no RTL or firmware | R634-2 | `c2243f791ced37dd2288dbf870758d93c5aa5325` |
| Robustness | CLEAN | near-boundary table and sensitivity; PHC-step probe; unrounded margin probe; store-size mutation | R634-2 | `c2243f791ced37dd2288dbf870758d93c5aa5325` |
| Tests | CLEAN | four round-2 tools and outputs (byte-equal re-runs, selftests 13/13 and 9/9); `correlation.json` regeneration; three end-to-end mutations; independent probes | R634-2 | `c2243f791ced37dd2288dbf870758d93c5aa5325` |
| Docs | CLEAN | both findings pages' delta, hash tables, PR #751 body; docs gates rc 0; identity scans | R634-2 | `c2243f791ced37dd2288dbf870758d93c5aa5325` |

Open at this head: SUGGESTIONs R634-2-S1 and S2, and RESIDUE R634-2-R1. None leaves a lens unclean.

## Real limits

- No hardware was used, and physical calibration was NOT RUN. Hosted skips are not hardware proof.
- The read-to-PHC model is reconstructed from source and from host-side record timing, not measured on the device:
  - The 144-byte store comes from source reading.
  - The 1 ms CPU allowance is an engineering bound.
  - The idle term is bounded from host timestamps, so it is loose and never short.
- The closest box 3 edge (cycle 1 GM loss) holds by about 0.65 ms only because of that lower bound. The page states this.
- Unchanged round-1 content was not re-reviewed beyond what the fixes touch. That includes boxes 1, 2 and 4, and the wire decoders, which I relied on only for wire times and spot-checked with my own parser.
- I ran no manager source bank and claim none. Source-head execution evidence is the author's published gates plus my documentation gates. I ran no full parent, PP, gPTP or Yosys bank, and no build.
- Hosted `docs-gates-0/1/2` were still in progress when I inspected them.

## Pending manager duties

- Publish this report and the files listed in `MANIFEST.sha256`.
- Carry R634-2-R1 to the residue checklist.
- Hosted and act acceptance at the exact head, including the in-progress docs gates.
- At the merge turn, build and validate the current-dev merge candidate (source base `734eb780`, live dev `8eacc408`) with the builder and native banks, and link the receipts.
- Merge only with explicit maintainer authorization, after the external delta review (R635-2) also clears.

R634-2 FINISHED
