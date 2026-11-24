# HANDOFF r1: [A834] milan-fpga pin bump to lwSRP d1bb4f4e

Status: **STOP: one brief condition is not met** (03:35 CET 2026-11-24). Everything else is done, with evidence.
Head `dbba60e68a6e4a46f80e381c30ff823ee4ff7484` on `20-lwsrp-pin-d1bb4f4` is pushed (remote head verified). The PR is
not opened. Nothing of this lane is running.
ETA: none. The lane waits for the owner's decision on the LUT/FF growth below. If the growth is accepted, the head
is review-ready as it stands; `PR-BODY.md` already states the growth as an open decision.

The unmet condition: "Images at 1x1 and 8x8 must not grow in BRAM tiles or LUT/FF." Tiles do not grow anywhere.
LUT/FF of the firmware memory, mapped out of context (`syn/ooc/ctrl_memory_ooc.py`, base and head through
`vivado-slot.sh`, the head mapped twice with identical results), do grow:

| ROM top | Base LUT / FF | Head LUT / FF |
|---|---|---|
| 1x1/1if | 309 / 37 | 299 / 38 (+1 FF) |
| 1x1/2if | 179 / 36 | 171 / 36 |
| 8x8/1if | 51 / 14 | 65 / 27 (+14 LUT, +13 FF) |
| 8x8/2if | 146 / 33 | 169 / 33 (+23 LUT) |

