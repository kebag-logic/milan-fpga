[R869] POSITIVE - exact head 0d1eb8e4c5821e9431097950882659f2083d96ba

# R869-1: internal cleared-context review of PR #952 (issue #951, #665's ruling of 2026-11-19, item 2)

- Head `0d1eb8e4c5821e9431097950882659f2083d96ba`, tree `d1ec05dff82782f478eaddde89b396c0c070422c`; base the flip train's head `0839453f` (`flip-train-1117`, step 14). Three commits: `e5dee83b` (the constant, tests, plants), `4224df63` (the compile-time refusal, +2 lines in `srp_mbx.c` only), `0d1eb8e4` (docs only: four files).
- Read in order: AGENTS.md, CONTRIBUTING.md (by reference), the issue body, its TAKEN and REVIEW READY comments, #665's ruling (issuecomment-7007273447, item 2), the PR body, `git diff 0839453f..0d1eb8e4` and each commit, then the author packet (`review-evidence/951-r1/author-r1`, archive `af4b3079`), then the exact-head hosted contexts. Prior public review findings on this PR: none. The PR thread holds only the two review-start notices (R869-1, R870-1), and there are no inline comments or review bodies. Nothing is carried forward.
- Verdict: no BLOCKER, MAJOR or MINOR. There are two RESIDUE items (stale wording only) and two SUGGESTIONs. All five lenses are covered clean at this head.

## What was checked, per the brief's focus items

### (1) The constant is derived, the TX term kept, the refusal right
- `sw/firmware/ctrl/srp/srp_mbx.c:34` `SRP_LEAVEALL_CS 1000u` is LeaveAllTime, named once. Both configure calls read it (`:526-527`, previously the literal `1000`). `:37` defines `SRP_LEAVEALL_LONGEST_CS` as `SRP_LEAVEALL_CS + SRP_LEAVEALL_CS / 2u` (1500 cs), and `:44` defines `SRP_REDECLARE_CS` as `2u * SRP_LEAVEALL_LONGEST_CS + SRP_JOIN_CS + (CTRL_LOOP_TX_MS + 9u) / 10u`. No literal mirrors the result.
- The values follow from `ctrl_loop.h:450` (`CTRL_LOOP_JOIN_CS` 19) and the per-shape `CTRL_LOOP_TX_MS` (`:360` 35, `:369` 77, `:378`/`:387` 105): 3000+19+4 = **3,023 cs** at 1x1/1if, 3000+19+8 = **3,027** at 8x8/1if, and 3000+19+11 = **3,030** at two interfaces. That is about 30.2 s at one interface, as the ruling asks. The per-shape TX term and the JoinTime term are unchanged.
- This participant's own LeaveAll draw is at most `leaveall_cs + 1 + (leaveall_cs/2 - 2)` = 1,499 cs (`third_party/lwSRP/src/core/mrp_mad.c:776`), so 1,500 cs covers it.
- 35.2.2.8's least, two LeaveAllTime periods (2,000 cs), is still met with margin.
- Compile-time refusal (`srp_mbx.c:46`): `SRP_REDECLARE_CS < 1ul << 8u * sizeof held_cs[0]`. Precedence is right (`8u*sizeof` binds first, then the shift, then `<`). `held_cs` is `uint16_t` (`srp_mbx.h:167`). The counter is loaded with exactly `SRP_REDECLARE_CS` (`:355`) and decremented once per centisecond (`:145`), so the strict `<` is the right bound. The probe below confirms that 65,535 compiles and 65,536 is refused, on RV32IM and on the host compiler, and that a LeaveAllTime of 30,000 cs is refused by the assertion's words (`receipts/static-assert-probe.txt`).

