[R383] POSITIVE - exact head a9f5e34faf51e01c9ecf95807d4a7e695b3eb1c3

# [R383] R383-3 external review of PR #615 (issue #607)

Head `a9f5e34faf51e01c9ecf95807d4a7e695b3eb1c3`, tree `b214ea78f574615b2c7f5ff9b78cd8e307e29a4c`,
source base `54ce877371ee6e8878cf67294e86c2a8481b62f6`. This round is a delta review of
`f3bd6b66..a9f5e34f`: one commit, round-3 assignment 5869530253. It covers all five lenses.

I reconstructed the task in this order:
- AGENTS/CONTRIBUTING and the docs map;
- the #607 body and acceptance 1-4, and assignments 5865111793, 5868277772 and 5869530253;
- the executor's public TAKEN (5869567066) and REVIEW READY (5870797956) comments;
- REQ-VER-03, `.github/workflows/elaborate.yml` and `sw/litex/litex_pins.txt`;
- the diff `f3bd6b66..a9f5e34f`, set against the whole-lane diff `54ce8773..a9f5e34f`;
- the exact-head hosted checks.

My own round-2 packet was read-only input. I read no other reviewer's report before writing the
verdict and ledger below.

**Verdict: POSITIVE.** My round-2 BLOCKER (R383-2 F2) is resolved at this head, and I found no new
finding. The evidence:
- **Pins-only builder bank.** I built a pins-only environment the way `elaborate.yml` builds
  one. In it, `python3 sw/builder/test_builder.py --require-elaboration --require-rv32`
  returns rc 0. All 91 arms run, and the four `[constraints] shipping ... PASS` lines print.
- **Hosted `elaborate`.** The exact-head job passed, with the same four lines and all 91 arm
  headers.
- **The probe's Builder override** changes no byte of the generated Tcl, XDC or netlist. It
  omits exactly the three firmware make and linker inputs.
- **The import guard** makes a local interpreter that has the firmware packages fail with the
  exact error the hosted job printed.
- **Mutation campaign.** Every round-2 mutant stays red, in both environments.

## Findings

None at this head. No suggestions.

## Round-3 items, independently checked

| # | Item | Result | Evidence |
|---|---|---|---|
| 1 | The shipping arm needs nothing the pinned `elaborate` install lacks: pins-only bank, 91 arms, 4 markers, repro green | **Met** | `receipts/01`-`04`, `12` |
| 2 | The override omits only firmware make/linker inputs and still reads the real generated Tcl/XDC via `milan_soc.main()`/Builder/`soc.build`; the guard makes a local run fail as the hosted job would | **Met** | `receipts/05`, `06`, `07`, `11` |
| 3 | M07, M16, M06d and the rest of `mutate2.py` stay red | **Met** (27 of 27, both environments) | `receipts/06`, `07` |
| 4 | Exact-head hosted `elaborate` | **success** | `receipts/09` |

### Item 1: pins-only environment and bank

**How the environment was built** (`pins_env.sh`, `receipts/01`). Every step was rc 0:
- a fresh Python 3.12.13 venv;
- `pip install pyyaml`, then `pip install -r sw/litex/litex_pins.txt`;
- `scripts/ci_litex_env.py` (VexiiRiscv `235753e2`) and `sw/litex/patches/apply.sh`;
- sv2v v0.0.12, downloaded and checked against the workflow's sha256;
- `ci_rv32_sdk_selftest.py`, then `ci_rv32_sdk.py`, which installed the digest-verified Bootlin
  SDK into a fresh `HOME`.

**What the environment contains.** `pip freeze` lists only the seven pinned git packages plus
pyyaml. No `pythondata_software_*` package is installed, and both `pythondata_software_picolibc`
and `pythondata_software_compiler_rt` fail to import. `MILAN_LITEX_PYTHON` is unset, no Vivado is
on `PATH`, and `HOME` does not hold the bench venv, so the bank's interpreter search can only
find the pins venv.

**#607 test file alone** (`receipts/02`). rc 0 in 87 s, with the four shipping PASS lines. The
Scala metadata was cold for this run.

**Full bank** (`receipts/03`, `04`). The command is the workflow's `Elaboration gates` step:
- rc 0 in 572 s;
- `arm_census.py` reads the bank's own registration tuple. It finds **91 registered arms, all 91
  headers printed in registration order**, with the #607 arm sixth;
- **4 shipping PASS markers** print;
- the verdict is `ALL GATES PASS EXCEPT 1 NOT RUN`. That one is the historical Arty calibration
  report, gate 11.

