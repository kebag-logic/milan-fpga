[R428] NEGATIVE - exact head a463a1deb9d63614e8bd2134ccd7b2cd541c72ed

# R428-3: internal cleared-context re-review of PR #631 (#629, lane M1, design only)

- **Head:** `a463a1deb9d63614e8bd2134ccd7b2cd541c72ed`, tree `dfcbb0d53770fdf4161117b08134cb88b7ad4526`. Base and live dev: `d4dd742679b902b2bc5eedf89d525066d59aafbb`.
- **Change:** one docs commit on `c554ae51`, touching only `docs/design/MEDIA_CLOCK_FOLLOWING.md` (+322 / -101). Against the base, the PR is that page (1,105 lines) plus one index row in `docs/README.md`. No RTL, builder, generator, configuration or processor file changes (`git diff --stat`; `hdl/` is byte-identical to the base).
- **Scope read, in order:** AGENTS.md and CONTRIBUTING.md; docs/README.md; the #629 body; rulings 5935520588; the round-3 assignment 5936791368; DECISION 5937429002; rulings 5937449258; the cited RTL; the full diff and its history; the round-3 author packet at commit `d3234c72` (`review-evidence/629-r1/author-r3/`); the manager's evidence comments; the hosted checks at the head.
- **Prior findings:** R428-2 and R429-2 were read only after this round's own pass was written.

## Verdict in one paragraph

The round-3 design change is sound, and I reproduced each of its technical claims independently:
- No rate estimator over 512 ms can pass the servo's 2 ppm lock test for every error shape of IEEE 1722-2016 10.8 size.
- The servo PI's worst-case gain is 2.125.
- E8's closed-loop bound is 753 ns at +/-1,426 ns, and 700 or 890 ns at a plant gain of 0.8 or 1.2.
- Every error shape I tried holds LOCKED with zero drops under E8.
- A one-sample or half-sample step is still rejected at all 16 group positions.
- The void-rule tolerances are exact.
- The area claim holds up in a focused synthesis probe.
- The switch test's grading is confirmed on the unmodified restart engine in the pinned HDL simulator.
- The 4.1 s rate-valid latency violates no Milan v1.2, IEEE 1722.1-2021 or IEEE 1722-2016 requirement.
- D5 = C1 is consistent with E8.

All my round-2 findings, and R429-2's, are resolved at this head.

One MINOR finding is open, in Docs only. The head was cut before rulings 5937449258 were posted. So the page and the PR body still record D1, D5 and D8 as open for decision and D2's wording as awaiting confirmation. They also call the CRF receiver's weakness "proposed as a separate issue" although it is filed as #633. That leaves the Docs lens unclean, so the verdict is NEGATIVE. The other four lenses are covered clean at this head.

## Judgments on the assigned items

### 1. The error-shape argument (round-2 F2 replaced by a design fix)

The page's argument (`MEDIA_CLOCK_FOLLOWING.md:554-566`) is correct, and it holds more generally than the page states it.

- **Any estimator, not only a linear one.** Error-free data with slope s is consistent with every rate in [s - 2J/T, s + 2J/T], each paired with a phase ramp inside +/-J. No estimator can tell these cases apart, so every estimator's worst case is at least 2J / T. For an unbiased linear estimator the page's weight argument gives the same bound: the weights sum to zero and weigh the sample times to one, so the sum of |w| is at least 2 / T about the mid-span.
- **The figures.** At J = 1,042 ns and T = 512 ms the bound is 4.070 ppm, 2,084 ns per window, against the 1,024 ns threshold. A least-squares slope reaches 3J / T, from the integral of |x| over the integral of x^2 on a uniform span. These are in `loop_gain_check.out`.
- **Why round 2's "group" shape passed.** It is the estimator's best case: 256 is even, so it cancels.

### 2. The PI amplification and plant-gain sensitivity

