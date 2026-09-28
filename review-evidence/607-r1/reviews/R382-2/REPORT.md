[R382] NEGATIVE - exact head f3bd6b6694ab61b8f70b7f13f1049a14a6fb3461

# R382-2 internal independent review: issue #607 / PR #615

- Role: internal independent reviewer, cleared context, own detached clone.
- Exact head: `f3bd6b6694ab61b8f70b7f13f1049a14a6fb3461`, tree `1cc73e0e1327694bc4f9def1968ca4237aa4652b`.
- Source base: `54ce877371ee6e8878cf67294e86c2a8481b62f6`.
- Delta under review: `350af5dc..f3bd6b66`, two commits:
  - `7f2630848` "Test shipping clock hooks and quarantine rejected bitstreams"
  - `f3bd6b669` "Keep clock constraint guidance within documentation style limits"
  - Both have one-line subjects with no body or trailers.
- Scope authority:
  - #607 acceptance 1-4;
  - the round-1 assignment (issue comment 5865111793);
  - the round-2 assignment (issue comment 5868277772).
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs. Each has an artifact-specific result in section 5.

**Verdict: NEGATIVE.** One BLOCKER is open: F2 (Conformance, Tests, Robustness).

My round-1 finding F1 is resolved in content. The new arm reads the real shipping build files, and my M07, M16 and call-deletion mutants turn the bank red. Those mutants, and the rest of a 33-mutant campaign, were run with the bench interpreter.

However, the new arm cannot run in the repository's own hosted elaboration environment. At this exact head the required status context `elaborate` fails. The cause is that `pythondata_software_picolibc` is absent there: the arm is the first bank member to drive LiteX's full `Builder.build`, which needs that package. I reproduced the failure locally. The previous head's `elaborate` was green.

`elaborate` is one of the seven contexts the dev merge bar requires. So the round-2 requirement that "the base tree stays green" is not met in the bank as the repository runs it. The hosted bank also stopped at this arm, so none of its later elaboration gates ran at this head.

Round-2 items (2)-(5) are met: the 12-5201 refusal, the bitstream quarantine, the text corrections, and no constraint-text change.

## 1. Reconstruction and method

Read in order:

1. AGENTS.md and CONTRIBUTING.md. That includes the seven required contexts at `CONTRIBUTING.md:55-57`.
2. docs/README.md.
3. Issue #607: body, both assignments, [A420] TAKEN and [A420] REVIEW READY.
4. The delta diff and history `350af5dc..f3bd6b66`, in the context of `54ce8773..f3bd6b66`.
5. Public evidence.
   - `review-evidence/607-r1` at `bae7b082` is round-1 evidence for `350af5dc`.
   - No round-2 evidence tree is published.
   - I used the round-1 `sweep-artifacts.json` and `shipping-inputs.json` indexes to hash-verify the retained sweep and shipping artifacts.
6. Exact-head hosted check runs, read-only.
7. My own round-1 packet, read-only.

I read no author notes and no other reviewer's report before this verdict and ledger were written.

Executable work. Scripts are in `scripts/` and raw output is in `receipts/`. The interpreter is the bench LiteX virtualenv that `sweep.sh` names (`$HOME/litex-milan/venv`). Every probe ran in a disposable copy of the clone under the packet's `scratch/`.

