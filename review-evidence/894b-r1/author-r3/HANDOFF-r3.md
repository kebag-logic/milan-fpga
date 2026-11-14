# 894b-a781 round 3: HANDOFF

**Status: REVIEW READY at `716a8ae7979a31315a6e085959dc4dcc8b7ee022`** (comment text `REVIEW-READY-COMMENT.md`, posted on #894 once, issuecomment-6884981996, identical to the file). Start head `184d47cacc0b4eccb923cfbd4f2df9c3a05f5638` (round 2 phase B's
REVIEW READY, unpushed). Authority: #894 issuecomment-6878014227 (the round 3 ruling), with issuecomment-6871343905
item (b)(ii) (a stated cost below its measurement is the defect) and #902's bounds issuecomment-6867990126.

## 0. Exit

- **Head `716a8ae7`**, three commits on round 2's `184d47ca`: `d8629751` (the keying, code and tests), `bae44edf`
  (docs), `716a8ae7` (the wire comparison's build of the core, the defect the first full pass found). Nothing pushed;
  no PR created or edited; no merge this round.
- **No STOP trigger:** every CPU-decided row within its bound; the load 0.711 of 0.75; the platform image 56.0; no slice
  stated over 1,600 us (1,475) and none measured over it (146,052 cycles); every 1x1 and 8x8/2if image byte-identical to
  `184d47ca`'s, at every step and at the head.
- **Item 1:** both costs keyed on the shape in THE SHAPES, 165 and 25 us at 8x8/1if from round 2's measurement by #665's
  definition, plus 5 %; checks with plants that name a point falling back. **Item 2:** byte-identity by sha256.
  **Item 3:** measured once at 8x8/1if on the new image: PASS, THE RETRY's 2,455,411 rounds within, no STATED line in
  any leg. **Item 4:** no move before the measurement (checked 15:03, 16:35, 17:3x, 20:1x); `894-tiers` moved to
  `9606b3a9` afterwards (seen 23:1x), not merged, left for a decision (REVIEW READY's first open question). **Item 5:**
  section 13, FR_NFR 3.4.1, PR-BODY.md restated; the full pass at the final head clean.
- **Open:** the core's compile-time read of `ctrl_loop.h` (the README's contract amended); `AECP_NOTICE_US` still keyed
  on the interface count (within its measurement); `Mailbox.ARoundFillsWhatItsPassHasLeft` at 8x8/1if (pre-existing,
  for a new Issue); 1x1/1if's SRP record (round 2's); the rows by every source reported.

## 1. Sync

- 14:3x CET: origin/894-tiers `7398ec0a` (already merged here at `184d47ca`), #902 OPEN at `7398ec0a`,
  origin/dev-soft-core `cec88385` (unchanged). No sync merge at the start.
- 15:03: rechecked before measuring: the same. No sync merge.

## 2. Changes, with file:line and reason

**`d86297516337b2d45d559949fd15dcb4418cb298`** (code and tests; one commit on `184d47ca`):

- **A correction of round 2's report first.** `AECP_ATTEMPT_US` (`aecp.h:60` at `184d47ca`) was never keyed on
  `MBX_N_IF`: it was one 34 us at every shape, in the AECP core. Round 2's B3 said both were keyed on the interface
  count; only `AECP_ROUND_COLD_US` (`aecp_mbx.h:29`) was. The ruling's item 1 (key both on the shape) is met for both.
