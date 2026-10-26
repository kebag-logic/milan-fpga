[R707] NEGATIVE - exact head 1e0c5c09f6d5e41c8a80ec5e6179c1c762b94086

# R707-2: internal cleared-context re-review of PR #794 (issue #789)

- **Head:** `1e0c5c09f6d5e41c8a80ec5e6179c1c762b94086`, tree `f47bc6723eb731402df912605faf01d8b9371172`. Three commits on dev `76de691e5625cc4ea2f9a19def9e07c1183a14ee`. This round judges the delta `fddf3671..1e0c5c09`: the two round-2 commits `b45573c1` and `1e0c5c09`, which change 5 files.
- **Role:** internal independent reviewer, round R707-2 (a delta round answering R707-1). All five lenses were applied.
- **Verdict:** NEGATIVE. One MINOR finding is open: R707-2-01 (Tests, Docs). There are two SUGGESTIONs, no RESIDUE, and no BLOCKER or MAJOR.
- **Round-1 findings:**
  - **R707-1-01 is RESOLVED at its cause.** The key is now a digest of every build input of the emitted tool job. My round-1 probe body, rerun with only its key resolver extended for the new `hashFiles` term, now has no `STALE-SERVED` row. Five more environment and script plants all move the key, and three scheduling or outside-the-build edits do not.
  - **R707-1-02 is RESOLVED against its stated verification.** My round-1 mutants G01 to G05 are each refused by name.
  - **New gap (R707-2-01):** the new judge holds the intermediate derivation, not the emitted jobs. This delta added a second rtl-fast-only rewrite stage after that point (`bind_fast_tool_key`), and a self-test dropped there passes every judge.
- **Hosted (run 40321654840, this head):** both owed figures are met, each inside its unchanged 30-minute limit.
  - The cold tool job took **12 min 47 s**: "Cache not found", then "Cache saved".
  - `yosys-elaboration` restored that exact key in 2 s, ran no build, and took **12 min 45 s**.

## Findings

### R707-2-01: MINOR (Tests, Docs). The retention judge holds the derivation's output, not the emitted jobs; a self-test dropped by the delta's own post-transform key-binding stage passes every judge

- **Where:**
  - `scripts/ci_fast_tool_selftest.py:458-459`: `fast_tool_controls` runs `fast_tool_retention` on `gate_graph("rtl-fast", template)`. That is the derivation's output, before the install and runtime transforms and before `bind_fast_tool_key`.
  - `scripts/ci_fast_tool_selftest.py:303-306` plants a drop only inside `fast_yosys_tool`.
  - `scripts/ci_gate_workflows.py:252-271, 383-392`: round 2 added `bind_fast_tool_key`, an rtl-fast-only stage that `generate()` runs on the emitted workflow after both transforms. Nothing holds the consumer's step list after it.
  - `fast_tool_findings` does run on the emitted graph. It checks the build, need, restore and verdict, but not retention.
  - `docs/testing/CI_WORKFLOWS.md:845-850` (item 4) says that in `rtl-fast.yml`, `yosys-tool` and the rewritten `yosys-elaboration` are held by the generator comparison, and "`fast_tool_retention` ... also holds both of their step lists whole against the template".
  - PR #794 body, `docs/testing/CI_WORKFLOWS.md` row: "For `rtl-fast.yml`'s two jobs it is also held by `fast_tool_retention`."
- **Authority:**
  - Round-2 assignment (issuecomment-6415180907) item 2, and this round's probe (2): "a check holds `yosys-elaboration`'s retained checks ... after derivation, so a generator dropping one fails a named judge".
  - AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect."
  - AGENTS.md section 6, Docs: changed contracts are reflected accurately.
- **Evidence** (`receipts/mutants_r2/mutants.txt`, `.json`; `scripts/probe_mutants_r2.py`):
  - **N11** adds one line to `bind_fast_tool_key`. The line removes "Prove the result cache refuses a planted entry" from the emitted `yosys-elaboration`.
  - The workflow regenerates. `ci_gate_workflows.py --check`, `ci_gate_workflows_selftest.py` and `ci_events.py --check` all exit 0. **SURVIVED.**
  - The same drop placed in the derivation (G04) is refused by name. So the judge works, but at a point before the stage this delta added.
  - **The listed jobs are not the emitted ones.** The emitted `yosys-elaboration` has 14 steps; the judged derived list has 10. The emitted `yosys-tool` has 8 steps, not "exactly the checkout and the two moved steps" (`receipts/workflows/r1-vs-head-jobs.txt`; I compared the derived and emitted lists this round). So item 4's "both of their step lists" in `rtl-fast.yml` is not what the judge reads.
  - **Scope.** The shared install and runtime transforms were also post-derivation before this PR, and they are equally unheld for every job in the four files. That part predates the delta and is not this finding. The finding is the delta's own rtl-fast-only stage, and the docs and PR claim of a hold on the emitted lists.