| # | What | Result |
|---|---|---|
| 01 | Bank entry `test_clock_constraints.py` on an unmodified head copy | rc 0. All four shipping elaborations PASS: 1x1 TDM8 and 8x8, each on e1 and e2. Only ignored outputs are left in the copy |
| 02 | Bank wiring | `test_builder.py:27557-27562` runs the entry. `test_clock_constraints.py:270-271` calls the shipping arm unconditionally. `--require-elaboration` refuses a missing interpreter (`test_builder.py:23622`). The hosted step is at `elaborate.yml:260` |
| 03 | `mutation_probe.sh`: 33 mutants against the bank entry | Control green. 31 killed. M19 survives and is equivalent, as in round 1. Round-1 survivors M07 and M08 are now killed |
| 04 | `mutation_probe_shipping_only.sh`: the same 33 mutants against the new arm alone | Kills every wiring, order, clock-list, generic-mask, platform and duplication mutant: M01, M07, M08, M09, M11, M14, M21-M27, M32. Tcl-body and log mutants are out of its scope and killed by the other arms (03) |
| 05 | `m07_elaboration_probe.sh`: real shipping elaboration of both configs for the control, M07 (board guard disabled) and M21 (call deleted inside the guard) | Control: hook 1, interaction report 1, generic `mr_ff` 0, order synth 258 < hook 271 < opt 275, bank PASS. M07 and M21: hook 0, report 0, generic `mr_ff` 1, **bank FAIL** (`shipping Ethernet hook missing or duplicated: []`) |
| 06 | `no_picolibc_probe.sh`: head copy with `pythondata_software_picolibc` shadowed as absent | Bank entry rc 1 with the hosted `ImportError`. The same copy with the package present: rc 0 |
| 07 | `log_gate_probe.py`: exact-head gate on hash-verified copies of real logs, each next to a decoy `.bit` | Shipping log: REFUSED, 14 findings (10 x 12-4739, 2 x 20-1307, 2 x 12-5201); decoy renamed `.bit.rejected`. Three sweep logs: ACCEPTED, `.bit` kept. Synthetic 12-5201 at WARNING, CRITICAL WARNING and ERROR: refused; at INFO: accepted |
| 08 | `regen_compare.sh`: generated `alinx_ax7101.{tcl,xdc,v}` at `350af5dc` versus `f3bd6b66`, both configs | Tcl and XDC byte-identical after path normalisation. The `.v` differs only in the LiteX header comment (blackbox listing order and the date stamp) |
| 09 | `verify_sweep_artifacts.py` plus the shipping-input hashes | 117/117 sweep artifacts match. 5/5 shipping inputs match |
| 10 | Focused documentation and policy gates | 7 rc 0; 0 added-line em dashes. The em-dash and TOC tools could not run: the pinned renderer is absent and installs are not permitted |
| 11 | Committed live wrong-name control against the read-only shipping checkpoint, 16 threads | rc 0. Vendor process rc 0 and emitted 3 x 12-4739, 1 x 12-5201, 1 x 20-1307. The gate refused. Checkpoint sha256 unchanged and equal to the public index |
| 12 | `git merge-tree` of this head with live dev `7a7582f0`, #612 `be6b48c1` and #605 `895be307` | dev: clean, tree `9e1b386c`. #612: clean. #605: conflicts in BUILDING.md, test_builder.py and alinx_ax7101.py, the same set as round 1 |
| 13 | Clone integrity after all probes | HEAD, index tree `1cc73e0e` and 946 tracked blobs/modes are equal. Gitlinks gptp-processor, protocol-processor and verilog-axis are equal. `external` was uninitialised, as at the start |
| 14 | Exact-head hosted check runs, snapshot | **`elaborate` failure.** `rtl-fast` success. `docs-check` and three Verilator shards still in progress. Previous head `350af5dc`: `elaborate` success |
| 15 | Hosted `elaborate` failed-step log, excerpt | The bank stops in `test_clock_crossing_constraints`. The shipping subprocess fails with `ImportError: pythondata-software-picolibc module not installed`, raised by `litex/soc/integration/builder.py` `_generate_includes` |

Vendor tool use: one read-only checkpoint session (receipt 11), with `general.maxThreads 16`. There was no implementation run.

## 2. Round-2 items

### (1) F1: committed shipping arm. Content MET, hosted run FAILS (F2)

What the arm does:

- `sw/builder/test_shipping_clock_constraints.py:18-67` runs the real `milan_soc.main()`.
  - It uses the builder-emitted argv of each shipping config, plus `--eth-port`, `--no-compile-software` and `--no-compile-gateware`.
  - It wraps `Builder.build` only to observe it. `XilinxVivadoToolchain.run_script` is patched to fail, so no vendor run is possible.
  - It reads the generated `alinx_ax7101.tcl` and `alinx_ax7101.xdc`.
