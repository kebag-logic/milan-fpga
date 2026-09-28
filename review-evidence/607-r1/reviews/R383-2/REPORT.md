[R383] NEGATIVE - exact head f3bd6b6694ab61b8f70b7f13f1049a14a6fb3461

# [R383] R383-2 external review of PR #615 (issue #607)

Head `f3bd6b6694ab61b8f70b7f13f1049a14a6fb3461`, tree `1cc73e0e1327694bc4f9def1968ca4237aa4652b`,
source base `54ce877371ee6e8878cf67294e86c2a8481b62f6`. This round is a delta review of
`350af5dc..f3bd6b66`: two commits, round-2 assignment 5868277772. It covers all five lenses.

I reconstructed the task in this order:
- AGENTS/CONTRIBUTING and the docs map;
- the #607 body, assignment 5865111793 and round-2 assignment 5868277772;
- REQ-VER-02/03/04;
- the full diff `54ce8773..f3bd6b66` and the round-2 delta;
- the public evidence tree `review-evidence/607-r1` at `bae7b082` and the exact-head hosted checks.

My own round-1 packet was read-only input. I read no other reviewer's report before writing the
verdict and ledger below.

**Verdict: NEGATIVE.** Everything round 2 asked for works at the source level, and I reproduced
it:
- The new shipping arm kills every hook-omission mutant, including M07, M16 and the call-deletion
  variant, which survived in round 1.
- 12-5201 is refused, and a refused build no longer leaves a bitstream deploy.sh can pick.
- The generated Tcl, XDC and netlist are unchanged.

However, the new arm makes the required hosted `elaborate` context fail at this exact head (F2,
BLOCKER). It needs a LiteX data package that the pinned CI install does not provide. Because the
bank stops at the first failure, 85 later builder-bank arms do not run in hosted CI. `elaborate`
was green at the source base, at `350af5dc` and at live dev.

## Findings

### F2 - BLOCKER - Conformance, Tests, Robustness

- **Where:** `sw/builder/test_shipping_clock_constraints.py:38` (`super().build(**kwargs)`),
  invoked from `sw/builder/test_clock_constraints.py:270-271` and the bank arm
  `sw/builder/test_builder.py:27557-27562,27575`. The pinned CI install is
  `sw/litex/litex_pins.txt` (via `.github/workflows/elaborate.yml`).
- **Title:** The new shipping-constraint arm fails in the required hosted `elaborate` job, and
  that aborts the rest of the builder bank there.
- **Authority/evidence:**
  - REQ-VER-03 (MUST): builder tests elaborate every shipping configuration.
  - `docs/testing/CI_WORKFLOWS.md:620-622`: `elaborate` is one of the seven required contexts
    the merge bar reads.
  - AGENTS section 7 requires a green exact-head gate set, and section 6 `Tests` requires that
    existing regressions remain green.
  - **The exact-head hosted job failed.** `elaborate` check run 108913705616 (pull_request
    event, head_sha `f3bd6b66`, tested merge `825f3c8a` = `f3bd6b66` into `7a7582f0`) runs
    `python3 sw/builder/test_builder.py --require-elaboration --require-rv32` and fails in
    `test_clock_crossing_constraints`. Each shipping child dies in
    `Builder._generate_includes -> get_data_mod("software", "picolibc")` with
    `ImportError: pythondata-software-picolibc module not installed!`
    (`receipts/14-hosted-elaborate-failure-excerpt.txt`).
  - **Only this head is red.** `elaborate` concluded `success` at `54ce8773`, at `350af5dc` and
    at live dev `7a7582f0` (`receipts/15-elaborate-context-by-commit.txt`).
  - **`--no-compile-software` does not help.** The flag skips the firmware compile, but LiteX
    still resolves the picolibc data location while it writes the software include files. Every
    previous elaborating bank arm stops at the `milan_datapath` Instance and never reaches
    `Builder.build`, so this is the first arm that needs that package. `sw/litex/litex_pins.txt`
    does not pin it.
  - **Reproduced at the source head.** On an extraction of `f3bd6b66`, I shadowed only
    `pythondata_software_picolibc` with an import-failing stub:
    - picolibc hidden: the committed `test_clock_constraints.py` ends rc 1 with the same
      ImportError;
    - picolibc visible: rc 0 with 4 shipping PASS markers.

    (`repro_no_picolibc.sh`, `receipts/09-repro-hosted-elaborate-failure.txt`)
  - **Why local banks were green.** The local build interpreter has this package installed
    separately from the pins, which is why the author's and the manager's local full banks passed.
  - **The bank stops at the first failing arm.** The loop at `test_builder.py:27574` has 91
    arms, and the #607 arm is sixth. When it raises, the job ends. The 85 later arms are not
    executed in the required context, including `test_all_configs_build`, the arm that
    elaborates every shipping configuration.
