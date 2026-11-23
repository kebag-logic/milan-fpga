[R896] POSITIVE - exact head 87b2fc0f2867ef132b9388e22ec262fc626cbb57

External independent review of issue #973 / PR #978, round R896-3.
Tree: `82af93a508702104d01ea085c238cba30c636c38`.
Reconstructed source range: `dd163e41438acb86e0c4d4e76df90f3f91ace1c0..87b2fc0f2867ef132b9388e22ec262fc626cbb57`.
Judged delta: `5759780f2251ef25221c6a395250312dce656ca4..87b2fc0f2867ef132b9388e22ec262fc626cbb57`.

R896-2-F1 is resolved at its cause. All five lenses are CLEAN for this source delta and its affected dependencies. No open source BLOCKER, MAJOR or MINOR remains. One wording RESIDUE is recorded below. R895-1-F1's hosted verification is **pending**; as directed for this round, pending hosted execution alone does not make this verdict negative. This is not merge authorization or hardware qualification.

Read AGENTS.md / CONTRIBUTING.md, docs/README.md, the frozen issue body and public scope/evidence comments, linked ownership/service requirements, SRP lifecycle, loop service order, mailbox LINK/coalescing contracts and image-ledger authorities. Then examined the full source diff/history and the four-commit delta, followed by published executable evidence. The independent verdict and artifact-specific ledger were written before opening prior public review finding bodies. Prior findings were then reconciled explicitly. Untouched code retains its prior verdict.

## Cause and correction

At `sw/firmware/ctrl/srp/srp_mbx.c:1309`, every sampled level now reaches `carried_up`; the old raw-DOWN short circuit is gone. At `:1286-1294`, when bit 0 is clear, a sampled DOWN masks the mark to zero. Thus the mark from an UP elided behind a full ring cannot survive a subsequently sampled DOWN and authorize a fresh UP after a later event take.

An unmarked UP first becomes state 2, without being accepted. A marked UP can become state 3 only after a later take found the ring empty. A sampled DOWN in either uncarried state becomes state 0. When bit 0 already carries UP, the helper preserves it and returns false on raw DOWN, retaining the existing fail-closed behavior and subsequent carried-UP recovery. The unsigned mask and boolean result are well-defined; stored states stay within 0..3. Each interface remains separately indexed, with the same serialization and re-entry guard.

`ctrl_loop.c:137-163` still takes events before polls, with an eight-record cap. `hdl/milan/mailbox/KL_mbx_evt.sv:149-162,387` still prioritizes LINK and coalesces against the last posted level. The static assertion retains the full-ring-versus-one-pass condition. No RTL, mailbox ABI, loop implementation, CPU bound/harness or coverage-ratchet change exists from the reviewed flip base (`source-audit.txt`).

The first delivered UP resets zero times and keeps the clean startup participants; a later UP after DOWN resets once. This is the established public interpretation of #973's startup-preservation acceptance, rather than a new acceptance change.

The corrected comment and README delimit the mark's lifetime by sampled DOWNs. The physical argument assumes an autonegotiated link whose down interval exceeds the poll gap. The cited timer range is corroborated by the [IEEE working-group explanation of Clause 28 break_link_timer](https://www.ieee802.org/3/cg/public/May2019/mccarthy_3cg_01b_0519.pdf), page 3 (1,200 to 1,500 ms). This is supporting context, not a fresh audit of the entire 2022 standard or proof for arbitrary unsampled software-generated pulses. The observed-DOWN sequence in the blocker is directly tested without that physical assumption.

## Independent execution

All builds and disposable source copies stayed under this packet's `scratch/`. Foreground parent commands remained attached to completion. Independent tasks ran concurrently inside those commands, with at most sixteen compilation jobs. The candidate's tracked sources and index were never edited.

