[R478] NEGATIVE - exact head 2f0f59291080aeab934e0d72e124fb448c105e12

# R478-1: internal cleared-context review of #652 / PR #660

- Head `2f0f59291080aeab934e0d72e124fb448c105e12`, tree `a094320f330221d3941c4a417283000b7b13a10a`; base and live `dev` `6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5`; five commits, 12 files.
- Reconstructed from AGENTS.md, CONTRIBUTING.md (sections 5 and 6), the #652 issue body, the lane comment, the executor's STOP, the ruling (option 1), REVIEW READY, the PR body, the diff and history, and the public evidence tree at `7ac6966b`. I read no private author material and no other reviewer's report.
- No prior public review findings exist on PR #660 or issue #652. The PR has no reviews and no inline comments, and its two comments are review-start notices. So nothing needed resolving or retaining.

## Verdict

NEGATIVE, on one open MINOR (F1, lenses `Tests` and `Docs`).

The product change itself checks out:
- The builder refuses at generation, before any write, naming both figures.
- The capacity is declared once, in `KL_nvm_backend.sv:247`, and the builder derives it from that declaration rather than copying it.
- The RTL guard gives identical results at base and head, and the netlist is unchanged.
- Gate 38 and gate 24a hold.
- The five tracked configurations are byte-identical.
- The #649 page tables reproduce independently from #649's published inputs.

The defect is in the `syn/resmap` self-tests. Ruling item 2 asks the `shapes` step to be fail-closed, and the PR body says that property has self-test arms. It has none: the comparison can be removed with every self-test still green.

## Findings

### F1: MINOR (`Tests`, `Docs`): the `shapes` step's fail-closed comparison and the `by_builder` producer are held by no self-test

**Where:** `syn/resmap/yosys_sweep.py:366` (`failures += outcome != expected`) and `syn/resmap/resmap_models.py:391` (`result["guards"]["by_builder"] = builder`). Also the PR #660 body, `syn/resmap/` row: "...any outcome the plan does not expect (a crash, an unexpected refusal, an expected refusal that builds) fails the step ... Self-test arms for each."

