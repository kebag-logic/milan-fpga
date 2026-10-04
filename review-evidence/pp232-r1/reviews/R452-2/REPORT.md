[R452] POSITIVE - exact head 2ea3dee2cd92e5907a8942a8c32436ab2f46ff2d

# R452-2: internal independent review of PR #153 (milan-fpga #232, area lane), round 2

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #153.
- Exact head `2ea3dee2cd92e5907a8942a8c32436ab2f46ff2d`, tree
  `fc05a7f236eb72c8213bd1cf52fa70b87dae61d7`. Both were verified in the reviewer's detached clone,
  and the worktree was clean before and after (`receipts/runs/final_state.txt`).
- Source base `f4167536d358c996f4e1b70b875879c1651f85d3`. Merged `main` is `83999eba`. The
  previous review head was `6e950fea`.
- Review start: PR #153 comment 5978340250. Round R452-2. Assignment: milan-fpga #232 comment
  5976892215.
- **Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open at this head. Every prior
  public finding is resolved or applied (section 2):
  - R452-1 F1 and R453-1 F2 (MINOR): resolved by IX5, IX6 and TS3.
  - R453-1 F1 (MINOR): resolved; the Vivado evidence is now published and re-derives.
  - R452-1 F2 and R453-1 R1 (RESIDUE): applied as written.
  - R452-1 S1 (SUGGESTION): adopted.

## 1. Reconstruction (in order)

1. **Repository rules.** The processor repository has no AGENTS.md or CONTRIBUTING.md. The
   reviewer applied:
   - `docs/README.md` (the conventions and single-source rules);
   - `hdl/README.md` (a module is not done until its testbench is);
   - `docs/guides/hdl-engineer.md`.
2. **Issue kebag-logic/milan-fpga#232.**
   - Its frozen body: scope; acceptance criteria AC1 to AC5.
   - The public decisions in its comments:
     - the lever-5 scope addition (5967852823);
     - the lane rules (5970460015: identical behaviour; 100 MHz judged at the declared 50 MHz);
     - the STOP and ruling (c) (5973996744, 5974004216);
     - round 1b (5974077269);
     - the round-2 assignment (5976892215: items 1 to 5 and the gates);
     - the author's REVIEW READY at this head (5978213864).
3. **Authorities.**
   - Milan SS5.3.4.2 and SS5.4.5.3, as cited in the `KL_aecp_notify` banner.
   - 06 F06.5, the registry lifecycle.
   - 01 F01.5 (`P-NOTIF-QUEUE-DEPTH`).
   - The block's port list, unchanged.
   - milan-fpga #643, for gate 16's T30 figures.
4. **History and diff.**
   - `git diff f4167536..2ea3dee2` in full.
   - The round-2 delta `6e950fea..2ea3dee2`: three commits.
     - `f3abfc6`: coverage, 5 files.
     - `0d9e5e7`: residue, 2 files.
     - `2ea3dee`: `--no-ff` merge of `main` `83999eba`.
5. **Public evidence.**
   - milan-fpga `ed9f5f46:review-evidence/pp232-r1`: the round-1 packet, which holds no
     round-2 material.
   - The round-2 packet, archived after it on the same evidence branch (`pp232-review-evidence`)
     at milan-fpga `83482f957cef27bd8968f5a4e1831f7b570b6f1d`, under
     `review-evidence/pp232-r1/author-r2/`: HANDOFF, PR-BODY, the parent patch and
     `evidence-r2/`, 261 files.
   - The archive's `MANIFEST.json`, which records the original and published sha256 of each
     path-redacted file.
   - The PR body at this head, and the exact-head hosted check runs.
6. **Prior public findings** (R452-1, 5976816563; R453-1, 5976889224). They were read only after
   the reviewer's own pass over the diff and the evidence was complete. Their resolution is in
   section 2.

## 2. Findings

### Open findings at this head

None (no BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION is raised in this round).

### Prior public findings: resolution at `2ea3dee2`

