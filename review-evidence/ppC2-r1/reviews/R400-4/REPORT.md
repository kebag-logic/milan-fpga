[R400] POSITIVE - exact head 47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346

# R400-4: processor PR #135 (lane C2, MAAP), issues #66, #67, #68, round 4 (merge only)

- **Head:** `47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346`, tree `329ff52af9e1f56d408f88182f577f14ed0a7f31`.
  It is one merge commit, with parents `921fff59` (my POSITIVE round-3 head) and main `0451d83d` (PR #136, lane C3).
- **Verdict: POSITIVE.** No MINOR, MAJOR or BLOCKER is open, and all five lenses are CLEAN.
  - I record one new SUGGESTION, R400-4-S1 (Docs, Tests), on C3 text the merge brings in.
  - Every prior public finding keeps its round-3 status. The MAAP files are byte-identical to round 3.
- **Independence:** I fixed my verdict and ledger before reading any prior review. The snapshot is
  `receipts/verdict-before-prior-findings.md`, written 2026-09-30 18:20 UTC. I read no private author
  material, no lane scratchpad, and no other reviewer's round-4 report.

## 1. What was reconstructed, in order

1. The repo has no `AGENTS.md` or `CONTRIBUTING.md`. I read `README.md` and `docs/README.md`: `make check`,
   `scripts/run_suites.sh`, `scripts/lint_hdl.sh`, `gen_matrix.py --check`, and the single-source rules.
2. **Issue #66:** the frozen acceptance, the lane-C2 assignment (5884446021), the ruling on the STOP
   (5890772857), round 3 (5903309279) and the round-4 assignment (5910732518). Round 4 is "merge only", with
   these requirements:
   - both sides kept in the four conflicted files;
   - any moved mutation patch re-anchored;
   - every suite and entry point rc 0, and both campaigns KILLED in full;
   - a "Round 4" note in the PR body;
   - "No other change".
3. **Interface authorities:** `protocol_processor_top.sv` (the ADP current-configuration mux, the
   `KL_pp_maap` instance, the TX-client and timer bases) and `KL_aecp_engine.sv` (the new
   `dyn_cur_config_v_o`).
4. **History and diffs:**
   - `git diff 0451d83d..47afa74d` and `git diff 921fff59..47afa74d`;
   - the merge base `b2db3a97` (the only one);
   - main's 11 commits `b2db3a97..0451d83d`.
5. **Public evidence:**
   - the author's round-4 packet (`review-evidence/ppC2-r1/author-r4` at milan-fpga `73c8b7a0`);
   - the manager comments on #66 and #135;
   - the hosted runs at the exact head.

## 2. Evidence I produced (foreground; Verilator builds capped at 8 jobs in total)

**Tooling.** The pinned path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist
on this host (`receipts/tool-identity.txt`). So I used the host package Verilator 5.052 (`verilator_bin`
sha256 `37fbb386…`, the same binary the author used), through a wrapper that rewrites `-j 0` to `-j 8`
(`scripts/verilator-cap8`). For the D3 driver I used `-j 2` with `--jobs 4` (`scripts/verilator-cap2`). The
pinned 5.050 is covered by the hosted run (row H below). Every run was in a local clone of this review clone
under `scratch/`, at the exact head, and its tracked files were unchanged afterwards.

| # | What | Result | Receipt |
|---|---|---|---|
| C1 | `git merge-tree --write-tree 921fff59 0451d83d` (the merge replayed) | the same four conflicts; `tb/pp_top/README.md` auto-merges | `receipts/merge-tree-replay.txt` |
| C2 | the replay compared with the head | only the four conflicted files differ; every auto-merged file equals the replay byte for byte | `receipts/replay-vs-head.diff`, `receipts/replay-vs-head-stat.txt` |
| C3 | every path classified by blob against base `b2db3a97` and both parents | 304 untouched, 37 branch-only (each equal to `921fff59`), 40 main-only (each equal to `0451d83d`), 5 both-sides, 0 extra changes, PASS | `scripts/merge_composition.sh`, `receipts/merge_composition.txt` |
| C4 | the five both-sides files: this PR's own hunks (`b2db3a97..921fff59`) compared with `0451d83d..47afa74d` | `.gitattributes`, `hdl.yml` and `tb/pp_top/README.md` are identical. `Makefile` differs only by `adp-config` in `.PHONY`. `sim_main.cpp` differs only in `main()`, main's `one_section` form with `maap_only` OR-ed in | `receipts/both-sides-hunks.txt` |
| T1 | `./scripts/run_suites.sh` | rc 0, 33 suites, 1,017,348 checks, 0 failing (`maap` 196, `rx_validator` 497, `adp_engine` 1,367, `pp_top` 7,949) | `receipts/run_suites.log` |
| T2 | `make -C tb/maap mutants` (full entry point) | rc 0, 32/32: 3 controls PASS, 29 of 29 arms KILLED. The same result in three `--only` subsets | `receipts/maap-mutants/full-entry-point.txt`, `g1..g3.txt` |
| T3 | MAAP ledger compared with the campaign | 29 of 29 arm tallies ("N FAIL of M") equal the `tb/maap/README.md` rows, PASS | `scripts/ledger_vs_campaign.py`, `receipts/maap-ledger-vs-campaign.txt` |
| T4 | `make -C tb/adp_engine mutants` (full entry point) | rc 0, 32/32: 2 controls PASS, 30 of 30 arms KILLED. The pp_top subset was also run alone: 11/11 | `receipts/adp-mutants/full-entry-point.txt`, `top.txt` |
| T5 | ADP ledger compared with the campaign | 30 of 30 failure counts equal the `tb/adp_engine/README.md` rows, PASS | `scripts/adp_ledger_vs_campaign.py`, `receipts/adp-ledger-vs-campaign.txt` |
| T6 | `python3 tb/pp_top/d3_mutants.py` (in six `--only` chunks covering all 83) | 83 of 83 KILLED; every golden PASS (pp_top, acmp_nvm, rx_validator) | `receipts/d3-mutants/chunk00..05.txt` |
| T7 | `gsi_mutants.py`, `name_wr_mutant.py` | rc 0: 20 detected, golden and restored PASS; decode killed, golden and restored PASS | `receipts/pp_top-drivers/*.txt` |
| T8 | `lint_hdl.sh`, `make check`, `gen_matrix.py --check`, `git diff --check` against `c951a9ff`/`921fff59`/`b2db3a97`/`0451d83d` | all rc 0 (links 981; 115 REQ / 17 GAP; 94 rows, 0 untested) | `receipts/entry-points.txt` |
| T9 | pp_top `maap-internal`, `adp-config`, `gsi-internal`, `name-writes`, `--d3-only`, `--dr3a` | rc 0: 34 / 55 / 6,182 / 85 / 133 checks, 0 failures; `--dr3a` measurements only (see the note below) | `receipts/entry-points.txt` |
| T10 | `make -C tb/nvm_port figures` | rc 0 | `receipts/nvm_port-figures.txt` |
| T11 | all 55 MAAP and ADP patches: `git apply --check` at the head; `git check-attr whitespace` | 55 of 55 apply unchanged, so none needs re-anchoring. The attribute is set on all three campaign directories | `receipts/patch-attrs-and-apply.txt` |
| P1 | disposable probe: C3's `gate-enable-dropped` patch planted, full default pp_top run at the merged tree | rc 2; 4 of 7,929 default-build checks fail: AD0 ×2, AD1b and D3R14; MP stays green. This is the same failure set C3's ledger records | `scripts/probe_gate_full_run.sh`, `receipts/probe-gate-enable-dropped-full-run.log` |
| H | hosted `hdl` workflow at the exact head, push run 36745796996 and pull_request run 36745800364 | every job succeeded (suites, docs-gates, portability). In the suites job these steps executed and succeeded (none skipped): lint + every suite, the SRP, **MAAP** and **ADP** campaigns, the matrix and the nvm_port figures. Its log shows Verilator **5.050**, 1,017,348 checks with 0 failing, and three campaign tallies of 90/90, 32/32 and 32/32. The only skipped step is the Verilator build (a cache hit) | `receipts/hosted-*.t*` |
| I | review clone integrity after all work | HEAD, index tree and worktree all equal `47afa74d`/`329ff52a`; 0 untracked or ignored files; 386 tracked files (374 at 100644, 12 at 100755); 0 gitlinks, and no `.gitmodules` exists | `receipts/clone-integrity.txt` |

**Note on T9.** My first `--d3-only`/`--dr3a` invocation ran from the repo root: 55 of 133 failed and
`obj_dir/build_tally.txt` could not be opened. The binary reads `ucode.hex`, `ltn_rom.hex` and `obj_dir/`
relative to its working directory. Run from `tb/pp_top`, the way the Makefile targets and `d3_mutants.py` run
it, it passes 133/0. This behaviour predates the merge, and the author's packet records the same thing. The
receipt keeps both runs, with the note.

## 3. The round-4 item, judged

### The composition (Conformance, Robustness)

- **`.gitattributes:3-4`:** the MAAP and ADP patch entries both follow the SRP entry, and both carry the
  whitespace attribute (T11).
- **`.github/workflows/hdl.yml:59-66`:** the MAAP campaign step, then the ADP campaign step, both after the SRP
  step. Both executed at the exact head in the hosted runs (H).
- **`tb/pp_top/Makefile:68-73`:** both targets are present, and `:104` lists `maap-internal adp-config` in
  `.PHONY`. The only glue is a blank line.
- **`tb/pp_top/sim_main.cpp`:**
  - `:10050-10054`: `run_maap_internal`, with its missing `}` restored;
  - C3's section AD follows, with `run_adp_config` at `:10392`;
  - `:10412-10427`: both switches, and main's `one_section` form with `maap_only` added.
- **Focused-mode equivalence.** The branch's old `!gsi_only && …` guards and the new form select the same
  sections in every mode:
  - `--gsi-internal-only`: section GI only;
  - `--name-writes-only`: NW only;
  - `--d3-only`: D3 only;
  - `--maap-internal-only`: MP only, via `run_maap_internal`;
  - `--adp-only`: AD only;
  - the default: `Suite` (with MP inside it, `:8942`), then GI, NW, D3 and AD.

  T9 confirms the tallies (34 and 55 are the section sizes alone). T3 confirms that the campaign's pp_top arms
  still see exactly 34 checks.
- **Nothing else.** C2–C4 show that `git diff 0451d83d 47afa74d` is this PR's reviewed content (every
  branch-only blob equals `921fff59`) plus that glue, and nothing else.

