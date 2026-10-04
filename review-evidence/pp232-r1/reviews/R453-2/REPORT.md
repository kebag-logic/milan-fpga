[R453] POSITIVE - exact head 2ea3dee2cd92e5907a8942a8c32436ab2f46ff2d

# [R453-2] External review, round 2: milan-fpga #232 / processor PR #153 (the #232 area lane)

- **Head reviewed:** `2ea3dee2cd92e5907a8942a8c32436ab2f46ff2d`, tree
  `fc05a7f236eb72c8213bd1cf52fa70b87dae61d7`. The detached review clone was byte-exact at the end of the
  round (`receipts/verify_clone.txt`).
- **Delta since R453-1** (`6e950fea..2ea3dee2`):
  - `f3abfc6`: coverage. `tb/aecp_notify` IX5, IX6 and TS; three controls in `notify_mutants.py`; the
    READMEs and 09.
  - `0d9e5e7`: residue. The RTL comment and 06.
  - `2ea3dee`: `--no-ff` merge of `main` `83999eba` (PR #152, the ADP walk's tests).
- **Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open, and no RESIDUE is new. R453-1 F1
  (Vivado evidence), R453-1 F2 (coverage and the control label) and R452-1-F1 (the clear-cycle
  coverage) are resolved. R453-1 R1, R452-1-F2 and R452-1-S1 are applied as written. Every lens is
  CLEAN.
- **Ordering.** The verdict and ledger were recorded before R452-1's report was read
  (`receipts/verdict_ledger_before_prior_findings.txt`, sha256 `dfc2e9ca...a1a5`). Section 3 resolves
  R452-1's findings after that.

## 1. Reconstruction

1. **Rules.** The processor repository has no AGENTS.md or CONTRIBUTING.md. The parent's (milan-fpga)
   apply, with the processor's `docs/README.md` and `docs/guides/hdl-engineer.md`.
2. **Issue #232.** The body: 9 scope items and 5 acceptance criteria. The scope decisions:
   5967852823, 5970460015 (behaviour identical, counts unchanged, 100 MHz judged at 50 MHz),
   5974004216 (lever 5 (c), final), 5974077269, and the round-2 assignment 5976892215 (items 1-5).
   REVIEW READY is 5978213864. Epic #229 was read for AC5.
3. **History.** `git diff f4167536..2ea3dee2` and the first-parent history. Round 2's three commits
   were read in full. `hdl/aecp/KL_aecp_notify.sv` was re-read at the index (`:551-603`), the row
   write (`:330-357`), the reset and pipeline (`:972-1060`), the stamps (`:399-404`, `:1095-1103`,
   `:1293-1299`) and `N_APPLY` (`:1360-1386`).
4. **Public evidence.**
   - The assignment links milan-fpga `ed9f5f46`, which is round 1's packet. The round-2 packet is
     at `83482f957cef27bd8968f5a4e1831f7b570b6f1d` on the same branch, `pp232-review-evidence`, under
     `review-evidence/pp232-r1/author-r2/`. Only `author-r2/` and `MANIFEST.json` were checked out;
     the `reviews/` tree was not read.
   - Every one of the 265 `author-r2` files equals its `MANIFEST.json` published sha256. The 261
     entries of the inner `evidence-r2/MANIFEST.sha256` equal the `original_sha256` records. The 21
     files whose paths the publisher redacted differ from the originals in bytes only for that reason
     (`scripts/evidence_manifest_check.py`, `receipts/evidence_manifest_check.txt`).
   - The issue and the PR carry no manager evidence comment for this head. The manager's bank
     results named in the assignment are not public (section 7).

## 2. Findings

None open.

### Resolution of R453-1 findings (this reviewer, round 1)

| ID | Round-1 severity | Status at `2ea3dee2` | Evidence |
|---|---|---|---|
| R453-1 F1 (Conformance, RTL, Docs): Vivado evidence unpublished | MINOR | **RESOLVED** | section 4.1 |
| R453-1 F2 (Tests, Docs): no committed check fails `own_vs_new_row`, `override_set_only` or `stamp_read_without_valid`; one lockstep control label mismatched | MINOR | **RESOLVED** | sections 4.2-4.4 |
| R453-1 R1 (Docs): rewrite-window wording | RESIDUE | **APPLIED** as written | `KL_aecp_notify.sv:559-564`; `06_aecp_engine.md:904` ("over the row write's own cycle and the cycle after it"); PR body item 1 (`receipts/pr153_body_at_review.md:118-120`). The text is verbatim the exact fix |

## 3. Prior public review findings on PR #153 (read after section 2's verdict was recorded)

R452-1 (PR #153 comment 5976816563, at `6e950fea`):

| ID | Severity | Status at `2ea3dee2` | Evidence |
|---|---|---|---|
| R452-1-F1 (Tests): the clear-cycle half of the window is ungraded; `override_set_only` and `own_compare_new_row` survive | MINOR | **RESOLVED** | Both edits are planted in `tb/pp_top/notify_mutants.py:284-294`, and both are KILLED at their README counts in this round's full campaign (section 4.3). R453-1's byte-identical `own_vs_new_row` edit fails IX5; `override_set_only` fails IX6 and IX6b (section 4.2) |
| R452-1-F2 (Docs): the inventory's index row mixes the synthesis mapping report and the implemented cells | RESIDUE | **APPLIED** as written | PR body inventory row (`receipts/pr153_body_at_review.md:310`) and HANDOFF section 5 (row at its line 176) carry the exact fix. The figures agree with the published census (288 RAM64X1D, 16 RAM32X1D, 88 RAM32M; 960 LUTRAM) |
| R452-1-S1 (Docs): record the index's zero content and `rst_n` in 06 | SUGGESTION | **APPLIED** | `06_aecp_engine.md:904`. Verified against the RTL: the index `initial` is at `:586`; `rows_r` (`:355-357`) and the index (`:587-590`) have no reset branch; the reset is synchronous (`:226`, `:973`) |

No other review, review comment or finding exists on PR #153 or issue #232.

## 4. Evidence for this round

### 4.1 Vivado figures re-derived (R453-1 F1)

- **The author's script.** `tools/rederive.py` was re-run from the published packet: rc 0, and its
  output is byte-identical to the published `rederive.txt` (`receipts/rederive_rerun*.txt`).
- **This reviewer's own parser.** `scripts/vivado_check.py` (`receipts/vivado_check.txt`, 125 PASS,
  rc 0) and `scripts/vivado_table_check.py` (`receipts/vivado_table_check.txt`, 73 PASS, rc 0) do not
  reuse the packet's tools.
  - **Raw-file record.** Every whole report in each of the eight run directories (76 files) has a
    sha256 equal to its `sources.tsv` raw record. For the path-redacted files, the original digest is
    used.
  - **Log digests.** Each run's `baseline.log` record in `sources.tsv` equals the README run table
    (bytes and full sha256). This includes `3345c0ac...9079073` (`main`) and `4d18c290...3eca3f37`
    (head), whose 16-digit prefixes round 1b published.
  - **The route at the merge** (head `6e950fea` minus `main` `5c71928a`), all from the whole
    `baseline_utilization.rpt`:
    - LUT 50,671 - 51,434 = **-763** (logic -1,625, memory +862);
    - FF 57,660 - 59,691 = **-2,031**;
    - Slice -6, CARRY4 -150.
  - **`u_notify`** (whole `baseline_hierarchy.rpt`): -927 LUT, -2,012 FF, 960 LUTRAM at head.
  - **`u_resp`**: 260 FF in all eight runs. **`u_d3`**: +34 LUT against `main`, and +619 against round
    1's head, the image's +581 move.
  - **Timing.** Head WNS/WHS is +0.274 / +0.023 ns and `main`'s +0.079 / +0.014. The four signoff
    corners are all positive (Slow +0.274 / +0.050, Fast +1.550 / +0.023), and each `*_negative.rpt`
    reads "No timing paths found". The route has 0 nets with routing errors in all four routes.
  - **`Synth 8-7186`.** Counted from the extract's own diagnostic lines: **0 in every head run** and 16
    (`rows_r[0..15]`) in every base and `main` run. This is corroborated independently of the extract
    by the whole hierarchy report: `u_notify` FF 3,299 -> 1,287, the 2,048 `rows_r` flops gone.
  - **RAM mapping.** The mapping report has 288 `g_ix_chunk[*] ... 64 x 1 | RAM64M x 1` rows, 16
    `g_ix_chunk[18] ... 16 x 1 | RAM16X1D x 1` rows and `rows_r_reg ... 16 x 128 | RAM32M x 64`. The
    census has `u_notify` RAM32M 88, RAM64X1D 288 and RAM32X1D 16, and 88x4 + 288x2 + 16x2 = 960.
  - **The PR body's table.** All 56 cells of its eight Vivado rows match the reports, and so do the
    17 quoted deltas: round 1 route -650 / -1,950 / -15 / -147 / WNS +0.027; standalone 1x1 -894 /
    -2,042 and 8x8 -925 / -2,175; the merge WNS +0.195.
  - **`Synth 8-6901` for `pd_ix_w`**: 3 at `main`, 0 at head (`receipts/xvlog_static_corroboration.txt`).
- **The head's HDL equals `6e950fea`'s** once comments are stripped. Only two HDL files differ,
  `KL_aecp_notify.sv` and `KL_adp_engine.sv`, and both are EQUAL (`scripts/strip_compare.py`,
  `receipts/hdl_strip_compare.txt`). So the round-1b route is the route of this head.

### 4.2 Round-1 controls, planted and probed unchanged (R453-1 F2)

- **The scripts are unchanged.** The 13 round-1 scripts were copied and re-verified byte-equal to
  R453-1's published manifest (`receipts/r1_scripts_*.txt`). `make_controls.py` planted all 12
  controls at the head file, each snippet found exactly once (`receipts/make_controls_head.txt`,
  `receipts/controls_head.sha256`).
- **`probe_all.sh`**, unchanged: `tb/aecp_notify` and `tb/pp_top` against the head and 7 controls
  (`receipts/probe_*.txt`, 2,179 s).
- **`probe_committed.sh`**, unchanged: all 12 controls through `tb/aecp_notify`, driven by
  `scripts/ix_probes_r2.sh` (`receipts/ix_ctl_*.txt`).

| Control | `tb/aecp_notify` (named failing checks) | `tb/pp_top` |
|---|---|---|
| head file | 30/30 PASS | 10,416/10,416 PASS |
| **`override_set_only`** | **IX6, IX6b** | 10,416 PASS |
| **`own_vs_new_row`** (= R452-1's `own_compare_new_row`, the same edit) | **IX5** | 10,416 PASS |
| **`stamp_read_without_valid`** | **TS3** | 10,416 PASS |
| `no_override` | IX4, IX6, IX6b | not run |
| `override_clr_only` | IX4 | 10,416 PASS |
| `reindex_late` | IX4 | 10,416 PASS |
| `no_clear` | IX1 | not run |
| `no_set` | IX3, IX4, IX6b | not run |
| `last_chunk_ignored` | IX2 | not run |
| `first_chunk_ignored` | IX2 | 10,416 PASS |
| `key_swapped` | IX3, IX6b | FAIL (U10a4, U10a5, ...) |
| `index_wrong_row` | IX3, IX6b | not run |

- **12 of 12 controls fail a named committed check.** The three round-1 survivors fail exactly the
  checks the assignment names.
- These sets equal the author's published R453-1 rows (`evidence-r2/probes/table.md`).
- `tb/pp_top`'s reach is unchanged from round 1.

### 4.3 Committed checks and campaign

- **The tests are correct by construction (RTL read).**
  - `register_to_write` returns in the first cycle with `rgy_wait_o` low. That is `n_st_r == N_ANS`
    (`:748`), which `N_APPLY` sets on the same edge as `wr_en_r` and `ix_clr_r` (`:1364-1385`), so the
    cycle is W, the row write's own cycle.
  - The reset is synchronous, so IX6's reset lands at the end of W. The row write and the clear land,
    and the set is suppressed (`:1048`, `:1057`).
  - Under `override_set_only`, W then reads the empty index and drops E: IX6 fails.
  - Under `own_vs_new_row`, W compares the incoming D against C: IX5 fails.
  - TS3 reads a stamp written in the same millisecond after a warm reset, so dropping `!ctr_sent_r[c]`
    holds it.
- **`notify_mutants.py --jobs 4`** at head: rc 0, **47 of 47 KILLED**, six goldens PASS (588 s). By
  round 1's `compare_counts.py`, **47 of 47 are at their README counts**: `override_set_only` 2,
  `own_compare_new_row` 1, `stamp_read_without_valid` 1, `ix_new_identity_unset` 3,
  `ix_rewrite_unmatched` 3 (`receipts/notify_head*.{log,txt}`).
- **On `main`'s RTL.** The head's `tb/aecp_notify` against `main` `83999eba`'s `KL_aecp_notify.sv`
  (blob `4b81c74e`, the same as `f4167536`'s and `5c71928a`'s) gives 30 checks, 30 PASS
  (`receipts/ix_on_main_*.txt`). The default build has 26 checks: 10 lifecycle, 11 IX and 5 TS. The
  identify build has 4.

### 4.4 Lockstep bench, re-run unchanged at head; the published control table

- **This reviewer's bench.** Run with round 1's `run_matrix.py` (`main` renamed as the reference, the
  head file as the candidate): 144 runs, 288,000,000 cycles, **0 mismatches**. All 12 controls are
  caught, `override_set_only` again only by the reset-aimed and random modes (10 of 16).
  - The TSV is identical to round 1's in every column, coverage included: 19,703 resets in W and
    19,231 in W+1; 62,303 old-identity hits in W; 47,552 resets with a stamp valid
    (`receipts/lockstep_r2*.{log,tsv,txt}`).
  - The first launch failed to build because of this reviewer's reference rename (the end label). The
    rename was corrected and the run relaunched. The script was not changed.
- **The author's bench, now published.** The corrected label matches its diff: round 1b's
  "set-cycle-only" control is `ix_busy_w = ix_set_r`, which also drops the clear. Every mismatch
  total and caught count in the published table re-sums exactly from `runs/*.txt`, for example
  14,848,035 (8/8), and 8 (4/8) for the reviewers' edit (`receipts/lockstep_author_table_sum.txt`).

### 4.5 The merge of `main` `83999eba`

- **The tree is a clean three-way merge.** The merge tree `fc05a7f2` equals `git merge-tree
  --write-tree 0d9e5e7 83999eba` exactly, so the merge has no conflict and introduces no edit of its
  own.
  - The merge base is `5c71928a`. The 18 files only `main` changed equal `83999eba`'s, and the 6
    files only the lane changed equal `0d9e5e7`'s.
  - `09_verification.md` is the only file both changed. It carries `main`'s ADP hunk on top of the
    lane's IX/TS rows (`receipts/merge_r2_check.txt`).
- **Counts.**
  - `tb/adp_engine`: 1,348 checks, 1,348 PASS at head and at `83999eba` alone. That is `main`'s own
    count, against 1,328 at `6e950fea`.
  - `tb/aecp_notify`: 20 -> 30 (section 4.3).
  - The ADP campaign (`make mutants JOBS=3`): rc 0, both controls PASS, 41 of 41 KILLED, 43 checks.
    Every arm is at its README count, two of them by hand (`cfg-valid-no-reset` 9 and
    `gate-enable-dropped-top` 7, the "since lane P1" figures in their rows; `receipts/count_notes.txt`).
- **Other gates.** Lint: 41 of 41 LINT OK. `make check`: lint, wavedrom, links (1,120), matrix (115
  REQ, 94 rows, 0 untested) and parameters all OK. Its `stale` step failed only in a `cp -r` copy whose
  mtimes the copy reordered; `make stale` is rc 0 in the clone and in a fresh `git archive`
  (`receipts/make_check.log`, `receipts/make_stale.txt`).

### 4.6 The parent adoption patch

- **Content.** `parent-adoption-232-241f9184.patch` (sha256 `88ee5e96...2560`) touches only
  `scripts/xvlog.budget`. It removes the one line
  `protocol-processor:hdl/aecp/KL_aecp_notify.sv|VRFC 10-3380|pd_ix_w` and changes the section header
  from 3 to 2 findings. It is byte-equal to round 1b's `parent-adoption-pp232-xvlog-c10-5fabb46e.patch`.
  `5fabb46e..241f9184` changes neither the budget (blob `f3721542` at both) nor `xvlog_gate.py`.
- **It applies.** On a fresh dev `241f91845230ae410506dffb16b71937127fd175`, the c8, p2-p1 and c10
  patches and then this one all apply with `git apply --check` (`receipts/parent_patch_apply.txt`).
- **xvlog rc 1 -> 0, corroborated statically.** No xvlog is installed here.
  - The `pd_ix_w` use-before-declaration is gone at head. Synthesis reports every occurrence: 3
    `Synth 8-6901` lines for `pd_ix_w` at `main`, and none in `KL_aecp_notify.sv` at head.
  - The two remaining banked keys' identifiers (`cancel_hit_w` in `KL_pp_originator.sv:194`,
    `vd_push_w` in `KL_pp_rx_validator.sv:383`) still occur.
  - So the expected finding set is exactly the patched budget's two keys. The rc values themselves
    are the author's runs.
- **Gate 16.** The reported failure is the same two T30 INTERNAL law checks with the same figures as
  #643's own text: 227 and 285 of 292 PDUs, first-event delay 8.830..9.034 ticks. The parent consumer
  set was not run here (out of scope for this assignment).

### 4.7 Hosted checks at the exact head (read-only; `receipts/hosted_checks.txt`, 09:44Z)

- Workflow `hdl`, runs 37190824944 (push) and 37190826788 (pull_request):
  - `docs-gates` and `portability` succeeded in both;
  - `suites` was still in progress in both. In the push job (111402436205), step 5, "Lint (zero
    tolerance) + every suite", had already succeeded; the campaign steps 6 to 12 were running or
    pending.
