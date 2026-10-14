[R593] POSITIVE - exact head 4c5d70b50230fbd5da347852d39daf7f23b3df0b

R593-5, external independent delta review of issue #640 / PR #713. Tree `8156e281ac181efc76139470e3cf5c530ae17793`; donor `e4869fd0c42889b2ac806587cc5c78afb1c33461` unchanged. No open BLOCKER, MAJOR or MINOR remains in the assigned delta. Earlier wording residues and optional suggestions are retained below. This is a source review, not merge authorization or completion of issue #640.

The governing [round-five decision](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6163132636) permits registration of `gptp_tables`, the necessary sixth worker, matching contract fixtures, and corrected reach descriptions. I reconstructed the repository contract, documentation map, issue body and public decisions, linked requirements/interfaces, source-base range and history, then the three-commit delta `412e3f6c8c402bce63e94c291d2782b5579aaa1d..4c5d70b50230fbd5da347852d39daf7f23b3df0b` and public executable evidence. Incoming dev and unchanged M7 implementation retain earlier review coverage. `receipts/independent-pass.md` records my verdict and all five lenses before I read any prior reviewer report or findings.

The source-base range starts at `e8454e2751d05b02ee8e5a571857589ab358ab86`; the earlier parent merge includes dev `fa8209889411e8ca95757174c981f720dbcd95a2`. The delta is exactly seven files and three commits (`receipts/delta.patch`, `delta-history.txt`, `source-range-map.txt`). It changes no RTL, donor gitlink, suite inventory, stimulus, assertion threshold, per-suite deadline, job timeout or headroom percentage. The harness executable lines are identical after excluding whole-line comments.

| Lens | CLEAN/UNCLEAN | Examined artifacts and result | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue decision 6163132636; `scripts/suite_shards.py:54-84,161,201,207`; `.github/workflows/rtl.yml:161,227,426`; `TESTING.md:514-525`. Required provisional timeout, additional worker, ownership and aggregate count agree. All assigned local checks return 0. | R593-5 delta, with unchanged scope retained from R593-4/R593-3 | `4c5d70b50230fbd5da347852d39daf7f23b3df0b` |
| RTL | CLEAN | `receipts/delta.patch`, `delta-checks.log`, `identity.log`; unchanged `hdl/` and donor gitlink; `tb/verilator/gptp_tables/sim_main.cpp:15,20` changes comments only. No new timing, reset, CDC, width or interface behavior. Fresh exact-source lockstep passes. | R593-5 delta; R593-4 covers the unchanged merged implementation | `4c5d70b50230fbd5da347852d39daf7f23b3df0b` |
| Robustness | CLEAN | `scripts/ci_events.py:5258-5303,5367-5411,6144,6439,6543`; `receipts/delta-checks.log` and `ci-selftest.log`. Missing suite duration, overload, stale denominators, missing worker, mismatched aggregate and widened dedicated ownership are rejected. | R593-5 delta; unchanged M7 controls retain R593-4 coverage | `4c5d70b50230fbd5da347852d39daf7f23b3df0b` |
| Tests | CLEAN | Selector self-test; CI check/self-test; exact serial preflight; six shell shard lists and serial inventory; fresh 36-check `gptp_tables` baseline; hosted evidence below. Controls still fail on their claimed defect. No suite dropped or renamed. | R593-5 delta | `4c5d70b50230fbd5da347852d39daf7f23b3df0b` |
| Docs | CLEAN | `docs/testing/CI_WORKFLOWS.md:347-374,516-519,2237,2684`; `TESTING.md:514-525`; `gptp_tables/README.md:29,31` and `sim_main.cpp:15,20`; generated one-valued table. Current scheduling and reach agree with execution. Earlier wording residues remain non-blocking under the owner rule. | R593-5 delta; untouched measurement/pin documentation retains R593-4 coverage | `4c5d70b50230fbd5da347852d39daf7f23b3df0b` |

Local executable evidence:

