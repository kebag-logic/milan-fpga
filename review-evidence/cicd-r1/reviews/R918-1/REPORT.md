[R918] NEGATIVE - exact head fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f

Round R918-1, external independent review of issue #998 / PR #1001. Two open MINOR findings concern measurement evidence. No source correctness defect was found. All five lenses were applied independently. This verdict and ledger were written before consulting another reviewer's report.

Source tree: `6aa4a42135fc7615a344aba1935eac8133bdf54b`. Reviewed range: `300da99beed5bb1c77e4b04af0bb4f9369856e0d..fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f`, the three commits `427b7f4f`, `f09c9a0f`, `fcbc31f3`. The source base is the train head, not the recorded PR base oid. Remote refs were checked and retained in `receipts/remote-heads.txt`.

Authorities reconstructed: AGENTS.md sections 6-7; CONTRIBUTING.md verification and public-evidence rules; docs/README.md; [issue #998](https://github.com/kebag-logic/milan-fpga/issues/998), whose body requires measured CPU/wall evidence and identical output for every adopted change; REQUIREMENTS.md REQ-VER-01 through REQ-VER-04; docs/testing/TESTING.md and CI_WORKFLOWS.md; inline interfaces and harnesses for the affected models; [issue #996](https://github.com/kebag-logic/milan-fpga/issues/996) and its default-port authority. The issue had no comments in the retrieved public snapshot. Public role assignments were the two review-start comments, including [this review's start](https://github.com/kebag-logic/milan-fpga/pull/1001#issuecomment-7130112822).

The public author's evidence was read at immutable commit `9b89b4b559f4577bd73df1aacc6881c6a60a8269`, under `review-evidence/cicd-r1/author`. No private author material or management source bank was used.

## Findings

**R918-1-F1 | MINOR | Conformance, Tests, Docs | author/receipts/ccache/{nocc,cold}.time:1; author/receipts/INDEX.md:16; author/REPORT.md:174-175; PR body Description, ccache row**

Authority/evidence: #998 acceptance criterion 1 requires measured CPU/wall evidence for the adopted change. The report and PR claim the CRF 23-case campaign improved from 377 wall / 498 user seconds to 247 wall / 262 user seconds, about 47%. But the retained `nocc.time` says **967.68 wall / 1587.52 user**, and `cold.time` says **782.82 wall / 547.52 user**. Those are the report's separate avtp_rxmon measurements. `cold.stats` likewise contains its 71.59% hits, not the CRF experiment's stated 66%. The index assigns the same paths to both experiments; only the CRF warm receipt and aggregate verdict lines remain identifiable. See the [published cold receipt](https://github.com/kebag-logic/milan-fpga/blob/9b89b4b559f4577bd73df1aacc6881c6a60a8269/review-evidence/cicd-r1/author/receipts/ccache/cold.time), the corresponding copies in `receipts/author/ccache/`, and `receipts/static-audit.log`.

Impact: the adopted 47% figure cannot be reconstructed from the designated raw receipts. This is a measurement-test provenance gap, not evidence that caching produces an incorrect executable. The independent cache replay below establishes output identity for the unit harness; it does not recreate that original full-campaign performance measurement.

Required outcome: retain separately named CRF and avtp_rxmon timing/cache receipts, with the actual commands, revision/variant identity, and matching output comparison; reconcile the index and claims with them. Alternatively correct or withdraw claims whose measurement cannot be recovered.

Verification: recompute the CRF cold/no-cache CPU and wall changes from the correctly attributed raw receipts, and verify that their full campaign outputs preserve every named result. Re-review the repaired evidence. This is not wording-only RESIDUE.

**R918-1-F2 | MINOR | Conformance, Docs | PR body Description, CPU-budget row; author/REPORT.md:137; author/receipts/budget/{base,tbO3}*.perf**

Authority/evidence: #998 acceptance criterion 1 and the requested PR-to-packet figure reconciliation. The PR and report say **7-9% fewer L1 data-cache misses**. Pairing the three identically suffixed raw runs gives:

| Pair | Base L1d misses | -O3 L1d misses | Reduction |
|---|---:|---:|---:|
| unsuffixed | 3,946,517,051 | 3,374,059,598 | 14.5054% |
| -2 | 3,741,671,160 | 3,411,296,019 | 8.8296% |
| -3 | 3,654,245,643 | 3,457,482,933 | 5.3845% |

The same pairs' CPU reductions are 4.8655%, 2.6136%, and 2.5002%, which support the stated 2.5-5% CPU range. Raw files are in `receipts/author/budget/`; `scripts/audit_static.py` reproduces the arithmetic in `receipts/static-audit.log`.

Impact: the public optimization claim misstates the observed miss reductions. It does not invalidate the independently reproduced output identity.

Required outcome: correct the miss figures in the PR and evidence report to the demonstrated paired results, or identify and retain a different reproducible pairing that supports the claimed range.

Verification: calculate each reduction as `100 * (1 - optimized / base)` and check the revised claims against the named files. Because this changes a measurement figure, it is MINOR, not RESIDUE.

## Independent executable evidence

The four complete behavioral suites were rebuilt and run at both revisions. Default harnesses and default mutation campaigns were invoked separately so simulation stdout/stderr could be retained independently of compiler chatter. MMCM includes unit, rails, PHC-step, and slew-suite executions. CRF includes unit, discontinuity, connected-talker/servo, and its campaign. MAAP includes its default campaign's real datapath integration cases. All eight suite runs exited zero.

The comparison deletes **no simulation lines**, masks **no numbers**, and performs **no sorting**. The build transcripts and exact command/exit records are separate receipts. Therefore the claim is literal equality of the complete behavioral output, not equality of compiler echoes. The public author's comparator has multiset fallbacks; this review does not rely on those fallbacks.

| Suite | Identical output bytes | Lines | Default campaign cases | Result |
|---|---:|---:|---:|---|
| crf_rx | 151,847 | 2,595 | 23, including 20 named rejections | PASS |
| maap | 20,530 | 379 | 65, including 63 named rejections | PASS |
| mmcm_servo | 21,504 | 373 | Explicit additional control below | PASS |
| aaf_clock_meter | 6,312 | 115 | 38, including 37 named rejections | PASS |

`receipts/output-comparison.json` records SHA-256 equality and negative controls for the comparator. The raw logs are `receipts/{base,head}.<suite>.output.log`; `*.commands.json` and `*.rc` retain invocations, wall times, revisions, and exits. All named campaign rejections are preserved identically.

The additional MMCM `discard_removed` mutant compiled on both revisions and exited **1** at the same required check, **`[S1] overlapped window is discarded`**. Both clean controls exited zero; both clean outputs and both mutant outputs are byte-identical. Compiler failure was not counted as a kill. See `receipts/servo-control.json` and `receipts/{base,head}.servo-control.{clean,mutant}.log`.

The CPU-budget 8x8/1-interface fixture was built independently. Recompiling only the host testbench object from -O3 to -Os and relinking produced two binaries that both exit zero, complete every stimulus step, and emit identical **2,947,272-byte** logs. Both MD5 values are **`4a5c0c06df755c05f19f03fb2056167d`**, also the published `bud-ab1`/`bud-ab2` value. This is a simulation identity check, not a new hardware or full budget-bank claim. See `receipts/budget-comparison.json`, `budget-build-identity.json`, `budget-fixture.txt`, and both `budget.<level>.output.log` files.

The cache guard passed all six combinations of installed/absent cache and unset/empty/explicit caller override. An actual CRF unit replay produced identical uncached, cold-cache, and warm-cache output: **15,714 checks, zero failures**. The warm rebuild hit all five compilation entries; cumulative stats show five hits and five preceding cold misses. `receipts/cache-replay.json`, the three `cache-*-output.log` files, and cache statistics retain this evidence.

The cancellation regression passed using the packet's scratch directory for temporary fixtures. It covers INT/TERM boundaries, cleanup, masked failures, timeouts, hard stops, and unsupported-facility refusal. See `receipts/cancellation.log` and `.rc`.

## Probe, model, and compiler audit

The harness audit found **36 source occurrences representing 27 distinct internal names**. It includes the `root()` alias, the local `root` pointer, constants, and the source macro census; no additional token-pasted probe was found. Every name is listed in the suite's configuration. The only three externally written internal signals are writable.

| Suite | Distinct names | Read/write disposition and examined artifacts |
|---|---:|---|
| crf_rx | 9 | `pdu_count_o`, `fmt_err_o` are `public_flat_rw`; `tout_r` and six servo observations are read-only. `sim_main.cpp:1394,1412,1765`, `sim_talker_step.cpp:72,126`, `probes.vlt:10`. |
| mmcm_servo | 9 | Integrator, command/error, sequencer, window/tick/jump observations and `u_tick_cdc.sync` are read-only. `sim_phc_step.cpp:161-180`, `probes.vlt:9`, `hdl/common/cdc_pulse.sv:37`. |
| aaf_clock_meter | 5 | All read-only. `sim_main.cpp:226`, `sim_servo.cpp:160,225-228`, `probes.vlt:9`. The unchanged meter-only build already protects `g5_v_r` with the RTL annotation at `KL_aaf_clock_meter.sv:345`. |
| maap | 4 | `lfsr_r` is writable; timer and two constants are read-only. `sim_main.cpp:967,1155,1192`, `probes.vlt:9`. |

`receipts/probe-audit.json` records each source occurrence and access designation. Runtime preloads still pass their counter-wrap and generator checks. The generated dependency records for all **six altered model builds** contain no defaulted input declarations; MAAP coverage uses the same source closure. The seven command-table changes correspond exactly to those builds plus coverage. See `defaulted-port-audit.json`, `model-commands.json`, and `command-table-audit.json`.

The larger, unchanged MAAP integration hierarchy was also inspected against #996's eleven defaults. Capture inputs connect to driven internal marker/depacketizer/monitor/state wires; the transmitter transit bit connects to a producer or explicit zero; packetizer stream IDs come from driven control-plane outputs. The processor's interface-index port is omitted at `KL_pp_shadow.u_pp`, so its unconnected-port default correctly supplies interface zero. None of those examined connections is a top input or an undriven connected net. Exact source locations are in `maap-integration-port-audit.json`. This is not a claim that global issue #996 is resolved; follow_ring and media_phase retain their flags.

The pinned simulator was verified as **5.050**. Its launcher/binary hashes, compiler version and make version are in `tool-identity.json`. Generated make rules show `OBJCACHE` prefixing compiler calls, not execution or verdict classification. The firmware-boundary capture implementation and hosted workflows are unchanged; no hosted cache installation was added. `OPT_FAST=-O3` reaches the host testbench rule after `-CFLAGS`; the model already receives -O3. `unchanged-authorities.json` and the retained build records support these conclusions.

The four probe-list CPU claims recalculate to **37.4401%, 25.8554%, 26.6209%, and 9.8083%** improvements, consistent with the rounded PR figures. The public local-shard summaries support their stated pass counts; their hosted extrapolations remain estimates. The two exceptions to figure reconciliation are F1 and F2.

No changed RTL, firmware, test expectation, protocol bound, or hosted scheduling rule was found. No new forbidden identity or review/bench-lane label was found in source comments in the reviewed delta. Existing labels outside the delta were not refiled.

## Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1, F2 | #998 AC1; PR body; author timing/perf files; four output pairs; budget comparison | R918-1 | fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f |
| RTL | CLEAN | `receipts/delta.patch`; four `probes.vlt`; harness references; generated model closures; MAAP integration connections | R918-1 | fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f |
| Robustness | CLEAN | Counter wrap/preload, malformed/truncated MAAP, stopped-gap/timeout/recovery, servo slew/boundary checks; named mutants; cache selection; cancellation receipts | R918-1 | fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f |
| Tests | UNCLEAN: F1 | Four complete paired logs; mutation drivers and named rejection output; `servo-control.json`; budget/cache/cancellation receipts; missing attributed CRF performance receipts | R918-1 | fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f |
| Docs | UNCLEAN: F1, F2 | TESTING.md:169-178; command-table diff; PR Description; author REPORT.md and receipts/INDEX.md | R918-1 | fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f |

[R918] PASS RTL - `receipts/probe-audit.json`, `defaulted-port-audit.json`, `maap-integration-port-audit.json`, `delta.patch` - all harness accesses retain appropriate visibility; no affected defaulted-input hazard or interface change found.

[R918] PASS Robustness - `receipts/output-comparison.json`, `servo-control.json`, `cache-selection.json`, `cancellation.log` - boundary, negative, state/reset, cache-override and cancellation behavior retained in the examined cases.

## Limits and pending manager duties

- Source validation is separate from the final current-dev candidate. Live `dev` was independently observed at `e275d7950ef3385753e6a15d2e191ba855b171ed`. No manager source bank at this head is claimed. The author packet's local hosted-shard replicas are author evidence, not a manager bank or hosted job execution.
- No full parent, processor, gPTP, Yosys, builder, or native bank was run here. No hosted/act acceptance is asserted. The manager owns current-dev candidate construction, builder/native banks, protected hosted contexts, executed-versus-skipped accounting, receipts, and the 30-minute hosted-job acceptance criterion. That criterion is not established by these local ratios.
- Physical calibration: **NOT RUN**. No hardware was accessed. Field skips and simulation results supply no physical proof.
- The first CPU-netlist setup attempt lacked an explicit heap/processor bound; the observed unit peak reached **13,985,181,696 bytes**, above the requested 12 GB. It was stopped and restarted with a 2 GiB heap and two processors; clean dependency cache was released. The successful native build used two jobs. The first cancellation run used the default temporary directory and was subsequently repeated successfully with scoped scratch fixtures. These are execution-process deviations, not findings against the PR. `receipts/resource-note.json` retains the resource limit.
- The original detached clone was never source-edited. Final verification compared actual blob bytes, file modes, and index entries with the exact head, and verified all five initialized submodule gitlinks and their tracked bytes. All matched; see `receipts/tree-integrity.json`. No source fix, commit, push, GitHub write, merge, author contact, sub-agent, hardware access, Docker, or act execution occurred.
- F1 and F2 require repair and re-review. This negative round does not approve later repairs. The manager must finish independent review and candidate validation before any authorized merge, then perform containment and issue/project completion.

## Receipts and reproduction

Run the portable scripts from this packet with an isolated source repository and the existing pinned dependencies. `scripts/run_pairs.py SOURCE_REPO` creates base/head disposable trees under `scratch/` and joins all child work; `scripts/compare_outputs.py` verifies the literal output comparisons. `scripts/audit_models.py SOURCE_REPO`, `scripts/audit_static.py SOURCE_REPO`, `scripts/cache_pair.py`, `scripts/servo_control.py`, and `scripts/verify_tree.py SOURCE_REPO` reproduce the focused audits. For the CPU fixture, place a disposable copy of the existing CPU dependency under `scratch/deps/pythondata-cpu-vexiiriscv`, then run `scripts/budget_pair.py PRODUCT_DEPENDENCIES RV32_SDK PINNED_SIMULATOR`. It uses the existing product dependencies without installing them.

All disposable build/probe trees are excluded from publication. `MANIFEST.sha256` lists the publishable scripts and receipts. Simulation logs are raw and unchanged; `*.public.log` build receipts replace private host paths only. Exact commands and exit statuses accompany the suite logs. The report is published separately from the manifest's receipt population.

After this independently written verdict and ledger, the public PR timeline was refreshed. It contained the two review-start announcements and no prior review findings, submissions, or inline findings to resolve or retain. No other reviewer report was read. The reconciliation is recorded in `receipts/prior-findings.json`.

R918-1 FINISHED
