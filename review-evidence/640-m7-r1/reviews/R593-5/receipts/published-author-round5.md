Source: https://github.com/kebag-logic/milan-fpga/blob/e2bf579edf1920f0e371cb64c50c9f314dea37d1/review-evidence/640-m7-r1/author-r5/HANDOFF.md

## Round 5

REVIEW READY under issue #640 comment 6163132636.
Parent: `4c5d70b50230fbd5da347852d39daf7f23b3df0b`. Donor: `e4869fd0c42889b2ac806587cc5c78afb1c33461` (unchanged).
The parent origin is the assigned HTTPS repository; the branch is `640-m7`.
Its merge base with the original base is `e8454e2751d05b02ee8e5a571857589ab358ab86`.
Both tracked trees and indexes are clean. No push occurred.
The donor root and origin were verified before donor Git inspection.

### Changes and disposition

| Change | File and line | Result |
|---|---|---|
| Provisional suite duration | `scripts/suite_shards.py:161,201` | `gptp_tables` is recorded at the required 1800 seconds and declared provisional |
| Added worker and overhead | `scripts/suite_shards.py:207,846` | Prior maximum overhead 115 seconds inserted before the dedicated worker; its landmark moves to 5 |
| Workflow capacity and evidence | `.github/workflows/rtl.yml:161,227,426` | Six workers, `milan_dp` alone on 5/6, aggregate requires six matching records |
| Contract and negative fixtures | `scripts/ci_events.py:1959,1974,2237,5261,5367,6144,6544` | Ownership, counts, dropped-worker and omitted-last-worker controls follow the six-worker shape |
| Current scheduler documentation | `docs/testing/TESTING.md:518`; `docs/testing/CI_WORKFLOWS.md:347,356,2684` | Current counts and examples match; historical five-worker measurements stay dated |
| Measured reach | `tb/verilator/gptp_tables/README.md:29,31`; `tb/verilator/gptp_tables/sim_main.cpp:15,20` | TX 25/256; results 2/8; thresholds and stimulus unchanged |

Step 1 commit: `fb4d30b1a491d2dddc5c98cf7d725c19f92841db`.
Step 2 commit: `90f75192f5771ad873eba45a391ba764da91af57`.
Step 3 commit: `4c5d70b50230fbd5da347852d39daf7f23b3df0b` advances the remaining stale-denominator fixture
at `scripts/ci_events.py:5402`, as the new-worker procedure requires.
The final CI contract/self-test and Python idiom gate pass again.
All three are new one-line commits with the configured identity.

R592-4-F1 and R593-4-F1 are implemented for re-review.
R593-4-F2 now agrees with fresh execution.
R592-4-S1 was optional: the inert historical ROM row is retained.
Earlier residues and suggestions remain assigned as the reviews describe.
No donor commit, RTL change, register change or budget exception was added.

### Timing and ownership

The untouched starting selector reproduces the missing-duration refusal (rc 1).
Adding only the mandated provisional duration reproduces the capacity refusal
(rc 1): workers 0..3 predict 4629, 4628, 4630 and 4730 seconds,
above the 4320-second bound. These are expected negative controls.

After adding the worker, predicted seconds are
`3746, 3746, 3746, 3747, 3747, 2877`.
The 120-minute timeout and 60 percent bound are unchanged.
All 63 default suites have complete, disjoint ownership.
`gptp_tables` appears exactly once, on 0/6; `milan_dp` is alone on 5/6.
The specialized owners remain `tsn_fuzz` on 1/6 and `chmap_capture` on 3/6.
The serial list remains the full lexical inventory.

Local measured components: clean build plus baseline 21.803 seconds;
stock 26-control campaign 402.903 seconds; limits check 0.032 seconds.
Their sum is 424.738 seconds. This is a sum of separate local executions,
not a hosted suite window or one end-to-end default-target measurement.
The committed provisional 1800 seconds comes from `suite_timeout`, as required.
After a successful published run, step 3 of the selector's procedure must
replace the suite duration and new-worker overhead with hosted measurements.
No publication or hosted execution was authorized here.

### Gate table

All final gates below returned zero. Gates ran directly with logs redirected,
without verdict pipelines. The simulation uses the pinned 5.050 compiler;
the fresh baseline uses GNU make 4.3, `MAKEFLAGS=w` with `-j8`, and
`VERILATOR_JOBS=2`. Static Python gates use CPython 3.12.3 with the existing
scratch environment's dependencies. Process-ownership tests use native Python
because the supplied 3.12.3 build lacks pidfd support.

