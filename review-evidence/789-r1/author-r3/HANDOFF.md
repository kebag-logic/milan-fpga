# HANDOFF: [A682c], issue #789 round 3, PR #794

Status: DONE. Two commits, gates green on two interpreters at the final head, pushed. All four hosted runs
are green at the final head in attempt 2: rtl-fast 16/16, docs 9/9, elaborate 6/6, rtl-full 34 success with
the nightly physical leg skipped.

- Lane: `789-yosys-tool-job`, from dev `76de691e5625cc4ea2f9a19def9e07c1183a14ee` (live dev at push time and at hand-off is the same).
- Round-2 head: `1e0c5c09f6d5e41c8a80ec5e6179c1c762b94086`.
- **Round-3 head: `1c9a3e8e54fc746f95ab89e074346904ba49f3e0`**: two commits, each a one-line subject with no
  body and no trailers:
  - `10e0b5195309d198fdc2748a802eafc0f3acb4f4`: the emission judge, its plants, S2, the docs.
  - `1c9a3e8e54fc746f95ab89e074346904ba49f3e0`: a docs-only correction. The install transform has its own
    step-keeping self-test (`scripts/ci_install_cache_selftest.py`), so "the comparison is their only hold"
    was too strong; it is now "the only whole-list hold".
- Pushed fast-forward `1e0c5c09..10e0b519`, then `10e0b519..1c9a3e8e`, each after the privacy check
  (`receipts/push-privacy-check.txt`, `push-privacy-check-1c9a3e8e.txt`: 0 lines; PR-wide from dev: 0 lines).
- Assignment: #789 issuecomment-6420212695, answering R707-2 (PR #794 issuecomment-6420207322).
- TAKEN: #789 issuecomment-6420235376.
- REVIEW READY: #789 issuecomment-6424747887 (copy in `receipts/review-ready.md`).

## Assignment items

| item | result |
|---|---|
| 1. R707-2-01: hold `yosys-elaboration`'s retained checks in the emitted jobs, after every stage, the key binding included; a key-binding plant that drops one self-test must fail a named judge | done: new judge `fast_tool_emission`; in-tree plant through the real `bind_fast_tool_key` refused as "emitted yosys-elaboration drops Prove the result cache refuses a planted entry"; mutant K01 (= R707-2 N11) SURVIVED at `1e0c5c09`, KILLED by name at `1c9a3e8e` (and `10e0b519`) |
| 2. S1 (identify the after-build pair by more than its `id`) | accepted in its documentation form: `CI_WORKFLOWS.md` now says the generator recognises the pair by id, and that `fast_tool_emission` holds its content to the runtime transform's own output (plant: rewritten tool evidence record refused). The generator guard is unchanged. |
| 2. S2 (workflow `defaults` plant in `fast_tool_key_inputs`) | accepted: plant added; mutant D01 (digest omits `defaults`) SURVIVED at `1e0c5c09`, KILLED at `1c9a3e8e` (and `10e0b519`) |
| 3. push (privacy check first); hosted `rtl-fast` stays green at the new head | pushed; rtl-fast run 40356479027 attempt 2: success, 16 of 16 (see Hosted) |

## Changes (file:line at `1c9a3e8e`, and why)

`scripts/ci_fast_tool_selftest.py` (the only code change; the generator and every workflow are unchanged, so
`git diff 1e0c5c09 1c9a3e8e -- .github/ scripts/ci_gate_workflows.py` is empty and the tool key is the same as
at `1e0c5c09`):

- `:4-6` docstring: names the new hold (R707-2-01 Docs).
- `:24` imports `FAST_TOOL_RECIPE`, the derivation's stand-in, which the new judge unbinds.
- `:34` `SELF_TEST`: the result-cache self-test named once, used by the retention plants (`:288`, `:311`, `:316`)
  and the new emission plants, which replaces the local `repeated` literal.
- `:36` `BOUND_RECIPE`: the exact form a bound recipe takes, `recipe-<64 hex>`, optionally followed by
  `-${{ hashFiles('...') }}`.
- `:205-218` `step_findings`: the drop/change/add/reorder comparison, moved out of `fast_tool_retention` so that
  both judges use one comparison. Retention's words are unchanged (`:232`).
- `:320-358` **`fast_tool_emission`** (R707-2-01): it replays the shared install and runtime transforms on the
  derivation (`gate_graph`) and requires the emitted workflow to equal that replay in every workflow key, job
  list, job key and step. The one allowed difference is the tool cache's and the restore's key, each the
  replay's string with its stand-in replaced by the same bound recipe. It reads the emitted graph, so every stage
  after the derivation is held, the key binding included. It covers the whole file, not only the two jobs, so the
  binding stage cannot touch any other job either. Each deviation is named.
