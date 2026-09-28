[R374] POSITIVE - exact head 0404675dcd8788d29cb15a831a8c182438bf1c92

# R374-3: internal independent review of processor PR #130 (issue #127), round 3

- **Repository:** Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #130 for issue #127.
- **Exact head:** `0404675dcd8788d29cb15a831a8c182438bf1c92`, tree `87b2925d9609f9e298ae9a0781dcdd127dcbb1ac`. The PR API reports the same head.
- **Delta reviewed:** `00b5c6c9..0404675d`. This is one commit (executor [A404]) whose parent is `00b5c6c96af5ebcaa92ddb3bdaeb4aa5302ef27c`. It changes four files:
  - `.gitattributes` (added);
  - `.github/workflows/hdl.yml`;
  - `tb/srp_top/Makefile`;
  - `tb/srp_top/README.md`.
- **Full base:** `16be6768f710e79450aace277abacd6c2c3336e5`.
- **Round:** R374-3. I worked in a cleared context from my own detached clone.
- **Reconstructed from:**
  - The repository has no AGENTS.md or CONTRIBUTING.md. I used `README.md`, `docs/README.md` and the `tb/srp_top/README.md` campaign section instead.
  - Issue #127 body and the assignments 5860872275 (round 1) and 5862744241 (round 3, "Round 3 assignment for PR #130").
  - Manager comments 5862222946 (donor bank 8/9 at `00b5c6c9`) and 5863087123 (review start).
  - The full diff `16be6768..0404675d` and its history.
  - My read-only round-2 packet.
  - The manager's donor and parent receipts at this head.
- **Independence:** I read the prior public findings (R374-2, R375-2) only after my own pass over the diff. I did not read any round-3 review by another reviewer, any private author material, or any lane scratchpad.

## Verdict

**POSITIVE.** No MINOR, MAJOR or BLOCKER finding is open. All five lenses are CLEAN. There is one optional SUGGESTION (S1, CI cost and placement).

- **(1) Whitespace gate.**
  - `git diff --check 16be6768 0404675d` exits 0.
  - At the round-2 head without the new attribute file, it still exits 2, with 26 trailing-whitespace and 5 blank-at-EOF hits across 23 files.
  - The `.gitattributes` rule matches exactly the 56 `tb/srp_top/mutations/*.patch` files. It turns off only `blank-at-eol` and `blank-at-eof`.
  - `git apply --check` accepts all 56 patches, and all 56 also apply and reverse cleanly.
  - I reran the committed campaign: 7/7 controls pass, 56/56 arms are KILLED, and families K1–O8 are covered 49/49.
  - The manager's donor bank is 9/9 at this head. Step 9 is `git diff --check`, rc 0.
- **(2) Makefile target.**
  - `make -C tb/srp_top mutants` runs `python3 mutants.py --output "$(MUTANT_OUTPUT)"`. This is the complete, unfiltered campaign.
  - Plain `make` still resolves to `run`, the positive suite. It passes 1987/1987 and never invokes the driver.
  - `scripts/run_suites.sh` calls only the default goal.
  - The README text matches this behaviour.
- **(3) Hosted CI step.**
  - The step is correct:
    - PATH uses the pinned build.
    - The output goes to `/tmp` on the runner, and the logs go to the job output.
    - A nonzero driver result fails the step, which I proved with three failure probes.
  - It is also what makes the parent count this campaign. An ablation shows 20 of 95 armed suites at head, and 19 of 95 when either the CI step or the Makefile target is removed.
  - I therefore judge it in scope and proportionate. Its runtime cost is S1.
- **(4) Nothing else changed.** The `hdl/` delta is empty, and no other test or source file changed.

## Findings

### S1 - SUGGESTION - Robustness, Tests - the campaign runs serially inside the `suites` job, ahead of two other gates

