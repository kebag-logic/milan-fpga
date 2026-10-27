# [A676e] processor #202 round 5 — HANDOFF

**Status: REVIEW READY. Every required gate returned 0; no STOP condition met.**
TAKEN: issue #202 issuecomment-6431125699. REVIEW READY: issue #202 issuecomment-6432105171.

Round-5 assignment: issue #202 issuecomment-6431105729, answering R710-3 (PR #204
issuecomment-6430017921, NEGATIVE, one MINOR) and the residue in R709-3 (PR #204
issuecomment-6431102177, POSITIVE). Scope: tests, mutant tables and documents only. **The RTL
is not changed** (`git diff 429c909 98e0137 -- hdl` is empty); the new check needed no RTL
change, so the STOP condition was not met.

## 1. Records

| Item | Value |
|---|---|
| Repository | Mister-M-alt/protocol-processor-control-plane-avb-milan (`git remote get-url origin` checked before the first commit; the merge base and `origin/main` were `ed211803`, and the checked-out start was the round-4 head `429c909`, as the assignment says) |
| Branch | `202-maap-conflict-new-stream-id` (local; not pushed) |
| Base (processor main) | `ed2118035e4cec76fb1b59cfbf8a053aeacc8af8` |
| Round-4 head (start) | `429c909cb8a60398a2028436932e04b95dd0a0bd` |
| Head | `98e0137cfaf07b3b3efd21d2bd19648762e86f2b`, tree `9fdc9864d6ad8a900403a0ba81969b028c8d8140` |
| Scratch parent | the committed local clone `pp202-parent`, new branch `scratch-pp202-a676e` from round 4's `2eb0139126` (dev `e76a755a` with the wiring), push URL invalid, never pushed (§6) |

Round-5 commits on `429c909` (one-line subjects, no body, no trailers):

