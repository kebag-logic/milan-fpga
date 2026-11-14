[A773]

## Contents

- **[Status](#status)**: round 9's head, the map table a direct index, 1x1/1if held, and `894-tiers` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)**: #894, #904 and #908, with the executor and reviewers.
- **[Description](#description)**: the round 9 ruling's items in its order, each its own commit.
- **[Findings](#findings)**: every finding of round 8's two reviews, with its resolution, file:line and verification.
- **[Authoritative references](#authoritative-references)**: the rulings and clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: the commands to check out the branch.
- **[How to validate](#how-to-validate)**: the reviewer's commands and their expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what this round leaves open.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

**REVIEW READY at 1x1/1if.** Head `5b264bf26416108add32d7fe5abca5252ffde2cb`: the delta from `dd01b0af` to `5b264bf2`, seven commits. `894-tiers` -> `dev-soft-core` (still `cec88385`, #810 merged).

- **The map-edit table is a collision-free direct index** (#894's ruling of 2026-11-14, issuecomment-6870437042, item 1). A key's slot is its position in the port's key domain, stream or cluster x the most channels one has + channel, sized from the build's shape constants, which the entity generator reads from the image's descriptors. A static assertion holds the table to the whole domain. The geometry's range refusal runs first, and a key outside the domain takes the same turn. The definition test is byte-identical and passes.
- **Every accepted key is enumerated** (item 2) at every checked-in configuration and at two wider geometries the builder accepts: R838-3's 16 talkers x 4 channels, and 16 talkers of up to 32. Every key is held as its own, and every 63-mapping ADD and REMOVE stays within 2 (n + R). R838-3's own probe now passes: 63 visits of 126 for the ADD, where it found 714.
- **Item 3's fallback is not needed:** the direct index fits. Every image's rom is round 8's or 8 B smaller; sram and tiles are unchanged.
- **The inputs are re-measured and restated** (item 4).
  - **The table keeps at least its former 256 slots.** With only the domain's 64 at 1x1/1if, the edit's stack frame moves 192 B, and the data cache takes the largest legal command's record from 91,625 to 98,720 cycles. That would be 1,040 us, the pace 9 ms at AMAP_LIVE_WRITE's earlier 25 us, and the every-command load 0.705, over 0.70. At 256 slots the REMOVE of 63 is 91,625 cycles, 965 us by the rule, so 975 us stays as the larger.
  - **The 8x8 shape's record** is 156,716 cycles at the head's firmware, 1,650 us by the rule, over the 1,555 stated, so it is restated at 1,650 (8x8/2if is reported).
  - **AMAP_LIVE_WRITE at 1x1/1if** is 25.51 us measured, 30 us by the rule, over the 25 stated. It was already 25.32 at round 8's head. Restated at 30 us, txL is 49.69 ms at 7 ms, so **the pace is 8 ms**, the smallest that holds.
  - **Every 1x1/1if row by every source:** txL 48.09 of 49, R4L 188.39 of 238, the last queued notice 126.46 of 130 (the slice 900 us, `tier_grid.py` 18 of 420 holding, the built design chosen).
  - **The loads:** 0.513 at the pin and 0.509 with tsn-c-stack#32 (0.70), and 0.692 with every command the largest legal one.
  - **The final pass's legs** find no other input over its stated cost at 1x1/1if or 8x8/2if.
- **Docs** (item 5): R838-3-F2 and R837-3-2 (238 and 49 ms wherever current, the pace rule's R4L condition, the head's loads, the 30 ms rows' ruling) and R838-3-F3 (the fixture's +184 B, reconciled below).
- **No STOP trigger:** 8 ms holds; the last queued notice is within 140 ms; no image is over its cap; the map commands' behaviour is unchanged; the collision case's pass is within THE SHARE at 1x1/1if (the refused collision and conflict edits' passes at most 93,813 of 200,000 cycles; the accepted REMOVE's 149,490).
- **The full local pass at the head, once, on clean clones and never piped:** the sweep's four shards exit 0 (65 suites, 2,713,040 checks, 0 failures); every hosted job's steps of rtl-fast, rtl, elaborate and docs run locally, 139 run and 226 not run with a reason, 0 bad; the AECP campaign 273 of 273 caught; every lane gate and harness leg at its expected exit.

## Linked Issue / roles

Relates to #894
Relates to #904
Relates to #908

Executor: `[A773]`
Internal cleared-context reviewer: `[R837]`
External reviewer: `[R838]`

## Description

| Piece | What changed |
|---|---|
| `aecp_shape.py`, `aecp_entity.py`, `aecp_maps.c` (`f0611e7f`) | **Item 1: the direct index.**<br>- `aecp_shape.key_domain` emits `AECP_ENTITY_KEY_STREAMS`, `_STREAM_CHANNELS`, `_CLUSTERS` and `_CLUSTER_CHANNELS`. These are the most STREAM_OUTPUTs and the most AAF channels any of their current or advertised formats has, and the most clusters of a STREAM_PORT_INPUT and channels of one of its clusters. They are read from the descriptor bytes the image loads. The generated tables sit behind `AECP_ENTITY_SHAPE_ONLY`, so `aecp_maps.c` includes the constants alone.<br>- `place()` returns `first * MAP_CHANNELS + channel` (`MAP_FIRSTS`, `MAP_CHANNELS` the larger of each pair), or `MAP_SLOTS` outside the domain. The decode runs `legal()` first, then `place()`; a key outside the domain takes `legal()`'s `ILLEGAL` turn, BAD_ARGUMENTS before its port is read. A map row outside the domain holds no mapping's key.<br>- `_Static_assert`: streams x stream channels and clusters x cluster channels each within `MAP_SLOTS`, and `AECP_MAP_PAGE < 256`.<br>- No product state reaches the domain refusal: a format is set only where the integrator's verdict calls it supported (the builder's shapes), and a cluster's channels are fixed. |
| `test_aecp.cpp`, `aecp_arms.py`, `aecp_map_mutants.py` (`58e6b60f`) | **Item 2: the controls.**<br>- `Core.EveryAcceptedMapKeyIsItsOwn`: every key port 0 of each type accepts is added in ADDs of 63 mappings, each key held as its own, then removed in REMOVEs of 63. In the work arm each edit is within 2 (n + R).<br>- `aecp_arms.key_arms` (in `all_arms`, and `--keys`) runs it in the work arm at the five checked-in configurations and at `KEY_GEOMETRIES`: 16 talkers x 4 (R838-3's), and 1 x 8 + 15 x 32 (the builder's most; a Talker must list a Base format, so 32 channels alone are refused).<br>- `Core.EveryKeyOfTheDomainIsItsOwn` fills the whole domain and `Core.MapKeysOutsideTheDomainAreRefusedAtTheirTurn` holds its edge. `Core.MapEditWorkIsLinearInItsMappings` keeps its 8/16/32/63 counts and n(n+1)/2 controls, its output keys drawn from the port's own.<br>- Removed: `Core.MapKeysThatShareASlotAreTheirOwn` (a hash's property; its key is outside the domain). |
| `aecp_maps.c`, the AECP README, `rows_tiers.py` (`992e52a0`) | **Item 4: the table's floor and the record.** `MAP_SLOTS` is the domain's size, at least 256: the edit's stack frame, and every cost measured with it, stays where it was (measured below). `LONG_RECORD_US['1x1/1if']` stays 975: its comment records 91,625 cycles, 965 us by the rule. The README states the index, the domain, the floor and the controls. |
| SPLIT_CONTROL_MEMORY section 13, the harness README, `long_notice.py` (`5cfa32c2`) | **Item 5: docs and residue** (below), and section 13's "The direct index". |
| `rows_tiers.py`, SPLIT_CONTROL_MEMORY section 13 (`88ed7082`) | **Item 4 at 8x8:** the 8x8 shape's record is 156,716 cycles at the head's firmware, 1,650 us by the rule, over the 1,555 stated, so `LONG_RECORD_US['8x8/2if']` is 1,650, the larger kept. 8x8/2if is reported: its R4L is 180.74 ms (180.65 before) within 238, and its txL 558.51 ms (488.98), over 49 as before. |
| `rows_tiers.py`, `aecp_mbx.h`, SPLIT_CONTROL_MEMORY section 13, FR_NFR 3.4.1 (`1f47c09c`, `5b264bf2`) | **Item 4: the datapath events and the pace.** `DATAPATH_US['1x1/1if']['AMAP_LIVE_WRITE']` is 30 us: `eventcost.py`, the cut the table states (the take and every sink's work, which reproduces its recorded 31.96 / 29.06 / 23.33 us at #810's merge), measures 25.51 us at the head and 25.32 at round 8's. `AECP_PACE_MS 8u`: at 7 ms txL is 49.69 ms. At 8 ms every 1x1/1if row holds; 8x8/2if's reported R4L is 195.74 ms and txL 446.92. |

### Measured

- **The `aecp-largest-notice` group** (CPU cycles):

  | Table | 1x1/1if REMOVE of 63 | ADD | Refused edits | 8x8 | 8x8-1if |
  |---|---:|---:|---:|---:|---:|
  | round 8 (hash, 256 slots) | 92,766 | 86,504 | 23,014 to 79,384 | 142,634 | 151,629 |
  | direct index, the domain's 64 slots (`58e6b60f`) | 98,720 | 92,801 | 23,956 to 83,664 | 146,010 | 155,625 |
  | direct index, at least 256 slots (the head's firmware) | 91,625 | 83,716 | 23,883 to 75,892 | 156,716 | 154,850 |

  At 8x8 the floored table's record rises too, most of it in the memory copies after the edit, so 8x8/2if's stated record is raised to 1,650 us (reported rows only).

  The 64-slot table does less work and costs more: its smaller frame moves the edit's arrays 192 B across the 8 KiB direct-mapped data cache. Restated, its 98,720 would be 1,040 us. Then, at AMAP_LIVE_WRITE's earlier 25 us, txL is 52.90 ms at 7 ms and 49.28 at 8, so the pace would be 9 ms (txL 47.63, R4L 203.44). But the 1x1/1if load with every command the largest legal one would be 0.705, over 0.70, and `tier_grid.py --point 1x1/1if` would hold none of its 420 designs. That load crosses 0.70 near 1,015 us.
- **The pace table at 1x1/1if** (txL against 49, R4L against 238): P 6 53.99 / 158.39; P 7 49.69 / 173.39; **P 8 48.09 / 188.39**; P 9 47.35 / 203.39; P 10 and 11 45.76 / 218.39 and 233.39; P 12 R4L 248.39, over.
- **The datapath events** (`eventcost.py`, the take and every sink's work, us): at 1x1/1if AVB_INFO_CHANGED 30.55, AS_PATH_CHANGED 31.57, AMAP_LIVE_WRITE 25.51 (stated 35, 35, 30); at 8x8/2if 35.76, 32.79, 22.65 (40, 40, 25).
- **The map work** (`Core.MapEditWorkIsLinearInItsMappings`, 63 mappings): a REMOVE of one key's values 127 visits (2 (n + R) = 128); an accepted ADD 63 (126); a REMOVE of every row 315 (378).
- **`Core.EveryAcceptedMapKeyIsItsOwn`:** each 63-mapping ADD is 63 visits plus each row read, and each REMOVE is within its bound. At 16x32 there are 488 keys in 8 ADDs; the last REMOVE is 1,165 visits against 2,078.
- **R838-3's probe** (`probe_maps.py`, unchanged) at the tree: ADD 8 / 16 / 32 / 63 visits for 8 / 16 / 32 / 63 mappings (it found 8, 16, 144, 714); REMOVE 40 / 80 / 160 / 315 (40, 80, 496, 2,268). It exits 0.
- **Every accepted key**, enumerated from the generated descriptors at the five configurations and both geometries: 75 dynamic ports, each key in the table and its own.
- **The images** (rom bytes, round 8's head -> this head; sram and tiles equal): fixture 1x1/1if 110,584 -> 110,576, 1x1/2if 111,872 -> 111,872, 8x8/1if 124,112 -> 124,104, 8x8/2if 125,376 -> 125,368; platform 1x1/1if 115,632 -> 115,632, 1x1/2if 116,944 -> 116,944, 8x8/1if 129,208 -> 129,200, 8x8/2if 130,504 -> 130,496. The 1x1/1if fixture has 16 B left in its block, and the 8x8/1if platform 1,872 B inside its 56.0.
- **R838-3-F3, reconciled:** round 8's rewrite grew `.text` by 180 B in every image. `.rodata` is aligned to 8 B. At the 1x1/1if fixture the start head's `.text` ended on a boundary, so 4 B of padding were added, +184 B of rom. At the other seven it ended 4 B past one, so 4 B were removed, +176 B. Both endpoints stand; round 8's "every image +176 B" was wrong for that one image and for the code's growth.
- **At this head** (the full pass's legs): 57 join intervals in 14 group runs, 185.485 to 190.040 ms within 181.0 to 239.0, 54 of them in the 13 unplanted runs; 195 MRP timers' run-outs, 126 released and 69 empty, none late, absent or unresolved; every measured input within its stated cost at 1x1/1if and 8x8/2if (`measured_inputs.py`, `eventcost.py`).

New checks and their planted defects, each caught by its own words:

| Check | Planted defect | Failing words |
|---|---|---|
| Every accepted key its own slot | `map-index-channel-dropped`; `map-index-stream-or-cluster-dropped` | "an ADD of every key the port accepts holds each as its own" |
| Every position of the domain one key's | `map-index-stride-short` (stride one short; no accepted 1x1 key collides, the filled domain does) | "an ADD of every key of the domain holds each as its own" |
| No key outside the domain forms an index | `map-domain-a-channel-wide` | "a key outside the domain is refused at its turn, before its port is read" |
| A row outside the domain holds no key | `map-outside-row-looked-up` | "a row outside the domain bars no mapping" |
| Work linear (a quadratic plant, re-anchored from `map-hash-the-stream-alone`) | `map-table-scanned` | "past twice their sum" |
| Work linear (kept) | `map-remove-values-rewalked` | "not under n(n+1)/2"; "past twice their sum" |

`map-table-key-unchecked` is removed: no key compare is left to drop. The AECP table is 273 plants (269 less 2, plus 6), and every test is claimed by one.

## Findings

| Finding | Resolution | File:line | Verification |
|---|---|---|---|
| R838-3-F1 MAJOR; R837-3-1 MINOR: legal key collisions defeat the map-work bound | Ruled (item 1): a direct index over the port's key domain, injective by construction at every geometry the builder accepts; the range refusal first, a key outside the domain refused at the same turn; a static assertion that the table holds the domain | `aecp_shape.py:19-59`, `:106`; `aecp_entity.py:44`; `aecp_maps.c:5-6`, `:139-161`, `:201-210`, `:212-226`, `:367-391` | R838-3's probe exits 0 (above); the KEYS arm at seven geometries; the enumeration receipt; 5 new plants caught; the definition test byte-identical and passing |
| R838-3-F2 MINOR; R837-3-2 MINOR: current prose with pre-egress bounds, the pace rule, the loads, the 30 ms citation | each line states the head's value | harness `README.md:183`, `:185`; `SPLIT_CONTROL_MEMORY.md:2351`, `:2355`, `:2376`, `:2475`, `:2481` | compared with `PACED_BOUNDS`, `paced_rows.choice`, `CTRL_LOOP_TX_BOUND_MS` and `load_grade.py --check` (0.792 / 0.752, 0.513 / 0.509); `docs_check.py` and `check_em_dash.py` 0 findings |
| R838-3-F3 MINOR: the fixture's +184 B against "every image +176 B" | reconciled above: +180 B of code everywhere, the 8-byte alignment of `.rodata` making +184 at one image and +176 at seven; no repo text carried the claim | this body; the REVIEW READY comment | `rom_layout.py` over round 8's two heads' ELFs and this head's, each section's size and address |
| R838-3-R1 RESIDUE: "11 commits" | "the delta from `dd01b0af` to `5b264bf2`" | this body | `git rev-list --count dd01b0af..5b264bf2` is 7 |
| R837-3-R1 RESIDUE: the collision edits' description | the reviewer's wording | `long_notice.py:19-23` | read against `collision_indices`, `legal_values` |
| R838-3-S1 to S7; R837-3 S1 to S4 (suggestions) | S7 / R837-3 S1 taken: this round's index is generated from the files present; the rest not taken this round | the packet's `INDEX.md` | each row's sha256 against its file |

## Authoritative references

- **#894's ruling of 2026-11-14** (issuecomment-6870437042), this round's; **the egress ruling of 2026-11-13** (issuecomment-6867990126), whose STOP triggers it keeps.
- **Earlier:** the ruling 6867393730; the contingent ruling (issuecomment-6858269025) and its amendment (issuecomment-6862465874); the pace ruling (issuecomment-6848507008); the slice ruling (issuecomment-6845846512); the ruling on the owner's questions (issuecomment-6844175391) and the owner's confirmation (issuecomment-6844947317); the tiers' rows (issuecomment-6840564634).
- **The reviews:** R838-3 (PR #902 issuecomment-6870395150) and R837-3 (issuecomment-6870427229).
- **The requirements:** FR_NFR.md 3.4.1; NFR-SCOUT-01; #904's one decode and linear work.
- **The clauses:** IEEE 1722.1-2021 7.4.45, 7.4.46, 9.2.2.6 and 9.3.2.6; IEEE 802.1Q-2018 10.7.11; Milan v1.2 4.2.7.1.1 (Table 4.3), 5.4.2.27, 5.4.2.28 and 6.3.

## How to get into the same state

```sh
git fetch origin 894-tiers
git switch --detach 5b264bf26416108add32d7fe5abca5252ffde2cb
git submodule update --init --recursive
```

## How to validate

```sh
python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
python3 -B sw/firmware/ctrl/test/aecp_arms.py --output <dir> --keys
python3 -B sw/firmware/ctrl/test/aecp_arms.py --output <dir> --work --filter 'Core.MapEditWork*:Core.Every*'
python3 -B sw/firmware/ctrl/test/aecp_arms.py --output <dir> --core --filter 'Core.Map*:Core.Every*'
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/rows_tiers.py --selftest
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --selftest
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/tier_grid.py --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <dir> --groups aecp-largest-notice --record-budget-findings --record-share-findings
python3 -B scripts/check_py_idiom.py
python3 -B scripts/check_cpp_idiom.py
git diff --check dd01b0afef87037ec485cd49b40a26b542854bdd HEAD
```

Expected result / pass criteria:

- **The firmware self-test** passes, every AECP plant caught (273, the 32 on the map file and THE PACE among them). `--keys` exits 0 at seven geometries, each `MAP KEYS` line within its 2 (n + R).
- **The work arm** prints `MAP WORK` lines, each at most 2 (n + R), the collisions under n(n+1)/2.
- **The core filter** passes 13 tests, the definition test among them.
- **The harness self-test** passes with every mutant caught; rows_tiers, flip and load refuse every control.
- **`flip_grade.py --check --point 8x8/2if`** exits 1, as it did: 8x8/2if is reported, its txL 446.92 ms.
- **The 1x1/1if flip check prints RESULT: PASS**: txL 48.09 of 49, R4L 188.39 of 238, last 126.46 of 130. `tier_grid.py` chooses the built design at 900 us, 18 of 420 holding; the loads are 0.513 and 0.509.
- **`aecp-largest-notice` at 1x1** exits 0, with its longest record 91,625 cycles and no pass over THE SHARE.
- **The checks that exit 1 by design** are the reported 8x8/2if (`flip_grade.py --check`, `--point 8x8/2if`, `--design as-built`, `rows_tiers.py --terms`) and the 8x8-1if harness legs.

## Known limitations / out of scope

- **A stated input was under its measurement since round 8:** AMAP_LIVE_WRITE at 1x1/1if (25.32 us there, 30 by the rule, 25 stated). Round 8's 7 ms pace rested on it. This round restates it and takes 8 ms.
- **The direct index's constants come from the entity generator.** Lane 894b's THE SHAPES header is to become their single source when it merges #902 (ruling 6871343905, (c)).
- **The table's floor is a layout choice made by measurement.** Any later change to the edit's frame or to the data around it can move the record again, as the 64-slot table did. The record is measured in every full pass's `aecp-largest-notice` legs.
- **#908 stays open** until the last queued notice is within 125 ms and txL within 40 ms with the join timer at 20 cs.
- **The bench capture of the join intervals on the wire** is S12b's (180.0 to 240.0 ms); this round had no bench access.
- **8x8/1if is lane 894b's** (the ruling 6867393730, item (b); the egress ruling, item 6).
- **8x8/2if's build of one** is #910's debt; 8x8/2if stays reported, not held.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (#894 at 1x1/1if: met under the rulings; 8x8/1if: lane 894b; #908: stays open by its own terms)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes (the full pass above: the sweep 65 suites and 0 failures; 139 hosted steps run and 0 bad; the firmware campaigns, AECP 273 of 273; every lane gate and harness leg at its expected exit)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
