[R878] POSITIVE - exact head 8aeb2f0bb9bfad9c486a0abf9dbeaf134d3de2fb

External independent review R878-4 of issue #948 / PR #959. Tree `f00413b5354577dded4c76c4098b01bd6c8002bd`. All five lenses are CLEAN for this narrow re-check. No open BLOCKER, MAJOR or MINOR was found. The existing wording residue and optional safeguard suggestion remain below.

The delta from `64117b77cb9e5c421717835b5be032b5905c447d` is exactly one commit and one changed line: `sw/firmware/ctrl/README.md:255`, 185 to 192 pin controls. `delta.diff` and `delta-history.txt` preserve that comparison. There are no code, test, interface, gitlink, mode or other documentation changes. Whole-PR context remains `15168e14..8aeb2f0b`; untouched implementation retains its prior technical verdicts.

Reconstruction used AGENTS.md, CONTRIBUTING.md, docs/README.md, the public issue ruling/takeover and acceptance decisions, REQUIREMENTS.md and relevant interface descriptions before judging the delta and published receipts. `independent-delta.md` records this round's independent verdict and ledger before prior public review reports were read. Prior findings were then reconciled at their causes. No private author material, management checkout, other active review report or lane scratchpad was consulted. Submitted reviews and inline threads were empty; prior findings reside in conversation comments (`review-surfaces.json`, `public-pr-snapshot.json`).

**Count and figure evidence**