All SRAM tops, and every RAMB36 and RAMB18 count, are unchanged. The cause is content. Vivado builds part of each
ROM in logic, and that logic follows the bytes. The pin adds 60 B of `.text` (lwSRP's `mrp_mad.o`, the reviewed fix),
which shifts every later byte. 8x8/1if's third bank (the 2,048 B its 58.5-RAMB36 ledger adds) goes from 40 to 104 B.
Nothing in scope can avoid it. Offsetting 64 B elsewhere in the firmware would be new, unrelated work.
Owner's choice: accept the growth (tens of LUT/FF), or name a bound.

Outputs: `REVIEW-READY.md`, `PR-BODY.md` (base `dev-soft-core`), `ISSUE-srptx.md`, `receipts/INDEX.md`.

## Commits (one-line, no trailers)

- `3fb8cc76` Reproduce lwSRP #20 at the board (round 1's `edc9167f`, cherry-picked unchanged)
- `002a195b` Pin lwSRP d1bb4f4e, every pin site
- `402834ac` The twin Applicant grade: txLA! alone, txLAF! for an omitted value in a full MRPDU, with its self-test
- `dbba60e6` The idiom gate's two findings in that file (docstrings only)

## Brief items

| # | Item | Outcome |
|---|---|---|
| 1 | Pin `d1bb4f4e` (tree `ba42b837` = `25b5a740`'s) at every pin site | Done: gitlink, `LWSRP_REV`, `SUBMODULES.md`, diagram SVG/drawio/PNG and manifest from `docs/diagrams/submodule_boundaries.gen.py` (no `scripts/regen.sh` exists in this tree; the generator reads the staged gitlink), prose pins in `MAILBOX_SPLIT.md` and both ctrl READMEs, and two lwSRP permalinks (the integrator contract moved from lines 324-326 to 327-329). `SPLIT_CONTROL_MEMORY.md:491` and `ci/image/exec-audit-receipt.json` keep `08ee86e8`: they record what was measured |
| 2 | Reproduction test | Red at `08ee86e8`: 351 of 387 (8x8/1if) and 78 of 86 (1x1/1if) withdrawals never sent as Lv; 39 of 44 tests fail per arm. Green at `d1bb4f4e`: all sent, worst 190 ms (240), 44 of 44; no-withdrawal leg holds |
| 3 | Twin grade with S5 | Both S5 options taken: txLAF! modelled for an omitted value, and the full-MRPDU check is explicit (the frame plus the value's smallest vector exceeds 1500 octets; IEEE 802.1Q-2022 10.7.5.8, 10.7.5.9, 10.7.6.6, Tables 10-3 and 10-4). A correct Lv after the own LeaveAll is graded legal (MSRP and MVRP self-test checks). `leave-all-omission` reads "sends JoinMt". 0 findings on both halves' captures; all 16 plants refused twice, in two runs, at both heads. `twin_mrp.py --selftest`: 10 checks; 5 planted faults each fail a named check (the old rLA! model fails 4) |
| 4 | Gates | All pass (table below), except the LUT/FF condition above |
| 5 | srptx red at the base | Red at `aa30d77f`: wire 1,108, hold 59, licence and both off-grid controls 49 each; `srptx-mutants` fails its control. The same as `854bd723` (1,212 of 1,216 lines identical; the other 4 name the same frames with another delay). At the head: the same kinds, `[TIME]` up (1,185 / 60 / 50), exactly round 1's head counts. Not fixed; `ISSUE-srptx.md` written |

## Gates (receipts in brackets)

| Gate | Result |
|---|---|
| Firmware gate, 4 shards in parallel (MemAvailable 62 GB) [firmware/] | rc 0 each at `402834ac`. Shard 0: 90 arms, 2,244 cases, 0 failures, 44 SRP host arms (the two own-LeaveAll arms among them). Shard 1: 832 of 832. Shard 2: 392. Shard 3: 543; the pin controls name `d1bb4f4e` |
| Own-LeaveAll race, 8x8/1if every input and 1x1/1if [own-leaveall/] | See item 2; re-run at `402834ac`, identical |
| `make twin`, `make twin-plants` x2 [twin/] | 0 findings; 32 refusals (16 x 2) per run; at `dbba60e6` and `402834ac`; no LeaveAll frame near full (least spare 1,359 octets) |
| Load and flip [budget-model/] | Load PASS: 1x1/1if 0.512 (0.70), 0.509 with tsn-c-stack #32; 8x8/1if 0.744 (0.75). Flip 1x1/1if PASS: txL 47.98 ms (49), last 127.43 ms (130 stated, 140 owner), ACMP 29.15 ms (30), R4 13.33 (20), R4L 203.48 (238). Flip 8x8/1if PASS: THE TRANSMIT 77 ms against its row 76.81 ms. All byte-identical to the base `aa30d77f`, so the pin moves none of them; their shifts from round 2 lie in dev between `854bd723` and `aa30d77f`, which changes `load_grade.py` |
| Harness arm A, 1x1/1if [harness/] | rc 0; 99 groups, 0 refusals; 0 of 162,079 passes over THE SHARE (longest 153,382); MRPDU worst 2.318 ms (49); 7 misses, all `backlog-owed`'s egress-hold rows, as recorded before |
| Harness arm A, 8x8/1if | rc 0; 98 groups; 0 of 291,836 over (longest 163,158); MRPDU worst 1.682 ms; own LeaveAll rows 0.492, 0.579, 0.581 ms (49); egress ledger PASS (7 rows under their figures, no new miss); its self-test rc 0; own-LeaveAll window: every pass within THE SHARE, MSRP LeaveAll MRPDU 160.4 ms after its timer, MVRP 0.42 ms |
| answering-every-port, both points | rc 0; 16 groups, 0 misses, 0 over THE SHARE (longest 154,865 and 165,018); notices within 21.34 and 26.22 ms |
| answering-later, both points | rc 0; 8 groups, 0 misses, 0 over (155,174 and 154,995); MRPDU 0.952 and 0.880 ms; notices within 8.29 ms (20) |
| Harness self-test | rc 0 |
| Image ledger `plat_ledger.py --self-test` [ledger/] | PASS, 9 of 9; base PASS too |
| `test_ctrl_memory.py` | 0 failures |
| Pin docs (generator `--check`/`--selftest`, PNG, submodule docs) [docs/pin-docs.log] | rc 0 each |
| `docs.yml` steps [docs/] | All pass at `dbba60e6`, with the renderer steps (em-dash, contents) run with the pinned Markdown renderer and builder leg 0 re-run with the SDK at `$HOME/br-milan-rv32`. The 4 hosted-runner steps are not applicable (no event payload or run id) |

## Image byte deltas (every image) [ledger/image-deltas.txt, ledger/margins.md]

Every image: `.text` +60 B (lwSRP `mrp_mad.o` 13,155 -> 13,219 B). No other object or section changes, and no
stack frame changes.

| Image | ROM base -> head | Banks | Margin | SRAM | Tiles |
|---|---|---:|---:|---|---|
| platform 1x1/1if | 126,536 -> 126,592 (+56) | 126,976 | 384 | 56,736, +0 | 45.0 |
| platform 1x1/2if | 128,136 -> 128,192 (+56) | 129,024 | 832 | 59,040, +0 | 46.0 |
| platform 8x8/1if | 139,304 -> 139,368 (+64) | 141,312 | 1,944 | 98,160, +0 | 58.5 (ledger) |
| platform 8x8/2if | 140,880 -> 140,944 (+64) | 141,312 | 368 | 115,504, +0 | 63.0 (ledger) |
| harness 1x1/1if (mapped; stand-ins +56) | 117,352 -> 117,416 (+64) | 118,784 | 1,368 | 55,568, +0 | 43.0 |
| harness 8x8/1if (mapped; stand-ins +64) | 130,088 -> 130,144 (+56) | 131,072 | 928 | 96,928, +0 | 56.0 (budget 56) |

**8x8/1if ROM margin.** It is no longer exactly its two banks. On live dev the base needs 139,304 B, 40 B past two
banks (139,264), so dev's 58.5-RAMB36 ledger (`4a08c90d`) adds a 2,048 B third bank. At the head that bank holds
104 B, a margin of 1,944 B. The harness's 8x8/1if image sits at its 56-tile budget with 928 B of ROM margin.

## Open points for the manager

1. **LUT/FF decision** (above): the one brief condition this head does not meet.
2. **File `ISSUE-srptx.md`**: srptx red at `aa30d77f` and before, in no CI workflow.
3. **PR**: open it from `PR-BODY.md` once point 1 is decided. It uses "Refs kebag-logic/lwSRP#20"; no milan-fpga issue
   covers this pin bump (searched: #969 and #608 are other defects). AGENTS.md wants a public issue per task, so the
   manager may want one before the PR.
4. **Tool notes.** `scripts/regen.sh` does not exist; the generator is `docs/diagrams/submodule_boundaries.gen.py`, and
   it reads the staged gitlink, so stage the submodule first. The firmware shards need the RV32 SDK on PATH. The builder
   legs need it at `$HOME/br-milan-rv32`, as the hosted runner provisions it.
5. **Observation, not confirmed:** `dispatch-build/keys/` appeared in the checkout when the shards started (the shard
   dispatch self-test's relative build path) and made the builder legs refuse the checkout as having untracked source.
   I did not establish that an uninterrupted run leaves it. A confirming probe was refused by the session's permissions.
6. **Housekeeping:** the base worktree `/data-2/milan/tmp/lwsrppin-a834/base` (`aa30d77f`, detached) and 8.5 GB of
   scratch remain for re-runs; `git worktree remove` and deleting the scratch directory clear them.
7. My first shard launch lacked the SDK on PATH and was stopped within a minute. The plants run built with the system
   Verilator 5.054 was also stopped and redone with the pinned 5.050. No receipt comes from either.

STOP: the 8x8 firmware memory grows in LUT/FF (8x8/1if ROM +14 LUT and +13 FF, 8x8/2if +23 LUT, 1x1/1if +1 FF; out-of-context map, reproduced) against the brief's "must not grow"; tiles unchanged; all other gates pass at dbba60e6, pushed; owner decision needed