- **Where:** `.github/workflows/hdl.yml:55-58`.
- **Evidence:**
  - At this head, the `suites` jobs of both hosted runs (push 36375812095 and pull_request 36375813740) started the new step at 04:10:42Z and 04:11:33Z. When this report was written, the step was still running after more than 20 minutes (`receipts/head-ci-status.txt`). The preceding "Lint + every suite" step took about 12 minutes.
  - Locally, the same arms took 1911 s of summed chunk wall time (`receipts/campaign/k*/driver.log`).
  - The step is placed before "Traceability matrix no-drift" and "nvm_port README figures". A campaign failure therefore skips both of those gates in that run.
  - The receipt directory is not uploaded. Only the driver's stdout, which includes the tail of any failing log, survives.
- **Impact:** CI wall time and runner time rise on every push and on every pull_request event, and a campaign failure hides the results of two unrelated gates. Correctness is unaffected.
- **Suggested outcome (optional):**
  - Run the campaign as its own job, parallel to `suites` and reusing the Verilator cache. Keep the literal `make -C tb/srp_top mutants` invocation in `hdl.yml`, because the parent inventory keys on it.
  - Optionally, upload `MUTANT_OUTPUT` as an artifact on failure.
- **Verification:** hosted run time per event, and the parent inventory still reporting `protocol-processor/tb/srp_top: mutants`.

## Resolution of prior findings at this head

| Prior finding | Status at `0404675d` | Evidence |
|---|---|---|
| R374-2 N1 (MINOR): patch files fail `git diff --check` | **RESOLVED** | `receipts/whitespace-gates.log`: rc 0 for both `16be6768..0404675d` and `00b5c6c9..0404675d`. `receipts/whitespace-scope-probes.log`: the round-2 head, checked out without the attribute file, is rc 2 with 26 + 5 hits across 23 files, so the exemption is what fixes it. Patch bytes are unchanged since `00b5c6c9` (`git diff --quiet` rc 0). Every patch passes `git apply --check`, 56/56 (`receipts/apply-check.log`). The campaign is 56/56 KILLED (`receipts/campaign-summary.txt`). Manager donor bank 9/9 (`receipts/manager-donor-full-results.json`). |
| R375-2 R2-F1 (MINOR): same defect | **RESOLVED** | Same evidence as N1. |
| R374-2 S1 (SUGGESTION): campaign not visible to the parent inventory | **RESOLVED** | `tb/srp_top/Makefile:28-29` together with `hdl.yml:58`. The parent `measure_test_evidence.py --check` (parent `c0723222` with the gitlink at head) reports "20 of 95" and lists `protocol-processor/tb/srp_top: mutants driver mutants.py`. The ratchet reads 75 ≤ 77, and "can be lowered to 75" (`receipts/inventory/inventory-head.log`). This matches the manager's parent step 10. |
| R374-1 F1–F5 and R375-1 F1–F4 (resolved at round 2) | **REMAIN RESOLVED** | This delta changes no RTL, testbench source, driver or patch (`receipts/clone-integrity.txt`, "delta files"). The mutant-based resolutions (O1–O8 guards, coalescing, the MVRP/prepare arbitration, the restored expiry pulse) were re-killed in my rerun. The manager's parent consumer gates are 11/11 at this head. |

## Lens evidence

### Conformance: CLEAN

- The round-3 scope is non-functional: the whitespace policy, a Makefile target and a README update. The CI step was not requested, but it serves the taken suggestion. It changes no behaviour and makes no decision on issue #127.
- The issue decisions are untouched: LV + rLv semantics, #108 kept separate, and periodic-declaration and six-cycle behaviour. Both `hdl/` and all testbench sources are byte-identical to `00b5c6c9`.
- The assignment's proof bar still holds at this head:
  - Restoring the timer-expiry pulse fails (`r-expiry-pulse-restored` and `my-expiry-pulse` are KILLED on K2, K4, K5, K11 and K12, with 62 failures each).
  - Every new check family is pinned by a killed arm (49/49).

### RTL: CLEAN