- `:361-434` `fast_tool_emission_planted`: the plants below, then the stage plant (`:424-434`). That plant patches the real
  `bind_fast_tool_key` to bind and then drop the result-cache self-test, and requires exactly
  `["emitted yosys-elaboration drops Prove the result cache refuses a planted entry"]`.
- `:482-483`, `:495` S2: a workflow `defaults` plant (`run.shell`) that must change the key; `:509-510` print line.
- `:590-595`: the pristine head must pass `fast_tool_emission` too; `:607` runs its plants.

`docs/testing/CI_WORKFLOWS.md`:

- `:344-350` S1: the generator recognises the evidence pair by its two ids, not its content, and
  `fast_tool_emission` holds the content to the runtime transform's own output.
- `:369-371` S2: the workflow `env` and `defaults` are among the inputs whose edit must change the key.
- `:376-406` R707-2-01 Docs: which list each judge holds. `fast_tool_retention` holds the derived lists, the
  derivation's own output, against the template. `fast_tool_emission` holds the emitted lists, the generated
  file after every stage, against the replay of the shared transforms on the derivation, with only the two key
  strings different. Neither judges the shared install and runtime transforms themselves (emission replays
  them). For what they emit, the generated-graph comparison is the only whole-list hold, and
  `scripts/ci_install_cache_selftest.py` also requires the install transform to keep every derived step,
  unchanged unless it is an `Install ` or `Build ` step (`1c9a3e8e` corrects this sentence).
- `:875-882` item 4 of the sequence pin: the same split. R707-2 quoted the old wording as the claim that did
  not match the judge's input.

No source comment names a lane, review label or round.

## New checks: plant, failing words

All run in the hosted "CI scheduling and evidence controls" step via `ci_gate_workflows_selftest.py`. In-tree
plants on a copy of the emitted graph (`fast_tool_emission_planted`), each required by its words:

| plant | failing words |
|---|---|
| each of the 14 emitted `yosys-elaboration` steps dropped in turn | "emitted yosys-elaboration drops <step>" |
| each of the 8 emitted `yosys-tool` steps dropped in turn | "emitted yosys-tool drops <step>" |
| the result-cache self-test body rewritten | "emitted yosys-elaboration changes Prove the result cache refuses a planted entry" |
| the tool build rewritten | "emitted yosys-tool changes Build Yosys from source on cache miss" |
| the tool evidence record rewritten to touch `/opt/yosys` (S1) | "emitted yosys-tool changes Record actual job execution" |
| a consumer step added | "emitted yosys-elaboration adds Planted step" |
| a tool step added after the build, before the cache save | "emitted yosys-tool adds Planted step" |
| the two ooc self-tests swapped | "emitted yosys-elaboration reorders or repeats its steps" |
| a consumer job `env` added | "emitted yosys-elaboration's job keys differ from the transformed derivation's" |
| a tool job `env` added after the digest | "emitted yosys-tool's job keys differ from the transformed derivation's" |
| another job's step dropped (`verilator-lint`, Fetch RTL dependencies) | "emitted verilator-lint drops Fetch RTL dependencies" |
| a job added | "emitted jobs differ from the transformed derivation's: adds planted" |
| the stand-in left in the restore | "emitted yosys-elaboration's Restore the pinned Yosys build key is not its stand-in with one recipe bound" |
| the restore bound to another recipe digest | "emitted tool cache and its restore bind different recipes" |
| a workflow `env` entry set after the digest | exactly "emitted workflow keys differ from the transformed derivation's: env" |
| **the real `bind_fast_tool_key` patched to drop the result-cache self-test** | exactly "emitted yosys-elaboration drops Prove the result cache refuses a planted entry" |
| S2: workflow `defaults` gains a `run.shell` | the key must change; else "tool key unchanged by an edit of its build inputs: the workflow defaults" |

`ci_gate_workflows_selftest.py` now prints 86 "Fast Yosys tool" lines (50 at `1e0c5c09`; 36 new emission lines).

### Generator mutants through the three hosted judges

`tools/probe_mutants_r3.py` copies a `git archive` export of the head, applies one source edit to
`scripts/ci_gate_workflows.py`, regenerates with the mutated generator, then runs `ci_gate_workflows.py --check`,
`ci_gate_workflows_selftest.py` and `ci_events.py --check`. SURVIVED means all three exit 0. Receipts:
`receipts/probes/mutants-1e0c5c09.{txt,json}`, `mutants-10e0b519.{txt,json}`, `mutants-1c9a3e8e.{txt,json}`
(the last two have identical outcomes; `1c9a3e8e` changes docs only).

