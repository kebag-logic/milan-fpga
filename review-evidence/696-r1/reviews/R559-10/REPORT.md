[R559] POSITIVE - exact head 313616d1a18549d41907db389d378f0beb9bc543

External independent delta review R559-10 of issue #696 / PR #706.
Reviewed tree: `8eb5d868bfac1973ba1d82b0665aabae07d9494c`.
All five lenses are CLEAN. No open BLOCKER, MAJOR or MINOR remains.
One new prose RESIDUE and retained earlier residues are listed below.
Optional suggestions remain optional.

This verdict covers the source composition at the named head. It does not
assert completion of the manager's merge, hosted acceptance or bench duties.

## Scope and independent reconstruction

The reconstruction order was AGENTS.md / CONTRIBUTING.md, docs/README, the
[issue and public rulings](https://github.com/kebag-logic/milan-fpga/issues/696),
requirements and interface authorities, the requested
`c6bd08c6f52632c6d33d834ce842ac3cf63f29cc..313616d1a18549d41907db389d378f0beb9bc543`
diff and history, then the
[published source receipts](https://github.com/kebag-logic/milan-fpga/tree/dd8350f0d648656904188e490ecff933024bff0c/review-evidence/696-r1).
The independent verdict and ledger were written before reading prior reports.
Prior public findings were then checked against this head; their complete
[disposition](RECONCILIATION.md) is part of this verdict.

Authorities examined include `REQUIREMENTS.md`, FR-MAAP-01 in
`docs/reference/FR_NFR.md`, the Annex B contract in `MAAP_FABRIC.md`, the MAAP
module interface, the MAAP rows of `REGISTER_MAP.md`, the synchronous PHC
contract at `milan_datapath.sv:2934`, and the resource policy and measurement
recipe. The binding scope includes:

- M4 first-enable sampling and real-datapath MAC diversity.
- Clause-based correction or explicit justification for M1-M8.
- The [M8 ruling](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6076940309): discard incomplete PDUs without effects; counting withdrawn.
- The [area/shared-buffer ruling](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6079087547): +60 LUT / +60 FF on the MAAP hierarchy, bounded response capacity disclosed.
- The [first-draw criterion](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6102832618): power-of-two seed separation, high-half word bijection and stated limits.
- The [latest merge assignment](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6142198285): import dev `e81ce82f`, retain protected MAAP inputs, verify the worker budget and measure against that dev.
- Bench interoperability belongs to the assigned post-merge bench lane.

The requested focus named the older `aa980479` delta. The exact assigned head
also includes `b075a994`, `26e2748f` and `313616d1`; those were included.
Imported dev features were examined for composition and relevant interfaces.
This is not a new full implementation review of every imported feature or
execution of the prohibited full banks.

## Composition and record identity

[Mechanical reconstruction](receipts/composition.log) reproduces all three
merge trees, without conflicts or additional resolution content:

| Merge | Ordered parents | Reconstructed tree |
|---|---|---|
| `a7291311` | `32582421`, `09c7231e` | `0705eb4a691dcfb8211de9c7da79883cc357b249` |
| `b075a994` | `aa980479`, `c6bd08c6` | `4650fd5d9d5c940bc6788491229dc808cf866962` |
| `313616d1` | `26e2748f`, `e81ce82f` | `8eb5d868bfac1973ba1d82b0665aabae07d9494c` |

`aa980479` changes exactly the five requested M2/M6 sentences in the plan;
`26e2748f` changes the three analogous M5 sentences. Eleven MAAP source,
harness, contract and baseline blobs remain identical to `32582421`.
Against imported dev `e81ce82f`, `milan_datapath.sv` differs only in the MAAP
area comment and the `eff_link_w` / `ptp_now_w[31:0]` input connections.
M6's counter-column wiring is retained.

R558-9-F1 and R558-9-R1 are resolved at plan `:696-697,707,952,973`.
R558-11-F1 and R558-11-R1 are resolved at `:1099-1100,1115`.
Each lane names the #645/#647 record it used; the text names #696's
50,013-LUT replacement. The historical 50,267 planning baseline remains
explicitly dated. No remaining unqualified route-comparison sentence names
50,267 as the current gate record.

The unmodified [R558-9 script](scripts/record_vs_lane_routes.py) reports
22 matching current-inventory route rows. The unmodified
[R558-11 script](scripts/check_plan_composition.py) confirms all 66 inventory
figures and the partial-central 38,784-LUT arithmetic.
[Additional comparisons](receipts/lane-records.log) show that each historical
base row equals the `e8454e27` record and M2, M5 and M6 pass against both
historical and current records. These checks consume stated measurements;
they do not perform a new route.

## Executed review evidence

The scoped compiler identifies as version 5.050; its runtime binary SHA-256 is
`44898b22af4178b45214a0820a04eeac8632ae721ff005e69ef1cf69121bbfdd`.
GNU make is 4.4.1. [Identity receipt](receipts/tool-identity.json).

All builds and disposable data were placed under packet `scratch/`.
The foreground driver waited for every child. Independent jobs ran concurrently,
with at most sixteen compilation jobs and no synthesis execution. The initial
lint invocation omitted its worker option and used the host-CPU default, so
that invocation did not respect the requested sixteen-job bound. Its receipt
is preserved as `lint-initial.log`; lint was rerun alone with `--jobs 1`.
The reproduction driver now runs bounded lint after the concurrent builds.
The observed unit peak was 10,125,099,008 bytes, below the assigned 12 GB cap;
no OOM event occurred. [Resource receipt](receipts/resource-envelope.txt).

| Check | Result at this head | Receipt |
|---|---|---|
| Default MAAP target, `make -j16 ... all VERILATOR_JOBS=4` | 186 unit checks, zero failures; 65 campaign rows: all 63 defects rejected by named assertions, two clean controls pass | [Full log](receipts/maap-default.log) |
| Real CSR/datapath MAAP arm within that campaign | Clean five-check integration passes; all five integration plants detected | [Campaign log](receipts/maap-default.log) |
| Shipping 1x1 and timed notification legs | 233 and 423 checks, zero failures | [Datapath log](receipts/datapath-legs.log) |
| Original 4x4 datapath recipe, selected alone | 1,967 checks, zero failures; GET_COUNTERS versus CSR, distinct columns, invalid descriptors, per-stream isolation and MAAP admission | [4x4 log](receipts/datapath-nxn.log) |
| `lint_rtl.py --check --jobs 1` | PASS, 90 violations <= existing ratchet 90; bounded rerun | [Lint log](receipts/lint.log) |
| Focused documentation/resource/shard set | All seventeen commands pass: links/privacy, style and self-test, feature status, solution docs and self-test, imported docs and self-test, submodule docs and self-test, module matrix, contents, anchors, added-line checks against both bases, resource baseline and shard self-test | [Results](receipts/results.json), [driver](scripts/run_static.py) |
| `pp_resource_gate.py check-baseline` | PASS, three endpoints; policy unchanged | [Baseline log](receipts/resource-baseline.log) |
| Worker assignment | MAAP remains 1,375 s on worker 1/5, predicted 4,205 s <= 4,320 s; all five workers within bound; inventory 62 | [Prediction](receipts/shard-prediction.json), [self-test](receipts/suite-shards.log) |
| Tree integrity after execution | Exact tracked bytes, modes and stage-zero index agree with HEAD in both checkouts; three required submodules match pinned bytes and gitlinks | [Review checkout](receipts/tree-final.log), [execution checkout](receipts/execution-tree-final.log) |

The mutation driver rejects compilation failures and abnormal termination;
a defect counts only when its executable exits 1 and prints the required
named assertion. Detections include reset-time sampling, link-loss restart,
pending/active response overwrite, truncated-input effects, invalid supplied
range, the below-offset DEFEND echo and first-draw fold plants.

Required initialized gitlinks: processor
`2ad2f845dd583f8310075fa2380cb60a04fd091a`, gPTP
`7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9`, axis
`48ff7a7e2ef782cf778d47910cf85835c64b1bce`.
No tracked source fix, commit, push, GitHub write, hardware access or merge was
performed. No execution job remains in flight.

## Published source evidence and its limits

[The public-evidence audit](receipts/public-evidence-audit.log) verifies twenty
selected author receipts against their publication manifest. It checks source
head/tree provenance, the actual MAAP log, the OOC hierarchy, resource-gate
outputs and broad-bank result records. Of 378 measured input entries, 241
candidate inputs and 122 dev inputs match checkout bytes or exact git objects.
Fifteen generated/external entries were not regenerated by this reviewer.

The author evidence at this exact source head records MAAP at 446 LUT / 340 FF,
or +7 / +60 against 439 / 280. The routed source is 49,277 LUT / 53,419 FF,
WNS +0.242 ns and WHS +0.017 ns; compared with its imported dev route, the delta
is -150 LUT / +41 FF. The source route and both standalone endpoint checks pass.
The accepted 50,013-LUT record remains separately dated under D7.

Published source-bank receipts report all five shards, a disjoint 62-suite
inventory and 2,187,183 checks, plus native, processor, firmware, coverage and
portability evidence. These are the author's executions, not banks rerun by
this reviewer and not a manager source bank.

Evidence boundaries:

- The campaign summary carries an unmatched log digest (`d60eed49...`, 26,785
  bytes). The published log is `9d1dd18a...`, 26,543 bytes; both publication
  manifests agree on those bytes. This review verifies the published log
  directly and reruns its campaign. No raw-to-published mapping is inferred
  for the unmatched summary digest.
- Builder calibration gate 11 is explicitly NOT RUN because its historical
  placement report is absent. Required elaboration is reported separately.
- Field skips and the hosted physical-job skip are not hardware proof.
  Physical calibration and bench interoperability were not run here.
- The every-seed argument uses the inspected linear RTL structure; sampled
  linearity checks cannot exhaust arbitrary nonlinear replacements. Pool-fold
  bias, occupied response-buffer capacity, untagged-only reception and absent
  discard counting remain disclosed deviations. Separation excludes the zero
  fallback and is guaranteed only for the ruled seed-pair/block domain.
- The hosted [exact-head snapshot](receipts/hosted-snapshot.json) contained
  executed successful jobs, jobs still running and a skipped physical job.
  It establishes no completed hosted aggregate acceptance. No repeated hosted
  polling or local workflow replica was performed by this reviewer.

## Findings

**R559-10-R1 - RESIDUE - Docs - PR #706 body, Status, checkout introduction and
Known limitations.**

Authority/evidence: the public body names the correct published head, but says
`This is an unpublished update for PR #706.`, introduces checkout with
`After publication of this head:`, and lists `publication` as pending.
[Public PR](https://github.com/kebag-logic/milan-fpga/pull/706).

Impact: stale publication wording only. No measurement, figure, verdict, code,
test, generated artifact, privacy rule or conformance claim changes.

Required exact outcome for the residue checklist:

1. Replace the Status sentence with `This update is published on PR #706.`
2. Replace the checkout introduction with `To check out this head:`
3. Remove `publication, ` from the pending-duties bullet.

Verification: read the updated public body against the published head; preserve
historical receipt attributions and manager acceptance duties.

Earlier residues, optional suggestions and every prior blocking/minor finding
are resolved or retained in [RECONCILIATION.md](RECONCILIATION.md).
None is treated as resolved by moving it to another issue.

## Reviewer-owned coverage ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #696 frozen rulings; `KL_maap.sv:138-496`; `MAAP_FABRIC.md:47-201`; source resource receipts; 186-check unit run and first-draw/echo detections against ruled Annex B criteria | R559-10 | 313616d1a18549d41907db389d378f0beb9bc543 |
| RTL | CLEAN | `milan_datapath.sv:3447-3534,6334-6346,7181-7192`; `KL_maap.sv:138-496`; `composition.log`, `lint.log`, three focused datapath legs; synchronous seed/link inputs and retained counter-column interface | R559-10 | 313616d1a18549d41907db389d378f0beb9bc543 |
| Robustness | CLEAN | `sim_main.cpp:660-960,1020-1278`; `sim_integration.cpp`; `mutants.py`; full campaign: truncation/keep masks, pool boundaries, link loss/return, response cancellation/occupancy and backpressure | R559-10 | 313616d1a18549d41907db389d378f0beb9bc543 |
| Tests | CLEAN | `maap/Makefile`, `integration.mk`, `mutants.py:208-281`, `sim_main.cpp:1180-1276`; `milan_dp/sim_nxn.cpp:4778-4882,9417-9468`; `suite_shards.py`; named detections, real integration and worker-budget checks | R559-10 | 313616d1a18549d41907db389d378f0beb9bc543 |
| Docs | CLEAN | `MARK_II_AREA_PLAN.md:109-147,680-707,930-973,1090-1115`; `AREA_BUDGET.md`; resource baseline; MAAP module/contract docs; public PR and author receipts; comparison scripts and focused documentation gates | R559-10 | 313616d1a18549d41907db389d378f0beb9bc543 |

## Pending manager duties and reproduction

The manager must obtain remaining independent exact-head acceptance and close
all review rounds, accept exact-head hosted and local workflow evidence, then
construct and validate the final merge candidate against current dev.
The assignment supplies source comparison base `c6bd08c6` and merge-turn dev
reference `6c810c45ac4ac7d5b45797430753020c9ea31d86`. These differ from imported
`e81ce82f`, used by the author measurements. No final current-dev candidate,
manager source bank or manager merge-bank success is claimed here. Publish
candidate builder/native receipts at the merge turn. Merge authorization,
containment, issue/project completion and separately assigned bench acceptance
remain manager duties. Carry prose residues forward; suggestions remain optional.

Scripts accept repository and packet paths. Initialize the three required
submodules at their pins. Create `scratch/docs-env` with the hash-locked
`tools/markdown/requirements.txt` and PyYAML, then run from this packet:

```sh
python3 scripts/composition.py "$SOURCE"
python3 scripts/run_focused.py "$SOURCE" "$PACKET" --jobs 3 --verilator "$VERILATOR"
python3 scripts/run_nxn.py "$PACKET" "$VERILATOR"
python3 scripts/run_static.py "$SOURCE" "$PACKET"
python3 -I scripts/record_vs_lane_routes.py "$SOURCE" 313616d1
python3 -I scripts/check_plan_composition.py "$SOURCE"
python3 scripts/lane_records.py "$SOURCE"
python3 scripts/audit_public_evidence.py "$SOURCE" "$PACKET"
python3 scripts/verify_tree.py "$SOURCE"
```

The evidence audit needs the public `dd8350f0` object fetched in SOURCE.
Review logs normalize local/compiler paths; unnormalized originals stay under
`scratch/`. Author receipts retain their published bytes. `MANIFEST.sha256`
enumerates publishable files relative to this packet; `scratch/` is excluded.

R559-10 FINISHED
