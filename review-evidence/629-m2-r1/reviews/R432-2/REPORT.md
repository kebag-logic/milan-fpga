[R432] POSITIVE - exact head d81198c2001756fd84c353d93c312c133c5af66b

# R432-2: internal cleared-context re-review of PR #634 (issue #629, lane M2), round 2

- Head under review: `d81198c2001756fd84c353d93c312c133c5af66b`, tree `4f0217ae46ef99d71a63bba26cee3da8fe827ebd` (re-derived by `git write-tree` after restore). It is eight commits on my round-1 head `57f4b742`, on dev `cdf49d1a28527562888f0a903de51b6b15b1244f`.
- Reconstructed in this order:
  - AGENTS.md, CONTRIBUTING.md (sections 1, 3, 6) and docs/README.md;
  - the #629 body, the lane M2 assignment (5942692103), the STOP (5946475441) and its ruling (5946491571), and the round-2 assignment (5946975634);
  - the full delta `57f4b742..d81198c2`, read against the whole range `cdf49d1a..d81198c2`;
  - the author's round-2 packet at `9423a7b1:review-evidence/629-m2-r1/author-r2` and the PR body's Round 2 section.
- I read the round-1 findings (R432-1 and R433-1, from the same evidence archive) only after finishing my own pass over the delta. I read no other round-2 report.
- Simulator: the pinned Verilator 5.050, identity checked (`receipts/toolchain_identity.txt`). Make: a GNU make 4.3 I built from the GNU release tarball in scratch, plus the host's 4.4.1. The meter suite ran under 4.4.1; the root suite and the `milan_dp` aclk leg ran under 4.3.

## Verdict in one paragraph

Every round-1 finding is closed at this head under its original severity. I checked each one with my own runs. The capture receipt matches the regenerated census, and the gate passes while its four mutations fail. Every figure in sections 17, 18 and 20, the harness README and FASTCONNECT 4.2 matches the receipt or `check_nvm_record_space.py`. Under a real GNU make 4.3, an outer `make -C` hands its recipe `MAKEFLAGS=w`. With that flag, the round-1 Makefile leaks "Entering directory" into the source list and this head's does not. The full root suite then passes under make 4.3 with the pinned simulator: 31/31, 16 mutants caught. The meter suite passes too: 446/0 checks, 6/0 servo checks and 33/33 in its campaign. My round-1 probe script, unmodified, now catches 15 of 15 probes, each by the intended check. I also planted new probes for this round. These were caught: a one-PDU-late deviation verdict, a listener change pulsing `disrupt_p`, the bind edge dropped as an era start, a rising-only `tu` detector (at the root) and swapped `AAFM_STAT` halves (at the root). Two diagnostic-only properties escape, so I file one SUGGESTION and one wording RESIDUE. Nothing at MINOR or above is open. The verdict is POSITIVE. Hosted acceptance belongs to the manager, and several hosted contexts were still running when I last looked.

## Disposition of prior public findings on this PR

