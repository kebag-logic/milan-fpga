[R604] NEGATIVE - exact head ef86ea848dbfb0d869108a1987accb203a17474d

# R604-1 internal independent review: processor PR #175 (issue #151)

- PR #175, head `ef86ea848dbfb0d869108a1987accb203a17474d`, tree `544a270ded252e41a8eccb89c3f4d367b7780722`, three commits on main `2cbed0a987c1e68402658d69459ab7e5aa571adc`.
- Scratch parent: `kebag-logic/milan-fpga` dev `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`.
- Review start: PR #175 comment 6105258016.
- Reconstructed in the brief's order, from these sources:
  - the repository's own rules (`README.md`, `hdl/README.md`, `docs/guides/hdl-engineer.md`, `docs/architecture/09_verification.md`). This repository has no `AGENTS.md` or `CONTRIBUTING.md`;
  - the issue body and the lane scope comment (6098621173);
  - the diff `2cbed0a9..ef86ea84` and its history;
  - the author's published executable evidence under `review-evidence/pp151-r1/author/evidence` at milan-fpga `bda25e67`. I read only the logs, not the hand-off notes.
- Prior public review findings on this PR: **none exist**. At review time the PR had 0 reviews, 0 review comments and one start comment, so nothing needs resolving or carrying forward.

## Verdict

**NEGATIVE.** The core change is correct and I reproduced it independently:

- all 31 guards are module-scope `$fatal`, and no condition changed;
- each guard is refused as a fatal, at its own line, by Verilator lint, sv2v 0.0.12 and 0.0.13 with Yosys 0.66, xelab, and `synth_design`;
- passing elaborations are unchanged;
- the scratch parent shows no shipping shape tripping a guard.

Two MINOR findings remain open, so the verdict is NEGATIVE:

- **F1:** one guard's "nearest passing case" is not the nearest, and a boundary mutant survives the bench.
- **F2:** the integrator guide and its contract figure still say the guards raise `$error`.

## Findings

### F1 - MINOR - Tests, Docs, Conformance: `gen_g_size` is not graded at its nearest passing case, and a tightened guard survives

- **Where:**
  - `tb/elab_guards/guards.py:120-122` grades `KL_aecp_resp_buf.gen_g_size` (condition `RESP_BYTES_P <= 16`, `hdl/aecp/KL_aecp_resp_buf.sv:196`) with violating 16 and passing **24**.
  - The claims this contradicts:
    - `tb/elab_guards/guards.py:77`: "The passing case is the nearest set that lints clean";
    - `tb/elab_guards/README.md:55`: the same sentence;
    - `docs/guides/hdl-engineer.md:67`: "Every guard has a violating case and its nearest passing case";
    - the PR body's guard table, row 19.
- **Authority:**
  - The lane scope's proof item: "the nearest passing set elaborates".
  - The issue's acceptance: "A bench grades each guard's severity".
  - The bench's own stated rule, quoted above.
- **Evidence** (`receipts/gsize_probes.log`, script `scripts/gsize_probes.sh`; `receipts/nearest_passing_probe.log`):
  - At the head, `RESP_BYTES_P` = 17, 20 and 23 lint clean with `scripts/lint_hdl.sh`'s flags (rc 0, no diagnostic).
  - 17 also elaborates under sv2v 0.0.12 + Yosys 0.66 and under sv2v 0.0.13 + Yosys 0.66 (rc 0).
  - A mutant that moves the guard's boundary to `RESP_BYTES_P <= 23` passes the bench: `--only KL_aecp_resp_buf.gen_g_size` reports `elab guards: 35 checks: 35 PASS, 0 FAIL`, rc 0. That guard wrongly refuses the legal values 17 to 23 (lint of 17 in the mutant tree prints `%Warning-USERFATAL ... RESP_BYTES_P=17 leaves no payload above the header record`).
  - The bench's own `bench:tightened` arm proves this class only for `KL_pp_originator`.
  - I checked the other 30 guards against their conditions; each passing case is the nearest one that elaborates clean. The three deadline guards at 2 are justified: at 1 they draw `%Warning-UNSIGNED` (`receipts/nearest_passing_probe.log`).
- **Impact:** For one of 31 guards, the passing side of the boundary is unpinned. A regression that tightens the guard would ship green. A published claim (bench, guide, PR table) is false for that row.
- **Required outcome:** Grade `gen_g_size` at `RESP_BYTES_P=17`, with its passing case elaborating in all four front ends. Alternatively, record a measured reason why 17 to 23 are not legal, without changing the guard's condition in this PR. Then show a tightened-boundary mutant of this guard killed by name.
- **Verification:** Re-run `scripts/gsize_probes.sh` against the fixed head. Step 3's bench run must exit non-zero with a `FAIL: ELAB ... KL_aecp_resp_buf.gen_g_size RESP_BYTES_P=17` line. `make -C tb/elab_guards` and `make vivado` must stay at 0 FAIL.

