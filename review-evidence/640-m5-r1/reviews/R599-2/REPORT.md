[R599] POSITIVE - exact head c0cba330fd485e52fcb90d5ccc69169edf9f0c2b

R599-2, external independent delta review of issue #640 / PR #722, M5.
Tree: `bd80ea775d965f843609b1282cce9920279c02f0`.
Source base: `e8454e2751d05b02ee8e5a571857589ab358ab86`.
Round-one head: `988ec7f653d0a21e0f7b40b03b8c74155d8962cf`.

All five lenses are CLEAN for this source delta. No BLOCKER, MAJOR or MINOR
finding remains open. The previous measurement-scope and attribution findings
are resolved in the current public text. All three wording residues are applied.
The alternate-placement suggestion remains optional and unexecuted. This
verdict is not merge authorization or completion of umbrella issue #640.

I reconstructed the contract from AGENTS.md, CONTRIBUTING.md, docs/README.md,
the issue body and public scope decisions, requirements and interfaces, the
full source-base diff and history, then the published author evidence. I wrote
my independent assessment and ledger before reading prior public findings.
No private author material or another reviewer's local report was read.
Public start: https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6105579742.

The governing scope is [M5 assignment 6098404907](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6098404907)
and [round-two assignment 6105372796](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6105372796).
The estimated 600-LUT saving is not a claimed result. The frozen contract
preserves the ABI, access semantics, snapshots and bus contract and requires
honest measurement. D7 leaves re-recording to M9; D8 keeps the 38,040-LUT
target and assigns the planning update to the week-four re-measure.

The three new commits change only `docs/design/MARK_II_AREA_PLAN.md` and six
comment lines at `hdl/common/csr/milan_csr.sv:1066`. No rebase or amend occurred.
The RTL still has 3,225 lines, and its comment-stripped bytes are identical.
The independent pass also examined the original restructuring, SNAP kinds,
frozen reference, generated lockstep top, harness, mutants, reader disposition
and module documentation. `receipts/history.txt` and `receipts/delta.diff`
record the history and round-two delta.

**Prior finding dispositions.** The
[R599-1](https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6105370578)
and [R598-1](https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6105288411)
public findings were read after my independent assessment was written.

- **R599-1-F1: MINOR; Conformance, Docs; RESOLVED.** Artifact:
  `MARK_II_AREA_PLAN.md:1023`. The former non-reproduction claim mixed scopes,
  understating the planning basis. The corrected text distinguishes #649's
  in-datapath fit from standalone and integration-proxy measurements.
  `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:647` excludes tracked
  8x8 from the N=1,2,4 fit; line 657 gives 210.6 LUT/stream. Published HANDOFF
  tables give base slopes 83/7 = 11.86 and 436/7 = 62.29, and M5 slopes
  344/7 = 49.14 and 392/7 = 56. These support the new rounded figures.
  Required outcome: scope-labelled numbers without a reproduction claim.
  Verification: current text, `receipts/measurement-check.txt` and passing
  documentation gates. The required outcome holds.
- **R598-1-F1 = R599-1-F2: MINOR; Docs; RESOLVED in current public attribution.**
  Artifact: PR body, Description, "Saving against the plan", captured in
  `receipts/pr-body-at-review.md`. `syn/ooc/pp_resource_gate.py:255` and the
  baseline scope tree place `u_pp` inside the wrapper. The corrected parts
  are CSR -121, wrapper -342, and elsewhere -227: total -690. The nested
  `u_pp` -344 is explicitly not added. Outside-CSR movement is -569, not
  -686; only CSR is credited. This removes double counting and the hidden
  residual. Required outcome: disjoint parts reconciled to the total.
  Verification: the current PR body and `receipts/measurement-check.txt`.
  The [public round-two correction](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6105430562)
  states the same correction for HANDOFF sections 5 and 7. The supplied
  immutable round-one HANDOFF still contains old wording. I did not inspect
  the unpublished revised HANDOFF and do not certify its bytes. When
  publishing it, use the corrected version and identify the historical
  snapshot as superseded for attribution prose.
- **R598-1-S1: SUGGESTION; Docs; RESOLVED.** The manager made its outcome
  required for round two. Artifact: `MARK_II_AREA_PLAN.md:1027`.
  Substituting measured 121 for planned 600 gives 37,957 + 479 = 38,436,
  396 above 38,040. Required outcome: state this planning consequence.
  Verification: exact arithmetic and the new sentence, including D8's
  week-four qualification.
- **R599-1-RES-1: RESIDUE; Docs; RESOLVED.** Artifact: `milan_csr.sv:1066`.
  The obsolete four-way-select description is replaced by the requested
  "stage 2 (an OR of the two stage-1 words since lane M5 of #640) loads
  r_data a cycle later on rd_pend2", reflowed without changing line count.
  The banner now matches the implementation. Verification: source diff,
  comment-only check and identical netlists.
