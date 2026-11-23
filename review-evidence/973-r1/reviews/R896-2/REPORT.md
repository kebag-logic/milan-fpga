[R896] NEGATIVE - exact head 5759780f2251ef25221c6a395250312dce656ca4

External independent review, issue #973 / PR #978, round R896-2.
Tree: `68f513cdd17297261b34f7601b0f95e8185f5c84`.
Source range reconstructed: `dd163e41438acb86e0c4d4e76df90f3f91ace1c0..5759780f2251ef25221c6a395250312dce656ca4`.
Delta judged: `9a71daa9aa2379e2a57eb93ccafe83101bcb37f7..5759780f2251ef25221c6a395250312dce656ca4`.

The delta introduces a blocking link-flap regression at both shipping shapes. An elided UP leaves a stale recovery mark across a subsequent DOWN. A fresh UP inside a later pass then resets twice and replaces the startup participants. The original re-attach probe now passes, but its recovery fix does not preserve #973's first-UP requirement in this sequence.

All five lenses were applied. The independent finding, verdict and ledger were written before reading either prior review report. Prior public findings were then reconciled below. Untouched code retains its prior verdict; the newly dependent event-ring and lifecycle behavior was examined again. No source fixes, commits, pushes, GitHub writes, author contact or additional reviewers were used.

## Authority and scope

Read AGENTS.md, CONTRIBUTING.md, docs/README.md, the frozen issue body and its three public scope/evidence comments, relevant REQUIREMENTS.md provisions, the SRP lifecycle contract, mailbox coalescing contract, loop service order and split-memory authorities. Then examined the full source-range diff/history and the four-commit delta, followed by public executable evidence.

The issue requires preservation of startup participants for an UP at any pass phase, an effective before/after host test and plant at 1x1/1if and 8x8/1if, unchanged CPU bounds, and images within their ledgers. The established interpretation remains: the first UP resets zero times and keeps already-clean participants; a subsequent UP after a dispatched DOWN resets once. The issue cites IEEE 802.1Q-2018 10.7 and 35.2. This review applies the project's existing lifecycle contract, without claiming a new audit of the complete standards.

The source delta changes no RTL, mailbox contract, loop implementation, CPU budget/harness or coverage ratchet. Its new dependency is the meaning of `ctrl_loop.events_left` and the event poster's coalescing/priority behavior.

## New finding

### R896-2-F1 BLOCKER - Conformance, RTL, Robustness, Tests, Docs - stale uncarried-UP mark authorizes a different UP

**Artifacts:** `sw/firmware/ctrl/srp/srp_mbx.c:1285` and `:1303`; `sw/firmware/ctrl/test/srp_link_pass.cpp:142`; `sw/firmware/ctrl/srp/README.md:117`; `probe_stale_mark.cpp`; `endstation_ax7101_1x1_tdm8.log` and `endstation_ax7101_8x8.log`.

**Authority/evidence:** #973's first-UP/startup-preservation acceptance and the documented register/event ordering. The poll short-circuits `carried_up` when the register reads DOWN. Consequently bit 1 of `link_carried`, set for an earlier uncarried UP, survives that DOWN. A later UP can promote the old mark to bit 0 using an empty-ring observation that preceded the *new* UP.

The executable sequence uses the committed fixture, normal event posting and the committed full-ring stimulus. It neither writes `link_carried` nor pauses the event poster:

1. Start with link DOWN and clean startup participants. Fill the event ring with counter-change events.
2. Raise UP after a pass's event take. The ring is still full, so no UP record posts. The poll marks the uncarried UP (`link_carried = 2`).
3. Return DOWN before any take frees space. The fabric's last posted level is already DOWN, so the pending UP disappears. Drain the ring while DOWN. No LINK record clears the mark, and the raw-DOWN short circuit leaves it set.
4. Raise a fresh UP after a later pass's event take. That pass observed an empty ring before the fresh UP. The poll promotes the stale mark and resets immediately, before the new LINK is dispatched.
5. The next dispatched UP sees `link_seen` and resets again.

`KL_mbx_evt.sv:155` selects LINK only when its level differs from `posted_up_r`; `:387` records the level when posting starts. `ctrl_loop.c:144` takes events before the polls, and `:158` records whether it exhausted its eight-record allowance. The host model's `next_source` and full-ring behavior match those relevant rules. The failure needs an ordinary coalesced transient, not re-attach or illegal re-entry.

