[R876] NEGATIVE - exact head 1825ba4eaccfe40788391b7af5533fae8c910a85

External independent review R876-2 of #956/#957 and PR #958. Tree `450fc60a4ae5c1259afe9b487d5593e31e8fa8ee`. All five lenses applied. The prior implementation findings are resolved. One MINOR documentation finding remains: the updated PR body's current-limitations section contradicts its current measurements. No implementation change is requested by this round.

## Findings

### R876-2-F1 - MINOR - Docs - current PR limitations retain prior-head numerical claims

**Artifact:** PR #958, "Known limitations / out of scope"; captured in `pr-body.md:249`, particularly lines 253, 255, 257 and 259. Compare the same body's "Round 2's gates" section, `docs/design/SPLIT_CONTROL_MEMORY.md:3221`, `:3225`, and the public author-r2 receipts below.

**Authority/evidence:** AGENTS.md section 6 requires enough accurate evidence for another cold reviewer. The current limitations say that the product image has **16 bytes** of ROM left and that four measured costs sit at their statements. Those are the prior round's numbers, without a historical label. The current receipts, verified against their published hashes, give:

| Claim | Current limitation text | Current receipt |
|---|---:|---:|
| 8x8/1if ROM spare | 16 B | **128 B**, aligned `rom_end` 139,136 of 139,264 B |
| 1x1/1if `centisecond` | 16,064 cycles; 170/170 us | **14,213 cycles; 150/170 us** |
| 8x8/1if `record.srp` | 35,273 cycles; 375/375 us | **35,507 cycles; 375/375 us** |
| 8x8/1if `record.maap` | 17,259 cycles; 185/185 us | **17,014 cycles; 180/185 us** |

The measured costs still at their statements are `item.acmp_declined` at both product points and `record.srp` at 8x8/1if. The top of the PR already states these correctly. `evidence-check.log` independently recomputes all 66 published cost rows per point and the aligned ROM charge.

**Impact:** a cold reader receives contradictory current memory margins, measured costs and margin-risk claims in one review object. This changes figures and measurement claims, so it is MINOR, not wording-only RESIDUE. It does not demonstrate an implementation or budget violation.

**Required outcome:** rewrite the current-limitations paragraph and ROM bullet using the current values above. Retain the formal-measurement limitation. If the old values are retained, label them explicitly as the prior head's history and state the current values alongside them. Describe only the current costs that remain at their statements.

**Verification:** compare the revised PR body with `author-r2/receipts/rom-ledger-images-0d80f0ed-vs-b4a1dde2.txt` and both `cpu-*-legs-0d80f0ed-vs-b4a1dde2.md` receipts. This is a PR-text correction; no source rebuild or implementation change is necessary. Docs remains UNCLEAN until re-reviewed.

### R876-2-R1 - RESIDUE - Docs - reviewer-role placeholders

**Artifact:** PR #958 "Linked Issue / roles", `pr-body.md:76` and `:77`.

**Authority/evidence:** both roles still say "to be assigned", while the public review-start comments name the independent internal and external reviewers.

**Impact:** stale administrative wording only; no measurement, test, code, contract or verdict changes.

**Exact fix:** replace the two lines with `Internal cleared-context reviewer: [R875]` and `External reviewer: [R876]`, linking the public round-2 start comments `7073171544` and `7073176800` respectively.

**Verification:** compare the two role lines with those start comments. Carry to the residue checklist; this does not affect lens cleanliness or the overall verdict.

## Prior findings: disposition at this head

The prior public findings were examined after the independent delta pass. No other round-2 review report was read.

| Prior finding | Disposition and cause-level evidence |
|---|---|
| R876-1-F1; R875-1-F1, MAJOR, Conformance/RTL/Robustness/Tests | **Resolved.** `srp_mbx.c:1191` clears `declaration[k]` with `listener_present[k]` before destroying the participant. Both independent reset probes now pass. New tests cover Asking Failed, Ready and Ready Failed equal before/after reset, separate/coalesced/repeated edges, reset silence, unchanged repeats and interface isolation. Existing closed-gate and all-output checks also pass. The composed probe observes one correctly flagged notice per controller after recovery. |
| R876-1-F2, also retained by R875-1, MAJOR, Conformance/RTL/Robustness/Tests | **Resolved.** `srp_mbx.c:1431` captures newly due work on resume; `:1457` consumes the build's original due while preserving new work and refused output. `poll` and `transmit_aged` use `tx_owed`; `srp_mbx.h:175` combines due/resume without growing the platform struct. Both reviewers' phase probes and all 200 current phase cases pass at all three points. Absolute 30,000 ms assertions remain. The second-slice refusal test and its plant pass. |
| R876-1-F3, MINOR, Conformance/Docs; R875-1-F2, MINOR, Docs | **Resolved.** `docs/reference/FR_NFR.md:427` states 2,973 cs at 8x8/1if, 2,970 at two interfaces, and a count ending 10 ms sooner when the transmit allowance rises from 99 to 105 ms. Old 2,026/2,027/3,027 figures are explicitly historical. |
| R875-1-F3, MINOR, Docs | **Resolved in its named artifact.** `sw/firmware/ctrl/srp/README.md:328` now states 139,136 B and 128 B left, matching aligned ledger accounting. F1 above records the separate stale current claim in the updated PR body. |