- It requires:
  - exactly one `milan_eth_constraints eth_clocks<n>_rx` for the configured port (`:48-51`);
  - bounded clocks named from `soc.crg.pll.clkouts[0/1]` through the namespace, independently of the hook's own list (`:40-41`);
  - the hook strictly between `synth_design` and `opt_design` (`:52-54`);
  - no uncommented `mr_ff` line in the XDC (`:55-56`);
  - no `.bit` produced (`:57`).
- `test_shipping_constraints` (`:71-84`) runs both shipping configs on both ports, each in a fresh process.
- Both shipping AX7101 configs in `configs/` are covered: `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8`.

Mutation results:

- Against the bank entry (receipt 03), my round-1 M07 and M16 are both killed, and so is the call-deletion variant M21. So are a guard `and not with_mac` variant (M22), board `arty` (M23), e1-only (M24), a duplicated hook (M25), a missing Milan clock (M26), a hook moved to pre-routing (M27), and the round-1 survivor M08, which now fails on e2.
- The real elaboration probe (receipt 05) shows the regression the arm now catches, on both configs.
- The base tree is green with the bench interpreter (receipt 01).

What fails:

- In the repository's hosted elaboration environment, the arm fails on the unmodified head (receipts 14, 15; reproduced locally in receipt 06). See F2.

### (2) `check_implementation_log` refuses `[Vivado 12-5201]`. MET

- The pattern is at `sw/litex/clock_constraints.py:63-64`.
- On the real shipping log it now reports 14 findings, including both `CRITICAL WARNING: [Vivado 12-5201]` lines (receipt 07).
- Unit arm: `test_clock_constraints.py:174`. Live arm: `:248,253`. I reproduced the live arm (receipt 11).
- Mutant M28, which drops 12-5201, is killed.

### (3) A refused build leaves no bitstream that `deploy.sh` would pick. MET

- On a refused or unreadable log, `clock_constraints.py:72-79` renames every `gateware/*.bit` to `*.bit.rejected` and re-raises.
- Discovery that no longer matches a quarantined file:
  - `deploy.sh:69` discovers `ls -t "$HERE"/*/gateware/alinx_ax7101.bit`;
  - `build.sh flash` discovers `gateware/$bitname` (`build.sh:69-70,99-101`).
- The gate runs before any manifest write (`milan_soc.py:3955-3959`). So a refused build also publishes no `flashboot_layout.json`.
- The platform's `bitstream_commands` (`alinx_ax7101.py:304-310`) write no other flashable image.
- An accepted retry keeps its new `.bit`.
- Covered by `test_clock_constraints.py:163-204` and by mutants M29, M30 and M31, all killed.

### (4) Text corrections. MET

- `sweep.sh:4-8`: compare WNS only among seeds with a successful launch, a `flashboot_layout.json` and an unquarantined `.bit`.
- `docs/litex/CLOCK_DOMAINS.md:346-350`: points to the generated-Tcl hook and to BUILDING section 5. The anchor resolves (`BUILDING.md:33,515`).
- `milan_soc.py:1500-1502`: MII keeps asynchronous groups (true at `:1511-1516`). GMII carries the 8 ns datapath-only bound, and the hook scopes the MultiReg false paths (true at `clock_constraints.tcl:48-71`).
- BUILDING.md and RUNNING_TESTS.md are updated to match, checked line by line in section 5.

### (5) No timing-relevant constraint text changed. MET; the sweep table does not need re-reporting

- The delta does not touch `clock_constraints.tcl`, `configs/` or any generated-constraint path:
  - `alinx_ax7101.py` gains a two-line comment;
  - `milan_soc.py` changes a comment only;
  - `clock_constraints.py` changes only the post-build log gate.
