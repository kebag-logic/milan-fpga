[R491] POSITIVE - exact head 5747a8cb99495cb0331658cdd499b9c44e3eda91

Round R491-2, external independent review of issue #658 / PR #670.
Tree: `d1d63caa2490c515624194cb5711ddb76c1601dd`.
Source base: `e617275074e370cec342af99b929e2588fc8d43f`.

All five lenses are CLEAN at this head. The seven new guard removals are
KILLED by their named assertions. The clean leg passes 162 checks. No open
BLOCKER, MAJOR, MINOR or RESIDUE remains from the reconciled findings.
Two earlier optional suggestions remain optional. This is a source-review
verdict; candidate-merge validation and deployment evidence remain separate.

## Reconstruction and scope

Reconstruction followed AGENTS.md and CONTRIBUTING.md, docs/README.md, the
issue body and public scope decisions, requirements and interfaces, then the
specified full diff and history. Prior public finding comments were consulted
after the independent pass over the diff. No private lane material, management
checkout, or separate reviewer packet was used. No source change or GitHub
write was made.

The [stage-2 decision](https://github.com/kebag-logic/milan-fpga/issues/658#issuecomment-5988843004)
supersedes the initial runtime adaptation request. Dynamic ports receive
identity defaults; restore clips them before AECP release. Normal format
narrowing remains BAD_ARGUMENTS when it would orphan a mapping. Map
persistence belongs to the saved-state work. The
[round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/658#issuecomment-5997263077)
requires guard-sensitive tests, corrected coverage/persistence prose, and the
dev merge.

Authorities applied: REQUIREMENTS.md sections 1, 3 and 8; Milan v1.2
5.4.2.7 and 5.4.2.26-28; IEEE 1722.1-2021 7.4.44-46 as allocated by the
repository; SAVED_STATE_MATERIALIZATION.md sections 1, 5.2 and 8.4;
ENDSTATION_BUILDER.md D7/D8; CHANNEL_MAP_64.md sections 5-6;
REGISTER_MAP.md 0x900; the pinned processor's edit-face and restore contracts.
No new interpretation of an external standards clause is proposed.

History confirms six round-2 commits plus merge `57155256f`, whose ordered
parents are `2e1606bab` and `510fae60`. The parent datapath RTL is byte-identical
to round 1. The dev merge advances the processor to
`ead8036035affd53ef4b29979190f2f4f67084c0`; its map edit interface and dynamic
format store remain compatible. The final commit confines new internal-state
guard probes to `DYNMAP_DEFAULT_TB`. Receipt: `source-provenance.json`.

## Prior finding dispositions

The public sources are [R490-1](https://github.com/kebag-logic/milan-fpga/pull/670#issuecomment-5997255034)
and [R491-1](https://github.com/kebag-logic/milan-fpga/pull/670#issuecomment-5997138134).

| Finding | Severity and lenses | Disposition at this head |
|---|---|---|
| R490-1 F1 | MINOR; Tests | RESOLVED. `sim_nxn.cpp:4298`, `:4338`, `:4392`, `:4454`, `:4490` stage the guards. Mutation definitions 5-11 each fail their named assertion. The two RAM-only exceptions are accepted with the bounded justification below. |
| R490-1 F2 | MINOR; Docs, Tests | RESOLVED. PR body now says the gPTP leg grades release and post-walk usability; `[DYNMAP]` grades refusal. `sim_ax1x1gptp.cpp:705`, `:720`, `:735` starts/completes restore before writing all eight capture keys. Payload checking depends on those loopback words; it supplies no in-window refusal proof. |
| R491-1 F1 | MINOR; Docs | RESOLVED. `SAVED_STATE_MATERIALIZATION.md:1216` contains the requested text exactly after line-wrap normalization. It distinguishes no boot-clip trigger, sticky live-map pending, unmaterialized map records in stages 1/2, and the future stage-3 writer. The pinned writer explicitly excludes channel maps at `KL_aecp_nvm_writer.sv:116`. |
| R490-1 R1 | RESIDUE; Docs | RESOLVED; split wording accepted. `CHANGELOG.md:55` says “The CSR map window refuses writes.” The next bullet says “That lasts until one sweep after the restore's terminal.” Together they preserve the requested refusal and duration. They contain six and nine words; the original combined sentence has thirteen. `check_doc_style.py:39` caps sentences at ten. |
| R490-1 R2 | RESIDUE; Docs | RESOLVED. `REGISTER_MAP.md:2160` contains the exact requested per-direction qualification, after line-wrap normalization. Static output directions are no longer said to hold the identity image. |

`receipts/text-corrections.json` records both exact-text comparisons and the
CHANGELOG counts. Documentation style and hygiene checks pass. No residue
checklist entry remains necessary for R1 or R2.

### Retained optional findings

**R491-1-S1 - SUGGESTION - RTL**

- Artifact: `hdl/milan/milan_datapath.sv:4358`, `:4550`; pinned
  `KL_aecp_engine.sv:456`, `:2352`.
- Authority/evidence: retain the earlier optional shipping-shape area
  specialization suggestion. The shipping cursor has eight keys. This
  round's held-sweep test demonstrates why an overlapping edit needs the
  wait; it does not measure an alternative specialized implementation.
- Impact: a possible area optimization remains unmeasured. No correctness
  defect is established by keeping the wait.
- Required outcome: none for this PR. If pursued, preserve arbitration on
  every shape where an edit can overlap the final sweep.
- Verification: isolated synthesis comparison plus queued-at-release,
  overlapping-edit and larger-shape checks before adopting a specialization.

**R490-1-S1 - SUGGESTION - Tests**

- Artifact: `tb/verilator/capture_coherence/sim_dp.cpp:20`, `:257`;
  `sim_nxn.cpp:4162`, `:4193`.
- Authority/evidence: the talker end-to-end check runs without starting
  restore; the boot writer remains active. `[DYNMAP]` separately grades the
  post-release capture RAM. Both limitations remain explicit.
- Impact: the two checks compose the evidence; one post-release talker run
  would present it more directly.
- Required outcome: none for this PR; optionally add that run later.
- Verification: decoded capture-slot-to-stream-channel identity after a real
  restore terminal, without a map command, with the empty-image control.

## Applied lenses

**[R491] PASS Conformance - `hdl/milan/milan_datapath.sv:4440`, `:4451`,
`:4467`, `:4519`, `:4761`, `:5018`; `receipts/clean.log`.**
Identity functions use the generated dynamic masks, port cluster bases and
counts, declared formats and ADD-compatible channel bounds. Both shipping
ports expose eight ordered identity records. The real saved-format restore
reads back `0205022001006000`, four input mappings and eight output mappings.
Normal 8-to-4 narrowing is refused while channels 4-7 remain mapped; REMOVE
permits it, and widening adds nothing. The boot clip does not create a live
map persistence event. The merged processor still judges restored formats on
supported bit 0 and leaves map persistence to the parent.

**[R491] PASS RTL - `hdl/milan/milan_datapath.sv:1256`, `:4358`,
`:4550`, `:4639`, `:4741`, `:6783`; `KL_chan_map_capture.sv:498`;
processor `KL_aecp_engine.sv:456`, `:2352`.**
The cursor uses the larger key count and restarts at zero on either terminal.
One final sweep plus the registered-write drain precedes CSR release.
Store writes and both RAM muxes share exclusion; phase 5 retains write-leg
priority. The processor stalls fallible edit phases and ignores wait after
commit reservation, consistent with a boot busy signal that cannot reassert
before reset. Bounds/casts, reset values and write latency were inspected.
No new clock crossing or leaf interface is introduced. Processor adoption
does not change this handshake; the additional name restore delays the
terminal while retaining ownership.

**[R491] PASS Robustness - `sim_nxn.cpp:4338`, `:4392`, `:4454`,
`:4490`; `milan_datapath.sv:4535`, `:4563`; processor
`protocol_processor_top.sv:2795`, `:2804`, `:2849`.**
Each direction receives one CSR commit at every offset -2 through +12 from
forced CLOSED. All offsets through +9 are refused in both representations;
+10 through +12 land in both. No split occurs. A rollback that invalidates
both formats on the CLOSED clock restores both stores and RAMs. The held
sweep delays the ADD response to clock 1190, beyond the 1000-clock hold,
and preserves its remapped capture word. Reset restarts each scenario.
Static inspection also covers no-start restore, static output directions,
nonphysical input keys and the generated 8x8 shape. Boundary staging is
explicit; it is not a real-controller timing or physical-fault claim.

**[R491] PASS Tests - `dynmap_mutants.py:132`, `:189`, `:213`;
`dynmap_probes.vlt:7`; `sim_nxn.cpp:4031`, `:4108`, `:4298`;
`Makefile:323`, `:509`; `receipts/campaign-summary.json`.**
The clean oracle grades protocol response contents, store/RAM consistency,
timing, and non-vacuity. Mutation patterns must match once. Every selected
mutant compiled successfully and returned a failing harness verdict with its
designated failed assertion; a compiler error or crash was not counted.
The callback defaults to absent outside the staged edit, and new narrow-width
probe readers are compiled only for the dedicated shape. Rebased map tests,
render T18 and capture-column checks were inspected against their previous
expectations; they clear or consume the identity defaults without relaxing
the subsequent tests. The full current source banks are supplied validation,
not a bank rerun by this reviewer.

**[R491] PASS Docs - `SAVED_STATE_MATERIALIZATION.md:192`, `:605`,
`:1211`; `ENDSTATION_BUILDER.md:624`; `CHANNEL_MAP_64.md:363`;
`REGISTER_MAP.md:2160`; `CHANGELOG.md:55`; `milan_dp/README.md:731`,
`:800`; PR #670 body.**
The documents distinguish power-on identity, restore clipping, normal
REMOVE-before-narrowing, CSR refusal, static directions and future map
materialization. Both required exact-text corrections match. The CHANGELOG
split is accepted. The README accurately limits its two RAM-site equivalence
claims to the shipping geometry, and the PR body correctly limits the gPTP
coverage claim. No new persistence or hardware-conformance claim is inferred.

## Executed guard campaign

Every row below built successfully. Each harness ran 162 checks.
Runtime logs and return codes are under `receipts/`; `campaign-summary.json`
also records build status and transcript hashes.

| Case | Result | Harness failures | Receipt |
|---|---|---:|---|
| Clean exact-head source | PASS, exit 0 | 0 | `clean.log` |
| 5: remove all four CSR hold sites | KILLED, exit 1 | 4 | `mutant-05.log` |
| 6: remove input-store hold | KILLED, exit 1 | 2 | `mutant-06.log` |
| 7: remove output-store hold | KILLED, exit 1 | 2 | `mutant-07.log` |
| 8: ignore CLOSED terminal | KILLED, exit 1 | 2 | `mutant-08.log` |
| 9: remove final sweep | KILLED, exit 1 | 6 | `mutant-09.log` |
| 10: remove drain clock | KILLED, exit 1 | 4 | `mutant-10.log` |
| 11: remove edit wait | KILLED, exit 1 | 2 | `mutant-11.log` |
| Remove capture-RAM hold alone | Equivalent result, exit 0 | 0 | `capture-ram-only.log` |
| Remove render-RAM hold alone | Equivalent result, exit 0 | 0 | `render-ram-only.log` |

The two last transcripts are byte-identical to the clean transcript.
Their equivalence rationale is also supported structurally: generated
`endstation_ax7101_1x1_tdm8/gen/adp_shape_defaults.svh:73`, `:84`, `:86`,
`:94` gives eight mapped physical input keys and eight dynamic output keys.
The boot writer supplies both registered write legs throughout the sweep and
drain; each RAM mux gives that leg priority over CSR. At reset/startup the
CSR strobe is reset and no CSR transaction can reach that initial gap.
Thus removing either extra RAM hold term changes no reachable write on this
shape. This does not establish equivalence for a direction with no dynamic
map, nonphysical input keys, or unequal key spaces. The README names these
limits. The assignment explicitly permits a reviewer-accepted explanation
for an ungraded arm; I accept this bounded explanation.

The seven runs use the committed mutation definitions directly. Definitions
5, 11, 9, 8 and 10 correspond to the previously surviving P1, P2, P3, P5 and
P9 behaviors respectively. I did not execute the other reviewer's script.

Other executed checks: documentation hygiene returned zero findings,
including its 23/23 scrub controls and 4/4 routing arms; documentation style
passed all 22 documents; the full raw diff passed `git diff --check`.
The simulator identity was verified as pinned 5.050 before use; its wrapper
digest is recorded separately. Reproduction is in `REPRODUCE.md`.

## Dev merge, area and evidence boundaries

The merge introduces the reviewed dev adoption, not another implementation
of the map stores. The two conflict resolutions retain both CHANGELOG entries
and combine the amended parent map-restore ownership with the clipped
identity target. The current pinned writer still never writes map records.

The published round-2 OOC comparison against dev `510fae60` is +139 LUT after
synthesis and +337 LUT after optimization. The touched-instance attribution
is +137 LUT: parent own logic +3, processor wrapper +71, capture map +63.
The remaining +200 is optimization movement in untouched instances. I accept
that attribution under the own-logic rule; the full measured +337 remains
the cost of this OOC result. It is not reduced to +137 for resource acceptance,
and this OOC comparison is not the routed candidate's resource-gate verdict.
No synthesis was rerun in this review. The previous optional specialization
suggestion does not become a requirement from these figures.

The [public REVIEW READY evidence](https://github.com/kebag-logic/milan-fpga/issues/658#issuecomment-6001889975)
reports the exact-head focused/suite checks and distinguishes other checks at
`2c24849b` with unchanged inputs. The assignment additionally supplies the
manager's successful full source static/builder and native banks at this
head. These are distinguished from this reviewer's focused execution.

The immutable [published packet](https://github.com/kebag-logic/milan-fpga/tree/d445cbd4d2dadfa01fbefc36bec82d9ffde5695f/review-evidence/658-r1)
is historical round-1 evidence: its clean leg has 142 checks and its mutation
summary has nine controls. I inspected only selected executable receipts and
the reset-image microbenchmark, not its handoffs or scratch material. Those
receipts support the earlier baseline; they are not represented as fresh
162-check or sixteen-control evidence. `public-evidence-index.json` records
their immutable blobs and hashes.

The exact-head hosted snapshot records successful executed lint, two Yosys
shards, behavior, wire-accountability and documentation-without-git jobs.
Several long jobs and documentation/elaboration were still in progress.
“Physical gPTP (nightly and manual)” was SKIPPED, not executed.
See `receipts/hosted-checks.json` for timestamped individual states.
Hosted acceptance remains with the manager; I did not poll it to completion.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen stage-2 ruling; identity/clip/verdict RTL; pinned restore judge; `clean.log` protocol pages | R491-2 | 5747a8cb99495cb0331658cdd499b9c44e3eda91 |
| RTL | CLEAN | `milan_datapath.sv:1256,4358,4550,4639,4741,6783`; capture RAM write edge; pinned edit-face contract; merge/provenance and area evidence | R491-2 | 5747a8cb99495cb0331658cdd499b9c44e3eda91 |
| Robustness | CLEAN | `sim_nxn.cpp:4338,4392,4454,4490`; CLOSED offsets, rollback edge, held edit; generated static/dynamic shape bounds | R491-2 | 5747a8cb99495cb0331658cdd499b9c44e3eda91 |
| Tests | CLEAN | `dynmap_mutants.py`, probe file, build/run wiring, rebase diffs; clean and seven killed controls; two RAM equivalence controls | R491-2 | 5747a8cb99495cb0331658cdd499b9c44e3eda91 |
| Docs | CLEAN | Design sections 1/5.2/8.4; D7/D8; channel/register docs; CHANGELOG; README; current PR body; exact-text/style/hygiene receipts | R491-2 | 5747a8cb99495cb0331658cdd499b9c44e3eda91 |

## Real limits and pending manager duties

- This round ran the clean focused leg, seven guard mutants and two additional
  equivalence controls. It did not rerun the original six mutation cases,
  full parent/processor/gPTP banks, builder bank, portability synthesis,
  physical-rate gPTP suite, area synthesis, hosted replica, or hardware.
- Forced format/CLOSED state and an artificially held sweep prove these
  boundary guards, not that a controller can produce those timings on the
  shipping device. Output narrowing remains unreachable through a command.
- Physical calibration is NOT RUN. Field campaign skips provide no hardware
  proof. Diagnostic gPTP loopback is not licensed streaming acceptance.
- The manager must form and validate the final candidate against current dev.
  The assignment names live dev `28f9666feab2b2ba287643c63ed3a16b1e0bb863`;
  the reviewed source head instead contains dev `510fae60`. Re-resolve live
  dev at the merge turn. This ledger covers the source head only.
- Complete exact-head hosted/local acceptance and the routed candidate's
  resource record, including the applicable baseline-update procedure.
  OOC movement in unchanged instances does not waive that procedure.
- Obtain the other independent final review, ensure no review remains in
  flight, and retain explicit maintainer merge authorization. After merge,
  perform the required containment/integrity checks before closing workflow
  state. The manager owns the post-flash power-on map read.
- Keep map materialization in its saved-state lane, and retest overlapping
  datapath changes such as #645 against the completed guard campaign.

Final integrity proof re-hashed all 1,014 parent blobs, their filesystem modes
and index records, and all required initialized submodule blobs/indexes:
processor `ead8036035affd53ef4b29979190f2f4f67084c0` (558), gPTP processor
`5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` (104), and stream library
`48ff7a7e2ef782cf778d47910cf85835c64b1bce` (214). All four parent gitlink
records are unchanged; the optional external submodule stayed uninitialized.
HEAD/tree match the assignment and porcelain is empty. All disposable work
remains under packet `scratch/`, excluded from publication. Publish only
`REPORT.md` and files listed by `MANIFEST.sha256`.

R491-2 FINISHED
