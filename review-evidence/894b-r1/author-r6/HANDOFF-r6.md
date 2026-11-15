# HANDOFF — lane 894b (8x8/1if follow-up of #894), round 6, [A781]

Status: REVIEW READY at `af2c4d7a` (comment text `REVIEW-READY-COMMENT.md`, posted once on #894 as issuecomment-6895387328). PR text `PR-BODY.md`.
Nothing pushed; no PR created or edited.

- Start head: 0700f09e (round 5's STOP head), tree clean, verified 11:24 CET. Final head: af2c4d7a (the pass at
  f8ea6d72 found four comment lines; see item 5).
- Assignment: #894 issuecomment-6892938049 (round 6, on round 5's STOP issuecomment-6892905117), with the manager's
  notes: sync onto origin/894-tiers 4ae887a1; 8x8/1if images identical to round 5's measured ones (else measure
  again); item 2 (the held-egress ledger derived by the tool from the 60 ms hold plus the service +5 %); item 4
  (8x8/1if's own ADP record, 130 us); item 6 (an image past its ledger entry reported, not a STOP); the final pass;
  one REVIEW READY or one STOP.

## Items

1. Sync 4ae887a1. — DONE `5aadbc8c` (three doc/comment conflicts: my 8x8/1if text kept, #902's figure updates
   taken: poll_grade's SRP record cost 280, the srp README's 33.38 ms at 950 us, FR_NFR's past tense for 125.84 ms).
2. The ledger restated by rule (own commit), controls, section 13. — DONE `6bf90e0d` (amended once before any push
   to wrap one 121-column line the idiom gate refused; the first form e37970d6 never left this machine).
3. 8x8/1if's own ADP record (own commit), control, the load. — DONE `f8ea6d72`.
4. Images vs round 5's measured (the carry) and vs #902's for 1x1/8x8-2if. — DONE: all 8 at 5aadbc8c identical to
   round 5's measured a15345f7's (ELF and loadable), so the measurement carries; the six fixed identical to
   4ae887a1's. Round 5's measurement regraded at f8ea6d72's graders: gate PASS, survey 0 exceeded.
5. Final pass. — DONE at af2c4d7a, every gate as required (the gate table below). The first, at f8ea6d72, stopped at 11:4x: lane part a's comment scans (against 7398ec0a and
   4ae887a1) each found four new source-comment lines naming a review round (egress_ledger.py:13, :64, :246;
   load_grade.py:120). Fixed in `af2c4d7a` (the ledger ruling named by its subject and items; section 13 links it);
   the five running units stopped by exact name, the scratch recreated, the pass relaunched at af2c4d7a at 12:07.
6. REVIEW READY or STOP. — REVIEW READY (no STOP condition; below).

## Changes (file:line at af2c4d7a, reason)

- **`af2c4d7a`**: four comment lines in `egress_ledger.py` and `load_grade.py` name #894's ledger ruling by its subject
  and items, not by a review round; section 13's list of the rulings the comments name links it.

- **`egress_ledger.py`** (item 2): `HOLD_MS` read from `scenario.py`'s backlog-owed hold (`hold_ms`, the `wait cycles
  {60 * MS}` before `txready 1`); `MEASURED` the merged image's measurement (round 5, a15345f7, arm A's backlog-owed,
  to 10 ns); `figure()` the hold plus the service plus 5 %, rounded up to 0.01 ms, in integer 10 ns units; `LEDGER`
  derived. The tool's output: 63.40, 63.64, 63.93, 64.16, 64.41, 62.30, 61.94 ms. Self-test: section 13's table
  equals the tool's (four columns: round 3's, round 5's, the ledger), the derivation equals an independent Decimal
  one, the hold is the scenario's and a planted 59 ms hold is read as 59; 35 controls in process and as a process
  (one cycle over each restated figure exits 1 naming it; a new miss exits 1); 13 mutants (no 5 %, the 5 % on the hold
  too, a measurement the ledger does not derive from, a hold not the scenario's, and the earlier nine).
- **Section 13** (the table regenerated from the tool's output; both measurements; the attribution to #902's merged
  code with the bare merge `647d5c4a`'s identical figures; the rows stay recorded misses, a later restatement only by
  ruling for growth reproduced at a ruled upstream head); FR_NFR 3.4.1; the harness README.
- **`load_grade.py`** (item 4): `OWN` / `OWN_MEASURED`: 8x8/1if's own ADP record 130 us (12,210 cycles, arm A's
  backlog-adp-refill); `stated()` takes a NEAREST point's own figure where the nearest's is under it (the #32 column's
  125); `own_findings` in `--check` holds each own figure to its measurement by the rule and every column at or over
  it; `own_controls`: the own record left out (125 supplies it) and stated at 125, each refused by name (28 of 28).
  8x8/2if's table untouched. Load at 8x8/1if 0.711 at the pin, 0.673 with tsn-c-stack#32.

## Gate table (at af2c4d7a, each job on its own clean clone)

| Check | Result | Receipt |
|---|---|---|
| Lane gates, parts a, b and c (lane_gates_r6.sh) | 65 of 65 as required, three by design `_exits_1`; both comment scans and R844-1's audit 0 lines; each clone clean | `gates/lane-gates-af2c4d7a.txt` |
| Every hosted job step of rtl-fast, rtl, elaborate and docs (run_wf.py, verify_wf.py) | 139 run rc 0, 226 not run with a reason, 0 bad | `gates/workflows-verify-af2c4d7a.md`, `gates/not_run.json` |
| The firmware jobs | every step rc 0; control 716, AECP 302, SRP 345, unit 77/32/18 and verilator 193 [ok] lines, 0 escaped; boundary PASS | `firmware/firmware-jobs-af2c4d7a.txt` |
| counters-f5 | rc 0 at both shapes, the clone clean | `firmware/counters-f5-af2c4d7a.txt` |
| The sweep, four shards on picked ranges | exit 0 each, 65 suites, 2,713,040 checks, 0 failures, 0 SKIPPED (the first attempt: an environment race) | `gates/sweep-shard{0..3}-af2c4d7a.txt`, `gates/sweep-first-attempt-af2c4d7a.txt` |
| plat_ledger.py --self-test (item 6) | PASS at four points, 7 of 7 controls; no image past its entry | `gates/plat-ledger-af2c4d7a.txt` |
| Images (Q-img) | all 8 identical to 5aadbc8c's (round 5's measured); the six fixed identical to 4ae887a1's | `images/` |
| Round 5's measurement regraded at af2c4d7a's graders | gate PASS (held-egress rows under their derived figures by 0.094-0.219 ms); survey 0 exceeded; rows by every source reported | `harness/`, `model/` |
| Controls | egress_ledger 70 PASS lines, 13 of 13 mutants; gate_r5 21 of 21; load 28 of 28; record classes 13 of 13 | `gates/` |

## The STOP test

None fires: no measured CPU-decided row over its bound, the load 0.711 (0.75); no held-egress row over its derived
figure, no new miss; no 1x1 or 8x8/2if image changed (Q-img); joins 187.397-190.147 ms, slices within 147,500
cycles, no THE RETRY round over its statement; no donor or submodule path differs from 4ae887a1 or 98c0b62b.

## Run history (CET)

- 11:2x start; round 6's ruling read; HEAD 0700f09e clean, no units.
- 11:25 merge 4ae887a1 (5aadbc8c); quick graders PASS; images at 5aadbc8c and 4ae887a1 (clean clones) built.
- 11:26-11:31 items 2 (6bf90e0d) and 4 (f8ea6d72); regrade of round 5's measurement PASS; survey 0 exceeded.
- 11:33 the final pass at f8ea6d72 (launchC.py, label 894b-r6: the sweep's four shards each on a picked 8-wide range
  once four are free; the queue's 20 lines on picked ranges or the session CPUs, at most 4 there).
- 11:4x lane part a's comment scans exit 1 on four comment lines of mine; the five running units (r6-launch,
  r6-lane-a, r6-lane-c, r6-W-fw-control, r6-W-rtl-fast) stopped by exact unit name; no unit or process left.
- 11:5x-12:06 the four lines reworded, section 13's link; quick checks rc 0 (both comment scans 0 lines, R844-1's
  audit 0, py idiom, docs_check, load 28/28 and --check, egress_ledger 13 mutants, record classes 13/13);
  commit af2c4d7a; the old pass's launch log and lane logs kept under the scratch's r6/old-fullR6-f8ea.
- 12:07 the final pass at af2c4d7a (launchC.py, label 894b-r6b, units r6b-*), the same layout.
- 12:1x the regrades redone at af2c4d7a's graders on the clean clone: the gate (byte-identical to f8ea6d72's), the
  survey, the rows by every source, the ledger's derivation and gate_r5's controls, each identical; their receipts now
  carry af2c4d7a's name and the f8ea6d72-named ones are gone. One correction: the f8ea6d72-named egress_ledger
  self-test receipt had been captured before the 13th mutant ("the hold not the scenario's") was added and shows 12;
  af2c4d7a's shows 70 PASS lines and 13 of 13 mutants.
- 12:47 the sweep's four shards launched on picked ranges 0-7, 8-15, 16-23, 24-31; 12:53 they had ended, each
  exiting 1 with 10 to 15 suites refused by Verilator itself ("VERILATOR_ROOT is set to inconsistent path"): the
  spec's first PATH entry, another lane's shared pinned-tool directory, did not exist then (that directory was
  created again at 13:13:38, its birth time), so `verilator` resolved to the host's 5.054 beside the pinned
  VERILATOR_ROOT. An environment race, not the head: no other job of the pass reads that directory (they use the
  lane's own pinned 5.050) and no other log has the error. The failed shards' logs kept (fullR6/sweep-b-failed),
  their four clones removed (mine, unused, at af2c4d7a).
- 13:22 the sweep again (label 894b-r6c, its own launcher r6c-launch with no queue lines, on four picked ranges once
  free), its PATH a private tool directory under the scratch whose three files (the Verilator 5.050 wrapper and the
  two python wrappers) are byte-identical to the shared directory's and the wrapper to the lane's own pin.
- 13:20 Q-img rc 0: all 8 images at af2c4d7a identical to 5aadbc8c's (round 5's measured), the six fixed identical
  to #902's 4ae887a1's (receipts/images/). 13:22 counters-f5 rc 0 (both shapes clean, the clone clean).
- 13:2x added to the pass: plat_ledger.py --self-test (the platform image at the ledger's four points against the
  memory ledger, which no hosted job runs; item 6 is about it, and lane_gates_r6.sh did not carry it). 13:31 PASS,
  0 findings, 7 of 7 controls; 8x8/1if 56 of 56 RAMB36, ctrl_plat 18,176 B at its entry. No image past its entry,
  so item 6 has nothing to report (receipts/gates/plat-ledger-af2c4d7a.txt).
- 13:36-13:46 lane part c, firmware-verilator and both elaborate jobs rc 0; the queue's last unit ended 13:45:47.
  verify_wf over rtl-fast, rtl, elaborate and docs: 139 run, 226 not run with a reason, 0 bad (no workflow file changes
  since 98c0b62b, so round 4's table). Receipts: lane gates 65, 0 bad; the firmware jobs; counters-f5; not_run.json.
- 13:45 the sweep's rerun launched on 8-15, 48-55, 56-63, 88-95. The first attempt's receipt
  (gates/sweep-first-attempt-af2c4d7a.txt): each shard passed its first 2-4 suites, then failed; 50 of the 52 failing
  suites print the refusal, nvm_cosim's and gptp_shadow's builds failed without it. gptp_shadow passes in the rerun
  (9 controls, 0 failures).
- A slip of mine at 13:52: a recursive search over every lane's directory on the lanes' disk for the refusal, which I meant to
  scope to my own shard clones. It went to the background; my process listing to stop it by PID did not find it (a
  wrong match on its arguments, not its absence), so I wrongly took it as ended. It ended on its own at 13:57, read
  only, matching nothing. Nothing was killed.
- 13:5x nvm_cosim, the other suite whose first-attempt failure printed no refusal, passes in the rerun (465
  checks, 39 of 39 mutants killed).
- 14:39-14:52 the sweep's shards 3, 1, 0, 2 exit 0: 65 suites (15, 17, 17, 16), 2,713,040 checks, 0 failures, 0
  SKIPPED, round 3's totals to the check (receipts/gates/sweep-shard{0..3}-af2c4d7a.txt).
- 14:5x before posting: #894 read for comments after the ruling. #902's [A773] posted REVIEW READY at 26898c05
  (10:39) and 41ca9f87 (11:27); origin/894-tiers is at 41ca9f87 (fetched read-only). Its three commits since 4ae887a1
  are comments, docstrings and documents; a merge conflicts in FR_NFR.md and aecp_mbx.h's comments. Not merged (the
  notes pin 4ae887a1); stated in the comment and the PR body for the manager's relay.
- 14:5x REVIEW READY posted once on #894 (issuecomment-6895387328); the posted text equals the file but for one trailing blank line. Nothing pushed.
