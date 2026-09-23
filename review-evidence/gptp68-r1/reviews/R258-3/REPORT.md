[R258] POSITIVE - exact head ba9268100ebe92dfc61aed30e2910245fc8c97cf

# R258-3: internal independent review of FPGA-gPTP #68 / PR #74, correction round 2

| Item | Value |
|---|---|
| Exact head | `ba9268100ebe92dfc61aed30e2910245fc8c97cf`, tree `5a02fa35db15d9a773895f82bb17020b55cfa775` |
| Base (main) | `c1b617435824929a790739ea8585c3fe1a328cc0`. Commits `77c34e9`, `cbccf22` and `ba92681`: one line each, no trailers, no mode changes |
| Focus | The correction for R258-2 F1 and R259-2 F1 (the same MAJOR), judged against the manager's ruling (issue 68, comment 5798089412) and the owner's decision (5794731372) |
| Verdict | **POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open in any lens. One SUGGESTION (S1, Tests) is recorded; it does not affect coverage |
| Stage-1 record | The verdict and ledger were written to this file before any prior review finding was read. Sections 5 and 6 were added afterwards |

## 1. Reconstruction, in the order read

1. Parent `AGENTS.md` and `CONTRIBUTING.md`, read at live dev `759da623` (blob ids in `receipts/inputs.txt`). The donor repository has no files of its own under those names. Then the donor `README.md` and `docs/README.md`.
2. Issue #68: the body (the superseded 2026-09-09 rule), the manager's first assignment, the owner decision of 2026-09-23 14:15 (20 us at link-up, 100 us once locked, the whole trim within ±200 ppm), the ruling (link-up is **only** the first synchronization after asCapable **rises**, or after a reset), and the A199 and A211 assignments.
3. Authorities:
   - parent REQ-PTP-05 and REQ-PTP-09;
   - #387 decision part b (a step is one counted media re-base);
   - the parent's `KL_gptp_txret.sv:303-305` (the `PHC_ADJ_MAX_C` expression) and `:436` (the inclusive envelope compare).
4. `git diff c1b6174..ba92681`, 10 files, and `cbccf22..ba92681` for this round.
5. Evidence:
   - The pinned public tree `9c9922c` holds manager results for `77c34e9` only, because it predates this head (`receipts/manager_evidence_summary.txt`).
   - The PR's manager comments; the latest validation is at `cbccf22`.
   - The manager's local r3 receipts, summary fields only.
   - Hosted contexts at this head: none exist (`receipts/hosted_checks_head.txt`).
6. Prior public review findings (R258-1, R259-1, R258-2, R259-2) were read only after stage 1 above.

## 2. The ruling against the head (Conformance)

