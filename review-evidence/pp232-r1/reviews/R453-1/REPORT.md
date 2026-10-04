[R453] NEGATIVE - exact head 6e950fea861d76664dc2f7396c980b1ada2e47c1

# [R453-1] External review: milan-fpga #232 / processor PR #153 (the #232 area lane)

- Head reviewed: `6e950fea861d76664dc2f7396c980b1ada2e47c1`, tree `b0baec9241197c6b5071243bba67f550ef951d7e`
  (detached review clone; byte-exact at the end of the round, receipt `receipts/verify_clone.txt`).
- Source base `f4167536d358c996f4e1b70b875879c1651f85d3`; the lane's own change is `5c71928a..6e950fea`
  (7 files, +244/-21): `9e29e2a` RTL, `0c76b21` tests, `3ab2e4d` docs, `823fc20` merge of `main`
  `5c71928a`, `6e950fe` the #22 reorder. The other 30 files of `f4167536..6e950fea` are `main`'s
  (P1 #150, C10 #149), carried byte-equal by the merge (section 5.6).
- Verdict: **NEGATIVE**. Two MINOR findings are open: F1 (Conformance, RTL, Docs) and F2 (Tests, Docs).
  RTL behaviour is correct. An independent lockstep bench found **0 mismatches** in 288,000,000
  compared cycles over 9 shapes, and all 12 of its planted controls were caught. Every campaign
  re-run here is at its recorded count. What is missing is public, re-derivable evidence for the area
  and timing figures (F1), and a committed regression for two of the dependencies this lane introduces
  (F2).
- Prior public review findings on PR #153 at this head: none. The PR has two comments, both review-start
  notices from the manager (5976228848, 5976229121); there are no reviews or review comments. The
  issue has no review findings either. Nothing to resolve or retain.

## 1. Reconstruction (authorities read, in order)

1. Parent `AGENTS.md` and `CONTRIBUTING.md` (read-only from kebag-logic/milan-fpga). The processor
   repository has neither; its `docs/README.md` and `docs/guides/hdl-engineer.md` apply.
2. Issue #232: frozen scope (9 items) and acceptance criteria (5). Scope decisions:
   - 5967852823: lever 5 joins the issue.
   - 5970460015: lane assignment and rules. Behaviour must be identical. Every test stays green at the
     same counts. "100 MHz" is judged at 50 MHz.
   - 5974004216: lever 5 ruled (c), final; the PR body may say "Closes".
   - 5974077269: the round-1b merge and #22 assignment.
   - 5976213371: REVIEW READY at this head.
3. Epic #229 and its four comments, for acceptance criterion 5.
4. The diffs `f4167536..6e950fea` and `5c71928a..6e950fea`, the full commit graph, and
   `hdl/aecp/KL_aecp_notify.sv` read whole at head (FSM, row write, index, monitor, stamps).
5. Public evidence: milan-fpga `ed9f5f46` `review-evidence/pp232-r1/` (the same commit as branch
   `pp232-review-evidence`). Every file's sha256 equals its `MANIFEST.json` published digest. It holds
   the author's HANDOFF.md, PR-BODY.md and five parent patches, and nothing else: no Vivado report or
   log, no lockstep bench, no manager bank receipt. Hosted checks at the exact head (section 5.9).

## 2. Findings

### F1 MINOR - Conformance, RTL, Docs - The Vivado evidence behind AC1, AC4 and the area claims is not public

- **Artifact:** PR #153 body "Validation / Vivado" and the storage inventory; milan-fpga #232 comment
  5976213371; `review-evidence/pp232-r1/author/HANDOFF.md` sections 4, 5, 11 and R1b.6, R1b.9 (milan-fpga
  `ed9f5f46`).
- **Authority / evidence:**
  - #232 acceptance criterion 1 is "Vivado hierarchy and RAM reports match the documented storage
    mapping". Criterion 4 asks the design to meet the clock (judged at 50 MHz) and to record its LUT,
    FF and BRAM tradeoffs.
  - AGENTS.md section 6 (Docs): "The PR and Issue contain enough evidence for another cold reviewer".
    Section 1: evidence is published, never left in a lane scratchpad.
  - The handoff says the reports, checkpoints and logs "stay in scratch". It publishes only quoted
    lines and 16-hex-digit prefixes of the log digests (R1b.9: `3345c0ac81f8f149`,
    `4d18c2905ff3e812`). The evidence branch holds none of them, and no Vivado is installed on this
    review host.
- **What could and could not be checked:**
  - Could: every quoted figure is internally consistent (`receipts/area_check.txt`, 32 checks):
    - route -763 LUT (-1,625 logic, +862 memory), -2,031 FF, -6 slices, -150 CARRY4, WNS +0.195 ns;
    - `u_notify` -927 LUT, -2,012 FF;
    - 960 LUTRAM = 288x2 + 16x2 + 88x4;
    - the #638 cross-figures +543 and -792.
  - Could: a separate synthesis of `KL_aecp_notify` alone (section 5.5) gives exactly the head's quoted
    RAM counts: 88 RAM32M (64 `rows_r` + 24 `cmdq_*`) and 304 one-bit index memories (288 + 16).
  - Could not: confirm any Vivado number, the "RAM64M x 1" / "RAM16X1D x 1" mapping lines (the text
    elsewhere names RAM64X1D / RAM32X1D cells), the zero `Synth 8-7186` / `8-6901` counts, WNS +0.274 /
    +0.079, or `u_resp` 260 FF.
- **Impact:** The area figures are the lane's purpose, and two of the issue's five acceptance criteria
  rest on them. As published they cannot be re-derived or disputed outside the lane, and the bank that
  records #638's new baseline would inherit them unverified.
- **Required outcome:** Publish, for the round-1b `main` and head routes (and the round-1 standalone
  runs the PR body says "stand"), the Vivado logs or the report extracts the PR cites, each with its
  full sha256:
  - hierarchical utilization (`u_notify`, `u_resp`, `u_aecp/u_d3`);
  - the "Distributed RAM: Final Mapping Report";
  - the timing summary with the four signoff corners;
  - the `Synth 8-7186` / `8-4445` / `8-6901` counts.
- **Verification:** A cold reviewer re-derives -763 / -2,031 (route), -927 / -2,012 (`u_notify`),
  WNS +0.274, 88 RAM32M + 288/16 index primitives and zero `Synth 8-7186` from the published files.

### F2 MINOR - Tests, Docs - Two dependencies this lane introduces are proven only by an unpublished bench, and no committed test fails when either is broken

- **Artifact:**
  - `tb/aecp_notify/sim_main.cpp:231-288` (IX4 drives its command in the second rewrite cycle only,
    `:268-276`);
  - `hdl/aecp/KL_aecp_notify.sv:575-579` and `:598-600` (the rewrite comparator, both cycles);
  - `hdl/aecp/KL_aecp_notify.sv:399-404` and `:1096-1098` (the stamps' reset dropped, so
    `!ctr_sent_r[c]` becomes load-bearing after a warm reset);
  - the PR body's "Lockstep differential bench (lane scratch, not committed)" and its control table.
- **Authority / evidence:**
  - AGENTS.md section 6 (Tests): "Each new test can fail for the defect it claims to detect". Section 5
    asks for self-checking tests of changed behaviour, reset and ordering paths included.
  - The lane's rule (5970460015) is "Behaviour is identical", and the PR body states it as
    "Every output of `KL_aecp_notify` is cycle-identical to `main`'s".
  - Controls planted in head copies were run through the committed `tb/aecp_notify` (`make`) and
    `tb/pp_top` (`make`, 10,416 checks) suites (`receipts/probe_*.txt`, `receipts/probe_ctr_stamp.log`):

    | Control (`scripts/lockstep/make_controls.py`) | `tb/aecp_notify` | `tb/pp_top` | Lockstep (5.1) |
    |---|---|---|---|
    | `own_vs_new_row`: the rewrite comparator compares the row being written, not what `rows_r` holds (wrong only in the write's own cycle) | 20/20 PASS | 10,416/10,416 PASS | caught 16/16 runs, all four modes |
    | `override_set_only`: the comparator in the set cycle only (wrong after a reset inside the window, or on a never-indexed row) | 20/20 PASS | 10,416/10,416 PASS | caught 10/16 (reset-aimed modes) |
    | `stamp_read_without_valid`: `!ctr_sent_r[c]` dropped, so a stamp kept across a warm reset is read | 20/20 PASS | 10,416/10,416 PASS; `make counters` 28/28 PASS | caught 14/16 |
    | `override_clr_only`, `reindex_late` (for contrast) | IX4 FAILS | 10,416/10,416 PASS | caught 16/16 |
    | the head file itself | 20/20 PASS | 10,416/10,416 PASS | 0 mismatches |

  - So the committed bank grades only the set cycle (W+1) of the two-cycle rewrite. A defect confined
    to the write's own cycle (W), or to the stamp gate that the dropped reset now relies on, passes:
    - `tb/aecp_notify` section IX;
    - the whole of `tb/pp_top`, and the 44-arm notification campaign that drives those suites.
  - The only evidence for those paths is the author's lockstep bench, which is neither committed nor
    published (`review-evidence/pp232-r1` has no bench source, generator, control diff or run log).
  - Its published control table cannot be checked, and one row is inconsistent with its label.
    "Comparator only in the set cycle" is reported at 14,848,035 mismatches (8 of 8 runs), almost the
    same as "no clear" at 14,840,381. A control that does what that label says (`override_set_only`
    here) diverges only after a reset inside the window or on a never-indexed row:
    - 0 mismatches in all 4 protocol-shaped runs;
    - 1 to 23,392 in the reset-aimed runs.
    The published edit is therefore probably not the defect its label describes.
- **Impact:**
  - The guarantee the lane exists to keep has no durable guard for two of its three new dependencies.
    One is the rewrite's first cycle; the other is the valid gate that makes the stamps' dropped reset
    safe.
  - A later edit could break cycle identity in either place, `own_vs_new_row` being a plausible
    "simplification", and every committed gate would stay green.
  - The behaviour is correct at this head (section 5.1, published here). The finding is the missing
    durable regression and the unverifiable published proof.
- **Required outcome:**
  - Add committed, self-checking coverage that fails for each of the three defect classes above, with
    the corresponding controls planted in `notify_mutants.py` / `ctr_mutants.py` and recorded in the
    READMEs. Two ways meet this:
    - Directed checks: in the write's own cycle the freshly registered row answers for the identity
      `rows_r` still holds, not the new one, with a reset inside the window; and a counter change
      within one second of a warm reset that followed a push goes out at once.
    - Or the differential bench itself, committed as a suite with its controls.
  - Correct or publish the lockstep control table, so each published label matches its edit.
- **Verification:** `own_vs_new_row`, `override_set_only` and `stamp_read_without_valid` (this packet's
  `make_controls.py`, planted at the new head) each fail a named committed check, and the README/09
  records list them.

### Residue (wording only; does not affect the verdict)

- **R1 (Docs).** "re-indexes its row in the two cycles after it [the row write]" counts from the
  decision, while the same sentences call the first of the two cycles "the write's own cycle". The
  phrase is at `hdl/aecp/KL_aecp_notify.sv:559`, in the identity-index row of the "Storage (issue #232)"
  table at `docs/architecture/06_aecp_engine.md:904`, and in PR body item 1.
  - Exact fix for the RTL comment and the PR body: "re-indexes its row over two cycles: the cycle in
    which the row write lands (`wr_en_r` high) clears the old identity's bits, and the cycle after it
    sets the new identity's".
  - Exact fix for 06: "over the row write's own cycle and the cycle after it".

## 3. Lens results at `6e950fea`

| Lens | Result | Artifacts examined (at this head) |
|---|---|---|
| Conformance | UNCLEAN (F1) | #232 AC1-AC5 against the PR body, 06 section 7 and the handoff; the behaviour-identity rule against `KL_aecp_notify.sv` (section 5.1); exhaustion: NO_RESOURCES `:1382`, queue drop `:1079-1091`, `amap_busy_o` `:955-957`; `KL_aecp_resp_buf.sv` (580 lines, no unpacked array; `:336-339` main-memory writes); lever 5 per ruling 5974004216; AC5 not yet linked from #229 (manager duty, section 8) |
| RTL | UNCLEAN (F1: the area and timing figures cannot be re-derived) | `KL_aecp_notify.sv:330-357` (`rows_r`, row write), `:551-602` (index and match), `:604-606` / `:726` (#22 reorder), `:1043-1056` (`ix_clr_r`/`ix_set_r` reset and pipeline), `:1332-1384` (`N_APPLY`), `:1445-1460` (emission write-back), `:399-404` / `:1096-1098` / `:1296-1298` (stamps); sections 5.1, 5.5, 5.6 |
| Robustness | CLEAN | section 5.1: resets inside each rewrite cycle, a full registry, 9 shapes (`N_CTRL_P` 1..16, streams 1..9, identify on/off), fully random inputs with `now_ms_i` jumps and wrap, read/write collisions on the same row, warm resets with stamps valid |
| Tests | UNCLEAN (F2) | `tb/aecp_notify/sim_main.cpp` IX1-IX4b and `README.md`; `tb/pp_top/notify_mutants.py` four `ix_*` controls; committed suites against 8 controls (section 5.3); campaigns (section 5.4) |
| Docs | UNCLEAN (F1, F2; R1 residue) | `06_aecp_engine.md:872-876`, `:897-914`; `09_verification.md:283-296`; `tb/aecp_notify/README.md`; `tb/pp_top/README.md:2289-2294`, `:2338-2341`; the PR body; the handoff; the evidence branch. No added U+2014 and no bench-identifying token in the lane diff; `scripts/check-links.py` rc 0 |

## 4. What holds (evidence for the clean parts of each lens)

- [R453] PASS RTL - `hdl/aecp/KL_aecp_notify.sv:551-602`, `:1046-1056`, `:1364` - the identity index
  gives exactly the match the old comparator bank (`5c71928a:hdl/aecp/KL_aecp_notify.sv:539-546`) gave,
  in every cycle.
  - The invariant was read from the RTL:
    - only `N_APPLY` (`:1363-1368`) changes a row's identity;
    - the emission write-back (`:1452-1454`) rewrites the {eid, mac} it read at `N_EMIT_RD`, and no
      `N_APPLY` can come between the two (it needs `N_IDLE`; `N_EMIT_WAIT` withdraws on a registry op);
    - `wr_ix_r` cannot change in W or W+1, because `N_ANS` -> `N_IDLE` issues no row write;
    - a reset in W lets the clear and the row write land and suppresses the set, which leaves the index
      a subset of the row's identity; the row is invalid until the next `N_APPLY` clears and sets it
      again;
    - every index read is gated by `valid_r`, which only `N_APPLY` sets.
  - The read port `ix_wr_row_w = rows_r[wr_ix_r]` returns the old row in W and the new row in W+1,
    which is what the old bank read.
  - Geometry: 19 chunks of the zero-extended 114-bit key. The last chunk's upper two key bits are
    constant 0, which is why the tool trims it to 16 x 1.
  - Confirmed by section 5.1 (0 mismatches; 12 of 12 controls caught).
- [R453] PASS RTL - `KL_aecp_notify.sv:604-606` (#22).
  - `823fc20..6e950fe` moves only the two declarations, plus one comment line.
  - The declarations are bare (no initialiser), so the xelab-only class CONTRIBUTING names cannot
    arise.
  - The first use is at `:617`, after the declaration at `:605-606`; every new `ix_*` signal is
    declared at `:569-575`, before its first use.
- [R453] PASS Robustness - section 5.1 coverage line, 144 runs, 0 mismatches:
  - 19,703 resets in W and 19,231 in W+1;
  - 87,287,778 cycles with the registry full;
  - 15,610,828 cycles in which the walk read the row being written, and 200,530 in which the probe pick
    did;
  - 47,552 warm resets with a stamp valid.
- [R453] PASS Conformance (behaviour part) - the head equals `main` cycle for cycle under section 5.1.
  "Every test green at the same counts": every campaign of section 5.4 is at its README count,
  `tb/aecp_notify` 20/20, `tb/pp_top` 10,416/10,416.
- The #232 inventory resolves at head and the response buffer cannot spill (section 5.7). The merge
  keeps both sides (section 5.6). The lane changes no port, parameter or register (the RTL diff touches
  no port line).

## 5. Evidence

### 5.1 Reviewer lockstep bench (independent of the author's)

- **Sources:** `scripts/lockstep/` (`gen_wrapper.py`, `lk_main.cpp`, `build.sh`, `make_controls.py`,
  `run_matrix.py`).
- **Setup:**
  - Reference: `main` `5c71928a`'s `KL_aecp_notify.sv` renamed `KL_aecp_notify_ref`. It is byte-equal to
    `f4167536`'s, and `pp_pkg.sv` is equal at both.
  - Candidate: the head file.
  - The two blocks run side by side on the same inputs, every cycle.
- **What is compared:** all 37 outputs and the internal `rx_cmd_hit_w`, at both points of every cycle
  (after the input change with the clock low, and after the rising edge).
- **Matrix:**
  - Shapes `N_CTRL_P/N_STREAM_IN_P/N_STREAM_OUT_P/EN_IDENTIFY_NOTIF_P`: 16/8/8/0, 16/2/2/0, 16/2/2/1,
    16/9/9/0, 2/1/1/0, 5/8/8/0, 8/3/5/1, 3/1/2/0, 1/1/1/0.
  - Modes:
    - 0, protocol-shaped (registry op handshake, a timer model that echoes the arms, probe and PRNG and
      job handshakes);
    - 1, fully random (random op face, random expiries, `now_ms_i` jumps and wrap);
    - 2, rewrite-focused (resets aimed at W and W+1; commands carrying the row's stored or new identity
      in W and W+1);
    - 3, registry-filling.
  - 4 seeds each, 2,000,000 cycles per run.
- **Result:** 144 runs, 288,000,000 cycles, **0 mismatches**, every run rc 0 (`receipts/lockstep_r1.log`,
  `receipts/lockstep_r1.tsv`). Coverage totals (`receipts/lockstep_r1_coverage.txt`):
  - activity: 3,428,837 registry ops; 10,592,049 hit cycles;
  - commands in W / W+1: 826,774 / 820,330;
  - hits on the written row in W / W+1: 121,836 / 165,025; in 62,303 of the W hits the rewrite changes
    the row's identity and the command carries the old one;
  - resets: 78,103, of which 19,703 in W and 19,231 in W+1; 47,552 with a stamp valid;
  - collisions with the write index: walk read 15,610,828, probe pick 200,530;
  - registry full: 87,287,778 cycles;
  - 16,977,530 emission write-backs; 7,577,518 expiries.
- **Controls:** 12 planted copies of the head file at 16/2/2/0, 16 runs each, **all caught**:

  | Control | Runs caught | Mismatches |
  |---|---:|---:|
  | `no_override` | 16/16 | 993,233 |
  | `override_clr_only` | 16/16 | 992,954 |
  | `override_set_only` | 10/16 (0/4 protocol-shaped) | 23,621 |
  | `own_vs_new_row` | 16/16 | 425,703 |
  | `no_clear` | 16/16 | 613,088,442 |
  | `no_set` | 16/16 | 159,854,381 |
  | `last_chunk_ignored` | 16/16 | 26,208,056 |
  | `first_chunk_ignored` | 16/16 | 12,209,411 |
  | `key_swapped` | 16/16 | 144,529,024 |
  | `index_wrong_row` | 16/16 | 151,821,997 |
  | `reindex_late` | 16/16 | 220,147 |
  | `stamp_read_without_valid` | 14/16 | 6,638,375 |

- **The author's bench, as described** (it cannot be inspected; F2):
  - Its stated scope (5 shapes, protocol-shaped and random inputs, resets, every output and
    `rx_cmd_hit_w`) is adequate in kind.
  - Its window statistics (423,284 commands in a rewrite window, 46,701 hits) are plausible against
    the figures above.
  - It states no reset aimed at the window and no identity aimed at the written row, the two stimuli
    the `override_set_only` class needs.
  - One control row is inconsistent with its label (F2).

### 5.2 `tb/aecp_notify` section IX

- Head: `make` 20 checks, 20 PASS (`receipts/probe_none.txt`).
- The head's `tb/aecp_notify` against `main`'s RTL: 20/20 PASS (`receipts/ix_bench_on_main_rtl.log`). So
  IX describes unchanged behaviour, as claimed.
- IX4 drives its command in the cycle after `rgy_wait_o` falls, which is the set cycle (W+1). No IX
  check drives the write's own cycle (F2).
- The four `ix_*` controls are KILLED at their README counts (section 5.4).

### 5.3 Committed suites against reviewer controls

See the F2 table (`receipts/probe_*.txt`, `receipts/probe_ctr_stamp.log`; scripts
`scripts/probe_committed.sh`, `scripts/probe_all.sh`). Each probe copies `hdl/`, `scripts/`,
`tb/common/` and the named suites of the head's `git archive` into scratch, so the review clone is never
touched. Two more controls show the suites' reach:
- `first_chunk_ignored` fails IX2 and passes `tb/pp_top`;
- `key_swapped` fails IX3 and `tb/pp_top` U10a.

### 5.4 Campaigns at head

Each campaign ran from a `git archive` of `6e950fea`, with the pinned Verilator 5.050 (identity printed:
`Verilator 5.050 2026-07-01 rev v5.050`). Each arm's failing-check count was compared with the
committed README records by `scripts/compare_counts.py`; `receipts/count_notes.txt` resolves by hand the
rows it cannot parse ("the same N" and the rx_validator M6 row).

| Campaign | rc | Result | Against README |
|---|---:|---|---|
| `notify_mutants.py --jobs 5` | 0 | 44 of 44 KILLED, six goldens PASS (564 s) | 44/44 equal (`ix_*` 1, 2, 1, 1) |
| `ctr_mutants.py --jobs 3` | 0 | control PASS, 17 of 17 KILLED (209 s) | 17/17 equal |
| `aecp_mutants.py --jobs 4` | 0 | 5 controls PASS, 55 KILLED, 60 checks (1,003 s) | 55/55 equal (6 by hand) |
| `aecp_dispatch_mutants.py --jobs 4` | 0 | 4 controls PASS, 40 KILLED, 44 checks (1,009 s) | 40/40 equal |
| `acmp_mutants.py --jobs 3` | 0 | 19 of 19 KILLED, three goldens PASS (593 s) | 19/19 equal (1 by hand) |
| `gsi_mutants.py --jobs 3` | 0 | 20 detected by named checks, golden and restored PASS (811 s) | as recorded (20) |
| `name_wr_mutant.py` | 0 | decode killed, golden and restored PASS (251 s) | as recorded |
| `d3_mutants.py --jobs 10` | 0 | 110 of 110 KILLED, six goldens PASS (2,000 s) | 110/110 equal (1 by hand) |
| `scripts/lint_hdl.sh` | 0 | 41 of 41 LINT OK | |

### 5.5 RAM inference cross-check (a separate synthesis tool, not Vivado)

`scripts/yosys_notify.sh` runs sv2v and then `synth_xilinx -family xc7` on `KL_aecp_notify` alone, at
default parameters (`receipts/yosys_head_stat.txt`, `receipts/yosys_main_stat.txt`):

| | head | `main` |
|---|---|---|
| RAM32M | 88 | 1,048 |
| one-bit 64-deep memories | 304 | none |
| FDRE | 1,727 | 1,721 |
| LUT6 | 844 | 3,674 |
| MUXF7 + MUXF8 | 195 | 1,837 |

- The head's RAM counts equal the Vivado cell counts the handoff quotes (RAM32M 88 = `rows_r` 64 +
  `cmdq_*` 24; 288 + 16 index memories).
- This tool replicates `rows_r` per read port at `main` instead of spilling it to flops, so its flop
  delta says nothing about Vivado's `Synth 8-7186` spill. It supports RAM inferability at head, not
  the Vivado figures (F1).

### 5.6 The round-1b merge keeps both sides (`823fc20`)

- Merge base `f4167536`.
- Every file only `main` changed is byte-equal to `5c71928a` in the merge; every file only the lane
  changed is byte-equal to `3ab2e4d`.
- For the three files both sides changed, the lane's hunks apply verbatim over `main` in
  `06_aecp_engine.md` and `09_verification.md`.
- In `tb/pp_top/README.md` the one conflict keeps P1's re-run note ("`main` alone still fails 20")
  and appends the lane's `ix_*` sentence; the four `ix_*` rows are at `:2338-2341`.
- `823fc20..6e950fe` touches only `KL_aecp_notify.sv`: a 4+/2- declaration move.
- The lane's commits have one-line subjects, no body and no trailer.

### 5.7 Inventory and exhaustion (#232 scope)

- Every line citation in the PR body's inventory resolves at head:
  - `KL_aecp_notify.sv:336`, `:337`, `:379-384`, `:404`, `:410`, `:581-593`;
  - `KL_aecp_resp_buf.sv:336-339`; `KL_aecp_ucpu.sv:149`, `:159`;
  - `KL_aecp_desc_store.sv:285`, `:297`, `:309`; `KL_aecp_engine.sv:1195`;
  - `KL_pp_rx_slots.sv:193`, `KL_pp_trace_ring.sv:86`, `KL_pp_tx_slots.sv:263`,
    `common/KL_pp_timer_service.sv:108`, `KL_pp_dispatch.sv:303`.
- `KL_aecp_resp_buf.sv` declares no unpacked array, so the 5,079-FF spill cannot recur from it.
- Exhaustion:
  - registry full: NO_RESOURCES (`:1382`), exercised for 87 M cycles in section 5.1;
  - queue full: the push is dropped and counted (`:1079-1091`);
  - `amap_busy_o` holds the engine while anything is pending (`:955-957`);
  - the other classes coalesce. No new behaviour was introduced, which is consistent with the
    assignment's STOP rule.

### 5.8 Clone integrity

`scripts/verify_clone.sh` (`receipts/verify_clone.txt`):
- HEAD and the tree id match;
- every index record's mode and blob equal HEAD's tree;
- no `h`/`S` index flags;
- all 504 working files rehash to their blobs, with modes as recorded;
- no untracked or ignored file;
- HEAD has no gitlink, so no submodule pin is required at this head.

### 5.9 Hosted checks at the exact head (read-only)

Workflow `hdl`, run 37174627050 (pull_request) and 37174624143 (push):
- `docs-gates` success;
- `portability` (the Yosys gate) success;
- `suites`: complete in the push run (job 111354566102, conclusion success, every step); still running
  in the pull_request run (job 111354574902; its step 5, the suite sweep, already passed) when read at
  2026-10-04T05:19Z;
- the push job's log, checked out at `6e950fea`: `suites: 1021455 checks total, 0 failing`,
  `aecp_notify` 20 checks, `pp_top` 10,416 checks, AECP campaign 60 checks PASS, dispatch campaign
  44 checks PASS, matrix 94 rows and 0 untested (`receipts/hosted_checks.txt`).

Acceptance of the hosted contexts is the manager's.

## 6. Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #232 AC1-5, scope rulings, PR body, 06 section 7, handoff, `KL_aecp_notify.sv`, `KL_aecp_resp_buf.sv`; sections 5.1, 5.4, 5.7 | R453-1 | `6e950fea861d76664dc2f7396c980b1ada2e47c1` |
| RTL | UNCLEAN (F1) | `KL_aecp_notify.sv` whole; the `5c71928a..6e950fea` RTL diff; sections 5.1, 5.5, 5.6 | R453-1 | `6e950fea861d76664dc2f7396c980b1ada2e47c1` |
| Robustness | CLEAN | section 5.1 (resets in the window, full registry, 9 shapes, random inputs, collisions, stamps across warm resets) | R453-1 | `6e950fea861d76664dc2f7396c980b1ada2e47c1` |
| Tests | UNCLEAN (F2) | `tb/aecp_notify` IX, `notify_mutants.py`; sections 5.2-5.4 | R453-1 | `6e950fea861d76664dc2f7396c980b1ada2e47c1` |
| Docs | UNCLEAN (F1, F2; R1 residue) | 06, 09, both READMEs, PR body, handoff, evidence branch | R453-1 | `6e950fea861d76664dc2f7396c980b1ada2e47c1` |

## 7. Real limits of this round

- No Vivado on this host, and the reports are unpublished (F1). No Vivado figure is confirmed here;
  only their arithmetic consistency and a separate tool's RAM count are.
- The author's lockstep bench was not available. Section 5.1 replaces it as the behaviour proof.
- Not run, per the assignment: the parent consumer set (17), the full processor suite bank (the
  hosted push run ran it at this head: 1,021,455 checks, 0 failing), the Yosys bank, builder banks,
  act, xvlog (no Vivado), and hardware. Physical calibration was NOT RUN; skipped hosted contexts are not hardware proof.
- The lockstep bench compares observable outputs and `rx_cmd_hit_w`. Its coverage is stochastic plus
  aimed, not formal; the `override_set_only` class is reached only through reset-aimed stimulus.

## 8. Pending manager duties

- F1 and F2: obtain the evidence and the commits, then a re-review at the new head (every lens whose
  scope the fix touches is re-covered).
- AC5: link #232's results from epic #229 (no such link exists on #229 today).
- Bank the parent xvlog ratchet change (`parent-adoption-pp232-xvlog-c10-5fabb46e.patch`, 3 -> 2
  findings) with the adoption, or gate 9 fails.
- Build and validate the final current-dev candidate at the merge turn (live dev `241f9184` with the
  c8, p2-p1 and c10 patches). The author's parent run was at `5fabb46e`. Record gate 16's T30 checks
  against #643 / PR #648.
- Record a new #638 baseline A at the merge bank (head is +543 LUT over the recorded A, from `main`'s
  growth).
- Completion of the pull_request run's `suites` job (111354574902) at the exact head (section 5.9), and
  hosted/act acceptance.
- Carry R1 to the residue checklist.

R453-1 FINISHED