- `git diff --name-only 00b5c6c9 0404675d -- hdl` is empty.
- In the clone, every tracked file's `git hash-object` equals its index blob, and every mode matches (`receipts/clone-integrity.txt`; rechecked after all probes in `receipts/clone-integrity-final.txt`: clean status, no ignored leftovers, index = HEAD).
- The lint and RTL gates are covered by the manager's donor bank at this head: lint, all suites, `make check`, Yosys portability, 9/9.

### Robustness: CLEAN (S1 is optional)

- **Attribute scope** (`receipts/whitespace-scope-probes.log`, scratch clone, reset after each probe). Each of these still fails with rc 2:
  - trailing whitespace in `tb/srp_top/README.md`;
  - a `.patch` file in a nested `mutations/sub/` directory;
  - a non-`.patch` file in `mutations/`;
  - a `.patch` elsewhere in `tb/srp_top/`;
  - space-before-tab inside a mutation patch (probe D2), which proves that other whitespace classes remain enforced there.

  A trailing blank line and a blank line at EOF in a mutation patch are exempt, which is intended.
- **Invalid probe, disclosed.** My first space-before-tab probe (D) appended `+ \tfoo`, which has no leading whitespace indent, and was invalid. D2 replaces it.
- **Failure propagation** (`receipts/propagation/summary.txt`). The `hdl.yml` step body ran under `bash -e` on disposable copies of the head whose arm table was trimmed to one arm. All three cases give `make ... Error 1` and a step rc of 2:
  - cover-gap: the arm is KILLED, but coverage is 1/49;
  - no-apply: the patch context has drifted, and `git apply --check` raises `CalledProcessError`;
  - survivor: the patch edits only a comment, the arm is UNPROVEN, and the checks read 1 PASS, 2 FAIL.
- **PATH.** The step prepends `$HOME/verilator/bin`, the cached 5.050 install, exactly like the lint/suites step. The driver's child `make -C tb/<suite>` then resolves `verilator` from that PATH.
- **Output.**
  - `MUTANT_OUTPUT ?= /tmp/srp-leaveall-mutants` can be overridden from the command line or the environment, and paths with spaces are quoted (`receipts/make-target-checks.log`).
  - The driver builds in a unique `tempfile` tree, so the source tree is never written.
  - A job timeout is not set, so the 360-minute default applies.

### Tests: CLEAN

- **Committed campaign rerun at head** (`receipts/campaign/`, `receipts/campaign-summary.txt`):
  - I ran the committed driver as 12 `--only` partitions, 4 at a time with 2 compile jobs each, using the pinned simulator.
  - 7/7 distinct controls pass. Control logs include srp_encoder 562/562, stream FSMs 1215/1215 and the srp_top groups.
  - 56/56 arms are KILLED on their required named assertions. The driver checks this, and my aggregation also confirms that no arm is missing or unproven.
  - Families K1–O8 are covered 49/49, which is equivalent to the driver's `64 checks: 64 PASS`.
  - The per-arm failure counts and tags match the README tables.
- **Positive suite.** Plain `make -C tb/srp_top` on a scratch copy gives `1987 checks: 1987 PASS, 0 FAIL`, rc 0 (`receipts/plain-make-srp_top.log`). No driver line appears in the log.
- **Hosted run.** The hosted `suites` jobs at this head passed "Lint + every suite" and were running the campaign step when I checked. The docs-gates and portability jobs completed with success (`receipts/head-check-runs.json`, `receipts/head-ci-status.txt`).

### Docs: CLEAN

`tb/srp_top/README.md:209-218` says the following, and each point holds:

- The `make ... mutants MUTANT_OUTPUT=` form is shown.
- "Runs the complete campaign" is true: there is no `--only`.
- "Invoked by the HDL workflow" is true: `hdl.yml:58`.
- The default path is the one shown.
- "Plain `make` still runs the positive suite" is true: the default goal is `run`.
- The `.gitattributes` statement names exactly the two exempted classes and only these files.

