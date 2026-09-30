[R401] POSITIVE - exact head 47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346

# R401-4: independent external delta review of processor PR #135 (lane C2, MAAP; issues #66, #67, #68), round 4

- **Head:** `47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346`, tree `329ff52af9e1f56d408f88182f577f14ed0a7f31`.
- **Shape:** one merge commit with parents `921fff59` (my POSITIVE round-3 head) and processor `main` `0451d83d` (PR #136, lane C3 ADP).
- **Verdict: POSITIVE.** No MINOR, MAJOR or BLOCKER is open, and all five lenses are CLEAN.
- **New:** one SUGGESTION, R401-4-S1 (Docs, a dated tally in C3's ledger).
- **Prior findings:** every earlier MINOR stays resolved at this head. Every retained suggestion stays retained, with its bytes unchanged.

## 1. What I reconstructed, in order

1. **Project rules.** The repository has no `AGENTS.md` or `CONTRIBUTING.md`. The project rules come from `README.md` (the build and check entry points, and the "pin only when green here first" rule) and `docs/README.md` (single-source rules, `make check`).
2. **Scope.** Issue #66's frozen acceptance, then the manager's lane and round comments on #66:
   - 5884446021: the lane opening;
   - 5887951933: round 2;
   - 5890772857: the Release! ruling;
   - 5903309279: round 3;
   - 5910732518: round 4, "merge only". It requires both sides kept, any moved patch re-anchored, every suite and entry point rc 0, both campaigns KILLED in full, and "No other change".
3. **The PR body.** Its Round 4 section: the merge, validation and the parent-visible list.
4. **The merge, from git objects.** `git diff 0451d83d..47afa74d`, the merge base, and a replay of the merge.
5. **The public evidence at `kebag-logic/milan-fpga@73c8b7a0`, `review-evidence/ppC2-r1`.** I read the author-r4 receipt index and the manifest. I did not open the `reviews/` subtree before my verdict.
6. **Prior public review findings on #135.** I read these only after my own pass was complete (section 5).

## 2. Evidence I produced

Every command ran in the foreground. The scripts are in `scripts/` and the raw receipts in `receipts/`.

**Environment**
- **Isolation.** The runs used a `git archive` export of the exact head in a disposable scratch directory, never the review clone.
- **Simulator.** Release v5.050 is the version CI pins (`.github/workflows/hdl.yml:10`).
  - The assigned wrapper path does not exist on this host.
  - All 216 pinned wrappers under the shared tmp area are byte-identical (sha256 `905795b9…`). I copied one and recorded the hashes of its target binary (`receipts/20-setup.txt`).
- **Parallelism.** Every build and run was capped at 8 CPUs.

| Evidence | Result | Receipt |
|---|---|---|
| Merge composition (script 10) | Parents `921fff59`, `0451d83d`, merge base `b2db3a97`. The files changed by `0451d83d..head` are exactly the 42 files the lane changed from the base. 37 lane-only files are byte- and mode-equal to `921fff59`, and 40 main-only files to `0451d83d`. A `merge-tree` replay conflicts in exactly the 4 named files, and `tb/pp_top/README.md` auto-merges to the head's bytes. The replay-to-head diff is the hand resolution alone: +5/−28 lines, none under `hdl/`. `git diff --check` is clean against both parents | `receipts/10-merge-composition.txt` |
| Patch anchoring | 55 of 55 MAAP (27) and ADP (28) patches pass `git apply --check` at the head. Their targets are `KL_pp_maap.sv` and `KL_pp_rx_validator.sv` (lane side), and `KL_adp_engine.sv`, `KL_aecp_engine.sv` and `protocol_processor_top.sv` (main side). Each HDL file equals exactly one parent, so no patch needed re-anchoring | same |
| `tb/maap`, `tb/rx_validator`, `tb/adp_engine`, `tb/timer_map` | 196/0, 497/0, 1,367/0, 1,360/0 | `receipts/head/*-run.log` |
| `tb/pp_top` full run (both builds) | 7,949 checks, 0 failures (the default build 7,929, with NW 85, D3 133 and AD 55; the fixture build 20) | `receipts/head/pp_top-run.log` |
| pp_top focused modes (the merged `main()`) | `maap-internal` 34/0, `adp-config` 55/0, `gsi-internal` 6,182/0, `name-writes` 85/0, `--d3-only` 133/0, `--dr3a` rc 0. Each tally is its own section alone, so no focused mode leaks another section | `receipts/head/pp_top-*.log` |
| MAAP campaign `make -C tb/maap mutants` | 32/32: 3 controls PASS and 29 of 29 arm runs KILLED. All 29 (arm, suite) tallies equal `tb/maap/README.md`'s ledger | `receipts/head/maap-mutants.log`, `receipts/head/maap-mutants/`, `receipts/40-maap-ledger-compare.txt` |
| ADP campaign `make -C tb/adp_engine mutants` | 32/32: 2 controls PASS and 30 of 30 arms KILLED. All 30 failure counts equal `tb/adp_engine/README.md`'s ledger | `receipts/head/adp-mutants.log`, `receipts/head/adp-mutants/`, `receipts/41-adp-ledger-compare.txt` |
| Composition probe: C3's `gate-enable-dropped` under the full merged pp_top run | rc 2. Exactly D3R14, AD0 ×2 and AD1b fail (4 of 7,929 default-build checks), as C3's ledger records. No MP or other check moves | `receipts/50-gate-full-pp_top.txt`, `receipts/50-gate-full-pp_top.log` |
| Suite-input map (script 60) | Of 33 suites, only `tb/pp_top` has inputs that differ from both parents, and it ran above in full and in every mode. Every other suite's directory, HDL sources and `scripts/` are byte-equal to at least one parent head | `receipts/60-suite-inputs.txt` |
| Static | `lint_hdl.sh` (41 modules LINT OK), `make check`, `gen_matrix.py --check` and `check_upc_map.py`: all rc 0 | `receipts/head/{lint_hdl,make-check,gen_matrix,check_upc_map}.log` |
| Hosted, exact head (read-only query at 17:09Z) | `docs-gates` ×2 and `portability` ×2 are success. `suites` ×2 is in progress: step 5 ("Lint (zero tolerance) + every suite") is success, the SRP campaign is running, and the MAAP campaign, ADP campaign, matrix and nvm_port steps are pending. The simulator build step was skipped because the cache hit | `receipts/70-hosted-checks.txt` |
| Clone integrity after all work | HEAD and the index tree are exact, and 386 tracked blobs rehash equal with correct modes. There are no untracked or ignored files, the tree has no gitlinks, and there is no `.gitmodules` | `receipts/90-verify-clone.txt` |

## 3. The round-4 items

**(1) The four conflicted files keep both sides, and add nothing else** (`receipts/10-merge-composition.txt`).

- **`.gitattributes:3-4`:** the MAAP and ADP patch whitespace entries, after the SRP entry.
- **`.github/workflows/hdl.yml:59-66`:** the "MAAP mutation campaign" step, then the "ADP mutation campaign" step, after the SRP campaign (`:55`). Their default output directories are distinct (`/tmp/maap-mutants` and `/tmp/adp-mutants`).
- **`tb/pp_top/Makefile:69-73, :104`:**
  - `maap-internal` runs `--maap-internal-only`, and `adp-config` runs `--adp-only`;
  - both depend on `gsi-build`;
  - `.PHONY` lists both.
- **`tb/pp_top/sim_main.cpp`:**
  - `run_maap_internal` (`:10050`) sits beside C3's section AD and `run_adp_config` (`:10392`). Both switches are kept (`:10415-10416`).
  - `main()` takes C3's `one_section` form with `maap_only` added (`:10421-10427`).
  - The lane's old per-line guards gave the same result for `--maap-internal-only`: MP alone. My tallies confirm it: `maap-internal` is 34 and `adp-config` is 55, each alone, and the default run includes MP (inside `Suite`) and AD.

**(2) The diff equals the PR's own content plus nothing else.**

- The files changed by `0451d83d..head` are exactly the lane's files, and each lane-only file is the round-3 blob.
- Of the 5 files changed on both sides, `tb/pp_top/README.md` is the clean auto-merge.
- The other four differ from the replayed merge only by conflict-marker removal and the one `.PHONY` and `one_section` union.
- No main-only file differs from `0451d83d`.

**(3) C3's configuration-valid flag and the MAAP engine share nothing.**

- **The flag's path:** `KL_aecp_engine.dyn_cur_config_v_o` → `aecp_cur_cfg_v_w` → the `adp_cur_cfg_w` mux → `KL_adp_engine.current_cfg_i` (`protocol_processor_top.sv:1721-1723, :1753, :3690`). That is its whole fan-out.
- **The MAAP engine:** `KL_pp_maap` (`u_maap`, `:2175-2240`) connects none of these nets and references no config, ADP or AECP net.
- **TX clients:** ADP is 0, AECP is 4 and MAAP is 5 (`:3871-3876`).
- **Timer slots:** ADP's `TMR_ADP_*_BASE_C` and `TMR_MAAP_BASE_C` are distinct (`:760-767`), under the elaboration-time non-overlap guard (`:808-813`). Neither side changed any of them.
- **HDL scope:** main changed only `KL_adp_engine.sv`, `KL_aecp_engine.sv` and the top's configuration lines. The lane changed only `KL_pp_maap.sv`.

**(4) Every suite, entry point and both campaigns at the merged head.**

- My own runs are listed in section 2.
- The only suite whose inputs are new relative to both parents (`tb/pp_top`) passes in full and in every focused mode.
- Both campaigns are KILLED in full, with their ledgers equal.
- The hosted "every suite" step is success at this exact head.

**(5) The PR body's Round 4 note.**

These claims check against my evidence:
- 11 commits (9 non-merge and 2 merges) in 45 main-side files;
- 5 files changed on both sides, 4 of them conflicted;
- no patch moved, and 55 of 55 apply;
- MP stays at 34;
- pp_top goes from 7,893 to 7,949;
- `tb/maap` 196, `rx_validator` 497 and `adp_engine` 1,367;
- 32/32 for both campaigns.

The author ran simulator release v5.052 while CI pins v5.050. I reproduced every figure I re-ran on v5.050. The parent-visible list correctly says the resolution adds nothing parent-visible, and it attributes C3's single new engine output to main.

## 4. Findings

No MINOR, MAJOR or BLOCKER.

### R401-4-S1: SUGGESTION. Lenses: Docs

- **Where:** `tb/adp_engine/README.md:184` (a main-side line, unchanged by this PR). The `gate-enable-dropped-top` row reads "In the full default pp_top run (7,924 checks after the merge of PR #132) it fails these 3 and D3R14, 4 in all".
- **Authority/evidence:** at the merged head, the full default build has 7,929 checks. My probe (`receipts/50-gate-full-pp_top.txt`) shows the same patch still fails exactly D3R14, AD0 ×2 and AD1b, 4 in all. The failure record is true. Only the dated parenthetical count no longer matches a run at this head.
- **Impact:** none on any gate. A reader who re-runs it sees 7,929, not 7,924.
- **Suggested outcome:** when that file is next touched, drop the absolute count or restate it at the then-current head. This round is merge-only, so a retention is appropriate.
- **Verification:** the count cited equals the default-build tally of a full pp_top run at the head that cites it.

## 5. Prior public review findings, at this head

I read R400-1/R401-1, R400-2/R401-2 and R400-3/R401-3 after my own pass.

- **Content unchanged:** the 37 lane-only files, including `hdl/maap/KL_pp_maap.sv`, `tb/maap/*` and `docs/architecture/11_maap_engine.md`, are byte-equal to `921fff59`. The earlier resolutions therefore rest on unchanged content.
- **Arms re-proved:** the arms that proved them are all KILLED in my head campaign.

| Finding | Status at `47afa74d` | Basis |
|---|---|---|
| R400-1 F1 to F4, R401-1 F1 (MINOR) | **Remain resolved** | The arms `ival-sends-after-release`, `post-publishes-after-release`, `tx-path-absorbs-release`, `off-waits-for-an-edge`, `rx-release-returns-to-idle`, `seed-rearmed-on-idle-release-only`, `idle-serves-a-latched-expiry-first`, `teardown-keeps-announce-timer`, `drain-waits-for-the-link`, `release-waits-for-draw` and `release-keeps-draw-mark` are KILLED with ledger-equal tallies |
| R400-2-F1 (MINOR, Tests) | **Remains resolved** | U29 at the head; `tx-set-omits-{alloc,gwait,write,commit,lane}` KILLED on U29 |
| R400-2-F2 (MINOR, Docs) | **Remains resolved** | The PR body's "What remains (round 1, rewritten in round 3)" is unchanged and still matches the ruling in #66 comment 5890772857 |
| R401-1 F2 to F4, R400-2-S1 (SUGGESTION) | **Remain taken/resolved** | Their files are unchanged |
| R400-1 S1 (compare_MAC pair with equal low octets) | **Retained** | Not in the merge-only assignment; the PR body retains it |
| R400-1 S2 (shared default `/tmp/maap-mutants`) | **Retained** | `tb/maap/Makefile:4` is unchanged (`receipts/80-retained-suggestions.txt`). The merged CI's ADP step uses its own `/tmp/adp-mutants`, so the merge does not worsen it |
| R401-2 S1 (a), S2, and S3's comment re-flow at `KL_pp_maap.sv:619-623` | **Retained** | `KL_pp_maap.sv` is byte-equal to `921fff59` |
| R400-3-S1 and R401-3-S1 (re-flow of over-long lines) | **Retained** | Still present: `tb/maap/README.md:165` (140 characters) and `11_maap_engine.md:138` (113 characters). The PR body retains both, and this round is merge-only |

## 6. Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #66 acceptance and the round-4 assignment (5910732518: merge only, both sides kept, no other change). The merge has two parents and no rebase. The MAAP normative content (`11_maap_engine.md`, `KL_pp_maap.sv`, `tb/maap`) is byte-equal to the round-3 POSITIVE head, and the #66/#67/#68 arms (fit, seed, version and compare_MAC) are KILLED at the head | R401-4 | `47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346` |
| RTL | CLEAN | Each `hdl/` file equals exactly one parent. The C3 flag's fan-out in `protocol_processor_top.sv:1721-1723, :1753, :3690`, `u_maap` `:2175-2240`, the TX clients `:3871-3876`, the timer bases and the guard `:760-767, :808-813`. `lint_hdl.sh` 41/41 | R401-4 | `47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346` |
| Robustness | CLEAN | Focused-mode isolation (each mode's tally is its section alone), both campaigns in distinct scratch and output directories, C3's gate mutant under the full merged run (4 exact failures, MP undisturbed), the suite-input map, and clone integrity after all work | R401-4 | `47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346` |
| Tests | CLEAN | `tb/maap` 196, `tb/rx_validator` 497, `tb/adp_engine` 1,367, `tb/timer_map` 1,360, `tb/pp_top` 7,949 and its 6 modes. The MAAP campaign is 32/32 (29 KILLED, ledger-equal), and the ADP campaign is 32/32 (30 KILLED, ledger-equal). All 55 patches apply, and the hosted every-suite step passed at the head | R401-4 | `47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346` |
| Docs | CLEAN (R401-4-S1 is a SUGGESTION) | The auto-merged `tb/pp_top/README.md` (`adp-config` `:620`, `maap-internal` `:1189`). The `tb/maap` and `tb/adp_engine` ledgers were re-derived from runs. The PR body's Round 4 figures and parent-visible list. `make check` and `gen_matrix --check` rc 0 | R401-4 | `47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346` |

## 7. Real limits

- **Suites not re-run.** I did not run the full processor suite sweep (`run_suites.sh`) myself, or the SRP, D3, GSI and name-write campaigns, the `nvm_port` figures, or `syn/yosys/run.sh`. The first three are excluded bank classes for this role. For the 32 suites whose inputs equal a parent head, I rely on the byte-equality map, the hosted "every suite" step (success at this head), and the author's published receipts.
- **Simulator path.** The assigned simulator path was absent. I used a byte-identical copy of the host's shared v5.050 wrapper, whose identity is recorded. The author used v5.052.
- **Hosted campaigns.** The hosted MAAP and ADP campaign steps were still pending when I queried. I observed only the executed steps. The simulator build step was skipped because the cache hit, which is not a failure.
- **Parent and donor banks.** I did not run the parent consumer bank at dev `ccdd07b5`, the donor bank, or any builder, Yosys or hardware step. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Manager banks at this head.** The assignment states the manager's source, static, builder and native banks passed at this head. The evidence snapshot at `73c8b7a0` carries the author-r4 receipts but no separate manager round-4 bank record, and the PR/issue threads carry the manager's bank comments only up to round 3. I did not verify that statement independently.

## 8. Pending manager duties

- Confirm the hosted `suites` jobs at `47afa74d` complete, including the MAAP and ADP campaign steps. Own hosted/act acceptance.
- Run the donor bank and the official parent consumer bank at milan-fpga dev `ccdd07b5`, with the combined #132 + C1 adaptation (C3 adds no parent edit).
- Build the final current-dev candidate at the merge turn (source base `0451d83d`, live dev `ccdd07b5`), distinct from this source validation.
- Obtain the second independent review.
- Decide the retained SUGGESTIONs: R400-1 S1/S2, R401-2 S1(a)/S2/S3 (the comment re-flow), R400-3-S1, R401-3-S1 and R401-4-S1.

R401-4 FINISHED
