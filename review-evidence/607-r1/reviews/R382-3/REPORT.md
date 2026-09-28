[R382] POSITIVE - exact head a9f5e34faf51e01c9ecf95807d4a7e695b3eb1c3

# R382-3 internal independent review: issue #607 / PR #615

- Role: internal independent reviewer, cleared context, own detached clone.
- Exact head: `a9f5e34faf51e01c9ecf95807d4a7e695b3eb1c3`, tree `b214ea78f574615b2c7f5ff9b78cd8e307e29a4c`.
- Source base: `54ce877371ee6e8878cf67294e86c2a8481b62f6`. Live dev at review time: `7a7582f03ce5ba7863a90ac342c21be18d90db0b`.
- Delta under review: `f3bd6b66..a9f5e34f`, one commit, `a9f5e34fa` "Elaborate shipping constraint probes without firmware data packages".
  - It changes only `sw/builder/test_shipping_clock_constraints.py` (+26/-2).
  - The subject is one line, with no body or trailers.
- Scope authority:
  - #607 acceptance 1-4;
  - the round-1, round-2 and round-3 assignments (issue comments 5865111793, 5868277772, 5869530253);
  - my own round-2 BLOCKER F2 (PR comment 5869523757).
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs. Each has an artifact-specific result in section 5.

**Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR is open at this head. My round-2 BLOCKER F2 is resolved, and so are all four checks it required:

1. **Pins-only environment.** I built an environment the way `elaborate.yml` builds it. At this head, `test_builder.py --require-elaboration --require-rv32` returns rc 0. All 91 arms run, and the four `[constraints] shipping ... PASS` lines print. The same arm at `f3bd6b66` fails in that environment with the hosted `ImportError`.
2. **Real build path.** The probe override drops exactly three files: `variables.mak`, `output_format.ld` and `regions.ld`. It still reads the build Tcl/XDC that the real `milan_soc.main()` -> `Builder` -> `soc.build` path writes. The meta-path guard makes a bench interpreter fail in the same way the hosted job would.
3. **Mutants.** M07, M16 and M21 stay red, together with every other production mutant in my campaign. M06d is covered in section 8.
4. **Hosted run.** The exact-head hosted `elaborate` job succeeded, and its log shows the arm ran.

I raise one SUGGESTION (S1, Docs), which does not affect the verdict.

## 1. Reconstruction and method

Read in order:

1. AGENTS.md and CONTRIBUTING.md. That includes the seven required contexts.
2. docs/README.md.
3. Issue #607:
   - the body and acceptance 1-4;
   - the three assignments;
   - [A421] TAKEN and [A421] REVIEW READY (issue comment 5870797956).
4. The delta diff `f3bd6b66..a9f5e34f`, in the context of `54ce8773..a9f5e34f`.
5. The pinned LiteX `Builder` source (`litex` at `a1e1c36`, as installed from `sw/litex/litex_pins.txt`).
6. Public evidence:
   - `review-evidence/607-r1` at `bae7b082` is round-1 evidence. It is still relevant, because no production file changed after `350af5dc`;
   - the exact-head hosted check runs, read-only.
7. My own round-2 packet, read-only.

I read no author notes, no lane material and no other reviewer's report before this verdict and ledger were written. Section 8 was written afterwards.

### Executable work

Scripts are in `scripts/` and raw output is in `receipts/`. Every probe ran in a disposable copy of the clone under the packet's `scratch/`. In receipts, `<PKT>` is the packet directory, `<CLONE>` is the review clone and `$HOME` is the host account.

**Pins-only environment** (`build_pins_env.sh`, `pins_run.sh`). It follows `elaborate.yml:138-164,222,240,248-253`:

- Python 3.12.13 in a private venv, with `pip install pyyaml` and then `pip install -r sw/litex/litex_pins.txt`.
- `scripts/ci_litex_env.py`, then `sw/litex/patches/apply.sh`: three patches applied.
- `scripts/ci_rv32_sdk.py` into a private `HOME`. The archive digest `d42680e9...` was verified.
- sv2v v0.0.12 from the pinned zip, digest `ff8c9eea...` verified.
- PATH rebuilt without Verilator, Yosys, cross compilers or Icarus, matching what the hosted job has at the bank step. The hosted log confirms "no Verilator on this runner" at that step.
- The census (receipt 01d) shows `pythondata_software_picolibc` ABSENT and `pythondata_software_compiler_rt` ABSENT.
- No bench venv is reachable. `HOME` is private, so the bank's `sweep.sh` fallback path does not exist.

