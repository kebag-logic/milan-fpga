[R853] POSITIVE - exact head 544fd72cefbd27379ae756c6ce02ae8b7ba15f2c

# R853-4: internal review of PR #934 (#665 dev sync), round 7 delta

- **Exact head:** `544fd72cefbd27379ae756c6ce02ae8b7ba15f2c`, tree `5f901ed8640509bd9211a0e96059ccea97401bdf`, checked out
  in an isolated detached clone. The tree was clean before and after the probes (`receipts/restore.txt`).
- **Delta reviewed:** `9aa55d3b..544fd72c`, two commits.
  - `38d89bb0`: the testbench records each build's participant, and an owned run-out is graded only on a build that
    can be its owner's.
  - `544fd72c`: the README mutant table.
  - The delta touches 10 files, all under `tb/verilator/ctrl_service_budget/` plus `docs/reference/FR_NFR.md`. There is
    no firmware, product RTL, configuration or bound change.
- **Scope:** narrow delta only, as instructed. Code the delta does not touch keeps the verdicts of earlier rounds,
  including the external POSITIVE at `9aa55d3b`.

All five lenses are CLEAN at this head. R853-3-F1 is closed at its cause, and R853-3-RES-1 and R853-3-SUG-1 are
resolved. This round has no BLOCKER, MAJOR or MINOR finding. It records one RESIDUE, in issue-comment prose only, and
three SUGGESTIONs.

## Method (public state only)

1. **Context.** I read AGENTS.md and the issue scope as given in the review assignment. Then I read the delta itself:
   `sim_main.cpp`, `observers.py`, `mrpdu_grade.py`, `join_grade.py`, `run.py`, the three self-test files, the README
   and FR_NFR 3.4.1.
2. **Firmware contract.** I checked the delta against `sw/firmware/ctrl/srp/srp_mbx.c`: `participant()` at `:82` and
   `build_mrpdu` at `:1091`, with its two callers at `:1215` and `:1262`.
3. **Measurement images.** I compiled both shapes' split images myself with the CI-pinned RV32 compiler
   (`receipts/build_mrpdu_disasm.txt`), then disassembled them.
4. **Probes.** I re-ran my R853-3 probe unchanged and wrote one new adversarial probe.
5. **Self-test.** I ran the harness self-test at the exact head.
6. **Author evidence.** I checked the author's round-7 packet (archive `28908b90`,
   `review-evidence/sync1115-r1/author-r7`) against round 6's published legs.
7. **Prior findings.** I read the prior review findings only after my own pass.

## Focus checks

### (1) R853-3-F1 closed

I re-ran `probe_owner_build.py` unchanged at the head. The script is byte-identical to the published R853-3 copy,
sha256 `4c03d406...`. Output is in `receipts/probe_owner_build.jsonl`, rc 0.

| Case | Owners | Result at head |
|---|---|---|
| **F** | all four (if0/if1 x MSRP/MVRP) | `late`, row 131.0 ms, and the finding "its owner's first frame or build 130.999 ms after the owner's transmit opportunity at 1300.001 ms, past THE TRANSMIT's 49 ms (late)" |
| **FE** | all four | `late`, 131.0 ms |
| **JF** | all four | `released`, row 1.0 ms |
| **O** (control) | all four | unchanged: `late`, 131.0 |
| **J** (control) | all four | unchanged: `released`, 1.0 |

The cause is removed. In `mrpdu_grade.settle` (`mrpdu_grade.py:235`), a build that `candidate` (`:267`) rejects never
settles the run-out. That covers a build recorded as another participant's and any build before the owner's
opportunity.

### (2) Build record read correctly; no remaining foreign-settle path

**The record itself:**
- `sim_main.cpp:345-346` prints `ENTRY <cycle> build_mrpdu <participant>` at the commit of `build_mrpdu`'s entry.
- `builder_of` (`sim_main.cpp:459`) reads x12 (`a2`). It maps slot 2n to `ifn MSRP` and 2n+1 to `ifn MVRP`, which
  matches `srp_mbx.c:84`'s `slot % 2u ? i->mvrp : i->msrp`. A slot past `n_if` is printed `unresolved`.
- `grade.entry` (`grade.py:174`) parses an `unresolved` record to None, so `builder` (`mrpdu_grade.py:277`) treats it
  as unattributed.
- `observers.OWNER_HOOKS` resolves `build_pc` by exact symbol name. A renamed clone (`.isra`, `.constprop`) would raise
  a KeyError, never a silent mis-read.

**Both measurement shapes, compiled at `544fd72c`** (`--with-aecp --layout split --interfaces 1`; 1x1 =
`endstation_ax7101_1x1_tdm8`, 8x8-1if = `endstation_ax7101_8x8`):
- `build_mrpdu` is a single `noinline` function, `t build_mrpdu`, with no clone in either image.
- Its entry instruction is `addi sp,sp,-32`, which does not write `a2`. `a2` is only copied (`mv s1,a2`, `andi a5,a2,1`)
  until `mrp_transmit`'s argument set-up.