- `sw/firmware/ctrl/loop/ctrl_loop.h:293-310` (THE SHAPES' comment) and `:325-347` (the table): every listed shape
  states `CTRL_LOOP_RETRY_COLD_US` and `CTRL_LOOP_RETRY_ATTEMPT_US` in its own block: (1,2,2) 85/34, **(1,9,9) 165/25**,
  (2,2,2) 185/34, (2,9,9) 185/34. Why: the ruling's item 1, the shape header `CTRL_LOOP_SHAPE` reads, one statement a
  shape, no fallback to the interface count.
- `sw/firmware/ctrl/aecp/aecp_mbx.h:27-32` (`:32` the define): `AECP_ROUND_COLD_US` is `CTRL_LOOP_RETRY_COLD_US` (was
  `(MBX_N_IF == 1u ? 85u : 185u)`). The adapter's admission (`aecp_mbx.c:206`, `retry`) is unchanged text.
- `sw/firmware/ctrl/aecp/aecp.h:57-64` (`:64` the define): `AECP_ATTEMPT_US` is `CTRL_LOOP_RETRY_ATTEMPT_US` (was `34u`).
- `sw/firmware/ctrl/aecp/aecp.c:4-6`: includes `ctrl_loop.h`, because the core's `scan` charges `AECP_ATTEMPT_US` as a
  compile-time immediate (`aecp.c:882`, `a->round_us -= AECP_ATTEMPT_US`), and the shape includes the interface count,
  which only the mailbox contract states. **This is a design decision with a documented-contract cost, published as an
  open question:** `sw/firmware/ctrl/aecp/README.md` says the core has no mailbox dependency, and `ctrl_loop.h`
  includes `mbx.h`. Nothing it declares is called (the disassembly, section 4). The alternative, the attempt cost as a
  runtime field set by the adapter (as `notice_us` is), changes every image (a load for an immediate, the struct's
  layout), which the ruling's byte-identity forbids.
- `sw/firmware/ctrl/test/aecp_arms.py:111-113`: the host core arms (no shape header) take `-I loop -I mbx` after any
  mailbox group's (whose contract is its interfaces' own), so `aecp.c` compiles there at the shipping shape.
  `:155-160` `EIGHT_ONE`: the 8x8/1if mailbox arm runs THE RETRY's attempt tests too
  (`Mailbox.ARefusedAttemptIsChargedToItsRound`, `Mailbox.ARoundWithRoomPastARefusalGoesOnToTheNextPort`) beside the
  notice tests.
- `tb/verilator/ctrl_service_budget/round_grade.py:27-36` `stated_us(given)`: the round's costs at the image's shape,
  each evaluated from `aecp_mbx.h` and `aecp.h` through THE SHAPES (`shape_costs.at`, `shape_costs.evaluated`), no
  regex on the interface ternary (derive, never mirror); `:59` `held(log, given)`.
- `tb/verilator/ctrl_service_budget/grade.py:956`: `round_grade.held(log, stated_at)`, the image's shape (was the
  interface count).
- `tb/verilator/ctrl_service_budget/shape_costs.py`: `NAMES` (+2), `RETRY` (`:51-55`), `retry_findings` (`:324`),
  `retry_controls` (`:464`), the report's two columns, three `CONTROLS` (24 now), `findings` names the point of a
  refused shape (`:289`).
- `tb/verilator/ctrl_service_budget/selftest_round.py:30-53` `header_us(given)`: an independent reader (the shape's own
  block of `ctrl_loop.h` and each AECP name's body, by its own regexes); `:96-106` the check that a round at 8x8/1if is
  held to its shape's costs, apart from the interface count's.
- `tb/verilator/ctrl_service_budget/selftest_mutants.py:810-813`: two mutants (below).
- `sw/firmware/ctrl/test/ctrl_configs.py:237,269,278`: the boundary gate's words for the three harness modules.
- `rows_grade.py`, `load_grade.py` untouched: both already read THE SHAPES' names at a shape through `shape_costs.at`,
  so `AECP_ROUND_COLD_US` resolves to the shape's own there.

**The derivation (item 1: the measurement plus 5 %).** Round 2 phase B's measurement at `6122db33` (its 8x8/1if image
identical to `184d47ca`'s): THE RETRY's rounds of the `answering-every-port` arm (256,317 rounds), the dearest at each
count k of refused attempts with notices charged at `AECP_NOTICE_US` (255 us): k=0 2,206, k=1 12,547, k=2 19,326,
k=4 23,343 CPU cycles. The rule is #665's definition of the attempt (`aecp.h`: what a round of `AECP_ROUND_PORTS`
refusals costs past its cold start, a refusal) and of the cold start (what any round implies at it): the line that
holds every round and a round of every port refused (k = 4) at its cost, and of those the one with the least cold
start, the upper hull's last edge: 15,309 + 2,008.5 k cycles (153.09 us and 20.09 us). Plus 5 %, rounded up to 5 us:
**165 us and 25 us**. Every round is within it (the closest 19,326 of 21,500). Arm A and the `answering-ports` arm had
no STATED line (rc 0), so every round there was within 85 + 255 n + 34 k us, which lies under the line for every k up
to 4 (`receipts/model/retry-line-8x8-1if-6122db33.txt`; `scripts/retry_line.py`). The 125 us the ruling quotes is the
cold start implied at the 34 us attempt; measuring the attempt too gives this line.

