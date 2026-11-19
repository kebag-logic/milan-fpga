# [A801] #951 round 1 — the re-declare hold-off over two longest LeaveAll periods — handoff

Status (15:20): **REVIEW READY.** Final head `0d1eb8e4` (`0839453f` + 3 commits: code, tests and plants `e5dee83b`;
the width check `4224df63`; docs `0d1eb8e4`). Every gate passes at the code head `4224df63` (the firmware gate, its
campaigns with the two new plants, fw_coverage, the twin and its plants), and the docs workflow steps and both builder
legs at `0d1eb8e4`. The 20 split images differ from the base's in the hold-off's encoding alone; the release image is
byte-identical; the CPU legs on both images change no verdict, and a control image shows the measured differences
follow the code's placement, not the value. The reference device is not measured (no bench access). Posted: `[A801]
TAKEN` (issuecomment-7007407112) and `[A801] REVIEW READY` (section 9). Nothing pushed, no PR opened (the manager's).
Receipts: `receipts/` (140 files, `INDEX.md`); scripts in `receipts/tools/`.

## 1. Task and authority
- Issue #951 (part of #665). #665's ruling of 2026-11-19 (issuecomment-7007273447), item 2: derive the withdrawn
  Talker's re-declare hold-off from two longest LeaveAll periods (LeaveAll randomised up to 1.5 x LeaveAllTime, IEEE
  802.1Q-2018 10.7.4.3; Milan v1.2 Table 4.3) plus the existing JoinTime and transmit terms, about 30.2 s at one
  interface, never a mirrored literal; an image diff limited to that value; the Talker tests, mutants and docs
  restated; the reference device measured only if a conflict can be provoked safely.
- #895's accepted reading (its acceptance 2 and the #901 rulings): 2 x LeaveAllTime + JoinTime + one transmit, 35.2.2.8
  setting only the least.
- Branch `951-redeclare` at the flip train's head `0839453f` (PR #945, not merged). PR base `dev-soft-core`.

## 2. Changes (file:line at `4224df63`, reason)
- `sw/firmware/ctrl/srp/srp_mbx.c:32-34` `SRP_LEAVEALL_CS 1000u`: LeaveAllTime named once (Table 10-7, Milan Table
  4.3); `:526-527` `create_participants` configures both participants with it (was the literal `1000`), so the
  configuration and the hold-off read one name.
- `srp_mbx.c:35-37` `SRP_LEAVEALL_LONGEST_CS (SRP_LEAVEALL_CS + SRP_LEAVEALL_CS / 2u)`: the longest LeaveAll period,
  1.5 x LeaveAllTime, the upper end of 10.7.4.3's draw (lwSRP draws at most 1,499 cs, `mrp_mad.c` `leaveall_draw`).
- `srp_mbx.c:38-44` `SRP_REDECLARE_CS (2u * SRP_LEAVEALL_LONGEST_CS + SRP_JOIN_CS + (CTRL_LOOP_TX_MS + 9u) / 10u)`:
  two longest periods, the JoinTime and THE TRANSMIT's term unchanged: 3,023 cs at 1x1/1if (35 ms), 3,027 at 8x8/1if
  (77 ms), 3,030 at two interfaces (105 ms); was 2,023 / 2,027 / 2,030.
- `srp_mbx.c:45-46` (`4224df63`): `_Static_assert` that `held_cs` (uint16_t, `srp_mbx.h:167`) holds the hold-off. The
  constant grew by half; a narrower count would wrap silently. No code: all 20 images byte-identical to `e5dee83b`'s.
- `sw/firmware/ctrl/test/srp_talker.cpp:52-59`: the horizon `kTwoLongestLeaveAllMs = 2 x (10,000 + 10,000 / 2)` ms,
  an independent statement of the clauses (not the firmware's names), and `kHoldOffMs` on it; the two hold-off tests
  renamed `ChangedDestinationWaitsTwoLongestLeaveAllPeriods` and `...AfterTheLatestLeave`, their words restated;
  `:321` the "re-allocation after the hold-off" wait is `kHoldOffMs + 1000` (was a typed 21,000 ms).
- `sw/firmware/ctrl/test/srp_gate.hpp:318-345` (`SrpGate.F895ARangeLostWithdrawsAndTheNewRangeWaitsTheHoldOff`, the
  MAAP conflict through the composition): held at 29 s, declared by 31 s (was 19 s / 21 s), from the same clauses.
- `sw/firmware/ctrl/test/srp_talker_mutants.py`: `CHANGED`/`LATEST` renamed; `REDECLARE` the new define; the
  one-LeaveAll and drop-the-terms plants restated on the new terms; needles restated to the new words; two new plants
  (section 3). 53 Talker plants (51 before).
- `sw/firmware/ctrl/test/srp_mutants.py:87,421,454`: three LeaveTime plants' needle restated (`...,500,1000` ->
  `...,500,SRP_LEAVEALL_CS`), the same defect, each still caught.
- Docs: `sw/firmware/ctrl/srp/README.md` (the Talker paragraph: two longest periods, the values, the reading before
  #951, the width check; the composition's test line), `docs/design/MAILBOX_SPLIT.md` (`TALKER_DECL`),
  `docs/design/SPLIT_CONTROL_MEMORY.md` (forward pointers on the two lines that state the values; a section 13
  subsection with the constant, the images and the rows), `tb/verilator/ctrl_service_budget/README.md`
  (`srp-talker-loss`). Left as written: the dated history in SPLIT_CONTROL_MEMORY.md, and MAAP_FABRIC.md /
  SUBMODULES.md, which quote 35.2.2.8's minimum for the processor's Stream ID move, not this hold-off.

## 3. New checks and their planted mutants
| Plant | Test | Failing words | Caught |
|---|---|---|---|
| `talker-hold-off-two-leavealltime-periods` (the old value, 2 x LeaveAllTime) | `Talker.ChangedDestinationWaitsTwoLongestLeaveAllPeriods` | "no Talker of a changed destination is declared before the hold-off ends" | 8x8/2if and 1x1/1if |
| `talker-hold-off-two-leavealltime-periods-after-a-conflict` (the old value) | `SrpGate.F895ARangeLostWithdrawsAndTheNewRangeWaitsTheHoldOff` | "a changed destination waits two of the longest LeaveAll periods after the Leave" | 8x8/2if and 1x1/1if |
| restated: `talker-hold-off-one-leaveall`, `-drops-the-transmit-term`, `-drops-the-join-and-transmit-terms`, `-rounds-the-transmit-term-down`, `talker-lapse-starts-no-hold-off`; `short-leave`, `latency-leave-origin`, `walk-leave-shortened` | as before | the restated words | all, both campaigns |
| width check (not a campaign plant: a compile refusal) | `held_cs` planted `uint8_t` | `static assertion failed: "held_cs holds the hold-off"` | refused |

The old value put back in a scratch copy fails, by name, at 1x1/1if and 8x8/2if: `ChangedDestinationWaitsTwoLongest
LeaveAllPeriods` (declared before 30 s; 20,630 against 30,570 ms), `...AfterTheLatestLeave`,
`DestinationChangeWhileValidWithdrawsTheOld`, `ResetKeepsAnUnchangedSourceAndHoldsAMovedOne`, and the composed
`SrpGate.F895ARangeLost...` at 8x8/2if.

## 4. Image diff (base `0839453f` against head `e5dee83b`, 20 images; `4224df63` byte-identical to `e5dee83b`)
- Base builds reproduce the train's recorded budget image hashes, 12 of 12.
- Every image: of its linked inputs (39 or 44), only `srp_mbx.o` differs (archives compared by member); in it only
  `li a3,2023` -> `lui a3,0x1; addi a3,a3,-1073` (3,023; 2,027 -> 3,027 at 8x8/1if; 2,030 -> 3,030 at two
  interfaces), and its `.eh_frame` advance, which the link discards. In the map only `.text.declare_sources` grows,
  +4 B; what follows it moves +4 B (`.text`), +8 B (`.rodata`, its alignment); sram does not move.
- Relinked with relocations kept (`-Wl,-q`; loadable bytes equal to the built image, both sides, every image), the
  listings with every address field named by its relocation differ in exactly 3 lines: the hold-off's encoding.
- Release (all-fabric) image, base and head built in one path: `bios.bin`, `bios.elf` and its disassembly, the ROM and
  RAM init files, `libmilan_baremetal.a`'s member and the gateware `.v` outside its date comment are identical.
- Platform ledger: PASS at both, every point the same RAMB36 count.

## 5. CPU rows (receipts `cpu/`)
No code path changes (section 4), but `declare_sources` is in the hot region (hot-list entry 192 of 297), so the hot
code after it fetches 4 bytes later and fetch-cache line boundaries move. Arm A at 1x1/1if is 99 groups and 714 s
simulated (about a day of CPU per point at this host's rate), so the legs measured, on the base image and the head
image, each with its own clone and build (`build.build`, as run.py builds by default), were:
- the `valid-destinations` arm, every group (`srp-talker`, `srp-talker-loss`, `srp-talker-held`: the legs the hold-off
  reaches), at 1x1/1if and 8x8/1if;
- arm A's `srp`, `backlog-owed`, `datapath-events`, `aecp` at both, and `aecp-largest-notice` at 1x1/1if (arm A at
  8x8/1if has no such group).

| | 1x1/1if arm A | 1x1/1if vd | 8x8/1if arm A | 8x8/1if vd |
|---|---|---|---|---|
| rc, STATED, share | 0, none, 0 of 940 | 0, none, 0 of 15,106 / 15,051 | 0, none, 0 of 830 / 832 | 0, none, 0 of 66,974 / 67,475 |
| probes, verdicts changed | 50, 0 | 16, 0 | 45, 0 | 45, 0 |
| misses base / head | 7 / 7 (backlog-owed, tsn-c-stack #26) | 0 / 0 | 7 / 7 | 0 / 0 |
| largest difference | +0.171 ms, `backlog-owed.service.srp.last` 7.150 -> 7.321 of 20 | +0.156 ms, `mrpdu.periodic` 2.506 -> 2.663 of 49 | +0.045 ms of 20 | -7.065 ms `srp.talker_loss` 184.154 -> 177.088 of 220; +1.728 ms `mrpdu.join` 1.663 -> 3.392 of 49 |

- Same instructions where the passes fall the same: `srp` 860,482 / 860,482 (1x1/1if), `aecp-largest-notice` 421,938
  / 421,938, `datapath-events` 348,449 / 348,449; at 8x8/1if arm A every probe's pass the same instruction count (45 of
  45). Per-pass medians within 0.4 %.
- At 8x8/1if `valid-destinations` the loops fall out of step from each group's withdrawals: about one pass a
  centisecond, more in `srp-talker`, fewer in `srp-talker-loss` (`cpu/control/passes-per-second.txt`).
- **Control (scratch only):** the base's value with one `nop` after its store, the head's placement (its listing
  differs from the head's in those 4 lines only). `srp-talker-loss` at 8x8/1if: `srp.talker_loss` 176.954 ms (head
  177.088, base 184.154), and every declaration row equal to the head's to the microsecond. The rows follow the code's
  placement, not the value. Its `srp-talker` follows the head too: 34,434 passes (head 34,431, base 33,619), the
  same count each second, 824.5 M cycles (head 824.3 M, base 793.7 M), and every row the head's to the microsecond
  (`cpu/control/`).
- `flip_grade.py --check` (FAIL at 8x8/2if by design, as at the base and the train's record), `--point 1x1/1if`
  (PASS), `load_grade.py --check` (PASS), `shape_costs.py --check` (PASS): byte-identical output at base and head.
- No group runs a hold-off to its end on either image (the longest, `srp-talker`, withdraws at about 15 s of 21).

## 6. Gate table
Code head `4224df63` (every gate below), `0d1eb8e4` the final head (docs only after it). The first run at `e5dee83b`
gave the same results (receipts `gates/e5dee83b/`).

| Gate | Result |
|---|---|
| Talker arms (srp_talker.cpp 1x1/1if and 8x8/2if, SrpGate 8x8/2if) | PASS 16 + 16 + 9 (in the firmware gate's suites) |
| Firmware gate, 4 shards (`--require-rv32 --self-test`) | PASS: suites 74 verdicts, 0 failed; control campaign 825 of 825; AECP campaign 366 `[ok]`, SRP campaigns 513 `[ok]` (106 `[ok] talker-` = 53 x 2), 0 escaped |
| `fw_coverage.py --selftest`, `--check --jobs 4` | PASS (40 files) |
| Twin, twin-plants, twin-maps, twin-maps-plants | PASS, 0 findings, every plant refused; counts as at `e5dee83b` |
| Docs builder legs 0 and 1 (at `0d1eb8e4`) | PASS, each with one NOT RUN arm the tree declares. Leg 0's first run shared its clone with the docs steps and was refused at its end ("source bytes differ: tb/verilator/csr/Makefile"): step 84, `check_entity_shape.py --self-test`, plants a control in that file and restores it, and the leg read it then. Re-run in its own clone: PASS (`gates/final/builder-leg-0*.txt`) |
| Docs workflow steps (at `0d1eb8e4`) | PASS, 104 of 104 at `0d1eb8e4`, tracked files unchanged after them. The candidate's own `act_ci.py` self-test is not run: AGENTS.md runs it only inside the CI job. Installs are skipped, and the two builder legs run apart (`gates/final/docs-workflow-steps.txt`) |
| Table graders | identical to the base (section 5) |
| Images, release image | section 4; `4224df63`'s 20 images byte-identical to `e5dee83b`'s |
| Width check planted (`held_cs` uint8_t) | refused at compile time |

## 7. Reference device
Not measured. Provoking a MAAP conflict on the reference device needs bench access, which this lane may not use.

## 8. Open questions / STOP conditions
- Milan v1.2 Table 4.3 gives LeaveAll as 10 to 15 s with a +/-0.5 s tolerance; the ruling's derivation takes
  1.5 x LeaveAllTime (about 30.2 s) without it. Implemented as ruled; flagged.
- Procedure note: in a scratch clone (not the lane), submodule origins were set to their `.gitmodules` URLs for the
  builder legs' origin check before running the `rev-parse --show-toplevel` check the lane rules ask for; checked
  just after: each command hit its own submodule, the superproject's origin unchanged.

## 9. Posting
- `[A801] TAKEN`: #951 issuecomment-7007407112.
- `[A801] REVIEW READY`: #951 issuecomment-7011711156 (the text is `REVIEW-READY-comment.md`).
- Nothing else posted; no existing comment edited. Nothing pushed; the PR body is `PR-BODY.md` (base `dev-soft-core`,
  `Closes #951`, `Relates to #665`), for the manager to open.
