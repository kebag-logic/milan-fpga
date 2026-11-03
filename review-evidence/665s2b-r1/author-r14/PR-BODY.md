[A683q]

## Contents

- **[Status](#status)** — REVIEW READY at the head below: `dev-soft-core` `a68536fa` merged, the split CPU on `sys` at 100 MHz, every measured row and pass fitting. `665-s2b-cycles` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout, submodules and environment.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What is left, and the decisions for the owner.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

REVIEW READY at `a3f23bbabdd9800177224432361fcd41b53bf882`. Round 14 of lane S2b, on round 13's `4f58214f`: commits added on top, no rebase, no force, no merge. `dev-soft-core` is still `a68536fa`, which the head contains.

A save's progress is now bounded by a mechanism, whatever the input: an owed step not run for more than two centiseconds is the next pass's alone, before any input. A SET_NAME of the entity is durable at most 12,110 ms after its change at 8x8/2if and 4,070 ms at 1x1 on a flash with no busy time, and the harness holds a save to it with every receive channel at its contract refill rate and with no pass that takes nothing. Every measured row the CPU decides and every pass still fits at 100 MHz, at both points, in both arms, with the two drafts staged and without them; the least margin is the 8x8 last SRP record's, 0.77 ms (17.23 ms against 18, arm A, in a save's window). The three egress-held rows stay with tsn-c-stack #26.

The 32x32 figures are an estimate, restated at this head, and they miss: the last AECP and SRP records and the per-pass share under every reading (section 14 of `SPLIT_CONTROL_MEMORY.md`).

## Linked Issue / roles

Relates to #665

Executor: `[A683q]`
Internal cleared-context reviewer: `[R711]`
External reviewer: `[R712]`

## Description

### Round 14

Both round 13 reviews were NEGATIVE on one MAJOR (R711-3-F1 = R712-3-F1): since THE STEP, a save advanced only through passes that took no input, and nothing bounded how long input could keep them from coming. The manager's decision: bound it by a mechanism, state the worst case, and test it under the contract's load.

