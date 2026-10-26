[A682c] REVIEW READY
Commit: `1c9a3e8e54fc746f95ab89e074346904ba49f3e0` on `789-yosys-tool-job`: two round-3 commits on top of `1e0c5c09`, `10e0b519` (the judge) and `1c9a3e8e` (a docs-only correction). Pushed fast-forward after the privacy check (0 private lines, PR-wide from dev too). Working tree clean; live dev is still `76de691e`.

Changed:
- `scripts/ci_fast_tool_selftest.py` (**R707-2-01**): a new judge, `fast_tool_emission`, reads the emitted workflow. It replays the shared install and runtime transforms on the derivation, and requires the emitted `rtl-fast.yml` to equal that replay: every workflow key, job, job key and step. The one allowed difference is the tool cache's key and the restore's key, each the replay's string with the recipe stand-in replaced by the same bound recipe. So no rtl-fast stage after the derivation, the key binding included, can drop, add, reorder or rewrite a step or key of any job. 36 plants, each refused by name:
  - each step of both emitted jobs dropped in turn;
  - rewritten self-test, build and evidence-record bodies;
  - an added or swapped step, an added job key, an added job, a workflow `env` set after the digest, and another job's step dropped;
  - a stand-in left in the restore, and a restore bound to another recipe;
  - the real `bind_fast_tool_key` patched to drop the result-cache self-test, refused as exactly "emitted yosys-elaboration drops Prove the result cache refuses a planted entry".
- `fast_tool_retention` is unchanged in behaviour; its step comparison is now shared with the new judge.
- **S2 taken:** a workflow `defaults` plant in `fast_tool_key_inputs`.
- **S1 taken in its documentation form.** `docs/testing/CI_WORKFLOWS.md` says that the generator recognises the after-build pair by its ids, and that `fast_tool_emission` holds the pair's content to the runtime transform's output (a plant rewrites the evidence record). The generator guard is unchanged.
- `docs/testing/CI_WORKFLOWS.md`, "Fast feedback" and item 4, now say which list each judge holds. `fast_tool_retention` holds the derived lists against the template. `fast_tool_emission` holds the emitted lists, after every stage, against the replay. Neither judges the shared transforms themselves: for what they emit, the generated-graph comparison is the only whole-list hold, and `scripts/ci_install_cache_selftest.py` also requires the install transform to keep every derived step.
- The generator, the templates and all four workflows are unchanged (`git diff 1e0c5c09 1c9a3e8e -- .github/ scripts/ci_gate_workflows.py` is empty), so the tool key is unchanged.

Validation:
- **Gates: 32 of 32 rc 0 at `1c9a3e8e`,** on CPython 3.14.8 with PyYAML 6.0.3 and on CPython 3.12.13 with PyYAML 6.0.2 by hash (64 runs). The set:
  - `ci_gate_workflows.py --check`;
  - `ci_gate_workflows_selftest.py`, which prints 86 "Fast Yosys tool" lines, then `gate workflow and union controls: PASS`;
  - the rest of the "CI scheduling and evidence controls" list, and `ci_scope.py --selftest`;
  - `ci_events.py --check` (OK, 2199 items) and `--selftest` (PASS, 2199 items, 5258 arms);
  - `act_ci.py --selftest` and the 0555 runner contract gate, offline (two `selftest: PASS`; `act_ci.py` unchanged against dev);
  - `check_py_idiom.py` and its `--selftest`, and the other code-quality ratchets;
  - the docs gates under the pinned Markdown renderer (`check_em_dash.py --base 76de691e`: 0 findings over 133 added lines).
- **Generator mutants through the three hosted judges** (`ci_gate_workflows.py --check`, `ci_gate_workflows_selftest.py`, `ci_events.py --check`), with 15 edits of `bind_fast_tool_key` after the key is bound:
  - At `1e0c5c09`, 10 survive: R707-2's N11 (drop the result-cache self-test), drop sv2v, drop Fetch, swap the two ooc self-tests, rewrite a self-test, add a consumer step, add a tool step after the build, rewrite the tool evidence record, set a workflow `env` after the digest, and drop another job's step.
  - At `1c9a3e8e`, all 15 are refused by an "emitted ..." finding.
  - The digest-without-`defaults` mutant survives at `1e0c5c09` and fails here as "tool key unchanged by an edit of its build inputs: the workflow defaults".
  - The round-2 derivation mutants keep their words. The control passes.
- **Hosted at `1c9a3e8e`, attempt 2: all four runs green.**
  - [rtl-fast 40356479027](https://github.com/kebag-logic/milan-fpga/actions/runs/40356479027): 16 of 16 success. "Prepare pinned Yosys" restores the existing key in 11 s ("Cache hit occurred on the primary key", no build). `yosys-elaboration` restores the same key with `fail-on-cache-miss: true`, runs no build, proves `Yosys 0.66 (git sha1 86f2ddebc ...)` and passes all 13 steps in 15 min 45 s. Both jobs keep their 30-minute timeouts.
  - [docs 40356478658](https://github.com/kebag-logic/milan-fpga/actions/runs/40356478658): 9 of 9 success. Hosted "CI scheduling and evidence controls" prints the same 86 "Fast Yosys tool" lines as the local run.
  - [elaborate 40356478638](https://github.com/kebag-logic/milan-fpga/actions/runs/40356478638): 6 of 6 success.
  - [rtl-full 40356478782](https://github.com/kebag-logic/milan-fpga/actions/runs/40356478782): success; 34 jobs succeed, `verilator-suites` and `yosys-portability` among them, and the nightly "Physical gPTP" job is skipped.
- **Attempt 1 of all four was cancelled, unrelated to this change.** In docs-gates-0, "Resolve exact package downloads 6" (`scripts/ci_install_cache.py --packages librsvg2-bin`) printed nothing for 45 minutes and was stopped at the worker's limit. `ci-fail-fast` then cancelled the head's other runs. I re-ran all jobs of the four runs with `gh run rerun`; no commit was added.

Acceptance criteria:
- Round-3 items: R707-2-01 met, with the named key-binding plant. S1 and S2 are taken as above. The hosted `rtl-fast` is green at the new head.
- #789 overall: still `Relates to #789`. The live act replay is owed to the manager. An offline data-only check at this head passes: dev's trusted runner accepts all four workflows, and the stages order `yosys-tool`, `yosys-elaboration`, `rtl-fast`. No act or Docker was run.

Open risks/questions:
- The shared install and runtime transforms are still judged by neither fast-tool judge. This predates #789 and is stated in the docs.
- Candidate follow-up Issue, not filed: `scripts/ci_install_cache.py:59` runs `sudo apt-get update -qq` with no bound, so a mirror stall costs a docs worker its whole 45 minutes and cancels the head.
- No hosted run yet shows a key hit across a workflow edit that leaves the build inputs unchanged. Round 3 edits no workflow.
- R707's re-review and the external review at this head are owed.