| Check | Result at both 1x1/1if and 8x8/1if | Receipt |
|---|---|---|
| Unmodified `probe_stale_mark.cpp` appended to the committed link suite | 10/10 PASS per shape: seven retained tests, two new committed regressions, one independent probe; zero first-UP resets and unchanged participants | `endstation_ax7101_*.log`, `focused.json` |
| Same suite against only the two production SRP files from `5759780f` | Expected FAIL: both committed elided-UP regressions and the independent probe fail; seven retained tests pass | `prior-endstation_ax7101_*.log`, `delta-results.json` |
| Independent stale-mark probe with production SRP from `9a71daa9` | PASS per shape | `prior-stale-mark-*.log`, `controls.json` |
| Unmodified original re-attach probe, current head | 2/2 PASS per shape | `reattach-*.log` |
| Immediate fail-closed DOWN, cancelled-record carried-UP recovery/old-input fencing, attach already UP | 3/3 PASS per shape | `safety-endstation_ax7101_*.log`, `safety.json` |
| All fourteen committed link plants | 14/14 killed per shape by their named test assertions | `plants/<shape>/link-pass-*.log` |
| Retained `rv-poll-resets-on-register-up` and `rv-sink-double-reset` | 2/2 killed per shape | `plants/<shape>/rv-*.log` |
| Exact source/tree/index/modes and five required submodule populations | PASS | `integrity.txt` |

The three new plants are `link-pass-mark-survives-a-down`, `link-pass-mark-survives-a-down-later`, and `link-pass-mark-masked-before-the-shift`. All compile and fail the intended assertion. `link-pass-attach-carries-an-up` remains killed. Compilation errors are not counted as kills. The author's earlier non-compiling plant attempt remains disclosed in its packet; the corrected committed plants were independently executed here.

The new committed regression observes reset publication as well as participant identity. It does not write `link_carried` or pause the poster. It fills the ring, raises an UP, elides it with DOWN before a take makes room, drains while DOWN, then raises a fresh UP after a later pass's take. The later-UP variant checks a single reset after prior activity. These checks discriminate the defect from a merely green setup.

## Prior findings

