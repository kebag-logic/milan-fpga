[R836] NEGATIVE - exact head 18300f6e5f0c63b2ebc81d6bbc243496034f638a

R836-2 is the external independent delta review of PR #901 / issue #895. Tree: `d7318d3676d199141e119e0afa1a49145edaba2b`. Base: `b2d39235ab9bba85d7e560b5f5f78fb4be528960`. Previously reviewed head: `d023b77a7bf677205e45195e0e1f0daf80d1a4d4`.

The source fixes pass this review. One MINOR remains: the live PR body still presents superseded acceptance and evidence claims. Its corrected replacement exists in the public packet but has not been applied. No source fix is requested. All five lenses were applied; Conformance and Docs remain UNCLEAN for this publication requirement. RTL, Robustness and Tests are CLEAN within the ruled delta scope.

## Authority and evidence boundary

Context was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, #895's frozen acceptance and public decisions, REQUIREMENTS.md's placement contract, split architecture and mailbox publication authorities, the base-to-head diff and seven delta commits, then public receipts. Previous findings were consulted after the independent code pass. No current-round reviewer report was used.

The [round-2 ruling](https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6840463408) changes acceptance 4 to no regression beyond stated deltas, with 1x1/1if load at most 0.70. It conditionally excludes a different-mechanism Domain repair. Acceptance 6 is outside this review. The known conflict with `665-s2b-cycles` at `32551422` is not a finding; composition follows #810's review.

