[R383] NEGATIVE - exact head 350af5dcf0aab9fc8ad8d6c6cde3552c63e26a75

# [R383] R383-1 external review of PR #615 (issue #607)

Head `350af5dcf0aab9fc8ad8d6c6cde3552c63e26a75`, tree `7e34d6190d32d4b2cf4d10f5f4b5e90687794379`,
source base `54ce877371ee6e8878cf67294e86c2a8481b62f6`. This is a cleared-context external round that
applies all five lenses. The reconstruction order was: AGENTS/CONTRIBUTING, docs map, the #607 body and
the assignment comment 5865111793, REQ-VER-02/03/04, the diff and history, and then the public
evidence tree `review-evidence/607-r1` at `bae7b082`.

**Verdict: NEGATIVE.** Acceptance 1-4 are met at this head, and I reproduced them independently
(table below). One MINOR finding stays open under `Tests` and `Robustness`. A shipping AX7101
build that never installs the new Ethernet hook passes every committed check and the build gate.
That is the #607 failure class ("constraints silently fail to apply"), reachable through the
Python-side call path this PR introduces. `Conformance`, `RTL` and `Docs` are covered clean.

## Findings

### F1 - MINOR - Tests, Robustness

- **Where:** `sw/builder/test_clock_constraints.py:185-202`, `sw/litex/milan_soc.py:2734-2736`,
  `sw/litex/clock_constraints.py:18-19,61-71`.
- **Title:** An AX7101 build that silently skips the bounded-Ethernet hook passes the committed
  tests and the build gate.
- **Authority/evidence:**
  - AGENTS section 6 `Tests`: each new test can fail for the defect it claims to detect, and real
    integration wiring is tested where practical. #607 "Why it matters": "The build does not fail
    when these constraints are dropped".
  - The only committed check that the hook is wired is an AST spelling test:
    `any(... node.func.id == "add_eth_constraints" ...)` at `test_clock_constraints.py:201-202`.
  - Mutant M16 changes the gate at `milan_soc.py:2734` to `if board == "ax7101" and not with_mac:`.
    The real shipping 1x1 TDM8 recipe then elaborates to the datapath with **zero**
    `add_eth_constraints` calls, and `test_clock_constraints.py` still passes
    (`receipts/07-elab-mutants.txt`). The base tree installs the hook once, with `bounded_eth=True`.
    M7 (gate moved to `arty`) also passes the #607 test file.
  - With the hook absent, `BoundedEthVivadoToolchain` keeps LiteX's generic MultiReg false path
    (`clock_constraints.py:18-19`), and the XDC names no Ethernet exception. No 12-4739 or 20-1307
    can be emitted, so `check_implementation_log` accepts the build.
  - I measured that condition on the routed asl checkpoint (in memory, not saved): re-applying the
    generic mask turns all 13 eth->sys and 16 sys->eth endpoints into `False Path`
    (`receipts/15-vivado-probe-asl/probe_summary.txt`, `probe_interaction_after_generic_mask.rpt`).
    Those are exactly the unbounded crossings #607 removes.
  - No other test or script in the repository references `add_eth_constraints`,
    `milan_eth_constraints` or `clock_constraints` (`git grep` over `sw/builder` and `scripts`), so
    the builder bank does not grade the hook either. I did not run the bank, as this round does
    not allow it.
- **Impact:** a later refactor of the MAC/SoC branch can drop the intended 8 ns Ethernet bound and
  bring back the generic false path. The build still completes and publishes its manifest, and
  every automated check stays green. Only the manual sweep review of `*_clock_interaction.rpt`
  would notice, which is the silent-drop shape #607 exists to close.
- **Required outcome:** an automated check fails when an AX7101 build or elaboration with the GMII
  MAC does not install the bounded hook. Either of these would do; the design is the author's
  choice:
  - the build refuses an AX7101 MAC implementation log that lacks the hook's own
    `CONSTRAINTS: eth=... budget_ns=8.000` record;
  - a bank arm elaborates a shipping AX7101 configuration and asserts that the toolchain is
    bounded and that the pre-optimize Tcl carries `milan_eth_constraints` with the real CRG nets.
- **Verification:** mutants M16 and M7 (`elab_mutants.py`) turn the committed check red, and the
  base tree stays green.

### Suggestions (optional, do not affect coverage)