### The C3 configuration flag and the MAAP engine share nothing (RTL)

- **The flag's fanout.** `dyn_cur_config_v_o` (`KL_aecp_engine.sv:654`, driven at `:1814` from `dyn_cfg_v_r`)
  reaches the top as `aecp_cur_cfg_v_w` (`protocol_processor_top.sv:1721`, `:3690`). Its only load is the mux
  `adp_cur_cfg_w` (`:1723`), and that mux's only load is `u_adp.current_cfg_i` (`:1753`).
- **The MAAP instance.** `u_maap` (`:2175-2240`) has no port on either net.
- **TX clients.** ADP is `TXC_ADP_C = 0` and MAAP is `TXC_MAAP_C = 5` (`:3871-3876`), unchanged by either side.
- **Timers and PRNG.** The MAAP timer base (`TMR_MAAP_BASE_C`), owner and PRNG requests are unchanged; C3
  touches no arm face.
- **Disjoint edits.** The two sides edit disjoint `hdl/` files: this lane edits only `hdl/maap/KL_pp_maap.sv`,
  and C3 edits `KL_adp_engine.sv`, `KL_aecp_engine.sv` and the top.
- **Behaviour agrees.** P1 shows C3's boot-gate mutant fails the same four checks with MP green.

### The PR body's Round 4 note (Docs)