- The regenerated Tcl and XDC are byte-identical between `350af5dc` and `f3bd6b66` for both configs (receipt 08).
- In round 1 I showed that the `350af5dc` regeneration is byte-identical to the retained sweep inputs. The sweep artifacts still hash-match (receipt 09).
- So the round-1 per-seed table still applies:
  - asl: WNS +0.034 ns;
  - eto: WNS +0.268 ns;
  - eppo: WNS +0.105 ns;
  - Ethernet slack against the 8 ns bound: +6.293 / +6.290 / +6.232 ns;
  - no unsafe Ethernet pair.

## 3. Findings

### F2 - BLOCKER - Conformance, Tests, Robustness

**Location.** `sw/builder/test_shipping_clock_constraints.py:38` (`super().build(**kwargs)`), reached from `sw/builder/test_clock_constraints.py:270-271` and `sw/builder/test_builder.py:27557-27562`. Exact-head hosted artifact: check run `elaborate`, run 36418013981, job 108913705616, conclusion `failure`.

**Authority / evidence.**
- `CONTRIBUTING.md:55-57`: the dev merge bar requires the exact status context `elaborate`.
- Round-2 assignment (issue comment 5868277772): a builder-bank arm whose mutants turn it red "and the base tree stays green".
- AGENTS section 6, Tests lens: "Existing regressions remain green". Robustness lens: "configuration-dependent behavior".
- At this head, the hosted `elaborate` job ran `test_builder.py --require-elaboration --require-rv32` and failed (receipts 14, 15).
  - The new arm is the first bank member to run LiteX's full `Builder.build`.
  - `Builder._generate_includes` (`litex/soc/integration/builder.py:301` via `:260`) calls `get_data_mod("software", "picolibc")` even with `--no-compile-software`.
  - The repository's pinned CI install (`sw/litex/litex_pins.txt` and `scripts/ci_litex_env.py`) does not provide `pythondata_software_picolibc`.
- The previous head `350af5dc` passed `elaborate` (receipt 14).
- Reproduced locally (receipt 06): with only that package made unavailable, the bank entry fails on the unmodified head with the same `ImportError`, and passes when it is present.
- The executor's and the local bank's green results come from the bench virtualenv, which carries the package. That explains the difference.

**Impact.**
- A required merge context is red at the exact head, so the PR cannot meet the merge bar.
- The hosted builder bank aborts at this arm. So at this head CI observed none of the later elaboration gates (gates 23f/23g, `test_all_configs_build` and the rest).
- In the only environment the repository defines for CI, the new arm cannot pass on correct code. That leaves the shipping hook guarded only by developer machines that happen to carry an unpinned package.

**Required outcome.**
- The shipping arm runs, and passes on the unmodified head, in the repository's hosted `elaborate` environment. It must not skip there: under `--require-elaboration` a skip would give up the coverage that F1 required.
- Either route is acceptable:
  - the arm stops depending on the software package;
  - the dependency is pinned in the documented CI install. In that case the `litex_pins.txt` install notes must state it.
- The M07, M16 and call-deletion mutants must still turn the bank red.

**Verification.**
- An exact-head hosted `elaborate` success whose log shows the four `[constraints] shipping ... PASS` lines and the bank's final verdict.
- Re-run `mutation_probe.sh` and `m07_elaboration_probe.sh`.
- If the fix removes the dependency, `no_picolibc_probe.sh` returns rc 0.

### Suggestions

None new.

## 4. Round-1 findings (my own) at this head

| ID | Round-1 severity | Status at `f3bd6b66` | Evidence |
|---|---|---|---|
| F1 | MINOR (Tests) | **Resolved in content.** The arm exists in the bank and kills M07, M16 and M21 (plus M22-M27) on real elaborations. Its hosted run is the subject of F2, which is a separate open item | Receipts 03, 04, 05 |
| S1 | SUGGESTION | Taken. 12-5201 is refused | Receipts 07, 11; M28 |
| S2 | SUGGESTION | Taken. `sweep.sh:4-8` and `BUILDING.md:523-525` | Section 2 (4) |
| S3 | SUGGESTION | Declined, with a stated reason, which I verified. LiteX's `XilinxPlatform.__init__` builds the stock toolchain from the name (`litex/build/xilinx/platform.py:39-42`). A guard comment was added at `alinx_ax7101.py:301-302`. The #605 composition hazard is unchanged and is caught by #395's `test_platform_hooks` (round-1 receipt 09) | Receipt 12 |
| S4 | SUGGESTION | Taken. `CLOCK_DOMAINS.md:346-350` | Section 2 (4) |

