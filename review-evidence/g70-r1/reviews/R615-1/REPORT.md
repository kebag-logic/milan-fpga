[R615] POSITIVE - exact head 26622e27dfb629a6c59d22b77021012127e0c344

# R615-1 external independent review: issue #70 / PR #79

- Repository: Mister-M-alt/FPGA-gPTP, PR #79, head `26622e27dfb629a6c59d22b77021012127e0c344`, tree `17031f39a1215717c7f42c56bba63b2759fe3d16`, base main `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` (merge-base confirmed; the PR reports four commits and 14 changed files).
- Review start: https://github.com/Mister-M-alt/FPGA-gPTP/pull/79#issuecomment-6105015516
- Reconstruction order: the repository has no AGENTS.md or CONTRIBUTING.md at this head, so I started from README.md and docs/README.md (truth order: RTL, then executable tests, then current guides, then history). Then I read the issue #70 body (three acceptance items), the lane comment 6101768043 (scope 1-3 and the proof list), the REVIEW READY comment 6104614009 and the PR body. Next came the full diff `5dce647a..26622e27` with the history of `syn/ooc`. Last came the public evidence at kebag-logic/milan-fpga@60da4bff `review-evidence/g70-r1` (MANIFEST.json, author/HANDOFF.md, author/PR-BODY.md; all hashes match the manifest, and PR-BODY.md equals the live PR body apart from a trailing newline).
- Prior public review findings on PR #79: none. The PR has no reviews and no review comments, and the only issue comments are the two INDEPENDENT REVIEW STARTED notices. I checked this after my own pass, so there is nothing to resolve or retain.

## Verdict basis

Every acceptance and proof item holds at the exact head. I confirmed each one from my own execution, not from the author's receipts:

| Item | Result | Reviewer evidence |
|---|---|---|
| Clock applied before `synth_design`, both tops, from a file read first; period stays 10 ns | MET | `syn/ooc/engine_ooc.tcl:14` and `syn/ooc/ucpu_ooc.tcl:14` call `read_xdc $SPEC/syn/ooc/ooc_clock.xdc` ahead of `read_verilog` and `synth_design` (:22 / :16). `syn/ooc/ooc_clock.xdc:9` is `create_clock -period 10.000 -name clk [get_ports clk_i]`. The post-synthesis `create_clock` is gone. |
| Both logs show the clock defined before synthesis | MET (reproduced) | My exact-head `make ooc` gives `ucpu_ooc.log:28 # read_xdc`, then `:32 Command: synth_design`, then `:84 Parsing XDC File [.../ooc_clock.xdc]`, then `:372 Start Technology Mapping`. For the engine: `engine_ooc.log:28`, `:38`, `:116`, `:443`. Both log checks print `ooc clock order: PASS` (`receipts/vivado/make-ooc-head.txt`, `receipts/vivado_summary.txt`). |
| `make ooc` still produces the six retained reports | MET | `make ooc` rc 0 at the exact head. All six `.rpt` files are retained (`receipts/vivado/head/`). The regenerated ROM is byte-identical to the tracked `syn/ooc/work/gptp_ucode.hex` (sha256 `c496ed8a...0371`). |
| A planted read_xdc after synth_design stops `make ooc` before Vivado, by name, for both scripts | MET (re-applied independently, both scripts) | `make ooc` with a stub Vivado (exit 3, prints when reached). The ucpu plant gives `ucpu_ooc.tcl: ooc_clock.xdc is not read before synth_design` and `ucpu_ooc.tcl:17: read_xdc after synth_design`. The engine plant gives the same pair ending `:23`. Vivado was not reached in either case, while the unplanted control reaches it. Three more independent plants are also stopped by name: a second `create_clock` appended to the engine (`:27`), a `source` appended to the ucpu script (`:21`), and a 5 ns XDC (`receipts/checker_probes.txt` Part C). |
| Log check catches what Vivado actually ran | MET (independent real-Vivado plant) | I planted `set_property USED_IN_SYNTHESIS false [get_files ooc_clock.xdc]` after the `read_xdc` in `ucpu_ooc.tcl`. The static gate cannot see it and passes (rc 0). Real Vivado then synthesized without the XDC: the log shows the parse only at `:472`, after mapping. The log check fails by name: `ucpu_ooc.log: synth_design did not parse ooc_clock.xdc before mapping` (rc 1). See `receipts/vivado/plant-usedinsynth.txt`. Main's own logs also show `# create_clock` after `synth_design completed successfully` (ucpu `:462`, engine `:545`). |
| Constrained vs unconstrained figures with tool identity | MET (reproduced exactly) | I ran Vivado v2026.1 on `xc7a100tfgg484-2`, with no `-directive` (default) and `-mode out_of_context`, at 10.000 ns {0 5} on `clk_i`. Engine: unconstrained (main) 4,853 LUT, 4,387 logic + 466 memory, 3,652 FF, 1.5 BRAM, 4 DSP, WNS +1.773 ns, 0/12,254 failing. Constrained (head) is the same except 4,852 LUT (4,386 logic). The difference is inside `u_ucpu` (2,469 to 2,468 logic LUTs). ucpu: 1,643 / 733 / 1.5 / 4, WNS +1.941 ns, 0/3,165 in both flows. The timing report bodies are identical in both tops, and the ucpu utilization bodies are identical too. Both flows end with 65 warnings, 0 critical warnings and 0 errors. The unconstrained run equals the PR #76 figures carried at main in `docs/MANAGER.md`. |
| `docs/HDL_DEVELOPER.md` and `docs/MANAGER.md` show both flows with a Flow column; archived pages get a flow note only | MET | `docs/HDL_DEVELOPER.md:174-211` (table with Flow column, Vivado 2026.1, part, OOC mode and default directive) and `docs/MANAGER.md:29-56`. The six archived pages gain the text note only. The diff touches no archived figure. Notes in this repository's history are verified from git: both Tcl scripts are unchanged from `c99f7a8` through `5dce647a`, with `create_clock` after `synth_design`. I grepped every other page that quotes LUT, WNS or slack figures. `BENCH_FIRSTLIGHT.md` quotes placed bench builds, not OOC figures, so it correctly has no note. |
| No RTL change; `make tb`, `contract`, `lint`, `docs` pass | MET | `git diff --stat 5dce647a HEAD -- hdl tb bench scripts` is empty. Fresh `make -j16 tb` rc 0, 03:36:00Z to 04:00:34Z. It ran microCPU 768/768, parser 268/268, engine 1,613/1,613 in three images, engine mutants 34/34, gaskets 81/81 + 5/5, tsn-gen 288/288 + 4/4, and the bench tag test PASS. `make contract` rc 0, `make lint` rc 0 (Verilator 5.050), `make docs` rc 0. See `receipts/gates/`. |
| Self-test has 17 arms, and each of the ten rules has an arm only it catches | MET (independent mutation sweep) | I suppressed each rule's finding in a copy. All ten mutants (R1-R3, X1-X2, L1-L5) make `--selftest` fail by name ("... escaped"), with no crash. The unmutated control passes `(17 arms)`. See `receipts/checker_probes.txt` Part A. |

