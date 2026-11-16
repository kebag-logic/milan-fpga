[R846] POSITIVE - exact head 394612c55148b43354359daeab2aa88d4f019ec2

External independent delta review R846-3, issue #917 / PR #918. Tree `e10ca2a5920b466be5561dcbe323fb942043497f`; source base `cec88385ad0a0ec0d61b91597640797766e45010`; previous head `8f73ade54366cc832bad3386c8b6f3bbb12ca5e4`. The two commits (`9316395756`, `394612c551`) change 12 files, +286/-28. All five lenses are CLEAN. No open BLOCKER, MAJOR or MINOR remains. One wording RESIDUE and one retained publication-index SUGGESTION follow.

Reconstruction followed the operating contract, docs index, [issue #917](https://github.com/kebag-logic/milan-fpga/issues/917) and its public comments, [manager ruling item 2](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6894152131), [owner decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6898289590), requirements/interface authorities, full source-range diff/history, detailed delta and public receipts. My independent verdict and five-lens ledger were written before reading prior reviewer findings, which were then reconciled. No private author material, current-round reviewer report or management source bank was read.

## Findings

**R846-3-R1 - RESIDUE - Docs - Obsolete publication paragraph beside the current archive link.**

- Artifact: PR #918 Status, first of two consecutive `Author packets:` paragraphs; snapshot `public-pr-excerpts.txt`.
- Authority/evidence: the first says round-three receipts will join the archive when published. The next already links author-r1 through author-r3 at `887dbc64`, verified here.
- Impact: redundant, stale wording only; no measurement, figure, verdict, generated artifact, conformance, clause or privacy claim changes.
- Exact required outcome: delete the earlier paragraph beginning `Author packets:` with the author-r1/author-r2 link and ending `when published.` Keep the following paragraph linking author-r1 through author-r3 at `887dbc64`.
- Verification: one current archive paragraph remains. This does not make Docs unclean.

**R846-3-S1 - SUGGESTION - Docs - Regenerate indexes after publication redaction.**

- Artifacts: archived `author-r2/INDEX.md` and `author-r3/INDEX.md`; `receipt-audit.log`. In each, four indexed paths differ from their published size/digest: `receipts/workflows/logs/docs__docs-gates-1__gate_25_0.log`, `docs__docs-gates-2__gate_25_1.log`, `elaborate__elaborate-gates-0__gate_15_0.log`, `elaborate__elaborate-gates-1__gate_15_1.log`.
- Authority/evidence: all extracted files, including these, match `MANIFEST.json`'s `published_sha256`; the manifest records publication redaction. A valid content authority exists, but the secondary indexes are stale. This retains R845-2 S2 and records the same condition in author-r3.
- Impact: confusion when checking the secondary index, without establishing any changed execution verdict.
- Suggested outcome: regenerate the published indexes after the last transformation, or distinguish original and published digests explicitly. Preserve the transformation mapping.
- Verification: every published indexed file matches its recorded size/digest. Optional; no lens is unclean.

## Prior findings at this head

Sources: [R845-2](https://github.com/kebag-logic/milan-fpga/pull/918#issuecomment-6903179473), [R846-2](https://github.com/kebag-logic/milan-fpga/pull/918#issuecomment-6903058735), [R845-1](https://github.com/kebag-logic/milan-fpga/pull/918#issuecomment-6899723183), [R846-1](https://github.com/kebag-logic/milan-fpga/pull/918#issuecomment-6899591157). Original severities and lenses are retained below.

| Prior finding | Disposition and cause-level evidence |
|---|---|
| R845-2 F1, MINOR, Conformance/Docs/Tests | **Resolved.** `mailbox_margins.py:54-105` computes six cells from each stated row and its channel; `gen_mailbox.py:177-199` checks/splices them. `FR_NFR.md:425-439` describes this mechanism. My P1 changes refill 5 to 10: check rejects all three stale AECP rows; write produces 11 ms ingress and margins 208/218/208 ms, proposal margins 218/228/218 ms; ACMP is unchanged. Edited cells and zero/negative margins fail. Unchanged-head check/crosscheck/selftest and `ci_scope.py --selftest` pass. |
| R846-2 F1, MINOR, Tests/Robustness | **Resolved.** `held.py:42-77` and `grade.py:195-199` reject RXC while that channel holds a record and RXR stamped at/before its hold. Both exact review histories are refused by the public probe rerun here. All 13 held checks pass; removing either guard fails its own named check. Other-channel intervening and same-clock observations retain correct attribution. My additional boundary probes reject equal timestamps, accept the next clock and exact allowance limit, and reject one clock beyond the limit. |
| R845-2 R1 / R846-2 R1, RESIDUE, Docs | **Resolved exactly.** `suite.hpp:1648-1650` is the prescribed comment without B7/B8/B9 labels; executable check names remain. No new forbidden comment instance was found in this delta. |
| R845-2 R2, RESIDUE, Docs | **Resolved exactly.** The PR CPU-budget limitation now uses the requested base-versus-84d8a214 byte-identical-log explanation; see `public-pr-excerpts.txt`. |
| R845-2 S1, SUGGESTION, Tests | **Adopted.** Exact-head `budget/held-8x8/` receipt: two-interface 8x8, 5.31012 ms total, 4.98643 ms ingress, 6 ms allowance, 20 ms budget, zero refusals/misses and run rc 0. Recorded execution, not a fresh system simulation here. |
| R845-2 S2, SUGGESTION, Docs | **Retained as R846-3-S1.** Publication manifest matches; four secondary index rows differ in each published packet. |
| R845-2 S3, SUGGESTION, Docs | **Adopted.** `FR_NFR.md:444` and budget `README.md:396` explicitly explain that the measurement includes ingress and the separate held-margin subtraction is conservative. |
| R845-1 F1, MINOR, Tests/Robustness/Docs | **Remains resolved.** `suite.hpp:1652-1692` grades final-slot space, RX_DROP versus RATE_DROP and unread/held bytes. `mutants.py:679-681` plants both adapter defects; exact-head receipt catches B7 by name. README:452 correctly describes the separate tail-guard mutant. Executable artifacts are unchanged this round. |
| R845-1 F2, MINOR, Tests/Robustness | **Remains resolved.** `suite.hpp:1694-1720` covers foreign target, 22-byte cut and 14-byte stub behind a hold, no counters/ERR and intact delivery; `mutants.py:683` is caught by B8 in the exact-head receipt. |
| R845-1 F3, MINOR, Tests/Robustness | **Remains resolved.** `suite.hpp:1722-1745` grades FILTER_EN close during hold, release and subsequent inactivity; `mutants.py:687` is caught by B9. |
| R846-1 F1, MINOR, Conformance/Docs | **Remains resolved.** `KL_mbx_rx.sv:38-43`, design:277-281 and suite:393-400,1544-1549 distinguish the measured workload from permitted pipelining. Timeout/retry cite 9.3.2.6/9.3.6; next-refill delivery is the bench deadline. Prior clause verification carries forward unchanged. |
| R846-1 F2, MAJOR, Conformance/Tests/Docs | **Fully resolved.** Generated allowances/margins, held identity and last-byte measurement remain; both remaining round-two defects are now closed above. Missing release yields no measured start; orphan/duplicate/wrong-channel/late releases fail. No bound relaxed. |
| R845-1 R1 / R846-1 R1, RESIDUE, Docs | **Remain resolved.** Named source locations retain issue/ruling references and behavior without the issue-comment identifier. |
| R845-1 R2, RESIDUE, Docs | **Remains resolved.** Design:308-313 distinguishes passing/fitting rate refusal, filter refusal and RX_DROP for insufficient space. |
| R845-1 S1, SUGGESTION, Conformance/Docs | **Remains adopted.** Design:314-319 and PR limitations explain second controllers, pipelined commands and controller responses sharing the bucket. Fifty unpaced commands are not promised. |

## Artifact-specific results

[R846] PASS Conformance - `REQUIREMENTS.md:42`, `FR_NFR.md:413-445`, `mailbox_margins.py:54-105`, `MAILBOX_CONTRACT.md:874-882` - Checked unchanged bucket figures, per-channel allowances, table generation and arithmetic against the ruling. Token ingress stays 1 ms; held ingress is refill plus 1 ms. Held margins remain ACMP 173 ms, AECP 213/223 ms and MVU 213 ms, with 10 ms more at the proposal. The check names differing rows and enforces positive margins. No ABI, rate, bound or budget changed. Bench acceptance remains the public one-in-flight workload; hardware acceptance is owed.

[R846] PASS RTL - `KL_mbx_rx.sv:598-612,738-789`, unchanged hdl/firmware/config trees and contract blobs - Applied the lens to the new grader assumptions and receiver dependencies. Held state excludes an ordinary same-channel commit, and refill release requires an already-held record, supporting both guards. No reset, CDC, width, FSM, token or head-publication delta exists. Direct object identity preserves prior clean RTL coverage; no rebuild or route was needed for this delta.

[R846] PASS Robustness - `held.py:42-77`, `grade.py:195-199`, `selftest_held.py:72-94`, `mailbox_margins.py:54-105` - Invalid histories and boundary probes fail as required; independent channels and valid coincident observations remain measured. Missing/duplicate/wrong-channel releases are distinguished. Margin controls reject stale cells, unknown channels and non-positive margins. Prior ring/filter/reset/close protections retain executable checks and receipts.

[R846] PASS Tests - `gen_mailbox.py:489-520`, `selftest_held.py:72-94`, `selftest_mutants.py:449-452`, published exact-head mailbox/firmware receipts - New checks fail for their claimed defects and retain valid controls. Guard removal produces the named failure. Receipt checks distinguish zero exits, historical equality, explicit skips and actual measurements.

[R846] PASS Docs - `FR_NFR.md:425-445`, `MAILBOX_SPLIT.md:300-307`, budget `README.md:384-399`, `CI_WORKFLOWS.md:204-212`, `ci_scope.py:65-75,295`, `suite.hpp:1648-1650`, PR Round 3 - Prose matches generation, ordering checks, conservative ingress accounting and the local-gate boundary. Prior requested wording is exact. R1 and S1 do not affect coverage.

## Execution and published evidence

Archive: [887dbc6444faac5c0fe736ab8caae37701dc91a5](https://github.com/kebag-logic/milan-fpga/tree/887dbc6444faac5c0fe736ab8caae37701dc91a5/review-evidence/917-r1). `prepare.py` verifies 1,069 public receipt/index files against the publication manifest; 12 selected files have publication redactions. It extracts no reviewer reports. The archive commit is unsigned and no detached signing material was supplied: content digests and commit identity are verified, without claiming signer authentication.

Independent commands and receipts:

- `gen_mailbox.py --check --crosscheck`, `--selftest`, and `ci_scope.py --selftest`: rc 0, zero findings/failed arms and PASS.
- `probe_margins.py <checkout>`: rc 0, P1 plus edited-cell and zero/negative-margin probes. Mutations stay in scratch. An initial reviewer fixture selected an earlier ADP table cell instead of the ACMP margin row; that setup was corrected without candidate changes or weakened expectations.
- Published `probe_attribution.py <checkout>`: rc 0, both invalid review histories refused and valid controls measured.
- `probe_ordering.py <checkout>`: rc 0, 13 maintained checks, both named guard-removal controls and timestamp/allowance boundaries.
- `run.py --self-test`: completed uninterrupted, rc 0, `self-test: 0 failures`, 216/216 mutations caught. Expected `CONTROL ... ESCAPED` lines exercise rejection of invalid negative-control evidence; none is an escaped mutation. Both new guard removals are caught by their named held-order checks.
- `check_receipts.py`: rc 0; image/receipt comparisons below. `git diff --check cec88385..HEAD` passes.
- `verify_checkout.py <checkout>`: direct tracked blob bytes, file modes and index equality at the exact head/tree, plus required submodule gitlinks and their bytes/indexes. No candidate source edits were made.

Published source-head receipts were checked, not re-executed here:

- `author-r3/receipts/mbx/make-and-mutants-394612c5.log` identifies the clean exact head: 622/667 one-interface checks, 629/674 two-interface checks, 547 host-model and 32 co-simulation checks, zero failures; 13/13 quick and 242/242 full mutants caught, make/mutants rc 0. B7/B8/B9 plants fail by name.
- Firmware receipt records `test_ctrl_firmware: PASS`, rc 0. All 46 fixture-image hash entries are byte-identical. Split firmware matches the recorded base: 1x1/1if `bb04b69678bda6d7aa21458b5a39da1a611c3211efabd314ff590e06f6c76978`, 145496 bytes; 8x8/1if `506a1ae4da57e1d71f22201f02f4e1df49d6cb110dfe677c5d1fba0e154ca8fb`, 158176 bytes. ROM-bank/constraint digests match. RAM initialization is separately recorded, outside that ROM/ELF comparison.
- Workflow table and 77 rc files: 77 steps executed with rc 0, 49 NOT RUN with reasons, zero bad. These are author-run steps, not hosted acceptance, act acceptance or a manager bank. Untouched full suite/Yosys jobs were not rerun this round; earlier evidence is explicitly retained.
- Regrade receipt records byte-identical tables/grades for held 1x1, held 8x8/1if, no-hold AECP control and 94/94 groups at recorded base and head. The two historical populations retain **seven existing misses**, zero refusals. Equality is not a claim of a fresh all-green population.
- New two-interface held receipt: last byte 100001422, hold 100001427, release 100500065; probe credited correctly, both followers refused. Total 5.31012 ms includes 4.98643 ms ingress against 6 ms allowance and 20 ms budget, run rc 0. Prior-attribution negative control is refused. Earlier 1x1/8x8-1if rows remain 5.23609/5.11361 ms.
- Large observation logs are published by digest/size, excerpts and results. The regrade script's equality comparison and published artifacts were inspected; unavailable complete logs were not independently regraded. No new CPU-system measurement is claimed here.

## Reviewer-owned ledger

CLEAN means no open BLOCKER, MAJOR or MINOR under that lens; hardware and merge duties remain separate.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue/ruling; REQUIREMENTS; FR_NFR:413-445; mailbox_margins:54-105; channel table; P1/arithmetic probes | R846-3 | 394612c55148b43354359daeab2aa88d4f019ec2 |
| RTL | CLEAN | KL_mbx_rx:598-612,738-789; hdl/firmware/config/contract object identity; unchanged reset/CDC/FSM/token dependencies | R846-3, preserving unchanged R846-2 coverage | 394612c55148b43354359daeab2aa88d4f019ec2 |
| Robustness | CLEAN | held:42-77; grade:195-199; ordering/attribution probes; B7-B9 and receipts | R846-3 | 394612c55148b43354359daeab2aa88d4f019ec2 |
| Tests | CLEAN | Margin self-tests; selftest_held/selftest_mutants; independent controls; exact-head mbx/firmware and regrade receipts | R846-3 | 394612c55148b43354359daeab2aa88d4f019ec2 |
| Docs | CLEAN; R1 residue, S1 suggestion | FR_NFR:425-445; design:300-307; budget README:384-399; CI policy/scope; suite comment; PR/publication receipts | R846-3 | 394612c55148b43354359daeab2aa88d4f019ec2 |

## Limits and pending manager duties

- No manager source-head bank exists or is inferred. The manager builds/validates the final current-dev merge candidate and publishes builder/native receipts at the merge turn. Source base `cec88385` differs from assigned live dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a`; the PR's recorded base oid is not the validation base. Confirm the destination then: public PR metadata currently names `dev-soft-core`.
- Hosted/act acceptance belongs to the manager. This review ran no Docker/act, host orchestration, prohibited full banks, hardware, shared installs, source fixes, commits, pushes, GitHub writes or sub-agents.
- Physical calibration is **NOT RUN**; field skips and desk gates are not hardware proof. Three descriptor walks with none unanswered remain owed. Keep/reopen #917 until dated evidence exists; this verdict does not discharge `Closes #917`.
- Unchanged selected-route evidence reports AltSpreadLogic_high +0.203 ns setup / +0.036 ns hold. No route was run here; preserve the selected recipe/directive in merge evidence.
- 8x8/1if held and no-hold runs retain the same three stated-cost overruns: 120704/117875 versus 101000 cycles, 95723 versus 43000. Their overall rc 1 is not a pass. These remain #914's composed-measurement work. New 8x8/2if held run is rc 0; the complete new population has not been rerun everywhere.
- No hosted job runs `gen_mailbox.py --check`: known pre-existing separate CI work, not a finding here.
- Standards corrections are unchanged; prior verified clause assessment carries forward without a fresh full standards audit.
- Other independent verdict, residue checklist, optional index repair, explicit merge authorization, candidate gates, post-merge containment and final issue completion remain manager duties.

Publish REPORT.md and only MANIFEST.sha256-listed receipts/scripts. Scratch contains disposable extractions and is never published. Portable probe scripts take the checkout path; preparation expects the pinned archive object already available.

R846-3 FINISHED