I derived the loop from `KL_mmcm_drp_servo.sv` as written:
- `e = locerr - rate` (`:643`);
- `integ += e >>> 1`, `u = integ + e >>> 2` (`:228-229`, `:647-669`);
- the trim reaches `locerr` one window later. The PI writeback lands a few cycles after the boundary, and the phase-shift accumulator applies `u` over the next window (`:609-615`, dispatch block).

| Quantity (`loop_gain_check.out`) | Value | The page |
|---|---|---|
| Sensitivity worst-case gain, g = 1 | 2.1250 | 2.125 |
| Two-point over N windows, closed loop, g = 1: N = 1, 4, 6, 8 | 4.0137, 1.0155, 0.6967, 0.5278 | 4.01, 1.02, 0.70, 0.53 |
| E8 at J = 1,042 and 1,426 ns | 550 and 753 ns | 550 and 753 ns |
| E8 at J = 1,426 ns, g = 0.8 and 1.2 | 700 and 890 ns | 700 and 890 ns |
| E8 at J = 1,748 ns (the void tolerance), g = 1 and 1.2 | 923 and 1,091 ns | not stated; outside the design point |

The loop's poles are at |z| = 0.45, 0.50 and 0.55 for g = 0.8, 1.0 and 1.2, and the sensitivity is 2.0 at g = 0.5 and 4.0 at g = 1.5. So E8's margin depends on the plant gain staying near 1, as the page says (`:623`, `:1077-1083`). The servo row with the meter in front of it (`:999`) is what proves it.

### 3. E8 re-run against random-sign, periodic, ramp and alternating shapes

My own model, `e8_meter_probe.py`, is written from the page's rules and not from the author's code. It implements:
- groups by `sequence_num % 16`, with a gap restarting the history;
- the in-group void above 4,096 ns;
- the floor-mean pick;
- the 2 ms +/- 4,096 ns spacing check;
- an 8-entry read-old/write-new snapshot ring every 256 fresh picks, `>>> 3`, valid after 2,048 fresh intervals;
- the servo's integer PI with its clamps and slew, its lock count and its no-PI-on-invalid rule;
- +/-20 ns local quantisation;
- servo windows on their own 512 ms grid at a chosen phase, so a +/-300 ppm talker slides against them.

**Shapes.** 113 cases of 120 s each (`e8_meter_probe.out`, section "shapes"):
- random sign per group and per 512 ms block;
- alternating per group and per PDU;
- independent;
- sine at 10 ms, 1 s, 2 s, 4.096 s and 8.192 s;
- triangle ramps at 1 s, 4.096 s and 8.192 s;
- sawtooth ramps at 0.512 s, 2.048 s and 4.096 s;
- the worst case for E8, with signs from my own impulse response.

Each ran at +/-1,042 and +/-1,426 ns and at 0 and +/-300 ppm. The worst case was also run at four servo phases and at g = 0.8 and 1.2.

| Result over all 113 cases | Value |
|---|---|
| LOCKED-to-ACQUIRE drops | 0 |
| History restarts | 0 |
| Windows under 1,024 ns after the first LOCKED | 1.000 in every case |
| Worst \|e\|, g = 1 | 782 ns (worst case, phase 0; 753 ns plus quantisation) |
| Worst \|e\|, g = 1.2 | 869 ns |

**Steps.** A one-sample (+/-20,833 ns) and a half-sample (+/-10,417 ns) step were landed 20 s in, after LOCKED, at each of the 16 group positions at 0 and 300 ppm: 128 cases. Every one restarted the history exactly once, with 0 drops. The zero-step control restarted 0 times.

**The author's model.** `meter_rules_model_r3.py` re-runs byte-identical to its published output (`author_evidence_rerun.txt`). Every figure the page quotes from it matches the output, with one labelling exception, S1 below:
- the `:646-658` table;
- E4's 12 drops;
- LS1 never locking under 2 s periodic error;
- the sub-bound steps at most 432 ns, with E1 dropping;
- 7.3 s against 3.7 s to first LOCKED;
- the tolerance rows.

### 4. The area claim

