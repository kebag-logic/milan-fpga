[A516] REVIEW READY (round 2)
Commit: `0feff20fa228d0cb91d507943e6d39495b28b880` on local branch `234-area-baseline`: three one-line commits on round 1's `2a765a6c` (no rebase, no amend; not pushed, as assigned). `1269cdaf..0feff20f` is 14 files; round 2 adds `scripts/ci_scope.py`, `docs/testing/CI_WORKFLOWS.md` and `docs/findings/README.md`. No RTL, processor, interface, workflow, pin-list or baseline-JSON change; no Vivado run.

Changed, by assignment item (5968015720):
1. Non-finite timing: a WNS or WHS of `inf`/`nan`, or a summary whose TNS/THS total endpoints are absent or 0, exits 2 with a named reason. Three arms; mutants `finite slack` and `timed endpoints` killed.
2. One exit-code contract: a missing, non-JSON or endpoint-less baseline, an endpoint without a complete record, a gated figure without a tolerance, a ceiling naming no figure and a wrong-shape image manifest each exit 2 as `NOT COMPARABLE: <reason>`, never through a traceback. `check-baseline` lists a missing record and an unknown ceiling figure as problems. 13 `check` and 20 `check-baseline` arms run through `main()`. Exit 1 stays a material regression.
3. Route completion: the route endpoint reads the run's one `*_route_status.rpt`. Unrouted nets, routing errors or routable nets not fully routed exit 1; a missing, duplicated or unreadable report exits 2. Nine route arms (clean, errors, unrouted, partly routed, missing, two reports, no error row, bad count, unpaired rows) and two CLI arms. A's real status reads clean.
4. Every claimed refusal has an arm and a killed mutant. Self-test 51 -> 113 arms; shipped mutants 25 -> 84, and R446's reason probe classifies 84/84 as killed by an arm assertion, 0 by a crash. Both reviewers' mutant probes rerun unchanged: R446 23/23 killed, R447 18/18 killed, controls pass.
5. Policy pinned: `check-baseline` requires the route's BRAM tile ceiling and compares every JSON policy value with the `AREA_BUDGET.md` table, parsed from the table. The table was re-laid as one value per cell; no value changed. Because the gate now reads that page, `ci_scope.py --selftest` required it in `GATE_READ_DOCS`, and CI_WORKFLOWS counts it.
6. Improvements: a gated figure that improves by more than its tolerance prints "re-baseline recommended"; the exit code is unchanged and the policy stays growth-only.
7. One partition in `AREA_BUDGET.md` and the findings page: the own logic of every instance the gate record lists outside `u_nvm_port`, 51 terms. Net +79 LUT / +93 FF, absolute 391 LUT / 121 FF. The processor top's own logic is stated separately as one of the terms: -23 LUT / +107 FF, its `armq_r` queues (1,153 -> 1,260 flops).
8. Docs and PR body: R446-1 R1 to R4 and R447-1 RESIDUE 1 and 2 taken; the owner decision 5967924270 cited where the allocation "needs an owner decision"; Issue column lever 2 -> #230, levers 3 and 6 -> #639; both baseline findings indexed. HANDOFF.md and PR-BODY.md each carry a "Round 2" finding-by-finding table.

Validation at `0feff20f`:
- 43/43 touched gates rc 0, foreground, no pipes, GNU Make 4.3 first on PATH, worktree clean. That covers the rtl-fast OOC step (gate self-test 113 arms, 84/84 mutants, `check-baseline` 3 endpoints, pp_baseline 32/32), `ci_scope` and `ci_events` checks and self-tests, the docs job's gates incl. `make -C gptp-processor docs`, and the Python idiom, fail-fast, hygiene, TODO and test-evidence ratchets.
- `act_ci --selftest` is no longer in the table: AGENTS.md section 5 lets the candidate's copy run it only inside the disposable CI job boundary, and round 1 ran it on the host.
- Real data, existing run directories: A route, 1x1 and 8x8 rc 0, with A's route status clean (105,566 of 105,566 routable nets fully routed, 0 with routing errors). B route rc 1 (+625 LUT; its status clean too); B 1x1 and 8x8 rc 0; A's 10 ns control rc 2.
- Reviewer probes rerun unchanged at the head:
  - R447: `probe_cli` 54/54 as documented; `probe_route_status` clean 0, 37 unrouted nets 1; `check_tables` 49 groups, 0 mismatches; `replay_records` A 0/0/0, B 1/0/0, 10 ns 2. `partition_check`'s complete-partition line (+79, 391, +93) and processor-top line (-23, +107) equal both pages; a mechanical comparison reports 0 mismatches.
  - R446 `probe_gate_cli`: 116 of 117 as expected. The one BAD is `inf` with 0 endpoints at rc 2 against the probe's literal want of 1; F1 allows 2 and item 1 requires it. `nan` gives rc 2.
  - R446 `reconcile.py` unchanged: 2 mismatches, both its hard-coded round-1 sentences. The second asserts FF +95 on a partition whose records give -12, so no prose can satisfy it. An adapted copy, with only those two checks re-pointed at the round-2 sentences and its diff in the packet, reports 0 mismatches.

Acceptance criteria (#234, as ruled in 5967852698 and 5967924270):
1. Met at the declared 50 MHz shipping clock (manager ruling).
2. Not met at A: the registry and SRP FIFOs still spill. Levers are with #232, #230 and #639.
3. Documented. The ceiling and tolerances are accepted (manager ruling). NFR-RES-01 stays at 60 %, met by the #640 redesign; until then the gate holds every resource at its recorded value.
4. Hosted half wired (self-test, mutants, `check-baseline`); the Vivado half runs in the manager's merge bank (manager ruling).
5. Outside this step.

Open risks/questions:
- R446-1 R1/R2 and R447-1 RESIDUE 1 prescribe different words for the same three lines; R447-1's per-line wording is used, carrying all of R446-1's content.
- R447-1 RESIDUE 2 item 1 ("needs the owner's ruling") is replaced by the owner decision, which postdates it.
- As a gate-read page, `docs/design/AREA_BUDGET.md` now classifies as tooling-relevant, so a docs-only edit to it runs the rtl-fast heavy jobs.
- Packet for publication: HANDOFF.md, PR-BODY.md and receipts/round2/ (gate logs, probe logs, the adapted reconcile diff).
