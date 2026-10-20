[R664] POSITIVE - exact head f3fef856dbf7f8e559fa9066f6fc9af1ea091c9d

Round R664-4, external independent review of PR #767, issues #761 and #762. Tree `c1c7c13bd84fa4d6544783ab82bfe09fa7483c6a`.

All five lenses are CLEAN. R663-3-F1 and R664-3-F1 are resolved: the committed `[762-DP]` case now runs on the AX7101 1x1 TDM8 dynmap elaboration, with the three declared verification substitutes. The published clean run passes; both assigned wiring mutants fail exactly their named checks on that elaboration. No BLOCKER, MAJOR or MINOR remains from this review. Residues and optional suggestions below do not authorize changes to measurements or test expectations.

## Scope and independence

Reconstructed the contract from AGENTS.md, CONTRIBUTING.md, docs/README.md, issue bodies and public decisions, requirements and interface authorities, then the full-range change inventory and relevant implementation, the two-commit delta, and published execution receipts. The normative anchors are IEEE 1722-2016 4.4.4.3/10.4.3; Milan v1.2 5.3.8.7, 5.4.2.19/20, 5.3.8.10 Table 5.6 and 5.4.2.25 Table 5.16; REQUIREMENTS.md verification clauses; REGISTER_MAP.md:873; MILAN_COMPLIANCE_MATRIX.md:131; and the architecture/integration contracts. No new interpretation of the standards is introduced this round.

