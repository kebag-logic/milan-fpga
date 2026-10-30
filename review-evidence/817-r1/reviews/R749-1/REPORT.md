[R749] POSITIVE - exact head 6cfb27dacafb2e5b693412db3342ca0fccc9c0bc

# Internal cleared-context review, round R749-1: issue #817, PR #821

- PR #821 `817-servo-reset-cdc` -> `dev`. Head `6cfb27dacafb2e5b693412db3342ca0fccc9c0bc`, tree `0fa85222108a0bc0f4b47fe01552bf44c5de757d`. Source base and live dev are both `1e80128f0a467b58bf884b7d9bf62e013a2fb141` (the PR API record is in `receipts/pr821_api.json`).
- Commits: `a7ff491a` (the cut, the attribute, the hook wiring and the stub test) and `6cfb27da` (docs plus the shipping-test assertion). `git diff a7ff491a 6cfb27da` touches only `docs/**` and `sw/builder/test_shipping_clock_constraints.py`. So the author's route, built at `a7ff491a`, has the same build inputs as this head.
- Executor packet: the author-r1 evidence tree at `414795304a97868ff26cf2dcc5b547c99537fb51:review-evidence/817-r1`.
- Context was read in this order: AGENTS.md and CONTRIBUTING.md, the issue body (frozen acceptance), REQ-CSR-03, `docs/litex/CLOCK_DOMAINS.md`, `docs/integration/BUILDING.md` section 5, the diff `1e80128f..6cfb27da`, then the executable evidence.
- Isolation: before this verdict and ledger were written, PR data was read only through `gh pr view --json title,body,headRefOid,baseRefName,baseRefOid,files,commits` and `gh api .../pulls/821`. No PR or issue comments and no other reviewer's report were read. The prior-findings section at the end was added only after that.

## Verdict

**POSITIVE.** The review found no BLOCKER, MAJOR, MINOR or RESIDUE finding. Two SUGGESTIONs are recorded (S-1 and S-2); neither one affects lens coverage.

## The five checks the round was asked to make

### 1. Exactly one endpoint and one source clock; no other exception changes

`sw/litex/clock_constraints.tcl:27-59` emits exactly one command:

```
set_false_path -from <clock of the milan PLL net> -to <psrst_sync_r_reg[0]/D>
```

That pin is the D pin of the stage that no other stage feeds. The routed exception reports were diffed independently, with the 12-line headers stripped: `route-dev-1e80128f/alinx_ax7101_exceptions.rpt` against `route-a7ff491a/alinx_ax7101_exceptions.rpt`.

- The diff is exactly one added row: `26 [get_clocks -of_objects [get_nets milansoc_crg_clkout1]] * [get_pins {milan_datapath/g_mmcm_servo.mmcm_servo/psrst_sync_r_reg[0]/D}] false false`.
- In `post-route-{dev,head}/exceptions_ignored.rpt`, only the Date and Command header lines differ.
- `post-route-head/milan_ps_endpoints.tsv` still times 16 milan -> PS handshake endpoints at a 5.000 ns requirement, all with positive slack. The reset D pin reads `False Path`.
- The generated XDC is identical to dev's. The build Tcl gains exactly the one hook line. The generated Verilog differs only in its timestamp and the order of its module-tree comment (`constraints-text/*.diff`).

The criterion is met.

### 2. A real two-flop ASYNC_REG chain in one slice; the reset level; open risk 2

**The chain.** The RTL is at `KL_mmcm_drp_servo.sv:1292-1298`: `(* ASYNC_REG = "TRUE" *) logic [1:0] psrst_sync_r;` with `psrst_sync_r <= {psrst_sync_r[0], rst_n}` on `ps_clk_i`. In the route (`post-route-head/crossing.txt`):

- `psrst_sync_r_reg[0]` has ASYNC_REG=1 and sits at SLICE_X3Y16 AFF.
- `psrst_sync_r_reg[1]` has ASYNC_REG=1 and sits at SLICE_X3Y16 A5FF.
- They are one slice and adjacent BELs. At dev the attribute was empty (SLICE_X0Y4 BFF/CFF).

`receipts/lint/servo-semantic-delta.txt` shows that with comments and the attribute removed, the servo RTL is identical to dev's: the change has no behavioural effect.

**The reset level.**
- The source is `rst_n = ~ResetSignal("milan")` (`milan_soc.py:854`), the milan-domain FDPE reset synchroniser (`FDPE_3/C` in the route).
- It asserts asynchronously and releases two milan edges after its cause ends. So any assertion lasts at least one full 20 ns milan period beyond the cause, or 4 or more PS periods of 5 ns.
- One route delays both edges alike (11.368 ns max, 5.971 ns min), so the pulse width is preserved at the first stage. The PS clock samples the asserted level on several edges.