## Five-lens examination

[R876] PASS Conformance - `sw/firmware/ctrl/srp/srp_mbx.c:29`, `:215`, `:1175`, `:1425`; `sw/firmware/ctrl/test/srp_talker.cpp:141`, `:421`; #956/#957 public contracts - the reset record agrees with the registration lifecycle, and the changed destination retains the owner's 29-to-30-second model window. The subtraction remains 2,977/2,973/2,970 cs. The 30-second nominal-period interpretation and excluded 31-second tolerance-edge interpretation are unchanged from round 1.

[R876] PASS RTL - `srp_mbx.c:1404`, `:1425`, `:1472`; `srp_mbx.h:172`; `ctrl_loop.h` THE TRANSMIT/A3; full-range file inventory - examined firmware state ownership, due/resume union, callback ordering, refused output and reset cancellation. At one interface the selected interface is necessarily zero for valid due/resume state; making that compile-time constant preserves behavior. Both stream shapes pass at both interface counts. No HDL, mailbox ABI, CDC, submodule pin or budget change exists in this delta.

[R876] PASS Robustness - `srp_talker.cpp:919`, `srp_mbx.cpp:1745`, `test_aecp.cpp:1072`; independent reset and phase probe receipts - covered reset during registration, coalesced/repeated edges, other interfaces, closed gates, unchanged repeats, idle/running join timers, inter-slice due arrival, and refusal in the resumed slice. A paused build stays owed; a build without newly due work ends without spurious work; refused output remains the poll's with its interface due.

[R876] PASS Tests - `srp_talker.cpp`, `srp_mbx.cpp`, `test_aecp.cpp`, `srp_arms.py`, `srp_talker_mutants.py`, `srp_transmit_mutants.py`, `aecp_registration_mutants.py`, `tb/verilator/ctrl_service_budget/build.py:100` - examined test assertions and mutation anchors. The current tests preserve the absolute deadline, earliest bound, destination check and frame observations. The running-timer test asserts its precondition. Re-anchored plants still test their named defect; `CAME_DUE` no longer overwrites the unchanged-destination test selector. The CPU `transmit-aged` control still delays owed work, now including paused work; its dynamic full-measurement execution remains a stated limit, not a claimed pass.

Docs was applied to all changed documentation, source comments, the PR body and published receipts. Repository documents correctly explain the reset clear, kept due, aligned ROM charge and sampled CPU evidence. The added comments contain behavior/reason and issue/requirement references, with no new prohibited lane/reviewer identifiers found. `docs_check.py` passes, but does not validate the current PR body's numerical claims: F1 leaves Docs UNCLEAN.

Untouched code retains its prior review conclusions. This round rechecks every changed dependency and every named prior finding; it does not claim a fresh full-bank review.

## Executed checks

Portable entry points: `run_focus.py REPO`, `fresh_phases.py`, `run_checks.py REPO`, `check_evidence.py REPO`, and `audit.py REPO`. Every execution has a raw log and return-code receipt. Independent child processes ran concurrently under foreground supervisors, at most 16 compile jobs, with disposable inputs/builds only under `scratch/`.

- **Talker:** 245/245 tests at each of 1x1/1if, 8x8/1if and 8x8/2if: 219 repository tests, the original reset probe, seven original phase probes and 18 valid independent phase cases. Phase zero in the latter is excluded because it withdraws before the setup declares a source, as documented in round 1.
- **Original external phase probes:** additionally 7/7 per point in fresh processes. Since the latest-case test was refactored, `run_focus.py` obtains the original body from `0d80f0ed` and applies the original `focused.py` transformation in a disposable test copy. Production code, hold duration and absolute deadline are unchanged.
- **Composed AECP:** 6/6 at 1x1/1if, 1x1/2if and 8x8/1if, including the original independent link-reset probe and new reset test.
- **Sliced builds:** 4/4 focused tests at all four shape/interface combinations, including newly due work and the refused second slice.
- **Composed conflict:** 9/9 at 8x8/2if, including held-at-29-seconds and wire-by-30-seconds checks.
- **Mutation spot-check:** 10/10 selected SRP plants caught at 8x8/2if, plus the composed reset-notice plant at 1x1/2if. Includes `talker-unchanged-held`, the restored added-terms value, both resumed-due plants, reset cache, all five paused/refused-build plants. Each fails its named assertion; none escaped.
- **Static gates:** load, flip at both product points, shape costs and documentation checks all exit 0. Documentation: zero findings, scrub self-test 23/23, routing arms 4/4.

Independent phase observations, request to model wire:

