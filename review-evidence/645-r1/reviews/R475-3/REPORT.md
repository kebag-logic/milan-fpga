[R475] POSITIVE - exact head 2525eae9567865a8bc741901914bdf5a1caf2c26

R475-3 independently applied all five lenses to the round-2d delta of issue #645 / PR #672, including #647. All five are CLEAN at this source head. R474-2-F1 is resolved. No BLOCKER, MAJOR or MINOR remains in this review's scope. Two earlier wording residues and three optional suggestions remain below. This verdict does not authorize merge or establish hardware acceptance.

Reviewed tree: `a0545d5d4f4e098464fbd6a6a7a21fb4c735a423`. Source base: `fea346e76c2a57ed5cd131af8fc68dfeff57f877`. Incorporated dev: `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`.

Reconstruction and scope

Repository operating rules, contribution rules, documentation index, public issue bodies/rulings, requirements and interface authorities informed the review. The requested base-to-head comparison contains intervening dev work; the comparison against incorporated dev identifies the lane's 38 paths. The round delta against `886e16201654ba0fd0c60c41c228ea4c75b2f6d3` contains two lane commits and two dev merges. Both new merge trees equal automatic merges of their parents; neither changes shipping HDL or implementation inputs. `receipts/merge-audit.json`, `first-parent.txt` and `round-delta.diff` retain that evidence.

The governing decisions are the [round-2d assignment](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6032466525), [symmetric correction](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6009543884), [two-PDU span](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6009767440), [recovery qualification](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6010634115), and [timing STOP disposition](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6041375798).