**Open risk 2: is `set_max_delay -datapath_only` required? No.** The issue's own Fix paragraph allows either form ("or `set_false_path` into the first flop with ASYNC_REG on both flops"). The servo's protocol does not depend on a bound:

- **Release order is immaterial.** In `hdl/common/cdc_handshake.sv`, the request is the level `req_tog`, and `data_hold` is held until the acknowledgement returns. A request toggled while the PS side is still in reset is shifted in by `req_sync` after `psrst_n_w` releases, and is still detected as an edge (`req_sync` resets to 0). `ack_tog` restarts at 0 on both sides. The milan side also issues no batch until audio ticks have accumulated a nonzero `acc_r >>> 9` (`KL_mmcm_drp_servo.sv:1150-1169`). That takes far longer than any route delay.
- **The assertion race is bounded and benign.**
  - Suppose `req_tog` was 1 when reset asserts. The source clears it at the next milan edge, and the destination could see a spurious edge.
  - From that clear, a spurious `ps_en_o` needs 5 PS edges: `req_sync[1]`, `dest_req_r`, `pend_v_r`, `P_EN_S`, `ps_en_o`. That is at least about 28 ns after the reset reaches the servo.
  - With the routed 11.368 ns, the runner's own reset takes effect at most about 26.4 ns after that (11.368 + 3 PS edges).
  - So in this route no spurious PSEN escapes. If a longer route ever lost the race, the cost is at most one PSEN step with count 0 (`data_hold` is cleared on the same edge) while the servo is being reset. The servo then re-acquires from IDLE. It is not a UG472 PSEN-before-PSDONE violation, because no new batch can follow within 12 PSCLK.

So the bound is not required for correctness. A bound would restore the pre-PR margin. That is optional, see S-2.

### 3. Refusals and hook presence are killed by planted mutants; exactly one hook in the shipping elaboration

The stub-level gate is `test_servo_reset_sync`, run in private copies by `scripts/mutants.py`. The control passes, and all 12 mutants are KILLED. Results are in `receipts/mutants/`:

| Mutant | What it plants |
|---|---|
| S1 | cut removed |
| S2 | `-from` dropped |
| S3 | cut on the second stage |
| S4 | clock-level cut |
| S5 | ASYNC_REG check dropped |
| S6 | ASYNC_REG check made non-strict, so an empty value is accepted |
| S7 | stage-count check dropped |
| S8 | chain check dropped |
| S9 | clock check dropped |
| S10 | only the distinct-clock half dropped |
| S11 | only the single-clock half dropped |
| S12 | source-clock resolution unchecked |

The build-level gate is the shipping elaboration, 1x1 TDM8 on e1. It cannot run in a git-less copy, because elaboration lists submodule files through git. So `scripts/build_mutants_inplace.py` ran it in place, one mutant at a time, restoring each file with `git checkout`. The control passes. Results are in `receipts/build-mutants/`:

| Mutant | What it plants | Result |
|---|---|---|
| E1 | hook call removed | KILLED |
| E2 | hook duplicated | KILLED |
| E3 | hook names the sys PLL output | KILLED |
| E4 | Tcl sourced twice | KILLED |
| E5 | hook moved to pre-placement | KILLED |
| E6 | `.get("media_clock_servo", False)` default | SURVIVED |

E6 is an equivalent mutant. `main()` always passes the key explicitly (`milan_soc.py:4187-4188`), so the default is never read.

The copy campaign's own E1-E6 and C1 entries in `receipts/mutants/campaign.out` read FAILED or CONTROL-FAILED for that git-listing reason. They are superseded by the in-place run and are kept for transparency.

The head gate (`receipts/constraint-head/`, rc 0) prints `servo reset synchronizer cut and refusal controls PASS`. It also prints four shipping lines, each ending `kl_servo_reset_sync_constraints milansoc_crg_clkout1 PASS`. The shipping assertion (`test_shipping_clock_constraints.py:98-105`) requires the hook list to equal exactly one line naming the real `pll.clkouts[1]`, with one `source` of the Tcl, and both between `synth_design` and `opt_design`.

The author's live receipt (`live-hook-dev-netlist/live-lines.txt`) shows the real tool's behaviour on dev's routed netlist:
- The hook refuses dev's attribute-less netlist (`lacks ASYNC_REG`).
- With the attribute set in memory, it emits exactly the one cut.

### 4. The CDC-report criterion

The acceptance is met as worded. The criterion says "The CDC report lists the crossing as safe".

- The shipped pair report reads `Info milansoc_crg_clkout1 milansoc_crg_clkout4 Safely Timed None 17 17 0 0 0` (`post-route-head/cdc_milan_ps_summary.rpt:17`). That counts this crossing among 17 safe endpoints.
- The whole-design signoff CDC report has the same summary counts and the same 269 detail rows as dev's (`route-a7ff491a/signoff-cdc-rows-vs-dev.txt`).
- Diffing the full reports with whitespace ignored, the only differences are one column-ruler width and one CPU-wrapper row whose source register name changed with placement (row 121, PLIC).