The page claims one RAMB18 fewer and about 10 to 30 LUT more. A focused out-of-context xc7 synthesis of the ring alone, without the meter (`ring_area_probe/`), gives:

| Variant | Mapping |
|---|---|
| 256 x 32 (E1) | 1 RAMB18E1 |
| 8 x 32 (E8), old snapshot read asynchronously in the write cycle | 6 RAM32M, about 24 LUT; 35 FF; no RAMB18 |
| 8 x 32 (E8), old snapshot held in a fabric register | 4 RAM32M; 24 FF more than the BRAM form, whose register sits inside the RAMB18 |

So "one RAMB18 fewer, about 24 LUT of distributed RAM" holds. "Under 10 FF more" holds for the asynchronous-read form, and the register form costs about 24 FF more. Either is inside the page's ranges for the meter (`:911`), and the page says the figures are re-measured once the RTL exists (`:924-926`).

### 5. The 4.1 s rate-valid latency against lock-time requirements

**Plainly: no violation.** I know of no numeric media-clock lock, acquisition or re-lock time requirement in Milan v1.2, IEEE 1722.1-2021 or IEEE 1722-2016. The clauses the issue and page cite are checked:
- Milan v1.2 5.3.11.1, 5.3.11.2, 5.4.2.15/.16, 7.2.2, 7.3, 7.4 and 7.6;
- IEEE 1722.1-2021 7.2.9, 7.2.32 and 7.4.23/.24;
- IEEE 1722-2016 4.4.4.3, 4.4.4.7, 10.4.3, 10.6 and 10.8.

The repository's own requirement register has none either (`docs/reference/FR_NFR.md:235-239`, `:292`).

The time-bearing rules nearest to it are each met:

| Rule | Why it is met |
|---|---|
| `mr` held at least 8 AVTPDUs (4.4.4.3) | Independent of the meter; graded by the switch probe |
| 10.4.3's quick adjustment to a received `mr` | A shall for a CRF listener only. The CRF path keeps `KL_crf_rx`'s 512 ms rule unchanged. For AAF, 4.4.4.3 makes it a "may" |
| The SET_CLOCK_SOURCE response | The processor answers without waiting for lock, and that is unchanged (`protocol-processor/hdl/aecp/ucode/gen_ucode.py:1410-1440`) |
| Milan v1.2 7.4's +/-50 ppm | A frequency-quality bound. During the 4.1 s the audio clock holds its last trim, or the MMCM plan (10.64 ppm off nominal) on a first acquisition |
| NFR-TIME-02, no periodic MEDIA_RESET on a healthy stream | Unaffected: a history restart raises no `mr` |

Internal criteria:
- the bench's B AAF criterion is "LOCKED within 15 s" (`:1042`), and both models lock in 7.3 to 8.7 s after the first PDU;
- the servo row asks for 10 s (`:999`).

Limit: the standards' texts were not available in this environment. This check rests on the cited clause set and the reviewer's reading of those standards, not on a fresh full-text search.

### 6. The desk model's void rule (round-2 F1)

The round-3 model applies the void. My independent tolerance sweep (`e8_meter_probe.out`, section "void and spacing tolerance") hits the page's analytic edges (`:523-534`) exactly:

| Case | Edge |
|---|---|
| Correlated (random sign per group), 300 ppm | valid at 1,748 ns; continuous restarts at 1,749 |
| Correlated, 0 ppm | 2,048 / 2,049 ns |
| Independent, 300 ppm | first restarts between 1,760 and 1,800 ns |
| Independent, 0 ppm | first restarts between 2,049 and 2,060 ns |
| Independent +/-2,500 ns | never valid, about 121 voids per second at 0 ppm, as the page states (`:658`) |

### 7. The switch test, graded where each mutant fails