| Rule (owner decision + ruling) | Implementation at this head | Executed evidence |
|---|---|---|
| Link-up is the first pair after asCapable rises; every reset re-arms it | `S_LOCK = 0` has one writer, the PDPAIR rise (`hdl/ucode/gen_gptp_ucode.py:1813-1819`). It is reached only when the flag was clear. Reset clears the flags (`hdl/top/KL_gptp_engine.sv:775`), and SERVO runs only while asCapable stands (`gen:764-765`) | Phase 13: 8 probes, each after an asCapable fall and rise. Phase 21: -25 us steps. Phase 28b: warm reset, +25 us steps. Reviewer probes: PX1 (fall by lost responses), PX2 (fall and rise while grandmaster) and PX3 (rise, then mastership before any pair) each step at +25 us |
| A Sync receipt timeout with asCapable held stays locked | SRTO (`gen:1842-1849`) writes only the flags, and is word-for-word the base's SRTO | Phase 12b: +50 us slews, +150 us steps once. PX6: a Sync gap under the same grandmaster, +90 us, slews |
| A grandmaster identity change stays locked | The BTCA adoption (`gen:1565-1582`) clears the verdict and never writes `S_LOCK` | Phase 18c: 50 us slews, 5 ms steps |
| A failover through a Sync lapse stays locked | As the two rows above | Phase 18d: -50 us slews, +150 us steps once. PX5: timeout, then a new grandmaster, exactly -100 us, slews |
| A return from mastership with asCapable held stays locked | BECOME (`gen:1607-1634`) never writes `S_LOCK`, and is word-for-word the base's BECOME | Phase 21: +50 us slews. PX4: exactly +100 us slews, and -100 us - 1 ns steps |
| Step only when \|offset\| exceeds T; T = 20 us at link-up, 100 us locked | T = 20000 + `S_LOCK`. Every consumed pair writes 80000 (`gen:851-852`). The step test is a nonzero (offset + T) u/ (2T + 1) (`gen:814-821`) | Phases 13 (±20 us, ±(20 us + 1 ns)) and 13b (±100 us, ±(100 us + 1 ns)). Reviewer mutants R3 to R6 (each threshold 1 ns wider or narrower) are all caught |
| Each step is one counted pulse carrying -offset, then one addend | Step arm `gen:822-827`, then the shared clamp and the addend (`gen:840-845`) | `expect_policy_pair` (`tb/verilator/engine/sim_main.cpp:859-900`) checks pulse counts, order, value and held data on every #68 pair |
| The whole trim (P + I) stays within the parent's ±200 ppm envelope | `e_sat` clamps the integrator (`gen:835`) and the whole trim (`gen:843`) at `ppm_addend(200, clk)` (`gen:428-436`), which is exactly the parent's `PHC_ADJ_MAX_C` expression | Phases 15b and 34. The suite's clamp mutants are caught. SERVO is word-for-word the one at `cbccf22` |

## 3. Findings

No BLOCKER, MAJOR or MINOR finding.

```text
[R258] SUGGESTION Tests - tb/verilator/engine/sim_main.cpp:3000-3013 (bounce_ascapable), :3053-3088 (phase 13), :3505-3535 (phase 21) - S1: every asCapable bounce before a link-up pair falls through the delay-threshold verdict
```

- **Authority.** The ruling says an asCapable fall and rise re-arms the link-up, whatever the cause of the fall. Parent `AGENTS.md` section 6 (Tests) asks that each test can fail for the defect it claims to detect.
- **Evidence.**
  - The suite's bounces all use the far-delay verdict (`gen:1823`). None passes through allowedLostResponses (`gen:1442-1451`) or the cease rule (`gen:1397-1404`).
  - Reviewer mutant R2 moves the re-arm from the rise to the threshold-verdict fall. The suite catches it only through phase 28b (2 checks, `receipts/mutant_failures.txt`); phases 13 and 21 pass under it.
  - Probe PX1 (a lost-response fall, then the rise) catches R2 directly (`receipts/probe_phases.txt`). The head passes PX1.
- **Impact.** None at this head. The single rise writer covers every fall path by construction, and R2 is caught. A later refactor that ties the re-arm to one fall path would be caught only by the warm-reset phase.
- **Suggested outcome (optional).** One link-up pair after a lost-response bounce.
- **Verification.** R2 is caught by a bounce phase as well as by 28b.

## 4. Clean results per lens