1. `b2b2bfdb` Grade a quarantine record past its first epoch: in S5 src5 moves again 1 ms after an epoch ends, and the move after the wrap, 10 s after src5 left its first ID, must skip it; plant its age-1 overwrite as an arm (issue #202)
2. `83c2eeff` Name the quarantine by the longest T-SRP-LEAVEALL2 in 02, 05 and 09 rather than copy its 30 s, grade the record keep in both epochs in the 09 row, and name MP9's SRP talker FSM by its commit (issue #202)
3. `98e0137c` Record S5's one-epoch record case, the age-1 overwrite arm and the talker, ACMP and talker retry counts re-measured at b2b2bfd (issue #202)

`b2b2bfd..98e0137` changes documents and two test READMEs only, so every suite and campaign
input at the head is that of `b2b2bfd`, where the sweep and the campaigns ran
(`receipts/records/base-head-records.txt`).

## 2. What each item asked, and what was done

| Item | Done | Where |
|---|---|---|
| R710-3-F01 (MINOR): the record-keep rule is graded only inside the record's first epoch; the age-1 overwrite plant passes all 1,540 talker checks | S5 now has a fourth source (src5) whose second move comes 1 ms after an epoch boundary and 10 s after its first move, inside the record's second epoch; the move after the wrap, 10,056 ms after src5 left `...0B`, must skip it. New named check `S5 a record one epoch old is kept when its source moves again, so the ID it holds is not taken inside the quarantine`, tagged REQ-ACMP-010. The plant re-declares `...0B` with another DA 10,056 ms after its withdrawal, so S5's 35.2.2.8 history check fails too | §3 rows 1-2; §4 |
| — the plant as a named `STREAM_ID` arm | `record_overwritten_after_one_epoch` (the reviewer's substitution `!= 2'd2` → `== 2'd0` at `KL_acmp_talker.sv:1470`), named checks: the new one and `S5 no ID is declared again with another DA inside two LeaveAllTime periods`; KILLED, 3 failing checks | §3 row 3 |
| — README mutation records and the 09 row | `tb/pp_top/README.md` table row, re-measured counts, 33 of 33 and 98 of 98; `tb/acmp_talker/README.md` S5 row, count, arm list and the retry record; 09 §8.13 row | §3 rows 4-8 |
| — `probes/run_plant.sh` with the reviewer's plant | at `98e0137` (a `git archive` export): suite rc 2, the new named check FAILs (with the two other S5 checks), 1,545 checks, 1,542 PASS; golden rc 0, 1,545 PASS. The same plant at `429c909`: rc 0, 1,540 of 1,540 PASS (R710-3's finding) | `receipts/tests/reviewer-plant/` |
| R710-3-R01 and R709-3 RESIDUE-1 (the same line, `tb/pp_top/README.md:2076-2077`) | The two exact texts differ for the same words: R710-3 "on the SRP talker FSM before the leave copy (`ebb1f001`)", R709-3 "on the SRP talker FSM at `ebb1f001`". Both remove the round and name the commit; one line cannot carry both verbatim. It now reads "on the SRP talker FSM at `ebb1f001`, before the leave copy, the Lv never goes out (frames -1, 0)": R709-3's words with R710-3's "before the leave copy" | §3 row 9 |
| R709-3 RESIDUE-2: the quarantine's 30 s copied outside F08.1 | applied as written: 02:304 and 02:567 "within the longest `T-SRP-LEAVEALL2` (the [quarantine](05_acmp_engine.md#sec-05-sidq))"; 09:800 "within the quarantine"; 05:528-529 "A LeaveAll period is at most the longest `T-MRP-LEAVEALL` (F08.1), so the quarantine *Q* is the longest `T-SRP-LEAVEALL2`." The PR comment shows the link as an absolute evidence-repository URL; the reviewer's own published report (`REPORT.md`, evidence commit `cedb425a`) has the relative `05_acmp_engine.md#sec-05-sidq`, which is what the fix means (`receipts/records/r709-3-residue-source.txt`). `grep -n "30 s" docs/architecture/0[25]*.md docs/architecture/09*.md` now shows no quarantine hit (05:298, 05:310 and 09:534 are other timers); the integrator guide keeps "30 s", as R709-3 allows | §3 rows 10-12 |
| Gates: the talker and processor-top suites, `acmp_mutants.py`, `make check`, the parent patch unchanged and applying cleanly | all rc 0 (§5, §6); the patch is byte-identical (sha256 `e3991176…f1fa`) and applies cleanly to dev `e76a755a` | §5, §6 |
| R710-3-S1 to S4, R709-3 SUG-1 to SUG-4 | not taken (suggestions, outside the assignment). The PR body's latency note now says what S1 says: a conflict re-open can meet the park through LO and then waits one more `T-MRP-JOIN` | `PR-BODY.md` |

## 3. Changes (file:line at head, clause)

| # | File:line | Change | Clause |
|---|---|---|---|
| 1 | `tb/acmp_talker/sid_cases.hpp:61-63, 80-82, 437-443` | `Q_MS` (the quarantine and its epoch length); `count_to`, which steps the timebase one millisecond per clock so each epoch ends exactly *Q* after the last | 802.1Q-2018 35.2.2.8; 05 `sec-05-sidq` |
| 2 | `tb/acmp_talker/sid_cases.hpp:327-353, 364, 391-405, 416-426` | S5: src5 moves at the start (to `...0B`); the epoch grid from reset (100 ms; every step is 5 ms or 1 ms); near the end src2's two moves 1 ms into an epoch, src5's first move 10 s before that epoch ends and its second 1 ms after, src1's move; the after-wrap expectation `...0C`; the new check, REQ_TAG REQ-ACMP-010 | 802.1Q-2018 35.2.2.8; REQ-ACMP-010 |
| 3 | `tb/pp_top/acmp_mutants.py:577-584` | arm `record_overwritten_after_one_epoch` in `STREAM_ID` | — |
| 4 | `tb/pp_top/README.md:2090-2092, 2097, 2100, 2105, 2115, 2121-2122` | re-measured failing-check counts of six arms (one or two more each: src5's four `move_once` checks), the new arm's row, 33 of 33 and 98 of 98 at `b2b2bfdbe878` | — |
| 5 | `tb/acmp_talker/README.md:8` | 1,545 checks | — |
| 6 | `tb/acmp_talker/README.md:385` | the S5 row | 802.1Q-2018 35.2.2.8 |
| 7 | `tb/acmp_talker/README.md:403-409`, `:240-244, 274, 276, 277, 279` | the arm list; the talker retry campaign re-measured at `b2b2bfdbe878` (same 62 killed, 7 equivalent, 1 performance; four with more failing assertions; baseline and restored 1,545) | — |
| 8 | `docs/architecture/09_verification.md:809` | the quarantine row: the record kept in its first epoch and, past an epoch boundary, in its second; the new arm | REQ-ACMP-010 |
| 9 | `tb/pp_top/README.md:2076-2077` | MP9's SRP talker FSM named by its commit | R710-3-R01, R709-3 RESIDUE-1 |
| 10 | `docs/architecture/02_interfaces.md:303-306, 567` | "within the longest `T-SRP-LEAVEALL2` (the quarantine)" | R709-3 RESIDUE-2; docs/README §2 |
| 11 | `docs/architecture/05_acmp_engine.md:528-529` | *Q* defined from F08.1's rows, no value copied | R709-3 RESIDUE-2 |
| 12 | `docs/architecture/09_verification.md:800` | "within the quarantine" | R709-3 RESIDUE-2 |

## 4. New check, planted mutant, failing words

Talker suite 1,540 → 1,545 checks: src5's `move_once` adds four (consumed, status/tuple,
declaring, re-declared at the grant) and the new check one. S5 runs 65,520 moves of src0 to the
wrap (65,523 before: the three extra cursor IDs the src5 moves take).

| Check (words as printed) | Killed by (planted defect): failing checks |
|---|---|
| `S5 a record one epoch old is kept when its source moves again, so the ID it holds is not taken inside the quarantine (got ab0000000000000b 10056 ms after src5 left ...0B)` | `record_overwritten_after_one_epoch` (`sid_rec_age_r[ev_src_r] != 2'd2` → `== 2'd0` in the record write, R710-3's plant): 3 FAIL, the other two `S5 no ID is declared again with another DA inside two LeaveAllTime periods (1, first ab0000000000000b after 10056 ms)` and `S5 after the cursor wraps a move skips every configured ID, ... (got ab0000000000000b after 65520 moves)` |

The earlier record arms keep their kills: `record_overwritten_while_young` and
`record_lapses_in_one_epoch` fail the after-wrap check alone (`...09`, src2's record, is taken
first), and `move_ignores_left_ids` the after-wrap and the history checks; none of them fails
the new check. The new arm keeps src2's age-0 record and loses only src5's age-1 one, so the
move after the wrap takes `...0B`, which only the new check, the history check and the after-wrap
check see.

## 5. Processor gates (every `.rc` is the command's own exit status, never through a pipe)

Local tools: Verilator 5.052 (CI pins 5.050) through a PATH wrapper that turns a build's `-j 0`
into `-j 2` to `-j 8`, so concurrent runs share the unit's 16 CPUs; results do not depend on it.
Every gate ran in a disposable clone or export, never in the lane tree.

| Gate | Round-4 head `429c909` (round-4 record) | This round |
|---|---|---|
| `./scripts/run_suites.sh` (REQ_TAG_LOG set) | rc 0, 1,030,588 (at `ffc76f17`) | rc 0, 1,030,593 checks, 0 failing, at `b2b2bfd`; only `acmp_talker` moves, 1,540 → 1,545 |
| `check-req-tags.py --suites … --evidence …` | rc 0, 245 tags | rc 0, 246 tags in 20 files, 246 evidence lines, 14 suites |
| `make check` | rc 0 | rc 0 at `98e0137` (links 1,257, req-tags 246, ids, figures, matrix, parameters) |
| `./scripts/lint_hdl.sh` | rc 0 | rc 0 at `98e0137` (RTL unchanged) |
| `tb/acmp_talker` | 1,540 | rc 0, 1,545 at `98e0137` and in the sweep |
| `tb/pp_top` | 10,753 | rc 0, 10,753 in the sweep at `b2b2bfd` and again at `98e0137` |
| `tb/pp_top/acmp_mutants.py` (`--jobs 4`, at `b2b2bfd`) | 97 of 97 | rc 0, **98 of 98 KILLED**, eight goldens PASS; `STREAM_ID` 33 of 33 (30 names). Against round 4 only seven `STREAM_ID` rows move (six counts, one new arm) |
| `tb/acmp_talker/retry_mutants.py` (`--jobs 4`, at `b2b2bfd`) | 62 / 7 / 1 | rc 0, 62 killed, 7 equivalent, 1 performance control, baseline and restored 1,545; 59 of 59 retry assertion sites with a killed witness; four mutants with more failing assertions (README re-measured) |
| reviewer's `probes/run_plant.sh` (plant, golden) | plant survives (1,540 PASS) | plant: suite rc 2, new check FAIL; golden rc 0 |

No other campaign builds a changed file: the RTL, `tb/pp_top`, `tb/srp_*` and `tb/maap` are
unchanged, so round 4's SRP, MAAP, AECP, dispatch, counters, GET_STREAM_INFO, name-write,
notifications, D3, elaboration-guard and name-state campaign results at the same RTL stand.

## 6. Parent: the wiring patch and the final pin

`parent-src-stream-id-wiring.patch` (this directory) is round 4's file, byte-identical: sha256
`e399117609459a2e1b9e8ea22f7c87b0edd118a86ce56bcde67fbc5e92fbf1fa`, 70,077 bytes. Regenerated
from the scratch parent (`git diff 309af35f59 d3ab5b37f5 -- . ':(exclude)protocol-processor'`)
it has the same digest. On a fresh checkout of dev `e76a755a`, `git apply --check --index` and
`git apply --index` return 0, and the result equals the scratch parent's wiring commit
`d3ab5b37f5` outside the gitlink (`receipts/records/patch-check-dev.txt`).

Scratch parent branch `scratch-pp202-a676e` (from `2eb0139126`), push URL invalid, never pushed:
`f080fff704` pins processor `98e0137`; `61298744b7` records its ROM digests. HEAD `61298744b7`,
tree `7ecaff2ebc`, status clean (`receipts/records/PARENT-STATE.txt`). Dev `e76a755a` with the
patch applied and the gitlink set to `98e0137` differs from `f080fff704` only in the ROM-digest
record, which the scratch parent adds per pin (`receipts/records/patch-check-dev.txt`).

| Final pin (processor `98e0137`, parent `f080fff704`) | Result |
|---|---|
| processor consumed inputs `hdl`, `scripts`, `syn`, `Makefile` between `429c909` and `98e0137` | empty diff |
| ROM-digest record (`./syn/yosys/ooc.sh --record-rom-digests`) | rc 0; digests for `98e0137`, the same ROM contents as `429c909`'s |
| `pp_shadow` and its verdict | rc 0; 2,187 checks, 0 failures (four tallies); verdict rc 0 |
| recovery leg `sidmove` (AX 1x1, AAF talker 0 and the CRF output) and its verdict | rc 0; 50 checks, 0 failures; conflict to the new ID's declaration 1,735 ms for both graded sources; verdict rc 0 |
| recovery leg `sidmove8` (8x8, AAF talkers 0 and 1) and its verdict | rc 0; 52 checks, 0 failures; 1,816 ms for both; verdict rc 0 |
| out-of-context `./syn/yosys/ooc.sh KL_pp_shadow` | rc 0; 61,219 LUT, 4,332 LUTRAM, 28,334 FF, 15 RAMB36, 4 RAMB18, 10 DSP, 2,428 CARRY4 (round 4's figures) |

In that run the two legs' Verilator models were up to date (the processor sources at `98e0137`
are byte-identical to `429c909`'s, so the build reused round 4's objects). Both legs were then
built again from scratch at the same pin, into fresh object directories outside the parent tree
(Verilator: 121 modules each, 22 and 25 C++ files compiled), and passed again: rc 0, 50 and 52
checks, 0 failures, 1,735 ms and 1,816 ms, verdicts rc 0; the parent's status stayed clean
(`receipts/parent/final-pin/fresh-build/`).

Round 4's whole consumer gate (`pp_shadow` 2,187, `maap` 251, `milan_dp_render` 347,
`milan_dp` 13,685, `capture_coherence` 43 cases, the static gates; all rc 0) ran at processor
`ffc76f17`, whose consumed inputs equal this head's.

## 7. Completion

R710-3-F01 is answered with a check that fails on the reviewer's plant and passed at `429c909`,
a named arm that the driver kills, and the README and 09 records; the residues are applied
(§2 for the one line two reviews worded differently). Every required gate returned 0: the
talker and processor-top suites, `acmp_mutants.py` (98 of 98), `make check`, the full sweep with
the requirement-tag evidence, lint, the talker retry campaign, and the parent patch unchanged and
applying cleanly, with the scratch parent's final pin passing `pp_shadow`, both recovery legs and
the out-of-context check. The processor tree is clean, ignored files included; the scratch
parent is committed at `61298744b7` with processor `98e0137` as its gitlink. No push, PR
creation or edit, merge, rebase, hardware operation, RTL change or top-level interface change
was performed.

Resources: one service unit of 16 CPUs; no CPU range was free for shard units (`cpu_ranges.py
pick` returned 1), so the sweep and the campaigns ran inside the unit with MemoryHigh 9 GiB. Its
sampled `memory.current` (page cache included) peaked at 6.09 GiB; the host's MemAvailable
stayed at or above 29.8 GB (`receipts/records/resources.txt`).

## 8. Receipts

`INDEX.md` and every `receipts/**/INDEX.md` are generated from the files present.
`receipts/gate-status.json` lists the 21 accepted return-code records (all 0) and the reviewer
plant's runs (rc 2 at `98e0137`, rc 0 at `429c909`). Files over 190 KB are kept as their size,
sha256 and last 80 lines, and `receipts/RAW-RECORDS-*.csv` list every raw record with its size and
sha256 (the ACMP campaign's 313 KB `results.json` is summarized in
`receipts/campaigns/acmp-results-summary.tsv`, with the new arm's record whole in
`acmp-record_overwritten_after_one_epoch.json`). Local paths in receipts are normalized.

| Receipt | What it holds |
|---|---|
| `receipts/processor/sweep-b2b2bfd/` | the sweep log, its rc, the req-tag evidence and its check |
| `receipts/processor/final-head/` | lint, `make check`, the talker and pp_top suites at `98e0137` |
| `receipts/campaigns/` | the ACMP and talker retry campaigns (logs, rcs, per-arm logs) |
| `receipts/tests/reviewer-plant/` | `run_plant.sh` at `98e0137` (plant, golden) and at `429c909` |
| `receipts/tests/first-runs/` | the first runs on the working tree before the first commit (not gates) |
| `receipts/parent/final-pin/` | the scratch parent's final pin |
| `receipts/records/` | base and head records, the parent state, the patch check, the probe files' provenance, R709-3's residue text as published, resources |