**Repro** (`receipts/12`). My round-2 `repro_no_picolibc.sh`, unchanged, now shows:
- picolibc shadowed by an import-failing stub: rc 0 with 4 shipping markers (round 2: rc 1 with
  the hosted ImportError);
- picolibc visible: rc 0 with 4 markers.

### Item 2: what the override and the guard do

**The override.** It is at `sw/builder/test_shipping_clock_constraints.py:49-55`. In the pinned
LiteX, `Builder._build` calls `self._generate_includes(with_bios=with_bios)` (`builder.py:563`).
The `with_bios` block (`:299-310`) is the only place that writes the three files below and
resolves the data packages:
- `variables.mak`, via `_get_variables_contents`, which resolves the picolibc and compiler-rt
  data packages at `:260-261`;
- `output_format.ld`;
- `regions.ld`.

The rest of `_generate_includes` still runs: `mem.h`, `soc.h`, `csr.h`, `git.h` and
`sdram_phy.h`. `_create_build_bundle` touches software inputs only when a build bundle is
enabled. Then `self.soc.build(...)` writes the gateware.

The pinned and the bench copies of `builder.py` are byte-identical.

**Override equivalence** (`probe_equiv.py`, `receipts/05`). I used the bench interpreter, which
*does* carry both data packages. For both shipping configurations on e1 and e2, I ran:
- the committed probe;
- the `f3bd6b66` probe, which has no guard and no override.

After normalizing LiteX date stamps and output paths, `alinx_ax7101.tcl`, `.xdc` and `.v` are
**IDENTICAL**. The same holds for every other output file (litex.log is skipped). The only
difference is three files present in the prior run and absent in the head run:
`software/include/generated/{output_format.ld,regions.ld,variables.mak}`. No generated Tcl or
XDC references any of them.

**Real path.** The subclass replaces `milan_soc.Builder`, which is LiteX's `Builder`
(`milan_soc.py:63`). It calls `super().build()`, so `main()` → `Builder._build` →
`soc.build(run=False)` runs unchanged, and `run_script` is patched to fail. The production-path
mutants confirm it: M17-M21 break the toolchain, flag, hook placement or clock list inside that
path, and all are red in both environments (`receipts/06`, `07`).

**Guard, local run.** The guard is at `:19-26` and is installed at `:33`, before
`milan_soc`/LiteX are imported in each shipping child. LiteX's `get_data_mod` rewraps any
ImportError, so the guard's refusal surfaces as
`ImportError: pythondata-software-picolibc module not installed!`. That is the exact error
round 2 recorded from the hosted job. With the bench interpreter, which has both packages:
- **G1** (override removed) and **G2** (override forwards `with_bios`) are red with that
  message (`receipts/06`);
- **G4a** (override and include assertion removed, guard kept) is red with it too;
- **G4** also removes the guard. It differs from the `f3bd6b66` file only in unused
  definitions and docstrings (`receipts/08`). It is **green on the bench and red in the pins
  env** (`receipts/06`, `07`).

That green/red pair is round 2's blind spot, and G4a shows the guard closes it.

**Expected survivors.** These mutants are behaviourally neutral for what the arm grades:
- **G3/G5** (guard absent or inert). With the override intact, removing the guard changes no
  output.
- **G6** (override skips the include step entirely). The arm grades Tcl/XDC, which do not read
  those headers.

**Generated files across interpreters** (`receipts/11`). In the pins env, two runs with the
probe's own `PYTHONHASHSEED=0` are byte-identical. Against the bench (Python 3.14) run:
- the `milan_eth_constraints` line is byte-identical;
- the Tcl differs only in the VexiiRiscv install path;
- the XDC asynchronous clock-group pairs are equal as unordered sets (7), and every other XDC
  line matches in order;
- the `.v` differs in migen-derived internal signal names.

These are interpreter differences that predate this lane. The arm derives the clock names from
the namespace, so it grades both environments alike.

### Item 3: mutation campaign

`mutate3.py` is round-2 `mutate2.py` with its 27 mutants unchanged, plus G1-G6 (with G4 and
G4a). It runs at most 8 jobs in parallel on a head extraction.
- **Bench interpreter** (`receipts/06`): baseline green. All 27 round-2 mutants are
  **KILLED**, including:
  - M07, M07b and M16, each on `shipping Ethernet hook missing or duplicated: []`;
  - M06d (call deleted inside the guard) and M06, on the same assertion.
  - Totals: 31 killed and 4 survived (G3, G4, G5, G6), all as expected (item 2).
- **Pins-only env** (`receipts/07`): baseline green. All 27 round-2 mutants are **KILLED**, with
  the same assertions. G4 is killed with the hosted ImportError. Totals: 32 killed and 3
  survived (G3, G5, G6).

