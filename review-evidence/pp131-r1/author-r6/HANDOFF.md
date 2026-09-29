# [A442] Round 6 handoff: processor #131 / PR #132

Status: **all three round-6 items done; no STOP.** One commit, test and docs only; no RTL
change.

Head `9b4da6b5753fec8f5b2bba605c47af56c6cf1a0f` on branch `131-d3-core-scalars` (round-5 head
`9dce84ea`, base `c951a9ff`). Not pushed; the PR is not edited (PR-BODY.md carries a Round 6
section and the consolidated parent-visible list, moved there).

Assignment: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/131#issuecomment-5885497133 ·
TAKEN https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/131#issuecomment-5885505757 ·
REVIEW READY https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/131#issuecomment-5886545587 ·
reviews R390-5 (PR #132, 5884919813, NEGATIVE on F1) and R391-5 (5885492313, POSITIVE, S1
and S2).

## Commit

| Item | Commit | Subject |
|---|---|---|
| 1 R390-5 F1 = R391-5 S1, and 2 Docs | `9b4da6b` | Grade the owned half of the owner-matched drain: manager 1's abort held while manager 0 owns each of the walk's READs drains none of them, and list the manager-0 halves no in-tree manager presents |
| 3 PR body | (PR-BODY.md only) | Round 6 section; consolidated list with R391-5 S2 and the ungraded manager-0 inputs |

The assignment asks for one commit; items 1 and 2 are that commit. `9dce84e..9b4da6b`: 6 files,
+142 / -26 (`tb/acmp_nvm/{sim_main.cpp, acmp_nvm_wrap.sv, README.md}`, `tb/pp_top/{d3_mutants.py,
README.md}`, `docs/architecture/09_verification.md`). `git diff --quiet 9dce84e 9b4da6b -- hdl syn
scripts .github Makefile` is true. Line numbers below are at `9b4da6b`.

## Items: change and proof

**1. The owned half of the owner-matched drain (R390-5 F1 = R391-5 S1).**
- Authority: contract section 6.4 (`drain' = ... (owner = writer AND m_abort) OR (owner = binding
  AND m0_abort)`), the arbiter's owned terms `KL_pp_nvm_mgr_arb.sv:157-160`, its banner `:38-65`.