- It has exactly two callers, both plain `jal`; neither is a tail call:
  - `poll` sets `a2 = (owed_if << 1) + (ethertype == MVRP)` just before its call.
  - `transmit` reloads `a2` (the slot) from the stack after `reclaim`.
- `mrp_transmit` has exactly one caller, `build_mrpdu`, so every MRPDU build passes the recorded entry.

The receipt is `receipts/build_mrpdu_disasm.txt`. The author's published regrade
(`regrade-at-544fd72c.json`) agrees across all 13 legs:
- 2,258 builds, all attributed;
- 1,061 frame-bearing builds name their own MRPDU's participant, and 0 disagree.

**The grading** (`mrpdu_grade.py:235-281`):
- Another participant's build only ever sets `past`, so the most it can do is make the run-out late, never released or
  empty.
- An unattributed build settles only through `served`, on frames the commit index attributes to the owner. It never
  takes the `own` empty branch.
- The `own` empty branch is judged against `anchor`, the owner's opportunity, plus `LATE_MS`. The frame branch is
  judged against `since`, the same opportunity.
- The 49 ms bound (`LATE_MS = tx_budget_ms(...)`) is unchanged, as is its IEEE 802.1Q-2018 10.7.4.1 reading.

I wrote a new adversarial probe (`probe_build_record.py`; `receipts/probe_build_record.jsonl`, rc 0, 0 mismatches). It
ran 24 cases, all as expected, for all four owners:

| Case | Arrangement | Result |
|---|---|---|
| RE | the other participant's *recorded* empty build within the bound, the owner's MRPDU at 131 ms | `late` |
| RA | the same recorded empty build, no owner MRPDU, the log runs on | `absent` |
| UR | an `unresolved` slot's empty build within the bound | `late` |
| PB | the owner's own empty build before its opportunity, only another participant's build past the bound | `late`, resting on the `bound` |
| UF (control) | an unattributed build followed in its run by the owner's MRPDU | `released`, row 12 ms |
| OF (control) | the other's MRPDU and the owner's in one run | `released`, row 12 ms |

I found no path where another participant's build settles the owner's deadline.

### (3) Mutants, self-test and fixture move

**Self-test at the head:** `run.py --self-test` rc 0, "self-test: 0 failures", 885 `PASS:` checks, 269 `MUTANT caught`,
0 escaped (`receipts/selftest.log`, `receipts/selftest.rc`). The four new mutants (`selftest_mutants.py:890-898`) are
each caught by the check the README table names:
- "a build's recorded participant ignored..." and "settled by the first build after it, whichever participant's" are
  both caught by `foreign_checks`. Its case `shared` (`selftest_leaveall.py:330`) is the owner's empty build with
  another's MRPDU in its run.
- "a build with no participant recorded that sends nothing taken for the owner's" is caught by `builder_checks`
  `unattributed`, which shows `empty` for every owner under the mutant.
- "the owner's own build before its transmit opportunity settling its run-out" is caught by `builder_checks` `early`.

The README rows changed in `544fd72c` also match the self-test output: the LeaveAll interfaces mutant is now caught by
the join-interval check, and the anchor mutant by the anchor check.

**The fixture move** (`selftest_polls.py:280-294`) matches the firmware:
- `build_mrpdu` arms the join timer at the build (`srp_mbx.c:1095`, `join_left[slot] = SRP_JOIN_CS`).
  `CTRL_LOOP_JOIN_CS` is 19 cs (`ctrl_loop.h:342`). So `on_join_timer` cannot run before the build plus 190 ms.
- At `9aa55d3b` the fixture's join callbacks (1,171, 1,170 and 1,050 ms) ran before the expiry of the join timer their
  owner's build at about 1,000 ms had armed. No firmware can do that.
- At the head, the first build is at 989 ms, so its timer runs out at 1,179. The callbacks are at 1,180, 1,179 and
  1,190, each at or after its owner's expiry, with the build after the callback.
- The interval checks still judge commit to commit (181.0/239.0 inclusive, 180 and 240 named). The new rule only makes
  early builds stricter, so the move hides no escape.

### (4) Re-simulated legs and images

**Tables** (`receipts/tables_r6_vs_r7.txt`): all 13 round-7 `table.md` files are byte-identical to round 6's
`legs-at-9aa55d3b`. Every `regrade.rc` and `run.rc` equals round 6's: `v1` 0, every 8x8/1if leg 1. Across the 13
`regrade.log`s, the only failing lines are the `STATED` pass-cost lines (build-one pass, polls base, tier-2 slice),
which are #914's. No run-out line fails.