```text
[R258] PASS Conformance - hdl/ucode/gen_gptp_ucode.py:335-345, :802-856, :1565-1582, :1607-1634, :1788-1824, :1842-1849 with the owner decision (issue 68, comment 5794731372), the ruling (5798089412) and the parent's KL_gptp_txret.sv:303-305, :436 - the link-up re-arms only on an asCapable rise or a reset; a receipt timeout, a grandmaster change, a failover through a Sync lapse and a return from mastership stay locked; the 20 us and 100 us thresholds use "exceeds"; one step pulse of -offset precedes its addend; the whole trim is clamped to exactly PHC_ADJ_MAX_C (section 2)
[R258] PASS RTL - hdl/ucode/gen_gptp_ucode.py:710-729, :802-856, :1788-1824 with hdl/ucpu/KL_gptp_ucpu.sv:193, :226, :616-675 and hdl/top/KL_gptp_engine.sv:767-921; the four tracked ROMs - no .sv file changes. The threshold DIVU is u64/u32 with a register divisor 2T + 1 <= 200001. MULS sees only |offset| <= 100 us. The e_sat immediates are asserted < 2^24 (:448, :720) and it clobbers RU and RW only. The PDPAIR flag RMW and the S_LOCK write sit in one handler with no COMMIT between them. The S_PDGOT hoist is behaviour-neutral. All four ROMs regenerate byte-equal to the committed images. Against base only SERVO (48 -> 51) and PDPAIR (59 -> 61) change content; against cbccf22 only SRTO (6 -> 5) and BECOME (22 -> 21), at 2, 25, 50, 100 and 125 MHz and in both seeded images. 994/1024 words (995 seeded)
[R258] PASS Robustness - gen:1403, :1450, :1823 (the asCapable fall paths) and KL_gptp_engine.sv:775 (reset) against the single rise re-arm gen:1813-1819; gen:764-765 (the servo is gated on asCapable) - no pre-reset or pre-fall lock reaches a link-up pair. Executed probes PX1-PX6 (lost-response bounce; bounce while grandmaster; rise, then mastership, then return; the mastership return at the 100 us edges; a failover at exactly 100 us; a Sync gap under the same grandmaster at +90 us) give 1003/1003 at head. A 64-bit offset + T wrap still gives a nonzero quotient for every |offset| > T
[R258] PASS Tests - tb/verilator/engine/sim_main.cpp:3021 (12b), :3053 (13), :3090 (13b), :3229 (15b), :3402 (18c), :3432 (18d), :3476 (19), :3505 (21), :3904 (28b), :4641 (34); :859 expect_policy_pair; :676 the exact-integer mirror; tb/verilator/engine/mutants.py:181-253 - 1259/1259 on each of the three images. The mutation arm catches 27/27 with the control passing (four slices). Each new test fails under its targeted mutant: N1/N3 under "a receipt timeout unlocks", N5 under "becoming grandmaster unlocks", N2/N4 under "the locked threshold is 200 us", N6 under "asCapable's rise keeps the lock". Reviewer mutants R1-R6 are all caught. The base, 77c34e9 and cbccf22 generators are all rejected, and cbccf22 fails exactly the retired slews (N1, N3, N5). ucpu 768/768, tsngen 288/288, parent gptp_plane 29/29. S1 stays open as a SUGGESTION
[R258] PASS Docs - docs/INTEGRATION.md:161-288 (pulse semantics; the policy links :191-195; the table :199-206; Link-up :208-214; Locked :216-232; Rate envelope :234-270; Publication during a slew :272-288) and :339-340; docs/TEST_DEVELOPER.md:99-101; docs/SOURCE_EVIDENCE.md rows; generator notes :9-22, :334-345, :711-719, :1843-1844; the sim_main.cpp phase list; mutants.py:211-233 - every statement matches the code and the executed runs. make docs, its selftest and the diagram check pass. Added lines carry no em dash, non-ASCII or private path. The PR title states the implemented policy
```

## 5. Prior public review findings, resolved or retained at this head

