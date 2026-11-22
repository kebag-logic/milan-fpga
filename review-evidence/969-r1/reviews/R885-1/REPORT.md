[R885] NEGATIVE - exact head f863258d2a455697d85a5ab48813be8f0783e2d4

Round R885-1, internal cleared-context independent review of issue #969 / PR #971 (part of #665), branch `pf-969-1`
stacked on the flip PR's reviewed head `dd163e41` (PR #960; PR base `dev-soft-core`). Exact head
`f863258d2a455697d85a5ab48813be8f0783e2d4`, tree `b3eb9ddc12c32518963a7f61f1774929894f01be`. Reviewed delta:
`git diff dd163e41..f863258d` (17 commits, 17 files, +939/-93). All five lenses applied. Findings are in section 2,
the reviewer-owned ledger in section 4, and the prior public findings, retained, in section 8.

Verdict basis: four findings are open.
- F1, MAJOR: the CPU budget evidence never executes the changed receive and build paths.
- F3, MAJOR: a stale kept count after an interface reset or a reclaim refuses the last in-bound Talker of one
  receive. This is the external round's R886-1-F1, which I reproduced independently at this head.
- F2, MINOR: the authoritative memory docs still state the old ledger entries and planted ledgers.
- F4, MINOR: the gate does not plant the early defects at 8x8/1if, although the PR text says it does. This is
  R886-1-F2.

The cause and the main fix are confirmed. The cause reproduces failing-first at the base on every STREAM_INPUT at
1x1/1if and 8x8/1if in both orders, and the control order passes at the base. Every arm and planted defect I ran
passes or is caught at the head, apart from the F3 scenario.

Order of work: sections 1 to 7 were written from my own pass before I read any other review. Section 8 records what
reading the external round then changed: F3 added, F4 raised from RESIDUE to MINOR, F2 extended, and Conformance
changed from CLEAN to UNCLEAN.

## 1. Reconstruction (public state only)

