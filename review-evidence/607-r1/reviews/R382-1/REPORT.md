[R382] NEGATIVE - exact head 350af5dcf0aab9fc8ad8d6c6cde3552c63e26a75

# R382-1 internal independent review: issue #607 / PR #615

- Role: internal independent reviewer, cleared context, own detached clone.
- Exact head: `350af5dcf0aab9fc8ad8d6c6cde3552c63e26a75`, tree `7e34d6190d32d4b2cf4d10f5f4b5e90687794379`.
- Source base: `54ce877371ee6e8878cf67294e86c2a8481b62f6`. Two commits: `712d319e7` (fix) and `350af5dcf` (hook rename).
- Scope authority: #607 acceptance 1-4 and the assignment with manager decisions (issue comment 5865111793).
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs. Each has an artifact-specific result below.

Verdict: NEGATIVE. There is one open MINOR, F1 (Tests). The implementation meets acceptance 1-4, and I reproduced that from the retained artifacts. The open item is test coverage: no committed test shows that the real shipping SoC installs the bounded Ethernet hook. With the hook call removed from the real AX7101 path, the shipping elaboration silently goes back to the #607 state: generic MultiReg mask present, no 8 ns bound. Every committed control still passes, and the build-log gate has nothing to reject.

## 1. Reconstruction and method

Read in order:

1. AGENTS.md and CONTRIBUTING.md (verification bar, timing-claim recipe rule).
2. docs/README.md.
3. REQ-VER-02/03/04.
4. Issue #607 body, the assignment with manager decisions, and [A408] TAKEN / REVIEW READY.
5. The diff `54ce8773..350af5dc` and its history.
6. The public evidence tree `review-evidence/607-r1` at `bae7b082`: 32/32 files match their published hashes (receipt 14).

Executable work. Each item is under `receipts/`, and portable scripts are in the packet root.

| # | What | Result |
|---|---|---|
| 01 | `sw/builder/test_clock_constraints.py` at head, build interpreter | rc 0 |
| 02 | `verify_sweep_artifacts.py`: every retained sweep artifact hashed against the public `sweep-artifacts.json` | 117/117 match |
| 03 | Own scan of the three sweep implementation logs | 0 CRITICAL WARNING; 0 x 12-4739 / 20-1307 / 12-5201; hook lines present; `maxThreads 16`; directives as claimed |
| 04 | Regenerated the shipping 1x1 TDM8 build scripts at head from my clone (no vendor run), with the sweep's exact builder argv | `alinx_ax7101.tcl` and `.xdc` byte-identical to the sweep's after path normalisation. `.v` differs only in its date stamp and blackbox-listing comment order. The sweep constraints are exact-head |
| 05 | `parse_sweep_timing.py`: independent per-seed, per-corner parse of the raw reports | All acceptance-4 checks pass (table in section 2) |
| 06 | Build-log gate applied to the supplied shipping implementation log | Refused with 12 findings: 10 x 12-4739, 2 x 20-1307 |
| 07 | Committed live wrong-name control against the read-only shipping checkpoint, 16 threads | Vendor rc 0 and both IDs emitted; the gate refused. Checkpoint sha256 unchanged |
| 08 | `mutation_probe.sh`: unmutated control + 20 mutants against the committed #607 test | Control passes; 17 killed. Survivors: M07, M08, M19 (analysis in sections 4 and 5) |
| 09 | `compose_605_probe.py`: #615 x #605 conflict resolved both ways | Correct order passes both lanes' tests. Wrong order is caught by #395's platform test |
| 10 | Elaborated both AX7101 configurations (1x1 TDM8, 8x8) at head, no vendor run | Hook emitted in both; the 8x8 correctly adds the optional TDM clock. The XDC has no `mr_ff` mask, no `if {`, no `crg_clkout` |
| 11 | Hosted check runs at exact head (read-only snapshot) | Several jobs still in progress (section 7) |
| 12 | Focused doc/policy gates | 7 rc 0. em-dash / TOC could not run locally (renderer package absent; installs not permitted) |
| 13 | Clone integrity after probes | Index tree = `7e34d619`. 945 tracked blobs rehash equal, modes equal. gptp-processor, protocol-processor and verilog-axis gitlinks equal. `external` was uninitialised before and after |
| 15 | `m07_elaboration_probe.sh`: F1 reproduction on the real shipping elaboration | Hook absent, generic mask back, committed test PASS |