The author's harness, `mcr_switch_rerun/`, was rebuilt in the pinned HDL simulator 5.050 against the unmodified `KL_media_clock_restart.sv` (blob `c0b5efc2`). All six published case lines re-ran identical to the published receipt (`compare_to_author_receipt.txt`):
- the switch alone gives one toggle per output in 1,600/1,600 trials scaled and 32/32 at 100 MHz;
- the late re-seed mutant gives a second toggle on both outputs in 1,600/1,600 and 32/32;
- the first-PDU mutant reaches the wire in 17 % and 27 % of trials;
- the early second request reaches the wire in 0 of 13,056 trials.

My round-2 probe, `mcr_merge_probe_r2_rerun/`, re-ran identical to its round-2 receipt.

A new reviewer sweep, `mcr_window_probe/`, puts a second request at every delay from 0 to about two CRF periods, at 31 to 1,600 switch phases, over four period, latency and offset sets: 89,347 trials in all. It tests the page's statement (`:802-807`) that a request merges until the output's first PDU at the adopted level is reported. The result is 0 disagreements on both outputs, and 1,702/1,702 switch-alone trials give exactly one toggle per output.

My first edge definition, "launched at or after the switch", disagreed in a few trials. That was my harness's error: a PDU launched in the one or two cycles before adoption carries the old level, and the engine's rule is the adopted level (`KL_media_clock_restart.sv:236-246`). It is not a defect in the page, whose wording is exact to within those cycles.

The page's grading therefore holds:
- each era-start mutant is graded at the meter's ports and at the request tap, deterministically;
- the no-re-seed mutant is graded on the wire by check (ii), deterministically;
- the page states that the era-start rule has no wire-level mutant (`:1010-1031`).

### 8. D5 = C1 with E8

C1's locked level is ~`tu` and (INTERNAL, or servo LOCKED) (`:867`). Under E8:
- a lost PDU restarts the history and holds the servo's state without PI or lock updates (`KL_mmcm_drp_servo.sv:613-615`), so the counters do not move;
- a loss (the meter's 100 ms timeout) and a switch (W2's one-cycle unlocked presentation) both pass HOLDOVER, so UNLOCKED moves once;
- LOCKED returns after the rate validates plus four windows, about 6 to 7 s.

This is what `:878-888` states. Inside the design point the servo does not leave LOCKED (sections 2 and 3). C1 matches the ruling, although the page still lists it as "for decision" (F1).

### 9. Gates at the head

All rc 0 (`gates/*.rc`):
- `check_entity_shape.py` (`checks: 166 failures: 0`);
- `docs_check`, `check_doc_style`, `gen_toc --check` and `--verify-anchors`, `check_em_dash --base d4dd7426`, `check_doc_paths`, `check_gptp_docs`, `DOC_MAP.gen.py --check` and `timesync_chain.gen.py --check`;
- `git diff --check` over the base range and the worktree.

The three gates that need the pinned Markdown renderer (`gen_toc` twice and `check_em_dash`) refused with rc 2 under a bare interpreter, which is their documented refusal, so they were re-run in the pinned renderer environment. Only the re-run receipts are published.

## Findings

```text
[R428] MINOR Docs - docs/design/MEDIA_CLOCK_FOLLOWING.md:20-33, :393-396, :867, :1056-1057, :1060, :1063, :1084-1089; PR #631 body (Status, Decisions table, Round 3 paragraph) - the page and PR body record the round-3 decisions as open, and the CRF weakness as unfiled, against public rulings 5937449258
```

**F1**
- **Requirement/evidence:**
  - Rulings [5937449258](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5937449258) settle the round-3 decisions:
    - D8 = E8 accepted;
    - D5 = C1 accepted, together with E8;
    - D1 = L1 stands;
    - D2's wording is confirmed as "keeps the mean of each 16";
    - the CRF receiver's rate weakness is filed as #633.
  - At this head the page and the PR body still record them as open:
    - the Decisions table reads D1 "Re-opened in round 2, for decision", D5 "... for decision", D8 "New in round 3, for decision", and D2 "the two wording changes are for the manager to confirm" (`:1056-1063`);
    - the same states appear at `:20-33`, `:393-396` and `:867` ("C1, recommended with E8");
    - Limits says the CRF weakness "is proposed as a separate issue" (`:1084-1089`) and does not link #633;
    - the PR body's Status line, its Decisions table and its round-3 paragraph say the same.
  - AGENTS section 7 requires "authoritative documentation is current", and the Docs lens asks that changed contracts be reflected.
  - The head predates the rulings (commit 17:59Z, rulings 18:04Z), so this is not an authoring error. It is the merge candidate's state.
  - R428-1 F6 raised the same class at round 1, and round 2 fixed it.
