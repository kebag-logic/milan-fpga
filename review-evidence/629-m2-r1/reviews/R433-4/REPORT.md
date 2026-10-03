[R433] POSITIVE - exact head 2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee

# R433-4: external delta review of PR #634 (issue #629, lane M2), rounds 4 and 4b

- **Head and tree:** head `2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee`, tree `0a3979f48d426c6dbb50d00d2204fb6b4e5fba8c`.
- **Gitlinks:** `protocol-processor` `631eeb34`, `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`, `external` `efeb541a`.
- **Delta:** `1269cdaf..2bc5adc0`. Rounds 4 and 4b are the three commits since round 3's `0b066b6e`:
  - `c1288648`: the `--no-ff` merge of dev `1269cdaf`.
  - `917a78ec`: F-A512-1.
  - `2bc5adc0`: R432-3-R1 = R433-3-R1.
- **Reconstruction:** done from public state only:
  - AGENTS.md and CONTRIBUTING.md;
  - the #629 body and the round 4 and 4b assignments (`5964785948`, `5966355350`);
  - the REVIEW READY comments (`5966345440`, `5966931872`) and the PR body's Round 4 and 4b sections;
  - the diff, the history and the hosted checks at the exact head;
  - my own R433-3 findings, which I read after my pass over the diff.
- **Not read before this verdict and ledger were written:** the other reviewer's report and any private author material.
- **Evidence:** every run below was made by this reviewer, in disposable copies of the head under `scratch/`. The reviewed clone was never edited. Its index, worktree, blob modes and gitlinks equal the head (checks at the end).
- **Tools:**
  - GNU make 4.3, built from the GNU tarball (sha256 `e05fdde4...8e19`, verified);
  - the pinned Verilator 5.050 (`verilator --version`: `Verilator 5.050 2026-07-01 rev v5.050`).

## Verdict

**POSITIVE.** No finding is open at BLOCKER, MAJOR or MINOR, and all five lenses are covered clean at this head. The report records two RESIDUE items (wording only) and no new SUGGESTION. R433-3-S1 is retained as the manager's to file.

## Assignment items judged

### (1) The merge keeps both sides

The merge was re-done in a scratch clone: `0b066b6e` checked out, then `git merge --no-ff 1269cdaf`.

- **Conflicts:** exactly the three the assignment names: `CHANGELOG.md`, `docs/design/MEDIA_CLOCK_FOLLOWING.md` and `scripts/naming.budget`.
- **Auto-merged files:** I compared each with the published merge `c1288648` by blob id. `PNG_MANIFEST.json`, the three `submodule_boundaries.*` files, `REGISTER_MAP.md`, `SUBMODULES.md`, `KL_pp_shadow.sv`, the `protocol-processor` gitlink, `measure_test_evidence.py` and `rom_digests.tsv` are SAME.
- **The one other difference:** `scripts/port_docs.budget:21`, where the comment `hdl 1916` became `hdl 1940`. This is the generator's re-recording. My `check_port_contracts.py --write-budget` at the head reproduces the tracked bytes, and no ratchet number moved.
- **No other change:** outside the three conflict files, the published merge has no change beyond git's own auto-merge (`git diff c1288648` excluding the three files: only that comment line).
- **`CHANGELOG.md`:**
  - `git diff 0b066b6e c1288648` adds exactly dev's index line and its "processor pin 631eeb34" section.
  - `git diff 1269cdaf c1288648` adds exactly this lane's index line and its "AAF or CRF media-clock following" section.
  - The two sections are each byte-identical to their parent's, and the lane's section comes first.
- **`MEDIA_CLOCK_FOLLOWING.md`:**
  - Lines 6-12 keep "**Implemented by lane M2**" together with dev's "then-pinned submodule commit `b2db3a97`".
  - They add "Its processor part **landed at `631eeb34`**", linked to `#protocol-processor-changes`.
  - Dev's auto-merged "**Status: landed at `631eeb34`.**" bullet is at `:1284-1292`.
  - Its two processor citations hold at the pin: the range-check comment is at `protocol-processor/hdl/aecp/ucode/gen_ucode.py:1654-1663`, and the `E_SCLKS` program with its refusal tail at `:1674-1711`. The anchors pass `gen_toc.py --verify-anchors`.