Vendor tool use: one read-only checkpoint session, at most 16 threads. No implementation run.

## 2. Acceptance judgment

**A1: real clock names, derived; no 12-4739; `if` out of the XDC. MET.**

- `_CRG` records the raw PLL output signal objects: `sw/litex/milan_soc.py:245-246,268,424,434,449,451,458`.
- `add_eth_constraints` passes them as signals to `pre_optimize_commands.add`. LiteX resolves them through the namespace (`sw/litex/clock_constraints.py:38-58`).
- The Tcl resolves each net with `get_clocks -of_objects` and errors unless exactly one clock is found (`sw/litex/clock_constraints.tcl:13-29`). No hand-typed clock name remains in `sw/`. The only `get_clocks` literal left is the retired MII branch, `milan_soc.py:1518`, which works off the real port.
- Generated shipping XDC (receipts 04, 10): no `if {`, no `crg_clkout`. The conditional class constraint now lives in `kl_quasi_static_constraints` (`clock_constraints.tcl:4-11`).
- All three sweep implementation logs: 0 CRITICAL WARNING and 0 of 12-4739 / 20-1307 (receipt 03). Each log records `quasi_static cells=112` and the derived clock list `eth_clocks0_rx`, `milansoc_crg_clkout0/1` and six asynchronous clocks.

**A2: the eth bound takes precedence; no unsafe eth pair; LiteX untouched. MET.**

- The subclass removes exactly the generic `mr_ff` command, and refuses if the template changes (`clock_constraints.py:11-28`).
- The hook re-applies MultiReg false paths from every clock except the bounded partner, plus from `all_inputs`, then applies the bounds `set_max_delay 8.000 -datapath_only` and `-hold` false paths in all four directions (`clock_constraints.tcl:34-74`).
- The retained reports show the scoping works as intended:
  - `seed_*_eth_sys.rpt`: all 13 eth to sys endpoints are MultiReg first stages (`impl_xilinxmultiregimpl*_reg/D`). Before this change they sat under the generic false path; now each has requirement `8.000ns (MaxDelay Path 8.000ns)`.
  - sys to eth: all 12 endpoints are MultiReg, at 8.000.
  - eth to Milan: 50 endpoints, `KL_gptp_gmii_launch/u_rec_cdc`. Milan to eth: 6 endpoints. Both were "timed unsafe at 4 ns" on the shipping image; now they are at 8.000.
- `seed_interaction.rpt`, all seeds: all four eth pairs read `Max Delay Datapath Only`, and no pair is Unsafe. The only override on those exceptions is FP 5, the retained reset PRE false path. That matches the documented scope.
- No installed-package edit (`installed-constraint-source.json`, and the LiteX checkout was only read).

**A3: build fails on 12-4739 / 20-1307 for shipping; a committed test plants a wrong name. MET.**

- `check_implementation_log` (`clock_constraints.py:61-71`) runs in `main()` under `if args.build:` at `milan_soc.py:3957-3960`. That is before the AEM image and `flashboot_layout.json` are written. `build.sh`, `sweep.sh`, `sweep_extra.sh` and `deploy.sh` all launch `milan_soc.py ... --build`.
- On the supplied shipping log the gate refuses (receipt 06).
- The committed live control (`test_clock_constraints.py:206-235`) plants a wrong clock name and an XDC `if`, and I reproduced it myself (receipt 07).
- The bank-resident controls plant wrong port, net and async names and an ambiguous clock into the Tcl (`test_clock_constraints.py:146-153`).

**A4: fresh AX7101 1x1 TDM8 sweep meets the bound on every seed, WNS >= +0.03 ns. MET.**

The recipe is the builder-emitted shipping argv (identical to my regeneration), `AreaOptimized_high` / `ExploreArea`, the three canonical place directives, and 16 threads. Values are parsed independently from the raw reports (receipt 05):