**Authority:**
- Ruling item 2 (#652 thread): the `shapes` step records a builder refusal "fail-closed".
- Ruling item 4: the resmap self-tests are among the gates.
- AGENTS.md section 6, `Tests` lens: "Each new test can fail for the defect it claims to detect."

**Evidence** (receipts `resmap_mutations.txt`, `mut_*.log`, `shapes_*.log`): I planted 12 defects in memory, never touching the clone.
- Ten turned their self-test red: r1, r2, r4 to r10, and r12.
- r3 survived. It replaces line 366 with `failures += outcome == "failed"`, and `yosys_sweep.py --selftest` still passes (0 problems).
- I then ran the real `shapes` step two ways:

| Plan given to `shapes` | Head code | With r3 planted |
|---|---|---|
| Plan with the two `expect: refused` marks removed (`plan-nomarks.json`) | rc 1 (correct) | rc 0 |
| Plan expecting the 2x2 to be refused (`plan-2x2-refused.json`) | rc 1 (correct) | rc 0 |

  The step even prints its own "where the plan expects" surprise line and still exits 0.
- r11 also survived: dropping `guards.by_builder` leaves `resmap_models.py --selftest` green. The `resmap_tables` self-test only feeds `refusal_table()` a hand-made `by_builder`, so nothing ties the producer to the consumer.
- The head's behaviour is correct (rc 1 in both cases above). The gap is that no repository gate holds it. The author's controls for it were one-off manual runs.
- The executor's self-test arms do cover the outcome classifier (`builder_outcome`), `run`, `summary` and `builder_refusal`. Of the three outcomes the PR body says fail the step, only "a crash" is held, because the classifier calls it `failed`. "An unexpected refusal" and "an expected refusal that builds" are not held.

**Impact:**
- A later edit can turn the `shapes` step back into one that accepts any builder outcome, for example a newly over-capacity variant the plan expects to build, or a 235-name variant that starts building. Every gate stays green, and the resmap pipeline then prices or drops points silently.
- If the `by_builder` producer regresses, the regenerated refusals table labels builder refusals "elaboration guard". The only thing that would notice is a page re-derivation from #649's off-tree inputs.
- The PR body's "Self-test arms for each" overstates the evidence a cold reviewer is given.

**Required outcome:**
1. A `yosys_sweep.py --selftest` arm (synthetic, no export needed) that turns red when the `shapes` step does not fail on an unexpected refusal and on an expected refusal that builds. It must also pass when every outcome is the expected one.
2. A `resmap_models.py --selftest` arm that turns red when `build()`'s `guards` stops naming a builder-refused point in `by_builder`, or an equivalent end-to-end arm through `refusal_table`.
3. The PR body's claim matching what the arms hold.

**Verification:**
- Re-plant r3 (`failures += outcome != expected` -> `failures += outcome == "failed"`) and r11 (`result["guards"]["by_builder"] = builder` -> `pass`) with `scripts/mutate_module.py`. Each self-test must go red.
- The unmutated self-tests must stay green.

## Suggestions (non-blocking, do not affect coverage)

**S1 (`Conformance`, `Docs`), `scripts/nvm_contract.py:164` `"NAME": (0x80, 128)`: the requested judgment.** I judge this NOT a mirror the acceptance forbids:
- Acceptance 1 and the lane comment govern the limit `sw/builder` refuses by. The builder holds no copy: probe b3 replaced its read with a literal 128, and gate 38 went red.
- `nvm_contract.ALLOC` predates #652. It is the record-space gate's own statement of the section 4.2 design contract, i.e. a verification oracle and not a generator.
- A change to `N_NAME_MAX_C` already turns gate 38's pinned `_NAME_BLOCK_RECORDS` red (probe b6).

There is one residual drift path. Check 14 compares the design page's "block 128" against `ALLOC`, not against the RTL (probe c3). So a capacity change that edits the RTL and gate 38's pin but not `ALLOC` would leave the page and check 3 at 128, with every gate green. Suggested: one assertion in `check_nvm_record_space.py` that `ALLOC["NAME"][1]` equals the builder's `nvm_name_capacity()`. That ties the oracle to the same declaration.

**S2 (`Robustness`), `syn/resmap/yosys_sweep.py:366`:** `"expect": "refused"` is satisfied by any single `CONFIG ERROR:` line. If the 235-name variants later fail for an unrelated schema reason, they stay "refused as expected". The refusal line is recorded and shown on the page, so this is visible but not gated. Optionally record an expected refusal substring (for example "writable names") in the plan.

**S3 (`RTL`), `hdl/milan/KL_nvm_backend.sv:247`:** `N_NAME_MAX_C = 128` and `ID_NAME_C = 'h80` together fill the 8-bit id space, but no check ties them. The PR body already lists this. An elaboration-time `ID_NAME_C + N_NAME_MAX_C == 256` guard would close it without changing the decimal declaration the builder reads.

## Per-lens results (clean lenses in findings format)

```text
[R478] PASS Conformance - hdl/milan/KL_nvm_backend.sv:247,293-295; sw/builder/endstation_builder.py:2691-2749,3191,5745-5760,5911-5917; receipts focused_head.log, cli_235.log, byte_identity.log, resmap_shapes.log, reproduce_649_tables.log, models_base_vs_head.txt - checked against #652 acceptance 1-3, the lane comment and ruling items 1-3:
  - The capacity is one declaration, which the guard and the builder both read.
  - The refusal sits inside the write-free derivation pass, which runs before every write.
  - The CLI refuses 235 with rc 1 and one line naming 235, 128 and the declaration path:line; no outdir is created and the tracked tree is unchanged.
  - 128 builds; 129 and 235 are refused.
  - All five tracked configurations give 50 artifacts each, byte-identical at base and head (diff -r and sha256 lists).
  - The shapes step at head gives 7 built and 2 refused as expected; the 2x2-refused and no-marks plans give rc 1.
  - From #649's published inputs, the head page equals a fresh generation. Only datapath-marginals and guard-refusals changed (24 of 26 tables are byte-identical). Every model key other than the two refused points' marginals and guard entries is identical.
  - Section 4.2 figures (39/107, 54/164, 0xA6/0xEA) are the derived ones.
[R478] PASS RTL - hdl/milan/KL_nvm_backend.sv:240-247,293-295 at head vs base; receipts guard_parity.log, rtl_equiv_stat.log - pinned Verilator 5.050 (wrapper sha256 905795b9..., reports 5.050):
  - Lint-only -Wall at N_NAME_P 0/1/99/128/129/235 gives the same rc and the same g_refuse_names message at base and head (0, 129 and 235 refused; 1, 99 and 128 clean). No new lint warning appears at 128.
  - The sv2v v0.0.13 to Yosys 0.66 proc/opt statistics are byte-identical at base and head for N_NAME_P 99 and 128.
  - The new localparam is int unsigned, the same type and signedness as N_NAME_P. No port, parameter, default or register changed.
[R478] PASS Robustness - sw/builder/endstation_builder.py:2696-2713 (reader), syn/resmap/yosys_sweep.py:326-382 (outcome, builder_refusal), check_nvm_record_space.py:666-735; receipts probe_b*.log, mut_r1..r10,r12, page_c*.out - checked:
  - The reader refuses a commented-out, hex, or repeated declaration (gate 38 controls), and a block-comment copy counts as a second hit, so it is fail-closed.
  - An off-by-one (>=), a literal capacity, a refusal with no figure, and a guard on a literal are each caught (b2-b5).
  - A traceback, a usage exit, an exit with no refusal line, two refusal lines, or a missing outcome is never read as a refusal or a build (r1, r2, r6, r8).
  - Run never prices, and summary refuses a priced receipt for, a refused point (r4, r5).
  - Check 14 catches a stale record total, highest id, block, per-group count and a dropped row (c1-c5); the unedited page stays clean (c6).
  - S2 is recorded as a suggestion.
[R478] UNCLEAN Tests - F1 open (syn/resmap/yosys_sweep.py:366, resmap_models.py:391). Covered and found sound in the same round:
  - Gate 38 passes at head with its RTL arm run under pinned Verilator 5.050 (9/9 controls). Gate 24a passes ((d) 2/2 and (e) 2/2 controls).
  - Six builder/RTL mutants (b1-b6) each turn gate 38 red for the intended reason. b1 also reddens 24a.
  - The record-space gate and --self-test (stale_allocation_table among them) give rc 0.
  - The nvm_backend suite gives 751 checks (541+210), 0 failures, with its negative controls red. nvm_cosim gives 465/465 and kills 39/39 mutants.
  - The resmap self-tests (yosys_sweep, resmap_models, resmap_tables, resmap_map, soc_sweep) give rc 0.
[R478] UNCLEAN Docs - F1's PR-body claim. Covered and found sound in the same round:
  - docs/ENDSTATION_BUILDER.md:101-104,754-775,1108-1119: D8 (712 = 8x(16+1+72) clusters matches gate 24a's assertion), the section 1 line and the section 4 rule.
  - docs/design/SAVED_STATE_FASTCONNECT.md:283-311: figures derived and bound by check 14.
  - docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md: prose and the two regenerated tables, reproduced. The historical receipt rows at 1206-1207 are #649 history and are labelled as such.
  - Docs gates: docs_check, gen_toc --check / --check-anchors, check_doc_paths, check_doc_style, check_em_dash --base 6c22d3ca (0 findings over 66 added lines), check_py_idiom and check_sv_idiom all give rc 0.
```

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | RTL declaration and guard; builder reader, refusal and derivation order; CLI refusal; 5-config byte identity; shapes outcomes; #649 page re-derivation; section 4.2 figures | R478-1 | `2f0f59291080aeab934e0d72e124fb448c105e12` |
| RTL | CLEAN | `KL_nvm_backend.sv` base vs head: guard parity at 6 values (pinned Verilator 5.050), netlist statistics at 2 values | R478-1 | `2f0f59291080aeab934e0d72e124fb448c105e12` |
| Robustness | CLEAN | Declaration reader fail-closed paths; builder-outcome classifier; refused-point run/summary paths; check 14 under 5 page edits | R478-1 | `2f0f59291080aeab934e0d72e124fb448c105e12` |
| Tests | UNCLEAN (F1) | Gate 38, gate 24a, record-space gate and self-test, nvm_backend and nvm_cosim suites, resmap self-tests, 6 builder/RTL mutants, 12 resmap mutants | R478-1 | `2f0f59291080aeab934e0d72e124fb448c105e12` |
| Docs | UNCLEAN (F1) | ENDSTATION_BUILDER D8, section 1 and section 4; SAVED_STATE section 4.2; #649 findings page; PR body; docs gates | R478-1 | `2f0f59291080aeab934e0d72e124fb448c105e12` |

## Commands and results (receipts under `receipts/`, scripts under `scripts/`)

Each command ran from scratch exports of base and head (`scripts/export_tree.sh`, pinned submodule gitlinks) unless it is marked as run in the clone.

| Check | Result |
|---|---|
| Gates 38 and 24a: `scripts/run_focused.py` (test_name_count_fits_the_nvm_name_block, test_d8_role_pools), pinned Verilator on PATH | rc 0 |
| `scripts/guard_parity.sh` | Identical base/head verdicts and messages |
| `scripts/byte_identity.sh` | 5/5 configurations rc 0 at both; 50 = 50 files; `diff -r` rc 0; sha256 lists identical |
| `check_nvm_record_space.py` and `--self-test` (scratch repo) | rc 0 / rc 0 |
| `make -j16 -C tb/verilator/nvm_backend` | rc 0 |
| `make -j16 -C tb/verilator/nvm_cosim` | rc 0 |
| `yosys_sweep.py shapes` (run in the clone, work in scratch) | rc 0, 7 built, 2 refused as expected |
| `scripts/shapes_probe.py`, 4 cases | See F1 |
| Resmap self-tests | 5/5 rc 0 |
| `scripts/mutate_module.py`, 12 mutants plus an unmutated control | 10 red, r3 and r11 survive, control green |
| `scripts/probe.sh` b1-b6 | All red for the intended cause |
| `scripts/probe_page.sh` c1-c6 | c1-c5 red, c6 green |
| `scripts/rtl_equiv_stat.sh` | Identical statistics |
| `scripts/reproduce_649_tables.sh` from #649's published inputs (`649-review-evidence` at `113a1fb9`, `review-evidence/649-r2/author/inputs`) | Head and base pages each "every table equals a fresh generation" |
| `scripts/page_tables_diff.py` | 24/26 tables unchanged; datapath-marginals and guard-refusals changed |
| Docs gates (run in the clone) | All rc 0 |
| `receipts/clone_integrity.txt` | HEAD, HEAD tree, index tree = `a094320f...`; no status lines; `ls-files -s` equals `ls-tree -r` (blobs and modes); gitlinks `external` efeb541a, `gptp-processor` 5dce647a, `protocol-processor` 631eeb34, `third_party/verilog-axis` 48ff7a7e; submodule trees clean; ignored bytecode caches removed |

## Real limits

- I did not run the full builder bank (`test_builder.py --require-rv32`), the full Verilator sweep or Yosys portability bank, Vivado, hardware, Docker/act or host act_ci. These were out of scope for this round.
- Gate 38 and gate 24a ran as focused functions, not inside the full bank. Gate 11's Arty `mf48` arm, and the bank's other gates, were not exercised by me.
- I reproduced the #649 page re-derivation by applying the head `summary` command's documented rule for builder-refused points to #649's published `summary.json`, using this round's own `shapes` outcomes. I did not re-price any point or re-run #649's Yosys or Vivado steps.
- I ran no Vivado elaboration of the changed `$error` format string (`%0d` with a localparam argument). Verilator and sv2v/Yosys accept it.
- Physical calibration was NOT RUN, and field skips are not hardware proof.
- Hosted snapshot at 2026-10-04T21:36Z, exact head: success for rtl-fast, changes, full-ci-gate, verilator-lint, yosys-elaboration, Yosys shards 0-3/4, Verilator shard 3/5, bdd-conformance, wire-accountability and docs-check-no-git. In progress: docs-check, elaborate, and Verilator shards 0, 1, 2 and 4/5. Skipped: Physical gPTP (nightly/manual), which is not an executed job. I made no hosted acceptance judgment.

## Pending manager duties

- Carry F1 to the executor. Re-review is needed at the corrected head for `Tests` and `Docs`. If the fix touches only `syn/resmap` self-tests and the PR body, `Conformance`, `RTL` and `Robustness` stay covered at this head as an ancestor, provided nothing in their scope changes.
- Hosted acceptance on the exact head, including the in-progress contexts, and the act-first local replica.
- The final current-`dev` candidate merge build and validation, and post-merge containment.
- The external review (R479) and the merge authorization, which stay with the maintainer.
- Optionally route S1-S3.

R478-1 FINISHED
