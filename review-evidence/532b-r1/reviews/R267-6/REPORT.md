[R267] POSITIVE - exact head ad4a5ff6ba15502ed60d58b3ca91830b50fa9e1c

# R267-6: external review of PR #570 (issue #532, pasta invoked name)

- Head: `ad4a5ff6ba15502ed60d58b3ca91830b50fa9e1c`, tree `86b7eb522d05b8f4fc998695bdde0299df998fa2`
- Base: `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a` (sole parent; live `dev` at round start)
- Scope: one commit, two files (`scripts/act_ci.py` +60/-1, `docs/testing/CI_WORKFLOWS.md` +4). Raw diff: `receipts/diff.patch`.
- Round type: Round 1 of PR #570. Partial for #532 ("Relates to #532"); the issue stays open until the live slot proof prints `PROVED`.
- Reviewer role: external, cleared context, reconstructed from public state only.

## Authorities reconstructed

1. `AGENTS.md` sections 3-8 and `CONTRIBUTING.md` 2.1-2.2, 3, 5, 6 (lens list, verdict form, one-line commits, em-dash rule, bootstrap rule for the runner).
2. `docs/README.md` authority order.
3. Issue #532 body (acceptance 1-6) and the decisions in issue comments 5796770637 (slot design, uplink argv), 5825994510 (live proof after merge) and 5845269093 (the failure and the frozen decision for this lane: items 1-3).
4. Executor comments 5845283079 (TAKEN) and 5845335564 (REVIEW READY); PR #570 body.
5. `docs/testing/CI_WORKFLOWS.md` 1785-1869 (isolated slot contract).
6. The diff, the commit object, and every `require_tool` caller in `scripts/act_ci.py`.
7. Public executable evidence at `c054ca73:review-evidence/532b-r1/` (author subdirectory; copies of the files used are in `receipts/manager_evidence/`).

Frozen scope for this lane (comment 5845269093): (1) launch the uplink by the absolute path found on `SAFE_PATH` without resolving the final symlink; every other tool keeps its resolution; `SAFE_PATH` provenance kept; (2) offline tests: a fake multi-call tool through a symlink named `pasta` sees `pasta`; a re-resolving mutant fails; existing self-tests pass; (3) live proof after merge (not in this PR).

## Independent results

### The change

`scripts/act_ci.py:701-711`: `require_tool` still looks up only on `SAFE_PATH` (`shutil.which(name, path=SAFE_PATH)`, line 705) and still refuses absence (706-707). Only for `name == "pasta"` it returns `Path(found).absolute()` (709-710) instead of `.resolve()` (711). `SAFE_PATH` (line 83) is six absolute directories, so `.absolute()` is a no-op on the lookup result and never consults the working directory.

Caller audit (raw grep, all callers of `require_tool` in the file): the literal `"pasta"` reaches `require_tool` at exactly two sites, `slot_uplink_command` (`scripts/act_ci.py:3993`, the uplink executable after `--`) and the preflight existence loop over `SLOT_HOST_TOOLS` (`scripts/act_ci.py:4246-4247`, result discarded). Every other caller (`gh`, `git`, `sudo`, `chown`, `env`, `docker`, `nsenter`, `touch`, `systemd-run`, `dockerd`, `ip`, `systemctl`, `nft`, `kill`, `ps`, `sh`) passes a different literal and so keeps `.resolve()`. The change is therefore confined to the uplink's pasta invocation.

Host measurement (`receipts/host_tool_lookup.txt`): on this host `require_tool("pasta")` now returns `/usr/sbin/pasta` (the first `SAFE_PATH` hit; `/usr/sbin -> bin`, `/usr/bin/pasta -> passt`), every other slot tool returns its resolved `/usr/bin/...` path, and every `SAFE_PATH` directory that exists as a directory is `root:root 0755`.

Real-binary mode selection (`receipts/real_multicall_probe.txt`, reproduced by `probes/real_multicall_probe.sh` into `receipts/real_multicall_probe_script.txt`; only `--version` and an option-parse failure were executed): the lookup spelling runs as `pasta 2026_07_28.f8df3f1`; the resolved target runs as `passt 2026_07_28.f8df3f1` and rejects `--netns-only` with `--netns-only is for pasta mode only`, the exact live failure line quoted in comment 5845269093.

Provenance: no path from the invocation directory or ambient `PATH` can be selected. The lookup is unchanged, and the new arm with an executable `pasta` impostor on ambient `PATH` passes. Mutants M4 and M5 (below) that consult ambient `PATH` are killed. The trust basis is unchanged: before and after, the executed file is whatever the root-owned `SAFE_PATH` entry points to. The runner never ran an ownership or hash check on a resolved tool, so no identity check is lost. The decision's "identity checks may still record the resolved target" is permissive. The code records none at runtime; the new self-test arm binds the resolved identity (`scripts/act_ci.py:11451-11454`).

