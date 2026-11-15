[A773] REVIEW READY
Commit: `234bc149` (PR #902, `894-tiers` -> `dev-soft-core`; fifteen commits on round 11's `9606b3a9`, rounds 12 and 13; the manager pushes)

Round 13, under #894's ruling issuecomment-6888782796 on round 12's STOP (issuecomment-6888749411). Round 12's cut, its pace stamp, its paced class, its four restatements and the drain fix stand.

Changed:
- **The slice is the rule's choice** (`c274b9f5`, its own commit).
  - `CTRL_LOOP_SLICE_US` is 950 us at one interface, 1,300 at two. `ctrl_loop.h` states the rule: the slice rule's choice within 650 to 1,100 us.
  - The self-tests hold the stated slice to `rows_tiers.ruled`. Their two anchors on the literal `900u` now read the header.
  - `CTRL_LOOP_BUILD_MOST` stays 1, since 950 is shorter than a build of both MRPDUs (1,010 us). No row moves through it.
  - Only the one-interface images change, in `ctrl_loop.o`, at equal sizes.
- **The reruns on the rebuilt images** (`c274b9f5`):
  - the full arm A at 1x1/1if: 96 groups, 0 refusals, the 7 known held-egress misses, 0 of 140,032 passes over THE SHARE;
  - the whole answering-every-port arm (16 groups): rc 0;
  - the answering-ports leg and C-R1: rc 0, SET_CONFIGURATION 28,376 cycles, unchanged;
  - the 8x8/1if legs: rc 1 on round 11's reasons. That point states one interface's costs: a build of one of 92,066 to 94,601 cycles against 73,500, a polls base of 20,580 against 20,500, and the 40-notice model.
- **The stated tables.** At 1x1/1if every one holds by the rule over every one-interface leg, by leg prefix, but for the class lines (paced 245 and 300 of 300; the largest legal notice 365 of 365). So nothing is restated, and the rule's choice does not move.
- **Carries.** The 8x8/2if legs were also run again: 6 of 6 harness ELFs and 166 of 166 two-interface image files are identical to round 12's by sha256.
- **Item 5: a late-acknowledged SET_CONFIGURATION cannot complete on the product port.** Shown, not staged (`receipts/item5-no-late-completion.md`).
  - `KL_mbx_cdc` takes a commit on its crossing's pulse with no backpressure, and acknowledges it within contract 2.3's 64 cycles.
  - The split composition measures 2 polls (`sim_split.cpp`, in the sweep).
  - `mbx_face_commit` outwaits the bound. So no interface is ever owed, and no change waits.
  - The fault path stays tested (`Face.ALateCommitIsOwedAndPublishedAgainWhole`).
- **A gate round 12 never ran.** Lane part a's `hooks_selftest` refused `ed0df35b` (27 of 28): the hooks harness's face plant anchored on the line round 12's cut rewrote. `234bc149` anchors it on the new line and keeps the stream flag referenced. It passes 28 of 28 checks, with 96 of 96 mutants caught.
- **The documents** (`ed0df35b`): section 13, FR_NFR 3.4.1, MAILBOX_SPLIT and the harness and SRP READMEs, at 950 us.

Every CPU-decided row at 1x1/1if holds by every source at the rule's slice:
- R4 13.10 (20), R4L 188.48 (238), ACMP 28.95, ADP 27.30 and MAAP 27.42 (30);
- the first queued notice 14.66 (20), R5 74.07 and R6 69.86 (90), the last queued notice 127.21 (130);
- tx 33.38 and txL 48.43 (49).
- The load is 0.516 at the pin and 0.512 in the second column, against 0.70.
- The pace is 8 ms.
- The slice rule chooses the built design (10 of 420 hold, +0.0116).
- Joins are 187.994 to 190.021 ms in arm A and 185.486 to 190.147 ms over every leg.
- Every image is within its cap; the 8x8/2if platform has 152 B spare.

Validation (clean clones, never piped):
- **Lane gates.** Part a at `234bc149`: 48 gates, rc 0 but the four that exit 1 by design. The harness self-test has 0 failures; `rows_tiers` refuses 1,033 of 1,033, flip 585 of 585, load 26 of 26 and record classes 11 of 11. Parts b and c at `ed0df35b`: rc 0.
- **Every workflow step** (`verify_wf.py` over `rtl-fast.yml`, `rtl.yml`, `elaborate.yml` and `docs.yml`, at `ed0df35b` and `234bc149`): 139 ran rc 0, 226 not run with a reason, 0 bad.
  - The AECP campaign catches 299 of 299 rows and the control campaign 716 of 716. The SRP campaign rc 0; `fw_coverage.py --check` PASS.
- **The four-shard sweep** at `ed0df35b`, each shard on its own picked range: every shard's command rc 0.
- **`record_classes.py` over every leg:** RESULT PASS.
- **`docs_check.py`, `check_em_dash.py`** and both idiom gates: 0 findings.
- **The carry.** `234bc149` differs from `ed0df35b` only in `hooks.py`, which no workflow job or sweep suite reads. Its one reader, lane part a's hooks self-test, ran at `234bc149`.

Acceptance criteria (the round-13 ruling):
- **Item 1** met: the slice is the rule's 950 us, in its own commit; the header states the rule, and the self-tests hold it.
- **Item 3** met: every one-interface leg, the compare, the pace and slice rules, the firmware jobs, the sweep and every gate, round 12's leftovers included.
- **Item 4** met: the 8x8/2if carry is shown by hash; nothing else carries without an identity proof of its inputs.
- **Item 5** met by the product-port proof.
- **Item 6:** 8x8/2if is reported. For #894's 8x8 lane and #890: R4 44.24, the last queued notice 806.60 and txL 459.40 ms, the load 0.794 and 0.754, and the paced class 595 us.
- **No STOP trigger fired:**
  - no 1x1/1if row is over its bound, and the load is 0.516;
  - the rule's choice did not move again;
  - the pace is 8 ms;
  - the joins are within 181 to 239 ms;
  - no image is over its cap;
  - item 5 has no cost.

Open risks/questions:
- **No arm stages a late-acknowledged completion,** since the product port cannot reach it. An SoC built with no datapath, the CPU harnesses' fixture, holds the acknowledgement idle, and there every change waits as the contract defines.
- **8x8/1if's and the 8x8 `srp` legs' exits** are reported as before (#910; the 8x8/1if lane).
- **The packet:** `894-a773/round13/` (PR body for rounds 12 and 13 with its finding table, receipts, INDEX).