- **R599-1-RES-2: RESIDUE; Docs; RESOLVED.** Artifact:
  `MARK_II_AREA_PLAN.md:538`. Exact fix applied: "M5 saved 121 LUTs routed
  and 127 post-synthesis in its scope". This distinguishes saving from size.
  Verification: current line and diff.
- **R599-1-RES-3: RESIDUE; Docs; RESOLVED.** Artifact: PR body's CSR test row.
  Exact fix applied: "byte for byte apart from the module name".
  Verification: the frozen reference equals base `e8454e27` after only
  module-name normalization (`receipts/delta-check.txt`).
- **R599-1-S1: SUGGESTION; RTL, Docs; RETAINED, optional.** Artifact:
  `PP_SHADOW_BASELINE_RECIPE.md:142` and published route evidence. Two
  alternate placement directives could characterize the +0.299 to +0.097 ns
  WNS movement. The fall is 0.202 ns; +0.097 exceeds both the +0.030 absolute
  floor and +0.049 baseline-relative floor. Optional outcome: additional
  sensitivity evidence from the same synthesis checkpoint. Verification
  would compare full timing reports and recipe identities. It was not run
  here and does not leave a lens unclean.

No new finding or residue is raised in R599-2.

[R599] PASS Conformance - `REQUIREMENTS.md:126`, `REGISTER_MAP.md:150`, frozen
M5 scope, `MARK_II_AREA_PLAN.md:991`, `receipts/measurement-check.txt` -
REQ-CSR-01/02's ABI and snapshot obligations remain intact. Measurement scopes
and the partial-central consequence are explicit; the ultimate area target
is not claimed achieved. Published route evidence belongs to product commit
`1abe18eb`, whose logic is unchanged here, not to a newly executed route.

[R599] PASS RTL - `milan_csr.sv:1063`, `:2630`, `:2643`, `:2923`,
`receipts/delta-check.txt`, `receipts/netlist-compare.txt` - the comment
matches the OR stage. Original live/window precedence, zeroing of the unused
shadow operand and SNAP-kind capture remain sound. The N_LISTENERS_P guard
excludes an unreachable burst at N=1. The delta changes no port, clock,
reset, CDC, width or handshake. Comment-stripped source, lowered source,
generic netlist Verilog, netlist JSON and statistics compare identically.

[R599] PASS Robustness - `sim_lock.cpp:435`, `:459`, `:485`, `:603`, `:647`,
`receipts/csr-suite.log` - applied reset-during-read, unaligned/unmapped
address, invalid stream index, repeated listener/talker SNAP, stale/torn
snapshot and random-backpressure lenses. Both shipping lockstep shapes have
zero mismatching cycles; legacy feature-enabled/disabled legs pass. Engine
ports use a model, so these are bounded simulation observations.

[R599] PASS Tests - CSR `Makefile:79`, `gen_lockstep.py:90`,
`lock_mutants.py:50`, `sim_lock.cpp:713`, `receipts/csr-suite.log` - the
oracle is the digest-checked frozen base and every output is compared.
All seven planted defects fail their required named checks; the clean control
passes. Every mutation anchor still occurs exactly once and both exact-text
consumers are unchanged. No tracked or on-disk `tb/**/*.patch` file exists in
this checkout. Random-traffic grading still requires completed reads.

[R599] PASS Docs - `MARK_II_AREA_PLAN.md:538`, `:1023`, `:1027`,
`hdl/common/csr/doc/milan_csr.md:156`, current PR body, public round-two
correction, `receipts/docs-final.log` - measurement claims reconcile with
the public tables and D7/D8. The module page's OR stage, SNAP kinds and
unchanged three-cycle read timing match RTL. All 22 documentation and
source-structure commands passed at this head.

**Executed evidence.**

| Check | Result | Reproduction and receipt |
|---|---|---|
| Fresh complete CSR suite, initialized pinned submodules | rc 0; 1,815 checks, 0 failures, including mutations | `scripts/run_verified_csr.sh`; `receipts/csr-suite.log`, `.rc` |
| 1x1 lockstep | 5/5; 340,861 cycles; 28,167 random reads; zero mismatches | same suite log |
| 8x8 lockstep | 5/5; 374,265 cycles; 22,750 random reads; zero mismatches | same suite log |
| Wrong decode, torn snapshot, two stale snapshots, reset drift, two stage-1 claim defects | Seven named catches and passing control: 8/8 | same suite log |
| Banner delta, generator/campaign anchors, frozen reference | PASS; six comment lines replaced; seven anchors exact once | `scripts/check_delta.py`; `receipts/delta-check.txt` |
| Focused standalone lowering and generic synthesis before/after | Four commands rc 0; lowered source and both netlist formats byte-identical | `scripts/netlist_compare.sh`; `receipts/netlist-compare.txt`, `.rc`, `netlist-before.log`, `netlist-after.log` |
| Docs with/without Git; em-dash/style/gPTP/TOC checks and controls; anchors/paths/matrix; idiom, hygiene, naming, fail-fast, ownership, test evidence, port/source lists; diff whitespace | 22/22 commands rc 0 | `scripts/run_docs.py`; `receipts/docs-final.log`, `.rc` |
| Root and test-clone blob bytes, modes, index and required gitlinks | PASS | `scripts/verify_tree.py`; `receipts/integrity-before.txt`, `test-input-integrity.txt`, `integrity-final.txt` |