The `.gitattributes` comment correctly states the cause. No other document enumerates the `hdl.yml` steps (checked with grep), so no other file is stale.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #127 body and decisions; round-1 and round-3 assignments; empty `hdl` and testbench-source delta; expiry-pulse restoration arms KILLED; 49/49 families | R374-3 | 0404675dcd8788d29cb15a831a8c182438bf1c92 |
| RTL | CLEAN | `git diff 00b5c6c9 0404675d -- hdl` empty; blob, mode and index integrity; manager donor bank 9/9 (lint, suites, Yosys) | R374-3 | 0404675dcd8788d29cb15a831a8c182438bf1c92 |
| Robustness | CLEAN (S1 optional) | `.gitattributes` scope probes; `hdl.yml:55-58` PATH, output and ordering; 3 failure-propagation probes under `bash -e`; `MUTANT_OUTPUT` override and quoting | R374-3 | 0404675dcd8788d29cb15a831a8c182438bf1c92 |
| Tests | CLEAN | `git diff --check` (head and round-2 head); 56/56 `git apply --check`; committed campaign 7/7 controls, 56/56 KILLED, 49/49; plain make 1987/1987; parent inventory ablation (20/19/19/19); hosted check runs | R374-3 | 0404675dcd8788d29cb15a831a8c182438bf1c92 |
| Docs | CLEAN | `tb/srp_top/README.md:209-218`; `.gitattributes` comment; `Makefile` header; repository-wide grep for workflow-step listings | R374-3 | 0404675dcd8788d29cb15a831a8c182438bf1c92 |

## Real limits

- **Simulator path.** The assigned `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. I used the manager's per-head wrapper `$VALIDATION_STORAGE/pp127-manager-0404675d/pinned-tool-bin/verilator`. Its sha256 `905795b9…` is byte-identical to every other per-head pinned wrapper on the host, and it reports `Verilator 5.050 2026-07-01 rev v5.050` (`receipts/tool-identity*.txt`). The host PATH `verilator` is 5.052 and was not used. My shim `scripts/verilator` only rewrites `-j 0` to cap compile jobs.
- **Campaign partitioning.** A single foreground command is bounded at 10 minutes, so I did not run the complete `make mutants` end to end locally. I ran the identical committed driver in 12 `--only` partitions and reproduced the coverage tally in `scripts/aggregate.py`. The Makefile recipe was verified with `make -n`, and its end-to-end failure behaviour with the propagation probes. The hosted runs are executing the complete target, and their result was pending when I wrote this.
- **Hosted CI.** The `suites` job at this head had not completed when I wrote this; its "Lint + every suite" step had passed. Only docs-gates and portability are complete (success). Hosted acceptance is owned by the manager.
- **Parent.** I ran only the single parent checker `measure_test_evidence.py --check` on a scratch parent at `c0723222` with gPTP at `5dce647a`. I did not run the full parent bank; the manager's 11/11 run covers that.
- **Receipt redaction.** Local simulator-root and home paths in published receipts are replaced by `<SIMROOT>` and `<HOME>`. The original hashes of the copied manager receipts are in `receipts/manager-originals-sha256.txt`.
- **Hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof. This review makes no hardware claim.

## Pending manager duties

- Confirm that both hosted `suites` jobs at `0404675d` complete with success, including the new "SRP LeaveAll mutation campaign" step and the two gates after it. Record that step's runtime.
- Build the final current-dev candidate at the merge turn (source base `16be6768`). Live parent dev has moved past `c0723222`.
- Parent-side, at pin adoption: the inventory reports that "the mutation ratchet can be lowered to 75". Also land the CRF integration regression the issue requires (frames and STREAM_STOP).
- Merge requires two independent positive reviews and the full completion bar.

## Reproduction

All scripts are in `scripts/`. They are portable, and paths are passed as arguments or taken from `REAL_VERILATOR`.

- `run_chunk.sh <tree> <out> <jobs> <arms|ALL>`: the committed driver or the `mutants` target, with the pinned simulator first on PATH.
- `aggregate.py <tree> <campaign-dir>`: controls, arms and 49-family coverage.
- `apply_check.sh`, `propagation_probe.sh`, `inventory_probe.sh`: as described above.

R374-3 FINISHED