- It names the merge and its parents, the four resolutions, and "no mutation patch moves". T11 confirms that
  claim.
- Its tallies match mine: 33 suites, 1,017,348; pp_top 7,949; MP 34, AD 55; MAAP 32/32; ADP 32/32; D3 83/83.
- It keeps round 3's parent-visible list and adds C3's list, which I checked: one new `KL_aecp_engine` output,
  instantiated only by the top.
- It lists the retained suggestions.

## 4. Prior public findings: resolved or retained at this head

At `47afa74d`, these are byte-identical to `921fff59` (`receipts/prior-findings-anchors.txt`):
`hdl/maap/KL_pp_maap.sv`, `tb/maap/{sim_main.cpp, maap_wrap.sv, README.md, Makefile, mutations/}`,
`tb/rx_validator/` and `docs/architecture/11_maap_engine.md`.

| Finding | Status at this head | Evidence |
|---|---|---|
| R400-1 F1–F4 (MINOR) | **Resolved** (since round 2; still holds) | their arms are KILLED in T2: `ival-sends-after-release`, `post-publishes-after-release`, `tx-path-absorbs-release`, `off-waits-for-an-edge`, `rx-release-returns-to-idle`, `release-waits-for-draw`, `seed-rearmed-on-idle-release-only`, `seed-clamp-off-by-one`, `idle-serves-a-latched-expiry-first`, `teardown-keeps-announce-timer`, `drain-waits-for-the-link` |
| R400-1 S1, S2 (SUGGESTION) | **Retained** | not in the merge-only assignment. `tb/maap/Makefile:4` still defaults to `/tmp/maap-mutants`, and the MAAP sources are unchanged |
| R401-1 F1 (MINOR); F2–F4 (SUGGESTION) | **Resolved** (since round 2; still holds) | the same arms KILLED; `11` §6 unchanged |
| R401-2 S1 | (b) **Resolved** (it is R400-2-S1). (a) **Retained** | the reason is in the PR body; the text is unchanged |
| R401-2 S2 | **Retained** | not in the assignment |
| R401-2 S3 | first half **Resolved**; the comment re-flow **Retained** | this round changes no `hdl/` file |
| R400-2-F1 (MINOR) | **Resolved** | the five `tx-set-omits-*` arms are KILLED on U29 (T2), with tallies equal to the ledger (T3) |
| R400-2-F2 (MINOR) | **Resolved** | the PR body still carries "What remains (round 1, rewritten in round 3)" |
| R400-2-S1 | **Resolved** (taken) | U28 text unchanged |
| R400-3-S1, R401-3-S1 (SUGGESTION) | **Retained** | `11_maap_engine.md:137-138` and `tb/maap/README.md:163-165` are unchanged; the PR body lists them as retained, per "No other change" |