## 5. Lens results (clean-lens format)

```text
[R382] UNCLEAN Conformance - F2 open. Round-2 items (2)-(5) and #607 acceptance 1-4 are met at f3bd6b66: clock_constraints.py:61-80, milan_soc.py:1500-1502,2733-2735,3955-3959; generated tcl/xdc identical to 350af5dc (receipt 08); 117/117 sweep artifacts (receipt 09). Item (1) "base tree stays green" is not met in the required hosted elaborate context (receipts 14, 15)
[R382] PASS RTL - alinx_ax7101.py:298-310 (the toolchain swap is unchanged, a guard comment added, and the LiteX platform.py:35-53 construction path verified); clock_constraints.tcl unchanged in the delta; regenerated alinx_ax7101.tcl/.xdc byte-identical to 350af5dc for both shipping configs (receipt 08), so the round-1 RTL result (exception precedence, 8.000 bound, hold false paths, retained reset exceptions) still holds; no HDL in the diff
[R382] UNCLEAN Robustness - F2 open (configuration-dependent environment: the arm fails without an unpinned package). Otherwise checked clean: quarantine on refusal and on an unreadable log, an accepted retry, INFO-level non-match, e1/e2 ports (clock_constraints.py:72-79; test_clock_constraints.py:163-204; receipts 03, 07; M29-M31 killed)
[R382] UNCLEAN Tests - F2 open. The arm's detection power is verified: test_shipping_clock_constraints.py:18-84 and test_clock_constraints.py:163-271; 33 mutants, 31 killed plus the equivalent M19 (receipt 03); shipping-arm-only kill set (receipt 04); real-elaboration M07/M21 (receipt 05); live control (receipt 11)
[R382] PASS Docs - BUILDING.md:517-525, CLOCK_DOMAINS.md:346-350 (anchor resolves to BUILDING.md:515), RUNNING_TESTS.md:160-169, sweep.sh:4-8 and milan_soc.py:1500-1502, each checked against the code and receipts 03/07/08; check_doc_style, docs_check, check_doc_paths, check_baremetal_only, check_hygiene, check_py_idiom rc 0; 0 added-line em dashes (receipt 10). F2 is not a Docs defect: the changed docs make no environment claim, and litex_pins.txt's install notes were already silent on this package for full LiteX export before this delta. A fix that pins the package must update those notes
```

## 6. Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2 open) | #607 acceptance 1-4 and round-2 items 1-5 against the diff, regenerated constraints, hash-verified sweep and shipping artifacts, real-log gate, hosted `elaborate` result | R382-2 | `f3bd6b6694ab61b8f70b7f13f1049a14a6fb3461` |
| RTL | CLEAN | `alinx_ax7101.py` swap and comment, LiteX platform construction, unchanged `clock_constraints.tcl`, byte-identical generated Tcl/XDC for both shipping configs | R382-2 | `f3bd6b6694ab61b8f70b7f13f1049a14a6fb3461` |
| Robustness | UNCLEAN (F2 open) | Quarantine paths (refused, unreadable, retry), severity coverage, port coverage, missing-package environment | R382-2 | `f3bd6b6694ab61b8f70b7f13f1049a14a6fb3461` |
| Tests | UNCLEAN (F2 open) | New shipping arm, bank wiring, 33-mutant campaign (bank and arm-only), real-elaboration M07/M21, live control, hosted bank run | R382-2 | `f3bd6b6694ab61b8f70b7f13f1049a14a6fb3461` |
| Docs | CLEAN | BUILDING, CLOCK_DOMAINS, RUNNING_TESTS, `sweep.sh` and `milan_soc.py` comment text; focused doc gates | R382-2 | `f3bd6b6694ab61b8f70b7f13f1049a14a6fb3461` |

