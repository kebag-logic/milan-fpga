[R634] POSITIVE - exact head 75853d80c22893448936bd1890e782bd0a0ce642

# R634-2: internal cleared-context re-review of PR #758 (Refs #117), bench lane B21, PR round 2

Head `75853d80c22893448936bd1890e782bd0a0ce642`, tree `02e138dde9cad84cac346fe3d0d0bc35d61be435`.
Delta: one commit on `867fb945`, `docs/findings/117_AUDIO_CONTINUITY.md` only (+232, -57), under the
round 2 assignment (PR #758 comment 6231784136). Source base `4a9b5a2a74fe793a637745fd3ccf51ad2eaf93b4`.
Offline review: no bench action, no source edit, no GitHub write.

**Bottom line.** Every round 1 finding is resolved at its cause at this head. The restart row is now
bounded from the rebind command to the first valid output sample. The upper bound is causal on one
clock, so it contains every output latency. I recomputed it with my own script from the raw records,
without the author's code, and got identical values for all 20 cycles. The planted-latency controls
behave as stated. The corrected McASP grader compares slot words. Its collision control now fails, and
on the real Direction B recording it agrees with the exact comparator. All nine PR round 2 analyses
re-run from the published tools reproduce their published outputs byte for byte. No BLOCKER, MAJOR or
MINOR is open. Three RESIDUE items and four SUGGESTIONs are below.

## Reconstruction and inputs

- **Authority read, in order.** AGENTS.md and CONTRIBUTING.md; #117 body (box 4, audio continuity);
  the B5 assignment (#117 comment 5925737609: "time from each rebind to the first valid sample") and
  the B21 assignment (#117 comment 6208207821: "restarts under 1 s", every frame bit-exact and in order);
  the PR round 2 assignment (6231784136); the author's REVIEW READY (#117 comment 6232012039); the PR
  body; then the delta and the full round 3 section at the head (`:850`-`:1350`).
- **Packet.** Evidence commit `68f0200e64ce3e631cb38a920e62134656d0132d`, `review-evidence/117-b21-r1/author-r2`.
  All 447 files match `published_sha256` in the commit's `MANIFEST.json`. 82 of them are label-masked.
  The three masked scripts' page hashes equal their `original_sha256` (`receipts/packet-verify.txt`).
- **Cold archive, read-only by path.** All 12 inputs the page and `pr2/REPRODUCE.txt` name match their
  SHA-256 (`receipts/archive-inputs.sha256`).
- **Order kept.** I wrote my independent pass (`receipts/independent-pass.md`) before reading the round 1
  review reports. I read them only to resolve their findings below. I read no round 2 report from another
  reviewer.

## Re-derivation (scripts/reproduce_pr2.sh, receipts/reproduce-compare.txt)

I re-ran every PR round 2 command from the published packet tools on the archive raws, concurrently.
All nine exit 0, and 24 outputs are byte-identical to the packet. These are `rA-bound.json`,
`rA-controls.json`, the four plant files, `probes.json` and all 13 grader outputs, `floor-groups.txt`,
`step1-verdict.json`, `dB-mcasp.json` and `dB-exact.json`. `dA-transit-crf.json` matches once its two
capture names are masked. The derived received-frame record rebuilds to `1976539998...2468`, the
page's hash.

| Page figure (head) | Re-derived | Receipt |
|---|---|---|
| Upper bound 27.5 / 33.5 / 100.7 ms, 20 of 20 under 1 s | 27.511 / 33.5025 / 100.725 ms; tool PASS; independent script identical per cycle | `restart_table_check.txt`, `indep_upper.txt` |
| Lower bound 23.2 / 23.7 / 96.7 ms | 23.158 / 23.7205 / 96.727 ms | `restart_table_check.txt` |
| Per-cycle table `:1218`-`:1239`, widths 3.8 to 12.8 ms | 20 of 20 rows equal the tool to 0.1 ms; widths are the unrounded difference | `restart_table_check.txt` |
| Realtime within 0.03 ms of monotonic | 29.56 µs over 19,001 reads | `indep_upper.txt` |
| Plants: 0.5 s passes, 0.903 s fails cycle 19 only, 1.0 s fails all | Same; cycle 19 at 0.903 s reads 1010.7 ms, and cycle 1 reads 951.0 ms | `reproduce-compare.txt`, `plant_margins.txt` |
| 486 to 540 wire frames after the last output frame | 486 to 540 | `restart_table_check.txt` |
| First output frame in the first AAF packet after the command | No AAF packet between any command and its response, and none in any hold; the last packet 9.68 to 10.80 ms after DISCONNECT_RX_RESPONSE | `probe_aaf_between.txt` |
| dB: 30,480,000 matched at 148,874, 0 unequal; exact comparator agrees | Same; 64-frame head unique | `reproduce-compare.txt` |
| 6,437,039 (21.1%) equal to previous, 20.9% all-zero, values -2 to +1 LSB, +1 23 times | Same (`dB-exact.json`) | `reproduce-compare.txt` |
| Seven grader controls, collision as-run "fully matched", leading insertion as-run exits 1 | Same; as-run `KeyError: 'wire_frame'` | `reproduce-compare.txt` |
| Floor groups: 8 positive +6.3 to +8.4, one -2.5 at reads 57,646 to 57,845, from 576.485 s; against drift +4.0 to +6.1 and -4.8; dips -12.4 to -18.4 | Same; the sign rule holds in 9 of 9 | `reproduce-compare.txt` |
| Sampler woke every 1.02 to 1.04 s | 1.0200 to 1.0400 s over 610 wakes, from the raw sampler record (the published tool prints it only at 0.1 s; see S-1) | `sampler_spacing.txt` |
| Step 1 mechanical verdict: 2.81 frames; plants 4.58 to 47.10; margin 0.58 to 1.82 | Same | `reproduce-compare.txt` |
| Transit -13.070107 ppm, residual -27.681 to +23.894 µs; CRF 324,903 and 324,906, 0 breaks, 500.0 pps | Same (499.993 and 500.0 pps) | `reproduce-compare.txt` |
| Round 1 losses: 17 of 20 above the control maximum; the other three +7.8, +6.8, -5.2 | `st-long` +13.6, +13.5 against a control maximum of +4.5; `st-long2` 15 of 18 against +7.8; the three as stated | published `selftest/st-long*/...-selftest.txt` |

### The upper bound and its clock: judged sound

- **Start.** `restart_b21.py` logs `binding-rule` with `time.time()` after the format reads. It then
  calls `acmp("bind")`, which writes the CONNECT_RX request to the controller agent. So the start
  precedes the rebind command, and the SSH and controller session lie inside the interval. The
  `bind` event comes 10.1 to 22.6 ms later (`indep_upper.txt`).
- **End.** The capture reader (`selftest_b21.py`, Reader.run) stamps `time.time()` and
  `monotonic_ns()` after `os.read` returns. It records cumulative frames. `cap-lr.raw` holds exactly
  those frames (9,120,023 = the last record's count). So the read that delivered the first valid frame
  returned after the peer output that frame. Every output latency, including the capture's own
  buffering, lies inside the interval.
- **One clock.** `restart_run_b21.sh` runs both `restart_b21.py` and the capture reader locally on the
  bench host. Pairing places every start between two capture reads, so the realtime-against-monotonic
  guard covers every cycle.
- **Guard falsified.** A planted realtime step of 1.1 ms or 5 ms is refused (rc 1). A 0.9 ms step is
  accepted and moves the maximum bound by 0.9 ms (`probe_rt_step.txt`). That is negligible against
  the 899 ms margin.
- **Lower bound.** It runs from the tap time of the peer's received CONNECT_RX_COMMAND to the packet
  carrying the first output frame's 16-bit counter. The counter is unique within the 1 s search (a wrap
  takes 1.365 s). The capture logged no overrun, so no earlier valid output frame was missed. The lower
  bound is not the graded figure, and the verdict also requires lower ≤ upper.

## Round 1 findings at this head

| Finding | Required outcome | At `75853d80` | Status |
|---|---|---|---|
| R635-1-F1 MAJOR (Conformance, Tests, Docs) | Rebind to valid output on a defensible time basis or a conservative bound; 20-cycle mechanical table; excessive latency must fail; page and PR consistent | Causal upper bound on the bench host clock; per-cycle table `:1218`-`:1239`; verdict in `b21_restart_bound.py:149`-`:150`; plants fail as predicted (`:1241`-`:1245`); summary `:872`, restarts `:1095`-`:1117`, limits `:1186`-`:1191` and PR body all consistent; round 3's figure kept and labelled replaced | RESOLVED |
| R635-1-F2 MAJOR (Conformance, Robustness, Tests, Docs) | Compare original words on alignment and runs; collision no longer fully matched; skip and repeat counts kept; real record agrees with the exact comparator; as-run kept | Packet `tools/pr2/b21_grade.py:198`-`:290`: `find` and the run loop use `np.array_equal` and `np.all(M == Wd)`, with a final per-frame word check (`clean` at `:283`); collision control 1 foreign; skip 6 and repeat 1 counts kept; real record clean and equal to `b21_exact.py`; as-run kept | RESOLVED |
| R635-1-F3 MINOR (Robustness, Tests) | Completed non-clean grade for a leading 3-zero insertion; isolated control | `first_wire_frame` comes from `off0`, not `ev[0]`; control `insert_3_zero_leading`: 3 foreign zero frames and an insertion of 3, rc 0 | RESOLVED |
| R635-1-F4 / R634-1-F1 MINOR (Tests, Docs) | Signed groups as printed; explanation qualified or backed for both signs; short floor excursions kept apart from the permanent-step check | `:946`-`:959`: 8 positive and 1 negative, as printed; "computed association ... not a proven mechanism", backed by the published `floor-groups.txt`; "no permanent step" `:869` | RESOLVED |
| R634-1-F2 MINOR (Tests, Docs) | Publish or remove (a) transit, (b) CRF, (c) 21%, (d) grader controls | All four published and reproduced (`dA-transit-crf.json`, `dB-exact.json`, `probes.json`) | RESOLVED |
| R634-1-F3 MINOR (Tests, Docs) | State the loss counts as printed | `:659`-`:671` gives 2 + 15 of 20 above the control maximum, and names the other three with their values | RESOLVED (wording residue R-1 below) |
| R634-1 R1 to R5 (RESIDUE) | Exact fixes | R1 `:869`, `:946`, `:1179`; R2 `:1011`-`:1013`, `:1078`-`:1082`; R3 `:1051`; R4 `:1346`-`:1349`; R5 `:758`-`:761` | APPLIED |
| R634-1 S1, S2 (SUGGESTION) | Optional | S1 `:1032`-`:1033`, `:1195`-`:1197` (corrected to -2 to +1 from the data); S2 by the new `b21_step1_verdict.py`, `:961`-`:968` | APPLIED |
| R634-1 S3, S4, S5 (SUGGESTION) | Optional, not assigned | Not applied | RETAINED as S-2 |

## Findings of this round

No BLOCKER, MAJOR or MINOR.

**R634-2-R-1 - RESIDUE - Docs - `docs/findings/117_AUDIO_CONTINUITY.md:667`.**
- *Evidence.* "So the 17 losses with a shortfall point below the load" reads as if the other three have
  none. Two of them (+7.8 and +6.8) have a positive shortfall. They just do not exceed the control
  maximum.
- *Exact fix.* Write "So the 17 losses whose shortfall exceeds the control maximum point below the load".
- *Impact.* Wording only. The counts and values beside it are correct.

**R634-2-R-2 - RESIDUE - Docs - `docs/findings/117_AUDIO_CONTINUITY.md:1013`.**
- *Evidence.* The edited line is 106 characters long, inside a paragraph wrapped at about 78.
- *Exact fix.* Rewrap `:1010`-`:1014` to the page's width.
- *Impact.* None in the rendered page.

**R634-2-R-3 - RESIDUE - Docs - author REVIEW READY (#117 comment 6232012039) and packet `REVIEW-READY-pr2.md:5`.**
- *Evidence.* "in the round 3 section and one round 1 sentence" is inaccurate. The commit edits two
  round 1 passages: the loss-placement paragraph `:659`-`:671` and the raw-retention sentence
  `:758`-`:761`.
- *Exact fix.* In any republished handoff text, write "in the round 3 section and two round 1 passages
  (the loss placement and the raw-file retention sentence)".
- *Impact.* Wording only.

**S-1 - SUGGESTION - Tests, Docs - packet `tools/pr2/b21_floor_groups.py`.** The page's "1.02 to 1.04 s"
(`:951`) is correct, but the published tool prints wake spacing only at 0.1 s ("+1.0"). Print the
minimum and maximum spacing at 0.01 s so the figure is in a published output.

**S-2 - SUGGESTION - Docs - retained from R634-1 S3, S4, S5.**
- S3: link the public owner decision behind the resume terms.
- S4: restate in round 3's limits the configuration dependence, with the DUT on INTERNAL only and the
  peer following the DUT's CRF.
- S5: state that "the taps kept every packet" refers to the written records.

**S-3 - SUGGESTION - Tests - packet `tools/pr2/b21_restart_controls.py:45`.** The expected-failure rule
`u + d >= 1.0` ignores the read quantum, which the tool's own comment notes is up to 22.75 ms. At 0.903 s
the observed shift was 899.8 to 910.0 ms, so the outcome is safely predicted. Choosing plants that
clear every cycle's threshold by more than one quantum would make each control independent of read
quantization.

**S-4 - SUGGESTION - Docs - `:1186`-`:1191`.** Add one clause to the restart-bounds limit: the start
stamp precedes the controller session. Also say that this session (SSH and agent) is part of why the
upper bound sits 3.8 to 12.8 ms above the tap-clock lower bound.

**Comment rule.** The delta is Markdown only and adds no source comment. The new lane and review labels
are in a findings page, where lanes may be named. The packet tools are outside the tracked tree.

## Lenses

| Lens | Result | Artifact | What was checked, at `75853d80` |
|---|---|---|---|
| Conformance | PASS | `docs/findings/117_AUDIO_CONTINUITY.md:866`-`:878`, `:1084`-`:1135`, `:1202`-`:1300`; #117 box 4; B5 and B21 assignments | The restart endpoint is the criterion's (rebind command to the first valid output sample, under 1 s). The bound is conservative and causal, recomputed independently. Direction B bit-exactness is re-graded with word comparison and equals the exact comparator. The row claims in the summary, restarts, limits and PR body agree. |
| RTL | PASS | `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:108`-`:110`, `:640`; `tests/features/counters_contract_milan.feature:189`-`:194`; page `:1077`-`:1082` | The diff has no RTL. The one hardware-semantics sentence it adds (FRAMES_RX commits the interval total, observation interval at most 1 s) matches the RTL and the counter contract. The CSR readings (`SLIP_TDM`, `RENDER_STAT`) are unchanged from round 1. |
| Robustness | PASS | packet `tools/pr2/b21_grade.py:198`-`:290`, `tools/pr2/b21_restart_bound.py:66`-`:161`; `receipts/probe_rt_step.txt`, `probe_aaf_between.txt` | Leading insertion, collision, foreign and zero cases complete with non-clean grades. An unaligned record cannot be clean (`matched == len(M)`). The bound tool fails closed on an unpaired silence, a short first run, an inconsistent lower bound or a realtime step over 1 ms (probed). No packet sits between command and response or in any hold. |
| Tests | PASS | `scripts/reproduce_pr2.sh`, `receipts/reproduce-compare.txt`, `indep_upper.txt`, `plant_margins.txt` | Each control can fail: the as-run grader passes the collision and crashes on the insertion, and the 0.903 s and 1.0 s plants fail. Every published output reproduces byte for byte. My independent upper-bound script matches all 20 cycles. |
| Docs | PASS (3 RESIDUE) | `docs/findings/117_AUDIO_CONTINUITY.md` delta; PR body; `receipts/gates/` | Every figure in the delta traces to a published output or a re-derivation. The tool and input hash tables match the packet and the archive. The contents line is updated. Docs gates rc 0 at the head (docs_check, doc style, TOC, em dash at `e4b771f9`, doc paths, `git diff --check` against `4a9b5a2a` and `867fb945`). No host, instrument, interface or path names in the delta. |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Page `:850`-`:1350`; #117 box 4; B5/B21/PR round 2 assignments; `rA-bound.json`; independent bound | R634-2 | 75853d80c22893448936bd1890e782bd0a0ce642 |
| RTL | CLEAN | `KL_avtp_rx_monitor_ctx.sv:108`-`:110`, `:640`; `counters_contract_milan.feature:189`-`:194`; page CSR/counter text | R634-2 | 75853d80c22893448936bd1890e782bd0a0ce642 |
| Robustness | CLEAN | Corrected grader; bound tool; realtime-step and command/response probes; grader controls | R634-2 | 75853d80c22893448936bd1890e782bd0a0ce642 |
| Tests | CLEAN | Nine PR round 2 analyses reproduced; independent upper-bound recomputation; controls | R634-2 | 75853d80c22893448936bd1890e782bd0a0ce642 |
| Docs | CLEAN (RESIDUE R-1 to R-3 to the checklist) | Page delta; PR body; REVIEW READY; docs gates; hash tables | R634-2 | 75853d80c22893448936bd1890e782bd0a0ce642 |

## Real limits of this review

- **Offline only.** No bench action ran. Physical calibration was NOT RUN. Offline controls and field
  skips are not hardware proof.
- **Scope of the delta.** Round 3 content the delta does not touch keeps R634-1's verdict, which
  re-derived those figures at `867fb945`. The delta changes nothing those figures depend on.
- **Decoder.** The received-frame record is rebuilt with the author's unchanged decoder `b21_aaf.py`
  (identical in `tools/` and `tools/pr2/`). My command/response probe uses the author's tap parser. The
  upper bound, the realtime-step probe and the sampler spacing use my own code.
- **Clock.** The upper bound rests on the bench host's realtime clock inside the guard's 1 ms. The guard
  is verified, but the clock's rate is not independently calibrated. A rate error of even 1,000 ppm
  moves a 100 ms bound by 0.1 ms.
- **Signal.** Direction B's signal is low-level noise (-2 to +1 LSB). The page states this limit.
- **Hosted checks.** At read time, `bdd-conformance`, `full-ci-gate` and one `Fail fast across this
  head` had succeeded. `changes`, docs-gates, elaborate-gates and wire-accountability were queued or in
  progress. `verilator-suites`, `yosys-portability`, their shards and the physical gPTP job were
  skipped (`receipts/hosted-checks-75853d80.txt`). Skipped contexts are not executed evidence.
- **No manager source bank** runs at this head, and this review infers none. Source-head execution
  evidence is the author's published gate receipts, 11 of 11 rc 0, which my own docs gates confirm.

## Pending manager duties

- Obtain the external re-review (R635-2) and accept a clean ledger from both reviewers.
- Carry R634-2-R-1 to R-3 to the residue checklist.
- Validate the current-dev merge candidate at the merge turn (source base `4a9b5a2a`, live dev
  `1f6f2f57`), with builder and native banks, and link the receipts.
- Own hosted and local act acceptance at the exact head.
- Obtain maintainer merge authorization, then run post-merge containment.
- The PR says Refs #117. Box 4's other rows and #117's other boxes stay open, as does the deferred
  serial-audio evidence (#448).

Restore: the clone is at the exact head. Worktree equals index equals HEAD, and nothing is untracked or
ignored after I removed the `scripts/__pycache__` my gate run created. Six gitlinks match the head tree
(`receipts/restore-check.txt`).

R634-2 FINISHED