- **Impact:**
  - The required `elaborate` context cannot turn green at this head without a source change.
  - While it stays red, the hosted builder bank loses 85 arms, and REQ-VER-03's hosted evidence
    with them.
  - The round-1 F1 gate added for #607 is never graded green in CI.
  - A later PR would inherit a red required context on `dev`.
- **Required outcome:**
  - At a new exact head, the hosted `elaborate` job passes with the #607 arm executed: its log
    shows the four `[constraints] shipping ... PASS` lines.
  - All 91 bank arms run.
  - The shipping arm needs nothing that the pinned `elaborate` install does not provide. Pinning
    the missing data package is one way; avoiding LiteX's software-include generation while still
    reading the real generated Tcl/XDC is another. The design is the author's.
  - A skip is not an acceptable outcome. Under `--require-elaboration` a skip fails anyway, and a
    silent skip would reopen round-1 F1.
- **Verification:**
  - the exact-head hosted `elaborate` log;
  - `repro_no_picolibc.sh`, or its equivalent for the final package set, turns green;
  - M07, M16 and M06d stay red (`mutate2.py`).

### Suggestions

None this round.

## Round-2 items, independently checked

| # | Item | Result | Evidence |
|---|---|---|---|
| 1 | F1: committed shipping-elaboration arm in the builder bank | **Met at source; fails in hosted bank (F2)** | See the notes below this table. |
| 2 | `check_implementation_log` refuses `[Vivado 12-5201]` | Met | See the notes below this table. |
| 3 | A refused build leaves no bitstream deploy.sh would pick by modification time | Met | See the notes below this table. |
| 4 | `sweep.sh`, `CLOCK_DOMAINS.md`, `milan_soc.py` comment corrections | Met | See the notes below this table. |
| 5 | No timing-relevant constraint text changed | Met; no sweep re-report needed | See the notes below this table. |

**Item 1 (shipping-elaboration arm).**
- **What the arm does.** `test_shipping_clock_constraints.py` runs the real `milan_soc.main()`
  and Builder path for `ax7101_1x1_tdm8` and `ax7101_8x8` on e1 and e2. It compiles no firmware,
  and `run_script` is patched to fail. It asserts:
  - one `milan_eth_constraints eth_clocks<n>_rx [list <PLL clkout0> <PLL clkout1>] [list ...]`
    line;
  - that line placed after `synth_design` and before `opt_design`;
  - no uncommented `mr_ff` line in the XDC.
- **Head result.** Green at head: rc 0, 8.5 s (`receipts/01`).
- **Round-1 elaboration probe.** Re-run on the sweep argv (`receipts/13`):
  - the base installs the hook once, with `bounded_eth=True`;
  - M7, M8 and M16 (M16 and M7 survived in round 1) and M06d (call deleted inside the guard) are
    now **KILLED** by the committed test.
- **Mutation campaign** (`receipts/05`): 27 of 27 mutants are killed and the baseline is green.
  They include R382's `ax7101-disabled` gate, my round-1 M1-M16, and new mutants:
  - bounded flag never set;
  - hook moved to pre-placement;
  - platform keeps the stock toolchain;
  - Milan clock dropped from the bounded pair;
  - wrong eth clock;
  - 12-5201 dropped;
  - quarantine rename removed, copying, skipped for an unreadable log, or using a `.bit` suffix.
- **Shipping arm alone** (`receipts/06`): it kills all 13 hook and scope mutants, each with its
  own assertion (hook missing, generic MultiReg in XDC, outside pre-optimize, or wrong clock
  list).
- **Bank registration.** The arm is registered at `test_builder.py:27575`. Its function, run
  from the bank's interpreter, finds the build interpreter. It is green with 4 markers on the base
  and red under M16 (`receipts/07`).
- **Recipe match.** The arm's argv comes from `soc_params.json`. That argv regenerates the swept
  Tcl/XDC byte for byte (item 5), so it is the real shipping recipe.
- **CI.** The arm fails in the hosted pinned environment; see F2.

**Item 2 (12-5201 refusal).**
- The regex is `12-(?:4739|5201)` (`clock_constraints.py:64-65`), and M22 is killed.
- I re-ran the live control against a scratch copy of the retained routed asl checkpoint, hash
  `a0888c59...`, identical to the original (`receipts/10-live-plant*`):
  - the vendor returned rc 0;
  - it emitted 3 × 12-4739, 1 × 12-5201 (`set_clock_groups: cannot set the clock group when only
    one non-empty group remains`) and 1 × 20-1307;
  - the gate refused them and listed all three IDs.

**Item 3 (no pickable bitstream after refusal).**
- The quarantine renames `*.bit` next to the log to `*.bit.rejected`, both on a findings refusal
  and on an unreadable or missing log (`clock_constraints.py:72-79`). M23-M26 are killed.