## 3. New checks, planted mutants and failing words

| Check | Plant | Failing words |
|---|---|---|
| `shape_costs.retry_findings` (in `--check`, `--selftest` and the harness self-test's table checks) | `a round's cold start keyed on the interface count (earlier rule)` (`aecp_mbx.h` back to `(MBX_N_IF == 1u ? 85u : 185u)`) | "aecp_mbx.h keys AECP_ROUND_COLD_US on the interface count (MBX_N_IF), not as CTRL_LOOP_RETRY_COLD_US, ..." and "8x8/1if: AECP_ROUND_COLD_US is 85 us at its shape (1, 9, 9), not the 165 us THE SHAPES state for it" |
| the same | `a refused attempt one figure at every shape (earlier rule)` (`aecp.h` back to `34u`) | "aecp.h states AECP_ATTEMPT_US as '34u', ..." and "8x8/1if: AECP_ATTEMPT_US is 34 us at its shape (1, 9, 9), not the 25 us THE SHAPES state for it" |
| the table's rules (`listed`) | `a shape's round costs falling back to the interface count` (8x8/1if's block states the cold start as the ternary) | "ctrl_loop.h states '#define CTRL_LOOP_RETRY_COLD_US (MBX_N_IF == 1u ? 85u : 185u)' for the shape (1, 9, 9) (8x8/1if)" |
| Harness self-test: "a round at 8x8/1if is held to its shape's cold start and refused attempt, ..., apart from the interface count's" | `round: 8x8/1if's round costs at the interface count's (earlier rule)` (`stated_us` at the interface count) | that check fails, first (quick run) |
| the same | `round: a round held at its point's interface count, not the image's shape (earlier rule)` (`held` given the interface count) | that check fails, first (quick run) |

Receipts: `receipts/model/retry-keying-plants.txt`; `shape_costs.py --check --selftest` 24 of 24 refused.

**Not added, a pre-existing finding:** `Mailbox.ARoundFillsWhatItsPassHasLeft` fails at the 8x8 shape at one interface
at `184d47ca` itself (clean clone) and at this change's old values: its last step expects a queue served to its end in
`AECP_NOTICES_MOST` rounds of a share each (`test_aecp.cpp:3121`, `adapter.yields` 3, not 0). It was never run there
(the arm selected only the notice tests). Left out of `EIGHT_ONE`, reported for a new Issue
(`receipts/firmware/aecp-round-tests-8x8-1if.txt`).

## 4. Byte-identity (sha256)

| Step | Tree | Result | Receipt |
|---|---|---|---|
| 1: the keying with 8x8/1if's values unchanged (85/34), `aecp.c` reading `ctrl_loop.h` | worktree | **all 8 images identical to `184d47ca`'s**, ELF and loadable | `images/img-1-keying-only.txt`, `raw-1-keying-only.txt` |
| 2: 8x8/1if at 165/25 | worktree (= `d8629751`) | the six fixed identical; both 8x8/1if moved; platform 56.0 (rom 129,200, sram 97,264, unchanged) | `images/img-2-8x8-1if-165-25.txt` |
| disassembly, step 1 against step 2 | both 8x8/1if ELFs | exactly two instructions differ in each: `scan`'s `addi -34` to `-25` and `retry`'s `addi -85` to `-165`; section headers identical | `images/disasm-8x8-1if-step1-vs-step2.txt` |

## 5. The measurement at 8x8/1if