The pair-level Safe classification was already true at dev, because the path was then timed as synchronous. So this criterion does not by itself show that the synchroniser was recognised. The structural recognition is shown by the diagnostic, which declares the pair asynchronous in memory only and is never shipped:

- At this head: `CDC-3 Info 1-bit synchronized with ASYNC_REG property` for `FDPE_3/C -> psrst_sync_r_reg[0]/D`.
- At dev: `CDC-2 Warning ... missing ASYNC_REG property`.

The executor rightly does not ship a clock-level exception, because that would change the handshake's 16 endpoints, which acceptance criterion 2 forbids.

### 5. Suites and rtl-fast

These were re-executed here with Verilator 5.050 (identity in `receipts/lint/verilator-version.txt`), from a `git archive` of this head:

- `mmcm_servo`: rc 0, 109 + 8 + 113 + 90 = 320 checks, 0 failures.
- `mmcm_servo_autorepair`: rc 0, 47 checks, 0 failures.
- A lint of the servo with its CDC primitives: rc 0.

From the author's receipts:
- All 17 servo-compiling suites: rc 0, 73,367 checks, 0 failures (`suites/tally.txt`, `suites/w*/*.rc`). `mbx` first returned rc 2 from a missing `--no-print-directory` in MAKEFLAGS and passed on the rerun with CI's MAKEFLAGS. Both logs are kept.
- rtl-fast at `6cfb27da`: `failed jobs: none`. Its firmware jobs did not run, as the PR states.

Given the empty semantic delta, the suites cannot be affected by this change beyond elaboration.

## Timing and record

The shipping-directive route (`route-a7ff491a/corner-table.md`):

| Corner | WNS ns | WHS ns |
|---|---:|---:|
| Slow 0C / 85C | +0.166 | +0.055 |
| Fast 0C / 85C | +1.481 | +0.020 |

That meets the BUILDING.md floor (WNS >= +0.03 ns, WHS >= 0) at every corner. The route status is complete. The implementation-log gate passes (`check_implementation_log.log`).

`pp_resource_gate.py check --endpoint route-1x1` exits 1 on WNS alone: 0.44 -> 0.166 ns, a fall of 0.274 ns. Every resource figure passes. Under #818 that fall is a warning, and under the manager's record rule a record that does not yet carry this PR's route is not a finding. The two worst families (the LiteEth TX CRC observer, and the LiteDRAM ZQCS timer) are logic this PR does not change.

## Findings

### S-1. SUGGESTION. Tests, Robustness

- **Where:** `sw/builder/test_shipping_clock_constraints.py:98-105` and `sw/litex/milan_soc.py:3120-3123`. No committed control covers the pruned-servo branch.
- **Evidence:** `receipts/pruned/head.log` shows that a `--no-media-clock-servo` 1x1 elaboration at head emits no servo hook and `MCSERVO_P(1'd0)`, which is correct. `receipts/pruned/guard-removed.log` replaces the guard with `if True:`. That emits `kl_servo_reset_sync_constraints milansoc_crg_clkout1` into the pruned build, and nothing in the committed gates notices.
- **Impact:** if the guard regresses, a supported area-lever build (`--no-media-clock-servo`) fails post-synthesis in the vendor tool, because the hook finds no stages. The failure is loud; no wrong bitstream results. That is why this is a suggestion and not a test defect.
- **Optional outcome:** one pruned elaboration control asserting that the servo hook is absent.
- **Verification:** the guard-removal mutant above fails that control.

### S-2. SUGGESTION. RTL, Robustness

