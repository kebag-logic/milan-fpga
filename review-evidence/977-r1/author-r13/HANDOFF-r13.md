# #977 round 13 handoff

**Status (2026-11-28 01:52 CET):** REVIEW READY at `4461d77ca34ec1203321821a3313071ff1923984`, with tsn-c-stack `5a07d9b7` and lwSRP `e27b34c9`, both unchanged. The tree is clean, and nothing is pushed or posted.
- R958-4-F2: the per-record re-extraction leaves the maximum unchanged (160/200 us), so DELIVERY_US and its floor stand. The 8x8/1if load is 0.78214, within 0.79, so there is no STOP.
- Every gate passes, and every product ELF is byte-identical to 25ff0632's (80 of 80).
- The 0.79 ceiling, `4461d77c`, is last and droppable, citing "owner decision pending".

**ETA:** done. Next, the manager publishes:
- REVIEW-READY.md, PR-BODY.md and receipts/;
- the two supersession files, beside the round-10 and round-11 indexes.

The owner's answer on 0.79 is outstanding (R958-4-F1).

## Commits past 3256d1d2

- `831ffe10` reverts the 0.79 ceiling commit `3256d1d2`. R958-4-R1 changes a line that commit added (`flip_grade.py:66`), so the ceiling has to be restated last for a single `git revert` to keep dropping it.
- `48c7481a` R958-4-F2 and R1:
  - The deliveries comment and the design document state that each record is taken from its own tagged receive commit (44 at each point), that transmit probes are not records, and how missing or ambiguous records are refused.
  - The source comments cite "#977, the manager's decision of 2026-11-27 on deferred deliveries", not the comment ID.
- `4461d77c` the 0.79 ceiling restated, owner decision pending. Its content is `3256d1d2`'s apart from the flip comment's citation wording. It is last, and its reverse applies cleanly.

## Log

- 00:59 resumed at 3256d1d2 (tree clean; no helper units). Read R958-4 (7230559804, NEGATIVE) and R957-4 (7230545660, POSITIVE).
- 01:01 survey: each record in the burst group's logs has exactly one RXS-tagged commit on SRP's channel (4), equal to the group JSON's start_sys. The srp.register_tx probes tag no frame; their start is the triple's last record's commit. The plain s-srp-register group (its only record is an advertise) had been missed by round 12's s-srp-register-* glob.
- 01:02 tools/deliv13.py: records by tag and channel, refusals, aliases, and --selftest (8 of 8 controls hold, including the queued triple's three distinct commits, the later-window excess, and the old rule taking 10000 three times).
- 01:03 re-extraction from the existing r10d logs, 20 logs a point (10 groups, both arms): 44 records a point, 44 distinct group/commit pairs, 6 aliases excluded, none refused. Against round 12's 22 distinct: +12 later burst records, +8 setup advertise records (deliv12 skipped _advertise by name), +2 of the plain group. The maximum is unchanged: 8x8/1if 15,104 cycles a sink, 160 us (answering-ports swap); 1x1/1if 18,778, 200 us (answering-ports both-owed); beside it 125/145 and 190/200 us. Inside a triple the three records' windows coincide: their commits are 81 cycles apart, before the pass that takes all three.
- 01:04 831ffe10, 48c7481a, 4461d77c. load --check PASS, --selftest 32/32, load_deliveries every control refused; flip --check at 1x1/1if and 8x8/1if PASS, --selftest 628/628; 0.790 passes, 0.791 fails. `git diff --check` is clean against 71bad8c0 and 0b594023.
- 01:05 started r13-elf and r13-gates. The clone r13/cR at 48c7481a shows the refusal path: the 8x8/1if flip check fails at 0.782 over 0.77.
- 01:06 R958-4-R2: wrote receipts/supersession-author-r10-index.md and receipts/supersession-author-r11-index.md, for the manager to publish beside the old indexes. The round-12 appends to the local round10/round11 INDEX.md files are superseded by these two files.
- 01:18 r13-elf done: plat_ledger PASS, 80 ELFs, every sha256 identical to 25ff0632's; receipts/elf-identity-4461d77c.txt. r13-gates still in run.py --self-test.
- 01:49 r13-gates done (clean clone cG at 4461d77c): harness self-tests all rc 0 (run.py --self-test 0 failures, kept 33, load 32/32 and --check, flip 628/628 and --check at 1x1/1if and 8x8/1if, shape_costs 25/25 and --check). The Python and C++ idiom gates pass; the docs workflow passes 100 of 100 with no tracked file changed.
- 01:51 receipts copied. Host paths in the run.py log and the docs steps were replaced by <clone>/<out>/<scratch>/<home>, and the run.py log gzipped; receipts/INDEX.md generated with a publication note. REVIEW-READY.md and PR-BODY.md written. Nothing removed: scratch r13/cE, cG, cR, oF and r12's are left in place.
