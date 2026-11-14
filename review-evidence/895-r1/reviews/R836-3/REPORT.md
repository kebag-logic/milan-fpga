[R836] NEGATIVE - exact head 62298ab5cbfeb7056e4567f70e69d578201c75e0

# R836-3: external independent delta review of #895 / PR #901

One MINOR remains: the closing design summary reports R4 as 12.85 ms instead of the head's 12.96 ms. This is a numerical figure, not wording residue. Conformance, RTL, Robustness and Tests are CLEAN; Docs is UNCLEAN. The prior R836-2 blocking finding about the live PR body is closed. One new wording residue and the optional suggestions below are collected here for a single response.

## Scope and authority

Head `62298ab5cbfeb7056e4567f70e69d578201c75e0`, tree `71f9951455c31270524f6931cf621c21af6a82cf`; base `cec88385ad0a0ec0d61b91597640797766e45010` on `dev-soft-core`. The delta since `18300f6e5f0c63b2ebc81d6bbc243496034f638a` was examined within the full base-to-head diff. The #902 merges through `91c3fc0e` / `7398ec0a` were examined for this lane's resolutions, dependencies and recomputed figures, not as a replacement for #902's review. Unchanged code retains its preceding coverage except where this delta changes its dependencies.

Context was reconstructed from AGENTS.md / CONTRIBUTING.md, docs/README.md, issue #895's acceptance and public decisions, linked requirements and interfaces, diff/history, then public executable evidence. The independent verdict and five-lens ledger were recorded before consulting prior public findings. No other current-round review report or private author material was used.

Controlling public decisions include [acceptance 4 and bench scope](https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6840463408), [the 59.0 fixture fallback](https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6857334948), [the SID state/layout decision](https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6864645058), and [the round-4 STOP ruling](https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6876349305). The source REVIEW READY is [6880958086](https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6880958086). The current PR body was checked at this exact published head, not just its prepared replacement.