| # | What | Result |
|---|---|---|
| 01a-d | Build and census of the pins-only environment | rc 0 at each step. Both firmware data packages ABSENT. Pinned sv2v and SDK verified |
| 02 | Shipping arm alone, pins-only, at this head | rc 0. Four `[constraints] shipping ... PASS` lines: 1x1 TDM8 and 8x8, each on e1 and e2 |
| 03 | The same arm at `f3bd6b66` (round-2 head), pins-only | rc 1. `ImportError: pythondata-software-picolibc module not installed!`, from `builder.py:260` via `_generate_includes`. The environment reproduces F2 |
| 04 | **`python3 sw/builder/test_builder.py --require-elaboration --require-rv32`, pins-only, at this head** | **rc 0 in 406 s. 91 arm headers. Four shipping PASS lines. `ALL GATES PASS EXCEPT 2 NOT RUN`**: gate 1b Verilator (hidden, as on the hosted runner) and gate 11 (Arty calibration report). The adopted RV32 compiler is the private-HOME SDK. The interpreter is the pins venv |
| 05a-b | Probe versus an unmodified full Builder, bench interpreter (Python 3.14, which has the packages), 4 config/port pairs | Tcl and XDC are **byte-identical** after path normalisation. The `.v` code is identical with all comments stripped; only the order in LiteX's header hierarchy-tree comment differs. `csr.h`, `soc.h` and `mem.h` are identical apart from the timestamp line. `csr.json` is identical. Files present only in the full output: `software/include/generated/{output_format.ld,regions.ld,variables.mak}`, and nothing else. No file exists only in the probe output |
| 05c-e | The same comparison on the pins interpreter (Python 3.12). The full run gets a PYTHONPATH shim exposing the two packages; the probe does not | Tcl byte-identical in all four pairs. `.v` code identical. The same three files are the only difference. The XDC differs only in the order of the pairwise `set_clock_groups -asynchronous` lines. All 437 other lines are identical, and so is the multiset of group pairs (4 pairs for 1x1, 7 for 8x8). The order is deterministic per path: three full runs agreed with each other, and three probe runs agreed with each other. A full run without the shim fails with the F2 `ImportError`. See S1 |
| 06a-b | `mutation_probe3.sh`, pins-only: 44 mutants, M00-M42 and M44, against the bank entry `test_clock_constraints.py` | Control M00 green. All production mutants M01-M18 and M20-M32 are KILLED, including **M07** (`hook missing or duplicated: []`), **M16** and **M21**. M19 survives; it is equivalent, as in rounds 1 and 2. Probe mutants: M33, M34, M36, M37, M38, M42 and M44 KILLED. M35, M39, M40 and M41 survive, all equivalent here (section 2, item 3) |
| 06c | The same campaign on the bench interpreter, which has the packages: M00, M07, M16, M21, M33-M42, M44 | M00 green. M07, M16 and M21 KILLED. **M33 (the include step forwards `with_bios`) is KILLED by the guard.** M36, M37 and M38 (M33 with the guard removed, mis-prefixed or appended last) SURVIVE. **M44 is KILLED by the include assertion alone.** M42 is KILLED |
| 06d | Failure shape | On bench and on pins, M33 ends in the same LiteX `ImportError: pythondata-software-picolibc module not installed!`, raised at `builder.py:260`, as the round-2 hosted failure and receipt 03 do |
| 06e | Bench interpreter: M00, M21, M22 and M23. These are my equivalents of the other reviewer's M06d, M16 and M7, run after section 8's read | M00 green. M21, M22 and M23 KILLED (`hook missing or duplicated: []`). All three are also KILLED pins-only (06b) |
| 07 | My round-2 `no_picolibc_probe.sh`, unchanged | Bench interpreter with picolibc shadowed: **rc 0**, four shipping PASS lines. The same copy with picolibc importable: rc 0. The same script on the pins interpreter: rc 0 on both lines. On pins, the second line's "importable" label is moot, because the package is absent there |
| 08 | Focused documentation and policy gates | `check_baremetal_only`, `docs_check`, `check_doc_paths`, `check_doc_style`, `check_py_idiom`, `check_hygiene`, `git diff --check` and `py_compile` all rc 0. 0 added-line em dashes. Longest line 103 |
| 09 | `git merge-tree` of this head with live dev `7a7582f0` | Clean, tree `5d0af2c5`. Dev's changes since the base touch no file this PR touches, and neither pins nor workflows |
| 10 | Exact-head hosted checks | **`elaborate` success**: run 36428786466, job 108949299150, head_sha `a9f5e34f`. The step "Elaboration gates" succeeded. The log has 91 arm headers and the four shipping PASS lines. It ends `ALL GATES PASS EXCEPT 3 NOT RUN`, the same three as the green `350af5dc` run (job 108884247537). It contains no `ImportError` or traceback. Other contexts are listed in section 7 |
| 11-12 | Clone and probe-tree integrity | HEAD, index tree `b214ea78` and 946 tracked blobs/modes are equal, at the start and at the end. Gitlinks gptp-processor, protocol-processor and verilog-axis are equal. `external` was uninitialised, as at the start. The probe copy is also byte-equal to the head after all runs |