- **Impact:** a later edit to the key-binding stage can delete a hosted self-test from `rtl-fast`'s `yosys-elaboration` while every gate stays green. That is the failure R707-1-02 was raised for, moved one stage later. The docs then tell a reader the emitted lists are held when they are not. Nothing is dropped at this head (`receipts/workflows/compare_consumer_dev_vs_head.txt`: 13 retained steps kept in order, bodies identical to dev's, ids aside), so this is latent, hence MINOR.
- **Required outcome:**
  - A named judge fails when any rtl-fast-specific stage after the derivation removes, adds, reorders or rewrites a `yosys-elaboration` or `yosys-tool` step. One way is to require the emitted jobs to equal the transformed derivation with only the two key strings different. Another is for the binding stage to refuse any change but those two keys, with a plant. This is not prescriptive.
  - `docs/testing/CI_WORKFLOWS.md:845-850` and the PR body say exactly which list each judge holds: the derived lists, the emitted lists, or both. If the shared transforms stay held only by the generator comparison, they say so, as item 4 already does for `rtl.yml`.
- **Verification:**
  - Rerun `scripts/probe_mutants_r2.py <git-backed head copy> <scratch> <out>`. N11 is CAUGHT with a named refusal. C00 still passes all judges, and G01 to G05 and N01 to N10 stay CAUGHT.
  - Re-read item 4 and the PR body against the judge's input.

### R707-2-S1: SUGGESTION (Robustness). The after-build guard identifies the evidence pair by `id` only

- **Where:** `scripts/ci_gate_workflows.py:240-243`.
- **What:** the guard checks that the ids after the build are exactly `ci_record`, `ci_upload`. An extra step is refused, which `fast_tool_key_inputs` proves. A rewritten body under the `ci_record` id is not refused. That step runs before the cache save, outside the digest.
- **Suggestion:** hold the two steps' content as the runtime transform emits it, or state in `CI_WORKFLOWS.md:344-346` that the guard identifies them by id. This is optional, because the pair is the shared runtime transform's own output.

### R707-2-S2: SUGGESTION (Tests). Add a workflow `defaults` plant to `fast_tool_key_inputs`

- **Where:** `docs/testing/CI_WORKFLOWS.md:329-331` names the workflow `defaults` as a digested input. `scripts/ci_fast_tool_selftest.py:361-371` plants the workflow `env`, but not `defaults`.
- **Evidence:** my plant E3 (`receipts/key_inputs_r2/key_inputs.txt`) changes the run shell under the workflow `defaults`, and the key moves. So the behaviour is right; only the self-test does not hold it.
- **Suggestion:** add a one-line plant so a regression that drops `defaults` from the digest is named. N01 already drops env and defaults together and is caught through env.

### R707-1-S1 (round 1): closed

- The author declined it with a reason in the PR body: the moved cache step must stay equal to the template's, and two judges deliberately enforce that.
- It was optional, so this is accepted.

## Brief probes (1) to (4)