The public evidence is [archive 689125c2](https://github.com/kebag-logic/milan-fpga/tree/689125c247de8ce9bb38ccdbd74e3ed5ef966c64/review-evidence/895-r1), specifically author-r2 through author-r5. Below, `r5/` means its `author-r5/receipts/` directory. The archive commit is unsigned (`%G? = N`); no signer authentication is claimed. All 1,766 selected files match `MANIFEST.json`'s **published** SHA-256 values. This integrity check is distinct from the stale local INDEX entries in S5.

## Findings

### R836-3-F1 — MINOR — Docs — closing R4 figure is stale

- **Artifact:** `docs/design/SPLIT_CONTROL_MEMORY.md:2557`, the closing long-window-load paragraph: “under the tiers ... R4 12.85 ms”.
- **Authority/evidence:** CONTRIBUTING.md's measurement rule and the Docs lens require accurate head figures. The current tables at lines 2409 and 2432 give **12.96 ms**. Independently running the head's `flip_grade.py --check --point 1x1/1if` reproduces 12.96 (`flip-1x1.log`). 12.85 belongs to #902's pre-composition figure; the closing paragraph was updated in `62298ab5` but retained it.
- **Impact:** the authoritative head summary understates R4 by 0.11 ms and contradicts its own detailed table. The actual 20 ms bound still holds; this does not change the Conformance result.
- **Required outcome:** replace this occurrence of `R4 12.85 ms` with `R4 12.96 ms`, or derive the closing figure from the same head data.
- **Verification:** the closing paragraph agrees with lines 2409/2432 and `flip-1x1.log`. A text correction does not require a firmware bank rerun; re-review the changed documentation at its new head.

### R836-3-RS1 — RESIDUE — Docs — image-size statement says byte identity

- **Artifacts:** `docs/design/SPLIT_CONTROL_MEMORY.md:2539`, “The pace and THE TRANSMIT's figure move no byte of any image”; PR #901, ROM ledger bullet, “Every image is round 4's composed image to the byte”.
- **Authority/evidence:** source `sw/firmware/ctrl/aecp/aecp_mbx.h:56` changes the pace from 8 to 9. The same PR's CPU-harness section explicitly records the changed instruction immediate, `sltiu a0,a0,9` versus 8. The ROM tables establish unchanged linked **sizes**, not equality with round 4's executable bytes. Exact-head versus round-5 measured-build equality is a separate, supported claim.
- **Impact:** ambiguous prose contradicts the adjacent executable explanation; no measurement, ledger entry, execution result or acceptance claim needs changing.
- **Exact fix:** in the design page, “The pace and THE TRANSMIT restatements leave every image's linked ROM and SRAM sizes unchanged.” In the PR bullet, “Every image has the same linked ROM and SRAM sizes as round 4's composed image.”
- **Verification:** the prose distinguishes equal sizes across round 4/5 from equal loadable bytes between the measured round-5 build and the exact-head rebuild. RESIDUE only; it does not unclean Docs independently of F1.

## Prior findings, resolved or retained at their cause

The source for this reconciliation is the public findings in [R836-2](https://github.com/kebag-logic/milan-fpga/pull/901#issuecomment-6850878768), [R835-2](https://github.com/kebag-logic/milan-fpga/pull/901#issuecomment-6851427525), and their named preceding findings. Historical numerical statements below are not presented as current-head figures.

| Prior ID | Disposition at this head | Cause checked / evidence |
|---|---|---|
| R836-2-F1, including the live-PR portions of R836-1-F1/F3 and R835-1-F1/F3 | CLOSED | Live PR now names `62298ab5`, current amended scope, the composed rows, 34 Talker plants / 68 kills and SRP 413. `public-state.json`; current source table and r5 campaign receipts agree. |
| R836-2-RS1, overbroad claim that figures stayed unchanged | CLOSED for current publication | Current PR presents base, composed round-4 and head figures separately, and identifies costs/pace/tx changes. The historical round-2 comment is not current evidence. RS1 above is a different size-versus-byte wording issue. |
| R836-1-F1 / R835-1-F1, acceptance conflict | CLOSED | Public amended acceptance and STOP ruling; every current 1x1/1if row and load holds. 8x8/2if remains reported, and acceptance 6 is a bench item. |
| R836-1-F2(a) / R835-1-F2, old pass cost | CLOSED, retained delta coverage | The historical 315/320 correction was retained; the current composed tables and grader are separately labelled. F1 above identifies the different stale closing R4 cell. |
| R836-1-F2(b), ROM growth range | CLOSED | `SPLIT_CONTROL_MEMORY.md:357` explicitly gives 944–1,064 B against `b2d39235`; current composed ROM has its own table. |
| R836-1-F3 / R835-1-F3, plant count | CLOSED | Current `srp_talker_mutants.py` has 34 tuples; current body and r5 results say 34 at two interface counts. |
| R835-1-F4 / R836-1-RS2, publication count | CLOSED | `srp_bounds.h:49–59`; `srp_talker.cpp:502` counts the declarations passes. The merge adapts calls to the sliced transmit API and preserves its oracle. |
| R835-1-F5, ignored refused withdrawal; R836-1-S1 | CLOSED | `srp_mbx.c:296–300` retains the declared bit and starts no hold-off on refusal; `:339` keeps work owed. `srp_talker.cpp:547` exercises refusal and eventual wire Leave. The three corresponding plants remain in the 34. The earlier “unreachable” interpretation is withdrawn. |
| R836-1-RS1 / R835-1-RS1, source comment identifiers | CLOSED | The requested issue-only/cold-code wording survives in `sw/litex/ctrl_memory.py`. No new prohibited instance was found in this lane's delta; inherited instances remain #746's. |
| R835-1-RS2, first-declaration wording | CLOSED | `sw/firmware/ctrl/srp/README.md:193` qualifies “A declared output”; the gateless/unallocated case remains separate. |
| R835-2-RS1, second-pass withdrawal wording | CLOSED | `srp_bounds.h:53–55` now says a join/adoption refused for storage is made, while a withdrawal after a refused build stays owed (`fa3f31ee`). |
| R835-1-S2 / R835-2-S4, configured LeaveAllTime interpretation | CLOSED | SRP README lines 220–226 explicitly distinguish twice configured LeaveAllTime from two random intervals; the header-derived guard remains above the configured floor. |
| R836-1-S2/S3, R835-1-S1 / R835-2-S3, R835-2-S1/S2 | RETAINED, optional | S1–S5 below; no optional suggestion is promoted to an unresolved requirement. |

### Retained optional suggestions

Each is SUGGESTION, leaves its lenses clean, and retains the earlier finding's scope.

| ID / lenses | Artifact and authority/evidence | Impact | Optional outcome and verification |
|---|---|---|---|
| R836-3-S1 (R836-1-S2); Conformance, Robustness | `sw/firmware/ctrl/srp/srp_mbx.c:639`, destination comparison; 802.1Q 35.2.2.8 | D→E→D inside a hold-off compares the last recorded destination, so return to the last declared D can wait conservatively. The comparison is untouched. | Preserve last-declared identity if this recovery latency matters; add a timed D/E/D test. |
| R836-3-S2 (R836-1-S3); Tests | `sw/firmware/ctrl/test/srp_talker.cpp:361`, admission-swap allocation refusal | Failing all allocation also stops wire output, so that step cannot independently expose leave-before-join ordering on the wire. | Refuse only the replacement join while frame transmission remains possible; kill an order-reversal plant through wire observations. |
| R836-3-S3 (R835-1-S1 / R835-2-S3); Tests | `sw/firmware/ctrl/srp/srp_mbx.c:130`, `count_held`, and changed-destination tests | At 8x8/2if other work can wake transmission when the hold expires; the isolated expiry wake-up remains unproven, while the never-ends plant still covers eventual redeclaration. | Isolate expiry with no other scheduling stimulus and show a missing-wake plant fails. |
| R836-3-S4 (R835-2-S1); Robustness | `srp_mbx.c:296`, `:1179`, `:1229`; refused Leave, licence predicate and sliced transmit | Current safety relies on the adoption clearing `vlan_sent`. The next first declarations pass retries the Leave before MVRP can reopen the licence. The merge preserves this ordering, but a future refusal path could invalidate the implicit dependency. | State that invariant, or explicitly gate licence on validity and add a Listener-registered refused-withdrawal test proving no reopening before the Leave. |
| R836-3-S5 (R835-2-S2); Docs | `r5/INDEX.md`, four workflow logs named in `index.log`; public archive `MANIFEST.json` | The local index still describes pre-scrub bytes: 724/728 entries match; four logs are 8 or 12 bytes shorter. Round 2 similarly has 726/730. The archive's published hashes match all of them, so result provenance remains checkable; this is not missing execution evidence. | Regenerate the local INDEX after the final scrub. Run `check_index.py` and obtain zero mismatches; do not edit the logs to fit stale hashes. |

## Applied checks and results

### Conformance and architecture

Acceptance 1–3 were checked against the changed SID/gate integration and the retained declaration/refusal paths: `maap/maap_mbx.c:56–120,231`, `ctrl_app_srp.c`, `srp/srp_mbx.c:260–339,639,1229`, `mbx.c`'s source-SID publication API, and the mailbox SRC_SID authority. Startup writes both words on the source's own interface before opening its gate. A reopened gate waits for a fresh pair; one cached high word and the pending-source index serialize the two writes. The consumed written mark prevents a later reopening from reusing an earlier pair. The 16-bit masks cover the configured maximum 16 sources. The platform's source IDs remain stable; changing one while an open gate remains open is not a newly promised dynamic operation.

The feed still uses the published validity gate, with MAAP range and probe/registered-Listener demand. It adds no mailbox or lwSRP work to the feed itself. The refused Leave retains ownership and owed work, closes the licence first, and starts its hold-off only after acceptance. The merge's MSRP/MVRP slices retain declaration preparation and MVRP-commit licensing. No HDL or required gitlink changes occur in the base-to-head range; mailbox, CDC and datapath contracts therefore require no new RTL design proof. The new publication sequencing was nevertheless reviewed against those existing contracts.

Robustness coverage included startup, range loss/conflict, probe expiry, registered Listener demand, reopening, changed destination, high-word ordering, reset/refusal and wrong-interface cases in `test/srp_gate.hpp:196–318` and `test/srp_talker.cpp`. The mutation receipts exercise the relevant failure paths at both interface counts; the integration `[SID]` oracle requires actual stream frames and matches their IDs to advertised IDs, rather than allowing an empty capture to pass.

### Ruling order, cost restatements, pace, slice and load

History applies the STOP ruling in the stated order: `0d2662c0` costs, `c2622f79` pace, `b3a5ed99` transmit statement, then `8238156d` ledger, `10cd5472` idioms, `62298ab5` summary. The restatements are not independent arbitrary tuning.

| Restated cost | Measured cycles at 100 MHz | Measurement × 1.05, rounded up to 5 us | Head statement |
|---|---:|---:|---:|
| 1x1/1if AECP timer slot | 6,805 | 75 us | 75 us |
| 1x1/1if TICK | 4,385 | 50 us | 50 us |
| 8x8/2if AECP timer slot | 10,824 | 115 us | 115 us |
| 8x8/2if TICK | 4,948 | 55 us | 55 us; second column keeps 85 |
| 8x8/2if events fixed part | 2,882 | 35 us | 35 us |
| 8x8/2if MAAP record | 14,361 | 155 us | 155 us |

All six cover their measurement and follow the prescribed rounding. Ordinary cost comparisons against `r5/costs/` are listed in `audit.log`; none is below its measurement except the explicitly excluded AECP record. The largest legal record is 92,046 cycles, rounded by the rule to 970 us, within 975. **Known, not a finding:** the ordinary 1x1 AECP record measures 28,173 cycles, 300 us by the rule, against 235 stated. The ruling keeps 235 pending #902's response. Consequently the current analytical pass is the ruled source-head result, not a prediction that survives any later AECP restatement unchanged.

At the final costs, the pace candidates 7/8/9 ms give txL 53.03/49.46/47.86 ms. Nine is the first whole millisecond holding txL ≤49 and R4L ≤238. The slice rule chooses the built 900 us design; 18 of 420 grid candidates hold, with least margin +0.0225. At the old AECP-slot/TICK costs and pace 9 the slice would instead be 950, which explains why the ordering matters.

Independent current 1x1/1if calculation (`flip-1x1.log`), every source:

| Row | Head ms | Bound ms |
|---|---:|---:|
| R4 | 12.96 | 20 |
| R5 | 73.46 | 90 |
| R6 | 69.35 | 90 |
| First queued notice | 14.59 | 20 |
| Last queued notice | 127.08 | 130 |
| R4L | 203.48 | 238 |
| ACMP | 28.85 | 30 |
| ADP | 27.20 | 30 |
| MAAP | 27.29 | 30 |
| tx | 33.20 | 49 |
| txL | 47.86 | 49 |

The tx row rounds up to **34 ms**, not 30. `rows_tiers.tx_statements` reports no discrepancy. `SRP_REDECLARE_CS` at `srp_mbx.c:35` and `kHoldOffMs` at `srp_talker.cpp:55` both derive from the headers: 2,000 + 19 + ceil(34/10) = **2,023 cs** at one interface, **2,029 cs** at two. The test no longer types the old horizon.

The load was recomputed term by term from the head's rate/cost composition after comparing its cost inputs with the published leg extractions (`audit.log`): **0.5150633070** at the pin, **0.5114258070** in the second column; largest-legal-command load **0.694**. Each is ≤0.70. 8x8/2if is reported at **0.7958733509 / 0.7543838772**, not claimed to pass its flip. Its tx 89.15 is within the retained 98 statement, R4L 210.90 within 238, and txL 399.09 remains outside 49. The 8x8/1if service campaign belongs to its separate scope.

The published joins comprise 1,091 intervals over 227 group runs, 185.905–190.192 ms, inside 181–239. Arm A's seven held-egress misses at each point are the previously accepted cases; no newly unexplained miss was inferred from a zero process exit.

### ROM ledger, all points

The published links and plans, checked against the current ledger and source changes, give:

| Point | Fixture ROM / SRAM B; tiles | Platform ROM / SRAM B; tiles |
|---|---|---|
| 1x1/1if | 111,928 / 55,184; 41.0 | 116,992 / 56,224; 43.0 |
| 1x1/2if | 113,472 / 57,360; 42.5 | 118,560 / 58,400; 43.5 |
| 8x8/1if | 124,608 / 96,288; 54.5 | 129,720 / 97,264; 56.0 |
| 8x8/2if | 126,112 / 113,232; 59.0 | 131,256 / 114,224; 60.5 |

The 8x8/2if answering arm is 126,420 / 113,296 B, 59.0; valid-destinations is 126,280 / 113,232 B, 59.0. Their ROM space is 556 and 696 B; the fixture's is 864 B. The platform has **1,864 B** left and **4.5 tiles** of debt against 56; its 60.5 cap is fully consumed. Other points remain ≤56.

The independent `ledger_probe.py` used disposable synthetic ELF boundary cases through the real planner and ledger controls: both own images accepted, 20 wrong-point/no-override/over-budget cases refused, all six planted ledgers caught. It specifically accepts platform 60.5 and refuses 61.0; fixture 59.0 is accepted and 59.5 refused. This proves the boundary/identity controls, not a fresh platform link or SoC build. The attempted full `test_ctrl_memory.py` stopped at import because the review environment lacks `migen`; `memory-ledger.rc = 1` records that setup limit. The published full memory test is passing.

### Tests, idioms and exact-head public execution

`10cd5472` was checked independently: all **34 Talker plant tuples are identical in order, payload, target, oracle, entity and suite** before/after; `build.py` has identical Python AST; `srp_gate.hpp` splits declarations without changing initialization or assertions. No test was weakened by these edits. The names-run compression remains the authorized carried patch; the added just-past-run test covers its count guard.

`audit.py` checked the current archive hashes, exact-head receipt headers and return codes, four sweep specifications/results/completions and the eight harness comparisons. Results:

- Workflow table: **139 executed rows rc 0**, **226 NOT RUN with reasons**. NOT RUN is not a successful execution. The recorded lost-SDK-link incident is followed by the successful rerun; the no-git job intentionally removes `.git`.
- Source campaigns in those receipts: control 716, AECP 274, SRP 413; 34 Talker plants at two interface counts, **68 kills**, no escaped plant reported.
- Sweep: **65 distinct suites**, 15 + 17 + 17 + 16; **2,712,199 checks**, 361,003 + 2,046,229 + 284,233 + 20,734; no suite, timeout or in-suite failure. Each shard records this exact head and a clean final tracked tree. Initial field/freshness skips are not counted as evidence; the separate `tsn_fuzz` rerun reports 164 and 675 field checks and freshness PASS.
- All eight exact-head harness builds have successful loadable-image/logic comparisons with the measured builds, byte-identical sample logs, and rc-0 regrades. Whole executable hashes differ due to recorded stamps; `sha rc 1` is not hidden or represented as byte identity of the executable container.
- Source jobs start on separate clean clones. The firmware jobs' reported untracked `dispatch-build/keys/` residue comes from #902; it is not a tracked source change. Seventeen builder arms were NOT RUN for lack of the required environment, as disclosed.

This is verification of **author-published source execution**, not a reviewer rerun of the full banks and not a manager source bank. The independent runs here were bounded analytical checks, receipt/idiom audits and ledger probes. `git diff --check cec88385..HEAD` passes. The scoped simulator identity was verified as pinned version 5.050; no simulation bank was launched here.

## Reviewer-owned coverage ledger

All rows refer to this exact head. CLEAN records the artifacts actually examined and the applied requirement, not just a lens name. Optional suggestions do not unclean their lenses.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #895 amended acceptance and STOP ruling; FR_NFR 3.4.1; `maap_mbx.c:56`, `srp_mbx.c:35,296,639,1229`, mailbox SRC_SID contract; `flip-1x1.log`, `load.log`, `audit.log` and ROM plans against the ruled bounds | R836-3 | 62298ab5cbfeb7056e4567f70e69d578201c75e0 |
| RTL | CLEAN | Base/head HDL and gitlink diff is empty; `mbx.c` SID accessor, `maap_mbx.c:56–120` publication sequencing, SRP transmit conflict resolutions, widths/state/header-derived timing against existing interfaces | R836-3 | 62298ab5cbfeb7056e4567f70e69d578201c75e0 |
| Robustness | CLEAN | `srp_gate.hpp:196–318`, `srp_talker.cpp:502,547`, `srp_mbx.c:296,1179,1229`; reset/reopen/refusal ordering and `ledger-probe.log` wrong-point/over-budget refusals | R836-3 | 62298ab5cbfeb7056e4567f70e69d578201c75e0 |
| Tests | CLEAN | `10cd5472` tuple/AST audit; `srptx_grade.py` SID oracle and plants; r5 workflow/sweep/harness receipts, `audit.log`; real planner mutation cases in `ledger-probe.log` | R836-3 | 62298ab5cbfeb7056e4567f70e69d578201c75e0 |
| Docs | UNCLEAN — F1 | `SPLIT_CONTROL_MEMORY.md:357,2409,2432,2534–2557`; FR_NFR 3.4.1, MAILBOX_SPLIT, SRP/MAAP READMEs, current PR/REVIEW READY and public indexes checked against code and receipts | R836-3 (applied; not clean) | 62298ab5cbfeb7056e4567f70e69d578201c75e0 |

## Real limits and pending manager duties

No manager source bank ran at this head, and none is claimed or inferred. No hosted-context execution was newly audited here; hosted/act acceptance belongs to the manager. Physical calibration was NOT RUN. Simulation field results and field skips are not hardware proof; #895 acceptance 6 and #905's bench item remain excluded.

The full banks, complete raw timing traces and platform links were not independently rerun. Cost checks use the published leg extractions, source formulas and exact-head equivalence receipts, not a claim to have re-extracted every cycle from unavailable full traces. The archive is unsigned, though the published hashes match. The standalone memory test's missing dependency is recorded above; the narrower real-planner probe passed without installing anything.

Before merge, the responsible roles must:

1. Correct F1 and re-review the affected documentation; carry RS1 and the optional INDEX suggestion to the appropriate checklist.
2. Complete #902's AECP-record response, merge in the authorized order, re-sync this lane and recompute costs, pace, tx, slice, load and affected figures. This review is not advance approval of that future head.
3. Complete the independent review bar and exact-head hosted/act acceptance, distinguishing executed jobs from skipped contexts and known field/hardware exclusions.
4. Validate the **current-dev merge candidate**, including builder and native banks, and link its receipts. Source base is `cec88385`; the specified live dev is `b7d692952305e4e0e132abb8f99c339eeb17a873`. Source-head evidence does not validate that candidate.
5. Carry the placement note to #909 and retain the public routing of #906/#907 and the two Domain leave/join/VID items. Their authorized separate scope is not silently treated as fixed here.
6. Obtain explicit merge authorization, perform candidate and post-merge containment checks, and keep bench completion distinct from software review.

The clone was not patched. Final verification hashes every tracked blob and checks modes, index entries and required submodule gitlinks/working bytes: source, gPTP processor, protocol processor, lwSRP, TSN stack and stream primitives all match their pinned commits; the optional external checkout remains uninitialized with its gitlink unchanged. No probe output is placed in the source tree. `tree-verification.log` contains the exact pins and counts.

## Reproduction and publication

Publishable scripts and raw receipts are enumerated in `MANIFEST.sha256`; only those files and this report are intended for publication. `scratch/` contains disposable material and is excluded. Scripts take the source clone and/or the extracted public evidence root as positional arguments:

- `recompute.py SOURCE`: concurrent bounded graders; individual `.rc` files are authoritative (the missing-dependency memory attempt is 1).
- `audit.py SOURCE EVIDENCE_ROOT`: manifest, execution receipts, plant equivalence, cost/rate arithmetic and hold-off checks; rc 0.
- `ledger_probe.py SOURCE`: boundary and planted-ledger checks; rc 0.
- `check_index.py EVIDENCE_ROOT`: local INDEX hashes; rc 1 for the four retained current mismatches, with exact expected/actual values.
- `verify_tree.py SOURCE`: raw tracked bytes, modes, index and gitlinks; rc 0.

R836-3 FINISHED
