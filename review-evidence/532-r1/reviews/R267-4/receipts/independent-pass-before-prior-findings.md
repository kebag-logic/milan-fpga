# R267-4 independent pass, written before reading any prior review finding text

Head 022290e4c94a23b9ee97852b6c1c2ee2c1f25352, tree b9740a963ee3833cfe7d7be986ef6233ba033d1c.
Sources read up to this point: AGENTS.md, issue #532 body and its public
comments (assignment, DECISION, REVIEW READY records), the round diff
604297bb..022290e4 and the full head act_slot_proof.sh, the memory-cap code and
arm in scripts/act_ci.py, and docs/testing/CI_WORKFLOWS.md lines 1810-2053.
My own round-3 mutant scripts were taken from evidence commit d2352cdd (bin/ and
evidence-copies/ only); the round-3 report was not opened.

## Round scope (receipts/diff-scope-604297bb-022290e4.txt)
- act_slot_proof.sh lines 1-365 (every live check, `prove`, the ten records) and
  `main` are byte-identical to 604297bb; changes are the stand-in runner, the
  stand-in sudo and the case table only.
- act_ci.py: one fixture row in `selftest_slot_memory_cap`; nothing else.
- CI_WORKFLOWS.md: three paragraphs (cap count routine, case list, stand-in
  timing, unstaged guard reason) and the runner-pin bullet.
- No workflow file, no check_baremetal_only.py change in the round.

## Independent observations
1. The four one-sided overlap cases each leave exactly one overlap condition
   false at the head, and each one kills exactly its own conjunct mutant alone,
   in natural, forced A-first and forced B-first start order, as uid 1000 and
   uid 0 (receipts/one-sided-probe-*.txt: 12 head passes, 12 kills per mode).
2. The "never overlap" case alone is order-dependent (receipts/overlap-order-
   probe-022290e4-user.txt); the doc says so.
3. Slot B's isolation (slot2-reaches-container), slot B's verdict
   (parallel-break-b), the network-query failure and the container-query
   failure each kill their mutant (Q62, Q61, Q53, Q52) in every run.
4. The new runner arm (oom 1, oom_kill 0, oom_group_kill 0) is the only arm
   that kills S04, S07 and S10; S00 survives.
5. Residual, not in the round's findings: the "neither run reports its own slot
   daemon" case's runs hold for the fixed FAKE_HOLD (3 s), so the kill of Q23
   (await_holder accepts the generic running marker for a slot) needs the two
   runs to start within 3 s of each other. Shown by
   receipts/unannounced-skew-probe-022290e4-user.txt (killed at 0 s and 1 s
   skew, survives at 4 s). Killed in every run here. The doc's "exception"
   sentence names only the never-overlap case. Classified SUGGESTION: the kill
   holds under ordinary and 8-way load, and the grading at the head is
   timing-independent.
6. Q32 (collision rival started without waiting for the holder) stays
   race-dependent; removing it cannot produce PROVED from the stand-ins, and
   the extra protection it gives (a third-party lock holder) cannot be staged
   without a timer. Accepted as documented residual.
7. The collision holder's fixed 3 s after its rival returns is the one timer on
   the honest path; 16 of 16 self-tests under 8-way concurrency and 6 of 6
   serial runs passed.
8. Doc case list maps 1:1 onto the 44 cases (1 honest, 7 bad starts, 6
   completion, 3 interrupt, 8 parallel, 12 isolation, 7 collision).

Provisional: no BLOCKER, MAJOR or MINOR; one SUGGESTION (item 5).
