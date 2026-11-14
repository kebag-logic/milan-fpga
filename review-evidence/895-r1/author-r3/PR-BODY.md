[A775]

## Contents

- **[Status](#status)** — STOPPED at the head below: a stated pass cost at 1x1/1if in this lane's `valid-destinations` arm, over since the sync merge; what round 3 did, fixed and ran.
- **[Linked Issue / roles](#linked-issue--roles)** — Public tasks, executor, and independent reviewers.
- **[Round 3](#round-3)** — The sync with #810's head, #905, the round 2 residues, and the ruling of 2026-11-13 on the first STOP.
- **[The CPU budget harness at this head](#the-cpu-budget-harness-at-this-head)** — Every arm at both points, and the two stated costs found over on the way.
- **[Acceptance 4: no regression beyond stated deltas](#acceptance-4-no-regression-beyond-stated-deltas)** — The load and every flip-gate figure, from this head's legs.
- **[ROM ledger](#rom-ledger)** — Every point, at the new base, the merge and the head.
- **[Description](#description)** — The validity gate and the declarations (rounds 1 and 2), and each source's stream_id (#905).
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout, submodules and environment.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this does not do, and the items for a decision.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

**STOPPED** at `9e30c2c383ced58b0b2b87e774ea3b63d6389514` (`895-talker-redeclare` -> `dev-soft-core`), round 3. **Not REVIEW READY.** Its firmware is `cf5b1441`'s; `9e30c2c3` changes documentation only.

The branch history:
- Base `66f71326`, then #810's round 29 heads `7f50ee6a` and `b2d39235`, each merged by one merge commit.
- Rounds 1 and 2 to `18300f6e`.
- Round 3 merged #810's head `084cf7a8` (`665-s2b-cycles`; #810 is open and not in dev-soft-core) by one merge commit, `cd6d79b6`, then added this round's commits.

No rebase, no force, no amend. No RTL, mailbox-contract, tsn-c-stack, lwSRP or donor change; tsn-c-stack stays at `715589c` (#810's). No bound, cap, ceiling or ledger entry changed. The PR lands after #810.

**The STOP: a stated pass cost cannot be held at 1x1/1if.** In this lane's `valid-destinations` arm (`srp-talker`, `srp-talker-loss`), a pass given whole to a build of one MRPDU takes up to **46,489 CPU cycles**. `CTRL_LOOP_BUILD_ONE_PASS_US` (`ctrl_loop.h`) states **43,000 (430 µs)** at 1x1/1if, so `whole_grade.py` prints four passes as `STATED` and the leg fails.
- It comes from the sync merge. The same build-one pass (`srp-talker-loss`, sys 327.5 M) takes 35,270 cycles at round 2's head and **45,339 at the merge `cd6d79b6`**, before any round 3 firmware. It is 46,528 at `f1f21546`, 45,566 at `a9fd4415`, and 45,452 at this head.
- The cause is data-cache layout. Committed-PC traces of that pass (round 2, and this round's 8 B firmware in its first form, 45,204 cycles) show the same instructions (6,798 / 6,795) and the same instruction refills (130 / 129); load/store waits grow from 28,468 to 38,405 cycles, spread over SRP's and MRP's functions.
  - The split stack is the 8 KiB after `.bss`, the data cache's own size.
  - #810 grows `nvm_stage` by 110 B and adds the store's 552 B `nvm`. That moves the 1x1/1if stack 368 B against SRP's objects, which stay at the same addresses ([`SPLIT_CONTROL_MEMORY.md` 9](../docs/design/SPLIT_CONTROL_MEMORY.md#where-the-stack-falls-in-it)).
- #810 stated 430 µs over its own arms' groups; this arm is #895's. One of these needs a decision; none is this lane's to take:
  - a restated figure (the rule's +5 % gives 490 µs; THE RETRY's search reads it);
  - a stack placement that does not move with `.bss`;
  - this arm left out of the stated set.

What ran at this head (clean clones of `cf5b1441`):
- **The CPU budget harness**, every group of every arm at both points ([below](#the-cpu-budget-harness-at-this-head)). The only `STATED` lines are the four above. 0 refusals; arm A has 7 of 945 and 7 of 996 budget misses, the merged head's seven (tsn-c-stack #26); every other arm has 0.
- **The full firmware suite** (`test_ctrl_firmware.py --require-rv32`, no self-test): 79 results PASS, 0 FAIL, the tree clean after.
- **Firmware arms** maap, maap_if2, talker (`srp_talker` at both points, `SrpGate` at 8x8/2if), the SRP composition at one and two interfaces, unit, hot: all pass.
- **Plants:**
  - the five #905 Talker plants are caught on their words at 8x8/2if and 1x1/1if;
  - the control campaign, cut to the 80 mutants a MAAP-adapter or mailbox-driver change reaches, catches all 80;
  - the new names-runs check catches its planted defect (the run's count check dropped).
- **Coverage** (`fw_coverage.py --write`): `maap_mbx.c` 161/161 lines and 94/94 branches; `aecp_nvm.c` 113/113 and 90/90; every file at 100 %.
- **The ROM ledger** (`plat_ledger.py`): PASS, with `ctrl_plat` unchanged at every point.
- **The split boot simulation** reaches ready at 1x1/1if, 8x8/1if and 8x8/2if (26.299, 65.016 and 67.085 ms), with 0 findings.
- **srptx:** the licence scenario's 119 stream frames all carry the declared `0200000000010000`, with no `[SID]` finding. The #905 code arm is refused by `[SID]`. `[TIME]` (#906) and the hold `[TX]` (#907) are as at #810's head and the merge.

Not run: the clean-clone gate pass (workflows, the Verilator sweep, the full firmware campaigns) and act. They wait on the decision above.

Against the issues:
- **#895 acceptance 1 to 3** hold as at round 2. The Talker suites pass at both points.
- **#895 acceptance 4,** stated by the ruling of 2026-11-13: the 1x1/1if long-window load from this head's legs is **0.503** at the pin and **0.502** with tsn-c-stack#32, each at most 0.70, from the tables fed by those legs ([below](#acceptance-4-no-regression-beyond-stated-deltas)). The build-one figure above is the one cost over its statement.
- **#895 acceptance 5** holds: every 8x8/2if image is at most 58.5, with no fallback ([ROM ledger](#rom-ledger)).
- **#905 acceptance 1 to 3 and 5** are met; acceptance 4, the hardware run, is the bench lane's. This PR says "Closes #905" once it is REVIEW READY; it is not yet.

## Linked Issue / roles

Relates to #895
Relates to #905 (acceptance 1 to 3 and 5 here; 4 is the bench run)
Relates to #810 (merged here; this PR lands after it)
Relates to #894 (its names patch, carried unchanged)
Relates to #906, #907 (srptx findings, not fixed here)
Relates to #896
Relates to #665

Executor: `[A775]`
Internal cleared-context reviewer: to be assigned
External reviewer: to be assigned

## Round 3

| Item | What answers it |
|---|---|
| 1, the sync | One merge commit, `cd6d79b6`, of #810's head `084cf7a8`; submodule pins are equal on both sides. 8 files conflicted, each resolved from the composed tree: `load_grade.py` (each stated cost the larger of the two sides', both sides defining a cost as "the larger of that measurement and this table's"; 24 keys); `ctrl_memory.py` (#810's KLJ3 stage, 13,594 B, with #895's `ctrl_plat`, 20,352 B); the ledger's docstring and `test_ctrl_memory.py` (#810's); `coverage.ratchet` (`srp_mbx.c` #895's, `nvm_*` #810's); `SPLIT_CONTROL_MEMORY.md` (#895's section 5 table kept, as at `18300f6e`; section 13 #810's); two READMEs. The split boot simulation boots to ready at all three points at the merge. |
| 2, #905 | The MAAP adapter, `DA_GATE`'s owner, publishes each source's stream_id to `SRC_SID_HI:SRC_SID_LO` while its `DA_GATE` bit is clear: at its start, before any pass and any declaration or PROBE_TX response, and again before each reopening, read from the source port just before ([Description](#each-sources-stream_id-905)). Four unit tests at 1x1/1if, 1x1/2if and 8x8/2if, five plants at both points, and the srptx `[SID]` check on the twin's split half. Its state is 8 B of `struct maap_mbx` (`cd863d40`; [below](#the-cpu-budget-harness-at-this-head)). |
| 3, R835-2-RS1 | `srp_bounds.h`'s parenthetical now reads "(a join or an adoption refused for storage; a withdrawal it meets after a refused build stays owed)", as the report gives it. Comment only. |
| 3, R836-2-RS1 | The acceptance-4 introduction [below](#acceptance-4-no-regression-beyond-stated-deltas) keeps the analytical tables apart from the measured rows. The round 2 REVIEW READY that the residue names is a comment, which this lane does not edit. |
| Ruling (a) | #894's `C4-names.patch` applied unchanged, its own commit `a9fd4415` (`git apply` on `f1f21546`, clean), by ruling 6844175391 and its application to #895 in 6857334948. |
| Ruling (b) | Every 8x8/2if image re-linked at the head: fixture 58.5, `answering-every-port` 58.5, `valid-destinations` 58.5. No fallback, no cap moved. |
| Ruling (c) | srptx `[SID]` graded on its own words (clean at the head; its plant and arm refused). `[TIME]` is #906 and the hold `[TX]` path #907, recorded here and in the milan_dp README; neither is fixed. |
| Ruling (d) | The head's legs, every arm at both points; the graders on them; this body; the STOP. |

## The CPU budget harness at this head

Every group of every arm, at both points, on a clean clone of `cf5b1441` (`run.py --record-budget-findings --record-share-findings`; arm A in parts, merged and regraded as one leg):

| Point | Arm | Groups | Refusals | Budget misses | Passes over the share | Heaviest polls' base, cycles (stated 20,500 / 32,500) | `STATED` | rc |
|---|---|---:|---:|---|---|---:|---|---:|
| 1x1/1if | A (4 parts, merged) | 94 | 0 | 7 of 945 (tsn-c-stack #26's seven) | 0 of 137,125 | 19,479 | none | 0 |
| 8x8/2if | A (8 parts, merged) | 93 | 0 | 7 of 996 (the same seven) | 0 of 246,868 | 27,684 | none | 0 |
| 1x1/1if | `answering-every-port` | 16 | 0 | 0 of 280 | 0 of 17,733 | 18,072 | none | 0 |
| 8x8/2if | `answering-every-port` | 16 | 0 | 0 of 736 | 0 of 13,856 | 31,030 | none (32,597 at `a9fd4415`) | 0 |
| 1x1/1if | `valid-destinations` | 2 | 0 | 0 of 5 | 0 of 2,643 | 14,798 | **4 build-one passes, 45,452 to 46,489 over 43,000** | **1** |
| 8x8/2if | `valid-destinations` | 2 | 0 | 0 of 20 | 0 of 3,016 | 29,093 | none | 0 |
| 1x1/1if | B (`aecp`) | 1 | 0 | 0 of 25 | 0 of 107 | 15,613 | none | 0 |
| 8x8/2if | B (`aecp`) | 1 | 0 | 0 of 39 | 0 of 137 | 24,866 | none | 0 |

Least margins (`least_margin.py`): arm A 9.147 and 9.223 ms (an aged AECP record, 10.85 and 10.78 of 20 ms); `answering-every-port` 7.317 and 6.114 ms (a held AECP notice); `valid-destinations` 20.691 and 20.912 ms (the Talker rows, at most 199.3 of 220 ms); arm B 19.647 and 19.666 ms.

**Fixed on the way (`cd863d40`): #905's state put the 8x8/2if polls' base over.** At `a9fd4415`, `answering-every-port` read `STATED notice-burst-1/-4: a pass's polls base of 32,594 / 32,597 CPU cycles, over its stated 32,500` (`poll_grade.py`, 325 µs).
- Every MAAP poll cost a constant ~2,300 cycles more than #810's (median 7,355 against 5,041).
- A committed-PC trace of the heaviest pass at both images shows the same 13 instruction refills. The extra cycles are waits in the source port and `acmp_declaring`.
- `refresh_demand` asks `acmp_declaring` of every source. Its saved registers had landed on the data-cache set of the size fixture's `image_aecp_bridge.acmp_owner`, which the port loads once a source: two refills a source.
- That set came from #905's 24 B in `struct maap_mbx` and its poll's larger frame. All three 8x8/2if images at `a9fd4415` had the conflict; #810's had none.
- #905's state is now 8 B: one source's `SRC_SID` words in flight at a time, the high word written only on its source's own interface. The frame is back on #810's set, and the median MAAP poll is 5,511.
- **The heaviest polls' base at this head is 31,030** (#810's leg 30,659), and the leg passes.
- A first form that let either interface write the high word was dropped. `talker-sid-opens-before-its-high-word` escaped it at 2if: the other interface wrote the high word before the early-marked gate could open.

**Fixed on the way (`cf5b1441`): the names patch dropped coverage.** At `a9fd4415`, `fw_coverage.py --check` refused `aecp_nvm.c` (branches 89/90 below 88/88). The arc not taken was a name change of a run's type past the run's count.
- A test now changes a type-5 name just past its last run, taken from the fixture's own runs, and requires that nothing is queued.
- The patch itself is unchanged.

## Acceptance 4: no regression beyond stated deltas

Acceptance 4 as amended by the ruling of 2026-11-13 (issuecomment-6840463408): **no regression beyond stated deltas.** The 1x1/1if long-window load stays at most 0.70, and every other flip-gate figure has its delta stated against the base. The figures other than the 1x1/1if load belong to:
- #894: the 1x1/1if rows by every source;
- #890: the 8x8/2if load against 0.75;
- tsn-c-stack #26: the measured egress-held rows.

The flip gate itself is judged at their composition with this change. Acceptance 4 is stated here by that ruling, not as met or unmet.

**The figures are from this head's own legs.** Every measured cost of every leg above is fed by round 1's parsers (S2b's, unchanged: `parts.py`, `eventcost.py`, `costs24.py`, `aecp_kinds.py`) into `load_grade.py`'s two stated-cost tables. Each cost is the larger of the measurement and the committed table's, per section 13's rules (`tables895.py`).
- They move only measured costs:
  - at the pin, 1x1/1if `event.AECP` 65 -> 70; 8x8/2if `event.AECP` 110 -> 120, `event.MAAP` 215 -> 235 and `record.maap` 150 -> 160;
  - with tsn-c-stack#32, the same, plus 1x1/1if `build_one` and `item.mrpdu` 430 -> 490 and 8x8/2if `base` 325 -> 330.
- `poll_grade.py`'s and `ctrl_loop.h`'s figures, which the harness holds every pass to, are not moved. The 490 is the column's own rule applied to the STOP's measurement, not a change to `CTRL_LOOP_BUILD_ONE_PASS_US`.
- The fed tables are graded in a scratch copy. They are not committed: the head moves again with the decision above. R836-2-RS1: the analytical base figures below are `084cf7a8`'s committed tables; the head's are these measured ones.

| Point | Figure | Ceiling or bound | Base `084cf7a8` | Head (fed) | Delta | Owner |
|---|---|---|---:|---:|---:|---|
| 1x1/1if | long-window load at the pin | 0.70 (merge gate) | 0.501 | **0.503** | +0.002 | this lane: HELD, 0.197 under |
| 1x1/1if | the same with tsn-c-stack#32 | 0.70 (merge gate) | 0.499 | **0.502** | +0.003 | this lane: HELD, 0.198 under |
| 1x1/1if | R4 by every source | 20 ms | 74.83 ms | 75.51 ms | +0.68 ms | #894 (over at both) |
| 1x1/1if | R5 by every source | 90 ms | 38.25 ms | 38.54 ms | +0.29 ms | #894 (within at both) |
| 1x1/1if | R6 by every source | 90 ms | 33.65 ms | 33.93 ms | +0.28 ms | #894 (within at both) |
| 1x1/1if | first / last queued notice | 20 / 125 ms | 20.00 / 22.00 ms | 20.00 / 22.00 ms | 0 / 0 | #894 |
| 8x8/2if | long-window load at the pin | 0.75 (#890; `flip_grade.py` holds 0.70) | 0.822 | 0.825 | +0.003 | #890 (over at both) |
| 8x8/2if | the same with tsn-c-stack#32 | 0.75 | 0.770 | 0.773 | +0.003 | #890 (over at both) |
| 8x8/2if | R4 / R5 / R6 by every source | 20 / 90 / 90 ms | 377.98 / 148.68 / 139.23 ms | 379.78 / 149.49 / 139.97 ms | +1.80 / +0.81 / +0.74 ms | #894 (over at both) |
| 8x8/2if | first / last queued notice | 20 / 125 ms | 22.00 / 62.00 ms | 22.00 / 62.00 ms | 0 / 0 | #894 |
| both | a pass's own cost (second column) | | 230 / 355 us | 230 / 360 us | 0 / +5 us | |

`load_grade.py --check` exits 0 on the fed tables. `flip_grade.py --check` exits 1 at both commits with the same OVER set: the 8x8/2if load, 1x1/1if R4, 8x8/2if R4, R5, R6 and the first queued notice. No verdict changes. The one stated cost the legs refuse is the STOP's build-one figure.

## ROM ledger

RV32 images linked by the tree's own `ctrl_srp_image.py` and `ctrl_plat_image.py`, on each shape's split export and runtime (`plat_ledger.py`'s, built per commit). Each commit ran on a clean clone. Figures are rom / sram need in B, then RAMB36.

| Point | Image | Cap | Base `084cf7a8` | Merge `cd6d79b6` | Head |
|---|---|---:|---|---|---|
| 1x1/1if | fixture | 56 | 108,600 / 45,920: 38.5 | 109,576 / 45,936: 38.5 | 109,984 / 45,952: 38.5 |
| 1x1/2if | fixture | 56 | 110,304 / 57,312: 41.0 | 111,368 / 57,344: 41.5 | 111,920 / 57,360: 42.0 |
| 8x8/1if | fixture | 56 | 122,136 / 87,008: 51.5 | 123,096 / 87,040: 52.0 | 122,688 / 87,056: 51.5 |
| 8x8/2if | fixture | 58.5 | 123,808 / 113,168: 58.5 | 124,832 / 113,216: 58.5 | 124,568 / 113,216: 58.5 (360 B left) |
| 8x8/2if | harness `answering-every-port` | 58.5 | 124,116 / 113,232: 58.5 | 125,140 / 113,280: 59.0, refused | 124,876 / 113,280: 58.5 (52 B left) |
| 8x8/2if | harness `valid-destinations` | 58.5 | (no such arm) | 124,992 / 113,216: 59.0, refused | 124,728 / 113,232: 58.5 (200 B left) |
| 1x1/1if | platform | 56 | 113,672 / 46,880: 39.5 | 114,640 / 46,944: 39.5 | 115,056 / 46,944: 40.0 |
| 1x1/2if | platform | 56 | 115,400 / 58,336: 43.0 | 116,464 / 58,400: 43.0 | 117,024 / 58,400: 43.5 |
| 8x8/1if | platform | 56 | 127,256 / 87,984: 53.0 | 128,200 / 88,048: 53.0 | 127,800 / 88,048: 53.0 |
| 8x8/2if | platform | 60.5 (plans 60.0) | 128,960 / 114,160: 59.5 | 129,984 / 114,224: 60.0 | 129,728 / 114,224: 60.0 |

- **`ctrl_plat`** is 17,536, 19,072, 18,176 and 20,352 B at the merge and at the head, so the ledger keys stand.
- **What each change costs an image:**
  - SRP's Talker declarations (#895): 944 to 1,064 B of rom.
  - #905: 640 to 792 B of rom and up to 16 B of sram.
  - #894's names patch: -224 to -240 B at 1x1 and -1,048 to -1,056 B at 8x8.
- **The 8x8/2if images.** Without the names patch both harness arms planned 59.0 at the merge already, and the fixture did too once #905 was in (the first STOP).
- `SPLIT_CONTROL_MEMORY.md` section 5 states this head's table. Section 13 keeps #810's figures as the merge composed them; it is restated with the legs once the decision above is taken.

## Description

### Validity and the declarations (rounds 1 and 2, unchanged this round)

A source declares its MSRP Talker only while its SRP parameters are valid: MAAP holds its destination, and a probe of the last 15 s or a registered Listener asks for it (Milan v1.2 4.3.3.1, 5.3.7.4).
- It declares at once, Talker Advertise with base + n and its TSpec, or Talker Failed (code 1) when its bandwidth does not fit.
- A lapse withdraws it, its licence and TALKER_DECL bit first. A Leave lwSRP refuses stays owed until lwSRP takes it.
- An unchanged destination is declared again at once. A changed one waits two LeaveAllTime periods after the Leave (IEEE 802.1Q-2018 35.2.2.8, Table 10-7).

Round 2's PR description holds the details. This round's merge changes no SRP source.

### Each source's stream_id (#905)

The datapath stamps each source's `SRC_SID_HI:SRC_SID_LO` on its AVTPDUs (`milan_datapath.sv`, `pp_cd_src_stream_id_w`). The contract (`KL_mbx_pkg.sv:345`) says the owner writes both words while the source's `DA_GATE` bit is clear, before it opens the gate and before the declaration or the PROBE_TX response that carries the ID. No split firmware wrote them, so on hardware every frame of a connected split talker carried stream_id 0, and the reference listener received none.

- **Who and what.** The MAAP adapter (`maap_mbx.c`), which owns `DA_GATE`, writes them through `mbx_pub_src_sid`, one register a write. The value is the declaration owner's source port, the port `acmp_declaring` reads. In the platform that is `ctrl_plat.c`'s `stream_id()`: the entity's MAC and the output's unique ID (IEEE 1722.1-2021 7.2.3), the ID its Talker declares and GET_TX_STATE answers.
- **At start.** `maap_mbx_start` writes every source's two words before any service pass and before any bit opens, so before any declaration or PROBE_TX response.
- **Before every reopening.** `declaring` lets a closed source open only once its stream_id has been written since it last opened, and spends that mark when it lets it open.
  - The poll writes the stream_id of a held source one word a poll, the low word first, read from the port at the low word, in a poll that writes no gate.
  - One source's words are in flight at a time, and the high word is written only on its source's own interface.
  - Meanwhile the poll reports work owed, so the next passes finish it and the one after opens the gate.
- **State:** 8 B of `struct maap_mbx`: a 16-bit mask of the sources written, one per interface of those held, and the one high word owed with its source (`_Static_assert(MBX_N_PUB_SOURCES <= 16u)`).
- **What that covers.** A gate that changes is re-published with a fresh stream_id, and a stream_id the port changed while the gate was closed reaches the register before any frame does. A stream_id changed while the gate stays open is written before the next reopening. The platform's never changes.
- **Bounds.** Each interface's poll has one publication write: "a changed gate, or else one word of the `SRC_SID` of a source a gate holds closed for it" (`maap_mbx.h`, maap README). `MAAP_MBX_*_MAX` and every composed pass bound keep their values. `range()` is untouched, and so are the planted defects anchored on it. It does not read the port: the rule that no source query runs inside a MAAP callback stands.

### Tests and planted defects

- **`SrpGate.F905A*`** in `srp_gate.hpp` (the full composition: ADP, ACMP, MAAP, SRP), run at 1x1/1if, 1x1/2if and 8x8/2if. Each builds a history of publication writes from the model's reset and checks:
  - `EachSourceStreamIdIsWrittenBeforeItsGateOpens`: every source's SRC_SID holds its stream_id before any bit opens, each word in its register; a probe opens the gate with the declared ID.
  - `StreamIdChangedWhileClosedIsWrittenBeforeTheGateReopens`: the port's new stream_id, both words changed, is written before the reopening.
  - `GateReopensOnlyOnceItsStreamIdIsWrittenAgain`: a Listener's Leave and the JoinIn a pass later; the reopening waits for both words, and no word is written while the bit is set.
  - `RangeLostClosesTheGateUntilItsStreamIdIsWrittenAgain`: after a MAAP conflict, the gate is closed until the new allocation and both words.
- **`test_unit_driver.cpp` D14:** the writer's two registers, and its refusals.
- **Five plants** (`srp_talker_mutants.py`, 34 in the table), each caught by its test's words at 8x8/2if and 1x1/1if: `talker-sid-unwritten-at-start`, `talker-sid-words-swapped`, `talker-sid-never-held`, `talker-sid-opens-before-its-high-word`, `talker-sid-written-mark-kept`.
- **`Nvm.EveryChangeQueuesOnlyItsOwnedRecords`** now also changes a name past its type's last run (#894's runs). A planted defect that drops the run's count check is caught on the test's words.
- **The simulation check:** srptx's licence scenario on the twin's split half, the host-built platform firmware on `KL_mbx`, the crossing and `milan_datapath` at 1x1/1if, with a peer Listener Ready for source 0. The `[SID]` grade requires a stream to leave and every stream frame's AVTPDU stream_id to be one that a Talker Advertise the split declared on the wire carries.
  - At this head: 119 stream frames, each `0200000000010000`, the declared ID.
  - #810's head's own capture, graded by it, is refused: 119 frames carry `0000000000000000`.
  - The capture plant `stream-id-unwritten` is refused, and so is the code arm "no source's SRC_SID written (#905)". The arm runs by hand with `srptx_mutants.py`'s own build and run, because its clean control is refused by #906's findings.

## Authoritative references

- `hdl/milan/mailbox/KL_mbx_pkg.sv` SRC_SID_LO and SRC_SID_HI (contract 2.4), DA_GATE; `docs/reference/MAILBOX_CONTRACT.md`.
- IEEE 1722-2016 4.4.4.8 (stream_id); IEEE 1722.1-2021 7.2.3; Milan v1.2 4.3.3.1, 5.3.7.4, 5.3.7.5, 5.5.4.1.
- IEEE 802.1Q-2018 35.2.2.8, 10.7.4, Table 10-7 (the declarations, rounds 1 and 2).
- `docs/design/MAILBOX_SPLIT.md` (the publication writers); `docs/design/SPLIT_CONTROL_MEMORY.md` sections 3, 5, 9 and 13.
- `sw/firmware/ctrl/maap/README.md` (the gate, the SRC_SID rule, the service bounds), `sw/firmware/ctrl/srp/README.md`, `tb/verilator/milan_dp/README.md` (srptx), `sw/firmware/ctrl/loop/ctrl_loop.h` (`CTRL_LOOP_BUILD_ONE_PASS_US`).

## How to get into the same state

```sh
git fetch origin 895-talker-redeclare && git checkout 9e30c2c383ced58b0b2b87e774ea3b63d6389514
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
# the product LiteX tree's environment, the pinned RV32 SDK on PATH, Verilator 5.050,
# COURSIER_MODE=offline, SBT_OPTS=-Dsbt.offline=true, PYTHONHASHSEED=0
```

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --build-dir /tmp/fw     # every arm; PASS
python3 sw/firmware/gtest/fw_coverage.py --check                            # PASS, 39 files
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir /tmp/pl  # PASS (0 findings)
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/boot-1x1    # PASS; and the two 8x8 points
make -C tb/verilator/milan_dp srptx      # licence: no [SID] finding; [TIME] (#906) as at 084cf7a8
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --variant answering-every-port \
  --build-dir /tmp/n8 --record-budget-findings --record-share-findings   # rc 0, no STATED line
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --variant valid-destinations \
  --build-dir /tmp/w1 --record-budget-findings --record-share-findings   # rc 1: the STOP's four build-one passes
```

## Known limitations / out of scope

- **The STOP:** the 1x1/1if build-one figure in the `valid-destinations` arm, above. This lane changes no bound and no stack placement.
- **Layout sensitivity.** The split stack moves with every `.bss` change ([section 9](../docs/design/SPLIT_CONTROL_MEMORY.md#where-the-stack-falls-in-it)). At this head the 8x8/2if `valid-destinations` image keeps the per-source conflict that #905's 24 B gave every 8x8/2if image. Its heaviest polls' base is 29,093 against 32,500.
- **Not run this round:** the clean-clone gate pass (workflows, the Verilator sweep, the full firmware campaigns) and act. `SPLIT_CONTROL_MEMORY.md` section 13 is restated with the legs once the decision is taken.
- **Found, for their own issues** (neither from #905): srptx `[TIME]` (#906) and the hold `[TX]` path (#907), as recorded in the milan_dp README.
- **Stated limit of #905:** a source's first opening carries the stream_id written at the start, and a stream_id changed while the gate stays open is written before the next reopening. The platform's stream_id is fixed for the image's life.
- **Round 2's items stand:** the Domain's own leave and join on the refused path, and the Domain adoption's in-place VID change, each for its own issue. The bench run (#895 acceptance 6, #905 acceptance 4) is the bench lane's.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (#895 acceptance 4's build-one figure: the STOP)
- [x] Required tests pass for the changed firmware and checks (above); the full gate pass is not run
- [ ] Current PR head has a successful `rtl-fast` verdict
- [ ] Exact-head `verilator-suites` and `yosys-portability` after ready
- [x] No undocumented requirement/interface change (the SRC_SID writer is the contract's; the MAAP bound's wording follows it)
- [ ] Internal cleared-context review POSITIVE at the exact head
- [ ] External review POSITIVE at the exact head
- [ ] Every review lens covered clean at the merge candidate
- [ ] Candidate merge validated, post-merge containment clean
