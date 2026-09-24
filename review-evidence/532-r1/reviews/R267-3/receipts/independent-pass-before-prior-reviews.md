# Independent pass, recorded before any prior review report or reviewer script was opened

Recorded: 2026-09-24T02:28:02Z, exact head 604297bb41d6c8005d07539289b10bfa99273cdd.
Sources read so far: AGENTS.md, CONTRIBUTING.md, issue #532 body and every issue
comment, the PR #533 body and the manager comments, the diff and history, the
evidence tree listing (names only).

Candidate findings (all MINOR):

- N1 [Tests, Docs] scripts/act_slot_proof.sh:275-276: `|| networks=unknown` has no
  self-test case; the stand-in sudo never fails `docker network ls`. Mutant Q53
  (a failed network query read as absent) survives as uid 1000 and 0. The doc
  (CI_WORKFLOWS.md:1972-1973) says a network that "cannot be queried after it"
  is staged, and :1979 names only two uncovered guards.
- N2 [Tests, Docs] scripts/act_slot_proof.sh:307-308 with the `serialize` case
  (:592, stand-in :412-414): which overlap conjunct the case exercises depends on
  which parallel run wins the stand-in's queue lock. Q26, Q27 and Q28 are killed
  only in some runs. A forced-order probe shows that each order leaves at least one
  conjunct surviving. Also :226-227: a marker check followed by a status check lets
  a run that held and ended between the two read as "never held".
- N3 [Tests] scripts/act_ci.py:12204: the only OOM fixture is `oom 2` with
  `oom_kill 2`, so S07 (a single OOM ignored: `exhausted > 1`) and S04 (the OOM
  count read from `oom_kill`, always 0 in the slice's local file) survive as
  uid 1000 and 0.

Suggestions: per-slot bypasses Q61/Q62 (stage the verdict change and isolation
breach in slot B too); reflow CI_WORKFLOWS.md:1835; say that page-cache reclaim
makes a nonzero max count routine.
