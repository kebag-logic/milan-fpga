[R259] POSITIVE - exact head ba9268100ebe92dfc61aed30e2910245fc8c97cf

# R259-3: independent review of FPGA-gPTP #68 / PR #74, correction round 2

| Item | Value |
|---|---|
| Reviewer | R259, external cleared-context review, round R259-3 |
| Head | `ba9268100ebe92dfc61aed30e2910245fc8c97cf`, tree `5a02fa35db15d9a773895f82bb17020b55cfa775` (verified at start and end, `receipts/identity-start.log`, `receipts/identity-end.log`) |
| Base | `c1b617435824929a790739ea8585c3fe1a328cc0` (the parent's current `gptp-processor` pin) |
| Previous reviewed head | `cbccf226068c107fb30764891c98b8d70c54d775` (R258-2, R259-2) |
| Parent read for authority | kebag-logic/milan-fpga live dev `759da623072358afdb0e9d570a7b4b6a788492c9` |
| Simulator | Verilator 5.050, pinned wrapper sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`, `verilator_bin` sha256 `44898b22af4178b45214a0820a04eeac8632ae721ff005e69ef1cf69121bbfdd`; the system 5.052 was not used |
| Verdict | POSITIVE: no BLOCKER, MAJOR or MINOR open; one SUGGESTION (S1) |

## Reconstruction

Read in this order, from public state only:

1. Parent `AGENTS.md` and `CONTRIBUTING.md` at `759da623` (the donor carries no contributor file), the donor `README.md` and `docs/README.md`.
2. Issue #68: the body (the frozen 2026-09-09 rule), the assignments to A188, A199 and A211, the A188 DECISION, the owner decision of 2026-09-23 14:15 (5794731372, superseding the 2026-09-09 rule), and the manager ruling (5798089412) that fixes the reading of link-up. The author REVIEW READY comments were read as claims, not as evidence.
3. Parent decision kebag-logic/milan-fpga#387 5606198212 (parts a and b) and its 2026-09-23 mirror of the owner decision (5794731090). Parent `REQUIREMENTS.md` REQ-PTP-01, 05, 08 and 09.
4. Interface authorities: donor `docs/INTEGRATION.md`, `hdl/top/KL_gptp_engine.sv`, `hdl/ucpu/KL_gptp_ucpu.sv`; parent `hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv` (`PHC_ADJ_MAX_C`) and `docs/design/GPTP_PLANE.md`.
5. `git diff c1b61743..ba926810` (10 files) and the three commits. Each commit message is one line with no trailers.
6. Public evidence under kebag-logic/milan-fpga `review-evidence/gptp68-r1` at `9c9922c4` (the author and manager packets of rounds 1 and 2), the PR #74 body and title, and the manager's evidence comments on #68 and PR #74.
7. After my own pass over the diff and my own probes, the four prior public reviews on this PR (R258-1, R259-1, R258-2, R259-2), to resolve or retain their findings below.

## Verdict

The head implements the manager's ruling exactly. The link-up threshold (20 us) is re-armed by the asCapable rise alone, which every reset forces. A Sync receipt timeout, a grandmaster change and a return from mastership each leave the servo locked (100 us).

- **Code.** `S_LOCK` has exactly two writers: the asCapable rise in PDPAIR (`hdl/ucode/gen_gptp_ucode.py:1813-1819`, zero) and the tail of every consumed pair in SERVO (`:850-852`, locked). SRTO (`:1842-1849`) and BECOME (`:1607-1634`) no longer write it. Both legs are word-for-word the base's again, at every clock checked (`receipts/rom-check.log`).
- **Tests.** The six tests the ruling requires pass on all three images: 12b same grandmaster after a timeout (+50 us slews, +150 us steps once), 18d failover after a timeout (-50 us slews, +150 us steps once), 21 return from mastership (+50 us slews), and 13 and 21 asCapable fall and rise (+-25 us steps once). Each fails under a targeted mutant, and the retired `cbccf22` generator fails exactly the three slews.
- **Earlier findings.** The whole-trim clamp that resolved R258-1 F1 and R259-1 F1 is unchanged. SERVO is word-for-word `cbccf22`'s, phase 15b and phase 34 still pass, and the trim mutants are still caught.

## Findings

### S1 SUGGESTION: no check guards the lock across a lost Follow_Up (the 125 ms Follow_Up receipt timeout)

```text
[R259] SUGGESTION Tests, Docs - hdl/ucode/gen_gptp_ucode.py:1852-1857 (FUTO) with docs/TEST_DEVELOPER.md:100 and docs/INTEGRATION.md:214 - "nothing else re-arms the 20 us threshold" is unguarded for the Follow_Up receipt timeout
```

- **Evidence.** Reviewer mutant RV5 adds `S_LOCK = 0` to the FUTO leg, so a lost Follow_Up would re-arm the link-up. It **survives** the whole engine suite: 1259/1259 on the shipping image (`receipts/mutation-suite-head.log`). No phase consumes a pair of 20 to 100 us after a Follow_Up receipt timeout: phases 11, 11c, 16 and 17 fire FUTO, but each is followed by a millisecond re-base or a small slew.
- **The head is correct.** FUTO is two words, unchanged from base, and writes only `S_SYNCTS`. Reviewer probe P4 (a Sync with no Follow_Up, 150 ms, then a locked +50 us pair) slews at head and catches RV5 (`receipts/probe-phases-head.log`).
- **Docs.** `TEST_DEVELOPER.md:100` says the suite "Keeps the lock across timeouts". The suite exercises only the Sync receipt timeout.
- **Impact.** Regression protection only. A lost Follow_Up is far more common than a grandmaster change. A later change that unlocked there would add a counted media re-base (#387 part b) for every 20 to 100 us pair after it, and nothing would fail.
- **Suggested outcome (optional).** Add a check shaped like P4, and optionally P1 to P3 (asCapable falls through lost responses or the cease rule, and rise, mastership, return with no pair consumed). At present, the RV2 and RV3 shapes are caught only by phase 28b. Alternatively, word the bullet as "across Sync receipt timeouts". This does not affect coverage.
- **Verification.** RV5 caught by the engine arm, or the bullet reworded.

No BLOCKER, MAJOR or MINOR finding is open at this head.

## Focus: correction round 2 (A211) against the ruling

| Item | Result at this head | Evidence |
|---|---|---|
| Link-up re-armed only by an asCapable rise or reset | HOLDS | Static: the two `S_LOCK` writers above. `pub_flags_r` resets on every reset (`KL_gptp_engine.sv:775`), so every reset forces a rise. The asCapable rise is the single setter of flags bit 2 (the BTCA `:1571` and BECOME `:1621` masks only keep it). Dynamic: suite phases 13, 21, 28b, and reviewer probes P1 (lost-response fall), P2 (cease and resume) and P3 (rise, then mastership, then return, with no pair consumed: still a link-up, as `INTEGRATION.md:210` defines). Each probe fails under "asCapable's rise keeps the lock" and under RV2 |
| Receipt timeout, same grandmaster: locked | HOLDS | 12b: +50 us, no step pulse; after a second timeout, +150 us, one step pulse of -150000 ns. P5: exactly +100 us after a gap slews, -(100 us + 1 ns) steps |
| Failover through a Sync lapse: locked | HOLDS | 18d: -50 us slews; +150 us steps once. P5: a gap plus a new grandmaster, -100 us slews |
| Return from mastership with asCapable held: locked | HOLDS | 21: +50 us slews; "becoming grandmaster unlocks the servo" caught (7 checks) |
| Owner thresholds: 20 us link-up, 100 us locked, exactly the threshold slews | HOLDS | 13 and 13b boundaries (+-20 us, +-(20 us + 1 ns), +-100 us, +-(100 us + 1 ns)). `receipts/servo-arith-model.log`: the SERVO divide decides step exactly when abs(offset) > T, for T of 20 us and 100 us, over 824,024 offsets including the full 64-bit range and both wrap edges |
| Whole trim within the parent 200 ppm envelope | HOLDS (unchanged since `cbccf22`) | `e_sat` equals a clamp, and the retired integrator clamp, at 2, 25, 50, 100 and 125 MHz. `ppm_addend` is the parent `PHC_ADJ_MAX_C` expression (`KL_gptp_txret.sv:303-305`). Phase 15b rides both rails with asCapable held and more than 4 exchanges; phase 34 grades every addend of the run |
| One `phc_step_we_o` pulse per step, before its addend | HOLDS | `expect_policy_pair` (`sim_main.cpp:859-900`) checks counts, order, value and held data; `KL_gptp_engine.sv:796-797`, `:896-904` |
| Six new tests and their mutants | ALL CAUGHT | 13 #68 generator mutants of the arm, each caught against the stock harness. N1 and N3 fail under "a receipt timeout unlocks the servo". N2 and N4 fail under "the locked threshold is 200 us". N5 fails under "becoming grandmaster unlocks the servo". N6 fails under "asCapable's rise keeps the lock". 6 of 7 reviewer mutants (RV1 to RV4, RV6, RV7) caught; RV5 survives (S1). The `cbccf22` generator fails N1, N3 and N5, 29 checks; the base generator fails 84 |
| Four changed ROMs | EQUAL to their regeneration | Engine `938b0a11...`, tsngen `5c916f49...`, ucpu and syn/ooc `4afe436d...`. The seeded and per-clock digests match the PR body. Against base only SERVO and PDPAIR change content, and only PDREQ, SYNCTX and RESUME move. Against `cbccf22` only SRTO and BECOME change content. 994 of 1024 words are real; 198 words changed against base and 72 against `cbccf22` (`receipts/rom-check.log`, `receipts/rom-word-diff.log`) |
| Other ROM consumers | PASS | ucpu 768/768, tsngen 288/288 (`receipts/rom-consumer-suites-head.log`) |

## Prior public review findings, resolved or retained at this head

| Finding | Status at `ba926810` | Evidence |
|---|---|---|
| R258-1 F1 BLOCKER (Conformance, RTL, Robustness, Tests, Docs): the slew held about 320 ppm beyond the consumer envelope and wedged the plane | RESOLVED, not regressed | SERVO is word-for-word `cbccf22`'s. The whole trim and the integrator are clamped to the parent-derived envelope at five clocks. `INTEGRATION.md:234-270` states the bound and the held trim. Phase 15b drives a slew longer than allowedLostResponses + 1 Pdelay intervals on the rail, with asCapable held. "The whole trim is not clamped" (32 checks), "one unit wider" (33) and "the integrator is not clamped" (38) are caught |
| R259-1 F1 BLOCKER (same five lenses): the same defect, measured as a parent probe | RESOLVED, not regressed | As above. Under the decided policy a 900 ms first synchronization steps |
| R258-1 F2 MAJOR (Conformance, Tests), retained by R259-1: the parent suites were not green at the pin | RESOLVED on the donor side; the exact-head parent confirmation is a manager duty | The manager's local r3 receipts (`$DATA/tmp/gptp68-manager-r3`, not yet public) show, with the gitlink committed locally at live dev `759da623`: `gptp_shadow` 309/309, RESULT PASS; `check_cpp_idiom`, `check_py_idiom`, `xvlog_gate --check`, `check_rtl_source_lists` and `test_builder.py` exit 0. `gptp_plane` is not in that list. By analysis this round cannot change it: its only servo scenario is a 1 ms first pair after boot, which steps under both thresholds, then small offsets, then mastership with no later pair. It passed 29/29 at `cbccf22` in both round-2 reviews |
| R258-1 S1 SUGGESTION, retained by R259-1: the `e_sat` docstring overstated its domain | RESOLVED | `gen_gptp_ucode.py:711-719` states the exact domain |
| R259-1 SUGGESTION: "becoming grandmaster clears the verdict" was unguarded | RESOLVED | Phase 19 check; "becoming grandmaster keeps sync-ok" caught |
| R259-1 SUGGESTION: document bit 3 and `pub_offset_o` during a slew | RESOLVED | `INTEGRATION.md:272-290`, accurate against `KL_gptp_engine.sv:862` |
| Manager r1 parent failures ("closed loop locked", 19 reconstruction misses) | GONE | 1 ms steps under both thresholds; `gptp_shadow` 309/309 in the manager's r3 receipts |
| R258-2 F1 MAJOR (Conformance, Tests, Docs): receipt-timeout and mastership re-arms turn a failover into a link-up | RESOLVED, along its "only an asCapable rise re-arms" route | Both writes removed. Phases 13 and 21 re-scripted around asCapable rises. 18d pins the failover slew. The two keep-the-lock mutants are replaced by re-adding mutants, both caught. The ruling is linked from `INTEGRATION.md:195` and the PR body |
| R258-2 F2 MINOR (Docs): the PR title stated the retired rule | RESOLVED | Title read at review time: "Step at link-up above 20 us and once locked above 100 us, clamping the whole trim to the 200 ppm envelope" |
| R258-2 S1 SUGGESTION: the 0.5 s figure is a floor; overshoot; masters outside the envelope | TAKEN | `INTEGRATION.md:260-270` |
| R259-2 F1 MAJOR (Conformance, Tests, Docs): the same finding | RESOLVED, route (b) | As R258-2 F1. The generator docstrings (`:15-28`, `:335-345`, `:1788-1794`, `:1842-1844`), `INTEGRATION.md:189-232` and `mutants.py:180-235` agree. After a Sync gap a pair slews up to 100 us with and without a grandmaster change: 12b, 18d and P5 |
| R259-2 S1 SUGGESTION: the `e_sat` docstring misstated its callers | TAKEN | `gen_gptp_ucode.py:716-719`; text only, no word changes |

No prior finding is retained open.

## Clean results per lens

```text
[R259] PASS Conformance - hdl/ucode/gen_gptp_ucode.py:335-345, :802-856, :1607-1634, :1788-1824, :1842-1857 - implements the owner decision 5794731372 as fixed by the ruling 5798089412: 20 us at link-up, re-armed only by an asCapable rise or reset; 100 us once locked across a grandmaster change, a Sync receipt timeout and a return from mastership; one step pulse per step; whole trim within the REQ-PTP-01 Q8.24 +-200 ppm envelope that KL_gptp_txret.sv derives; confirmed by suite phases 12b, 13, 13b, 18c, 18d, 21, 28b and reviewer probes P1 to P5
[R259] PASS RTL - gen_gptp_ucode.py:710-729, :802-856, :1813-1819 with KL_gptp_ucpu.sv:186-230, :614-640 and KL_gptp_engine.sv:185, :243, :775-784, :796-797, :860, :896-904 - 64-bit threshold divide and e_sat exact for every reachable operand (32-bit divisors, 32x32 MULS operand bounded by 100 us), scratch slot 43 free of RTL mirrors, S_LOCK written before read after every reset, ROM regenerations equal the four tracked images, 994 of 1024 words, no RTL file changed
[R259] PASS Robustness - probes P1 to P5 and suite phases 12b, 18d, 21, 28b, 15b - lock and re-arm across warm reset, lost-response fall, cease and resume, mastership before any pair, lost Follow_Up, repeated timeouts and failovers, exact +-T and +-(T + 1 ns) boundaries, full 64-bit offset range, five clocks
[R259] PASS Tests - tb/verilator/engine/sim_main.cpp (phases 10 to 34 as diffed) and tb/verilator/engine/mutants.py:180-235 - 1259/1259 on all three images; the six ruling tests each fail under a targeted mutant; 13 #68 mutants plus 6 of 7 reviewer mutants caught; the retired cbccf22 and base generators fail; the mirror decides link-up from the script, never from the DUT; S1 (SUGGESTION) records the one uncovered shape
[R259] PASS Docs - docs/INTEGRATION.md:150-290, :339-340, docs/TEST_DEVELOPER.md:96-104, docs/SOURCE_EVIDENCE.md:29-30, generator docstrings, PR #74 body and title - every stated pulse, reset, threshold, envelope and publication claim checked against the RTL and the ROM; the PR body's digests, placements and word counts reproduce; make contract and make docs pass; no dash characters or non-ASCII in added lines
```

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Owner decision 5794731372, manager ruling 5798089412, #68 body and assignments, #387 5606198212 (a, b) and 5794731090, REQ-PTP-01/05/08/09; `gen_gptp_ucode.py:335-345`, `:802-856`, `:1571`, `:1607-1634`, `:1788-1824`, `:1842-1857`; engine phases 12b, 13, 13b, 18c, 18d, 21, 28b; probes P1 to P5 | R259-3 | `ba9268100ebe92dfc61aed30e2910245fc8c97cf` |
| RTL | CLEAN | `gen_gptp_ucode.py:428-448`, `:710-729`, `:802-856`, `:1788-1824`; `KL_gptp_ucpu.sv:186-230`, `:614-640`; `KL_gptp_engine.sv:185`, `:243`, `:775-784`, `:796-797`, `:860`, `:896-904`; parent `KL_gptp_txret.sv:300-305`; `receipts/servo-arith-model.log`, `rom-check.log`, `rom-word-diff.log` | R259-3 | `ba9268100ebe92dfc61aed30e2910245fc8c97cf` |
| Robustness | CLEAN (S1 is a SUGGESTION) | Warm reset (28b), lost-response fall (P1), cease and resume (P2), mastership before any pair (P3), lost Follow_Up (P4), gap boundaries (P5), repeated timeouts and failovers (12b, 18d), 64-bit model, five clocks | R259-3 | `ba9268100ebe92dfc61aed30e2910245fc8c97cf` |
| Tests | CLEAN (S1 is a SUGGESTION) | `sim_main.cpp` diff, `mutants.py:180-235`; engine run x3; 13 #68 mutants, 7 reviewer mutants, 2 older generators; probe build with 5 phases and 6 mutants; ucpu and tsngen runs | R259-3 | `ba9268100ebe92dfc61aed30e2910245fc8c97cf` |
| Docs | CLEAN (S1 is a SUGGESTION) | `docs/INTEGRATION.md:150-290`, `:339-340`; `docs/TEST_DEVELOPER.md:96-104`; `docs/SOURCE_EVIDENCE.md:29-30`; generator docstrings `:15-28`, `:165`, `:335-345`, `:710-719`, `:1788-1794`, `:1842-1844`; `mutants.py` comments; PR body and title; `receipts/docs-gates-head.log` | R259-3 | `ba9268100ebe92dfc61aed30e2910245fc8c97cf` |

## Real limits

- **Parent suites not run here** (the round's rules): no `gptp_shadow`, `gptp_plane`, `milan_dp` or builder run. The r3 parent receipts cited above are the manager's local files. They are not in the public evidence tree, whose newest round at `9c9922c4` (branch tip `47619cf0`) predates this head.
- **Hosted CI.** The donor repository has no workflows. There is no exact-head hosted context, executed or skipped, to inspect. Hosted and act acceptance are manager-owned.
- **Mutation scope.** I ran the arm's 13 #68 generator mutants, 7 reviewer mutants and 2 older generators, on the shipping image only, as the arm itself does. I did not re-run the arm's pre-#68 RTL mutants. The manager's local r3 donor log shows the whole arm at 27 of 27 plus the control.
- **Probes P1 to P5** are phases appended to a disposable copy of the harness. They are not part of the head, and the prior reviewers' own probe scripts were not replayed; 12b, 18d and P5 cover the same shapes.
- **Clocks.** The suites run at the 2 MHz test clock. The product clock is covered by arithmetic (`servo-arith-model.log`) and ROM regeneration at 25, 50, 100 and 125 MHz, not by simulation.
- **Not run:** synthesis (the `syn/ooc` image was regenerated only), hardware, and physical calibration. Field skips are not hardware proof.
- **Other exclusions.** No private author material and no other reviewer's report for this round were read. R258-3 runs independently.

## Pending manager duties

- Publish this packet (`MANIFEST.sha256` lists every receipt) and route the verdict. A second independent positive review is still required for merge.
- Publish the r3 donor and parent-consumer receipts. Add `gptp_plane`, and the `milan_dp` gPTP-ON leg that no round has run, with the gitlink at this head. A staged gitlink is refused by the parent's #523 guard; the r3 run used a local commit.
- Mirror the manager ruling 5798089412 to kebag-logic/milan-fpga#387. Only the owner decision is mirrored there, so the parent adoption lane plans from the full link-up definition.
- For #387: re-record the per-configuration ROM digests at the pin bump. The parent phase-4 cases do not distinguish 20 us from 100 us.
- At the merge turn: build and gate the current-dev candidate (source base `c1b61743`, live dev `759da623` or later), and own hosted and act acceptance.
- Optional: decide on S1.
- Physical calibration remains NOT RUN.

## Receipts and reproduction

`DATA=<dir holding reviews/ and tmp/> sh scripts/reproduce.sh` regenerates every receipt below, in the foreground. It writes only `receipts/` and `scratch/`, and reads the clone without writing it. Scripts: `env.sh`, `receipt.sh`, `identity.sh`, `rom_check.py`, `rom_word_diff.sh`, `servo_arith_model.py`, `docs_gates.sh`, `engine_suite.sh`, `rom_consumer_suites.sh`, `mutation_probe.py`, `probe_build.sh`, `probe_phases.cpp.inc`.

| Receipt | Exit | Content |
|---|---|---|
| `identity-start`, `identity-end` | 0, 0 | HEAD and tree match; clean status; index and tree digests unchanged; every tracked blob and mode matches; 0 gitlinks (this repository has no submodules); pinned simulator hashes |
| `rom-check` | 0 | four tracked images EQUAL; seeded and per-clock digests; per-program content against base and `cbccf22` at five clocks |
| `rom-word-diff` | 0 | 198 words changed against base, 72 against `cbccf22` |
| `servo-arith-model` | 0 | threshold divide, `e_sat`, divisor widths, MULS operand, at five clocks |
| `docs-gates-head` | 0 | `make contract`, `make docs`, dash and non-ASCII scan |
| `engine-suite-head` | 0 | 1259/1259 x3 |
| `rom-consumer-suites-head` | 0 | ucpu 768/768, tsngen 288/288 |
| `mutation-suite-head` | 1 | control pass; 13 #68 mutants caught; RV1 to RV4, RV6 and RV7 caught; RV5 survives (S1); `cbccf22` and base generators fail |
| `probe-build`, `probe-phases-head` | 0, 0 | P1 to P5 pass at head (1432/1432); every probe mutant caught |

R259-3 FINISHED
