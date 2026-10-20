[R678] NEGATIVE - exact head f1fda3f1f87c64801e436e129326b5bd5952bf20

Round R678-1, external independent review of PR #770 for issues #632 and #764. Tree: `b5bb11d04270aeb2721f1961c4d85a11fc7debde`. Reviewed sixteen commits from `e26f1816`, affecting 54 paths. All five lenses were applied independently. Four findings remain open: one BLOCKER, two MAJOR and one MINOR. One prose-only RESIDUE is listed separately.

The existing focused tests pass. They do not clear the missing listener requirement, the configurable AAF output offset, or the two detector/pipeline boundary defects below. The independent verdict and ledger were written before enumerating other public review findings. That enumeration found no prior findings to resolve or retain: two review-start comments, zero reviews and zero inline comments. The dated enumeration is [retained](receipts/prior-public-review-state.json).

**Scope and authorities examined**

Read AGENTS.md, CONTRIBUTING.md and docs/README.md first; then the issue bodies, frozen public scope and investigation; then requirements, interface/design authorities, diff/history and public executable evidence. No private author material, other checkout, other reviewer report or management directory was used.

- [Assignment](https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6284510903): phase inside the single servo, exact fixed-point fold, rate damping, fractional carry, bounded re-acquisition and simulation controls.
- [Latency addendum](https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6284578201) and [domain-reference addendum](https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6284659263): one reference per domain, each interface's own input/output constants, pin-level proof. The second replaces only the first addendum's reference-point item; it retains the remaining latency obligations.
- [Investigation](https://github.com/kebag-logic/milan-fpga/issues/764#issuecomment-6283948176), REQUIREMENTS.md, MEDIA_CLOCK_FOLLOWING.md, TIME_SYNC.md, REGISTER_MAP.md and the referenced capture/render contracts. Governing protocol requirements are IEEE 1722-2016 4.3.5, 10.6-10.8, especially Equation (15), and the assignment's Milan v1.2 7.6.1 frequency-and-phase requirement.
- [Public source evidence](https://github.com/kebag-logic/milan-fpga/tree/8331d72e70283ddb4513a54948bb57a883f301ec/review-evidence/632-r1) and [review-ready statement](https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6299127112). Downloaded receipts were hash-checked against that evidence commit's manifest; [receipt identities](receipts/public-bank-checks.txt) are retained.

**R678-1-F1 | BLOCKER | Conformance, RTL, Tests | docs/design/MEDIA_CLOCK_FOLLOWING.md:1685; docs/design/TIME_SYNC.md:509**

Title: The listener-compensation requirement remains unresolved and unimplemented.

Authority/evidence: The first latency addendum requires the listener's post-grid pin delay to count against presentation offset. The second retains that obligation and requires each interface's constants to be applied to presentation. The changed design explicitly says the listener is not compensated and a decision is needed. The render path still follows its eight-event fill setpoint rather than presentation time; neither the listener datapath nor an output-latency application was added. The public handoff repeats the pending decision. No maintainer/manager comment in the reconstructed scope accepts this omission. The original restriction to the media-clock chain and this later explicit latency requirement therefore remain an unresolved public scope conflict.

Impact: The assigned input-and-output interface contract is not delivered. The pin checks exercise capture timestamping, not the required listener presentation compensation. A positive simulation review would silently narrow the frozen addendum.

Required outcome: Obtain a public ruling that reconciles these requirements before treating the task as review-complete. Implement and prove the retained listener obligation, or have the authorized scope/acceptance decision explicitly record the changed obligation. Merely documenting or moving the missing work does not resolve it.

Verification: Reconstruct the ruling from the issue; check each retained output latency term in the implementation and grade the resulting listener pin instant with a failing dropped-term control. This is a source/simulation scope finding, not a request for pre-merge hardware proof.

**R678-1-F2 | MAJOR | Conformance, RTL, Robustness, Tests | hdl/milan/milan_datapath.sv:1438; hdl/ieee1722/aaf/KL_aaf_packetizer.sv:733; docs/design/MEDIA_CLOCK_FOLLOWING.md:1653**

Title: Configurable non-period AAF offsets defeat CRF-following phase alignment.

Authority/evidence: The assignment requires the DUT's generated AAF timestamps to remain within Equation (15)'s +/-5 percent band and whole-period relationship. The root now supplies the captured domain-event instant as `aaf_tbase_w`, but the packetizer still adds each stream's raw `transit_ns_i`. The root's `pres_offset_fold` at line 3413 passes the controller-set offset without period normalization. The CRF transmitter instead rounds its own offset to periods. The new design acknowledges that a non-period AAF offset moves the stream off the grid; no public scope decision exempts that supported setting.

Even with an ideally aligned domain event, an accepted offset of 2,010,000 ns leaves 10,000 ns modulo Ps at 48 kHz: `3 * 2010000 mod 62500 = 30000`. The permitted band is only 1,041.667 ns. The 2,000,000 ns default has zero residue, which is why the new pin fixtures' fixed default misses this case. This concerns AAF outputs while following CRF, not the explicitly deferred AAF-input following feature.

Impact: The clock can report settled while an outgoing AAF stream is about 0.48 Ps from the followed timing points. Different stream offsets also cannot all be corrected by moving the one domain clock.

Required outcome: Define and implement a clause-consistent output timestamp/offset contract for supported controller settings, while preserving coherent control-plane readback and the single-master domain. Any acceptance exception requires an explicit public decision rather than a documentation caveat.

Verification: Exercise multiple AAF outputs sharing the domain with different offsets, including a non-period offset and boundary values. Grade emitted timestamps against the followed CRF timing points, and require a planted raw-offset regression to fail the named phase check.

**R678-1-F3 | MAJOR | Conformance, RTL, Robustness, Tests, Docs | hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:755; :761; :808; docs/reference/REGISTER_MAP.md:2152**

Title: Averaging across the half-period fold can report a false settled phase.

Authority/evidence: The fixed-point per-sample fold itself is exact, but its signed representatives are averaged arithmetically. Samples just below +Ps/2 and just above -Ps/2 represent nearly the same physical phase; their arithmetic mean is near zero. `ph_inband_w` tests that mean, and four full clean windows assert `ph_settled_o` and MCSRV_STAT[9]. The register contract says the domain event has actually remained within +/-5 percent, and the source/design also claim the fold boundary cannot stall.

The unmodified detector was exercised by [probe_phase_boundary.cpp](probe_phase_boundary.cpp), built by [run_boundary_probe.py](run_boundary_probe.py). With 256 samples per window alternating +10,416 ns and -10,416 ns, the detector reports `theta=0` and `settled=1` after four clean windows. Every sample is about ten times the 1,041.667 ns bound. A separate +/-100 ns positive control also settles. [Raw output](receipts/boundary-probe.log) records both cases.

Probe limits: This isolates the detector by initializing/maintaining LOCKED and supplying a nominal rate-window baseline through public simulation state. It does not force the fold, sum, count, validity or settled outputs. It is not a closed-loop physical-plant demonstration or a claim that every noisy half-period engagement stalls indefinitely. It demonstrates that the actual estimator and published settled predicate accept this out-of-band sample population.

Impact: Near the fold discontinuity, phase samples can cancel the correction and falsely certify the new conformance status bit. The ordinary +0.44/-0.36 Ps engagements and the uncentred-fold mutant do not test this cancellation.

Required outcome: Preserve the meaning of a circular phase when aggregating across the fold, and ensure settled cannot assert from cancelling out-of-band representatives. Update the unconditional no-stall/status claims to match the proved behavior.

Verification: Add a detector regression for balanced and slightly unbalanced samples spanning +/-Ps/2, plus an in-band positive control. Also exercise closed-loop engagements arbitrarily close to that boundary with timestamp quantization/jitter, checking both bounded acquisition and absence of false settled indications.

**R678-1-F4 | MINOR | Conformance, RTL, Robustness, Tests, Docs | hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:948; tb/verilator/media_phase/sim_main.cpp:261**

Title: A restart on the window boundary commits one stale phase correction.

Authority/evidence: The phase contract says an mr restart lets the term go immediately. On the coincident T0 edge, `phase_det` clears `ph_theta_v_r`, but `servo_engine` reads its old value and snapshots the old phase into `pp_ph_r`. `pp_run_r` is still true when the reference rate history remains valid. This input combination is permitted: KL_crf_rx's `rate_break_w` at line 415 includes timestamp/tu/sequence discontinuities, not an mr toggle alone.

The same [boundary probe](receipts/boundary-probe.log) supplies a valid prior phase of 3,000 units and a restart on the boundary. It records `phase_valid=0 held=1 snapped_phase=3000 pp_run=1`, followed by a committed phase contribution of `6000/256` trim units after subtracting the rate contribution. The existing `watch_letgo` checks only the engaged flag and therefore passes despite this correction.

Impact: A newly restarted phase era receives one correction from the invalidated era even though status says the term has let go. The demonstrated error is bounded and small, hence MINOR; it still violates the specified hold behavior and leaves its lenses unclean.

Required outcome: A hold present on the snapshot edge must prevent starting a correction from invalidated phase. Retain the separately documented handling of rate updates that genuinely closed before an event; do not confuse that policy with this simultaneous-boundary case. Correct the comment that the prior valid flag already carries every current hold condition.

Verification: Place mr, enable/liveness loss and other hold events on and around the phase snapshot edge. Check the committed integrator/command contribution, not just the status flag. Keep rate-only carry and re-acquisition tests green.

**R678-1-R1 | RESIDUE | Docs | PR #770, Linked Issue / roles**

Title: Reviewer placeholders remain after the public assignments.

Authority/evidence: The PR body still says both reviewers are `[R<n>], to be assigned`; the public review-start comments assign the internal and external roles.

Impact: Stale template wording only. It changes no code, measurement, verdict, generated artifact, clause claim or privacy rule, and does not independently unclean a lens.

Exact fix: Replace the two placeholder lines with `Internal cleared-context reviewer: [R677]` and `External reviewer: [R678]`.

Verification: Compare those lines with the two public review-start comments. The manager may carry this to the residue checklist.

**Applied-lens evidence beyond the findings**

| Lens | Examined artifacts and result |
|---|---|
| Conformance | Compared the frozen assignment/addenda with the per-source contract and the root's selected-source wiring. Phase is inside the one MMCM servo; AAF-input following remains rate-only as explicitly documented. CRF RX publishes only consumed timestamps, and CRF TX uses every 96th domain event. Individual folds use exact thirds of a nanosecond; F1-F3 prevent acceptance. |
| RTL | Read the complete added phase datapath, reset/state/hold paths and surrounding update pipeline; checked fixed-point widths, signed extension, sample cap and fractional carry. Domain event, capture/walk bank timing, per-interface latency formulas and CRF event-divider replacement were traced through the root. Existing CDC primitives remain the crossing boundary; the new event arithmetic is in the datapath domain. Source lists and tied-off rate-only fixtures were checked. No top-level port or register layout change: only reserved read-only MCSRV_STAT[9] is populated; the phase word itself has no CSR. F1-F4 remain. |
| Robustness | Ran both engagement directions, reference step, 4 ppm ramp, 15 s holdover, INTERNAL, mr, PHC slew, over-rate PDU burst/cap and exact carry. Reviewed liveness timeout/fallback, reset initialization, missing history and state exclusion. Added the fold-boundary and simultaneous-restart probes. Arbitrary supported output offsets remain a configuration hole (F2). The new full phase harness has no dedicated local PHC-step case; the inherited rate-step evidence is distinct. |
| Tests | Independently ran all ten media_phase cases, the three-interface pin harness, all seventeen phase mutants with their clean controls, and chmap_capture's main test. Read capture_coherence's [PIN] grader and five added timestamp mutants, including frame/timestamp coincidence and queued walks. Read both re-timed milan_dp fixtures: only duration/cadence and the matching TDM-slot compile definition change; their assertions remain. Read the author's whole-datapath verdict receipt. F1-F4 identify coverage gaps despite these green tests. |
| Docs | Read the phase/source/interface contract, TIME_SYNC changes, compliance matrix, register description, changelog, test registration/budgets, module matrix, CDC source/render and public gate evidence. The regenerated CDC image was visually inspected. No new historical bench/review label was found in the added source comments; test-instance A/B identifiers describe fixtures. The listener and non-period-offset limitations are disclosed, but disclosure is not approval of changed acceptance. False-settlement and immediate-hold claims need correction with F3/F4. |

The linear small-signal recurrence was independently evaluated: poles 0.9437116 and 0.7015804 give about 0.0180 Hz phase bandwidth and 0.1102 Hz rate bandwidth. The 8-bit fraction carries `sum(e)/2` exactly in the exercised rate-only case: 40 windows, 15 odd errors, sum(e)=255, integrator movement 32640/256. The phase clamp represents a 256 ns/window steady pull (0.5 ppm); this is distinct from the full transient/noise bound in the harness, which allows 400 ns/window and measured 304.7/328.5 ns. The fine-phase actuator/model checks passed; none is physical clock-glitch or calibration proof.

The domain/pin proof is compositional: the long dynamic cases use the scaled clock/plant harness; the separate pin fixture uses three real front ends at their geometry and clock ratios. It is not a single long dynamic simulation of all three interfaces. The pin checks measured maximum stamp-to-pin errors of 30.2, 29.5 and 30.6 ns; the CRF timing points were within 95.8 ns of every interface's frame grid. I2S/blended/slave latency derivations were read but were not independently simulated in this round.

**Execution and public evidence**

| Evidence | Result and provenance |
|---|---|
| Independent exact-head media_phase | Ten cases, 118 checks, zero failures; pins, 11 checks, zero failures. [Case summary](receipts/review-validation-summary.txt), individual case logs and rc files are listed in MANIFEST.sha256. |
| Independent exact-head phase mutation campaign | 27 checks, zero failures: ten clean case/pin controls and all seventeen mutants rejected by their named checks. [Log](receipts/mutants.log), [rc](receipts/mutants.rc). |
| Independent exact-head capture crossbar | Main harness: 797 checks, zero failures. [Log](receipts/chmap-main.log). Its broader synthesis/lockstep bank was not rerun. |
| Independent boundary witnesses | Both real-RTL counterexamples reproduced; near-zero detector positive control retained. Probe rc=0 means the expected defect witnesses were observed, not a clean-design verdict. |
| Author full-suite source receipts | Shards 0/2/3 identify f1fda3f1. Shard 1 identifies e85df091; later changes are the three milan_dp fixture files. Shard 2 initially timed out on capture_coherence and is not itself a clean sweep; the separate exact-head uncontended receipt supplies that suite's successful rerun. |
| Author other source gates | Final mutation receipt is `media_phase_e85df091/mutants.log`, 27/0; the older `media_phase_mutants_s4.log` is not the final campaign. Docs summary identifies f1fda3f1; lint reports 89 at its ratchet. The public Yosys receipt identifies e85df091 and 59 passing tops. These are author executions, not independent executions by this review. |
| Author route-1x1 | The a6ae20f9 receipt passes the recorded recipe/resource gate: LUT 49,644 (+31), FF 52,641 (+288), slices 15,785 (+60), RAMB36/RAMB18/DSP unchanged, WNS +0.276 ns, WHS +0.032 ns; complete route with no unrouted net. The implementation/configuration/submodule paths are identical to this reviewed head, verified by raw git diff. This is ancestor source evidence, not a current-dev merge-candidate run. |
| Exact-state check | All 1,430 tracked parent blobs matched HEAD bytes and modes; the full index matched. The required processor, timing processor, stream-library and firmware-stack gitlinks, their tracked bytes/modes and indexes also matched. [Receipt](receipts/exact-tree.log). No tracked source fix or mutation was made. |

The older -0.46 Ps accounting was checked against the public divider probe: +40 to +60 ns for the retired divider relative to frame sync, leaving about 559 datapath cycles of capture age within the recorded 256-785 range. This explains the constant within that measurement model; it is not a fresh physical calibration.

Portable reproduction, from this packet with absolute paths supplied for the reviewed checkout and scoped compiler:

```sh
rtk proxy python3 run_focused.py "$REPO" --compiler "$SCOPED_COMPILER"
rtk proxy python3 run_mutants.py "$REPO" --compiler "$SCOPED_COMPILER"
rtk proxy python3 run_chmap.py "$REPO" --compiler "$SCOPED_COMPILER"
rtk proxy python3 run_boundary_probe.py "$REPO" --compiler "$SCOPED_COMPILER"
rtk proxy python3 verify_exact_tree.py "$REPO"
```

The scoped compiler identified itself as version 5.050, revision v5.050; its launcher hash is recorded. Drivers keep disposable build/probe trees under `scratch/`, join all child processes, and retain separate logs/return codes. Independent runs and builds were concurrent within the assigned job ceiling. No full parent/processor/timing/synthesis/builder bank, hardware operation, container runner, shared installation, source edit, commit, push or GitHub write was performed.

**Reviewer-owned completion ledger**

Every row was applied at the exact head below. UNCLEAN means no clean covering credit is banked by this round; ordinary passing tests do not resolve its listed findings.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | #632 assignment/addenda; #764 report; `docs/design/MEDIA_CLOCK_FOLLOWING.md:1528`; `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:755`; `hdl/milan/milan_datapath.sv:1438`; `hdl/ieee1722/aaf/KL_aaf_packetizer.sv:733` | R678-1 (F1-F4 open) | f1fda3f1f87c64801e436e129326b5bd5952bf20 |
| RTL | UNCLEAN | `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv`; `hdl/ieee1722/crf/KL_media_domain_event.sv`; `hdl/ieee1722/crf/KL_media_if_latency_pkg.sv`; `hdl/ieee1722/crf/KL_crf_rx.sv`; `hdl/ieee1722/crf/KL_crf_tx.sv`; `hdl/ieee1722/aaf/KL_chan_map_capture.sv`; `hdl/milan/milan_datapath.sv`; `sw/litex/milan_soc.py` | R678-1 (F1-F4 open) | f1fda3f1f87c64801e436e129326b5bd5952bf20 |
| Robustness | UNCLEAN | `tb/verilator/media_phase/sim_main.cpp`; `receipts/boundary-probe.log`; `hdl/ieee1722/crf/KL_media_domain_event.sv:84`; `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:763`; `hdl/milan/milan_datapath.sv:3413` | R678-1 (F2-F4 open) | f1fda3f1f87c64801e436e129326b5bd5952bf20 |
| Tests | UNCLEAN | `tb/verilator/media_phase/{sim_main.cpp,sim_pins.cpp,phase_mutants.py}`; `tb/verilator/capture_coherence/{sim_dp.cpp,mutants.py}`; `tb/verilator/chmap_capture/sim_main.cpp`; `tb/verilator/milan_dp/{sim_nxn.cpp,stream_counters.hpp,stream_counters.py}`; `receipts/public-bank-checks.txt` | R678-1 (F1-F4 open) | f1fda3f1f87c64801e436e129326b5bd5952bf20 |
| Docs | UNCLEAN | `docs/design/MEDIA_CLOCK_FOLLOWING.md`; `docs/design/TIME_SYNC.md`; `docs/reference/REGISTER_MAP.md`; `docs/reference/MILAN_COMPLIANCE_MATRIX.md`; `CHANGELOG.md`; `docs/testing/TESTING.md`; `docs/traceability/MODULE_MATRIX.md`; `docs/diagrams/cdc_census.png`; PR #770 body | R678-1 (F3/F4 open; R1 residue) | f1fda3f1f87c64801e436e129326b5bd5952bf20 |

**Limits and pending manager duties**

No manager source bank exists at this exact head, and none is claimed or inferred here. Source validation above is distinct from composition with live dev `78ca9bdf104819265588726bce4322696c38b8c2` (or its successor at the merge turn). The manager owns the current-dev merge candidate, builder/native banks, hosted/local acceptance, applicable resource re-baseline, required independent review completion, authorized merge and post-merge containment.

Hosted job execution versus skipped contexts was not adjudicated in this round. The original source shard-0 field-campaign skips executed nothing; any separate field-campaign receipt remains separate evidence, not hardware proof. Physical calibration: NOT RUN. The post-merge bench measurement by the #764 method remains the manager's explicit duty and is not a finding here. Neither issue's physical acceptance is discharged by these simulations.

The report and manifest-listed receipts are the publishable packet. `scratch/` is disposable and excluded. Corrected source and any changed acceptance decision require independent re-review; this negative round does not approve later fixes.

R678-1 FINISHED