| Seed (place directive) | Slow WNS | Fast WNS | Slow WHS | Fast WHS | TNS/THS | Worst eth slack vs 8.000 | Unsafe eth pair |
|---|---|---|---|---|---|---|---|
| asl (AltSpreadLogic_high) | +0.034 | +1.567 | +0.123 | +0.022 | 0/0 | +6.293 (eth to Milan) | none |
| eto (ExtraTimingOpt) | +0.268 | +1.299 | +0.126 | +0.022 | 0/0 | +6.290 (eth to sys) | none |
| eppo (ExtraPostPlacementOpt) | +0.105 | +1.516 | +0.102 | +0.036 | 0/0 | +6.232 (eth to sys) | none |

Margin analysis:

- The asl +0.034 ns is real, not rounding. The implementation log's own post-route summary and both Slow reports give 0.034 at the tool's ps resolution, 4 ps above the rule.
- The worst path is intra-Milan (`clkout1 -> clkout1`, 20 ns), not an Ethernet crossing.
- The 0 C and 85 C rows are identical in every report. Artix-7 uses fixed Slow/Fast models, so the two temperature settings do not give independent timing corners. #605 states the same. So there are two distinct corners per seed, both reported.

The per-seed table matches the author's published table exactly.

## 3. Commit 2 and composition with queued lanes

- **Commit 2** renames the hook to `milan_eth_constraints`, avoiding the reserved `kl_eth` token (`scripts/check_baremetal_only.py:414`). No `kl_eth` remains under `sw/` or `docs/`, and `check_baremetal_only.py --check` rc 0 (receipt 12). Both commits have one-line subjects with no body or trailers.
- **#612 (#577 image check):** `git merge-tree` of #615 with #612 head `be6b48c1` is clean (tree `52075ae5`).
  - #612 validates inside `build_desc_image()`. That is independent of the log check, which still precedes all manifest writes in the merged `main()`.
- **#605 (#395 corner reports):** merging with head `895be307` conflicts in `sw/litex/platforms/alinx_ax7101.py`, `sw/builder/test_builder.py` and `docs/integration/BUILDING.md`.
  - The platform conflict is order-sensitive. #615 replaces `self.toolchain` after `Xilinx7SeriesPlatform.__init__`, and #605 appends pre-placement grade commands at the same point.
  - Resolved with the swap first, both lanes' focused tests pass (receipt 09).
  - Resolved the other way, #605's grade commands land on the discarded toolchain. #395's `test_platform_hooks` fails (`AssertionError: []`), so that mistake is caught by an existing test.
  - Report hooks compose: #605 writes `*_signoff_clock_interaction.rpt` and #615 writes `*_clock_interaction.rpt`, so the file names do not collide.
- **Live dev `7a7582f0`:** merge-tree clean (tree `17cfe5f9`).

## 4. Findings

### F1 - MINOR - Tests

**Location.** `sw/builder/test_clock_constraints.py:186-202`, the only real-SoC wiring check, against `sw/litex/milan_soc.py:2734-2736`. The committed test never shows that the real shipping SoC installs the bounded Ethernet hook.

**Authority / evidence.**
- AGENTS section 6, Tests lens: "Real integration wiring is tested where practical" and "Tests do not merely reproduce implementation assumptions".
- #607 describes a build that "does not fail when these constraints are dropped".
- The only link between the real `MilanSoC` and the hook is an AST check that `add_eth_constraints(...)` is called somewhere in `milan_soc.py`. `test_generated_constraints` drives a synthetic `Module`, not the real SoC.
- Mutant M07 (receipt 08) changes the guard at `milan_soc.py:2734` so the AX7101 never calls the hook, and it survives.
- Reproduced on the real shipping 1x1 TDM8 elaboration (receipt 15, `m07_elaboration_probe.sh`): elaboration rc 0, `milan_eth_constraints` lines 0, `report_clock_interaction` lines 0, and the generic `mr_ff` false path back in the XDC. The committed #607 test still passes.
- No other builder gate inspects generated constraints; a search for `milan_eth_constraints`, `mr_ff` and `pre_optimize` in `sw/builder/` and `scripts/` finds nothing.

**Impact.** A later refactor of the MAC/board wiring could restore the exact #607 state with a green bank and a green build:
- the Ethernet-to-sys crossings unbounded again;
- Ethernet-to-Milan timed as related or unsafe;
- no interaction report produced.

The new log gate cannot see this, because no constraint is rejected. It is simply never issued.