| ID | Severity, lenses | Status at this head | Evidence |
|---|---|---|---|
| R452-1-F1 | MINOR, Tests | **RESOLVED** | See "R452-1-F1 / R453-1-F2" below. My ten round-1 controls, run with my round-1 `plant.py` and `clear_cycle_probe.sh` (byte-identical, `receipts/runs/r1-scripts.sha256`), each fail a named committed check. `override_set_only` fails IX6 and IX6b; `own_compare_new_row` fails IX5 |
| R452-1-F2 | RESIDUE, Docs | **APPLIED as written** | The PR body's inventory row "Registry identity index (new)" now reads "synthesis mapping report: ... implemented cells after optimization: 288 RAM64X1D (576 LUTs) and 16 RAM32X1D (32 LUTs), which with `rows_r`'s 64 and `cmdq_*`'s 24 RAM32M make `u_notify`'s 960 LUTRAM". The published HANDOFF §5 row (`author-r2/HANDOFF.md:176`) has the same text |
| R452-1-S1 | SUGGESTION, Docs | **ADOPTED** | `docs/architecture/06_aecp_engine.md:904` now says: "The index's correctness relies on its configuration-time zero content (an explicit `initial`), as the ROM images rely on `$readmemh`; `rst_n` leaves both the index and `rows_r` as they are" |
| R453-1-F1 | MINOR, Conformance, RTL, Docs | **RESOLVED** | See "R453-1-F1" below. Every figure the finding's Verification names re-derives from the published extracts, with the reviewer's own script and with the author's |
| R453-1-F2 | MINOR, Tests, Docs | **RESOLVED** | The same coverage as R452-1-F1. Its three named controls are committed as killed arms: `own_compare_new_row` (R453-1 calls it `own_vs_new_row`), `override_set_only` and `stamp_read_without_valid`. The lockstep bench is published with its control table corrected |
| R453-1-R1 | RESIDUE, Docs | **APPLIED as written** | `hdl/aecp/KL_aecp_notify.sv:559-562`: "re-indexes its row over two cycles: the cycle in which the row write lands (wr_en_r high) clears the old identity's bits (the write port still reads the old row then), and the cycle after it sets the new identity's". 06 `:904`: "over the row write's own cycle and the cycle after it". The PR body's item 1 has the RTL wording, with `wr_en_r` in code style. The wording is accurate: `N_APPLY` raises `wr_en_r` and `ix_clr_r` together (`:1364-1365`), and `ix_set_r <= ix_clr_r` (`:1057`) |

#### R452-1-F1 / R453-1-F2: the rewrite window's first cycle and the stamps' valid bit

**What the head adds** (`f3abfc6`):
- `tb/aecp_notify/sim_main.cpp:311-380` (`register_to_write`, `after_failure`,
  `rewrite_window`):
  - IX5 and IX5b: in the row write's own cycle, the reused row's previous controller C, which
    `rows_r` still holds, plus a failed probe for the row. The row must stay.
  - IX6a, IX6 and IX6b: a synchronous reset in E's row-write cycle. The row write and the clear
    land, but the set does not. E then re-registers into the same row, where in its first
    cycle only the comparator can match.
- `:382-411` (TS1 to TS3): a same-second change is held, and after a warm reset it goes out at
  once.
- `tb/pp_top/notify_mutants.py:284-294`: the three review faults as controls.
- The records:
  - `tb/aecp_notify/README.md:79-132`;
  - `tb/pp_top/README.md:2292-2346`;
  - 09 §8.4 (the IX and TS rows).

**Checked by reading the RTL.** The reset is synchronous (`notify_core`,
`always_ff @(posedge clk_i)`, `:972`). Neither the row write (`:355-357`) nor the index write
(`:587-590`) has a reset. So IX6a's premise holds: `rows_r[0]` holds E while the index holds
nothing for row 0. Faults that IX6 kills:
- `override_set_only`: in T+1 it reads the empty index.
- `no_override`: it reads the index in both cycles.