Public packet: [archive 5fda6970](https://github.com/kebag-logic/milan-fpga/tree/5fda69702df2e27bbbf4711c766b3b40f6703f99/review-evidence/895-r1/author-r2). `audit.py` verified all 748 author-r2 published SHA-256 hashes. This verifies checksums, not a signer: the archive commit is unsigned and no detached signature was found. Redacted files were checked against published hashes, not pre-redaction hashes.

Source-head execution evidence is the author's clean-clone receipts. No manager source bank ran here, and none is claimed. Reviewer execution was limited to the Talker suite and three new plants at both points, load/row calculations and controls, docs/whitespace checks, and byte/index audits. No full bank, hardware, container workflow, source fix, commit, push, or GitHub write was performed.

## Findings

### R836-2-F1 - MINOR - Conformance, Docs - the live PR retains round-1 acceptance and evidence

- **Artifact:** [PR #901 body](https://github.com/kebag-logic/milan-fpga/pull/901), Status, Tests, How to validate, and Definition of Done; `receipts/public-state.json`. The final read still reports head `18300f6e` and body update time `2026-11-13T10:39:36Z`.
- **Authority/evidence:** ruling items 1 and 2 require the PR and REVIEW READY to state acceptance 4 by the ruling and correct the plant count. The live body says `REVIEW READY at d023b77a`, nine Talker tests, 28 plants, SRP campaign 392, and `[x] Linked Issue acceptance criteria are satisfied (1 to 5 here; 6 is the bench lane's)`. Current source has 11 tests and 29 plants; the final campaign has 398 kills, including 58 Talker kills. Current arm-A minimum margins are 11.233 and 9.718 ms; the live body quotes 11.255 and 9.733. It lacks the amended acceptance-4 comparison table. The packet's `PR-BODY.md` supplies the replacement, and [the new REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6850450637) supplies the corrected handoff.
- **Impact:** the public review object contradicts current evidence and the ruling. These are count, measurement and acceptance claims, not wording-only residue. This retains the publication portions of both reviewers' F1 and F3. The original acceptance conflict is resolved, making the remaining defect MINOR rather than the former MAJOR.
- **Required outcome:** apply the current-head PR description, including amended acceptance, complete deltas, 11 tests, 29 plants, SRP 398, current margins and pending duties. Historical round-1 comments may remain clearly superseded history.
- **Verification:** read back the live PR and compare with source, `receipts/evidence-audit.txt` and the new REVIEW READY. No firmware or full-bank rerun is required for this metadata correction. Until then this is open, not conditional approval.

### R836-2-RS1 - RESIDUE - Docs - qualify which figures stayed unchanged

- **Artifact:** #895 issuecomment-6850450637, acceptance-4 introduction; corresponding introduction in published `author-r2/PR-BODY.md`.
- **Evidence:** the introduction says head figures equal `d023b77a` and deltas are unchanged. This holds for analytical load/every-source tables. Measured margins were rerun and do move; the table already gives their correct values.
- **Impact:** an overly broad introduction to an accurate table. No figure, verdict, test, code, generated artifact or clause claim requires changing.
- **Exact fix:** `The analytical load and every-source row tables are unchanged from d023b77a. The measured margins below come from this round's legs, with their base-to-head deltas stated.`
- **Verification:** the introduction distinguishes analytical tables from measured margins. No lens is unclean for this residue.

No new source-comment residue was found. The newly introduced comment IDs and lane-name instances identified in round 1 are removed; neighboring old ledger wording remains pre-existing material.

## Previous findings reconciled

| Prior finding | Disposition | Cause / current artifact |
|---|---|---|
| R836-1 F1 / R835-1-F1 | Acceptance conflict resolved; PR portion open as R836-2-F1, MINOR | Amended #895/ruling and reproduced calculations; live PR remains superseded |
| R836-1 F2(a) / R835-1-F2 | CLOSED | `SPLIT_CONTROL_MEMORY.md:2211` gives 320 us, matching head grader; base is 315 |
| R836-1 F2(b) | CLOSED | Same page `:291` gives +944 to +1,064 B ROM against `b2d39235`, matching eight image pairs |
| R836-1 F3 / R835-1-F3 | New REVIEW READY and prepared body corrected; live PR portion open | `srp_talker_mutants.py:132` adds three plants: 29 names and 58 final kills; live PR says 28 |
| R835-1-F4 / R836-1 RS2 | CLOSED | `srp_bounds.h:49`, test `srp_talker.cpp:501`, publication plant killed at both points |
| R835-1-F5 | CLOSED | `srp_mbx.c:295`, `:326`, `:338`; test `srp_talker.cpp:545`; both refusal plants killed at both points |
| R836-1 RS1 / R835-1-RS1 | CLOSED | `ctrl_memory.py:217`, `:223`, `:224`: issue-only reference and cold-code wording |
| R835-1-RS2 | CLOSED | SRP README `:193`, `:195`: first-declaration and gateless-code-2 qualifications |
| R836-1 S1 | CLOSED by F5 fix | The former unreachable-refusal claim is withdrawn: adoption/reclaim/build reaches it and the current test proves it |
| R835-1-S2 | CLOSED | SRP README `:222` distinguishes configured LeaveAllTime from randomized draws |

Optional suggestions retained, not claimed fixed:

- **R836-1 S2 - SUGGESTION - Conformance, Robustness**, `srp_mbx.c:655`: D-to-E-to-D during a hold-off compares recorded destinations rather than the last declared FirstValue. It can conservatively delay return to D. Authority: acceptance 2 / 35.2.2.8's unchanged-value allowance. Optional outcome: preserve last-declared identity; verification: timed D/E/D test. Relevant code is unchanged.
- **R836-1 S3 - SUGGESTION - Tests**, admission-swap refusal in `srp_talker.cpp:378`: refusing all allocations limits wire observation of join-before-leave order. Optional outcome: join-only refusal while frames continue; verification: a leave-before-join plant fails on wire evidence. Test and swap path are unchanged.
- **R835-1-S1 - SUGGESTION - Tests**, `srp_mbx.c:138` / hold-off tests in `srp_talker.cpp`: independently observe expiry wake-up at 8x8/2if with nothing else owing a pass. Optional outcome: such a scenario and missing-`hold` plant; verification: killed at both points. Explicitly not taken; existing hold-off controls remain.

## Source fixes and independent executions

At `srp_mbx.c:295`, Leave failure preserves `talkers` and `held_cs`, and `done=false` reaches `sources_owed` at `:338`. The old declaration's admitted bandwidth remains published (`:326` through `:336`); licence closure precedes the attempt (`:284`). Success clears the bit and starts hold-off at `:298`. The poll owns a refused frame, and `transmit_aged` at `:1250` prevents another THE TRANSMIT call until it drains.

The test at `srp_talker.cpp:545` uses a real Domain adoption, exhausted pool, reclaimable empty Domain and full ring. It establishes the post-build adoption, retained declaration and retry obligation, and no premature hold-off. After draining it decodes the Leave, checks TALKER_DECL at that frame's commit, absence of subsequent Advertise, eventual hold-off and cleared obligation. Restoring old withdrawal handling fails the retained-declaration assertion. Removing `done=false` fails eventual wire Leave. These are behavioral test failures, not compile failures.

`transmit` at `srp_mbx.c:1221` prepares all interfaces, builds the first owing interface, then prepares that interface again. With no intervening poll, a closed licence cannot close again. IDLE_SLOPE and TALKER_DECL therefore publish at most twice on the built interface, SR_DOMAIN once, LICENCE once per source: `5 + MBX_N_PUB_SOURCES`, within unchanged `SRP_MBX_PUB_POLL_MAX`. `srp_bounds.h:49` states this correctly. Test `:501` counts one actual call with a refused join, including the other interface. The duplicate-TALKER_DECL plant fails at both points.

`focused.py` ran all 11 Talker tests at 1x1/1if and 8x8/2if, then the three new plants at each. **22 test executions pass, no skips; six plant executions are caught by their named diagnostics.** Raw logs are in `receipts/focused-1/` and `receipts/focused-2/`. Two foreground workers, eight compile jobs each, complete before exit; only disposable source copies are modified.

**Domain leave/join is NOT DONE.** `change_domain`, `srp_mbx.c:908` and `:919`, still discards Domain Leave/join return values. The published probe source and both logs show internal VID 3, `domain_owed=0`, while VID 2 produces 28 declaring events and no Leave over 25 seconds; VID 3 is never declared. This confirms failure, not repair. Reserving MVRP's new VID before committing Domain/publication state makes this a separate ordering problem. The ruling explicitly permits this handoff for a different mechanism. Its separate issue remains a manager duty; no Domain defect is marked resolved here.

## Acceptance 4: recomputation and deltas

Reviewer runs at head and a base export reproduce four published grader logs byte for byte. Both load checks exit 0; both flip checks exit 1. Head controls pass 25/25 and 131/131. These are analytical calculations from committed measured-cost tables, not fresh target timing measurements.

| Point / figure | Base | Head | Delta | Bound / disposition |
|---|---:|---:|---:|---|
| 1x1/1if load, pin | 0.486 | 0.488 | +0.002 | <=0.70, held |
| 1x1/1if load, second column | 0.483 | 0.486 | +0.003 | <=0.70, held |
| 1x1/1if R4 | 66.12 ms | 66.77 ms | +0.65 ms | 20 ms; #894 |
| 1x1/1if R5 | 35.95 ms | 36.24 ms | +0.29 ms | 90 ms |
| 1x1/1if R6 | 28.67 ms | 28.92 ms | +0.25 ms | 90 ms |
| 1x1/1if first notice | 20.00 ms | 20.00 ms | 0 | 20 ms |
| 1x1/1if last notice | 22.00 ms | 22.00 ms | 0 | 125 ms |
| 8x8/2if load, pin | 0.816 | 0.817 | +0.001 | 0.75 owner ceiling; #890 |
| 8x8/2if load, second column | 0.767 | 0.768 | +0.001 | 0.75 owner ceiling; #890 |
| 8x8/2if R4 | 346.15 ms | 347.69 ms | +1.54 ms | 20 ms; #894 |
| 8x8/2if R5 | 144.15 ms | 144.53 ms | +0.38 ms | 90 ms; #894 |
| 8x8/2if R6 | 135.80 ms | 136.15 ms | +0.35 ms | 90 ms; #894 |
| 8x8/2if first notice | 22.00 ms | 22.00 ms | 0 | 20 ms; #894 |
| 8x8/2if last notice | 62.00 ms | 62.00 ms | 0 | 125 ms |
| 1x1/1if pass own cost | 180 us | 185 us | +5 us | second-column table |
| 8x8/2if pass own cost | 315 us | 320 us | +5 us | second-column table |

32x32/2if is reported only: pin 2.150, second-column 1.659, own pass 590 us, all unchanged. The executable flip check still uses 0.70 for 8x8/2if; the owner's 0.75 reading is separately stated. Neither passes there. No flip approval is implied.

Arm A retains seven misses: 7/945 instances at 1x1/1if and 7/996 at 8x8/2if, four paths at each. The responding-port arm has 0/280 and 0/736, arm B 0/25 and 0/39, and valid-destination arm 0/5 and 0/20. The seven egress-held exceptions belong to tsn-c-stack #26; positive margins below exclude those over-budget rows.

| Least positive measured margin | Base | Current legs | Delta |
|---|---:|---:|---:|
| 1x1/1if arm A | 11.006 ms | 11.233 ms | +0.227 ms |
| 1x1/1if responding-port arm | 9.080 ms | 9.036 ms | -0.044 ms |
| 8x8/2if arm A | 8.973 ms | 9.718 ms | +0.745 ms |
| 8x8/2if responding-port arm | 6.246 ms | 7.879 ms | +1.633 ms |

Head counts/margins were checked against published leg/regrade receipts. Base measured margins are explicitly attributed to round-29 legs in `SPLIT_CONTROL_MEMORY.md:2227`; #665 issuecomment-6827605854 corroborates base miss counts and measurements. Raw base per-group timing logs are absent from this archive. Thus analytical figures and differences were independently recomputed, but every base timing sample was not independently replayed or re-extracted. That limit applies to these measured margins.

Changed costs against base: 1x1 MAAP record 90->115 us, AECP timer 60->65; 8x8 MAAP record 130->150, TICK 40->45. Second column also moves polls base 155->160 and 285->290, plus 1x1 ACMP owed frame 120->125 and walk 20->25. No cost table moves since `d023b77a`. Acceptance 4 is stated by the ruling, not as the whole flip gate being met.

## ROM and hot layout

Eight published image pairs use identical runtime/export inputs at base and firmware head `17ac263f`. Only docs and the coverage ratchet change from that commit to `18300f6e`; firmware/build inputs/ledger bytes are identical. The image tables agree with `SPLIT_CONTROL_MEMORY.md:286` through `:291`.

| Point | Fixture ROM / SRAM, B | Tiles | Platform ROM / SRAM, B | Tiles | ROM delta fixture / platform |
|---|---:|---:|---:|---:|---:|
| 1x1/1if | 108872 / 45568 | 38.5 | 113936 / 46576 | 39.5 | +976 / +968 B |
| 1x1/2if | 110664 / 56976 | 41.5 | 115760 / 58032 | 43.0 | +1064 / +1064 B |
| 8x8/1if | 122400 / 86464 | 51.5 | 127504 / 87456 | 53.0 | +960 / +944 B |
| 8x8/2if | 124136 / 112624 | 58.0 | 129288 / 113632 | 60.0 | +1024 / +1024 B |

Fixture SRAM deltas are +16/+32/+48/+48 B; platform SRAM and `ctrl_plat` each grow 64 B at every point. The 8x8/2if fixture's responding-port variant is 124444 ROM / 112688 SRAM, 58.5 tiles, the ruled fallback; SRAM exceeds 58.0's allocation by 48 B. Platform plans 60.0 against plan 60.0/cap 60.5; the other six points are <=53.0, below 56. Platform cold-code debt is 4.0 tiles / 16384 B. Ledger keys still bind the named staging/allocation/platform symbols. The published memory gate passes wrong-point and widened-ledger controls. This reviewer did not relink the images.

Hot-list `ctrl_split_hot.txt:182` places `moved` before `declare_sources` and the walk. The initial refusal fix grew `declare_sources` by one instruction; superseded legs disclose walk 2015/2000 cycles and polls base 16141/15500, both failures. At `srp_mbx.c:402`, Boolean OR assignment becomes Boolean `|=`. `stale` is `bool`, and the comparison has no side effects, so values are equivalent. The published account reports four bytes saved in `moved`, compensating the declaration growth at both points. No hot-list/linker-script change occurs.

Final rerun evidence: polls bases 15078/27578 cycles, each 422 under unchanged bounds; 1x1 walk 1987/2000; maximum work pass 173458/200000 at 8x8/2if. Eight final exact-head comparisons report identical loadable bytes to measured builds, identical sample logs, and successful regrades. Whole executable hashes differ because of stamps; receipts explicitly distinguish that. Linked ELF/symbol dumps are absent here, so this review does not independently assert every hot symbol address or universal timing invariance. Evidence covers this measured layout.

## Clean-clone gate pass

`check_evidence.py` tallies 139 workflow steps rc 0, 226 NOT RUN with reasons, zero other outcomes. All 39 job/lane/harness tree-after records have empty status; workflow records name the exact head. Skipped orchestration, installs and sweep-dispatch rows are not counted as executions.

The separate sweep records 62 immediate suite passes and three planted-script failures from directory-print output. Their rerun uses the same head with the workflow's `--no-print-directory` form and records successful build/tally exits. This supports the disclosed final 65-suite result, not a claim that every first attempt passed. Incomplete harness partitions and the first arm-B regrade refusal are likewise disclosed; only final merged/regraded legs count.

Final campaigns report control 696, AECP 227, SRP 398, zero escapes. Coverage reports 725/725 lines and 651/654 raw branches for `srp_mbx.c`; ratchet 651/651 is the eligible count after exclusions, not 654 exercised branches. `ctrl_app_srp.c` is 89/89 lines and 72/72 branches. Builder, behavior, memory and split-boot results are author source-head receipts, not manager runs or hardware proof.

Reviewer docs and whitespace checks pass. Scoped simulator identity was verified as 5.050; no simulation rerun was necessary for this delta. Exact-head workflow/status queries returned no entries through the queried endpoints, which proves neither a hosted pass nor the absence of check runs. Hosted/local workflow acceptance remains the manager's responsibility.

## Reviewer-owned ledger

Unchanged code retains its previously reviewed scope. Changed behavior/tests/publications/docs and their timing dependencies were reapplied. The explicitly deferred Domain mechanism remains unresolved outside this round's repair scope.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1 publication requirement | Amended #895/ruling; `srp_mbx.c:295`, `:638`, `:1250`; mailbox publications; base/head graders; live PR | R836-2 | `18300f6e5f0c63b2ebc81d6bbc243496034f638a` |
| RTL | CLEAN | `srp_mbx.c:282`, `:326`, `:338`, `:402`, `:1221`; `srp_bounds.h:49`; hot-list/image receipts; no HDL/gitlink delta | R836-2 | `18300f6e5f0c63b2ebc81d6bbc243496034f638a` |
| Robustness | CLEAN within ruled delta | Refused Leave/reclaim/full-ring and pending-frame retry; `srp_talker.cpp:545`; reset, entry guards, changed destination, admission and refused-join tests at both points | R836-2 | `18300f6e5f0c63b2ebc81d6bbc243496034f638a` |
| Tests | CLEAN | `srp_talker.cpp:501`, `:545`; `srp_talker_mutants.py:132`; six independent kills; final 58 Talker kills; coverage and gate audit | R836-2 | `18300f6e5f0c63b2ebc81d6bbc243496034f638a` |
| Docs | UNCLEAN: F1 | Memory page `:291`, `:2202`, `:2211`; SRP README `:193`, `:222`, `:231`; MAILBOX_SPLIT `:1143`, `:1167`; bounds `:49`; PR/prepared body/REVIEW READY | R836-2 | `18300f6e5f0c63b2ebc81d6bbc243496034f638a` |

## Pending duties and real limits

1. Apply/read back the corrected PR body and obtain reviewer closure of F1. Carry RS1 to the wording checklist. No source fix is requested.
2. File the confirmed Domain leave/join loss and the previously disclosed Domain FirstValue/VLAN-change issue. Neither is repaired by this head.
3. Complete the #810 round-30 composition after its review and validate its changed measurements. This ledger does not approve a future merge tree.
4. Obtain the other independent verdict and required hosted/local workflow acceptance; do not bypass a review in flight.
5. Validate the final current-dev candidate, including manager builder/native banks, and publish receipts. Source base: `b2d39235ab9bba85d7e560b5f5f78fb4be528960`; supplied live dev: `b7d692952305e4e0e132abb8f99c339eeb17a873`. Source validation is distinct from that candidate.
6. Hardware acceptance 6 remains separate. Physical calibration was NOT RUN here; field skips are not hardware proof. Merge authorization and post-merge containment remain pending.

The final `audit.py` receipt proves tracked blob bytes and executable/symlink modes, index equality to the exact tree, and the five initialized required submodule pins and tracked bytes. No mismatch remains. The unused, uninitialized `external` gitlink is unchanged. Builds/exports stay under `scratch/`, excluded from publication. `MANIFEST.sha256` lists every publishable script and receipt relative to this packet.

R836-2 FINISHED
