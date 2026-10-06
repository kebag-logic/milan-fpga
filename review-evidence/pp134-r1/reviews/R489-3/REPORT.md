[R489] POSITIVE - exact head ffc3a8e5733202384e55ea9094569cca86b78261

External independent review of issue #134 / PR #160, round R489-3.
Tree: `a7c1bce09cefceda944558258f6b38cfba7ac7ed`.
Source base: `ead8036035affd53ef4b29979190f2f4f67084c0`.
[Public review start](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/160#issuecomment-6008707578).

All five lenses are CLEAN. No open BLOCKER, MAJOR, MINOR or RESIDUE remains.
Both round-1 mandatory findings and both round-2 mandatory findings are resolved.
Four suggestions remain nonblocking. This verdict covers the named source head;
the manager owns acceptance of the final current-dev merge candidate.

**Reconstruction**

The supplied instruction reference was read first. No repository or applicable
ancestor `AGENTS.md` or `CONTRIBUTING.md` was present. Reading followed
`docs/README.md`, root `README.md`, frozen acceptance and public scope decisions,
linked requirements/interfaces, the requested diff and history, then public evidence.
The independent verdict and five-lens ledger were written before reading earlier
review reports (`receipts/independent-verdict.txt`). Public findings were then
reconciled. Separate review and inline-comment endpoints were empty.

The [issue](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/134)
requires both own and peer LeaveAll, retention until expiry, one stop, killed mutants,
LeaveTime measurement and clause documentation. The
[expiry ruling](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/134#issuecomment-5990549074)
adds both RTL planes, expiry-first composition, all received events, k=0..400,
the original-order mutant, current clock count and the 40-LUT/40-FF bar. The
[diagnostic ruling](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/134#issuecomment-5994864535)
requires both missing arguments, planting checks, corrected-base record equality
and the main `21c6f709` merge. The
[consumer ruling](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/134#issuecomment-5995957938)
explains the additional notification bench patch at the historical parent base. The
[round-4 ruling](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/134#issuecomment-6001384633)
requires corrected mutation records, exact bank identities and a subsequent main merge.

Authorities examined include parent #608's public ruling, parent #639's preserved
timer interface, the public shipping-area recipe, REQ-SRP-001/-005, F01.4 delta 13,
F08.1 T-MRP-LEAVE, SRP sections 6.3–6.5, interfaces section 4.6 and the streaming
counter ownership row, and the timer service's one-clock expiry output.

The requested diff includes inherited mainline changes. The issue-specific delta
against main `e6a759de` is 24 files: registrar ordering, tests/mutants/docs and two
diagnostic arguments. Inherited notification, interface, figure/ID-gate and test
changes were examined separately. Both merges have two parents and reproduce the
automatic merge tree exactly (`receipts/identity-and-merges.txt`):

| Merge | Required main parent | Recomputed and committed tree |
|---|---|---|
| `9050c4bb` | `21c6f7096ac80007f723de59c6f717f55bd34cfc` | `3bcc8532549ea69139323a863049022d10f799c1` |
| `ffc3a8e5` | `e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8` | `a7c1bce09cefceda944558258f6b38cfba7ac7ed` |

**Reviewer-executed evidence**

The scoped simulator identified itself as version 5.050 before use. All builds and
probes ran under packet `scratch/`, with foreground orchestration waiting for every
child. Drivers received explicit job counts; make used `-j16`, with each simulator
build capped at two compiler workers. The maximum simultaneous allocation was twelve
compiler workers. Recorded memory peak was 5,381,255,168 bytes, below the 12-GiB cap;
no OOM event occurred.

| Run | Result | Receipt |
|---|---|---|
| Complete default integrated SRP executable | 8,656/8,656; 210,547,557 clocks; 6,416 CLOSED collision cases, zero STUCK | `receipts/focused/top-default.log` |
| Stream-FSM executable | 1,347/1,347, including 128 SC1 combinations | `receipts/focused/fsm-default.log` |
| Independent received-event matrix | 2,048/2,048: both planes/aging causes, all eight indices, old/new variants, matching/nonmatching packets and all eight event forms | `receipts/matrix.log`; `scripts/collision_matrix.cpp` |
| Integrated storage shapes | 15/15 at 1x1, 2x2, 3x5 and 9x9, clean and under each original fault | `receipts/focused/*-storage.log` |
| FSM walk shapes | 35, 46, 67 and 123 passing checks | `receipts/focused/fsm-default-walk.log` |
| Inherited notification composition suite | 45/45, including round-boundary and spacing cases | `receipts/notify-composition.log` |
| Mutation planting | 449/449: 283 patches, 110 D3 exact-edit controls, 56 notification controls | `receipts/planting.json`, `planting.log` |
| Focused documentation checks | All pass: ID self-test 30, figure self-test 17, 1,174 links, 115 requirements, 94 module rows/zero untested, 28 parameters, staleness | `receipts/docs-checks.log` |

Every executable receipt has a return-code file. Positive controls and supplemental
runs returned zero. Fault returns below are make's expected failure status 2, with
completed assertion tallies. No build failure, timeout or missing tally counts as a kill.

| Planted fault | Scope | Failing assertions |
|---|---|---|
| `lv-second-lv-ends` | Complete default integrated executable | 16: S1 ×8, S2 ×8 |
| `lv-never-ends` | Complete default integrated executable | 3,032: S2 ×8, S3 ×8, SC2 ×3,016 |
| `lv-expiry-masked` | Integrated collision sweep | 16 SC2, one per combination |
| `lv-expiry-masked` | FSM suite | 16 SC1 |
| `lv-expiry-last` | FSM suite | 48 SC1 |
| `lv-expiry-dropped` | FSM suite | 86: 80 SC1 plus six older checks |
| `lv-sweep-misses-collision` | Integrated collision sweep | 16 SC3; closure checks remain green |

The original-order patch restores both entire FSM files byte-for-byte to source-base
blobs (`receipts/reverse-patch-identity.json`). It does not approximate the old defect.

**Five independent assessments**

Conformance — CLEAN. Table 10-4, with delta 13 confined to IN/rLv, gives this
expiry-first composition when reception meets expiry in LV:

| Same-clock input after expiry | Final state | Publication/timer result |
|---|---|---|
| rLv | MT | Registration closes once |
| Received or own LeaveAll | MT | Closes once; no replacement leave ARM |
| rIn or rMt | MT | No registration; closes once |
| rNew, rJoinIn or rJoinMt | IN | Received value retained; obsolete timer canceled; no transient withdrawal |

Both planes implement these outcomes. SC1 checks all forms; the independent matrix
also varies every index, type/value changes and unmatched identities. S1–S3 measure
5,000 ms in all eight own/peer cases, within Table 4.3's recorded 4,500–7,500-ms range,
with one ACTIVE fall and no new rise. Artifacts: `docs/architecture/08_timing.md:40`,
`docs/architecture/10_srp_engine.md:548`, `tb/srp_top/sim_main.cpp:799` and
`tb/srp_stream_fsms/sim_main.cpp:1072`. Renewal publishes the composed final state,
without an intermediate Lv/Join pair, as section 6.5 and the scope ruling specify.

RTL — CLEAN. At `hdl/srp/KL_srp_talker_fsm.sv:729` and
`hdl/srp/KL_srp_listener_fsm.sv:769`, expiry precedes non-registering Lv reception.
New/Join keep the first branch, producing IN and cancellation. The listener's
`ind_unreg_w` at line 449 excludes matching renewal, so applicant withdrawal,
published state and indication agree. Type/failure-change behavior and refreshed
latency/failure payloads pass the independent matrix. The latency-change strobe
logic was inspected and remains unchanged. The pending-ARM guard still excludes
obsolete expiry. No port, parameter, register or timer handshake was added.
Inherited notification logic was inspected and its composition suite passed.

Robustness — CLEAN. The 401-offset sweeps cover both causes/planes, Ready/ReadyFailed
and boundary indices. SC3 requires exactly one decoded Lv at each calibrated expiry
clock; the shifted-stimulus fault proves a sweep missing that clock is rejected.
Snapshots restore DUT and driver state while total executed clocks remain monotonic.
The original-order fault exposes lost expiry on both planes. The independent matrix
extends checks to every index, changed payload/type and nonmatching traffic. S1–S3
retain repeated withdrawal and post-expiry observation. The 300-million-clock budget
has measured margin over 210,547,557 clocks.

Tests — CLEAN. Default executables include S1–S3 and SC1–SC3, and the campaign requires
their coverage. All focused controls fail the intended assertions. Complete original-
fault runs, including storage shapes, reproduce the corrected README. At
`tb/pp_top/d3_phases.hpp:2964` and `:2994`, the final `%d` receives the `int` constant
`D3_RECORDS`: four/four and six/six conversions/arguments. Neither old diagnostic
suffix occurs in any patch or either exact-edit table; all 449 arms plant.
`receipts/format-audit.json` records this. Eleven-receipt runtime equality remains
public reported evidence, not a local re-execution.

Docs — CLEAN. Section 10 §6.5, both suite READMEs and harness comments agree on
expiry-first composition and continuous renewal publication. The measured clock count
matches `tb/srp_top/sim_main.cpp:368`. Section 6.5 references T-MRP-LEAVE/F08.1 without
duplicating the numeric authority; the suite README retains acceptance's measurements.
Inherited interface changes were compared with landed byte, host and device faces.
All three changed waveform exports were rendered and visually inspected. Focused
documentation gates and the base-to-head whitespace check passed. Evidence is scoped
to its actual head below.

**Prior findings at this head**

Sources: [R488-1](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/160#issuecomment-5990539778),
[R489-1](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/160#issuecomment-5990392302),
[R488-2](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/160#issuecomment-6001378167)
and [R489-2](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/160#issuecomment-6000718766).
Their verdicts were read after the independent checkpoint.

| ID, severity, disposition | All attributable lenses | Location / authority | Impact / required outcome | Verification at this head |
|---|---|---|---|---|
| R488-1-F1 — MAJOR, RESOLVED | Conformance, RTL, Robustness, Docs; remedial Tests examined | Both registrar branches above; Table 10-4; ruling 5990549074 | Coincident Lv could lose expiry indefinitely. Require both planes to consume expiry and document the result | All 6,416 offsets close; 128 SC1 and 2,048 independent cases pass; original-order fault fails 16 integrated and 16 FSM cases |
| R488-1-F2 — MINOR, RESOLVED | Tests, Docs | `tb/srp_top/sim_main.cpp:368`; full execution receipt | Stale measured budget figure. Require current count | Comment and execution both give 210,547,557 |
| R488-2-F1 — MINOR, RESOLVED | Tests, Docs | `tb/srp_top/README.md:539`; acceptance 1; round-4 ruling | Mutation record excluded other default checks. Require complete-run results | Early closure: 16 S1/S2; never ends: 16 S2/S3 plus 3,016 SC2; four storage shapes pass under each fault |
| R488-2-F2 — MINOR, RESOLVED | Tests, Docs | PR body bank table and tree identities; round-4 ruling | Unnamed intermediate baseline obscured 24 checks. Require named trees and reconciling totals | Corrected main tree `579e3c59…` and intermediate `ad2af42e…` reconstructed exactly. All 33 rows sum to 1,021,640 and 1,028,224; delta 6,584 = 24 + 128 + 6,416 + 16. `receipts/bank-reconciliation.json` |
| R489-1-S3 / R488-1-S-1 — SUGGESTION, RESOLVED | Docs | `docs/architecture/10_srp_engine.md:558`; single-source rule | Avoid duplicate timing authority | Paragraph cites T-MRP-LEAVE/F08.1 without repeating the range |
| R489-1-S1 — SUGGESTION, RETAINED | Tests, Robustness | `tb/srp_top/sim_main.cpp:843`, `:849`, `:853`; prior no-Lv finding and current controls | Group S alone does not count both decoded withdrawals. Optional: count both target deliveries directly | Missing delivery prevents the original mutants from being killed; both are killed here. If strengthened, deleting either required delivery should fail group S itself |
| R489-1-S2 — SUGGESTION, RETAINED | Docs | `tb/srp_top/README.md:521`, `sim_main.cpp:357`; interfaces `:541` | ACTIVE edges proxy integrator-owned counters. Optional exact wording: “counts ACTIVE edges; an integrator whose streaming level follows this licence counts the corresponding STREAM_START/STREAM_STOP edges” | Read-through against counter ownership. This review measures ACTIVE, not a physical stream or parent counter |
| R488-1-S-2 — SUGGESTION, RETAINED | Tests, Docs | `tb/srp_top/sim_main.cpp:839`, `:853`; README S1 | Peer premise observes any LeaveAll lane; separate LV check and absent own sLA make the combined premise sound. Optional: observe Listener lane explicitly or describe the combined premise | Static check of conjuncts; a stronger premise should reject wrong-lane-only stimulus |
| R488-2-S1 — SUGGESTION, RETAINED | Conformance, Docs | `docs/architecture/10_srp_engine.md:566`; F01.4; expiry-first ruling | Final publication suppresses intermediate Lv/Join indications. Optional: add an F01.4 implementation note linking section 6.5 | Section 6.5 and README state the choice; direct checks verify continuous renewal and preserved type/value indications |

No new mandatory finding or RESIDUE is recorded. These four suggestions leave the
lenses clean; no item is assigned to the residue checklist.

**Public evidence and limits**

The immutable [pp134-r1 bundle](https://github.com/kebag-logic/milan-fpga/tree/7aecfd0bad90ea2d6e8306d45faf18b0eac9dfa6/review-evidence/pp134-r1)
contains the historical `5ab43bd9` handoff, PR body and four patches. All six published
hashes match (`receipts/public-manifest-verification.json`). It contains no raw
`ffc3a8e5` bank receipts. Later
[round-3b evidence](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/134#issuecomment-6000454088)
reports corrected eleven-receipt equality, twelve campaigns and donor/consumer gates.
[Round-4 evidence](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/134#issuecomment-6001904516)
and the [PR body](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/160)
identify the corrected bank trees. Their arithmetic and tree identities are checked
here; the full banks were not rerun.

Reported shipping 1x1 OOC is 23,161→23,145 LUT and 19,783→19,780 FF: **−16 LUT/−3 FF**,
within the 40/40 bar, with unchanged RAM/DSP and matched parameters, images and 50-MHz
clock. The public recipe distinguishes this shipping-clock endpoint from the separate
10-ns target. This is retained round-3b evidence, carried through the README-only
round-4 change. This reviewer did not rerun OOC or claim a new area measurement of
the inherited #158 merge at `ffc3a8e5`.

The assignment states that the manager's full source static/builder and native banks
passed at this exact head. Captured issue/PR material has scope decisions, review
starts and reported validation, without separate raw exact-head manager bank receipts.
Acceptance remains manager-owned. No processor-wide, parent, gPTP, builder or synthesis
bank was started by this review.

At 2026-10-06 03:34:43 UTC, exact-head hosted runs
[37408875830](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/37408875830)
and [37408871633](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/37408871633)
had executed successful documentation and portability jobs. Both suite jobs were
running; later campaigns were pending. Cached simulator build steps were skipped;
that is not test execution. No pending or skipped context is credited as passed.
Job/step metadata is preserved in `receipts/hosted-*.json`.

No full standards PDFs were available in the donor. Clause assessment uses frozen
public rulings, repository requirements and recorded table interpretation, not an
independent audit of the complete specifications. Physical calibration is **NOT RUN**.
Field skips are not hardware proof. No hardware, physical stream stop or integrating
system's actual streaming counter was measured.

Current consumer dev is `28f9666feab2b2ba287643c63ed3a16b1e0bb863`, with **only the #148
bench patch**, as the current assignment specifies. Historical five-patch runs are
not relabeled as that candidate. Public gitlinks at that dev are processor `ead80360…`,
gPTP `5dce647a…`, external `efeb541a…`, and `third_party/verilog-axis` `48ff7a7e…`,
recorded in the consumer receipts. No consumer checkout or gitlink was changed here.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen acceptance/rulings; Table 10-4/delta 13; REQ-SRP/F08.1; S/SC and independent matrix; correctly scoped area evidence | R489-3 | ffc3a8e5733202384e55ea9094569cca86b78261 |
| RTL | CLEAN | Both registrar chains and indications; timer strobe/ARM guard; inherited notification logic/suite; both merge-tree identities | R489-3 | ffc3a8e5733202384e55ea9094569cca86b78261 |
| Robustness | CLEAN | Both causes/planes, every event/index, changed/mismatched values, packet timing, collision-presence control, original-order fault, replay accounting | R489-3 | ffc3a8e5733202384e55ea9094569cca86b78261 |
| Tests | CLEAN | 8,656 integrated, 1,347 FSM and 2,048 independent cases; shapes; seven fault/suite combinations; 449 planting trials; D3 arguments; bank arithmetic | R489-3 | ffc3a8e5733202384e55ea9094569cca86b78261 |
| Docs | CLEAN | Section 10 §6.5, suite READMEs/comments, measured figures, corrected fault records, exact bank identities, inherited interfaces/rendered waveforms, documentation gates | R489-3 | ffc3a8e5733202384e55ea9094569cca86b78261 |

**Reproduction, integrity and manager duties**

Portable scripts are in `scripts/`. Run `run_focused.py` with `--source`, `--packet`,
`--simulator` and `--jobs 4`; run `check_planting.py SOURCE PACKET`; then run
`run_shapes.py --packet PACKET --jobs 4` and `run_supplemental.py --source SOURCE
--packet PACKET --jobs 3`. The last two can run concurrently. `verify_tree.py SOURCE`
checks head, raw blobs, modes, index and required gitlinks. Direct supplemental
commands and their equivalent portable reproducer both passed.

Final integrity: all **562 tracked entries** match HEAD bytes and modes, the stage-zero
index matches, and status is empty including ignored/untracked files. This donor has
**zero submodule gitlinks**. No tracked source was edited; no restoration patch was
needed. No private author material, private reviewer packet, management checkout,
other checkout, shared install, remote write, source fix, commit, push, merge or
delegated review was used. Merge-tree calculations created no commit and changed
neither checkout nor index.

`MANIFEST.sha256` lists publishable scripts and receipts with packet-relative paths;
scratch is excluded. Execution logs retain diagnostics and assertions. Local simulator
installation paths are replaced with a neutral root; original/published hashes are
in `receipts/path-redactions.json`, with originals in unpublished scratch.

The manager must accept reported source banks and current consumer evidence, complete
hosted/act acceptance, obtain the second independent positive review, and build and
validate the final current-dev candidate at the merge turn. Its source base is
`ead8036035affd53ef4b29979190f2f4f67084c0`, live dev
`28f9666feab2b2ba287643c63ed3a16b1e0bb863`; that candidate is distinct from source
validation. Retained suggestions may be carried at the manager's discretion.
Publication remains with the manager.

R489-3 FINISHED
