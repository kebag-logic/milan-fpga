# [A345] Round 2 handoff

Candidate: `5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e` on `502-pending-live-write`.
The requested author work and local validation are complete.
Independent re-review remains required; no review verdict is asserted.

Issue: [#502](https://github.com/kebag-logic/milan-fpga/issues/502).
PR: [#579](https://github.com/kebag-logic/milan-fpga/pull/579).
Assignment: [option (a), round 2](https://github.com/kebag-logic/milan-fpga/issues/502#issuecomment-5848417938).
Reviews: [R328-1](https://github.com/kebag-logic/milan-fpga/pull/579#issuecomment-5848360185),
[R329-1](https://github.com/kebag-logic/milan-fpga/pull/579#issuecomment-5848407513).

## Delivered changes

Round-2 commit `220c9d56d28073362c2e715b832482146f38e6b1` remains in history.
The resume adds exactly one commit:
`fix(nvm): preserve map write priority with minimal predicates`.
Its message has one subject line, no body and no trailers.

- `hdl/milan/milan_datapath.sv:4255` names the original input-map and
  output-map change conditions without changing either comparison.
  Phase 5 at line 4370 retains the original `if / else if` bodies and
  input-change priority. The shadow pulse combines the accepted beat,
  phase 5, matching context, reset release and either change condition.
- `KL_pp_shadow.sv:388,945` and all committed tests are byte-identical
  to `220c9d56`. The accepting-edge bypass and sticky pending input remain.
- `SAVED_STATE_MATERIALIZATION.md:131,227` and
  `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:968` describe the shared conditions.
- The earlier round-2 storage observer remains at
  `tb/verilator/pp_shadow/sim_main.cpp:292,304,324`.
  It observes live name RAM, input-map storage, output owners/clusters,
  and the capture map across every watched edge.
- Separate durable baselines still grade refused records at line 1456,
  duplicates at line 1469 and REMOVE at line 1477.
  Controls use port 0, stream 0, channel 0 and cluster 0 in both dynamic
  directions. The static output refuses before record validation.
- The explicit mutation campaign remains in `docs/testing/TESTING.md:268`.

## Priority and equivalence

`amap_edit_in_key_v_w` and `amap_edit_out_key_v_w` cannot both
be true for one record.
`milan_datapath.sv:4081-4082` clears both on every combinational evaluation.
Input validity is set only at line 4164 inside the input descriptor branch;
output validity is set only at line 4189 in its `else if` output branch.
The descriptor constants are distinct: `0x000e` at line 3651 and `0x000f`
at line 3884. There are no other asserting assignments.

`priority-probe.py` adds read-only observations in a scratch harness,
without forcing RTL or changing the committed tests:

| Fixture | Input-valid cycles | Output-valid cycles | Both true | Checks | Failures |
|---|---:|---:|---:|---:|---:|
| Static | 25444 | 0 | 0 | 175 | 0 |
| Dynamic | 25444 | 37673 | 0 | 266 | 0 |

The RTL establishes mutual exclusion generally; the probe corroborates it
over the command controls, including ADD, duplicate, refusal and REMOVE.
The delivered structure also preserves the base priority independently:
an unchanged input condition falls through to a changed output condition.
`verify-minimal.py` expands the two named predicates and proves that the
entire phase-5 block equals `104c8a54` after removing whitespace.
`receipts/resume-minimal-equivalence.log` records that comparison and
confirms the shadow and tests are unchanged from `220c9d56`.

## Area decision

Both forms were measured during this resume with
`syn/yosys/ooc.sh KL_pp_shadow milan_datapath`, default
`configs/generated/endstation_arty_current`,
`synth_xilinx -family xc7 -flatten`, Yosys 0.66 and sv2v 0.0.13.
Both commands returned zero. The original recipe substitutes only the two
frozen RTL exports from `220c9d56`; all remaining sources, pins and tools
are identical. The candidate uses the repository recipe directly.

| Top | Form | LUT | LUTRAM | LUT total | FF | RAMB36 | RAMB18 | DSP | CARRY4 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| KL_pp_shadow | 220c9d56 | 60846 | 6136 | 66982 | 30187 | 15 | 4 | 6 | 2104 |
| KL_pp_shadow | Delivered minimal | 60846 | 6136 | 66982 | 30187 | 15 | 4 | 6 | 2104 |
| milan_datapath | 220c9d56 | 91376 | 6640 | 98016 | 43475 | 17 | 20 | 15 | 3628 |
| milan_datapath | Delivered minimal | 89526 | 6640 | 96166 | 43475 | 17 | 20 | 15 | 3629 |

Keep the minimal form: it saves 1850 datapath LUTs, with unchanged LUTRAM,
FF, RAM and DSP counts; CARRY4 increases by one relative to `220c9d56`.
The earlier recorded `104c8a54` baseline is 97292 datapath LUT total,
43475 FF and 3629 CARRY4. Relative to that baseline, the delivered datapath
saves 1126 LUTs and retains every other reported resource count.
The standalone shadow remains 80 LUTs above that earlier baseline.
The baseline receipts predate the reboot; both compared forms above were
freshly measured. These are synthesis counts, without a timing claim.

`resume-area-results.json`, `resume-area-recipe.json`, `resume-inputs.json`,
command receipts and `resume-area-artifact-hashes.json` identify the inputs,
tools and results. `resume-area-original-recipe.sh` preserves the exact
original-form recipe adaptation.
Large generated artifacts stay in scratch; only sizes and hashes are saved.

## Reviewer scripts and oracle wording

All four supplied artifacts match public evidence commit
`07f5d026ab972eac7f5238f746358cce3ebaf62b` byte-for-byte.
The export is verified against the delivered commit: 911 superproject,
248 protocol-processor, 104 time-processor and 214 stream-library blobs.
The recorded inventory adapter answers only the Git-free export's HDL
inventory query from the immutable pin's verified 45-file list.

- R329 unchanged controls: dynamic 263 checks and static 173 checks,
  zero failures. M3 and M7 are killed in both legs; eight stale anchors
  are explicitly refused.
- R328 unchanged: delayed bypass, lost history and reset variants are
  killed in both legs; seven stale anchors are explicitly refused.
- The unchanged recorded author adapter changes only those old anchors,
  preserving every published replacement. All eight R329 and seven R328
  adapted variants are killed in both legs. Refusals and build errors
  are never counted as kills.
- M5/phase4 fails the named refused-record pending checks. M6 fails the
  named REMOVE durability and accepting-edge checks in both legs.
- R329's unchanged probe: 295 checks, zero failures. P3 reports SUCCESS,
  one mapping, zero marks, pending 0 and durable 1.
- The unchanged R328 patch is applied to its public `104c8a54` harness
  context and run against the delivered RTL. Its redacted include is
  resolved by a scratch header copy, without editing the patch.

The previous phrase "passes 138/193 checks" described two run totals,
not a passed/total fraction. The static leg passes all 138 checks;
the dynamic leg passes all 193 checks. Each reports zero failures.
Those totals include 10 static and 14 dynamic explicit
`ORACLE ... live change without pending` assertions. Every one passes;
no oracle check fails and no observed live change lacks pending.
The committed storage-transition observer is separately exercised by the
focused suite and mutation campaigns.

## Round-1 finding dispositions

These remain author dispositions awaiting independent re-review.
The reviewers' lens assignments are retained.

| Finding | Severity | Lens | Delivered evidence |
|---|---|---|---|
| R328-F1 | MINOR | Tests | Durable refused-record controls; M5/phase4 killed in both legs |
| R328-F2 | MINOR | Docs | Actual live-write sources and current latch named in materialization document |
| R328-F3 | MINOR | Docs | Explicit pending-mutant inventory and affected-file responsibility |
| R328-S1 | SUGGESTION | Conformance, Robustness | Option (a); actual change predicates shared with shadow pulse |
| R328-S2 | SUGGESTION | Tests | Unsaved interval begins at observed storage transitions |
| R329-F1 | MINOR | Tests, Robustness | Separate durable REMOVE baseline; M6 killed by named checks |
| R329-F2 | MINOR | Tests, Robustness | Refused-record controls in both dynamic directions and static input |
| R329-F3 | MINOR | Conformance, Tests, Docs | Durable duplicate controls and unchanged P3 show pending clear |

## Final validation

All final gates return zero; `completed-gates.md` lists every exact command.
The default sweep ran unsharded, all default chunks, on the delivered head:

```text
suites: 55   passed: 55   failed: 0   timed out: 0
checks: 2125319   in-suite failures: 0
```

The sweep declares four skips: unavailable AAF/AVTP and gPTP/802.1AS
field campaigns, plus their two results-freshness checks. Each contributes
zero to the tally; none supplies field or hardware evidence.

The focused suite reports 575 + 575 + 575 + 263 checks, zero failures.
The pending-mutant clean control passes and the late-mark variant fails
the named K10/K12 checks, including both REMOVE directions.
The full builder is rerun in both compiler modes with elaboration required.
Present mode also requires RV32 compilation. It reports one NOT RUN:
the historical placement-calibration fixture is unavailable.
Absent mode reports two NOT RUN arms: the deliberately hidden compiler
instruments and the same unavailable fixture. These omissions are explicit.
Lint passes its 90/90 ratchet; ports, naming, test-evidence, documentation
in Git and no-Git modes, em-dash, style, contents, anchors, paths, capture,
language idioms, wire accountability and diff checks all pass.
No-Git documentation intentionally omits Git inventory parity.
`default-sweep-artifacts.json` records every suite and preflight log.
The final tree audit verifies all tracked blob bytes and modes across
the lane and its three populated source submodules, and confirms a clean
tree and the single one-line resume commit.

Every command runs in the foreground, without a pipeline, from the physical
lane or its verified scratch export. The recorded gate runner applies a
43200-second timeout and prepends the scratch simulator wrapper and existing
documentation environment. The wrapper delegates to simulator 5.050 and
caps otherwise unbounded build parallelism at eight jobs.
The area recipe uses its recorded Yosys/sv2v versions.

## Handoff boundary

Firmware, CSR/configuration inputs, submodule pins and submodule sources
remain unchanged. The capture gate passes without remeasurement.
No hardware, push, PR edit, merge or delegated work was performed.
The original lane remained the only implementation checkout.
No review verdict or clean-lens ledger is claimed.
`PR-BODY.md` is a replacement body for later publication.
`REVIEW-READY.md` is the exact issue-comment payload.
Independent review, hosted checks and merge remain outside this resume.