### Offline gates (all run in the foreground at the exact head)

| Command | Result | Receipt |
|---|---|---|
| `python3 -I scripts/act_ci.py --selftest` | rc 0, `selftest: PASS`, 432 `ok` arms, 0 FAIL | `receipts/selftest_isolated.log` |
| `python3 scripts/act_ci.py --selftest` (docs.yml "Local act runner contract gate" form, `.github/workflows/docs.yml:388-389`) | rc 0, 432 arms | `receipts/selftest_docs_contract_form.log` |
| same at base `7eb3b0d4` (exported tree) | rc 0, 425 arms (7 new arms at head) | `receipts/base_7eb3b0d4_selftest.log` |
| `bash scripts/act_slot_proof.sh --selftest` | rc 0, `PASS (44 cases)` | `receipts/slot_proof_selftest.log` |
| `python3 scripts/ci_events.py --check` | rc 0, 1655 items | `receipts/ci_events_check.log` |
| `python3 scripts/ci_events.py --selftest` | rc 0, 1655 items, 2197 arms | `receipts/ci_events_selftest.log` |
| `docs_check.py`, `check_doc_style.py`, `check_py_idiom.py`, `check_sh_idiom.py`, `check_doc_paths.py`, `check_baremetal_only.py --check`, `git diff --check <base> HEAD` | all rc 0 | `receipts/docs_style_gates.log` |
| `check_em_dash.py --base <base>`, `gen_toc.py --check` | rc 2 without the pinned renderer; rc 0 with `tools/markdown/requirements.txt` installed by hash in a scratch venv (em-dash 0 findings over 4 added lines, 339/339 arms; TOC OK) | `receipts/docs_style_gates.log` |

Python 3.14.7. The gates are reproducible with `probes/run_offline_gates.sh`.

### Mutation probe (`probes/mutation_probe.py`, receipt `receipts/mutation_probe.txt`)

Each variant is a fresh `git archive` of the head with one exact-string edit to `scripts/act_ci.py`, followed by the full `python3 -I scripts/act_ci.py --selftest`.

| Variant | Exit | Failing arms | Verdict |
|---|---|---|---|
| M0 unchanged control | 0 | none (432 ok) | PASS |
| M1 `require_tool` resolves pasta again (the pre-fix code) | 1 | SAFE_PATH spelling; uplink observes `pasta` | KILLED |
| M2 uplink re-resolves at launch (`slot_uplink_command`) | 1 | uplink observes `pasta`; pinned uplink argv | KILLED |
| M3 every tool keeps its symlink name | 1 | every other slot host tool still resolves | KILLED |
| M4 lookup on ambient `PATH` | 1 | SAFE_PATH spelling; resolved identity | KILLED |
| M5 pasta only looked up on ambient `PATH` | 1 | SAFE_PATH spelling; resolved identity; uplink observes `pasta` | KILLED |
| M6 pasta via `os.path.realpath` | 1 | SAFE_PATH spelling; uplink observes `pasta` | KILLED |
| M7 pasta rebuilt from resolved parent + target name | 1 | SAFE_PATH spelling; uplink observes `pasta` | KILLED |

Seven of seven mutants were killed and the control passed. This independently agrees with the author's published `path-mutations.log` and `full-mutant-result.json` (3/3 plus the full re-resolve mutant).

## Findings

No `BLOCKER`, `MAJOR` or `MINOR` finding. Two optional suggestions from the independent pass (a third, Tests, is recorded under the concurrent-review section below):

```text
[R267] SUGGESTION Docs - docs/testing/CI_WORKFLOWS.md:1855-1857 - rule sits away from the uplink bullet and says less than the code does
Requirement/evidence: the uplink is described at CI_WORKFLOWS.md:1797-1801; the new rule appears 58 lines later, after the bare-metal gate paragraph. "Its final symlink stays unresolved" is true, but the code resolves no component at all: on this host the uplink path is /usr/sbin/pasta, reached through the /usr/sbin -> bin directory link (receipts/host_tool_lookup.txt).
Impact: none on behaviour; a reader of the live-proof transcript may expect /usr/bin/pasta.
Required change: optional. Attach the rule to the uplink bullet and say the SAFE_PATH spelling is used as found.
Verification: docs gates as above.
```

