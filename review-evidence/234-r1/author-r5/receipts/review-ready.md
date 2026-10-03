[A516] REVIEW READY (round 5)
Commit: `ec7eb2d8ff81700842f4e3a35b79879c8c3838e5` on local branch `234-area-baseline`. That is two one-line commits on round 4's `79e53831`: no rebase, no amend, and not pushed, as assigned. `79e53831..ec7eb2d8` touches 5 files: the gate, its self-test and mutants, `AREA_BUDGET.md` and the recipe (+115 / -64). No RTL, processor, interface, workflow, baseline-JSON, tolerance, floor or ceiling change, and no Vivado run.

Changed, by assignment item (5970587136):
1. The name class as accepted (R446-4 F1, ruling (a)).
   - One walk, `names()`, run by `strict()` on every JSON the gate reads. It holds every key of the baseline and of the image manifest to `[A-Za-z0-9_.:/-]{1,128}`, open objects included: notes such as `description` and `measured`, and manifest entries.
   - The one exception is a record's sub-block scope names (`SCOPES`), which may also hold `[` and `]`. Anything else exits 2, naming the key and its place, e.g. `the key 'x[1]' is not a name of 1 to 128 of A-Z a-z 0-9 _ . : / -, in /description/0`.
   - `named()` now refuses repeated keys only. The per-site endpoint-name and policy-figure checks the walk subsumes are removed.
   - Arms:
     - a bracketed key in a manifest entry, exit 2;
     - another named key in a manifest entry, exit 0;
     - a bracketed key in the file's `description` note and in a `scopes` object inside an endpoint's `measured` note, exit 2 through both commands;
     - a bracketed scope name through `check` (new) and `check-baseline`, exit 0.
   - Mutants: `every key named`, `baseline scope names`, `scope names at their path only`, `scope path matched in full`, `names inside lists` and `names below the top level` are added, and `baseline key names` is re-pointed at the walk. All are killed.
   - The generator reaches keys inside open objects:
     - a `note` operator writes a named, bracketed or bad key into a note;
     - an `entry key` operator does the same in a manifest entry;
     - the fixture's notes are now objects, so every existing key operator reaches inside them.
   - R446-4's `probe_r4_structure.py`, unchanged: the bracketed note cases (file and endpoint) and the bracketed manifest key give rc 2. The other 29 cases are unchanged against R446-4's published log (32 compared, 3 changed). The probe prints the manifest case `BAD rc=2 want=0` because its built-in want predates the ruling.
2. Wording, exactly as given:
   - R446-4 R1 (PR body, Round 4 paragraph);
   - R447-4 R1 (gate docstring: the barrier is scoped to `check`, `record` and `check-baseline`; `--selftest` and `--fuzz` are test drivers outside it);
   - R447-4 R2 (`AREA_BUDGET.md`, recipe);
   - R447-4 R3 (PR body Description row);
   - R446-4 S1 (the docstring's exit-status sentence is scoped to the three commands).
3. Not taken: R447-4 S1 and S2, listed as open suggestions in the PR body's limitations. Item 1's manifest operator writes keys only. Those keys do reach `manifest via json.loads`, which the generated cases alone now detect.

Validation at `ec7eb2d8`, worktree clean:
- Gates: 43 of 43 rc 0, with GNU Make 4.3 first on PATH and no pipes. They include:
  - the gate self-test: 254 arms and 500 generated cases;
  - the mutant campaign: 162 of 162 killed, control passes;
  - `check-baseline`: 3 endpoints;
  - the docs gates;
  - the Python ratchets (the self-test module is 999 lines, under the 1,000-line limit).
- `--fuzz`, seed 234, 0 failures, no traceback:
  - 20,000 on the fixtures (12,861 shape-breaking cases, all exit 2);
  - 20,000 on A's real route (13,602);
  - 5,000 on A's real standalone 1x1 (3,175).
- Real data: A route, 1x1 and 8x8 rc 0, route status complete. B route rc 1 (+625 LUT). B 1x1 and 8x8 rc 0. The 10 ns control rc 2.
- Both reviewers' round-4 probes and packet drivers, unchanged. R447-4's `verify_tree.sh` passed after each group.
  - R446-4:
    - `probe_r447_3_cases` and `probe_r4_adhoc`: 0 not as expected.
    - `probe_r4_generative`: 22 runs. 2 BAD: the barrier-narrowing mutants, killed by the self-test as in round 4. 4 not applied.
    - `run_prior_probes` (light, mutants, reasons): as before, including `probe_pr_mutant_reasons` 153 of 153 ARM.
    - `run_gates.sh`: 31 of 31 rc 0.
  - R447-4:
    - `probe_r4_structure`: 51 cases, 0 off expectation, each rc equal to its log.
    - `probe_r4_resolution`: 11 of 11.
    - `probe_r4_oracle`: as R447-4 found.
    - `probe_r4_fuzzkill`: 20 applied, all killed by the self-test; 3 not unique.
    - `reruns.sh`: as before, including `classify_mutants` 149 ARM, 4 ESCAPED, 0 survived.
    - `run_fuzz.sh`: 90,000 cases, 0 failures. Its seed-234 case digests equal this round's.
  - Seven reviewer mutants no longer apply, because round 5 rewrote their spans. Each is re-pointed at the code that now holds its rule, and the self-test kills it.
    - Of the 16 name mutants, shipped and adapted, the generated cases alone detect 13.
    - The three they miss would refuse a bracketed scope name, which the oracle cannot tell from a correct refusal. The exit-0 arms kill them.

Acceptance criteria (#234, as ruled in 5967852698 and 5967924270): unchanged from rounds 2 to 4.
1. Met at 50 MHz.
2. Not met at A, with the levers in #232, #230 and #639.
3. Documented; NFR-RES-01 is to be met by #640.
4. The hosted half is wired. The Vivado half runs in the manager's merge bank.
5. Outside this step.

Open risks/questions:
- A misnamed key is refused while reading strict JSON, so its baseline reason reads "is unreadable: the key ..." where round 4's endpoint-name and policy-figure reasons read "is malformed". Both exit 2 with the key named.
- My scratch probe runner deleted the first light-group receipts when the heavy group started. The light group was rerun with a fixed copy, and the tables report that rerun (HANDOFF R5.8).
- Packet for publication:
  - HANDOFF.md ("Round 5") and PR-BODY.md ("Round 5");
  - receipts/round5/: gates, real data, fuzz runs and replays, both reviewers' probes and drivers, the structure comparison, the name-mutant and kill matrices;
  - the round-5 scripts under scratch-scripts/.