- Hosted/act acceptance is the manager's.

## 5. Lens results at `2ea3dee2`

| Lens | Result | Artifact-specific evidence |
|---|---|---|
| Conformance | CLEAN | AC1: hierarchy and RAM reports published and re-derived (4.1). AC2: no AECP or notification buffer in flops (`u_resp` 260 FF, `rows_r` FD 0). AC3: suites and campaigns green at their counts (4.3, 4.5; hosted step 5). AC4: 50 MHz closure in four corners, LUT/FF/BRAM recorded (4.1). Behaviour identity: lockstep 0 mismatches (4.4); IX/TS pass on `main`'s RTL (4.3). AC5 is the manager's link (section 8) |
| RTL | CLEAN | `6e950fea..2ea3dee2` HDL comment-equal (4.1); the new index comment `KL_aecp_notify.sv:559-569` and 06's zero-content and `rst_n` statements checked against `:226`, `:355-357`, `:586-590`, `:973`, `:1044-1057`, `:1364-1385`; round 1's RTL review stands |
| Robustness | CLEAN | lockstep re-run at head: resets in W and W+1, a full registry, 9 shapes, random inputs, stamps across warm resets (4.4); IX6 now drives a reset inside the window in the committed bank |
| Tests | CLEAN | `tb/aecp_notify/sim_main.cpp:307-411` (IX5, IX5b, IX6a, IX6, IX6b, TS1-TS3) read against the RTL; 12 of 12 round-1 controls fail named checks (4.2); `notify_mutants.py` 47/47 at README counts (4.3); ADP campaign 41/41 (4.5) |
| Docs | CLEAN | `tb/aecp_notify/README.md` (IX5-IX6b, TS, 7-row record), `tb/pp_top/README.md:2294-2346`, `09_verification.md:283-299` (three notify sections: FT, IX, TS), `06_aecp_engine.md:904`; PR body figures and citations (`:551-603`, `:1365`, `:605-607`, `:609`, `:618`, `:727`, `:1098-1099` resolve); the published lockstep table and labels; `make check`; no U+2014 and no tool-identifying token added |