| Item | Change | Evidence |
|---|---|---|
| 1. The mechanism | THE STEP's age limit (`ctrl_loop.h`): once more than `CTRL_LOOP_STEP_AGE` centiseconds, two, have been dispatched since the step last ran or owed nothing, the next pass is the step's alone, before any input, with the deadline read as it starts; it returns one, so the input it held off is taken by the next pass, one step later | `Loop.L13AnAgedStepIsAPassOfItsOwn` and ten planted defects. N measured: in every window the harness stages, at both points, in both arms, with and without the drafts, at most two centiseconds were posted between two passes that carried a step (one at 1x1), so no aged step lands among a window's records; at one, aged steps would land in 8x8's windows, where the least margin, 0.77 ms, is below a step, 0.96 ms. Every row and every pass fits at this head (below) |
| 2. The bound | A save is durable at most 1,000 ms (DR2a) + S × 3 ticks + 10 ms after its change; S is its steps after the first-dirty window. A SET_NAME of the entity marks both its names: at 8x8/2if S = 370 and the worst case is 12,110 ms, at 1x1 S = 102 and 4,070 ms, with no flash busy time (`nvm_store.h`, `save_window.bound_ms`). `save-held` holds every receive channel at its contract refill rate with its bursts through a whole save; `save-starved` adds a grandmaster change as every pass starts, so no pass takes nothing | 8x8/2if, arm A / arm B, without and with the drafts: `save-starved` durable 12,087.0 / 12,087.0 and 12,087.1 / 12,088.0 ms after its change, within 12,110; `save-held` 4,696.9 / 4,696.7 and 4,697.0 / 4,731.1 ms; 0 passes over the share in either group; each channel's longest record within its bound, SRP at most 14.81 ms against 18. 1x1: `save-starved` 4,049.0 / 4,048.1 and 4,047.9 / 4,048.0 ms within 4,070. The plant with the age limit removed: `CONTROL store-step-ageless caught`, the save not durable 12,618.4 ms after its change |
| 3. One build a pass either way (R711-3-F2) | The poll reads whether the interface with the turn builds before it visits either (`turn_builds`) | `Srp.JointLinkChangeBuildsInterfaceOneBesideAWithdrawal`, the mirrored case, fails on the plant `build-turn-read-after-its-visit`, the old reading; the review's link groups at 8x8: `y-links` 1.741 / 1.809 ms (arm A / arm B), `x-links-same` 1.531 / 1.556 ms, no pass over |
| 4. Every pass that carries a step (R711-3-F3 = R712-3-F2) | The harness prints every pass that enters the store's step, idle or work, with the store's own CPU time | Over every group of every leg: the longest pass that carries a step is 1.22 / 1.23 ms at 1x1 and 1.29 / 1.27 ms at 8x8 (arm A / arm B, without the drafts), 1.18 / 1.18 and 1.25 / 1.25 ms with them; the longest step's own time 0.97 ms, within `NVM_STEP_US`; each step kind's cost at both points in section 13. Round 13's sentence now gives the lone save's 1.21 and 1.26 ms on one basis |
| 5. The verify phase bounded (R711-3-F4) | `grade.save_phase` refuses a verify window that opens after the save's read-backs have read back every programmed byte, read off the journal reads | The self-test's phase check holds the case and its mutant; the mutant `save: a verify window is graded after its read-backs read back the container` is caught; every leg's 24 windows graded with 0 refusals |
| 6. Residue | R712-3 RESIDUE-1 and R711-3 RESIDUE-1 (section 14's S slope is arm A's at both ends), R712-3 RESIDUE-2 (the read-back step's cost in `nvm_store.h`), with their exact texts; S1 (the room rule at exactly `NVM_STEP_US`) | `SPLIT_CONTROL_MEMORY.md` section 14's S bullet (both texts, with this head's 10.04 ms); `nvm_store.h`'s `NVM_READ_BYTES` comment; `NvmBoth.step_room` with exactly `NVM_STEP_US` left, on the model port, and the plant `step_needs_room_past_its_cost`; R712-3 SUGGESTION-2, the unrounded 1.116 ms in section 14 |

**Found and fixed on the way.** The first held runs showed two things. Their SET_NAME took one of AECP's tokens, so the channel's first burst lost a record: AECP's bursts now start one refill period after the change, and a held group that commits fewer records than it offered is refused by name. And at 8x8 one pass was over the share, 2.135 ms, 1 ms after the change: AECP's mark of the SET_NAME's two names walked the store's records twice, 22,088 cycles, in the pass that drained the first bursts. A record is now marked by its id without the walk (`nvm_rec_id_of`, `nvm_store_changed_id`), with host tests and planted defects, and that pass is 1.711 ms. Every leg ran again at that head. A SET_NAME of the entity marks both its names, which the stated worst case counts. The `srp-poll-extra-read` plant had no site once the poll read every link before its visits; it is re-anchored at those reads and caught.

**A save from its change to durable** against its stated worst case (ms, arm A / arm B):

| Save | Worst case, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| `save`, alone | 4,070; 12,110 | 2,019.2 / 2,018.4 | 2,018.3 / 2,018.3 | 4,697.4 / 4,697.4 | 4,697.4 / 4,698.3 |
| `save-held` | 4,070; 12,110 | 2,019.0 / 2,018.1 | 2,018.1 / 2,018.1 | 4,696.9 / 4,696.7 | 4,697.0 / 4,731.1 |
| `save-starved` | 4,070; 12,110 | 4,049.0 / 4,048.1 | 4,047.9 / 4,048.0 | 12,087.0 / 12,087.0 | 12,087.1 / 12,088.0 |
| `save-starved`, longest gap between flash steps | | 30.98 / 30.97 | 31.08 / 31.05 | 31.33 / 31.25 | 31.48 / 31.42 |

**The rows and the share at this head**, every leg at `21d0e0f6`, whose images the head's equal, and arm A's every group again at the head (below), each family against min(T_svc = 20 ms, its 10 % ceiling):

CPU 100 MHz on sys (the product split CPU clock), bus 100 MHz. Cells are arm A / arm B, ms, bold over the bound.

The four backlog windows:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.78 / 0.77 | 0.72 / 0.71 | 1.32 / 1.32 | 1.23 / 1.23 |
| ADP record, first | 20 | 0.82 / 0.81 | 0.76 / 0.75 | 1.36 / 1.37 | 1.28 / 1.27 |
| MAAP record, first | 20 | 0.80 / 0.80 | 0.75 / 0.73 | 1.34 / 1.35 | 1.26 / 1.26 |
| AECP record, first | 20 | 0.81 / 0.81 | 0.76 / 0.74 | 1.35 / 1.36 | 1.27 / 1.27 |
| SRP record, first | 18 | 2.87 / 2.85 | 2.69 / 2.65 | 5.45 / 5.43 | 5.05 / 5.06 |
| ACMP record, last | 20 | 5.11 / 5.16 | 4.53 / 4.61 | 7.87 / 8.51 | 7.34 / 7.72 |
| ADP record, last | 20 | 3.58 / 3.67 | 3.28 / 3.29 | 5.85 / 6.07 | 5.44 / 5.56 |
| MAAP record, last | 20 | 3.57 / 3.70 | 3.26 / 3.33 | 5.83 / 6.10 | 5.43 / 5.59 |
| AECP record, last | 20 | 10.04 / 10.37 | 9.07 / 9.67 | 14.83 / 15.93 | 13.49 / 14.33 |
| SRP record, last | 18 | 10.67 / 10.59 | 9.88 / 9.64 | 16.35 / 15.90 | 15.58 / 14.87 |
| an ACMP command behind a full acmp ring | 20 | 3.57 / 3.54 | 3.27 / 3.22 | 6.64 / 6.70 | 6.37 / 6.29 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 2.83 / 2.80 | 2.54 / 2.52 | 3.62 / 4.63 | 3.31 / 4.27 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 20 | 0.14 / 0.12 | 0.08 / 0.11 | 0.11 / 0.19 | 0.08 / 0.22 |
| an event behind 15 others | 20 | 0.92 / 0.92 | 0.87 / 0.85 | 1.47 / 1.48 | 1.39 / 1.38 |
| AECP record, last, in the owed window | 20 | **62.93** / **62.95** | **62.93** / **62.85** | **65.13** / **65.13** | **65.13** / **65.04** |
| a response with 7 frames owed ahead of it | 20 | **62.07** / **62.10** | **62.06** / **62.01** | **63.78** / **63.77** | **63.76** / **63.69** |
| an ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

A save's windows (`save_window.py`), 24 at each leg:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 1.43 / 1.44 | 1.42 / 1.32 | 1.96 / 1.91 | 1.84 / 1.69 |
| ADP record, first | 20 | 1.42 / 1.43 | 1.41 / 1.31 | 1.95 / 1.90 | 1.83 / 1.68 |
| MAAP record, first | 20 | 1.46 / 1.47 | 1.44 / 1.35 | 1.99 / 1.93 | 1.86 / 1.71 |
| AECP record, first | 20 | 1.47 / 1.48 | 1.45 / 1.36 | 2.00 / 1.94 | 1.87 / 1.72 |
| SRP record, first | 18 | 2.73 / 2.58 | 2.45 / 2.35 | 4.37 / 4.21 | 4.09 / 3.99 |
| ACMP record, last | 20 | 5.95 / 5.89 | 5.43 / 5.29 | 9.02 / 9.23 | 8.30 / 8.32 |
| ADP record, last | 20 | 4.43 / 4.40 | 4.08 / 3.97 | 6.57 / 6.79 | 6.08 / 6.15 |
| MAAP record, last | 20 | 4.46 / 4.43 | 4.11 / 4.01 | 6.61 / 6.82 | 6.12 / 6.18 |
| AECP record, last | 20 | 10.91 / 10.92 | 9.87 / 10.34 | 15.96 / 16.56 | 14.86 / 15.31 |
| SRP record, last | 18 | 11.46 / 11.22 | 10.51 / 10.32 | 17.23 / 16.91 | 16.48 / 15.56 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 3.55 / 3.53 | 3.31 / 3.21 | 5.42 / 5.35 | 5.03 / 4.87 |

save-held, every receive channel at its refill rate with its bursts:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | 20 | 2.76 / 2.73 | 2.28 / 2.26 | 4.78 / 4.80 | 4.43 / 4.44 |
| ACMP record, every channel at its refill rate, the longest | 20 | 4.39 / 4.32 | 3.66 / 3.63 | 8.11 / 8.17 | 7.17 / 7.09 |
| AECP record, every channel at its refill rate, the longest | 20 | 5.57 / 5.41 | 5.04 / 4.96 | 10.92 / 11.00 | 9.82 / 9.76 |
| MAAP record, every channel at its refill rate, the longest | 20 | 2.82 / 3.01 | 2.27 / 2.54 | 5.30 / 5.33 | 4.84 / 4.85 |
| SRP record, every channel at its refill rate, the longest | 18 | 8.09 / 8.01 | 7.07 / 7.09 | 14.12 / 14.20 | 13.42 / 13.38 |

save-starved, the same and a grandmaster change as every pass starts:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | 20 | 2.85 / 2.82 | 2.37 / 2.35 | 4.86 / 4.88 | 4.51 / 4.53 |
| ACMP record, every channel at its refill rate, the longest | 20 | 4.55 / 4.47 | 3.82 / 3.85 | 8.27 / 8.50 | 7.32 / 7.28 |
| AECP record, every channel at its refill rate, the longest | 20 | 6.10 / 6.09 | 5.60 / 5.54 | 11.49 / 11.35 | 10.36 / 10.35 |
| MAAP record, every channel at its refill rate, the longest | 20 | 2.94 / 2.89 | 2.37 / 2.40 | 5.41 / 5.61 | 4.95 / 4.97 |
| SRP record, every channel at its refill rate, the longest | 18 | 8.67 / 8.69 | 7.65 / 7.68 | 14.60 / 14.81 | 13.88 / 13.89 |

The share is 2.0 ms. Passes over it, of the work passes run, and the longest in ms, arm A / arm B:

| Groups | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| The four backlog windows | 0 of 1264, 1.11 / 0 of 1251, 1.10 | 0 of 1285, 1.01 / 0 of 1250, 1.01 | 0 of 1311, 1.97 / 0 of 1285, 1.92 | 0 of 1313, 1.89 / 0 of 1287, 1.77 |
| A save's windows | 0 of 10748, 1.22 / 0 of 8643, 1.23 | 0 of 11112, 1.18 / 0 of 8633, 1.17 | 0 of 18324, 1.96 / 0 of 11744, 1.95 | 0 of 17871, 1.86 / 0 of 11737, 1.85 |
| save-held | 0 of 3411, 1.03 / 0 of 3395, 1.03 | 0 of 3405, 1.04 / 0 of 3421, 1.03 | 0 of 8474, 1.69 / 0 of 8489, 1.69 | 0 of 8504, 1.63 / 0 of 8499, 1.63 |
| save-starved | 0 of 44390, 0.97 / 0 of 43629, 0.97 | 0 of 39664, 0.97 / 0 of 43670, 0.97 | 0 of 52488, 1.71 / 0 of 52090, 1.72 | 0 of 52624, 1.66 / 0 of 53926, 1.66 |
| Every group run | 0 of 66819, 1.22 / 0 of 57520, 1.23 | 0 of 56068, 1.18 / 0 of 57576, 1.18 | 0 of 88204, 1.97 / 0 of 74225, 1.95 | 0 of 80929, 1.89 / 0 of 76066, 1.85 |

Every row the CPU decides fits; the tightest is the 8x8 last SRP record in a save's window, 17.23 ms in arm A, 0.77 ms under 18. The three egress-held rows miss as before. No pass is over the share in any group of any leg; the longest, 1.97 ms, carries no step.

**32x32, an estimate, restated at this head:** the last SRP record 31.0 / 35.8 / 65.4 ms under S / L / U, the last AECP record 28.3 / 35.0 / 63.7 ms, the longest pass 3.6 / 4.9 / 7.9 ms (section 14 of `SPLIT_CONTROL_MEMORY.md`). gPTP's assumed mean leaves the 8x8 last SRP record 0.32 ms; at the top of its range, 1.116 ms, it is 0.35 ms over; its bound puts it 7.23 ms over.

### Round 13

Both round 12 reviews found passes over the 2.0 ms share that no group staged: a save's flash step beside a composed window's heaviest work, 2.39 and 2.72 ms at 8x8/2if, and both links changing together, 2.08 ms. The share is not amended; each is fixed in code, and each stale statement in text.

| Item | Change | Evidence |
|---|---|---|
| 1. A save in a composed window | THE STEP (`ctrl_loop.h`): the store's centisecond consumer only owes a step; the loop reads the store's clock as a pass starts and, after the polls of a pass that took no event and no record, hands the step the clock's value at which the pass has spent the share. The step is taken only while 1.0 ms (`NVM_STEP_US`) is left; otherwise it stays owed, once. THE SHARE names it | At round 12's head the review's windows reproduce exactly (x-save 2.388 ms, y-save 2.716 ms, y-links 2.081 ms). At this head `backlog-adp`'s window in each flash phase of a save at eight tick phases, both points, both arms, with and without the drafts: 0 of 99,289 passes over the share; a pass carrying a step at most 1.02 ms at 8x8 and 1.22 ms at 1x1. The planted store step (`--mutation store-step-unbounded`, 8x8, arm A): 15 of 24 windows over the share, the longest 2.71 ms, 5 of them with every row within its bound; `CONTROL store-step-unbounded caught` |
| 2. A joint link change | A poll builds one interface at most; the other on the next pass, and it goes first after that | `y-links` 1.76 / 1.82 ms (arm A / arm B), `x-links-same` 1.54 / 1.56 ms, no pass over. `Srp.JointLinkChangeBuildsOneInterfaceAPass` fails on the plant `joint-reset-builds-both` |
| 3. The boot simulation's flash window | The boot SoC on the product's uncached window (`milan_soc.ctrl_uncached_flash`); an export with another is refused; the self-test plants the call's removal | 1x1 25.515 ms, 8x8 64.885 ms to ready (24.660 and 64.271 ms through the cached window at `c954b8a9`, 25.413 and 65.026 ms with the window alone); `PLANT flash-window-cached: caught`, 3 of 3 plants caught |
| 4. Stale statements | The SRP README's share (2.0 ms), the AECP README's 20 ms service bound, the store README's cadence; the platform image's 58.5 tiles; the gPTP additions restated from the table's own units, each a mean or a bound | Section 14 of `SPLIT_CONTROL_MEMORY.md` |
| 5. Residue | A save's time to durable in absolute terms (here and in section 13); the harness README's arm B backlog rows; the interface reset clears `listener_present` (S1, accepted) | `Srp.InterfaceResetClearsListenerPresent`, plant `reset-keeps-listener-present` |

**The first fix was not enough, and its result is kept.** With the room gate alone every pass of the 14 save windows then graded fit, but at 8x8 the deferred read-backs landed in the passes that drain SRP's full ring, and the last SRP record took 18.02 to 18.21 ms against 18 in four blank-check windows. The step now waits for a pass that takes no input, so no record waits on it beyond the pass running when the record arrives.

**The store's steps,** one save with no other load, CPU cycles at 100 MHz, the flash port's and the store's in the step's pass, from a measurement-only build that prints every pass running the flash port (not on this branch):

| Step | 1x1/1if | 8x8/2if |
|---|---:|---:|
| Erase issue | 5,051 | 5,112 |
| Busy poll | 3,994 | 4,710 |
| Blank-check read-back, 128 bytes | 73,491 | 72,841 |
| Page program issue | 95,373 | 95,386 |
| Verify read-back, 128 bytes | 76,234 | 76,737 |

The longest, a page program's issue, is 0.954 ms, within the 1.0 ms the step is given.

**A save from the change to durable,** from the SET_NAME to the end of the step that reads back the container's last bytes, one save with no other load, on the harness's flash model, which has no busy time: at 8x8 4,697.1 ms at round 12's head and 4,697.4 ms at this head; at 1x1 2,018.4 ms. The blank check and the verify read back 128 bytes a tick, 104 ticks each at 8x8, 2.08 s of ticks where a whole page a step took 1.04 s before round 12. The owner's 0.5 s (#823) belongs to the append-only design in Mark II, not to this image, and this PR does not claim it.

**A save's progress.** The store steps only in a pass that took no input. In `backlog-adp`'s window at 8x8 a step owed as the window opened waited until its records had drained, at most 16.95 ms past its tick, and the ticks meanwhile owed it once, so a window delays a save by about a tick. Nothing here bounds that wait under input that never leaves a pass empty.

**The rows with a save in progress** (`backlog-adp`'s window in a save's flash phases; ms, arm A / arm B, bold over the bound):

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 1.48 / 1.46 | 1.41 / 1.37 | 1.85 / 1.87 | 1.71 / 1.81 |
| ADP record, first | 20 | 1.47 / 1.45 | 1.40 / 1.36 | 1.84 / 1.86 | 1.70 / 1.80 |
| MAAP record, first | 20 | 1.51 / 1.49 | 1.43 / 1.39 | 1.88 / 1.89 | 1.73 / 1.84 |
| AECP record, first | 20 | 1.52 / 1.50 | 1.44 / 1.40 | 1.89 / 1.90 | 1.74 / 1.85 |
| SRP record, first | 18 | 2.68 / 2.59 | 2.44 / 2.41 | 4.39 / 4.38 | 4.08 / 4.01 |
| ACMP record, last | 20 | 5.95 / 5.92 | 5.47 / 5.33 | 8.89 / 9.30 | 8.20 / 8.39 |
| ADP record, last | 20 | 4.44 / 4.42 | 4.10 / 4.02 | 6.44 / 6.85 | 5.94 / 6.24 |
| MAAP record, last | 20 | 4.47 / 4.46 | 4.14 / 4.06 | 6.48 / 6.89 | 5.96 / 6.28 |
| AECP record, last | 20 | 10.86 / 11.15 | 10.22 / 10.34 | 15.86 / 16.79 | 14.51 / 15.38 |
| SRP record, last | 18 | 11.17 / 11.14 | 10.60 / 10.31 | 16.99 / 17.29 | 15.79 / 15.46 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 3.57 / 3.55 | 3.32 / 3.26 | 5.29 / 5.40 | 4.87 / 4.96 |

The tightest is the 8x8 last SRP record, 17.29 ms against 18, arm B: 0.43 and 0.83 ms more, arm A and arm B, than `backlog-adp`'s window with no save, since a step can be running when the window's records arrive.

**The rows of the four backlog windows at this head:**

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.78 / 0.79 | 0.71 / 0.72 | 1.32 / 1.39 | 1.23 / 1.24 |
| ADP record, first | 20 | 0.82 / 0.83 | 0.75 / 0.76 | 1.37 / 1.43 | 1.28 / 1.28 |
| MAAP record, first | 20 | 0.81 / 0.81 | 0.73 / 0.74 | 1.35 / 1.41 | 1.26 / 1.26 |
| AECP record, first | 20 | 0.82 / 0.82 | 0.74 / 0.75 | 1.36 / 1.42 | 1.27 / 1.28 |
| SRP record, first | 18 | 2.88 / 2.92 | 2.68 / 2.70 | 5.42 / 5.61 | 5.06 / 5.06 |
| ACMP record, last | 20 | 5.06 / 5.18 | 4.79 / 4.60 | 7.85 / 8.31 | 7.28 / 7.37 |
| ADP record, last | 20 | 3.52 / 3.68 | 3.38 / 3.30 | 5.85 / 6.07 | 5.38 / 5.35 |
| MAAP record, last | 20 | 3.54 / 3.72 | 3.42 / 3.33 | 5.84 / 6.06 | 5.36 / 5.33 |
| AECP record, last | 20 | 9.68 / 10.17 | 9.44 / 9.60 | 14.69 / 15.96 | 13.58 / 14.35 |
| SRP record, last | 18 | 10.58 / 10.47 | 9.74 / 9.58 | 16.56 / 16.46 | 15.33 / 14.81 |
| an ACMP command behind a full acmp ring | 20 | 3.59 / 3.63 | 3.27 / 3.28 | 6.59 / 7.01 | 6.36 / 6.37 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 2.81 / 2.81 | 2.54 / 2.53 | 3.60 / 4.42 | 3.29 / 3.95 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 20 | 0.08 / 0.10 | 0.13 / 0.06 | 0.12 / 0.12 | 0.19 / 0.25 |
| an event behind 15 others | 20 | 0.92 / 0.93 | 0.85 / 0.88 | 1.47 / 1.54 | 1.38 / 1.39 |
| AECP record, last, in the owed window | 20 | **62.90** / **63.01** | **62.90** / **62.87** | **65.10** / **65.31** | **65.12** / **65.14** |
| a response with 7 frames owed ahead of it | 20 | **62.05** / **62.14** | **62.03** / **62.02** | **63.75** / **64.19** | **63.75** / **63.76** |
| an ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

Against round 12's head the 8x8 last SRP record rose from 15.88 / 15.96 to 16.56 / 16.46 ms: a pass of SRP's drain runs 68 more instructions, the clock read as each pass starts, but about 3,300 more CPU cycles, half of them instruction-fetch waits from the moved code layout, and the record waits sixteen passes.

**The per-pass share,** passes over it of the work passes, those that write nothing to the mailbox counted by their run's longest, and the longest in ms (arm A / arm B):

| Groups | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| The four backlog windows | 0 of 1280, 1.10 / 0 of 1251, 1.10 | 0 of 1276, 1.01 / 0 of 1250, 1.01 | 0 of 1314, 1.96 / 0 of 1286, 1.95 | 0 of 1317, 1.86 / 0 of 1286, 1.82 |
| A save's 24 windows | 0 of 11195, 1.22 / 0 of 8643, 1.21 | 0 of 11134, 1.18 / 0 of 8631, 1.16 | 0 of 18088, 1.95 / 0 of 11745, 1.98 | 0 of 18111, 1.86 / 0 of 11742, 1.83 |
| Every group the leg ran | 0 of 19927, 1.22 / 0 of 10496, 1.21 | 0 of 13012, 1.18 / 0 of 10483, 1.16 | 0 of 27214, 1.96 / 0 of 13648, 1.98 | 0 of 20045, 1.86 / 0 of 13645, 1.83 |

**32x32, an estimate, restated at this head.** No such shape exists. U is the assigned four times 8x8/2if; L the line through 1x1/1if and 8x8/2if; S the slope at one interface, from a labelled scratch point.

| Row | Bound, ms | 1x1/1if | 8x8/1if | 8x8/2if | U: 4 x 8x8/2if | L: the line, 1x1/1if to 8x8/2if | S: the streams alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.79 | 1.17 | 1.39 | 5.5 | 3.4 | 2.7 |
| ADP record, first | 20 | 0.83 | 1.21 | 1.43 | 5.7 | 3.5 | 2.8 |
| MAAP record, first | 20 | 0.81 | 1.20 | 1.41 | 5.6 | 3.5 | 2.8 |
| AECP record, first | 20 | 0.82 | 1.21 | 1.42 | 5.7 | 3.5 | 2.8 |
| SRP record, first | 18 | 2.92 | 4.68 | 5.61 | **22.5** (+4.5) | 14.9 | 11.8 |
| ACMP record, last | 20 | 5.18 | 7.25 | 8.31 | **33.3** (+13.3) | 19.1 | 15.8 |
| ADP record, last | 20 | 3.68 | 5.01 | 6.07 | **24.3** (+4.3) | 14.3 | 11.2 |
| MAAP record, last | 20 | 3.72 | 5.00 | 6.06 | **24.2** (+4.2) | 14.1 | 11.0 |
| AECP record, last | 20 | 10.17 | 13.21 | 15.96 | **63.9** (+43.9) | **35.8** (+15.8) | **28.1** (+8.1) |
| SRP record, last | 18 | 10.58 | 14.91 | 16.56 | **66.2** (+48.2) | **37.1** (+19.1) | **31.4** (+13.4) |
| An ACMP command behind a full ACMP ring | 20 | 3.63 | 5.80 | 7.01 | **28.0** (+8.0) | 18.6 | 14.6 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 2.81 | 3.90 | 4.42 | 17.7 | 9.9 | 8.2 |
| An event behind 15 others | 20 | 0.93 | 1.32 | 1.54 | 6.1 | 3.6 | 2.9 |
| The longest work pass | 2 | 1.10 | 1.56 | 1.96 | **7.9** (+5.9) | **4.9** (+2.9) | **3.5** (+1.5) |

The rows that would not fit: the last AECP record under S, L and U by 8.1, 15.8 and 43.9 ms; the last SRP record by 13.4, 19.1 and 48.2 ms; the longest work pass at 3.5, 4.9 and 7.9 ms, over the share by 1.5, 2.9 and 5.9 ms; under U alone the first SRP record by 4.5 ms, the last ACMP, ADP and MAAP records by 13.3, 4.3 and 4.2 ms, an ACMP command behind a full ACMP ring by 8.0 ms.

**gPTP, a labelled assumption,** restated from the table's own units, a frame or a servo run each, 0.4 ms at 40,000 cycles: on a row 1.1 units, 0.45 ms, as a mean (62 units a second over 18 ms); 20 units, 8.0 ms, as a bound, all that can fall in 18 ms on two ports; on a pass 4 units, 1.6 ms, as a bound (two records a channel a pass). At 8x8/2if the last SRP record, 17.29 ms at its worst, keeps 0.26 ms under the mean and is 0.39 ms over at the range's top, 1.1 ms; the bound puts it 7.29 ms over. The longest pass, 1.98 ms, becomes 3.58 ms under the pass bound. So F6's records need their own room in the pass. At 32x32 the longest pass becomes 5.1 ms under S and 9.5 ms under U, and a Pdelay response, two passes, takes 10.2 ms under S, within Milan v1.2 4.2.6.2.6's 15 ms, and 18.9 ms under U, past it. Not measured: no gPTP firmware is linked here.

### Round 12

| Piece | Change | Why |
|---|---|---|
| Merge | `dev-soft-core` `a68536fa`, contract 2.4 and dev's #806, #814, #818, #787 | Assigned. Three semantic conflicts follow below; each is its own commit |
| Split CPU clock | `milan_soc.CTRL_CPU_CD` `sys`, `ctrl_cpu_domain` refuses any other, no CPU clock of its own, no crossing | The owner's decision of 2026-10-30. The all-fabric CPU and the Milan datapath clock do not change |
| CPU budget harness | Built through `ctrl_cpu_cd`; `build.json` records `cpu_cd`, `cpu_hz`, `sys_hz`; a CPU anywhere else is refused, built or reused; the `--cpu-hz` option is retired | One clock, and no figure at another presented as the product's |
| Split boot simulation | The merged S3 harness still drove the CPU from the Milan clock: now `ctrl_cpu_cd`, the boot graded against the approved T_svc = 20 ms | Merge conflict in meaning: boot at 1x1 24.660 ms, 8x8 64.271 ms |
| Platform image | `ctrl_plat_image.py` built RV32I against the split link: now the split hart's flags and audits, with the record mover and the word-wide primitives; `ctrl_memory.LEDGERED`'s `ctrl_plat` size re-measured, 19,944 B, 58.0 RAMB36 within the ledgered 59.0 | Merge conflict in meaning: it no longer linked |
| SRP link change | `reset_interface` withdraws and destroys in the pass that takes it; the next pass's poll builds; SRP's receive waits; a pass of link edges builds once | It was the one 8x8 pass over the 2.0 ms share, 2.21 and 2.22 ms. Events a pass do not set it (labelled experiments: six 2.207 ms, four 2.108 ms) |
| Saved-state read-back | Blank check and verify read 128 bytes a step (`NVM_READ_BYTES`) | A whole page through the product's uncached window and lwSRP's periodic work in one tick put an 8x8 pass at 2.26 ms. A save's read-back takes twice as many ticks: at 8x8 the blank check and the verify are 2.08 s of ticks, and a save takes 4,697.1 ms from the change to durable (measured in round 13 at `c954b8a9`) |
| Harness flash window | Uncached and not executable but in the hybrid-XIP arm, refused otherwise | The cached window read the flash through the data cache, which the product never does: 12.39 ms at 8x8 and 4.07 ms at 1x1 for one pass in each save |
| Harness AECP pacing | Each frame waits a refill period of the channel's token bucket | At 100 MHz the groups outran the refill and the filter refused the frames past its burst: 3 refused probes at 1x1, 15 at 8x8 |
| The two refused windows | Each backlog window opens on a drained event ring; its table and any refusal give the records held at its opening | The window's definition was wrong, not the firmware: it named a population only a drained ring can take, and waited a fixed time for one. With k records held only 16 - k + 1 of the fifteen grandmaster changes commit |
| Docs | `ARCHITECTURE_HW_SW_SPLIT.md`, `SPLIT_CONTROL_MEMORY.md` sections 5, 11 to 13 and new 14, both harness READMEs, `MAILBOX_SPLIT.md`'s access bounds, the SRP, store and platform READMEs | Every figure names its clock. The bare-metal all-fabric image keeps its own clock contract |

The rows at round 12's head, `c954b8a9`, each family against min(T_svc = 20 ms, its 10 % ceiling); round 13 restates them above.

CPU 100 MHz on sys (the product split CPU clock), bus 100 MHz. Cells are arm A / arm B, ms, bold over the bound.

| Row | Bound, ms | 1x1/1if | 1x1/1if, both drafts | 8x8/2if | 8x8/2if, both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.75 / 0.75 | 0.65 / 0.67 | 1.30 / 1.31 | 1.21 / 1.22 |
| ADP record, first | 20 | 0.79 / 0.80 | 0.70 / 0.71 | 1.34 / 1.35 | 1.25 / 1.26 |
| MAAP record, first | 20 | 0.77 / 0.78 | 0.68 / 0.69 | 1.33 / 1.33 | 1.24 / 1.24 |
| AECP record, first | 20 | 0.78 / 0.79 | 0.69 / 0.70 | 1.34 / 1.34 | 1.25 / 1.25 |
| SRP record, first | 18 | 2.79 / 2.80 | 2.50 / 2.56 | 5.35 / 5.29 | 4.99 / 5.00 |
| ACMP record, last | 20 | 5.16 / 5.06 | 4.34 / 4.52 | 7.76 / 7.98 | 7.42 / 7.30 |
| ADP record, last | 20 | 3.65 / 3.59 | 3.18 / 3.22 | 5.81 / 5.85 | 5.26 / 5.08 |
| MAAP record, last | 20 | 3.68 / 3.63 | 3.22 / 3.26 | 5.80 / 5.84 | 5.30 / 5.12 |
| AECP record, last | 20 | 9.67 / 10.02 | 8.72 / 9.48 | 14.41 / 15.16 | 13.79 / 14.05 |
| SRP record, last | 18 | 9.95 / 10.00 | 9.49 / 9.68 | 15.88 / 15.96 | 14.84 / 14.81 |
| an ACMP command behind a full acmp ring | 20 | 3.45 / 3.47 | 3.03 / 3.11 | 6.51 / 6.73 | 6.19 / 6.21 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 2.73 / 2.74 | 2.42 / 2.45 | 3.53 / 4.19 | 3.95 / 4.11 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 20 | 0.12 / 0.12 | 0.11 / 0.10 | 0.25 / 0.23 | 0.23 / 0.09 |
| an event behind 15 others | 20 | 0.88 / 0.89 | 0.78 / 0.80 | 1.44 / 1.45 | 1.35 / 1.35 |
| AECP record, last, in the owed window | 20 | **62.66** / **62.73** | **62.75** / **62.77** | **64.99** / **64.95** | **64.94** / **65.01** |
| a response with 7 frames owed ahead of it | 20 | **62.07** / **61.93** | **61.94** / **61.95** | **63.68** / **63.93** | **63.91** / **63.68** |
| an ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

The share is 2.0 ms. Passes over it of the work passes run, longest in ms, arm A / arm B:

| 1x1/1if | 1x1/1if, both drafts | 8x8/2if | 8x8/2if, both drafts |
|---:|---:|---:|---:|
| 0 of 1277, 1.07 / 0 of 1250, 1.07 | 0 of 1279, 0.98 / 0 of 1250, 0.98 | 0 of 1319, 1.97 / 0 of 1286, 1.92 | 0 of 1310, 1.77 / 0 of 1302, 1.77 |



Out of context, the split CPU on `sys` closes at 100 MHz, WNS +1.605 ns, WHS +0.070 ns, 3,543 LUTs, 5,643 FFs, 9.5 tiles: 405 LUTs, 1,236 FFs and 5 tiles fewer than behind the crossing. The routed split image is lane S9's.

**The 1x1, 4 KiB windows.** At the CPU's 100 MHz, on a drained ring, all four commit their fifteen grandmaster changes with no record held. The composed maximum covers all four, so it is no longer partial: at least 40.25 ms, a lower bound while the two bound-talker windows close with SRP records unreleased.

**32x32 and gPTP** are restated at round 13's head above.

**One CPU, measured** at round 12's head. As built, the split placement already has one hart. The figures below are the split firmware on that hart, and on the SoC core as it ships, cacheless, on `sys` at 100 MHz, arm A. The cacheless core does not fit 8x8.

| Row | Bound, ms | Split CPU, 1x1 | Cacheless RV32IM, 1x1 | Cacheless RV32I, 1x1 | Split CPU, 8x8 | Cacheless RV32IM, 8x8 | Cacheless RV32I, 8x8 |
|---|---:|---:|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.75 | 1.56 | 1.58 | 1.30 | 2.90 | 2.93 |
| ADP record, first | 20 | 0.79 | 1.60 | 1.62 | 1.34 | 2.94 | 2.98 |
| MAAP record, first | 20 | 0.77 | 1.58 | 1.60 | 1.33 | 2.92 | 2.96 |
| AECP record, first | 20 | 0.78 | 1.59 | 1.61 | 1.34 | 2.93 | 2.97 |
| SRP record, first | 18 | 2.79 | 5.44 | 5.63 | 5.35 | 11.37 | 11.72 |
| ACMP record, last | 20 | 5.16 | 9.98 | 10.45 | 7.76 | 16.08 | 16.09 |
| ADP record, last | 20 | 3.65 | 7.14 | 7.78 | 5.81 | 11.70 | 11.77 |
| MAAP record, last | 20 | 3.68 | 7.18 | 7.81 | 5.80 | 11.71 | 11.75 |
| AECP record, last | 20 | 9.67 | 17.34 | 19.76 | 14.41 | **26.83** | **28.51** |
| SRP record, last | 18 | 9.95 | 17.98 | **21.63** | 15.88 | **30.26** | **34.52** |
| An ACMP command behind a full ACMP ring | 20 | 3.45 | 6.87 | 7.06 | 6.51 | 14.29 | 14.42 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 2.73 | 5.50 | 5.94 | 3.53 | 8.75 | 7.78 |
| An event behind 15 others | 20 | 0.88 | 1.82 | 1.84 | 1.44 | 3.16 | 3.20 |
| Passes over the 2.0 ms share, longest ms | 2 | 0 of 1277, 1.07 | **3 of 1267, 2.14** | **3 of 1270, 2.35** | 0 of 1319, 1.97 | **62 of 1314, 3.61** | **64 of 1315, 3.85** |

## Authoritative references

- #665 and #640, "Updated 2026-10-31" and their 2026-10-31 and 2026-11-01 comments; the round 14 assignment (#665 issuecomment-6589337173) and the round 13 reviews it answers (this PR's issuecomment-6589042666 and issuecomment-6589327842); the round 13 assignment (#665 issuecomment-6573625213) and the round 12 reviews it answers (this PR's issuecomment-6573244887 and issuecomment-6573608668); the round 12 assignment (issuecomment-6514866239); the 20 ms decision (issuecomment-6495692075); #823's 0.5 s, the append-only design's.
- `docs/reference/FR_NFR.md` 3.4.1 and 3.4.2, NFR-SCOUT-01 and -03; `sw/firmware/ctrl/loop/ctrl_loop.h`, THE SHARE.
- PR #828's `MARK_II_AREA_PLAN.md` and `MARK_II_STREAM_ENGINES.md`, read only.
- IEEE 802.1AS-2011 with Cor1 and Cor2, as Milan v1.2 profiles it; Milan v1.2 4.2.6.2.6; IEEE 802.1Q-2018 10.7.11.

## How to get into the same state

```sh
git fetch origin
git checkout a3f23bbabdd9800177224432361fcd41b53bf882
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

The harness's prerequisites are in `tb/verilator/ctrl_service_budget/README.md`: the product LiteX tree, the pinned RV32 SDK and Verilator, with `COURSIER_MODE=offline` and `SBT_OPTS=-Dsbt.offline=true`.

## How to validate

```sh
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-store-step --mutation store-step-unbounded
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-store-ageless --mutation store-step-ageless
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/split-boot-1x1
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/split-boot-8x8 --shape endstation_ax7101_8x8
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/split-boot-plants --self-test
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --lwsrp third_party/lwSRP --shard 0/4
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test
python3 sw/firmware/gtest/fw_coverage.py --check --lwsrp third_party/lwSRP
python3 sw/builder/test_builder.py --require-rv32
cd tests && behave
```

Expected result / pass criteria: each self-test reports 0 failures and every planted defect caught; the firmware self-test runs as shards 0/4 to 3/4. Each point grades every group, a save's 24 windows and the held saves among them, with 0 refusals, 0 passes over the 2.0 ms share, every save durable within its stated worst case (a `SAVE` line each) and only the three egress-held paths over budget, so without `--record-budget-findings` a run exits 1 on those alone. The planted store step prints `CONTROL store-step-unbounded caught`; the age limit's removal prints `CONTROL store-step-ageless caught`. The boot runs pass at both shapes, and the boot self-test catches 3 of 3 plants, `flash-window-cached` among them.

Evidence on the head `a3f23bba`, each on a clean clone, each rc 0: every `run:` step of docs.yml (64 ran; 31 hosted-only steps not run, each with its reason); the full sweep as four shards, 65 of 65 suites, 2,613,655 checks, 0 failures, each shard's counts round 13's; the firmware self-test's four shards, 622 of 622 mutants caught in shard 1 and every AECP and SRP plant caught in shards 2 and 3; the store's gate, 455 tests and 121 planted defects; firmware coverage, 38 files; the harness self-test, 124 grader mutants caught; the harness at both points, arm A, every group (45 and 44 groups), 0 refusals, 0 passes over the share, every save within its stated worst case, the figures the legs' above; the boot runs at both shapes, 25.477 and 64.584 ms to ready, and the boot self-test, 3 of 3 plants; the builder (its two arms that need another host not run, as before); behave, 508 scenarios; `git diff --check` against `a68536fa`. The harness's images rebuilt at the head equal the measured legs' (6 of 6). The sweep's first attempt stopped in every shard's preflight, in `test_suite_cancellation.py` (#833). In three shards the cleanup reported "owned descendants remain", and in one the lock-wait case timed out. The second attempt is the result above for shards 0, 1 and 3. Its shard 2 was killed for memory twice in `capture_coherence`, once on 8 CPUs and once on 16, because that suite's mutant driver builds one datapath per CPU it may use. Shard 2 then passed alone on four CPUs, with the same command at the same head.

## Known limitations / out of scope

- **The 32x32 rows.** An estimate that misses, listed above. Nothing here builds 32x32.
- **For the owner, none decided here:** which lever closes the last AECP and SRP records and the share at 32x32 (the admitted rings and buckets, D4(b)'s two records a pass, the share, the per-stream polls); which CPU lever 4 means, since the split placement already has one hart; a clock past 100 MHz or a second hart if the firmware's levers do not close it.
- **A save's worst case is this image's, not #823's.** 12,110 ms at 8x8/2if for a SET_NAME of the entity, on a flash with no busy time; a part's erase time adds to it. #823's 0.5 s applies to the append-only design's writer through this same step, and this image does not meet it.
- **The age limit's margin in the heaviest window:** a step there is held off for at most 26.4 ms with two ticks in the gap, about 3.6 ms short of the third, which would put an aged step among the window's records; a change that lengthens that drain must measure it again.
- **The step's room:** the longest step, a page program's issue, is 0.96 ms of the 1.0 ms `NVM_STEP_US` gives it; a slower flash port or a longer step must restate that constant (the harness reports every step's own time, and no gate holds the figure yet).
- **The least margin** is 0.77 ms, the 8x8 last SRP record with a save in progress; gPTP's assumed mean, 0.45 ms, fits it, its bound, 8.0 ms, does not.
- **The three egress-held rows** stay with tsn-c-stack #26.
- **The drafts** (lwSRP, tsn-c-stack) are measured staged and are not pinned here.
- **The platform image's hot list:** four entries name the size fixture's callbacks and place nothing in that image.
- **No fabric option outlives the switch-over:** nothing here adds one.
- The hybrid-XIP arm still misses T_svc on every path, so D3's rule stands.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (this round's are; #665 stays open)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