```text
[R267] SUGGESTION Robustness - scripts/act_ci.py:709 - invoked-name preservation is keyed on the literal tool name inside the shared lookup
Requirement/evidence: the decision scoped the fix to the uplink launch; the implementation places it in require_tool for every caller that asks for "pasta". Today the only other caller discards the result (scripts/act_ci.py:4246-4247), so behaviour equals the decision.
Impact: none today. A future argv[0]-sensitive host tool added to SLOT_HOST_TOOLS is not covered; a future non-uplink pasta caller inherits the unresolved spelling.
Required change: optional. Keep as is, or name the set of multi-call tools beside SLOT_HOST_TOOLS.
Verification: the existing "every other slot host tool still resolves" arm plus M3.
```

## Per-lens results

```text
[R267] PASS Conformance - scripts/act_ci.py:701-711, 3979-4011, 4246-4247; issue #532 comment 5845269093 items 1-2; receipts/real_multicall_probe.txt - The uplink executable is the unresolved absolute SAFE_PATH path; all other callers keep .resolve(); SAFE_PATH lookup unchanged. The real host binary selects pasta mode by that spelling and passt mode by the resolved target. The offline tests required by item 2 exist and fail against the re-resolving mutant. Item 3 (the live proof) is out of scope for this PR, and the PR says so ("Relates to #532").
[R267] PASS RTL - receipts/clone_integrity.txt (git diff --raw base..head lists only scripts/act_ci.py and docs/testing/CI_WORKFLOWS.md; gitlinks unchanged) and scripts/act_ci.py:3979-4011 - No HDL, processor or submodule artifact is touched, so clock, reset, CDC and FSM checks do not apply. The architecture and interface part was applied to the runner. The require_tool contract (SAFE_PATH-only, refusal on absence) and the slot_uplink_command argv shape are preserved word for word apart from the executable spelling, and the pinned argv arm still passes.
[R267] PASS Robustness - scripts/act_ci.py:705-711, 11470-11480; receipts/host_tool_lookup.txt; receipts/mutation_probe.txt (M4, M5) - Absent, dangling and non-executable pasta refuse. An ambient-PATH impostor is never chosen. .absolute() cannot bind the working directory because SAFE_PATH is absolute. The trust basis is unchanged: root-owned SAFE_PATH directories, and no resolved-identity check existed before. The preflight existence check still covers pasta before the lock.
[R267] PASS Tests - scripts/act_ci.py:11428-11480, 12480; receipts/mutation_probe.txt; receipts/base_7eb3b0d4_selftest.log - 7 new arms (425 -> 432), wired into selftest_slot_stages. The fake is a real executable reached through a real symlink named pasta. The uplink tail from slot_uplink_command is executed with an untrusted PATH and cwd. 7/7 mutants were killed, including the re-resolving one required by item 2, and the control passes. The limit that systemd-run is not executed is stated in the code comment and below.
[R267] PASS Docs - docs/testing/CI_WORKFLOWS.md:1855-1857 against scripts/act_ci.py:701-711; receipts/docs_style_gates.log; PR #570 body; issue comment 5845335564 - The text matches the code (pasta keeps its SAFE_PATH spelling, other tools resolve). No conflicting contract statement exists elsewhere (grep of docs/, CONTRIBUTING.md, AGENTS.md). The docs, em-dash, style, TOC and path gates pass. The commit is one line with no trailers. The issue and PR carry enough evidence for a cold reviewer. Placement is only a SUGGESTION.
```

## Completion ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `scripts/act_ci.py:701-711,3979-4011,4246-4247`; #532 comments 5796770637, 5845269093; `receipts/real_multicall_probe.txt` | R267-6 | `ad4a5ff6ba15502ed60d58b3ca91830b50fa9e1c` |
| RTL | CLEAN (no HDL in diff; runner interface contract checked) | `receipts/clone_integrity.txt` (raw diff, gitlinks); `scripts/act_ci.py:3979-4011,11483-11504` | R267-6 | `ad4a5ff6ba15502ed60d58b3ca91830b50fa9e1c` |
| Robustness | CLEAN (one SUGGESTION) | `scripts/act_ci.py:83,705-711,11470-11480`; `receipts/host_tool_lookup.txt`; mutants M4, M5 | R267-6 | `ad4a5ff6ba15502ed60d58b3ca91830b50fa9e1c` |
| Tests | CLEAN | `scripts/act_ci.py:11428-11480,12480`; `receipts/mutation_probe.txt`; self-test logs at head and base; `receipts/slot_proof_selftest.log`; `receipts/ci_events_*.log` | R267-6 | `ad4a5ff6ba15502ed60d58b3ca91830b50fa9e1c` |
| Docs | CLEAN (one SUGGESTION) | `docs/testing/CI_WORKFLOWS.md:1785-1869`; `receipts/docs_style_gates.log`; commit object; PR body | R267-6 | `ad4a5ff6ba15502ed60d58b3ca91830b50fa9e1c` |