| Point | Held loop | Serviced loop, sampled phases |
|---|---:|---:|
| 1x1/1if | 29,995 ms | 29,770 to 29,890 ms |
| 8x8/1if | 29,997 ms | 29,730 to 29,890 ms |
| 8x8/2if | 29,995 ms | 29,700 to 29,790 ms |

The repository sweep also passes every 10-ms withdrawal phase with held and serviced loops at all three points. These are model observations, not hardware measurements.

## Published evidence checked

Public packet: [362a3039 / review-evidence/956-r1](https://github.com/kebag-logic/milan-fpga/tree/362a303989763207c30c801b66aa9333a0130204/review-evidence/956-r1). All **153** `published_sha256` entries match. The fetched evidence commit has **no signature header**, and no cryptographic signature was verified; the receipt establishes published-byte hash consistency only.

- Author source gate receipts at `847b2e21`: four completed shards, return code 0, 76 suite verdicts, 826 control / 389 AECP / 574 SRP plants caught, no escape. The named reset/resume/refusal and `talker-unchanged-held` rows appear in those receipts. Earlier stopped/failed runs are not counted as passes.
- `b4a1dde2..1825ba4e` changes only the plant table and two documentation files. Thus the production image inputs for the other author receipts match this head; the gate that reads the changed plant table ran again at `847b2e21`.
- Memory receipt and section listing agree: aligned `rom_end` is 139,136 B, leaving 128 B in 34 ROM tiles, within 58 total platform RAMB36. `ctrl_plat` remains 18,048 / 19,712 / 18,944 / 21,568 B at the four ledger points. No memory budget changes.
- CPU receipts pair 71 and 95 probes, preserve the seven known held-egress misses per point and report no new miss or pass over the share. All 66 cost rows at each point were independently recomputed. Largest measured build-one costs are 52,531 and 126,644 cycles. The 8x8/1if static transmit row is 76.86 of 77 ms, load 0.744 of 0.75. These sampled legs are not the full formal measurement.
- The author self-test receipt reports completion with zero failures; it expressly does not execute the CPU measurement's `transmit-aged` plant. The two builder receipts each retain one NOT RUN arm. The release comparison identifies generated timestamp/name and ISA-string-order differences; literal byte identity of all outputs is not claimed here.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #956/#957; `srp_mbx.c:29,215,1175,1425`; `srp_talker.cpp:141,421`; phase/reset/composed receipts | R876-2 | `1825ba4eaccfe40788391b7af5533fae8c910a85` |
| RTL | CLEAN | `srp_mbx.h:172`; `srp_mbx.c:1404,1425,1472`; THE TRANSMIT/A3; unchanged HDL/ABI/gitlink inventory; memory receipt | R876-2 | `1825ba4eaccfe40788391b7af5533fae8c910a85` |
| Robustness | CLEAN | `srp_talker.cpp:919`; `srp_mbx.cpp:1745`; `test_aecp.cpp:1072`; independent reset/phase and four-shape sliced-build runs | R876-2 | `1825ba4eaccfe40788391b7af5533fae8c910a85` |
| Tests | CLEAN | changed tests and plants; `build.py:100`; 11 caught focused plants; four published firmware shards; executable receipts | R876-2 | `1825ba4eaccfe40788391b7af5533fae8c910a85` |
| Docs | UNCLEAN (R876-2-F1) | `FR_NFR.md:427`; SRP README; `SPLIT_CONTROL_MEMORY.md:3214`; comments; PR body `Known limitations`; author receipts | R876-2, applied but not clean | `1825ba4eaccfe40788391b7af5533fae8c910a85` |

## Limits and pending manager duties

- Correct and re-review F1; carry R1 to the residue checklist. No source fixes, commits, pushes, GitHub writes, author contact or merges were performed.
- No manager source bank exists or is inferred at this head. Source-head gate evidence above is the author's published evidence. The manager must validate the final current-dev candidate with builder and native banks at the merge turn; supplied live dev is `e275d7950ef3385753e6a15d2e191ba855b171ed`, distinct from the source base `15168e14` and recorded PR base `59b09884`.
- Hosted/act acceptance remains the manager's. This round did not execute or infer hosted jobs from required-context names, run containers, or run full simulation/synthesis/builder banks. No new full CPU measurement or platform relink was performed here.
- Physical calibration is **NOT RUN**. Field skips and simulated timing are not hardware proof. The requested 29-to-30-second bench measurements at 1x1/1if and 8x8/1if remain pending. Review cleanliness does not assert issue completion or waive the merge/completion contract.
- Final audit verifies all 1,936 tracked superproject blobs, file modes and index entries against the exact head, plus all five required initialized submodules' pins, bytes, modes and indexes. The optional uninitialized `external` gitlink remains exactly recorded. No tracked bytes needed restoration because probes used disposable copies. All foreground executions completed; no review job remains running.

Publish only REPORT.md and the files listed in MANIFEST.sha256. `scratch/` is excluded.

R876-2 FINISHED