`own_compare_new_row` survives IX6, because there `wr_row_r` equals the row. IX5 kills it, since
in T+1 the incoming row is D and C must still match.

**Measured** (pinned Verilator 5.050, wrapper sha256 `905795b9...e92f`, all on `git archive`
trees of the exact head):

| Control (my round-1 `plant.py`, unchanged) | `tb/aecp_notify` named failures | `tb/pp_top` |
|---|---|---|
| `no_override` | IX4, IX6, IX6b | 10,416/10,416 PASS |
| `override_set_only` | **IX6, IX6b** | 10,416/10,416 PASS |
| `override_clr_only` | IX4 | 10,416/10,416 PASS |
| `no_clear` | IX1 | 10,416/10,416 PASS |
| `no_set` | IX3, IX4, IX6b | fails (GI section and others) |
| `last_chunk_ignored` | IX2 | 10,416/10,416 PASS |
| `clear_new_identity` | IX1 | 10,416/10,416 PASS |
| `own_compare_new_row` | **IX5** | 10,416/10,416 PASS |
| `register_not_reindexed` | IX3, IX4, IX5, IX6, IX6b | fails |
| `stamp_without_valid` | **TS3** | 10,416/10,416 PASS |

- **10 of 10 controls fail a named committed check.** In round 1, two of these (the bold
  rows) passed every committed suite.
  - Files: `receipts/runs/probe_named.txt` (rc 0), `receipts/probe/clearprobe-*.log`,
    `receipts/runs/clearprobe{1,2}.log`.
  - `stamp_without_valid` deletes `!ctr_sent_r[c] ||`. The committed
    `stamp_read_without_valid` replaces `(!ctr_sent_r[c]` with `(1'b0`. Both are the same
    logic, and both fail TS3.
- **`notify_mutants.py --jobs 3`:** rc 0. "47 of 47 KILLED by their named checks; goldens
  PASS". Compared by script with the two READMEs: 53 records (47 arms and 6 goldens), 0
  differing (`receipts/runs/notify-compare.txt`).
  - `override_set_only`: 2 (IX6, IX6b).
  - `own_compare_new_row`: 1 (IX5).
  - `stamp_read_without_valid`: 1 (TS3).
  - `ix_new_identity_unset` and `ix_rewrite_unmatched`: 3 each, as re-recorded.
