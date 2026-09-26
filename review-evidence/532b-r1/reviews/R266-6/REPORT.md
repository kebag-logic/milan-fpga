[R266] POSITIVE - exact head ad4a5ff6ba15502ed60d58b3ca91830b50fa9e1c

# R266-6: independent internal review of PR #570 (issue #532, partial)

- Head: `ad4a5ff6ba15502ed60d58b3ca91830b50fa9e1c`, tree `86b7eb522d05b8f4fc998695bdde0299df998fa2`.
- Base: `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`, the live `dev` tip at review time.
- Diff: two files, +64/-1.
  - `scripts/act_ci.py` (+60/-1).
  - `docs/testing/CI_WORKFLOWS.md` (+4).
  - No HDL, workflow or submodule change.
- Scope authority: the [issue 532 decision](https://github.com/kebag-logic/milan-fpga/issues/532#issuecomment-5845269093), items 1 and 2. Item 3, the live proof rerun after merge, belongs to the manager and is not claimed here.
- Reviewer: the internal reviewer, working from a cleared context and an isolated detached clone. Only public state was used.
- Prior findings on PR #570: none. At 2026-09-26T10:34Z the PR had no reviews and no inline comments, and its only comments were the two review-start notices. There is nothing to resolve or retain.

## Verdict

**POSITIVE.** There is no open BLOCKER, MAJOR or MINOR. There are two SUGGESTIONs (S1, S2), and neither affects coverage.

The fix does what the decision asks, and nothing more:

- `require_tool` still does its lookup only through `shutil.which(name, path=SAFE_PATH)`.
- For `pasta` alone it returns that absolute SAFE_PATH hit without resolving it.
- Every other tool still returns `Path(found).resolve()`.

Two host probes confirm the fix end to end:

- On this host, lookup yields `/usr/sbin/pasta` (old rule: `/usr/bin/passt`). The other 16 tool names the runner looks up are byte-identical to the old rule.
- A real `systemd-run` (systemd 262) started a unit through a symlink named `pasta` pointing at the real `passt` binary. The launched binary ran in pasta mode, while `/usr/bin/passt` refused `--netns-only`. This is the exact failure from the first live run.

## Findings

### S1: SUGGESTION (Tests)

- **Where:** `scripts/act_ci.py:11455-11458`, the arm "every other slot host tool still resolves its final symlink".
- **Evidence:** the arm iterates `SLOT_HOST_TOOLS` only. The runner also looks up `chown`, `docker`, `env`, `gh`, `git`, `kill`, `ps`, `sh` and `sudo`.
  - Mutant M10 widens the preserved set to `("pasta", "sudo")`. It survives the full `--selftest` (`receipts/mutation-results.json`).
  - M11, which widens it to the slot tool `ip`, is killed.
  - The arm's name is accurate: it claims slot host tools. So this is not an overclaim.
- **Impact:** a later edit could let a non-slot tool bypass final-symlink resolution with no offline signal. Today the rule is one literal equality at `scripts/act_ci.py:709`, so the risk is low.
- **Optional outcome:** check every name the runner passes to `require_tool`, not only `SLOT_HOST_TOOLS`.
- **Verification:** M10 is killed.

### S2: SUGGESTION (Docs)

- **Where:** `docs/testing/CI_WORKFLOWS.md:1855-1857`, and the list at `docs/testing/CI_WORKFLOWS.md:2077-2112`.
- **Evidence, first point:** the new paragraph says the uplink "uses the absolute `pasta` path from `SAFE_PATH`" and that "its final symlink stays unresolved". Both are true. But no component of the path is resolved:
  - On this host the uplink path is `/usr/sbin/pasta`, and `/usr/sbin` is itself a symlink to `bin` (`receipts/host-lookup-probe.log`).
  - A reader could infer that the directory part is canonicalised.
- **Evidence, second point:** the list "The offline self-test of the runner pins:" does not mention the new lookup arms: SAFE_PATH provenance against an ambient PATH impostor, the invoked name, and the missing, dangling and non-executable refusals.
  - The list does not claim to be exhaustive, and nothing in it is false.
  - The word-for-word uplink pin it names runs through `fake_host_tool` (`scripts/act_ci.py:10814`). That pin never exercises `require_tool`.
- **Impact:** a cold reader slightly under-reads what is pinned, and may misread which path components are resolved.
- **Optional outcome:** say that the SAFE_PATH spelling is kept verbatim, and add one bullet for the lookup arms.
- **Verification:** the docs gates stay green.

## Lens results (clean lenses, with artifacts)

```text
[R266] PASS Conformance - scripts/act_ci.py:701-711, :3993, :4246-4260; receipts/host-lookup-probe.log; receipts/systemd-run-name-probe.log; receipts/host-passt-probe.log - decision items 1-2 against issue 532 comment 5845269093
[R266] PASS RTL - receipts/diff.patch (no hdl/, workflow or submodule path); scripts/act_ci.py:701-711 and its 17 caller names - interface contract of require_tool and slot acquisition order
[R266] PASS Robustness - scripts/act_ci.py:703-711, :11428-11480; receipts/mutation-results.json M04-M08, M12 - impostor, fallback, bare-name, relative, missing, dangling and non-executable paths
[R266] PASS Tests - scripts/act_ci.py:11428-11480, :12480; receipts/gates/act-ci-selftest-*.log (432 ok, 0 FAIL); receipts/mutation-results.json - 10 of 10 predicted kills; S1 recorded as SUGGESTION
[R266] PASS Docs - docs/testing/CI_WORKFLOWS.md:1855-1857, :2077-2112; receipts/gates/{docs-check*,doc-style*,em-dash,toc-*,ci-events-*}.log - text against code and host probes; S2 recorded as SUGGESTION
```

### Conformance

Against the decision (issue 532 comment 5845269093):

1. **The uplink keeps the SAFE_PATH spelling.** `scripts/act_ci.py:709-710` returns `Path(found).absolute()` for `pasta`, where `found` came from the SAFE_PATH-only lookup at `:705`.
   - Every SAFE_PATH entry is absolute, so `absolute()` is a no-op that never consults the working directory.
   - The uplink argv takes that value at `scripts/act_ci.py:3993`, right after `--` in the `systemd-run` command.
2. **Every other tool keeps its resolution.** `scripts/act_ci.py:711` is unchanged.
   - `receipts/host-lookup-probe.log` applies the old rule and the new function to every name in a `require_tool("…")` call plus `SLOT_HOST_TOOLS`. That is 17 names.
   - Only `pasta` differs.
3. **SAFE_PATH provenance is kept.** The lookup at `:705` is unchanged.
   - A name without a slash is never looked up on the working directory on POSIX.
   - Mutant M04 (ambient PATH) and M05 (PATH fallback) are both killed.
4. **Identity checks.** The decision allows, and does not require, identity checks to record the resolved target.
   - The runner records no identity for `pasta`, before or after this change.
   - The offline arm at `:11451-11454` binds the selected path to the fixture's executable target.
5. **The live failure mode is reproduced and cleared on the real binary** (`receipts/host-passt-probe.log`, passt `2026_07_28.f8df3f1`, sha256 `dd97f59e…`):
   - `/usr/bin/passt --netns-only --version` exits 1 with `--netns-only is for pasta mode only`.
   - `/usr/sbin/pasta --netns-only --version` prints `pasta …`, and so does `exec -a /usr/bin/pasta /usr/bin/passt …`. So the mode comes from argv[0].
   - Through `systemd-run --user --wait --pipe` (systemd 262), both a scratch symlink named `pasta` pointing at `/usr/bin/passt` and `/usr/sbin/pasta` ran in pasta mode, and `/usr/bin/passt` refused. The launcher therefore does not canonicalise the executable path before exec (`receipts/systemd-run-name-probe.log`). All three transient user units were collected (`inactive`).
6. **Partial status.** The PR body says `Relates to #532` and states that the issue stays open. That matches the decision.

### RTL (architecture and interface contracts)

- The diff touches no HDL. Clock, reset, CDC, FSM and width checks have no subject (`receipts/diff.patch`).
- The lens was applied to the contracts the diff does touch:
  - The `require_tool` return contract is still "an absolute executable path found on SAFE_PATH". Only the final-symlink resolution is dropped, and only for `pasta`.
  - The acquisition order is unchanged. `scripts/act_ci.py:4246-4247` still looks up every slot tool, `pasta` included, before `validate_slot_root`, the lock and any mutation.
  - `slot_uplink_command` (`:3979-4011`) changes no word except the executable spelling.
  - The fake-host pins (`fake_host_tool` at `:10814`, `slot_uplink_command_pinned` at `:11157`) are unaffected.

### Robustness

Each path below was checked against a killed mutant (`receipts/mutation-results.json`):

- **Ambient PATH impostor:** M04 is killed by six arms.
- **SAFE_PATH miss that falls back to PATH:** M05 is killed by three arms.
- **Bare name, which would let the launcher search its own PATH:** M06 is killed. The uplink run would have executed the untrusted impostor.
- **cwd-relative spelling:** M12 is killed.
- **Dropped executable-bit requirement:** M07 is killed.
- **A dangling or any directory entry accepted:** M08 is killed.
- **Symlink re-read at exec (time of check against time of use).** The final symlink is now read again at exec. That is no regression:
  - Redirecting the symlink needs write access to a root-owned SAFE_PATH directory, which also permits replacing the resolved target.
  - The old rule checked no ownership either. `require_tool` has none, before or after.

### Tests

- **The new arms run and pass.** `selftest_host_tool_paths` (`scripts/act_ci.py:11428-11480`) is wired at `:12480` inside `selftest_slot_stages`. Its seven arms run and pass, at lines 181-187 of `receipts/gates/act-ci-selftest-isolated.log`.
- **Full self-test:** 432 `ok`, 0 FAIL. The two invocation forms produce byte-identical output: `python3 -I scripts/act_ci.py --selftest`, and the docs workflow's runner-contract form without `-I`.
- **The fixture tests the right thing.**
  - It builds a real symlink `pasta` pointing at a `passt` script that prints `${0##*/}`.
  - It runs the argv tail of `slot_uplink_command` with `cwd` and `PATH` set to an untrusted directory that holds an impostor `pasta`.
  - It then requires the output `pasta`.
  - The host probe above shows the real binary depends on exactly that name.
- **Reviewer mutants.** 12 were run. All 10 predicted kills were killed:
  - M01 (the "resolve again" mutant the decision requires) fails on the invoked-name arm and the provenance arm. That matches the author's published `full-mutant-result.json`.
  - M02, re-resolving at the launch site, is killed.
  - M03, preserving every tool's symlink, is killed.
  - M04 to M08, M11 and M12 are killed.
- **Expected survivors.** The control M09 (resolve the directory, keep the final name) survives as designed. M10 survives; see S1.
- **Other suites.**
  - `bash scripts/act_slot_proof.sh --selftest`: PASS, 44 cases. This file is unchanged and does not exercise `require_tool`.
  - `scripts/ci_events.py --check` and `--selftest`: OK, with 1655 contract items and 2197 arms.

### Docs

- **The new text matches the code and the probes.** `docs/testing/CI_WORKFLOWS.md:1855-1857` says the uplink uses the absolute SAFE_PATH `pasta` path, that its final symlink stays unresolved, and that other host tools keep their resolved paths.
- **Nothing obsolete was restored.** The rest of the slot section (`:1790-1862`) is still accurate.
- **Every docs gate passed.** Markdown gates ran in a scratch venv with the pinned `tools/markdown/requirements.txt`:
  - `docs_check.py` passed both with git and in a git-free export: 0 findings across 166 Markdown and 884 scrubbed files.
  - `check_doc_style.py` passed.
  - `gen_toc.py --check` and `--verify-anchors` passed.
  - `check_em_dash.py --base 7eb3b0d4…` found 0 across 4 added lines, with 339/339 arms.
  - `check_doc_paths.py` passed.
  - `ci_events.py --check` passed.
- **Two points are optional.** See S2.

## Commands run (all foreground; exit codes in `receipts/gates/gates-summary.txt`)

- **`run_gates.sh <clone> receipts/gates <base>`:** 18 of its 21 commands exited 0.
  - All of these passed: the `act_ci` self-test in both forms, `act_slot_proof --selftest`, `ci_events --check` and `--selftest`, `check_baremetal_only --check` and `--selftest`, the Python and shell idiom checks, the naming, fail-fast, test-evidence and hygiene ratchets, `check_todo_ownership`, `docs_check`, `check_doc_style`, `check_doc_paths`, and `git diff --check`.
  - Three exited 2 because the host has no pinned Markdown renderer: `gen_toc --check`, `gen_toc --verify-anchors` and `check_em_dash`. Their logs are overwritten by the pinned-venv reruns, which all exited 0, so the first rc=2 lines in `gates-summary.txt` have no separate log.
- **`host_lookup_probe.py`:** only `pasta` changed (rc 0).
- **`mutation_probe.py`:** every mutant matched its prediction (rc 0). It ran against a git-archive copy in scratch and restored that copy's bytes, checked by sha256.
- **Host binary probes:** `receipts/host-passt-probe.log` and `receipts/systemd-run-name-probe.log`. These ran only `--version`, and `--netns-only --version`, which exits at parse time. No namespace, socket, privilege or Docker was used.
- **Hosted check-run snapshot:** `receipts/hosted-check-runs.tsv`, read-only.
- **Clone integrity after probes:** `receipts/clone-integrity.log`.
  - `HEAD` and the tree are exact, with a clean status.
  - The worktree and the index both equal `HEAD`. Every index mode and blob equals the `HEAD` tree.
  - The four gitlinks match their `HEAD` entries: `external` `efeb541a…` (not initialised), `gptp-processor` `5dce647a…`, `protocol-processor` `990f9652…`, `third_party/verilog-axis` `48ff7a7e…`.

## Completion ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `scripts/act_ci.py:701-711`, `:3993`, `:4246-4260`; issue 532 decision; `receipts/host-lookup-probe.log`, `host-passt-probe.log`, `systemd-run-name-probe.log` | R266-6 | `ad4a5ff6ba15502ed60d58b3ca91830b50fa9e1c` |
| RTL | CLEAN | `receipts/diff.patch` (no HDL/workflow/submodule path); `require_tool` contract and callers; `slot_uplink_command` `:3979-4011`; fake-host pins `:10814`, `:11157` | R266-6 | `ad4a5ff6ba15502ed60d58b3ca91830b50fa9e1c` |
| Robustness | CLEAN | `scripts/act_ci.py:703-711`, `:11428-11480`; `receipts/mutation-results.json` (M04-M08, M12) | R266-6 | `ad4a5ff6ba15502ed60d58b3ca91830b50fa9e1c` |
| Tests | CLEAN (S1 is a SUGGESTION) | `scripts/act_ci.py:11428-11480`, `:12480`; `receipts/gates/act-ci-selftest-*.log`, `slot-proof-selftest.log`, `ci-events-*.log`; `receipts/mutation-results.json` | R266-6 | `ad4a5ff6ba15502ed60d58b3ca91830b50fa9e1c` |
| Docs | CLEAN (S2 is a SUGGESTION) | `docs/testing/CI_WORKFLOWS.md:1790-1862`, `:2077-2112`; `receipts/gates/docs-check*.log`, `doc-style*.log`, `em-dash.log`, `toc-*.log`, `doc-paths.log` | R266-6 | `ad4a5ff6ba15502ed60d58b3ca91830b50fa9e1c` |

## Real limits

- **No live slot proof, no privileged run and no Docker.**
  - The candidate runner was run only as its offline `--selftest`, which never reached a daemon: this user is not in the docker group.
  - The candidate runner was never run with `--pr`, `--sudo` or a live self-test, and never on the host as orchestrator.
  - Physical calibration was NOT RUN. Field skips are not hardware proof.
- **The `systemd-run` probe used the user service manager, not the system manager under `sudo -n` with `Type=forking` and `PIDFile`.**
  - It shows that the launcher and the exec path keep the invoked name on systemd 262.
  - It does not prove that the slot uplink starts. That is decision item 3.
- **Hosted evidence was a snapshot at about 10:34Z.**
  - Completed with success: `docs-check`, `docs-check-no-git`, `rtl-fast`, `elaborate`, `wire-accountability`, `full-ci-gate`, `yosys-elaboration`, Yosys shards 0-3, and Verilator shards 0 and 3.
  - Still in progress: Verilator shards 1, 2 and 4.
  - Skipped: `Physical gPTP`.
  - This was inspected only. The manager owns hosted and act acceptance.
- **The scoped Verilator path named in the brief does not exist on this host.** It was not needed, because the diff has no RTL.
- **The Markdown gates ran in a scratch venv.** It was installed from the repository's hash-pinned requirements, because the host lacks the renderer.

## Pending manager duties

- **Build and validate the current-dev merge candidate.** Source base and live dev were both `7eb3b0d4…` at review time.
- **Collect the exact-head hosted `verilator-suites` and `yosys-portability` evidence.**
- **Get the second independent positive review.**
- **After merge:**
  - Audit and install the merged runner. The new `scripts/act_ci.py` sha256 is `79579e6b618f1d05fae202018e18f066a23cd8d667202fdbe03b561ecad638f8`; the previous audited install was `f27af88b…`.
  - Rerun `scripts/act_slot_proof.sh` from the trusted checkout (decision item 3).
  - Keep #532 open until the proof prints `PROVED`.
- **Post-merge containment.**

R266-6 FINISHED
