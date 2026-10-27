[R703] POSITIVE - exact head e0e1b4649ea3af908a8f32eccaad7903fa2cc134

# [R703] R703-6: internal cleared-context review of PR #792 (issue #665, lane S2, round 6)

- Exact head: `e0e1b4649ea3af908a8f32eccaad7903fa2cc134`, tree `57bc6a82a6182a5c243b61b44d4a34120bcb59db` (verified in the clone).
- Previously reviewed head: `f58d049beb377c3f535628067022d4d5b51e8208` (R703-5, POSITIVE). Source base `e76a755a` (`dev-soft-core`).
- Scope of this round: the delta `f58d049b..e0e1b464`, one commit, 2 files, +38/-0:
  - `sw/firmware/ctrl/test/ctrl_configs.py:179-200` adds five `OUTSIDE` entries, and `:217-220` adds one `SUITES` entry;
  - `tb/verilator/ctrl_service_budget/README.md:107-118` describes the classification and the rule for new files.
- Authorities: the S2 assignment (issuecomment-6409745905) and its frozen acceptance; the round-6 assignment (issuecomment-6435512208); the author's TAKEN (6438501884) and REVIEW READY (6441276168); the gate's own contract (the `ctrl_configs.py` module docstring, `:3-58`, and the `OUTSIDE`/`SUITES` doc comments, `:152`, `:202-204`); AGENTS.md sections 6 and 7.

## Verdict

**POSITIVE.** The round-6 change does what the assignment asks, and it does not weaken the gate:
- Each of the six harness files the TSN stack boundary gate finds by text is classified under the gate's own taxonomy.
- Each entry's stated reason matches what the file's code does.
- Each entry is load-bearing.
- The hosted `firmware-boundary` step that failed at `f58d049b` now passes at this exact head.
- No image, measurement or figure changes.

No BLOCKER, MAJOR or MINOR is open. There are:
- one new RESIDUE item, plus one carried RESIDUE item that is retained;
- the external reviewer's carried TESTING.md residue, also retained;
- one new SUGGESTION, plus three carried SUGGESTIONs.

The S2 measurement STOP still stands: the rows miss T_svc = 10 ms. The PR correctly keeps "Relates to #665". That STOP is the lane's frozen, published outcome, not a defect of this round.

## What I verified (own pass over the delta, before reading any prior finding)

