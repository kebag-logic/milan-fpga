[R566] NEGATIVE - exact head 759d1d248fad095ab07bfcc480a0828117501f39

# R566-1: internal independent review of PR #699 (Closes #641, #651)

- **Head:** `759d1d248fad095ab07bfcc480a0828117501f39`, tree `f43a876d37d15c921a5457698d1101b93274430f`. Three commits on dev `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.
- **Reconstructed from:**
  - AGENTS.md, CONTRIBUTING.md and REQUIREMENTS.md (REQ-VER-02, REQ-VER-04).
  - The #641 and #651 bodies, assignment comment 6081334020, TAKEN, and REVIEW READY 6083295073.
  - The PR body, the diff and its history.
  - The public evidence tree `review-evidence/641-r1` at `2f7a3d63`.
- All five lenses were applied independently at this head.
- **Prior public review findings on this PR:** none. The PR has no reviews and no review comments. Its only comments are the two review-start notices, and neither issue carries a reviewer finding. Nothing needs to be resolved or retained.

**Verdict basis.** Every acceptance item of #641 and #651 is met, and each was reproduced across both make versions, both sv2v versions and both flows. One MINOR Docs finding (F1) is open, so the verdict is NEGATIVE. Docs is unclean; Conformance, RTL, Robustness and Tests are clean.

## Findings

### F1 - MINOR - Docs - authoritative prose still says the Yosys flows do not enforce elaboration guards

- **Where:**
  - `docs/development/CODE_QUALITY.md:1258-1271`.
  - `docs/findings/README.md:26`: the Current entries row for #649 says "Yosys does not enforce the RTL's elaboration guards."
  - `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:25`: the summary bullet is still present tense. The PR qualified only the method note at :101-103.
  - The same claim is in the source comment `hdl/ieee8021q/filtering/rx_mac_filter.sv:144-150`.
- **Authority and evidence:**
  - CODE_QUALITY.md says: "It is **not** enforced on the sv2v → Yosys path that `syn/yosys/run.sh` and `syn/yosys/ooc.sh` use ... `OOC_CHPARAM="TDATA_WIDTH=52" syn/yosys/ooc.sh rx_mac_filter` synthesises the illegal shape and reports PASS ... That check is not in this change".
  - At this head that command returns rc 1 under both converters:
    - `receipts/sweep/head-sv2v13.results.json` fails with `Can't resolve task name '$error'`.
    - `receipts/sweep/head-sv2v12.results.json` fails with the guard's own message, `TDATA_WIDTH=%0d is not a whole number of bytes`.
    - The legal `TDATA_WIDTH=64` control returns rc 0 in both.
  - The base flow with sv2v 0.0.13 returns rc 0 (`receipts/sweep/base-sv2v13-elab.results.json`). This PR is the change that made the paragraph false.
  - AGENTS.md §5 tells the executor to "update authoritative documentation when behavior or architecture changes". The Docs lens requires that changed contracts appear in the authoritative docs.
- **Impact:**
  - The development guide tells readers that a Yosys PASS is not evidence for this contract.
  - It gives a runnable command whose stated verdict is now the opposite of what the command returns.
  - The findings index presents "Yosys does not enforce" as a current finding.
  - This is a claim about a gate's verdict, not pure wording.