- **Impact:** a cold reader of dev after merge would take D1, D5 and D8 as unsettled and the CRF weakness as untracked. The page's "Where the decisions stand" paragraph exists to prevent exactly that. The implementation lane takes its contract from this page.
- **Required outcome:** the page's decision states, the D2 and D5 wording, the C1 row label and the Limits item record rulings 5937449258, including the link to #633. The PR body says the same. No technical content needs to change.
- **Verification:** a docs-only re-review of the page and PR body at the next head, with the docs gates and `check_entity_shape.py` at rc 0.

### Suggestions (optional; they do not affect coverage)

- **S1 (Docs), `:671-674`.** "the largest window error is 104 against 351 ns at +/-1,426 ns" quotes the open-loop rate error, `open_max` for independent error at 0 ppm. Elsewhere the page uses "window error" for the servo's closed-loop |e| (`:601-603`, `:665-666`). The closed-loop figures in the same rows are 184 against 465 ns (`author_model_figures_check.txt`). Name the quantity, or quote both. The conclusion, that P2 lowers the noise, stands either way.
- **S2 (Robustness), `:482`, `:609-615`, `:678-681`.** Under E8 a single lost PDU freezes the servo's trim and state for 4.096 s. At 8,000 PDUs/s, losing about one PDU in 32,768 keeps the rate permanently invalid, against one in 4,096 under E1. The page states the 4.096 s hold but not the loss rate at which E8 never validates. Stating it, or noting that a gap need only void the snapshot it spans, would help the implementation lane. A reserved Milan stream should not lose PDUs at that rate, so this is not a defect.
- **S3 (Tests), `:990`.** The first-PDU-pick (P1) mutant "leaves 256 ns" only probabilistically under independent +/-1,426 ns error: about an 8 % chance per window. Pin the stimulus seed and a duration of at least about 60 windows, so the mutant fails deterministically.

## Prior public findings at this head

| Finding | Status at `a463a1de` | Evidence |
|---|---|---|
| R428-2 F1 / R429-2 N2, the desk model omits the void rule; the +/-2,500 ns row | Resolved | The r3 model applies it. The row reads "never valid" (`:658`, `:667-669`), and the tolerance is stated (`:523-534`). My sweep reproduces the edges exactly (section 6) |
| R428-2 F2 / R429-2 N1, the error-shape claim | Resolved by a design fix | D8 = E8 (`:542-674`). The argument, bound and shapes are verified independently (sections 1 to 3) |
| R428-2 F3 / R429-2 N3, the switch mutant that cannot fail | Resolved | Mutants graded at the meter ports, the request tap and pinned stimulus (ii) (`:997`, `:1002`, `:1010-1031`). The probes re-run identical, and the window statement is verified (section 7) |
| R428-2 S1 | Taken | `:449-455` separates the 16-PDU pick from a per-format 96-sample pick |
| R428-2 S2 | Taken | `:471-475`: the floor varies by less than 1 ns per pick |
| R428-2 S3 / R429-2 (10.6 qualifier) | Taken | `:112-113` "due to network packet loss" |
| R428-2 S4 / R429-2 S2 | Taken | `:388-396` and the D2 row name the ruled wording. Confirmed since; see F1 |
| R429-2 S1 | Taken | `:105-111` rests the permission on the absence of a prohibition, and reads 5.3.11.1 as capability |
| R429-2 S3 | Taken | `:802-807` per output: 125 us AAF, 2 ms CRF |
| R429-2 S4 | Taken | `:936` lists `hdl/common/gen/adp_shape_defaults.svh` |
| R428-1 F1 to F5, R429-1 F1 to F5, and their suggestions | Remain resolved | Round 3 touches none of their text except where it is listed above. The round-3 hunks are confined to (b) 10.6, the meter, the estimator, switching, `mr`, D5, area, the test plan, Decisions and Limits |
| R428-1 F6, the page not current with the rulings | Was resolved at `c554ae51`. The same class recurs for the round-3 rulings | F1 |

