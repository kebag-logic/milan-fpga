[R456] NEGATIVE - exact head 98729742b71d5088f250440eb46085daf1c0cbdb

# R456-1: internal cleared-context review of #643 / PR #648

- **Head:** `98729742b71d5088f250440eb46085daf1c0cbdb`, tree `174b326e6fcf29ff695a9376ab84ef3c045e4440`. Two commits on dev `5fabb46e767c9308ab2580916237f43577698c6e`.
- **Diff:** `5fabb46e..98729742`. It touches `sim_tdm8_render.cpp`, `tdm8_render_mutants.py`, the suite Makefile, `docs/design/MEDIA_CLOCK_FOLLOWING.md`, `docs/testing/TESTING.md` and `tb/verilator/README.md`. No file under `hdl/` changes.
- **Scope source:**
  - the #643 body;
  - the lane assignment (5972861856);
  - the item-1 STOP (5973437153);
  - the ruling, option (c) (5973450039);
  - REVIEW READY (5974434363);
  - the PR body;
  - public evidence `review-evidence/643-r1` at `531abe2b`.
- **Prior public review findings on PR #648:** none. The PR carries only the two review-start comments, so there is nothing to resolve or retain.
- **Verdict:** NEGATIVE. There is one open MAJOR and one open MINOR.

## Findings

### R456-1-F1 MAJOR: the tie rule's premise fails at the boundary phase after settle

**Severity and lenses:** MAJOR. Lenses: Conformance, Tests, Robustness, Docs.

**Where:**
- `tb/verilator/milan_dp_render/sim_tdm8_render.cpp:664` (the tie window is `after == 1 || after == 2`);
- `:3077-3113` (the tie rule and the fill check);
- `:173-176` (the slack rationale);
- `docs/design/MEDIA_CLOCK_FOLLOWING.md:1366-1370` ("One cycle of feed jitter moves a pop across that boundary");
- `tb/verilator/README.md:63` and `docs/testing/TESTING.md:521` (the tie-rule summary);
- the PR body's "No standing phase is a tie" paragraph.

**Authority and evidence.** The ruling (5973450039) accepted a tie rule "for a pop coinciding with the PDU end within one cycle of feed jitter". The brief requires that the rule cannot mask a real defect. The issue requires that the law hold at every phase once the aligner has settled, or else STOP. I applied the head harness unchanged except for the phase list: a one-cycle scan from +2018 to +2035 (`scripts/probes.sh`, `probes3.sh`). The receipts are in `receipts/summary.txt` and `receipts/probes/`.

1. **A correct design fails after settle.**
   - At +2025 the fill check reads 94/124 at processor `631eeb34` (`hp-tieon-law.log`). It reads the same 94/124 at `c4cb84ff` with both adoption patches (`c4-tieon-law.log`).
   - The aligner held its settled report through the phase: 0 ticks were outside the band.
   - A per-PDU trace (`hp-tietr18-law.log`, tabulated in `summary.txt`) shows the mechanism:
     - the stream snaps with the pop counted, seen +1 cycle after the end, so the fill is 14;
     - inside the graded window the end-to-pop offset then walks to +2, and later to +3 cycles;
     - the 30 failing PDUs read fill 15 with the pop at +3, which is outside the rule's window;
     - their first events land at 18,753 cycles, which is 9T + 3.
   - So after settle the boundary moves by more than "one cycle of feed jitter" within a single phase.
2. **The rule masks a real one-event defect at that phase.**
   - With the setpoint planted one event low (`RENDER_SETPOINT_EVT_C ... - 1`, `hp-tiespm1-law.log`), +2025 passes every `[LAW]` check: the fill check reads 124/124 (13 under the rule, or 14) and the band check passes at d = 8.001..8.002 T.
   - At +2026 the band check also passes, and the fill check catches only 2 PDUs.
   - With the setpoint one event high, the band check passes at +2018 to +2024, because d = 9.00x T sits inside the 64-cycle slack. Only the fill check catches it there.
3. **The published one-cycle scan is one run history, not the property.**
   - The diagnostic's own list, +2010 to +2045, reproduces at 160/0 (`hp-tie36-law.log`, `hp-tietr36-law.log`). That matches the published `phase-law-tables.md` §8.
   - The same head with the list +2018 to +2035 fails at +2025. Where the boundary falls, and what each PDU reads there, depends on the run's history.
4. **What is not affected.**
   - The 18 standing phases sit at least 58 cycles from the boundary. At +0 the delay is 8.972 T, so the previous pop is 58 cycles before the end; at +1953 it is 8.035 T, so the next pop is 73 cycles after it.
   - Every standing phase passes at both processors (`suite-p631.log`, `suite-pc4c.log`).
   - The setpoint ±1 defect fails fill and band at all 18 standing phases (`hp-spp1-law.log`, `hp-spm1-law.log`: 36/36 failing).
   - The standing suite is therefore green and discriminating today. Its phase independence rests on a margin that no check states or asserts, and the documented tie rule does not cover the boundary it was ruled for.