- **`scripts/naming.budget`:**
  - The conflict was only the header count, 95 against dev's 96.
  - `measure_naming.py --write-budget` at the head regenerates the tracked file byte for byte. It keeps 95 because this lane removed the servo's `crf_rate_i`, which dev's 96 still counted.
  - `submodule_boundaries.gen.py` also rewrites byte-identically (receipt `docs_replay.log`: no tracked change after the three generators).
- **Auto-merged content:** each side is compatible with the other.
  - `REGISTER_MAP.md:1020` is dev's `ADP_IDX0` meaning.
  - `measure_test_evidence.py` gains dev's two processor campaign dispositions beside this lane's entries.
  - `KL_pp_shadow.sv` gains dev's `EN_IDENTIFY_NOTIF_P (1'b0)` and `identify_button_i (1'b0)` tie-offs.

### (2) The shipping image at the merge

- **What I could check:** the published figures are internally consistent with the XC7A100T totals:
  - LUT 50,767 / 63,400 = 80.07 %;
  - slices 15,832 / 15,850 = 99.89 %;
  - registers 59,634 / 126,800 = 47.03 %;
  - BRAM 92.5 / 135 = 68.52 %;
  - DSP 14 / 240 = 5.83 %;
  - round 2's LUT 51,051 = 80.52 %.
- **Where they are reported:** WNS +0.193 ns, WHS +0.024 ns, 0 critical warnings and the #607 line are stated in the REVIEW READY comment and the PR body Round 4 table, with the bitstream's sha256.
- **No STOP condition:** no resource is above 100 % and both slacks are positive.
- **Round 4b:** it changes no RTL, so the round-4 image stands for this head. `git diff c1288648..2bc5adc0` touches only `gmstep_mutants.py` and the design page.
- **Limit:**
  - The Vivado timing and utilization reports are not in the public evidence tree (`review-evidence/629-m2-r1` at `f7cb2d68` holds only round 1's handoff and PR body).
  - No Vivado installation is reachable from this unit, so I did not rebuild the image.
  - Item (2) is therefore judged on the published figures and their arithmetic, not on reports I opened. Publishing them is listed under manager duties.

### (3) F-A512-1 and the 45-anchor claim

**The fix.**

- The request is at `hdl/milan/milan_datapath.sv:3229-3232`: `(crf_clk_selected_r & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w)) | aafm_disrupt_p_w | aafm_mr_toggle_p_w`.
- At dev `cdf49d1a:3155-3156` it was a pure AND chain, so dev's "append `& ~media_rebase_p_w` to the last line" vetoed the CRF restart there.
- On this lane, the same text binds to `aafm_mr_toggle_p_w` alone.
- The fix at `tb/verilator/milan_dp/gmstep_mutants.py:231-232` plants `CRF_RESTART_TERMS[:-1] + " & ~media_rebase_p_w)"`. The planted request reads `(crf_clk_selected_r & (...) & ~media_rebase_p_w) | aafm_disrupt_p_w | aafm_mr_toggle_p_w` (receipt `anchor_probe.txt`). This is the named defect.
- The comment at `:65-67` says why.

**Results.**

- `make -j16 gmstep-mutants` (`--all`), make 4.3 and pinned Verilator: **22 checks, 22 PASS**. Both clean legs pass. The control breaks exactly one check, its named "coincident: a PHC step does not suppress the CRF restart" (`gmstep_all.log`).
- My own probe (`scripts/coincident_probe.py`) runs through the campaign's own `run_control`. It gave 3/3 as expected:
  - **V1** vetoes the whole selected-CRF group with a different text: CAUGHT by the named check, which therefore grades the behaviour and not the anchor text.
  - **V2** is round 4's published form: SURVIVES, which reproduces the disarming.
  - **V3** vetoes only the received-toggle term: CAUGHT, so the coincident check exercises the `mr`-toggle cause.

**The anchor claim (spot-checked in full).**

- `scripts/anchor_probe.py` imports the five campaigns' own tables and applies each control's edits in order, as the campaign does.
- **All 45 anchors are found exactly once:** render 4, render-CSR 3, crflic 6, gsi 12 (11 in the processor top, 1 in the datapath), gmstep 20.
- **No anchor from render, render-CSR, crflic or gsi** lies in the request or on a line this lane changed since `cdf49d1a`.
- **Eight gmstep controls lie in the request:**
  - six OR a cause onto the whole request;
  - one rewrites the CRF group;
  - one is the fixed veto.
- The probe prints each planted request. None of the others is disarmed by the new precedence.
- The PR body's per-campaign split gives gsi 11 ("ten in the processor top"). That is the only miscount, and it is wording: R433-4-R2.

**Other campaigns at this head (make 4.3):**

- `crflic-mutants`: 7/7.
- `gsi-mutants`: 9/9, with the processor half planted in copies at `631eeb34`.
- `render-csr-controls`: 4 checks, 0 failures. The wrong-fill and bit-9 mutants fail their named checks, and the absent stage passes.

### (4) Re-measure under GNU make 4.3

**The `milan_dp` shard.**

- I ran `scripts/run_all_suites.sh <logs> --shard 4/5` as the hosted step, from a fresh copy under make 4.3: rc 0, 1/1 suite, **11,839 checks, 0 in-suite failures**.
- The sweep's `render_mutants.py` was 6/6 and `gmstep_mutants.py` 6/6.
- All 264 `[CLKSRC-WALK]` (212) and `[CLKSRC-RANGE]` (52) lines read `ok` at processor `631eeb34`. This is SET/GET_CLOCK_SOURCE over the longer list, with the unlisted index refused.
- This equals the author's tally.

**The docs gates.** Steps 7, 9, 12, 14, 15, 19, 30, 31, 32, 35, 36, 37, 39, 43, 45, 47 and 49 of `docs-check` ran verbatim from `docs.yml`, under make 4.3 and the pinned Markdown environment: every step rc 0 (`docs_replay.log`). Among them:

- the Entity shape gate `check_entity_shape.py --self-test`: RESULT PASS;
- `measure_naming --check`;
- `check_port_contracts`;
- `measure_test_evidence --check`;
- `gen_toc --check` and `--verify-anchors`;
- `check_doc_paths`;
- the Python idiom gate;
- the em-dash gate against `1269cdaf`: 0 findings over 541 added lines.

**The root suite.** It is not touched by round 4b, but the pin feeds it. `milan_dp_mclk` `make -j16 run` gave legs 55/0, 32/0 and 50/0, and campaign 31/31.

**Capture gate.** Unchanged, by the assignment's rule. The merge touches no capture census or firmware input. `check_nvm_capture` is in the manager's bank.

**Hosted, exact head.** These are observed results, not my acceptance; the manager owns hosted acceptance.

- At 08:31 UTC: `docs-check` success, with Entity shape 222/0 and em-dash 0 over 541 from its log; `docs-check-no-git`, `wire-accountability`, `rtl-fast`, `changes`, `verilator-lint`, `bdd-conformance`, `full-ci-gate`, `elaborate`, `yosys-elaboration` and Yosys shards 0-3 success; Verilator shards 0, 3 and 4 success.
- Shards 1 and 2 were still running. `verilator-suites` and `yosys-portability` had not reported.
- `Physical gPTP` was skipped (schedule or dispatch only).

## Findings

No BLOCKER, MAJOR, MINOR or new SUGGESTION.

### RESIDUE (owner rule 2026-10-02: wording only; no effect on verdict or lens)

- **R433-4-R1** (lenses Docs, Tests): `scripts/measure_test_evidence.py:681`.
  - **Evidence:**
    - The `DUT_READER_DISPOSITIONS` prose for `tb/verilator/milan_dp_mclk/mclk_mutants.py` says the campaign plants "the #629 design's fourteen named root defects".
    - `mclk_mutants.py` has 16 (`len(MUTANTS) == 16`), and the campaign reports 31/31.
    - `tb/verilator/milan_dp_mclk/README.md:16`, `mclk_mutants.py:13` and `docs/testing/TESTING.md:517` all say sixteen.
    - The author disclosed it as not taken.
  - **Why it is wording only:** the string is a human-readable reason. The ratchet keys on the path, and the text is only printed in its listing. Changing it moves no count, check, verdict or generated file.
  - **Exact fix:** "fourteen named root defects" becomes "sixteen named root defects".
- **R433-4-R2** (lenses Docs, Tests): the PR body, Round 4b table, item 1, second row.
  - **Evidence:** "gsi (11, ten in the processor top)". The campaign table gives 12 anchors, 11 of them in the processor top (`receipts/anchor_probe.txt`). The 45 total and every other figure in the row are right.
  - **Exact fix:** "gsi (11, ten in the processor top)" becomes "gsi (12, eleven in the processor top)".

## Prior public findings at this head

| Finding | Severity | State at `2bc5adc0` | Evidence |
|---|---|---|---|
| F-A512-1: gmstep coincident control disarmed by the reshaped request | (ruled fix-in-PR) | **CLOSED** | `gmstep_mutants.py:231-232`; `--all` 22/22, named check only; V1 caught, V2 survives |
| R432-3-R1 = R433-3-R1: "The last two" in the meter Outputs bullet | RESIDUE | **TAKEN** | `MEDIA_CLOCK_FOLLOWING.md:1000-1003` carries the exact replacement text, once; "The last two" is absent |
| R432-3-S1 = R433-3-S1: the shape gate's database read counts a parse stopped by `$(error)` as readable (outside #629) | SUGGESTION | RETAINED, the manager's to file | untouched by rounds 4 and 4b |
| Earlier rounds' findings (R432-1, R433-1, R433-2 F1, R432-2) | various | remain CLOSED | rounds 4 and 4b touch none of their artifacts except the design page lines above; the root suite and its campaign still pass |
| The author's own "fourteen" disclosure | n/a | recorded as R433-4-R1 | above |

## Lens results

```text
[R433] PASS Conformance - git re-merge of 0b066b6e+1269cdaf vs c1288648 (blob compare); CHANGELOG.md both sections; MEDIA_CLOCK_FOLLOWING.md:6-12,1284-1292 against gen_ucode.py:1654-1711 at 631eeb34; milan_dp [CLKSRC-WALK] 212 / [CLKSRC-RANGE] 52 ok at the new pin; the coincident check (IEEE 1722-2016 4.4.4.3/10.4.3, #602 ruling) graded again - both sides kept, the clause behaviour graded
[R433] PASS RTL - git diff 0b066b6e..2bc5adc0 -- hdl (only dev's KL_pp_shadow.sv tie-offs) plus the gitlink 631eeb34; milan_datapath.sv:3229-3232 request unchanged since round 3; milan_dp, mclk, crflic, gsi, gptp/gmstep legs elaborated and passed at the new pin; shipping-image figures arithmetic-consistent (reports not public: limit)
[R433] PASS Robustness - coincident PHC-step-with-CRF-restart path graded (V1 group veto and V3 toggle-only veto both caught by the named check); every control anchor fails closed (count == 1, 45/45); unlisted clock-source index refused at the new pin (52 RANGE ok); sweep preflight cancellation controls pass under default signal dispositions
[R433] PASS Tests - gmstep_mutants.py --all 22/22 (named check only); coincident_probe.py 3/3; anchor_probe.py 45 anchors; crflic 7/7; gsi 9/9; render-csr-controls 4/0; shard 4/5 11,839 checks 0 failures; milan_dp_mclk 55/32/50 and 31/31 - each control fails for the defect it names
[R433] PASS Docs - CHANGELOG.md, MEDIA_CLOCK_FOLLOWING.md:6-12,1000-1003; naming.budget, port_docs.budget and the boundary diagram regenerate byte-identical; docs-check steps replayed rc 0 under make 4.3 (em-dash 0/541 vs 1269cdaf); PR body Round 4/4b checked against receipts - wording residue R433-4-R1, R433-4-R2 only
```

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Re-done merge vs `c1288648`; `CHANGELOG.md`; `MEDIA_CLOCK_FOLLOWING.md:6-12,1284-1292`; `gen_ucode.py:1654-1711` at `631eeb34`; `milan_datapath.sv:3229-3232`; CLKSRC walk and range at the new pin | R433-4 | `2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee` |
| RTL | CLEAN | `git diff 0b066b6e..2bc5adc0 -- hdl` (`KL_pp_shadow.sv` tie-offs only) and the `631eeb34` gitlink; elaborations of five `milan_dp` legs and the root suite at the head; shipping-image figures (published, arithmetic checked) | R433-4 | `2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee` |
| Robustness | CLEAN | Coincident-event probes V1 to V3; anchor fail-closed check over 45 anchors; range refusal at the new pin; suite preflight cancellation | R433-4 | `2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee` |
| Tests | CLEAN (R433-4-R1 and R2 are RESIDUE) | `gmstep_mutants.py:65-68,231-232`; `--all` 22/22; `crflic` 7/7; `gsi` 9/9; `render-csr-controls`; shard 4/5; `milan_dp_mclk` run and campaign; reviewer probes | R433-4 | `2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee` |
| Docs | CLEAN (R433-4-R1 and R2 are RESIDUE) | `CHANGELOG.md`; `MEDIA_CLOCK_FOLLOWING.md`; `naming.budget`; `port_docs.budget`; boundary diagram regeneration; docs-check replay under make 4.3; PR body Round 4 and 4b; `measure_test_evidence.py:681` | R433-4 | `2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee` |

## Real limits

- **Shipping image:**
  - I did not rebuild it, and its Vivado reports are not in public evidence. Item (2) rests on the published figures, which are arithmetic-consistent, and the bitstream digest.
  - Slices at 99.89 % leave 18 slices of headroom.
- **Replay coverage:**
  - Not replayed by me: the other four Verilator shards, the Yosys shards, the builder and native banks, `elaborate`, `bdd-conformance`, and `docs-check` steps 1-6, 10-11, 13, 16-18, 20-29, 33-34, 38, 40-42, 44, 46 and 48 (provisioning, SDK and builder steps).
  - The hosted runs at the exact head and the manager's banks cover them. `act_ci.py --selftest` was not run (AGENTS.md section 5).
- **Two discarded first attempts:** both are kept under `receipts/attempt1/`, and neither is a reported result.
  - The first shard launch came from a non-interactive background job with SIGINT ignored. The sweep's cancellation preflight then timed out ("cancel-transition-SIGINT") before any suite ran. The relaunch through `scripts/sigdfl_exec.py`, with default dispositions, is the reported run. This is the same class of hazard as the author's disclosed `nohup` attempt.
  - My first probe run used threads with a shared stdout capture, which garbled its log. The reported run uses processes.
- **Out of scope, not this PR:** dev's own dispositions for `crflic_mutants.py` ("one of three") and `gmstep_mutants.py` ("for two, the option-off leg", "three #387 acceptance names") were already stale at `cdf49d1a`. The lane did not touch them.
- **Not tested here:** physical calibration and hardware; field skips are not hardware proof.

## Pending manager duties

- Hosted acceptance at the exact head: Verilator shards 1 and 2, `verilator-suites` and `yosys-portability` had not finished at 08:31 UTC.
- The builder (48) and native (5) banks, the merge candidate on live dev `1269cdaf`, and act.
- Publish the round-4 Vivado timing and utilization receipts, if wanted, for a cold reader of item (2).
- Carry R433-4-R1 and R433-4-R2 to the residue checklist.
- File R433-3-S1 if wanted.

## Integrity of the reviewed clone

- After all runs, `git rev-parse HEAD` gives `2bc5adc0...`, and `HEAD^{tree}` gives `0a3979f4...`.
- `git diff --quiet HEAD` and `git diff --cached --quiet` both return 0.
- `git status --porcelain --ignored` is empty. Two `__pycache__` directories my import probe created were removed.
- The gitlinks are `631eeb34`, `5dce647a`, `48ff7a7e` and `efeb541a`, and the `protocol-processor` worktree is clean.

R433-4 FINISHED