The [manager packet](https://github.com/kebag-logic/milan-fpga/tree/eea845dba7b561499de5cf537a5b665d72e278b1/review-evidence/948-r1/manager-r4) records the executed boundary job at run 45191675681, attempt 2, over `dev-soft-core aa30d77f`. Its receipt reports 192 pin controls, zero misbehaving controls, and one finding: the README still said 185. This is the failed prior-head run, not a successful hosted run of the corrected head.

`ctrl_pin.py:653` derives reaching targets from Makefile dry runs; `ctrl_pin_bench.py:11` adds a poisoned-stack control for each. The PR adds seven reaching targets in `tb/verilator/milan_dp/Makefile`: `twin8-fw`, `build-twin8-sp`, `twin-fanout`, `twin-fanout-plants`, `fan-stop-plants`, `fan-stop-plant-shared`, and `fan-stop-plant-one-index`. Thus 185 + 7 = 192. Each added target appears as an executed successful rejection control in local `figures.log`.

The conflict-free merge tree over `aa30d77f75cd97b3a29878ca0ed68010a7629266` is `0e5c07bdf20743cfa16be75379315462b53ba26d`. Every Makefile, `sw/firmware/ctrl/test/ctrl_*.py`, .gitmodules and the five initialized gitlinks is identical between that tree and the source head (`merge-tree-aa30.txt`, empty `count-merge-dependency.diff`). The count has the same inputs there. This limited tree comparison is not final current-dev candidate validation.

The fresh standalone `ctrl_boundary.population`, `figures` and `figure_controls` check uses that independently established pin count. It reports **103 defects, 8 passing controls, 5 additional boundary defects, 192 pin controls**. All four current figures agree. Restoring 185 yields exactly the named pin-count failure. Increasing each figure by one is rejected by name. No other figure changes (`figure-contract.log`, rc=0).

The supplemental complete `ctrl_pin.pin_controls` rerun reached its 600-second limit, rc=124, after **185 successful controls and no reported escaped control**. It completed the `counters` and `counters-f5` missing-prerequisite controls; the final `counters-mutants` control and six lifecycle controls did not complete. No complete local 192-control suite pass is claimed. The narrow count conclusion rests on the published executed population, seven-target derivation and unchanged merge dependencies; the fresh figure check completed. `figures.log` and `figures.rc` retain the timeout without turning it into a pass.

**Fresh documentation checks**

| Check / receipt | Result |
|---|---|
| `docs_inventory.py --check`, `docs-inventory.log` | Fresh, 541 lines; no regeneration required |
| `docs_check.py`, `docs-check.log` | Zero findings across 223 Markdown and 1,916 text files; 23/23 scrub and 4/4 routing controls |
| `check_em_dash.py --base 15168e14`, `em-dash.log` | Zero findings over 75 added lines in nine pages; 339/339 controls |
| `gen_toc.py --check`, `toc-final.log` | 160 annotated contents lists pass; 18 pages below threshold |
| `git diff --check 15168e14 HEAD`, `diff-check.rc` | rc=0 |
| `check_figure_contract.py`, `figure-contract.log` | Four figures pass; old value and four one-more mutations rejected |

The renderer-dependent gates initially refused missing html5lib, rc=2. They passed after installing only the repository's hash-locked Markdown dependencies into packet scratch. Setup refusal logs remain. These are focused fresh checks, not a rerun of all 104 documentation-workflow steps.

**Prior public findings at this head**

| ID | Severity / all attributable lenses | Disposition and cause-level evidence |
|---|---|---|
| R878-1-F1 | MINOR / Docs | Remains RESOLVED. Walkthrough `:157,175` shows enqueue/done/mask and per-input STOP; MEDIA_CLOCK_FOLLOWING `:444` names the followed match bit. Both agree with unchanged datapath connections. |
| R878-1-F2 | MAJOR / RTL, Robustness, Tests, Docs; accepted extension also Conformance | Remains RESOLVED. Monitor `:574,609,1104` checks each input's frame size; depacketizer `:311,443,497-503,571` handles truncation and the hold-only tail. FO11-FO14 and DT1-DT5 are unchanged; public current-code receipts pass 1,253 fan-out and 375 direct checks per lead. |
| R877-1-F1 | MINOR / Tests, Robustness | Remains RESOLVED. `sim_nxn.cpp` FAN STOP/START legs and `fan_stop_plant.py` are unchanged. Public round-three twin receipts catch both shared-STOP and both one-index named failures. |
| R877-1-R1 | RESIDUE / Docs | RESOLVED: TESTING `:706` retains “and passes. Its fan-out leg”. |
| R877-1-S1 | SUGGESTION / RTL | Remains IMPLEMENTED: depacketizer `:204,294` explains reset-valid/pointer qualification of unreset storage. |
| R877-2-F1 | MINOR / RTL, Robustness, Tests, Docs | Remains RESOLVED. Monitor `:362,486,500,1047,1176` retains six-bit tallies, urgency on all three dispatch paths and simultaneous-pulse preservation. FO15 `:845` independently reconciles accepted traffic, payload order, delivery tally and drops. Public receipt: 150 = 46 delivered + 104 dropped per input; three-bit/idle-only and six-bit/idle-only plants both fail by name. |
| R877-2-F2 | MINOR / Docs | RESOLVED: TESTING `:706` and `sim_fanout.cpp:706` agree on 81, 66, 99, 60, 93, 70, 63 payload octets and remainders 1-7. |
| R877-2-RS1 | RESIDUE / Tests | RESOLVED: `sim_fanout.cpp:704` points to FO14's shorter frames. |
| R877-2-RS2 | RESIDUE / Docs | RESOLVED: walkthrough `:175` and TESTING measure enqueue latency from the tap's eighth beat. |
| R877-2-RS3 | RESIDUE / Docs (PR body) | RESOLVED: current PR describes a fixed three-cycle shift register carrying each beat's valid. |
| R877-2-RS4 | RESIDUE / Docs (PR body) | RESOLVED: PR separates prior +0.017/+0.024 ns stricter-floor failures from current routes. |
| R877-2-RS5 | RESIDUE / Docs | RESOLVED: depacketizer header and datapath README retain corrected paragraph layout. |
| R878-2-R1 | RESIDUE / Docs | RESOLVED: PR roles name internal R877 and external R878. |
| R878-3-R1 | RESIDUE / Docs | RETAINED: pending-publication tense remains; exact fix below. |
| R877-2-S1 | SUGGESTION / RTL, Robustness | RETAINED, optional: late-enqueue safeguard remains unimplemented. |

These dispositions preserve the reviewers' labels. The README delta changes none of the cited causes or tests. No blocking/minor finding is cleared by moving it to another Issue.

**Remaining findings**

**R878-3-R1 - RESIDUE - Docs - PR #959 Status and checkout/publication wording.**

Authority/evidence: the PR says the correction is committed locally “for the manager to push” and becomes fetchable after that push; it is already published. Impact: stale publication tense only. Required outcome, exact fix: replace the pending-push sentence with `The correction is published on branch 948-rx-fanout.` Remove `The candidate becomes fetchable after the manager pushes it.` Keep historical source/route measurements attributed to their tested revision. Verification: compare with the published branch and review-start notice. This retains the wording-only residue; no measurement, figure, clause claim or verdict changes. Docs stays CLEAN.

**R877-2-S1 - SUGGESTION - RTL, Robustness - `hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv:263,403,435`.**

Authority/evidence: enqueue beyond the documented three-cycle latency could allocate an entry after its frame's fate was recorded. Impact: a future interface-contract violation could leave readout waiting until reset. The current parser/monitor satisfies the contract; the PR discloses the limit and FO14/FAN exercise real integration. Optional required outcome if adopted: reject/recover from late enqueue or assert the latency contract. Verification: inject over-late enqueue and require bounded recovery or an explicit assertion failure. Neither lens is unclean.

**Applied lenses and reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #948 ruling 7061889923; REQUIREMENTS REQ-VER-04; README `:255`; figure-contract.log. The correction preserves frozen fan-out acceptance and interface/standard claims. | R878-4; untouched technical coverage reaffirmed from R878-3 | 8aeb2f0bb9bfad9c486a0abf9dbeaf134d3de2fb |
| RTL | CLEAN | delta.diff; monitor urgency/frame-size and depacketizer tail/fate paths above; unchanged datapath connections. No logic, width, clock/reset, memory or interface artifact changes. | R878-4; untouched technical coverage reaffirmed from R878-3 | 8aeb2f0bb9bfad9c486a0abf9dbeaf134d3de2fb |
| Robustness | CLEAN | ctrl_pin.py `:653,881`; ctrl_pin_bench.py `:11`; ctrl_boundary.py `:420,431`; old-value and four one-more controls; prior overflow/truncation/STOP causes. Rejection and recovery behavior is unchanged. | R878-4; untouched technical coverage reaffirmed from R878-3 | 8aeb2f0bb9bfad9c486a0abf9dbeaf134d3de2fb |
| Tests | CLEAN | ctrl_boundary.py `:159,412`; seven-target Makefile delta; figure-contract.log; figures.log with explicit timeout; hashed FO15/DT5/STOP receipts. Figure oracle remains mutation-sensitive. | R878-4; untouched technical coverage reaffirmed from R878-3 | 8aeb2f0bb9bfad9c486a0abf9dbeaf134d3de2fb |
| Docs | CLEAN; retained wording residue | README `:166-185,249-255`; docs-inventory, docs-check, em-dash, toc-final receipts; issue/PR; prior corrected interface/test descriptions. No source comment added in this delta. | R878-4 | 8aeb2f0bb9bfad9c486a0abf9dbeaf134d3de2fb |

**Published evidence and real limits**

`packet-integrity.log` verifies all **507 non-review manifest entries** at publication commit `eea845dba7b561499de5cf537a5b665d72e278b1`, plus **121 author-round-three receipt hashes**, with zero mismatches. The commit has no embedded cryptographic signature; the packet supplies no detached signature/key artifact. Published-byte integrity is verified; signer authentication is not claimed. `published-spotchecks.txt` preserves bounded raw receive, mutation, twin/STOP, DT5, documentation and fit receipt sections. Large routed artifacts were not rebuilt or independently rehashed.

Round-three receipts report docs 104/104, affected runtime/mutation passes and six completed routes. Selected ExtraPostPlacementOpt routes have worst setup +0.272 ns at 8x8 and +0.193 ns at 1x1, satisfying #818's setup >= +0.030 ns and hold >= 0 at reported corners. The selected 8x8 stricter both-+0.030 failure and unselected 1x1 AltSpreadLogic_high applicable-floor failure remain failures. This README edit changes no routed input; no new route claim is made.

R878-2's positive was at `64e55a59`; R878-3's positive was at `64117b77`. Their heads are not interchangeable. R878-3 disclosed a review-order limitation, which remains in that historical record. This round's independent delta verdict/ledger preceded reading those reports. It does not privately waive an earlier procedural limitation or the separate internal-review requirement.

This is source-head review, not merge authorization. **No manager source bank exists at this exact head, and none is inferred.** Source evidence remains the author's published receipts plus the focused checks explicitly reported here. Full parent, processor, timing-plane, portability and builder banks were not run. No simulator was used by focused pin controls; their simulator substitute cannot provide RTL evidence. No complete local boundary/compiler bank or corrected-head hosted success is claimed. Skipped contexts and field skips are not executions or hardware proof. **Physical calibration NOT RUN.**

The manager owns protected hosted/act acceptance at the exact head, the then-current-dev merge candidate and builder/native banks, receipt publication, separate independent review/completion requirements, residue cleanup, explicit merge authorization and post-merge containment. Stated live dev `e275d7950ef3385753e6a15d2e191ba855b171ed` was not substituted for source base `15168e14`. The aa30 tree comparison does not discharge those duties.

Final raw-byte/mode/index verification covers 1,947 parent entries and all tracked entries of the five required registered submodules at their gitlinks (`checkout-final.log`); `status-final.txt` is clean. No source fix, commit, push, GitHub write, other-checkout edit or hardware action occurred. All invoked processes have ended. Portable scripts and reproduction instructions are included. Only MANIFEST.sha256-listed files and REPORT.md are publishable; scratch is excluded.

R878-4 FINISHED