**Run-out moves** (`receipts/moves_summary.txt`): diffing round 6 and round 7 `results.json` gives exactly 27 moves,
all `empty -> released`, all periodic.
- Round 6 settled each on an `if0 MSRP` build before the opportunity: 15 owned by `if0 MSRP` and 12 by `if0 MVRP`. The
  closest of those builds was 9.474 ms before the opportunity, and none carried the owner's frame.
- Round 7 settles each on the owner's own recorded build, 0.260 to 1.475 ms after the opportunity. Its frame commits
  within 1.661 ms.
- 815 run-outs are graded empty; the latest owner empty build is 1.955 ms after the opportunity.

**Traces:** the line-for-line identity with round 4's traces once the build participant is removed is the author's
claim. It appears in `regrade-at-544fd72c.md` with each trace's line count. The traces themselves are not published, so
I could not re-check it (see Limits).

**Images:** the delta changes no file under `sw/`, `hdl/`, `configs/` or `gateware/`. The author's
`image-identity-at-38d89bb0.json` records the `ctrl_app.elf` of all 13 legs as byte-identical to round 4's, and 0
unexplained differences. Only `budget_config.hpp` and `native/Vsim` differ, both testbench files.

**Docs:**
- FR_NFR.md:388 matches `settle` (see SUG-1 on one shorthand).
- README.md:147-152 describes the build-association rule, `:160` the record, and `:174-175` what is proven, with
  R853-3-RES-1's fix.
- The mutant table at `:1388-1398` matches the self-test.
- I found no new lane label, review round, reviewer ID or issue-comment ID in any source comment of the delta. README
  links to review comments are allowed in documentation.

## Prior public findings: disposition at this head

My independent pass over the delta, both probes and the self-test were complete before I read the R853-3 and R854-3
findings.

| Finding | Severity | Status at `544fd72c` |
|---|---|---|
| R853-3-F1 (owned run-out settled by whichever participant built first) | MAJOR, Conformance / Robustness / Tests / Docs | **CLOSED at cause.** `settle`/`candidate` reject foreign and pre-opportunity builds (`mrpdu_grade.py:235-281`). Case F is late for all four owners at 1,300.001 ms with its 131 ms row, FE late, JF released, O/J unchanged. Standing controls are `builder_checks` (`selftest_leaveall.py:361`) and `foreign_checks` `shared`, with four mutants caught by name. FR_NFR 3.4.1 and the README state the rule. |
| R853-3-RES-1 (README "late or absent build" omits unowned) | RESIDUE, Docs | **RESOLVED.** README.md:175 reads "or a late, absent or unowned run-out, prints `STATED`". |
| R853-3-SUG-1 (anchor mutant first caught elsewhere) | SUGGESTION, Tests | **RESOLVED.** At this head the anchor mutant is caught by the anchor check itself (`receipts/selftest.log:4490`), and its README row names that check. |
| R854-3 | POSITIVE at `9aa55d3b`, no findings | Nothing to carry. |

## Findings

### R853-4-RES-1 - RESIDUE - Docs