Public executable evidence came from the [initial archive](https://github.com/kebag-logic/milan-fpga/tree/6efdd2447c72b9b60f5d0d9e393c851bb742945a/review-evidence/645-r1) and the [published round-2d archive](https://github.com/kebag-logic/milan-fpga/tree/65b9e8ee8f9e00cc303b3c294d243a89781807e9/review-evidence/645-r1/author-r2d). All 591 initial-author files and 416 round-2d-author files match their publication-manifest hashes. No private author material or current concurrent review report was used. The independent assessment and ledger were recorded in `receipts/independent-pass.md` before reading prior public reviewer findings. Those findings were then reconciled below; the public formal-review and inline-comment lists were empty.

Independent findings on the delta

[R475] PASS Conformance - `hdl/ieee1722/aaf/KL_chan_map_capture.sv:896`, `docs/reference/REGISTER_MAP.md:1870` - Declared holds do not increment the duplicate counter, including an empty pair awaiting its first new commit. Ordinary starvation remains counted. This matches the issue's unchanged-counter contract without modifying the AAF presentation law or declared action span.

[R475] PASS RTL - `hdl/ieee1722/aaf/KL_chan_map_capture.sv:879-969,1034-1107`, `hdl/milan/milan_datapath.sv:6565-6666` - The new `!pop_hold_w` term feeds only the saturating duplicate accumulator. Pop/hold/drop control, pointers, same-cycle push/pop composition, wire output, reset and flush precedence remain unchanged. No clock crossing, width or external-interface change is introduced by this delta. The retained settle controller still uses the existing axis domain, bounded pending state and recovery dwell.

[R475] PASS Robustness - `tb/verilator/chmap_capture/sim_main.cpp:1703-1917,2032`, `scripts/hold_expiry_probe.py` - Empty and full correction, unprimed state, flush, coincident pulse/first beat, saturation and the delayed second-pair commit were exercised. The independent expiry probe holds that pair empty through all five declared walks: cumulative dup deltas are `0,0,0,0,0,1,3` over seven walks. Thus suppression ends exactly with the declared holds. A subsequent flush stops starvation accounting; skips remain unchanged.

[R475] PASS Tests - `tb/verilator/chmap_capture/sim_main.cpp:1756,1920`, `tb/verilator/follow_ring/mutants.py:68-196` - The new test proves reachability using a no-pulse twin that counts exactly one duplicate. Its pulsed twin requires zero duplicates/skips and the emitted sequence `e6,e6,e6,e6,e6,e7` on both pairs. HELD-DUP and STARVED-HELD-DUP each fail every required named check. Reverting only the counter predicate changes exactly two assertion outcomes and the final verdict; all wire/span output lines remain identical (`receipts/starved-counter-only.diff`). The existing six-phase/two-output/six-offset span tests and their three controls pass.

[R475] PASS Docs - `docs/design/TIME_SYNC.md:489-496`, `docs/reference/REGISTER_MAP.md:1870`, `docs/design/MEDIA_CLOCK_FOLLOWING.md:1545-1546` - The split wording preserves the requested distinction: every source change and each pull starting outside prior recovery receives a settle action; an inside-recovery pull is the declared residual. The concluding exception sentence is verbatim. The plural “dropped events” fix is also verbatim. The style check and compiled-source traceability check pass; the latter includes 7/7 controls and does not credit the reduced harness with the whole datapath.

Fresh execution and public evidence

| Check | Result | Receipt |
|---|---|---|
| Capture suite | 785 checks, 0 failures | `receipts/capture-run.log` |
| Both held-duplicate controls | 2/2 caught; each build rc 0, each fault run rc 1 | `receipts/held-mutants.log`, `receipts/mutants/` |
| Additional hold-expiry probe | 789 checks, 0 failures; replaces the expensive saturation phase with nine expiry/flush assertions in a disposable harness copy | `receipts/hold-expiry-run.log` |
| Controller at 6.25, 25, 50 and 100 MHz | 4/4 pass: quiet, recovery interruption, source priority, reset, LOCKED dwell, disengaged dwell and ceiling | `receipts/controller.log`, `receipts/controller/` |
| Documentation style; traceability | Both rc 0; traceability controls 7/7 | `receipts/doc-style.log`, `receipts/traceability.log` |
| Public evidence and merge audit | Publication hashes, area arithmetic/input hash, quiet totals and both new automatic merges verified | `receipts/public-evidence-audit.json`, `receipts/merge-audit.json` |

The scoped simulator identity was verified as 5.050 before compilation; its version and launcher digest are in `receipts/simulator-identity.json`. Builds used explicit job limits, with no implementation run or full bank launched.

Published OOC reports give capture `1156-1076 = 80` LUT and `1372-1336 = 36` FF, plus settle `74-41 = 33` LUT and `93-51 = 42` FF: **+113 LUT/+78 FF**, below 120/120. The measured capture input hash equals this head's bytes. The prior **+119/+82** remains conservative; the smaller result is not represented as an intentional logic saving. No new routed area or timing proof exists at this head.

The published campaign comparison records **128/128 arrival logs and 32/32 INTERNAL logs byte-identical** to round 2c, with both return codes zero and identical quiet JSON. The eight groups total **320,462,699** quiet samples within +/-1 axis cycle. I recomputed those totals and checked the comparison receipt; I did not independently rerun the long campaigns or compare all individual logs, which are not republished in this round. Published margins remain 2.17/2.24 ticks (empty/full).

The published physical simulation receipt contains 143 normal checks, 40 accounting checks and 14 ordering-control checks, all passing. Its two wire actions each declare and observe -5 events with unchanged counters. This is simulation using diagnostic admission overrides. The public source evidence also reports the complete default bank, render pull-in/boundary, builder, parser and portability results; none is recast here as an independent full-bank execution or final current-dev candidate validation.

Prior public finding disposition

Sources: [R475-1](https://github.com/kebag-logic/milan-fpga/pull/672#issuecomment-6009109435), [R474-1](https://github.com/kebag-logic/milan-fpga/pull/672#issuecomment-6009527655), [R475-2](https://github.com/kebag-logic/milan-fpga/pull/672#issuecomment-6031787384), [R474-2](https://github.com/kebag-logic/milan-fpga/pull/672#issuecomment-6032462363). Original severities and lens assignments are preserved.

| Prior ID | Original severity / lenses | Disposition at this head |
|---|---|---|
| R474-2 F1; earlier R474-1 S1 retained by R475-2 | MINOR / Conformance, RTL, Robustness, Tests, Docs | RESOLVED: excluded held walks; new reachability/wire case; both faults caught; independent expiry check. Published P1 gives pulsed dup 0, control +2. |
| R475-1 F1 | MAJOR / all five | RESOLVED under the public two-PDU amendment; exact consecutive action, strict outside order, six phases and fanout controls pass. |
| R474-1 F1 | MAJOR / all five | RESOLVED: full-side excess drop, ten-left case and `fill - 5` physical expectation retained; both-sign published campaign evidence unchanged. |
| R474-1 F2 | MAJOR / all five | RESOLVED under the recovery ruling: two-cycle arm, fine holds, qualified rearming and narrow graded residual retained. Controller rerun passes; physical fine-hold evidence is published. |
| R475-1 F2; R474-1 F4 | MINOR / Docs | RESOLVED: disengaged INTERNAL explicitly waits 2,048 ticks; four-rate controller confirms it. |
| R475-1 F3; R474-1 F3 | MINOR / Conformance, Tests, Docs; BLOCKER / Tests, Docs | RESOLVED in source: text-only exclusion and accurate generated matrix pass at this exact head. Required hosted completion remains a manager duty. |
| R474-2 R1 | RESIDUE / Docs | RESOLVED: split wording preserves the requested meaning and passes the style gate. |
| R474-2 R2 | RESIDUE / Docs | RESOLVED verbatim: “dropped events”. |
| R475-2 R1, R2 | RESIDUE / Docs | RETAINED below. |
| R474-2 S1, S2, S3; R474-1 S2 retained by R475-2 | SUGGESTION / lenses below | RETAINED below; optional and not treated as repaired. |

Retained residues and suggestions

- **R475-2 R1; RESIDUE; Docs.** Artifact: PR #672 body, Status paragraph. Evidence: the exact head is published, while the paragraph still calls it local pending publication. Impact: stale publication wording only. Exact fix: replace “The executor does not push. This head is local until the manager publishes it; it then awaits independent re-review.” with “This head is published and awaits independent re-review.” Keep the timing-blocked status. Verification: compare the paragraph with the published head. Manager residue checklist.
- **R475-2 R2; RESIDUE; Docs.** Artifact: `docs/design/MEDIA_CLOCK_FOLLOWING.md:1086`. Evidence: the locator beside the preserved #386 trigger still names `g_settle_recentre`; that trigger is `g_src_recentre`. Impact: neighboring-block locator only; no behavior, measurement or clause changes. Exact fix: replace only that parenthetical identifier with `g_src_recentre`. Verification: follow it in `milan_datapath.sv`. Manager residue checklist.
- **R474-2 S1; SUGGESTION; Tests.** Artifacts: `tb/verilator/follow_ring/settle_control.py:54`, `tb/verilator/follow_ring/quiet_distributions.py:66`, `hdl/milan/milan_datapath.sv:6585`. Evidence: the controller tests +/-1 quiet noise, while the reader's band is supplied as an argument; neither directly pins the non-arming boundary at magnitude 2. Impact: reduced protection against lowering the shipped band. Optional outcome: assert that +/-2 never arms, or bind the reader to the shipped constant. Verification: a one-cycle-band fault must fail. The current constant is 2; no product defect is asserted.
- **R474-2 S2; SUGGESTION; Tests, Docs.** Artifacts: `docs/design/MEDIA_CLOCK_FOLLOWING.md:1107-1166`, `tb/verilator/follow_ring/Makefile:36`. Evidence: full quiet/arrival measurements are explicitly at 6.25 MHz; the four-rate test exercises controller logic, not physical quiet distributions or pull-in latency. Impact: shipping-clock dynamics have less standing evidence. Optional outcome: add a 50 MHz quiet/pull-in case and identify its measured latency separately. Verification: require no quiet arming and record the post-pull action. No shipping-frequency measurement was repeated here.
- **R474-2 S3 / R474-1 S2; SUGGESTION; Tests.** Artifact: `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:1101-1105`. Evidence: zero decisions prints an uncounted NOT RUN instead of failing that scenario; published normal evidence contains two decisions. Impact: the physical leg alone can omit its recentre assertions. Optional outcome: require a startup decision where the scenario guarantees one. Verification: suppress that action and require a named failure. Separate controller and missing-action controls remain current evidence.

Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #645/#647 decisions; `docs/design/MEDIA_CLOCK_FOLLOWING.md:1090-1166`; `docs/design/TIME_SYNC.md:386`; counter predicate and wire/counter receipts | R475-3 | 2525eae9567865a8bc741901914bdf5a1caf2c26 |
| RTL | CLEAN | `hdl/ieee1722/aaf/KL_chan_map_capture.sv:805-1107`; `hdl/milan/milan_datapath.sv:1308,6565-6666`; merge audit, area input identity, builds | R475-3 | 2525eae9567865a8bc741901914bdf5a1caf2c26 |
| Robustness | CLEAN | `tb/verilator/chmap_capture/sim_main.cpp` [LRC]/[SPAN]/[SAT]; independent hold-expiry/flush probe; four-rate recovery/reset/ceiling controller; published campaigns | R475-3 | 2525eae9567865a8bc741901914bdf5a1caf2c26 |
| Tests | CLEAN | `tb/verilator/chmap_capture/sim_main.cpp:1756,1920`; `tb/verilator/follow_ring/mutants.py:68-196`; physical checker and public controls; traceability 7/7; raw execution receipts | R475-3 | 2525eae9567865a8bc741901914bdf5a1caf2c26 |
| Docs | CLEAN | `docs/design/TIME_SYNC.md:489-496`; `docs/reference/REGISTER_MAP.md:1870`; design test rows; compiled-source matrix; PR/issue declarations and public evidence | R475-3 | 2525eae9567865a8bc741901914bdf5a1caf2c26 |

Real limits and pending manager duties

This is a functional delta review at the named source head. No full parent, processor, time-processor, builder or portability bank was run here. No implementation, hardware, flashing or calibration was performed. Physical calibration is **NOT RUN**; the absent Arty builder arm and field skips earn no hardware credit. Ambiguous render windows remain ungraded. The declared second-pull residual remains accepted scope, and #657's four historical render-mutation failures remain outside this lane.

The exact-head hosted snapshot records successful executed firmware, lint, conformance, wire-accountability and some portability jobs, with documentation, elaboration and long jobs still running. Physical gPTP is **skipped**, not executed. No successful aggregate or `rtl-fast` completion is inferred from individual jobs. Hosted and local-replica acceptance remain the manager's; neither was launched here.

Under ruling 6041375798, the `eth0_rx_dv` IOB-pack failure is owned by #691 and is not a finding in this round. It still prevents a successful current-head timing claim: no bitstream or WNS/WHS exists for this head. After #691 lands, the manager must merge dev, rerun the timing sweep, and obtain the necessary review of that new delta. Earlier timing success cannot clear the new candidate.

The manager must retain the two residues, reconcile the independent companion verdict, finish hosted/local evidence acceptance, construct and fully validate the final current-dev candidate, and secure explicit maintainer merge authorization. After merge, containment and issue/project closure remain required. The INTERNAL-to-AAF and AAF-to-CRF physical repeats and release obligations remain outstanding; “Closes #645/#647” must not discharge them. Published source-bank results do not validate a later merge candidate.

Reproduction and restoration

Portable entry point: `python3 scripts/reproduce.py --repo <detached-clone> --sim <scoped-simulator>`, invoked from this packet. Public evidence objects named above must be present. Scripts run foreground subprocesses, use explicit job limits, and keep all generated source copies and builds below `scratch/`. Source files were never edited; no commits, pushes, GitHub writes, other-checkout edits, shared installs or external contact occurred.

`receipts/final-integrity.log` verifies the exact head and tree, every tracked raw blob and executable mode, each index, and all three required submodule gitlinks and checkouts: processor `ead8036035affd53ef4b29979190f2f4f67084c0`, time processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, AXIS `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The 1,178 superproject blobs and 876 required-submodule blobs pass. The unused external gitlink remains uninitialized. The final worktree is clean.

Raw simulation verdicts are retained. Publication copies of build logs and command receipts replace local installation/workspace prefixes with placeholders; original and published hashes are recorded in `receipts/publication-redactions.json`. Originals remain under unpublished scratch. Only `MANIFEST.sha256` entries and this report are publication inputs; scratch is excluded.

R475-3 FINISHED
