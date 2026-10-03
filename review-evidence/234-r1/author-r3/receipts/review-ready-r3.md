[A516] REVIEW READY (round 3)
Commit: `b5894838d6c47180ac4169e7d52dd746f461af21` on local branch `234-area-baseline`. That is four one-line commits on round 2's `0feff20f`: no rebase, no amend, and not pushed, as assigned. `0feff20f..b5894838` touches 6 files: the gate, its self-test and mutants, the hierarchy parser it imports (`syn/ooc/pp_baseline_rank.py`), `AREA_BUDGET.md` and the recipe. No RTL, processor, interface, workflow, baseline-JSON, tolerance, floor or ceiling change, and no Vivado run.

Changed, by assignment item (5968718943):
1. One validator for the baseline file, `load()`. Both `check` and `check-baseline` run it before using any field.
   - It parses strict JSON: `NaN`, `Infinity` and a decimal that reads as infinity are refused.
   - Then it checks every endpoint's shape:
     - a record with every field;
     - a known kind;
     - an identity with exactly the recorded keys and types;
     - a sha256 hex input digest;
     - exactly the kind's recorded figures, each a number and not a bool;
     - scopes of non-negative integer counts;
     - every tolerance, floor and ceiling a table of numbers;
     - no unknown field.
   - Any deviation exits 2, naming the endpoint and the reason. `judge()` runs only on a validated baseline.
   - Tests: 25 malformed-baseline arms, each driven through `main()` by both commands, and one killed mutant per check.
   - R446-2's `probe_malformed_record.py`: 0 cases not exit 2.
   - R447-2's `probe_contract.py`: every edited case gives rc 2 in both columns with no traceback. The control keeps rc 1 under `check` and rc 0 under `check-baseline`.
2. Parsers:
   - Every report count is read as `[0-9]+`, never through `isdigit()` or `\d`. That covers route status, timed endpoints, utilization and hierarchy rows. The slack is read as `-?[0-9]+\.[0-9]+`, and budget cells as `[0-9]`.
   - The route status reader requires exactly one `routable nets`, one `fully routed nets` and one `nets with routing errors` row. Anything else exits 2, naming the row.
   - Arms: both net rows removed, each row removed alone, and superscript and other-script digits in every parser. The mutants relaxing either guard are killed.
   - R446-2's route probe: both CONTRACT cases give rc 2. R447-2's `probe_route_real.py` on A: superscript rc 2 and both rows missing rc 2, 15/15. Every other case is unchanged.
3. Policy-pin arms. The fixture's WNS floor is now 0.03. Arms cover a floor cell differing, a ceiling cell differing, a JSON figure the table lacks, and a timing summary without its Total Endpoints columns. R446-2's `probe_extra_mutants.py` reports all four KILLED, and the control passes.
4. Self-audit: 61 sites, each with the validation in front of it, tabled in HANDOFF.md and PR-BODY.md. The places fixed this round:
   - the `\d` utilization pattern;
   - the `isdigit()` endpoint and route counts;
   - `float()` slack;
   - `parents[2]` (now guarded by depth);
   - `RecursionError` from the image manifest;
   - the hierarchy parser's silent skip of a non-count row (it now refuses it; output on all seven real reports is unchanged);
   - the `\d` budget cells;
   - the baseline file as a whole.
5. Docs:
   - The contract as it holds is stated in `AREA_BUDGET.md:189-196`, the recipe and the PR body: `check` exits 0 within tolerance, 1 for a material regression only, and 2 for every input it cannot judge. The reason is always printed, and no input reaches a traceback.
   - R446-2 R1 is taken exactly (`AREA_BUDGET.md:170`).
   - Recipe note: the route status report has no header, so each measurement uses a fresh directory, and the bank deletes nothing.
   - B's `armq_r` census is published in the packet: 1,153 flops in A and 1,260 in B at 1x1, from censuses whose sha256 equals the run receipts.
   - S1 is not taken, as assigned.

Validation at `b5894838`, worktree clean:
- 43 of 43 touched gates rc 0, with GNU Make 4.3 first on PATH and no pipes. They include:
  - the gate self-test (181 arms), the mutant campaign (122 of 122 killed; control passes) and `check-baseline` (3 endpoints);
  - the pp_baseline self-tests and its 32 mutants;
  - the `ci_scope` and `ci_events` checks;
  - the docs gates, including `make -C gptp-processor docs`;
  - the Python ratchets.
- R447-2's own `run_gates.sh`: 31 of 31 jobs rc 0.
- Real data: A route, 1x1 and 8x8 rc 0. B route rc 1 (+625 LUT). B 1x1 and 8x8 rc 0. The 10 ns control rc 2.
- Every probe both reviewers published in rounds 1 and 2, rerun unchanged (22 runs plus R447-2's gate runner). The results are tabled in the PR body, and every BAD or not-applied line is explained there:
  - R446-1 `probe_gate_cli`: 116 of 117; the one is `inf` at rc 2 against a literal want of 1, as in round 2.
  - R446-1 `probe_gate_mutants`: 21 killed, 0 survived, 2 not applied.
  - R446-1 `reconcile.py`: 2 hard-coded round-1 sentences, as before.
  - R446-2 route probe: 15/16; the 16th is S1.
  - R447-1 extra mutants: 17 killed, 1 not unique.
  - R447-1 `probe_route_status`: now 2 and 2, because its report has no net rows.
  - R447-2 `classify_mutants`: 96 ARM, 23 ESCAPED, 0 CRASH, 0 survived.
  - Policy probes 105/105 and 107/107.
  - Partition probes: 0 mismatches.
  - Each not-applied reviewer mutant maps to a shipped mutant that is killed.

Acceptance criteria (#234, as ruled in 5967852698 and 5967924270): unchanged from round 2.
1. Met at 50 MHz.
2. Not met at A, with the levers in #232, #230 and #639.
3. Documented; NFR-RES-01 is to be met by #640.
4. The hosted half is wired. The Vivado half runs in the manager's merge bank.
5. Outside this step.

Open risks/questions:
- `check` now refuses a baseline file in which any endpoint is malformed, not only the one it judges. That is one validator for the file, as item 1 asks.
- `syn/ooc/pp_baseline_rank.py`, shared with the ranking command, now refuses a non-count table row instead of skipping it.
- `record --write` does not catch a failure to write the baseline file. That is the environment, not an input, and `check` never writes.
- Packet for publication: HANDOFF.md, PR-BODY.md, receipts/round3/ (gates, probes, real data, R447-2's gate runner) and evidence/round3/armq-census.tsv.