Prior public review findings on PR #570: none existed when this round started. The PR had no reviews, no inline comments, and only the two review-start notices (receipts `pr570_*.json`). The round is independent.

## Concurrent review on this PR (read only after the verdict and ledger above were written)

The internal reviewer's round R266-6 on this head (PR comment 5845547496) was published while this round ran. It carries no BLOCKER, MAJOR or MINOR finding, only two SUGGESTIONs. Their disposition at this head:

- **R266-6 S1 (Tests), retained as a SUGGESTION and independently reproduced.** The "every other slot host tool still resolves" arm (`scripts/act_ci.py:11455-11458`) covers only `SLOT_HOST_TOOLS`. This round's added mutant M8 also preserves the name of the non-slot tool `sudo`. It survives the full self-test: exit 0, 432 ok (`receipts/mutation_probe_with_M8.txt`; the probe exits 1 only because M8 survived, and M0-M7 are unchanged). Decision item 1 requires that other tools keep their resolution. Item 2 names only the pasta and re-resolve tests. The one production branch is a single literal equality, so this stays optional. It is recorded here as `[R267] SUGGESTION Tests - scripts/act_ci.py:11455-11458 - non-slot require_tool callers are not pinned to resolution`, and the Tests ledger row remains CLEAN, since a SUGGESTION does not affect coverage.
- **R266-6 S2 (Docs), retained as a SUGGESTION.** Its first point is the same observation as this round's Docs suggestion (no component of the `SAFE_PATH` spelling is resolved). Its second point, that the self-test list at `docs/testing/CI_WORKFLOWS.md:2077-2112` does not name the new lookup arms, is optional; that list does not claim to be exhaustive.

Neither changes this round's verdict or ledger.

## Real limits

- `systemd-run` and the service manager's exec of the uplink were not executed; that would need privilege or host service-manager side effects, which this round did not use. That argv[0] survives that path is inferred from two facts. The live failure transcript shows `systemd-run` passing the given path through verbatim (`Starting [systemd-run] /usr/bin/passt`), and the real binary selects its mode from the invoked name (direct exec probe). Only the post-merge live proof (item 3) closes this.
- The new test executes the uplink tail directly, not through the unit launcher, as its own code comment states.
- No Docker, act, `--sudo`, live self-test, host `act_ci` orchestration, network namespace or hardware was used. Physical calibration was NOT RUN. Hosted skipped contexts (for example `Physical gPTP (nightly and manual)`) are not hardware proof.
- The offline `--selftest` of the candidate runner was run on the reviewer host as this assignment directs, with `TMPDIR` in the packet scratch directory. It needs no Docker, per the docs.yml step comment.
- The "manager's full source static/builder and native banks" evidence was not located in the public evidence directory at `c054ca73`, which holds only the author subdirectory. This round did not verify it.
- Hosted state at inspection (`receipts/hosted_check_runs.tsv`): `rtl-fast`, `docs-check`, `docs-check-no-git`, `wire-accountability`, `elaborate`, `full-ci-gate` and Yosys shards 0-3 were successful at the exact head. Verilator shards 1/5 and 4/5 were still in progress, and the `verilator-suites` and `yosys-portability` aggregates were not yet emitted.
- A comment-list command during the final prior-findings check printed the first line of a concurrent review comment from the other reviewer on this PR. Its body was read only after this verdict and ledger were written; see the section above.
- The clone was restored and verified: no tracked, index or mode change; the index tree equals the head tree; gitlinks are unchanged. The only generated artifact, `scripts/__pycache__/` from the gate runs, was removed, and `git status --porcelain --ignored` is empty (`receipts/clone_integrity.txt`).

## Pending manager duties

- Wait for the exact-head `verilator-suites` and `yosys-portability` aggregates, and own hosted and act acceptance.
- Publish or point to the source static/builder and native bank evidence for this head.
- Build and validate the current-dev candidate merge result at the merge turn (source base `7eb3b0d4` equals live dev at round start).
- Obtain the second independent positive review, and get explicit maintainer merge authorization.
- After merge, run containment and then the live `scripts/act_slot_proof.sh` from the trusted merged runner (item 3). On this host the uplink unit will show `/usr/sbin/pasta`, which is the expected `SAFE_PATH` spelling. #532 stays open until `PROVED`.

R267-6 FINISHED