### Item 4: exact-head hosted `elaborate`

See `receipts/09`. Check run 108949299150, run 36428786466:
- event `pull_request`, `head_sha a9f5e34f`, attempt 1, conclusion **success**;
- every step succeeded, including `Install LiteX at the pinned revisions` and `Elaboration
  gates`;
- the tested merge is `e2d15369` (`a9f5e34f` into live dev `7a7582f0`).

What the log shows:
- the four shipping PASS lines;
- all 91 arm headers in registration order;
- the verdict `ALL GATES PASS EXCEPT 3 NOT RUN`: gate 1b MAKEFLAGS, gate 1b RTL-mutation
  elaboration (no Verilator in that step), and gate 11.

Live dev's own push `elaborate` (job 108871208492) reports the same three NOT RUN arms with 90
arm headers, since dev has no #607 arm. So the extra two are pre-existing runner facts, not
this lane.

My pins bank had one NOT RUN because my `PATH` kept `/usr/bin`, which carries the host
Verilator and make (see Limits).

## Unchanged since round 2 (not re-derived)

This delta touches only `sw/builder/test_shipping_clock_constraints.py`, and receipt 05 shows
it leaves every generated build input unchanged. So these round-2 results carry over at this
head:
- #607 acceptance 1-4;
- the 12-5201 refusal;
- the bitstream quarantine;
- the regenerated-vs-retained sweep Tcl/XDC identity;
- the 117 retained sweep hashes.

They rest on production files, and those are identical at `f3bd6b66` and `a9f5e34f`. I re-ran
the committed tests that grade them (M01-M26, `receipts/06`, `07`) rather than the vendor
control.

## Round-2 finding status (my own)

- **R383-2 F2 (BLOCKER, Conformance/Tests/Robustness): resolved.**
  - The shipping arm needs nothing outside `litex_pins.txt`. The pins-only bank is rc 0 with all
    91 arms and 4 markers.
  - The hosted `elaborate` is green at the exact head, with the arm executed and the 4 markers in
    its log.
  - The fix did not skip anything: the arm runs, and all of its assertions stand.
  - `repro_no_picolibc.sh` is green, and M07, M16 and M06d stay red.
  - No pin, workflow or CI-policy file changed, so the Docs re-cover condition I set in round 2
    was not triggered. Docs is covered again at this head anyway.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-3 items 1-4 and R383-2 F2's required outcome against REQ-VER-03 and `elaborate.yml`. Artifacts: pins-only bank rc 0 with 91/91 arms and 4 markers (`receipts/03`,`04`); exact-head hosted `elaborate` success with 91 arms and 4 markers (`receipts/09`). #607 acceptance 1-4 carried over, since production inputs are unchanged (`receipts/05`) and M01-M26 are red (`receipts/06`,`07`). | R383-3 | a9f5e34faf51e01c9ecf95807d4a7e695b3eb1c3 |
| RTL | CLEAN | No RTL, firmware, constraint or production Python change in `f3bd6b66..a9f5e34f` (name-status: one test file). Generated `alinx_ax7101.{tcl,xdc,v}` for 1x1 TDM8 and 8x8 on e1/e2 are identical with and without the override (`receipts/05`). Pins-vs-bench generated files: identical hook line and clock-group relation set (`receipts/11`). | R383-3 | a9f5e34faf51e01c9ecf95807d4a7e695b3eb1c3 |
| Robustness | CLEAN | The arm in the pinned install with the firmware packages absent (`receipts/02`,`03`) and with picolibc stub-shadowed (`receipts/12`). The guard on an interpreter that has the packages: G1, G2 and G4a red with the hosted error (`receipts/06`). The include-step assertion `:62`. Run-to-run reproducibility under the pinned interpreter (`receipts/11`). LiteX `builder.py:285-310,468-517,523-612` read for other data-package lookups. | R383-3 | a9f5e34faf51e01c9ecf95807d4a7e695b3eb1c3 |
| Tests | CLEAN | `sw/builder/test_shipping_clock_constraints.py:19-92`, `test_clock_constraints.py:270-271` and `test_builder.py:27557-27575`. 27/27 round-2 mutants red in both environments, and G1/G2/G4a red (`receipts/06`,`07`). G4 (round-2 shape) green on the bench and red in the pins env (`receipts/06`-`08`). Survivors G3/G5/G6 are neutral for the graded Tcl/XDC (`receipts/05`). Pins bank and hosted bank run 91/91 arms (`receipts/04`,`09`). | R383-3 | a9f5e34faf51e01c9ecf95807d4a7e695b3eb1c3 |
| Docs | CLEAN | `docs/testing/RUNNING_TESTS.md:160-172` ("compile no firmware and run no vendor implementation") and `docs/integration/BUILDING.md` section 5, checked against the new probe. No docs, workflow or pin file changed in the delta. docs_check, check_doc_paths, gen_toc --check/--verify-anchors, check_em_dash --base 54ce8773, check_doc_style, check_baremetal_only and check_py_idiom all rc 0 (`receipts/10`). Commit `a9f5e34f` is one line with no trailers. | R383-3 | a9f5e34faf51e01c9ecf95807d4a7e695b3eb1c3 |