## Findings

No open BLOCKER, MAJOR or MINOR.

### R615-1-01: RESIDUE
- Lenses: Docs.
- Location: `docs/HDL_DEVELOPER.md:209`, "OOC figures dated before issue #70 used the unconstrained flow."
- Authority/evidence: the archived flow notes added by this PR say that order is verified only for this repository's `syn/ooc` (`c99f7a8` to `5dce647a`). For the prototype line it is verified at `c99f7a8` only, and figures from other repositories "keep their own recipes" (for example `docs/history/v1/RESOURCE_VALIDATION.md:11-18`). The guide sentence is not scoped that way.
- Impact: wording only. No figure, measurement, test or verdict changes.
- Exact fix: replace the line with "This repository's `syn/ooc` figures before #70 were unconstrained." (9 words, within the docs check's ten-word rule).
- Verification: `make docs` passes. The sentence names `syn/ooc`.

### R615-1-02: SUGGESTION
- Lenses: Robustness, Tests.
- Location: `syn/ooc/check_ooc_clock.py:77-78` (the static rule matches `read_xdc` on the last path component only) and `:40` (the log parse regex accepts `ooc_clock.xdc` in any directory).
- Evidence: the plant `read_xdc /elsewhere/ooc_clock.xdc` passes the static check with rc 0 (`receipts/checker_probes.txt` Part D). The file the gate validates (`syn/ooc/ooc_clock.xdc`) is therefore not bound to the file the script reads.
- Impact: low. A deliberate redirect would be needed, and the issue does not require this binding.
- Suggested outcome: require the literal `$SPEC/syn/ooc/ooc_clock.xdc` argument, and match the parse line against the resolved repository path. Add one self-test arm.

### R615-1-03: SUGGESTION
- Lenses: Robustness, Tests.
- Location: `syn/ooc/check_ooc_clock.py:90-100`.
- Evidence: the XDC rule counts only `create_clock`. An added `create_generated_clock`, or any timing exception in `ooc_clock.xdc`, passes (Part D). A malformed period such as `10.0.0` ends in a `ValueError` traceback rather than a named finding. That still fails closed, with rc 1. The three missing-file rules have no self-test arm; disabling them still passes the self-test, but they too fail closed through an exception.
- Impact: low. The gate stays fail-closed, but its messages are less specific.
- Suggested outcome: require `create_clock` to be the XDC's only command, report a non-numeric period as a finding, and add arms for the three missing-file rules.

### R615-1-04: SUGGESTION
- Lenses: Docs, Conformance.
- Location: `hdl/ucpu/KL_gptp_ucpu.sv:11-14`. This RTL comment says the module's out-of-context delta against the 1,070-LUT anchor "prices EXACTLY the arithmetic growth".
- Evidence: after this PR the in-repository instrument differs from the anchor's flow. `syn/ooc/ucpu_ooc.tcl:5-12` now says so, but the lane forbids RTL edits. My run shows the standalone microCPU is identical in both flows (1,643 LUT), so no stated figure is wrong today.
- Suggested outcome: a follow-up issue to point the comment at `syn/ooc/ucpu_ooc.tcl` once an RTL change is in scope.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #70 acceptance 1-3 and lane proof list against the diff. `syn/ooc/*.tcl` and the XDC order. Exact-head and main Vivado runs. Planted controls through `make ooc`. Figures checked against the issue, the REVIEW READY comment and the PR body. No-RTL diff check. | R615-1 | 26622e27dfb629a6c59d22b77021012127e0c344 |
| RTL | CLEAN | Empty diff for `hdl tb bench scripts`. `make lint` rc 0. Synthesis of both tops in both flows, with identical timing bodies and a 1-LUT delta localized to `u_ucpu`. The XDC is parsed inside synthesis before mapping. The ROM is regenerated byte-identical. | R615-1 | 26622e27dfb629a6c59d22b77021012127e0c344 |
| Robustness | CLEAN | `check_ooc_clock.py`: Tcl tokenizer, static and log rules, failure modes. `run.sh` gate placement: static before settings or Vivado, log check after both runs under `set -e`. Real-Vivado `USED_IN_SYNTHESIS` plant caught only by the log check. Gap probes (02, 03; SUGGESTION only). | R615-1 | 26622e27dfb629a6c59d22b77021012127e0c344 |
| Tests | CLEAN | 17-arm self-test. A 10-of-10 rule-suppression sweep killed by name, plus 3 informational mutants. Arm attribution. Six `make ooc` plant arms with a stub Vivado. Fresh `make tb`, `make contract`, `make docs`. | R615-1 | 26622e27dfb629a6c59d22b77021012127e0c344 |
| Docs | CLEAN (RESIDUE 01 carried) | `docs/HDL_DEVELOPER.md:174-228` and `docs/MANAGER.md:29-66`, checked against my measured figures. Six archived flow notes, with dates, commits and anchors (`#latest-measured-snapshot` exists). A repository-wide grep for other quoted OOC figures. Tcl and XDC headers. PR body and issue figure tables. `make docs` rc 0. | R615-1 | 26622e27dfb629a6c59d22b77021012127e0c344 |

## Execution receipts (listed in MANIFEST.sha256)

- `receipts/vivado/`: one exclusive acquisition of the shared Vivado lock, 03:30:17Z to 03:35:51Z, with sessions strictly sequential. It holds the exact-head `make ooc` (rc 0), main `5dce647a` `make ooc` (rc 0) and the `USED_IN_SYNTHESIS` plant (static rc 0, Vivado rc 0, log check rc 1). It includes all logs and reports. No other heavy build ran during the lock.
- `receipts/vivado_summary.txt` comes from `scripts/summarize_vivado.py`.
- `receipts/checker_probes.txt` comes from `scripts/checker_probes.py` (20/20 expected outcomes, rc 0).
- `receipts/gates/`: tb, contract, lint and docs logs with rc files. Tool identity is in `env.txt` (Verilator 5.050 rev v5.050 from the pinned wrapper).
- `receipts/rom_and_evidence.txt`: ROM hashes, public evidence hashes and the hosted-check state.
- `receipts/verify_clone.txt`: the clone is at exact head and tree, the index tree equals the head tree, the worktree equals HEAD in bytes and modes, every tracked blob re-hashes to its HEAD id, and there are no untracked or ignored files. The tree has no gitlinks (0 mode-160000 entries), so no submodule gitlink applies. Every probe ran in `git archive` exports under `scratch/`, and the clone was never modified.
- Receipts are sanitized by `scripts/sanitize_receipts.sh`, which replaces host and path identifiers with placeholders. The figures are unchanged, and the summary re-derived from the sanitized receipts is byte-identical.

## Real limits

- Out-of-context synthesis only. No placement, routing or board timing. Physical calibration NOT RUN. No hardware.
- There is one Vivado run per flow. Run-to-run determinism was not re-sampled beyond my reproduction of the author's figures.
- No hosted execution exists at the exact head: 0 check runs, and a combined status of pending with 0 contexts. I claim no hosted, act or manager source bank.
- The author's raw Vivado logs are not in the public evidence (only excerpts and hash prefixes). My own logs replace them as the order proof.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `5dce647a`, live dev `ac2c5e77`) with the builder and native banks at the merge turn, and link those receipts on the PR.
- Own hosted and act acceptance.
- Carry RESIDUE R615-1-01 to the residue checklist with its exact fix.
- Decide whether SUGGESTIONs 02-04 get follow-up issues.

R615-1 FINISHED