1. **R707-1-01: the tool key binds every build input. Rerun, plus one planted environment edit.**
   - **Unchanged round-1 probe.** I ran `scripts/round1/probe_key_inputs.py`, byte-identical to the round-1 packet (sha256 `6e594ad8…`), on a git-backed copy of the head. It stops with an `AssertionError`, because its key resolver refuses any `${{` left in the key, and the key now ends `-${{ hashFiles('scripts/ci_install_cache.py') }}-ubuntu-24.04-${{ runner.os }}` (`receipts/key_inputs_round1_unmodified/`).
   - **Same probe, resolver extended.** `scripts/probe_key_inputs_r2.py` runs the round-1 probe body unchanged, and extends only the resolver to evaluate `hashFiles` as the runner does (`receipts/key_inputs_r2/key_inputs.txt`).
     - The resolved pristine key is `yosys-v0.66-86f2ddeb…-recipe-e15c97b1…-19cd9b6e…-ubuntu-24.04-Linux`. That is **byte-identical** to the key the hosted tool job saved and the consumer restored (`receipts/hosted/job-121571465201-cache-excerpt.txt`, `job-121577793452-cache-excerpt.txt`).
     - **No `STALE-SERVED` row.** The three round-1 stale rows now move the key: workflow `env` `CXXFLAGS`, workflow `env` `CXXSTD`, and the install-transform rewrite of the build. The version, source, recipe and image rows still move it, and "edit outside the recipe" keeps `key-changed=False`.
     - **Round-1 row "yosys-elaboration job env gains CXXFLAGS".** Round 1 labelled it `tool-changes=False`, because the tool job did not carry a job `env` then. The tool job now carries it, and the key moves, which is correct.
     - **Round-1 row "workflow env gains an unrelated name".** It now moves the key. That is deliberate and documented (`CI_WORKFLOWS.md:329-331`: every env entry is digested, and a `VERILATOR_VERSION` bump rebuilds Yosys once in the tool job). It is over-binding, not stale-serving.
   - **Round-2 plants.**
     - E1, the planted environment edit (workflow `env` `CXXFLAGS=-O0`): key moves.
     - E2, consumer job `env` (carried into the tool job): key moves.
     - E3, workflow `defaults` run shell: key moves.
     - E4, job-budget step exports `CXXFLAGS`: key moves.
     - E5, a content edit of `scripts/ci_install_cache.py`, bound through `hashFiles`: key moves.
     - E6, consumer `if` (schedules the tool job only): key unchanged.
     - E7, consumer timeout: key unchanged.
     - E8, a `Fetch RTL dependencies` body edit (outside the build): key unchanged.
   - **What reads the build.** `scripts/ci_install_cache.py` imports no repository module and reads no repository file (`:11-19, 50-69`), so the one `hashFiles` binding is complete.
   - **Generator mutants on the key** (`receipts/mutants_r2/`), all CAUGHT:
     - G08: constant digest.
     - G09: no image.
     - G10: workflow digest kept; the generator refuses it.
     - N01: no workflow env or defaults.
     - N02: no job keys.
     - N03: build step only, the round-1 behaviour.
     - N04: no script binding.
     - N05: restore not rebound.
     - N06: the tool job carries no env.
     - N07: after-build guard removed.
     - N08: stand-in left.
     - N09: read scan dead.
     - N10: unmodelled job keys accepted.
2. **R707-1-02: the retained checks are held against the template. Rerun, plus one planted drop.**
   - **Unchanged round-1 probe.** I ran `scripts/round1/probe_mutants.py`, byte-identical (sha256 `2b3346ef…`), on a git-backed head copy (`receipts/mutants_round1_unmodified/`). The control passes all three judges. G06, G07, G11 to G14, G16 and W02, W03 are CAUGHT. G01 to G05, G08 to G10, G15, G17 and W01 report `ERROR` (anchor count 0), because round 2 rewrote the code those anchors matched.
   - **Re-anchored port.** `scripts/probe_mutants_r2.py` makes the same edits at the head's code (`receipts/mutants_r2/`). G01 to G05, each dropping one retained step, are CAUGHT, and each is refused by name: "yosys-elaboration drops <step>". G15 (the consumer keeps its build) is named. W01 to W04, hand edits of the generated file, are refused by both check modes. The control passes.
   - **The one survivor is N11**, a drop in the post-transform stage (R707-2-01).
   - My results match the author's published mutant receipts at this head (`author-r2/receipts/probes/mutants-1e0c5c09.txt`, sha256 verified against the packet manifest).
3. **Hosted run 40321654840**, rtl-fast at `1e0c5c09`, `pull_request`, attempt 1, conclusion success (`receipts/hosted/`).
   - **Cold tool job, "Prepare pinned Yosys"** (job 121571465201, `timeout-minutes: 30`). It ran 12:29:23 to 12:42:10 UTC, **12 min 47 s**. The build step took 12 min 26 s.
     - The log reads "Cache not found for input keys: yosys-v0.66-…-recipe-e15c97b1…-19cd9b6e…-ubuntu-24.04-Linux".
     - Then "Cache saved with key:" with that key, 12:42:08.
   - **Consumer, `yosys-elaboration`** (job 121577793452, `timeout-minutes: 30`). It ran 12:45:02 to 12:57:47, **12 min 45 s**.
     - The restore took 2 s ("Cache restored from key:" with the identical key, ~19 MB).
     - The log has no `/tmp/yosys-src` line, so no build ran.
     - The version proof prints `Yosys 0.66 (git sha1 86f2ddebc, g++ 13.3.0-6ubuntu2~24.04.1 -fPIC -O3)`.
     - All seven retained checks passed. The post step skipped the save on the primary-key hit.
   - **This head edits a workflow**: `rtl-fast.yml` against dev.
   - **The rest of the run.** The `rtl-fast` aggregate succeeded, and so did all 16 jobs of the run.
   - **The other workflows at this head.** `docs` (9 of 9), `elaborate` (6 of 6) and `rtl-full` (34 success) are green. `rtl-full`'s only skipped job is "Physical gPTP (nightly and manual)". Its `verilator-suites` and `yosys-portability` executed and succeeded.
   - **The new control ran hosted.** The hosted `docs-gates-0` job (121567822650) ran the "CI scheduling and evidence controls" step, which printed the same 50 "Fast Yosys tool" lines my local run prints (`receipts/hosted/docs-gates-0-fast-tool-lines.txt`).