## 5. Findings

No MINOR, MAJOR or BLOCKER is open.

### R400-4-S1: SUGGESTION. Lenses: Docs, Tests

- **Where:** `tb/adp_engine/README.md:184`, the `gate-enable-dropped-top` row. This is C3's text, brought in
  unchanged by the merge.
- **Authority/evidence:** the row says the patch "in the full default pp_top run (7,924 checks after the merge
  of PR #132) … fails these 3 and D3R14 … 4 in all". At the merged head, P1 measures the same four failures
  out of 7,929 default-build checks, and the author's round-4 packet records the same figure.
- **Impact:** none on any gate. The failure set, which is the substantive claim, still holds. The count is
  dated to C3's branch, so a reader comparing it with the merged tree sees a different number.
- **Suggested outcome:** when this ledger is next touched, restate the count at the then-current head, or mark
  it as measured on C3's branch. Nothing is required in this merge-only round.
- **Verification:** `scripts/probe_gate_full_run.sh <repo> <head> <scratch>` prints the four named failures
  and the default-build tally.

## 6. Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #66 assignment 5910732518 against the merge: both sides kept in the four conflicted files, no re-anchor needed (T11), no other change (C2–C4); the MAAP Annex B behaviour is byte-identical to round 3 | R400-4 | 47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346 |
| RTL | CLEAN | `protocol_processor_top.sv:1721-1753, 2175-2240, 3690, 3871-3878`; `KL_aecp_engine.sv:654, 1784-1814`; the `hdl/` diff on each side from `b2db3a97` (disjoint files); lint 41 OK | R400-4 | 47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346 |
| Robustness | CLEAN | merge replay and per-path classification (C1–C4); focused-mode equivalence in `main()`; P1 (C3's mutant with MP present); the SRP campaign's and nvm_port's input trees equal in both parents and the head (`receipts/unchanged-input-trees.txt`) | R400-4 | 47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346 |
| Tests | CLEAN (S1 is a SUGGESTION) | T1–T10: 33 suites, 1,017,348 checks; MAAP 32/32 and ADP 32/32 in full, with both ledgers equal to the runs; D3 83/83; GSI; name-write; the focused modes; hosted H | R400-4 | 47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346 |
| Docs | CLEAN (S1 is a SUGGESTION) | the PR body's Round 4 section; `tb/pp_top/README.md` (AD at `:612-623`, MP at `:1169-1191`, both entry points); `tb/maap/README.md` and `tb/adp_engine/README.md` ledgers; `11` §6 unchanged; `make check` rc 0 | R400-4 | 47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346 |

## 7. Real limits

- **Pinned tool.** The pinned Verilator 5.050 path named in my brief is absent, so every local run used host
  5.052. The hosted suites job at the exact head ran 5.050 and reports the same tallies (H), and I did not
  re-run it.
- **SRP campaign.** I did not re-run `make -C tb/srp_top mutants` (90 runs). Its inputs are identical trees in
  `921fff59`, `0451d83d` and the head (`hdl/srp`, `hdl/common`, `hdl/packet_engine`, `tb/srp_top`,
  `tb/common`), and it executed and passed 90/90 in the hosted job at the head.
- **Yosys.** I did not run `syn/yosys/run.sh` or any parent, builder, gPTP or Yosys bank; they are outside my
  brief.
- **Chunked D3 run.** The D3 driver ran as six `--only` chunks with `--jobs 4`, each with its own goldens,
  rather than one invocation. Together they cover all 83 mutants.
- **Background runs.** Two long runs, the first `run_suites.sh` and the name-write + GSI pair, outlived the
  shell's 10-minute foreground limit. The session moved them to the background, and I polled them to
  completion before continuing; their receipts are complete, with rc lines. Every other run finished in the
  foreground.
- **Hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof.
- **Manager evidence.** I found no manager-authored round-4 bank receipt in the evidence tree at `73c8b7a0`,
  and no round-4 manager-bank comment on #135 when I read it. The latest is round 3's (5906975060). My brief
  states the manager's source banks passed at this head, and I did not verify that independently.

## 8. Pending manager duties

- Hosted/act acceptance at `47afa74d`. I inspected only the two hosted `hdl` runs above.
- The donor bank and the official parent consumer bank at milan-fpga dev `ccdd07b5`, with the combined
  #132 + C1 adaptation (C3 adds no parent edit). Then the final current-dev candidate at the merge turn:
  source base `0451d83d`, live dev `ccdd07b5`.
- The second independent round-4 review.
- A decision on the retained SUGGESTIONs: R400-1 S1/S2, R401-2 S1(a)/S2/S3's re-flow, R400-3-S1, R401-3-S1,
  and R400-4-S1.
- Pin adoption, per the PR body's round-3 list plus C3's list.

R400-4 FINISHED