Sources: [R896-2](https://github.com/kebag-logic/milan-fpga/pull/978#issuecomment-7091979848), [R895-1](https://github.com/kebag-logic/milan-fpga/pull/978#issuecomment-7085166316). R896-1 reported no findings.

| ID and original classification | Disposition at this head | Evidence |
|---|---|---|
| R896-2-F1 BLOCKER; Conformance, RTL, Robustness, Tests, Docs | **Resolved** | Unconditional sampled-level update clears the uncarried mark; independent before/after failures and passes at both shipping shapes; new plants killed; README/comment argument corrected. |
| R895-1-F1 BLOCKER; Tests, Docs | Source cause and local verification resolved; **hosted verification retained pending** | `ctrl_configs.py:180` classifies the non-compiling plant table. Published exact-head boundary receipt passes with 4,455 compiled sources, zero findings, 117 boundary + 185 pin + 4 figure controls, zero misbehaved. PR status accurately requires the hosted job. `hosted-final.json` has no completed boundary job. |
| R895-1-F2 MINOR; all five lenses | **Resolved**, remains resolved after this delta | Original re-attach probe passes 2/2 at both shapes; committed suite retains one-reset and later-UP controls; old reset and attach plants still killed. |
| R895-1-F3 SUGGESTION; Robustness | Retained, non-blocking | Double DOWN reset remains documented at README:129-130 and in the PR. No DOWN exactly-once claim is approved. The previous rejected size experiment is not rerun or recast as a fix. |
| R895-1-F4 SUGGESTION; Robustness, Docs | Addressed | README:128 states recovery of an UP dropped by re-entry. Stable marked-UP recovery remains; the existing guard still counts/asserts unsupported re-entry. |
| R895-1-F5 RESIDUE; Docs | Resolved | Live PR body lists `Relates to #665, #970, #972, #872`. |

The retained F1 item is a manager completion obligation, not evidence of a remaining classification defect or a newly failed run. This round's explicit pending-job exception governs its verdict treatment; merge acceptance is not waived.

## New wording residue

**R896-3-F1 RESIDUE - Docs - PR #978 Description, “The change is byte-identical in `.text` at 1x1/1if and 8x8/1if”; issue #973 comment 7093336734, “Size” bullet.**

- **Authority/evidence:** `published-receipts/checks/size-variants.txt` establishes unchanged `.text` byte counts (11,628 and 11,544 for the production SRP object), not byte-for-byte content equality. `published-receipts/images/compare-r2.txt` likewise compares numeric size fields.
- **Impact:** readers can mistake equal allocation size for identical executable contents. No numeric measurement, budget, test result or conformance claim needs changing.
- **Exact required wording:** replace the PR sentence with “The `.text` byte count is unchanged at 1x1/1if and 8x8/1if.” Use the same wording in the issue comment's Size bullet, retaining the existing +4 B two-interface figure.
- **Verification:** the public text says size equality, and the existing measured figures remain unchanged. Carry to the residue checklist; this does not make a lens unclean.

No other new finding or suggestion. Added source comments describe behavior and reason with issue/standard references; no new bench label, lane name, review round/identity or issue-comment identifier was found.

## Published evidence assessment

Immutable [author round-3 packet](https://github.com/kebag-logic/milan-fpga/tree/bf7e243062cfee72687b6b0374f70be88982171a/review-evidence/973-r1/author-r3), commit `bf7e243062cfee72687b6b0374f70be88982171a`. All **890/890** entries in the publication manifest match their published SHA-256 values. Selected raw public receipts are retained under `published-receipts/`. The copied prior runners/probes match the public originals byte-for-byte.

The evidence commit is **unsigned** (`%G? = N`; signature verification exits 1). No cryptographic signature is claimed verified. The immutable public commit and matching published hashes are the available provenance. Hash verification establishes byte identity, not independent execution of every bank.

The exact-head author receipts report 77 suite verdicts, 826 control, 385 AECP and 585 SRP successful campaign checks, no escapes in the final gate. All 42 published link-plant logs (fourteen at 1x1/1if, 8x8/1if and 1x1/2if) contain their named failure and diagnostic; the two shipping campaigns were also independently rerun here. The moved poll-read plant remains in the published gate. The disclosed `rv-poll-clears-carried` development escape is not counted as a kill: fallback can recover that altered state one poll later.

Coverage self-test/check passes over 40 files. Twin, twin-plants, twin-maps and twin-maps-plants pass, with named plant failures. Split boot passes both shipping shapes and its controls/plants. Docs receipts report 104/104. Both author builder JSON receipts identify this exact head/tree; their NOT RUN rows remain excluded: one ineffective environment-option plant and one unavailable physical calibration report. **These are author source receipts. No manager source bank ran at this head, and none is inferred.**

Independently parsed CPU tables contain 88 and 86 paired probes, zero budget misses or changed verdicts. Maximum rounded base/head differences are 0.204 ms and 0.146 ms; round-2/head differences are 0.114 ms and 0.059 ms. Published ten-group runs report zero refusals, misses or passes beyond the 2 ms share. Four grader outputs are byte-identical to the published source-base outputs. Loads stay 0.511 / 0.744 against 0.70 / 0.75; 1x1 last notice, ACMP and txL remain 127.31 / 29.06 / 47.88 ms. The stored notice gate remains 130 ms. Report-only analytic rows are not treated as held measured bounds.

| Platform point | ROM bytes | SRAM bytes | RAMB36 | Applicable ledger |
|---|---:|---:|---:|---:|
| 1x1/1if | 126488 | 56736 | 45 | 56 |
| 1x1/2if | 128112 | 59040 | 46 | 56 |
| 8x8/1if | 139256 | 98160 | 58 | 58 |
| 8x8/2if | 140856 | 115504 | 63 | 63 |

All images fit. Both shipping one-interface points retain every numeric size field from round 2. Two-interface `.text` grows 4 B; aligned ROM grows 8 B at 1x1/2if and remains unchanged at 8x8/2if. The 8x8/1if ROM still has only eight bytes before its next allocation. `evidence-audit.txt` records the independent receipt calculations.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts and result | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #973 acceptance; REQUIREMENTS.md ownership/service provisions; `srp_mbx.c:1286-1323`; zero-reset/participant probes; CPU pairs and image ledgers satisfy unchanged bounds | R896-3 | 87b2fc0f2867ef132b9388e22ec262fc626cbb57 |
| RTL | CLEAN | `srp_mbx.c:1216-1235,1286-1323,1497`; `srp_mbx.h:66-69`; `ctrl_loop.c:137-163`; `KL_mbx_evt.sv:149-162,387`; state, width, indexing and ordering checked; no RTL/CDC delta | R896-3 | 87b2fc0f2867ef132b9388e22ec262fc626cbb57 |
| Robustness | CLEAN | `srp_link_pass.cpp:171-241`; stale-mark and re-attach probes; `safety-*.log`; full ring, sampled DOWN, first/later UP, attach, immediate revocation and recovery pass | R896-3 | 87b2fc0f2867ef132b9388e22ec262fc626cbb57 |
| Tests | CLEAN | `srp_link_mutants.py:24-103`; `srp_mutants.py:961-999`; `ctrl_configs.py:180`; prior/head failures and passes; 32 independent plant kills; published firmware/boundary/twin receipts | R896-3 | 87b2fc0f2867ef132b9388e22ec262fc626cbb57 |
| Docs | CLEAN | `srp/README.md:112-133`; `srp_mbx.c:1273-1284`; `srp_mbx.h:66-69`; CHANGELOG:62-69; public issue/PR and hashed receipts; argument corrected, one non-blocking wording residue | R896-3 | 87b2fc0f2867ef132b9388e22ec262fc626cbb57 |

These are source-review results. The retained hosted verification item does not become an executed-job claim through this ledger.

## Reproduction and integrity

With the exact checkout, initialized submodules and existing host test dependencies:

```sh
python3 -B /path/to/packet/run_focused.py /path/to/checkout /path/to/packet
python3 -B /path/to/packet/run_controls.py /path/to/checkout /path/to/packet
python3 -B /path/to/packet/run_delta.py /path/to/checkout /path/to/packet
python3 -B /path/to/packet/run_safety.py /path/to/checkout /path/to/packet
python3 -B /path/to/packet/audit_evidence.py /path/to/checkout /path/to/packet
python3 -B /path/to/packet/audit_integrity.py /path/to/checkout
```

The evidence audit reconstructs the author receipts under `scratch/evidence` from the immutable public evidence commit. If that object is absent, first run `git -C /path/to/checkout fetch origin bf7e243062cfee72687b6b0374f70be88982171a`. Every runner exits zero when its expected results hold; prior-head test binaries and planted binaries themselves intentionally exit nonzero. Run the four runners in the listed sequence to retain the sixteen-job ceiling. Published logs replace only checkout/packet paths with neutral placeholders; disposable build logs remain unpublished.

Final byte audit checked 1,943 superproject entries and all tracked entries of the five required initialized submodules against their exact pins, including file kinds, executable modes and stage-zero index records. All pass. The supplied `external` submodule remains uninitialized. No tracked restoration was needed. Only `MANIFEST.sha256`-listed files and this report are publishable; `scratch/` is excluded.

## Limits and pending manager duties

- At **2026-11-23 06:36:15 UTC**, exact-head `firmware-boundary` is **pending**, with no emitted job yet. `rtl-fast` run 45124291359 is queued; `rtl-full` 45124291344 and `elaborate` 45124291121 are pending; `docs` 45124291599 is queued. Observed job entries are queued, not executed or skipped passes. See `hosted-final.json`. The manager owns hosted/local-replica acceptance and clearing the retained boundary verification.
- No full parent, processor, synthesis or builder bank, local workflow replica, privileged operation or hardware run was performed by this reviewer. The scoped simulator's pinned 5.050 identity was checked; no RTL simulation was executed here. Broad gate claims above refer to public author receipts, not reviewer reruns.
- Physical calibration is **NOT RUN**. Field skips, host tests, twins and CPU simulation do not prove physical timing, link behavior or audio operation. The existing fit/timing and post-merge bench obligations remain.
- This is source-head validation against the reviewed flip base `dd163e41`, not the final current-dev merge result. The manager must construct and validate that candidate at merge time, starting from live dev (the supplied reference is `e275d7950ef3385753e6a15d2e191ba855b171ed`), and publish its builder/native receipts. The tight image headroom makes composed ledger checks material. Related #970/#972 work and #872 integration are not discharged here.
- Complete the remaining independent-review bar, required hosted jobs, current-dev candidate validation, explicit merge authorization, containment, post-merge bench work and issue/project completion. Carry R896-3-F1 to the residue checklist. No GitHub write, source fix, commit, push, merge, author contact or additional reviewer was used in this round.

R896-3 FINISHED