Vendor tool use: none this round. There was no implementation run and no checkpoint session.

## 2. Round-3 items (issue comment 5869530253) and my round-2 F2 checks

### (1) The shipping arm needs nothing the pinned install lacks. MET

What the delta does, at `sw/builder/test_shipping_clock_constraints.py`:

- `:49-55` overrides `_generate_includes` in the probe's `InspectBuilder`, a subclass of `milan_soc.Builder`, which is LiteX's `Builder` (`milan_soc.py:63,3834`). It records the requested `with_bios` and calls LiteX's own step with `with_bios=False`.
  - In pinned LiteX, `with_bios` gates only `variables.mak` (via `_get_variables_contents`, which calls `get_data_mod("software", "picolibc"/"compiler_rt")` at `builder.py:260-261`), `output_format.ld` and `regions.ld` (`builder.py:299-311`).
  - Everything after that in `_generate_includes` still runs: `mem.h`, `soc.h`, `csr.h`, `git.h` and the rest.
  - So does everything else in `_build`: `finalize`, the CSR map, `_prepare_rom_software`, `_generate_rom_software(compile_bios=False)` and `soc.build` (`builder.py:523-612`).
- No pin, workflow or production file changed. The arm does not skip.
  - `test_clock_constraints.py:270-271` calls it unconditionally.
  - The bank reaches it through `test_builder.py:27557-27562`.
  - The hosted log shows it ran (receipt 10).

Evidence: receipts 02, 03, 04 and 07, and hosted receipt 10.

A pins-only environment built as `elaborate.yml` builds it runs all 91 arms green, with the four PASS lines. The round-2 arm fails in that same environment, so the environment is a faithful reproduction and not a lucky one.

### (2) The override omits only the firmware make/linker inputs and still reads the real generated build Tcl/XDC. MET

Receipts 05a-e compare the probe against a stock `Builder` run of `milan_soc.py` with the same argv, on the same interpreter and tree:

- The generated-file sets differ by exactly `variables.mak`, `output_format.ld` and `regions.ld`.
- The Tcl is byte-identical on both interpreters.
- The Verilog code is identical.
- The XDC is byte-identical on the bench interpreter. On Python 3.12 it is identical in content and differs only in the order of pairwise asynchronous clock-group lines. The arm does not read those lines, and their order has no constraint meaning. See S1.

The path is the real one:

- `milan_soc.main()` is invoked through `sys.argv` (`:86-90`).
- `InspectBuilder.build` calls `super().build` (`:61`).
- The Tcl/XDC are read from `self.gateware_dir` after that returns (`:66-68`).
- Mutant M42, which bypasses LiteX's `Builder.build` for a direct `soc.build`, is KILLED by the new assertion at `:62`.

The meta-path guard (`:19-26`, installed at `:33` in each shipping child before LiteX is imported) makes a local bank fail exactly as the hosted job would:

- On the bench interpreter, which has both packages and installs them through editable meta-path finders, M33 (forward `with_bios`) is KILLED. The traceback is the hosted one (receipt 06d).
- Without the guard (M36), or with it defeated (M37, M38), the same regression is green on the bench. That is the round-2 blind spot, and the guard is what closes it.
- The guard is scoped to the child process, because `test_shipping_constraints` runs each elaboration via `subprocess.run` (`:100-106`). It cannot leak into other bank arms.
- The bench `.pth` files install finders only. No firmware data module is in `sys.modules` at startup, so the guard is consulted before any such import.

### (3) M07, M16, M06d and the rest stay red. MET for my mutants; M06d in section 8