- **S1 - SUGGESTION - Docs - `sw/litex/milan_soc.py:1499-1502`.** The retained comment still says
  "Each PHY clock is its own asynchronous group: the crossings into sys/milan are ... synchronizers
  LiteX already false-paths". For GMII neither statement holds any more. The PR removed the block
  that used to qualify it, so the three-line #607 note below it now carries the whole correction.
- **S2 - SUGGESTION - Robustness - `sw/litex/milan_soc.py:3956-3960`, `sw/litex/deploy.sh:69`.**
  A refused build raises after `write_bitstream`, so `gateware/alinx_ax7101.bit` stays on disk.
  When `BIT` is unset, `deploy.sh` defaults to the newest `.bit` by modification time. The flash
  transaction is still protected, because it needs a layout that binds the bitstream and a refused
  build writes none. Renaming or marking a refused bitstream would close the volatile/manual path.

## Acceptance, independently checked

| # | Result | Evidence from this round |
|---|---|---|
| 1 | Met | The generated XDC has no `crg_clkout`, no `mr_ff` and no `if {` (`receipts/05`). The hook resolves `eth_clocks0_rx` and `milansoc_crg_clkout0/1` through the namespace, plus 6 async clocks. Its echo in all three sweep logs is identical, code line for code line, to the head's `clock_constraints.tcl` (`receipts/04`). All three logs have 0 CRITICAL WARNING, 0 12-4739 and 0 20-1307 (`receipts/03`). The quasi-static class applies to 112 cells. |
| 2 | Met | Scoping, not precedence: my in-memory control shows the scoping is load-bearing (F1 evidence). All four pairs are `Max Delay Datapath Only`, with no `Unsafe` row in any of the 15 per-seed/per-corner interaction reports (`receipts/08`, `receipts/15`). Installed LiteX `vivado.py`/`common.py` hashes equal the recorded ones at revision `a1e1c36`. |
| 3 | Met as written | `check_implementation_log` runs on every `--build` (`milan_soc.py:3957-3960`), and every launcher reaches it (`build.sh:499`, `sweep.sh:116`, `sweep_extra.sh:48`, `deploy.sh` `do_build`). I reran the committed live control on my checkpoint copy: vendor rc 0, both IDs emitted, refusal raised (`receipts/11-live-plant*`). Mutants M1-M6 and M9-M15 of the gate, wiring and Tcl are killed by the committed tests (`receipts/06`). The gap is F1. |
| 4 | Met | 117 of 117 published sweep artifacts are hash-identical on disk (`receipts/02`). Post-route WNS/WHS are +0.034/+0.022 (asl), +0.268/+0.022 (eto), +0.105/+0.036 (eppo), with TNS = THS = 0. Worst Ethernet slack is +6.232 ns against 8.000. My probe on the asl checkpoint gives Slow WNS **0.034 ns** on a Milan intra-clock path (req 20.000), not an Ethernet crossing. Vivado resolves timing to 1 ps, so the +0.030 rule holds with 4 ps to spare: real, but thin. Fast WNS is 1.567 (the 2 ns reset bound) and WHS is 0.022. Eth slacks reproduce the executor's table exactly. The 0 C and 85 C rows are the same fixed Artix-7 Slow/Fast models, so there are two distinct corners, not four. |

