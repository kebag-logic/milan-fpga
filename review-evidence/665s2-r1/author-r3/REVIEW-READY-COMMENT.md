[A681c] REVIEW READY
Commit: `f887663852d118e810ef690c3dd5cf9fe2292588` (branch `665-s2-cpu-budget`, PR #792; one commit on round 2's `cd3525c3`; base `dev-soft-core` `e76a755a`)
Changed: only `tb/verilator/ctrl_service_budget/`.
- **Service** (R703-2 F1): each loaded channel's first and last record in a composed window is graded from its commit to the end of the pass that releases it. A record never released is reported, with its lower-bound wait. A window that leaves its load unreleased does not set the composed maximum.
- **Fan-out** (R703-2 F2): a new `aecp-fanout` group registers the firmware's 16 controllers on every interface. Every notifying command the image completes ends at its last recipient, and the per-recipient cost is reported.
- **Owed row** (R704-2 F1): 12 ACMP commands, with the 7 responses ahead checked by sequence. Each row's load is derived from the contract in the grader, and the self-test counts the real stimulus.
- **Self-protection and counting** (R703-2 F3, R704-2 F2): N6, N8 and N10 fail named checks; the SHUTDOWN control is now an instance of `adp.shutdown`.
- **Found while re-measuring:**
  - The ACMP core owes at most 8 responses (`ACMP_OWED_MAX`), so commands behind the owed input are taken and never answered: 4 of 4 at 1x1, 2 of 4 at 8x8. Each is graded as never answered.
  - The 8x8 idle floor was the pass the script's end cut short; that pass is now excluded.
- R703-2 RESIDUE R1-R5 applied.
Validation (all rc 0, at the head):
- `run.py --self-test`: 81 checks, 52 of 52 mutants caught.
- Unchanged groups (50 of 52 scripts byte-identical) were regraded on round 2's attested builds; `backlog-owed` was run again and `aecp-fanout` is new. Results:
  - 1x1: `18 groups graded, 0 refusals, 58 T_svc misses (58 of 141 probe instances, 22 of 81 paths)`.
  - 8x8: `17 groups, 0 refusals, 102 of 182, 60 of 129 paths`.
  - Arm B: 1x1 `41 of 68, 18 of 44`; 8x8 `60 of 92, 36 of 68`.
  - SHUTDOWN: S1 `0 of 2, 0 of 1 paths`; S8 `0 of 3, 0 of 2 paths`.
- Controls `slow-adp-rx`, `slow-adp-shutdown` and `as-built` are caught.
- A head regrade is byte-identical, and fresh builds at the head reproduce 10 of 10 group logs byte for byte.
- Docs, idiom, hygiene, TODO, SoC/RTL source and whitespace gates pass, with em dash 0 of 607 added lines; behave passes 406/406.
- Both reviewers' probes were rerun unmodified:
  - R703-2 `review_mutants2.py`: N6, N8, N10 caught; N11 and N12 escape, with 0 published values changed under either.
  - R703-2's capacity fan-out: 11.33241 / 20.68273 ms.
  - R704-2 `probe_scenario_control.py`: the SRP-omission plant now fails 2 named checks. Its twelve-command owed variant measures 126.29163 / 161.10225 ms.
  - R704-2 `audit_receipts.py`: SHUTDOWN reported equals de-duplicated (1/2, 2/3).
  - Not run: `verify_identity.py`, which checks the reviewer's own checkout at `cd3525c3`.
Acceptance criteria:
- Round 3 items 1-5: met. The SRP starvation is reported by duration: in arm A's bound-talker windows none of SRP's 32 records is ever released (at least 568-659 ms). Composed maximum: 14.81 ms (1x1) and 27.84 ms (8x8), from windows that released their load; the starved windows' 31.32 / 44.19 ms passes are reported as lower bounds. SET_NAME at capacity: 11.33 ms (1x1), 20.68 / 22.98 ms (8x8).
- Both points re-measured and tables replaced: met.
- Rows within T_svc: **not met** (D4; S2b follows), so the PR body says "Relates to #665".
Open risks/questions:
- For the manager: whether the ACMP owed-capacity drop, the SRP starvation under passes longer than the tick (`srp_mbx.c:441-451`) and the per-recipient fan-out cost become Issues or S2b scope.
- Not done: RESIDUE R-4 (`docs/testing/TESTING.md`, a release-lane file); R703-2 S1-S3 (optional); the lock-expiry and counter-push fan-outs (Limits).
- S2b should re-base its before-and-after figures on this head, because round 2's composed maximum and 8x8 idle floor are superseded.