The pinned simulator identified as Verilator 5.050; launcher SHA-256:
`905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`.
The fresh suite used GNU make 4.4.1, `make -j16`, with at most two compiler
jobs per independent suite build. The campaign has no `--jobs` option and
builds mutants sequentially. Focused generic synthesis used sv2v 0.0.13 and
Yosys 0.66 with the shipping 1x1 shape include and default module parameters.
It proves this comment edit neutral, not shipping route/timing equivalence.

Disposable trees, builds and mutation temporaries are confined to `scratch/`.
The resumed session's archive-based suite run was superseded by a fresh
detached clone with pinned, registered submodules and verified input bytes.
Complete command outputs are retained with local path prefixes normalized
for publication. `receipts/log-provenance.json` records original and published
digests. No result, count or diagnostic was removed. Only REPORT.md and the
files explicitly listed in MANIFEST.sha256 are publishable.

**Reviewer-owned completion ledger.** This covers the reviewed source delta;
it does not claim validation of the pending merge candidate or release.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | M5 scope; REQ-CSR-01/02; REGISTER_MAP.md:150; MARK_II_AREA_PLAN.md:991; measurement-check.txt | R599-2 | c0cba330fd485e52fcb90d5ccc69169edf9f0c2b |
| RTL | CLEAN | milan_csr.sv:1063,2630,2643,2923; delta-check.txt; netlist-compare.txt | R599-2 | c0cba330fd485e52fcb90d5ccc69169edf9f0c2b |
| Robustness | CLEAN | sim_lock.cpp:435,459,485,603,647; csr-suite.log | R599-2 | c0cba330fd485e52fcb90d5ccc69169edf9f0c2b |
| Tests | CLEAN | CSR Makefile:79; gen_lockstep.py:90; lock_mutants.py:50; sim_lock.cpp:713; csr-suite.log; delta-check.txt | R599-2 | c0cba330fd485e52fcb90d5ccc69169edf9f0c2b |
| Docs | CLEAN | MARK_II_AREA_PLAN.md:538,1023,1027; module page:156; current PR body; public correction; docs-final.log | R599-2 | c0cba330fd485e52fcb90d5ccc69169edf9f0c2b |

**Real limits and pending manager duties.**

The [published author packet](https://github.com/kebag-logic/milan-fpga/tree/648503cfeee36d03d7baf2a7b8608e1310caae49/review-evidence/640-m5-r1)
and public REVIEW READY comments supply broader source-gate and route receipts.
I verified the HANDOFF's published digest and measurement arithmetic, without
reproducing physical implementation. No full parent, processor, gPTP,
synthesis or builder bank, route, hardware work, local hosted-workflow replica
or merge was run here. There is no manager source bank at this exact head;
none is claimed or inferred.

The exact-head hosted snapshot (`receipts/hosted-jobs.tsv`, `hosted-steps.tsv`)
shows executed success for `rtl-fast`, its lint, elaboration, firmware and BDD
jobs, all three docs contexts, `elaborate`, Yosys shards 0-3, and Verilator
shards 0 and 3. Verilator shards 1, 2 and 4 were still running. Physical gPTP
was skipped with zero steps. Physical calibration was NOT RUN; field and
physical skips are not hardware proof. The manager owns hosted/act acceptance,
including required aggregates; this snapshot does not clear that duty.

At the merge turn, the manager must construct the current-dev candidate,
validate it with the builder and native banks and publish the receipts.
The source base differs from live dev
`ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5` at this snapshot. No candidate
result is asserted here. Complete the independent review bar, ensure no
round remains in flight, obtain maintainer merge authorization, and perform
post-merge containment before marking the lane complete.

Publish the corrected HANDOFF with a supersession link, mark RES-1..3 applied,
and carry the optional placement suggestion without making it blocking.
The measured 121-LUT saving remains below estimate; cumulative scenarios
await D8's week-four update. The selected-split route remains at M0s STOP;
8x8 integrated synthesis was not completed in the author's measurement.
Post-merge boot readback and physical release obligations remain separate.
M5 does not close the umbrella issue's final area target.

R599-2 FINISHED