Pins-only (receipts 06a-b):

- Every production mutant from rounds 1-2 is KILLED: M01-M18 and M20-M32. That includes M07 (board guard disabled), M16 (async group dropped) and M21 (call deleted).
- M19 is the documented equivalent survivor.

Bench (receipt 06c): M07, M16 and M21 are KILLED.

The four survivors among the new probe mutants are equivalent for what the arm claims:

- **M35** (guard not installed). It is inert while the include override holds. M36 shows its value.
- **M39 and M41** (the include step skipped entirely). The generated headers are not inputs to the Tcl/XDC/Verilog, as shown by receipts 05a-c, so the arm's oracle is unchanged.
- **M40** (include assertion dropped). It is inert while LiteX calls the step. M42 and M44 show that the assertion is live.

### (4) Exact-head hosted `elaborate`. SUCCESS

Run 36428786466, job 108949299150, `head_sha` `a9f5e34faf51e01c9ecf95807d4a7e695b3eb1c3`, conclusion `success`. Step 16, "Elaboration gates", ran 13:28:53Z-13:44:34Z.

The log:

- has 91 arm headers;
- prints `[constraints] shipping ax7101_1x1_tdm8 e1|e2` and `ax7101_8x8 e1|e2 ... PASS`;
- adopts the provisioned RV32 SDK;
- ends `ALL GATES PASS EXCEPT 3 NOT RUN`.

Those three are the MAKEFLAGS control, gate 1b Verilator, and gate 11 Arty calibration. They are identical to the green run at `350af5dc`. My local run lists 2 because the host `make` re-reads MAKEFLAGS.

### #607 acceptance 1-4 and round-2 items (2)-(5). Unchanged and still MET

No production, constraint, configuration or documentation file changed in this delta (receipt 09). So these results carry forward unchanged from R382-2 at `f3bd6b66`:

- the generated Tcl/XDC (receipt 05 shows the hook, the namespace-derived clocks, synth < hook < opt, and no generic `mr_ff`);
- the log gate (12-4739, 20-1307 and 12-5201);
- the bitstream quarantine;
- the text corrections;
- the round-1 sweep table: WNS +0.034 / +0.268 / +0.105 ns, and Ethernet slack against the 8 ns bound of +6.293 / +6.290 / +6.232 ns.

The production-side mutants that encode those results were re-killed at this head in the pins-only environment: M02-M06, M09-M18, M20 and M26-M32.

## 3. Findings

No BLOCKER, MAJOR or MINOR.

### S1 - SUGGESTION - Docs

**Location.** Issue comment 5870797956 ([A421] REVIEW READY), under "Output equality" and "Open risks/questions".

**Evidence.** Receipts 05c-e.

- On the pins-only interpreter (Python 3.12, `PYTHONHASHSEED=0`), the order of LiteX's pairwise `set_clock_groups -asynchronous` XDC lines is deterministic for a given path. Three full runs are identical, and three probe runs are identical.
- It differs between the probe path and a stock `Builder` path. The stock path imports the firmware data packages; the probe does not.
- All other XDC lines are identical, and so is the multiset of group pairs.
- On the bench interpreter, the probe and full XDC are byte-identical.
- The REVIEW READY text describes the order as run-dependent. It also states byte-identity "on the same interpreter" without naming which interpreter.

**Impact.** None on the arm, which does not read those lines. The order of asynchronous clock groups carries no constraint meaning. A future reader who compares a CI-generated XDC byte-for-byte with a bench one could be misled.

**Suggested outcome (optional).** When this lane's evidence is next summarised, record that probe-vs-full XDC byte-identity holds on the bench interpreter, and that on Python 3.12 only the clock-group line order differs.

**Verification.** Receipts 05d and 05e.

## 4. My round-2 findings at this head

| ID | Round-2 severity, lenses | Status at `a9f5e34f` | Evidence |
|---|---|---|---|
| F2 | BLOCKER; Conformance, Tests, Robustness | **Resolved.** Taken by the preferred route: the arm no longer depends on the firmware data packages. The arm runs and passes in a pins-only environment and in the exact-head hosted `elaborate` job, with no skip. `no_picolibc_probe.sh` returns rc 0. The M07, M16 and call-deletion (M21) mutants are red. No pin was added, so the `litex_pins.txt` install notes need no change | Receipts 02, 03, 04, 06a-c, 07, 10 |
| F1 (round 1) | MINOR; Tests | Stays resolved. The arm is intact and its kill set is unchanged | Receipts 06a-c |