| mutant (K: in `bind_fast_tool_key` after binding; G: in the derivation; D: replacement) | `1e0c5c09` | `1c9a3e8e` |
|---|---|---|
| control | PASS | PASS |
| K01 drop the result-cache self-test (R707-2's N11) | SURVIVED | "emitted yosys-elaboration drops Prove the result cache refuses a planted entry" |
| K02 drop Elaborate | killed incidentally ("tool key changed by an edit outside the build recipe") | "emitted yosys-elaboration drops Elaborate the integration-heavy tops" |
| K03 drop the version proof | killed ("does not restore exactly the tool tree before its version proof") | "emitted ... drops Install the pinned Yosys and prove the version" (+ the old words) |
| K04 drop sv2v install | SURVIVED | "emitted yosys-elaboration drops Install the pinned sv2v release" |
| K05 drop Fetch RTL dependencies | SURVIVED | "emitted yosys-elaboration drops Fetch RTL dependencies" |
| K06 swap the two ooc self-tests | SURVIVED | "emitted yosys-elaboration reorders or repeats its steps" |
| K07 rewrite a self-test body | SURVIVED | "emitted yosys-elaboration changes Prove the result cache refuses a planted entry" |
| K08 add a consumer step | SURVIVED | "emitted yosys-elaboration adds Planted step" |
| K09 add a tool step after the build | SURVIVED | "emitted yosys-tool adds Touch the built tree" |
| K10 rewrite the tool evidence record | SURVIVED | "emitted yosys-tool changes Record actual job execution" |
| K11 set a workflow env after the digest | SURVIVED | "emitted workflow keys differ from the transformed derivation's: env" |
| K12 give the tool job an env after the digest | killed ("tool job env differs") | "emitted yosys-tool's job keys differ ..." (+ the old words) |
| K13 drop another job's step | SURVIVED | "emitted verilator-lint drops Fetch RTL dependencies" |
| K14 bind the restore to another recipe | killed ("does not restore exactly the tool tree") | "emitted tool cache and its restore bind different recipes" (+ the old words) |
| K15 drop the tool build | killed ("tool job does not carry ...") | "emitted yosys-tool drops Build Yosys from source on cache miss" (+ the old words) |
| G01 to G09 (round-2 derivation drops and swap) | killed by name | killed by name, same words |
| G10 extra tool-job step in the derivation | refused by the generator | refused by the generator |
| D01 digest omits the workflow `defaults` (S2) | SURVIVED | "tool key unchanged by an edit of its build inputs: the workflow defaults" |

At `1e0c5c09`: 11 survive (K01, K04 to K11, K13, D01). At `1c9a3e8e` (and `10e0b519`): none survives
(25 killed, 1 refused, control passes).

## Gate table (exact head `1c9a3e8e`, clean tree)

Run by `tools/run-gates.sh` (concurrent, one log and rc per gate) on CPython 3.14.8 with PyYAML 6.0.3
(`receipts/gates-py314/`), and on CPython 3.12.13 with PyYAML 6.0.2 installed by hash from
`ci/requirements-evidence.txt` into a fresh scratch venv (`receipts/gates-py312/`). The docs gates ran under the
pinned Markdown renderer in both runs. 32 of 32 rc 0 in each (`SUMMARY.txt`), 64 runs. The same 64 also
passed at `10e0b519` (`receipts/at-10e0b519/`).

| gate | py3.14 | py3.12 |
|---|---|---|
| `ci_gate_workflows.py --check` | 0 | 0 |
| `ci_gate_workflows_selftest.py` (86 "Fast Yosys tool" lines; ends `gate workflow and union controls: PASS`) | 0 | 0 |
| the other 12 commands of "CI scheduling and evidence controls" (11 selftests + `generate_ci_evidence_pins.py --check`) | 0 | 0 |
| `ci_scope.py --selftest` | 0 | 0 |
| `ci_events.py --check` (OK, 2199 items) | 0 | 0 |
| `ci_events.py --selftest` (PASS, 2199 items, 5258 arms; log gzipped, digest in `ci_events-selftest.summary.txt`) | 0 | 0 |
| runner contract gate: `act_ci.py --selftest`, then the 0555 install `--selftest --worktree` (two `selftest: PASS`, 1244 ok, 0 FAIL); offline, `act_ci.py` unchanged against dev | 0 | 0 |
| `check_py_idiom.py` and `--selftest` | 0 | 0 |
| `check_baremetal_only --check`, `check_hygiene --check`, `check_todo_ownership`, `measure_naming --check`, `measure_test_evidence --check`, `measure_fail_fast --check` | 0 | 0 |
| `docs_check`, `check_em_dash --base 76de691e` (0 findings over 133 added lines), `check_doc_style`, `gen_toc --check`, `gen_toc --verify-anchors`, `check_doc_paths` | 0 | 0 |

Not run: `bdd-conformance` (`cd tests && behave`). Nothing under `tests/` reads the changed files (`grep -rln
"ci_fast_tool_selftest\|CI_WORKFLOWS.md\|ci_gate_workflows" tests/` is empty). No RTL changed, so no Verilator,
Yosys or Vivado bank ran. No act and no Docker: the live act replay is the manager's (bootstrap rule; never
the host act slots).