| Finding | Status at `ba92681` | Evidence |
|---|---|---|
| R258-1 F1 BLOCKER (held slew near 320 ppm, beyond the consumer envelope; the plane wedged) | RESOLVED, not regressed | SERVO is word-for-word the one at `cbccf22` (`receipts/rom_program_diff.txt`). The whole trim and the integrator are clamped to exactly `PHC_ADJ_MAX_C`. Phases 15b and 34 pass, and the three clamp mutants are caught. The manager's r3 `gptp_shadow` passes at this head |
| R259-1 F1 BLOCKER (the same defect) | RESOLVED | As R258-1 F1 |
| R258-1 F2 MAJOR (the parent suites were not green at the pin), retained by R259-1 | RESOLVED at source scope | The parent `gptp_plane` gives 29/29 with this head's donor (`receipts/parent_gptp_plane.txt`). The manager's r3 local receipts pass `gptp_shadow`, the builder, both idiom gates, `xvlog_gate` and the source lists, with the gitlink committed locally. Re-recording the per-configuration ROM digests belongs to the #387 pin bump (pending) |
| R258-1 S1 SUGGESTION (the `e_sat` domain), retained by R259-1 | RESOLVED | `gen:711-719` states the exact domain |
| R259-1 SUGGESTION ("becoming grandmaster clears the verdict" had no guard) | RESOLVED | Phase 19 (`sim_main.cpp:3476`); the mutant "becoming grandmaster keeps sync-ok" is caught |
| R259-1 SUGGESTION (bit 3 and `pub_offset_o` during a slew) | RESOLVED | `INTEGRATION.md:272-288` |
| R258-2 F1 MAJOR (the timeout and mastership re-arms turn a failover into a link-up) | RESOLVED under the ruling | The SRTO and BECOME `S_LOCK` writes are gone, and both programs equal the base's. Phases 12b, 18d and 21 pin the locked slews; 13 and 21 build link-ups from asCapable bounces. The `INTEGRATION.md` Link-up and Locked sections link the ruling. Mutants re-adding each write are caught. PX4, PX5 and PX6 slew at head and step under `cbccf22` |
| R259-2 F1 MAJOR (the same) | RESOLVED by route (b) | As above. All three of its cases slew at head: same grandmaster +50 us (12b) and +90 us (PX6) after a Sync gap, and a failover at -50 us (18d). Docstrings, `INTEGRATION.md` and `mutants.py` agree |
| R258-2 F2 MINOR (the PR title stated the retired rule) | RESOLVED | The title now reads "Step at link-up above 20 us and once locked above 100 us, clamping the whole trim to the 200 ppm envelope" (`receipts/inputs.txt`) |
| R258-2 S1 SUGGESTION (0.5 s is a floor; overshoot; masters outside ±200 ppm) | ADDRESSED qualitatively | `INTEGRATION.md:260-270` |
| R259-2 S1 SUGGESTION (the `e_sat` docstring misstated its callers) | RESOLVED | `gen:716-719` names both callers correctly |

Reading them changed no verdict or ledger entry from stage 1.

## 6. Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Owner decision and ruling against `gen_gptp_ucode.py` SERVO, PDPAIR, SRTO, BECOME and BTCA; the parent's `KL_gptp_txret.sv:303-305,436`; phases 12b, 13, 13b, 18c, 18d, 21, 28b; probes PX1-PX6 | R258-3 | `ba9268100ebe92dfc61aed30e2910245fc8c97cf` |
| RTL | CLEAN | The µcode programs above and `e_sat`; `KL_gptp_ucpu.sv` DIVU and MULS widths; `KL_gptp_engine.sv` reset and PHC face; four ROMs regenerated byte-equal; program-level content diff at 7 configurations | R258-3 | `ba9268100ebe92dfc61aed30e2910245fc8c97cf` |
| Robustness | CLEAN | Every asCapable fall path against the single rise re-arm; warm reset; a fall and rise while grandmaster; a rise, then mastership, with no pair; threshold edges after mastership, failover and a Sync gap; 64-bit wrap | R258-3 | `ba9268100ebe92dfc61aed30e2910245fc8c97cf` |
| Tests | CLEAN (S1 SUGGESTION open) | Engine suite on 3 images; mutation arm 27/27; per-check attribution; reviewer mutants R1-R6; old generators; ucpu, tsngen and parent `gptp_plane` | R258-3 | `ba9268100ebe92dfc61aed30e2910245fc8c97cf` |
| Docs | CLEAN | `INTEGRATION.md`, `TEST_DEVELOPER.md`, `SOURCE_EVIDENCE.md`; generator docstrings; harness and mutant comments; commit messages; PR title and body claims (digests, placement, word counts, tallies) | R258-3 | `ba9268100ebe92dfc61aed30e2910245fc8c97cf` |