## 5. Lens results (clean-lens format)

```text
[R382] PASS Conformance - sw/builder/test_shipping_clock_constraints.py:19-92 at a9f5e34f against round-3 items 1-3 (issue comment 5869530253) and R382-2 F2: pins-only bank rc 0, 91 arms, 4 shipping PASS (receipt 04); round-2 arm red in the same environment (03); exact-head hosted elaborate job 108949299150 success with the 4 PASS lines (10); #607 acceptance 1-4 carried, since no production/constraint/config file changed (09) and the production mutants were re-killed (06a-b)
[R382] PASS RTL - delta diff f3bd6b66..a9f5e34f (test file only; no HDL, constraint Tcl, platform or milan_soc.py change, receipt 09); generated alinx_ax7101.tcl byte-identical and .v code identical between probe and stock Builder on both interpreters, xdc content-identical (receipts 05a-e); clock_constraints.tcl, alinx_ax7101.py and milan_soc.py unchanged since the R382-2 RTL PASS at f3bd6b66
[R382] PASS Robustness - test_shipping_clock_constraints.py:19-33 (guard scoped to the per-elaboration child, :100-106, consulted ahead of the bench editable finders) and :49-62 (override plus include assertion); configuration dependence checked on the pins-only interpreter (packages absent), bench (present), and bench with picolibc shadowed (receipts 04, 06c, 07); guard-defeat mutants M36-M38 and include-bypass mutants M42/M44 (06c)
[R382] PASS Tests - test_shipping_clock_constraints.py:19-92, test_clock_constraints.py:270-271, test_builder.py:27557-27562; 44-mutant campaign pins-only (M00 green; all production mutants killed; M19/M35/M39/M40/M41 equivalent, reasons in section 2) and bench guard subset plus the other reviewer's M06d/M16/M7 equivalents M21/M22/M23 (receipts 06a-e); existing regressions green: full pins-only bank (04) and hosted elaborate with the same NOT RUN set as 350af5dc (10)
[R382] PASS Docs - test_shipping_clock_constraints.py:2,20,23,30-32,50-53 docstrings/comments checked against pinned LiteX builder.py:260-261,285-311,523-612 and receipts 05a-c; RUNNING_TESTS.md:160-165 ("compile no firmware and run no vendor implementation") still true; litex_pins.txt unchanged and needs no note (no pin added); focused doc gates rc 0, 0 added em dashes (08); S1 is a SUGGESTION on issue-comment wording only
```

## 6. Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-3 items 1-3 and R382-2 F2 against the delta; pins-only bank; round-2 control; exact-head hosted `elaborate`; #607 acceptance 1-4 carried with production mutants re-killed | R382-3 | `a9f5e34faf51e01c9ecf95807d4a7e695b3eb1c3` |
| RTL | CLEAN | Delta scope (test file only); probe-vs-stock generated Tcl/XDC/Verilog on two interpreters; unchanged constraint Tcl, platform and SoC source since R382-2 | R382-3 | `a9f5e34faf51e01c9ecf95807d4a7e695b3eb1c3` |
| Robustness | CLEAN | Firmware-data guard scope and ordering; include override and assertion; package-present, package-absent and shadowed environments; guard-defeat and bypass mutants | R382-3 | `a9f5e34faf51e01c9ecf95807d4a7e695b3eb1c3` |
| Tests | CLEAN | Shipping arm and bank wiring; 44-mutant campaign on pins and bench; full pins-only bank; hosted exact-head bank | R382-3 | `a9f5e34faf51e01c9ecf95807d4a7e695b3eb1c3` |
| Docs | CLEAN (S1 is a SUGGESTION only) | Changed docstrings and comments against pinned LiteX; RUNNING_TESTS and BUILDING claims; `litex_pins.txt` notes; focused doc gates | R382-3 | `a9f5e34faf51e01c9ecf95807d4a7e695b3eb1c3` |

All five lenses are covered at the merge candidate head itself.

## 7. Real limits and pending manager duties

Limits:

- The pins-only environment is a local reconstruction, not the hosted runner image:
  - Python 3.12.13 in a venv rather than setup-python;
  - host `make`, hence 2 NOT RUN rather than 3;
  - PATH rebuilt from the host's `/usr/bin`, minus Verilator, Yosys, cross compilers and Icarus.
  - The exact-head hosted `elaborate` success is the authoritative confirmation, and it agrees.