## Hosted

Receipts under `receipts/hosted/`.

**Attempt 1 at `1c9a3e8e`: all four runs cancelled, unrelated to this change** (`attempt1-cancellation.txt`).
- In docs run 40356478658, `docs-gates-0` (job 121690197250, `timeout-minutes: 45`) ran from 16:11:35 to
  16:57:46. Its step 10, "Resolve exact package downloads 6" (`python3 scripts/ci_install_cache.py --packages
  librsvg2-bin ...`, unchanged by this PR, `ci_install_cache.py:59` runs `sudo apt-get update -qq` unbounded),
  printed nothing from 16:12:10 to 16:57:40 and was stopped at the 45-minute limit.
- Step 55, "CI scheduling and evidence controls", was skipped.
- The head's other runs were then cancelled, rtl-fast's `yosys-elaboration` among them at 17:00:26.
- **Candidate follow-up Issue (for the manager; not filed, out of scope):** bound the package-index update in
  `scripts/ci_install_cache.py` so that a mirror stall fails in minutes, not after the worker's whole limit.

**Re-runs.** I re-ran all jobs of rtl-fast and docs (attempt 2), then of elaborate and rtl-full, with `gh run
rerun`. This is the narrower form of the hosted trigger the brief permits by push. It adds no commit. The
watcher's `cancel()` only touches runs still in progress, so a completed run cannot be cancelled by a later
sibling failure.

**rtl-fast run 40356479027, attempt 2 at `1c9a3e8e`: success, 16 of 16 jobs** (`run-40356479027-attempt2*.json`).

| job | UTC (2026-10-26) | duration | evidence |
|---|---|---|---|
| Prepare pinned Yosys (121720749925) | 17:04:23 -> 17:04:34 | 11 s | "Cache restored from key: yosys-v0.66-86f2ddeb…-recipe-e15c97b1…-19cd9b6e…-ubuntu-24.04-Linux"; "Cache hit occurred on the primary key …, not saving cache."; no `/tmp/yosys-src` line (`tool-job-121720749925-excerpt.txt`) |
| yosys-elaboration (121720868622) | 17:11:12 -> 17:26:57 | 15 min 45 s | same key restored, `fail-on-cache-miss: true`, no `/tmp/yosys-src` line, "Yosys 0.66 (git sha1 86f2ddebc, g++ 13.3.0-6ubuntu2~24.04.1 -fPIC -O3)", all 13 steps success (`consumer-job-121720868622-excerpt.txt`, `-steps.json`) |
| rtl-fast aggregate (121733305648) | 17:27:14 -> 17:27:21 | 7 s | success |

Both jobs stay within their unchanged 30-minute timeouts. The key is the round-2 key; no workflow changed.

**docs run 40356478658, attempt 2: 9 of 9 success.** `docs-gates-0` (121720319131) ran "CI scheduling and
evidence controls" 17:17:54 to 17:18:21. That step printed 86 "Fast Yosys tool" lines, identical to the local
py3.14 run, the 36 emission lines among them (`docs-gates-0-121720319131-fast-tool-lines.txt`).

**`10e0b519`, rtl-fast run 40354998766:** "Prepare pinned Yosys" (121685529045) restored the same key in 14 s
(`tool-job-121685529045-excerpt.txt`). The run was cancelled by the workflow's `cancel-in-progress` concurrency
group when `1c9a3e8e` was pushed.

**elaborate 40356478638 and rtl-full 40356478782, attempt 2 (re-run 17:53 UTC):**
- elaborate is success, 6 of 6 jobs (`run-40356478638-attempt2*.json`).
- rtl-full is success, 18:56:44 UTC (`run-40356478782-attempt2*.json`). 34 jobs succeed, `verilator-suites`
  and `yosys-portability` among them. The one skipped job is "Physical gPTP (nightly and manual)".

**Act, offline only** (`receipts/act-offline-mapping.txt`, `tools/act_offline_mapping.py`). Dev's trusted
`act_ci.py` (blob `865867c3`, the same as the candidate's) was loaded as a module. Its
`validate_workflow_sandbox` accepts all four workflows of a `git archive` export of `1c9a3e8e`. The stages
order `yosys-tool`, `yosys-elaboration`, `rtl-fast`. The workflows are identical to `1e0c5c09`'s. No act,
Docker or act slot was used.

## Not done / owed elsewhere

- The live act replay (manager).
- The candidate follow-up Issue on the unbounded package-index update (see Hosted).
- External review at the new head; R707's re-review of R707-2-01.
- `Relates to #789` stays: the act replay acceptance item is still owed.