- `deploy_pick_probe.py` evaluates deploy.sh's own `BIT=`/`LAYOUT=` default lines, read from the
  file (`deploy.sh:69,71`) (`receipts/11`):
  - with an older accepted build and a newer 12-5201-refused build plus a newest missing-log
    build, both pick the **older accepted** build;
  - the refused and missing-log builds keep only `.bit.rejected`;
  - `layout_from_soch.py`'s `gateware/*.bit` glob also finds nothing in them.
- A refused build writes no `flashboot_layout.json`, because the check (`milan_soc.py:3956-3959`)
  raises before the layout write at `milan_soc.py:4008`.

**Item 4 (text corrections).**
- **`milan_soc.py:1499-1502`.** It now says that MII keeps asynchronous groups and that GMII data
  crossings carry the 8 ns datapath-only bound, with the SoC hook scoping the MultiReg false
  paths. That matches `milan_soc.py:1503-1517` and `clock_constraints.py`, and closes round-1 S1.
- **`sweep.sh:4-7`.** WNS is compared only among seeds with a successful launch, a flash manifest
  and an unquarantined `.bit`. This matches the gate's placement before manifest publication.
- **`CLOCK_DOMAINS.md:343-349`.** It points at `milan_eth_constraints` between `synth_design` and
  `opt_design`, which is true of the generated Tcl (`receipts/01`), and it links BUILDING
  section 5.
- **`BUILDING.md:517-525` and `RUNNING_TESTS.md:160-172`.** Both match the code.
- **Docs gates.** 8 of 8 are rc 0 at head (`receipts/12`).

**Item 5 (no timing-relevant change).**
- `clock_constraints.tcl` is unchanged between `350af5dc` and `f3bd6b66`. The `milan_soc.py`
  delta is comment-only, and the `alinx_ax7101.py` delta is a comment.
- I regenerated all three sweep seeds' inputs at head without a vendor run (`receipts/02`,
  `receipts/03`):
  - `alinx_ax7101.tcl` and `.xdc` are **byte-identical** to the retained round-1 swept inputs
    after path normalization;
  - head vs `350af5dc` Tcl, XDC and netlist are identical, with only LiteX date stamps and the
    unordered hierarchy-summary comment excluded.
- 117 of 117 retained sweep artifacts still match their published hashes (`receipts/04`). The
  round-1 per-seed table stands, and no re-report is required.

## Round-1 finding status (my own)

- **R383-1 F1 (MINOR, Tests/Robustness): resolved at source.** The committed shipping arm kills
  M07, M16 and the call-deletion variant, and the base stays green (item 1). The gate it adds does
  not run green in the required hosted job, which is tracked separately as F2 rather than
  reopening F1.
- **R383-1 S1: taken.** See item 4.
- **R383-1 S2: taken.** See item 3.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2) | #607 acceptance 1-4 and round-2 items 1-5 against: `test_shipping_clock_constraints.py`; `clock_constraints.py:61-80`; the live control (`receipts/10`); regenerated vs retained swept Tcl/XDC (`receipts/02`,`03`); retained sweep hashes (`receipts/04`); REQ-VER-03 against the exact-head hosted `elaborate` log (`receipts/14`,`15`) | R383-2 | f3bd6b6694ab61b8f70b7f13f1049a14a6fb3461 |
| RTL | CLEAN | No RTL/firmware file in `54ce8773..f3bd6b66`. `clock_constraints.tcl` is unchanged since `350af5dc`. Generated `alinx_ax7101.{tcl,xdc,v}` for asl/eto/eppo are identical head vs `350af5dc` and Tcl/XDC identical to the swept inputs (`receipts/02`,`03`). The GMII comment `milan_soc.py:1499-1502` agrees with `milan_soc.py:1503-1517`. The round-1 checkpoint analysis still applies to identical inputs. | R383-2 | f3bd6b6694ab61b8f70b7f13f1049a14a6fb3461 |
| Robustness | UNCLEAN (F2) | 12-5201 at every severity (`test_clock_constraints.py:163-203`, M22); quarantine on refusal and on an unreadable log, accepted retry (M23-M26); deploy.sh pick with refused, missing-log and accepted builds (`receipts/11`); the arm's behavior in the pinned CI environment (`receipts/09`,`14`) | R383-2 | f3bd6b6694ab61b8f70b7f13f1049a14a6fb3461 |
| Tests | UNCLEAN (F2) | `sw/builder/test_shipping_clock_constraints.py`; `test_clock_constraints.py` delta; `test_builder.py:27557-27575`; 27 file mutants, all killed (`receipts/05`); shipping arm alone, 13 of 13 killed (`receipts/06`); bank arm base green and M16 red (`receipts/07`); elaboration probe at head (`receipts/13`); hosted `elaborate` failure (`receipts/14`) | R383-2 | f3bd6b6694ab61b8f70b7f13f1049a14a6fb3461 |
| Docs | CLEAN | `docs/integration/BUILDING.md:517-525`, `docs/litex/CLOCK_DOMAINS.md:343-349`, `docs/testing/RUNNING_TESTS.md:160-172`, `sw/litex/sweep.sh:4-7`, `milan_soc.py:1499-1502` checked against the code and the generated Tcl; docs_check, check_doc_paths, gen_toc --check/--verify-anchors, check_em_dash --base, check_doc_style, check_baremetal_only, check_py_idiom all rc 0 (`receipts/12`) | R383-2 | f3bd6b6694ab61b8f70b7f13f1049a14a6fb3461 |