Public scope: [original assignment](https://github.com/kebag-logic/milan-fpga/issues/761#issuecomment-6256482625), [stopped-silence ruling](https://github.com/kebag-logic/milan-fpga/issues/762#issuecomment-6260976223), [stopped-gap extension](https://github.com/kebag-logic/milan-fpga/issues/762#issuecomment-6265746720), and [round-4 assignment](https://github.com/kebag-logic/milan-fpga/pull/767#issuecomment-6283915359).

The full source range is `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f..f3fef856dbf7f8e559fa9066f6fc9af1ea091c9d`. The reviewed delta is `d30a208d44d5868cc356e6a8b7abc89b062ca9bd..f3fef856dbf7f8e559fa9066f6fc9af1ea091c9d`: commits `16358b62734706dd7adf8bb07e72c7f973f36abd` and `f3fef856dbf7f8e559fa9066f6fc9af1ea091c9d`, changing only `sim_nxn.cpp`, `dynmap_probes.vlt` and the suite README. RTL, configuration, build recipes, receiver harnesses and restart harnesses are unchanged from round 3.

My independent verdict and five-lens ledger were written before opening prior public review bodies. I then reconciled all six prior review comments; there were no formal review bodies or inline findings. No private author material, handoff file, other reviewer's local packet, source fix, GitHub write or other-checkout edit was used. The initial skeleton has been replaced.

## Acceptance and execution evidence

Evidence source: [public commit 55c754698d494aaa17cf76f96229f9822c123c3a](https://github.com/kebag-logic/milan-fpga/tree/55c754698d494aaa17cf76f96229f9822c123c3a/review-evidence/761-r1), `author-r4/receipts/`. All **860 author-r4 receipt files** match their manifest's published SHA-256 values. This proves published-byte integrity. The commit API reports `verified=false`, reason `unsigned`; no detached signature was identified in the packet inventory. No signed execution attestation is claimed.

`sim_nxn.cpp:3036` invokes the new function at `:4572`. After the dynamic-map cases, it resets the datapath, starts the restore walk, binds input 0 over ACMP, runs the existing discard checks, then calls the unchanged interruption oracle at `:6735`. Reset does not clear the cumulative harness failure tally, so earlier failures cannot be hidden.

`Makefile:243,325` use the same AX1x1 shape and stream/audio/prune arguments. `dynmap_probes.vlt:24` exposes elaborated constants; the harness reads them rather than printing assumed values. Actual build commands name `endstation_ax7101_1x1_tdm8` and `NSTREAMS_TB=1`. Configuration authorities: `configs/endstation_ax7101_1x1_tdm8.yaml`, its generated shape/argv, `sw/litex/milan_soc.py:952,1068,1098`, and `docs/integration/BUILDING.md:183`.

All four raw runs have the same 22 parameter values: N_STREAMS=1, source/sink totals=2, CRF sink index=1; eight wire channels/capture slots; TDM master; 32-bit slots at 48 kHz with 24.576 MHz audio clock; loopback enabled. MCSERVO/LTAP/MAAP/RXFILT/DPROBES=1; I2SPB/LPF=0. Nineteen values match the shipping definition. Three explicit substitutes remain:

| Parameter | Verification elaboration | Shipping definition |
|---|---:|---:|
| MILAN_CLK_FREQ_HZ | 100000000 | 50000000 |
| GPTP_PLANE_EN_P | 0 | 1 |
| AUDIO_IF_RENDER_SLOTS_P | 0 | 8 |

The parameter table was recomputed against this checkout and matches the public table byte-for-byte. Its script is a diagnostic table generator, not a fail-closed gate; the reviewer receipt checker separately asserts every expected value. This covers shipping stream/audio geometry with named substitutes, not a flashable product image or physical render proof.

| Public run | Build/run rc | Checks/failures | Observed outcome |
|---|---|---|---|
| clean | 0 / 0 | 199 / 0 | All 15 `[762-DP]` checks pass, including two shape checks |
| tie0 | 0 / 1 | 199 / 2 | Only stopped gap SI +0 and stopped silence SI +0 fail, each reading +1 |
| sink1, `[N_STREAMS:1]` | 0 / 1 | 199 / 2 | The same two failures; at N=1 this selects the CRF sink |
| bound-level | 0 / 1 | 199 / 1 | Only started gap SI +1 fails, reading +0 |

Each mutant diff changes only `.stopped_i` at `hdl/milan/milan_datapath.sv:6308`. Build receipts use `dynmap-build` with copied datapath source and identical shape arguments. The reviewer checker verifies parameters, 15 named checks, exact failure names and totals in the raw logs. No new simulation was needed to falsify a remaining unsupported claim.

Source-head suite receipts retain all broad legs: 1,981 / 1,983 / 3,765 / 1,981 checks, no failures; dynmap is 199, notify 423, crflic 416 and prune 33. The dynamic-map campaign reports 16/16 after its missing generated listener input was supplied. The failed first attempt and prerequisites are retained, not presented as a clean first run. Gate_50 reports 14/14 rc 0. The other static table has 80 of 82 commands at rc 0, with the same two disclosed environment-dependent selftest failures. Builder reports all gates pass except calibration gate 11 NOT RUN. These are author receipts, not reviewer reruns or a manager source bank.

The PR body accurately names the broad shapes, including retired Arty `obj_nxn4c`; both public wiring-mutant headers name their actual shapes. Status and Known limitations cite `d30a208d`. A direct snapshot confirms **63 successes and one skipped Physical gPTP job** there. At the single current-head snapshot: seven successes, one skipped physical job, nineteen running and fourteen queued. This is not completed hosted evidence at `f3fef856`.

## Applied lenses

[R664] PASS Conformance - `sim_nxn.cpp:4572,6735`; #762 rulings; config/generated argv; REGISTER_MAP.md:873 - stopped-gap/silence counts are exercised at the assigned N=1 geometry; START restores gap counting. Selected-CRF loss/gain behavior at `milan_datapath.sv:3247` is unchanged. Earlier protocol coverage carries forward.

[R664] PASS RTL - `git diff d30a208d..HEAD`; `milan_datapath.sv:6308`; `KL_avtp_rx_monitor_ctx.sv:903,1025,1069,1144`; `KL_crf_rx.sv:401,559`; `Makefile:243,325` - no RTL/interface change. Correct AAF slice excludes CRF. Exposing constants introduces no reset/CDC/width/timing dependency. Round-3 RTL coverage remains applicable.

[R664] PASS Robustness - `sim_nxn.cpp:2745,4572,6735`; four `r4-mutants/*.run.log` receipts - fresh reset after dynamic-map activity, bind/stop/start, live sequence-mismatch/unlock witnesses, relock and resumed counting. The guarded watchdog shortcut advances idle time to 97 ms; expiry/count propagation execute. Wrong-vector control tests the N=1 CRF-index distinction. Unit ordering/reset/rebind coverage is unchanged.

[R664] PASS Tests - `dynmap_probes.vlt:24`; `sim_nxn.cpp:3036,4572,6735`; mutation diffs/build commands/raw runs; `receipts/receipt-checks.txt` - constants are elaborated, counts do not rely on the implementation replica, assigned defects fail intended checks, clean passes. Existing broad legs remain scheduled. Receiver/restart controls are unchanged.

[R664] PASS Docs - `tb/verilator/milan_dp/README.md:82,778,1190`; PR body; wiring-mutant headers; shape table - geometry and substitutions are explicit; retired-shape and hosted-state corrections are present. New source comments state behavior/reason with #762 and check tags. No new bench-lane label, reviewer identity, round or issue-comment ID appears. Check tags are test names, not lane labels.

## Prior public findings

| Finding | Disposition at this head | Cause/evidence |
|---|---|---|
| R664-1-F1, MAJOR, Conformance/RTL/Robustness/Tests | Resolved; carried | Expiry capture/later-Unbind survival at ctx:903/1069/1144; exact `d > 0` oracle at `sim_lockstep.cpp:867`. No relevant delta. |
| R664-1-F2, MAJOR, all lenses | Resolved; carried | Public stopped-state rulings, both engine guards, documentation and decided cases remain aligned. |
| R663-1-F1, BLOCKER, Tests/Docs | Resolved; carried | `ci_case_receipts_selftest.py:174` retains inventory length +1; gate_50 reports 0/35 refusal over 34 cases. |
| R663-1-F2, MINOR, Conformance/Robustness/Docs | Resolved; carried | Both engines retain the same stopped silence/gap law and documentation. |
| R663-1-F3, MINOR, Tests/Docs | Resolved; carried | Independent exact boundary counts and paired consume-race control unchanged. |
| R663-2-F1, MINOR, Tests | Resolved in full | Integrated count oracle plus shipping geometry and wiring controls meet its remaining requirement. |
| R663-2-F2, RESIDUE, Docs | Resolved | Both port comments explicitly name silence and sequence gaps. |
| R663-2-F3 and R664-2-R1, RESIDUE, Docs | Resolved | Current PR roles/status distinguish published head and historical handoffs; no current-head unpushed claim. |
| R663-3-F1 and R664-3-F1, MINOR, Conformance/Robustness/Tests/Docs | Resolved | N=1 geometry, parameter comparison, clean control, tie-off/CRF-vector failures, corrected PR/headers. |
| R663-3-R1, RESIDUE, Docs | Resolved | Both status references cite d30a208d, Physical gPTP explicitly skipped; snapshot confirms it. |
| R663-1-S1, R663-2-S1, R664-2-S2, R663-3-S1 | Retained, optional | Details below; no relevant implementation change. |

## Residues and optional suggestions

**R664-4-R1 | RESIDUE | Docs**

- Artifact: `tb/verilator/milan_dp/Makefile:319`.
- Authority/evidence: Comment says dynmap exits immediately after `[DYNMAP]`; `sim_nxn.cpp:3036` now runs fresh-boot `[762-DP]` first.
- Impact: stale navigation wording only; scheduling, checks and verdicts are correct.
- Exact outcome: replace “exiting right after it (DYNMAP_DEFAULT_TB)” with “followed by a fresh-boot [762-DP] check of #762 before the leg exits (DYNMAP_DEFAULT_TB)”.
- Verification: comment agrees with dynmap branch and README; no behavior change.

**R664-4-R2 | RESIDUE | Docs; existing wording carried for cleanup**

- Artifacts: `tb/verilator/milan_dp/README.md:76`; `Makefile:674`.
- Authority/evidence: BUILDING.md identifies Arty as retired. The new README and recipe explicitly retain three substitutes. Old wording says “shipping Arty”, “byte for byte” shipping argv and “only combination” reaching a board.
- Impact: contradictory legacy prose; round-4 measurements/acceptance claims are accurate and unaffected.
- Exact outcome: change the README row to “the retired Arty shape (framer width differs from shadow reset)”. Replace the Makefile comment with “AX7101 1x1 TDM8 verification geometry: one stream, eight wire channels, TDM8 master, loopback enabled, I2S playback and LPF pruned. This recipe uses 100 MHz fabric, gPTP option OFF and no render lane.” Remove its byte-for-byte/only-combination assertion.
- Verification: prose agrees with the parameter table; no parameter/generated-output changes. The pre-existing executable `CASE_OPTIONS_nxn4c` banner at Makefile:571 also says “shipping Arty”; record that unchanged label for separate relabelling without altering its case or tally. It is not evidence that the retired shape ships.

**R664-4-S1 | SUGGESTION | Tests, Docs**

- Artifact: `tb/verilator/milan_dp/Makefile` target `dynmap-mutants`; `r4-dynmap-mutants/prerequisites.txt`, first-run receipt.
- Authority/evidence: Its listener clean control needs generated inputs from another suite; initial execution failed without them, then passed after preparation. Current PR commands include preparation.
- Impact: standalone target reproducibility is less reliable on fresh checkouts; no unaccounted failure remains in the successful campaign.
- Optional outcome: make the target create prerequisites, or document them adjacent to it.
- Verification: fresh disposable checkout reaches clean control without manual prerequisite discovery and completes the campaign.

Retained optional findings:

| ID / severity / all lenses | Artifact and evidence | Impact; optional outcome; verification |
|---|---|---|
| R663-1-S1 / SUGGESTION / Tests | `milan_dp_mclk/sim_mclk.cpp:887`, `milan_datapath.sv:3247`; source gate statically pinned | Add zero-restart checks for CRF relock with INTERNAL/AAF selected; ungated gain-edge plant fails, clean passes. |
| R663-2-S1 / SUGGESTION / Robustness, Tests | `crf_rx/sim_main.cpp:1635`; stopped silence covered, no new timeout-edge sweep | Optionally grade STOP/START before/on/after timeout; delayed stopped-state sampling fails the intended boundary check. |
| R664-2-S2 / SUGGESTION / Tests, Docs | `crf_rx/mutants.py:44,72`, `sim_main.cpp:1723`; only two stopped-gap plants paired by built-in driver | Preserve five earlier paired unit controls too; until then qualify “every #762 mutant” as “both stopped-gap mutants”. Clean passes; seven paired plants fail their count checks. |
| R663-3-S1 / SUGGESTION / Tests, Robustness | `milan_dp/sim_nxn.cpp:6735`; integrated checks address input 0 | On N>=2 optionally stop input 1 with input 0 started; replicated-bit-0 wiring fails input-1 check. Cannot occur at shipping N=1. |

## Reviewer-owned ledger

Round-3 clean RTL/dependency coverage carries from `d30a208d44d5868cc356e6a8b7abc89b062ca9bd`. Unchanged engine law, boundaries and normative documents carry round-2 coverage from `eef90b4238b6c19b679b44adc6f09362809be153`. Four lenses left unclean by the shipping-shape finding are covered anew here.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | scope; sim_nxn.cpp:4572,6735; config/argv; REGISTER_MAP.md:873 | R664-4; unchanged law carried from R664-2 through R664-3 | f3fef856dbf7f8e559fa9066f6fc9af1ea091c9d |
| RTL | CLEAN | three-file delta; datapath:3247,6308; ctx:903,1025,1069,1144; CRF:401,559; Makefile:243,325 | R664-3 carried; R664-4 confirms unchanged implementation/dependencies | f3fef856dbf7f8e559fa9066f6fc9af1ea091c9d |
| Robustness | CLEAN | fresh boot/count case; CRF sink index 1; raw mutation runs; boundary oracles | R664-4; unchanged unit coverage carried | f3fef856dbf7f8e559fa9066f6fc9af1ea091c9d |
| Tests | CLEAN | constant probes; build commands; mutation failures; all-leg/campaign receipts | R664-4 | f3fef856dbf7f8e559fa9066f6fc9af1ea091c9d |
| Docs | CLEAN | README; PR body; shape table; mutant headers; prior disposition | R664-4; wording residues recorded separately | f3fef856dbf7f8e559fa9066f6fc9af1ea091c9d |

## Reproduction, integrity and limits

From the assigned checkout, with the evidence commit fetched:

```sh
python3 "$PACKET/scripts/verify_evidence.py" "$PACKET"
python3 "$PACKET/scripts/check_receipts.py" "$PACKET"
python3 "$PACKET/scripts/verify_checkout.py" "$SOURCE_ROOT"
```

The receipt checker uses downloaded public receipts in packet scratch and retained check-run snapshots. `receipts/receipt-checks.txt` records its result. Selected raw author runs/diffs and explicitly identified build-command/tail extracts accompany this report. They are inspected execution receipts, not freshly executed simulation.

Integrity passes for 1,422 tracked source blobs, raw bytes/modes, complete index, six source gitlinks and five required initialized submodule populations (1,072 more blobs). The optional external submodule is uninitialized; its source/index gitlink is verified. HEAD/tree match the assignment. No source mutation required restoration. Disposable material is confined to packet scratch; only manifest-listed files and REPORT.md are publication candidates.

No simulation/compiler executable was invoked, so no simulator-identity claim is made for reviewer execution. No full parent/processor/gPTP/synthesis/builder bank, host replica, hardware action, commit, push or merge was performed. No manager source bank runs at this exact head; none is claimed or inferred. Physical calibration remains NOT RUN. Field skips, simulation, routing and skipped physical jobs are not hardware proof.

## Pending manager duties

Publish report/manifest-listed receipts, carry residues and optional suggestions, complete independent review, and accept hosted/local-replica evidence at the final exact head. Hosted completion was pending at the captured snapshot.

Build and validate the final current-dev candidate, including builder/native banks, and link receipts on the PR. Source base `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f` differs from supplied live dev `e26f1816e456dc8027924bc2e5d327a8aa6e46db`; this source review does not validate their composition. Explicit merge authorization, post-merge containment, documentation and issue/project closure remain required. This verdict is not merge authorization.

R664-4 FINISHED