| Command or probe | Observed result | Receipt |
|---|---|---|
| `python3 scripts/suite_shards.py --selftest` | rc 0; provisional `gptp_tables=1800`; worker predictions 3746, 3746, 3746, 3747, 3747, 2877 seconds, each below 4320 | `receipts/suite-shards.log` |
| `python3 scripts/ci_events.py --check` | rc 0; 2,175 contract items | `receipts/ci-check.log` |
| `python3 scripts/ci_events.py --selftest` | rc 0; 3,096 arms | `receipts/ci-selftest.log` |
| Exact `run_preflight_gates()` from `scripts/run_all_suites.sh`, without invoking suites | rc 0; all eight gates; 102.484 seconds | `receipts/serial-preflight.log`, `serial-preflight/preflight/*.log` |
| `scripts/run_all_suites.sh --shard I/6 --list`, I=0..5, plus serial `--list` | 63 default suites, each exactly once; `gptp_tables` only 0/6; `milan_dp` alone 5/6; specialized owners unchanged | `receipts/shard-*.txt`, `serial-inventory.txt`, `delta-checks.log` |
| Independent negative controls | Removing the duration refuses; five-worker loads 4629/4628/4630/4730/2877 exceed the bound; stale job-name denominators 3, 4, 5 and 7 all refuse; worker/aggregate/ownership faults refuse | `receipts/delta-checks.log` |
| `make -j16 run VERILATOR=<verified-5.050> VERILATOR_JOBS=16` in a disposable verified input copy | rc 0; 36 checks, zero failures; TX depth 25, results depth two, 111 writes behind a waiting result; repeated runtime retained | `receipts/gptp-tables-runtime.log`, `baseline-inputs.sha256`, `focused-baseline.json` |
| `python3 scripts/gen_one_valued_table.py --check` | rc 0; generated limits table current | `receipts/generated-limits.log` |
| Raw identity audit after probes | 1,323 parent blobs and 1,046 initialized dependency blobs match bytes/modes/index; all six root gitlinks match; clean checkout | `receipts/identity.log` |