| Finding | Original severity | At `d81198c2` | Evidence (this round) |
|---|---|---|---|
| R432-1 F1 = R433-1 F2: stale capture receipt | MAJOR | CLOSED locally; hosted `docs-check` pending (manager) | `scripts/check_nvm_capture.py` rc 0 with every control; `--mutation bytes`, `records`, `clock` and `ignore-off-timing` each rc 1 (`receipts/capture_gate*.log`). The receipt's `measured_for` is the live census: 8x8 164 records / 13,210 B, 1x1 54 / 3,290 B. The six arms match the README recipe: both shapes at 50 MHz, ON and OFF, 16 captures each, plus the labelled 100 MHz 8x8 point, each under `unshare -Urn`, offline and `PYTHONHASHSEED=0`. Base `a2f17342` has tree `c28595df`, and `a2f17342..d81198c2` touches only docs, the README and the receipt, so no hashed harness file or firmware changed after the measurement. 8x8 maximum 13.86484 ms, below 24.5 ms. |
| R432-1 F2: root suite under hosted make | MAJOR | CLOSED locally; hosted shard 2/5 pending (manager) | `receipts/make_c_flag_inheritance_probe.txt`: under make 4.3 a `make -C` recipe sees `MAKEFLAGS=[w]`; under 4.4.1 it sees `[]`. `receipts/make43_light_probe.txt`: with `MAKEFLAGS=w`, the `57f4b742` Makefile's `SRCS_DP` holds "Entering directory" tokens under both 4.3 and 4.4.1, and this head's holds none. `receipts/mclk_suite_make43_pinned.log`: `make -C tb/verilator/milan_dp_mclk` with make 4.3 first on PATH (so the driver's nested `make` is 4.3 too) and Verilator 5.050 gives rc 0, legs A 55/0, C 32/0, B 50/0, "31 checks: 31 PASS", 441 s. |
| R432-1 F3: port-doc and naming ratchets | MINOR | CLOSED | `check_port_contracts.py`: hdl 217 <= 217. `measure_naming.py --check`: 95 recorded, PASS. Neither budget was raised (`receipts/static_gates.log`). `KL_aaf_clock_meter.sv:104-163` documents `clk_i`, `rst_n` and `subtype_i`, puts `CLK_FREQ_HZ_P` in Hz and maps `fsh_i` to its octets. `max_dev_ns_o` carries its unit. |
| R432-1 F4 = R433-1 F1: "`tu` taken from the `tv` net" | MINOR | CLOSED | Root mutant 15 `.tu_i ((mclk_mut_r == 15) ? avtprx_tv_bit : avtprx_tu_bit)` is caught by "tu: the followed talker's tu edge restarts the meter's history". Leg A's `[TU]` row, 5 checks, passes clean. `sim_main.cpp`'s M7 banner now says that the wiring mutant runs at the root. |
| R432-1 F5 (a)-(e): meter rules no test could fail | MINOR | CLOSED | `receipts/r1_reviewer_meter_probes_at_d81198c2.txt`: the round-1 script, sha256 `8a33265d...` (as published), catches 15 of 15. Each F5 probe fails its intended check: M3/M12 "the restart lands at the step's PDU", M6 "gap before lock", M7 "listener change ... clears", M7 "bind edge ... kept" and M4 "0 channels". (b) also fails at the root: mutant 16 is caught by "switch (iv): the meter's lock clears at the switch". |
| R432-1 F6: the `obj_aclk` row cites a missing script | MINOR | CLOSED | `tb/verilator/milan_dp/README.md:74` now names `milan_dp_mclk` mutant 3. That mutant is caught in my run: "INTERNAL: the packet grid holds the physical grid's rate". |
| R432-1 F7 = R433-1 F3: FR_NFR status row | MINOR | CLOSED | `FR_NFR.md:156` reads "AAF following implemented and graded in simulation (#629, PR #634); bench acceptance open". This matches the ledger row `aaf.media-clock-following` `implemented`. |
| R433-1 F4: the 0x8C8 sentence | MINOR | CLOSED | `REGISTER_MAP.md:1837-1839` maps `0x8E0` and `0x8E4` and leaves `0x8E8` to `0x8F4` unmapped. |
| R432-1 R1, R2, R4; R433-1 R1, R2, R3 | RESIDUE | TAKEN | Design Implementation notes VERSION row and area row (`ooc.sh` recipe plus the STOP item 8 link); TESTING "three legs (A, B, C)"; TIME_SYNC W2 row. |
| R432-1 R3: PR body | RESIDUE | TAKEN | The PR body's Status and Known limitations carry the post-ruling state. |
| R432-1 S2: FR-CLK-04 `mr` qualifier | SUGGESTION | TAKEN | `FR_NFR.md:239`. |
| R433-1 S2: two-sided INTERNAL rate | SUGGESTION | TAKEN for `sim_aclk`; RETAINED for render T30 | `receipts/milan_dp_aclk.log`: 193 checks, 0 failures; INTERNAL measured +0.8002 ppm, and the check `abs(ppm) < 5 && abs(ppm - plan) > 5` passes. The T30 reason holds: `sim_tdm8_render.cpp:2897-2904` describes T30's INTERNAL window as the aligner's pull-in after T14's hold, and T31 grades the settled walk. |
| R432-1 S1 = R433-1 S1: settle band on `mga_sel_w` | SUGGESTION | RETAINED, reason accepted | It would change the merged design's settle table and TIME_SYNC's "at INTERNAL: 2048 ticks after the change", so it needs its own decision and re-validation. No defect is observed. A SUGGESTION does not affect coverage. |

## Findings of this round

No BLOCKER, MAJOR or MINOR.

### R432-2-S1 - SUGGESTION - Tests, Robustness - the largest deviation's era clear and its saturation are documented but ungraded

- **Where:**
  - `hdl/ieee1722/crf/KL_aaf_clock_meter.sv:492-493` (saturation) and `:598` (era clear);
  - the contract added this round at `:155-158` ("saturating at 65535; a level, cleared by an era start");
  - `docs/reference/REGISTER_MAP.md:2084` and `:2088`.
- **Evidence:** in `receipts/reviewer_meter_probes_r2.txt`, two probes escape every meter case they were run on (rates, restarts, beyond, step_in_gap):
  - P1, the era-start clear of `max_dev_r` removed;
  - P2, the 0xFFFF saturation removed, so the field wraps.
  - P1 escapes because `follow()` resets the DUT before each rate, and `case_rates` visits rising magnitudes.
  - The root grades the field once, inside a single era (`sim_mclk.cpp:734`).
  - The design's test plan does not name either property. Its CSR row is "each field equals the meter's", which is graded.
- **Impact:** a bench reading of `AAFM_STAT[31:16]` could carry a previous era's or listener's maximum, or wrap, with no failing test. The field is a diagnostic with no functional consumer.
- **Suggested outcome:** a meter check that reads `max_dev_ns_o` after an era start (a listener change or entry) with a smaller offset than before, and one step above 65,535 ns. This needs a non-PDU-0 deviation that is not already a restart, so it may need a held group or a direct jump-bound bypass. Alternatively, record that the field is untested.
- **Verification:** P1 and P2 from `scripts/reviewer_meter_probes_r2.py` become CAUGHT.

### RESIDUE (owner rule 2026-10-02: wording only; no effect on verdict or lens)

- **R432-2-R1.** `docs/design/MEDIA_CLOCK_FOLLOWING.md:994-997`, the meter's "Outputs" bullet still lists the largest deviation inside "a status word". Since `13721318e` it is the meter's own port `max_dev_ns_o`, and the root composes `AAFM_STAT` from both ports. Exact fix: replace "and a status word with the lock, the rate validity, the followed listener, a history-restart count and the largest `|ts_i - ts_0 - i * 125,000|` seen this era." with "a status word with the lock, the rate validity, the followed listener and a history-restart count; and the largest `|ts_i - ts_0 - i * 125,000|` seen this era (`max_dev_ns_o`). The root composes the two into `AAFM_STAT`."

## Delta checks that came out clean (evidence)

- **(1) Capture re-measure and census helper.**
  - `scripts/nvm_shape.py:251-261` `closed_record_census` is the gate's former inline computation, unchanged: `REC_HDR + payload` summed, plus the overflow refusal.
  - `soc.py` derives the census with the same `binding_base()` (`milan_soc.py:88` imports it from `nvm_shape`) and writes it into `sources.json`. `run.py:66` grades against it.
  - The gate binds receipt rows to its own recomputation (`check_nvm_capture.py:77-84`) and drives its timing fixture from the live census.
  - The trace fix (`sim_main.cpp:61-91,169-193`) only defers the five TX traces to a console line start and flushes at the end. The grading path is unchanged.
  - `scripts/check_capture_figures.py` (`receipts/capture_figures_vs_receipt.txt`, 18/18) recomputes every section 18 table row, maximum, ratio, margin, census, commit, tree and digest from the receipt's raw rows.
  - `check_nvm_record_space.py` reports 3,336 B / 54 records / 0xA6 at 1x1 and 13,256 B / 164 / 0xEA at 8x8 (20 percent of a slot; commit at most 3.07 / 3.27 s). These equal FASTCONNECT 4.2's table, deadline block, DDR budget and commit table. I also checked the arithmetic by hand.
  - Stale-figure sweep: old figures remain only in dated findings and in the `fw_service_budget` trace fixture. That fixture's `oracle.json` pins recorded traces, not the live census; the author flags it outside #629.
- **(2) Nested make.** See the F2 row. The same unguarded pattern exists in `milan_dp_render/Makefile:57,62` and `pp_shadow/Makefile:107`. Neither file is changed by this PR, and neither has a driver that re-enters make. The author lists both as outside #629, so I note them and file nothing.
- **(3) The meter's port split.**
  - `KL_aaf_clock_meter.sv:379-381` gives `max_dev_ns_o = max_dev_r` and `status_o = {restart_cnt_r, idx, 1'b0, en, rate_valid, locked}`.
  - `milan_datapath.sv:5675-5705` gives `aafm_stat_w = {max_dev_ns_w, status_w}`. That is bit-for-bit the round-1 word, inside the parent's fabric; the processor boundary is unchanged.
  - Both test wrappers compose the same 32 bits.
  - Area is unchanged. `syn/yosys/ooc.sh KL_aaf_clock_meter` rc 0: 558 LUT + 16 LUTRAM = 574, 636 FF, 0 RAMB, 0 DSP, 102 CARRY4 (`receipts/ooc_aaf_clock_meter.txt`).
  - My root probe RS swaps the halves. It is caught on `--tu`, `--csr` and `--select` ("AAFM_STAT {idx, en, locked} got=1 exp=5"; `receipts/reviewer_root_probes_r2.txt`). So the composition is graded.
  - Lint passes at 90 <= 90 (`receipts/static_gates.log`).
- **(4) The new failing tests.**
  - Root mutants 15 and 16 are caught by their named checks, and the clean `--tu` and `--silent` legs pass.
  - The leg-B row "switch onto a talker silent past the meter's timeout" matches the design's rules. A listener change clears the lock with no `disrupt_p` (design `:986-993`), and nothing but the source change requests a restart (design `:1088-1092`).
  - The meter's graded rules M1, M3, M4, M6, M7 and M12 each fail under their named mutant (`receipts/meter_suite.log` and `receipts/meter_mutants.log`, 33/33 twice).
  - My own probes: P3 (the deviation verdict one PDU late) fails M3 and M12 "the restart lands at the step's PDU". P4 (`disrupt_p` on a listener change) fails M7 "no disrupt_p pulse". P6 (the bind edge dropped from the era start) fails M7 "rate_valid falls at the event". P5 (a rising-only `tu` detector) escapes the meter suite, whose M7 drives only a rising edge, but fails at the root on "tu: the falling edge restarts it again", in both `--tu` and full leg A.
- **(5) Docs.**
  - Docs gates, all rc 0 with the pinned Markdown environment (`receipts/docs_gates.log`): `docs_check` 0 findings, `check_doc_style`, `gen_toc --check`, `gen_toc --verify-anchors` (299 links), `check_em_dash --base cdf49d1a` (531 added lines, 0 findings) and `check_doc_paths` (890 paths).
  - `git diff --check cdf49d1a HEAD` rc 0, and the design page ends in a single newline.
  - `check_entity_shape.py` 166/0.
  - `milan_dp_mclk/README.md` (sixteen mutants, legs A, B and C, 438 s under make 4.3) agrees with my run (441 s, 31/31).
  - TESTING's two rows, TIME_SYNC's W2 row and FR-CLK-04's qualifier agree with the RTL and the design.
- **(6) The rebuilt image.** These figures come from the author's receipts. I did not rebuild.
  - The timing summary shows WNS +0.065 ns and WHS +0.036 ns, with 0 failing endpoints out of 180,759.
  - All four sign-off negative-slack reports read "No timing paths found".
  - Route status shows 0 nets with routing errors.
  - Placed utilization: Slice 15,834 / 15,850 = 99.90 % and Slice LUTs 80.52 %. The hierarchical report places `g_aaf_meter.aaf_clock_meter` at 483 LUT / 630 FF.
  - Nothing under `hdl`, `sw/litex`, `syn` or `configs` changed after `13721318e`, and the image was built at `d81198c2`.
  - "0 critical warnings, #607 clean" is the author's reading of `vivado.log`. That log is published only as a hash, so I could not check it.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-2 assignment items 1-6 against the delta. Round-1 F1/F2/F4/F7 and R433-1 F1-F4 re-judged (table above). Capture limit 24.5 ms against the receipt maxima (`check_nvm_capture.py` rc 0). Design `:978-997` and `:1084-1092` (era, lock falls, one request per switch) against the root `[SWITCH-TIMEOUT]` and `[TU]` rows and against IEEE 1722-2016 4.4.4.3 and 4.4.4.7. `FR_NFR.md:156,239`; `REGISTER_MAP.md:1837-1839,2071-2088`. | R432-2 | `d81198c2001756fd84c353d93c312c133c5af66b` |
| RTL | CLEAN | `KL_aaf_clock_meter.sv:104-163,319-381,407-605`; `milan_datapath.sv:5662-5714` (port split and composition); both test wrappers; Yosys out-of-context area 574 LUT / 636 FF; lint 90 <= 90; port-doc 217 <= 217; naming 95; root probe RS caught; image receipts (timing summary, four corners, route status, both utilization reports) | R432-2 | `d81198c2001756fd84c353d93c312c133c5af66b` |
| Robustness | CLEAN (S1 is only a SUGGESTION) | Lock and era paths: listener change, entry, bind edge, `tu` edges, timeout after a silent switch; meter probes P1-P6; root probes P5 and RS; nested make under an inherited `MAKEFLAGS=w` (make 4.3 and 4.4.1); TX-trace interleave fix; census growth through the capture gate and `check_nvm_record_space.py` | R432-2 | `d81198c2001756fd84c353d93c312c133c5af66b` |
| Tests | CLEAN (S1 is only a SUGGESTION) | `tb/verilator/aaf_clock_meter`: `make` rc 0, 446/0 and 6/0, campaign 33/33, plus a second campaign 33/33. `tb/verilator/milan_dp_mclk` under make 4.3: rc 0, 31/31, mutants 15 and 16 caught. `tb/verilator/milan_dp` `aclk`: 193/0, two-sided INTERNAL check at +0.80 ppm. `check_nvm_capture.py` with 4 mutations. Round-1 probe script 15/15. Round-2 meter probes (4 caught, 2 escape: S1). Root probes 2/2 caught. | R432-2 | `d81198c2001756fd84c353d93c312c133c5af66b` |
| Docs | CLEAN (R1 is RESIDUE) | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` sections 17, 18, 20 and `nvm_capture_cpu/README.md` (figures script 18/18); `SAVED_STATE_FASTCONNECT.md` 4.2, 8.1, 9 against `check_nvm_record_space.py`; design Implementation notes; FR_NFR; REGISTER_MAP; TESTING; TIME_SYNC; the `milan_dp` and `milan_dp_mclk` READMEs; the PR body Round 2 section; docs gates (6/6 rc 0); `git diff --check` | R432-2 | `d81198c2001756fd84c353d93c312c133c5af66b` |

## Real limits of this review

- **Not run:**
  - physical calibration, the bench and hardware;
  - Vivado: the image figures are the author's receipts, and `vivado.log` is published only as a hash;
  - the full suite sweep, the builder bank and the native bank (the manager's);
  - Yosys portability, the gPTP and processor banks, Docker/act, `act_ci.py` and its self-test.
- **The capture arms were not re-measured.** I did not use the product LiteX/SDK environment. I verified the receipt through the gate's regrade (it recomputes every arm's summary and maxima from the raw rows), through the figures script, and through the base-to-head file list.
- **The README's negative controls were not re-run.** These are `skip-copy`, `no-traffic` and `byte-only`. Neither I nor, as far as the author's packet states, the author re-ran them this round. The round-2 harness edits do not touch their byte or traffic oracles.
- **The rebuilt image was not reproduced.** Its timing figures are the author's receipts.
- **The meter suite ran under make 4.4.1.** Only the root suite and the aclk leg ran under 4.3. The meter suite has no nested make derivation.
- **The root probes were scoped.** RS ran on three short legs. P5 ran on `--tu` and full leg A. Neither ran through the schemata campaign.
- **Receipts are path-scrubbed.** In the three suite logs, the home-directory prefix is replaced by `$HOME` and the pinned simulator's install root by `<pinned-simulator-root>`. Nothing else is edited.
- **Hosted state at 12:08Z** (`receipts/hosted_check_runs_at_head.txt`): `docs-check`, `elaborate` and Verilator shards 1/5, 2/5 and 4/5 were still in progress. "Physical gPTP (nightly and manual)" was skipped, not executed. Every completed context was success.
- **Incident.** At about 11:48:50Z I stopped my own first root-suite run, started in error on the unpinned host simulator, by matching command-line patterns. That run is not used as evidence. The same pattern very probably also ended the root-suite campaign of the other internal review session running on this host at the same time. Its log, of which I saw only the last lines, ends `rc=2` after 2 min 19 s. I touched none of its files. Separately, I mistook my first meter campaign for interrupted and ran it again; both runs completed 33/33.

## Pending manager duties

- **Hosted acceptance at the exact head.**
  - `docs-check` green, with the capture-gate step and every later step executed (F1's hosted verification).
  - Verilator shard 2/5 green, with `milan_dp_mclk` tallied and 16/16 mutants caught (F2's hosted verification).
  - The remaining in-progress shards and `elaborate`.
- **The interrupted parallel review run.** Confirm that the other internal review session's root-suite campaign was cut short by the incident above, and have it re-run.
- **Merge turn.**
  - Protocol-processor #141 lands first, then the parent bumps its pin, as the design orders.
  - The final current-dev candidate build and validation.
  - The builder (48) and native (5) banks at this head are the manager's; they are reported passed.
- **Residue checklist.** Carry R432-2-R1. R432-1 R1-R4 and R433-1 R1-R3 are taken.
- **Bench lane.** Following AAF and CRF, a switch, lock loss, A2-a at INTERNAL, and the oscillator-grade risk as an observation.
- **Optional.** S1 above. The retained settle-band suggestion (R432-1 S1 = R433-1 S1) is the author's proposed follow-up for a manager decision.

R432-2 FINISHED