### (2) Talker tests, mutants and docs restated; a test fails on the old value
- `srp_talker.cpp:57-59` states the horizon from the clauses: `kLeaveAllTimeMs` 10,000 and 2 x (10,000 + 5,000). These are not the firmware's names, so the tests are independent of the constant's spelling. The two hold-off tests are renamed (`:294`, `:340`), the re-allocation wait is derived (`kHoldOffMs + 1000`), and `DestinationChangeWhileValidWithdrawsTheOld` (`:370`) and `ResetKeepsAnUnchangedSourceAndHoldsAMovedOne` (`:465`) are restated.
- `srp_gate.hpp:318-345`: the composed conflict test holds the source at 29 s and declares it by 31 s.
- `srp_talker_mutants.py:73-75, 139-158`: two new plants put back 2 x LeaveAllTime. One is caught by `ChangedDestinationWaitsTwoLongestLeaveAllPeriods`, the other by the composed `SrpGate.F895ARangeLost...`. The one-LeaveAll and drop-a-term plants are restated. In `srp_mutants.py:87/421/454` the three LeaveTime plants' match text names `SRP_LEAVEALL_CS`, with the same 500 to 400 edit.
- The reviewer's own probes (`scripts/holdoff_probes.py`, `receipts/probes/holdoff-probes-summary.txt`) cover srp_talker at 1x1/1if and 8x8/2if, SrpGate at 8x8/2if, and srp_mbx at 1x1/1if:
  - control (unmodified): every arm passes (16/16, 16/16, 9/9, 84/84).
  - **old value, 2 x LeaveAllTime**: four Talker tests fail by name at both points (`ChangedDestinationWaitsTwoLongestLeaveAllPeriods`, `...AfterTheLatestLeave`, `DestinationChangeWhileValidWithdrawsTheOld`, `ResetKeepsAnUnchangedSourceAndHoldsAMovedOne`), and so does `SrpGate.F895ARangeLostWithdrawsAndTheNewRangeWaitsTheHoldOff`.
  - longest period 1 cs short (20 ms less hold-off): `...AfterTheLatestLeave` fails at both points. Its margin over 30,000 ms is about 5 ms: at 1x1/1if the Leave leaves at most 190 + 35 ms after the request and the hold-off is 30,230 ms.
  - hold-off 1 s too long: the same four Talker tests and the SrpGate test fail, so the upper side is held too.
  - LeaveAllTime 1100 cs (configuration and hold-off together): the four Talker tests and SrpGate fail.
  - `SRP_LEAVEALL_CS * 3u / 2u` (an equivalent spelling) and a mirrored literal `3000u` both pass. The tests hold the value, not the text. The derivation itself is pinned by the plant table: `REDECLARE` (`srp_talker_mutants.py:73`) must match exactly one site, so a literal would make the campaign refuse.
- Docs: see the Docs lens and RES-1/RES-2.

### (3) Image diff limited to the value; release image byte-identical
- Independent object compare (`scripts/object_compare.py`, `receipts/object-compare.txt`): `srp_mbx.c` compiled at base (`git archive 0839453f`) and head with the gate's `SPLIT_RV32_FLAGS` (rv32im, -Os) at 1x1/1if, 8x8/1if, 1x1/2if and 8x8/2if, with branch targets named by label. At every shape exactly three lines differ: `li a3,2023|2027|2030` becomes `lui a3,0x1; addi a3,a3,-1073|-1069|-1066` (4096-1073 = 3023, 4096-1069 = 3027, 4096-1066 = 3030). The only sized symbol that changes is `declare_sources`, by +4 bytes.
- The author's 20 image pairs (`receipts/images/SUMMARY.txt`) agree: one differing linked input (`srp_mbx.o`), relinks with kept relocations equal to the built images, and 3 differing canonical listing lines each. The reviewer did not relink images (limit below).
- Release image: in the author's `release-base.sha256` against `release-head.sha256`, only the raw `alinx_ax7101.v` and the raw `libmilan_baremetal.a` differ. Their "outside its // comment lines" and "member milan_baremetal.o" hashes are equal, and `bios.bin`, `bios.elf`, its disassembly and the ROM, RAM and SRAM init files are equal. `srp_mbx` is not linked in the all-fabric firmware (`git grep srp_mbx sw/litex sw/builder`: no hit).

### (4) CPU rows: carried, with the full re-measure owed at the train's final head
- What the evidence shows. No code path changes; that is shown at object level here and at image level in the author's relinks. The hot code after `declare_sources` fetches 4 bytes later.
- What was measured. The legs the hold-off reaches (`valid-destinations`: `srp-talker`, `srp-talker-loss`, `srp-talker-held`) and arm A's tightest groups were measured on both images at both verdict-bearing one-interface points. 156 probes, no verdict moved, the same seven known `backlog-owed` misses on each image, and no STATED line or share overrun.
- Placement, not value. The largest move is `srp.talker_loss` at 8x8/1if, -7.07 ms of 220. The control image (base value plus one `nop`, i.e. head placement) reproduces the head's rows to the microsecond, which ties the movement to placement. The table graders print the same output on both trees.
- Judgement: this suffices for the rows to carry at this step. The change cannot alter any path's instruction count beyond the one extra instruction on the hold-off's store. The movements are phase effects with large margins, and the remaining groups are not on the changed code. It is not a substitute for the train's final-head re-measurement of every row, including 8x8/2if and arm A's unmeasured groups; that stays a manager duty (below).