**Impact.**
- Under the PR's own grading, the law still passes or fails with the feed's phase after settle, inside a few-cycle band near the tick-coincident end. That is the defect class #643 exists to close.
- At that band a setpoint −1 defect is accepted.
- The docs and the PR state a one-cycle premise that the head's own trace contradicts.
- A change that moves the RX path's end-to-tick relation by about 26 to 58 cycles, beyond the observed few-cycle walk, would put a standing phase on the boundary.

**Required outcome.** Because this concerns how the declared law is graded, record a public decision first: a STOP to the manager or owner. Then make all of the following true:
- after settle, the graded law either:
  - passes a correct design at every feed phase, including a one-cycle scan across the boundary in more than one run history at both processors; or
  - excludes the phases where it cannot be graded, names them by a stated bound with the reason, and has the suite assert the standing phases' margin from that bound;
- the tie rule as documented matches the measured end-to-pop walk;
- the "cannot mask a defect" property is either true per phase, or restated as a sweep-level property with evidence that a setpoint ±1 defect fails the sweep;
- `MEDIA_CLOCK_FOLLOWING.md`, the README and TESTING rows, and the PR body no longer claim "one cycle of feed jitter" or "ties at +2,025 and +2,026 only" as the property.

**Verification.** Re-run `scripts/probes.sh` (tie scan +2018..+2035, setpoint ±1 at the tie scan) and `scripts/probes3.sh` (+2010..+2045 and the per-PDU trace) on the corrected head at both processors. Then compare against the stated rule.

### R456-1-F2 MINOR: TIME_SYNC.md:451 still states the accept-pulse reading

**Severity and lens:** MINOR. Lens: Docs.

**Where:** `docs/design/TIME_SYNC.md:451`, which reads: "The fill at accept stays the setpoint. Every first event stays inside the law band."

**Authority and evidence.**
- The paragraph reports what the tdm8render `[CRF]` run measures across the live selection. It sits under the `phi` walk table, which is "measured by `make -C tb/verilator/milan_dp_render tdm8render`".
- This PR moved that run's instrument to the PDU end. `T30 CRF LAW` now reads "fill at the PDU end 14..14" (`suite-p631.log`).
- The PR's own `MEDIA_CLOCK_FOLLOWING.md:1355-1364` says a reading at the accept pulse moves with the feed's phase.
- The sentence is a measurement claim, not wording, so it is not RESIDUE.

**Impact.** The authoritative design page attributes to this run a reading it no longer takes. #643's own evidence also shows that reading is phase dependent: an accept-time read of 9 at 2.3 % of the period.

**Required outcome.** The sentence states what the run measures now: the fill at every PDU end is the setpoint plus that PDU, under the tie rule, with first events in the band from the PDU end. Alternatively it defers to the grading-instant section.

**Verification.** Read the corrected paragraph, then run the docs gates.

### Suggestions (non-blocking)

- **S1 (out of scope, candidate new Issue).** `tb/verilator/milan_dp/sim_aclk.cpp:1401`, `:1506`, `:1522` and `:1606` still grade "the fill at accept" for RENDER-INT, RENDER-LIVE-CRF and RENDER-RC-INT. That is the accept-pulse instrument #643's mechanism 3 found phase dependent. The gmstep leg already treats it as print-only (`tb/verilator/milan_dp/README.md:688-694`).
- **S2.** `observe_pdu_end` (`:647`) reads `fill_o` one cycle after the end. That equals the stage's `fill_end_w` (`KL_render_setpoint.sv:533`) except at an end where the stage snaps: a high rail reads back as 14. Requiring the stage's rail, underrun and recentre counters to stay unchanged across each graded window would close that path.
- **S3.** The ceiling check (`:3270-3281`) bounds the wait from `[LAW]` entry. In the full leg the report has already held for 8,626 ticks there ("waited 0"). The check therefore shows the report is present; it does not show settle within the ceiling of the disturbance. The check name and the docs row could say "within 32,768 ticks of `[LAW]` entry".

## What was verified, item by item

