[R614] NEGATIVE - exact head 26622e27dfb629a6c59d22b77021012127e0c344

# R614-1 internal independent review: issue #70 / PR #79

- Repository: Mister-M-alt/FPGA-gPTP, PR #79 (`g70-ooc-clock` into `main`), closes #70.
- Exact head `26622e27dfb629a6c59d22b77021012127e0c344`, tree `17031f39a1215717c7f42c56bba63b2759fe3d16`, base main `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`. The PR head SHA on GitHub was re-read at the end of the review and equals this head.
- Reconstruction order: README and docs map (the repository has no AGENTS.md or CONTRIBUTING.md); issue #70 body (acceptance 1-3); the manager's scope comment on #70 (proof items); the author's REVIEW READY comment; the PR body; `git diff 5dce647a..26622e27` and history; the public evidence at kebag-logic/milan-fpga `60da4bf` `review-evidence/g70-r1` (author HANDOFF.md and PR-BODY.md, manifest hashes match). No hosted checks exist at this head: the repository has no workflows, check-runs total 0, and the combined status is `pending` with 0 contexts.

## Verdict

NEGATIVE. The change does what issue #70 asks. Both scripts read `ooc_clock.xdc` before `synth_design`, and both real Vivado logs show the read ahead of `Command: synth_design`, with the XDC parsed inside synthesis. The planted order defect stops `make ooc` before Vivado, by name, for both scripts. I re-measured both flows independently and every figure the PR records reproduced exactly. All four donor gates pass.

One MINOR finding stays open (F1). In a real Vivado run, the new post-synthesis gate passes a synthesis that ran with no clock at all. That contradicts the gate's own stated guarantee in `run.sh:5-6`. Robustness, Tests and Docs are therefore unclean.

## Findings

### F1 - MINOR - Robustness, Tests, Docs: the log gate passes a synthesis that ran without its clock

- Where:
  - `syn/ooc/check_ooc_clock.py:121-144` (`log_findings`), `:39` (`LOG_PARSE_RE` matches the basename only), docstring `:4`.
  - `syn/ooc/run.sh:5-6` (header claim) and `:36` (log check).
- Authority:
  - Issue #70 exists so that OOC slack is not read from an unconstrained synthesis.
  - The gate's own contract: `run.sh:5-6` says "check_ooc_clock.py fails the run when either script, or the log Vivado wrote for it, shows synthesis without the clock of ooc_clock.xdc". The docstring says "synth_design must see the 10 ns clock".
- Evidence (`receipts/vivado/port.txt`, scripts `scripts/vivado_runs.sh` arm `port`):
  - Setup: the exact head in a scratch export, with the micro-CPU clock port renamed in that copy only (`clk_i` to `clk_x` in `KL_gptp_ucpu.sv`).
  - Static gate: `ooc clock order: PASS (ooc_clock.xdc, ucpu_ooc.tcl, engine_ooc.tcl)`.
  - Vivado 2026.1 logged `CRITICAL WARNING: [Vivado 12-4739] create_clock:No valid object(s) found for '-objects [get_ports clk_i]'` at log lines 86 and 478, inside synthesis. It ends with `2 Critical Warnings`.
  - The timing report shows WNS `NA` and `checking no_clock (1003)`.
  - The log gate then printed `ooc clock order: PASS (ucpu_ooc.log)`, rc 0.
- What the gate actually checks: that the file was read and parsed before mapping. It does not check that the clock bound to a port, or what period took effect. The same blind spot lets `read_xdc` of a different file with the same basename pass both layers: static arm `receipts/static/arm_foreign_xdc_same_name.log` passes, and the log regex at `:39` accepts any `*/ooc_clock.xdc`.
- Impact: `make ooc` can return 0 and print utilization from an unclocked synthesis. A figure recorder would label it "Constrained". That is the defect class #70 removes. Nothing guards it except reading WNS by hand, and `run.sh` prints only utilization.
- Required outcome (preferred): the post-synthesis check fails when the clock did not take effect, with a self-test arm for each new rule. Ways to detect it:
  - any `CRITICAL WARNING` in either log, or the end-of-session `N Critical Warnings` count above zero;
  - or a timing-report check that requires `clk  {0.000 5.000}  10.000` in the Clock Summary and `checking no_clock (0)`.