- The prescribed pinned Verilator path (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`) does not exist on this host. The delta has no RTL, and no Verilator run was needed or done.
- By instruction, I ran no parent, PP, gPTP, Yosys or native bank. The one builder bank I ran is the scoped pins-only reproduction the round-3 assignment requires. No implementation build or vendor session was run.
- Acceptance-4 timing is the round-1 sweep, carried forward because no production file has changed since `350af5dc`. It was not re-run.
- Static timing only. Physical calibration was NOT RUN, and no hardware or field behaviour is established by this review. Field skips are not hardware proof.
- The em-dash and TOC tools were not run locally, because the pinned Markdown renderer is absent. I counted added-line em dashes by hand instead: 0. The hosted `docs-check` is green at this head.

Hosted snapshot at 2026-09-28T13:49:15Z (receipt 10). It was re-read at 13:53:31Z with the same state:

- Success: `elaborate`, `rtl-fast`, `docs-check`, `docs-check-no-git`, `bdd-conformance`, `changes`, `full-ci-gate`, `wire-accountability`, `verilator-lint`, `yosys-elaboration`, Yosys shards 0-3, and Verilator shards 0, 2 and 3.
- Skipped: `Physical gPTP (nightly and manual)`. This is a skipped context, not an executed one.
- Still in progress: Verilator shards 1 and 4. The aggregate `verilator-suites` / `yosys-portability` contexts had not reported.

Pending manager duties:

- Hosted and act acceptance of the remaining Verilator shards and the aggregate contexts at this head.
- Candidate merge validation against live dev `7a7582f0` (merge-tree clean, tree `5d0af2c5`), then post-merge containment.
- #605 merge order is unchanged from round 1:
  - keep the AX7101 toolchain swap before #605's pre-placement hook loop;
  - union the `test_builder.py` and `BUILDING.md` hunks.
- A second independent positive review is still needed.
- A maintainer's merge authorization is still needed.

## 8. Prior public findings on this PR (read after sections 1-7 were written)

On PR #615 there are no review objects and no inline review comments. The prior public findings are in the round-1 and round-2 review comments, and all of them are resolved at this head.

**R382-1 and R382-2** (PR comments 5868262752, 5869523757). My own findings; section 4 covers them:

- F1 stays resolved.
- F2 is resolved.
- R382-1 S1, S2 and S4 stay taken. S3 stays declined, for the reason I verified in round 2. None of the files they concern changed in this delta.

**R383-2** (PR comment 5869518605):

| ID | Severity, lenses | Status at `a9f5e34f` | Evidence |
|---|---|---|---|
| F2 | BLOCKER; Conformance, Tests, Robustness | **Resolved.** Its required outcome and verification are each met. The hosted `elaborate` job passed at the new exact head, and its log shows the four shipping PASS lines. All 91 bank arms ran there and in my pins-only bank. The arm needs nothing the pinned install lacks, by the non-pin route, and it does not skip. The no-picolibc reproduction is green (my equivalent, `no_picolibc_probe.sh`). That finding's M07, M16 and M06d stay red. It defines M06d as "call deleted inside the guard", which is my M21. Its M16 (`and not with_mac`) is my M22 and its M7 (`arty` guard) is my M23. All three are KILLED pins-only and on the bench | Receipts 04, 06b, 06e, 07, 10 |
| Suggestions | none | n/a | n/a |

I did not run that finding's `mutate2.py` itself, because it is part of another reviewer's packet. I covered its named mutants through the equivalents above, and its categories through my own campaign:

- hook omission and guard;
- wrong board;
- port;
- bounded flag and bounded pair;
- hook placement;
- platform toolchain;
- 12-5201;
- quarantine rename, copy, unreadable log and wrong directory.

My campaign kills all of those at this head (M01-M18, M20-M32).

**R383-1** (PR comment 5868272025):

- F1 (MINOR; Tests, Robustness) stays resolved. The arm is intact, and its M16 and M7 equivalents (M22, M23) are killed.
- S1 and S2 stay taken. `milan_soc.py:1500-1502` and the quarantine in `clock_constraints.py:72-79` are unchanged in this delta, and M29-M31 are killed (06b).

The originating findings from PR #605 ([R372-1] F1 and [R373-1] F1, as summarised in #607) stay resolved. No production or constraint file changed after `350af5dc`, and the production mutants were re-killed at this head.

R382-3 FINISHED
