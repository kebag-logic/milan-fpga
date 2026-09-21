[R218] POSITIVE - exact head 2a2007cff57bd2a01254e1da7c43ec73b9d8d4b3

Independent external CONTRACT review, round four, issue #500 / PR #503. Applied lenses: **Tests, Docs**. No open finding remains under either assigned lens at this page head. This verdict covers the proposal and its executable evidence. It grants no product implementation, silicon, release, readiness or merge claim.

The evidence reviewed and rebuilt is commit `c1ee27d81c4a1e98f9584e979b73a88acfe238b3` on public branch `500-design-evidence`. The live validation base was `2d8fd62fd986ea2d6a87d284e144f023034c0944` before review and at completion. The PR remained open and draft at the supplied head.

Public artifacts used below:

- **P**: [Proposed materialization page at the reviewed head](https://github.com/kebag-logic/milan-fpga/blob/2a2007cff57bd2a01254e1da7c43ec73b9d8d4b3/docs/design/SAVED_STATE_MATERIALIZATION.md).
- **E**: [Immutable executable evidence, receipts and ticket drafts](https://github.com/kebag-logic/milan-fpga/tree/c1ee27d81c4a1e98f9584e979b73a88acfe238b3/design-evidence/500-materialization). References to its `proposal-evidence/`, `reviewer-probes/` and `tickets/` directories mean this exact commit.
- [Issue #500](https://github.com/kebag-logic/milan-fpga/issues/500), its [O1/O3 clarification](https://github.com/kebag-logic/milan-fpga/issues/500#issuecomment-5755853228), and [issue #70](https://github.com/kebag-logic/milan-fpga/issues/70), including its limited binding silicon evidence.
- The complete public [R217 round-three review](https://github.com/kebag-logic/milan-fpga/pull/503#pullrequestreview-5266850209) and [R218 round-three review](https://github.com/kebag-logic/milan-fpga/pull/503#pullrequestreview-5266850499), independently matched to their [immutable reports](https://github.com/kebag-logic/milan-fpga/tree/3d790bc1eacad2af0cb7d80c647f0c8eca186c46/review-evidence/503-round3/reviews).
- The [revised public response](https://github.com/kebag-logic/milan-fpga/blob/514932dfc1e76c7c26a9212fcd30a540a73e50df/review-evidence/503-round4/author/RESPONSE.md), [revision decision](https://github.com/kebag-logic/milan-fpga/pull/503#issuecomment-5760942111), [proposed mechanism decision](https://github.com/kebag-logic/milan-fpga/pull/503#issuecomment-5761117424), [ownership clarification](https://github.com/kebag-logic/milan-fpga/pull/503#issuecomment-5762146376), [REVIEW READY](https://github.com/kebag-logic/milan-fpga/pull/503#issuecomment-5763185026) and [final-head gate status](https://github.com/kebag-logic/milan-fpga/pull/503#issuecomment-5763325186).

I reconstructed the contract from those public artifacts, `CONTRIBUTING.md`, `AGENTS.md`, `docs/README.md`, `REQUIREMENTS.md`, accepted `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` and `SAVED_STATE_FASTCONNECT.md`, and the linked processor contracts and executable sources. No private handoff, scratchpad, management receipt or agent transcript was used. The exact ticket drafts T1 through T9 in E were read, alongside public issues #501/#502 and processor issues #15/#20/#61/#63/#83/#92.

[R218] PASS Tests - E `proposal-evidence/run.py`, `harness/`, `prototype/`, `results.json`, `reviewer-probes/r218_r3_probe_stage1.py`; P sections 7, 8 and 14 - rebuilt all 76 builds, executed all 386 scenarios and 4,560 checks, independently examined named killers and baseline premises, reproduced the stage 1 counterexample and exercised seven additional all-nine-sink scenarios. Zero verdict failures; all eight CLI controls behaved as required. The limitations below bound this result.

[R218] PASS Docs - P sections 3, 5, 8.6, 8.9, 10, 12, 14, 15 and 16; E `README` files and `tickets/T1` through `T9`; issue #500's O1/O3 clarification and the accepted snapshot/fast-connect contracts - ownership, recovery, release ordering, normative amendments, repository responsibilities, prerequisites and cost/model qualifications agree with the examined sources and fresh results. The open product defects remain explicit prerequisites or stated limitations; filing them is not treated as repair.

The two round-three findings are corrected in the **contract and evidence**, as follows. Their original severity and every lens label are preserved. These dispositions do not claim that the proposed mechanisms have landed in product RTL, and do not bank the other reviewer's assigned lenses.

**R218 R3-F1, continuing R217 R2-F2: MAJOR Conformance / RTL / Robustness / Tests / Docs.** Corrected. P:441, section 8.6, section 10, and T1/T2/T9 consistently put descriptor-store recovery in stage 1, alongside dynamic-state reset. Stage 2 adds names to that existing recovery ownership. The guard's response debt belongs to hard reset and survives the owners' rollback reset. This addresses the actual pinned descriptor-store watchdog behavior: after response timeout, its next request can fail immediately unless the watchdog is rearmed. Draining the late response alone does not repair it.

The fresh full campaign exercised S1a through S1h on the stage 1 build and both full shapes: healthy selectors, a 4,000-cycle response below the store watchdog, 5,000 and 16,000-cycle finite responses, a response beyond the D3 deadline, one error followed by healthy service, an unproven initial image, and a pass-1 read error. The expected outcomes remain COMPLETE, proven DEFAULTS with service for recoverable dependencies, and CLOSED for an unproven image or excessive debt. ST1 is killed separately by both S1c and S1d. DG01, DG02, DF01 through DF03, IMG01 and the ordinary-service late-beat control also remain effective.

I additionally reran the public round-three selector-only reproduction against the fresh binaries. Its slot contains only configuration `0x00=0000`, clock source `0x0a=0001` and offset `0x50=1500000`; all other records are erased. All 12 runs completed with the demanded result:

| Build / stimulus | Observation |
|---|---|
| Full and stage 1, 5,000-cycle response | DEFAULTS, no mismatched default records, ownership released and entity enabled. Stage 1: request 2443, abort 6543, late beat 7444, owners leave reset 7455, terminal 8110, enable 8123. |
| Full and stage 1, 16,000-cycle response | DEFAULTS and service. Stage 1: request 2443, abort 6543, late beat 18444, owners leave reset 18455, terminal 19110, enable 19118. |
| R03 and ST1, either finite late response | Completed scenario, but CLOSED with ownership retained and enable 0, despite zero mismatched default records. This reproduces the defect; a default-value-only oracle would miss the availability failure. |
| All four builds, one descriptor error followed by healthy service | DEFAULTS and service. The deletion does not manufacture a failure for every descriptor error. |

**R217 R3-F1, continuing R217 R2-F3: MAJOR Conformance / RTL / Robustness / Tests / Docs.** Corrected for this contract review. P:438 and sections 8.1/8.9/10, T1/T4/T8, the final admission prototype and its harness agree. S4 excludes competing work from the shared hard reset until the binding walk has terminated and the listener has committed and drained its final preload action. It establishes a finite preload phase without abandoning accepted preloads or attempting a partial rollback.

I checked this against the unchanged pinned listener's actual priority and holder logic, and `protocol_processor_top.sv`'s dispatch/scoreboard, event-router acknowledgement, timer wiring and binding-view update. Transaction and talker-event valid **and** acceptance-ready are masked. START/STOP has a different interface: only valid is masked; ready/error is completion after capture and commit or failure. Its holder and completion flags start empty on the same hard reset and cannot fill while owned. Neither listener nor S4 takes D3 rollback reset. The event router retains its presented payload until acknowledgement; its existing coalescing/overflow policy for later arrivals is outside the prototype and is explicitly preserved, not advertised as lossless buffering of every arrival.

The timer exclusion has a stated invariant: while owned the listener can reach only X_INIT/X_IDLE/X_PRELOAD, which do not arm its timers, and the real timer service resets its armed bits. The admission gate counts filtered listener-owner expiries. S4's release follows actual listener record writes and A4 discovery strobes, not just the manager's valid/ready acceptance. In real top-level wiring that strobe updates the binding view. At the pinned pipeline depth, manager done already follows the action; the page correctly says the two additional drain predicates are not independently discriminated by this pipeline, rather than claiming separate mutant proof for them.

The release points remain distinct: S4 releases live ACMP listener service and starts D3; D3 COMPLETE/DEFAULTS releases AECP/state-bus ownership; their combined terminal qualifies ADP advertisement enable. Queued live listener actions can therefore execute during D3. They are not late preloads. CLOSED does not reacquire the listener. T4 must start the binding walk on every boot path, and T8/T9 must land in the same processor pin or an earlier pin before stage 1 merges.

The fresh campaign retained first/later-sink interference, reset/power-cut, live-touch, release-minus-one/release/release-plus-one, higher-priority request and drain controls. LG01 fails both the bounded-walk check and read-only binding preservation. LG02/LG03 fail for the two unpaired handshake errors; LG04 fails expiry exclusion; LG05 exposes START/STOP completion before restore. The tracked build still fails L01 and L05. In L01 the deleted gate permits a 3,229,969-cycle untaken preload and two withdrawals; L05 answers unbound and destroys the saved binding. Those failures are required controls, not green product evidence. Public [processor issue #92](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/92) remains open; S4's substantive mechanism and these discriminating tests address the proposal's responsibility for it.

My adjacent fixture populated **all nine sinks** at 8x8, retaining the published first/last identities and giving sinks 1 through 7 distinct talker IDs, UIDs and controller IDs. L00, L01, L03b, L05, L06, L09 and L13 all completed: **7 runs, 132 checks, zero failures**. Each run accepted exactly sinks 0 through 8 once, at cycles 867, 871, ..., 899; manager terminal was 901 and release 903. The existing grader checked every saved binding's real write and discovery arm before release, paired acceptance, bound, later service and verified-slot contents. STOP/BIND applied after restore; D3 rollback preserved all nine bindings. This extends the published two-bound-sink fixture without modifying either RTL or binaries.

Earlier findings attributable to this review were re-examined on the changed artifacts and fresh results. They are not banked merely from round three:

| Prior finding | Original severity and all applicable lenses | Current disposition and artifacts |
|---|---|---|
| R218 R1-F1 / R217 R1-F1, partial restore | MAJOR Conformance / RTL / Robustness / Tests / Docs | Corrected contract retained: P section 8.6; V11b/V12-V18, R01-R04, X01 and M16 exercise rollback and agreement. |
| R218 R2-F1 / R217 R2-F1, recurring and balanced header faults | MAJOR Conformance / RTL / Robustness / Tests / Docs | Retained: S1 distinguishes DEVICE from UNFRAMED; per-record pass vectors prevent equal-count substitutions. H1-H8, V18/V18b/V18c, V10, C01-C03, X01-X02 and binding B02/B04 reproduce their required outcomes. |
| R218 R1-F2 / R217 R1-F2, early enable | MAJOR Conformance / RTL / Robustness / Tests / Docs | Retained and extended through S4: reset ownership, terminal-qualified enable, read quarantine/drain and CLOSED refusal; W controls, V17, K19, W01/D01/G05/R05/O01 and B01/B03. |
| R218 R1-F3, runner survival/incomplete-run acceptance | MAJOR Tests / Docs | Corrected: planned scenario matching, `case_completed`, every named killer required, exit status and all eight process controls. |
| R217 R1-F5, runner process verdict | MINOR Tests / Docs | Same substantive correction retained; original MINOR severity remains recorded. |
| R218 R1-F4, configuration replay deletion | MAJOR Conformance / Tests / Docs | Retained: configuration value **and valid flag**, per-group/index comparisons, all nine TRG and RPL groups; synthetic two-rate shape tests non-default rate replay. |
| R218 R1-F5, capacity/status staging | MAJOR Conformance / Robustness / Tests / Docs | Corrected staging retained: #501 blocks stage 3; #502 correction precedes every shippable stage. K16 is explicitly containment only. Neither open product defect is declared resolved. |
| R217 R1-F4, corresponding capacity/status staging | MAJOR Conformance / RTL / Robustness / Docs | Same staging correction; preserve its additional RTL attribution and original label set. |
| R217 R1-F3, malformed map padding | MAJOR Conformance / RTL / Robustness / Tests / Docs | Retained: exact eight-byte FF sentinel, no holes/partial tails or aliased indices; V3a-V3g and P01/P02. |
| R218 R2-F6, synthetic output-format oracle | MINOR Tests / Docs | Corrected distinction retained: V1s uses shipping output legality and value plus valid; both format directions' named killers must fail their shipping and synthetic checks. Partial-kill control exits 1. Synthetic narrowed-output ordering cases remain labelled. |
| R218 R2-F7, T8 versus issue #15 reuse | MINOR Docs | Corrected: T8 states permanent quarantine and pending after permanent device silence; finite late completion can restore port service. It neither delivers nor amends issue #15 criterion 2 and does not close issues #15/#20. |

For the runner specifically, I inspected its baseline grading, mutation substitutions, plan, named-killer lists and report logic. The full result contains intentional failures: the tracked implementation's nine required failures, mutant failures and the stale-store vacuity control. It is not 4,560 ordinary passing assertions. Every one of the 71 mutants failed **every** named killer in a completed scenario. Under M13, a stale value still fools naive readback while the cleared-first assertion fails. Eight doctored-binary CLI controls required the exact diagnostics and exits: surviving mutant 1, incomplete scenario 1, failed baseline 1, violated tracked control 1, violated vacuity control 1, absent tracked build 2, partial kill 1, empty selection 2. All eight matched.

The wider contract checks under the assigned lenses produced no further finding:

- **Ownership and durability:** O1 remains the firmware's single sequential control-face master; O3 orders the distinct device-face initiators, binding restore, D3 restore and later writes. The new writer/arbiter never writes the control face. The taint/set-wins rule covers changes during latch/write and on done; the backend's logical-record completion, dirty snapshot and firmware's verified-slot acknowledgement remain separate events. K2-K9/K15/K17/K18 and the acknowledgement/reset controls exercise their boundaries rather than treating device-face done as durable flash.
- **Inventory and framing:** the prepared shipped shapes have 53/156 records, of which 49/145 are D3; names number 38/99. Group IDs, indices, lengths, empty names, scalar valid bits, map padding and unsupported-value refusal agree across the page, drafts, inventory and graders. Restore ordering covers selectors, formats, offsets, maps and names, including format/map consistency. The 8x8 map record's nine entries do not cover every legal 72-channel output set. #501 must settle a conforming allocation or accepted mapping limit before a stage 3 lane opens; pending-and-skip is not accepted persistence.
- **Volatile state:** IDENTIFY is executed as a must-not-persist case and M06 is killed. Lock and registry have no D3 materializer; their complete integrated reset proof is still owed. Allocated SUID/MCR records have no source and are not newly materialized. Bindings and started/stopped remain the binding manager's responsibility, outside D3 rollback.
- **Defaults and invalid input:** invalid framing/value is refused per record, while transport failures abort the restore transaction. A failed image proof cannot be relabelled blank or successful DEFAULTS. Descriptor timeout/error is separated from unsupported selector value; late response debt survives rollback and cannot be consumed by a later request. Finite recovery is distinguished from permanent persistence-port quarantine.
- **Repository ownership and staging:** T1/T2/T3/T8/T9 are processor work; T4 owns parent integration, firmware ordering and silicon proof; T5/T6 track #501/#502, and T7 the old area table. T8/T9 are public drafts to file after contract acceptance and before implementation. The proposal distinguishes unchanged pinned stores/listener/timer/backend, amended port/binding-manager prototypes, new modules and modeled parent behavior. Interfaces may be reviewed first, but a stage 1 merge cannot omit its prerequisite pin changes.

I **accept the proposed live-write trigger amendment for this contract review**. The source of identity is the accepted live write, and the early pending obligation must start there: a later class-1 mark does not uniquely identify the changed record, and name/map mark tails currently admit false durable status. The replacement acceptance covers nine separate trigger groups and nine replay groups, preserving direction distinctions and IDENTIFY exclusion. It has executable deletion controls, not just prose.

That acceptance does not silently alter the existing normative documents. Recorded contract acceptance and reconciliation of FASTCONNECT sections 12.2/16, SNAPSHOT scope D2 and processor F07.9 remain required before implementation, together with affected public ticket criteria. The page enumerates those edits in section 15.1 and remains Proposed; the accepted pages receive pointers, not an unnoticed requirement rewrite. The selected mechanism comments and this review supply no waiver of #501/#502 or donor issues #15/#20. Timing/debounce choices and implementation-stage validation still need their recorded implementation contracts.

The cost claims were checked against the immutable recipes, parameters, wrappers and all 26 committed rows. No fresh OOC synthesis is claimed:

| Examined cost claim | 1x1 | 8x8 | Qualification |
|---|---:|---:|---|
| Writer plus arbiter | 2,377 LUT / 888 FF | 3,116 LUT / 1,109 FF | Prototype OOC measurements. |
| Writer/arbiter plus S1-S4 increments | 2,506 LUT / 942 FF | 3,242 LUT / 1,163 FF | Estimates using separately measured increments, not integrated bounds. |
| Existing listener alone | 2,174 LUT / 1,530 FF | 2,268 LUT / 1,557 FF | Existing cost, never charged again as incremental. |
| Listener with admission gate | 2,187 LUT / 1,547 FF | 2,276 LUT / 1,574 FF | In-place OOC differences +13/+17 and +8/+17. The standalone gate is 13/17 and 14/17 LUT/FF; the total estimate uses the standalone 8x8 value. |

S1's port difference is +4 LUT/+2 FF, S2 is +5/+1, and the amended binding manager adds +107/+34 at 1x1 and +103/+34 at 8x8. The recipe uses the declared sources and `sv2v`/`synth_xilinx -family xc7 -flatten`, prices distributed RAM explicitly and refuses missing/zero/unpriced statistics. The listener cost wrapper passes START/STOP completion unchanged, matching the final contract and evidence. Candidate (a) remains a replicated-manager/shadow proxy and (c) a fabric proxy excluding firmware and integration. The old 30-name backend calibration is 1,030 LUT/468 FF, not the accepted page's historical 772/377; P and T7 expose that discrepancy. Reset seams, additional integration muxing, CDC, placement, timing and the final incremental resource budget still require implementation measurement. The 1 MHz model and its 20,000-cycle watchdog cannot establish an integrated 20 ms bound.

Validation and integrity results:

- Initial page tree was clean. Only the four documentation files in the PR differ from live dev. Page tree object: `1fc6e7edcfc5a3e1f055ed1f73ba70614996977e`. Ancestry and `git diff --check` passed.
- Fresh disposable public evidence checkout at E; explicit private `D3_OUT`, `OOC_OUT`, `TMPDIR` and probe outputs under `/data`. Builds used CPUs 80-95, build pool 1 and at most eight build jobs. Each test/gate campaign was awaited before the next started.
- All **69** published digests match immutable blobs: 50 evidence files plus 19 repository inputs. E's executable files are unchanged from its recorded execution-source commit `a78c79afebab98d53b94c034c92f7191989e8806`. Against the candidate/live-base inputs, 18 are byte-identical; only `scripts/nvm_shape.py` differs, in comments with identical parsed Python syntax.
- Before and after execution, independently hashed all tracked blobs against Git objects: 850 page blobs, 900 evidence-checkout blobs, and 539 initialized submodule blobs in each checkout. Zero mismatches. Processor pin `424c688fa2205b934a7689a58f2aa766420f2326`; gPTP pin `c1b617435824929a790739ea8585c3fe1a328cc0`; axis pin `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The unused `external` gitlink `efeb541ae5fe1e078332d8462dca2fc2d9cb8db5` remained uninitialized.
- Full evidence: `SUMMARY FULL builds 76, runs 386, checks 4560, verdict failures 0`, exit 0. **No published build or planned scenario omitted.** Results were byte-identical to E: `results.txt` SHA-256 `be0949d71dc00aa57186b957787b47229d4387ee72478034b5759a42ee617903`; `results.json` SHA-256 `5c74cee9ed36bf3dff53405b62d77fd4dd5b9c38679afc231f0e179cfe85dc48`.
- `CONTROLS 8, not as required 0`; selector-only probe/check: `12 runs, 0 not as demanded`; additional all-nine-sink check: `7 runs, 132 checks, 0 failures`.
- All **26** selected documentation/contract commands below returned 0. `docs_check` reported zero findings, 23/23 scrub self-tests and 4/4 routing arms. Record-space self-tests rejected their planted defects. Repository ratchet commands passed their existing thresholds; that does not declare their pre-existing inventories empty.

Reproducible effective commands are below. `$PAGE` denotes the supplied review checkout, `$E` the disposable evidence checkout at the immutable commit, and `$SCRATCH` a fresh private directory under `/data`. These are placeholders, not published host paths. The evidence directory was copied unchanged to a same-depth sibling because its full runner writes results beside itself; tracked sources were not overwritten.

```sh
git -C "$E" checkout --detach c1ee27d81c4a1e98f9584e979b73a88acfe238b3
git -C "$E" submodule update --init protocol-processor gptp-processor third_party/verilog-axis
cp -a "$E/design-evidence/500-materialization" "$E/design-evidence/500-review-run"
export TMPDIR="$SCRATCH/tmp" D3_OUT="$SCRATCH/d3" OOC_OUT="$SCRATCH/ooc"
RUN="$E/design-evidence/500-review-run/proposal-evidence/run.py"
taskset -c 80-95 python3 -B "$RUN" prep
taskset -c 80-95 python3 -u -B "$RUN" build --pool 1 --jobs 8
taskset -c 80-95 python3 -u -B "$RUN" run --pool 8
taskset -c 80-95 python3 -u -B "$RUN" controls --pool 8

export FULL_OUT="$SCRATCH/d3" PROBE_OUT="$SCRATCH/probes"
export EVIDENCE="$E/design-evidence/500-materialization/proposal-evidence"
taskset -c 80-95 python3 -B "$EVIDENCE/../reviewer-probes/r218_r3_probe_stage1.py"
taskset -c 80-95 python3 -B "$EVIDENCE/../reviewer-probes/r218_r3_check.py"
```

For the additional seven scenarios, set `D3_OUT` to a separate empty scratch directory and run the following with `taskset -c 80-95 python3 -B`. This is the fixture and assertions used; the local runner additionally saved JSON diagnostics.

```python
import importlib.util, os, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location('r218_adjacent', Path(os.environ['EVIDENCE']) / 'run.py')
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)
s = m.prep_shape('8x8')
assert s.params['N_STREAM_IN_P'] == 9
over = m.l_slot(s)
for sink in range(1, 8):
    over[0x20 + sink] = m.binding_payload(
        0x00A3000000000000 + sink, 0x0A10 + sink, 0x00C3000000000000 + sink)
slots = m.crafted(s, 'all-nine-bound', over)
b = m.Build('base-8x8', '8x8', binary=Path(os.environ['FULL_OUT']) / 'build/base-8x8/obj/d3sim')
for case in ['L00_listener_restore_control', 'L01_tk_event_held',
             'L03b_tk_discovered_queued', 'L05_txn_read_only_in_the_window',
             'L06_stop_held', 'L09_bind_held_live_change',
             'L13_d3_rollback_keeps_the_bindings']:
    r = m.run_case(b, s, case, slots=slots)
    g = m.grade_run(r, s, {'crafted': over})
    g.check('all_nine_sinks_preloaded',
            sorted(sk for _cy, sk in g.preloads()) == list(range(9)), str(g.preloads()))
    assert r.rc == 0 and r.done
    assert all(ok for ok, _detail in g.checks.values()), (case, g.checks)
```

From `$PAGE`, each following line was run sequentially as `taskset -c 80-95 python3 -B <line>`:

```text
scripts/docs_check.py
scripts/check_doc_style.py
scripts/check_solution_docs.py
scripts/check_doc_paths.py
scripts/check_archive.py
scripts/gen_toc.py --verify-anchors
scripts/gen_toc.py --check
docs/traceability/gen_module_matrix.py --check
scripts/check_feature_status.py
scripts/check_submodule_docs.py
scripts/check_hygiene.py --check
scripts/check_todo_ownership.py
scripts/check_em_dash.py --base 2d8fd62fd986ea2d6a87d284e144f023034c0944
scripts/check_nvm_record_space.py
scripts/check_nvm_record_space.py --self-test
scripts/check_port_contracts.py
scripts/check_rtl_source_lists.py
scripts/check_soc_sources.py
scripts/check_cpp_idiom.py
scripts/check_py_idiom.py
scripts/check_sv_idiom.py
scripts/check_sh_idiom.py
scripts/ci_scope.py --selftest
scripts/measure_naming.py --check
scripts/measure_fail_fast.py --check
scripts/measure_test_evidence.py --check
```

Identity checks included `git ls-remote origin refs/heads/dev refs/pull/503/head refs/heads/500-design-evidence`, the public PR API's head/base/draft fields, `git submodule status`, `git merge-base --is-ancestor 2d8fd62fd986ea2d6a87d284e144f023034c0944 HEAD`, `git diff --check 2d8fd62fd986ea2d6a87d284e144f023034c0944...HEAD`, and byte hashing against `git ls-tree -r HEAD` with replacement objects disabled. Exact remote identities were checked again at completion. The only added review artifact in the page checkout is `REVIEW.md`; tracked sources remain byte-exact.

Omissions and limits of this verdict:

- No full product native bar, full builder rerun, `milan_dp` rerun, Docker/act, hardware, privileged action, push or public write. The manager's public final-head receipts were read as public claims; they are not substituted for this review's fresh tests. The deferred full native bar and protected hosted checks remain mandatory before readiness/merge. No old-head gate result is attributed to this candidate.
- No OOC or Vivado execution; consequently no Vivado lock was needed or acquired. All 26 committed OOC rows and their recipes were inspected, but none is claimed freshly reproduced here. No integrated area, placement, timing or silicon bound is established.
- Of the 47 historical adapted probe runs, the 12 R218 round-three selector-only runs were independently repeated; the other 35 were inspected but not separately repeated. The fresh full campaign omitted none of its 386 scenarios and retained the relevant older controls.
- The real listener and timer service are exercised, but real dispatch overflow, event-router coalescing, ADP discovery and START/STOP microprogram timing are modeled at their interfaces. Actual CDC/memory-path watchdog/poison timing, map-edit phases 0 through 5, firmware boot change 2, feature-dependent integration, physical flash cuts, complete volatile-state reset and post-place costs remain implementation obligations. Synthetic non-default rate, narrowed output formats and nonempty reset maps do not become shipping facts.
- Open #501, #502 and processor #92 remain open product work. T8/T9 filing is still required and is not implementation. Their presence alone clears nothing: the clean result above relies on the revised dependency contracts, examined mechanisms and discriminating evidence. Donor issues #15/#20 and accepted requirements receive no silent waiver.

Reviewer-owned covering ledger, accepted here by R218 for the assigned lenses only:

| Lens | Covering round | Exact page head |
|---|---|---|
| Tests | R218 round four | `2a2007cff57bd2a01254e1da7c43ec73b9d8d4b3` |
| Docs | R218 round four | `2a2007cff57bd2a01254e1da7c43ec73b9d8d4b3` |

Conformance, RTL and Robustness are not banked by this ledger. No merge-completion claim is made: this ledger covers neither those three lenses nor the remaining required validation. This report is a local reviewer-owned artifact prepared for publication; no public state was changed.

R218 FINISHED