### (5) Milan v1.2 Table 4.3's +/-0.5 s LeaveAll tolerance
- The ruling fixes the value at two longest periods, 1.5 x LeaveAllTime each, about 30.2 s. The PR implements exactly that and publishes the tolerance question as an open risk (PR body, REVIEW READY).
- The repository's own traceability reads Table 4.3 as "LeaveAllTime 10 to 15 s (+/-0.5 s)" (`docs/traceability/ieee8021q.md` MRP-6), and `tb/verilator/milan_dp` grades LeaveAll at 9.5 to 15.5 s. So a peer at the tolerance's edge makes two periods 31.0 s, against a hold-off of 30.23 to 30.30 s.
- This is a maintainer decision, not a defect of this lane: 35.2.2.8's least is met, and the frozen scope follows the ruling. Recorded as SUG-1.

### (6) Gates
Reviewer runs at the exact head, in this clone, with builds in scratch:
- `test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4 --jobs 4`: PASS, 74 `verdict: PASS`, 0 failures (`receipts/gates/firmware-gate-shard0.txt`, rc 0).
- `--shard 3/4` (the SRP campaigns, both interface counts): PASS. It gave 513 `[ok]`, 0 ESCAPED, and 106 `[ok] talker-` lines (53 plants x 2). Both new plants and every restated hold-off plant are caught at both points (`receipts/gates/firmware-gate-shard3.txt`, rc 0).
- `fw_coverage.py --check --jobs 8`: `firmware coverage: PASS (40 files)`. `srp/srp_mbx.c` is at lines 100.00 % and branches 100.00 % (`receipts/gates/fw-coverage-check.txt`, rc 0).
- A first launch of these runs collided with a duplicate of itself and was discarded whole (killed, scratch wiped). The receipts above come from the single clean relaunch.

From the author's receipts (read, not re-run):
- Shard 1: 825 of 825 caught. Shard 2: PASS. Shards 0 and 3 match the reviewer's counts above.
- `fw_coverage --selftest` and `--check`: PASS. Twin, twin-plants, twin-maps and twin-maps-plants: PASS.
- Docs workflow steps: 104/104 at `0d1eb8e4`, with no tracked file changed after them.
- Both builder legs: PASS at `0d1eb8e4`, each with one NOT RUN arm that the tree itself declares.

Hosted contexts at this head (`receipts/hosted-checks.txt`): none of the firmware contexts ran to completion.
- `elaborate-gates-1` failed in the runner's LiteX environment: the `sbt` call in VexiiRiscv's argument generation, which this change does not involve.
- `docs-check` and the Union jobs failed as cascades of cancelled dependents, and the rest were cancelled by "Fail fast".
- These are not findings about the change; the manager owns hosted and act acceptance.

## Findings

**RES-1 - RESIDUE - Docs - `docs/design/SPLIT_CONTROL_MEMORY.md:2857` - a renamed test is still named by its old name**
- Evidence: the bullet "The term held" names `Talker.ChangedDestinationWaitsTwoLeaveAllTimePeriodsAfterTheLatestLeave`. This PR renamed it to `Talker.ChangedDestinationWaitsTwoLongestLeaveAllPeriodsAfterTheLatestLeave` (`srp_talker.cpp:340`), and `git grep` finds the old name only here. The adjacent bullet `:2855` was given a "Since #951" pointer, but this one was not.
- Impact: a cold reader cannot find the test by the name given. The bullet is #901's historical record, and its figures were true then; no figure, test or claim changes.
- Exact fix: after the old name, add "(renamed `Talker.ChangedDestinationWaitsTwoLongestLeaveAllPeriodsAfterTheLatestLeave` by #951, which holds two of the longest LeaveAll periods, 30,000 ms)".
- Verification: `git grep -n WaitsTwoLeaveAllTimePeriods` returns only that annotated historical line.