| Claim | Evidence at this head | Receipt |
|---|---|---|
| The gate finds exactly these six harness files by text | Among the harness's 11 `*.py` files, exactly `build.py`, `fixture_variant.py`, `runtime_ssp.py`, `selftest.py` (programs) and `scenario.py`, `split_soc.py` (no `__main__`) contain `sw/firmware/ctrl` or `ctrl_build` (the gate's `BUILDER_NAMES`, `ctrl_configs.py:82`). The harness has no Makefile | `receipts/probe_held.log` |
| `build.py` in `OUTSIDE` is truthful: its own compiles are none of the firmware's, and its image compiles are ones the gate already captures | `build.py:137-145` runs `ctrl_srp_image.py --config configs/<shape>.yaml --interfaces n --with-aecp --layout split`. The points are `run.py:29`: 1x1/1 and 8x8/2. `ctrl_runs.image_runs` (`ctrl_runs.py:71-80`) runs both shapes (`ctrl_image.py:93`) x {1, 2} x {`--without-srp`, srp, `--with-aecp`}. In `ctrl_srp_image.py:126-149` the compile flags do not depend on `--layout`. `--layout split` adds only the `plat/ctrl_split_start.S` compile (`:85-87`), which `test_ctrl_memory.py --build-only` (a known builder, `ctrl_configs.py:122`) builds (`test_ctrl_memory.py:955-963`). `--libc`/`--compiler-runtime` enter only the link (`:88-91`), and nothing compiles after the link (`:152-200`). The variant path changes only `HERE`, which the C compiles read only for `ctrl_aecp_image.c` (`aecp_inputs` does not use `HERE`) | code reads cited |
| `runtime_ssp.py`, `scenario.py`, `selftest.py`, `split_soc.py` compile no firmware or stack source | `runtime_ssp.py:21-30` only adds `-fno-stack-protector` to `ctrl_image_runtime.py`'s compiles (already `OUTSIDE`, `ctrl_configs.py:170`). `scenario.py:486-487` only reads `aecp.h`. `selftest.py` uses only `build.digest`/`run_inputs`/`tree_digest`/`reused` (`:687-694`) and reads `aecp.h` (`:605`). `split_soc.py:313` exports with `compile_software=False, compile_gateware=False` | code reads cited |
| `fixture_variant.py` in `SUITES` is the honest category | It runs `ctrl_srp_image.main()` in-process (`fixture_variant.py:15-20`), so it does compile firmware, and `OUTSIDE` would be false. It runs only under `run.py --variant`, never in a build-only run | code read |
| `OUTSIDE`/`SUITES` have no other consumer | Only `ctrl_configs.held` reads them (`ctrl_configs.py:317`). The only importers of `ctrl_configs` are `ctrl_boundary.py:132` and `ctrl_runs.py:52`, both gate modules. No image builder imports it, so no image can change | grep |
| Each entry is load-bearing, and the previous head's refusal is reproduced | `probe_held.py` runs the gate's own `held()` on a stub capture (every known builder run, every other found-by-text file compiled, scope `--without verilator`). As committed: ACCEPTED. Removing any one of the six: REFUSED, naming exactly that file. Removing all six: the refusal is **byte-identical** to hosted run 40408916714's | `receipts/probe_held.log` (rc 0), `receipts/probe_drop_all_refusal.txt`, `receipts/hosted_40408916714_refusal.txt`, `receipts/probe_vs_hosted_refusal.txt` |
| The failing hosted step passes at the exact head | Run 40506046891, job `firmware-boundary` (122195890804), `head_sha` e0e1b464, step 11 "Hold the TSN stack boundary over the firmware builders' compiles" **success** (executed, not skipped). It prints `ctrl_boundary: PASS` over 2854 compiled sources of 3084 recorded invocations, with 283 `[ok]` controls and 0 failures. `firmware-verilator` (122195890666) prints `ctrl_boundary: PASS` over 934 invocations, with 177 `[ok]` controls | `receipts/hosted_firmware_boundary_steps.txt`, `receipts/hosted_fw_boundary_job_result.txt`, `receipts/hosted_fw_verilator_job_result.txt` |
| The README's "no hosted job can run the harness's build" | No workflow installs `pythondata-software-picolibc` or `-compiler-rt`: they are not in `sw/litex/litex_pins.txt:52-58`, and grep of `.github/` finds neither. `firmware-verilator` installs only `pyyaml` (`rtl-fast.yml:1120`), with no LiteX. "Patched LiteX tree" matches `nvm_capture_cpu/README.md:18-19` (product patches) | greps |
| No image or figure change | By construction, as above. The author's `image_identity.txt` at e0e1b464 shows all nine ELFs SAME as round 2's `build.json` | author-r6 receipts (manifest verified) |
| Harness self-test unchanged | `run.py --self-test` at head: 87 checks, 62 `MUTANT caught`, `self-test: 0 failures`, rc 0 | `receipts/harness_run_selftest.log` |
| Bare-metal scope and docs | `check_baremetal_only.py --check`: 0 findings across 1431 files. `docs_check`, `doc_style`, `doc_map`, `naming`, `hygiene`, `py_idiom`, `doc_paths`: rc 0. The delta adds 0 em/en dashes and no heading. `git diff --check f58d049b HEAD`: clean | `receipts/baremetal_check.log`, `receipts/docs/summary.txt` |
| Comment rule (owner 2026-10-15) | The new source comment (`ctrl_configs.py:179-180`) and entries cite only issue IDs (#665, #723). There are no lane labels, lane names, review rounds, reviewer IDs or comment IDs | delta read |
| Published author receipts | `review-evidence/665s2-r1/MANIFEST.json` at `bfc68ced`: 144 `author-r6/` entries, 0 mismatched, 0 unlisted, 0 redacted. `gates/HEAD.txt` = e0e1b464. The author's local boundary logs show `ctrl_boundary: PASS` for both runs | `receipts/evidence_manifest_check.txt` |

## Findings

No BLOCKER, MAJOR or MINOR.

### RESIDUE (wording only; exact fix given; does not make the verdict NEGATIVE)

- **R703-6-R1 RESIDUE: Docs. The PR body names `ctrl_plants.py` as a reader of `ctrl_configs.py`.**
  - Where: PR #792 body, "No image or figure change" paragraph: "`ctrl_configs.py` is read only by the boundary gate (`ctrl_boundary.py`, `ctrl_runs.py`, `ctrl_plants.py`)."
  - What is true: only `ctrl_boundary.py:132` and `ctrl_runs.py:52` import it. `ctrl_plants.py:23` mentions `ctrl_configs.GATE` only in its docstring.
  - Impact: none. The load-bearing claim, that no image builder reads it, is true.
  - Exact fix: "... is imported only by the boundary gate's own modules (`ctrl_boundary.py`, `ctrl_runs.py`); no image builder reads it."
- **R703-5-R1 (carried, retained) RESIDUE: Docs.**
  - `tb/verilator/ctrl_service_budget/README.md:576` (`:564` at the previous head) still paraphrases its refusal: "the composed window committed two ACMP records, its declared load none".
  - The round-6 REVIEW READY comment again says "all 62 README mutant rows match".
  - The PR body no longer makes that claim.
  - Exact fix as R703-5-R1 states: make the row a verbatim prefix of the printed line, or say "61 rows quote the self-test's output; the declared-load row paraphrases its refusal".
- **R703-1 R-4 / R704-3-R1 (carried, retained).** `docs/testing/TESTING.md:518` still names only `nvm_capture_cpu` as the Makefile exception. The file is outside the lane, as disclosed. Fix as R704-3-R1 states.

### SUGGESTION (optional)

- **R703-6-S1: Tests, Docs. Two of the six entries stretch the category's wording, which the gate's taxonomy cannot express more exactly.**
  - The `SUITES` doc comment (`ctrl_configs.py:202-204`) speaks of "a suite builder's build-only run". `fixture_variant.py` is run by `build.py`/`run.py --variant`, and neither is a known builder.
  - Likewise, `build.py`'s planted control copy is a firmware compile outside the checkout. It is closer to what `SUITES` describes for the planted-defect campaigns, but one file takes one category.
  - Both reasons disclose this in their entry text, and the gate's effect is correct: `held()` treats the two categories alike.
  - Optional: one clause in each entry or doc comment, e.g. "run by the harness, itself not a known builder". The durable fix is the author's own open question for the manager: a hosted job that can run `build.py` under the capture, so it can become a known builder.
- **Carried, unchanged (no code they concern changed in this delta):** R703-5 S1 (probe M1: `main()`'s `results.json` write not exercised), R703-5 S2 (the mutant loop counts any exception as caught), and R703-5 S3 (the older optional escapes).

## Prior public findings at this head (read after the pass above)

| Finding | Status at `e0e1b464` | Evidence |
|---|---|---|
| R703-4-F1 MINOR, R703-4-F2 MINOR | Remain resolved. No code under `tb/verilator/ctrl_service_budget/` changed (`git diff --stat f58d049b..HEAD`: README only), and the self-test still runs 87 checks with 62 of 62 mutants caught | `receipts/harness_run_selftest.log` |
| R703-5-R1 (README mutant row) | **Retained** (above). The PR-body overstatement is gone; the round-6 REVIEW READY repeats it | `README.md:576` |
| R703-5-R2 (PR body "rendered from") | **Resolved.** The sentence is no longer in the PR body | live PR body |
| R703-1 R-4 / R704-3-R1 (`TESTING.md:518`) | **Retained**, outside the lane | `docs/testing/TESTING.md:518` |
| R704-3-R2 (`scenario.py` docstring) | **Resolved.** `scenario.py:845-846` carries the required text | file read |
| R704-3-R3 (README row label) | **Resolved.** `README.md:377` reads "the owed response, from the moment the room returns" | file read |
| R704-3-R4 (PR body sequencing) | **Resolved.** The PR body Known limitations cites the cache-first owner decision (issuecomment-6421463860) | live PR body |
| R703-5 S1-S3, R703-2 S1-S3 (optional) | Not applied; they stay optional | no code change in the delta |

## Lens ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | **CLEAN** | `[R703] PASS Conformance` — round-6 assignment items 1-3 and its STOP condition, checked against `ctrl_configs.py:152-221` and the gate contract `:3-58`. The departure from "BUILDERS or PART_OF" is disclosed in TAKEN before any edit, and each category is the truthful one under the gate's four (probe and code reads above). Hosted step success at the exact head. S2 frozen acceptance: no measurement or figure changed (no image builder imports `ctrl_configs`; author image identity). The measurement STOP (rows miss T_svc) is unchanged and correctly stated as "Relates to #665" | R703-6 | e0e1b4649ea3af908a8f32eccaad7903fa2cc134 |
| RTL | **CLEAN** | `[R703] PASS RTL` — `git diff --stat f58d049b..e0e1b464` touches no `.sv`/`.v`/`.cpp`/`.vlt`/SoC file. The test SoC export (`split_soc.py:313`) and the Verilator model inputs are unchanged. ELF identity holds for all nine images (author `image_identity.txt`). The R703-5 RTL verdict at `f58d049b` stands, because nothing it depends on changed | R703-6 | e0e1b4649ea3af908a8f32eccaad7903fa2cc134 |
| Robustness | **CLEAN** | `[R703] PASS Robustness` — the gate's failure path: each entry is an exact path (no glob), so a renamed or new harness file naming the firmware's tree is refused by name. Removing any entry refuses it (`receipts/probe_held.log`). The README states the rule for new files (`README.md:117`). The `tree:firmware` reuse side effect is disclosed: a pre-commit build is refused as stale, not silently reused (`build.py:443-456`) | R703-6 | e0e1b4649ea3af908a8f32eccaad7903fa2cc134 |
| Tests | **CLEAN** | `[R703] PASS Tests` — `probe_held.py`: 6 of 6 removals refused by name, drop-all byte-identical to hosted run 40408916714. Hosted `firmware-boundary`: 283 controls `[ok]`, 0 failures, PASS. `firmware-verilator`: 177 `[ok]`, PASS. Harness self-test at head: 87 checks, 62 of 62 mutants. The gate's code and controls are unchanged (the delta adds dict entries only) | R703-6 | e0e1b4649ea3af908a8f32eccaad7903fa2cc134 |
| Docs | **CLEAN** (RESIDUE R703-6-R1, the carried R703-5-R1 and TESTING.md:518 do not leave a lens unclean) | `[R703] PASS Docs` — `README.md:107-118` checked against the code and workflows (claims verified above). The PR body's round-6 sections were read in full. The docs gates I could run at head pass (`receipts/docs/summary.txt`); the em dash and TOC gates are covered by the author's verified receipts (rc 0). Comment rule clean | R703-6 | e0e1b4649ea3af908a8f32eccaad7903fa2cc134 |

## Real limits of this review

- **My local run of the full boundary gate did not complete, and I do not claim it.**
  - Attempt 1 was refused: `test_ctrl_firmware.py` "exited -15 under the capture", killed by SIGTERM at 284 s from outside the gate. The gate has no internal timeout, and the unit's memory peak was 1.6 GB of 12 GB.
  - Attempt 2 reached `test_ctrl_nvm.py` (both builders exit 0) before my own 595 s foreground cap stopped it. The gate runs its builders serially and needs longer than one foreground call allows here.
  - Raw: `receipts/boundary_without_verilator*.{log,rc}`.
  - For that step I rely on the hosted exact-head job (executed, PASS) and the author's verified receipt. The gate-specific effect of the delta is independently proven by `probe_held.py`.
- I did not run `--only verilator`, the firmware mutant shards, `behave`, the Verilator sweep or the em dash/TOC gates locally. The latter two need a Markdown renderer that is not installed here, and I made no shared install. Hosted exact-head jobs for the firmware shards, `firmware-unit`, `bdd-conformance` and `verilator-lint` show success. The author's receipts are manifest-verified.
- Hosted acceptance is the manager's. At my last snapshot (`receipts/hosted_rtl_fast_jobs_snapshot4.txt`):
  - every rtl-fast job had completed with success, but the "Fail fast across this head" job was still in progress;
  - `docs`, `elaborate` and `rtl-full` were queued.
- The ELF identity is the author's measurement. I accept it on the construction argument (no image builder reads the changed file) and did not rebuild the images.
- No manager source bank ran at this head, and none is claimed. Physical calibration was NOT RUN, and field skips are not hardware proof.
- The clone was restored and verified at the end: HEAD and tree match, index modes and blobs equal the HEAD tree, 0 untracked, the six gitlinks are as recorded, and the submodules are clean (`receipts/restore_verification.txt`). My `__pycache__` directories were removed. Temporary directories the gate made under the system temp area were left.

## Pending manager duties

- Decide the author's open question: keep `build.py` in `OUTSIDE`, or open an Issue for a hosted job that can run it under the capture (runtime packages, patched LiteX and Verilator together) so that it becomes a known builder.
- Accept the hosted contexts at this exact head: `rtl-fast` completion including fail-fast, and `docs`, `elaborate`, `rtl-full` (queued at review time). Also the act replica.
- Build and validate the current-dev merge candidate (source base e76a755a against live dev `97aab1d0`) with its builder and native banks, and link the receipts.
- Carry R703-6-R1, R703-5-R1 and TESTING.md:518 (R704-3-R1) to the residue checklist.
- The external review for this round is outstanding. Merging needs two independent positive reviews and the full completion bar.

R703-6 FINISHED