The 1,800 seconds is the prescribed default `suite_timeout` value, not a local timing measurement. Local component measurements are separately and accurately identified in the [author's published round-five evidence](https://github.com/kebag-logic/milan-fpga/blob/e2bf579edf1920f0e371cb64c50c9f314dea37d1/review-evidence/640-m7-r1/author-r5/HANDOFF.md#round-5): 21.803 seconds baseline/build, 402.903 controls, 0.032 limits. Their sum is not a hosted default-target window. The new worker's provisional overhead is the previous maximum, 115 seconds. The unchanged five-worker layout fails the capacity calculation, so step 2 requires six workers. The final fixture edit advances literal denominator 3 to 4 as the documented procedure specifies; both remain independently demonstrated refusals. No checker condition was relaxed.

The reach table is handwritten. `scripts/gen_one_valued_table.py:39-43,83-90` owns only the marked one-valued-column table; that generated region is current and unchanged. Both corrected reach descriptions agree with the fresh runtime without changing any threshold or stimulus.

Hosted evidence was read directly from [run 38529993870](https://github.com/kebag-logic/milan-fpga/actions/runs/38529993870), associated with published head `4c5d70b50230fbd5da347852d39daf7f23b3df0b`. The run checks out synthetic merge `85b959cb02bfa5b53978bbd1a479256963bbb388`, whose ordered parents are dev `fa820988` and this head. Its tree is exactly `8156e281ac181efc76139470e3cf5c530ae17793`, equal to the reviewed source tree (`receipts/hosted-merge-identity.json`). The full gate executed successfully with `run_full=true`.

| Hosted worker | Uploaded suites | Checks | Execution result |
|---|---:|---:|---|
| [0/6](https://github.com/kebag-logic/milan-fpga/actions/runs/38529993870/job/115739516717) | 8 | 1,677,584 | PASS; includes `gptp_tables` |
| [1/6](https://github.com/kebag-logic/milan-fpga/actions/runs/38529993870/job/115739516836) | 14 | 32,484 | PASS |
| [2/6](https://github.com/kebag-logic/milan-fpga/actions/runs/38529993870/job/115739516680) | 12 | 204,187 | PASS |
| [3/6](https://github.com/kebag-logic/milan-fpga/actions/runs/38529993870/job/115739516629) | 15 | 238,010 | PASS |
| [4/6](https://github.com/kebag-logic/milan-fpga/actions/runs/38529993870/job/115739516619) | 13 | 22,998 | PASS |
| [5/6](https://github.com/kebag-logic/milan-fpga/actions/runs/38529993870/job/115739516595) | 1 | 11,956 | PASS; `milan_dp` alone |

Every worker reports zero failures and zero timeouts. The [executed `verilator-suites` aggregate](https://github.com/kebag-logic/milan-fpga/actions/runs/38529993870/job/115763240226) passes, accepts six matching target-SHA records, and reports **2,187,219 checks, zero in-suite failures**. The independent artifact audit proves all 63 current default suite logs appear exactly once, on their selected workers, with the same target SHA (`receipts/hosted-audit.log`). This is executed evidence, not skipped status. The Yosys workers and aggregate also completed successfully; their acceptance remains the manager's. Physical gPTP was explicitly skipped and supplies no execution or hardware evidence.

`receipts/hosted-gptp-tables.log` contains the actual 36-check baseline and all 26 caught controls, each by its own named check. Every current mutation name appears exactly once. Its baseline runtime is byte-identical to the independently executed local runtime, SHA-256 `76a0b8c3987bbc59685a807b4cae776a9e8ac7e71fa7db3b5f75fdd5f1e4fc16`. It confirms TX depth 25 and result depth two with 111 writes behind a waiting result.

The successful hosted run now supplies step-3 measurements: **`gptp_tables` 572 seconds; added worker 4 overhead 81 seconds**. `receipts/hosted-measure-view.log` records the selector's own `--measure` result over the six documented `gh run view --log` inputs. The required replacements remain a manager follow-through; no source edit was authorized or made. An initial measurement attempt used raw API log formatting and was refused with rc 2 (`hosted-measure.log`); using the documented log format returns 0. That was a reviewer input-format error, not a source finding.


Prior public findings were read after the independent pass and explicitly reconciled. Findings from rounds one through three retain their accepted dispositions where their artifacts are untouched; this round does not claim fresh execution of those earlier campaigns.

The immediate findings are [R592-4](https://github.com/kebag-logic/milan-fpga/pull/713#issuecomment-6163086064) and [R593-4](https://github.com/kebag-logic/milan-fpga/pull/713#issuecomment-6163125428). Earlier finding bodies were read from their PR comments and are preserved in the [public review archive](https://github.com/kebag-logic/milan-fpga/tree/e2bf579edf1920f0e371cb64c50c9f314dea37d1/review-evidence/640-m7-r1/reviews).

| Prior item | Disposition at this head | Evidence |
|---|---|---|
| R592-4-F1, BLOCKER, Tests/Conformance; R593-4-F1, MAJOR, Conformance/Tests | Resolved in the assigned source delta | Required registration and six-worker capacity; selector/contract/preflight rc 0; 63 unique suites; hosted evidence above |
| R593-4-F2, MINOR, Docs | Resolved | README and harness now say 25 TX beats and two results; fresh 36-check runtime agrees; executable lines unchanged |
| R592-1-F1, MINOR, Tests | Remains resolved | Required depth-two check and result-write-index control unchanged; fresh runtime reports depth two and 111 writes behind waiting results |
| R592-1-F2 = R593-1-R-02, RESIDUE, RTL/Docs | Remains resolved | `KL_gptp_shadow.sv:236-242,258-261,877-879` retains corrected never-written/stale-word and beat-depth explanations |
| R592-1-F3 = R593-1-R-01, RESIDUE, Docs | Remains resolved | `MARK_II_AREA_PLAN.md:727-728` gives individual exclusions and the untaken timestamp-FIFO option |
| R592-1-F4, SUGGESTION, Tests | Remains resolved | Actual decode enables `00 01 03 07 0f 1f 3f 7f ff`; directed check and odd-count control unchanged |
| R592-1-F5, RESIDUE, Docs | Remains resolved going forward | Published later evidence distinguishes 33 engine, four gasket and three traffic-generator controls; original round-one prose remains history |
| R593-1-S-01, SUGGESTION, Tests | Remains resolved | Declared ledger tag value 1; fresh census confirms it |
| R593-1-S-02, SUGGESTION, Tests | Required disclosure resolved; optional per-segment coverage retained | `README.md:75-80` states cumulative coverage and #714; the underlying defect is not claimed fixed |
| R593-2-F1, MINOR, Tests/Docs | Remains resolved | All eleven consumer columns censused; tag/ok/gen declared at 1; generated table current; stuck/declaration controls unchanged |
| R593-2-S-01, SUGGESTION, Tests | Remains resolved | Tautological line absent; runtime prints actual decode enables |
| R593-2-R-01, RESIDUE, Docs | Remains resolved | Invalid detached branch checkout command absent from current PR body |
| R592-2-RES1, RESIDUE, Docs | Remains resolved | PR is ready; body no longer calls it a draft |
| R593-1-S-03, SUGGESTION, RTL/Robustness | Retained, explicitly pre-existing/out of lane | Lane guard still permits widths the classifier/gearbox cannot serve; manager routes to #495 |
| R592-2-S1, SUGGESTION, Tests | Retained, optional | Full-ledger write guard unchanged; ledger reaches three of eight entries |
| R592-3-RES1, RESIDUE, Tests/Docs | Retained | Overbroad reference-input independence sentence; exact fix below |
| R592-3-RES2, RESIDUE, Docs | Retained | Ambiguous unchanged-width sentence beside correct table; exact fix below |
| R593-3-R-01, RESIDUE, Tests/Docs | Retained | Makefile comment says two declaration controls; exact fix below |
| R593-3-S-01, SUGGESTION, Docs | Retained, optional | Donor M7 measurements still lack a direct evidence link |
| R593-4-D1, RESIDUE, Docs | Retained | Published PR body still describes the continuation as unpublished/local; exact fix below |
| R592-4-S1, SUGGESTION, Docs | Retained, explicitly optional | `syn/yosys/rom_digests.tsv` retains correct but inert donor `6b5a4282` row |

The retained findings below preserve their original IDs and lens assignments. They are not new defects or new requirements for this delta.

- **R592-3-RES1 | RESIDUE | Tests, Docs | `tb/verilator/gptp_tables/README.md:9-10`, `gptp_tables_wrap.sv:14-15`.** Evidence: result-reference `push_res_w` and `res_ok_w` depend on the converted ledger head, independently covered by the ledger lockstep. Impact: overbroad wording only; oracle and verdict unchanged. Exact fix: after “from signals the change did not touch”, append “except that the result queue's write strobe and `ok` bit come from the plane's resolution logic, which reads the ledger's converted head port; the ledger lockstep grades that port in every cycle the ledger holds an entry, which includes every resolution”. Verification: compare both sentences with wrapper lines 410-428; existing checks remain unchanged.
- **R592-3-RES2 | RESIDUE | Docs | `docs/design/MARK_II_AREA_PLAN.md:713`.** Evidence: the adjacent table correctly narrows stored widths from 74/73 to 69. Impact: ambiguous wording only. Exact fix: “Their function, depths and read latency are unchanged; only the two frame FIFOs' stored byte-enable fields narrow, as the table shows.” Verification: prose agrees with the existing table; no figure changes.
- **R593-3-R-01 | RESIDUE | Tests, Docs | `tb/verilator/gptp_tables/Makefile:62`.** Evidence: the executable list has four declaration controls. Impact: comment wording only. Exact fix: replace “and two wrong declaration” with “and four wrong declaration”. Verification: compare with `declaration_missing`, `declaration_wrong_value`, `declaration_many_valued`, `declaration_stray`; no test or verdict changes.
- **R593-4-D1 | RESIDUE | Docs | PR #713 Status, reproduction introduction, Known limitations.** Evidence: API head is published `4c5d70b5`, while the body still describes an unpublished continuation. Impact: publication wording only. Exact fix: use “REVIEW READY at the published parent and donor revisions listed above”; introduce reproduction with “Check out the published parent revision and initialize its pinned submodules”; qualify no-push/no-edit statements as implementation-stage history. Verification: read corrected wording against published heads. The manager carries this checklist item.

Retained optional suggestions and their verification:

- **R593-1-S-02 | SUGGESTION | Tests | `tb/verilator/gptp_tables/README.md:75-80`, cumulative coverage in `sim_main.cpp`.** Required disclosure is present; per-reset-segment checks still follow #714's fix. A future post-reset silence can pass cumulative coverage. Optional future outcome: grade useful activity independently after each reset; verify a silent segment fails by name. This round does not claim the underlying defect is fixed.
- **R593-1-S-03 | SUGGESTION | RTL, Robustness | `KL_gptp_shadow.sv:271`.** The classifier and gearbox assume 64-bit lanes. Optional outcome under #495: refuse unsupported widths or make those paths generic; verify supported/unsupported elaboration cases. No new delta impact.
- **R592-2-S1 | SUGGESTION | Tests | `KL_gptp_txret.sv:637`, suite README ledger row.** The unchanged full-ledger write guard has no full-ledger stimulus. Optional outcome: reach that boundary and kill a named guard mutation. Existing three-entry reach remains disclosed.
- **R593-3-S-01 | SUGGESTION | Docs | donor `docs/MANAGER.md:72-97`.** Its M7 figures lack a direct M7 evidence link. Optional outcome: link the published measurements; verify the link and revision. No changed figure or conformance claim.
- **R592-4-S1 | SUGGESTION | Docs | `syn/yosys/rom_digests.tsv:32`.** Correct digest for `6b5a4282`, a donor revision no parent commit pins, remains inert. Optional outcome: remove that historical row or retain it as allowed by the round-five ruling; verify the generated ledger and current pinned digest.

Limits and pending manager duties:

- This is the authorized delta review. Earlier M7 RTL and reset/traffic robustness coverage stand for untouched artifacts. The reviewer ran a fresh baseline and scheduling/contract probes, not full parent, processor, synthesis or builder banks. The 26-control campaign was not rerun locally here; its exact-tree hosted artifact was read directly and all 26 current mutation names were verified exactly once, in driver order. Local execution versions are recorded in `receipts/local-versions.txt`.
- The source evidence is the author's published gate record. Its public round-five handoff lists results, receipt sizes and hashes; underlying author raw logs are not in that directory. No manager source bank at this exact head is claimed or inferred.
- Selector step 3 still requires replacing the provisional suite duration and new-worker overhead with measurements from a successful hosted run. The manager owns that follow-through and subsequent exact-head evidence/review for any changed artifact; #737's broader rebalance remains separate.
- The manager owns hosted and local workflow-replica acceptance, donor-before-parent landing, required contexts, both independent verdicts and the no-review-in-flight check. This reviewer performed no hosted/local-replica orchestration or GitHub write.
- The final candidate must use then-live dev, not the original source base. The manager runs builder and native banks at the merge turn and links the receipts. Equality of a hosted synthetic merge tree and this source tree does not substitute for those duties.
- Historical area/timing measurements remain tied to `e8454e27` lineage and route `49e1ce48`. No synthesis, route, baseline re-record or physical measurement was performed. The post-merge daily #640 area measurement and containment remain manager duties. Issue #640's overall LUT target is not closed by this intermediate M7 review.
- Physical calibration NOT RUN. The physical hosted job is skipped on this PR; field skips are not hardware proof. The existing #714/reset-segment and full-ledger coverage limits remain disclosed, not cured by moving paperwork.

All commands were foreground commands; independent checks overlapped, with the one focused build capped at 16 jobs. Disposable input copies, builds and unfiltered local logs remain under `scratch/`, excluded from publication. No source fix, commit, push, merge, shared installation, hardware access, author contact or other-checkout edit occurred. `scripts/verify_identity.py` verifies exact bytes, modes, index and required pins after probes. The unused `external` checkout remains uninitialized with its gitlink checked.

Portable scripts and raw or explicitly selected command-output receipts are enumerated in `MANIFEST.sha256`, with packet-relative paths. The focused build's unfiltered compile log contains installation paths and stays unpublished; its raw runtime, source-input hashes, return code and timing are published. Hosted excerpts preserve selected output lines; full downloaded logs and archives stay in `scratch/`.

R593-5 FINISHED
