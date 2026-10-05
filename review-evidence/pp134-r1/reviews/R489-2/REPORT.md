[R489] POSITIVE - exact head 9050c4bbd25556929a0f24fb98258bc98e3bcfbe

External independent review of issue #134 / PR #160, round R489-2.
Tree: `3bcc8532549ea69139323a863049022d10f799c1`.
Source base: `ead8036035affd53ef4b29979190f2f4f67084c0`.
[Public review start](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/160#issuecomment-6000475277).

All five lenses are CLEAN. No open BLOCKER, MAJOR, MINOR or RESIDUE remains.
The prior same-clock expiry defect and stale measured-clock figure are resolved.
Three prior suggestions remain non-blocking, with their precise scope below.
This is an exact-source verdict; it does not approve an unbuilt current-dev candidate.

**Reconstruction and acceptance**

1. Read the supplied instruction reference, searched the clone and applicable ancestor
   instruction locations, then read `docs/README.md`, root `README.md` and `hdl/README.md`.
   This donor has no repository `AGENTS.md` or `CONTRIBUTING.md` and no submodules.
2. Read [issue #134](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/134)
   and its public manager scope decisions. The initial
   [assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/134#issuecomment-5988316116)
   requires own and peer LeaveAll, retained registration/licence until LeaveTime,
   exactly one stop, two planted faults, clause documentation and donor/consumer gates.
   The [expanded ruling](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/134#issuecomment-5990549074)
   authorizes a minimal RTL fix on both planes, expiry-first event composition, all
   relevant received-event pairs, the 0..400 collision sweep, a reverse-order mutant,
   retained S1-S3, a corrected measured-clock count and the 40-LUT/40-FF area bar.
   The [round-3 ruling](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/134#issuecomment-5994864535)
   adds the two missing D3 diagnostic arguments, record equality against a corrected
   base, mutation planting audit and merge of main `21c6f709`.
   The [round-3b ruling](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/134#issuecomment-5995957938)
   adds the fifth parent adoption patch and reruns the parent consumer set.
3. Read the linked [parent #608 ruling](https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-5885808887),
   parent #639's interface-preservation acceptance, and the repository authorities:
   REQ-SRP-001/-005, F01.4 delta 13, F08.1 T-MRP-LEAVE, SRP sections 6.3–6.5,
   the counter ownership contract in interfaces section 4.6, and the timer service's
   one-clock expiry output and registrar pending-ARM guard. The public area recipe
   was also inspected; its judged standalone endpoint uses the bound integrated clock.
4. Independently examined the complete requested `ead80360..9050c4bb` diff and history
   before reading prior review findings. The diff has 64 paths, including the mandated
   main merge. The issue-specific delta against `21c6f709` contains both registrar
   ordering changes, tests/mutants/docs and two format arguments. Inherited changes
   include counter-notification spacing, interface documentation, figure/ID gates,
   waveform exports and corresponding tests; these were inspected separately.
5. Then inspected public evidence and exact-head hosted metadata. Wrote the independent
   positive verdict and all-five-lens ledger in `receipts/independent-pass.md` before
   opening either prior public review report. Finally reconciled both reports and
   checked the PR's review and inline-comment endpoints, both empty.

**Reviewer-executed evidence**

Runs used disposable extractions under `scratch/`; no tracked source in the review
clone was edited. The scoped simulator reported version 5.050, recorded in
`receipts/simulator-identity.txt`. Independent checks ran concurrently under foreground
orchestration, with separate logs and return-code files. Campaign concurrency was
explicitly four; compiler subprocesses were capped at one per build, with at most
six simultaneous simulation builds. Make was invoked with `-j16`. No full bank,
parent build, hardware action or implementation-area run was started.

| Evidence | Result | Publishable receipt |
|---|---|---|
| Complete default integrated SRP executable, `make -j16 -C tb/srp_top run` | 8,656/8,656; 210,547,557 executed clocks; rc 0 | `receipts/srp-top.log`, `.rc`, `.json` |
| Stream-FSM suite, `RUN_ARGS=suite` | 1,347/1,347, including 128 SC1 pairs; rc 0 | `receipts/stream-fsms.log`, `.rc`, `.json` |
| Focused six-patch campaign, seven mutant/suite combinations plus three positive controls | 10/10 campaign checks; expected assertions fail in every mutant | `receipts/lv-mutants.log`, `.rc`, `.json`, `receipts/lv-mutants/` |
| Separate integrated reverse-order mutant receipt | rc 2 from the expected red simulation; exactly 16 SC2 failures, one per combination | `receipts/masked-integrated.log`, `.rc` |
| Independent expanded received-event probe | 1,536 additional cases; 2,883/2,883 with existing suite; rc 0 | `receipts/expanded-events.log`, `.rc`; `scripts/expanded_events.cpp` |
| Plantability of all SRP-top patches plus the changed counter-window patch | 115 checks, no failures; rc 0 | `receipts/patch-planting.log`, `.rc` |
| Focused documentation gates | ID self-test 30, figure self-test 17; 1,174 links; 115 requirements; 94 module rows, zero untested; 28 parameters; all pass | `receipts/docs-focused.log`, `.rc` |
| Source restoration and index/mode audit | 562 tracked blobs equal HEAD; index equal; zero gitlinks; empty status | `receipts/tree-before.json`, `tree-after.json`, `final-status.txt` |

The complete SRP executable includes all its default groups, S and SC included.
The separate four-shape storage/walk builds were not rerun by this reviewer; those
belong to the reported full source bank. Campaign fault return code 2 is the outer
make failure; the logs contain completed assertion tallies, not build failures or
timeouts. The campaign overwrites the shared `lv-expiry-masked.log` filename on its
second suite, so `masked-integrated.log` separately preserves the integrated failure.

| Fault | Observed failing checks |
|---|---|
| `lv-second-lv-ends` | 16, S1/S2 |
| `lv-never-ends` | 16, S2/S3 |
| `lv-expiry-masked`, integrated | 16, SC2 |
| `lv-expiry-masked`, stream FSMs | 16, SC1 |
| `lv-expiry-last` | 48, SC1 |
| `lv-expiry-dropped` | 86 total: 80 SC1 and six older checks |
| `lv-sweep-misses-collision` | 16, SC3; final-closure checks still pass |

**Five independent lens assessments**

- **Conformance — CLEAN.** Table 10-4's LV/rLv no-op and LV/leavetimer transition
  compose to MT regardless of their order; the manager's expiry-first rule determines
  renewal composition. Delta 13 still applies only to IN/rLv. In all eight S cases,
  LeaveTime measures 5,000 ms, inside the Table 4.3 range of 4,500–7,500 ms, with one
  ACTIVE fall, one registration-change indication and no new ACTIVE rise. The 6,416
  integrated offsets close on both planes, including the 16 actual collisions, and
  SC1 covers New, JoinIn, In, JoinMt, Mt, Lv and both LeaveAll forms. Relevant artifacts:
  `docs/architecture/08_timing.md:40`, `docs/architecture/10_srp_engine.md:548`,
  `tb/srp_top/sim_main.cpp:799`, `tb/srp_stream_fsms/sim_main.cpp:1072`, E receipts above.
- **RTL — CLEAN.** At `hdl/srp/KL_srp_talker_fsm.sv:729` and
  `hdl/srp/KL_srp_listener_fsm.sv:769`, expiry now precedes the non-registering Lv
  branch. New/Join retain their first branch: final IN, updated value and timer cancel.
  The listener's `ind_unreg_w` at line 449 already excludes a same-clock matching
  renewal, so state, applicant request and external indication agree. Existing type,
  latency and failure-change indications remain intact. No port, parameter, register
  or expiry handshake changed; the obsolete-expiry/pending-ARM exclusion remains.
  The inherited notification-stamp update was inspected against its dispatch/retirement
  state and CS/TW tests, with full-bank execution left to manager evidence.
- **Robustness — CLEAN.** S1-S3 retain repeated-Lv and post-expiry observation. SC2/SC3
  exercise both planes, own/peer LeaveAll, both variants and boundary indices, and prove
  that a decoded event actually reaches the calibrated collision. Snapshot restoration
  includes DUT and BFM state; the run counter counts replayed clocks instead of rewinding.
  The independent 1,536-case extension adds every slot, changes between Advertise/Failed
  and Ready/ReadyFailed, unmatched stream identities, cancellation, final indications,
  refreshed latency/failure data and absence of changes to other slots. The reverse-order
  and dropped-expiry controls show that a lost expiry produces a red, completed test.
- **Tests — CLEAN.** S1-S3 are retained; SC1-SC3 are dispatched by the normal executable
  and named by the campaign coverage gate. The independent executions reproduce the
  documented counts and fault signatures. SC3's separate control prevents an all-green
  sweep that misses the collision. The 300-million-clock budget has measured margin:
  210,547,557 clocks. Both D3 diagnostic formats now receive `D3_RECORDS` at
  `tb/pp_top/d3_phases.hpp:2964` and `:2994`. Refreshed patch contexts plant successfully.
  The corrected-base record equality and all-campaign totals are reported public
  evidence, not claimed as independent reruns here.
- **Docs — CLEAN.** SRP section 6.5, both suite READMEs and the harness comment agree on
  LV retention, expiry-first composition and continuous publication for renewals.
  The architecture cites T-MRP-LEAVE/F08.1 without repeating its numeric range; the
  suite README retains the measured numbers acceptance requires. Counts match execution.
  The inherited interface text was compared with landed byte/host/device faces; the
  three changed waveform exports were rendered and visually inspected. ID/figure,
  link, requirement/module and parameter checks pass. Historical public evidence is
  explicitly distinguished from exact-head and future candidate evidence below.

**Prior public findings: resolved or retained at this head**

Sources: [prior internal findings](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/160#issuecomment-5990539778)
and [prior external findings](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/160#issuecomment-5990392302).
The source reports were first read after the independent-pass checkpoint was written.

| ID | Severity and disposition | All attributable lenses | Location / authority / evidence | Impact and required outcome | Verification at this head |
|---|---|---|---|---|---|
| R488-1-F1 | MAJOR, RESOLVED | Conformance, RTL, Robustness, Docs; remedial Tests also examined | Both registrar branches cited above; Table 10-4 and manager ruling 5990549074; `receipts/srp-top.log`, `stream-fsms.log`, `masked-integrated.log` | Previously a coincident Lv lost the expiry indefinitely. Required expiry-first final behavior and matching documentation are implemented on both planes | All 6,416 offsets close; SC1 passes; restored branch order fails 16 integrated and 16 SC1 checks; no retained exception |
| R488-1-F2 | MINOR, RESOLVED | Tests, Docs | `tb/srp_top/sim_main.cpp:368`; `receipts/srp-top.log` | The measured budget justification was stale. Required outcome is a current measured count | Comment and measured `TOTAL_CLOCKS` both equal 210,547,557 |
| R489-1-S3 and R488-1-S-1 | SUGGESTION, RESOLVED | Docs | `docs/architecture/10_srp_engine.md:558`; docs/README single-source rule | Avoid a second numeric LeaveTime authority | The architecture now references T-MRP-LEAVE and F08.1; suite measurements remain in the README |
| R489-1-S1 | SUGGESTION, RETAINED | Tests, Robustness | `tb/srp_top/sim_main.cpp:818`, `:851`; prior no-Lv probe finding; current campaign controls | S1 alone does not count each decoded withdrawal. The complete gate set detects missing delivery because its planted faults then cannot be killed. Optional outcome: directly count both decoded target Lvs in group S | Existing original mutants are killed. If adopted, deleting either required Lv should fail the focused group itself. SC3 already observes decoded delivery for the collision group |
| R489-1-S2 | SUGGESTION, RETAINED | Docs | `tb/srp_top/README.md:519`; `sim_main.cpp:357`; interfaces section 4.6 | ACTIVE edges are a processor-side proxy for integrator-owned streaming counters. No parent counter was measured here. Optional wording: “counts ACTIVE edges; an integrator whose streaming level follows this licence counts the corresponding STREAM_START/STREAM_STOP edges” | Read-through against the counter ownership contract; no code change required |
| R488-1-S-2 | SUGGESTION, RETAINED | Tests, Docs | `tb/srp_top/sim_main.cpp:841`; README S1 row; prior aggregate-lane observation | The peer premise observes any decoded LeaveAll lane; the separate LV-state assertion and absence of own sLA make the combined check sound. Optional outcome: observe the Listener lane explicitly, or describe the combined premise accurately | Retain S1 state check and mutation coverage; if strengthened, a wrong-lane-only stimulus should fail the premise |

There are no new mandatory findings and no RESIDUE item. Retained suggestions do not
make any lens unclean. The current independent source verdict supersedes the prior
round's clean/unclean ledger only for the exact head named here.

**Public evidence provenance and limits**

- The immutable [pp134-r1 bundle](https://github.com/kebag-logic/milan-fpga/tree/7aecfd0bad90ea2d6e8306d45faf18b0eac9dfa6/review-evidence/pp134-r1)
  holds the earlier head's handoff, PR body and four adoption patches. Its handoff
  names `5ab43bd98209ef3cde206b325c06f0e7405e1e86`; the published SHA-256 was verified.
  It is historical evidence, not an exact-head raw bank receipt for `9050c4bb`.
- The current [PR body](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/160)
  and [public REVIEW READY](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/134#issuecomment-6000454088)
  report all required source and parent gates, twelve campaigns, equality of 579
  existing runtime receipts and 282 structured results, equality of the eleven
  corrected historical receipts, and the 446-entry planting audit. They report a
  shipping-clock 1x1 area change of 23,161→23,145 LUT and 19,783→19,780 FF
  (-16/-3), with unchanged RAM/DSP and matched parameters/images. These are public
  reported results; this reviewer did not rerun those banks or measurements.
- The review assignment states that the manager's full source static/builder and
  native banks passed at this head. The captured issue/PR manager comments contain
  scope rulings and review-start notices, but no separate raw manager bank receipts.
  Acceptance of those banks remains the manager's duty; this report does not turn
  the historical bundle into current executable proof.
- Exact-head hosted runs [37355183501](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/37355183501)
  and [37355190245](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/37355190245)
  show executed, successful documentation and portability jobs. Both suite jobs
  were still in progress at the captured snapshot. Their cached-simulator build
  steps were skipped; that skip is not a test execution. Pending suite/campaign
  steps are not credited as passed. Raw job/step metadata is in `receipts/hosted-*`.
- No standards PDFs were available in the donor. Clause conformance was checked
  against the public manager ruling and repository's recorded requirements/table
  interpretation; no independent full-specification audit is claimed.
- Physical calibration is **NOT RUN**. Field skips are not hardware proof.
  No hardware was used. The simulated stop is an ACTIVE edge; the parent integrator's
  actual streaming counter and physical stream were not measured by this review.
- No private author material, management checkout, private reviewer report, other
  checkout or shared installation was accessed or changed. There were no source fixes,
  commits, pushes, remote writes, contact with the author or delegated reviews.

**Reviewer-owned final ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen acceptance and four scope rulings; Table 10-4/delta 13; REQ-SRP-001/-005 and F08.1; S/SC and expanded-event receipts; reported area/source gates | R489-2 | 9050c4bbd25556929a0f24fb98258bc98e3bcfbe |
| RTL | CLEAN | Both registrar event chains and listener indications; timer expiry/ARM guard; no changed interface; inherited notification change; compiled exact-head simulations | R489-2 | 9050c4bbd25556929a0f24fb98258bc98e3bcfbe |
| Robustness | CLEAN | Repeated Lv, both causes/planes, collision observability, replay accounting, all slots, unmatched IDs, type/payload renewal, isolation, killed controls | R489-2 | 9050c4bbd25556929a0f24fb98258bc98e3bcfbe |
| Tests | CLEAN | S1-S3 and SC1-SC3, 8,656/1,347 source checks, 1,536 independent cases, seven mutant combinations, planting audit, D3 argument fixes and clock count | R489-2 | 9050c4bbd25556929a0f24fb98258bc98e3bcfbe |
| Docs | CLEAN | SRP section 6.5, suite READMEs, current timing/counts, inherited interface/figure/ID changes, rendered waveforms, evidence provenance, prior-finding disposition | R489-2 | 9050c4bbd25556929a0f24fb98258bc98e3bcfbe |

**Reproduction, integrity and pending duties**

Run `scripts/run_focused.py`, then `scripts/run_expanded.py` and
`scripts/run_supplemental.py`, supplying `--source <exact-head-clone>` and
`--packet <packet-directory>`; the first also takes `--simulator <scoped-5.050-launcher>`.
All extraction/build/probe state stays under the packet's `scratch/`. Run
`scripts/verify_tree.py <exact-head-clone>` afterward. The focused documentation command
was `make -j16 ids figures links matrix modmatrix params`, with TMPDIR inside scratch.
`git diff --check ead80360..HEAD` also passed.

After probes, every tracked working blob and executable/symlink mode equals HEAD,
and every stage-zero index entry equals HEAD's tree. All 562 blobs passed. The donor
has zero required submodule gitlinks; no parent checkout or pin was changed here.
The parent staging assertion above is public reported evidence, not this local audit.
`MANIFEST.sha256` lists every publishable receipt and script using relative paths;
`scratch/` is deliberately excluded. Logs retain full build and assertion output;
only the local simulator include root is replaced with `<SCOPED_SIMULATOR_ROOT>`.
`receipts/path-redactions.json` records original and published hashes; unredacted
originals stay in unpublished scratch. No result, diagnostic or failing assertion
is removed.

The manager must obtain the second independent positive review, accept the reported
donor/parent gates with the processor gitlink staged and all five adoption patches,
and own hosted/act acceptance. The final current-dev candidate must be built and
validated at the merge turn against live dev
`28f9666feab2b2ba287643c63ed3a16b1e0bb863`; source base remains
`ead8036035affd53ef4b29979190f2f4f67084c0`. Source validation and that candidate are
distinct. Retained suggestions may be carried at the manager's discretion; there is
no residue checklist item from this round. Publication is left to the manager.

R489-2 FINISHED
