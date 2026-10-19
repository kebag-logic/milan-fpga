[R664] NEGATIVE - exact head d30a208d44d5868cc356e6a8b7abc89b062ca9bd

Round R664-3, external independent review of PR #767, issues #761/#762.
Tree: `d203767adbab4025cbfb3f760540783f65cc2e6c`.
Source base: `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`.
Previous reviewed head: `eef90b4238b6c19b679b44adc6f09362809be153`.
Delta: `cb65d9d7`, `336a6f6a`, `d30a208d`: two RTL comments, an integrated test, and its README paragraph. No executable RTL change.

All five lenses were applied. One MINOR remains: the integrated test and its wiring mutants work on the exercised configurations, but none exercises a shipping AX7101 datapath geometry. This retains the shipping-shape portion of R663-2-F1. No new RTL correctness defect was found. The two requested comment edits and PR status/role corrections are applied.

## Reconstruction and independence

Read AGENTS.md/CONTRIBUTING.md, docs/README.md, both issue bodies and public decisions, requirements/interface authorities, the source-base diff/history and round-3 delta, then public execution evidence. The independent verdict and all-five-lens ledger were written before consulting prior reviewer reports. Prior public findings were then checked at their causes. No current round report, private author material, management checkout, or other reviewer scratchpad was read.