## 7. Evidence (all in `MANIFEST.sha256`)

| Receipt | Result |
|---|---|
| `receipts/identity.txt` | Verilator 5.050: wrapper sha256 `905795b9...e92f`, binary `44898b22...bfdd`. The system default 5.052 was not used |
| `receipts/rom_check.txt` | Four tracked images byte-equal to the generator at head, base and `cbccf22`. All 10 per-configuration digests equal the PR table |
| `receipts/rom_program_diff.txt` | Program-level content diff, base -> head and `cbccf22` -> head, at 7 configurations |
| `receipts/engine_suite_head.txt`, `raw/engine/` | 1259/1259 on the shipping, request-seeded and Sync-seeded images |
| `receipts/mutants_own_slice0..3.txt` | The suite's own arm: 27 caught, control PASS in each slice |
| `receipts/mutant_failures.txt`, `raw/mutant_attribution/` | Per-check failures of the 13 #68 mutants, reviewer R1-R6, and the base, `77c34e9` and `cbccf22` generators. Control 1259/1259 |
| `receipts/probe_phases.txt`, `raw/probe/` | Probes PX1-PX6 in a disposable harness copy (`raw/probe/sim_probe.cpp`). Head 1003/1003; each control fails its targeted probe |
| `receipts/ucpu_tsngen.txt` | ucpu 768/768; tsngen 288/288 |
| `receipts/contract_docs_lint.txt` | contract, docs, docs selftest, diagram check and engine lint: all PASS |
| `receipts/parent_gptp_plane.txt`, `raw/parent_gptp_plane/` | Parent `gptp_plane` at live dev files: 29/29 with the head, base and `cbccf22` donors |
| `receipts/manager_evidence_summary.txt`, `receipts/hosted_checks_head.txt` | What the pinned public evidence and the local r3 receipts cover; 0 hosted contexts |
| `receipts/clone_integrity.txt` | The clone after all probes: HEAD and tree exact; clean index and worktree; no hidden entries; 103 files byte- and mode-equal to their blobs; 0 gitlinks |
| `scripts/` | `reproduce.sh` and the scripts it calls (portable; paths come from the environment) |

## 8. Real limits

- **Hardware.** Physical calibration was NOT RUN. No hardware, synthesis or timing claim is made. The product clocks (25 to 125 MHz) are analysed through generated images and operand widths, not simulated; every executed run is at 2 MHz.
- **Donor gates.** I did not run the full donor `make` (gaskets, parser, bench tag test and bench lint were not run by me). The manager's local r3 receipt records `make -j8` exit 0 at this head.
- **Parent gates.** Of the parent, I ran only `gptp_plane`, from six files fetched at live dev and checked against their blob ids. `gptp_shadow`, the builder, `xvlog` and the idiom gates are the manager's (local r3, exit 0).
- **Probes.** PX1-PX6 insert phases after phase 21 in a disposable copy of the head harness and truncate the run after them. They grade through the suite's own helper and mirror.
- **Mutation scope.** The suite's arm runs on the shipping image only, as `mutants.py` does.
- **Hosted CI.** The donor repository has no workflows, so no executed or skipped hosted context exists at this head.

## 9. Pending manager duties

1. Publish the r3 receipts for this head. The pinned tree `9c9922c` covers `77c34e9` only. The local r3 receipts record donor `make -j8` exit 0, and the six parent consumer gates exit 0 at parent `7aa069b9` (live dev `759da623` plus one local commit setting the gitlink). The staged-gitlink form was refused by the parent's #523 guard, and the receipt should say so.
2. Validate the final current-dev candidate at the merge turn: source base `c1b6174` and live dev `759da623`, or whatever dev is then.
3. The #387 pin bump re-records every per-configuration ROM digest, because every image changes.
4. Obtain the external positive review (R259-3) and maintainer merge authorization. No round may be in flight at merge.
5. Keep physical and field acceptance explicit: NOT RUN.

R258-3 FINISHED