- Required outcome (alternative, if the manager scopes this out of #70): narrow `run.sh:5-6` and the docstring to what is held ("ooc_clock.xdc is read before synth_design and parsed inside synthesis"), and track the binding check as a follow-up issue.
- Verification: re-run the `port` arm of `scripts/vivado_runs.sh`. The gate must FAIL by name, and the unplanted head must still PASS.

### F2 - SUGGESTION - Tests: two self-test branches have no arm of their own

- `receipts/mutation_sweep.txt`, from my own 15-mutant sweep of the checker: 13 of 15 were killed, mostly by name.
- Survivor 1: `if not clocks:` in place of `len(clocks) != 1 or clocks[0] is None` (`check_ooc_clock.py:94`). No arm plants an XDC with two `create_clock` lines. The rule is correct at this head, but nothing holds its "exactly one" half.
- Survivor 2: searching the whole log for the `read_xdc` echo instead of only the part before `Command: synth_design` (`:135`). The echo-after-done rule (`:140-143`) catches the same fixture, so in practice this mutant is equivalent.
- Suggestion: add an XDC arm with a second `create_clock`.
- This does not affect the verdict.

### Probes that found no defect

- Static planted controls through `make ooc` with a stub Vivado. Each arm is a fresh export of the head; the stub exits 3 if it is reached. Results are in `receipts/static/`.

  | Arm | `make ooc` rc | Stub reached | Gate output |
  |---|---:|---|---|
  | Unplanted head | 2 | yes | PASS, as designed |
  | `read_xdc` moved after `synth_design` in `engine_ooc.tcl` | 2 | no | `engine_ooc.tcl: ooc_clock.xdc is not read before synth_design` / `engine_ooc.tcl:23: read_xdc after synth_design` |
  | The same move in `ucpu_ooc.tcl` | 2 | no | the same two findings, at `ucpu_ooc.tcl:17` |
  | Main's scripts restored | 2 | no | `create_clock after synth_design` at `ucpu_ooc.tcl:13` and `engine_ooc.tcl:20` |

- The head's log check applied to main's real unconstrained logs: rc 1, 6 findings, including `ucpu_ooc.log:462` and `engine_ooc.log:545: create_clock after synth_design` (`receipts/vivado/main_logs_under_head_check.txt`).
- Two static-only arms also pass the static gate: `create_clock` before `synth_design` in the script, and `USED_IN_SYNTHESIS false` on the XDC. Neither was run through Vivado, so I assert no impact for them (see limits).

## Independent re-measurement

- Shared exclusive Vivado lock: one acquisition, 2026-10-11T03:52:30Z to 03:57:55Z, five sessions run one after another.
- Tool: Vivado v2026.1 (64-bit), SW Build 6511674. Part `xc7a100tfgg484-2`. `synth_design -mode out_of_context`, no `-directive`. Shipping ROM, sha256 `c496ed8a…`, byte-identical to the tracked `syn/ooc/work/gptp_ucode.hex`.
- Both flows were run with `syn/ooc/run.sh` from scratch exports: main `5dce647a` is the unconstrained flow, the head is the constrained flow.

| Top | Metric | Unconstrained (main) | Constrained (head) | PR / guides |
|---|---|---:|---:|---|
| engine | Slice LUTs | 4,853 | 4,852 | match |
| engine | `u_ucpu` logic LUTs | 2,469 | 2,468 | match (handoff) |
| engine | Registers / BRAM / DSP | 3,652 / 1.5 / 4 | 3,652 / 1.5 / 4 | match |
| engine | WNS, failing / total endpoints | +1.773, 0 / 12,254 | +1.773, 0 / 12,254 | match |
| ucpu | LUTs / registers / BRAM / DSP | 1,643 / 733 / 1.5 / 4 | 1,643 / 733 / 1.5 / 4 | match |
| ucpu | WNS, failing / total endpoints | +1.941, 0 / 3,165 | +1.941, 0 / 3,165 | match |

- Timing report bodies from `Design Timing Summary` on, with paths stripped, are byte-identical between the flows. Engine body sha256 is `247d9975…` in both flows; ucpu is `195b76f3…`.
- Both flows report clock `clk {0.000 5.000} 10.000`, `no_clock (0)` and 0 critical warnings.
- Head logs: `# read_xdc` at line 28; `Command: synth_design` at 32 (ucpu) and 38 (engine); `Parsing XDC File` at 84 and 116, before `Start Technology Mapping` at 372 and 443. These match the PR body line for line.
- Head `run.sh` rc 0, with static and log gates PASS and six reports retained (`receipts/vivado/head.txt`). Main's unconstrained figures reproduce the PR #76 figures the manager guide carried.

## Donor gates (my run at the exact head)

- Run from a `git archive` export of the head, with the pinned Verilator first on PATH (identity `Verilator 5.050 2026-07-01 rev v5.050`, `receipts/gates/verilator_version.txt`) and `make -j16`.
- `make tb`: rc 0.
  - microCPU 768/768, parser 268/268.
  - engine 1,613/1,613 in three images.
  - engine mutation arm 34/34.
  - gaskets 81/81 plus 5/5, tsn-gen 288/288 plus 4/4.
  - bench tag test PASS.
- `make contract`: rc 0.
- `make lint`: rc 0.
- `make docs`: rc 0.
- Checker self-test: `PASS (17 arms)`. Static check: PASS.
- These agree with the author's published gate receipts. Logs are in `receipts/gates/`, with host paths redacted.

## Lens notes

- **Conformance:**
  - Acceptance 1: both tops read the XDC before `synth_design`, shown by the scripts and the real logs.
  - Acceptance 2: `make ooc` retains six reports; re-measured once at main with both flows. The results are on #70 (REVIEW READY comment) and in `docs/HDL_DEVELOPER.md`.
  - Acceptance 3: every figure in the current guides carries a Flow column or label. The PR #76 delta is labelled unconstrained (`docs/MANAGER.md:54-56`).
  - Every archived page that quotes OOC figures gained a flow note and nothing else. I checked by grep across `docs/history`: the prototype SVG figures are embedded only in `IP_BLOCKS.md`, which has a note, and `BENCH_FIRSTLIGHT.md` quotes a placed build.
  - The history claims are verified: `c99f7a8` is the sole root commit, and both Tcl scripts are unchanged from it through `5dce647a`, with `create_clock` after `synth_design`.
  - Every proof item in the scope comment is met.
- **RTL:** `git diff 5dce647a..26622e27 -- hdl tb bench scripts` is empty. The only synthesis input change is the clock constraint. The XDC targets `clk_i`, which exists on both tops (`KL_gptp_engine.sv:64`, and `KL_gptp_ucpu.sv`).
- **Robustness:** the order rule holds at both layers against the planted controls. F1 is open.
- **Tests:** a 17-arm self-test runs in the `ooc` target. My mutation sweep is in `receipts/mutation_sweep.txt`. F1 has no arm, so the lens is unclean; F2 is a suggestion only.
- **Docs:**
  - The figures, tool identity, Flow columns, flow notes and anchors are correct.
  - `MANAGER.md:50` ("removed one engine LUT; nothing else moved") matches my reports.
  - The overclaim at `run.sh:5-6` and in the docstring is part of F1.

## Prior public review findings

After writing my verdict and ledger, I re-read PR #79. It has two comments, both review-start notices: this round's and the external round's (comment 6105015516). It has 0 PR reviews and 0 inline comments. Issue #70 carries only the scope, TAKEN and REVIEW READY posts. No public review findings exist on this PR, so there is nothing to resolve or retain.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #70 acceptance and scope proof items; scripts and XDC; real Vivado logs for both flows; issue REVIEW READY table; history pages and git history of `syn/ooc` | R614-1 | 26622e27dfb629a6c59d22b77021012127e0c344 |
| RTL | CLEAN | Empty diff on `hdl tb bench scripts`; XDC port against both tops; ROM regenerates byte-identical | R614-1 | 26622e27dfb629a6c59d22b77021012127e0c344 |
| Robustness | UNCLEAN (F1) | `check_ooc_clock.py`, `run.sh`; static planted arms; real-Vivado port-rename arm; main logs under head check | R614-1 | 26622e27dfb629a6c59d22b77021012127e0c344 |
| Tests | UNCLEAN (F1; F2 suggestion) | 17-arm self-test; 15-mutant sweep; `make tb`/contract/lint/docs rc 0 at head | R614-1 | 26622e27dfb629a6c59d22b77021012127e0c344 |
| Docs | UNCLEAN (F1) | `docs/HDL_DEVELOPER.md`, `docs/MANAGER.md`, six archived flow notes, script headers, PR body figures against my reports | R614-1 | 26622e27dfb629a6c59d22b77021012127e0c344 |

## Real limits

- Raw Vivado logs and reports are not published because they carry host paths. The published receipts are path-redacted extracts plus normalized body hashes.
- The re-measurement ran under the shared lock with no other Vivado session. Other lanes' non-Vivado jobs were running on the host at the same time; they are outside my control.
- Two static-only arms were not synthesized: `create_clock` before `synth_design`, and `USED_IN_SYNTHESIS false`. What Vivado does with either is unverified.
- The port-rename arm synthesized only the micro-CPU top. The engine shares the same log rule.
- No manager source bank runs at this head, and I do not claim or infer one. Source-head execution evidence is the author's published gate receipts plus my own gate run above.
- Physical calibration was NOT RUN. No hardware was used, and field skips are not hardware proof.
- I did not read private author material, lane scratchpads, management material or any other reviewer's report before writing this verdict.

## Pending manager duties

- Disposition of F1, either outcome, followed by a re-review at the new head.
- Current-dev merge-candidate validation (builder and native banks) at the merge turn: source base `5dce647a`, live dev `ac2c5e77`.
- Hosted/act acceptance. The repository has no hosted workflows at this head.
- The second independent review, and the full completion bar before merge.

R614-1 FINISHED
