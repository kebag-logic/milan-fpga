[A516] REVIEW READY (round 7, re-baseline on the composed tree)
Commit: `aabdc2839a272631222c30a62e83218d893b40d2` on local branch `234-area-baseline`. That is the `--no-ff` merge `4d81e10d` of dev `54643724` into round 6's `d5f56313`, then three one-line commits: no rebase, no amend, and not pushed, as assigned. `4d81e10d..aabdc283` touches 4 files: `syn/ooc/pp_resource_baseline.json`, `docs/design/AREA_BUDGET.md`, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md` and `docs/findings/README.md`. No RTL, processor, interface, gate code, self-test, mutant, workflow, recipe, tolerance, floor or ceiling change. Against dev as merged, the PR is the same 15 files as in rounds 3 to 6.

Changed, by assignment item (5972491855), answering R446-7 F1 by option (a):
1. Merge (`4d81e10d`): parents `d5f56313` and `54643724`, no conflict. Its tree `04a0c948` equals R446-7's candidate tree and `git merge-tree`'s, so nothing was hand-merged. `docs/findings/README.md` keeps both sides' rows.
2. Re-measurement at the merge commit (`a89d0696`), with the recipe as committed, one Vivado at a time, each run under `flock /tmp/milan-vivado.lock`:
   - `route-1x1`: LUT 50,767 (+639), FF 59,634 (+628) and slices 15,832 (+17, 18 free). RAMB36, RAMB18 and DSP stay 79 / 27 / 14. WNS +0.193 and WHS +0.024 ns meet the floors. All 106,622 routable nets are routed, with 0 routing errors.
   - Against the `1269cdaf` record the route exits 1: LUT 139 over the tolerance and FF 28 over, exactly R446-7's prediction from PR #634's published figures.
   - `ooc-1x1`: 24,332 LUT (-11) and 25,345 FF (+1). `ooc-8x8`: 31,556 (-6) and 33,937 (+8). Both exit 0 even against the old record.
   - `record --write` for all three endpoints. Every tolerance, floor and ceiling is unchanged, checked field by field. `record --write` keeps notes, so I edited each endpoint's `measured` note by hand to name dev `54643724`.
   - `check` exits 0 on all three new runs, and `check-baseline` reports 3 endpoints.
   - Sources of the delta, where the reports show them:
     - The AAF clock meter, `milan_datapath/g_aaf_meter.aaf_clock_meter`: 483 LUT (32 as LUTRAM) and 630 FF, equal to PR #634's published cost. That is 76 % of the LUT growth and all of the FF growth.
     - The rest of `milan_datapath`: +223 LUT. #634 changed the source of `csr` (+58) and of three CRF blocks. Instances with unchanged modules moved too (`aaf_latency_tap_bank` +68, `talker_diag` +61, `ctl_tx_mux` +54); the reports do not separate the changed wiring from optimization.
     - `DESC_NAME_ENTRIES_P`, 38 to 39 at 1x1 and 99 to 107 at 8x8: the only wrapper parameter that moved, with no wrapper source changed. It reaches `u_pp/u_aecp/u_store` and `u_nvm` only. Their moves are route +9 and +19 LUT, 1x1 +7 and -11, and 8x8 -3 and -5 (with +8 FF in `u_nvm`).
     - The firmware ROM `alinx_ax7101_rom.init`: constants only, at the same size (AEM image 7,352 to 7,512 bytes, its CRC, the model ID, NVM name count 38 to 39). No block RAM count moves.
3. Docs (`469d1620`):
   - `AREA_BUDGET.md`:
     - the table now gives dev `54643724`: 80.07 % LUT, 12,727 over NFR-RES-01, 18 slices free, +0.193 / +0.024 ns;
     - the allocation and timing-fall figures are updated, and the `1269cdaf` figures are kept in one sentence;
     - the rule is stated: a merge that moves the shipping image records its own re-baseline.
   - The #234 findings page has a dated section, "Re-baseline of 2026-10-03, after PR #634", with the delta per endpoint and sub-block and C's run receipts. The sections after it are the `1269cdaf` history.
   - Both index rows give the new figures and the rule.
4. Re-baseline gap (`aabdc283`): `AREA_BUDGET.md` "Where the gate runs" now states the bank's rule, with no new tooling.
   - The bank triggers on the merge result's dev delta since the revision the `measured` note names, not on the PR's own diff.
   - It runs the comparison whenever that delta touches RTL, the processor pin or the build recipe.
   - Growth the PR did not make is first recorded as a re-baseline naming its predecessor, and the PR is then judged against that record.

Validation:
- Vivado: 8x8 elaboration 1.1 min, route 39.2, standalone 1x1 19.3, 8x8 23.5. All rc 0, no `Synth 8-4445` diagnostic, and every image rehashed equal.
- Gates: 43 of 43 rc 0, with GNU Make 4.3 first on PATH and no pipes, on the merge commit `4d81e10d` and at the head, the worktree clean each time. They include:
  - the gate self-test: 260 arms and 500 generated cases, digest `151eb3fc6a0d989c`;
  - the mutant campaign: 174 of 174 killed;
  - `check-baseline`;
  - every docs gate;
  - `check_em_dash` and `git diff --check` against `--base 54643724`.
- Real data at the head: C's route, 1x1 and 8x8 exit 0, every figure equal to the record.

Acceptance criteria (#234, as ruled in 5967852698 and 5967924270): unchanged in scope. Criterion 4's gate now carries a record of the composed tree's own image, which passes, so the next RTL-changing PR is not charged PR #634's growth.

Open risks/questions:
- I ran the merge-commit gate table beside the route's synthesis, and the service unit reached its memory cap: `memory.events` max 25,048, with oom 0 and no kill. The run finished rc 0, and its figures equal PR #634's published ones. Nothing else ran beside a synthesis after that.
- Another lane's Vivado shared the host during the route. It was not holding the lock when my route took it.
- B, the next adoption measured on `1269cdaf`, now passes the route against C's record at -14 LUT. That is only because it lacks the meter, so it says nothing about the adoption, which must be measured again on a tree with PR #634.
- The rule and the predecessor catch are docs statements of the manager's bank rule; hosted CI cannot enforce them without Vivado.
- R446-5 R1 is not in the round-7 assignment; R446-7 carries it to the manager. The PR body's Round 5 row is unchanged.
- Packet for publication:
  - HANDOFF.md ("Round 7") and PR-BODY.md ("Round 7");
  - receipts/round7/: gates at the merge commit and at the head, real-data checks before and after recording, the Vivado chain log and run receipts;
  - evidence/round7/: C's records, the delta tables and the gate table;
  - the round-7 scripts under scratch-scripts/.
