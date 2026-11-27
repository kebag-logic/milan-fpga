[A825] STOP: round 3 at milan-fpga `4935ef692356ae39f0c1ba818569a1a4961e2196`, lwSRP `73007b4807977517045e8aa485c61ebb8f5ee843` (both local, for the manager to push). At 8x8/1if the option-(a) load is 0.759 against its 0.75 (`flip_grade.py --check --point 8x8/1if` FAIL), and its registrations term alone puts it over: 0.015, at 150 us a Talker all in, against the 64 us that holds it. One more item fails: at 1x1/1if two test-port arms (answering-ports, declaring-outputs) put AECP's notice item over its stated 150 us by code placement (open item 0). Every other round-3 acceptance item holds (below). By the ruling's item 6 that goes to the owner.

Commit: `4935ef69` (`pf-977-1`). The image is `8b4a79d5`'s: every later commit is ledger, harness, test runners, twin or docs, and every harness and platform image built at `4935ef69` is byte-identical to the one measured and routed.
lwSRP: `opt-exec-3` `73007b48`, a new branch: opt-exec-1 and opt-exec-2 rebased onto `main` `d1bb4f4e` plus round 3's options; the pushed branches are not rewritten.
Integration: the train and PR #992's branch merged in, then `dev-soft-core` `2509db68` (PR #988's merge, carrying 300da99b) and #992's `507bce7f` again, once the train had merged, both sides kept each time.
Changed: PR-BODY.md and PR-BODY-lwsrp.md in the packet.

**1. Acceptance (round 3)**

| Item | Result | Evidence |
|---|---|---|
| 8x8/1if load <= 0.75 | **0.759, FAIL** | `flip_grade.py --check --point 8x8/1if`; `load_grade.py --check` |
| 0 passes over THE SHARE on every arm, the burst included | 0 in all 16 arms at both points (8x8/1if `none` 0 of 318,647, the registering groups 0 of 5,879); the base had 1 in each 8x8/1if arm that runs srp-bound | every-arm runs, 8 variants each point |
| THE TRANSMIT's build slice, every record within its slice and charge | every arm: no slice or record over (no STATED slice or record line); the registering groups' longest build slices 131,717 and 39,035 CPU cycles of 147,500 and 95,000 | same |
| no regression at 1x1/1if | **not met in two arms**: the rows equal the composed base's and the load is 0.515 (the base 0.512, the new registrations term 0.003); but in answering-ports and declaring-outputs AECP's notice item (`aecp-fanout`) is 15,283 and 15,282 CPU cycles, over its stated 150 us (15,000), where the base's are 14,212 and 14,001, so those two runs fail | `flip_grade.py --check --point 1x1/1if` at both; the two arms' runs and profiles |
| owner bounds unmoved | 0.70 / 0.75; last queued notice 127.43 ms (stated 130, the owner's bound 140); ACMP 29.15 of 30; txL 47.98 of 49 ms | same |
| kept_grade owed list empty of #977 items | empty; PASS at both points (kept 74,188 against bound 77,991 at 8x8/1if, within +5 %) | `kept_grade.py` on srp-kept and srp-bound |

**2. Why 64 us is not reached.** On the head's image a registering record costs 13,877 CPU cycles a Talker all in at 8x8/1if (150 us by the rule): 8,629 its share of the record past the unit (95 us) and 5,444 its share of THE SETTLE after it (60 us). At 1x1/1if it is 12,508 (135 us). THE SETTLE is ACMP's completion of each sink the record changed, in tsn-c-stack, outside item 5's list, so even a record that cost nothing past the unit would leave about 60 us. Round 3's exact cuts took the all-in cost from round 2's 17,598 to 13,877 cycles a Talker: lwSRP's rapid replacement, lean copies and lean tx!, the reversed descending Message, the sink index, the walk owed only for a source's StreamID. A replacement in one delivery would change the Mt vectors MRP sends, so it is not taken. Without the term the load is 0.744. The flip check reads the pin's column, which states the five costs of ACMP's completion walk at the larger of their measurements before and after tsn-c-stack #32 (a statement never goes down). At the measurements of images carrying #32 alone (load_grade's donor column) the load is 0.719. Neither is mine to change.

**3. Found and fixed on the way**
- `kept_grade` held every kept and bound record to the unit alone: the charge lookup took the last handler that started strictly before the record, which is its own handler. Fixed in `3b9cd5d9`, with a self-test check that fails on the old lookup.
- With the charge right, #969's kept <= bound (+5 %) broke at 8x8/1if: 88,194 against 82,671 at `670e2b63`, round 3 having made the bound path cheaper than the kept one. `8b4a79d5` scans the kept list and the held table only where a StreamID they hold ends in the same octet, and copies a kept or held StreamID an octet at a time (a `memcpy` call cost about 410 cycles): now 74,188 against 77,991. Its rom and `ctrl_plat` growth is ledgered by the owner's rule of 2026-11-15 (`dd26638e`: the size fixture's 8x8 one-interface image 58.5, the platform's 8x8 two-interface image 65.0, ROM debt owed to S14).
- The flip check's self-test planted THE TRANSMIT's figure "a millisecond under" at 77 ms, the figure itself since it became 77 ms, so 1 of 616 controls escaped: re-planted at 76 (`3059a8ab`).
- At one-interface shapes lwSRP makes no MAP work at one port, so no block returns with an indication: three of #969's planted count defects escaped there. The tests return a block of their own (`34b90ec8`); every one is killed at 1x1/1if, 8x8/1if and two interfaces.