- **Required outcome:**
  - The CODE_QUALITY.md paragraph and the findings index row state current behavior, namely:
    - Both flows refuse an active guard.
    - Under sv2v 0.0.12 (the CI pin) the native `$error` is honoured.
    - The converted 0.0.13 form is honoured through `enforce_elaboration.py` (#651).
    - The `TDATA_WIDTH=52` example now fails.
  - The #649 summary bullet carries the same qualification as its method note.
  - The `rx_mac_filter.sv` comment is corrected in a comment-only edit, if the maintainer allows that under this lane's no-RTL-change scope. Otherwise it goes in a public follow-up issue.
- **Verification:**
  - Re-read the named lines at the new head.
  - The documentation gates stay green: `check_em_dash.py --base`, `check_doc_style.py`, `gen_toc.py --check` and `docs_check.py`.
  - The quoted command still returns non-zero under both converters (`scripts/sweep_replay.py --points rx-tdata-52`).

### R1 - RESIDUE - Docs - "fatal tasks" names the wrong task

- **Where:**
  - `syn/yosys/README.md:44`: "restores converted error/fatal displays to fatal tasks".
  - `syn/yosys/enforce_elaboration.py:4`: "Restore fatal elaboration tasks".
- **Problem:** the helper rewrites both forms to `$error` (`enforce_elaboration.py:14,19`).
- **Exact fix:**
  - README: "restores converted error/fatal displays to `$error` tasks, which Yosys refuses when their generate branch is active".
  - Docstring: "Restore converted elaboration errors as `$error` tasks".
- Wording only; it changes no verdict.

### S1 - SUGGESTION - Tests - the enforcement path is never exercised in CI

- `syn/yosys/guard_selftest.py` runs in no workflow. Its siblings `ooc_selftest.py` and `cache_selftest.py` run in `rtl-fast.yml:223,230`.
- CI pins sv2v 0.0.12, which emits native `$error` (`receipts/sv2v-lowering/`). So `enforce_elaboration.py` is a byte no-op in every hosted worker.
- The hosted portability evidence at this head is 58 of 58 result-cache hits (`receipts/hosted-yosys-shards-summary.txt`).
- The committed self-test feeds hand-written fixture text, not real converter output.
- A regression in the helper, or a change in the converter's format, would therefore surface only when CI moves to 0.0.13.
- **Suggested change:**
  - Add the self-test to `rtl-fast` beside its siblings, with matching `ci_events.py` coverage.
  - Optionally add an arm that converts a planted guard with whatever sv2v is installed.
- Acceptance #651.2/3 does not require this. Under the CI pin the guards were already refused natively: a base-flow replay with 0.0.12 refuses all three sweep points (`receipts/sweep/base-sv2v12.results.json`).

### S2 - SUGGESTION - Robustness - refusal depends on Yosys rejecting a procedural `$error`

- The restored `initial $error(...)` fails in Yosys 0.66 as `Can't resolve task name '$error'`, on every head-sv2v13 row.
- So the refusal reason drops the guard's own message.
- It also relies on an unsupported-construct error, not on Yosys support for elaboration tasks.
- Separately, sv2v 0.0.13 lowers a procedural `initial ... $error` to `"Error [%0t]"`, which the regex does not match (`receipts/sv2v-lowering/sv2v-0.0.13.v`, block g6).
  - No such guard is in the RTL today.
  - The procedural `$fatal` at `KL_pp_acmp_listener.sv:344` is still refused through `$finish`.
- **Suggested change:**
  - Restore the module-scope task by dropping the `initial`, so Yosys prints the guard text as it does with native lowering.
  - State the Yosys-version dependence in the README.
  - The pinned self-test catches a behavior change on a Yosys bump only if S1 is adopted.

### S3 - SUGGESTION - Robustness/Tests - pp_shadow's nested derivation still discards its exit status

- `tb/verilator/pp_shadow/Makefile:107` has no `.SHELLSTATUS` check, unlike `milan_dp_render` and `milan_dp_mclk`.
- The arm-I probe shows that removing its new `MAKEFLAGS=` guard is detected by no gate under either make (`receipts/raw/arm-i-make441.jsonl` and `arm-i-make43.jsonl`, variant `shadow-unguarded`).
- This is pre-existing and outside #641's acceptance. Suggest a follow-up issue.

## Acceptance, reproduced

| Item | Result | Reviewer evidence |
| --- | --- | --- |
| #641.1: a stopped parse is unreadable and fails the gate; planted `$(error)` under make 4.3 and 4.4.1 | Met | Self-test rc 0, 226 checks, under GNU Make 4.4.1 and under an isolated 4.3 built from `make-4.3.tar.gz` (sha256 `e05fdde4...`, equal to the author's digest): `raw/shape-selftest-make441.*`, `raw/shape-selftest-make43.*`. Mutations are killed. Restoring the base inventory fails "a stopped make parse leaves a partial database" under both makes (`raw/mut-M1-*`). Keeping the probe goal but dropping only the exit-status check also fails (`raw/mut-M2-*`). |
| #641.2: both consumers guarded with `MAKEFLAGS=`; the gate reads both under 4.3 and 4.4.1 | Met | Both Makefiles match `milan_dp_mclk`'s form. At head, the arm-I probe reports `database_ok=true` with one frozen shape prerequisite per consumer under both makes. Under 4.4.1, unguarded `milan_dp_render` with the base inventory reproduces the original fail-open (ok, 0 prerequisites, no finding), and the head inventory refuses it (`raw/arm-i-make441.jsonl`). `tdm8_render_mutants.py` passes `TDMRM_SRC`/`DP_SRC` explicitly, so clearing `MAKEFLAGS` drops no override. No consumer reads `MAKECMDGOALS`. |
| #641.3: fixture sizes derived from the built image | Met | `oracle.json` carries no size fields. `run.oracle_media` derives 3336 B / 54 records (1x1) and 13256 B / 164 records (8x8) from the head generators, matching all three slot digests (`raw/derive-media.jsonl`). The oracle's log and slot digests equal the published measurement receipts. Fixture self-test rc 0, 55 checks (`raw/fw-selftest.*`). A channel-count drift is refused with "oracle image changed" (`raw/mut-X2-*`). A vendor-name change, which does not reach the journal, correctly passes (`raw/mut-X1-*`). |
| #651.1: both flows rc != 0 on any elaboration guard | Met | Under sv2v 0.0.13, the head flows refuse streams-8, streams-8-chans-2 and pp-names-235 in both run.sh and ooc.sh, plus the rx `TDATA_WIDTH=52` override (`sweep/head-sv2v13.*`; run.sh elaborate mode `sweep/head-sv2v13-elab.*`). The base flows return 0 for pp-names-235 and the rx override (`sweep/base-sv2v13-elab.*`). Under sv2v 0.0.12, head and base both refuse natively (`sweep/head-sv2v12.*`, `sweep/base-sv2v12.*`). |
| #651.2: a self-test plants a refused configuration and shows each flow failing | Met | `guard_selftest.py` rc 0, 36 controls (`raw/guard-selftest.*`). It fails when the run.sh enforcement is deleted (`raw/mut-G2-*`), when the ooc.sh enforcement is deleted (`raw/mut-G3-*`), and when the regex is narrowed to Error only (`raw/mut-G4-*`). |
| #651.3: yosys-portability inherits the check | Met; hosted aggregate pending | `rtl.yml:557` calls `syn/yosys/run.sh`, which applies enforcement before the cache key is formed. The 4 hosted Yosys shards at this head passed with sv2v v0.0.12, all 58 tops as result-cache hits. That is consistent, because enforcement is a byte no-op under 0.0.12 (S1). |
| Every shipping configuration still passes | Met, within limits | All 58 run.sh tops pass head `--mode elaborate` under sv2v 0.0.13, with 182 restored guards across 18 tops and no leftover converted display (`shipping-elab/head-sv2v13.results.json`). Under 0.0.12 the input is byte-identical, and the author's 58/58 and 18/18 full-flow receipts and the hosted shards cover that path. |
| No RTL or shipping-image change | Met | The diff touches nothing under `hdl/`, `configs/`, `sw/` or submodule gitlinks. `oracle.json` is a test fixture. |

## Additional checks

- **Docs/script subset at head, all rc 0** (`raw/doc-subset/`):
  - em-dash `--base 5603c353`, doc-style, doc-paths, docs_check.
  - gen_toc `--check` and `--verify-anchors`.
  - py, sh and cpp idiom; hygiene; todo-ownership; test-evidence; naming; fail-fast.
  - ci_events `--check`, pp_srcs `--check`, rtl source lists.
- `git diff --check` is clean.
- Commits are one line with no trailers.
- **Builder arm reported NOT RUN:** `sw/builder/test_builder.py:449-453` needs an archived place report in a home directory (`REAL_RPT`). It is a registered NOT RUN. This PR changes nothing in `sw/builder` or the estimator, so the NOT RUN is acceptable for this change.
- No probe needed Verilator. The pinned wrapper's identity is recorded in `receipts/toolchain.txt`.

## Reviewer ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | #641/#651 acceptance checked against `shape_consumer_inventory.py:191-205`, both Makefiles, `oracle.json`, `run.py:429-465`, `run.sh:549-556`, `ooc.sh:562-566` and `rtl.yml:557`; reproduced per the acceptance table | R566-1 | 759d1d248fad095ab07bfcc480a0828117501f39 |
| RTL | CLEAN | No RTL diff. Interaction with the RTL guards checked: generate-branch legality and parameter-override activation on `KL_nvm_backend`, `rx_mac_filter` and 18 shipping tops (182 restored guards), across sv2v 0.0.12/0.0.13 and Yosys 0.66 (`shipping-elab/`, `sweep/`) | R566-1 | 759d1d248fad095ab07bfcc480a0828117501f39 |
| Robustness | CLEAN | Make exit-status semantics with an empty goal; stops before and after a rule; missing build products; `MAKEFLAGS` override paths; regex forms (Error, Fatal with `$finish`, procedural); cache-key custody; fail-closed helper exit (`arm-i-*`, `mut-*`, `sweep/`). S2 and S3 are suggestions only | R566-1 | 759d1d248fad095ab07bfcc480a0828117501f39 |
| Tests | CLEAN | `entity_shape_selftest.py:401-423`, `guard_selftest.py`, the `run.py` trace controls and `gen_oracle.py`. Each new control is killed when its fix is reverted or narrowed (M1, M2, G2, G3, G4, X2). S1 is a suggestion | R566-1 | 759d1d248fad095ab07bfcc480a0828117501f39 |
| Docs | UNCLEAN (F1) | `syn/yosys/README.md:43-58`, `649_RESOURCE_MAP_AND_SENSITIVITY.md:25,99-103`, `docs/findings/README.md:26`, `docs/development/CODE_QUALITY.md:1258-1271`, `fw_service_budget/README.md:18-19,82-85,198-216`, and `docs/findings/397_SERVICE_BUDGET.md:58` (a dated measurement record, not a finding) | R566-1 | 759d1d248fad095ab07bfcc480a0828117501f39 |

## Real limits

- No full Yosys bank was run. Positive shipping coverage under sv2v 0.0.13 is elaborate mode only; full mapping of the rewritten input was not run.
- **Base false green for the streams-8 pair under 0.0.13 is unconfirmed:**
  - The full-synthesis replay was still mapping the 8-stream datapath when I stopped it after about 6 minutes (`raw/sweep-base-sv2v13-full-aborted.log`).
  - Base elaborate mode aborted inside Yosys with no guard error.
  - pp-names-235 and the rx override do reproduce the false green.
- No fixture re-measurement or simulation build was run. Fixture correctness rests on derivation, digest binding and the author's measurement receipts.
- The local Yosys is a distribution package build, not the hosted binary with bundled ABC.
- No builder or native bank was run. There is no hardware or physical-calibration evidence.
- **Hosted state at review time** (`receipts/hosted-checks-at-review.txt`):
  - Passed: Yosys shards 0-3, Verilator shards 0 and 3, docs-check, elaborate, yosys-elaboration.
  - Pending: Verilator shards 1, 2 and 4, firmware-unit, and the `yosys-portability` aggregate.
  - Physical gPTP is a skipped context.

## Pending manager duties

- Hosted acceptance, including the `yosys-portability` aggregate and the remaining Verilator shards.
- act.
- The candidate builder (48) and native (5) banks on the current-dev merge candidate.
- Re-review after the F1 fix.
- Post-merge containment.
- Carry R1 to the residue checklist.

## Packet

- **`scripts/`:** the portable probes `sweep_replay.py`, `arm_i_probe.py`, `shipping_elaborate.py`, `derive_media.py` and `doc_subset.sh`.
- **`receipts/`:** raw logs, rc files and peak-memory files. Absolute paths are normalized to `$PACKET`, `$CLONE`, `$TOOLS` and `$HOME`.
- **`MANIFEST.sha256`:** lists every published file.
- **Clone state after all probes:** verified identical to its starting state. HEAD, index digest, tree digest and the gitlinks `gptp-processor 5dce647a`, `protocol-processor 2ad2f845` and `third_party/verilog-axis 48ff7a7e` all match, and the worktree is clean (`receipts/baseline-state.txt` equals `receipts/final-state.txt`).

R566-1 FINISHED
