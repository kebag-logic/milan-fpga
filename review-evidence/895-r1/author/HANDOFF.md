# HANDOFF — [A775] lane 895: a split Talker declares only while its SRP parameters are valid

**Status: REVIEW READY at `d023b77a7bf677205e45195e0e1f0daf80d1a4d4`; the clean-clone gate pass ran once on it and
passed (section 7).** The ruling #895 issuecomment-6824623445 is applied. Two host restarts (after the STOP, and at 19:20 during this
round): no work was lost, the measurements were on scratch and the tree was clean.

- Worktree $LANES/895-talker, branch `895-talker-redeclare`, not pushed. Base `66f71326`; #810 round 29's
  heads `7f50ee6a` and `b2d39235` merged; #810 has published no round 30 (its head is still `b2d39235`, 20:45).
- Comments posted on #895, once each: TAKEN issuecomment-6819155432, STOP issuecomment-6821396849, REVIEW READY
  issuecomment-6838154041. Nothing more is owed on #895; push and the PR are the manager's (PR-BODY.md).

| Commit | Subject (short) |
|---|---|
| `3696098f`, `432c1e87`, `4f79ab7d`, `0f980b5c` | round 1, to the STOP: allocation-driven re-declaration (superseded) |
| `e0ab5e54` | merge of #810 round 29 `7f50ee6a` |
| `3fbf0ae1` | declarations follow validity through the composition; withdraw at a lapse; hold only a changed destination |
| `7392638e` | merge of #810 round 29 `b2d39235` |
| `fcd30dcc` | the platform's 8x8/2if image ledgered at 60.0 RAMB36, `ctrl_plat` 20,352 B, the 4.0 RAMB36 owed to S14 |
| `969fb8d8` | a refused swap keeps its declared type; a lapsed Talker Failed and an admission lost covered; the harness arm |
| `9f0a12d3` | the arm in its own module (`talker_window.py`); the coverage ratchet for `srp_mbx.c` and `ctrl_app_srp.c` |
| `8a407ed5` | a range MAAP loses, through the composition, and its plant; the arm's loss group; a row per source and interface |
| `81ae5c3b` | the arm's rows state the JoinTime's wait, as the srp group's Domain row does |
| `fe96abfa` | the size fixture's 8x8/2if point ledgered at 58.5, its cap (the answering-every-port arm plans 58.5) |
| `f44f0b6e` | the load gate's stated costs from this round's legs; the rows and loads they move |
| `d023b77a` | SRP's Talker plant table named in `ctrl_configs.OUTSIDE` (the TSN stack boundary refused it on `f44f0b6e`) |

The lane's own diff against #810's merged head `b2d39235`: 29 files, +1,252 / -141.

## 1. Design at the head

### 1.1 The clauses (read in the standards' text)

- **Milan v1.2 4.3.3.1**: a destination MAC is valid when MAAP allocated it with no conflict, and a PROBE_TX_COMMAND
  for the output arrived in the last 15 s or a matching Listener attribute is registered. **5.3.7.4**: with every SRP
  parameter valid, the PAAD declares a Talker attribute populated with them. **5.5.4.1**: source n's destination is
  the range's base + n.
- **IEEE 802.1Q-2018 35.2.2.8**: no changed FirstValue for a StreamID; at least two LeaveAllTime periods (Table 10-7:
  1000 cs) between the removal and the new declaration; the same FirstValue may come back at once. **35.2.2.8.7, Table
  35-6**: code 1 insufficient bandwidth. **10.7.4.3** LeaveAll.
- **IEEE 1722-2016 Annex B**: Table B.7 (rAnnounce! / rDefend! in DEFEND with compare_MAC FALSE: Restart!), B.3.6.4
  (compare_MAC, octet-wise reverse), B.3.5.3 (Restart! takes a new range).

### 1.2 Validity and its feed

