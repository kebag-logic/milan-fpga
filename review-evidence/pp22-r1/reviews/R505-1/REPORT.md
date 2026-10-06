[R505] POSITIVE - exact head 2139f3dc10161b456dfbd51d2f73a63f9164e041

Independent external review of issue #22 / PR #162, round R505-1. Tree: `b7d98916ed833c26c7f7d713964b16c10c36daa3`. Source base: `e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8`. No open BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION findings. This verdict covers the assigned source change and adoption patch. The deferred synthesis criterion and final integration acceptance remain with the manager.

The review reconstructed the supplied repository instructions, `docs/README.md`, public issue scope, linked requirements/interfaces, exact diff/history and then public executable evidence, in that order. No on-disk `AGENTS.md` or `CONTRIBUTING.md` existed in the checkout or searched ancestors, and neither file was tracked. The independent diff pass preceded the search for prior findings. No other reviewer's report or private author material was read.

The [issue](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/22), [assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/22#issuecomment-6008772151) and [review start](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/162#issuecomment-6009540943) bind pure declaration moves, unchanged statistics/suite records, complete source analysis, mutation planting and the parent ratchet. The [PR body's manager ruling](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/162) reserves `Synth 8-6901` measurement and issue closure for the next parent pin adoption. `Relates to #22` accurately preserves that boundary.

Behavioral authorities examined: `hdl/README.md`; both changed module banners; `docs/00_MILAN_COMPLIANCE_REVIEW.md` GAP-17; `docs/architecture/02_interfaces.md` §§2–3; `03_packet_engine.md` F03.6 and §5; `09_verification.md`; and both focused suite READMEs. These cover cancellation/response routing, timer/slot ownership, V1/V2/V8/V9/V10 validation, byte streaming and verification obligations. This change introduces no protocol or clause claim.

The reviewer-owned ledger is:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue/assignment/ruling; interface/packet-engine authorities; exact declaration-move proof; 46-file analysis; parent patch and budget | R505-1 | `2139f3dc10161b456dfbd51d2f73a63f9164e041` |
| RTL | CLEAN | `KL_pp_originator.sv:188–198`; `KL_pp_rx_validator.sv:232–233,385,615–682`; complete diff; three statistics pairs | R505-1 | `2139f3dc10161b456dfbd51d2f73a63f9164e041` |
| Robustness | CLEAN | Cancellation/sequence/inflight model and held-frame/drop contracts; five completed negative controls; two clean controls; base analysis failures | R505-1 | `2139f3dc10161b456dfbd51d2f73a63f9164e041` |
| Tests | CLEAN | Two suites at base/head; 277 patch checks and 199 exact-text plants; public 33-suite/17-consumer records; hosted job/step snapshots | R505-1 | `2139f3dc10161b456dfbd51d2f73a63f9164e041` |
| Docs | CLEAN | Documentation guide, banners, suite READMEs, public handoff, PR body, budget count and deferred-synthesis ruling; results/limits reconciled | R505-1 | `2139f3dc10161b456dfbd51d2f73a63f9164e041` |

The sole commit has the specified base as its parent and changes exactly two files, both still mode `100644`. `scripts/check_reordering.py` constructs the head from the base by moving the exact four declaration lines and existing separating blank line, then requires whole-file byte equality. The originator declarations precede their uses at lines 197–198. The intact validator FIFO/verdict groups precede the `vd_push_w`/`vq_full_w` use at line 385. All eleven declared names precede their uses. Module scopes, declaration types, drivers and widths remain unchanged; there is no initializer, port, register, parameter or executable-statement change. See `receipts/pure-reordering.json`, `exact.diff` and `history.txt`.

| Reviewer execution | Result | Receipts |
|---|---|---|
| Originator at base/head | Both 107 checks, 107 PASS, 0 FAIL; identical tally | `receipts/{base,head}-originator.log`, `.rc`, `focused-suites.json` |
| RX validator at base/head | Both 555 checks, 555 PASS, 0 FAIL; identical tally | `receipts/{base,head}-rx_validator.log`, `.rc`, `focused-suites.json` |
| Moved-line searches at both revisions | Eight fixed-text searches find no match in patch/Python tables | `receipts/planting.json` |
| Every tracked `tb/**/*.patch` | 277/277 pass `git apply --check` | `receipts/planting.json` |
| Notification/ACMP/D3 exact-text tables | 56 + 33 + 110 = 199/199 arms plant through their own `plant()` functions | `receipts/planting.json` |
| Originator controls | Four killed: highest-free selection, ignored sequence, retained cancel timer, shared sequence; 15/7/5/10 failing checks respectively; clean control passes | `receipts/originator-controls/` |
| Validator control | Held-AECP admission defect killed by four failures including both named F28 checks; clean control passes | `receipts/validator-control/` |
| All 46 derived HDL sources, separate package-first analysis | Head: every rc 0 and zero `VRFC 10-3380`/`10-8530`. Base: only originator/validator fail, each with one of each diagnostic, naming `cancel_hit_w`/`vd_push_w` | `receipts/{base,head}-analysis-table.json`, `analysis-summary.json`, `receipts/xvlog/` |
| Parent patches at `28f9666feab2b2ba287643c63ed3a16b1e0bb863` | 148 then 22 apply; 22 removes exactly two keys and changes count 2→0; the actual budget parser returns both sections empty | `receipts/parent-contract.json`, `parent-budget-after.txt` |

The parent's source generator independently derives the same ordered 46-file census as the published tables. Reviewer analysis reproduces both tables exactly. Plantability and mutation kills are separate claims: all 476 planting checks passed, but only the five listed defects were built and killed here. Each kill requires a completed simulation and named-check failures; build failure is not a kill.

All 16 files in the [pinned public evidence](https://github.com/kebag-logic/milan-fpga/tree/2e889399824b70f9ed9a20c53d925e61a617a976/review-evidence/pp22-r1) match its published SHA-256 manifest. Complete Yosys statistics were compared byte-for-byte, including cell-type counts and every reached parameterized module:

| Scope | Bytes per revision | Reached modules | Identical SHA-256 |
|---|---:|---:|---|
| `KL_pp_originator` | 2,045 | 1 | `102354aa0632d5ca1fa83cf6c72f36cdb3f6a9a2524c5dc55114d5ff87b52298` |
| `KL_pp_rx_validator` | 2,427 | 1 | `b48ab8257a5d01221d8df24ec2138e12f0572f385ef4f657a0427af7554a2dda` |
| `protocol_processor_top` | 47,371 | 43 | `c19429cb06a6aa5f47e0f4b5fd53ac4d5bd390ba1f4d83b752ccbc14a35793e6` |

The public handoff/integrity record enumerates identical base/head counts for all 33 suites: 1,021,651 checks and zero failures at each revision, including additional per-build tallies. Both reported complete-suite log hashes match. The snapshot contains these tables and hashes, not the two full suite logs; the reviewer directly checked the tables and reran the two affected suites. No full processor or Yosys bank was rerun. See `receipts/public-evidence-integrity.json`, `public-records-check.json` and `public/evidence/author/`.

The public parent record lists rc 0 for all 17 consumers at `28f9666f`, with the prescribed patches in order and the processor pin/index at this head. Its analysis gate reports zero findings across 73 parent and 52 processor sources. Its builder explicitly excludes one calibration arm because the reference physical report was absent. Simulation shape guards and field skips remain exclusions. Public parent Git trees confirm the timing-processor and AXIS pins in the execution receipt; the external leaf remains uninitialized. See `receipts/gitlink-crosscheck.json`. This review checked the patch/budget contract without rerunning the parent bank.

At the exact-head hosted snapshots, both workflows (`37415361289`, `37415356790`) have successful completed `docs-gates` and `portability` jobs; `suites` remains in progress. A simulator-build step is skipped and is not counted as executed validation. No workflow-wide success or final acceptance is inferred. The review assignment reports that the manager's source static/builder and native banks passed. The retrieved issue/PR timelines contain scope/review-start comments but no additional manager bank execution receipts; the assignment statement is not recast as reviewer execution. Raw API snapshots are under `public/`.

After the independent diff pass, the PR conversation, submitted-review and inline-comment endpoints were checked. At retrieval there were no prior public FINDINGS, no submitted reviews and no inline comments on PR #162. Its two conversation entries were review-start notices. There is no prior finding to retain or resolve at this head. No other reviewer's report was consulted. See `receipts/prior-findings.json`.

Limits and pending manager duties:

- This validates source against `e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8`, not the final current-dev candidate. The manager builds and validates that candidate at the merge turn; the assigned live-dev reference is `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`.
- The manager owns hosted/local-workflow acceptance, required final contexts, two independent positive reviews, integration and publication. In-progress work must complete, and skipped contexts retain their actual coverage meaning.
- No Vivado synthesis or implementation was run. The next parent pin adoption must measure `Synth 8-6901`; #22 closes only on that result.
- Physical calibration was NOT RUN. Field skips, simulation and shape guards are not hardware proof. No hardware was accessed.
- Full-bank evidence was audited rather than rerun. Equal statistics alone are not formal equivalence; the exact byte-move proof establishes the source-level invariance for this patch.

Every build and probe used disposable trees under `scratch/`; the source checkout was never edited. Independent work ran concurrently under foreground supervisors with explicit campaign job limits and `make -j16`, at most twelve compile workers. The scoped simulator identity was verified before use. Peak unit memory was 3,363,676,160 bytes under the 12,884,901,888-byte cap, with no OOM/limit events. No prohibited banks, GitHub writes, commits, pushes, merges, shared installations or other-checkout edits were performed.

The final direct check hashes all 556 tracked disk blobs with Git's blob framing, checks modes and compares the complete stage-zero index to the exact head, with object replacement disabled. Everything matches, with no untracked or ignored files. This processor checkout has no submodule gitlinks; the public parent pins were separately cross-checked. See `receipts/final-integrity.json`.

Portable scripts are in `scripts/`. In a fresh packet copy, run `focused_suites.py <clone>` and `check_planting.py <clone> --jobs 4`, then `check_parent_contract.py <clone>` to obtain the source census. `analyse_sources.py` and `run_campaigns.py` may run concurrently under a foreground supervisor. `check_public_records.py`, `check_reordering.py <clone>` and `verify_integrity.py <clone>` reproduce the comparisons. Set `REVIEW_VERILATOR` and `XVLOG` to override executable paths. Fresh-output scripts intentionally refuse reused scratch directories.

`MANIFEST.sha256` lists every publishable receipt and script using packet-relative paths. Only listed files and this report are for publication. `scratch/` is excluded.

R505-1 FINISHED