### F2 - MINOR - Docs, Conformance: the integrator contract still says the guards raise `$error`

- **Where:**
  - `docs/guides/integrator.md:114`: "exceeding either raises `$error` rather than silently aliasing a timer slot".
  - `docs/diagrams/21-integration-faces.svg:53`, a hand-authored figure: "An over-large stream shape stops the build with $error."
- **Authority:**
  - `README.md` ("Every diagram is drawn against the landed RTL").
  - This PR's own rule, `hdl/README.md` rule 6 and `docs/guides/hdl-engineer.md` §2.1.
  - The guards at `hdl/top/protocol_processor_top.sv:876-911` are `$fatal(1, ...)` at this head.
- **Evidence:** `git grep` at the head. The PR body lists both under "Outside this PR's scope and left as they are". But this PR is what made them false, and the lane scope excludes no documentation.
- **Impact:** The integrator-facing contract and its figure name the task this PR removed. That is exactly the task the PR's own measurement shows sv2v 0.0.13 + Yosys builds through. An integrator reading them gets the wrong stop guarantee.
- **Required outcome:**
  - Both places name `$fatal`, for example "stops elaboration with a `$fatal` in every front end (HDL engineer guide §2.1)".
  - The figure stays a valid hand-authored SVG.
- **Verification:**
  - `git grep -n '\$error' docs/guides/integrator.md docs/diagrams/21-integration-faces.svg` prints nothing.
  - `make check` stays rc 0 (figures, links, params).

### R1 - RESIDUE - Docs: "Verilator reports all four tasks as warnings" is wrong for `$info`

- **Where:**
  - `docs/guides/hdl-engineer.md:91`: "Verilator reports all four tasks as warnings";
  - `tb/elab_guards/README.md:5`: "Verilator lint reports all four as warnings";
  - `tb/elab_guards/guards.py:8` (docstring): "Verilator lint reports every severity as a warning".
- **Evidence:** `receipts/probe_forms.log`. A violating module-scope `$info` prints an `-Info:` note and lint exits 0. The guide's own table row ("module scope `$info` ... **elaborates**") is correct. Only the prose overgeneralises; no measurement, test, figure or code behaviour changes.
- **Exact fix:** In all three places, replace the clause with: "Verilator reports `$fatal`, `$error` and `$warning` as warnings (`USERFATAL`, `USERERROR`, `USERWARN`) and `$info` as an `-Info` note that does not fail the lint".

### S1 - SUGGESTION - Tests: run the bench's Yosys leg in the hosted job that has sv2v and Yosys