- **Validity** is ACMP's `acmp_declaring` (tsn-c-stack `src/acmp.c`: `dest_mac_valid && (answered within
  da_fresh_ms = 15000 || listener_registered)`), which the MAAP adapter publishes per interface as `published_gate[k]`
  (DA_GATE; only interface k's own sources).
- **Feed:** the composition's delivery poll (`ctrl_app_srp.c` `deliver`, after MAAP's poll, every pass) calls
  `srp_mbx_gate(srp, k, published_gate[k], maap.ifs[k].core.base)` for each interface. The entry masks to the sources,
  records a changed mask, and for each valid source compares and copies base + n (a 6-byte compare); a newly valid or
  moved source is marked `readdressed`; any change owes THE TRANSMIT's declarations (`sources_owed`, `hold`). It calls
  no lwSRP function and makes no mailbox access; it refuses before attach and on reentry. Every composition gets it, so
  no platform or image wiring. **No mailbox contract change**: DA_GATE is read from RAM.

### 1.3 Declarations (`declare_sources`, in THE TRANSMIT's pass)

| Source state | What SRP does |
|---|---|
| not valid, not declared | nothing (no boot-time Talker Failed any more) |
| valid, not held | declares at once: Talker Advertise (admitted: fits 75 % of the link after the sources before it), else Talker Failed code 1; on its own interface only |
| declared, validity lapses (no probe for 15 s and no Listener, or MAAP lost or restarted the range) | withdraws: licence closed (LICENCE, then the report), `TALKER_DECL` and `IDLE_SLOPE` drop it, then MAD_Leave of its declared type; `held_cs[n]` = `SRP_REDECLARE_CS` = 2 x 1000 + 20 + 2 = 2,022 cs |
| declared, destination changes while valid | withdraws as above; the new destination is held |
| valid again, unchanged destination | declares at once (35.2.2.8: the same FirstValue) |
| valid again, changed destination | declares when `held_cs[n]` has run out: two LeaveAllTime periods from the Leave's request plus a JoinTime and THE TRANSMIT's bound |
| admission changes | swapped in place: the new type joined first, the old left after; a refused join keeps the old type |
| link reset | `talkers` carries the destroyed participants' declarations: a moved source is held, an unchanged one declared at once |
| refused join | owed again with THE TRANSMIT's next declarations |

The unit fixture has no gate: `srp_mbx_config.sources_valid` declares every source from creation, so the existing SRP
suites run unchanged.

### 1.4 Bounded work and costs

- `srp_mbx_gate`: per interface, a mask compare and, per valid source, a 6-byte compare and copy; at most
  CTRL_SRP_SOURCES x MBX_N_IF a pass, in the polls' base (every pass).
- `declare_sources`: per source at most one licence closure, one Leave and one join, once an interface a THE TRANSMIT
  call, as a Domain adoption already does; THE TRANSMIT's call publishes `IDLE_SLOPE` and `TALKER_DECL` once and
  LICENCE once a withdrawn licence (`srp_bounds.h`, restated).
- The centisecond consumer counts each held source down (`count_held`: CTRL_SRP_SOURCES decrements a centisecond).
- Measured by the harness (section 4).

### 1.5 Conflicts and notes, recorded (not resolved privately)

- **The Domain adoption** re-declares every declared source in place with a changed vlan_identifier, a FirstValue field
  35.2.2.8 does not let a Talker change either. Unchanged here (outside #895); to be proposed as an issue.
- **Each source is declared on its own interface only** (the gate holds only that interface's sources); before, every
  interface declared every source.
- **The datapath has one stream window** (interface 0's; `ctrl_plat.c` drops interface 1's window writes). Pre-existing.

## 2. #896: does this change remove its trigger?

- #896's soak (#878 round 3) correlates every false Listener withdrawal with registrar churn on the board's own failed
  talker stream, and the peer's stream alone, with no connection to that talker, ran 15 min with none.
- At the base every source declared Talker Failed (code 2, destination 0) on every interface from participant creation,
  and nothing re-declared it after MAAP allocated (#895's defect). So the board kept a Talker Failed standing for each
  of its sources throughout that soak, and the peer's Listener on it asked failed.
- **At this head** a source declares nothing until valid, and once a listener probes it (PROBE_TX, the peer's connect)
  it declares Talker Advertise with MAAP's base + n at once, when it fits (code 1 Failed only when its bandwidth does
  not). So the board's own standing Talker Failed, the churn #896 correlates with, is gone in #878's configuration.
- **The mechanism is not touched.** `srp_mbx.c`'s `capture()`, the registration snapshot, its `withdrawn` flag and the
  Listener path (`acmp_tk_unregistered()` from `ctrl_app_srp.c`) are unchanged. A transient empty read on any other
  stream's churn can still become a Leave. #896's acceptance 1 (a host replay of the captured MSRP sequence) needs the
  bench capture, which is not in the tree; its acceptance 3 soak is the bench lane's after #895. #896 stays open.

## 3. Tests and planted defects

- `srp_talker.cpp` (`Talker.*`, 9 tests) at 1x1/1if (2 sources) and 8x8/2if (9 sources): ValidSourceDeclaresAtOnce-
  AndNothingBefore, LapseWithdrawsTheAdvertiseAndDeclaresNothing, UnchangedDestinationIsDeclaredAgainAtOnce,
  ChangedDestinationWaitsTwoLeaveAllTimePeriods, DestinationChangeWhileValidWithdrawsTheOld,
  AdmissionChangeSwapsTheTypeInPlace, ResetKeepsAnUnchangedSourceAndHoldsAMovedOne, GateEntryRecordsOnlyWhatChanged,
  RefusedDeclarationIsDeclaredAgain.
- `test_acmp_mbx.cpp` `SrpGate.*` (`srp_gate.hpp`, through the composition with ADP, ACMP, MAAP and SRP), at 8x8/2if in
  the suites (also run at 1x1/1if here: pass): F895AProbeDeclaresTheSourceAndItsExpiryWithdrawsIt (the probe window and
  the 15 s expiry), F895AListenerKeepsTheSourceDeclaredPastTheProbeWindow (the Listener path),
  F895ARangeLostWithdrawsAndTheNewRangeWaitsTheHoldOff (a peer's ANNOUNCE takes the range: MAAP restarts, the Talker
  withdraws, the new range's base + n is declared only after the hold-off; the Listener keeps it valid).
- Acceptance 3's list: allocation (Valid...), change (DestinationChange..., ChangedDestination...), loss (Lapse...,
  RangeLost...), re-allocation (Unchanged..., ChangedDestination..., RangeLost...), the probe window and the 15 s expiry
  (Probe...), the Listener path (Listener...), the withdrawal (Lapse..., Probe..., RangeLost...).
- `srp_talker_mutants.py`: 28 Talker defects, one a rule, each killed by its named test on its words at both points
  (the two-interface campaign at 8x8/2if, the one-interface at 1x1/1if). The new one, `talker-lapse-starts-no-hold-off`
  (a lapse's withdrawal starts no hold-off), is killed by RangeLost... at 8x8/2if and 1x1/1if
  (`receipts/plants/`).
- SRP campaign shard 3/4 at `9f0a12d3`: 390 caught, 0 escaped (`test_ctrl_firmware: PASS`). The full campaigns run again
  in the clean-clone pass.
- `fw_coverage.py`: `srp_mbx.c` 724/724 lines, 653/653 branches; `ctrl_app_srp.c` 89/89, 72/72 (ratchet at `9f0a12d3`).

## 4. Costs, load and rows (acceptance 4)

**Legs** (CPU budget harness, split SoC simulation, VexiiRiscv on `sys` at 100 MHz), on clean clones; the firmware
image is the same at each (section 7 shows its loadable bytes identical at the final head):

| Leg | Head | Groups | Refusals | Budget misses | Work passes over the 200,000-cycle share | Heaviest work pass, cycles |
|---|---|---:|---:|---|---|---:|
| arm A, 1x1/1if (split in three runs, merged and regraded) | `9f0a12d3` | 94 | 0 | 7 of 945 (4 of 87 paths) | 0 of 158,337 | 161,050 (`backlog-owed`) |
| arm A, 8x8/2if (five runs, merged and regraded) | `9f0a12d3` | 93 | 0 | 7 of 996 (4 of 136 paths) | 0 of 257,109 | 168,175 (`backlog`) |
| answering-every-port, 1x1/1if | `9f0a12d3` | 16 | 0 | 0 of 280 | 0 of 19,677 | 161,566 |
| answering-every-port, 8x8/2if | `fe96abfa` | 16 | 0 | 0 of 736 | 0 of 14,971 | 173,458 (26,542 under) |
| valid-destinations, 1x1/1if | `8a407ed5` | 2 | 0 | 3 of 5 (the JoinTime wait, before `81ae5c3b` stated it) | 0 of 2,637 | 57,354 |
| valid-destinations, 8x8/2if | `8a407ed5` | 2 | 0 | 16 of 20 (the same) | 0 of 2,980 | 74,023 |
| arm B `aecp`, 1x1/1if and 8x8/2if | `8a407ed5` | 1 each | 0 | 0 of 25, 0 of 39 | 0 | |

Arm A's 7 misses are the merged head's seven (#810 round 29: 7 of 945 and 7 of 996, the rows tsn-c-stack #26 holds:
the 60 ms egress hold and the command behind the owed input). No pass over its stated cost (`STATED`) anywhere:
`whole_grade.py` held every pass given whole to THE TRANSMIT, the declarations' and withdrawals' among them, and
`poll_grade.py` every pass's base and items. Saves durable within their stated worst cases (8x8/2if `save-second`
22,110 of 22,150 ms; 1x1/1if 6,030 of 6,070 ms).

**Least row margin by measurement** (`scripts/costs/least_margin.py`, misses set aside): arm A 11.255 ms at 1x1/1if
and 9.733 ms at 8x8/2if (aged backlog windows' AECP last record), answering-every-port 8.826 and 7.879 ms (a held
notice), arm B 19.720 and 19.571 ms. The valid-destinations rows are graded at the final head (section 7).

**The new costs**, measured (most over every instance, CPU cycles; `scripts/costs/`, `receipts/costs/`):
- the DA gate handed to SRP every pass (`ctrl_app_srp.c` -> `srp_mbx_gate`) is in the polls' base: its most 15,078
  at 1x1/1if and 27,578 at 8x8/2if, each **422 under** `poll_grade.py`'s 155 and 280 us (the bound, unchanged);
- the hold-off countdown is in a centisecond's consumers: at most 9,586 and 19,596, under the 130 and 510 us stated;
- the declaration and withdrawal passes are THE TRANSMIT's builds: build of one at most 37,120 and 58,464 cycles
  (valid-destinations arm), under `ctrl_loop.h`'s; their heaviest work pass 57,354 and 74,023;
- MAAP's record at a range lost to a peer's ANNOUNCE (the core restarts) is the dearest MAAP record: 10,526 and 14,067.
- Thinnest: the registrar walk at 1x1/1if, 1,987 cycles against `poll_grade.py`'s 20 us (13 under), in arm A's `srp`
  group; this change does not touch the walk (its rise from at most 1,904 is most likely code layout in the cache).

**Tables fed** (`load_grade.py`, `scripts/costs/tables895.py`: each cost the larger of this measurement and the
committed table's; with tsn-c-stack#32 the larger of the measurement, the pin's column and the committed one; the
polls' and builds' bounds unchanged):

| Column, point | Moved |
|---|---|
| pin, 1x1/1if | `record.maap` 90 -> 115, `event.AECP` 60 -> 65 |
| pin, 8x8/2if | `record.maap` 130 -> 150, `event.TICK` 40 -> 45 |
| tsn-c-stack#32, 1x1/1if | `record.maap` 90 -> 115, `event.AECP` 60 -> 65, `base` 155 -> 160, `item.acmp` 120 -> 125, `item.walk` 20 -> 25 |
| tsn-c-stack#32, 8x8/2if | `record.maap` 130 -> 150, `base` 285 -> 290 |

**Load and rows** at `f44f0b6e` (before: the committed tables at `fe96abfa`):

| Point | Load at the pin | With tsn-c-stack#32 | Ceiling | Verdict |
|---|---:|---:|---|---|
| 1x1/1if | **0.488** (0.486) | **0.486** (0.483) | 0.70, merge gate | HELD, 0.212 and 0.214 under (`load_grade.py --check` rc 0) |
| 8x8/2if | 0.817 (0.816) | 0.768 (0.767) | reported against 0.75 | over, 0.067 and 0.018, as before this change (the flip check holds 0.70 and exits 1, by design, #890) |

Rows by every source (`flip_grade.py --check`, exit 1 by design at the merged head: the tier rows are #894's), before
-> after: 1x1/1if R4 66.12 -> 66.77 ms (bound 20, red before and after), R5 35.95 -> 36.24, R6 28.67 -> 28.92 (bound 90,
within), first and last queued notice 20 and 22 ms unchanged; 8x8/2if R4 346.15 -> 347.69, R5 144.15 -> 144.53, R6
135.80 -> 136.15 (red before and after), notices 22 and 62 unchanged. No row changes its verdict. What alone closes
8x8/2if's 0.768 to 0.70 (`scripts/costs/closes.py`, which reproduces the committed page's figures on the committed
tables): an SRP record 365 -> 251 us, SRP's refill 2 -> 2.89 ms, AECP's 5 -> 13.83, ACMP's 5 -> 18.31, or 1.10x the
compute.

## 5. ROM ledger (acceptance 5)

`ctrl_srp_image.py` and `ctrl_plat_image.py` at `8a407ed5`, round 28's runtime archives and split SoC exports
(`receipts/rom/images-final.md`):

| Point | Fixture rom / sram, B | Fixture RAMB36 | Platform rom / sram, B | Platform RAMB36 | `ctrl_plat`, B |
|---|---:|---:|---:|---:|---:|
| 1x1/1if | 108,872 / 45,568 | 38.5 | 113,936 / 46,576 | 39.5 | 17,536 |
| 1x1/2if | 110,664 / 56,976 | 41.5 | 115,760 / 58,032 | 43.0 | 19,072 |
| 8x8/1if | 122,400 / 86,464 | 51.5 | 127,504 / 87,456 | 53.0 | 18,176 |
| 8x8/2if | 124,136 / 112,624 | **58.0** (ledger 58.0, cap 58.5) | 129,288 / 113,632 | **60.0** (ledger 60.0, cap 60.5) | 20,352 |

Every other point is at or under 56 (the largest 53.0). The platform's 8x8/2if image records its debt: 60.0 - 56 = 4.0
RAMB36 = 16,384 B of cold code owed to S14 (`ctrl_memory.py`, SPLIT_CONTROL_MEMORY section 3 and 5).

**The size fixture's entry is 58.5 (`fe96abfa`), the ruling's fallback.** The fixture's own image fits 58.0 (792 B of
rom and 16 B of sram to spare), but the CPU budget harness's `answering-every-port` arm, the fixture with its test
port and keyed by the same ledger point, was refused at 8x8/2if: 124,444 B rom, **112,688 B sram, 48 B past the
112,640 that 58.0 holds**, 58.5 tiles (`legs/GN8b.log`'s image log). It fit at #810's round 29 alone (112,576 + 64 =
112,640, 0 B spare). This change adds 48 B of RAM at 8x8/2if (a layout probe compiled against the point's headers:
`srp_interface` 624 -> 640 B, 8-byte aligned, for three masks and the owed flag; `srp_mbx_config` +4 B; `held_cs` 18 B).
The cuts the ruling names recover about 30 B (masks 16 bits wide out of the interface struct, one hold-off counter an
interface, no config flag), short of 48, and would rewrite the code 28 plants anchor on. So the entry is 58.5, its
cap; the image itself plans 58.0. `test_ctrl_memory.py` PASS (every planted ledger caught). The ledger only lifts the
cap: banks are sized from the image, so the harness SoC and every simulation of a 58.0 image are unchanged.

## 6. Simulation evidence (the assignment's split-SoC evidence)

The CPU budget harness's `valid-destinations` arm: the split SoC simulation (the split CPU on `sys` at 100 MHz, the
mailbox RTL, the fixture's ACMP source port made the platform's, base + n once MAAP holds the range). Every frame the
mailbox sends is in the log (`WIRE` lines); `scripts/wire_talkers.py` decodes MAAP's ANNOUNCEs and every MSRP Talker
attribute and grades them (`receipts/sim/`, each log's sha256 beside it):

| Point, group | MAAP range | Before the first probe | Each source's Advertise | Its withdrawal | After |
|---|---|---|---|---|---|
| 1x1/1if `srp-talker` | `91e0f000a134`, 2 | no Talker attribute | `a134` (s0), `a135` (s1): base + n | Leave 14,999.5 and 14,999.9 ms after its Advertise (the 15 s window) | nothing; no Talker Failed at any time |
| 1x1/1if `srp-talker-loss` | `a134` -> `1ba5` | none | `a134`, `a135` | Leave of both 199 ms after the peer's ANNOUNCE (the next transmit opportunity) | the new range announced; nothing declared (held) |
| 8x8/2if `srp-talker` | `91e0f000d1a4`, 9, both interfaces | none | each on its own interface (even if0, odd if1), `d1a4` .. `d1ac` | each 14,999.8 to 15,198.7 ms after its own probe (15 s, then the JoinTime) | nothing; no Talker Failed |
| 8x8/2if `srp-talker-loss` | `d1a4` -> `4dae` | none | the same | if0's five Leaves at 4,711.8 ms, if1's four at 4,911.7 ms | the new ranges announced; nothing declared |

`tb/verilator/ctrl_split_boot` boots the platform image with an idle datapath and no frame input (its README's
Limits), so it cannot carry this evidence without a change to that harness, outside this lane; the platform's own
path differs from the fixture's only in its source port, which reports the same base + n.

## 7. Gates: the clean-clone pass on `d023b77a` (`receipts/gates/`)

| Gate | Result |
|---|---|
| every `run:` step of `rtl-fast.yml`, `rtl.yml`, `elaborate.yml`, `docs.yml`, each job on its own clone (`scripts/gates/run_wf.py`, `verify_wf.py`) | **139 rc 0, 226 not run with a reason, 0 bad**; 28 job trees clean after (`gates/verify-table.md`) |
| firmware self-test, the campaigns (`firmware-unit`, `-control-`, `-aecp-`, `-srp-mutants`) | PASS; control 696 of 696 caught, AECP 227, SRP 392 (the Talker plants among them), 0 escaped (`gates/workflows/mutant-counts.txt`) |
| `fw_coverage.py --check`; the TSN stack boundary; the saved-state store gate | PASS (39 files); PASS; 455 tests |
| CPU budget harness, both points, every arm (`scripts/gates/harness_final.sh`, `compare_builds.py`) | built at the head: image loadable bytes identical to the measurement builds', Verilog identical but its comments; a group re-run per arm byte-identical to its measured log; every measured group regraded rc 0 (section 4's counts; the valid-destinations rows 0 of 5 and 0 of 20 with their JoinTime wait) |
| `load_grade.py --check` / `--selftest`; `flip_grade.py --selftest` / `--check` | rc 0 / 25 of 25; 131 of 131 / rc 1 by design (as at the merged head) |
| `test_builder.py --require-rv32`; `behave` | rc 0; 508 scenarios, 2,330 steps |
| the lane gates (`scripts/gates/lane_gates.sh`: idioms, docs, `ctrl_hot`, harness, hooks and target self-tests, `gen_mailbox`, `lint_rtl`, `test_ctrl_memory.py`, nvm self-test, the split boot simulation 1x1, 8x8, native controls and self-test, `git diff --check` from the base and from #810's head) | every rc 0 but the flip check's three, by design; three clean clones after |

The first pass, on `f44f0b6e`, found one defect of this lane: the TSN stack boundary (`firmware-boundary`, `ctrl_boundary.py`) refused `srp_talker_mutants.py`, a file naming the firmware's tree that no registry named. `d023b77a` names it in `ctrl_configs.OUTSIDE`, and the whole pass ran again on that head (`receipts/gates-f44f0b6e/`). The same pass showed `test_builder.py --require-rv32` reads the SDK at `$HOME/br-milan-rv32/host`. The runner's job home now links the host's pinned SDK there, as #665's runner home did. `ci_rv32_sdk.py --verify-only` refuses that SDK only for its missing installer receipt (`gates/rv32-sdk.txt`: Buildroot 2026.05, GCC 14.3.0).

## 8. Run history (this round)

- 13:14 ruling; implementation, tests, plants, ledger (`3fbf0ae1` .. `9f0a12d3`).
- Host restart; resumed: no unit was running; legs and the SRP campaign started on `9f0a12d3` at 15:52.
- 16:00 the arm's probes had no `.if<i>` suffix, so `path_key()` folded every source into one unnamed path: the arm's
  leg stopped (my own unit), names fixed, the loss group added; the loss test and its plant; `8a407ed5`; the arm's legs
  restarted from a clone at `8a407ed5`.
- 16:4x the arm's rows waited a JoinTime for their transmit opportunity: the wait stated as the Domain row's (`81ae5c3b`).
- 16:4x the answering-every-port arm's 8x8/2if image refused at 58.0 (48 B of sram over); cuts short of 48 B; the
  point ledgered at 58.5 (`fe96abfa`); its leg run on a clone of that head.
- 16:3x-19:10 arm A's legs split over parts and helper runs on the same builds (`scripts/part.sh`, `helper.py`,
  duplicates stopped by PID), merged and regraded (`merge.py`); costs parsed (`scripts/costs/`).
- 19:20 host power-off; resumed 20:42 with the tree clean and every measurement on scratch; tables fed (`f44f0b6e`).
- 20:47-22:27 the gate pass on `f44f0b6e`: the TSN stack boundary refused the new plant table (fixed, `d023b77a`); the
  builder test needed the SDK at the runner home (linked). Two lane-gate units of that pass were stopped by me after
  I edited their script while they ran (superseded results; never again).
- 22:27-23:50 the whole pass on `d023b77a`: every gate as section 7 records.
- 23:5x REVIEW READY posted once: #895 issuecomment-6838154041; PR-BODY.md written. Push and PR are the manager's.