- **Where:** `sw/litex/clock_constraints.tcl:57`, the unbounded cut.
- **Evidence:** the reset route grew from 2.671 ns at dev to 11.368 ns in this route. The assertion-race margin in check 2 shrinks from about 13 ns to about 1.6 ns. Nothing bounds the route.
- **Impact:** none on correctness. If the race were lost, the result is at most one zero-count phase step during a servo reset.
- **Optional outcome:** add `set_max_delay -datapath_only` of one milan period on the same `-from`/`-to`. The issue allows that form, and it would keep the margin explicit.
- **Verification:** the routed exception list is still the dev list plus one row, and the pin reports `MaxDelay ... -datapath_only` (the author's `mdd` variant, slack +2.270 at dev).

### Source comments

No RESIDUE found. The new comments name only issue IDs (#817, #607) and state behaviour and reason. They carry no lane labels, rounds or reviewer IDs. This covers `KL_mmcm_drp_servo.sv:1292-1293`, `clock_constraints.tcl:21-26`, `milan_soc.py:279-280` and `3120-3121`, `clock_constraints.py:32` and `45`, and the test comments. Both commits are one line with no trailers.

## Ledger (reviewer-owned)

All five lenses were covered in round R749-1, at exact head `6cfb27dacafb2e5b693412db3342ca0fccc9c0bc`.

| Lens | Result | Examined artifacts |
|---|---|---|
| Conformance | CLEAN | Issue #817 acceptance items 1-5 against: `route-dev-1e80128f` and `route-a7ff491a` `alinx_ax7101_exceptions.rpt` (one added row); `post-route-head/crossing.txt` (False Path); `exceptions_ignored.rpt` (identical); `constraints-text/*.diff`; `post-route-head/cdc_milan_ps_summary.rpt:17`; `cross-probe-head` and `cross-probe-dev` `diag_async_cdc_details.rpt`; `corner-table.md`; REQ-CSR-03 (`REQUIREMENTS.md:135-137`); the issue's Fix paragraph |
| RTL | CLEAN | `KL_mmcm_drp_servo.sv:1290-1378` (synchroniser, handshake, runner reset); `hdl/common/cdc_handshake.sv` (toggle protocol, reset values); `milan_soc.py:854` (reset source); placement in `post-route-head/crossing.txt`; `receipts/lint/servo-semantic-delta.txt` (EMPTY); `receipts/lint/servo-lint-head.log` (rc 0) |
| Robustness | CLEAN | `clock_constraints.tcl:27-59` refusals (stage count, ASYNC_REG strictness, chain, clock count and distinctness, source net); `milan_soc.py:264-281` and `397-402` (milan clock defined whenever the audio MMCM exists); `milan_soc.py:3104-3123` and `4187-4188` (pruning path); `receipts/pruned/*.log`; the reset assertion and release analysis in check 2 |
| Tests | CLEAN | `test_clock_constraints.py:164-248` and `test_shipping_clock_constraints.py:98-105`; `receipts/constraint-head` (rc 0); `receipts/mutants` (12 of 12 stub mutants KILLED, control PASS); `receipts/build-mutants` (5 of 5 non-equivalent KILLED, E6 equivalent, control PASS); `receipts/suites` (`mmcm_servo` 320/0, `mmcm_servo_autorepair` 47/0); the author's `suites/tally.txt` and `rtlfast-6cfb27da/*.out` |
| Docs | CLEAN | `docs/litex/CLOCK_DOMAINS.md:92,237,379-380`; `docs/integration/BUILDING.md:618-621`; `docs/testing/RUNNING_TESTS.md:190-197`, each checked against the Tcl and the route; `receipts/docs` (`docs_check` 0 findings, `check_doc_paths` OK, `check_doc_style` OK); the author's `docs-6cfb27da/all.out` (44 steps, 0 failed) |

## Real limits

- No vendor implementation ran in this round. Route, CDC, exception, placement and live-hook facts come from the author's published receipts at `a7ff491a`, which has build inputs identical to this head. They were checked here by independent diffs, not reproduced.
- Only two of the 17 servo-compiling suites were re-executed here. The rest rest on the author's receipts and on the empty semantic RTL delta.
- No Yosys bank, builder bank, behave run or full rtl-fast was run here.
- Hosted CI state was not inspected.
- Physical calibration and hardware were NOT RUN. Field skips are not hardware proof.
- The probes ran in place and were then restored. `receipts/clone-integrity.txt` records the result:
  - HEAD, tree and index-tree match the head.
  - Worktree and index are identical to HEAD.
  - All six submodule gitlinks are at their recorded commits.
  - The ignored elaboration outputs these probes created were removed, leaving 0 status entries.

## Pending manager duties

- Validate the current-dev merge candidate (builder and native banks) at the merge turn and link its receipts. Live dev equals the source base `1e80128f` today.
- Own the hosted and act acceptance.
- Apply the #818 ruling to the resource gate's WNS warning (0.274 ns fall).
- Re-record the area record once on dev after the last release merge.
- Optionally carry S-1 and S-2 to new issues.
- The author's open item 3 (the handshake's 16 endpoints, which `cdc_handshake.sv` asks to have excepted) is out of scope here and needs its own issue if wanted.

## Prior public review findings

This section was written only after the verdict and ledger above were on disk.

PR #821 has the following public record:
- One issue-thread comment: the review-start notice for this round.
- No review objects.
- No review-thread comments.

Issue #817 carries only the executor's TAKEN and REVIEW READY comments. TAKEN's interpreted scope matches the scope reconstructed here: one false path from the milan clock to the first stage's D pin, ASYNC_REG on both stages, and refusals in place of skips.

So there are no prior review findings on this PR to resolve or retain at this head.

R749-1 FINISHED