| Brief item | Result | Evidence |
|---|---|---|
| Waits for the settled report: engaged, \|err\| <= 32 cycles for 2,048 ticks, within 32,768; fails if it never comes | Holds | `:184-186` and `:3270-3281`. The 32 comes from `(100e6/48000)/64` = `SRC_SETTLE_ERR_C` (`milan_datapath.sv:6264-6266`). `mga_err_w` is `signed [15:0]`, read as `int16_t`. A2-a planted: "waited 32768 ... 0 running", and the ceiling check fails at both processors |
| 18 fresh phases at the INTERNAL grid cadence | Holds | `:193-195` (16 phases at 2083.3/16, plus +927 and +1156). `:3291-3325`: a 4-PDU gap drains to prefill, then the snap, then 124 graded PDUs at `kPduPhysFracNum` 52/391. Delays fall monotonically from 8.973 T to 8.035 T across the 18 phases, so they cover the tick. Every phase reads 14..14 |
| Per phase: settled hold, fill 14 at every PDU end, first event in (8, 9] + 64 cycles | Holds at the 18 standing phases; not at the boundary (F1) | `suite-p631.log` and `suite-pc4c.log`: 18 × (124 PDUs, fill 14..14, 0 ties, 0 ticks outside the band). The two processors differ by at most 1 cycle per phase |
| `observe_pdu_end` is the beat `pdu_end_w` is made of | Holds | `pdu_end_w = s_ok_w && s_tlast_i` with `s_ok_w = s_tvalid_i && tuser < N` (`KL_render_setpoint.sv:305`, `:534`). `s_tvalid_i` is `dpkt_pcm_tvalid_w && dpkt_pcm_tready_w` (`milan_datapath.sv:6466`). `lb_tap_tvalid_w` is the same term with `LOOPBACK_P` (`:6143-6146`). The pop pulse is registered one cycle late (`:499`), so "after 1 = counted, after 2 = not counted" is correct |
| The tie rule cannot mask a real defect | Fails | F1: setpoint −1 passes every check at +2025 |
| A2-a removed fails all 18 | Holds at both processors | `hp-a2a-law.log` and `c4-a2a-law.log`: 88/19, which is 18 per-phase settled checks plus the ceiling check. Fill and band still pass, so A2-a is caught only by the settled gate, as ruled. The driver's tuple verdict is unit checked: missing one of 18 does not count, and +130 cannot stand in for +1302 (`check_mutant_verdict.log`) |
| T30 keeps its pin and A2-a checks | Holds | `:3195-3224`: the window is still graded and `prove_the_aligned_window_is_the_acceptance_state(intr, crf)` is still called. Only the INTERNAL law call moved. Suite 226/0 |
| The CRF law moved without weakening | Holds | With setpoint +1, `--crf-only` fails both T30 CRF LAW checks at 0/292 (`hp-spp1-crf.log`). Clean CRF LAW reads 292 PDUs at fill 14..14 |
| Both processors | Holds | Suite rc 0 at both: 226/0, 65/0, leg defects 5/5. Wall 680.2 s at `631eeb34` and 703.6 s at `c4cb84ff`, cold under make 4.4.1 on a loaded host. `--law-only` clean is 88/0 at both |
| The test fixes the reported failure | Holds | The base harness (`5fabb46e`) at `c4cb84ff` reproduces #643: 227/292 and 285/292, delay 8.830..9.034 (`c4-base-full.log`). At `631eeb34` it passes at 155/0 |
| Docs: instant, #647, boot pull-in, wall time | Hold | The boot probe matches the stated figures. The report is met at tick 4370 after a 2,334-tick run, lapses at 4657, and is met again at 18418. err runs from −222 to +49 (sampled every 100 ticks). Without the dwell, 14 of 18 phases fail the held check (`hp-boottrace-law.log`, `hp-bootnodwell-law.log`). The wall-time figures are consistent with this measurement |
| Docs: tie rule | Fails | F1. TIME_SYNC.md:451 is stale (F2) |

## Lens results