- The PR body states it and I confirmed it in `.github/workflows/hdl.yml`:
  - the hosted `suites` job has no sv2v or Yosys, so `tb/elab_guards` runs its Verilator leg only;
  - the `portability` job, which installs the latest sv2v (the toolchain that caused #151), runs `syn/yosys/run.sh` only, at default shapes where no guard fires.
- The Verilator leg alone kills every `$error`, `$warning` and `initial` arm (`receipts/head_mutants_sv2v12.log`, `head_mutants_sv2v13.log`), so hosted regression coverage of the class holds.
- Adding `make -C tb/elab_guards` to `portability` would grade the guards against each new sv2v release as it ships. This does not affect the verdict.

## What was checked, by lens

### Conformance (issue #151 acceptance and lane scope)

- **Inventory.** I repeated the search myself: every `$fatal`, `$error`, `$warning`, `$info`, `$finish`, `$stop`, `assert` and `initial` under `hdl/`, all file types. It finds exactly 31 elaboration severity tasks in 13 files, every one a module-scope `if (...) begin : <label> $fatal(1, ...); end`:

  | File | Line(s) |
  |---|---|
  | `KL_acmp_nvm_shadow` | :538, :545 |
  | `KL_pp_acmp_listener` | :347 |
  | `KL_aecp_desc_store` | :263, :267, :270, :273 |
  | `KL_aecp_engine` | :944, :949, :964, :968, :972 |
  | `KL_aecp_notify` | :367 |
  | `KL_aecp_nvm_writer` | :315, :318, :322, :326 |
  | `KL_aecp_resp_buf` | :194, :197, :201 |
  | `KL_aecp_ucpu` | :297 |
  | `KL_pp_nvm_port` | :189, :198 |
  | `KL_pp_originator` | :149 |
  | `KL_pp_release_merge` | :38 |
  | `KL_srp_encoder` | :148 |
  | `protocol_processor_top` | :876, :880, :884, :897, :911 |

  The two `initial $readmemh` and `KL_aecp_notify.sv:674`'s memory-clear `initial` are not guards. The inventory matches the PR's table and the bench's `GUARDS`.
- **No guard changes its condition.** Of the 32 changed RTL lines, 29 are exactly `$error(` → `$fatal(1, ` with nothing else changed (checked mechanically). The listener's three lines move `if (STRM_TIMEOUT_CYC_P == 0) $fatal(...)` from `initial begin : parameter_checks` to `begin : g_strm_tmo_check`, keeping the same condition and message. Every changed RTL file keeps its line count.
- **The recorded rule is measured.** I built my own one-guard probe (`scripts/probe_forms.sh`, `scripts/vivado_probe_forms.sh`; sources in `receipts/probe_sources/`). It covers four tasks × {module scope, `initial`} × {violating, passing} through five front ends: Verilator 5.050 lint, sv2v 0.0.12 + Yosys 0.66, sv2v 0.0.13 + Yosys 0.66, Vivado 2026.1 xelab, and `synth_design -rtl`. It reproduces every cell of the five-row table in `docs/guides/hdl-engineer.md` §2.1 (`receipts/probe_forms.log`, `probe_forms_vivado.log`, `probe_forms_vivado_synth_words.log`):
  - module-scope `$fatal` is refused in all five;
  - module-scope `$error` elaborates only under sv2v 0.0.13;
  - `$warning` elaborates everywhere except Verilator;
  - `$info` elaborates everywhere;
  - an `initial` `$fatal` elaborates in Verilator and xelab.

  I also confirmed the lowering the guide describes (sv2v 0.0.13: `$fatal` becomes `initial $display; $finish(1)`, `$error` becomes `initial $display`) and the issue-premise correction: under sv2v 0.0.12 Yosys refuses `$error`.
- **Per guard, per front end, violating refused in the front end's own words, nearest passing elaborates.**
  - At the head: 155/155 under sv2v 0.0.12 and 155/155 under 0.0.13 (Verilator + Yosys, `receipts/head_guards_sv2v12.log`, `head_guards_sv2v13.log`), and 155/155 for xelab + `synth_design` (`receipts/head_guards_vivado.log`). Each line quotes the tool: `%Warning-USERFATAL <file>:<line>`, `ERROR: FATAL: .`, ``System task `$finish' executed``, `[VRFC 10-8279] $fatal`, `[Synth 8-6058]`.
  - At base, with the head's bench: 62 of 156 fail under each sv2v (30 Verilator, 30 Yosys, 2 inventory), as the PR states.
  - My head and base bench lines equal the author's published logs line for line (sorted). The one exception to "nearest" is F1.
- **Scratch parent at dev ac2c5e77**, with the gitlink set to base `2cbed0a9` and to head `ef86ea84`:
  - `scripts/lint_rtl.py --check --self-test`: `LINT GATE: PASS (90 violation(s) <= ratchet 90 ...)` at both, logs identical.
  - `syn/yosys/run.sh --mode elaborate`: `tops: 58 pass: 58 fail: 0` at both, identical with timings masked.
  - `milan_datapath` linted directly at each of the five shipping configs (`endstation_arty_current` 1, `endstation_arty_4x4` 4, `endstation_arty_8ch` 4, `endstation_ax7101_1x1_tdm8` 1, `endstation_ax7101_8x8` 8 streams; generated shape directory first; 50 MHz) prints **0 `USER*` diagnostics**, identical at base and head. Verilator's rc 1 there is the parent's ratcheted lint debt (`Exiting due to N warning(s)`), not a guard.
  - **No shipping shape trips a guard** (`receipts/parent_*`).

### RTL

- The 13 RTL files changed only as described above.
- `scripts/lint_hdl.sh`: rc 0, 41 `LINT OK`, identical at base and head.
- **Netlist identity** (`scripts/netlists.sh`, `scripts/netlist_compare.sh`, `receipts/netlist_identity.txt`), with sv2v 0.0.12 + Yosys 0.66 and `read_verilog -defer; hierarchy -check -top; proc; opt_clean; stat; write_verilog -noattr`. It covers every `syn/yosys/run.sh` top at its defaults (42) and `protocol_processor_top` at 1x1, 2x2, 4x4, 8x8, 16x16, 1x8, 8x1 and `N_AVB_IF_P=2`, 50 cases in all:
  - 46 are byte-identical after masking `all.v` line numbers and Yosys `$N` indices;
  - 4 (`protocol_processor_top` at defaults, 1x1, 8x1, 8x8) are identical once `write_verilog`'s own `_NNNN_` wire numbers are also masked. The base's numbering is offset by one, consistent with the listener's former `initial` block;
  - all 50 `stat` cell and wire counts are identical.
- **ROM images** at base and head: `ucode.hex` `518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8`, `ltn_rom.hex` `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956`. These are identical, and equal the parent's `syn/yosys/rom_digests.tsv` row for its current pin `2ad2f845`.

### Robustness (fault and mutation probes)

- **Two or more independent mutants re-applied.** I built five reviewer mutants, each in its own scratch copy (`scripts/my_mutants.py`, `receipts/reviewer_mutants.log`). Each was graded by the bench and, separately, by direct tool runs:
  - **R1:** `KL_srp_encoder.g_depth_check` as `$error`. Direct: Verilator `USERERROR`; sv2v 0.0.12 Yosys `ERROR: <message>`; sv2v 0.0.13 Yosys **elaborates** (the #151 failure, reproduced on a real guard).
  - **R2:** `KL_aecp_ucpu.gen_g_d8_cap` as `$warning`. Direct: Yosys elaborates under both.
  - **R3:** `KL_pp_release_merge.g_slot_count_check` in the old listener form, `initial begin : <label> if (...) $fatal(...); end`. This is a different shape from the bench's own `initial if` arm. Direct: Verilator is not refused by the guard; Yosys refuses under both sv2v.
  - **R4:** `KL_aecp_nvm_writer.g_rs_agg_check` as `$info`. Direct: elaborates everywhere.
  - **R5:** `protocol_processor_top.gen_g_owner_overlap` as `$error`.

  The bench kills all five by name under both sv2v. R1 (`[XSIM 43-4462]`), R2 and R3 (xelab builds) are also killed by name in the Vivado legs (`receipts/reviewer_mutant_vivado_*.log`).
- **The author's campaign, re-run** (`make mutants` equivalent): control PASS and `98 of 98 killed` under sv2v 0.0.12 (659 s) and under 0.0.13 (613 s). Under 0.0.12 the `initial` arms are killed by both legs; under 0.0.13 by Verilator alone, as the README records.
- **Base fault confirmed and fixed** (`receipts/base_nvm_elab_sv2v12.log`): at base with the pinned sv2v 0.0.12, `make -C tb/nvm_port elab` fails (`YOSYS FAIL MAX_PAYLOAD_P=65528 failed, but not at the guard's $finish`). At the head it passes under both sv2v, and now grades the deadline guard's Yosys leg too.
- The bench's own robustness held:
  - its inventory fails an unlisted or deleted guard (the campaign's `bench:unlisted` and `bench:deleted` arms);
  - `--only` rejects an unknown name (rc 2) and the mutation driver refuses an existing output directory (rc 2), both run (`receipts/bench_self_checks.log`);
  - planted shapes are applied exactly once (checked by reading the code).

### Tests

- The new suite has the gaps in F1 and S1 and is otherwise sound:
  - it grades class, line and words per guard, plus an inventory;
  - its tally line is read by `scripts/run_suites.sh`.
- Changed benches:
  - `make -C tb/pp_top line-guards if-guards` passes at base (`USERERROR` expected) and at head (`USERFATAL`).
  - All **298** patches under `tb/` apply at the head (`receipts/head_patches_apply.log`), including the five whose context lines this PR updated.
- Gates:
  - `make check` rc 0 at base and head; the only differences are `links: 1187` → `1191` and `ids: 563 files` → `567`, the PR's added links and files.
  - `python3 scripts/gen_matrix.py --check` rc 0, 94 rows, 0 untested, at both.
- Hosted evidence at the exact head (snapshot `receipts/hosted_checks_snapshot.txt`): `docs-gates` and `portability` completed successfully in two runs; `suites` was **in progress** and is not counted here.

### Docs

- These read correctly against the measurement:
  - `hdl/README.md` rule 6;
  - `docs/guides/hdl-engineer.md` §2 row and §2.1;
  - `tb/elab_guards/README.md`;
  - the updated `tb/nvm_port/README.md`, `tb/nvm_port/elab_bounds.sh` header, `tb/pp_top/README.md`, `if_guards.py` and `line_guards.py` docstrings;
  - the new `KL_pp_acmp_listener.sv:345` comment, and `KL_pp_nvm_port.sv:194`'s "listener's precedent at module scope", which this PR makes true.
- Exceptions: F1 (the nearest-case claims), F2 (the integrator guide and figure), and R1 (wording).
- `docs/architecture/09_verification.md` §8 deliberately globs suites rather than listing them, so the missing `tb/elab_guards` row the PR body mentions is not a defect.

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | issue #151 body and lane scope; 31-guard inventory; probe table in 5 front ends; bench at head and base in 4 front ends; scratch parent at dev `ac2c5e77` (lint gate, 58-top elaboration, 5 shipping shapes) | R604-1 | `ef86ea848dbfb0d869108a1987accb203a17474d` |
| RTL | CLEAN | 13 changed `hdl/` files (condition identity, scope, line counts); `lint_hdl.sh` base/head; 50 Yosys netlists base/head; ROM digests | R604-1 | `ef86ea848dbfb0d869108a1987accb203a17474d` |
| Robustness | CLEAN | 5 reviewer mutants (bench + direct tools, 3 also in Vivado); author campaign 98/98 under each sv2v; base `elab_bounds.sh` fault and head fix; bench self-checks | R604-1 | `ef86ea848dbfb0d869108a1987accb203a17474d` |
| Tests | UNCLEAN (F1) | `tb/elab_guards` (`guards.py`, `mutants.py`, Makefile, README); `tb/nvm_port elab`; `tb/pp_top line-guards if-guards`; 298 patches; `make check`; `gen_matrix --check`; hosted check-runs snapshot | R604-1 | `ef86ea848dbfb0d869108a1987accb203a17474d` |
| Docs | UNCLEAN (F1, F2; R1 residue) | `hdl/README.md`; `docs/guides/hdl-engineer.md` §2/§2.1; `docs/guides/integrator.md`; `docs/diagrams/21-integration-faces.svg`; `docs/architecture/09_verification.md`; changed tb READMEs and docstrings; PR body | R604-1 | `ef86ea848dbfb0d869108a1987accb203a17474d` |

## Real limits

- I ran focused gates only. Whole `./scripts/run_suites.sh`, whole `syn/yosys/run.sh`, and the 15 base/head campaigns in the PR body were not re-run; for those I rely on the author's published receipts and the hosted jobs.
- The Vivado out-of-context netlist identity (`syn/ooc`) was not re-run. My netlist identity is Yosys-only: 50 cases, 4 of them identical up to Yosys's own wire numbering.
- The scratch parent is at dev `ac2c5e77`, whose recorded processor pin is `2ad2f845`. The author's parent receipts are at `e8454e27`.
  - I set the gitlink to base and to head without the pp170 consumer patch. Results are identical at both.
  - Parent checks were the lint gate, the `--mode elaborate` Yosys run and a direct shipping-shape lint. They are not donor or consumer banks.
- The apt-packaged Yosys in the hosted `portability` job was not measured; only the pinned Yosys 0.66.
- No manager source bank exists or is claimed at this head. Physical calibration NOT RUN; no hardware; no field evidence.

## Pending manager duties

- Merge-turn current-dev candidate validation (builder and native banks) and the donor + consumer banks (consumer with the pp170 parent-name-evidence patch). Link the receipts on the PR.
- The hosted `suites` job at this head was still in progress at snapshot time. Accepting it, and hosted/act acceptance generally, is the manager's call.
- **Parent follow-up, outside this PR.** I reproduced the author's report (`receipts/parent_head_lint_hole.log`):
  - The parent's `scripts/lint_rtl.py` `lint_one` reports `0 hard error(s)` for `KL_pp_shadow` at `-GN_STREAM_IN_P=40`.
  - Meanwhile Verilator prints `%Warning-USERFATAL` from `protocol_processor_top.sv:911` and `KL_aecp_nvm_writer.sv:315`.
  - The parent's own guard `hdl/milan/KL_nvm_backend.sv:285` is still a `$error` (`USERERROR`). This PR's measured rule says sv2v 0.0.13 + Yosys builds through that.
  - Both need a parent-side issue.
- Carry R1 to the residue checklist.

## Integrity

- After all probes, `$REVIEWS/r604-1-pp151` is unchanged (`receipts/clone_integrity.txt`):
  - HEAD `ef86ea84`, tree `544a270d`, and `git write-tree` equals the tree;
  - empty `status --porcelain --ignored`;
  - every tracked file's bytes equal its HEAD blob, and every index mode equals the HEAD mode;
  - this repository has no gitlinks.
- All runs used copies under `scratch/`.
- Tool identities: `receipts/tool_identity.txt`. The pinned Verilator 5.050 was verified by version and sha256.

R604-1 FINISHED
