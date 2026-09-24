[A259] Issue #112 author handoff — REVIEW READY

Closes #112

Head: `73a5478784bd861f8c8d33c0d1619594390b9529`  
Branch: `112-stale-grant`  
Base: `939c143333d11e2378a514f1c7b6abd4c3259bfd`  
Commit subject: `Prevent SRP admission grants from using stale declaration slopes`

Implementation and assigned validation are complete. The working tree is clean.
The commit has one subject line, no body and no trailers. Independent review,
publication and merge remain outside this author handoff.

Scope was reconstructed from [issue #112](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/112),
its [assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/112#issuecomment-5816023315),
[parent issue #551](https://github.com/kebag-logic/milan-fpga/issues/551), and
[R296-1/R297-1 on PR #553](https://github.com/kebag-logic/milan-fpga/pull/553).
The archived probes were read from `551-review-evidence`, commits
`1e31f5e38e62575de912dee267136313fea38cba` and
`1dc193dd559acba2e20c4d428af99bbaa51ae9c1`, in a temporary read-only fetch.
That scratch repository and the baseline area source export have been deleted.

The change

- `hdl/srp/KL_srp_top.sv` strobes an internal invalidation mask on the exact
  accepted declare/withdraw edge, including identical re-declarations.
- `hdl/srp/KL_srp_admission.sv` clears the changed source's grant, invalidates
  its cached and in-flight slope validity, and restarts the partial admission
  round. A valid current slope must participate in a completed full round
  before admission can assert. Unrelated published grants survive the event.
- Both public top interfaces are unchanged, including parameters and ports;
  [interface-check.log](interface-check.log) records the comparison with base.
- `docs/architecture/10_srp_engine.md` section 6.3, the integrator guide, and
  public port comments describe freshness, latency, optimistic ACTIVE and
  aggregate sampling. The generated module matrix includes the new unit suite.
- `syn/ooc/srp_ooc.tcl` adds the default-shape area recipe with a sorted source
  list and the repository's existing part, clock and report settings.

Acceptance evidence

| Requirement | Evidence |
|---|---|
| Current-declaration slope only | Every-cycle unit assertions compare any grant's slope with exact arithmetic on the current declaration; cold refusal and rapid changes to both fields are covered. |
| Grow refused without a pulse; shrink admitted | Every source and phase at 1/2/3/5/8 sources; service-port cases use sources 0/1/7 and all eight sampling phases. Growth is 224 → 20000 bytes, shrink the reverse. |
| Latency measured | Accepted declaration is cycle zero. Shape 1: 4 cycles; 2: 4/6; 3: 6/9; 5: 5/10/15; 8: 8/16/24. The service-port suite independently measures 8/16/24 at the default shape. |
| Stale-evaluation mutant fails | Two-source control 5252/0; mutant 184 failures. Eight-source control 723046/0; mutant 4032 failures, including the named no-refused-grant-pulse assertion. Campaign 4/4. |
| ACTIVE and optimistic window | Real Listener Ready PDUs arrive just after service acceptance. The suite checks optimistic ACTIVE before the real grant, its full equation, and expiry after three completed rounds. |
| Granted and aggregate slopes | Unadmitted/pending sources publish zero. Invalidation holds the previous aggregate; partial sums are discarded; every completed unit round publishes the sum of grants. Settled greedy admission and refusal match the independent arithmetic oracle. |
| Interfaces and consumer | Both public headers match base; the two prescribed consumer checks pass at the exact head. |

The default grant latency is 80/160/240 ns at 100 MHz, or 160/320/480 ns
at 50 MHz, from accepted declaration. The bound assumes no further declaration
or withdrawal restarts the round. Request waiting time and Listener registration
latency are separate. The optimistic window remains a talker-FSM policy; a
consumer requiring confirmed admission uses ACTIVE AND the real grant.

Validation results

Every listed gate returned 0. Invocations ran in the foreground without piping
gate output. Exact commands, the final head, and return codes are in
[gate-ledger.json](gate-ledger.json).

| Gate | Result | Receipt |
|---|---|---|
| Complete processor bank | 33 suites; 739421 checks, 0 failures | [suites.log](suites.log) |
| Focused SRP integration | 735 checks, 0 failures | [srp-top.log](srp-top.log) |
| Admission shapes 1/2/3/5/8 | 683 / 5252 / 20053 / 123286 / 723046 checks; all pass | [admission-shapes.log](admission-shapes.log) |
| Stale-evaluation campaign | 4 checks, all pass; both mutants killed by assertions | [mutants.log](mutants.log) |
| HDL lint | 40 tops pass | [lint.log](lint.log) |
| Native portability and memory mapping | 35 tops; engine staging and total memory assertions pass | [native-portability.log](native-portability.log) |
| Explicit changed-SRP elaboration/check | Both tops pass | [admission](portability-KL_srp_admission.log), [SRP top](portability-KL_srp_top.log) |
| Documentation bundle | 41 diagram blocks, 18 waveform blocks, links and both matrices pass | [make-check.log](make-check.log) |
| Individual workflow documentation gates | Links, compliance matrix, waveform freshness, export staleness, module matrix all pass | [ledger](gate-ledger.json) |
| Historical figure gate | 46 builds; all measured figures agree | [nvm-figures.log](nvm-figures.log) |
| Whitespace and interface audit | Pass | [diff-check.log](diff-check.log), [interface-check.log](interface-check.log) |
| Parent source lists | 106 files; all four consumer lists complete | [parent-source-lists.log](parent-source-lists.log) |
| Parent consumer suite | 371 checks, 0 failures | [parent-pp-shadow.log](parent-pp-shadow.log) |

The native portability list remains unchanged because the parent records its
omissions. The two changed SRP tops were additionally checked directly. The
initial parent source-list failure from extending that native list is retained
in `parent-source-lists-initial.log`; the final receipts above supersede it.
No parent budget or source file was edited.

Area at the default shape

Same recipe for base and head: complete `KL_srp_top`, eight sources/eight sinks,
all ports present, `xc7a100tfgg484-2`, out-of-context synthesis, 10 ns clock,
post-synthesis hierarchical utilization. The ordered comparison returned 0
for both runs. Full settings and values: [area-comparison.json](area-comparison.json).

| Complete SRP engine | Base | Head | Delta |
|---|---:|---:|---:|
| LUTs | 7566 | 7334 | -232 |
| Registers | 10485 | 10464 | -21 |
| LUTs used as memory | 194 | 194 | 0 |
| RAMB18 | 1 | 1 | 0 |
| RAMB36 | 0 | 0 | 0 |
| DSP blocks | 2 | 2 | 0 |

The admission hierarchy measures 782 → 503 LUTs and 862 → 841 registers.
Whole-engine optimization also changes mapping in unmodified children; the
engine total is the area result, not an isolated gate-count estimate. The
post-synthesis timing reports show +1.302 → +1.083 ns slack under this recipe.
These are synthesis measurements, not routed timing or hardware evidence.
Reports: [base](area-base/util_hier.rpt), [head](area-head/util_hier.rpt).

Parent state and delivery

The designated consumer checkout remains at parent commit
`3eaee03f0c50522c4e4da8e12c771ec130a8c2f9`. Its only changed tracked path is
`protocol-processor`, whose clean detached checkout is the final head above
(previous checkout `a14ef8b4787b5309dd9ab472e82ae2b4a3fdbb72`). No parent commit
or push was made. [final-state.log](final-state.log) records the audit.

The processor source delta is also preserved as [CHANGE.patch](CHANGE.patch).
[PR-BODY.md](PR-BODY.md) is prepared. [REVIEW-READY.md](REVIEW-READY.md) is the
issue comment payload; its posting receipt is `review-ready-url.txt`.
No push, PR mutation, merge, delegated agent work or hardware action occurred.
No toolchain, SDK copy or environment was placed in this output directory.
The parent #553 licence/counter/PDU regression remains that lane's work; this
handoff proves processor grant freshness and the assigned consumer checks.