At `d8629751` on clean clone `mC`, once, round 2 phase B's groups: C-A0..C-A3 arm A in four parts (95 groups, the same
split), C-AE the `answering-every-port` arm (16 groups), C-AL the `answering-ports` arm's `aecp-largest-notice`, and
C-CTA the transmit-aged control. Arm A's harness-built image is byte-identical to step 2's fixture-8x8-1if (ELF
`59e8767b...`); the variant arms build their own images, as before.

- **C-AL** (15:05-15:09, session CPUs): rc 0, 0 budget misses, 0 STATED lines; THE RETRY's 4,379 rounds held to 165 /
  255 / 25 us, none over. The largest legal command's rows: (gate below).
- **C-CTA** (15:09-15:26): caught, 8 of 8 groups' timer-driven MRPDU over 49 ms (66.505 to 67.015 ms), its 128 STATED
  lines all the planted MRP lateness, none a round (`receipts/harness/control-transmit-aged-8x8-1if-d8629751.txt`).
- **C-AE** (40-47, 15:11-15:56): **rc 0, 0 STATED lines: no cost over its statement.** THE RETRY's 256,351 rounds
  (with C-AL's, 260,730) held to 165 / 255 / 25 us, none over; the dearest by refused attempts the same as round 2's
  (12,547 / 19,326 / 23,343 cycles), the same line, 165 and 25 us again, the closest round 89.9 % of its statement
  (`receipts/model/retry-line-8x8-1if-d8629751-AE.txt`). The queued notices: the first at most 2.259 ms (20), the last
  at most 26.195 ms (130; round 2 23.730: a round now admits fewer notices at the 165 us cold start). 0 budget misses
  of 728 instances. Slices within 147,500 (SRP's 123,006, the build 114,754, THE RETRY's round 89,462).
- **Arm A** C-A0 (24-31, 15:09-17:35), C-A1 (session CPUs, 15:26-17:04), C-A2 (64-71, 15:29-17:12), C-A3 (8-15,
  15:34-17:12): rc 0 each, 0 STATED lines each.

**Final (every leg; `receipts/harness/gate-8x8-1if-d8629751.txt`, `scripts/gate_r3.py`): RESULT PASS.** 112 groups,
1,680 instances, all measured; every leg rc 0; 0 STATED lines in any leg.

| Row (bound, ms) | Worst, ms (round 2's where it differs) | Instance |
|---|---:|---|
| AECP (20) | 4.693 | `notice-every-7.held.aecp.if0` |
| ACMP (30) | 6.813 | `notice-every-6.held.acmp.if0` |
| ADP (30) | 5.897 (5.522); ENTITY_AVAILABLE 4.413 | `notice-burst-1`; `backlog-adp@program-aged2-7` |
| MAAP (30) | 6.020 | `notice-every-0.held.maap.if0` |
| SRP (90) | 10.284 | `notice-every-6.held.srp.if0` |
| MRPDU (49) | 3.578 | `save-starved.mrpdu.periodic.if0` |
| AECP's notices (20) | 0.624 | `aecp-fanout`, SET_NAME |
| first queued notice (20) | 2.259 | `notice-burst-4` |
| last queued notice (130) | 26.195 (23.730) | `notice-burst-3` (40 queued) |
| largest legal command, paced R4L (238) | 2.442 | `aecp_long.refused.collision_values.if0` |

- Budget misses: 7, exactly the seven held-egress rows, each the same figure as round 2 and under round 1's ledger
  (63.083 / 63.305 / 63.526 / 63.747 / 63.969 / 62.025 / 61.680 ms); 0 new.
- Joins: 346 in 111 groups, 186.687 to 190.705 ms (gate 181.0 to 239.0); run-outs 2,311 (1,332 released, 979 empty),
  none late, absent or unresolved.
- Slices against 147,500: SRP's 146,052 (`backlog-adp@blank-aged2-1`), the build 137,924 (`srp`), THE RETRY's round
  89,462 (round 2 109,745). Passes given whole: build-one 137,924 of 147,500, step 81,053 of 97,500. THE SHARE: only
  `aecp-largest-notice`'s two passes (213,816), reported at 8x8/1if as before.
- **THE RETRY's rounds: 2,455,411, held to 165 / 255 / 25 us, none over** (the answering-every-port arm exited 1 on
  1,654 at round 2's costs).
- Load: 0.711 at the pin, 0.671 with tsn-c-stack#32 (0.75), with the cold start at 165 us (round 2 0.709 / 0.670).
- Every stated cost against this measurement (`receipts/model/restate-check-8x8-1if-d8629751.txt`): the SRP record's
  heaviest 32,421 cycles (345 us stated, the same record as round 2), every poll within its statement; every heaviest
  figure is the same as round 2's measurement's: nothing restated.
- **Rows by every source at 8x8/1if, derived and reported (owed to #872)** at `d8629751` with round 2's polls: R4 18.64,
  R5 113.95, R6 108.80, first 17.07, last 274.91, R4L 192.91, ACMP 45.56, ADP 44.85, MAAP 46.26, tx 58.61, txL 147.06
  ms; load 0.711 / 0.671; every command the largest 0.993 (`receipts/model/rows-8x8-1if-d8629751.txt`). The cold start
  at 165 us moves the queued notices' rows: the last 266.70 to 274.91 ms.

## 6. Restated figures

- **Stated from round 2's measurement (item 1):** `CTRL_LOOP_RETRY_COLD_US` 165 us and `CTRL_LOOP_RETRY_ATTEMPT_US` 25 us
  at (1, 9, 9) (section 2).
- **Not restated:** the measurement on the new image holds every other stated cost (section 5): `CTRL_LOOP_SRP_UNIT_US`
  345, `poll_grade.EIGHT_ONE` as round 2 restated it.
- **The documents restated** (`bae44edf`): FR_NFR 3.4.1 (the stated-cost rule: a refused attempt's restated at 8x8/1if;
  THE SHAPES with the round costs; the 8x8/1if gate measured again, every round within, the load 0.711); section 13
  (the table's two columns; the readers; "THE RETRY's round costs at 8x8/1if" in place of round 2's "Left for a
  decision"; the gate's figures with round 2's in brackets where they moved; the rows by every source, reported); the
  AECP README (the core's one compile-time header outside its own; the costs by shape); the harness README.

## 7. Gate table

**The full pass at the final head `716a8ae7`** (each part on its own clean clone, never piped; `launchC.py`, the sweep
on picked ranges, the queue on picked ranges or the session CPUs):

| Gate | Result | Receipt |
|---|---|---|
| The sweep, 4 shards (`native-shards.py`, label `894b-r3d`; CPUs 0-7, 16-23, 32-39, 40-47) | exit 0 each; 65 suites (15, 17, 17, 16), 2,713,040 checks, 0 failures, 0 SKIPPED (`TSN_GEN_ROOT` set) | `gates/sweep-shard{0..3}-716a8ae7.txt` |
| Every hosted job step of rtl-fast, rtl, elaborate, docs (`run_wf.py`, `verify_wf.py`) | 139 run, 226 not run with a reason, 0 bad | `gates/workflows-verify-716a8ae7.md` |
| Firmware jobs (unit, boundary, control, AECP, SRP campaigns, verilator) | every step 0; campaigns 716, 275, 345 caught, 0 escaped; boundary PASS; `aecp_wire.py --every` exit 0; the 8x8/1if mailbox arm `[ok]` | `firmware/firmware-jobs-716a8ae7.txt` |
| Lane gates a, b, c | 55 gates, 51 at 0, the four exit-1-by-design; harness self-test 879 checks, 259 caught, 0 escaped; rows_tiers 971/971, flip 581/581, load 25/25; load 0.513/0.509; table 24/24; flip 8x8/1if PASS (0.711), 1x1/1if PASS; 15 diff-check bases | `gates/lane-gates-716a8ae7.txt` |
| Harness legs at 1x1 and 8x8/2if | rc 0 but H-J8 (#910's build of one, as round 2); C-R1 caught; 48 joins, 185.485 to 190.040 ms; 172 run-outs, none late | `harness/legs-1x1-8x8-716a8ae7.txt` |
| Every image (Q-img) | six fixed identical to `184d47ca`'s; both 8x8/1if identical to the measured `d8629751`'s; 56.0 | `images/img-4-fullpass-716a8ae7.txt` |

**The first pass at `bae44edf` (superseded):** the same as above but one bad step, firmware-verilator's boundary step
(`aecp_wire.py` refused: `ctrl_loop.h: No such file or directory`), fixed in `716a8ae7`; its sweep's shard 3 ran
without `TSN_GEN_ROOT` and was run again (`gates/workflows-verify-bae44edf-first.md`,
`gates/firmware-verilator-step14-bae44edf-and-fix.txt`).

**Before the pass:**

| Gate | Where | Result |
|---|---|---|
| `shape_costs.py --check --selftest` | worktree | PASS, 24 of 24 controls refused |
| quick gates (flip x3, load, rows_tiers, tier_grid, docs, em-dash, idioms, diff, ctrl_hot) | worktree before commit | as expected (flip 8x8/2if rc 1 by design); the Python idiom gate first failed on two lines of 121 columns, wrapped before the commit; 8x8/1if load 0.711 |
| the new self-test checks and mutants (quick run of `selftest_round.round_checks`) | worktree | 49 checks pass; both new mutants and the two earlier round mutants caught |
| AECP host arms: core at 1 and 2 interfaces, debug | worktree | rc 0 (83, 83, 1 tests) |
| AECP 8x8/1if mailbox tests (`EIGHT_ONE`) | worktree | 4 of 4 selected pass |
| **Harness self-test** (`run.py --self-test`) | `d8629751`, clean clone `hC` | **0 failures: 879 checks, 259 mutants caught, 0 escaped**; both new mutants caught by the 8x8/1if round check (`receipts/harness/harness-selftest-d8629751.txt`) |

## 8. Run history

- 14:31 CET: start. Read the round 3 ruling (fetched, scratch), 6871343905 and 6867990126. Round 2's finished scratch
  deleted (the full pass's clones, the measurement's arm A builds), the B-AE logs kept for the derivation.
- 14:4x: the derivation from B-AE's logs (`retry_line.py`): 165 and 25 us.
- 14:52: step 1 images (unit on session CPUs 96-127): all 8 identical. 15:0x: step 2: six fixed identical, 56.0.
- 15:03: committed `d8629751`. The shared picker had no free range (0-95 all booked by other lanes); the measurement
  launcher (`launchM.py`) takes ranges as they free, falling back to this session's CPUs after 15 minutes (at most two
  there). 15:04: C-launch, C-AL and C-st (the harness self-test, clean clone `hC`) started on 96-127.
- 15:09-15:27: C-AL rc 0; C-CTA caught; C-st rc 0 (879 checks, 259 caught). C-A0 and C-AE took picked ranges as they
  freed (24-31, 40-47); C-A1 fell back to the session CPUs at 15:26.
- Docs drafted in the worktree (uncommitted): FR_NFR 3.4.1's two rule sentences, section 13's table and rule text, the
  AECP and harness READMEs; the measured figures wait for the gate.
- 15:56: C-AE rc 0, 0 STATED lines. 17:04-17:35: arm A's four parts rc 0, 0 STATED lines. 17:3x: the gate PASS
  (`gate_r3.py`); every stated cost within its measurement; the rows by every source re-derived (reported).
- 17:3x: committed `bae44edfaaaef3e8927060fad5335273611308e1` (docs). origin/894-tiers still `7398ec0a`, #902 OPEN,
  dev-soft-core `cec88385`: no sync merge in the round.
- 17:39: the full pass at `bae44edf` (`launchC.py`, label `894b-r3`): the sweep's four shards on picked 24-31, 32-39,
  40-47, 64-71 (each unit's affinity checked); the queue (`mkqueueC.sh`) on picked ranges, falling back to the session
  CPUs after 5 minutes (at most two there). Round 2's sweep clones on /data (mine, finished) removed first.
- 18:05-18:49: the firmware jobs (boundary, control, AECP, SRP campaigns, unit) ended rc 0: campaigns 716, 275 and 345
  caught, 0 escaped. lane-b 18:32, lane-a 18:49 rc 0 (their gates' rc below).
- 18:35-18:46: sweep shards 3, 1 and 0 ended, exit 0. **Shard 3 ran 20,734 checks, not round 2's 21,575: `tsn_fuzz`'s
  field campaigns were SKIPPED, because the sweep spec (taken from another lane's) lacked `TSN_GEN_ROOT`, which round 2's
  carried.** Shards 0 and 1 match round 2's counts exactly (361,003; 2,046,229). 18:5x: shard 3 run again
  (`shard-3b`, the same clone cleaned as `native-shards.py` cleans it, the spec with `TSN_GEN_ROOT` added) on picked
  24-31 (affinity checked). The first shard-3 run is not counted.
- 18:53-19:55: the rest of the queue ended: every hosted job's driver rc 0 (docs-check-no-git's post-run `git status`
  fails by design, as in round 2), the legs as #902's (H-J8 exits 1 on #910's build of one, 138,054 and 147,814 against
  121,500, the same as round 2), Q-img: the six fixed identical to `184d47ca`'s, both 8x8/1if identical to the measured
  image. Shard 3b 19:47 exit 0, 21,575 checks, nothing skipped: the sweep 65 suites, 2,713,040 checks, 0 failures.
- 19:56: `verify_wf.py` at `bae44edf`: 139 run, 226 not run with a reason, **1 bad: firmware-verilator's ci_step_14**
  (`ctrl_boundary.py --require-rv32 --selftest --only verilator`), REFUSED because `aecp_wire.py --every` exits 1:
  `aecp.c:6: fatal error: ctrl_loop.h: No such file or directory`. **My change's defect:** the wire comparison builds
  the AECP core standalone with `-I aecp` and the stack's headers only, a compile context I did not run before the
  commit (the host core arms, which I did fix, are another). Fix: `sw/firmware/ctrl/test/aecp_wire.py:133-136` adds
  `-I loop -I mbx`, as `aecp_arms.core_arm` does. Reproduced before the fix (rc 1, the same words), and after it
  `aecp_wire.py --every` passes at one and two interfaces (142 and 294 observations, 11 oracle controls each). The
  full pass at `bae44edf` is therefore not the final one; it runs again at the fix's head.
- 20:0x: the boundary step at the fix (worktree, `ctrl_boundary.py --require-rv32 --selftest --only verilator`): PASS
  (the first try there exited 2 on my unit's missing `MAKEFLAGS=--no-print-directory`, environment only). 20:1x:
  committed `716a8ae7979a31315a6e085959dc4dcc8b7ee022` (the fix). origin/894-tiers `7398ec0a`, #902 OPEN,
  dev-soft-core `cec88385`: no sync merge. The first pass's scratch removed (its verifier output and step 14's log kept
  as receipts).
- 20:20: the full pass at `716a8ae7` (`G-launch`; the sweep spec now carries `TSN_GEN_ROOT`). **A slip of mine:** the
  sweep reused label `894b-r3`, whose four clones on /data were `--shared` clones of the first pass's source clone,
  which I had just deleted, so their object alternates were broken (git printed "unable to normalize alternate object
  path"). The four shard units (mine, their arguments listed first) were stopped at once by unit name, their clones
  deleted, and the sweep relaunched on fresh clones under label `894b-r3d` (`H-launch`, the sweep first, then the 25
  queue lines `G-launch` had not started; `G-launch` stopped after listing its arguments). The five firmware jobs
  `G-launch` had started run on, on their own fresh clones at `716a8ae7`.
- 20:39-23:07: the final full pass at `716a8ae7` ran to the end: the sweep 21:35-21:51 (exit 0 each, 2,713,040
  checks), the firmware jobs, the lane gates, every hosted job (`verify_wf.py` 23:0x: 139 run, 226 not run with a
  reason, 0 bad), the legs (H-J8 exit 1 as round 2), Q-img (identical as above).
- 23:1x: origin/894-tiers found at `9606b3a9` (#902 OPEN, its round 12 delta reviews NEGATIVE at that head): ten commits
  pushed after 20:1x, `aecp_maps.c`'s code among them. Not merged (section 0, item 4); left for a decision in the
  REVIEW READY.
- 23:2x: receipts written and indexed (`index.py`: 0 bad); REVIEW READY posted on #894, issuecomment-6884981996, the
  round's one comment. Nothing pushed; no PR created or edited; no merge.