**4. Round 2's questions**
- Q1: `whole_grade.redeclared` holds each 1x1/1if build pass that commits a re-declaration to its stated cost by name and refuses a registering group with none. On both arms that run the registering groups (none, answering-ports): 8 such passes in the burst and 2 in srp-register, none over.
- Q2: recovered in six of the eight 1x1/1if arms (at most 14,070 cycles, within 14,285, so 150 us by the rule); not in answering-ports and declaring-outputs (open item 0).
- Q3: the round-2 drain difference stays named with its NOTE. This round's base, the composed train, predates the registering groups, so it has no burst to compare; the differential's named differences are in section 6.
- The 130 ms wording is corrected: 130 ms is the stated last-notice figure, the owner's bound 140 ms.

**5. Validation** (receipts in the packet, `receipts/INDEX.md`)

| Gate | Head | Result |
|---|---|---|
| firmware gate, 4 shards | `4935ef69` | PASS, 4 of 4 |
| fw_coverage --check | `4935ef69` | PASS (40 files) |
| twin, its plants, maps and their plant | `4935ef69` | PASS, 0 findings, 32 plants refused |
| builder legs 0 and 1 | `4935ef69` | PASS but one arm each the test machine cannot run (a calibration report on no disk; a make that does not re-read MAKEFLAGS) |
| docs workflow | `4935ef69` | 104 steps, 0 failed |
| harness self-tests | `4935ef69` | run.py 0 failures, kept_grade 33, load 28 of 28, flip 616 of 616, shapes 25 of 25 |
| load and flip checks | `4935ef69` | load PASS; flip 1x1/1if PASS; flip 8x8/1if FAIL (0.759) |
| plat_ledger --self-test, test_ctrl_memory | `4935ef69` | PASS, 9 of 9 controls; PASS |
| routes, the split image | `dd26638e` (images identical at the head) | 1x1/1if WNS +0.301 ns, WHS +0.014 ns; 8x8/1if WNS +0.143, WHS +0.036; 0 routing errors |
| every-arm runs, both points, 8 variants | image `8b4a79d5`, regraded at `4935ef69` (every table identical) | 14 of 16 exit 0; 1x1/1if answering-ports and declaring-outputs exit 1 (open item 0); `backlog-owed`'s 7 rows past their 20 ms in none and answering-ports at both points, as at the base |
| base-vs-head differential, every arm | | equal but the named effects of section 6 |
| lwSRP: unit tests, differential (both profiles), MemorySanitizer, reversals, equivalence, embedded, guides | `73007b48` | PASS; 36 of 36 planted defects |

**6. The differential's named differences** (`receipts/arms/diff-NOTES.md`)
- `srp-register` and `srp-register-burst` run at the head alone: the base's harness predates them.
- AECP's notices interleave otherwise across descriptors in answering-every-port (7 groups at 1x1/1if, 14 at 8x8/1if), the same frames in each subject's order: round 2's named effect.
- ADP's schedule: the head's first ENTITY_AVAILABLE comes sooner (802.1 against 805.1 ms at 1x1/1if, 865.1 against 865.2 at 8x8/1if). ADP's later delays are random draws (Milan v1.2 5.6.3.5; one each event that finds it waiting), so their times differ, their frames equal one for one. In the long saved-state store groups, in `srp-kept` at 8x8/1if, and in `srp-talker-held` at 1x1/1if, the head's runs hold more advertisements. There a READ_DESCRIPTOR of the ENTITY descriptor reports `available_index` one higher (octet 81), and the saves themselves agree within 3 ms.

Acceptance criteria: met but two: the 8x8/1if load (item 6), and 1x1/1if's answering-ports and declaring-outputs arms, where AECP's notice item is over its stated cost by code placement (open item 0).
Open risks/questions:
0. AECP's notice item at 1x1/1if is 15,283 and 15,282 CPU cycles in the answering-ports and declaring-outputs arms, over its stated 150 us, so those arms fail (the round-2 answer: not to be raised at 1x1/1if). The base's are 14,212 and 14,001. The declaring-outputs profiles run 3,095 instructions against 3,074; the extra 1,281 cycles are `fan_out`'s loop at another address (0xd7f8 against 0xd670), placement on the core's fetch L1, not a new path. The split image's hot list (`ctrl_split_hot.txt`) "is learned so at the head it ships with", and round 3 changed hot SRP and lwSRP code without relearning it. Two ways out, for the owner. (a) Relearn the list by its three-window procedure at the head the owner's decision leads to, then measure every arm (any code that decision brings moves the placement again). (b) State the item by the rule, 165 us: every 1x1/1if row holds but the last queued notice, 132.95 ms, so `AECP_QUEUED_MS` would be 135, within the owner's 140. That is a firmware constant, so a new image.
1. AECP's notice item at 8x8/1if is at most 13,916 CPU cycles over every arm (declaring-outputs; 13,874 in answering-later), 150 us by the rule against its stated 145. It is within that figure (14,500 cycles) but past the rule's 5 %. The base's answering-later notice is 13,212, and that profile shows the same 3,074 instructions at both: placement again (`fan_out` +524, `sent_frame` +172). Stating 150 moves THE TRANSMIT's tx row at 8x8/1if to 77.02 ms, past its stated 77, so `CTRL_LOOP_TX_MS` would be 78 (within #665's 80 ms): a firmware constant, a new image.
2. `aecp_long` at 8x8/1if is 31,326 cycles at the head and 31,065 at the base (330 us by the rule) against the train's 325: over the rule at the base already. Stating 330 moves no row.
3. Not done in this STOP round, since each changes the image: items 0 to 2, and anything item 6's decision asks for. The next round's head needs the hot list relearned and every arm measured again whichever way it goes.