The renamed hook (commit 2) is complete: no `kl_eth` token remains outside the gate that forbids it
(`scripts/check_baremetal_only.py:414`). The sweep argv matches the `sweep.sh` AX7101 shipping
recipe, except that it uses 16 threads instead of 32.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #607 acceptance 1-4 and assignment 5865111793; `sw/litex/clock_constraints.py`, `sw/litex/clock_constraints.tcl`; `milan_soc.py:241-458,2731-2736,3956-3960`; `alinx_ax7101.py:300-301`; three sweep `vivado.log`s, generated `alinx_ax7101.{xdc,tcl}`, `seed_*interaction.rpt`, `seed_crossings.tsv` (hash-verified); asl checkpoint probe; live control rerun | R383-1 | 350af5dcf0aab9fc8ad8d6c6cde3552c63e26a75 |
| RTL | CLEAN | Constraint architecture on the asl routed checkpoint: clock list; `report_exceptions` eth<->sys/milan (hold false and max_dpo=8 only); `report_cdc` (eth data pairs "Safely Timed"; reset-PRE CDC-10 rows pre-existing and out of scope); `check_timing` (0 no_clock, 0 unconstrained endpoints); exception priority (max delay over multicycle); MultiReg classing eth=12 part=198 other=0; no RTL or firmware file in the diff | R383-1 | 350af5dcf0aab9fc8ad8d6c6cde3552c63e26a75 |
| Robustness | UNCLEAN (F1) | Wrong port/net/async-net refusal inside Vivado (`probe_summary.txt` hook rows rc=1); template-drift refusal; missing-log refusal; severity coverage; Vivado-only platform construction (`milan_soc.py:3736-3738`); refused-bitstream residue (S2); hook-absent elaboration (M16) | R383-1 | 350af5dcf0aab9fc8ad8d6c6cde3552c63e26a75 |
| Tests | UNCLEAN (F1) | `sw/builder/test_clock_constraints.py`; `sw/builder/test_builder.py:27557-27563,27575`; 15 file mutants (13 killed); 3 elaboration mutants on the real shipping recipe (M16 and M7 survive, M8 killed by elaboration); `git grep` finds no other reference to the hook; bank arm rerun rc 0 | R383-1 | 350af5dcf0aab9fc8ad8d6c6cde3552c63e26a75 |
| Docs | CLEAN | `docs/integration/BUILDING.md:517-540`, `docs/litex/LITEX_SOC.md:55-61`, `docs/testing/RUNNING_TESTS.md:160-176` against the code; docs_check, check_doc_paths, gen_toc --check/--verify-anchors, check_em_dash --base, check_doc_style, check_baremetal_only, check_py_idiom all rc 0 (`receipts/13`); S1 is optional | R383-1 | 350af5dcf0aab9fc8ad8d6c6cde3552c63e26a75 |

## Limits

- I did not run a full builder, parent, PP, gPTP or Yosys bank; this round does not allow it. I ran
  the #607 bank arm alone and the listed docs gates. I did not run a fresh implementation: the sweep
  evidence is the executor's, and I verified it by hash, by hook echo against the head, and by an
  independent read-only probe of the worst-WNS seed. I read eto and eppo from their retained reports.
- The checkpoint probe used at most 8 threads, and the live control used 16. Nothing was saved to a
  checkpoint. The build host was shared and heavily loaded, which affects runtime only.
- The composition results come from a file-level three-way merge, not from a built candidate.
- Physical calibration was NOT RUN. No hardware was touched, and static timing is not silicon proof.
- Hosted checks at the head were partly still in progress when I read them (`receipts/09`):
  docs-check, elaborate, and Verilator shards 0, 1, 2 and 4. The skipped "Physical gPTP" context is
  not evidence.
- Observation outside #607 scope: `report_cdc` flags CDC-10 (combinational logic before a
  synchronizer) on the Ethernet reset synchronizer PRE pins, fed by sys `phy_reset_storage` and
  Milan `link_guard/eth_rst_r`. This PR does not change it; the manager may want a separate Issue.
- The receipts redact the build host name and home directory.

## Pending manager duties

- Final current-dev candidate on live dev `7a7582f03ce5ba7863a90ac342c21be18d90db0b`, plus
  hosted/act acceptance.
- Composition (`receipts/12`):
  - #605 conflicts in `sw/litex/platforms/alinx_ax7101.py` (import, and the `__init__` block),
    `sw/builder/test_builder.py` (2 hunks) and `docs/integration/BUILDING.md` (1 hunk). The
    `__init__` resolution must replace the toolchain with `BoundedEthVivadoToolchain()` **before**
    #605 appends its `configure_commands()` to `pre_placement_commands`. Otherwise those commands go
    to the discarded toolchain, and `kl_timing_grade_reports` fails at the bitstream stage.
  - Semantically the two compose: #615's in-memory exceptions persist in the routed checkpoint
    that #605's checkpoint reports read (checked on the asl checkpoint).
  - #612 merges cleanly with every file #615 touches. Its image check sits in
    `build_desc_image`, independent of the log gate.
- Re-review after F1 is addressed. The `Tests` and `Robustness` lenses need covering again at the new head.

## Prior public review findings

I checked this after the verdict and ledger above were written. PR #615 had two issue comments,
both round-start notices from the manager (R382-1 and R383-1), no PR reviews and no inline review
comments. The #607 issue thread holds the assignment, the takeover note and the handoff, and none of
those is a review round. Round 1 has no prior published review finding to resolve or retain at this
head. The concurrent R382-1 report was not read.

R383-1 FINISHED