A fix for F2 that changes the pinned CI install or `elaborate.yml` touches the scope of `Docs`
(workflow and CI policy text) as well as `Tests`/`Robustness`/`Conformance`. `Docs` must then be
re-covered at that head.

## Limits

- **Local runs.** I did not run a full builder, parent, PP, gPTP or Yosys bank, because this round
  does not allow it. I ran:
  - the #607 test file;
  - the #607 bank arm alone;
  - focused mutants, 6-way parallel at most;
  - elaboration regenerations and the docs gates;
  - one Vivado live control on a scratch checkpoint copy, using the committed 16-thread setting
    and saving no checkpoint.
- **Round-2 manager evidence.** The public evidence tree at `bae7b082` holds round-1 material
  only. I found no published round-2 manager bank receipt there. The statement that the local
  source banks passed at this head is the manager's, and it is consistent with F2: the local
  interpreter carries the package the hosted pins lack.
- **Hosted checks.** Hosted checks were partly in progress when I read them (`receipts/08`):
  docs-check, yosys-elaboration and the 5 Verilator shards. The skipped "Physical gPTP" context
  is not evidence. `elaborate` had completed with a failure.
- **Composition.** The hosted run tested merge `825f3c8a` with live dev. My reproduction of F2 is
  on the exact source head. Round-1 composition notes for #605 and #612 were not re-run. The new
  comment at `alinx_ax7101.py:301-302` sits inside the `__init__` block that conflicts with #605.
- **Hardware.** Physical calibration was NOT RUN. No hardware was touched, and static timing is
  not silicon proof.
- **Verilator.** Not used in this round, so its identity was not needed.
- **Redaction.** Receipts redact the host name, home directory and absolute local paths.

## Pending manager duties

- Route F2 to the lane. After the fix, get a new exact-head hosted `elaborate` success with the
  four shipping markers visible, then re-review. `Conformance`, `Tests` and `Robustness` need
  covering again; `Docs` does too if CI files change.
- Final current-dev candidate on live dev `7a7582f03ce5ba7863a90ac342c21be18d90db0b`, and
  hosted/act acceptance.
- #605 composition: its `__init__` resolution must still create `BoundedEthVivadoToolchain()`
  before #605 appends to `pre_placement_commands`. The new comment at `alinx_ax7101.py:301-302`
  states the same rule.

## Prior public review findings on this PR

I read these only after the verdict, findings and ledger above were written. PR #615 has two
round-1 review verdicts:
- my own R383-1 (5868272025), dispositioned above;
- R382-1 (5868262752).

There are no PR reviews or inline review comments. At this head I disposition R382-1 as follows:

- **R382-1 F1 (MINOR, Tests): resolved at source, with F2 retained against the hosted bank.**
  - The required test exists and is in the builder bank (`test_builder.py:27575`). It elaborates
    both shipping AX7101 configurations on either port without a vendor run.
  - It requires `milan_eth_constraints eth_clocks<port>_rx` with the PLL-derived sys/Milan nets
    between `synth_design` and `opt_design`, and no generic `mr_ff` false path in the XDC.
  - M07 (both the `arty` and `ax7101-disabled` guards) and the call-deletion variant are KILLED
    locally (`receipts/05`,`06`,`13`).
  - "Killed by the bank" holds for the bank arm run locally (`receipts/07`). It does not yet hold
    in the required hosted `elaborate` job, where the arm errors before grading anything; that is
    F2.
- **R382-1 S1: taken.** 12-5201 is refused (item 2).
- **R382-1 S2: taken.** See `sweep.sh:4-7` (item 4).
- **R382-1 S3: addressed by the comment alternative that finding offered.**
  `alinx_ax7101.py:301-302` states that nothing may configure the toolchain before the swap. The
  executor's reason for keeping the swap is plausible: the installed `XilinxPlatform.__init__`
  maps a name to a stock instance. The swap is still order-dependent, and the #605 composition
  duty above covers it.
- **R382-1 S4: taken.** See `CLOCK_DOMAINS.md:343-349` (item 4).

The concurrent R382-2 report was not read.

R383-2 FINISHED