## Limits

**Pins-only environment fidelity.** It models `elaborate.yml`, but it is not the hosted runner:
- It keeps `/usr/bin` on `PATH` for git, sbt, JVM 17, tclsh and make. That exposes the host
  Verilator and make, which the hosted `Elaboration gates` step does not have, so my bank
  recorded 1 NOT RUN arm to the hosted job's 3.
- I used the host sbt, not a download of sbt 1.10.7. The Scala toolchain caches under the fresh
  `HOME` started cold.
- The pip download cache was the user-level one. The installed set was only the pins.

**Local runs.** Beyond the one pins-only bank that item 1 requires, I ran no full builder,
parent, PP, gPTP or Yosys bank. I ran:
- the #607 test file;
- focused mutants, at most 8 in parallel;
- equivalence probes;
- the docs gates.

**Vendor tool.** Not run in this round. The live 12-5201 control and the sweep evidence are
carried from round 2 (identical production inputs). Physical calibration was NOT RUN, no
hardware was touched, and static timing is not silicon proof.

**Verilator.** Not used, so the scoped binary's identity was not needed.

**Hosted state.** When I last read the checks at 13:53:46Z, `Verilator shard 1/5` and `4/5`
were still in progress. Every other exact-head context had succeeded. The skipped "Physical
gPTP" context is not evidence. `elaborate` completed with success.

**Composition.** The hosted run tested merge `e2d15369` with live dev `7a7582f0`. My local
evidence is on the exact source head. The round-2 #605 composition note stands.

**Redaction.** Receipts redact local absolute paths, the home directory and the host name.

## Pending manager duties

- Hosted/act acceptance at this exact head, including `Verilator shard 1/5` and `4/5`, which
  were in progress when read.
- The final current-dev candidate on live dev `7a7582f03ce5ba7863a90ac342c21be18d90db0b`.
- #605 composition: its `__init__` resolution must still create `BoundedEthVivadoToolchain()`
  before #605 appends to `pre_placement_commands`.
- The merge bar in CONTRIBUTING/AGENTS section 7, including the second positive review.

## Prior public review findings on this PR

I read these only after the verdict, findings and ledger above were written. PR #615 has six
review verdicts: R382-1, R383-1, R382-2, R383-2, and this round's pair (R382-3 is concurrent and
was not read). There are no PR reviews or inline review comments (both counts are 0). At this
head:

- **R383-2 F2 (my own, BLOCKER): resolved.** See the round-2 finding status above.
- **R382-2 F2 (BLOCKER, Conformance/Tests/Robustness): resolved.** This is the same defect.
  Its required outcome is met:
  - The arm runs and passes in the repository's pinned environment. The exact-head hosted
    `elaborate` job succeeded, with the four `[constraints] shipping ... PASS` lines and the
    final bank verdict in its log (`receipts/09`), and my pins-only bank reproduces it
    (`receipts/03`, `04`).
  - It does not skip.
  - The route taken is "the arm stops depending on the software package". No pin changed, so
    no `litex_pins.txt` note is owed.
  - M07, M16 and the call-deletion mutant still turn the arm red (`receipts/06`, `07`).
  - The equivalent no-picolibc check returns rc 0 (`receipts/12`).
  - That reviewer's own probe scripts were not run by me; my equivalents are named.
- **R382-2 suggestions:** none were raised.
- **R382-2's round-1 dispositions (F1 resolved in content; S1, S2 and S4 taken; S3 declined
  with a reason) agree with mine.**
  - F1's remaining hosted clause, "the base tree stays green", now holds at this exact head.
  - The #605 composition duty for S3 stays with the manager.
- **R382-1 F1 (MINOR, Tests): resolved,** including in hosted CI at this head. S1, S2 and S4 are
  taken. S3 was addressed by the comment alternative, as dispositioned in R383-2.
- **R383-1 F1 (MINOR, Tests/Robustness): resolved.** S1 and S2 are taken, as dispositioned in
  R383-2.

No prior finding remains open at this head.

R383-3 FINISHED