- Harness (`tb/acmp_nvm/sim_main.cpp`):
  - state `:325-335`: `m1_abort_over_m0` (the stimulus), `m0_rd_own` (manager 0 owns a READ this
    cycle) and the counters `m0_own_cyc`, `m0_own_cyc_m1_abort`, `m0_own_rds`, `m0_own_span`,
    `m0_own_span_min`;
  - drive `:661`: manager 1's abort is `m1_abort_over_m0 && m0_rd_own`, alone (no request);
  - monitor `:691-705` (`sample_m0_owned_read()`, called at `:787`): a READ is owned from the
    cycle after its issue (`:791` sets `m0_rd_own` in the issue cycle's sample) through the
    port's done or err, the pulse the arbiter's ownership retires on (`end_w`); it counts owned
    cycles, those carrying manager 1's abort, the READs whose ownership ended, and the fewest
    owned cycles before any READ's end (where an armed drain would take effect); reset `:863-865`;
  - N11d `:2702-2722`: seed sinks 0 and 7, reset, hold the abort over manager 0's owned READs, run
    the walk. The check requires the walk complete as saved (`l_walk_ok`, no fail, cause 0),
    nothing written (`l_nvm_untouched`), 8 READ issues and **none carrying the abort** (so N11b
    and N11d each grade one term), 8 READs whose ownership ended, **the abort in every owned
    cycle** and at least one before each READ's end, no drain, no leak, no binding abort.
  - The N11 banner (`:2619-2633`) names N11d and the ungraded manager-0 halves.
- Wrap (`tb/acmp_nvm/acmp_nvm_wrap.sv:88`, `:544`): `arb_end_o = np_done_w || np_err_w`, the
  port's done or err. Test bench only.
- Non-vacuity at the head (`receipts/n11d-counts-9b4da6b.txt`, a scratch extract with one
  print-only line): the abort is present in **168 of the 168 owned cycles** over the **8** READs,
  at least **12** of them before each READ's end, in **0 of the 8** issue cycles; no drain.
- Mutants (`tb/pp_top/d3_mutants.py:399-414`), both `ACMP_NVM`, named check
  `N11d manager 1's abort held while manager 0 owns each of the walk's READs`:
  - `owned_arm_cross_intent`: both owned terms take either manager's abort (R390-5's
    `r5_owned_cross_both`);
  - `cross_own_m1_drains_m0`: manager 0's owned term takes manager 1's abort (R391-5's own text;
    R390-5's `r5_owned_cross_m0_only`).
  Both KILLED, 1 failing check each (N11d only): the walk's first READ is drained from its second
  owned cycle, the binding manager never sees its bytes or done and fails the walk on its
  per-wait deadline ("present in 45 of the 45 cycles manager 0 owned its 1 READs ... the walk is
  not done, or failed"). README rows `tb/acmp_nvm/README.md:386-387`.
- STOP check: not applicable this round (no STOP condition); the head's arbiter passes N11d as its
  banner states.

**2. Docs.**
- `docs/architecture/09_verification.md:192`: the row names manager 1's half of each rule as
  graded (its WRITE with an abort never drained, N11a; its abort draining none of manager 0's
  READs, N11b in the issue cycle and N11d while owned; after its WRITE an issue-cycle READ abort
  still drained, N11c) and the manager-0 halves as ungraded by construction, pointing at the
  README. `:200-201`: 83 controls.
- `tb/acmp_nvm/README.md`: 360 checks (`:8`); N11a-d (`:213-235`); **"Ungraded by construction:
  the manager-0 halves of the same rules"** (`:236-263`): why (the binding manager raises
  `nvm_abort_o` only in a stalled `H_RS_STREAM` clock, so only while its own READ is strobed or
  owned; its issue-cycle abort needs an aggregate expiry, inside the restore walks, where both
  managers only read), the five inputs as R391-5 S1 counts them (its six single-half edits less
  the one N11d now grades), each with the reviewer edit and the out-of-tree probe:

  | Input manager 0 never presents | Edit | Out-of-tree probe (measured at `9b4da6b`) |
  |---|---|---|
  | its abort in manager 1's issue cycle | `cross_iss_m0_drains_m1` = `r5_issue_cross_m1_only` | R390-4 unit probe case F kills it |
  | its abort while manager 1 owns a READ | `cross_own_m0_drains_m1` = `r5_owned_cross_m1_only` | no probe kills it (unit probe 9/9); R391-5 monitor: input absent |
  | its WRITE strobe with its abort | `write_iss_m0_only` | unit probe case B kills it |
  | its abort while it owns a WRITE | `write_own_m0_only` | no probe kills it (unit probe 9/9); monitor: input absent |
  | its issue-cycle READ abort after a WRITE | `stale_we_m0_only` | unit probe case B kills it (the WRITE half of the same edit); monitor: input absent |

  (`receipts/unit-probe-r391-5-mutants-9b4da6b.txt`; R391-5's `monitor-arbiter-inputs.txt`: no
  monitored input with both real managers over `tb/pp_top` and 17,406 sweep runs.)
- Mutation record `:365-387`: "All eleven", "The seven N11 controls", two rows.
- `tb/pp_top/README.md:667-669`: seven own-contract controls, 83 KILLED.

**3. PR body.** PR-BODY.md keeps its `[A418]` first line and `Closes #131`. Round 5's section now
points to Round 6 for the list; the Round 6 section has the three items, the consolidated list
"rounds 1-6" (round 5's, unchanged, plus two additions) and the evidence at `9b4da6b`:
- Behaviour, "Round 6": the arbiter's rules graded for manager 1's half (N10, N11a-d) and the
  binding walk's issue-cycle drain (D3R18); the five manager-0 inputs listed, ungraded by
  construction, with the obligation that whatever makes manager 0 present one grades it first.
- `sim_nxn.cpp` legs, R391-5 S2: with `[AECP-WTMO]` moved after
  `grade_the_first_descriptors_on_the_wire()`, the word-36 check ("[AECP-IMG] the response
  buffer reports no fault (word 36)") runs before the wedge and no longer shows that the response
  master's fault clears after a heal; the real edit re-reads word 36 after the arm, or keeps the
  arm and adds a word-36 read to its heal. Stale comments: `:2547-2549` ("parked in S_BAD with
  FAULT_TIMEOUT from the two sections above") and `:2560-2562` ("[AECP-WTMO] already moved the
  error counter"), the two that R391-5 names, plus `:2605-2607` ("[AECP-WTMO] added one deliberately"),
  the same kind, found this round. Line numbers are in the scratch `sim_nxn.cpp` at dev
  `eaa88a32` with the edits (arm call `:2484`, word-36 check `:2609-2610`).
- `parent_edits.py` is byte-identical to round 5's (sha256 `80d2c396…`); its diff at the gate
  parent equals round 5's `parent-edits.diff` apart from index lines.

## Section 15.2 table and sweep

All 37 rows remain applied. [TABLE-15.2.md](TABLE-15.2.md) adds a round-6 column: 3 rows
updated (9: 09 section 8.2; 28: the `acmp_nvm` README and wrap; 29: the `pp_top` README), 34
unchanged. Named sweep at the head ([SWEEP.md](SWEEP.md), `sweep_reconcile.py` unchanged):
**705 matching lines, 358 rewritten or added by this lane, 347 with a location-specific scope
reason, 0 unreviewed**. The one new match is N11d's `restore_fail_o` line
(`tb/acmp_nvm/sim_main.cpp:2712`); the README's `360 checks` line replaces `359 checks`.

## Negative controls

[MUTANTS.md](MUTANTS.md): the full campaign at the head, **83 of 83 KILLED**, goldens PASS
(acmp_nvm, pp_top, rx_validator), every count equal to its README row (R391-5's
`check_readme_counts.py`: 86 entries, 0 problems). The round-6 additions:

| Control | Defect planted (`KL_pp_nvm_mgr_arb.sv:157-160`) | Named assertion that fails | Failing checks |
|---|---|---|---:|
| `owned_arm_cross_intent` (R390-5 `r5_owned_cross_both`) | both owned terms take either manager's abort | `N11d manager 1's abort held while manager 0 owns each of the walk's READs` | 1 |
| `cross_own_m1_drains_m0` (R391-5; R390-5 `r5_owned_cross_m0_only`) | manager 0's owned term takes manager 1's abort | `N11d manager 1's abort held while manager 0 owns each of the walk's READs` | 1 |

Every other control's count is unchanged from round 5 (`issue_arm_cross_intent` still 1, N11b
only).

The reviewers' round-5 scripts at `9b4da6b` (receipts):
- **R390-5 `r5_extra_mutants.py --suites acmp_nvm`** (`r390-5-extra-acmp-9b4da6b.txt`): golden
  PASS; `r5_owned_cross_m0_only` **KILLED by N11d** (the verification F1 names);
  `r5_owned_cross_both` KILLED by N11d; `r5_issue_cross_m0_only` KILLED by N11b;
  `r5_issue_cross_m1_only` and `r5_owned_cross_m1_only` pass (manager-0 halves, ungraded by
  construction, listed); `r5_identity` passes (sanity).
- **R390-5 `r5_owned_cross_probe.py`** (`r390-5-owned-probe-9b4da6b.txt`): its anchors still
  plant; probe at the head 361 of 361; probe plus `r5_owned_cross_m0_only` fails R5P and N11d;
  the unmodified tree harness plus that edit now fails N11d (rc 2), where round 5 passed.
- **R390-5 `run_arb_unit_mutants.py`** (`r390-5-arb-unit-9b4da6b.txt`): byte-identical to
  R390-5's `arb-unit-r5.txt` (the arbiter is unchanged): head 9 of 9.
- **R391-5 `run_r391_5.sh ... acmp [MUTANT]`** for the golden and all 16 edits
  (`r391-5-acmp-mutants-9b4da6b.txt`): golden 360 of 360; **`cross_own_m1_drains_m0` fails
  N11d** (the verification S1 names); every other count equals R391-5's round-5 receipt.
  Passing `tb/acmp_nvm`: the five manager-0 halves and `issue_arm_m1_only` (D3R18 kills it in
  `tb/pp_top`, as before). The monitor over `tb/acmp_nvm`: only manager-1 kinds, and
  `m1_abort_on_m0` now at its 20-line cap (R391-5 counted 8, N11b's issue cycles).
- **R391-5 `check_readme_counts.py`** on the gate campaign (`r391-5-readme-counts-9b4da6b.txt`):
  86 entries, 0 problems.
- R391-5's `d3`, `full`, `d1` and `sweep` probes were not rerun: `tb/pp_top` and every file under
  `hdl/` are unchanged since `9dce84e`.

## DR3a measurements

`./obj_dir/Vpp_top_sim --dr3a` from the gate clone's `tb/pp_top` default build at `9b4da6b`:
**byte-identical** to round 5's receipt (`cmp`; [receipts/dr3a-9b4da6b.txt](receipts/dr3a-9b4da6b.txt)),
as it must be with no file under `hdl/` changed. Carried table (clocks from `restore_go_i`;
the wrap's nominal clock is 1,000,001 Hz, so RS_TMO = 20,001 and AGG = 1,000,001 clocks; a cycle
is 20 ns at 50 MHz and 10 ns at 100 MHz):

| Path | Terminal | go to release | go to terminal (cycles) | 50 MHz | 100 MHz |
|---|---|---:|---:|---:|---:|
| erased device, DRAM 31 | COMPLETE | 122 | 1,286 | 25.7 µs | 12.9 µs |
| nine records, DRAM 31 | COMPLETE | 122 | 1,989 | 39.8 µs | 19.9 µs |
| erased device, DRAM 143 | COMPLETE | 122 | 1,734 | 34.7 µs | 17.3 µs |
| nine records, DRAM 143 | COMPLETE | 122 | 2,661 | 53.2 µs | 26.6 µs |
| pass 0 DEVICE error | DEFAULTS (2) | 122 | 813 | 16.3 µs | 8.1 µs |
| pass 1 rule fetch error, roll-back | DEFAULTS (6) | 122 | 1,554 | 31.1 µs | 15.5 µs |
| pass 1 fetch 16,000 late, roll-back on debt | DEFAULTS (6) | 122 | 17,539 | 350.8 µs | 175.4 µs |
| NVM silent from its first read | DEFAULTS (3) | 20,003 | 40,006 = 2 x RS_TMO + 4 | 2 x 20 ms | 2 x 20 ms |
| image refused (magic) | CLOSED (7) | 122 | 164 | 3.3 µs | 1.6 µs |
| descriptor memory silent | CLOSED (7) | 122 | 8,188 | 163.8 µs | 81.9 µs |
| every grant 200 inside the per-wait deadline | DEFAULTS (3) | 158,530 | 1,000,000 (= AGG) | 1,000 ms | 1,000 ms |
| every READ byte just inside the per-wait deadline | DEFAULTS (3) | 1,000,002 | 1,000,004 (AGG + 4) | 1,000 ms + 80 ns | 1,000 ms + 40 ns |

Unchanged too (`tb/pp_top` 7,888 of 7,888 at this head): D3R18 +4, D3R19 +546 and +272, D3R20 +1,
D3R21 +5 clocks after the bound; longest healthy waits 405 / 853 cycles (DRAM 31 / 143), binding
12; DR2a producer share 50,028 bench cycles. The integrator's bounded wait stays 1,000 ms plus two
per-wait deadlines plus a few clocks (1,060 ms a margin). Submitted, not self-ratified.

## DR4 scalar-stage contribution

No synthesized file changed (`git diff 9dce84e 9b4da6b -- hdl syn` is empty), so the synthesis
input is identical to round 5's and Vivado was not re-run this round. Carried from round 5's
same-session measurement (Vivado 2026.1 out-of-context, the shipping 1x1 shape): lane 1 is
**+1,031 LUT / +559 FF / 0 BRAM / 0 DSP**; round 6 adds 0. Against the 2,500 LUT / 1,400 FF
scalar-core ceiling for lanes 1-2, 1,469 / 841 remain for lane 2. Post-place and the 8x8
post-place obligation stay lane 2's (open, not waived).

## Parent-visible changes (for the pin-adoption lane)

- **No processor port, parameter or behaviour change** (no RTL change). The `tb/acmp_nvm` wrap
  tap is test-bench only; no parent file builds that wrap.
- The consolidated list moves to PR-BODY.md "Round 6", unchanged apart from two additions:
  the five manager-0 arbiter inputs no in-tree manager presents (R391-5 S1: carry the accurate
  list, not "one input"), and R391-5 S2 in the `sim_nxn.cpp` legs (the word-36 check order, three
  stale comments).
- `parent_edits.py` unchanged (12 files); not re-edited for S2, which belongs to the real edit.

## Suites and gates

[GATES.md](GATES.md): every command with rc, seconds, log size and SHA-256, run by
[gates.py](gates.py) (round 5's runner, unchanged) with the pinned Verilator 5.050 wrapper. The
processor clone is a clean clone of the lane at `9b4da6b` with PR #13's head fetched read-only
(for `nvm_port figures`); the parent is a clone of the read-only checkout at dev `eaa88a32`
(`mk_parent.sh`), gitlink at `9b4da6b`, with `parent_edits.py` applied.

| Tree | Entry point | rc |
|---|---|---:|
| processor | `./scripts/run_suites.sh` (33 suites, 1,016,036 checks, 0 failing; `tb/pp_top` 7,888, `tb/acmp_nvm` 360) | 0 |
| processor | `./scripts/lint_hdl.sh` | 0 |
| processor | `make -j1 check` (lint, WaveDrom, links 968, matrices, params 26/26/26, stale) | 0 |
| processor | `python3 scripts/gen_matrix.py --check` | 0 |
| processor | `./syn/yosys/run.sh` | 0 |
| processor | `make -C tb/nvm_port figures` | 0 |
| processor | `git diff --check c951a9ff HEAD` | 0 |
| processor | `python3 tb/pp_top/d3_mutants.py` (83 of 83 KILLED, goldens PASS, 83 README counts equal) | 0 |
| processor | `make -C tb/srp_top mutants` (64 checks, coverage 49/49) | 0 |
| parent | the manager's 16 commands (C++ and Python idiom, xvlog, RTL source lists, `pp_srcs`, builder tests, `pp_shadow`, port contracts, naming, evidence classifier, docs, `lint_rtl`, `nvm_cosim` lint and quick, `milan_dp`, `milan_dp_render`), every reading equal to round 5's | **16 of 16 rc 0** |

`ax1x1gptp` (outside the set, about 55 minutes) was not rerun: no processor file it builds changed
since `9dce84e`, where it passed 139 of 139. The processor gate clone's `git status` was empty
after the gates.

Before the commit, the same diff also passed the parent's C++ and Python idiom gates in a scratch
parent (the first attempt found `sample_producers()` over the 100-line function ratchet; the
owned-cycle monitor moved into `sample_m0_owned_read()`).

## Notes for review

1. **N11d presents the abort only in owned cycles, never in the issue cycle.** That keeps the
   two terms apart: `issue_arm_cross_intent` still fails N11b alone and the owned edits fail N11d
   alone. Together N11b and N11d cover every cycle of each READ.
2. **Ownership is modelled from the issue to the port's done or err**, the contract's definition
   (section 6.4: `owner'` retires on done or err), not read from the arbiter's `own_r`, so a
   mutant cannot move the stimulus. The new `arb_end_o` tap is the port's own pulse.
3. **Two manager-0 inputs have no out-of-tree kill.** R390-4's unit probe does not present
   manager 0's abort while manager 1 owns a READ, or while manager 0 owns a WRITE. The README says
   so; for those two the evidence is structural (the binding manager's abort) and R391-5's
   monitor.
4. **A third stale `sim_nxn.cpp` comment** (`:2605-2607`, "[AECP-WTMO] added one deliberately")
   is named with R391-5's two; it has the same cause.
5. R390-5's reviewer probe R5P still plants on the head (its anchors are untouched), so that
   reviewer can rerun it unchanged.

## Packet

HANDOFF.md, PR-BODY.md, TABLE-15.2.md, SWEEP.md (with `sweep_reconcile.py`), MUTANTS.md (with
`mutants_table.py`), GATES.md (with `gates.py`, `gates_table.py`, `run_logged.py`),
`parent_edits.py` and `mk_parent.sh` (unchanged from round 5), and `receipts/`:
`n11d-counts-9b4da6b.txt`, `d3_mutants-results-9b4da6b.json` (the full campaign),
`dr3a-9b4da6b.txt`, `parent-edits.diff` (the 12-file diff at the gate parent), and the reviewer
reruns `r390-5-extra-acmp-9b4da6b.txt`, `r390-5-owned-probe-9b4da6b.txt`,
`r390-5-arb-unit-9b4da6b.txt`, `unit-probe-r391-5-mutants-9b4da6b.txt`,
`r391-5-acmp-mutants-9b4da6b.txt`, `r391-5-readme-counts-9b4da6b.txt`. Logs, scratch
parents and clones stay under the scratch area (not copied; sizes and hashes in GATES.md). No
file in the packet exceeds 200 KB.