- Contract: AGENTS.md, CONTRIBUTING.md (by AGENTS.md's pointers), the issue #969 body (frozen acceptance: at 8x8/1if
  and 1x1/1if, on every STREAM_INPUT, a binding made or restored while the Talker attribute is already registered
  declares its Listener within one transmit of the probe's success, after a power-on settle and after a bind while
  bound; a host test covers both orders with a planted defect for each; REGISTERING / REGISTERING_FAILED in
  GET_STREAM_INFO follow), the author's TAKEN (#969 issuecomment-7077075041, the bound of one kept Talker per
  STREAM_INPUT stated publicly before implementation) and REVIEW READY (#969 issuecomment-7080057766), the PR body,
  and the public packet `review-evidence/969-r1/author-r1` at `4ce6f35f`.
- Clauses: Milan v1.2 5.3.8.5, 5.5.3.5.18 step 4, Tables 5.9/5.10; IEEE 802.1Q-2018 10.7 (filtering to attributes of
  immediate interest), 10.7.8 NOTE, Table 10-3 (QA quiet; LO answers with In on tx), 35.2.6; the #925 latest-kind
  ruling; #930's walk schedule.
- Interfaces read: `sw/firmware/ctrl/srp/srp_mbx.c` / `.h` (filter, walk, bind, receive, poll), lwSRP
  `src/core/mrp_mad.c` (filter at :998 before any allocation; applicant table :149-240), `mrp.h:292-297` (filter
  contract), `ctrl_loop.h:361-377` (per-shape stated costs), `tb/verilator/ctrl_service_budget/` (scenario.py,
  load_grade.py, rows_tiers.py, shape_costs.py), `protocol-processor/hdl/srp/KL_srp_listener_fsm.sv:28-33` (the
  release processor's N port registrars, #212).

## 2. Findings

### F1 - MAJOR - RTL, Robustness, Tests, Docs - the CPU budget evidence does not execute the changed paths

- Artifacts:
  - The harness's MSRP stimuli: `tb/verilator/ctrl_service_budget/scenario.py:644-671` (the `srp` group) and every
    other MSRP stimulus (`receipts/budget-harness-msrp-stimuli.txt`). They are attribute types 3 (Listener) and 4
    (Domain) only; no Talker Advertise (1) or Talker Failed (2) appears anywhere in the harness.
  - The changed receive path in `sw/firmware/ctrl/srp/srp_mbx.c`: `:518` and `:460-478` (`keep_talker`, now on every
    Talker event of a StreamID no binding holds, past the bound too); `:284-294` (`talker_changed`'s new hold);
    `:944-954` with `:975` (`count_kept`, a full registrar visit before a receive whenever a binding changed or, at
    the bound, whenever any pool block was returned since the last count).
  - The changed build path: lwSRP `src/core/mrp_mad.c:183`. An observed attribute in LO transmits In on tx!, so
    every kept Talker is encoded in the entity's MRPDU after each LeaveAll.
  - The stated bounds: `ctrl_loop.h:364,373` (`CTRL_LOOP_SRP_UNIT_US`, 285 us at 1x1/1if and 375 us at 8x8/1if), and
    the author's `grader-flip_grade.py_--check_--point_8x8_1if.txt` (THE TRANSMIT's row, 76.81 ms against 77 ms).
  - The PR body's claim: "Re-measured on the five groups that run the changed paths (srp, acmp-cmd, fixture,
    backlog, backlog-owed) ... No stated cost or row bound moved".
- Authority/evidence:
  - The stated costs are measurements, "each the most measured over every instance plus 5 %"
    (`load_grade.py:153-155`). record.srp at 8x8/1if comes from 35,547 cycles measured in srp-talker-held
    (`load_grade.py:141-144`).
  - The slice starts an SRP record only while `CTRL_LOOP_SRP_UNIT_US` is left, so a record that costs more than its
    unit runs the slice past its length (`ctrl_loop.h:305-313`).
  - Focus item (4) of this round requires the CPU budget at 1x1/1if and 8x8/1if within bounds, with no load
    regression.
  - No group of the harness ever receives a peer Talker attribute. So none of the five re-measured groups enters
    `keep_talker`'s acceptance, the new hold, the kept attributes' creation and indication, the at-bound recount, or
    the In encodings of kept attributes.
  - The per-probe deltas the author published (`per-probe-base-vs-head.txt`) therefore cannot show the change's
    cost. The srp group's probes are a Listener Ready, a malformed MRPDU and a Domain.
- Impact: before #969, a Talker of a StreamID no binding holds cost one filter scan and allocated nothing. Now:
  - up to `SRP_KEPT_TALKERS` such Talkers an interface (2 at 1x1, 9 at 8x8) each become an lwSRP attribute with a
    registration, an indication and a held entry;
  - every such event, including a flood past the bound, adds a scan of the kept list beside the bindings' scan;
  - at the bound, practically every receive adds a visit of every attribute, because each registration's map work
    returns a block (`srp_mbx.c:977-983`);
  - each LeaveAll adds up to `SRP_KEPT_TALKERS` Talker encodings to THE TRANSMIT's build.

  The issue's own stimulus, the talker's declarations for every input arriving before the bindings settle, is
  exactly such a record. Nothing shows either way whether it stays within 285/375 us, or whether the 8x8/1if tx row
  stays within 77 ms, where the margin is 0.19 ms. A record past its unit breaks the tier-2 slice bound on the
  shipping images.
- Required outcome: measured evidence on the CPU budget harness's built image at 1x1/1if and 8x8/1if, at the exact
  head (after F3's correction), of:
  - (a) the receive of an MRPDU carrying a Talker Advertise for every STREAM_INPUT's StreamID with no binding yet
    (the power-on order), and of one carrying a Talker Failed, each record against `CTRL_LOOP_SRP_UNIT_US`;
  - (b) a receive at the bound after a block return (the recount), with Talkers of further unbound StreamIDs past
    the bound in the same record, against `CTRL_LOOP_SRP_UNIT_US`;
  - (c) THE TRANSMIT's build after a LeaveAll with the kept attributes present, against `CTRL_LOOP_BUILD_PASS_US` /
    `CTRL_LOOP_BUILD_ONE_PASS_US` and the 77 ms tx row at 8x8/1if.

  Any cost past its statement is restated by the stated rule or by an owner ruling, and the PR text says which group
  executes which changed path.
- Verification: the new group's receipts with per-record and per-build cycles at both points;
  `flip_grade.py --check` at 1x1/1if and 8x8/1if, `load_grade.py --check`, `shape_costs.py --check` passing on the
  restated figures.

### F2 - MINOR - Docs - the authoritative memory docs still state the old entries and planted ledgers

- Artifacts at the head, each still stating the old figure:

  | Location | Stated at the head |
  |---|---|
  | `docs/design/SPLIT_CONTROL_MEMORY.md:188` | "or plans 63.5" |
  | `docs/design/SPLIT_CONTROL_MEMORY.md:189` | "or plans the platform's 63.0" |
  | `docs/design/SPLIT_CONTROL_MEMORY.md:190` | "or plans 58.0" |
  | `docs/design/SPLIT_CONTROL_MEMORY.md:305` | "63.0 RAMB36, a debt of 7.0, 28,672 B" |
  | `docs/design/SPLIT_CONTROL_MEMORY.md:307` | "58.0, a debt of 2.0, 8,192 B" |
  | `docs/design/SPLIT_CONTROL_MEMORY.md:311` | "holds the platform's two-interface entry at 63.0 ... the platform's one-interface entry at 58.0" |
  | `sw/firmware/ctrl/plat/README.md:147` | "plans 57.5 RAMB36 in the composed train ... Its own entry ledgers it at 57.5" |
  | `sw/litex/ctrl_memory_ledger.py:10` (module docstring; from R886-1-F3) | "the target platform's at 63.0" |

- Authority/evidence:
  - `sw/litex/ctrl_memory.py` `LEDGERED` now holds 63.5 and 58.5 (the diff lines for `platform-8x8-two-interfaces`
    and `-one-interface`).
  - `sw/litex/ctrl_memory_ledger.py:167,169,173` plant 64.0, 63.5 and 59.0.
  - `plat_ledger.py` at the head plans 63.5 and 58.5 (`receipts/plat_ledger-head.log`).
  - The PR updated the neighbouring sentences (`SPLIT_CONTROL_MEMORY.md:162-163`, `plat/README.md:146,174`, the
    docstring's own list) but not these, so each file now states both figures.
  - `:188`, `:189`, `:305`, `:307`, `:311` and the docstring were true at `dd163e41` and are made stale by this PR.
    `:190` and `plat/README.md:147` were already one step stale at the base and are now two.
  - AGENTS.md section 6, Docs: changed contracts are reflected in the authoritative docs.
- Impact: a cold reader of the authoritative ledger doc reads the 8x8 entries, their debt to S14 and the planted
  controls at figures the code refuses. These are figures, so this is not residue.
- Required outcome:

  | Location | Should state |
  |---|---|
  | `:188` | 64.0 |
  | `:189` | the platform's 63.5 |
  | `:190` | 59.0 |
  | `:305` | 63.5 RAMB36, a debt of 7.5, 30,720 B (with the kept Talkers, #969) |
  | `:307` | 58.5, a debt of 2.5, 10,240 B |
  | `:311` | the two-interface entry at 63.5 with the kept Talkers (#969), 63.0 with each AAF Stream Input's format written (#946); the one-interface entry at 58.5 with them, 58.0 with the largest legal record's cut |
  | `plat/README.md:147` | 58.5 with the kept Talkers (720 B of `rom` past 58.0, 1,328 B left); its own entry at 58.5, refused at 59.0 |
  | `ctrl_memory_ledger.py:10` | the target platform's at 63.5 |

- Verification: `grep -n` of those lines against `ctrl_memory.LEDGERED`, `OWN` and `planted()`; the docs workflow's
  gates.

### F3 - MAJOR - Conformance, RTL, Robustness, Tests, Docs - a stale kept count below the bound refuses the last in-bound Talker of one receive

This is the external round's R886-1-F1, retained and reproduced here.

- Artifacts:
  - `sw/firmware/ctrl/srp/srp_mbx.c:944-954` (`count_kept` recounts only when a binding changed or when the count is
    already at the bound) and `:940-943`, whose comment says "Below the bound the count is at least the attributes
    kept, which is all keep_talker needs";
  - `:460-478` (`keep_talker`);
  - `:975` (one count before the whole receive);
  - `sw/firmware/ctrl/srp/README.md:353-359` (the same invariant);
  - the reviewer probe `scripts/stale_count_probe.cpp`.
- Evidence: the probe was run as `SrpStaleCountProbe.*` in `srp_mbx.cpp` at 1x1 and 8x8, with one and two interfaces
  (`receipts/tally-stale-count-probe-head.txt`, raw logs in `receipts/raw/head-f1/`). The steps:
  1. Keep one unrelated Talker (below the bound).
  2. Either reset interface 0 (link down and up), or let that Talker leave and its block be reclaimed.
  3. Offer one MRPDU carrying a Talker Advertise message for every STREAM_INPUT's StreamID.
  4. Bind every input.

  Results:
  - After the reset and after the reclaim, the last input does not declare: input 1 at 1x1 and input 8 at 8x8. Its
    desired, declared and feedback kinds stay 0, and its Listener is absent from THE TRANSMIT's next MRPDU.
  - The same MRPDU into a fresh registrar passes (`ZProbeFreshOneReceiveOfEveryInput`).
  - This is 2 failures and 1 pass on each of the 4 arms.
  - The cause: the count kept from before the reset or reclaim is never recounted below the bound, and no recount
    can happen inside a receive.
- Impact: after a link flap, which is common at boot and on a cable re-plug, a bridge re-declares every Talker in
  one MRPDU. The entity then registers only N-1 of the N it has room for, and the last input waits for the talker's
  next declaration, up to a LeaveAll period. That is #969's original symptom on one input, inside the bound, so it
  is not the documented past-the-bound allowance. It falls under the issue's acceptance (a binding made or restored
  while the Talker is registered declares within one transmit), on the bench's order of a power-on with a link that
  settles twice.
- Required outcome: the admission count must not refuse an in-bound Talker because of occupancy that no longer
  exists, after an interface reset or a reclaim, including within one multi-attribute receive. The storage bound,
  the precedence of bound StreamIDs, callback non-reentrancy and the unbound walk policy are kept. The comment at
  `:940-943` and the README invariant are corrected. A regression test of partial occupancy, then a reset or a
  reclaim, then a full receive is added at 1x1 and 8x8, with a planted defect that the test catches.
- Verification: this round's three probes pass on every input at both shapes and interface counts, together with
  the existing SrpEarlyTalker, S13/S14 and control cases. The new plant is caught, and the `kept-unlisted` probe
  (section 2, Observations) is rechecked against the new test. F1's measurement covers the corrected accounting.

### F4 - MINOR - Tests, Docs - the gate does not plant the early defects at 8x8/1if, although the PR text says it does

This is the external round's R886-1-F2, retained. My pre-read pass recorded it as RESIDUE R1; I raise it to MINOR
(section 8).

- Artifacts: PR #971 body, "Planted defects: 11 in `srp_early_mutants.py` (SRP campaign, both interface counts and
  8x8/1if)"; REVIEW READY, "the 11 new plants at each interface count and at 8x8/1if"; `test_ctrl_firmware.py:232-235`.
- Evidence:
  - The 8x8/1if campaign plants only the `listener-copy-` and SRP-cut prefixes.
  - The author's shard-3 log lists each `feedback-early-*` plant twice: the two-interface and one-interface
    campaigns at the 1x1 entity (lines 1447-1487 and 1655-1665). None is in the 8x8/1if block.
  - This round planted all 11 at 8x8/1if and 8x8/2if itself, through the tree's own `srp_mutants.campaign`, and every
    one was caught (`receipts/early-campaign-8x8-if1.log`, `-if2.log`, raw logs in `receipts/raw/early-8x8-if*/`).
- Impact: the stated gate scope is not the gate's. A regression specific to 8x8 in these rules would pass all four
  shards.
- Required outcome: either the 8x8/1if campaign plants the early defects (and the receipt shows them caught), or the
  PR body and evidence state the gate's actual scope: "SRP campaign at the 1x1 entity, one and two interfaces; the
  platform's `early-talker-ignored` at 8x8/1if and 1x1/1if".
- Verification: the shard-3 receipt, or the corrected PR body.

### Observations (no finding)

- The `kept-unlisted` probe survived every SRP arm (19 arms; `receipts/tally-allsrp-p-kept-unlisted.txt`). In that
  probe, the filter counts a newly kept Talker without listing it, so a refresh of it is counted again. At the bound,
  the next receive relists from the registrar after any returned block. Below the bound, the over-count persists:
  it is the same class of defect as F3, and no test grades the count below the bound across receives. It survives
  for the reason F3 exists. My pre-read draft called this "practically equivalent" because the over-count would be
  recounted; that was wrong for the reason F3 shows, and I withdraw it. F3's regression test should be checked
  against this probe.
- The `unbound-walks` probe (the base's walk on every Talker indication) survived. That is expected: it is the
  base's schedule, a difference in load only, and the #930 differential grades mailbox writes and licences, not walk
  counts.
- The ledger reason strings in `sw/litex/ctrl_memory.py` add "owed to S14" in two entries. These are data strings,
  not source comments, and they follow the form of every existing entry, so the comment rule (owner 2026-10-15)
  does not apply. No added source comment carries a new lane label, review round, reviewer ID or issue-comment ID.
  `S13`/`S14` in `test_plat_sinks.cpp` and `sink_mutants.py` are test-case IDs continuing that suite's `S1`..`S12`.
- The bound is first-come. On a network where more unbound Talkers than `SRP_KEPT_TALKERS` reach the entity before
  its bindings settle, a wanted one can be refused, and then waits for the talker's next declaration (at most a
  LeaveAll period). This matches the release processor's count, it was stated publicly in TAKEN, and the PR's
  limitations say it. The bench re-run should record how many Talkers the test network declares.

## 3. Lens results (each with what was examined at the head)

**Conformance: UNCLEAN (F3).** Examined `srp_mbx.c:460-519,260-295,944-976` against Milan v1.2 5.3.8.5, 5.5.3.5.18
step 4 and Tables 5.9/5.10, and IEEE 802.1Q-2018 10.7, 10.7.8, Table 10-3 and 35.2.6. My pre-read pass found every
acceptance criterion met on the host model:
- Own failing-first at the base adapter (the `dd163e41` `srp_mbx.c`/`.h` under the head's tests): all 6 arms fail on
  the cases the fix owns (`receipts/tally-basesrc.txt`).
- S13 (power-on restore, Advertise and Failed) and S14 (BIND_RX while bound) fail at 8x8/1if on every input 0-8, and
  at 1x1/1if on inputs 0-1. They fail on the words for the declaration in the next MRPDU, within a JoinTime,
  REGISTERING and REGISTERING_FAILED (`receipts/base-platsinks-failures-by-input.txt`). Inputs 2-3 of S13 at 8x8 fail
  one step earlier: no MRPDU follows the probe's answer at all.
- My own control probe (`scripts/control_test.cpp`: UNBIND_RX then BIND_RX to the same stream, on every input)
  passes at the base and at the head (`receipts/tally-basesrc-ctl.txt`, `receipts/tally-head-ctl.txt`).
- The binding-first order passes at the base.
- At the head, every arm passes (`receipts/tally-head.txt`).

F3, retained after independent reproduction, is an acceptance-level failure inside the bound, so the lens is
UNCLEAN.

**RTL: UNCLEAN (F1, F3).** No RTL, mailbox-contract or lwSRP file changes in the diff stat. Examined: the static
assertions `srp_mbx.c:29,31`; `SRP_HELD_STREAMS` (`srp_mbx.h:161`); the pool's fixed 16 blocks against
`change_domain`'s four; the plat_ledger plan; the size fixture's stand-in at 56.0; the author's route receipts.
These are clean. The CPU timing effect is not established (F1), and the admission-accounting invariant is false (F3).

**Robustness: UNCLEAN (F1, F3).** Examined:
- the bound against a flood: `interested_msrp` takes a bound StreamID before `keep_talker` (`srp_mbx.c:510-518`); at
  most `SRP_KEPT_TALKERS` attributes an interface are kept, funded by the fixed blocks; nothing is allocated past
  the bound;
- reset, replay after a refused receive, two interfaces, and the at-bound recount.

Memory exposure is bounded, and bound Talkers are not starved of blocks. Reset and reclaim below the bound fail
(F3), and the CPU exposure at the bound is unmeasured (F1).

**Tests: UNCLEAN (F1, F3, F4).** I checked independently that the new tests can fail for their defects:
- the 11 early plants are caught at 8x8/1if and 8x8/2if (`receipts/early-campaign-8x8-if*.log`);
- 6 of my 8 probes are caught (`receipts/tally-p-*.txt`: own-declared-counted, bound-counted, bound-plus-one,
  hold-bound-too, any-stream-kept, bound-one-short); the two survivors are analysed above;
- the restated `AHeldStreamEndsWithEitherRegistrationOrAReset` keeps its base semantics (an unanswered LeaveAll)
  and passes at the base, so it is not weakened;
- every SRP suite of the gate passes at the head: 19 arms, including srp_listeners at 1x1/1if and 8x8/1if, the #930
  differential (`receipts/tally-allsrp-head.txt`).

Missing: the reset/reclaim-then-full-receive case (F3), the budget measurement of the change (F1), and the gate's
8x8/1if plants (F4).

**Docs: UNCLEAN (F1's PR sentence, F2, F3's invariant, F4's PR sentence).** Examined `srp/README.md` (the filter,
pool, held and kept-Talker text, and D4 against `KL_srp_listener_fsm.sv:28-33`), `srp_mbx.h:126-161` and the new
comments, `plat/README.md`, `SPLIT_CONTROL_MEMORY.md`, `ctrl_split_boot/README.md`, `ctrl_memory_ledger.py`'s
docstring, and the PR body.

## 4. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F3) | `srp_mbx.c` filter/keep/count/hold/bind; issue acceptance; Milan 5.3.8.5, 5.5.3.5.18, Tables 5.9/5.10; own failing-first at base, control probe, head arms; stale-count probe | R885-1 | f863258d2a455697d85a5ab48813be8f0783e2d4 |
| RTL | UNCLEAN (F1, F3) | no RTL in diff; static asserts, pool funding, held bound; plat_ledger, fixture plan, route receipts; CPU budget stated costs vs changed paths; admission invariant | R885-1 | f863258d2a455697d85a5ab48813be8f0783e2d4 |
| Robustness | UNCLEAN (F1, F3) | flood/bound, reset, reclaim, replay, two interfaces, at-bound recount; memory bounded; CPU at bound unmeasured | R885-1 | f863258d2a455697d85a5ab48813be8f0783e2d4 |
| Tests | UNCLEAN (F1, F3, F4) | `srp_mbx.cpp` SrpEarlyTalker, `test_plat_sinks.cpp` S13/S14, `srp_early_mutants.py`, `sink_mutants.py`, `test_ctrl_firmware.py:232`; 8x8 plant campaigns; 9 probes; 19 SRP arms; budget harness stimuli | R885-1 | f863258d2a455697d85a5ab48813be8f0783e2d4 |
| Docs | UNCLEAN (F1, F2, F3, F4) | `srp/README.md`, `srp_mbx.h`, `srp_mbx.c:940-943`, `plat/README.md`, `SPLIT_CONTROL_MEMORY.md`, `ctrl_split_boot/README.md`, `ctrl_memory_ledger.py:10`, PR body | R885-1 | f863258d2a455697d85a5ab48813be8f0783e2d4 |

No lens is banked clean by this round.

## 5. Gates checked by this round (own execution at the head unless stated)

- srp_mbx.cpp at 1x1/8x8 x 1/2 interfaces and platsinks at 8x8/1if and 1x1/1if: PASS, 95/95/96/96/14/14
  (`receipts/tally-head.txt`). Every SRP suite of the gate: 19 arms PASS (`receipts/tally-allsrp-head.txt`).
- Early plants at 8x8/1if and 8x8/2if: 22 of 22 caught. The gate's own four shards are the author's receipts at
  `4c5018eb` (firmware as final); I read shard 3's plant list and did not re-run them.
- `fw_coverage.py --check`: PASS (40 files); `srp_mbx.c` 854/854 lines, 773/776 raw branches (100.00 % effective)
  (`receipts/fw_coverage-check-head.log`). Coverage does not reach F3's scenario.
- `test_ctrl_memory.py`: PASS, 0 failures (`receipts/test_ctrl_memory-head.log`).
- `plat_ledger.py`: PASS, 0 findings (`receipts/plat_ledger-head.log`). The size fixture's 8x8/1if stand-in plans
  56.0 RAMB36 (rom 130,808 B of 131,072; sram 97,072 B of 98,304), within 56 (`receipts/fixture-plans-head.txt`).
  The platform points:

  | Point | RAMB36 | rom, B | sram, B | `ctrl_plat`, B |
  |---|---:|---:|---:|---:|
  | 1x1/1if | 45.5 | 127,224 | 56,736 | 18,048 |
  | 1x1/2if | 46 | 128,832 | 59,104 | 19,776 |
  | 8x8/1if | 58.5 | 139,984 | 98,288 | 19,072 |
  | 8x8/2if | 63.5 | 141,568 | 115,760 | 21,824 |

- Hot list unmoved, and the release bios identity: the author's receipts (`hot-code-identity*.txt`,
  `release-all-fabric-base-vs-head.txt`), read, not re-run. Twin and plants: the author's receipt, not re-run.
- Routes: the author's receipts at `f6f83166`, read, not re-run (no Vivado here). They use the same rom and sram
  banks as the head; the head's rom is 24 B smaller in the same banks, so they are not timing proof at exact
  `f863258d`. #818's floor is met at every corner: 8x8/1if WNS +0.058 / WHS +0.036 ns; 1x1/1if +0.437 / +0.017 ns.
- Hosted checks at the exact head (snapshot `receipts/hosted-checks-f863258d.txt`): 29 completed with success; 1
  skipped (the nightly/manual physical gPTP context, not executed); 28 queued or in progress; none failed. The
  manager owns hosted/act acceptance.

## 6. Real limits

- No CPU-budget harness run here (it needs an SoC build per point). F1 rests on reading the harness's stimuli and
  the code paths, not on a measured overrun, and says so.
- The firmware gate's four shards, the twin, the docs workflow and the routes were not re-run; their receipts are
  the author's. My executions are the focused arms, campaigns and probes listed above.
- No bench, and no physical calibration. Host-model passes are not hardware proof.
- Probes ran in disposable copies under the packet's scratch. The review clone was never edited: after the probes,
  HEAD, tree, index and worktree equal the exact head, and every submodule is at its gitlink
  (`receipts/clone-integrity.txt`).

## 7. Pending manager duties

- Current-dev candidate merge validation (builder and native banks) at the merge turn, against live dev `e275d795`.
  No manager source bank exists at this head, and none is claimed here.
- Hosted/act acceptance at the exact head (28 contexts were still running at the snapshot).
- After the corrections, an independent re-review of the corrected head, covering all five lenses.
- The bench re-run after merge, at 8x8/1if and 1x1/1if: both orders, the control, and a link flap before the
  talker's declarations (F3), recording how many Talkers the test network declares.

## 8. Prior public findings on this PR

Read only after sections 1-7 above had been written from my own pass. At that point the draft's verdict was already
NEGATIVE, on F1 (MAJOR), F2 (MINOR) and R1 (RESIDUE), with Conformance CLEAN. The PR's public comments at reading
time held two review-start notes and one finding-bearing round: the external round R886-1
(PR #971 issuecomment-7080351329, at this same exact head). Each of its findings is resolved or retained at this
head as follows.

| Prior finding | Status at f863258d | Basis |
|---|---|---|
| R886-1-F1, MAJOR, stale kept count after reset/reclaim | RETAINED as F3 | Reproduced independently with my own probe (`scripts/stale_count_probe.cpp`; fails at 1x1 and 8x8, one and two interfaces; the fresh control passes). My pre-read analysis had assumed a below-bound over-count is harmless. That is wrong for a multi-attribute receive, and I withdraw it. Conformance in my ledger moves from CLEAN to UNCLEAN. |
| R886-1-F2, MINOR, early plants not in the 8x8/1if gate | RETAINED as F4 | The same defect as my pre-read R1. The gate's selection is unchanged at this head (`test_ctrl_firmware.py:232-235`). I raise R1 from RESIDUE to MINOR, since a cold reviewer reads it as a gate-scope defect and the owner's rule sends uncertain cases to MINOR. |
| R886-1-F3, MINOR, ledger figures in prose | RETAINED, folded into F2 | Its two `SPLIT_CONTROL_MEMORY.md` items are F2's `:188`/`:189`. Its `ctrl_memory_ledger.py:10` docstring item is confirmed and added to F2. |

R885-1 FINISHED