**RES-2 - RESIDUE - Docs - `tb/verilator/ctrl_service_budget/talker_notice.py:22-23` (module docstring) - stale rationale left beside a restated sibling**
- Evidence: the docstring reads "The new range waits two LeaveAllTime periods, so no Advertise follows within the group". The PR restated the same sentence in `tb/verilator/ctrl_service_budget/README.md:329` to "two of the longest LeaveAll periods, about 30 s (#951)" but not here.
- Impact: wording only. The conclusion ("no Advertise follows within the group") still holds, more so, and no code, row or grading reads it.
- Exact fix: replace "two LeaveAllTime periods" with "two of the longest LeaveAll periods, about 30 s (#951)".
- Verification: `git grep -n "two LeaveAllTime periods" tb/verilator/ctrl_service_budget` returns nothing.

**SUG-1 - SUGGESTION - Conformance - `sw/firmware/ctrl/srp/srp_mbx.c:35-37`, #665 ruling item 2 - maintainer to confirm the Table 4.3 tolerance reading**
- The comment's "a peer's as well as this participant's" holds under 10.7.4.3 and under the ruling.
- It does not hold for a peer at Table 4.3's +0.5 s edge (2 x 15.5 s = 31.0 s), which is the repository's own reading in MRP-6.
- If the maintainer wants the tolerance covered, that is a new issue. It would make the longest period 1,550 cs and the hold-off about 31.2 s, and would restate the same tests, plants and docs. Otherwise the train record should name the reading as decided. This is not a defect of this lane, which follows the ruling and published the question.

**SUG-2 - SUGGESTION - Docs/process - issue #951, third bullet - the conditional bench measurement**
- "Measure the reference device's delay if a conflict can be provoked" was not done: the lane had no bench access.
- `Closes #951` would close the issue with it unrecorded. The manager should record it as carried to the bench run, or as declined by the maintainer, before the merge closes the issue.

**Note for the manager, not a finding.** The ruling says the 30.2 s hold "matches the release". `docs/design/MAAP_FABRIC.md:307-314` says the all-fabric placement moves a conflicted source to a new Stream ID that is declared without a wait. The PR body states the processor path correctly, but the train record's wording of "the release" may want reconciling.

## Per-lens results (each lens applied at this head)