4. **Nothing else in the workflows changed behaviour since round 1** (`receipts/workflows/`).
   - `git diff fddf3671..1e0c5c09 -- .github/` touches only `rtl-fast.yml`, 4 lines: the tool cache key and the consumer restore key.
   - Parsed job by job, 14 of 16 jobs are identical, and so are the top-level keys. The two differing jobs differ only in that one `with.key`, with the same step counts (8 and 14) and no job-level key changed.
   - The templates and the other three workflows are untouched across the PR. Every timeout equals dev's, and `yosys-tool` is 30.

## Gates at the exact head

- **All 23 gates exit 0** (`receipts/gates/SUMMARY.txt`, `*.log`, `*.rc`). They ran concurrently, under a private environment with `tools/markdown/requirements.txt` installed by hash, on CPython 3.14.8 with PyYAML 6.0.3. They are:
  - `ci_gate_workflows.py --check`;
  - `ci_gate_workflows_selftest.py`, which includes the new `ci_fast_tool_selftest.py` (50 "Fast Yosys tool" lines);
  - the rest of the "CI scheduling and evidence controls" list;
  - `ci_scope.py --selftest`;
  - `ci_events.py --check`: OK, 2199 items;
  - `ci_events.py --selftest`: PASS, 2199 items, 5258 arms;
  - `docs_check`, `check_em_dash --base 76de691e` (0 findings over 101 added lines), `check_doc_style`, `gen_toc --check`, `check_doc_paths`;
  - `check_py_idiom`.
- **Runner self-tests.** `act_ci.py --selftest` and the 0555 runner contract gate were not run by me, because the brief excludes them. The author's receipts at this head (`author-r2/receipts/gates-py31{2,4}/act_ci-runner-contract.{log,rc}`) are sha256-verified against `review-evidence/789-r1/MANIFEST.json` at `2f109261`.
  - Each reads rc 0, two `selftest: PASS` lines, 1244 `ok` lines (623 plus 621), and no line starting `FAIL`.
  - That packet's commit is not GPG-signed (GitHub verification: "unsigned"). I verified the receipts by the manifest's published SHA-256, and 16 of 16 sampled files match.
  - `act_ci.py` is unchanged against dev.

## Comment rule and residue

- **Source and workflow lines.** The 494 added lines of the delta (652 PR-wide) contain no bench lane label, lane name, review round, reviewer ID or issue-comment ID (`receipts/comment-rule/scan.txt`). Comments name `#789` and state behaviour.
- **Docs delta.** It names no lane or reviewer either.
- **Result:** no RESIDUE.

## Lens ledger (reviewer-owned)

| lens | result | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #789 Decision and Acceptance; round-2 assignment issuecomment-6415180907; `scripts/ci_gate_workflows.py:36-67, 215-271, 300-337, 383-392`; `.github/workflows/rtl-fast.yml:254-377` (key lines 286-287, 374-375); hosted jobs 121571465201 and 121577793452 (`receipts/hosted/`); `receipts/key_inputs_r2/`; R707-1-01 resolved; generator-only change (`ci_gate_workflows.py --check` rc 0, W01 to W04 refused) | R707-2 | 1e0c5c09f6d5e41c8a80ec5e6179c1c762b94086 |
| RTL | CLEAN | Job graph: `needs`, `if`, ordering, timeouts and the critical path, via `receipts/workflows/r1-vs-head-jobs.txt` and `compare_consumer_dev_vs_head.txt`; `git diff --stat fddf3671..1e0c5c09` (no HDL, `syn/` or constraint file); RTL-facing steps passed on hosted job 121577793452 with bodies identical to dev's | R707-2 | 1e0c5c09f6d5e41c8a80ec5e6179c1c762b94086 |
| Robustness | CLEAN (S1 only) | Exact restore with `fail-on-cache-miss` and no fallback; `hashFiles` evaluated after checkout in both jobs (`rtl-fast.yml:261-287, 344-377`) and resolved identically to hosted; build-environment plants E1 to E5 versus scheduling and outside edits E6 to E8; after-build guard and unmodelled job-key refusal (N07, N10); `ci_install_cache.py:11-69` reads no repository file | R707-2 | 1e0c5c09f6d5e41c8a80ec5e6179c1c762b94086 |
| Tests | UNCLEAN (R707-2-01) | `scripts/ci_fast_tool_selftest.py:1-477`; `scripts/ci_gate_workflows_selftest.py:27, 537`; 23 exact-head gates (`receipts/gates/`); round-1 probes rerun unmodified and ported (`receipts/*_round1_unmodified/`, `receipts/mutants_r2/`, 24 mutants plus a control); hosted `docs-gates-0` control output | R707-2 | 1e0c5c09f6d5e41c8a80ec5e6179c1c762b94086 |
| Docs | UNCLEAN (R707-2-01) | `docs/testing/CI_WORKFLOWS.md:317-380, 824-856, 1208-1215, 3338-3353`; PR #794 body (`Description`, `Round 2`, `New checks`, hosted table); docs gates under the pinned renderer; comment-rule scan | R707-2 | 1e0c5c09f6d5e41c8a80ec5e6179c1c762b94086 |