- **The new checks on `main`'s RTL.** The head's bench, with `main` `83999eba`'s
  `KL_aecp_notify.sv` (byte-equal to `f4167536`'s), gives `30 checks: 30 PASS, 0 FAIL`
  (`receipts/runs/ixmain.log`). So IX5, IX6 and TS describe unchanged behaviour.
- **Counts.**
  - Default build: 10 lifecycle + 11 IX (IX1, IX2, IX3, IX4a, IX4, IX4b, IX5, IX5b, IX6a, IX6,
    IX6b) + 5 TS (TS1 to TS3 and the section's two REGISTER checks) = 26.
  - With FT's 4, the suite has 30. This matches the README (`:20`) and the measured
    `[build default] 26 checks`.
- **Lockstep bench.** Published under `evidence-r2/lockstep/`, with each round-1b control's
  diff. The control "comparator only in the set cycle" is relabelled to its real edit,
  `ix_busy_w = ix_set_r`, which also drops the clear. My edits `override_set_only` and
  `own_compare_new_row` are added as `controls-r2/*.diff`. This is consistent with what both
  round-1 reviews measured.

#### R453-1-F1: the Vivado evidence

- **Integrity.**
  - `sha256sum -c evidence-r2/MANIFEST.sha256`: 241 of 261 files OK. The other 20 are exactly
    the files that the archive's `MANIFEST.json` marks `path_redacted`. For all 265 `author-r2`
    files, the published bytes hash to the recorded `published_sha256`, and every
    `original_sha256` equals the packet's own MANIFEST entry.
  - Each run's `sources.tsv` gives the size and sha256 of each raw file, and some files are
    published whole. Over the eight runs, 76 whole files hash to their raw-file record, 12 of
    them through the recorded pre-redaction digest. Each run's `baseline.log` digest equals
    the `vivado/README.md` runs table: `3345c0ac...9079073` for `main`, `4d18c290...3eca3f37`
    for the head.
  - The extracts themselves (`log-extract.txt`, `timing-extract.txt`, `census.tsv`) can only
    be tied to their raw sources by the recorded digest, because the raw logs stay
    unpublished (Limits).
- **Re-derived by the reviewer's own parser** (`scripts/vivado_rederive.py`, rc 0,
  `receipts/runs/vivado_rederive.log`), reading the reports directly:
  - **Route at the round-1b merge, head minus `main`:**
    - LUT 50,671 - 51,434 = **-763** (logic -1,625, memory +862).
    - FF 57,660 - 59,691 = **-2,031**.
    - Slices -6; CARRY4 -150.
    - WNS 0.079 -> **0.274**; WHS 0.014 -> 0.023.
    - `u_notify`: LUT 3,270 -> 2,343 = **-927**; FF 3,299 -> 1,287 = **-2,012**; LUTRAM 96 -> 960.
    - `u_resp`: 345 LUT / 260 FF at both.
    - `u_d3`: 1,897 -> 1,931 LUT, 581 FF.
  - **Round 1 route:** -650 LUT, -1,950 FF, -15 slices, -147 CARRY4, WNS 0.116 -> 0.143.
  - **Standalone 1x1:** -894 LUT, -2,042 FF; `u_notify` -933 / -2,046.
  - **Standalone 8x8:** -925 LUT, -2,175 FF; `u_notify` -450 / -2,046.
  - **`Synth 8-7186`:** 0 in all four head runs; 16 in each of the four base and `main` runs.
    The line counts equal each extract's header count.
  - **`Synth 8-4445`:** 0 in all eight runs.
  - **`Synth 8-6901` for `pd_ix_w`:** 3 at `main` (`KL_aecp_notify.sv:557-559`), 0 at the head.
- **Mapping and census** (`r1b-head-6e950fea-route-1x1`):
  - `rows_r_reg | User Attribute | 16 x 128 | RAM32M x 64` (`log-extract.txt:80`).
  - 288 index lines `64 x 1 | RAM64M x 1` and 16 lines `16 x 1 | RAM16X1D x 1`.
  - The six `cmdq_*` lines total RAM32M x 24.
  - Census: `u_notify` RAM32M 88, RAM64X1D 288, RAM32X1D 16, so 88 x 4 + 288 x 2 + 16 x 2 = 960
    LUTRAM. `ctr_last_r_reg` 192 FDRE.
  - Route status: 104,326 of 104,326 routable nets fully routed, 0 with errors.
  - Signoff corners from the timing extract: Slow 0 C and 85 C +0.274 / +0.050; Fast 0 C and
    85 C +1.550 / +0.023. All four `*_negative.rpt` read "No timing paths found".
- **The author's `tools/rederive.py`:** rc 0, and its output is byte-equal to the published
  `rederive.txt` (`receipts/runs/author_rederive.*`).
- **The route stands for this head.** The two HDL files changed since `6e950fea`
  (`KL_aecp_notify.sv` and `KL_adp_engine.sv`) produce identical preprocessed text with
  comments stripped (`receipts/runs/hdl_comment_strip.log`: 1,029 and 830 lines). No other
  `hdl/` or `syn/` file changed.

## 3. Lens evidence

### Conformance: CLEAN

- **No interface change.** No port, parameter or register changes. The round-2 HDL delta is
  comments only (shown above), and round 1's lockstep equivalence (0 mismatches, 448 M cycles)
  carries over.
- **#232 acceptance** against the published evidence:
  - **AC1:** the hierarchy and "Distributed RAM: Final Mapping Report" extracts match 06 §7's
    storage table: `rows_r` and the index in distributed RAM, `cmdq_*` 24 RAM32M, stamps and
    flags in flops.
  - **AC2:** zero `Synth 8-7186` at every head. `u_resp` is 260 FF with no RAM in all eight
    runs.
  - **AC3:** the suites and campaigns below are green.
  - **AC4:** judged at the declared 50 MHz per 5970460015. The route closes in all four
    signoff corners. LUT, FF and BRAM tradeoffs are recorded.
  - **AC5:** a manager duty.
- **Lever 5:** stays ruled (c).
- **"Closes milan-fpga#232"** is allowed by 5974004216.

### RTL: CLEAN

- `0d9e5e7` changes only the index comment (`:559-569`). Its new wording matches the pipeline:
  - `wr_en_r` and `ix_clr_r` are raised together at `N_APPLY` (`:1364-1365`).
  - The clear's address is the old row, read through `ix_wr_row_w = rows_r[wr_ix_r]` (`:576`)
    in the cycle the write lands.
  - `ix_set_r <= ix_clr_r` (`:1057`).
- The merge `2ea3dee` keeps both sides. Parents are `0d9e5e7` and `83999eba`; the merge base is
  `5c71928a`.
  - **Lane side:** 7 files. For each, the changed lines of `git diff 5c71928a 0d9e5e7` equal
    those of `git diff 83999eba 2ea3dee`.
  - **`main` side:** 19 files (PR #152: the ADP walk, 11 mutation patches,
    `KL_adp_engine.sv` comments, 00, 04 and 09). For each, the changed lines of
    `git diff 5c71928a 83999eba` equal those of `git diff 0d9e5e7 2ea3dee`.
  - `09_verification.md` is the only file both sides changed, and it carries both hunks.
- `scripts/lint_hdl.sh`: rc 0, 41 of 41 LINT OK (`receipts/runs/lint.log`).

### Robustness: CLEAN

- The reset-inside-the-window path is now graded by a committed check (IX6), not only by
  lockstep.
- The dropped-stamp-reset path is now graded by TS3: after a warm reset, a same-millisecond
  change goes out at once, so a stale stamp is never read.
- The index's reliance on configuration-time zero content is documented (06 `:904`).
- Exhaustion behaviour is unchanged.

### Tests: CLEAN

- **R452-1-F1 and R453-1-F2 resolved** (section 2): 10 of 10 reviewer controls fail named
  checks; notify 47 of 47 at the README counts; the new checks pass on `main`'s RTL.
- **`scripts/run_suites.sh` at the head:** rc 0, 33 suites, **1,021,485 checks**, 0 failing
  (`receipts/runs/suites.log`).
  - `aecp_notify` 30 (20 at round 1b).
  - `adp_engine` 1,348 (`main`'s PR #152).
  - `pp_top` 10,416.
- **The merge's campaign `make -C tb/adp_engine mutants JOBS=3`:** rc 0, 43 checks PASS. Both
  controls PASS, and 41 arms are KILLED with none surviving (`receipts/runs/adp.log`).
  - Compared with `tb/adp_engine/README.md`, 39 of 41 match on the row's first integer
    (`receipts/runs/adp-compare.txt`).
  - The other two match the count their rows give in prose, which the comparison script does
    not parse: `cfg-valid-no-reset` measured 9 ("9 since lane P1's AD8 and AD9");
    `gate-enable-dropped-top` measured 7 ("At the head of lane P1 it fails 7").
  - The lane does not touch those rows.

### Docs: CLEAN

- **The round-2 records match the runs:**
  - `tb/aecp_notify/README.md` (build table 10 + 11 + 5; IX4 to IX6b; TS; seven controls with
    counts);
  - `tb/pp_top/README.md:2292-2346` ("47 of 47");
  - 09 §8.4 ("three of the notification block's": FT, IX, TS).
- **The PR body's line citations resolve at this head:** `:336`, `:337`, `:379-384`, `:404`,
  `:410`, `:551-603`, `:582-594`, `:585`, `:605-607`, `:609`, `:618`, `:727`, `:1098-1099`,
  `:1365`.
- **The PR body's round-2 figures equal the reviewer's measurements:** 1,021,485 checks; notify
  47/47; ADP 41/41; lint 41/41; `make check`; the Vivado deltas.
- **`make check`:** rc 0 (1,120 links; 115 REQ rows; 94 matrix rows, 0 untested; 28
  parameters). **`scripts/gen_matrix.py --check`:** rc 0.
- **Prior residue:** both items applied as written (section 2).

## 4. Parent adoption patch and gate 16

- **`parent-adoption-232-241f9184.patch`** (sha256 `88ee5e96...2b72560`). It is byte-equal to
  round 1b's `parent-adoption-pp232-xvlog-c10-5fabb46e.patch`, as the author states.
  - Its only change is to `scripts/xvlog.budget`: it lowers the submodule section from 3 to 2
    findings and removes `KL_aecp_notify.sv|VRFC 10-3380|pd_ix_w # line(s) 557`.
  - At milan-fpga dev `241f9184`, c8-bbf704ec, p2-p1-1269cdaf, c10-1269cdaf and this patch
    each pass `git apply --check` and apply in order (`receipts/runs/parent_apply.log`).
  - The resulting budget holds exactly `KL_pp_originator.sv|...|cancel_hit_w # 194` and
    `KL_pp_rx_validator.sv|...|vd_push_w # 383` (`receipts/parent/`).
- **Corroboration of xvlog rc 1 -> 0.** xvlog itself is not available here, so this comes from
  two other sources:
  1. The reviewer's declaration-order scan (`scripts/decl_order_scan.py`,
     `receipts/runs/decl_order_scan.log`). It flags `pd_ix_w` at `main` (first use 557,
     declaration 667) and not at the head. For both remaining keys it gives the budget's lines:
     194, and 383.
  2. Vivado's own `Synth 8-6901` lines in the published extracts: `pd_ix_w` at `main` `:557`;
     at the head only `cancel_hit_w`/`cancel_ix_w` (194/195) and `vd_push_w`/`vq_full_w` (383)
     among processor files.
- **Gate 16 (T30).** The author's figures at this head are `got=227 exp=292` and
  `got=285 exp=292`, first-event delay 8.830..9.034 ticks. These equal milan-fpga #643's own
  statement of the defect ("227 of 292 PDUs", "285 of 292, delay 8.830..9.034 ticks"). The
  processor's logic is cycle-identical to `main`'s, so the boot timing that sets the feed's
  phase cannot differ. This supports "equal to `main`'s, #643". Gate 16 was not re-run here
  (Limits).

## 5. Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #232 body, AC1-AC5 and rulings (5967852823, 5970460015, 5974004216, 5976892215); 06 §7 against the published mapping, hierarchy and timing extracts; comment-stripped HDL equality since `6e950fea`; port and parameter list unchanged | R452-2 | 2ea3dee2cd92e5907a8942a8c32436ab2f46ff2d |
| RTL | CLEAN | `KL_aecp_notify.sv:336-357`, `:551-603`, `:972`, `:1043-1057`, `:1364-1365`, `:1450-1455`; `0d9e5e7`; merge `2ea3dee` per-file change-set equality (7 lane, 19 `main`); lint 41/41; Vivado `Synth 8-7186`/`8-6901` extracts | R452-2 | 2ea3dee2cd92e5907a8942a8c32436ab2f46ff2d |
| Robustness | CLEAN | reset in the row write's own cycle (IX6, read against the synchronous reset and the reset-free row and index writes); stamp valid bit across warm reset (TS3); 06 zero-content note; exhaustion paths unchanged | R452-2 | 2ea3dee2cd92e5907a8942a8c32436ab2f46ff2d |
| Tests | CLEAN | 10 round-1 controls via unchanged `plant.py` + `clear_cycle_probe.sh` (10/10 named); `notify_mutants.py` 47/47 at README counts; IX/TS on `main`'s RTL 30/30; suites 1,021,485; ADP campaign 41/41; published lockstep control table | R452-2 | 2ea3dee2cd92e5907a8942a8c32436ab2f46ff2d |
| Docs | CLEAN | `tb/aecp_notify` and `tb/pp_top` READMEs, 09 §8.4, 06 `:904`, RTL comment `:559-569`; PR body citations and round-2 figures; `evidence-r2` READMEs, MANIFEST and redaction record; `make check`, `gen_matrix --check` | R452-2 | 2ea3dee2cd92e5907a8942a8c32436ab2f46ff2d |

## 6. Real limits

- **No Vivado or xvlog is available to the reviewer.**
  - The Vivado figures are re-derived from the published reports and extracts. The raw
    `baseline.log` files and full timing reports are tied to them only by recorded sha256.
    76 whole files do verify against that record.
  - xvlog rc 1 -> 0 is corroborated statically and by Vivado's `Synth 8-6901` lines, not
    executed.
- **No new route was run for this head.** The round-1b route applies because the head's HDL is
  equal to `6e950fea`'s with comments stripped.
- **Not re-run in this round:**
  - the parent consumer set, including gate 16 (parent banks are out of scope here; gate 16's
    figures are checked against #643's record instead);
  - the ctr, D3, aecp, dispatch, acmp, gsi and name_wr campaigns, the Yosys gate and the
    lockstep bench. Since R452-1 ran them at `6e950fea`, no HDL logic, `tb/pp_top` bench or
    their drivers changed; only `notify_mutants.py` did, and it was re-run;
  - R453-1's own probe scripts (another reviewer's). Its three named controls are covered by
    the committed arms and by my equivalent edits.
- **Hosted checks at the exact head** (09:31 UTC): `docs-gates` and `portability` completed with
  success in both event contexts; `suites` was in progress in both. Hosted/act acceptance is
  the manager's.
- **Physical calibration NOT RUN.** No hardware was used, and field skips are not hardware
  proof.
- **This is source validation,** distinct from the final current-dev candidate.
- **Resource note:** the review unit's memory peak was 11.2 GB of its 12 GB cap.

## 7. Pending manager duties

- Build the final current-dev candidate at the merge turn: source base `f4167536`, live dev
  `241f9184`, with c8 + p2-p1 + c10 + `parent-adoption-232-241f9184.patch`.
  - Gate 9 (xvlog) must be rc 0 with the patch.
  - Gate 16's two T30 checks go against #643 / PR #648 if they still fail.
- Hosted/act acceptance, including the `suites` jobs still in progress at 09:31 UTC.
- Link #232's results from epic #229 (AC5).
- Record a new #638 baseline A at the merge bank.
- The assignment's evidence pointer (`ed9f5f46`) predates round 2. The round-2 packet this
  review relied on is at milan-fpga `83482f95` (`pp232-review-evidence`), and it should be the
  one the merge record cites.

## 8. Receipts

- **`scripts/`:**
  - `r1/`: the round-1 scripts, byte-identical to R452-1's (`receipts/runs/r1-scripts.sha256`);
  - `probe_named.py`, `vivado_rederive.py`, `decl_order_scan.py`, `final_state.sh`,
    `collect_receipts.sh`.
- **`receipts/`:**
  - `runs/`: logs and rc files of every run above, the comparisons and the hosted-check listing;
  - `probe/`: the 20 clear-cycle probe logs;
  - `campaigns/`: the notify `results.json` and its per-arm logs;
  - `parent/`: the budget after the four patches, and its cumulative diff.
  - Local paths are replaced by `$PACKET`, `$CLONE` and `$HOME`.
- Every published file is listed in `MANIFEST.sha256`.
- After all probes, the reviewer clone is at the exact head and tree. The worktree is clean. The
  index equals HEAD's tree (515 entries). Every tracked file's bytes and mode equal its blob.
  The repository has no submodule gitlinks (`receipts/runs/final_state.txt`, rc 0).

R452-2 FINISHED