| Gate / plain command | Result | Defect detected or evidence limit |
|---|---|---|
| `python3 scripts/suite_shards.py --selftest` | PASS | Missing/retired/zero durations, wrong provisional timeout, overload, wrong worker count, moved specialized owners, overlapping or incomplete ownership |
| `python3 scripts/ci_events.py --check` | 2175 items, PASS | Workflow/contract drift, including wrong worker count or aggregate record count |
| `python3 scripts/ci_events.py --selftest` | 3096 arms, PASS | Dropped sixth worker, stale denominator, stale `--expect`, widened dedicated ownership and tally/result loops omitting the last worker |
| `python3 scripts/ci_scope.py --selftest` | PASS | Scope/history changes that would skip required execution |
| `scripts/run_all_suites.sh --shard I/6 --list` for I=0..5, plus `--list` | PASS | Independent counter comparison detects missing, duplicated or renamed suites; specialized and dedicated owners asserted |
| Serial `run_preflight_gates` | 8/8 gates, PASS, 105.601 seconds | Exact function bodies loaded from the current driver; only its final `main` invocation omitted; no full sweep claimed |
| `make -j8 -C tb/verilator/gptp_tables run` | 36/36 twice | Consumer mismatch, missing activity/index/reset/depth coverage, wrong decode, incorrect one-valued declarations; actual run used verified input copies in scratch |
| `python3 tb/verilator/gptp_tables/mutants.py` | 26/26, PASS | Every original planted defect fails its named check, listed below |
| `python3 scripts/gen_one_valued_table.py` and `--check` | Both PASS | Stale generated one-valued table; generation made no change; reach table is handwritten |
| `python3 scripts/check_py_idiom.py` | PASS | Python ratchet violations, with unchanged budgets |
| `python3 scripts/check_cpp_idiom.py` | PASS | C++ ratchet violations, with unchanged budgets |
| `python3 scripts/docs_check.py` | PASS | Public hygiene and routing; 23 scrub and four routing controls |
| `GIT_DIR=/dev/null python3 scripts/docs_check.py` | PASS | Filesystem fallback; 22 scrub and four routing controls; Git inventory-parity arm explicitly skipped |
| `python3 scripts/check_em_dash.py --base 412e3f6c` | PASS | All 21 added Markdown lines, three pages; 339 planted controls |
| `python3 scripts/check_doc_style.py` | PASS | Documentation style gate; no new planted control |
| `python3 scripts/check_doc_paths.py` | PASS | 985 paths and ten line anchors; no new planted control |
| `python3 scripts/gen_toc.py --check` | PASS | Stale generated contents; no headings changed |
| `python3 scripts/check_hygiene.py --check` | PASS | Whitespace/encoding ratchets; unchanged budgets |
| `python3 scripts/measure_naming.py --check` | PASS | Unrecorded boundary naming findings; unchanged budget |
| `python3 scripts/measure_fail_fast.py --check` | PASS | Masked verdicts and discarded statuses; unchanged budget |
| `python3 scripts/measure_test_evidence.py --check` | PASS | Evidence ratchets and 63-suite scheduling contract; unchanged budgets |
| Final source/evidence audit | PASS | Exactly seven changed paths, 24 tested input files match final bytes, non-comment harness lines and runtime output identical, all controls present |
| `git diff --check` and tracked status checks | PASS | Whitespace defects or unintended tracked changes |

The serial preflight executes these unchanged gate commands:

```sh
python3 scripts/test_suite_cancellation.py
python3 scripts/suite_tally.py --selftest
python3 scripts/suite_shards.py --selftest
python3 scripts/check_merge_containment.py --selftest
python3 scripts/check_results_fresh.py --self-test
bash syn/yosys/check_list_hermetic.sh
python3 scripts/xvlog_gate.py --selftest
python3 scripts/check_merge_review_integrity.py --selftest
```

Their controls respectively detect cancellation/orphan/timeout failures,
false or unreadable tallies, scheduler omissions, false containment,
stale/unverifiable evidence (18 controls), non-hermetic top discovery,
use-before-declaration and replacement-reference populations, and invalid
review/closure claims (86 controls). These checks provide no actual merge,
review approval, full-suite or hardware verdict.

### Table defect controls

The campaign copied the original committed inputs before the documentation edit.
Only two whole-line C++ comments changed afterward. Its executable source,
26 mutation definitions, wrapper, declarations and RTL match the final head.
The repeated baseline's runtime output is byte-identical and all 24 declared
inputs in its scratch build match the final source. It reaches TX depth 25,
ledger depth 3 and result depth 2, with 111 writes behind a waiting result.