## 6. Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #232 AC1-AC5 and rulings; assignment 5976892215; PR body; `evidence-r2/vivado` (8 runs); lockstep; IX/TS on `main`'s RTL | R453-2 | `2ea3dee2cd92e5907a8942a8c32436ab2f46ff2d` |
| RTL | CLEAN | `6e950fea..2ea3dee2` HDL (comment-equal); `KL_aecp_notify.sv` index, row write, reset, stamps, `N_APPLY`; the merge tree | R453-2 | `2ea3dee2cd92e5907a8942a8c32436ab2f46ff2d` |
| Robustness | CLEAN | lockstep 144 runs / 288 M cycles with aimed resets and a full registry; IX6 | R453-2 | `2ea3dee2cd92e5907a8942a8c32436ab2f46ff2d` |
| Tests | CLEAN | `tb/aecp_notify` IX/TS; `notify_mutants.py`; round-1 controls x committed suites; ADP suite and campaign | R453-2 | `2ea3dee2cd92e5907a8942a8c32436ab2f46ff2d` |
| Docs | CLEAN | 06, 09, both READMEs, PR body, HANDOFF residue rows, published lockstep/probe/Vivado READMEs, `make check` | R453-2 | `2ea3dee2cd92e5907a8942a8c32436ab2f46ff2d` |