At both shipping shapes, the new test observes two resets instead of zero, premature `link_seen`, and a changed participant pointer. All seven committed phase/full-ring/re-attach tests pass in the same binaries. With only production `srp_mbx.c/.h` restored from `9a71daa9` into a disposable source copy, the identical new test passes at both shapes. This establishes a regression in this delta, not an inherited defect or a failing setup.

**Impact:** the shipping SRP lifecycle again exhibits the double reset and startup-participant loss #973 is intended to remove. The new comment/README argument establishes that an old owed event has been handled or elided; it does not establish that a fresh UP occurring after the latest event take has no event outstanding. The first-UP claim is therefore false for this supported ordering, which is substantive documentation failure rather than wording residue.

**Required outcome:** an observation associated with an earlier uncarried UP must not authorize a fresh UP after an intervening DOWN. Preserve re-attach/elided-DOWN recovery, immediate fail-closed DOWN, the ordinary carried-UP recovery behavior, and the first/later-UP reset rules. Add a committed regression and an effective plant for this sequence; make the lifecycle explanation account for the observation's validity. No particular implementation is prescribed.

**Verification:** the supplied new probe passes at both shipping shapes with zero first-UP resets and unchanged startup participants; all existing seven link tests and the original re-attach probe remain green; `rv-poll-resets-on-register-up`, `link-pass-attach-carries-an-up` and the updated link plants remain killed. Recheck image ledgers and applicable CPU evidence after the production fix, given the eight-byte ROM headroom.

**Lens attribution:** Conformance: frozen acceptance fails. RTL: adapter state and event-poster/loop ordering are inconsistent. Robustness: an elided transient followed by a new edge triggers it. Tests: the committed full-ring test covers an UP that stays UP, but misses its elision and replacement. Docs: the new recovery argument and first-UP guarantee omit this case.

## Prior findings, explicitly disposed