A fix for F2 touches the Tests scope (and possibly `sw/litex/` or the CI install). The lenses covering any changed artifact must be re-covered at the new head. If the fix touches only `sw/builder/` or the CI install and leaves the generated constraints unchanged, the RTL and Docs rows stand. The exception is that pinning the package changes `litex_pins.txt`, which is in the Docs scope.

## 7. Real limits and pending manager duties

Limits:
- The prescribed pinned Verilator path (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`) does not exist on this host. The delta has no RTL or HDL change, so no Verilator run was needed or done.
- The em-dash and TOC tools could not run locally, because the pinned Markdown renderer is absent. I checked added lines by hand instead: 0 em dashes. The hosted `docs-check` was still in progress at the snapshot.
- By instruction, I ran no full builder, native, parent, PP, gPTP or Yosys bank and no implementation build.
- Acceptance-4 timing is the round-1 sweep. It is carried forward by byte-identical constraint regeneration and hash verification, and was not re-run.
- Mutants and probes used the bench interpreter. The picolibc-absent reproduction shadows one module; it does not rebuild the hosted environment.
- Static timing only. Physical calibration was NOT RUN, and no hardware or field behaviour is established by this review.

Pending manager duties:
- F2: the hosted `elaborate` context must succeed at the fix head, and the log must show the shipping arm ran.
- At snapshot time, hosted `docs-check` and Verilator shards 1, 2 and 4 were in progress, and `verilator-suites` / `yosys-portability` had not reported. Hosted and act acceptance stays with the manager.
- #605 merge order is unchanged from round 1: keep the toolchain swap before #605's pre-placement hook loop, and union the `test_builder.py` and `BUILDING.md` hunks. Candidate merge validation on live dev `7a7582f0` (merge-tree clean, tree `9e1b386c`) and post-merge containment.
- A second independent positive review is still needed.
- Round-2 public evidence (gate logs for `f3bd6b66`) was not published at review time. Only the executor's comment states those results.

## 8. Prior public findings on this PR (read after sections 1-7 were written)

On PR #615 there are no review objects and no inline review comments. The prior public findings are the two round-1 review comments, and both are resolved or retained here.

**R382-1** (issue comment 5868262752). My own findings; section 4 covers them:

- F1 is resolved in content, and its hosted run is carried by F2.
- S1, S2 and S4 are taken.
- S3 is declined, with a reason I verified.

**R383-1** (issue comment 5868272025):

| ID | Severity, lenses | Status at `f3bd6b66` | Evidence |
|---|---|---|---|
| F1 | MINOR; Tests, Robustness | **Resolved in content** by the bank-arm option that finding offered: it elaborates a shipping AX7101 config and asserts `milan_eth_constraints` with the real CRG nets in pre-optimize. That finding's M16 (`if board == "ax7101" and not with_mac:`) is my M22. Its M7 (gate moved to `arty`) is my M23. Both are killed by the bank entry and by the shipping arm alone. Its verification clause "the base tree stays green" holds on the bench interpreter and fails in the hosted `elaborate` environment. That part is retained under F2 | Receipts 03, 04, 05, 14, 15 |
| S1 | SUGGESTION; Docs | Taken. `milan_soc.py:1500-1502` no longer claims an asynchronous group or a LiteX false path for GMII | Section 2 (4) |
| S2 | SUGGESTION; Robustness | Taken. Refused or unverifiable builds rename `*.bit` to `*.bit.rejected`, outside `deploy.sh:69` and `build.sh` discovery | Section 2 (3); receipt 07; M29-M31 |

The originating findings from PR #605 ([R372-1] F1 and [R373-1] F1, as summarised in #607) stay resolved. The generated constraints are byte-identical to the round-1 head, and the round-1 sweep evidence still hash-matches.

R382-2 FINISHED