- **Artifact:** REVIEW READY (#665 issuecomment-6950748861), the line "27 of the 1,871 MRP run-outs move". The same
  wording appears in the round-7 handoff (`author-r7/HANDOFF-r7.md:109`).
- **Evidence:** both say round 6 "settled each on an if0 MSRP build at least 9.5 ms before the owner's opportunity". The
  author's own `regrade-at-544fd72c.json` records the closest as 9.474 ms before it
  (`round6_settled_by.build_after_opportunity_ms` maximum -9.474; `receipts/moves_summary.txt`).
- **Impact:** none on any measurement, table, test or verdict. The published JSON and tables are correct, and the
  statement is not in the repository or the PR body.
- **Exact fix:** "at least 9.47 ms before the owner's opportunity".

### R853-4-SUG-1 - SUGGESTION - Docs

- **Artifact:** `docs/reference/FR_NFR.md:388` and `tb/verilator/ctrl_service_budget/README.md:174`.
- **Evidence:** both say "the first build that can be the owner's after it settles it". In `settle`, an unattributed
  build that commits none of the owner's frames does not settle the run-out; the next candidate is taken. The following
  sentence in each document states that exactly, so the paragraph as a whole is accurate. The shorthand alone reads as
  if the first candidate ends the search.
- **Optional wording:** "the first build after it that settles it, the owner's recorded build or one with no participant
  recorded that commits the owner's frame, does so within 49 ms of it".

### R853-4-SUG-2 - SUGGESTION - Tests, RTL

- **Artifact:** `mrpdu_grade.py` / `run.py`. The build-record agreement is not a standing gate.
- **Evidence:** the agreement that every frame-bearing build names its own MRPDU's participant (1,061 / 0) is the
  author's one-off regrade analysis. The run does not check it. A future compiler or convention change that kept the
  symbol name but moved the slot would make the record lie on empty builds, where no frame can expose it. Today
  `noinline` and the ILP32 argument convention prevent that, as the disassembly shows.
- **Optional change:** fail the run, `STATED`, where a frame-bearing build's recorded participant differs from its
  frame's EtherType participant, or where any build records `unresolved`.

### R853-4-SUG-3 - SUGGESTION - Conformance, Robustness

- **Artifact:** `mrpdu_grade.py:156` (`opportunity`, untouched by the delta).
- **Evidence:** the arming build is still the latest build of *any* participant at or before the owner's last commit.
  With builds now attributed, it could be the owner's own recorded build. Using another participant's later build would
  shift the owner's deadline later by the gap.
- **Why this is not reachable today:** `transmit` stops building once a build leaves a frame owed
  (`srp_mbx.c:1251`, `!m->owed_len`), and the poll's rebuild is the same participant. So no other participant's build
  falls between an owner's build and its commit in this firmware.
- **Optional change:** take the owner's own recorded build, falling back to the current rule for unattributed logs.

## Reviewer-owned completion ledger (this delta)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `mrpdu_grade.py:235-281` against IEEE 802.1Q-2018 10.7.4.1 (owner's opportunity, 49 ms `LATE_MS` unchanged); `srp_mbx.c:82-85,1091-1099,1215,1251-1262`; `probe_owner_build.py` and `probe_build_record.py` results | R853-4 | `544fd72cefbd27379ae756c6ce02ae8b7ba15f2c` |
| RTL | CLEAN | `sim_main.cpp:340-346,456-465` (`builder_of`, x12 = `a2`, `n_if` bound, `unresolved`); `observers.py:28-30`; both compiled split images' `build_mrpdu` entry and call sites (`receipts/build_mrpdu_disasm.txt`); no product RTL or firmware in the delta | R853-4 | `544fd72c...` |
| Robustness | CLEAN | `candidate`/`builder` handling of other, unattributed and `unresolved` builds, pre-opportunity builds, a log ending inside the bound (unresolved) or past it (absent/late); probe cases RE/RA/UR/PB/UF/OF x 4 owners | R853-4 | `544fd72c...` |
| Tests | CLEAN | `selftest_leaveall.py:311-399` (`foreign_checks` `shared`, `builder_checks`); `selftest_mutants.py:890-898`; `selftest_polls.py:256-294` fixture move against `srp_mbx.c:1095`, `ctrl_loop.h:342`; self-test rc 0, 885 / 269 / 0 escaped; the 13 legs' tables and rcs against round 6 | R853-4 | `544fd72c...` |
| Docs | CLEAN | `docs/reference/FR_NFR.md:388`; `README.md:147-152,160,174-175,1388-1398`; delta source comments checked against the comment rule; REVIEW READY and handoff (RES-1 is issue-comment wording only) | R853-4 | `544fd72c...` |

Lens coverage before this delta is carried from the external POSITIVE at `9aa55d3b` and earlier rounds, as the owner's
round rule directs. This delta changes no artifact outside the harness's grading, record, self-test and the two
documents above.

## Real limits

- **Traces.** The 13 legs' traces are not published, so I could not re-check their line-for-line identity with round 4's
  minus the build record. I verified the tables (byte-identical), rcs, results-JSON diffs and per-move records instead,
  and all agree with the claim.
- **Images.** I compiled both shapes with stand-in runtime archives and no flash map, so my ELF digests differ from the
  legs'. `srp_mbx.c`'s object does not depend on either input. The 13 leg ELFs (seed MACs differ) were not disassembled
  individually; their byte identity with round 4 is the author's receipt.
- **What I did not run:** no leg was re-simulated here, and no Verilator build was done. No hosted, act or manager bank
  was run or inferred. This is source-delta review of the author's published execution evidence.
- **Hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof.
- **Not re-reviewed.** Earlier rounds' code outside this delta.

## Pending manager duties

- Compose and validate the current-dev merge candidate (source base `659d7687`, live dev `e275d795`), builder and
  native banks, including #898 (merged at `cb96336d`), which this head does not contain. Publish those receipts on the
  PR.
- Own hosted and act acceptance at the merge head, and carry R853-4-RES-1 to the residue checklist.
- The #914 `STATED` lines (each 8x8/1if leg exits 1 on them alone) and the out-of-scope #929, #916 and #919 remain as
  the author recorded them.
- Merge only with explicit maintainer authorization.

## Packet

`MANIFEST.sha256` lists every published receipt:
- **Probes:** `probe_owner_build.py` (R853-3's, unchanged) and `probe_build_record.py`. Each is run as
  `python3 -I -B <probe> <checkout>`.
- **Receipts:** under `receipts/`.

R853-4 FINISHED
