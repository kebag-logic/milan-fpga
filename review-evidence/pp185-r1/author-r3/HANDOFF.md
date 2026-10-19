# [A647] #185 + #186 handoff

Lane: processor branch `185-186-control-unlock`, from main `08ae0013`
(08ae00130f096f241463172c4781885934400ee4). Assignment: processor issue #185, comment
6249574548 (A10): one lane, two commits; round 1b (manager correction on #186, comment
6253571045) adds a third.

Head: `4865184c9ba88dd85aba3fc8036a6b74bcdb7073` (round 2, on PR #196's `b0f6f9c3`).
Round 1 ended at `c8261711`, round 1b at `fcb6b513`, round 1c at `f42c886c`.

| Commit | Subject |
|---|---|
| `198f1b1` | READ_DESCRIPTOR CONTROL: overlay the IDENTIFY current value from the dynamic store (#185) |
| `c826171` | LOCK_ENTITY: the notification a LOCK or UNLOCK causes echoes its flags; the timeout keeps 0 (#186) |
| `fcb6b51` | LOCK_ENTITY: the automatic unlock's notification carries UNLOCK, as the command-driven one does (#186) (round 1b) |
| `a2cf652` | Merge processor main 246cbc22 (#181 notify-queue cut, #184 MSRP Domain) into 185-186-control-unlock (round 1c) |
| `f42c886` | tb/aecp_notify README: the two occupancy controls that also fail section LF after the merge (round 1c) |

`c826171`'s subject records the round-1 instruction; `fcb6b51` reverses its timeout
half, as the correction asks.

Nothing was pushed. No PR was opened.

## Round 3 (evidence only)

Status: done. Head unchanged: `4865184c9ba88dd85aba3fc8036a6b74bcdb7073` (PR #196); no
tracked file changed, so no commit (item 4). Assignment: PR #196 comment 6273649559
(read exactly), answering R668-2-F1 (comment 6273273700, read in full; its
`audit_evidence.py`, sha256 `2cf0bacc…bda0a`, and `evidence-audit.json`, `7e7ceadc…b3a7`,
taken from the archived packet kebag-logic/milan-fpga `ce4c9e37`,
`review-evidence/pp185-r1/reviews/R668-2/`). No RTL, generator, test or bank re-run and
no campaign re-run: every figure below is from the existing round-1c and round-2
records. Receipts under `receipts/round3/`; `receipts/round2/` and `receipts/r1c/` are
kept as they were (`round3/kept-receipts-check.txt`: all 1,475 files of the round-2
index byte-identical, every new file under `round3/`; that index is kept as
`round3/INDEX-round2.md`). REVIEW READY is posted on #185 with the head (Posting).

### The defect and the fix (item 1)

`r1c_failsets.py` (`receipts/round2/scripts/r1c_failsets.py:14`) took every top-level
`*.log` of a campaign's output directory as a mutant, and its closing tally (`:25-36`)
counted every name with equal failure lists at both sides. Goldens and controls pass
with an empty list, so each one entered "mutants fail the same checks". The same glob
found no log at all for name_state (its runs log in subdirectories) and reported 0.

The replacement, `receipts/round3/scripts/r3_failsets.py`, reads the roster from each
campaign's `results.json` (`roster`, `:40-66`) and classifies each record by the name
its driver gives a baseline: `golden-...` (notify, d3, acmp:
`tb/pp_top/notify_mutants.py:893-896`, `tb/pp_top/d3_mutants.py:613-616`,
`tb/pp_top/acmp_mutants.py:410-413`), `control <target>` with no `patch`
(`tb/pp_top/aecp_dispatch_mutants.py:291-297`) and `golden`
(`tb/name_state/mutants.py:135`). It refuses a record whose name disagrees with what it
plants (`named_checks` empty, `patch` absent) and a name listed twice. Failure IDs are
the leading check ID of each failing check, from `failing_checks` or the runs'
`failures`; aecp_dispatch's `results.json` keeps only a count, so its IDs are the
`FAIL:` lines of the log the driver names for that arm, held to that count
(`dispatch_failures`, `:27-38`). Only mutants enter the unchanged / changed / added /
removed totals (`compare`, `:68-74`; a change is a different verdict or failure-ID
multiset); baselines are compared and printed on their own lines, so a baseline-only
comparison gives zero mutants.

### The regenerated comparisons (item 2)

`round3/scripts/r3_compare.sh` ran the script on the same records the kept comparisons
used: round 2 base `b0f6f9c3` and head `acc059a` (all five campaigns), the notify rerun
at the exact head `4865184` (`head-final2`), round 1c base `246cbc22` and head `a2cf652`,
and round-1b head `fcb6b513`. Every input `results.json` and dispatch log is hashed in
`round3/inputs.sha256` (358 files); the 11 that round 2 published (copied, or listed in
`OVER-200KB.sha256` for acmp) match byte for byte (`round3/inputs-check.txt`). The
round-1c and round-1b `results.json` under 200 KB and each dispatch record set's `FAIL:`
lines are in `round3/records/`; acmp's round-1c and round-1b `results.json` (253 KB
each) are over 200 KB, so only their sha256 and size are recorded (`inputs.sha256`).
All 16 comparisons rc 0.

| Comparison (round3/compare/) | Mutants base / head | Unchanged | Changed | Added | Removed | Baselines base / head | Kept figure it supersedes |
|---|---:|---:|---:|---:|---:|---:|---|
| round2/notify-base-vs-head | 125 / 135 | 120 | 5 | 10 | 0 | 15 / 15 | 135 |
| round2/aecp_dispatch-base-vs-head | 63 / 69 | 60 | 3 | 6 | 0 | 4 / 4 | 64 |
| round2/d3-base-vs-head | 110 / 110 | 110 | 0 | 0 | 0 | 6 / 6 | 116 |
| round2/acmp-base-vs-head | 54 / 54 | 54 | 0 | 0 | 0 | 7 / 7 | 61 |
| round2/name_state-base-vs-head | 16 / 16 | 16 | 0 | 0 | 0 | 1 / 1 | 0 |
| round2/notify-base-vs-head-final2 (exact head) | 125 / 135 | 120 | 5 | 10 | 0 | 15 / 15 | (new) |
| round2/notify-head-vs-head-final2 | 135 / 135 | 135 | 0 | 0 | 0 | 15 / 15 | (new) |
| r1c/notify-base-vs-head | 109 / 125 | 107 | 2 | 16 | 0 | 13 / 15 | 120 |
| r1c/aecp_dispatch-base-vs-head | 54 / 63 | 51 | 3 | 9 | 0 | 4 / 4 | 55 |
| r1c/d3-base-vs-head | 110 / 110 | 110 | 0 | 0 | 0 | 6 / 6 | 116 |
| r1c/acmp-base-vs-head | 51 / 51 | 51 | 0 | 0 | 0 | 6 / 6 | 57 |
| r1c/name_state-base-vs-head | 16 / 16 | 16 | 0 | 0 | 0 | 1 / 1 | 0 |
| r1c/notify-r1b-head-vs-r1c-head | 114 / 125 | 114 | 0 | 11 | 0 | 15 / 15 | 129 |
| r1c/aecp_dispatch-r1b-head-vs-r1c-head | 63 / 63 | 63 | 0 | 0 | 0 | 4 / 4 | 67 |
| r1c/d3-r1b-head-vs-r1c-head | 110 / 110 | 110 | 0 | 0 | 0 | 6 / 6 | 116 |
| r1c/acmp-r1b-head-vs-r1c-head | 51 / 51 | 51 | 0 | 0 | 0 | 6 / 6 | 57 |

Every mutant is KILLED and every baseline PASSes with no failing check on both sides of
every comparison. `round3/SUPERSEDES.md` (generated from the files) maps each kept
comparison to the one that supersedes it; the two exact-head notify comparisons are new.

Reconciliation: the partition gives R668-2's numbers exactly, so there is no difference
to explain. `round3/scripts/r3_replay.sh` ran R668-2's `audit_evidence.py` unchanged on
the published round-2 receipts (rc 0, its own assertions of 120 / 60 / 110 included); its
output equals the published `evidence-audit.json`, and `r3_reconcile.py` finds every
figure (mutants at base and head, unchanged, changed and added names, head baselines) of
notify, aecp_dispatch and d3 equal to this comparison's: 0 mismatches
(`round3/reconcile/reconcile.txt`). Beyond the audit's three campaigns, acmp is 54
mutants and 7 goldens (R668-2 noted 54 kills against the kept 61), and name_state 16 and
1. The kept detailed rows were right: `r3_oldrows.py` checks each kept DIFFER / HEAD ONLY
row against the new changed / added mutants and their failure-ID multisets, and all 14
kept comparisons agree. The only extra rows are round 1c notify's two goldens
(`golden-pp_top-aecp-dispatch-only`, `golden-pp_top-arm-queue-only`, new baselines at
`a2cf652`), which the old script listed as HEAD ONLY mutants
(`round3/reconcile/old-rows.txt`).

### Round 3 new checks, planted mutants and failing words

| Check (golden result) | Planted mutant | rc | Failing words |
|---|---|---|---|
| `r3_failsets_selftest.py`, 4 synthetic cases (4 of 4 PASS; the old script says "3 mutants fail the same checks at base and head" on the baseline-only case) | `baselines-counted`: every record a mutant, R668-2-F1 itself | 1 | `FAIL: baseline-only: rc 0, missing ['MUTANTS: 0 unchanged, 0 changed, 0 added, 0 removed', …]`; it prints `MUTANTS: 3 unchanged` |
| same | `changed-ignores-ids`: a change is a verdict change only | 1 | `FAIL: mixed: rc 0, missing ['MUTANTS: 2 unchanged, 1 changed, 1 added, 0 removed', 'CHANGED m2']` |
| same | `dispatch-count-unchecked` | 1 | `FAIL: dispatch count mismatch: rc 0, missing ['1 FAIL: lines, results.json says 2']` |
| same | `plant-disagreement-ignored` | 1 | `FAIL: name/plant disagreement: rc 0, missing ['name and named_checks disagree on baseline']` |
| `r3_reconcile.py` (rc 0, 0 mismatches) | the notify comparison carrying the old 135 | 1 | `\| notify \| unchanged mutants \| 120 \| 135 \| MISMATCH \|` |
| same | a replayed audit that differs from the published one (d3 goldens 7) | 1 | `MISMATCH: the audit replayed on these records equals the published audit` |
| input-hash check in `r3_compare.sh` (rc 0, 0 mismatches) | one listed digest altered | 1 | `MISMATCH round2/base/notify/results.json = receipts/round2/base/campaigns/out/notify/results.json (copied)` |
| `r3_oldrows.py` (rc 0, 0 disagreements) | one failure ID dropped from a kept DIFFER row | 1 | `DISAGREE round2/compare/failsets-aecp_dispatch-base-vs-head.txt: … failure IDs differ` |
| `r3_kept_check.py` (rc 0) | one byte appended to a kept round-2 receipt | 1 | `CHANGED round2/compare/failsets-d3-base-vs-head.txt` |

Logs and rc files: `round3/selftest/`. The planted copies are written by `r3_plant.py`
and `r3_plant_checks.sh` into scratch, never into the receipts or the tree.

### Prose corrected (item 3)

Every prose total that quoted a kept comparison's figure now gives mutants and baselines
apart, and points at the superseding receipts: the round-2 campaigns table
(aecp_dispatch 67 = 63 + 4 and 73 = 69 + 4 checks, the other 60 mutants identical;
notify the other 120 mutants identical, 15 goldens; acmp 54 and 7; d3 110 and 6;
name_state 16 and 1), the round-2 exact-head notify sentence (150 records = 135 mutants
and 15 goldens), the round-1c notify sentence (114 mutants and 15 goldens common with
round 1b, not 129) and the round-1c campaigns table (aecp_dispatch 51 + 4, all 63
mutants and 4 controls identical to round 1b; notify 107 identical, 13 goldens; acmp 51
and 6; d3 110 and 6; name_state 16 and 1); in PR-BODY, the three aecp_dispatch rows (58,
67 and 73 checks as mutants plus 4 controls) and the two notify rows. The kept campaigns
tables (`round2/compare/campaigns-table.md`, `r1c/compare/campaigns-table.md`) quote
only each campaign's own closing line and log diff, not these totals, so they stand. No
tracked README or doc quotes them (`git grep` and the lane's README and doc additions):
their figures are kill counts and per-mutant rows, which R668-2 found correct.

### Round 3 records

No processor gate, campaign or parent gate ran in round 3 (no bank re-run, as the
assignment says); the base and head records are round 2's, unchanged. Lane tree: HEAD
`4865184c`, `git status --short --ignored` empty. `receipts/INDEX.md` is regenerated from
the files present (`receipts_index.py`).

## Round 2

Status: done. Five commits on `b0f6f9c3`; final head `4865184`. Every processor gate and
all 13 campaigns that build a changed file are rc 0 at base `b0f6f9c3` and at the head,
every difference explained below. Parent consumer gates: 16 of 17 rc 0 at base and
head; gate 11 (`lint_rtl.py --check`) is rc 1 at both, byte-identical, from processor
main `b48312e1` (#190) as merged into the branch before round 2, not from this lane
(parent section). REVIEW READY is posted on #185 with the head (Posting). Base `b0f6f9c3`
(b0f6f9c3b5107c49e2323b9009d3c9b56ade51ad, PR #196's head: round-1c head `f42c886` plus
the manager's merge of main `b48312e1`). Assignment: PR #196 comment 6264668094 (read
exactly), answering R668-1 (comment 6264247031) and R667-1 (comment 6264653909), both
read in full. The reviewers' bench patch and probes were taken from their archived
packets (kebag-logic/milan-fpga `pp185-review-evidence` at `a7fe02aa`:
`R668-1/claim-collision.patch`, `R668-1/probe-claim.py`,
`R667-1/scripts/probe_midround.py`, `R667-1/scripts/probe_rdc.py`). Three commits
on `b0f6f9c3`, then a README-record commit and a bench-structure commit (below); no
rebase, no amend, nothing pushed:

| Commit | Subject |
|---|---|
| `43a7987` | LOCK_ENTITY: every notification carries one cause's flags and locked_id; the expiry waits for a lock job's holder read and a lock change re-latches a running lock round (#186) |
| `4ba8c02` | READ_DESCRIPTOR CONTROL: overlay only a CONTROL whose control_type is IDENTIFY (#185) |
| `acc059a` | Docs: one cause per lock notification and the IDENTIFY-only CONTROL overlay in 06, 00 and 09; the merged notify-campaign total and the round-2 records in tb/pp_top/README |
| `7368215` | tb READMEs: the round-2 head campaigns' records (rd-tail-uncut 17, occupancy_reset_set 32) |
| `4865184` | tb/aecp_notify: the lock-cause checks in functions of under 100 lines, as the parent's C++ idiom gate requires |

Final head: `4865184c9ba88dd85aba3fc8036a6b74bcdb7073`.

### Round 2 item 1 (R668-1-F1, R667-1-F1): one cause per lock notification

Root cause, as the assignment states it: a round's job arguments are latched at the
claim while the lock can change afterwards. Two paths split a notification's flags
(the job's arguments, loaded by the engine with the job) from its `locked_id` (the
holder `E_LOCKUNS` reads afterwards through the rgy face): an expiry on the claim edge
(the claim snapshotted the LOCK's arguments and cleared the pending bit beside the
expiry, so the automatic unlock was lost), and any lock change after the claim (the
round's remaining jobs kept the old arguments). A third, found while designing: an
expiry between a job's load and its holder read.

Mechanism (notify block only; the engine, `gen_ucode.py`, every port and the register
map are unchanged), recorded in 06 §6.8 "One cause per notification" and the PR body:

- `hdl/aecp/KL_aecp_notify.sv:435`: `lk_exp_r`, an owed expiry; reset `:1263`.
- `:956-970`: `lk_due_w` (owed: the strobe while held, or `lk_exp_r`), `lk_defer_w`
  (a LOCK job presented in `N_EMIT_WAIT`, or `N_IDLE` taking a state query),
  `lk_exp_now_w = lk_due_w && !lk_defer_w`, and `lk_on_w`, the lock as an op this cycle
  sees it. `:566-572`: the op outcomes read `lk_on_w`.
- `:1420-1450`: the expiry applies when `lk_exp_now_w` (as before: release, pend,
  UNLOCK, no exclusion, the coalesce count), and when a lock round runs re-latches its
  jobs' arguments to UNLOCK and clears its exclusion (`:1440-1446`); otherwise it waits
  in `lk_exp_r` (`:1448`).
- `:1481`, `:1489`, `:1508-1509`: LOCK and UNLOCK decide on `lk_on_w`; a take
  (`:1496-1505`) or a release (`:1521-1528`) during a lock round re-latches its
  arguments and exclusion to the op's flags and requester.
- `:1540-1543`: in an idle cycle in which the expiry applies, the claim waits a cycle.
- Banner `:135-145` (the one-cause rule) and `:176-185` (the withdrawal paragraph: the
  LOCK job's own holder read also withdraws it; the old text said no unsolicited
  program touches the rgy face, which `E_LOCKUNS` does).

Rejected alternatives: re-reading the flags in the microprogram (the cause's word
exists only in the notify block); aborting the remainder of a round on a change (a job
the engine has loaded would then be retired against the wrong row's sequence id). The
owner-acceptance alternative is refused by the assignment and was not used.

Kept: the LOCK/UNLOCK command-word echo (LF, LN, L5b unchanged and passing) and #181's
queue (`cmdq_nempty_r` lines untouched; CQ and OC1 in every run).

### Round 2 item 2 (R667-1-F2): the CONTROL overlay restricted to the IDENTIFY CONTROL

`identify_index_i` is not an engine input, and wiring it in would edit
`hdl/top/protocol_processor_top.sv`, outside the round's scope, so the test is the
`control_type` one (IEEE 1722.1-2021 Table 7-98, as model rule L8 applies it), inside
the engine's microprogram:

- `hdl/aecp/ucode/gen_ucode.py:258`: `E_RDESCID = 656`, in the free 653..671 run.
- `:1331`: E_RDESCCT's one-octet-linear branch goes to `E_RDESCID` (was
  `E_RDESCCT + 17`).
- `:1351-1379`: `E_RDESCID` compares `control_type` @82..@89 with
  90-E0-F0-00-00-00-00-01 as four 16-bit words (the µISA has no 64-bit immediate):
  CHECK_ARG on each, its refusal arm restoring SUCCESS and serving `E_RDESC` whole;
  IDENTIFY branches back to `E_RDESCCT + 17`. Placement assert `:1378`. Comment
  `:1304-1308`. ROM 91 → 92 programs; UPC map 62 constants / 92 entry points.
- `tb/aecp_cmds/decode.json:33`: the ROM digest only (re-recorded with
  `make -C tb/aecp_cmds record`; every decode row is unchanged).

### Round 2 items 3 and 4

- R667-1-F3: `tb/pp_top/README.md:2865-2870` states the merged 125 and its parts (98,
  #181's eleven, #186's sixteen); round 2's ten controls take it to 135 (`:2879`).
- R667-1-R1: `06_aecp_engine.md` §6.8 and compliance row 16 read "on `T-LOCK-UNLOCK`
  expiry".
- R668-1-F2, applied as written: `tb/aecp_notify/sim_main.cpp:398` (no `LF:`, adds
  REQ-AEM-003/REQ-NOT-001); `tb/pp_top/sim_main.cpp:12138` (no RDC/LK labels, adds
  REQ-AEM-006/014), `:12554`, `:12604`, `:12644`; `tb/ucpu/sim_main.cpp:851-861`
  (no `RC:` or `(P12)`, the wire-order phrase, REQ-AEM-006/014);
  `tb/pp_top/notify_mutants.py:33-38`, `:625-630`, `:693-694` (the three phrases,
  REQ-AEM-003/REQ-NOT-001). Verification: a scan of every comment line the PR adds
  (`git diff -U0 b48312e1 4865184`, hdl/tb/scripts, `//`, `//!`, `#`) finds no bench
  label (333 lines, 0 hits; `receipts/round2/labels/`, with the scan at `acc059a`). Assertion strings, control names and
  counts are unchanged, as the item asks.
- R667-1-S1 to S5 are not assigned and were not done.

### Round 2 new checks, planted controls and failing words

Every new check has a planted control that fails it, measured on its own first
(`receipts/round2/newarms/`) and again in the full head campaigns (identical).

**`tb/aecp_notify` section LC** (`tb/aecp_notify/sim_main.cpp:481-532` serves each lock
job as the engine does: arguments at the load edge, then the state query, withdrawn in
its first cycle, taken in the second, answered in the third; `:552-571` grades a frame
list; `:573-722` the cases, in `lock_cause_claim` and `lock_cause_rounds`), 45
checks (15 graded, 30 REGISTERs). Each frame is graded by @24..@35 (flags, `locked_id`,
big-endian), destination and sequence_id against the exact list:

| Check | Case | Frames required |
|---|---|---|
| LC0 | C, X registered; X LOCK 0x00010000, undisturbed (premise; claim 1 cycle after the op) | C (0x00010000, X) |
| LC1 ×8 | the same with the expiry 1 clock before / on / 1 after / 2 after the claim, LOCK words 0 and 0x00010000 | before, on: C (1, 0), X (1, 0). 1 after: C, X (1, 0), then C, X (1, 0). 2 after: C (word, X), X (1, 0), C, X (1, 0) |
| LC2 | expiry between the engine's load of C's job and its holder read | C (0x00010000, X), X (1, 0), C, X (1, 0) |
| LC3 | expiry in the cycle the holder read is taken | as LC2 |
| LC4 | C, D; X LOCK, X UNLOCK 0x80020001; Y LOCK 0x00030000 while C's UNLOCK job waits | C, D (0x00030000, Y), twice; Y holds |
| LC5 | as LC4 with Y registered (row 1) | C (0x00030000, Y) twice; Y never notified |
| LC6 | C, D; X LOCK 0x00010000; X UNLOCK 0x80020001 while C's job waits | C, D (0x80020001, 0), twice |
| LC7 | C, D; X LOCK; expiry while C's job is presented; X LOCK 0x00040000 | C, D (0x00040000, X), twice; X holds |

At `b0f6f9c3` (its notify block in the head tree, `receipts/round2/try/notify-basertl.log`)
12 of the 15 graded checks fail: LC1 on, 1 after and 2 after the claim for both words,
LC2, LC3, LC4 to LC7. On the claim C receives (0x00010000, 0) alone (the R668-1
reproduction); in LC4 C and D receive (0x80020001, Y) (the R667-1 reproduction).

| Control (`notify_mutants.py` `LOCK_CAUSE`) | Planted | Named | Failing checks at head |
|---|---|---|---|
| `lock_claim_beside_expiry` | the claim's wait branch never taken | `LC1:` | 2: LC1 on the claim, both words (`LC1: X's LOCK with flags 0x00000000 expires on its round's claim: each frame one cause, @24..@35 byte-exact, and the automatic unlock (UNLOCK, locked_id 0) reaches C and the former owner X`) |
| `lock_expiry_in_presented_job` | `lk_defer_w` without the presented-LOCK-job term | `LC2:` | 3: LC1 2 after (both), LC2 (`LC2: the lock expires after the engine loads C's job and before it reads the holder: ...`) |
| `lock_expiry_at_holder_read` | `lk_defer_w` without the state-query term | `LC3:` | 4: LC1 2 after (both), LC2, LC3 (`LC3: the lock expires in the cycle the holder read is taken: ...`) |
| `lock_expiry_pending_dropped` | a deferred expiry never kept (`lk_exp_r <= 1` removed): the lost timeout notification | `LC2:`, `LC3:` | 5: LC1 2 after (both), LC2, LC3, LC7 |
| `lock_expiry_round_not_relatched` | the expiry's re-latch removed | `LC1:` | 6: LC1 1 and 2 after (both), LC2, LC3 |
| `lock_expiry_relatch_keeps_exclusion` | that re-latch keeps the exclusion | `LC1:` | 6: as the previous |
| `lock_take_round_not_relatched` | the LOCK's re-latch removed: the mid-round case | `LC4:` | 3: LC4, LC5, LC7 (`LC4: Y locks (flags 0x00030000) while X's UNLOCK round waits on C: no job carries UNLOCK once Y holds the lock; ...`) |
| `lock_take_relatch_keeps_exclusion` | that re-latch keeps the exclusion | `LC5:` | 1: LC5 |
| `lock_release_round_not_relatched` | the UNLOCK's re-latch removed | `LC6:` | 1: LC6 |
| `lock_op_ignores_due_expiry` | `lk_on_w = lk_held_r` | `LC7:` | 1: LC7 |

Existing controls whose anchors moved (same planted behaviour, re-anchored in
`tb/pp_top/notify_mutants.py`): `foreign_unlock_allowed` (`:283`, the `lk_denied_w`
line now reads `lk_on_w`) and `lock_taker_notified` (`TAKE`, `:95`, the take branch's
latch lines with the new re-latch comment after them). Both KILLED with the same checks
as at base. Four section-LF controls now also fail LC checks (`lock_coalesced_timeout_*`
1 → 5, `lock_take_keeps_old_flags` 3 → 10, `lock_release_keeps_old_flags` 1 → 2), and
`occupancy_reset_set` 17 → 32 (every LC graded check: after each warm reset the set
occupancy claims an empty queue entry first). Every base failure is kept.

**`tb/pp_top` RDC7** (`tb/pp_top/sim_main.cpp:12172-12185`, section AX, default and line
builds): the premise that CONTROL 0's `control_type` is IDENTIFY, then READ_DESCRIPTOR
byte-exact as the image whole for `control_type` 0011223344556677, 91e0f00000000001,
90e0f10000000001, 90e0f00000010001 and 90e0f00000000002, then 255 overlaid again with
IDENTIFY restored. **`tb/ucpu` RC3** (`tb/ucpu/sim_main.cpp:902-911`): the program in
isolation on a type off in its last octet, the image whole. RC1's fixture now carries
IDENTIFY at @82..@89 (`:868-869`).

| Arm (`aecp_dispatch_mutants.py`, `aecp-dispatch`) | Planted | Named failing words | Failing checks |
|---|---|---|---|
| `rdc-ctype-any` | E_RDESCCT branches past E_RDESCID: the round-1 program, R667-1 F2's reproduction | `RDC7 CONTROL 0 with control_type 0011223344556677, not IDENTIFY, IDENTIFY 255: its image whole: READ_DESCRIPTOR byte-exact` | 5 (every RDC7 type) |
| `rdc-ctype-w82-nop` | the @82 word's CHECK_ARG a NOP | `RDC7 CONTROL 0 with control_type 91e0f00000000001, ...` | 1 |
| `rdc-ctype-w84-nop` | the @84 word's | `RDC7 ... 90e0f10000000001, ...` | 1 |
| `rdc-ctype-w86-nop` | the @86 word's | `RDC7 ... 90e0f00000010001, ...` | 1 |
| `rdc-ctype-w88-nop` | the @88 word's | `RDC7 ... 90e0f00000000002, ...` | 1 |
| `rdc-ctype-status-kept` | the refusal arm's SET_STATUS a NOP (and its placement assert) | `RDC7 ... 0011223344556677, ...` | 5 |

Patches regenerated because the moved branch is in their context: `rdc-unset-image`
(its +3 shift now also moves E_RDESCID's branch back) and `rdc-vtype-uint8-only`; both
KILLED as before (2 and 1). `rdc-base-no-overlay` and `rdc-unit-shift-8` 7 → 8 and
`rd-tail-uncut` 16 → 17 (RDC7's last, overlaid read). The scratch generator is
`receipts/round2/scripts/r2_mkpatches.py`.

Accepted lengths and refusal cases: READ_DESCRIPTOR's are round 1's table with one new
row, a CONTROL whose `control_type` is not IDENTIFY: SUCCESS, the image whole (the PR
body's table). LOCK_ENTITY's command lengths and answers are unchanged (cdl 28;
SUCCESS, ENTITY_LOCKED, BAD_ARGUMENTS, NOT_SUPPORTED, flags echoed); the notification
table is round 1b's, now guaranteed per frame: a LOCK's word with its holder, an
UNLOCK's word or UNLOCK with 0, including around a round's claim and during a round.

### Round 2 records

Base is `b0f6f9c3`, in the scratch parent's protocol-processor checkout (detached,
ignored products cleaned first). Head is `acc059a` (the three commits), in the lane tree
after `git clean -fdX`. Three streams each, every gate and campaign unpiped in the
foreground of its own detached job with its own log, rc and duration; pinned Verilator
5.050 first on PATH, then sv2v 0.0.12 and Yosys 0.33 (0.66 for the second synthesis
record). The host was shared and loaded (load average 80 to 150), so durations are long.

| Gate | Base b0f6f9c3 | Head acc059a | Comparison |
|---|---|---|---|
| scripts/run_suites.sh | rc 0, 1,030,132 checks, 0 failing (3,828 s) | rc 0, 1,030,205 checks, 0 failing (5,050 s) | 5 lines differ, the round's own: UPC map 91 → 92 entry points (`E_RDESCID`); aecp_notify 86 → 131 (section LC, 45); pp_top 10,608 → 10,634 (RDC7, 13 in each of the default and line builds); ucpu 445 → 447 (RC3); the total (+73) |
| executed REQ-tag check | rc 0, 233 evidence lines | rc 0, 233 | log identical |
| scripts/lint_hdl.sh | rc 0 | rc 0 | byte-identical |
| make check | rc 0 | rc 0 | one line: ids 617 → 623 files (the six new patches) |
| scripts/gen_matrix.py --check | rc 0 (94 rows, 0 untested) | rc 0 | byte-identical |
| syn/yosys/run.sh, Yosys 0.33 (CI pin) | rc 0 (123 s) | rc 0 (214 s) | six memory warnings' all.v line numbers (+32, the notify block's added lines) |
| syn/yosys/run.sh, host Yosys 0.66 | rc 0 | rc 0 | the same six lines |
| tb/elab_guards/guards.py --frontend yosys | rc 0 | rc 0 | identical with source and all.v line numbers masked (the notify guard's inventory line +10) |

Campaigns: all 13 that build a changed file (the round changes the notify block, the
microcode generator and the pp_top, aecp_notify, ucpu and aecp_cmds benches and
records, which every one of the 13 builds or reads, as in round 1). Fresh output
directories outside the trees, TMPDIR in scratch. `receipts/round2/compare/` holds the
table, the sorted masked diffs and the per-mutant failing-check sets; the failing-check
sets there counted the passing goldens and controls as mutants, and are superseded by
`receipts/round3/compare/round2/` (Round 3). The totals below are the corrected ones.

| Campaign | Base b0f6f9c3 | Head acc059a | Comparison |
|---|---|---|---|
| tb/pp_top/aecp_dispatch_mutants.py --jobs 2 | rc 0, 67 checks PASS: 63 mutants KILLED, 4 controls PASS (1,551 s) | rc 0, 73 checks PASS: 69 mutants KILLED, 4 controls PASS (2,512 s) | the 6 `rdc-ctype-*` arms added, each KILLED by name; `rdc-base-no-overlay` 7 → 8, `rdc-unit-shift-8` 7 → 8, `rd-tail-uncut` 16 → 17, each adding RDC7's last read and keeping every base failure; the other 60 mutants identical; the 4 controls PASS at both |
| tb/pp_top/notify_mutants.py --jobs 2 | rc 0, 125 of 125 KILLED, goldens PASS (4,163 s) | rc 0, 135 of 135 KILLED, goldens PASS (5,811 s) | the 10 `LOCK_CAUSE` controls added; the four LF controls and `occupancy_reset_set` (17 → 32) also fail LC checks, every base failure kept; the other 120 mutants identical; the 15 goldens PASS at both |
| tb/aecp_cmds/mutants.py --jobs 2 | rc 0, 17 of 17 detected | rc 0, same | identical |
| tb/pp_top/aecp_mutants.py --jobs 2 | rc 0, 67 checks PASS | rc 0, same | identical |
| tb/pp_top/ctr_mutants.py --jobs 2 | rc 0, 18 checks PASS | rc 0, same | identical |
| tb/pp_top/gsi_mutants.py --jobs 2 | rc 0, 20 detected | rc 0, same | identical |
| tb/pp_top/name_wr_mutant.py | rc 0, decode killed, golden and restored PASS | rc 0, same | identical |
| tb/name_state/mutants.py --jobs 2 | rc 0, 16 KILLED | rc 0, same | identical; the 16 mutants fail the same checks; the golden PASSes at both |
| tb/maap/mutants.py --jobs 2 | rc 0, 32 checks PASS | rc 0, same | identical |
| tb/adp_engine/mutants.py --jobs 2 | rc 0, 62 checks PASS | rc 0, same | identical |
| tb/pp_top/acmp_mutants.py --jobs 2 | rc 0, 54 of 54 KILLED, goldens PASS (5,485 s) | rc 0, same (3,954 s) | identical; the 54 mutants fail the same checks; the 7 goldens PASS at both |
| tb/elab_guards/mutants.py --jobs 2 | rc 0, 160 of 160 killed | rc 0, same | identical (line numbers masked) |
| tb/pp_top/d3_mutants.py --jobs 3 | rc 0, 110 of 110 KILLED, goldens PASS (10,005 s) | rc 0, same (7,163 s) | identical; the 110 mutants fail the same checks; the 6 goldens PASS at both |

The head campaigns moved two README rows, `rd-tail-uncut` (16 → 17) and
`occupancy_reset_set` (17 → 32), so a README-only commit follows them:

| Commit | Subject |
|---|---|
| `7368215` | tb READMEs: the round-2 head campaigns' records (rd-tail-uncut 17, occupancy_reset_set 32) |

Head after it: `73682150dd3a43266c3f1492c5f0536bd28fff11`. `git diff acc059a 7368215` is the two
READMEs alone (+10 -4), which no build, suite or campaign reads (as in round 1c, only
`make check`'s link, ID and figure gates and comments name them). Every processor gate
ran again at `7368215` (below), and the exact-edit anchor check finds 648 edits, 0
failures.

| Gate at final head 7368215 | rc | vs head acc059a |
|---|---|---|
| scripts/run_suites.sh | 0 (1,030,205 checks, 0 failing; 1,848 s) | byte-identical |
| executed REQ-tag check and its evidence | 0 | byte-identical |
| scripts/lint_hdl.sh, make check, scripts/gen_matrix.py --check | 0 | byte-identical |
| syn/yosys/run.sh (0.33 and 0.66), elab guards under Yosys | 0 | byte-identical |

After the gates and `git clean -fdX`, `git status --short --ignored` in the lane is
empty (`receipts/round2/head-final/`).

The parent head pass at `7368215` then failed its gate 1 on this lane's 164-line bench
function (parent section), so one more commit, `4865184`, splits it; its suite output is
byte-identical. At the final head `4865184` every processor gate ran again
(`receipts/round2/head-final2/gates`), each log byte-identical to `acc059a`'s, the
REQ-tag evidence differing only in two aecp_notify source line numbers (+19); and the
notify campaign, the one campaign that builds `tb/aecp_notify`, gave 135 of 135 KILLED,
goldens PASS, all 150 records identical to `acc059a`'s (135 mutants and 15 goldens). The other 12 campaigns build
nothing `7368215` or `4865184` changed, so their `acc059a` records stand. The lane is
clean after `git clean -fdX`.

### Round 2 scratch-parent consumer gates

The scratch parent is the same clone of kebag-logic/milan-fpga at dev
`e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`, with the same two parent patches as round 1c,
committed locally as in round 1c on a new local branch `pp185-a647-r2-scratch` from
`63d7b6d9e`, never pushed:

| Parent commit | Subject |
|---|---|
| `40f12b103` | Scratch: parent-evidence-classification.patch (#180) |
| `63d7b6d9e` | Scratch: parent-adoption-milan_dp-67.patch (#176) |
| `da384f953` | Scratch: protocol-processor at b0f6f9c3 (round-2 base pass) |
| `8f8d9d396` | Scratch: protocol-processor at round-2 head 73682150 (pass stopped at gate 1, below) |
| `700bdd4aa` | Scratch: protocol-processor at round-2 head 4865184c (head pass) |

The patches are verbatim (`git apply --check -R` passes; sha256 76625170…495e and
e142e2e7…66d3). Each pass checked the gitlink committed at its SHA and the submodule
checked out there, with a `rev-parse --show-toplevel` check before every git command;
both trees' ignored products were cleaned first, and `git status --short` in the parent
is empty before and after each pass. The base pass ran after the base processor streams
(they share the submodule checkout).

Two passes were stopped and are kept apart, not counted: the first base pass at gate 17,
which waited on another lane's exclusive Vivado lock (gates 1 to 11 had run; the script
now runs gate 17 last, `parent_gates_r2.sh`), and the first head pass at `7368215`, whose
gate 1 failed on this lane's own code: `check_cpp_idiom.py` "FAIL: long function 1 >
ratchet 0" (the parent's CODE_QUALITY rule, 100 lines), `Harness::lock_cause()` at 164
lines. `4865184` splits it into three functions under 100 lines; its output is
byte-identical (`receipts/round2/try/`), every processor gate at `4865184` is
byte-identical to `acc059a`'s (the REQ-tag evidence moves two aecp_notify source lines
by +19), and the notify campaign, the one campaign that builds that bench, gives 135 of
135 KILLED with all 150 records identical (`receipts/round2/head-final2/`).

| # | Parent consumer gate | Base (b0f6f9c3) | Head (4865184) | Comparison |
|---|---|---|---|---|
| 1 | check_cpp_idiom.py | rc 0 | rc 0 | identical (long function 0 <= 0) |
| 2 | check_py_idiom.py | rc 0 | rc 0 | 259,088 → 259,204 lines (the drivers' +116) |
| 3 | check_rtl_source_lists.py | rc 0 | rc 0 | identical |
| 4 | pp_srcs.py --check --selftest | rc 0 | rc 0 | identical |
| 5 | check_port_contracts.py | rc 0 | rc 0 | identical (protocol-processor 1,765 ports, 111 <= 111 undocumented) |
| 6 | measure_naming.py --check | rc 0 | rc 0 | identical |
| 7 | measure_test_evidence.py --check (#180 patch) | rc 0 | rc 0 | identical |
| 8 | docs_check.py | rc 0 | rc 0 | identical |
| 9 | check_sh_idiom.py | rc 0 | rc 0 | identical |
| 10 | sw/builder/test_builder.py | rc 0 (1,352 s) | rc 0 (1,487 s) | ALL GATES PASS EXCEPT 1 NOT RUN at both (the external build tree, as before); with temp names and numbers masked, identical but for the NVM writer self-test arms' timing-dependent first findings (70 `self-test OK` at both) |
| 11 | lint_rtl.py --check | **rc 1** | **rc 1** | byte-identical: "LINT REGRESSION: hdl/milan has 3 violation(s), ratchet allows 2", three NEW findings in the parent's own files: `KL_pp_shadow.sv:1161` drives `cfg_tspec_max_frame_i`, 128 bits since processor main `b48312e1` (#190, per-source TSpec), with 16; and SYNCASYNCNET at `KL_pp_shadow.sv:257` and `milan_datapath.sv:453`. Present at base `b0f6f9c3`, the manager's merge of `b48312e1`, before any round-2 commit; dev `e9cbb676` has not adopted #190's port. Not fixed here: it is a parent change outside this lane |
| 12 | make -C tb/verilator/pp_shadow | rc 0 | rc 0 | RESULT: PASS; 2,188 PASS/FAIL lines identical as sorted; `ucode.hex` 91 → 92 programs; nothing else with numbers masked |
| 13 | nvm_cosim lint | rc 0 | rc 0 | Verilator walltimes only |
| 14 | nvm_cosim quick | rc 0 | rc 0 | identical |
| 15 | make -C tb/verilator/milan_dp SIM_JOBS=2 | rc 0 (1,698 s) | rc 0 (1,753 s) | 13 RESULT: PASS; 1,187 PASS/FAIL lines identical as sorted; `ucode.hex` 91 → 92; otherwise numbers (timings, sizes) and one build line's order |
| 16 | make -C tb/verilator/milan_dp_render | rc 0 | rc 0 | PASS/FAIL identical as sorted; `ucode.hex` 91 → 92; nothing else with numbers masked |
| 17 | flock $VIVADO_LOCK xvlog_gate.py --check | rc 0 | rc 0 | the pin line only (b0f6f9c3 → 4865184c) |

### Round 2 acceptance

| Assignment item | Met | Where |
|---|---|---|
| 1. One design for R668-1-F1 and R667-1-F1: every LOCK_ENTITY notification carries one cause (a LOCK echo with its holder; an UNLOCK or automatic unlock with 0) | yes | `KL_aecp_notify.sv` (item 1 above); LC0 to LC7; the reviewers' probes pass at the head (`receipts/round2/probes-head/`) |
| ...the final state still delivered, no timeout notification lost, the recipient exclusion correct | yes | LC1 to LC3 and LC7 end with the final state at every controller; `lock_expiry_pending_dropped` is the lost-notification control; LC5 and the two keeps-exclusion controls |
| ...mechanism chosen inside the notify block, recorded in 06 §6.8 and the PR body; owner acceptance refused | yes | 06 §6.8 "One cause per notification"; PR body Round 2; no owner decision used |
| ...LOCK/UNLOCK command-word echo and #181's queue kept | yes | LF, LN, L5b, L6d, TD1 and CQ/OC1 pass; the `cmdq_nempty_r` lines are untouched; the 11 occupancy controls KILLED |
| ...regression: expiry one clock before, on and after the claim, zero and nonzero LOCK words, a registered former owner, byte-exact, no lost timeout notification; planted control KILLED | yes | LC1 (8 checks: before, on, 1 and 2 after, words 0 and 0x00010000, X registered), @24..@35 graded per frame; `lock_claim_beside_expiry` and five more KILLED |
| ...regression: a LOCK by another controller while an UNLOCK round runs, no job carries UNLOCK once its holder is non-zero; planted control KILLED | yes | LC4 (and LC5 with the requester registered); `lock_take_round_not_relatched` KILLED |
| ...RDC/LN/LF/TD/RN and occupancy/router checks still pass | yes | run_suites (pp_top, aecp_notify, event_router), the notify campaign's occupancy controls |
| 2. R667-1-F2: the overlay restricted to the IDENTIFY CONTROL, by `control_type` against Table 7-98 as rule L8 does, inside the engine, no top-level change | yes | `E_RDESCID` in the engine's microprogram; no `hdl/top` change in round 2 |
| ...a suite case with a non-IDENTIFY one-octet linear CONTROL served whole, planted control KILLED; RDC0 to RDC6 pass | yes | RDC7 (and RC3); `rdc-ctype-any` (the F2 reproduction) and five more KILLED |
| 3. R667-1-F3: `tb/pp_top/README.md` states the merged 125 and its parts | yes | `tb/pp_top/README.md:2865-2870` |
| 4. R667-1-R1 and R668-1-F2 applied as written | yes | item 4 above; label scan 0 hits |
| 5. R667-1-S1 to S5 not assigned | not done, as assigned | |
| Round-1 gate list, both campaigns and every campaign building a changed file, at base and head, rc 0 | yes | records above; the final head's gates byte-identical to `acc059a`'s, the notify campaign re-run there |
| Scratch-parent consumer gates at the new head | run; 16 of 17 rc 0 at base and head, gate 11 rc 1 at both | parent table below: the gate 11 findings are identical at base `b0f6f9c3` and the head and come from main `b48312e1` (#190), merged by the manager, not from this lane |
| STOP conditions | none hit | round 2 changes `hdl/aecp/KL_aecp_notify.sv` and `hdl/aecp/ucode/gen_ucode.py` in hdl, plus tests, mutant lists, records and docs; `git diff b0f6f9c3 4865184 -- hdl/top hdl/common hdl/aecp/ucpu_pkg.sv hdl/aecp/KL_aecp_engine.sv` is empty; no register-map, top-level port or parameter change |
| Receipts under `receipts/round2/`, index regenerated from the files present | yes | `receipts/INDEX.md` |
| No push, no TAKEN again; REVIEW READY with the new head on #185 | yes | Posting below |

## Round 1c

Status: done. Head is `f42c886` (merge `a2cf652` and one README-record commit) on main
`246cbc22`. Every processor gate and all 13 campaigns are rc 0 at the merged base and
at the head. All 17 parent consumer gates are rc 0 at base and head on a committed local
scratch parent. Every record difference is listed below. REVIEW READY is posted on #185
with the head (see Posting).

Processor main had moved from `08ae0013` to `246cbc22`
(246cbc22df280db8fcc09708882bb40b2e964c0e: #181 notify-queue cut, PR #187; #184 MSRP
Domain, PR #191). `git merge origin/main` conflicted in the five files the round names.
The round-1b head `fcb6b513` was merged with one merge commit (no rebase, no amend):

| Commit | Subject |
|---|---|
| `a2cf652` | Merge processor main 246cbc22 (#181 notify-queue cut, #184 MSRP Domain) into 185-186-control-unlock |

Head: `a2cf652eb3de82a8a186d02e150c093d99c0fbbc` (parents `fcb6b513`, `246cbc22`).
Nothing was pushed, and TAKEN was not posted again.

### Round 1c conflict resolutions (file:line at a2cf652)

Both sides keep their behaviour:

- `hdl/aecp/KL_aecp_notify.sv:842-846`: the emission pick's lock arm keeps the lane's
  `pick_arg1_w = lockf_r[31:16]` / `pick_arg0_w = lockf_r[15:0]`. Its next arm reads
  main's registered occupancy, `else if (cmdq_nempty_r)`, instead of the lane's base
  `cmdq_count_r != 5'd0`. This was the only RTL conflict. Main's other occupancy
  writes merged cleanly and are unchanged: the declaration `:441`, `amap_busy_o`
  `:1179`, reset `:1210`, push `:1314`, claim `:1532`. So are the lane's flags latch:
  `:422-423`, reset `:1233`, the two timeouts latching `LOCKF_UNLOCK_C` `:1400,1405`,
  LOCK/UNLOCK latching `rgy_flags_i` `:1450,1466`.
- `tb/aecp_notify/sim_main.cpp:370-372`: the default run calls the lane's `lock_flags()`
  (section LF), then main's `command_queue()` (CQ), then main's
  `occupancy_held(...)` (OC1) last. LF therefore also runs under the OC1 monitor, which
  samples every clock edge.
- `tb/aecp_notify/README.md:12-17` (the section list names LF and CQ, then OC), `:27`
  (the default build runs LF 6, CQ 8 and OC1), `:38` (86 checks: 57 in the first run, 5
  in FT, 20 in PT/CK/PD/CA, 4 in SC; measured), `:359` section LF and `:389` sections
  CQ and OC, both kept in full.
- `tb/pp_top/notify_mutants.py:30-34` (docstring: #181's occupancy flop, then #186's
  flags), `:637` `LOCK_FLAGS` and `:728` `OCCUPANCY` both kept,
  `:770` `MUTANTS = ... + OCCUPANCY + LOCK_FLAGS`.
- `docs/architecture/09_verification.md:309` "ten of the notification block's" (base
  seven, plus the lane's LF and main's CQ and OC), `:330-332` the LF, CQ and OC rows.

Checks on the merge, before any gate:
- Every main-only file is identical to main. `git diff 246cbc22 a2cf652` is empty for
  `hdl/packet_engine` (the router scan), `hdl/srp`, `syn/ooc`, `tb/srp_*`,
  `tb/aecp_notify/{occupancy.vlt,Makefile,port_tuple.hpp}`.
- Every lane-only file is identical to the lane head. `git diff fcb6b513 a2cf652` is
  empty for the engine, the microcode generator and table, `hdl/top`, the pp_top,
  ucpu and aecp_cmds benches.
- `git diff --stat 246cbc22 a2cf652` has the same 28 files and per-file counts as
  `git diff --stat 08ae0013 fcb6b513`, except `tb/aecp_notify/README.md` (+34 → +40,
  the count lines).
- Every exact-edit anchor of the 16 campaign drivers and every mutation patch applies
  exactly once at `a2cf652` (622 edits, 0 failures).
- No generated record needed re-recording. Main changes no file a lane generator reads
  (the engine, `gen_ucode.py`, `aecp_commands.json`), and `make check` and
  `gen_matrix.py --check` pass on the merge.

### Round 1c: the merged notify campaign and the README record

The notify campaign at the merge (`a2cf652`) gives 125 of 125 KILLED, goldens PASS.
Base `246cbc22` gives 109 of 109. Every mutant present at both fails the same checks,
except two of #181's controls. They now also fail LF checks, because LF's SET_NAME
round goes through the command queue whose occupancy they break:

| Control | Base 246cbc22 | Head a2cf652 |
|---|---|---|
| `occupancy_push_unseen` | 7: DR2, DR2b, CQ1, CQ1b, CQ2, CQ2b, OC1 | 9: DR2, DR2b, **LF2, LF3**, CQ1, CQ1b, CQ2, CQ2b, OC1 |
| `occupancy_reset_set` | 14: TS1 ... DR3, CQ1 ... OC1 | 17: the same plus **LF1, LF2, LF3** |

Their named checks (OC1, CQ...) are among those failures, so both are still KILLED. The
16 lock controls fail exactly the checks they failed at round-1b head `fcb6b513`
(the 114 mutants and 15 goldens common to both runs are identical; corrected in round 3,
the round-1c comparison had counted the goldens as mutants, 129). The two
`tb/aecp_notify/README.md` mutation rows are corrected, with one sentence on why
(`tb/aecp_notify/README.md:441,445,453-454`), in a README-only commit:

| Commit | Subject |
|---|---|
| `f42c886` | tb/aecp_notify README: the two occupancy controls that also fail section LF after the merge |

Final head: `f42c886c9abf311af64152eda669cbb040460bd1`. `git diff a2cf652 f42c886` is that
README alone (+5 -2). No build, suite or campaign reads it. The only README references
in the Makefiles, drivers and scripts are comments, plus `make check`'s link, ID and
figure gates, and those were rerun at `f42c886`. The 13 campaigns ran on the
`a2cf652` tree. acmp and d3 were still running when the README was committed, and
their private trees copy only `hdl`, `tb/common` and `tb/pp_top`.

### Round 1c records: processor gates

Base is merged main `246cbc22`, in the scratch parent's protocol-processor checkout
(detached, ignored products cleaned first). Head is `a2cf652`, in the lane tree after
`git clean -fdX`. Both ran at the same time, each gate unpiped in the foreground of its
own detached job, with its own log, rc and duration. Pinned Verilator 5.050 came first
on PATH, then sv2v 0.0.12 and Yosys 0.33. The final head `f42c886` reran every gate
on a cleaned lane tree (table below).

| Gate | Base 246cbc22 | Head a2cf652 | Comparison |
|---|---|---|---|
| scripts/run_suites.sh | rc 0, 1,030,029 checks, 0 failing (3,146 s) | rc 0, 1,030,123 checks, 0 failing (3,098 s) | 5 lines differ, the lane's own deltas as in rounds 1 and 1b: UPC map 61 → 62 constants / 90 → 91 entry points; aecp_notify 80 → 86 (LF); pp_top 10,519 → 10,599 (RDC, LN); ucpu 437 → 445 (RC, L3/L3b); the total (+94) |
| executed REQ-tag check | rc 0, 233 evidence lines | rc 0, 233 | log identical; evidence identical as sorted with source lines masked |
| scripts/lint_hdl.sh | rc 0 | rc 0 | identical |
| make check | rc 0 | rc 0 | links 1202 → 1204, aecp entries 84 → 85, ids 608 → 617 files: the lane's deltas, as in round 1 |
| scripts/gen_matrix.py --check | rc 0 (94 rows, 0 untested) | rc 0 | identical |
| syn/yosys/run.sh, Yosys 0.33 (CI pin) | rc 0 (125 s) | rc 0 (126 s) | identical with all.v line numbers masked (six memory warnings) |
| syn/yosys/run.sh, host Yosys 0.66 | rc 0 | rc 0 | the same |
| tb/elab_guards/guards.py --frontend yosys | rc 0 | rc 0 | identical with source and all.v line numbers masked |

### Round 1c records: campaigns

These are all 13 campaigns that build a changed file, as in rounds 1 and 1b (the merge
changes no other file of the lane's set). Each ran with a fresh output directory
outside the trees and TMPDIR in scratch. Base ran in the submodule at `246cbc22` and
head in the lane at `a2cf652`, two streams each. `receipts/r1c/compare/` holds the
table, the sorted masked diffs and the per-mutant failing-check sets; the failing-check
sets there counted the passing goldens and controls as mutants, and are superseded by
`receipts/round3/compare/r1c/` (Round 3). The totals below are the corrected ones.

| Campaign | Base 246cbc22 | Head a2cf652 | Comparison |
|---|---|---|---|
| tb/pp_top/aecp_dispatch_mutants.py --jobs 2 | rc 0, 58 checks PASS: 54 mutants KILLED, 4 controls PASS (1,591 s) | rc 0, 67 checks PASS: 63 mutants KILLED, 4 controls PASS (1,732 s) | the 9 `rdc-*` arms added, each KILLED by name. `lk-sctrl-lock-nop` 12 → 13, `rd-tail-uncut` 9 → 16, `rd-str-short-guard-nop` 1 → 6 (README rows as recorded since round 1). The other 51 mutants fail the same checks; the 4 controls PASS at both. All 63 mutants and 4 controls are identical to round-1b head |
| tb/pp_top/notify_mutants.py --jobs 2 | rc 0, 109 of 109 KILLED, goldens PASS (2,217 s) | rc 0, 125 of 125 KILLED, goldens PASS (3,289 s) | the 16 lock controls and their 2 goldens added. 107 mutants identical; the 13 base goldens PASS at both. `occupancy_push_unseen` 7 → 9 and `occupancy_reset_set` 14 → 17 (above). All 16 lock controls identical to round-1b head |
| tb/aecp_cmds/mutants.py --jobs 2 | rc 0, 17 of 17 detected | rc 0, same | identical |
| tb/pp_top/aecp_mutants.py --jobs 2 | rc 0, 67 checks PASS | rc 0, same | one line: `td-lock-default-59s` still fails TD1, whose message names flags UNLOCK (as round 1b) |
| tb/pp_top/ctr_mutants.py --jobs 2 | rc 0, 18 checks PASS | rc 0, same | identical |
| tb/pp_top/gsi_mutants.py --jobs 2 | rc 0, 20 detected | rc 0, same | identical |
| tb/pp_top/name_wr_mutant.py | rc 0, decode killed, golden and restored PASS | rc 0, same | identical |
| tb/name_state/mutants.py --jobs 2 | rc 0, 16 KILLED | rc 0, same | identical as sorted; the 16 mutants fail the same checks; the golden PASSes at both |
| tb/maap/mutants.py --jobs 2 | rc 0, 32 checks PASS | rc 0, same | identical |
| tb/adp_engine/mutants.py --jobs 2 | rc 0, 62 checks PASS | rc 0, same | identical |
| tb/pp_top/acmp_mutants.py --jobs 2 | rc 0, 51 of 51 KILLED, goldens PASS (2,392 s) | rc 0, same (2,216 s) | identical as sorted; all 51 mutants fail the same checks; the 6 goldens PASS at both |
| tb/elab_guards/mutants.py --jobs 2 | rc 0, 160 of 160 killed | rc 0, same | identical with source and all.v line numbers masked |
| tb/pp_top/d3_mutants.py --jobs 3 | rc 0, 110 of 110 KILLED, goldens PASS (5,084 s) | rc 0, same (5,023 s) | identical as sorted; all 110 mutants fail the same checks; the 6 goldens PASS at both |

Not run, as in rounds 1 and 1b, because they build no file this lane changes:
tb/srp_top and tb/srp_admission mutants (#184 changed their sources, but on main; the
lane changes none of them), tb/acmp_talker/retry_mutants.py, tb/desc_mem_guard/mutate.py,
tb/desc_store's lint mutations and `make -C tb/nvm_port figures`.

### Round 1c records: the final head f42c886

Every processor gate ran again at `f42c886` in the lane tree, after the head campaigns
and `git clean -fdX`. Each log is byte-identical to its `a2cf652` log:
run_suites (rc 0, 1,030,123 checks, 1,882 s), the REQ-tag check and its evidence,
lint_hdl, make check, gen_matrix, syn/yosys/run.sh under 0.33 and 0.66, and the
Yosys elab guards (`receipts/r1c/compare/head-vs-final-head.txt`). The exact-edit anchor
check at `f42c886` finds 622 edits, 0 failures. After the gates and the cleaning,
`git status --short --ignored` is empty.

### Round 1c scratch-parent consumer gates

The scratch parent is the same clone of kebag-logic/milan-fpga at dev
`e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`. This round it is committed, locally, on a
local branch `pp185-a647-r1c-scratch`, and it was never pushed:

| Parent commit | Subject |
|---|---|
| `40f12b103` | Scratch: parent-evidence-classification.patch (#180) |
| `63d7b6d9e` | Scratch: parent-adoption-milan_dp-67.patch (#176) |
| `e418e44bc` | Scratch: protocol-processor at merged main 246cbc22 (base pass) |
| `fbc999ff6` | Scratch: protocol-processor at lane head f42c886c (head pass) |

The two patch commits hold the patches verbatim: `git apply --check -R` of each passes
on the tree, sha256 76625170…495e and e142e2e7…66d3. `git diff --stat e9cbb676 HEAD`
is exactly their two files plus the gitlink. Each pass checked, before running, that
the gitlink was committed at the pass's SHA (`git rev-parse HEAD:protocol-processor`)
and the submodule was checked out there. Every git command was preceded by a
`rev-parse --show-toplevel` check. Both trees' ignored products were cleaned, and
`git status --short` in the parent is empty before and after each pass. The base pass
ran after the base processor streams, since it shares their checkout; the head pass
ran after the base pass.

| # | Parent consumer gate | Base (246cbc22) | Head (f42c886) | Comparison |
|---|---|---|---|---|
| 1 | check_cpp_idiom.py | rc 0 | rc 0 | identical |
| 2 | check_py_idiom.py | rc 0 | rc 0 | 258,874 → 259,068 lines (the lane's +194, as in round 1b) |
| 3 | check_rtl_source_lists.py | rc 0 | rc 0 | identical |
| 4 | pp_srcs.py --check --selftest | rc 0 | rc 0 | identical |
| 5 | check_port_contracts.py | rc 0 | rc 0 | protocol-processor ports 1,763 → 1,765 (`rgy_flags_o`, `rgy_flags_i`, documented); undocumented 111 <= 111 |
| 6 | measure_naming.py --check | rc 0 | rc 0 | the same two ports (3,991 → 3,993 ports); candidates unchanged |
| 7 | measure_test_evidence.py --check (#180 patch) | rc 0 | rc 0 | identical |
| 8 | docs_check.py | rc 0 | rc 0 | identical |
| 9 | check_sh_idiom.py | rc 0 | rc 0 | identical |
| 10 | sw/builder/test_builder.py | rc 0 (1,358 s) | rc 0 (1,442 s) | ALL GATES PASS EXCEPT 1 NOT RUN at both (gate 11's external build tree). With the round-1 masking (the NVM writer self-test arms' timing-dependent finding counts and first findings; all 70 `self-test OK` at both), identical except two temp names |
| 11 | lint_rtl.py --check | rc 0 | rc 0 | identical |
| 12 | make -C tb/verilator/pp_shadow | rc 0 | rc 0 | RESULT: PASS; 2,188 PASS/FAIL lines identical as sorted; `ucode.hex` 90 → 91 programs; parallel-make output order |
| 13 | nvm_cosim lint | rc 0 | rc 0 | Verilator walltimes only |
| 14 | nvm_cosim quick | rc 0 | rc 0 | identical |
| 15 | make -C tb/verilator/milan_dp SIM_JOBS=2 | rc 0 (1,766 s) | rc 0 (1,731 s) | 13 RESULT: PASS; 1,143 PASS/FAIL lines identical as sorted; `ucode.hex` 90 → 91; phase timings, output order; 16 of 360 informational `timestamp` lines moved by a constant 5,120 ns (stamp and phc), residuals identical, as in round 1 |
| 16 | make -C tb/verilator/milan_dp_render | rc 0 | rc 0 | PASS/FAIL identical as sorted; `ucode.hex` 90 → 91; output order |
| 17 | flock $VIVADO_LOCK xvlog_gate.py --check | rc 0, 0 findings | rc 0, 0 findings (3,290 s, most of it waiting on another lane's exclusive lock) | the pin line only (246cbc22 → f42c886c) |

### Round 1c: accepted lengths, refusal cases and new checks

Round 1c changes no behaviour of either side, so the accepted lengths and refusal cases
are those of round 1 (READ_DESCRIPTOR) and the round-1b LOCK_ENTITY notification table
below. Round 1c adds no new check. Its only check-related change is the merge order
LF → CQ → OC1 in `tb/aecp_notify`'s default run. Every check of both sides keeps its
planted mutant, and each mutant is still KILLED by its named check at the head: the 9
`rdc-*` arms, the 16 lock controls, and #181's 11 occupancy controls (named failing
words in rounds 1 and 1b below, and in `tb/aecp_notify/README.md` for #181's).

### Round 1c acceptance

| Item | Met | Where |
|---|---|---|
| Merge origin/main into the branch, one merge commit, no rebase | yes | `a2cf652` (parents `fcb6b513`, `246cbc22`) |
| #181 kept: `cmdq_nempty_r == (count != 0)`, its in-tree checks, the router scan | yes | the pick reads `cmdq_nempty_r` (`KL_aecp_notify.sv:846`); OC1 in every run and CQ pass (86 checks); its 11 controls KILLED; `hdl/packet_engine` identical to main |
| The lane kept: LOCK_ENTITY flags (both unlocks UNLOCK) and the CONTROL overlay | yes | LF, LN, L5b, L6d, TD1, RN, L3/L3b, RDC pass; the 16 lock and 9 `rdc-*` arms KILLED, each record identical to round 1b |
| Generated records only through their generators | yes | none needed re-recording (no generator input changed); the README mutation record follows the campaign |
| Every processor gate at merged base and head, rc 0 | yes | tables above; final head byte-identical to the merge |
| Every campaign building a changed file, base and head, rc 0 | yes | the 13 above |
| Parent consumer gates, committed local scratch parent at dev e9cbb676 with the two patches | yes, 17 of 17 rc 0 at base and head | table above |
| Receipts under the output directory, with an index generated from the files present | yes | `receipts/r1c/`, `receipts/INDEX.md` |
| One-line commit subjects; no push; TAKEN not posted again | yes | |
| STOP conditions | none hit | `git diff fcb6b513 f42c886 -- hdl/top hdl/common hdl/aecp/ucpu_pkg.sv` is empty (main changed none of them either); against main `246cbc22` the only `hdl/top` lines are round 1's internal wire and its two connections (+3); no register-map, top-level port or parameter change |

## Round 1b

Manager correction on #186 (comment 6253571045, read exactly): the round-1 instruction
that the lock-timeout notification keeps flags 0 is withdrawn. Both unlock
notifications, the command-driven one and the automatic one after the one-minute
timeout (Milan v1.2 Table 5.22), carry flags UNLOCK with locked_id 0 (IEEE
1722.1-2021 7.5.2, 7.4.2.1 Table 7-143). I checked the clauses: Table 5.22's
LOCK_ENTITY row says only "Sent when the entity automatically unlocks itself after
the one (1) minute timeout"; Table 7-143 defines bit 31 (value 1) as UNLOCK and bits 0
to 30 as reserved.

New head: `fcb6b5138e17b33a3c51572594a1aa210aa0bef1`, one commit on `c8261711`:

| Commit | Subject |
|---|---|
| `fcb6b51` | LOCK_ENTITY: the automatic unlock's notification carries UNLOCK, as the command-driven one does (#186) |

Nothing was pushed, nothing was rebased or amended, and TAKEN was not posted again.

### Round 1b changes (file:line at fcb6b51)

- `hdl/aecp/KL_aecp_notify.sv:423`: `LOCKF_UNLOCK_C = 32'h0000_0001` (Table 7-143 UNLOCK).
  `:1393` (the timeout coalesced into a pending lock round) and `:1398` (the timeout
  with no round pending) latch `LOCKF_UNLOCK_C` where they latched 0. Comments at
  `:102-105` (banner), `:422`, `:1391`. A LOCK or UNLOCK still latches the command's
  whole word (`:1443`, `:1459`, unchanged), and the reset value stays 0.
- `hdl/aecp/KL_aecp_engine.sv:2971`, `hdl/aecp/ucode/gen_ucode.py:1175-1179`: comments
  only (the job's arguments are UNLOCK for the timeout). The microcode, `ucode.hex` and
  every ROM are unchanged: E_LOCKUNS still emits r14[31:0].
- `hdl/aecp/ucode/aecp_commands.json:69`: the notify doc string, "auto-unlock with flags
  UNLOCK", which renders F06.14's LOCK_ENTITY row (`06_aecp_engine.md:253`).
- `tb/pp_top/sim_main.cpp:12523` (`LN_AUTO_FLAGS = 1`), `:12567`: **LN2** now expects
  flags UNLOCK and locked_id 0 ("LN2 the auto-unlock after that LOCK (Milan Table 5.22)
  carries UNLOCK"). `:5279-5284`: **L6d** (main suite, the 400 ms wrap timeout) expects
  flags 1. Comments at `:12514-12515`.
- `tb/pp_top/notify_phases.hpp:2394`, `:2403-2404`: **TD1** (the sixth build, the top's
  60,000 ms default) expects flags UNLOCK. `:1655`: section **RN**'s independent lock
  model predicts UNLOCK on the automatic unlock's pushes. `:1603`: the same model's
  push after the holder's UNLOCK now predicts the UNLOCK's flags, 1. That line has been
  stale since round 1 (round 1 made the UNLOCK's notification echo its flags but left
  the model at 0). The fixed seed never reaches it: its 7 lock takes end in 6 automatic
  unlocks, and the lock is still held at the end. It is corrected here because it is
  the same "both unlocks carry UNLOCK" contract.
- `tb/aecp_notify/sim_main.cpp:389-391`: **LF2** (a timeout coalesced over a pending
  LOCK) expects job args 0000/0001, flags UNLOCK. Comment at `:332-339`.
- `tb/ucpu/sim_main.cpp:1354-1360`: **L3b** runs E_LOCKUNS with the auto-unlock job's
  r14 = 1 and expects flags UNLOCK, locked_id 0.
- `tb/pp_top/notify_mutants.py:623-633`, `:640-644`, `:662-667`, `:692-697`: LN2's new
  words, the two anchors `LOCKF_TIMEOUT` and `LOCKF_COALESCED`, the earlier two timeout
  controls re-anchored, and three new controls (below).
- Docs: `06_aecp_engine.md:253,806-819,1295` (§6.8's flags paragraph, F06.14, the
  opcode answers); `00_MILAN_COMPLIANCE_REVIEW.md:600` (decision row 16, its evidence
  adds L6d); `09_verification.md:330` (the LF row); `tb/pp_top/README.md` (TD1 at
  `:915`, LN at `:2326-2331`, RN at `:2573`, the #186 paragraph at `:2813` and its
  rows at `:2924-2937`); `tb/aecp_notify/README.md:360,370,378,382`;
  `tb/ucpu/README.md:80`.

### Round 1b: the LOCK_ENTITY notification table (coalesced changes included)

This supersedes the round-1 table under "Accepted lengths and refusal cases" below.
Command lengths and answers are unchanged from base (cdl 28; SUCCESS / ENTITY_LOCKED /
BAD_ARGUMENTS / NOT_SUPPORTED, flags echoed). The unsolicited LOCK_ENTITY goes to every
registered controller except the requester (an automatic unlock excludes nobody):

| Cause | Notification flags @24..@27 | locked_id | Round 1 (c826171) |
|---|---|---|---|
| a LOCK that took the lock | the LOCK's whole flags word (reserved bits included) | the new holder | same |
| an UNLOCK that released it | the UNLOCK's whole flags word (UNLOCK = 1, reserved bits included) | 0 | same |
| the lock timeout, no round pending (Milan Table 5.22 automatic unlock) | **UNLOCK (0x00000001)** | 0 | 0 |
| the lock timeout coalesced into a pending lock round | **UNLOCK (0x00000001)**, no exclusion | 0 | 0 |
| a LOCK coalesced over a pending timeout round | the LOCK's own word | the holder now | same |
| no change (already-unlocked query, refused LOCK, keep-alive) | no notification (unchanged) | - | same |

### Round 1b checks, planted mutants and failing words

Changed checks: LN2, L6d, TD1, RN (model), LF2, L3b. Each fails when the timeout is
planted back to 0, which is the round-1 behavior and what the qualification observed:

| Check | Planted mutant | Where measured | Failing words |
|---|---|---|---|
| LN2 (section AX, default build) | `lock_timeout_flags_zero`: the no-round timeout latches `32'd0` | notify campaign | `LN2 the auto-unlock after that LOCK (Milan Table 5.22) carries UNLOCK: flags 0x00000001, locked_id 0x0000000000000000, byte-exact` |
| L6d (main suite) | `lock_auto_unlock_flags_zero`: the same edit | notify campaign | `L6d: 60 s auto-unlock notifies (Milan Table 5.22), flags UNLOCK, locked_id 0, seq 3` |
| LF2 (tb/aecp_notify) | `lock_coalesced_timeout_flags_zero`: the coalesced timeout latches `32'd0` | notify campaign | `LF2: X's LOCK with flags 0x00040000 times out before its round leaves: the coalesced notification is the auto-unlock's, flags UNLOCK (job args 0000/0001)` |
| LN2 (line build), RN, TD1, L6d | both timeout latches `32'd0` (hand-planted, `receipts/r1b/hand/`) | `make` in tb/pp_top, then `make aecp-line` and `make timer-defaults` | default build `10057 checks, 3 failures`: L6d, LN2, `RN: ... zero divergence from the independent registry and lock model (6 of 2211 frame comparisons diverged)`; line build `279 checks, 1 failures`: LN2; defaults build `3 checks, 1 failures`: `TD1: T-LOCK-UNLOCK at its default: ... (LOCK_ENTITY, u = 1, flags UNLOCK, locked_id 0) ...` |
| L3b (tb/ucpu) | E_LOCKUNS flags from r12 = 0 (hand-planted) | `make` in tb/ucpu | `445 checks: 443 PASS, 2 FAIL`: `L3 the causing command's flags echoed at @24, got 00000000`, `L3b flags UNLOCK, locked_id 0 (00000000 00000000 00000000)` |

The tree was restored after each hand-planted run and checked clean (`git status`
empty), and `git clean -fdX` ran before the gates.

The notify campaign's lock controls, measured on their own (`--jobs 4 --only`, the 16)
and again in the full campaign, identical: goldens PASS, 16 of 16 KILLED.

| Control | Planted | Failing checks (round 1 → 1b) |
|---|---|---|
| `lock_unlock_notifies_flags_zero` | E_LOCKUNS flags from r12 (the #186 reproduction) | L5b → L5b, L6d |
| `lock_auto_unlock_flags_zero` (new) | the timeout latches 0 | L6d |
| `lock_notification_flags_zero` | the same E_LOCKUNS edit, section AX | LN1, LN4 → LN1, LN2, LN4 |
| `lock_flags_unlock_bit_only` | the latch takes `{31'd0, rgy_op_i[0]}` | LN1, LN4 (same) |
| `lock_timeout_keeps_flags` | the timeout no longer writes the latch (keeps the LOCK's word) | LN2 (same) |
| `lock_timeout_flags_zero` (new) | the timeout latches 0 | LN2 |
| `lock_flags_from_exclusion` | the job's arguments from the exclusion eid | LN1 to LN4 (same 4; LN2's words now "carries UNLOCK") |
| `lock_job_arguments_dropped` | the engine loads a LOCK job like any other | LN1, LN4 → LN1, LN2, LN4 |
| `lock_job_r14_unpacked` | `lockf_w = lockc_r` | LN1, LN4 → LN1, LN2, LN4 |
| `lock_notification_not_sent` | the LOCK job runs UPC_NOSEND_C (premise) | LN1 to LN4 (same) |
| `lock_response_flags_zero` | E_LOCKEN's response flags from r12 (premise) | LN1, LN4 responses (same) |
| `lock_coalesced_timeout_keeps_flags` | the coalesced timeout keeps the LOCK's word | LF2 (same) |
| `lock_coalesced_timeout_flags_zero` (new) | the coalesced timeout latches 0 | LF2 |
| `lock_take_keeps_old_flags` | a LOCK latches nothing | LF1, LF3 → LF1, LF3a, LF3 |
| `lock_release_keeps_old_flags` | an UNLOCK latches nothing | LF1b (same) |
| `register_refused` | the REGISTER answered NO_RESOURCES (premise) | LK0, LN0 (same) |

The new failures in the earlier controls come from the timeout's UNLOCK. A word of 0
or a stale LOCK word on the automatic unlock now differs from the expected 1 (LN2,
L6d), and LF3a's LOCK with flags 0 follows a timeout that latched 1.

### Round 1b records (head fcb6b51)

Base records are those of round 1 (`08ae0013`, unchanged). Head ran in the lane tree
after `git clean -fdX`, and each new record was compared with base and with the round-1
head `c8261711`. Pinned Verilator 5.050 first on PATH, then sv2v 0.0.12 and Yosys 0.33.
Each gate ran unpiped in the foreground of its own detached job, with its own log, rc
and duration.

| Gate | Head fcb6b51 | vs round-1 head c8261711 | vs base 08ae0013 |
|---|---|---|---|
| scripts/run_suites.sh | rc 0, 1,030,094 checks, 0 failing (2,183 s) | identical | as in round 1: UPC map 61 → 62 / 90 → 91, aecp_notify 67 → 73, pp_top 10,519 → 10,599, ucpu 437 → 445 |
| executed REQ-tag check | rc 0 | log identical; evidence identical with source lines masked (pp_top lines after L6d +1) | evidence identical as sorted with lines masked |
| scripts/lint_hdl.sh | rc 0 | identical | identical |
| make check | rc 0 | identical | as in round 1 (links 1196 → 1198, aecp entries 84 → 85, ids 592 → 601) |
| scripts/gen_matrix.py --check | rc 0 | identical | identical |
| syn/yosys/run.sh, Yosys 0.33 (CI pin) | rc 0 | six memory warnings' all.v lines +1 (the new localparam) | as in round 1, those lines moved |
| syn/yosys/run.sh, host Yosys 0.66 | rc 0 | the same six lines +1 | the same |
| tb/elab_guards/guards.py --frontend yosys | rc 0 | inventory line of `KL_aecp_notify.g_rows_guard` +2 (the banner), all.v lines +1 | as in round 1, lines moved |

Campaigns at head `fcb6b513`: all 13 that build a changed file, as in round 1 (the
round-1b files are the notify block, the engine's and the generator's comments, the
command table, and the pp_top, aecp_notify and ucpu benches). Two streams in the lane
tree, each output directory fresh and outside the tree, TMPDIR scratch. Base records are
round 1's.

| Campaign | Head fcb6b513 | vs round-1 head c8261711 |
|---|---|---|
| tb/pp_top/aecp_dispatch_mutants.py --jobs 2 | rc 0, 67 checks PASS | identical, line for line (durations masked) |
| tb/pp_top/notify_mutants.py --jobs 2 | rc 0, 114 of 114 KILLED, goldens PASS (2,406 s) | the 3 new controls added; every non-lock control fails the same checks; the lock controls' changes are those in the table above |
| tb/aecp_cmds/mutants.py --jobs 2 | rc 0, 17 of 17 detected (695 s) | identical |
| tb/pp_top/aecp_mutants.py --jobs 2 | rc 0, 67 checks PASS (1,382 s) | identical but for one failing-check line's text: `td-lock-default-59s` still fails TD1 (59,003 ms), whose message now names flags UNLOCK |
| tb/pp_top/ctr_mutants.py --jobs 2 | rc 0, 18 checks PASS (280 s) | identical |
| tb/pp_top/gsi_mutants.py --jobs 2 | rc 0, 20 detected (763 s) | identical |
| tb/pp_top/name_wr_mutant.py | rc 0, decode killed, golden and restored PASS (62 s) | identical |
| tb/name_state/mutants.py --jobs 2 | rc 0, 16 KILLED (457 s) | identical as sorted lines |
| tb/maap/mutants.py --jobs 2 | rc 0, 32 checks PASS (208 s) | identical |
| tb/adp_engine/mutants.py --jobs 2 | rc 0, 62 checks PASS (681 s) | identical |
| tb/pp_top/acmp_mutants.py --jobs 2 | rc 0, 51 of 51 KILLED, goldens PASS (2,026 s) | summary identical; each mutant's failing checks identical except `armq_read_tail`'s L6d line, whose message now names flags UNLOCK (the same check) |
| tb/elab_guards/mutants.py --jobs 2 | rc 0, 160 of 160 killed (1,319 s) | identical with all.v line numbers masked (47 lines, +1) |
| tb/pp_top/d3_mutants.py --jobs 3 | rc 0, 110 of 110 KILLED, goldens PASS (4,546 s) | identical; each of the 117 records' failing checks identical |

Not run, as in round 1, because they build no changed file: tb/srp_top and
tb/srp_admission mutants, tb/acmp_talker/retry_mutants.py, tb/desc_mem_guard/mutate.py,
tb/desc_store's lint mutations and `make -C tb/nvm_port figures`.

### Round 1b scratch-parent consumer gates

Same scratch parent (dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`, never committed or
pushed). In the submodule (`rev-parse --show-toplevel` checked before every git command)
the head was fetched from the lane and checked out detached at `fcb6b513`, its ignored
products cleaned, and the gitlink staged at
`fcb6b5138e17b33a3c51572594a1aa210aa0bef1`. The parent's ignored products were also
cleaned. The two parent patches are still applied verbatim, and `git apply --check -R`
of each passes (sha256 76625170…495e and e142e2e7…66d3). `git diff --stat` shows exactly
their two files.

| # | Parent consumer gate | Base (08ae0013) | Head (fcb6b513) | vs round-1 head (c8261711) |
|---|---|---|---|---|
| 1 | check_cpp_idiom.py | rc 0 | rc 0 | identical |
| 2 | check_py_idiom.py | rc 0 | rc 0 | 258,981 → 258,994 lines (the driver's +13) |
| 3 | check_rtl_source_lists.py | rc 0 | rc 0 | identical |
| 4 | pp_srcs.py --check --selftest | rc 0 | rc 0 | identical |
| 5 | check_port_contracts.py | rc 0 | rc 0 | identical |
| 6 | measure_naming.py --check | rc 0 | rc 0 | identical |
| 7 | measure_test_evidence.py --check (#180 patch) | rc 0 | rc 0 | identical |
| 8 | docs_check.py | rc 0 | rc 0 | identical |
| 9 | check_sh_idiom.py | rc 0 | rc 0 | identical |
| 10 | sw/builder/test_builder.py | rc 0 | rc 0 (1,912 s) | ALL GATES PASS EXCEPT 1 NOT RUN at both (gate 11's external build tree). With the round-1 masking (the NVM writer self-test arms' timing-dependent first findings; all 70 `self-test OK` at both), identical except two temp names |
| 11 | lint_rtl.py --check | rc 0 | rc 0 | identical |
| 12 | make -C tb/verilator/pp_shadow | rc 0 | rc 0 | RESULT: PASS; 2,188 PASS/FAIL lines identical as sorted; Verilator build sizes |
| 13 | nvm_cosim lint | rc 0 | rc 0 | Verilator walltimes only |
| 14 | nvm_cosim quick | rc 0 | rc 0 | identical |
| 15 | make -C tb/verilator/milan_dp SIM_JOBS=2 | rc 0 | rc 0 | PASS/FAIL lines identical as sorted; otherwise Verilator build sizes and render-phase timings |
| 16 | make -C tb/verilator/milan_dp_render | rc 0 | rc 0 | records identical as sorted; build sizes |
| 17 | flock $VIVADO_LOCK xvlog_gate.py --check | rc 0, 0 findings | rc 0, 0 findings | the pin line (c8261711 → fcb6b513) |

### Round 1b acceptance

| Item | Met | Where |
|---|---|---|
| Correction: the automatic unlock after the timeout carries flags UNLOCK, locked_id 0 | yes | `KL_aecp_notify.sv:1393,1398`; LN2, L6d, TD1, RN, LF2, L3b |
| Correction: the command-driven unlock carries UNLOCK, locked_id 0 | yes (since round 1: it echoes the UNLOCK's word) | L5b, LN4, LF1b |
| LN2 updated, its planted mutant keeps 0 and fails | yes | `lock_timeout_flags_zero` → LN2; also `lock_auto_unlock_flags_zero` → L6d, `lock_coalesced_timeout_flags_zero` → LF2, and the hand-planted runs |
| Docs and the handoff's coalesced-change table | yes | above; 06 §6.8, F06.14, compliance row 16, 09, READMEs |
| Gates, campaigns, parent consumer gates rerun, rc 0 | yes | tables above |
| STOP conditions | none hit | no register-map, top-level port or parameter change (`git diff c826171 HEAD -- hdl/top hdl/common hdl/aecp/ucpu_pkg.sv` is empty) |

REVIEW READY with the new head was posted on #185 (comment 6257747212).

## Status (round 1)

Round 1 text below is kept as written at `c8261711`. Where it says the timeout keeps
flags 0, round 1b supersedes it.

- TAKEN was posted on #185 (comment 6249589802) in the first session. It was not posted again.
- Done. Both commits are on the lane branch at head `c826171`. Every processor gate and
  every campaign that builds a changed file is rc 0 at base and at head. All 17 parent
  consumer gates are rc 0 at base and at head. Every record difference is listed and
  explained below. REVIEW READY is posted on #185 with the head (comment 6255090417).

## Resume notes (second session)

- The first session was stopped by the manager at 14:3x. All of its edits were intact in the
  tree, uncommitted. I checked that no planted mutant had been left in it. Every
  `rdc-*.patch` still applies forward (`git apply --check`) and none applies in reverse. The
  campaign anchor check found every exact-edit anchor of the 16 drivers exactly once (594
  edits, 0 failures). Every tree file matched the intended change in the diff review.
- The base `run_suites.sh` had been cut off. It was re-run from the start in the scratch
  submodule at base.
- The tree was split into the two commits by hunk. Mixed hunks were applied by exact string
  edits, and the full state was kept in a stash and a scratch backup. At the #185 commit,
  `tb/aecp_cmds/decode.json` was re-swept (`make -C tb/aecp_cmds record`, 617,916 trials)
  and the ucpu README count was set to that commit's 442. After the #186 commit, the
  head's tracked files were byte-identical to the backup, and the re-swept record matched
  the first session's byte for byte.
- After measuring the new arms on their own, I added their mutation records to the suite
  READMEs and to 09. To keep two commits, the branch was reset to the #185 commit, that
  commit was amended, the #186 commit was cherry-picked and amended. There was no rebase,
  and nothing had been pushed. The superseded SHAs were `8b86d69` and `ccb8b6f`.
- The full dispatch campaign at `60da763` showed three earlier arms failing more checks
  than at base, because they also reach new RDC or LN checks (below). Their README rows
  were updated. Head campaigns were running in the lane tree at the time, so I rebuilt
  the two commits with `git commit-tree` from a temporary index, each being the earlier
  commit's tree with the new `tb/pp_top/README.md` blob. The branch was moved with
  `git update-ref`, and only the README was refreshed in the working tree.
  `git diff 60da763 ccd1b8b` touches `tb/pp_top/README.md` alone (+10 -4). The
  superseded SHAs were `722d585` and `60da763`. Nothing reads that README except
  `make check`'s link, ID and figure gates (a search of the campaign drivers, Makefiles
  and scripts finds only comments).
- The first parent consumer pass at `ccd1b8b` failed gate 1, `check_cpp_idiom.py`:
  "FAIL: multi-declarator declaration 2 > ratchet 0" (Rule 11 of the parent's
  CODE_QUALITY.md). Both findings were mine, in `tb/pp_top/sim_main.cpp`
  (`const uint8_t v0 = ..., v1 = ...;` and the same for `t0, t1`, in
  `rd_control_after_set`). I stopped that pass and the head campaigns that were running,
  split the two declarations in the #185 commit (and so in the #186 tree), and rebuilt
  both commits the same way (`198f1b1`, `c826171`; `ccd1b8b` and `37ef8c3` superseded).
  `git diff ccd1b8b c826171` is that file alone (+4 -2). The probe's gates 2-11 passed;
  its records are kept under the scratch records as `probe-parent-ccd1b8b` and are not
  counted. Every processor gate, every campaign that builds `tb/pp_top/sim_main.cpp`, and
  every parent consumer gate was then run again at `c826171`.
- `make check` passes at both commits (rc 0).

## Scope notes

- The session brief names "E_SCFG" as the allowed change scope and "Closes #179" for the PR
  body. #179 (SET_CONFIGURATION, closed and merged) and E_SCFG belong to another lane. This
  lane's assignment (A10, comment 6249574548) covers #185 (READ_DESCRIPTOR's CONTROL overlay)
  and #186 (the LOCK_ENTITY notification's flags). I did the assignment exactly: the
  changes are those two arms, their tests, the generators and records that must follow them,
  and the docs that record them. E_SCFG is untouched. The PR body closes #185 and #186, not
  #179.
- STOP check: there is no register-map, top-level port or parameter change.
  `git diff 08ae001 HEAD -- hdl/top` adds one internal wire (`aecp_rgy_flags_w`) and its two
  connections, and nothing in `protocol_processor_top`'s port or parameter list. The
  `hdl/common` package, `ucpu_pkg.sv` and every register map are unchanged. Two internal
  module ports were added, `KL_aecp_engine.rgy_flags_o` and `KL_aecp_notify.rgy_flags_i`
  (32 bits each). They are wired only inside `protocol_processor_top` and in the
  `tb/aecp_cmds` wrapper (left open). Nothing in the parent instantiates either module; a
  search of the scratch parent finds only comments and source lists.

## Changes (file:line at head c826171)

### #185 READ_DESCRIPTOR CONTROL current value (commit 198f1b1)

- `hdl/aecp/ucode/gen_ucode.py:257`: `E_RDESCCT = 600`, in the free 594..639 run in front
  of E_RDESC.
- `hdl/aecp/ucode/gen_ucode.py:1286-1344`: the clause comment, the layout constants
  (`CT_VTYPE_LANE` 80, `CT_VOFF_LANE` 88, `CT_VALUES` 104, `CT_LINEAR_INT16` 0x0002,
  `CT_CUR_OFF` 108, `CT_CUR_TAIL` 112), and the `E_RDESCCT` program at
  `gen_ucode.py:1308`. It runs the configuration check and the locate, then three layout
  guards to E_RDESC. Otherwise it copies image bytes 0..107, puts `current[0]` @108 from
  `RGN_DYN + SEL_IDENT` (GET_CONTROL's row, no image arm), rebuilds 109..111 from the
  image lane, and copies the TAIL from 112. Placement asserts: `E_RDESCCT + 12` and `+ 17`.
- `hdl/aecp/KL_aecp_engine.sv:904`: `UPC_RDESCCT_C = 11'd600`.
- `hdl/aecp/KL_aecp_engine.sv:3303-3314`: the re-dispatch at the @28 seam. It applies to
  AEM, message_type 0, READ_DESCRIPTOR, cdl >= 20, configuration 0 and descriptor_type
  CONTROL, and it sits beside issue #82's four.
- `hdl/aecp/ucode/aecp_commands.json:91`: READ_DESCRIPTOR's entries gain `RDESCCT`.
- `tb/aecp_cmds/decode.json:62`: `RDESCCT` floor 20, cdls 20 and 100, SUCCESS at 129. RDESC
  loses its 129 answer. The trial count and the engine and ROM digests were re-swept.
- `tb/ucpu/sim_main.cpp:46,205-221,288,861-899`: section RC (RC1, RC2) on a conformant
  113-byte IDENTIFY CONTROL. `tb/ucpu/README.md:6,70-76` record it.
- `tb/pp_top/sim_main.cpp`: AX fixture (CONTROL_LINEAR_UINT8, lane 0xA0..0xA7, image
  `current[0]` 0x5A); RDC0 at `:12383`; RDC1 to RDC3b at `:12029` (`rd_control_after_set`);
  RDC4 at `:12108`; RDC5 (before and after the power cycle) to `:12454`; RDC6 (a 111-byte
  CONTROL) to `:12505`; the helpers `rd_ctrl` and `rd_ctrl_image` at `:12353` and `:12358`.
- `tb/pp_top/aecp_dispatch_mutants.py:135-162` and the nine
  `tb/pp_top/aecp_dispatch_mutations/rdc-*.patch`.
- Docs: `docs/architecture/06_aecp_engine.md:306,315,336-354,1294` (§6.1 overlay table
  row, the CONTROL paragraph, the opcode answer row); `docs/00_MILAN_COMPLIANCE_REVIEW.md:599`
  (decision row 15); `docs/architecture/09_verification.md:185` (Identify row);
  `tb/pp_top/README.md` (section AX title, the RDC bullet, nine arm rows and their note,
  and the three earlier rows the RDC checks move: `lk-sctrl-lock-nop` 12 → 13,
  `rd-tail-uncut` 9 → 16, `rd-str-short-guard-nop` 1 → 5).

### #186 LOCK_ENTITY notification flags (commit c826171)

- `hdl/aecp/ucode/gen_ucode.py:1166-1186`: E_LOCKUNS builds flags @24 from r14[31:0], the
  causing command's word (`gen_ucode.py:1183`), where it used r12 = 0. The comment states
  the register contract.
- `hdl/aecp/KL_aecp_engine.sv:528`: output `rgy_flags_o`. At `:2273` it is
  `{cfg_ix_r, desc_ix_r}`, LOCK_ENTITY's @24..@27 as E_LOCKEN echoes it.
- `hdl/aecp/KL_aecp_engine.sv:1589-1598`: `lockf_w` packs r14[31:0] as LOCK_ENTITY's
  for the command and for the notification job routed to the rgy face (`uns_r && regun_r`).
- `hdl/aecp/KL_aecp_engine.sv:2970-2978`: a PP_UNS_LOCK_C job lands `uns_arg1_i` and
  `uns_arg0_i` in `cfg_ix_r` and `desc_ix_r`.
- `hdl/aecp/KL_aecp_notify.sv:94-103` (banner), `:271` (`rgy_flags_i`), `:420` (`lockf_r`),
  `:836-837` (the job's arguments), `:1224` (reset), `:1390` and `:1395` (the timeout,
  coalesced or not, latches 0), `:1440` and `:1456` (a LOCK or UNLOCK latches the command's
  word).
- `hdl/top/protocol_processor_top.sv:3451,3857,4065`: the internal wire and its two
  connections.
- `tb/aecp_cmds/aecp_cmds_wrap.sv:231`: `.rgy_flags_o ()`.
- `hdl/aecp/ucode/aecp_commands.json:69`: the notify doc string, which renders F06.14's
  LOCK_ENTITY row (`06_aecp_engine.md:253`).
- `tb/aecp_notify/sim_main.cpp:137` (`lock_op`), `:340-403` (section LF: LF1, LF1b, LF2,
  LF3a, LF3), and `tb/aecp_notify/README.md` (the build table, the count and section LF).
- `tb/ucpu/sim_main.cpp:1340-1359`: L3 (flags 0x80010001 echoed), L3b (auto-unlock 0).
- `tb/pp_top/sim_main.cpp:5231-5240`: L5b expects the UNLOCK's flags 1. `:12508-12572`:
  section LN (LN0 to LN4).
- `tb/pp_top/notify_mutants.py:622-704`: `LOCK_FLAGS`, 13 controls.
- Docs: `06_aecp_engine.md:253,800-816,1292`; `00_MILAN_COMPLIANCE_REVIEW.md:600` (decision
  row 16); `09_verification.md` §8.4 (LF row, "eight of the notification block's");
  `tb/pp_top/README.md` (the LN bullet, 13 notify rows and their note, and
  `rd-str-short-guard-nop` 5 → 6 for LN0); `tb/ucpu/README.md:78`.

## Accepted lengths and refusal cases

READ_DESCRIPTOR (AEM, message_type 0, opcode 0x0004). The recorded sweep is
`tb/aecp_cmds/decode.json`.

| Case | Program | Answer |
|---|---|---|
| cdl 12..19 | BADARG | BAD_ARGUMENTS, the command echoed (unchanged) |
| cdl >= 20, configuration 0, CONTROL, located, length >= 112, `values_offset` 104, `control_value_type` < 0x0002 (LINEAR_INT8 or LINEAR_UINT8) | E_RDESCCT | SUCCESS: image bytes, with `current[0]` @108 = what GET_CONTROL reads (0 after reset and power cycle, the value after every SET_CONTROL); cdl 16 + length (129 for the 113-byte fixture). Padded commands (cdl 100) answer the same |
| same, length < 112 (ends inside lane 104..111) | E_RDESCCT → E_RDESC | SUCCESS, the image whole |
| same, `values_offset` != 104 | E_RDESCCT → E_RDESC | SUCCESS, the image whole |
| same, `control_value_type` >= 0x0002 (wider or non-linear) | E_RDESCCT → E_RDESC | SUCCESS, the image whole |
| CONTROL index not in the image | E_RDESCCT → E_RDSTUB | NO_SUCH_DESCRIPTOR, §7.4.5 4-byte stub (as E_RDESC) |
| `configuration_index` >= configurations_count | E_RDESCCT → E_RDSTUB | BAD_ARGUMENTS stub (as E_RDESC; unreachable with configuration 0 and one or more configurations) |
| configuration != 0, or any other type | unchanged | as at base |

GET_CONTROL answers every located CONTROL index from the same IDENTIFY row (E_GCTRL), so
the overlay agrees with GET_CONTROL for any index it serves.

LOCK_ENTITY (opcode 0x0001) accepts the same lengths and returns the same answers as at
base: cdl 28, SUCCESS / ENTITY_LOCKED / BAD_ARGUMENTS / NOT_SUPPORTED, flags echoed. What
changes is the unsolicited LOCK_ENTITY sent to every registered controller except the
requester:

| Cause | Notification flags @24..@27 | locked_id |
|---|---|---|
| a LOCK that took the lock | the LOCK's whole flags word (reserved bits included) | the new holder |
| an UNLOCK that released it | the UNLOCK's whole flags word (UNLOCK = 1, reserved bits included) | 0 |
| the lock timeout (Milan Table 5.22 auto-unlock) | 0 (round 1; **UNLOCK since round 1b**) | 0 |
| coalesced changes (a round still pending) | the last cause's (a timeout's 0, **UNLOCK since round 1b**; a LOCK's own) | the holder now |
| no change (already-unlocked query, refused LOCK) | no notification (unchanged) | - |

## New checks, planted mutants and failing words

Every arm was killed by its named check. The dispatch arms were measured with
`aecp_dispatch_mutants.py --jobs 4 --only rdc-...` and the notify arms with
`notify_mutants.py --jobs 4 --only ...`, both on the head tree (142 s and about 10 min).
The full campaigns at head re-grade them (below).

### #185 (aecp_dispatch_mutants.py, target aecp-dispatch): control PASS, 9 of 9 KILLED

| Arm | Planted | Named failing words | Failing checks |
|---|---|---|---|
| `rdc-base-no-overlay` | the engine's #185 re-dispatch removed (the issue reproduction) | `RDC1 CONTROL 0 after SET_CONTROL(255) and three refused SET_CONTROLs: READ_DESCRIPTOR byte-exact` | 7 |
| `rdc-unset-image` | E_RDESCCT given an image arm for an unwritten row | `RDC0 CONTROL 0 before any SET_CONTROL: current[0] the reset 0, not the image's 0x5A: READ_DESCRIPTOR byte-exact` | 2 |
| `rdc-voffset-guard-nop` | the values_offset guard's BRANCH replaced with NOP | `RDC2 CONTROL 0 with values_offset 106, IDENTIFY 255: its image whole: READ_DESCRIPTOR byte-exact` | 1 |
| `rdc-vtype-int16` | the value-type bound 0x0002 moved to 0x0003 | `RDC3 CONTROL 0 as a CONTROL_LINEAR_INT16, IDENTIFY 255: its image whole: READ_DESCRIPTOR byte-exact` | 1 |
| `rdc-vtype-uint8-only` | only CONTROL_LINEAR_UINT8 overlaid | `RDC3b CONTROL 0 as a CONTROL_LINEAR_INT8, IDENTIFY 255: overlaid: READ_DESCRIPTOR byte-exact` | 1 |
| `rdc-short-floor-111` | the too-short floor 112 moved to 111 | `RDC6 CONTROL 0 of 111 bytes, IDENTIFY 255: its image whole: READ_DESCRIPTOR byte-exact` | 2 (with LN0) |
| `rdc-unit-shift-8` | @109 from a shift of 8, not 16 | `RDC1 CONTROL 0 after SET_CONTROL(255) and three refused SET_CONTROLs: READ_DESCRIPTOR byte-exact` | 7 |
| `rdc-ident-reset-255` | the IDENTIFY row resets to 255 (premise) | `RDC0 IDENTIFY unset: GET_CONTROL reads Milan 5.3.12's reset 0 (premise)` | 5 |
| `rdc-sctrl-no-write` | E_SCTRL's IDENTIFY write a NOP (premise) | `RDC1 GET_CONTROL reads 255 (premise)` | 11 |

`tb/ucpu` RC1 and RC2 grade the program in isolation: the 113-byte form, with a one-byte
TAIL, and a `values_offset` of 106 served whole.

### #186 (notify_mutants.py): goldens PASS, 13 of 13 KILLED

| Control | Planted | Named failing words |
|---|---|---|
| `lock_unlock_notifies_flags_zero` | E_LOCKUNS flags from r12 = 0 (the issue reproduction), main suite | `L5b: C2's second notification carries sequence_id 1 (Milan 5.4.5.1) and the UNLOCK's flags 1` |
| `lock_notification_flags_zero` | the same edit, section AX | `LN1 ...its notification echoes the LOCK's flags: flags`, `LN4 ...its notification echoes the UNLOCK's flags: flags` |
| `lock_flags_unlock_bit_only` | the latch takes `{31'd0, rgy_op_i[0]}` | LN1, LN4 (as above) |
| `lock_timeout_keeps_flags` | the timeout no longer clears the latch | `LN2 the auto-unlock after that LOCK (Milan Table 5.22) carries flags 0: flags` |
| `lock_flags_from_exclusion` | the job's arguments from the exclusion eid | `LN3 ...its notification carries flags 0: flags` (and LN1, LN2, LN4) |
| `lock_job_arguments_dropped` | the engine loads a LOCK job like any other | LN1, LN4 |
| `lock_job_r14_unpacked` | `lockf_w = lockc_r` (no notification packing) | LN1, LN4 |
| `lock_notification_not_sent` | the LOCK job runs UPC_NOSEND_C (premise) | `LN1..LN4 ...: the registered bench is notified` |
| `lock_response_flags_zero` | E_LOCKEN's response flags from r12 (premise) | `LN1 a second controller's LOCK: SUCCESS echoing flags 0x00010000`, `LN4 its UNLOCK: SUCCESS echoing flags 0x80020001` |
| `lock_coalesced_timeout_keeps_flags` | the coalesced timeout keeps the latch | `LF2:` (tb/aecp_notify) |
| `lock_take_keeps_old_flags` | a LOCK latches nothing | `LF1:`, `LF3:` |
| `lock_release_keeps_old_flags` | an UNLOCK latches nothing | `LF1b:` |
| `register_refused` | the REGISTER answered NO_RESOURCES (premise) | `LN0: the bench registers for unsolicited notifications again` (and LK0) |

`tb/ucpu` L3 and L3b grade E_LOCKUNS in isolation (flags 0x80010001 echoed whole; the
auto-unlock's 0).

## Base and head records

Base ran in the scratch parent's protocol-processor checkout at `08ae0013`; its ignored
products were cleaned after `run_suites.sh` and before the base campaigns. Head ran in the
lane tree after `git clean -fdX`, first at `60da763`, then again at the final head `c826171`.
Every final-head log is identical to the `60da763` log (Verilator walltimes masked), except
the executed REQ-tag evidence: 11 pp_top source lines moved by +2, from the two split
declarations. Every gate ran in the foreground of its own
detached job, with its own log, rc and duration, never piped. The pinned Verilator
5.050 came first on PATH, then sv2v 0.0.12 and Yosys 0.33.

| Gate | Base 08ae0013 | Head c826171 | Record comparison |
|---|---|---|---|
| scripts/run_suites.sh | rc 0, 1,030,000 checks, 0 failing (1,632 s) | rc 0, 1,030,094 checks, 0 failing (2,155 s) | every suite line identical except: UPC map gate 61 → 62 engine constants and 90 → 91 entry points (`UPC_RDESCCT_C` / `E_RDESCCT`); aecp_notify 67 → 73 (section LF: 5 checks and its registration); pp_top 10,519 → 10,599 (section AX 239 → 279, RDC +28 and LN +12, in the default and the line build); ucpu 437 → 445 (RC +5, L3/L3b +3) |
| executed REQ-tag check (check-req-tags.py --suites/--evidence) | rc 0, 226 evidence lines, 14 suites | rc 0, 226, 14 | identical; the evidence file identical but for pp_top source line numbers |
| scripts/lint_hdl.sh | rc 0 | rc 0 | identical |
| make check | rc 0 | rc 0 | identical except `links: 1196 → 1198` (the two new decision rows' anchors), `aecp commands: 84 → 85 entries` (RDESCCT) and `ids: 592 → 601 files` (the nine new patch files); F06.14 41 rows at both |
| scripts/gen_matrix.py --check | rc 0 (94 rows, 0 untested) | rc 0 | identical |
| syn/yosys/run.sh (sv2v 0.0.12, Yosys 0.33, the CI pin) | rc 0, 42 tops (82 s) | rc 0 (92 s) | identical except six memory warnings' all.v line numbers (+21, the engine's and notify block's added lines) |
| syn/yosys/run.sh with the host Yosys 0.66 (second record) | rc 0 | rc 0 | the same six line numbers |
| tb/elab_guards/guards.py --frontend yosys --jobs 4 (CI portability job) | rc 0 (80 s) | rc 0 (147 s) | identical except the guard inventory's source lines (engine +2, notify +7) and the all.v line of the engine's guards (+3) |

Campaigns at base and head: every one that builds a changed file, meaning the engine, the
notify block, the top, the microcode generator and its table, or the pp_top, aecp_notify,
ucpu or aecp_cmds benches. Base ran in the scratch submodule at `08ae0013` and head in the
lane tree, each output directory fresh and outside the tree, and TMPDIR scratch. The eight
campaigns that build `tb/pp_top/sim_main.cpp` ran at `c826171`. The other five (aecp_cmds,
name_state, maap, adp, elab_guards) ran at `c826171` too, and their `60da763` runs are
identical.

| Campaign | Base 08ae0013 | Head c826171 | Comparison |
|---|---|---|---|
| tb/pp_top/aecp_dispatch_mutants.py --jobs 2 | rc 0, 58 checks PASS (1,073 s) | rc 0, 67 checks PASS (1,098 s) | the 9 `rdc-*` arms added, each KILLED by name. Three earlier arms fail more checks, every base failure kept: `lk-sctrl-lock-nop` 12 → 13 (RDC1's premise), `rd-tail-uncut` 9 → 16 (the seven overlaid RDC reads), `rd-str-short-guard-nop` 1 → 6 (RDC6's four and LN0, after RD4's unanswered read). Their README rows were updated. Every other record is identical; the `60da763` run is identical to this one, line for line |
| tb/pp_top/notify_mutants.py --jobs 2 | rc 0, 98 of 98 KILLED, goldens PASS (1,631 s) | rc 0, 111 of 111 KILLED, goldens PASS (2,202 s) | the 13 lock controls added and two goldens for their new suite runs (`--aecp-dispatch-only`, `--arm-queue-only`); every earlier control fails the same number of checks |
| tb/aecp_cmds/mutants.py --jobs 2 | rc 0, 17 of 17 detected (738 s) | rc 0, same | identical |
| tb/pp_top/aecp_mutants.py --jobs 2 | rc 0, 67 checks PASS (1,293 s) | rc 0, same (1,272 s) | identical |
| tb/pp_top/ctr_mutants.py --jobs 2 | rc 0, 18 checks PASS (356 s) | rc 0, same (287 s) | identical |
| tb/pp_top/gsi_mutants.py --jobs 2 | rc 0, 20 detected (1,059 s) | rc 0, same (866 s) | identical |
| tb/pp_top/name_wr_mutant.py | rc 0, decode killed, golden and restored PASS (101 s) | rc 0, same (64 s) | identical |
| tb/name_state/mutants.py --jobs 2 | rc 0, 16 KILLED (413 s) | rc 0, same (399 s) | identical as sorted lines |
| tb/maap/mutants.py --jobs 2 | rc 0, 32 checks PASS (160 s) | rc 0, same (179 s) | identical |
| tb/adp_engine/mutants.py --jobs 2 | rc 0, 62 checks PASS (461 s) | rc 0, same (562 s) | identical |
| tb/pp_top/acmp_mutants.py --jobs 2 | rc 0, 51 of 51 KILLED, goldens PASS (2,399 s) | rc 0, same (2,002 s) | identical as sorted lines, each mutant's failing checks identical |
| tb/elab_guards/mutants.py --jobs 2 | rc 0, 160 of 160 killed (1,414 s) | rc 0, same (1,439 s) | identical with engine, notify and all.v line numbers masked (44 lines) |
| tb/pp_top/d3_mutants.py --jobs 3 | rc 0, 110 of 110 KILLED, goldens PASS (4,830 s) | rc 0, same (4,434 s) | identical as sorted lines (117), each mutant's failing checks identical |

Not run, as they build no changed file: tb/srp_top and tb/srp_admission mutants (SRP
sources only), tb/acmp_talker/retry_mutants.py (pp_pkg, srp_pkg, KL_acmp_talker),
tb/desc_mem_guard/mutate.py (the descriptor store and its guard), tb/desc_store's lint
mutations (the image generator) and `make -C tb/nvm_port figures` (KL_pp_nvm_port).

## Scratch-parent consumer gate table

The scratch parent is a clone of kebag-logic/milan-fpga at dev
`e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f` under the scratch root. It was never committed
or pushed. Its submodules sit at their pins (external efeb541a, gptp-processor e4869fd0,
lwSRP 08ee86e8, tsn-c-stack 70936b77, verilog-axis 48ff7a7e). The protocol-processor
gitlink was staged (`git add`, not committed) at base `08ae0013` for the base pass. For the
head pass the head was fetched from the lane, checked out detached, and the gitlink staged
at `c8261711e040db0d89c77980b198716974b4684b`, where it was left. Every git command in the
submodule and in the parent was preceded by a `rev-parse --show-toplevel` check. The
parent's and the submodule's ignored products were cleaned before each pass.

Two uncommitted scratch-only parent edits were applied before both passes, verbatim:
- `parent-evidence-classification.patch` (#180, from the pp178 lane; 2,689 bytes, sha256
  76625170…495e): the reader classifications of the processor's elab_guards drivers;
- `parent-adoption-milan_dp-67.patch` (#176, from the pp176 lane; sha256 e142e2e7…66d3): the
  milan_dp #67 case's 2013-length SET_STREAM_INFO expectation.

`git diff --stat` in the parent at both passes shows exactly these two files
(`scripts/measure_test_evidence_readers.py` +16, `tb/verilator/milan_dp/sim_nxn.cpp` +8 -4).

| # | Parent consumer gate | Base (08ae0013) | Head (c8261711) | Comparison |
|---|---|---|---|---|
| 1 | python3 scripts/check_cpp_idiom.py | rc 0 | rc 0 | identical. The first head pass, at `ccd1b8b`, failed here with my two multi-declarator lines (resume notes); fixed |
| 2 | python3 scripts/check_py_idiom.py | rc 0 | rc 0 | no findings; 258,800 → 258,981 lines, the Python this change adds to the campaign drivers |
| 3 | python3 scripts/check_rtl_source_lists.py | rc 0 | rc 0 | identical |
| 4 | python3 scripts/pp_srcs.py --check --selftest | rc 0 | rc 0 | identical |
| 5 | python3 scripts/check_port_contracts.py | rc 0 | rc 0 | protocol-processor ports 1,761 → 1,763 (`rgy_flags_o`, `rgy_flags_i`, both documented); undocumented 111 <= 111 unchanged |
| 6 | python3 scripts/measure_naming.py --check | rc 0 | rc 0 | the same two ports counted (3,989 → 3,991 ports scanned); 95 candidates, all recorded, unchanged |
| 7 | python3 scripts/measure_test_evidence.py --check (with the #180 patch) | rc 0 | rc 0 | identical |
| 8 | python3 scripts/docs_check.py | rc 0 | rc 0 | identical |
| 9 | python3 scripts/check_sh_idiom.py | rc 0 | rc 0 | identical |
| 10 | python3 sw/builder/test_builder.py | rc 0 (1,986 s) | rc 0 (1,751 s) | ALL GATES PASS EXCEPT 1 NOT RUN at both: gate 11's calibration report needs an external build tree absent here. With temp names, durations, and the finding counts and first findings of the firmware NVM writer's self-test arms masked (those arms grade on parallel threads and stop at the first named finding, so the counts depend on timing; every arm is `self-test OK` at both), base and head are identical except one more temp name. The `vivado.log` it mentions is a synthetic file written by its constraint-log test; Vivado is not started |
| 11 | python3 scripts/lint_rtl.py --check | rc 0 | rc 0 | identical: 90 violations within the ratchet of 90 |
| 12 | make -j8 -O -C tb/verilator/pp_shadow | rc 0 (393 s) | rc 0 (411 s) | RESULT: PASS at both; the 2,188 PASS/FAIL record lines identical as sorted; differences are `ucode.hex: 2048 words, 90 → 91 programs` (E_RDESCCT) and Verilator's build sizes |
| 13 | make -j8 -O -C tb/verilator/nvm_cosim lint | rc 0 | rc 0 | identical |
| 14 | make -j8 -O -C tb/verilator/nvm_cosim quick JOBS=4 POOL=2 | rc 0 | rc 0 | identical |
| 15 | make -j8 -O -C tb/verilator/milan_dp SIM_JOBS=2 | rc 0 (2,251 s) | rc 0 (2,106 s) | the 1,143 PASS/FAIL record lines identical as sorted (parallel legs). The rest differs only in phase timings, Verilator sizes, the 90 → 91 programs line, and 16 of 360 informational `timestamp` lines whose absolute stamp and phc moved by a constant 5,120 ns of simulated time, residuals identical |
| 16 | make -j8 -O -C tb/verilator/milan_dp_render | rc 0 (877 s) | rc 0 (808 s) | records identical as sorted; the 90 → 91 programs line and build sizes |
| 17 | flock $VIVADO_LOCK python3 scripts/xvlog_gate.py --check (Vivado 2026.1 xvlog) | rc 0, 0 findings | rc 0, 0 findings | identical but for the line naming the processor pin (08ae0013 → c8261711) |

## Acceptance (issues #185 and #186 "Done when", assignment items 1-5)

| Item | Met | Where |
|---|---|---|
| #185: READ_DESCRIPTOR CONTROL returns the current value after every SET_CONTROL, as the four overlaid types of #82 do (IEEE 7.2.22, 7.3.6.2; Milan 5.3.12) | yes | E_RDESCCT and its re-dispatch; AX RDC0 to RDC6 byte-exact (reset 0, 255 after SET_CONTROL(255) and three refused, 0 after SET_CONTROL(0), either side of a power cycle); ucpu RC1, RC2 |
| #186: the notification a LOCK_ENTITY command drives echoes the command's flags, as the response does (IEEE 7.5.2, 7.4.2.1) | yes | the flags latch, the job's arguments, the r14 packing, E_LOCKUNS; L5b (UNLOCK, flags 1), LN1 and LN4 (reserved bits in both halves), aecp_notify LF1, LF1b, LF3; ucpu L3 |
| #186: the lock-timeout notification (Milan Table 5.22) keeps flags 0 | withdrawn by the correction; round 1b makes it UNLOCK | see Round 1b acceptance |
| Suite cases for each, each with a planted mutant that fails it | yes | 9 dispatch arms and 13 notify controls, all killed by their named checks (tables above) |
| docs/architecture/06_aecp_engine.md and the command records updated | yes | 06 §6.1, §6.8, F06.14, the opcode answers; `aecp_commands.json`; re-swept `decode.json`; compliance review rows 15, 16; 09; suite READMEs |
| Every processor gate at base and head, with the CI-pinned sv2v and Yosys | yes, all rc 0 | records above |
| Parent consumer gates on a scratch parent at dev e9cbb676, gitlink at the head, with the #180 and #176 parent patches | yes, all 17 rc 0 at base and head | table above |
| STOP on a register-map, top-level port or parameter change | none made; no STOP | `git diff 08ae001 HEAD -- hdl/common hdl/aecp/ucpu_pkg.sv` is empty; `hdl/top` gains one internal wire and two internal connections only |

PR-BODY.md therefore carries "Closes #185" and "Closes #186". The brief's "Closes #179" is
not used: #179 is SET_CONFIGURATION, already closed by another lane, and this assignment does
not touch it (Scope notes).

## Posting

Round 1: REVIEW READY was posted on processor issue #185 with the head (comment
6255090417), as the assignment ("Post REVIEW READY or STOP here") and the brief ask.
Round 1b: "[A647] REVIEW READY: branch 185-186-control-unlock, head
fcb6b5138e17b33a3c51572594a1aa210aa0bef1 (round 1b; three commits on main 08ae0013)."
was posted on #185 (comment 6257747212). TAKEN was not posted again. Nothing was posted
on #186 or elsewhere. No existing comment was edited.
Round 1c: "[A647] REVIEW READY: branch 185-186-control-unlock, head
f42c886c9abf311af64152eda669cbb040460bd1 (round 1c; main 246cbc22 merged in a2cf652)."
was posted on #185 (comment 6263866453). TAKEN was not posted again.
Round 2: "[A647] REVIEW READY: branch 185-186-control-unlock, head
4865184c9ba88dd85aba3fc8036a6b74bcdb7073 (round 2 on b0f6f9c3, five commits)", with one
sentence on parent gate 11, was posted on #185 (comment 6272997482,
`receipts/round2/posting.txt`). TAKEN was not posted again; nothing was posted elsewhere;
no existing comment was edited.
Round 3: "[A647] REVIEW READY" with the unchanged head `4865184c` was posted on #185
(comment 6273894224, `receipts/round3/posting.txt`). TAKEN was not posted
again; nothing was posted elsewhere; no existing comment was edited.

## Final state

- Round 3: no commit; the lane is still at `4865184c` (PR #196), clean, nothing pushed.
  Receipts: `receipts/round3/` beside the kept `receipts/round2/`.
- Round 2: lane branch `185-186-control-unlock` at
  `4865184c9ba88dd85aba3fc8036a6b74bcdb7073`, five commits on PR #196's `b0f6f9c3`
  (`43a7987`, `4ba8c02`, `acc059a`, `7368215`, `4865184`). Clean (`git status --short
  --ignored` empty after `git clean -fdX`). Nothing pushed, rebased or amended.
- Round 2 scratch parent: dev `e9cbb676` plus local branch `pp185-a647-r2-scratch` (the
  two patch commits and three gitlink commits, parent table), never pushed. HEAD
  `700bdd4aa`, gitlink committed at `4865184`, submodule checked out there (detached),
  working tree clean.
- Round 1c state, for the record: lane `185-186-control-unlock` at `f42c886c9abf311af64152eda669cbb040460bd1`.
  It is five commits on `08ae0013` plus the merge of main `246cbc22`: `198f1b1`,
  `c826171`, `fcb6b51`, the merge `a2cf652` and the README commit `f42c886`. The tree is
  clean (`git status --short --ignored` is empty after `git clean -fdX`). Nothing was
  pushed, nothing was rebased, and no PR exists.
- Scratch parent: dev `e9cbb676` plus the four local commits on the local branch
  `pp185-a647-r1c-scratch` (round 1c table), never pushed. HEAD is `fbc999ff6`, with the
  gitlink committed at `f42c886` and the submodule checked out there (detached). The
  working tree is clean. Rounds 1 and 1b used the same clone with the patches
  uncommitted, as their brief asked.
- All scratch work (records, scripts, backups, campaign outputs) is under the scratch root,
  outside both trees and outside this directory.

## Artifacts in this directory

- `HANDOFF.md`, `PR-BODY.md`.
- `receipts/round2/` (round 2): `base/gates` and `head/gates` (every processor gate at
  `b0f6f9c3` and `acc059a`, with `HEAD.txt`, the REQ-tag evidence and status),
  `base/campaigns` and `head/campaigns` (the 13 campaign summaries with rc, duration and
  each `results.json`), `head-final/gates` (every gate at `7368215`, and the anchor
  check), `head-final2` (every gate and the notify campaign at `4865184`),
  `parent-base` and `parent-head` (the 17 consumer gates and the parent's commits,
  gitlink, submodule HEAD, patch digests and status), the two stopped passes kept apart
  (`parent-base-stopped-at-xvlog`, `parent-head-7368215-stopped`), `compare` (the
  campaign table, sorted masked diffs and per-mutant failing-check sets), `newarms` (the
  six dispatch arms, the nine re-measured and the fourteen notify controls on their
  own), `probes-head` (the reviewers' claim-collision, mid-round and vendor probes at
  the head), `try` (the pre-commit runs: the new section against the base notify RTL,
  the full pp_top suite, the decode re-record, and the split's output comparison),
  `labels` (the comment-label scans and the residue lines at the head) and `scripts`.
  The campaigns' per-mutant logs stay in the scratch records. Files over 200 KB are
  listed in `OVER-200KB.sha256`.
- `receipts/r1c/` (round 1c): `base/gates` and `head/gates` (every processor gate at
  `246cbc22` and `a2cf652`, with `HEAD.txt`, the REQ-tag evidence and status),
  `base/campaigns` and `head/campaigns` (the 13 campaign summaries with rc and duration),
  `head-final/gates` (every gate at `f42c886`), `parent-base` and `parent-head` (the 17
  consumer gates, the parent's local commits, the committed gitlink, the submodule HEAD,
  the patch digests and their `apply --check -R`, and the parent status before and after),
  `compare` (the campaign table, sorted masked diffs, per-mutant failing-check sets base
  vs head and round-1b head vs round-1c head, the parent table and diffs, and head vs final
  head), `merge` (the lane log, the diff stats, the merge's combined diff, the conflicted
  files against each parent, the anchor check and the final status), `try` (the
  pre-commit aecp_notify run, make check and matrix on the merge), the streams' `.out`
  files and `scripts` (the scripts that ran them). Files over 200 KB (the parent
  pp_shadow and milan_dp logs, base and head, and the milan_dp diff) are listed in
  `OVER-200KB.sha256`.
- `receipts/`: the logs, rc and duration files of every gate and campaign summary, under
  `base`, `head` (`60da763`), `head-final` (`c826171`), `parent-base`, `parent-head`,
  `base-campaigns`, `head-campaigns`, `newarms` (the new arms on their own) and the per-commit
  checks `c185`, `c185b`, `c186`, `c186b`. Four logs over 200 KB are recorded by sha256 and
  size in `receipts/OVER-200KB.sha256`: pp_shadow and milan_dp, base and head. The per-mutant
  campaign logs stay in the scratch records.
- `receipts/r1b/` (round 1b): `head` (every processor gate at `fcb6b513`, with
  `HEAD.txt`, the REQ-tag evidence and `status-after.txt`), `head-campaigns` (the 13
  campaign summaries with rc and duration), `parent-head` (the 17 consumer gates, the
  gitlink, the submodule HEAD and the parent diff stat), `newarms` (the 16 lock controls
  on their own, with each control's log), `hand` (the hand-planted runs, their patches
  and the post-restore `git status`), `try` (the pre-commit suite runs and `make
  check`/lint/matrix), and `scripts` (the scripts that ran them). The two round-1b logs
  over 200 KB (parent pp_shadow and milan_dp) are listed in `OVER-200KB.sha256`.
- `receipts/INDEX.md`: generated from the files present by
  `receipts/r1c/scripts/receipts_index.py` (the round-1b script, unchanged), with each
  file's size and sha256: 897 files, 11 over 200 KB listed. Round 1b's index had 526
  files and 6 over 200 KB.
- `try/pp_top.log` is the second pre-commit pp_top run (rc 0). The first one failed RN
  (`6 of 2211 frame comparisons diverged`) because the model still predicted flags 0 on
  the automatic unlocks. That run led to the RN and TD1 updates, and its log was
  overwritten by the rerun.

## Tool identities

Round 2 used the same binaries, checked again at its start (`receipts/round2/` logs
print the Verilator, sv2v and Yosys versions).

- Verilator 5.050 (`verilator --version`: "Verilator 5.050 2026-07-01 rev v5.050"), the pinned
  wrapper exported first on PATH. The host default, 5.052, was not used.
- sv2v 0.0.12 (`--numeric-version`), sha256 b29952bc8f400ca90207507db0ff6763263e03d3eec711da80338430ed636b9b.
- Yosys 0.33 (git sha1 2584903a060), CI's ubuntu apt build, sha256
  88c0a12bb814a1a8716b1ae10b482e35d3005ed558e1f5f626b3dc983ea3abd0, used for
  `syn/yosys/run.sh` and the elab-guard grading. The host Yosys 0.66 (sha256
  ec566d8f...b5b) was also run as a second record.
- Vivado 2026.1 xvlog, used only by the parent's `xvlog_gate.py`, under
  `flock $VIVADO_LOCK` (exclusive).
