# #665 lane S2b: round histories, rounds 12 to 25

Moved out of the PR body by the round 25 ruling (#665 issuecomment-6751196896, item 6), verbatim from round 24's PR body (the PR body at `a30c9986`), and round 25's section from its own (at `3a1d14c2`, by round 26): each round's Description section, and the decisions its Known limitations listed. The PR body keeps the acceptance, the bounds, the load table and the gates.

## Description, rounds 25 to 12

### Round 25

(As round 25's PR body gave it, at `3a1d14c2`.)

**The ruling** (issuecomment-6751196896, on [A683zd]'s STOP at `a30c9986`, issuecomment-6751120577): round 24's gate failed at 1.181 (8x8/2if) and 2.209 (32x32/2if), mostly SRP's retained retry. This round brings 1x1/1if and 8x8/2if under the ceiling in software: (1) the retry bounded by its source; (2) AECP's owed frame costed by what each source sends; (3) ACMP's per-sink walk as a donor change, tsn-c-stack#32, with the gate graded on it; (4) the ceiling at 1x1/1if and 8x8/2if, 32x32/2if reported; (5) two notes; (6) this body under 60,000 characters.

| Item | At this head |
|---|---|
| 1. SRP's retained retry, bounded by its source | `dbd57a7a`. A refused SRP record is retried only once a pool has returned a block (`ctrl_pool_returned`, counted at each return in `ctrl_pool.c`) or lwSRP has reported an Applicant or Registrar change of its interface (`srp_interface.moved`, set in `moved()`) since the refusal, and then at most once a centisecond (`retry_spent`, given back at each centisecond in `tick`). A refusal records what it saw (`apply_receive`). The 1 s give-up and "no other SRP record meanwhile" are unchanged. The basis is below. Four firmware tests at both interface counts, among them a refused record taken on the first pass after the pool frees. Nine plants (`srp_retry_mutants.py`), in the SRP campaign at two interfaces. Two existing plants of the retained receive (`receive-retry-passes-owed`, `receive-retention-short`) escaped under the rule; `3a1d14c2` gives their tests the centisecond and the millisecond that make them fail again. The load gate reads the rule's lines from the tree (`RETRY_RULE`): a copy of `srp_mbx.c` that retries with nothing changed, or every pass a change allows, leaves SRP's term with no source and fails the gate. To fit the 8x8/2if `answering-every-port` arm's ledger, `struct srp_mbx` ends with its two frame buffers |
| 2. AECP's owed frame, by source | `ca403b0c`. A record's owed frame is its response to one recipient, or a command's response with its notice to the registered controllers (at most 16 an AVB interface), whichever is larger, once a record. A registration's probe is its own frame, once its 250 ms retry (Milan v1.2 5.4.5.3). Each kind is measured from the AECP frames the traced legs committed; a probe, which no group stages, is stated at a response's cost. COUNTERS_CHANGED notices, which have a contract rate, are a new term at their holdoff. The single 32-recipient charge is gone, and a plant restoring it fails the gate |
| 3. ACMP's walk, tsn-c-stack#32 | `d32c196c`. The donor change is drafted in its own clone of the TSN stack, branch `32-acmp-dirty-walk`, one commit on `main`, not pushed; its handoff and its PR body, with the keyword line for tsn-c-stack#32, are in the evidence packet, and its four acceptance items are met. The gate states two columns, each measured on this tree's image: `STATED_US` at the pin, and `STATED_US_DONOR` with tsn-c-stack#32 applied at the pin in a scratch build. It grades the second, labelled as owed to the pin move (tsn-c-stack#28, tsn-c-stack#31 and tsn-c-stack#32); this tree's pin does not move. A plant that lowers a cost tsn-c-stack#32 does not move fails the gate |
| 4. The ceiling | `24e5d12a`. 0.70 at 1x1/1if and 8x8/2if. 32x32/2if is reported, labelled as pending the owner's choice (more compute, or per-shape contract rates), with the compute its graded load would need for 0.70. A plant that drops a held point's ceiling fails the gate |
| 5. Also found | `AECP_NOTICES_MOST` (40 at two interfaces, against 136 at 32x32/2if) is drafted for #866, unchanged here. The 8x8/2if `answering-every-port` arm's `rom` margin is in the ledger (`044107a5`, section 5): 12 bytes at `a30c9986`, 324 at this head, 132 over with tsn-c-stack#32 at the pin |
| 6. This body | 21,485 characters. The round histories (rounds 12 to 24) are in the evidence packet, `evidence/ROUND-HISTORIES.md` |

**Item 1's basis.** lwSRP refuses a receive (`-SHLAN_ERROR_NO_MEMORY`) only where an allocation fails: `get_or_create_attr` and `map_reserve` under `rx_on_attr` (`third_party/lwSRP/src/core/mrp_mad.c`). The allocations a replay asks for follow from five inputs, each of which holds or is counted while a record waits:
- The receive filter's answers, `interested_msrp` and `interested_mvrp`, read only the sources (fixed), the sinks' bindings and the Domain's VID. While a receive waits `srp_mbx_bind` refuses, and `transmit` makes no declaration and no Domain change.
- An attribute is created only by an allocation, which leaves the pool no larger. It is freed only by `mrp_reclaim` or a participant's destroy, each a block returned (`ctrl_pool_returned`).
- Every Applicant and Registrar state change goes through `deliver_event_changed` or the leave timer, each reported to the observer (`moved()`).
- An attribute's value changes only by a receive (only the retained one is taken meanwhile) or a declaration (none meanwhile).
- The pool's free blocks increase only by a return.

So a refusal is a function of the frame, the pool and the attributes' states. Equal counts and a clear flag bracket no change that could turn it, and no line was found that reads anything else.

**The load at this head** (`load_grade.py --check`):

| Point | Load at the pin | Load with tsn-c-stack#32 (graded, owed to the pin move) | Ceiling | Compute for 0.70 | Its three largest graded terms | A pass's own cost, us |
|---|---:|---:|---:|---:|---|---:|
| 1x1/1if | 0.466 | 0.453 | 0.70 | 1.00x | SRP's channel 0.150, ACMP's records 0.053, AECP's owed frame 0.049 | 180 |
| 8x8/2if | 0.844 | **0.747** | 0.70 | 1.07x | SRP's channel 0.243, AECP's owed frame 0.076, ACMP's records 0.061 | 275 |
| 32x32/2if | 2.150 | 1.659 | reported, pending the owner | 2.37x | SRP's channel 0.519, owed MRPDUs 0.299, THE TRANSMIT's builds 0.150 | 590 |

The costs tsn-c-stack#32 moves, stated, us (pin, then with tsn-c-stack#32): an ACMP record 280, 265 / 440, 305 / 980, 425 at 1x1/1if / 8x8/2if / 32x32/2if; an ADP record 105, 95 / 240, 125 / 735, 270; ACMP's timer slot 185, 165 / 350, 205 / 845, 330; ACMP's owed frame 65, 35 / 185, 40 / 665, 105; the polls' base 155, 155 / 280, 245 / 590, 570.

**What 8x8/2if would need** (0.747 against 0.70, 0.047 to find). Each of its three largest terms, alone:
1. **SRP's channel, 0.243**: its records 0.203 (405 us, one a 2 ms refill) and one retry a centisecond 0.041. It needs an SRP record, at whose cost the retry is stated, from 405 to 326 us (-20 %), or SRP's refill from 2 to 2.61 ms.
2. **AECP's owed frame, 0.076**: a command's notice to 32 recipients, 340 us once a record (0.068), and the registrations' probes 0.008. It needs a record's owed frame from 340 to 103 us (-70 %), or AECP's refill from 5 to 16.5 ms. A notice is owed only by a command that changed something, which has no contract rate of its own.
3. **ACMP's records, 0.061**, 305 us with tsn-c-stack#32 at one a 5 ms refill. It needs an ACMP record from 305 to 68 us (-78 %), or ACMP's refill from 5 to 22.4 ms.

Only the first closes it alone with a cut under a quarter of its cost. Two together can too: SRP's record -10 % with AECP's frame -35 % finds 0.048.

**32x32/2if** (reported, pending the owner): 1.659 with tsn-c-stack#32, 2.150 at the pin, 2.37x the compute for 0.70. tsn-c-stack#32 takes ACMP's records, owed frame and timer slot from 0.637 to 0.186 there (0.186 to 0.093 at 8x8/2if). What is left is led by SRP's channel (0.519, an SRP record 865 us) and THE TRANSMIT's builds (a build of both of an interface's MRPDUs 10,810 us) with their owed MRPDUs, stated at a build of one's cost (7,485 us; no group stages one), together 0.449. tsn-c-stack#32 moves neither.


### Round 24

**The ruling** (issuecomment-6734415848, on [A683zc]'s STOP at `86849933`): with every source at its contract rate the CPU was loaded 1.009 at 8x8/2if and 2.51 at 32x32/2if (projected), so no tier order bounds a row. This round makes the load right first: (1) merge `dev-soft-core` `1d6bf555`; (2) the long-window load as a graded figure, with a gate and a plant, target 0.70 at 8x8/2if and 32x32/2if; (3) the 32x32/2if costs from measurement on S15's harness (#859), L kept as a cross-check; (4) each cost that grows with the streams cut at its cause, with a gate holding its 8x8/2if cost within 25 % of its 1x1/1if cost; (5) a cited source for each per-pass term of the method; (6) the load table, and stop. The round 23 tier design stays ruled, and its grading waits for a load under the ceiling.

| Item | At this head |
|---|---|
| 1. The merge | `d6252b84`. One code conflict, `milan_soc.py`'s `CtrlMailbox`: this lane's record mover and `dev-soft-core`'s split datapath each rewrote its constructor; both kept. The generated module matrices regenerated. The twin at the merge: 0 findings. It put 8 bytes in the image (ENTITY's `available_index`), and the 8x8/2if `answering-every-port` arm's `rom` went 4 bytes past its ledgered 57.5 tiles; `dc40e2ea` lets the arm's AVB and counters readers share its path reader, 122,868 bytes. |
| 2. The load gate | `tb/verilator/ctrl_service_budget/load_grade.py` (`a9ea6bb8`, `a30c9986`): each source's rate, a contract rate or a protocol timer read from the tree with its clause, times its stated cost, at 1x1/1if, 8x8/2if and 32x32/2if; a point over 0.70 fails it, and so does a term with no source. A pass's own cost is no source and is reported beside it. Five plants and one an arrival bound (each period halved must raise its terms), 18 in all, each shown able to fail. It fails at this head. |
| 3. 32x32/2if measured | Every cost measured on S15's simulation shape with this branch's image and graders, in a scratch clone (S15's own harness runs `dev-soft-core`'s firmware and grades rows and passes, not this image's items); section 14 of `SPLIT_CONTROL_MEMORY.md` puts L beside each: within 10 % for the SRP, ACMP and ADP records and ACMP's timer slot; it under-projects the builds by about half and over-projects AECP's record and owed frame by about double. |
| 4. Costs that grow | Each growing cost's cause found and placed, not cut: the ACMP core's `finish()` walk of every sink after every entry (the TSN stack) in ACMP's record, its owed frame, its timer's expiry and the ADP record; lwSRP's `mrp_rx` and this lane's `snapshot` walk in the SRP record; MAAP's demand refresh and the SRP delivery's walk in the polls' base. The load stays over 0.70 at 8x8/2if whatever this lane's code can cut with its behaviour unchanged (0.79 without the retry), so no cut and no per-item gate is committed. |
| 5. The per-pass terms | Each timer slot at its own expiry rate; the grandmaster event at its message intervals (IEEE 802.1AS-2011 10.7.2.2, 10.7.3.2, 11.5.2.2); the retained SRP record by its retry's own rule: one attempt a poll while it waits, for up to 1 s, no other SRP record taken, and a loop that never sleeps, so SRP's channel brings the larger of its records' rate and its retries' share of a pass, 0.58, 0.56 and 0.59 at the three points. |
| 6. The load table | Below. Rows not graded. |

| Point | Load | Ceiling | Its three largest terms | A pass's own cost, us |
|---|---:|---:|---|---:|
| 1x1/1if | 0.905 | reported | SRP's retained retry 0.581, AECP's owed frames 0.059, ACMP's records 0.056 | 180 |
| 8x8/2if | **1.181** | 0.70 | SRP's retained retry 0.560, AECP's owed frames 0.112, ACMP's records 0.087 | 310 |
| 32x32/2if | **2.209** | 0.70 | SRP's retained retry 0.585, ACMP's owed frame 0.306, owed MRPDUs 0.299 | 610 |

With SRP's channel at its records' rate the loads would be 0.449, 0.819 and 2.054.

### Round 23

**The ruling** (issuecomment-6732443213; the maintainer's decision of 2026-11-09, option B) accepts round 22 as built (the polls by source and the 32x32/2if model point) and changes the structure and the bulk bounds:
1. two tiers: tier 1 is AECP's, ACMP's and ADP's records and the first queued notice, served before any tier-2 work; tier 2 is SRP's records (THE DRAIN), THE RETRY's rounds, THE TRANSMIT's builds and the polls' heavy items, in slices of at most a stated length with tier 1 checked between every two, the slice chosen so that R4 fits at 32x32/2if by the model, and a gate holding each slice to it;
2. THE TRANSMIT's MRPDU build and THE RETRY's round resumable at a slice boundary, with the same bytes on the wire;
3. bounds: tier 1 (R4 and the first queued notice) 20 ms at every shape; SRP's rows (R5, R6) 90 ms, half of MRP's JoinTime; the last queued notice 125 ms, half of the 250 ms a controller waits on an AECP command; the every-source count is the bound;
4. the model at 1x1/1if, 8x8/2if and 32x32/2if, 32x32/2if gating;
5. the rows re-measured on the new image.

**The method.** Round 22's arrival-bound model, its stated costs and its 32x32/2if projection by section 14's L, unchanged, with the tier structure on top: a pass takes its events first (the events-first ruling on PR #668), then tier 1 at its D4(b) cap of two records a channel, then its polls' base, then tier-2 slices until less than a slice is left of THE SHARE, tier 1 checked between every two. A tier-1 row pays its own burst, the slice running when it arrives, the tier-1 work its order puts ahead of it, the window's events and each ordinary pass's own cost; a tier-2 row pays every tier-1 record and event in its window, each pass's own cost and, unless its own source goes first within tier 2, every other tier-2 source's work. Every reading the ruling leaves open is tried and each row reported at its least: the order within tier 1 (in turn, or AECP, ACMP, ADP or the first notice first), MAAP in either tier (the ruling names it in neither), a tier-1 record ending the pass at the slice boundary or taken between two slices, no order within tier 2 or the row's own source first, and slices of 50 to 2,000 us. Two levers beyond the ruling are tried too: the centisecond's consumers in tier 2, and the per-pass cap lifted to THE SHARE.

**The 90 ms bound's timer:** 90 ms is half of 180 ms, the shortest JoinTime Milan v1.2 4.2.7.1.1 Table 4.3 allows (IEEE 802.1Q-2018 10.7.11, Table 10-7), the timer FR_NFR.md 3.4.1's MRP row applies and whose 10 % was the old 18 ms. The firmware configures 200 ms (`SRP_JOIN_CS`, 20 centiseconds), half of which, 100 ms, the 90 ms is within.

**The rows by the method** (W in ms, every source; within the ruling, and with every lever where it differs):

| Point | Row | Bound | The ruling's own reading, slices of 50 to 2,000 us | Least within the ruling | Least with every lever |
|---|---|---:|---:|---:|---:|
| 1x1/1if | R4 | 20 | 14.15 to 15.93 | 8.37 (AECP first) | 6.19 |
| 1x1/1if | ACMP's held record | 20 | 13.99 to 15.77 | 9.49 (ACMP first) | 7.68 |
| 1x1/1if | the first queued notice | 20 | 22.55 to 25.09 | 10.90 (the notice first) | 10.47 |
| 1x1/1if | R5, R6 | 90 | 143.22, 139.42 or none | 64.69, 63.66 (SRP first in tier 2) | |
| 1x1/1if | the last queued notice | 125 | 232.96 or none | 35.38 (its rounds first in tier 2) | 33.88 |
| 8x8/2if | R4 | 20 | 30.82 to 32.44 | 19.38 (AECP first) | 18.52 |
| 8x8/2if | ACMP's held record | 20 | 29.42 to 31.74 | **22.99** (ACMP first) | **21.70** |
| 8x8/2if | the first queued notice | 20 | 41.91 to 44.91 | 13.02 (the notice first) | 12.59 |
| 8x8/2if | R5, R6 | 90 | none | **317.89, 308.47** (SRP first in tier 2) | |
| 8x8/2if | the last queued notice | 125 | none | 114.92 (its rounds first in tier 2) | 105.67 |
| 32x32/2if | R4 | 20 | **107.76 to 108.94** | **56.29** (AECP first) | **48.33** |
| 32x32/2if | ACMP's held record | 20 | 95.66 to 96.84 | **67.84** | **55.40** |
| 32x32/2if | the first queued notice | 20 | 186.87 to 191.46 | **20.83** (the notice first) | 18.20 |
| 32x32/2if | R5, R6, the last queued notice | 90, 90, 125 | none | **none under 2,000** | **none under 2,000** |

No one configuration puts every tier-1 row within 20 ms at 8x8/2if or at 32x32/2if: the latest is at least 30.82 and 107.76 ms within the ruling, and 28.83 and 86.80 ms with every lever. At 1x1/1if the latest is 14.15 ms. The "own source first" orders within tier 2 are each row's own most favourable, not one design for all three.

**What dominates.**
- **R4 at 32x32/2if:** the timer slots' events, 26.65 ms: each of the 11 ordinary passes that take AECP's burst may take one event of every slot, chiefly each interface's ACMP slot, 11 TMR_NO_RESP expiries an interface (16 sinks; Milan v1.2 5.5.2.3, Table 5.26) at a projected 923 us (170 and 340 us at the measured points), 20.3 ms. Then each pass's own cost (9.08 ms; the polls' base projects to 709 us a pass), the ticks (8.24 ms) and its own burst (7.10 ms). Its own burst and the timer events of its fewest eight passes are 26.70 ms with nothing else counted, and one event of every timer slot is 3.16 ms, more than THE SHARE before any record. The slice moves R4 by at most 1.2 ms: its window holds one slice of tier-2 work.
- **Tier 1 at 8x8/2if:** the timer slots' events, 9.02 ms in R4's window (ACMP's slot 5.44 ms), then, in turn, ACMP's records (8.60 ms) and R4's own burst (4.08 ms).
- **The bulk rows at 32x32/2if:** every source's load over a long window is 2.51 of the CPU before any pass's own cost (826 us a pass): SRP's records 0.446 (892 us projected, one every 2 ms by the contract) and their retained retries 0.446, ACMP's and AECP's owed-frame items 0.274 and 0.241, the timer events 0.223, ACMP's records 0.189. SRP's records and the items they make, the tier-1 records and the ticks alone are 1.48. At 8x8/2if the load is 1.009, at 1x1/1if 0.571.

**Not committed:** items 1 to 5. Item 1's first step is the slice chosen so that R4 fits at 32x32/2if by the model, and none does; R4's window holds one slice of tier-2 work, so no tier-2 change, item 2's resumable builds among them, moves it, and a measurement cannot hold a row the bound fails. No prototype was built. The model, its outputs and R4's floors are published with the STOP.

### Rounds 19 to 22

**Round 19** (issuecomment-6707464945) amended the queued-notice ceilings to 25 ms at 1x1/1if and 70 ms at 8x8/2if. It asked for the stated costs as upper bounds (a gate fails when any measured instance exceeds its stated cost), R4 and R5 by construction, and THE DRAIN's limit counted before a record starts. [A683y] stopped with no commit: R4, the first notice at 8x8/2if and R5 could not hold 20 ms by construction.

**The maintainer's decisions of 2026-11-08.** Round 20 (issuecomment-6718341163) allows 22 ms at 8x8/2if for exactly three rows: R5 (a link change composed with SRP's burst), the first queued notice, and R4 (the AECP record beside queued notices). Every other row, and every 1x1/1if row, stays at T_svc, 20 ms; the 25 and 70 ms ceilings stand, and THE SHARE is not amended. Round 22 (issuecomment-6724377734) adds three: the two-interface shapes keep gating the flip; the split's structure must scale to the Mark II target, 32x32 streams, which are 16x16 logical streams each redundant on two networks; and the split bench moves to after the new year, so the loop is restructured instead of a bound changed. [A683z] merged `dev-soft-core` `a9d69c77` (S4 #812, S5 #844) as `3d206bf4`.

**The arrival-bound method** (round 21, issuecomment-6719813882) is the bound since. Each source that can take a pass, a round, a build, an aged step, an event or a poll has an arrival bound in any window W, from its contract rate or its protocol timer, with the clause cited, never from a run. A row's bound is the smallest W at which the row's own work, plus every source's arrival bound in W at its stated cost, fits in W. Each stated cost is the measured maximum over every instance plus 5 %, and a gate fails when an instance exceeds it. The every-source count is the bound; the count of the sources a row's staging makes certain is a diagnostic. Round 21 committed the first queued notice as modelled (`feee6824`, `70703f8d`, `bc98d727`: the first notice 22 ms at 8x8/2if and 16 ms at 1x1/1if, the last 62 and 22 ms, every round held to its stated cost by `round_grade.py`) and stopped: R4, R5 and R6 did not fit, dominated by every ordinary pass's polls at their heaviest measured instance (800 us at 8x8/2if) and by AECP's records waiting behind SRP's whole burst.

**Round 22, the restructured loop** (issuecomment-6724377734):

| Item | At this head |
|---|---|
| 1. The polls by source | Committed (`86849933`). A pass's polls, from ADP's poll's entry to SRP's delivery's return, less its heavy items, are its base, which every ordinary pass is charged; each of eight heavy items runs as its own function, doing its work only once its source has posted it, and is charged by its own arrival bound. `poll_grade.py` holds each pass's base and each item to its stated cost (below); a plant that runs SRP's rebuild in the base and a plant that rebuilds twice are each caught, and eight grader mutants. No firmware changes: the image is round 21's byte for byte. |
| 2. THE DRAIN in slices | Prototyped, not committed. No slice makes R4 fit (its floor, with no poll and no THE DRAIN, is 22.72 ms at 8x8/2if) and R6's floor is 29.66 ms, so no R6 arrival bound can replace THE DRAIN's sum. Measured in slices of 3 at 8x8/2if, SRP's held record goes from 8.405 to 24.475 ms and 10 passes go over THE SHARE. |
| 3. The queue | At 8x8/2if the last notice is 74 ms against 70 once THE DRAIN's pass count is derived (a pass takes at least 2 of SRP's 395 us records, so up to 34 passes may leave some behind), as built or in any slice; the committed search keeps round 21's 4. At 1x1/1if 16 and 22 ms at every count. |
| 4. Bounds | Unchanged. |
| 5. 32x32/2if, modelled | Does not fit (below). |
| 6. Re-measured | The image is round 21's, so are its rows: R4 at most 17.111 ms at 8x8/2if and 11.860 ms at 1x1/1if; the first queued notice 2.385 and 7.662 ms, the last 33.465 and 12.902 ms; the only misses the egress-held rows (tsn-c-stack #26). |

The polls' stated costs, the most measured over every group of arm A and the `answering-every-port` arm plus 5 %, us at 1x1/1if / 8x8/2if, each with its source:

| Item | Source, and its arrival bound | Stated |
|---|---|---:|
| the base | every ordinary pass | 155 / 280 |
| withdraw (`reset_interface`), rebuild (`open_interface`) | a link change, one each an interface (R5's) | 90 / 245, 290 / 630 |
| walk (`mrp_attr_visit`) | a centisecond of lwSRP's timers or a build's declarations (IEEE 802.1Q-2018 10.7.4.1), one an interface a pass | 20 / 60 |
| reclaim (`mrp_reclaim`) | an SRP record or a build, two an interface a pass | 25 / 35 |
| retained (`apply_receive`) | an SRP record refused for storage, retried a poll until it expires; none staged, at an SRP record's cost | 250 / 395 |
| mrpdu (`build_mrpdu`) | a build's MRPDU its ring refused (A3), two a build; none staged, at a build of one's cost | 405 / 1,215 |
| acmp (ACMP's poll, a call that committed a frame) | ACMP's and ADP's records (`mailbox.yaml`) and TMR_NO_RESP (Milan v1.2 5.5.2.3, Table 5.26) | 65 / 185 |
| aecp (`transmit`, a call that committed a frame) | AECP's records (`mailbox.yaml`) and the registrations' probes (Milan v1.2 5.4.5.3) | 225 / 340 |

The 800 us round 21 charged every pass was mostly the `answering-every-port` fixture's own poll, about 53,000 of its 75,836 cycles: a test's stimulus that marks every notice once, which the base leaves out.

**The 32x32/2if model point.** The contract's rates are per channel, the fabric's limiter, so a window holds the same records at every shape, and its tables already hold 16 sources and 16 sinks an interface. The protocol timers scale with the shape's counts: 16 sinks an interface, 68 descriptors with counters, 136 notices a reset can leave pending (`aecp.h`'s rule). Each cost is projected by section 14's L, the line through 1x1/1if (2 streams) and 8x8/2if (16) to 64, whose error at the two measured points is zero by construction. It does not fit: R4's floor is 41.59 ms and R6's 63.04 ms against 20; a pass given whole to a build of both of an interface's MRPDUs projects to 5.75 ms and to a build of one to 3.99 ms, each past THE SHARE; the queue's last notice is at least 144 ms out.

**The rows by the method** (W in ms, every source / certain sources only):

| Point | Row | Bound | As built | Slices of 3 | The least over slices of 1 to 12 | Floor |
|---|---|---:|---:|---:|---:|---:|
| 1x1/1if | R4 | 20 | 74.70 / 18.59 | 43.71 / 15.60 | 34.76 / 9.82 | 9.70 |
| 1x1/1if | R5 | 20 | 37.54 / 12.90 | 44.08 / 13.13 | 44.08 / 13.13 | |
| 1x1/1if | R6 | 20 | 29.19 / 12.76 | 40.87 / 12.98 | 40.87 / 12.98 | 14.50 |
| 8x8/2if | R4 | 22 | 657.58 / 51.36 | 149.66 / 39.04 | 118.72 / 13.95 | **22.72** |
| 8x8/2if | R5 | 22 | 163.88 / 34.09 | 131.79 / 34.61 | 131.79 / 34.61 | |
| 8x8/2if | R6 | 20 | 148.81 / 33.56 | 117.51 / 34.09 | 117.51 / 34.09 | **29.66** |
| 32x32/2if | R4 | 20 | none under 2,000 / 1,398 | none / 306 | none / 209 | **41.59** |
| 32x32/2if | R5 | 20 | none / 217 | 666 / 208 | 666 / 208 | |
| 32x32/2if | R6 | 20 | none / 215 | 626 / 206 | 626 / 206 | **63.04** |

**The bounds that hold at this head:**
- the first queued notice: 22 ms at 8x8/2if and 16 ms at 1x1/1if (THE RETRY's search, round 21's);
- the last queued notice at 1x1/1if: 22 ms within its 25 ms ceiling, at THE DRAIN's derived pass count as at the committed one;
- every pass's polls base, and each heavy item of the polls, within its stated cost (`poll_grade.py`), every round within its stated cost (`round_grade.py`), and every pass given whole to a build or an aged step within its own (`whole_grade.py`), each a gate over every group at both points;
- by measurement only, which holds no row: every row within its bound at both points but the egress-held rows.

**What does not:** R4, R5 and R6 at either measured point by every source, the last queued notice at 8x8/2if (74 ms against 70) at THE DRAIN's derived pass count, and every row at the 32x32/2if model point. What dominates them: THE RETRY's rounds beside records (11.34 ms of 22 at 8x8/2if, three yielding, then firm ones) with THE TRANSMIT's builds (4.86 ms) and the row's own burst, which put R4's and R6's floors over their bounds before any poll or other record; SRP's burst and the other channels' records between slices; and in these short windows each heavy item's source posting about once a pass.

### Round 18

The ruling (#665 issuecomment-6681686082, amended by issuecomment-6682851386) answers round 17's STOP: at most 16 registered controllers per AVB Interface (Milan v1.2 5.3.4.2), each registration notified on its own port (5.4.5.1), so 16 recipients at 1x1/1if and at most 32 at 8x8/2if; FR_NFR.md 3.4.1's notice bound amended for queued notices, ceilings 60 ms at 8x8/2if and 20 ms at 1x1/1if; SRP and MRP relaxed to T_svc. THE SHARE is not amended.

| Ruling item | At this head |
|---|---|
| 1. 16 controllers | `AECP_REGISTRATIONS` (16) sizes every registry and fan-out. |
| 2. Queued notices by construction | Rounds spend what their pass has left at stated costs, each refused attempt charged and one attempt a port, so a round cannot run free on refusals; a search of `ctrl_loop_service`'s choices (`ctrl_retry_search.py`, a gate) derives the bound, since the hand total was 18 ms short. **With the round costs measured at this head the search gives 22 ms at 1x1/1if and 62 ms at 8x8/2if, each over its ceiling**: a notice costs about 240 us to 16 recipients and 345 us to 32, against 220 and 320 stated. Measured, the last queued notice is at most 12.53 ms at 1x1/1if and 31.64 ms at 8x8/2if. |
| 3. SRP and MRP at 20 ms | By construction: THE DRAIN takes SRP's records first, its last composed record within `CTRL_LOOP_SRP_MS` 18 ms; an MRPDU a timer owes has a pass given whole of its own, within `CTRL_LOOP_TX_MS` 20 ms at 8x8/2if and 16 ms at 1x1/1if; THE TRANSMIT's 44/176 ms hold is gone; both held at compile time. A new row times the timer-driven MRPDU: at most 3.55 ms at 8x8/2if and 1.14 ms at 1x1/1if. A link change composed with the burst is outside the drain's count. |
| 4. Re-measure | Partial: the finished legs are in the handoff. One held AECP record at 20.752 ms (8x8/2if, `notice-burst-6`), over T_svc. The 8x8/2if `backlog` window's first pass 195,052 cycles with both drafts, inside the share but not its 6,490-cycle margin. |
| 5. Restate | Held back: `ctrl_loop.h`, `aecp.h` and sections 13 and 14 would restate bounds this head does not hold. RESIDUE-1's reflow is carried with them. |

Found and fixed on the way, each by a check this round added or a test that could not fail before: a round's refused attempts ran free in its budget; a notice beside a refused sibling waited a whole retry spacing; one flash page a save at 1x1/1if cost 28,000 cycles more, its lines aliasing the stack frames of the per-byte transfer in the D-cache (now programmed from a copy on the stack); after a link change a pass's spare records and SRP's rebuild of the interface passed the share (238,693 cycles; records now stop at their cap while a rebuild is owed); THE DRAIN's limit test could never reach its limit; and four plants that did not compile or planted a line another check still held.

### Round 17

The ruling on round 16's reviews, R711-5 (issuecomment-6674103087) and R712-5 (issuecomment-6674722422), both NEGATIVE, is #665 issuecomment-6674728988. It keeps every bound and the share and asks for items 1 to 3 by construction, or a STOP with the residual and the smallest lever if they cannot all hold. They cannot, so this round adds no commit. Every figure below is read from the head's constants and this head's measured cycles. The notice legs' images are the head's byte for byte. A probe ran in a disposable copy of the head, on the real `aecp.c`, `aecp_mbx.c` and `ctrl_loop.c` on the host mailbox model, with one event before every pass and every pass charged 2 ms.

| Ruling item | At this head | The least any construction reaches, and the lever |
|---|---|---|
| 3. Every retried notice answered together within 20 ms; the most a datapath reset can make pending | **40 notices at 8x8/2if, 12 at 1x1/1if.** Each descriptor holds one pending notice per bit its type supports. A held or resetting face fails every observation port, so one scan fails them all and they share one backoff. A reset that moves the counters makes the 20 counter notices pending at once by itself. The probe: the last of the 40 is committed **132 ms** after the answer, 38 of 40 over; at 1x1 the last of the 12 at 48 ms, 10 of 12 over. One round builds one notice | **8x8/2if: 50 ms, under any construction inside the share.** A notice's fan-out to its 32 recipients is at least 48,916 cycles and a round up to 12,571, so a pass carries at most two notices. The 40 need 20 passes after their retry comes due: 8 + 2 x 21 = 50 ms; the 20 counter notices alone, 30 ms. Their fan-outs alone are 19.6 ms of CPU, against the 12 ms the spacing leaves. No firmware cycle cut, record cap or burst split is enough. The lever is either (a) a decision on how FR_NFR.md 3.4.1's notification bound applies to notices queued behind one another, or (b) a fabric-side fan-out: one TX record sent to every registered controller, about 14,100 cycles a notice, the 40 in four passes, 18 ms. (b) is a contract and RTL change. **1x1/1if: 16 ms** with a round that builds and sends up to five notices a pass; not built |
| 1. The composed burst's last SRP record within 18 ms, by the constants | 34 ms or more. The 32 records take 16 passes at two a pass, plus the running one. Not counted in that: passes that dispatch a centisecond, passes given whole, and passes in which an event posted during the pass holds SRP's receive back (`rx_order_ready`), which the contract's unrated event sources do not bound | **18 ms at 9 of 9 passes, no slack, together with item 2's lever.** (i) An SRP drain: a record waiting past one pass takes the next pass ahead of the other channels', up to 10 SRP records a pass at 12,293 cycles a record. (ii) The build lever below. (iii) SRP's readiness ordered by ring position against the events its pass took. No other channel's record is taken for six passes, and no retried notice's round or fan-out fits in the window; not built |
| 2. A timer-driven MRPDU within 18 ms of its armed deadline, every participant | `CTRL_LOOP_TX_MS` 44 ms from the hold, and 176 ms for every participant at two interfaces | **10 ms alone, 18 ms with item 1.** A timer-made build is aged at its centisecond's dispatch, and an interface's MSRP and MVRP builds share one pass given whole: 172,568 cycles at this head's heaviest builds and round. Both interfaces then take 5 passes; not built |
| 4. Re-measure | Not run: no change | [A683u]'s legs are this head's |
| 5. Restate, and R712-5 RESIDUE-1 | Held back: the restatement depends on the decision, and a wording-only commit restarts every gate | RESIDUE-1 is carried to the next round |

Found on the way, for a later Issue: SRP takes no record in a pass during which an event is posted, and the contract coalesces event sources but rates none. So input that posts an event during every pass holds SRP's receive off without bound. Every staging posts its flood as a pass starts, so no group meets it. It is lever (iii) above.

### Round 16

The ruling on round 15's STOP (#665 issuecomment-6634982529) put the composed burst in the SRP row's scope and asked for the layout's cycles back: a pass that fits by less than the 6,490 cycles data layout alone moved it fits by chance. Its four items, at `d930ea98f75be96f1062217d62bccd24dd291265`:

| Ruling item | Change | Evidence |
|---|---|---|
| 1. The SRP lever, by pass class, its bound from the constants, stated in ms beside `CTRL_LOOP_STEP_AGE` and `CTRL_LOOP_RETRY_MS` | THE TRANSMIT (`ctrl_loop.h`, `ctrl_loop.c`, `srp_mbx.c`). The attribution of round 15's residual: the 32 SRP records of the burst's first instant are taken by sixteen passes, and five of them carried an MRPDU build a centisecond's join timers started, about 2.4 to 2.9 ms, which put the last past 18 ms; the heaviest pass was one of them. So the loop marks a pass that took no record, at most one event and no centisecond (`tx_pass`, before its polls) and calls SRP's build after the polls, before THE RETRY and THE STEP. SRP's poll builds and declares nothing, and reports a held build owed. Once a build is held more than `CTRL_LOOP_TX_AGE` (two) centiseconds, counted on SRP's own tick, the next pass after one not given whole is the build's alone, before any input, with THE RETRY's round after it. A frame a build left owed stays the poll's (A3). THE TICK's cap (`CTRL_LOOP_RX_PER_TICK_PASS`): with THE TRANSMIT alone the heaviest pass was the one that dispatches the 10 ms centisecond beside the burst's first records, 195,756 cycles, so such a pass takes one record of a channel. Stated beside the constants: `CTRL_LOOP_TX_MS`, (2 + 1) x 10 + 7 x 2 = 44 ms from a hold to its build under any input, so every participant's MRPDU is sent within 2 x `MBX_N_IF` x 44 = 176 ms, inside the 200 ms JoinTime (IEEE 802.1Q Table 10-7); and `CTRL_LOOP_SRP_MS`, 18 ms, THE SHARE's nine passes, with what THE TRANSMIT gives SRP's records by pass class: at most one aged build among any record's wait, since two stand 20 ms apart; `srp_mbx.c` holds both at compile time | 8x8/2if, the composed burst's last SRP record: 16.48 to 17.11 ms (19.05 to 19.67 at `d0eef1cb`), with both drafts 15.98 to 16.46; the last AECP record 15.76 to 16.43 ms (19.66). 1x1/1if: 10.74 to 10.88 and 10.23 to 10.42 ms. Every other channel within its own bound. `--mutation transmit-beside-records` (THE TRANSMIT's pass every pass): `CONTROL transmit-beside-records caught`, every group 19.59 to 20.11 ms. `LoopBring.L18TransmitBindingRefusals`, `Loop.L19TheTransmitOnlyInAPassThatTakesNoRecord`, `Loop.L20AnAgedTransmitIsAPassOfItsOwn`, `Loop.L21APassThatDispatchesACentisecondTakesOneRecordOfAChannel`, `Srp.TransmitWaitsForAPassThatTakesNoRecord`, `Srp.AHeldBuildTakesAPassOfItsOwnPastItsAge`, `Srp.AnOwedFrameComesBeforeTheBuild`, with 46 new plants (24 and 3 in the loop, 19 in SRP's adapter) and `rx-pass-unbounded` re-planted, each failing its named test on its words; two grader mutants for the new control |
| 2. The share by construction: every pass class's worst case in cycles, each at least 6,490 under the share, at both points, at the head's layout and the struct-ends layout | `ctrl_loop.h`, THE SHARE: seven classes, each with its heaviest measured pass at 8x8/2if and 1x1/1if; the one no group stages, a pass given whole to an aged build, by composition | Least 9,580 cycles under, a pass that takes a record at 8x8/2if (190,420 cycles); with the new fields at their structs' ends, 10,844 (189,156). Every other class at least 28,649 under. No further record cap was needed |
| 3. Every row, pass and save window again, both points, both arms, with and without the drafts, as round 15 item 1 staged them, plus the notice groups | Twelve legs and the struct-ends and 8x8/1if legs, on clean clones of `12e5ec56`, whose firmware the head's is (the head's images are the legs' byte for byte, 9 of 9) | 0 refusals; 0 of 1,489,645 work passes over the share, the longest 1.904 ms; every row the CPU decides within its bound, the three egress-held rows over as before. Least margin 0.235 ms, 8x8 arm A, a save's verify window opened one short of the age limit, last SRP record 17.765 ms (0.020 at `d0eef1cb`, 0.101 at `65251a2f`). Every save durable within its stated worst case: `save-starved` 12,087.0 of 12,110 ms and `save-second` 22,110.1 of 22,150 at 8x8/2if; 4,048.1 of 4,070 and 6,029.8 of 6,070 at 1x1/1if. The controls `retry-ageless` (8 of 8 notices late at both points) and `store-step-aged-heavier` (8 of 8 windows over) are caught |
| 4. Restate `ctrl_loop.h`, `aecp.h` and sections 13 and 14 | `ctrl_loop.h` (the heaviest pass, the least margin, a build-carrying pass, every class, SRP's bound); `aecp.h` (the retried notice measured from its port's answer: 12.30 to 13.20 ms at 1x1/1if, 12.47 to 13.51 at 8x8/2if); section 13's new subsection with every table; section 14's estimate, its misses, the idle pass and the gPTP paragraph | `SPLIT_CONTROL_MEMORY.md` sections 13 and 14 |

Also fixed on the way: the harness control as first committed did not build under `-Werror` (its plant left two locals unused), found when it first ran; and SRP's README named a binding among what holds a build, where its test asserts a binding holds none.

### Round 15

Both round 14 reviews were NEGATIVE: R711-4 (MAJOR F1, F2) and R712-4 (MINOR F1, F2). The age limit itself was confirmed at its cause. What did not hold was what the round stated about it: that no aged step lands among a window's records, with the least margin 0.77 ms, and that 12,110 ms is a change's worst case at 8x8/2if. The test of the limit also could not tell centiseconds from dispatches.

Round 15 staged the windows opened at the step's worst age and stopped at `bc4685ec` (#665 issuecomment-6620336528): one 8x8 pass, 2.021 ms, held an AECP change-notice retry beside the burst's records and a centisecond. The ruling (issuecomment-6620376502) made the retry the product's, kept the share, and asked for the retry to be kept out of the burst's pass by construction. The first continuation did that at `65251a2f` (issuecomment-6630201662). The ruling on it (issuecomment-6630265194) found that a retry held for a pass that takes nothing could wait up to 30 ms under input that leaves no pass empty, past its notice's 20 ms, and asked for the bound back by construction. The second continuation, at the head above, does that, and stops on what its new row found.

#### Round 15 continued (2): THE RETRY's age limit, and the STOP

| Ruling item | Change | Evidence |
|---|---|---|
| 1. The bound by construction, by pass class, stated in ms beside `CTRL_LOOP_STEP_AGE`; `aecp.h` corrected | THE RETRY's age limit (`ctrl_loop.h`). Once AECP reports a held retry `CTRL_LOOP_RETRY_AGE_MS` (4 ms) past its time, read on AECP's own millisecond clock from the earliest held retry (`aecp_retry_aged`, `aecp.retry_since`), the next pass is the round's alone. It calls the round before it takes any input and returns one, as an aged step's pass does. An aged step's pass, read first, takes the round after the step instead. The age is not reported while anything waits ahead of the round (a response or notice owed, a command waiting on its apply, a START/STOP pending). The retry stays out of every pass that takes input or dispatches a centisecond. The bound beside `CTRL_LOOP_STEP_AGE`, `CTRL_LOOP_RETRY_MS`: the age, then the pass running when it is reached, the pass that takes the round, and the pass that sends what it built, each within THE SHARE, 4 + 3 x 2 = 10 ms. With AECP's 8 ms spacing, a retried notice is built and committed within 18 ms of its port's answer, inside `AECP_NOTICE_MS` (20 ms), and `aecp_mbx.c` asserts that sum at compile time. No two passes given whole to aged work run back to back, and THE BOUND names their cost to a waiting input | `ctrl_loop.h`, `ctrl_loop.c`, `aecp.h`, `aecp.c`, `aecp_mbx.c`; the two new per-pass functions in the hot list after `ctrl_loop_service` (`ctrl_hot.py --check`) |
| 2. A harness row, graded from the port's answer against 20 ms; a grader mutant and a firmware mutant, each caught by name | `notice_window.py`, in the labelled `answering-later` arm. The face block's stream observation stays unanswered until an attempt at or after NOW_MS 3,150 fails. That attempt marks the answer (an `ENTRY`), so the next retry is a whole 8 ms backoff away. The notice is a BIND_RX's GET_STREAM_INFO, fanned out to 16 registrations an interface, under `save-starved`'s input (every receive channel at its refill rate with its bursts, a grandmaster change as every pass starts) with a save in flight, at eight phases. A late notice fails the run whatever its options record. Each channel's longest record under that load is a row too | 1x1: 12.364 to 12.450 ms, 16 recipients; 8x8: 12.519 to 13.010 ms, 32 recipients; every group within 20 ms. `--mutation retry-ageless` (the age removed): `CONTROL retry-ageless caught`, 8 of 8 groups late, 30.619 to 30.872 ms at 8x8; at 1x1, 8 of 8, 30.307 to 30.392 ms. The same groups on `65251a2f`'s firmware: 30.68 to 30.72 ms. Grader mutants "notice: a retried notice later than its bound is a budget finding only" and "notice: a retried notice is held to its ceiling, not its bound" each fail "a retried notice later than its bound fails the run whatever the options record, and one within it passes"; 149 grader mutants caught, 0 failures. Firmware plants: 8 new in the loop and 8 new in AECP, 4 re-anchored, each failing its named test on its words (`Loop.L17AnAgedRetryIsAPassOfItsOwn`, `Core.HeldRetryAgesFromItsEarliestTimeWhenTheRoundCouldTakeIt`, `Mailbox.AgedRetryTakesAPassOfItsOwn`) |
| 3. Every row, pass and save window again | Started at the code head `49f268ed`; stopped at the residual below | Begun at the code head `49f268ed`, and stopped at the residual below. As far as it ran, at 8x8: the four backlog windows and every aged window at the limit in arm A, arm B's 16 verify aged windows, and 59, 51 and 52 groups of N-A8's, N-B8's and D-A8's own runs. Every one has 0 refusals and 0 passes over the share, and only the three egress-held rows are over their bounds. The least margin is 0.020 ms, arm A's `verify-aged2-6` (last SRP record 17.980 ms), whose records hold one aged retry pass (9,973 cycles) beside its aged step's. Arm B's thinnest set (0.101 ms at `65251a2f`) is now 0.445 ms at the limit. `backlog-adp`'s heaviest pass fell to 189,736 cycles (199,112). `save-starved` is durable 12,086.7 ms after its change (12,110) |
| 4. Restate `ctrl_loop.h`, `aecp.h` and sections 13 and 14 from this head's figures | `aecp.h` restated with the bound by construction. The figure restatement of `ctrl_loop.h` and sections 13 and 14 is held back: it depends on the decision below | |

**Why STOP.** The exit is a pass over the share, or a row that does not fit. The new row's groups are the first to stage a composed burst under input that leaves no pass empty. At the load's first instant, every channel's bucket burst comes at once while the grandmaster flood runs. At 8x8/2if both exits occur there:

- **A row that does not fit.** Every group's longest held SRP record is 19.047 to 19.666 ms against its 18 ms. It is the last of the load's first SRP burst. Its 21 passes hold the composed burst's ACMP, AECP and SRP records, and two aged retry rounds of about 13,000 cycles each (about 0.26 ms). The same groups on `65251a2f`'s firmware, which has no age limit, give 18.975 to 19.421 ms. With one registration an interface they give 18.175 to 18.823 ms, and with AECP's first burst one refill period late, as `save-starved` stages it, 18.624 to 19.339 ms. So the overrun predates the age limit: this staging is new, and no earlier group combined a composed burst with the flood. With both drafts staged it is 18.030 to 18.626 ms.
- **A pass over the share.** `notice-retried-4` has one pass of 201,540 CPU cycles (2.015 ms), the burst's third, which takes ADP, ACMP, AECP, MAAP and SRP records and holds no round. With the age removed (`retry-ageless`, otherwise this head's image) it is 202,048 cycles. On `65251a2f`'s firmware it is 195,897. Each of these groups' heavy burst passes is about 5,000 cycles heavier at this head than on `65251a2f`'s firmware, with the same records and fewer fetch refills (470 against 480). The extra cycles fall mainly in `ctrl_app_srp` and `ctrl_app_aecp`, which this change does not touch. That points to the image's layout (the two new hot-list functions, and the fields added to `struct ctrl_loop` and `struct aecp`), not to the round's work. Not tested further here.

**For the manager:**
- Whether a composed burst under input that leaves no pass empty is in the SRP row's scope. If it is, the 8x8 last SRP record needs a lever outside THE RETRY, since it misses on `65251a2f` too.
- Whether the layout's 5,000 cycles are to be recovered here (the ruling allows a re-trace of the hot list when item 1 takes a margin below zero), or the share's margin is accepted as it stands in the staged windows.

**Round 15 item 1's staging at this head, as far as it ran** (8x8/2if; least margin to the bound, ms; passes over the 2.0 ms share):

| Groups | Arm | Least margin, row | Passes over the share |
|---|---|---:|---|
| The four backlog windows, the 24 aged windows at the limit | A | 0.020, `verify-aged2-6` (17.980) | 0 of 28,829 |
| The 16 verify aged windows | B | 0.308, `verify-aged1-3` (17.692); at the limit 0.445 | 0 of 13,411 |
| 59 groups of N-A8's own run | A | 0.165, `program-aged1-3` (17.835) | 0 of 115,278 |
| 51 groups of N-B8's own run | B | 0.705, `blank-aged1-6` (17.295) | 0 of 88,840 |
| 52 groups of D-A8's own run | A, both drafts | 1.620, `verify-aged2-5` (16.380) | 0 of 110,260 |

The three egress-held rows miss as before. N-A1 (9 groups) fits with 6.4 ms or more. Not run: D-B8, N-B1, D-A1, D-B1, AH-A8, P81-A8.

#### Round 15 continued (1), at `65251a2f`

| Item | Change | Evidence |
|---|---|---|
| Ruling 1. The retry kept out of the burst's pass, with its bound | THE RETRY (`ctrl_loop.h`): the loop calls AECP's round (`aecp_retry`) only in a pass that took no input and dispatched no centisecond, after its polls and before THE STEP, whose deadline counts the round's time, or after the step in the pass given whole to an aged step. The loop decides from what the pass took and dispatched; there is no cycle estimate. AECP's poll and its timer's sink hold a due retry, arm no timer for it and report it owed (`aecp.retry_hold`) | No pass over the share in any leg at `65251a2f`. The residual window's heaviest pass was 197,193 cycles (1.972 ms), with no round in it (202,116 before) |
| Ruling 2. A test and a named mutant | `Loop.L16TheRetryOnlyInAPassThatTakesNothing`, `LoopBring.L15RetryBindingRefusals`, `Mailbox.RetryWaitsForAPassThatTakesNothing`, `Core.HeldRetryWaitsForTheRoundAndTheRoundForAnOwedResponse` | 25 plants, 11 in the loop and 14 in AECP, each failing its named test on its words |
| Ruling 3. Every row, pass and save window again | Ten legs at the code head `5e2651d5` | 0 refusals, 0 of 1,281,000 work passes over the share, every row within its bound (the three egress-held rows miss as before). Least margin 0.101 ms (8x8, arm B, `verify-aged2-2`, last SRP record 17.899 ms) |
| Ruling 4. The held-back restatement from that head's figures | `ctrl_loop.h`'s reason for N and section 13's and 14's figures at `65251a2f` | `SPLIT_CONTROL_MEMORY.md` sections 13 and 14 |
| Round 15's items 2 to 4 | Stand as met: a change while a save is in flight, 22,150 ms at 8x8/2if and 6,070 ms at 1x1; `Loop.L14TheAgeCountsCentisecondsNotDispatches`; the residues | `nvm_store.h`, `test_port_loop.cpp`, the store's README |

That continuation's open question, a retried notice's timing behind a backlog or under input that leaves no pass empty, is what the second continuation answers above. Its other findings stand: the scan placed in the hot list, `aged=` on an aged step's `PASS` line, the coverage of the round's guard, and THE RETRY's AECP plants in a table of their own.

### Round 14

Both round 13 reviews were NEGATIVE on one MAJOR (R711-3-F1 = R712-3-F1): since THE STEP, a save advanced only through passes that took no input, and nothing bounded how long input could keep them from coming. The manager's decision: bound it by a mechanism, state the worst case, and test it under the contract's load.

| Item | Change | Evidence |
|---|---|---|
| 1. The mechanism | THE STEP's age limit (`ctrl_loop.h`): once more than `CTRL_LOOP_STEP_AGE` centiseconds, two, have been dispatched since the step last ran or owed nothing, the next pass is the step's alone, before any input, with the deadline read as it starts; it returns one, so the input it held off is taken by the next pass, one step later | `Loop.L13AnAgedStepIsAPassOfItsOwn` and ten planted defects. N measured: in every window the harness stages, at both points, in both arms, with and without the drafts, at most two centiseconds were posted between two passes that carried a step (one at 1x1), so no aged step lands among the records of a window opened from idle (restated in round 15: one opened at the age limit takes one, and the least margin is 0.148 ms) |
| 2. The bound | A save is durable at most 1,000 ms (DR2a) + S × 3 ticks + 10 ms after its change with no save in flight (restated in round 15: a change marked while a save is in flight, 22,150 ms at 8x8/2if, 6,070 ms at 1x1); S is its steps after the first-dirty window. A SET_NAME of the entity marks both its names: at 8x8/2if S = 370 and the worst case is 12,110 ms, at 1x1 S = 102 and 4,070 ms, with no flash busy time (`nvm_store.h`, `save_window.bound_ms`). `save-held` holds every receive channel at its contract refill rate with its bursts through a whole save; `save-starved` adds a grandmaster change as every pass starts, so no pass takes nothing | 8x8/2if, arm A / arm B, without and with the drafts: `save-starved` durable 12,087.0 / 12,087.0 and 12,087.1 / 12,088.0 ms after its change, within 12,110; `save-held` 4,696.9 / 4,696.7 and 4,697.0 / 4,731.1 ms; 0 passes over the share in either group; each channel's longest record within its bound, SRP at most 14.81 ms against 18. 1x1: `save-starved` 4,049.0 / 4,048.1 and 4,047.9 / 4,048.0 ms within 4,070. The plant with the age limit removed: `CONTROL store-step-ageless caught`, the save not durable 12,618.4 ms after its change |
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


## Known limitations, round 25, as its body listed them (at `3a1d14c2`)

- **Round 25's decisions, for the owner** ([Round 25](#round-25), above):
  1. **8x8/2if is 0.047 over 0.70** after items 1 to 3, graded with tsn-c-stack#32. Each of its three largest terms alone would need: an SRP record 405 to 326 us, or SRP's refill 2 to 2.61 ms; a record's owed AECP frame 340 to 103 us, or AECP's refill 5 to 16.5 ms; an ACMP record 305 to 68 us, or ACMP's refill 5 to 22.4 ms. Or more compute: 1.07x.
  2. **32x32/2if** is reported, not gated: 1.659 with tsn-c-stack#32, 2.37x the compute it would need for 0.70. Decided since (option D, issuecomment-6759183115 and issuecomment-6759193032): per-shape contract rates for the flip, owed to #859, and the compute in #872.
  3. **The pin move** that carries tsn-c-stack#28, tsn-c-stack#31 and tsn-c-stack#32 owes the 8x8/2if `answering-every-port` arm 132 bytes of `rom`: with tsn-c-stack#32 the arm's image is 123,012 bytes, past its 122,880-byte granule. The graded column's costs that only that arm stages, a notice's among them, are the pin's.
- **`AECP_NOTICES_MOST`** caps the notices a datapath reset can leave pending at 40 at two interfaces whatever the shape, against 136 in the 32x32/2if model; the queued-notice bounds and their search are stated for 40. Drafted for #866; unchanged here.
- **A refused SRP record's give-up** past 1 s with a change pending waits at most the centisecond for the retry the change allows (`sw/firmware/ctrl/srp/README.md`).
- **No group stages** a retained record's retry, an owed MRPDU or a registration's probe: each is stated at the cost of the measured work that holds it (an SRP record, a build of one, a response).
- **The three egress-held rows** stay with tsn-c-stack#26.
- **The drafts** (lwSRP, tsn-c-stack) are measured staged and are not pinned here.
- **The platform image's hot list:** four entries name the size fixture's callbacks and place nothing in that image.
- **No fabric option outlives the switch-over:** nothing here adds one. The hybrid-XIP arm still misses T_svc on every path, so D3's rule stands.
- The earlier rounds' decisions for the owner and the manager are in `evidence/ROUND-HISTORIES.md`.

## Known limitations, rounds 17 to 24, as round 24 listed them


- **Round 24's decisions, for the maintainer** ([Round 24](#round-24)): the load is over 0.70 at 8x8/2if and 32x32/2if after items 3 to 5, and the ruling's exit names the choice, more compute or contract rates per shape. Its largest terms and what each would need:
  1. **SRP's retained retry** (0.560 at 8x8/2if, 0.585 at 32x32/2if): `srp_mbx.c` retries a refused record once a poll for up to 1 s and takes no other SRP record meanwhile, and the loop never sleeps, so the retries take up to 0.59 of the CPU. A retry rule bounded by a source (an attempt only once the pool or lwSRP's attributes changed, or one a centisecond) changes when a refused record is retried, which item 4 excludes. Without the retry the loads are 0.449, 0.819 and 2.054.
  2. **AECP's owed frame** (0.112 at 8x8/2if) is charged at a notice's fan-out to 32 recipients, for every response and every registration's probe retry: a stated cost by what each source sends, or a cheaper fan-out.
  3. **The ACMP core's walk of every sink after every entry** (`finish()`, the TSN stack) in ACMP's record, its owed frame, its timer slot's expiries and the ADP record: 0.184 at 8x8/2if and 0.637 at 32x32/2if. A walk over the sinks that changed is a TSN stack change, through its review and a pin move.
  4. **At 32x32/2if THE TRANSMIT's builds** (a build of both of an interface's MRPDUs 10.81 ms, five shares) and the owed MRPDUs stated at a build of one's cost (7.49 ms): 0.449.
- **No cut is committed for item 4**: each growing cost's cause is placed (`SPLIT_CONTROL_MEMORY.md` section 14), and the load stays over 0.70 at 8x8/2if whatever this branch's code can cut with its behaviour unchanged.
- **32x32/2if's queue**: `AECP_NOTICES_MOST` is 40 at two interfaces whatever the shape, the 32x32/2if model holds 136 notices, and the queued-notice bounds are stated for 40.
- **The 8x8/2if `answering-every-port` arm** has 12 bytes of `rom` under its ledger's granule.
- **Round 23's decision 4 is taken**: `dev-soft-core` `1d6bf555` is merged.
- **Round 23's decisions, for the maintainer** ([Round 23](#round-23)):
  1. **32x32/2if against the contract's rates.** The contract's per-channel rates do not scale with the shape, and the costs section 14's L projects at 64 streams do: an ACMP timer expiry 923 us, an SRP record 892 us, each pass's polls' base 709 us. Every source's load is then 2.51 of the CPU, so no loop structure bounds the bulk rows, and tier 1's own events and records are over 20 ms in R4's window. The tiers move that load between rows; they do not remove it. What is left: costs that do not grow with streams, measured on a 32x32 image, or rates and bounds per shape.
  2. **The order within tier 1 at 8x8/2if.** R4 fits only with AECP ahead of every other tier-1 channel, and ACMP's held record is then over T_svc (22.99 ms).
  3. **The method's per-pass terms that dominate:** one event a timer slot an ordinary pass up to its fires, a retained SRP record's retry once an SRP record, one grandmaster event an interface a pass.
  4. **Whether the lane merges `dev-soft-core` `1d6bf555`** (PR #853 and PR #861), which the head does not contain.
- **Round 22's decisions, for the maintainer** ([Rounds 19 to 22](#rounds-19-to-22)):
  1. **THE RETRY's rounds beside records**, firm ones of 1,625 us every 2 ms at 8x8/2if once a queue has yielded three times, take 11.34 ms of a 22 ms window with the three yielding rounds. With THE TRANSMIT's builds (4.86 ms) beside the row's own burst, R4's and R6's floors (22.72 and 29.66 ms) are over their bounds with no poll and no other channel's record counted. No polls split or slice reaches that term; "rounds give way" is ruled out, so the firm pace and the firm round's size are what is left, or the bounds.
  2. **THE DRAIN's time limit against SRP's stated 395 us record**: a pass takes at least 2 of SRP's records, so a slice above 2 is never guaranteed and the queue's last notice, at THE DRAIN's derived pass count, is 74 ms against 70 at 8x8/2if. The committed search keeps round 21's 4, from `CTRL_LOOP_SRP_RECORD_US` = 123 us.
  3. **THE DRAIN's slices** move the other channels' records ahead of SRP's last: measured in slices of 3 at 8x8/2if, SRP's held record goes from 8.405 to 24.475 ms and 10 passes go over THE SHARE. Not committed.
  4. **32x32/2if**: a pass given whole to a build of both of an interface's MRPDUs, and to a build of one, project past THE SHARE (5.75 and 3.99 ms), the composed burst's records alone to about 58 ms, and the queue's 136 notices to at least 144 ms: the structure that fits 8x8 does not reach 32x32.
- **No firmware changes in round 22.** Each heavy item of the polls already runs as its own function; a loop that dispatched them does not fit the ledgered 8x8/2if image, whose `answering-every-port` arm has 4 bytes of `rom` before the next 2 KiB granule.
- **Two heavy items have no measured line** (a retained record's retry, an owed MRPDU): no group stages them, and each is stated at the cost of the measured work that holds it.
- **No arrival bound is committed**, so no arrival gate or plant is: none of the rows they would hold fits. Each item's arrival bound, with its clause, is the model's and section 13's.
- **A test gap:** no test or mutant holds THE DRAIN's rule that a pass that took more than `CTRL_LOOP_RX_PER_PASS` of its records takes no other channel's; the slices' prototype, which removes it, passes the whole firmware suite.

- **Round 18's decisions, for the owner** ([Round 18](#round-18)): the queued-notice bound by construction is 22 ms at 1x1/1if and 62 ms at 8x8/2if with the measured round costs. Closing 1x1/1if needs a round of eight notices in a pass given whole, so a notice about 6 us cheaper at 16 recipients, a different round structure at one interface, or a 22 ms ceiling; closing 8x8/2if needs the like at 32 recipients, or a 62 ms ceiling.
- **The stated notice costs understate the measured ones** (220 and 320 us a notice against about 240 and 345), so THE SHARE holds for a full round by measurement, not by construction.
- **One held AECP record over T_svc** at 8x8/2if under the composed burst with every notice pending (20.752 ms in one phase of eight): that row fits by phase.
- **The `records` pass class** has a pass inside the share's 6,490-cycle margin at 8x8/2if with both drafts (195,052 cycles in the `backlog` window's first pass).
- **A link change composed with SRP's burst** costs THE DRAIN up to one capped pass an interface that `CTRL_LOOP_SRP_MS` does not count.
- **An assumption of the first-notice bound:** a port, one window read, answers for all it serves or for none.

- **Round 17's decisions, for the manager** ([Round 17](#round-17)):
  1. Item 3 at 8x8/2if cannot hold within the 2.0 ms share. Either (a) decide how the notification bound applies to notices queued behind one another, with FR_NFR.md 3.4.1 amended, or (b) give the fabric a fan-out record.
  2. Items 1 and 2: the lever set (an SRP drain ahead of the other channels, both participants of an interface built in one aged pass at the dispatch, SRP's readiness ordered by ring position) reaches 18 ms at 9 of 9 passes with no slack, and the other channels' records wait six passes. Or choose another lever.
- **A retried notice behind other notices**: one round builds one notice, so with 40 pending at 8x8/2if the last is committed 132 ms after its port's answer at this head. `aecp.h`'s 18 ms is a single notice's, with nothing ahead of its round.
- **SRP's 18 ms for the composed burst is met by measurement, not derived from the constants** (for the manager). THE SHARE's 2.0 ms is 18 ms over nine passes, with the A3 row of seven owed frames as its deepest admitted wait. The composed burst's 32 SRP records at 8x8/2if, and the backlog windows' full SRP ring, two a pass under D4(b), take sixteen passes, which the constants bound at about 34 ms. The row fits by those passes' measured cost: 16.48 to 17.11 ms in the notice groups, 17.765 ms at worst over every window. THE TRANSMIT made those passes lighter and bounds what stands among them by pass class (at most one aged build, one aged step and the aged retries; a build only in a pass that took no record because an event posted during it held SRP's records back). A bound from the constants alone would need more than two SRP records a pass or a stated cost for an SRP drain pass. `CTRL_LOOP_SRP_MS` and section 13 say so.
- **The margins:** 0.235 ms on the 8x8 last SRP record, and 9,580 cycles on the share. A change that grows the hot code ahead of SRP's drain, or adds fields to the loop's or a module's structs, must measure them again.
- **The struct-ends layout ran a subset:** the 8x8 notice groups and arm A's backlog, save and aged windows. The classes whose heaviest falls in other groups sit 28,649 cycles or more under the share.
- **THE TICK's cap moves the other channels' last records later** (ACMP 8.90 ms against 8.54 at 8x8/2if), each within its 20 ms; at 32x32 the last ACMP record now misses under the measured line too.
- **A pass given whole to an aged build** is staged by no group; its worst case is stated by composition (one build and one round, 183,922 cycles at 8x8/2if).
- **The idle pass** carries THE TRANSMIT's and THE RETRY's calls and their ages, about 8,700 CPU cycles at 1x1/1if and 15,400 at 8x8/2if.
- **The aged windows sample, they do not sweep:** eight delays across the tick, three flash phases, two ages; with the drafts, the limit only.
- **A change's worst case is this image's, not #823's.** 12,110 ms at 8x8/2if for a SET_NAME of the entity with no save in flight, 22,150 ms beside another's save in flight, on a flash with no busy time; on the part at its datasheet maximum, 15,370 and 28,670 ms. #823's 0.5 s applies to the append-only design's writer through this same step, and this image does not meet it.
- **The step's room:** the longest step is 0.962 ms (96,212 cycles, 1x1/1if) of the 1.0 ms `NVM_STEP_US` gives it; no gate holds the figure yet.
- **The three egress-held rows** stay with tsn-c-stack #26.
- **The drafts** (lwSRP, tsn-c-stack) are measured staged and are not pinned here.
- **The platform image's hot list:** four entries name the size fixture's callbacks and place nothing in that image.
- **No fabric option outlives the switch-over:** nothing here adds one.
- The hybrid-XIP arm still misses T_svc on every path, so D3's rule stands.