## Lens coverage at this head (round R428-3)

```text
[R428] PASS Conformance - docs/design/MEDIA_CLOCK_FOLLOWING.md:65-227, :380-674, :784-822, :846-889 at a463a1de; issue #629 body and rulings 5935520588/5937449258 - the estimator argument against IEEE 1722-2016 10.8 Eq. (15); the 4.1 s latency against every cited Milan v1.2 / IEEE 1722.1-2021 / IEEE 1722-2016 time-bearing rule (no violation); `mr` per 4.4.4.3/10.4.3 under E8; C1 against Milan 5.3.11.2; the frozen acceptance items the design maps (each source, follow within tolerance, switch/loss mutants)
[R428] PASS RTL - hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:228-233, :538-579, :596-700; hdl/ieee1722/crf/KL_crf_rx.sv:279-329, :390-403; hdl/ieee1722/avtp/KL_media_clock_restart.sv:205-266 at a463a1de; loop_gain_check.out; ring_area_probe/stat_*.txt; mcr_window_probe/w*.out - every new citation holds; the loop model (e, PI shifts, one-window plant) matches the RTL; the ring's mod-2^32 difference stays exact over 4.096 s (deviation << 2^31, span < 2^32 ns); fresh count 12 bits; the ring maps without a RAMB18; the merge rule is as the page states
[R428] PASS Robustness - e8_meter_probe.out (113 shape cases, 128 step cases, 44 tolerance cases); author_evidence_rerun.txt - zero drops and zero restarts inside +/-1,426 ns at +/-300 ppm and g = 0.8 to 1.2; one restart per one-sample or half-sample step at all 16 positions; void and spacing tolerances exact; the residuals (beyond +/-1,748 ns, plant gain, PDU loss: S2) stated or suggested
[R428] PASS Tests - docs/design/MEDIA_CLOCK_FOLLOWING.md:978-1031 at a463a1de; mcr_switch_rerun/receipt_author_cases.out; mcr_merge_probe_r2_rerun/receipt.out; mcr_window_probe/w1-w4.out - each named mutant has a deterministic failing check (ports, request tap, pinned stimulus (ii), estimator/bound/pick/void rows), the switch harness re-runs identical on the real restart engine, the merge window is verified at 89,347 trials; S3 is optional
[R428] MINOR Docs - see F1 (decision states and #633 at :20-33, :393-396, :867, :1056-1063, :1084-1089 and the PR body); gates/*.rc all 0; docs/README.md:72 index row; the public-text scan of the page is clean; S1 optional
```

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | the page's clause findings, estimator, `mr` and D5 sections; #629 body, rulings 5935520588 and 5937449258; the time-bearing clauses listed in section 5 | R428-3 | `a463a1deb9d63614e8bd2134ccd7b2cd541c72ed` |
| RTL | CLEAN | `KL_mmcm_drp_servo.sv`, `KL_crf_rx.sv`, `KL_media_clock_restart.sv` at the cited ranges; `loop_gain_check.out`; `ring_area_probe/`; `mcr_window_probe/` | R428-3 | `a463a1deb9d63614e8bd2134ccd7b2cd541c72ed` |
| Robustness | CLEAN | `e8_meter_probe.py` / `.out`; the author model re-run (byte-identical); the residual and limit text `:620-623`, `:1077-1089` | R428-3 | `a463a1deb9d63614e8bd2134ccd7b2cd541c72ed` |
| Tests | CLEAN | the test plan `:978-1050`; `mcr_switch_rerun/`, `mcr_merge_probe_r2_rerun/`, `mcr_window_probe/` on the unmodified restart engine | R428-3 | `a463a1deb9d63614e8bd2134ccd7b2cd541c72ed` |
| Docs | UNCLEAN (F1) | the page, `docs/README.md:72`, the PR #631 body, `gates/` | R428-3 | `a463a1deb9d63614e8bd2134ccd7b2cd541c72ed` |

