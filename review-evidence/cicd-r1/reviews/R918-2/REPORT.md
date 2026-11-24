[R918] POSITIVE - exact head fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f

Round R918-2, external independent re-review of issue #998 / PR #1001. The corrected receipts support the revised measurement claims. R918-1-F1 and R918-1-F2 are resolved at this unchanged head. No new finding, suggestion, or wording residue was identified in the assigned correction delta. All five lenses were applied to that delta; unchanged source conclusions carry forward from R918-1. This independent verdict and ledger were written before consulting the other reviewer's report.

The reviewed head's tree remains `6aa4a42135fc7615a344aba1935eac8133bdf54b`. The source range is `300da99beed5bb1c77e4b04af0bb4f9369856e0d..fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f`, comprising three commits and twelve files. There is no source delta since R918-1. `receipts/source-delta.patch`, `source-history.txt`, and `tree-integrity.json` preserve that boundary. The evidence reviewed is the immutable [correction packet](https://github.com/kebag-logic/milan-fpga/tree/0a9f8c0a965ac5cdc1646d668fad7b147ed66857/review-evidence/cicd-r1/author-r1b) and the current [PR body](https://github.com/kebag-logic/milan-fpga/pull/1001), retained as `inputs/pr-body.md`.

Authority order: AGENTS.md and CONTRIBUTING.md; docs/README.md; [issue #998](https://github.com/kebag-logic/milan-fpga/issues/998), especially acceptance criterion 1; REQUIREMENTS.md REQ-VER-01 through REQ-VER-04; docs/testing/TESTING.md section 1 and CI_WORKFLOWS.md; source diff/history; published executable evidence. The issue API returned zero comments. The public review-start comments establish roles, including [R918-2's start](https://github.com/kebag-logic/milan-fpga/pull/1001#issuecomment-7131968414). No additional scope ruling was inferred. The assigned narrow re-review preserves all unchanged R918-1 conclusions and limitations.

Corrected measurements

Every reduction below is `100 * (1 - optimized / baseline)`. Ccache CPU figures use the receipts' **user CPU**, not wall time or user-plus-system CPU.

| Campaign/run | Baseline user seconds | New user seconds | User CPU reduction | Baseline/new wall seconds | Wall reduction |
|---|---:|---:|---:|---:|---:|
| crf_rx mutants, cold | 497.96 | 262.00 | 47.3853% | 376.75 / 247.31 | 34.3570% |
| crf_rx mutants, warm | 497.96 | 229.32 | 53.9481% | 376.75 / 219.48 | 41.7439% |
| avtp_rxmon, cold | 1587.52 | 547.52 | 65.5110% | 967.68 / 782.82 | 19.1034% |

Artifacts: `author-r1b/receipts/ccache/crf_rx-mutants/{nocc,cold,warm}.time:1` and `author-r1b/receipts/ccache/avtp_rxmon/{nocc,cold}.time:1`. The CRF PR values, -47% cold and -54% warm, round correctly. The correction's AVTP 65.5% is correct; the PR's -65% is a conservative integer summary, not nearest-integer rounding. No correction is required for that conservative presentation.

The three complete published CRF logs are byte-identical: **2,167 bytes**, SHA-256 `fb31108c8b99bdb2364aa1ce41f4bb772da6b9f66dd7733d61df51f458941f5b`. Each has 23 distinct PASS verdict lines: three clean controls returning zero, twenty mutants returning one, twenty corresponding named rejections, and `checks: 23 failures: 0`. Equality compares raw bytes with no sorting, masking, or line removal. The PASS token grades detection of each expected failure; a mutant's nonzero return is not treated as a failed campaign.

The corrected AVTP timing files are byte-identical to the original packet's mis-attributed `author/receipts/ccache/{nocc,cold}.time`. The correction changes their attribution, not their numbers. `cold.stats` identifies 378 hits in 528 cacheable calls. Full AVTP logs were not published; `logs.sha256` supplies hashes and sizes only. This round verifies the assigned AVTP timing claim, and does not claim a new full-output equality check for AVTP.

| Budget pair | Base L1d misses | -O3 L1d misses | Reduction |
|---|---:|---:|---:|
| Unsuffixed | 3,946,517,051 | 3,374,059,598 | 14.5054% |
| -2 | 3,741,671,160 | 3,411,296,019 | 8.8296% |
| -3 | 3,654,245,643 | 3,457,482,933 | 5.3845% |

Artifacts: `author/receipts/budget/base{,-2,-3}.perf:9` and `tbO3{,-2,-3}.perf:9`, event `L1-dcache-load-misses:u`. The revised PR statement, “L1d misses 5-15 % lower in three paired runs (median 8.8 %),” matches all three pairs. The unchanged CPU range also matches the retained task-clock pairs: 4.8655%, 2.6136%, and 2.5002%.

Prior finding dispositions

| Finding | Original severity and lenses | Disposition at this head | Evidence and required outcome |
|---|---|---|---|
| R918-1-F1 | MINOR; Conformance, Tests, Docs | RESOLVED | CORRECTIONS.md explicitly supersedes the mixed attribution. Separately named CRF and AVTP receipts reproduce their own figures; all CRF named campaign results match. The PR ccache row identifies the correction packet. No source change was required. |
| R918-1-F2 | MINOR; Conformance, Docs | RESOLVED | The six raw budget counters reproduce 14.5 / 8.8 / 5.4%; CORRECTIONS.md replaces the old claim and the live PR body contains the corrected range and median. |
| R917-1-F1 | MINOR; Docs, also Conformance as independently assigned to the same cause in R918-1-F2 | RESOLVED | Same L1d cause and independently reproduced correction as R918-1-F2; the original Docs assignment is preserved. |
| R917-1-S2 | SUGGESTION; Docs | RESOLVED | Separately named CRF timing files now exist and reproduce the claim, resolving the same attribution cause as R918-1-F1. |

The original report and index are historical evidence, not the current receipt map. CORRECTIONS.md names the mistaken paths and their replacements explicitly. This is a correction of measurement evidence, not a downgrade to wording residue. The independent [R918-1 review](https://github.com/kebag-logic/milan-fpga/pull/1001#issuecomment-7131233002) remains the covering round for unchanged source behavior.

After the independent verdict and ledger were written, the prior [R917-1 finding section](https://github.com/kebag-logic/milan-fpga/pull/1001#issuecomment-7131916838) was consulted. Its other items are retained below, without claiming they were fixed by an evidence-only correction. No additional review submissions or inline review comments were present in the retrieved snapshot. `receipts/independent-verdict-order.json`, `prior-public-findings.md`, and `prior-findings-reconciliation.json` retain the ordering and dispositions.

**R917-1-R1(a-f) | RESIDUE | Docs | RETAINED, original classification.** Authority/evidence: the original public finding and unchanged source/PR wording at this head. Impact: stale wording and references; no measurement or behavior change. Required outcome: apply these exact wording fixes on the manager's residue checklist. Verification: inspect the resulting text and confirm the edit changes no figure, executable statement, generated artifact, or requirement claim.

| Item | Artifact | Exact retained wording fix |
|---|---|---|
| a | `tb/verilator/crf_rx/sim_main.cpp:1382`, `:1392`; `tb/verilator/mmcm_servo/sim_phc_step.cpp:37` | Replace “(--public-flat-rw keeps every signal writable)” with “(probes.vlt makes these flops writable)”; replace “the rootp name --public-flat-rw exposes” with “the rootp name probes.vlt exposes”; replace “read through --public-flat-rw” with “read through probes.vlt”. |
| b | `tb/verilator/maap/probes.vlt:4` | Drop “see the Makefile”, whose target has no explanatory probe comment. |
| c | `tb/verilator/aaf_clock_meter/probes.vlt:4` | Replace the reader description with “sim_servo.cpp reads them; g5_v_r is also public through its RTL metacomment, which the meter build (sim_main.cpp) relies on”. |
| d | `docs/testing/TESTING.md:171` | Replace the exclusive-sounding mechanism with “makes public exactly those, in a `.vlt` such as the suite's `probes.vlt`”. |
| e | `docs/testing/TESTING.md:174`; changed probe/Makefile comments; `scripts/run_all_suites.sh:125`; `tb/verilator/ctrl_service_budget/build.py:778` | Add `(#996)` to the default-port hazard sentences and `(#998)` to speed-up reasons, as requested by the original finding. |
| f | PR Description, follow_ring/media_phase paragraph | Replace “a minimal reproduction and the bisect are in the evidence comment, and the hazard needs its own Issue” with “the minimal reproduction and bisect are retained in `review-evidence/cicd-r1/author/receipts/bisect/` and issue #996”. |

**R917-1-S1 | SUGGESTION | Tests, Robustness | RETAINED.** Artifact: original review's probe-control P3 and proposed `scripts/probe_check.py`. Authority/evidence: the public finding records a dropped read probe compiling and passing silently. Impact: future probe omissions can escape existing tests. Optional outcome: add a static harness-to-generated-scope probe check. Verification: a removed read probe fails that check while the present complete list passes. This round does not rerun P3 or expand the assigned scope.

**R917-1-S3 | SUGGESTION | Robustness, Docs | RETAINED.** Artifacts: `scripts/run_all_suites.sh:37` and docs/testing/TESTING.md's cache paragraph. Authority/evidence: the prior public unwritable-cache probe reports compile failure. Impact: a host with an installed but unusable cache fails closed. Optional outcome: document a writable `CCACHE_DIR` and the explicit `OBJCACHE=` opt-out in both places. Verification: inspect the documentation against the unchanged guard at `scripts/run_all_suites.sh:131`. No new cache-behavior claim is made here.

**R917-1-S4 | SUGGESTION | Tests, Robustness | RETAINED as manager follow-up outside this PR.** Artifact: published `author/receipts/ab/pub.follow_ring.verdict`, as cited by the original reviewer. Authority/evidence: the public finding reports exit zero despite 43 failing checks in an unadopted experiment; the sweep tally catches it. Impact: a direct suite caller could miss failures. Optional outcome: the manager tracks a separate issue for the suite's exit status. Verification: a deliberately failing check produces a failing suite exit. This round neither reruns the experiment nor treats it as fixed.

These carried-forward residue/suggestion items retain their non-blocking disposition. They do not change the independent correction verdict or clean-lens ledger. No new such item is raised by this round.

Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #998 AC1; CORRECTIONS.md; separately attributed CRF/AVTP timings; six budget counters; current PR measurement rows; `receipts/corrections-check.json` | R918-2 for corrections; unchanged source R918-1 retained | fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f |
| RTL | CLEAN | `receipts/source-delta.patch`, `source-history.txt`, `tree-integrity.json`; unchanged four probe lists and budget build rule; correction files affect no HDL, interface, clock/reset, or test expectation | R918-1 retained; R918-2 dependency/delta check | fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f |
| Robustness | CLEAN | Three CRF logs, all 20 named rejections, clean controls, zero-failure summaries; corrected timing attribution changes no timeout, malformed-input, ordering, reset, wrap, or cache-override behavior | R918-2 corrected-log check; unchanged behavioral coverage R918-1 retained | fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f |
| Tests | CLEAN | Raw three-way CRF byte comparison; 23 distinct verdicts and named rejections; `scripts/check_corrections.py`; corrected raw timings/perf counters and SHA-256 manifest entries | R918-2 for F1; unchanged paired-suite/probe evidence R918-1 retained | fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f |
| Docs | CLEAN | CORRECTIONS.md; current PR ccache and budget rows; historical mis-attribution explicitly superseded; unchanged TESTING.md:169-178 and source-comment delta | R918-2 for F1/F2; unchanged documentation R918-1 retained | fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f |

No new source comments exist in this evidence-only delta. The source-comment review from R918-1 is unchanged. All five lens conclusions above concern the assigned re-review; they do not certify completion of pending manager acceptance work.

Reproduction and integrity

Run `python3 scripts/check_corrections.py` from the published packet to reproduce arithmetic, raw-log equality, verdict counts, manifest checks, and current-claim reconciliation. Run `python3 scripts/verify_tree.py SOURCE_CLONE` to compare raw tracked blob bytes, file kinds/modes, and index entries against the specified head, with replacement objects disabled, including the five required initialized submodules. Both commands returned zero. Results are `receipts/corrections-check.json` and `receipts/tree-integrity.json`.

The final byte/mode/index audit passed for 1,966 superproject blobs and all required pins: protocol-processor `801ef2283ec793e35a2590fc6593c90313a64041`, gptp-processor `1616fc8f062fbf58c35ad31674b5b233207bbdb8`, verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`, tsn-c-stack `715589c1db7cf67e2f3259fd7083ebc7f0923376`, and lwSRP `08ee86e812a0eb5e1dc6cd61b494d8baf3491348`. Their 868 / 115 / 214 / 100 / 65 tracked blobs respectively also match. The unused external submodule remains uninitialized. No candidate source bytes or index entries were changed.

The examined receipt bytes match the packet's `published_sha256` entries at evidence commit `0a9f8c0a965ac5cdc1646d668fad7b147ed66857`. That commit contains no digital signature, and no signature artifact was found under the packet. Accordingly this report claims immutable-object and SHA-256 integrity, not cryptographic signer authentication. This does not alter the measurement conclusions.

Limits and pending manager duties

- This round recomputes retained measurements; it does not repeat performance campaigns or full build banks. It carries forward the exact-head R918-1 behavioral coverage. No new simulation or hardware result is claimed.
- The source base is the train head `300da99beed5bb1c77e4b04af0bb4f9369856e0d`, on `dev-soft-core`; it is not the final current-dev merge candidate. The supplied live-dev reference is `e275d7950ef3385753e6a15d2e191ba855b171ed`; current-dev must be refreshed at merge time.
- No manager source bank exists or is inferred at this head. Source execution evidence remains the author's published gate receipts and previously published reviewer probes. The manager owns final candidate construction, builder/native-bank validation, and publication of those receipts.
- Hosted/act acceptance and issue #998's all-jobs-under-30-minutes criterion remain manager duties. No hosted context was newly inspected or certified here; successful skipped contexts must not be called executed jobs. Local CPU ratios do not establish hosted durations.
- Physical calibration: NOT RUN. Field skips and simulation results are not hardware proof. No hardware, shared installation, source fix, commit, push, GitHub write, merge, author contact, sub-agent, Docker, or act operation occurred.
- The manager must reconcile both independent verdicts, finish exact-candidate and protected hosted validation, wait for every review round, obtain merge authorization, then perform post-merge containment and issue/project completion. This positive correction review is not merge authorization.

Only REPORT.md and files listed in MANIFEST.sha256 are publication artifacts. Scratch material is excluded.

R918-2 FINISHED