Authorities: [initial assignment](https://github.com/kebag-logic/milan-fpga/issues/761#issuecomment-6256482625), [stopped-silence ruling](https://github.com/kebag-logic/milan-fpga/issues/762#issuecomment-6260976223), [stopped-gap extension](https://github.com/kebag-logic/milan-fpga/issues/762#issuecomment-6265746720), and [round-3 assignment](https://github.com/kebag-logic/milan-fpga/pull/767#issuecomment-6274405031). `receipts/public-scope.txt` preserves these public statements and the exact-head author handoff. The prior clause interpretation is carried forward: IEEE 1722-2016 4.4.4.3/10.4.3; Milan v1.2 5.3.8.7, 5.3.8.10/Table 5.6, 5.4.2.19/.20, and 5.4.2.25/Table 5.16. This is a delta review, not a new full-standard audit.

## Open finding

**R664-3-F1 | MINOR | Conformance, Robustness, Tests, Docs**

**Artifact:** `tb/verilator/milan_dp/sim_nxn.cpp:6438,6680`; `tb/verilator/milan_dp/Makefile:244,605,614,629,645`; PR #767 body, Round 3 and Definition of Done; published `author-r3/receipts/r3-mutants/*`.

**Title:** The shipping AX7101 shape required to close R663-2-F1 is still absent.

**Authority/evidence:** The round-3 assignment requires the integrated case on a shipping datapath shape. The review assignment explicitly asks whether that includes a shipping AX7101 shape rather than only a retired-board shape. REQUIREMENTS.md section 1 and `docs/overview/ARCHITECTURE.md` define the current product; `sw/litex/build.sh:195,378` and `configs/generated/sweep_opts_ax7101.sh:15` identify its one-stream, eight-wire-channel TDM8 master configuration.

The new function is reached in the broad `sim_nxn.cpp` flow. The four published executions and their build recipes are:

| Leg | Actual shape relevant to this finding | New case |
|---|---|---|
| `obj_nxn` | Arty 4-stream entity, default 2 wire channels, no TDM interface | 13 checks pass |
| `obj_nxndv` | Divergent Arty 4-stream entity, same geometry | 13 checks pass |
| `obj_nxn4c` | Arty 4-stream entity, 4 wire channels, TDM8 plus I2S pair | 13 checks pass; all wiring mutants run here |
| `obj_nxn8` | AX7101 8-stream entity, but default 2 wire channels, `AUDIO_IF_SLOTS_P=0`, slave/default audio mode, `LPF_P=1` | 13 checks pass |
| `AX1X1_BUILD` / `obj_ax1x1` | AX7101 1-stream entity, 8 wire channels, TDM8 master, loopback, playback/filter prunes | Uses `sim_main.cpp`; no `[762-DP]` case |

The AX7101 entity name in `SHAPE_8x8` does not establish a shipping datapath geometry. That recipe omits the geometry overrides, inheriting `milan_datapath.sv:123,129,139,208`. The AX8x8 config itself specifies TDM32 (`configs/endstation_ax7101_8x8.yaml:172`) and eight-channel stream formats. Thus NxN8 does not supply the missing product-shape run either. AX-specific focused legs using `sim_nxn.cpp` return through their focused paths before this new broad section; the published excerpt contains exactly the four broad executions.

`receipts/spot-checks.log` verifies the recipes, inherited parameters, absence from the shipping harness, all three mutant failures, and the clean control. The public mutation script and build receipts explicitly use `build-nxn4c`. The PR calls that retired geometry the “shipping Arty shape” and marks the acceptance criteria satisfied. That assertion is being used to satisfy an evidence requirement, so it is not merely wording residue.

**Impact:** The wiring regression is now dynamically detectable on the exercised test configurations, but the required product-configuration evidence remains missing. No actual failure of the correct RTL on AX7101 is alleged. Accepting a descriptor-only resemblance as the product shape would incorrectly close the assigned validation gap.

**Required outcome:** Exercise the stopped-gap, stopped-silence and START/relock/gap count case on a shipping AX7101 datapath geometry, with a passing clean control and the assigned tie-off and wrong-vector plants failing their named checks. Name the exact shape and any simulation substitutes accurately in the evidence and PR. Existing documented verification timing/gPTP substitutes can remain explicit; this does not require a new hardware campaign or full SoC simulation.

**Verification:** Show the elaborated stream/audio/prune parameters and matching entity definition. Clean: SEQ_NUM_MISMATCH +1 with stopped-gap SI +0; MEDIA_UNLOCKED +1 with stopped-silence SI +0; after START/relock, gap SI +1. Tie-off and wrong-vector runs must build successfully and fail the intended `[762-DP]` assertions. Review the corrected exact head and receipts. This is the unfulfilled portion of R663-2-F1, not a second independent RTL defect.

## What the new test does prove

`sim_nxn.cpp:6680-6728` sends STOP (`0x0023`) and START (`0x0022`) through `aecp_xact`, and polls GET_COUNTERS (`0x0029`, STREAM_INPUT 0) through `sin0_ctrs`. It establishes lock, advances through settle, injects a two-lost-PDU gap, expires silence while still stopped, then starts, relocks and injects another qualifying gap. Positive mismatch/unlock counts prevent the zero-SI checks from passing on a dead receive path.

The silence shortcut sets only `sil_ms_r[0]` to 97 after asserting it was lower, then executes four real milliseconds. It does not force the lock result or counter. This grades expiry and the integrated stopped-state wire; it does not independently measure 100 ms of physical silence. The 100 MHz assumption matches these broad recipes. The existing unaccelerated receiver tests retain the timeout-duration evidence.

The published controls agree with the assertions:

| Public run | Checks | Failures |
|---|---:|---|
| clean | 1,981 | 0 |
| `tie0` | 1,981 | stopped-gap SI +0 and stopped-silence SI +0 each observe +1 |
| `sink1` shifted vector | 1,981 | the same two named failures |
| `bound` vector | 1,981 | started-gap SI +1 observes +0 |

No unrelated check fails in those run logs. The mutation runs identify head `336a6f6a`; its sole difference from `d30a208d` is the README addition, verified locally. The exact-head broad-leg receipts report 1,981 / 1,983 / 3,765 / 1,981 checks, each with the 13 new successful checks. These are audited author executions, not newly executed simulations by this reviewer.

## Prior findings at this head

| Finding | Disposition | Cause/evidence checked |
|---|---|---|
| R664-1-F1, MAJOR, Conformance/RTL/Robustness/Tests | Resolved, carried from R664-2 | `KL_avtp_rx_monitor_ctx.sv:903,1069,1144`: eligibility captured at expiry, later Unbind does not clear it, consumption/reset/bind-era clearing retained. `sim_lockstep.cpp:319,867` retains the independent expiry calculation and exact per-trial `d > 0` oracle. Neither logic nor sweep changed this round. |
| R664-1-F2, MAJOR, all lenses | Resolved, carried | Public scope rulings settle stopped silence/gaps. AAF guards `:910,1025`, CRF guards `:401,559`, REGISTER_MAP `:873` and compliance row 5.4.2.25 remain aligned. |
| R663-1-F1, BLOCKER, Tests/Docs | Resolved in source, carried | `ci_case_receipts_selftest.py:174` still derives the invalid split as inventory length +1. Round-3 gate_50 has 14/14 rc 0 and reports over-shard 0/35 refused for 34 cases. Hosted acceptance remains separate. |
| R663-1-F2, MINOR, Conformance/Robustness/Docs | Resolved, carried | Both engines retain the same stopped-input silence/gap rule; unchanged count-graded stopped/recovery cases and documented rules. |
| R663-1-F3, MINOR, Tests/Docs | Resolved, carried | Exact boundary oracle and paired consume-race mutant remain unchanged; round-3 receiver receipt retains 14/14 mutation verdicts. Prior independent paired-probe evidence remains applicable. |
| R663-2-F1, MINOR, Tests | Partially resolved; retained through R664-3-F1 | Integrated wire-level count case and meaningful wiring mutants now exist. Required shipping AX7101 geometry remains unexercised. |
| R663-2-F2, RESIDUE, Docs | Resolved | Both requested sentences appear verbatim at `KL_avtp_rx_monitor_ctx.sv:152` and `milan_datapath.sv:6307`. |
| R663-2-F3 and R664-2-R1, RESIDUE, Docs | Resolved | PR body no longer claims the head is unpushed; names internal R663/external R664; separates completed eef90b42 evidence from round-3 publication and checks. |
| R663-1-S1, R663-2-S1, R664-2-S2 | Retained, optional | Details below. None changes the verdict or banks an otherwise unclean lens. |

## Retained suggestions

**R663-1-S1 | SUGGESTION | Tests.** Artifact: `milan_datapath.sv:3247`; `milan_dp_mclk/sim_mclk.cpp:887`; `sw/builder/test_builder.py:11379`. The selected-CRF gate remains correct and statically pinned. Prior public probing found no dynamic rejection of an ungated gain edge; these artifacts are unchanged. Impact: dynamic coverage would complement the static pin. Optional outcome: CRF re-lock while INTERNAL or AAF is selected produces no request/toggle. Verification: clean row passes and ungated-gain plant fails its named assertion.

**R663-2-S1 | SUGGESTION | Tests, Robustness.** Artifact: `tb/verilator/crf_rx/sim_main.cpp:1662`; `KL_crf_rx.sv:559`. Existing stopped-silence trial stops well before expiry; the RTL reads the state directly at expiry. Impact: a boundary row would preserve the edge contract explicitly. Optional outcome: STOP one edge before/on/after timeout gives SI +0/+0/+1. Verification: independent exact counts and a delayed-state plant. The manager explicitly did not assign this suggestion.

**R664-2-S2 | SUGGESTION | Tests, Docs.** Artifact: `tb/verilator/crf_rx/mutants.py:44,72`; `sim_main.cpp:1723`. The built-in driver pairs only the two stopped-gap plants; the prior external review demonstrated all seven paired controls. Neither file changed this round. Impact: preserving those paired controls would strengthen repeatable oracle-independence evidence. Optional outcome: incorporate the five earlier paired unit plants; until then, qualify the function comment as “both stopped-gap mutants.” Verification: clean control passes and all seven paired plants fail their own count assertions. This remains the prior optional suggestion, not a new round-3 residue.

No new prohibited source-comment lane/reviewer identity or additional wording residue was found in the round-3 delta. Named test IDs such as `[762-DP]` identify executable checks, not bench lanes.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN, F1 | #762 rulings; round-3 shipping-shape acceptance; `sim_nxn.cpp:6680`; `build.sh:195`; config/recipe comparison. Counter law itself remains clean. | R664-3; unchanged law carried from R664-2 | d30a208d44d5868cc356e6a8b7abc89b062ca9bd |
| RTL | CLEAN | Two RTL comment hunks; executable-token equality; `milan_datapath.sv:3247,6308`; ctx expiry/accept/consume/reset guards; CRF counter-writer exclusion. | R664-3 comment/dependency check, carrying R664-2 at eef90b4238b6c19b679b44adc6f09362809be153 | d30a208d44d5868cc356e6a8b7abc89b062ca9bd |
| Robustness | UNCLEAN, F1 | Stopped gap/silence, liveness, resumed count and watchdog shortcut in `sim_nxn.cpp:6680`; product-configuration coverage; unchanged unit boundary/reset/rebind evidence carried. | R664-3; unchanged unit behavior carried from R664-2 | d30a208d44d5868cc356e6a8b7abc89b062ca9bd |
| Tests | UNCLEAN, F1 | `Makefile:244,605,614,629,645`; new count oracles; public clean/mutant build/run logs; `receipts/spot-checks.log` | R664-3 | d30a208d44d5868cc356e6a8b7abc89b062ca9bd |
| Docs | UNCLEAN, F1 | Both port comments; `milan_dp/README.md:1188`; PR Round 3 shipping/acceptance claims; public receipts and scope | R664-3; unchanged normative documents carried from R664-2 | d30a208d44d5868cc356e6a8b7abc89b062ca9bd |

The ledger does not reopen unchanged engine correctness. F1 affects acceptance evidence, configuration-dependent verification, the test population and its public completion claim; it alleges no RTL defect. The round-2 receiver ordering, reset, wrap, rebind and clock-restart conclusions remain carried at their unchanged artifacts.

## Evidence, authentication and execution limits

Audited [the published packet at afc1a1ac](https://github.com/kebag-logic/milan-fpga/tree/afc1a1ac02210ae5868ec75b3102ff4778b29809/review-evidence/761-r1). `scripts/audit_public.py` verified 166 selected author receipts against `published_sha256`. Publicly redacted files are checked against their published digest, not their original private-byte digest. Raw selected build/run receipts accompany this report; all downloaded working copies remain under `scratch/`.

Signature authentication is **not established**. The publication commit reports `verified=false`, `reason=unsigned`; no detached signature was identified in the supplied packet. `receipts/evidence-authentication.json` records that result. Content-digest verification is not a signed execution attestation. This is the same disclosed provenance limit as round 2, not a new code finding.

Round-3 source receipts: milan_dp and avtp_rxmon rc 0; gate_50 14/14 rc 0; other static commands 80/82 rc 0, with the same disclosed host-only act-runner and git-absent selftest exceptions. Builder verdict is PASS EXCEPT gate 11 NOT RUN. The large milan_dp publication is a tail plus explicit leg/check excerpts, not a complete raw all-leg log; the four mutation/control logs are complete.

Carried eef90b42 source receipts: five shard summaries total 63 suites and 2,188,354 checks with zero failures/timeouts; route-1x1 gate PASS, LUT 49,597, FF 52,400, SLICE 15,680, WNS +0.189 ns, WHS +0.014 ns, complete route. No new route is required by the round-3 assignment for comment-only RTL changes, and none is claimed. Source evidence is the author's evidence; there is no manager source bank at d30a208d.

`receipts/hosted-observation.tsv` records an exact-head snapshot. At observation, long shards and several fast jobs were queued/running. Executed successes included the selector, lint, behavior, no-git docs and wire-accountability jobs. The physical gPTP job was **skipped**. This snapshot is not final hosted acceptance; no skipped physical context is execution evidence. No hosted or local replica acceptance verdict is issued here.

This round executed read-only recipe/receipt/logic-identity checks and a complete checkout integrity audit. The prescribed simulator identity was verified, but no new simulation build or mutation campaign was needed to falsify the shape claim. No full banks, hardware, Docker/local replica orchestration, privileged operations, source fixes, commits, pushes, GitHub writes or sub-agents were used.

Final integrity: 1,422 parent blobs plus all four required submodule populations and the additional populated lwSRP submodule match raw commit bytes, modes and index. Required gitlinks match their checked-out revisions. The external submodule remains uninitialized and unchanged. Parent status is clean; no tracked-byte restoration was needed. See `receipts/checkout-integrity.log`.

Portable reproduction, with SOURCE_ROOT at the stated head and PACKET at this directory:

```sh
python3 "$PACKET/scripts/audit_public.py" "$PACKET"
python3 "$PACKET/scripts/spot_checks.py" "$SOURCE_ROOT" "$PACKET"
python3 "$PACKET/scripts/verify_checkout.py" "$SOURCE_ROOT"
```

These commands are read-only against the source and download only published author execution receipts. `MANIFEST.sha256` lists publication files relative to this packet. Scratch and unlisted API working files are excluded.

## Pending manager duties

Obtain and publish the shipping-shape fix/evidence, then arrange re-review of the corrected exact head. Complete both independent reviews and the lens ledger, hosted/local-replica acceptance, and the full current-dev candidate validation. The supplied live dev is `e26f1816e456dc8027924bc2e5d327a8aa6e46db`, distinct from source base `e9cbb676`; the manager's merge-turn builder/native receipts must identify that candidate when published. This source review does not validate the composition.

Physical calibration is NOT RUN. Field skips, simulation and routing are not hardware proof. Merge authorization, post-merge containment, authoritative documentation and issue/project completion remain with the manager/maintainer. This report authorizes no merge.

R664-3 FINISHED