## Executed evidence (this round; every file listed in MANIFEST.sha256)

| What ran | Result |
|---|---|
| `loop_gain_check.py`, standard library | rc 0; section 2's figures |
| `e8_meter_probe.py all`, standard library, at most 8 worker processes, deterministic seeds | rc 0; sections 3 and 6 |
| `meter_rules_model_r3.py all`, the author's published model, re-run | byte-identical to its published output (`author_evidence_rerun.txt`) |
| The author packet's `MANIFEST.sha256` | does not verify as published. 16 entries name `./gates/`, which the archive holds as `./gates-head/`. Two files differ: `mcr_switch_probe/run_probe.sh` and `receipt.out`, whose published copies carry environment placeholders in place of paths. The content I re-ran reproduces |
| `run_probes.sh` steps 1 to 3, the pinned HDL simulator 5.050 (identity in `mcr_window_probe/verilator_version.txt`), on the restart engine at blob `c0b5efc2` | all rc 0 |
| `run_probes.sh` step 4, the xc7 ring synthesis probe | `ring_area_probe/stat_*.txt` |
| `run_gates.sh` with the pinned Markdown renderer environment | all rc 0 (`gates/`) |
| Hosted checks at the exact head (`hosted_checks_at_head.txt`) | 8 contexts executed and succeeded: `rtl-fast`, `docs-check`, `docs-check-no-git`, `elaborate`, `bdd-conformance`, `wire-accountability`, `changes`, `full-ci-gate`. 7 were **skipped, not executed**: `verilator-lint`, `verilator-suites`, the Verilator and Yosys shards, `yosys-elaboration`, `yosys-portability` and the physical gPTP context. The manager owns hosted acceptance |
| Clone restore check (`restore_check.txt`) | HEAD and tree exact; index tree equals `dfcbb0d5`; worktree and index equal HEAD; gitlinks unchanged (`external` efeb541a, `gptp-processor` 5dce647a, `protocol-processor` b2db3a97, `third_party/verilog-axis` 48ff7a7e); submodule worktrees clean |

All probe builds and runs happened under the packet's scratch directory, and no tracked file in the clone was edited. The gate runs created four ignored `__pycache__` directories in the clone, and I removed them afterwards.

## Limits

- **Desk and probe evidence only.** No RTL of the design exists, so no meter or servo-with-meter simulation was possible. The closed-loop figures model the servo's PI, not its RTL. The fine phase-shift actuator, the PHC guards and the gPTP plane's wander are not modelled, as the page says.
- **The ring area figure is an out-of-context mapping of the storage alone**, not the meter.
- **The standards' texts were not available here.** The lock-time check (section 5) rests on the cited clause set and the reviewer's reading.
- **Not run:** physical calibration, hardware or bench. The bench rows are plans. Hosted skips are not executions.
- **Source validation is not the final candidate.** It is distinct from the current-dev candidate merge, which the manager builds at the merge turn.
- **The other round-3 reviewer's report was not read.**

## Pending manager duties

- Rule on F1's route (a docs-only commit recording 5937449258 and #633 in the page and PR body), then the re-review of that head.
- The candidate merge build and validation against live dev, and acceptance of the hosted and local replica gates at the merge head, where the skipped contexts above are the manager's call.
- Optionally re-archive the author round-3 packet with a manifest that matches its published files.
- D4 stays with the owner. Protocol-processor #141 lands before or with the implementation. #632 and #633 are tracked separately.

R428-3 FINISHED