**Required outcome.** A committed test in the builder bank must elaborate the real shipping AX7101 GMII configuration(s) without a vendor run, as already done for REQ-VER-03, and read the generated build files. It should fail unless:
- the build Tcl carries `milan_eth_constraints eth_clocks<port>_rx` for the configured port, with the SoC-derived nets, between `synth_design` and `opt_design`;
- the XDC carries no generic `mr_ff` false path.

Mutant M07 must be killed by the bank.

**Verification.** Run `m07_elaboration_probe.sh` and `mutation_probe.sh`, re-pointed at the fixed head, and confirm that M07, and ideally a variant that deletes the call inside the guard, both report KILLED.

### Suggestions (optional; do not affect coverage)

- **S1 - SUGGESTION - Robustness, Tests.** `sw/litex/clock_constraints.py:63-64` does not match `[Vivado 12-5201]` ("cannot set the clock group when only one non-empty group remains"). Two such lines in the shipping log were the dropped asynchronous clock group of this same defect. Acceptance 3 names only 12-4739 / 20-1307, so this is met as written. Adding 12-5201 would cover the dropped-group form of the same class.
- **S2 - SUGGESTION - Docs.** `sw/litex/sweep.sh:4-5` still says to "pick by WNS" by grepping each seed's `vivado.log`. A refused seed keeps its timing summary and `.bit` there; the refusal is only visible in `$dir.launch.log` and in the missing `flashboot_layout.json`. The persistent flash path stays gated, because flash-pair needs a layout bound to the bitstream payload. A one-line note that a seed without its layout, or with the #607 refusal in its launch log, is not a candidate would keep the operator procedure in line with BUILDING section 5.
- **S3 - SUGGESTION - RTL.** `sw/litex/platforms/alinx_ax7101.py:300-301` swaps in a new toolchain object after base construction. Today this is equivalent: `device_image_arch` is None and nothing configures the toolchain earlier. But any state attached before the swap is silently discarded, which is exactly the #605 hazard in section 3. Constructing the subclass directly would remove the ordering dependency. Alternatively, a comment at the swap could say that nothing may configure the toolchain before it.
- **S4 - SUGGESTION - Docs.** `docs/litex/CLOCK_DOMAINS.md:341-351` says "Inspect generated constraints". The Ethernet bounds now live in the build Tcl pre-optimize section, not the XDC. A pointer to BUILDING section 5 would stop a reader from concluding from the XDC alone that the bounds are missing.

## 5. Lens results (clean-lens format)

```text
[R382] PASS Conformance - sw/litex/clock_constraints.{py,tcl}@350af5dc, milan_soc.py:245-458,2734-2736,3957-3960; sweep vivado.log x3 and seed_{interaction,exceptions,*_eth_*}.rpt x3 (117 artifacts hash-verified); regenerated alinx_ax7101.{tcl,xdc} - acceptance 1-4 and the manager decisions checked against raw artifacts; all met
[R382] PASS RTL - clock_constraints.tcl:4-77 against the post-route exceptions/interaction/path reports; _CRG clock-object capture milan_soc.py:245-458; bound 8.000 <= each pair's shorter period; hold false path only on the bounded async pairs; reset PRE and 2 ns ARS exceptions retained (report positions 5, 6); precedence FP > max_dpo > MCP observed; per-clock-pin MultiReg classification (eth=12, part=198, other=0); S3 only
[R382] PASS Robustness - kl_net_clock / port / MultiReg single-clock refusals (tcl:13-38), template-drift refusal (py:24-27), missing-log refusal, empty quasi-static class, optional DDR/TDM clocks (8x8 elaboration adds audio_tdm_raw), e2 port path, refused-seed flash path (deploy payload binding) - fail-closed on each; S1/S2 only
[R382] UNCLEAN Tests - sw/builder/test_clock_constraints.py@350af5dc and test_builder.py:27557-27563; 20 mutants: 17 killed, M07 survives and is reproduced on the real shipping elaboration (F1); M08 (fixed port 0) is correct for e1 and fails closed at elaboration for e2 (lookup_request); M19 is equivalent (list.remove refuses an absent template)
[R382] PASS Docs - docs/integration/BUILDING.md:517-540, docs/litex/LITEX_SOC.md:55-61, docs/testing/RUNNING_TESTS.md:160-176 checked line by line against code and evidence; CLOCK_DOMAINS.md:348-351 is now true; no em dash in added lines; check_doc_style / docs_check / check_doc_paths rc 0; hosted exact-head em-dash and link-health steps success; S2/S4 only
```