## 7. Real limits of this round

- **Vivado.** No Vivado or xvlog is installed on this host. The Vivado figures are re-derived from the
  published reports; whole reports are tied to their raw records by sha256. The log extracts
  (`Synth 8-*` lines, mapping reports) are the author's cuts of logs that remain in scratch. Their
  content is corroborated by the whole reports, not proved byte for byte.
- **Parent gates.** The xvlog gate's rc 1 -> 0 and gate 16's result are the author's runs. This round
  corroborates them statically (4.6) and did not run the parent consumer set.
- **Not run, per the assignment:** the full processor suite bank (hosted step 5 passed at the head),
  the ctr, D3, aecp, dispatch, acmp and gsi campaigns (the HDL is comment-equal to R453-1's head,
  where each was at its count), the Yosys, builder and parent banks, act, and hardware.
- **Physical calibration NOT RUN.** Skipped hosted contexts are not hardware proof.
- **Manager banks.** The manager's source static/builder and native banks at this head, which the
  assignment says passed, have no public receipt on the issue, the PR or the evidence branch at
  `83482f95`.
- **Lockstep coverage** is stochastic plus aimed, not formal.

## 8. Pending manager duties

- Hosted: completion of both `suites` jobs (111402436205, 111402442650) at the exact head, and
  hosted/act acceptance.
- Publish the source static/builder and native bank receipts for this head.
- AC5: link #232's results from epic #229. No #229 comment links them yet; the latest is 5978354239.
- The final current-dev candidate at the merge turn:
  - dev `241f9184` + c8 + p2-p1 + c10 + `parent-adoption-232-241f9184.patch`, with the processor
    gitlink at the merged head;
  - run the xvlog gate (expected `PASS (2 finding(s) == ratchet ...)`);
  - record gate 16's T30 checks against #643.
- Record a new #638 baseline A at the merge bank.
- Archive this packet. There is no residue to carry: R453-1 R1 and R452-1-F2 are applied.

R453-2 FINISHED