| Planted defect | Named check that failed |
|---|---|
| `rx_fifo_wrong_depth` | `rx_fifo lockstep` |
| `rx_fifo_wrong_read_latency` | `rx_fifo lockstep` |
| `rx_fifo_lane_alias` | `rx_fifo lockstep` |
| `tx_fifo_wrong_depth` | `tx_fifo lockstep` |
| `tx_fifo_wrong_read_latency` | `tx_fifo lockstep` |
| `tx_fifo_count_alias` | `tx_fifo lockstep` |
| `tx_fifo_decode_odd_counts` | `tx_fifo decode` |
| `ledger_wrong_depth` | `ledger lockstep` |
| `ledger_wrong_read_latency` | `ledger lockstep` |
| `ledger_index_alias` | `ledger lockstep` |
| `results_wrong_depth` | `results lockstep` |
| `results_wrong_read_latency` | `results lockstep` |
| `results_index_alias` | `results lockstep` |
| `results_write_index` | `results lockstep` |
| `timer_wrong_depth` | `timer lockstep` |
| `timer_wrong_read_latency` | `timer lockstep` |
| `timer_index_alias` | `timer lockstep` |
| `rx_fifo_lane_stuck` | `rx_fifo values: lane` |
| `tx_fifo_count_stuck` | `tx_fifo values: count` |
| `ledger_type_stuck` | `ledger values: type` |
| `results_seq_stuck` | `results values: seq` |
| `timer_deadline_stuck` | `timer values: deadline` |
| `declaration_missing` | `ledger values: tag` |
| `declaration_wrong_value` | `ledger values: tag` |
| `declaration_many_valued` | `ledger values: type` |
| `declaration_stray` | `values: declarations that name no censused column` |

### Primitive, resource and route evidence

Round 5 changes no synthesized input. No new synthesis, route, hardware or
bench measurement was run. The following are historical M0s results from
base `e8454e27` to routed M7 `49e1ce48`; they do not qualify the merged tree.

| Storage | Historical before | Historical after |
|---|---|---|
| Tap and TX frame FIFO, each 256 beats | Each RAMB36 + RAMB18 | Each one RAMB36 |
| Ledger 8 x 21 | 168 FF plus mux | 4 RAM32M + 1 RAM32X1D |
| Results 8 x 89 | 712 FF plus mux | 16 RAM32M + 1 RAM32X1D |
| Timer 8 x 32 | 256 FF plus mux | 5 RAM32M + 2 RAM32X1D |

| M0s integrated metric | Base | M7 |
|---|---:|---:|
| LUT | 50267 | 49898 |
| FF | 54413 | 53220 |
| Slices | 15779 | 15773 |
| RAMB36 / RAMB18 | 74 / 27 | 74 / 25 |
| WNS / WHS, ns | +0.299 / +0.031 | +0.122 / +0.019 |

The historical resource gate passed the then-current record, every endpoint
met timing, and the route was complete. The isolated plane saving remains
107-253 LUTs, below the estimated 500 (300-700), plus 1149 FFs and one tile.
No re-record occurred; D7 reserves that for M9. The owner requires the daily
area measurement after merge to capture the integrated effect.

### Execution limits and attempts

No Makefile changed. Builds and mutation copies stayed in disk scratch.
At most two simulation builds overlapped; no route ran beside them.
The service's observed peak was 1629097984 bytes, below 9 GB.
No source or generated artifact was added to the repository by validation.
Pre-existing ignored build products were left in place.

Two initial CI-contract invocations lacked PyYAML in bare CPython 3.12.3
(rc 2). Both pass with the existing scratch 3.12.3 environment.
An initial final-audit helper mistakenly compared generated build metadata
with pre-existing ignored products (rc 1). Restricting that helper to the
Makefile's declared input inventory produced the passing 24-file audit.
The initial pre-commit em-dash call saw zero committed changes and supplies
no evidence for these edits; the final call grades all 21 changed lines.
Expected selector refusals above are negative controls, not final gates.

No full parent/donor suite bank, synthesis bank, builder bank, physical
calibration, hosted workflow or local workflow replica was rerun this round.
The Round 5 assignment requires the scheduler/preflight and focused evidence.
Prior bank and area evidence retains its original revision and limits.
Corrected-head reviews, hosted duration refresh, required contexts,
current-dev candidate validation, donor-before-parent merge ordering,
explicit merge authorization, containment and daily area measurement remain.