Source: [R895-1 public findings](https://github.com/kebag-logic/milan-fpga/pull/978#issuecomment-7085166316). The previous external review reported no findings. Formal reviews and inline comments are empty at the final observation.

| Prior ID | Disposition at this head | Evidence |
|---|---|---|
| R895-1-F1, BLOCKER, Tests/Docs | Source cause and local verification resolved; hosted verification retained pending | `ctrl_configs.py:180` classifies the non-compiling table alongside its siblings. Published `gates/r2-bnd.txt` records the required local command passing: 4,455 compiled sources, zero findings, 117 boundary + 185 pin + 4 figure controls, zero misbehaved. The PR states this gate. Exact-head hosted success is not yet available. |
| R895-1-F2, MINOR, all five lenses | Original re-attach defect resolved; replacement regression is R896-2-F1 above | Re-ran the exact published `probe_reattach_elided.cpp`: both tests pass at 1x1/1if and 8x8/1if. The committed test additionally observes one reset. README:112 is true for the original case. Published named failure logs retain the register-UP and attach-carries-UP kills at all three campaign shapes. |
| R895-1-F3, SUGGESTION, Robustness | Retained, explicitly documented; non-blocking | README:125-126 and PR limitations state the double DOWN reset. `checks/f3-size-experiment.txt` records the discarded prototype's +16 B and 58.5 RAMB36 refusal against 58. No claim that DOWN now resets once. |
| R895-1-F4, SUGGESTION, Robustness/Docs | Addressed | README:124 states recovery of an UP dropped by re-entry. The mark/drain path provides that recovery for the described stable-UP case. The guard still counts/asserts the invariant violation. |
| R895-1-F5, RESIDUE, Docs | Resolved | The live PR body now says `Relates to #665, #970, #972, #872`. |

**Retained verification item R895-1-F1: BLOCKER, Tests/Docs; artifact `hosted-final.json`.** The source classification defect is fixed; this is not a claim that it still fails. Its required hosted completion proof is pending: `firmware-boundary` has not yet emitted a successful job at this head, and neither RTL workflow has completed. Impact: the prior finding's full verification condition cannot be cleared. Required outcome: the manager records a successful exact-head boundary job and the remaining required jobs executing without cancellation caused by it. Verification: inspect those exact-head job conclusions and receipts. This is additional to the new source blocker.

No new RESIDUE or SUGGESTION was found. Added source comments were checked for behavior/reason and issue references; no new bench lane label/name, review identity/round or issue-comment ID was found.

## Executed checks and receipts

The focused commands run foreground parent processes. Independent builds run concurrently inside them: two tasks with eight compilation workers, then four tasks with four workers, never more than sixteen. All disposable sources/builds are under `scratch/`.

| Check | Result | Receipt |
|---|---|---|
| Exact-head seven committed link tests plus new elided-UP test | 7 PASS, new test FAIL, at each shipping shape | `endstation_ax7101_1x1_tdm8.log`, `endstation_ax7101_8x8.log`, corresponding `.rc` files |
| New test with prior production SRP bytes | PASS at both shapes | `prior-stale-mark-*.log`, `.rc` |
| Original prior-review re-attach probe | 2/2 PASS at each shape | `reattach-*.log`, `.rc` |
| Public Round 2 receipt hashes | 299/299 match published manifest | `packet-hashes.json`, `evidence-audit.txt` |
| Public CPU pairs, grader equality, image figures | Checks below pass | `evidence-audit.txt` |
| Delta whitespace and protected-path comparison | PASS; protected paths unchanged | `source-audit.txt` |
| Raw source bytes/kinds/modes/index and required submodules | PASS | `integrity.txt` |

Reproduce from this exact checkout with its initialized submodules and existing host test dependencies:

```sh
python3 -B /path/to/packet/run_focused.py /path/to/checkout /path/to/packet
# Expected review result: exit 1, the new test fails at both shapes.
python3 -B /path/to/packet/run_controls.py /path/to/checkout /path/to/packet
# Expected: exit 0, prior-production regression controls and original re-attach probes pass.
python3 -B /path/to/packet/audit_integrity.py /path/to/checkout
```

`probe_stale_mark.cpp` is appended to the committed phase suite in a disposable test copy. `probe_reattach_elided.cpp` is copied byte-for-byte from the published prior packet. The prior-production comparison substitutes only the previous revision's two production SRP files in a disposable copy. No candidate source was edited. Published test logs retain output with checkout/packet paths replaced by `<checkout>`/`<packet>`; original run logs remain in unpublished scratch.

## Published evidence assessment

[Public packet](https://github.com/kebag-logic/milan-fpga/tree/f46f61902a75d67da3149eb533a6e56719438041/review-evidence/973-r1/author-r2/receipts), at immutable commit `f46f61902a75d67da3149eb533a6e56719438041`. All 299 receipt files match the manifest's published SHA-256 values. Selected raw public receipts are copied under `published-receipts/`; `packet-hashes.json` identifies the whole checked population. This verifies byte identity, not independent execution of every campaign. The publication commit is **unsigned** according to GitHub's verification field, and has no Git signature header. No cryptographic signature is claimed as verified; the public commit and manifest are the available provenance.

The exact-head author firmware receipts report 77 suite verdicts, 826 control, 385 AECP and 576 SRP successful campaign checks, with no escaped plants in the final gate. Eleven link plants are present at 1x1/1if, 8x8/1if and 1x1/2if. Spot-checked the register-UP, attach-carries-UP and new fallback failures against their assertions. The preliminary census's remaining five text hits are not confused with the later complete boundary PASS. Coverage self-test/check passes over 40 files.

The development `rv-poll-clears-carried` escape is retained and disclosed, not counted as a kill. The new fallback can restore that control's state one poll later. This explains that escape but does not excuse R896-2-F1. The old OR plant was moved to the new expression; its committed replacement still fails the fail-closed-DOWN assertion.

Twin, twin-plants, twin-maps and twin-maps-plants record zero exits; the placement comparator reports zero findings. The map plants have their named failures. These source receipts are the author's. **No manager source bank ran at this head, and none is inferred.**

CPU receipts cover ten groups per shipping point with zero refusals, budget misses or per-pass-share misses. Independently parsed 88 and 86 paired probes: no changed verdict or exceeded bound, maximum rounded absolute changes 0.217 ms and 0.149 ms. All four base/head grader outputs are byte-identical. Loads remain 0.511 / 0.744 against 0.70 / 0.75. The 1x1 last-notice, ACMP and txL figures remain 127.31 / 29.06 / 47.88 ms. The stored last-notice gate is still 130 ms; no bound was relaxed. The 8x8 analytic rows that are only reported are not treated as held bounds; its measured rows come from the CPU campaign.

| Image point | Base ROM B | Head ROM B | SRAM B, unchanged | RAMB36, unchanged |
|---|---:|---:|---:|---:|
| 1x1/1if | 126432 | 126488 | 56736 | 45 |
| 1x1/2if | 128032 | 128104 | 59040 | 46 |
| 8x8/1if | 139208 | 139256 | 98160 | 58 |
| 8x8/2if | 140784 | 140856 | 115504 | 63 |

All images fit their existing ledgers. The 8x8/1if ROM has eight bytes before the next allocation. Image comparison receipts attribute the functional object change to SRP and additional 8x8 changes to structure offsets. This round's `bool` to `uint8_t` replacement preserves the byte-sized field; ledger and member-size receipts retain SRAM totals.

Docs receipts record 104/104 steps. Both author builder receipts identify this exact head and tree and pass with explicit NOT RUN entries: an ineffective environment-option plant and an unavailable physical calibration report. Split-boot simulation reports both shipping shapes passing and six native controls plus six plants. None of these substitutes for hardware proof.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN, R896-2-F1 | #973 frozen acceptance; REQUIREMENTS.md ownership/service provisions; `srp_mbx.c:1285,1303`; old/new probe controls; CPU/image receipts | R896-2 | 5759780f2251ef25221c6a395250312dce656ca4 |
| RTL | UNCLEAN, R896-2-F1 | `srp_mbx.h:66`; `srp_mbx.c:1226,1282,1303,1491`; `ctrl_loop.c:137,158`; `KL_mbx_evt.sv:155,387`; host event model; structure/image comparisons | R896-2 | 5759780f2251ef25221c6a395250312dce656ca4 |
| Robustness | UNCLEAN, R896-2-F1 | Full-ring UP elision, intervening DOWN, fresh mid-pass UP; `probe_stale_mark.cpp`; original `probe_reattach_elided.cpp`; re-entry and double-DOWN dispositions | R896-2 | 5759780f2251ef25221c6a395250312dce656ca4 |
| Tests | UNCLEAN, R896-2-F1; R895-1-F1 hosted proof pending | `srp_link_pass.cpp:142,179`; `srp_link_mutants.py`; `ctrl_configs.py:180`; campaign wiring; focused logs; public firmware/boundary/twin receipts; hosted snapshot | R896-2 | 5759780f2251ef25221c6a395250312dce656ca4 |
| Docs | UNCLEAN, R896-2-F1; R895-1-F1 hosted proof pending | SRP README:111-127; `srp_mbx.c:1273` ordering argument; CHANGELOG; live issue/PR text; receipt manifest and gate claims | R896-2 | 5759780f2251ef25221c6a395250312dce656ca4 |

All five lenses were applied; none can bank clean coverage while the new finding remains. No untouched prior verdict is being revoked independently of this delta's effects.

## Limits and pending manager duties

- The final hosted snapshot has rtl-fast run `45113718971` and rtl-full run `45113718973` queued, with null conclusions. Some elaborate jobs have started; no successful `firmware-boundary` job is present. No cancellation caused by it is observed, but queued work proves neither execution nor success. Hosted/local-replica acceptance remains the manager's responsibility; this review did not wait for hosted completion.
- No full parent, processor, synthesis or builder bank was run here. The pinned simulation executable's 5.050 identity was checked, but no RTL simulation was run by this reviewer. Firmware gate, boundary, twin, CPU campaign and image-link execution claims above refer to published author receipts; only the focused probes and audits were independently rerun.
- Physical calibration is NOT RUN. Field skips, source tests, twins and simulated CPU rows do not prove physical timing, link behavior or audio operation.
- This is source-head review, not validation of the current-dev merge result. The manager must construct and validate the candidate against live dev (the supplied reference was `e275d7950ef3385753e6a15d2e191ba855b171ed`), publish exact-candidate builder/native receipts, and recheck fit/timing and ledgers after composition. Related #970/#972 work and #872 integration are not discharged here.
- Resolve the new blocker and re-review the affected lenses. Complete the retained hosted verification, remaining review bar, authorized merge, post-merge bench scenarios and containment, then issue/project completion. This negative verdict authorizes no merge.
- The clone remains at the exact requested head/tree. Raw bytes, file modes/kinds and index entries were checked for 1,943 superproject entries and all five required initialized submodules. `external` remains uninitialized, as supplied. No tracked restoration was necessary.
- Only files listed in `MANIFEST.sha256` and this report are publishable. `scratch/` contains disposable builds and downloads and must not be published.

R896-2 FINISHED