- [R456] UNCLEAN Conformance: F1, MAJOR. Checked at `sim_tdm8_render.cpp:3077-3113`, `:664`, `:3256-3325` against the ruling 5973450039, the #643 acceptance, and `TIME_SYNC.md:373-386`. The tie-scan probes are in `receipts/probes/`.
- [R456] PASS RTL. Checked at `hdl/ieee1722/aaf/KL_render_setpoint.sv:305,422-499,533-534,560-600,678-683` and `hdl/milan/milan_datapath.sv:5902-5932,6143-6146,6255-6310,6443-6488`. These are the RTL contracts the instrument reads: the end beat, the fill, the pop pulse, the aligner taps and the settle constants. Every harness tap matches its RTL source in name, width and cycle. The diff contains no `hdl/` file.
- [R456] UNCLEAN Robustness: F1, MAJOR. Checked with the boundary-phase scans and setpoint ±1 at the tie scan (`hp-tieon`, `hp-tietr18`, `hp-tiespm1` and `hp-tiespp1` logs, plus `c4-tieon-law.log`). Each of these artifacts was examined; the reset, prefill, ceiling and boot-overshoot paths in them are otherwise clean.
- [R456] UNCLEAN Tests: F1, MAJOR. Checked at `sim_tdm8_render.cpp`, `tdm8_render_mutants.py:113-122,302-310,462-480,611-620`, the suite logs, and the mutant and harness probes. A2-a, setpoint ±1 and the CRF LAW all discriminate at the standing phases.
- [R456] UNCLEAN Docs: F1 (MAJOR) and F2 (MINOR). Checked at `docs/design/MEDIA_CLOCK_FOLLOWING.md:1329,1355-1384`, `docs/design/TIME_SYNC.md:361-455`, `docs/testing/TESTING.md:285-287,521,523`, `tb/verilator/README.md:63` and the suite Makefile header.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | the issue body, 5972861856, 5973437153, 5973450039, 5974434363; `TIME_SYNC.md` law table; `sim_tdm8_render.cpp` `[LAW]`, tie rule and instrument; probe logs | R456-1 | `98729742b71d5088f250440eb46085daf1c0cbdb` |
| RTL | CLEAN | `KL_render_setpoint.sv` push, pop, fill and end logic; `milan_datapath.sv` aligner, settle, tap and setpoint wiring; the diff has no `hdl/` change | R456-1 | `98729742b71d5088f250440eb46085daf1c0cbdb` |
| Robustness | UNCLEAN (F1) | boundary scans at both processors, setpoint ±1 at the boundary, the boot no-dwell probe, the A2-a ceiling path | R456-1 | `98729742b71d5088f250440eb46085daf1c0cbdb` |
| Tests | UNCLEAN (F1) | the suite at both processors; `--law-only`; A2-a and setpoint ±1 mutants; the CRF LAW mutant; the base harness at both processors; verdict unit checks | R456-1 | `98729742b71d5088f250440eb46085daf1c0cbdb` |
| Docs | UNCLEAN (F1, F2) | the `MEDIA_CLOCK_FOLLOWING.md` test section; `TIME_SYNC.md` render-latency section; the TESTING and README rows; the Makefile header; the PR body | R456-1 | `98729742b71d5088f250440eb46085daf1c0cbdb` |

## Real limits

- **Make version.** GNU make 4.3 is not installed on this host, so every run used GNU make 4.4.1.
- **Wall times.** The host was shared and loaded, with a load average of about 40. Each elaboration ran at verilator `-j 8`. My wall times are therefore indicative, not a like-for-like comparison with 663.8 s.
- **Campaign not run.** I did not run the full `tdm8render-mutants` campaign. I reproduced the A2-a arm directly at both processors and unit checked the driver's tuple verdict instead. The campaign's 30/26/4 tally, and its four pre-existing failures, are the author's figures and were not re-measured.
- **Processor coverage at the boundary.** The setpoint ±1 boundary probes ran at `631eeb34` only. The clean boundary failure at +2025 ran at both processors.
- **Boundary location.** Where the boundary falls depends on run history. One list fails at +2025, and the published list passes there.
- **Boot trace resolution.** The boot-overshoot trace samples err every 100 ticks, so its extremes are approximate.
- **Not run:**
  - Yosys, parent, processor and gPTP banks;
  - act, Docker and hosted runs;
  - physical calibration and hardware.
  Field skips are not hardware proof.
- **Hosted state when checked.** Exact-head hosted check runs were success for rtl-fast, docs, lint, elaboration, the Yosys shards and Verilator shards 0 and 3. Verilator shards 1, 2 and 4 were still in progress. The physical gPTP context was skipped, and a skip is not an executed result.

## Pending manager duties

- Route F1 to a public decision before any fix, because it touches how the declared law is graded.
- Carry F2.
- Consider S1 as a new Issue.
- Confirm the author's open interpretations:
  - +927 and +1,156 are tick-anchored points, not #83's shifts;
  - `--epoch-only` no longer grades the INTERNAL law;
  - the suite README is the row in `tb/verilator/README.md`.
- Hosted and act acceptance.
- Candidate-merge validation on current dev.
- A fresh review of the corrected head under every lens it changes.

## Receipts

- **Scripts:** `scripts/run_probe.py` (the planting, build and run driver), `scripts/probes.sh`, `scripts/probes2.sh`, `scripts/probes3.sh`, `scripts/probes-runs.sh`, `scripts/vl_jobs.sh`, `scripts/check_mutant_verdict.py` and `scripts/summarize.py`.
- **Inputs:** `inputs/` holds the two adoption patches, byte-identical to the public evidence.
- **Results:** `receipts/environment.txt`, `receipts/suite-*.log` and `.rc`, `receipts/probes/*.log` and `.rc`, `receipts/check_mutant_verdict.log` and `receipts/summary.txt`.
- **Clone state:** after the probes, the review clone is byte-clean. The index equals the HEAD tree (mode, blob and path) and the four gitlinks are unchanged, including `protocol-processor` at `631eeb34`.

R456-1 FINISHED