```text
[R869] PASS Conformance - sw/firmware/ctrl/srp/srp_mbx.c:29-46,355,526-527; sw/firmware/ctrl/loop/ctrl_loop.h:360,369,378,387,450; third_party/lwSRP/src/core/mrp_mad.c:776 - SRP_REDECLARE_CS derived from SRP_LEAVEALL_CS (the configured value, named once) as 2 x 1.5 x LeaveAllTime + JoinTime + ceil(TX/10): 3,023/3,027/3,030 cs, about 30.2 s at one interface, per #665 ruling item 2; 35.2.2.8's 2,000 cs least met; own draw <= 1,499 cs covered (Table 4.3 tolerance: SUG-1, maintainer)
[R869] PASS RTL - no HDL in the diff (git diff --stat 0839453f..0d1eb8e4: 9 files, none HDL); width and overflow of the firmware counter applied instead: srp_mbx.h:167 uint16_t held_cs, srp_mbx.c:145 decrement, :355 load, :46 refusal, exact at 65,535/65,536 on RV32IM and host (receipts/static-assert-probe.txt); object-level diff limited to the immediate's encoding at 4 shapes (receipts/object-compare.txt)
[R869] PASS Robustness - receipts/probes/holdoff-probes-summary.txt; srp_talker.cpp:465 (reset holds a moved source); srp_gate.hpp:318-345 (conflict through the composition) - minimum side (old value, -1 cs) and maximum side (+1 s) both caught, LeaveAllTime change caught, overflow refused at compile time, reset during a hold-off and the conflict path held, at 1x1/1if and 8x8/2if
[R869] PASS Tests - srp_talker.cpp:52-59,294-367,370,465; srp_gate.hpp:318-345; srp_talker_mutants.py:71-75,139-158; srp_mutants.py:87,421,454; receipts/gates/firmware-gate-shard0.txt (74 PASS), firmware-gate-shard3.txt (513 [ok], 0 ESCAPED, 106 talker-), fw-coverage-check.txt (srp_mbx.c 100 %/100 %) - each changed test fails on the old value by name at both points; horizon from clause literals, not firmware names; an equivalent spelling passes; the derivation is pinned by the plant table
[R869] PASS Docs - sw/firmware/ctrl/srp/README.md:222-246,526-531; docs/design/MAILBOX_SPLIT.md:1290-1292; docs/design/SPLIT_CONTROL_MEMORY.md:2855,3003,3171-3186; tb/verilator/ctrl_service_budget/README.md:329; PR body and REVIEW READY - values, terms, images, rows and limits stated and consistent with the code and receipts; the new section's anchor slug resolves; added source comments carry no lane, round, reviewer or comment IDs (grep of added lines); two stale wording sites recorded as RES-1/RES-2 (RESIDUE, they do not unclean the lens)
```

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `srp_mbx.c:29-46,355,526-527`; `ctrl_loop.h` shape figures; lwSRP `mrp_mad.c:776`; #665 ruling item 2; 802.1Q-2018 35.2.2.8, 10.7.4.3 (as cited); the repository's MRP-6 reading of Milan Table 4.3 | R869-1 | `0d1eb8e4c5821e9431097950882659f2083d96ba` |
| RTL | CLEAN | diff stat (no HDL); `srp_mbx.h:167`; `srp_mbx.c:46,145,355`; `receipts/static-assert-probe.txt`; `receipts/object-compare.txt` | R869-1 | `0d1eb8e4c5821e9431097950882659f2083d96ba` |
| Robustness | CLEAN | `receipts/probes/holdoff-probes-summary.txt` (7 probes x 4 arms); the reset and conflict tests | R869-1 | `0d1eb8e4c5821e9431097950882659f2083d96ba` |
| Tests | CLEAN | `srp_talker.cpp`, `srp_gate.hpp`, `srp_talker_mutants.py`, `srp_mutants.py`; gate shards 0 and 3 and `fw_coverage --check` (reviewer runs); the author's shard 1/2, twin, docs-step and builder receipts (read) | R869-1 | `0d1eb8e4c5821e9431097950882659f2083d96ba` |
| Docs | CLEAN (RES-1, RES-2 residue) | `srp/README.md`, `MAILBOX_SPLIT.md`, `SPLIT_CONTROL_MEMORY.md` section 13 and the new section, `ctrl_service_budget/README.md`, the `talker_notice.py` docstring, the PR body, the issue comments | R869-1 | `0d1eb8e4c5821e9431097950882659f2083d96ba` |

## Real limits of this review
- Not re-run by the reviewer:
  - firmware-gate shards 1 and 2 (the control campaign's 825 and the AECP campaign);
  - the twin and its plants;
  - the docs workflow steps and both builder legs;
  - the CPU budget legs, the control image and the table graders;
  - the image links and relinks, and the release export.
  For these the reviewer read the author's receipts in archive `af4b3079`. The image claim was independently confirmed at object level only.
- No hosted firmware context ran to completion at this head (cancellations, and one runner-side `sbt` failure in `elaborate-gates-1`). No act run (not allowed here).
- Physical calibration and the reference device's delay after a conflict: NOT RUN. Field skips are not hardware proof.
- No manager source bank exists at this head, and none is claimed or inferred.
- The clone was restored and verified after every probe (`receipts/restore.txt`): index equals the HEAD tree, there are no tracked or ignored leftovers, and the gitlinks and submodule checkouts are unchanged.

## Pending manager duties
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, against live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`, with the train landing on `dev-soft-core`. Link its receipts on the PR.
- Own hosted and act acceptance: re-run the exact-head contexts. `elaborate-gates-1` failed in the runner's VexiiRiscv `sbt` step, and the firmware contexts were cancelled.
- At the train's final head, re-measure every CPU budget row, including 8x8/2if and arm A's groups not measured here. This lane's subset carries the rows only to that point.
- Obtain the maintainer's reading of Milan Table 4.3's +/-0.5 s tolerance (SUG-1). Record the issue's conditional bench measurement before `Closes #951` takes effect (SUG-2).
- Carry RES-1 and RES-2 to the residue checklist.
- A second, external positive review is still required by the completion bar.

R869-1 FINISHED
