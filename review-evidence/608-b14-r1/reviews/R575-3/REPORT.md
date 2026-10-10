[R575] POSITIVE - exact head 42399611fc2217014024f03f4ba0365fb072688c

# R575-3: external independent re-review of PR #709 (issue #608, lane B14), round 3

- Head `42399611fc2217014024f03f4ba0365fb072688c`, tree `75729d9482463bbc42eed313026c9cae9442026a`, source base dev `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.
- Delta under review: `d981b1cc..42399611`. That is one one-line commit with no trailers and the single parent `d981b1cc` (no rebase or amend). It changes only `docs/findings/B14_BENCH_5603C353.md` (+27/-14; `receipts/delta_d981b1cc_42399611.diff`). Across `5603c353..42399611`, five one-line commits add that page and change no other file. The gitlinks equal the base (`receipts/commits_and_scope.txt`).
- Evidence judged:
  - the author packet `review-evidence/608-b14-r1/author/` at archive commit `273764dfe9147f6749908358032ef397f785e05c`, extracted by SHA into a disposable tree;
  - 273764df changes no `author/` file outside `round2-recompute/` relative to the original packet commit `c848925d`.
  - Other reviewers' archives on that branch were not extracted.
- Verdict: **POSITIVE**. No BLOCKER, MAJOR or MINOR is open.
  - Both remaining finding classes from round 2 are resolved at this head: the FRAMES contract statement, and the public records.
  - One RESIDUE (R575-3-R1) and two SUGGESTIONs are recorded.

## Reconstruction (public state only)

1. AGENTS.md (sections 3, 6, 7 and 8) and the contract it points to for the review bar.
2. Issue #608 body, and the round-3 assignment (issue comment 6096487327). That comment freezes the round's scope:
   - state the FRAMES contracts as declared at the head;
   - make every cited record public under `review-evidence/608-b14-r1/author/round2-recompute/`, archived by the manager;
   - apply the residue;
   - touch no RTL.
3. PR #709 body at the head (the "Observations for triage" bullet, Evidence paragraph and Round 3 table).
4. The authorities cited by the delta: `KL_avtp_rx_monitor_ctx.sv`, `KL_crf_rx.sv`, `milan_datapath.sv`, `KL_talker_diag_ctx.sv`, `counters_contract_milan.feature`, `docs/reference/REGISTER_MAP.md` (`receipts/contract_excerpts_42399611.txt`).
5. The delta and history, then the archived packet.
6. Prior public findings R574-2 and R575-2, read only after my independent pass was recorded (`receipts/independent_pass_before_prior_findings.txt`).

## Findings

### R575-3-R1 RESIDUE: the round 2 recomputes paragraph attributes a round 3 record to round 2

- **Lenses:** Docs.
- **Where:** `docs/findings/B14_BENCH_5603C353.md:688` and `:697`.
  - `:688` reads "Round 2 added four recomputes."
  - The item 3 bullet under it cites `round2-recompute/outputs/ta_lv_vs_cycles.txt` for the `item3/cycles.tsv` agreement.
- **Evidence:**
  - The archived `round2-recompute/README.md` marks `scripts/ta_lv_vs_cycles.py` and its output `r3`, along with the input check and the rerun script.
  - The four round 2 recomputes the sentence counts are `ta_lv_recheck`, `final_vs_asfound`, `inventory_rows` and `slip_ledger`.
  - So the count is right, but a reader would take the cited agreement record as a round 2 product.
- **Impact:** provenance wording only. No figure, record, digest, verdict or clause claim changes. The record exists and reproduces (`receipts/round2_rerun.log`, `receipts/recheck_round2_records.txt`).
- **Exact fix:** after "Round 2 added four recomputes." at `:688`, insert: "Round 3 added the comparison with `item3/cycles.tsv` (`round2-recompute/scripts/ta_lv_vs_cycles.py`), the input check and the rerun script."
- **Verification:** re-read `:688-697` against the README's Round column.

### R575-3-S1 SUGGESTION: quote the ruling's own legality claim in the FRAMES observation

- **Lenses:** Docs, Conformance.
- **Where:** `:481`, which cites `KL_avtp_rx_monitor_ctx.sv:318-323`.
- **Suggestion:** those lines also say "Both readings are Milan-legal (the interval is implementation-specific, <= 1 s)" (`:320-322`). The feature's `:250-259` likewise reads the clause as bounding the interval from above only. Naming that claim beside the triage question at `:485` would give triage the repository's stated argument, as well as the law.
- Optional. The page asserts no departure, so this is not a defect.

### R575-3-S2 SUGGESTION: name the round 2 records' archive commit

- **Lenses:** Docs.
- **Where:** `:650` and `:690`, which say the `round2-recompute/` records were "added after `c848925d`".
- **Suggestion:** name archive commit `273764df` beside the folder's manifest digest.
  - The digest at `:691` already pins the content: it equals the archived file (`65636059...89dc`).
  - The archive-level `MANIFEST.json` at 273764df lists all 19 records, unredacted, with matching digests (`receipts/archive_manifest_round2.txt`).
  - So identity is not at risk. The commit only saves a reader a search of the branch history.

## Prior findings at this head

| Finding | Status at `42399611` | Evidence |
|---|---|---|
| R574-2-F1 = R575-2-F1 (FRAMES contract) | **RESOLVED.** `:475-485` and the PR body bullet now state that the AAF listener's per-PDU FRAMES_RX is the frame-total law declared at `KL_avtp_rx_monitor_ctx.sv:318-323` and implemented at `:627-630` (ruling of 2026-08-05), and that the header `:28-36` says at most one per interval, so the declarations conflict. The CRF listener is served by `KL_crf_rx.sv:233` ("intervals with >= 1 accepted PDU"), through GET_COUNTERS word 11 at `milan_datapath.sv:3701` (index select `:3686-3688`). FRAMES_TX matches `KL_talker_diag_ctx.sv:32-36`. The feature describes the Table 5.6 reading at `:194-201` and grades a per-frame FRAMES_RX as INFO at `:408`. The triage question at `:485` asserts no departure. Every cited line range was opened at the head. The implementation claim was also executed (see Tests) | `receipts/contract_excerpts_42399611.txt`, `receipts/rxmon_nx_*.log`, `receipts/mut_info_probe.log` |
| R574-2-F2 (nonexistent record) | **RESOLVED.** `item4/summary.json` is gone from the page, and the item 4 row at `:668` names `item4/short-summary-001-050.json` and `-051-100.json`, both present. All 64 backticked packet paths on the page resolve in the archive at 273764df. The planted control (the `d981b1cc` page) reports exactly the removed `item4/summary.json` as missing, with rc 1 | `receipts/cited_paths.txt`, `receipts/cited_paths_planted_d981b1cc.txt`, `receipts/removed_citation_and_bare_names.txt` |
| R574-2-F3 = R575-2-F2 (round 2 records not public) | **RESOLVED.** The records are archived at `review-evidence/608-b14-r1/author/round2-recompute/` (273764df) and cited by path; see the detail below the table. The archive commit is not named on the page; see S2, and the round 3 assignment, which had the manager archive after the commit | `receipts/round2_rerun.log`, `receipts/round2_rerun_tampered.log`, `receipts/recheck_round2_records.txt`, `receipts/archive_manifest_round2.txt`, `receipts/snapshot_privacy_scan.txt` |
| R574-2-R1 = R575-2-R1 (register map wording) | Applied at `:515`: "must be rendered "not supported" by software, never "0 errors"", which matches `REGISTER_MAP.md:482-484` | `receipts/contract_excerpts_42399611.txt` |
| R574-2-S1 (peer FRAMES_RX) | Applied at `:484`. `soak/summary.json` gives peer input 0 +57,599,253 and peer input 8 +3,599,953; per page `:447-448`, those inputs hold the DUT's AAF and CRF | `soak/summary.json` (archive) |
| Earlier rounds (R574-1, R575-1 findings and residue) | Stand, as the assignment directs. The delta does not touch their lines, except the item 3 and 8 record rows, which now add archived recompute paths | `receipts/delta_d981b1cc_42399611.diff` |
| R574-1-S1 = R575-1-S1 (findings index) | Open SUGGESTION, left to the manager | - |

R574-2-F3 = R575-2-F2 resolution detail:
- The folder's `MANIFEST.sha256` digest is `65636059407702a12a5f7e09c7d28e3858f16d9ad65f6ce3261cafd4cb6489dc`, as at `:691`. All 18 listed files verify, and the folder holds no unlisted file.
- `scripts/run_all.sh` reproduces all five packet-only outputs byte for byte, with rc 0. A scratch copy with one altered output byte returns rc 1.
- My own script, `scripts/recheck_round2_records.py`, confirms:
  - all 103 `raw-inputs.tsv` rows equal their cited raw-index lines;
  - the 101 item 3 captures total 89,799,919 B;
  - both snapshot copies hash to their `raw-index/soak.jsonl` digests;
  - the re-decode shows the DUT's Talker Advertise `Lv` in cycles 1, 2 and 42 only, 0.0390, 0.0951 and 0.3184 s after the bridge's `Lv`;
  - the bridge's `Lv` agrees with `item3/cycles.tsv` in 101 of 101 cycles, worst 0.498 us, and TA presence agrees in 101 of 101.
- The outputs reproduce the page's other recompute figures: 15 of 15 equal at the final read; 44 of 44 inventory rows, split 2/18/18/2/4; and 73 `SLIP_LB` frames.
- The snapshots carry no station address or entity identifier. The only 16-hex tokens are stream-format codes.

## Lens results (exact head `42399611`)

```text
[R575] PASS Conformance - docs/findings/B14_BENCH_5603C353.md:475-485 and the PR #709 body bullet vs KL_avtp_rx_monitor_ctx.sv:28-36,318-323,627-630, KL_crf_rx.sv:233, milan_datapath.sv:3686-3688,3701, KL_talker_diag_ctx.sv:32-36, counters_contract_milan.feature:194-201,250-271,393-408; peer FRAMES_RX figures vs archived soak/summary.json - every declared-contract statement matches its source at the head and no departure from a declared contract is asserted
[R575] PASS RTL - hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:318-323,627-630 (frx_add_r commit), hdl/ieee1722/crf/KL_crf_rx.sv:233, hdl/milan/milan_datapath.sv:3701 - the page's description of each listener's server and law matches the RTL; tb/verilator/avtp_rxmon NxN at the head 118 checks 0 failures, and reverting the FRAMES_RX commit to +1 fails 6 coalesced-law checks (receipts/rxmon_nx_rxbase.log, rxmon_nx_rxmut.log); no RTL file is in the diff
[R575] PASS Robustness - the evidence chain's failure paths: a missing cited record is detected (planted d981b1cc page, rc 1), a tampered archived output fails the archived rerun (rc 1), the raw inputs are tied line by line to the archived raw index (103/103), and archive MANIFEST.json covers all 19 round2 files unredacted; the diff adds no behaviour, so no design failure path changed (receipts/cited_paths_planted_d981b1cc.txt, round2_rerun_tampered.log, recheck_round2_records.txt, archive_manifest_round2.txt)
[R575] PASS Tests - tests/features/counters_contract_milan.feature 86/86 scenarios pass at the head, and grading a per-frame FRAMES_RX as FAIL instead of INFO fails exactly :408 (receipts/behave_counters.log, mut_info_probe.log); the round2-recompute rerun reproduces byte for byte and my independent recheck passes (receipts/round2_rerun.log, recheck_round2_records.txt)
[R575] PASS Docs - docs/findings/B14_BENCH_5603C353.md at the head, the delta and the PR #709 body: all 64 cited packet paths resolve at 273764df, the round2 manifest digest matches, and ten documentation gates return rc 0 (receipts/gates/rc.txt); R575-3-R1 is RESIDUE and S1/S2 are SUGGESTIONs, so none leaves the lens unclean
```

Documentation gates at the head, all rc 0 (`receipts/gates/`):
- `docs_check.py`: 0 findings, scrub self-test 23/23.
- `check_doc_style.py`: OK.
- `gen_toc.py --check`: OK.
- `gen_toc.py --verify-anchors`: 423 links reproduced.
- `check_em_dash.py --base 5603c353`: 0 findings over 704 added lines.
- `check_doc_paths.py`: 954 paths resolve.
- `check_baremetal_only.py --check`: 0 findings.
- `check_baremetal_only.py --selftest`: 700 arms pass.
- `git diff --check` against both `5603c353` and `d981b1cc`: clean.

Interpreters: the Markdown gates ran under the pinned `tools/markdown/requirements.txt` environment, and the bare-metal gate under a system interpreter with pyyaml (`receipts/gates/ENV.txt`). The pinned Verilator 5.050 identity was checked before use: it reports `Verilator 5.050 2026-07-01 rev v5.050`.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | page `:475-485`; the PR body bullet; `KL_avtp_rx_monitor_ctx.sv:28-36,318-323,627-630`; `KL_crf_rx.sv:233`; `milan_datapath.sv:3686-3688,3701`; `KL_talker_diag_ctx.sv:32-36`; the feature at `:194-201,250-271,393-408`; archived `soak/summary.json` | R575-3 | `42399611fc2217014024f03f4ba0365fb072688c` |
| RTL | CLEAN | the same RTL lines; the `tb/verilator/avtp_rxmon` NxN suite at the head and with the FRAMES_RX commit mutated; the diff contains no RTL | R575-3 | `42399611fc2217014024f03f4ba0365fb072688c` |
| Robustness | CLEAN | `scripts/cited_paths.py` planted control; the archived `run_all.sh` tamper control; the `raw-inputs.tsv` to raw-index tie; archive `MANIFEST.json` round2 entries | R575-3 | `42399611fc2217014024f03f4ba0365fb072688c` |
| Tests | CLEAN | `counters_contract_milan.feature` (86/86) and its INFO mutant; the NxN suite and its mutant; the round2 rerun; `scripts/recheck_round2_records.py` | R575-3 | `42399611fc2217014024f03f4ba0365fb072688c` |
| Docs | CLEAN (R575-3-R1 residue; S1, S2 suggestions) | the whole page at the head; delta `d981b1cc..42399611`; the PR body; ten documentation gates; the archived `round2-recompute/README.md` and `MANIFEST.sha256` | R575-3 | `42399611fc2217014024f03f4ba0365fb072688c` |

## Real limits

- **Raw files:** the raw item 3 captures are not public, so I could not re-decode them.
  - `ta_lv_all.txt` was checked for internal consistency, and against `item3/cycles.tsv` and the raw-index digests.
  - The round 3 claim that all 103 raw inputs were re-hashed is the author's. Publicly, only the two snapshot copies can be re-hashed, and they match.
- **Not ruled here:** whether the frame-total law conforms to Milan v1.2 Table 5.6, and which conflicting repository declaration governs. That is the page's open triage question.
- **Bench actions:** whether a bench action was made during round 3 cannot be checked from public state. The delta changes no measurement.
- **Hosted docs-check:** at `2026-10-10T10:43:57Z`, the exact-head hosted `docs-check` was still `in_progress`.
  - Executed with success: `rtl-fast`, `elaborate`, `bdd-conformance`, `changes`, `docs-check-no-git`, `full-ci-gate`, `wire-accountability`.
  - Skipped, not executed: `verilator-suites`, `yosys-portability`, their shards, `verilator-lint`, `yosys-elaboration`, `firmware-unit` and `Physical gPTP` (`receipts/hosted_check_runs_42399611.tsv`). I observed these runs; I did not accept them.
- **Hardware:** physical calibration was NOT RUN. Field skips are not hardware proof.
- **Source bank:** no manager source bank was run or inferred at this head. Source-head execution evidence is the author's published gate receipts, plus the focused checks above.

## Pending manager duties

- Carry R575-3-R1 to the residue checklist.
- R574-1-S1 = R575-1-S1: the findings index entry. R575-3-S1 and S2 are optional.
- Hosted and act acceptance, including completion of the exact-head hosted `docs-check`.
- Validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts: source base `5603c353`, live dev `e8454e2751d05b02ee8e5a571857589ab358ab86`.
- Merge only under explicit maintainer authorization.

## Clone state after the review

- The probes ran only in disposable trees under the packet's `scratch/`. The ignored `__pycache__` directories that test runs created in the clone were removed.
- `git status --porcelain --ignored` is empty.
- The index equals the HEAD tree, and all 1,233 worktree blob hashes equal the index.
- Modes match, and the five gitlinks equal the head (`receipts/clone_integrity.txt`).

## Publishable files

- `REPORT.md`, plus every file listed in `MANIFEST.sha256`: `scripts/` and `receipts/`.
- `scripts/run_all.sh` reproduces the checks from a clone at the head.
- Local paths in the receipts are written as `$PACKET`, `$CLONE` and `$HOME`.

R575-3 FINISHED