## 6. Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Diff; the three sweep logs and hash-verified reports; regenerated build scripts; shipping log refusal; live control | R382-1 | `350af5dcf0aab9fc8ad8d6c6cde3552c63e26a75` |
| RTL | CLEAN | `clock_constraints.tcl`, `_CRG` clock capture, post-route exception/interaction/path reports, #605 composition | R382-1 | `350af5dcf0aab9fc8ad8d6c6cde3552c63e26a75` |
| Robustness | CLEAN | Refusal paths in Tcl/py, optional-domain elaborations (1x1 TDM8, 8x8), refused-seed deploy binding | R382-1 | `350af5dcf0aab9fc8ad8d6c6cde3552c63e26a75` |
| Tests | UNCLEAN (F1 open) | `test_clock_constraints.py`, `test_builder.py` wiring, 20-mutant campaign, real-elaboration M07 probe | R382-1 | `350af5dcf0aab9fc8ad8d6c6cde3552c63e26a75` |
| Docs | CLEAN | BUILDING / LITEX_SOC / RUNNING_TESTS / CLOCK_DOMAINS, focused doc gates, hosted docs steps | R382-1 | `350af5dcf0aab9fc8ad8d6c6cde3552c63e26a75` |

- A fix for F1 touches the Tests scope and needs re-review of Tests at the new head.
- If it also touches `sw/litex/` or `docs/`, the lenses covering those files must be re-covered at that head.

## 7. Real limits and pending manager duties

Limits:
- The prescribed pinned Verilator binary (under the `372-manager-candidate1` tool directory) does not exist on this host. The diff has no RTL or HDL change, so no Verilator run was needed or done.
- The em-dash and TOC gates could not run locally: the pinned Markdown renderer dependencies are absent, and installs are not permitted. They are covered by the manager's bank and the hosted exact-head docs-check steps "Added-line em-dash gate" and "Link health ..." (success).
- By instruction, I ran no full builder, native, parent, PP, gPTP or Yosys bank and no implementation build.
- The acceptance-4 evidence is the executor's sweep. I verified it by hash, by byte-identical regeneration of its constraints at this head, and by my own parse of its raw reports. I did not re-run it.
- The 8x8 configuration was elaborated only, with no implementation. Acceptance 4 names only 1x1 TDM8.
- I read only vendor-generated artifacts in the executor's validation storage, each checked against the public hash index. I read no notes or scratch material.
- Static timing only. Physical calibration NOT RUN; field or hardware behaviour is not established by this review.

Pending manager duties:
- Hosted exact-head jobs `elaborate`, `docs-check` and Verilator shards 0, 1, 2 and 4 were in progress at review time. The `elaborate` step runs `test_builder.py --require-elaboration`, which now calls `test_clock_constraints.py` and needs `tclsh` on the runner; confirm it ran and passed rather than skipped.
- #605 merge order: keep the toolchain swap before #605's pre-placement hook loop, and union the `test_builder.py` and `BUILDING.md` hunks. #395's `test_platform_hooks` detects the wrong order.
- Candidate merge validation on live dev `7a7582f0` (my merge-tree is clean, tree `17cfe5f9`), and post-merge containment.
- Second independent positive review ([R383]).

## 8. Prior public findings

- Checked after the verdict and ledger above were written. No review findings exist on PR #615 at this head:
  - the only issue comments are the manager's two review-start notices (R382-1 and R383-1);
  - there are no review objects and no inline review comments.
- Nothing prior to resolve or retain. F1 and S1-S4 are new in this round.
- The originating findings, [R372-1] F1 and [R373-1] F1 on PR #605 (as summarised in #607), are resolved at this head:
  - the fresh implementations emit no 12-4739 or 20-1307;
  - the intended 8 ns bound applies in all four Ethernet directions and outranks the MultiReg exception;
  - the 112-cell quasi-static class is applied.

R382-1 FINISHED