Round 1's RTL lens was CLEAN at `fddf3671`. The delta changes the two key strings and generator code only. I re-covered RTL at this head from the job-graph comparison.

## Prior public review findings on this PR

I read R707-1 for its probes and named findings, as the assignment requires, after my own pass over the delta. I read the external review only after the verdict and ledger above were written.

| prior finding | at this head | evidence |
|---|---|---|
| R707-1-01, MINOR (Conformance, Robustness, Tests) | **RESOLVED** | Probe (1): no `STALE-SERVED` row; E1 to E5 move the key, E6 to E8 do not; N01 to N04, N06 and N08 to N09 caught |
| R707-1-02, MINOR (Tests, Docs) | **RESOLVED** against its stated verification: G01 to G05 are refused by name, and docs item 4 and the #406 summary now name the holds. The narrower remaining gap at the new post-transform stage is filed as R707-2-01. | Probe (2); `receipts/mutants_r2/` |
| R707-1-S1, SUGGESTION (RTL) | Closed: declined with a reason | PR body, "Round 2 (R707-1)" |
| R708-1 (external, POSITIVE at `fddf3671`) | Files no BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION, so there is nothing to resolve or retain. The PR has no review threads or review comments. | PR #794 issuecomment-6414349885 |

## Real limits

- **No act, Docker or host runner.** I ran no act, Docker, host `act_ci.py` or its self-test, and not the 0555 contract gate. For those I rely on the author's manifest-verified receipts. The live act replay is not run. With a miss fatal, it must show act's cache server saving in `yosys-tool` and restoring the `hashFiles`-bearing key in `yosys-elaboration`.
- **No source bank.** No manager source bank ran at this head, and I claim none. My execution evidence is my own gate reruns and probes, plus the author's receipts.
- **Models, not builds.** The key plants are in-memory template and generator edits. I built no Yosys. Round 1's Makefile lines and the hosted banner show that the inputs reach the binary.
- **Package versions.** The distribution's package versions, the compiler's among them, are resolved at run time and are not in the key. The key names the image by its label, as #789's Decision specifies ("the runner image"), and `CI_WORKFLOWS.md:349-351` says so. I judge this within the frozen Decision, not a finding.
- **No hosted warm hit across a workflow edit.** No hosted run yet shows the tool job *hitting* across two heads where a workflow edit leaves the build inputs unchanged. This head's new key was a one-time cold build. Probes E6 to E8 and the self-test show that such an edit keeps the key.
- **Interpreter.** CPython 3.14.8 only. The 3.12 pair is the author's receipts.
- **Probe environment.** The round-1 probes need a git-backed copy (the Makefiles call `git ls-files` in the submodules). My first export without `.git` failed the control, so I discarded it and reran on a full copy of the clone.
- **No hardware.** Physical calibration was NOT RUN, and field skips are not hardware proof. No RTL changed.

## Pending manager duties

- The re-review of a fix for R707-2-01 at a new head.
- The live act replay of the head, including the cache save and exact-key restore across the two jobs.
- The external review at this head: R708-1 was at `fddf3671`.
- Hosted acceptance at the final head, executed jobs versus skipped contexts. At this head all four runs are green, as listed above.
- The PR body's `Relates to #789` versus `Closes #789` once the act replay is in.
- The current-dev merge candidate and its banks at the merge turn: source base `76de691e`, live dev `76de691e5625cc4ea2f9a19def9e07c1183a14ee`.

R707-2 FINISHED
