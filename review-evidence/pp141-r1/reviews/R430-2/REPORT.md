[R430] POSITIVE - exact head a90ca735844a3e7a5bdfd2d1baeba24c95608992

# R430-2: independent internal delta review of protocol-processor PR #142 (closes #141)

Lane P141: SET/GET_CLOCK_SOURCE over INTERNAL, CRF and one source per AAF input. Exact head
`a90ca735844a3e7a5bdfd2d1baeba24c95608992`, tree `877a0f78e3b6f15c1159899c10d7ba5e3ca3c836`,
reviewed in a cleared context in an isolated detached clone. This round covers round 2
(`76b09ff0`, assignment #141 comment 5947144104, answering R431-1's MAJOR) and round 2b
(`a90ca735`, a `--no-ff` merge of `main` `2ebd4fe8` = PR #139, lane C6; assignment #141
comment 5950735422). R430-1 was POSITIVE at `4a40b179`.

Reconstructed from: the repository's README, `docs/README.md` and the hdl/tb READMEs
(the processor repository has no `AGENTS.md` or `CONTRIBUTING.md`); issue #141's body and
the manager's comments 5942683005, 5946147101, 5947144104 and 5950735422; the PR body
(Round 2 and Round 2b sections); `git diff 2ebd4fe8..a90ca735` and the history; the public
author packets `review-evidence/pp141-r1/author-r2` and `author-r2b` (milan-fpga branch
`pp141-review-evidence` at `9f6c270a`; the packet's `PR-BODY.md` equals the live PR body).
My own verdict and ledger were fixed in `receipts/verdict-before-prior-reviews.md` before I
opened the R430-1 or R431-1 report.

## Verdict

**POSITIVE.** R431-1 F1 is closed at this head. The merge keeps both sides exactly. Every
ROM equals main's, and every campaign patch plants the same words as at the lane head.
Every suite and every campaign I re-ran is rc 0, with failing counts equal to the README
records. There is no BLOCKER, MAJOR, MINOR or RESIDUE finding. One new SUGGESTION is
raised, and the four prior SUGGESTIONs are retained.

## The four judgments

### (1) R431-1 F1 closed

- **`git apply --check -v` of every patch** in the tree, each against a pristine export
  (`receipts/apply-check-<rev>.txt`):

  | Revision | Patches | Refused |
  |---|---:|---:|
  | 4a40b17 | 207 | 1 (`lk-prefix-zero-body`) |
  | 76b09ff | 207 | 0 |
  | 2ebd4fe8 | 205 | 0 |
  | a90ca735 | 207 | 0 |

  At the head, 184 of the 207 patches have at least one hunk placed at an offset (218 hunks
  in all). Both `sclks-*` patches apply at offset 25 (see S1).
- **The planted defects are unchanged** (`receipts/patch-refresh-diff.txt`,
  `plant-compare.txt`):
  - The `-`/`+` lines of `lk-prefix-zero-body`, `sclks-bound-three` and
    `sclks-bound-inclusive` hash identically at 39fd019 and at the head.
  - Each 39fd019 patch planted at 39fd019 and the same patch's refreshed form planted at
    76b09ff generate a byte-identical `ucode.hex`:
    - `lk-prefix-zero-body`: `c8c8edab…`, 98 words;
    - `sclks-bound-three`: `cb507184…`, word 1196;
    - `sclks-bound-inclusive`: `8342c858…`, word 1197.
  - The same holds for all 22 `gen_ucode.py` patches, and each one differs from the
    unmutated ROM.
- **The dispatch campaign, whole, at the head:** 4 distinct controls PASS (`aecp-dispatch`,
  `aecp-line`, `line-guards`, `d3`) and **37 of 37 KILLED**. All 37 failing counts equal the
  README table (`tb/pp_top/README.md:1071-1107`): `lk-prefix-zero-body` 7,
  `sclks-bound-three` 11, `sclks-bound-inclusive` 6. Receipts: `receipts/dispA.log`,
  `dispB.log`, `results/disp*.results.json`, `compare-pp_top-campaigns.txt`.
- **The PR body** corrects the round-1 re-measure statement ("Round 1 held that a
  comment-only change ... That was wrong") and the "no file cites `gen_ucode.py`" sentence.

### (2) The merge keeps both sides

- **The merge, redone:** I checked out `76b09ff` in a scratch clone and ran
  `git merge --no-ff 2ebd4fe8`. The merge had no conflict, and its tree is `877a0f78…`,
  the published tree (`receipts/merge-redo.txt`). The published parents are
  `76b09ff`, `2ebd4fe8`.
- **Stable patch-ids:** `03c842a7..76b09ff` equals `2ebd4fe8..a90ca735`
  (`d6247794…`), and `03c842a7..2ebd4fe8` equals `76b09ff..a90ca735` (`30d3367d…`).
  Each side's change is therefore carried exactly.
- **`hdl/` against main:** only `gen_ucode.py` differs, 6+/5−, comment lines only. With
  comments and whitespace tokens dropped, its code tokens are identical: 13,405
  (`receipts/hdl-vs-main.txt`). No `.sv`, `syn/`, script or workflow file differs.
- **ROMs** (`receipts/rom-regeneration.txt`, `rom-map.txt`):

  | Output | Lane head (76b09ff = 03c842a7 = 39fd019 = 4a40b17) | Main = merge |
  |---|---|---|
  | `ucode.hex` | `3559d0a6…`, 87 programs, 1,080 words | `518b900c…`, 89 programs, 1,107 words |
  | `ltn_rom.hex` | `23cc67ee…` | the same |
  | `image.bin` | `20356f59…`, 1,880 bytes | the same |

  - The program maps of main and the merge are identical.
  - Lane head and merge differ in 27 words, all C6's: E_IDNOTIF 464-469 (6) and
    E_SINFOUNS 480-500 (21).
  - E_SCLKS sits at 1184-1209 and E_SCLKSRF at 1144-1150, at both the lane head and the
    merge. Neither overlaps 464-469 or 480-500. Only those two C6 programs occupy 456-511.
- **The 22 `gen_ucode.py` campaign patches:** each plants the same word indices, with the
  same base and mutated values, at 76b09ff and at the head. None touches a C6 word
  (`receipts/plant-compare.txt`).
- **`tb/pp_top`'s five builds** are numbered consistently: default 1, fixture 2 (DV),
  identify 3 (ID), line 4 (AX), timebase 5 (TB). I checked the Makefile banner and
  recipes, `sim_main.cpp:20,109-110,13574-13630`, `pp_top_wrap.sv:30-36,526-535`, the
  README, 06, 08, 09, 00 and `aecp_mutants.py:57`. The lane's own text names no build
  number.
- **Each side's content is present:**
  - The wrap has `identify_button_i` (`:58`), `aecp_clk_src_index_o` (`:344`, wired at `:602`)
    and the `dbg_ident_gap_*` taps.
  - `D3ClockSourcePhase` runs at the end of section D3 (`sim_main.cpp:10750`).
  - 09 §8.2 carries the D3C row and "87", followed by C6's §8.3 and §8.4.

### (3) The re-measure

I re-ran every campaign at the head from `git archive` exports, one isolated tree per
stream, with pinned Verilator 5.050 (identity verified: `Verilator 5.050 2026-07-01 rev
v5.050`). Counts were compared with each README by script (`scripts/compare_readme.py`).
Prose-form records were matched by hand, and each is cited.

| Campaign | Ran as | rc | Result | Against the README |
|---|---|---|---|---|
| `aecp_dispatch_mutants.py` | 2 chunks (18 + 19 arms) | 0, 0 | 4 controls PASS, **37/37 KILLED** | 37 equal |
| `aecp_mutants.py` | 2 chunks (28 + 27) | 0, 0 | 5 controls PASS, **55/55 KILLED** | 55 equal (grouped rows expanded) |
| `d3_mutants.py --jobs 8` | whole | 0 | 3 goldens PASS, **87/87 KILLED** | 86 by script; `validator_admits_held_aecp`@rx_validator 4 = "4 FAILs" (`tb/rx_validator/README.md:86`). The D3C rows: `clks_row_two_bits` 10, `clks_restore_count_narrowed` 2, `clks_restore_index_narrowed` 4, `clks_restore_bound_inclusive` 4. The raised controls: `TRG_clks` 10, `RPL_clks` 5, `rule_ignored` 7, `unframed_reads_as_device_error` 42, `done_without_d3` 45 |
| `notify_mutants.py --jobs 3` | whole | 0 | 5 goldens PASS, **40/40 KILLED** | 40 equal |
| `acmp_mutants.py --jobs 2` | whole | 0 | 3 goldens PASS, **19/19 KILLED** | 18 by script; `cdl_not_44_rejected`@rx_validator 27 = "27 FAILs" (`tb/rx_validator/README.md:88`) |
| `gsi_mutants.py` | whole | 0 | **20 detected**; golden and restored PASS | as recorded |
| `name_wr_mutant.py` | whole | 0 | decode killed; golden and restored PASS | as recorded |
| `make -C tb/maap mutants` | whole | 0 | **32/32** | all equal (3 cross-suite records by hand: `tb/pp_top/README.md:1554,1564`, `tb/rx_validator/README.md:87`) |
| `make -C tb/adp_engine mutants` | whole | 0 | **32/32** | all equal |
| `tb/srp_top/mutants.py` | 6 label chunks | 0 ×6 | 11 distinct controls PASS, 78 entries (73 labels) KILLED, coverage rebuilt from the tags **65/65**: **90/90** | 69 equal the tables; the other 9 equal the re-measure prose that supersedes them (`tb/srp_top/README.md:376-378,409-413`) |
| `retry_mutants.py` | whole | 0 | **62 killed**, 7 equivalence, 1 performance | 62 equal |
| `srp_admission/mutants.py` | whole | 0 | **12/12** | 9 per-suite counts equal the prose (`tb/srp_admission/README.md:95-99`) |
| `desc_mem_guard/mutate.py` | whole | 0 | detected | as recorded |
| `make -C tb/nvm_port figures` | whole (clone at the head, `refs/pull/13/head` fetched as CI does) | 0 | all measured figures agree with the tree | |

The entry points, all rc 0:

| Command | Result |
|---|---|
| `./scripts/run_suites.sh` | **33 suites, 1,019,127 checks, 0 failing**. `tb/pp_top` has 9,168: 8,696 + 20 + 178 + 218 + 56 by build; section D3 has 150 |
| `./scripts/lint_hdl.sh` | 41 modules LINT OK |
| `make check`; `check-links.py`, `check-matrix.py`, `check-integrator-params.py`, `render-wavedrom.py --check`, `make stale`, `gen_matrix.py --check` | 41 mermaid and 18 wavedrom blocks, 1,035 links, 115 REQ rows, 17 GAP findings, 27 parameters, 94 rows with 0 untested |
| `check_upc_map.py`; `check_m9_opcodes.py --selftest` and plain | 61 constants and 89 entry points; 9/9 selftest; 30 opcodes |
| `git diff --check` against 2ebd4fe8, 76b09ff and 03c842a7 | clean |

**Merge-specific probe:** the README claims that the SET bound fixed at three fails only
D3C's eleven checks in the whole default build, and the row narrowed to two bits only
D3C's ten (`tb/pp_top/README.md:276-279`). C6 added ID0, NP, ST and RN to that build, so I
planted each control in a disposable export and ran the whole merged default build. It
has 8,696 checks, and the controls fail exactly 11 and 10 D3C checks, with no other
failure (`receipts/probe-sclks-bound-three.log`, `probe-clks_row_two_bits.log`). The
claim holds at the merge.

### (4) No port, parameter or RTL change beyond C6's

`hdl/` differs from main only in the `gen_ucode.py` comment, whose code tokens are
identical. The top and every ROM are byte-identical to main's. Against the lane head, the
merge brings only C6's `EN_IDENTIFY_NOTIF_P` (default 0) and `identify_button_i`, which
main already carries. The lane's only bench change is the wrap connecting
`aecp_clk_src_index_o` to a bench output; it changes no RTL.

## Lens results

- **Conformance, CLEAN.**
  - L6 (`07_memory_maps.md:135`), REQ-MDL-005 (`00:449`), REQ-AEM-013 (`00:406`), 06 §6.4's
    row (`06:465`) and the E_SCLKS comment (`gen_ucode.py:1654-1663`) are unchanged since the
    clause ruling. They credit membership to IEEE 1722.1-2021 §7.2.32, BAD_ARGUMENTS to
    Table 7-141 and the current index to §7.4.23.1.
  - C6's §7 text sits beside them without contradiction.
  - In the merged default build, D3C1 (SUCCESS byte-exact, one unsolicited notification at
    sequence 0) and D3C2 (BAD_ARGUMENTS carrying the index in force) pass.
- **RTL, CLEAN.** See judgments (2) and (4): the token comparison, the ROMs, the word map and
  the overlap check. Lint is clean over 41 modules.
- **Robustness, CLEAN.** The merge redone gives the same tree. All 207 patches apply. All 22
  `gen_ucode.py` patches plant identical words at the lane head and the merge. The old and
  refreshed patches give byte-identical mutated ROMs. Two default-build probes and one
  byte-wide-compare probe ran. S1 is a suggestion only.
- **Tests, CLEAN.** The suite sweep is 1,019,127 / 0 failing. Every campaign is rc 0, with
  counts equal to the records, as in the table above.
- **Docs, CLEAN.** `make check` and the CI docs gates pass, and the build numbering is
  consistent. The PR body's Round 2b figures (the patch-ids, the tree, the ROM sha256s,
  89 programs and 1,107 words, the per-build tallies, 1,035 links, 27 parameters) and its
  line-reference map hold at the head (`receipts/line-refs-a90ca735.txt`).

## Findings

There is no BLOCKER, MAJOR, MINOR or RESIDUE finding.

```text
S1 [R430-2] SUGGESTION Robustness, Tests - tb/pp_top/aecp_dispatch_mutations/sclks-bound-three.patch:3 (@@ -1659,7) and sclks-bound-inclusive.patch:3 (@@ -1660,8)
Authority/evidence: R431-1 F1 asked, as a preference, that these headers be regenerated against the head. Round 2 did that at 76b09ff, but C6's 25 lines above E_SCLKS moved them again. At the head they apply at 1684 and 1685, at offset 25 (receipts/apply-check-a90ca735.txt). They plant exactly the same words, 1196 and 1197 (receipts/plant-compare.txt). The PR body records the choice under "Not taken".
Impact: none today, because git apply places hunks by context. As with lk-prefix-zero-body in round 1, a stale header lets the next edit near E_SCLKS move context lines that nobody re-checks.
Required outcome (optional): regenerate both hunk headers at the merge's line numbers when the file is next touched.
Verification: apply_check.sh shows both patches "at 1684/1685" with no offset, and plant_words.py gives words 1196 and 1197.
```

### Prior public review findings at this head

| Prior finding | Disposition at a90ca735 | Evidence |
|---|---|---|
| R431-1 F1, MAJOR (Tests, Robustness, Docs): `lk-prefix-zero-body.patch` refused after the comment re-wrap, so the dispatch campaign aborted and hosted `suites` went red | **Closed** | 207/207 patches apply at the head (1 refused at 4a40b17, reproduced). The planted lines are identical and the mutated ROM is byte-identical to round 1's. The full campaign gives 4 controls PASS, 37/37 KILLED, and all counts equal the README. The PR body is corrected. Hosted `suites` at this head was still running when this review ended. Its lint, suites, SRP, MAAP, ADP and AECP-deadline steps had succeeded, and the dispatch step was in progress (`receipts/hosted-jobs.txt`). Final hosted acceptance is the manager's. |
| R431-1 S1 / R430-1 S2, SUGGESTION (Conformance, Docs): the D1 index numbers lack D1's own condition | **Retained as SUGGESTION** | `07_memory_maps.md:135` and `00_MILAN_COMPLIANCE_REVIEW.md:449` are unchanged in substance since 4a40b17. The processor reads no order. |
| R431-1 S2, SUGGESTION (Robustness, Tests): a refused patch aborts the dispatch campaign instead of counting UNPROVEN | **Retained as SUGGESTION** | `plant()` at `tb/pp_top/aecp_dispatch_mutants.py:152-158` is unchanged since 4a40b17. It is pre-existing driver behaviour. |
| R430-1 S1, SUGGESTION (Tests, Robustness): the SET compare's width (FMT_W) is not graded | **Retained as SUGGESTION**, re-probed at this head | I narrowed the compare to FMT_B in a disposable export. That changes ROM word 1197 from `706492000479` to `706482000479`, and the whole merged default build still passes 8,696/8,696 (`receipts/probe-fmtb.log`). The gap predates this PR and lies outside #141's frozen acceptance. |

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | L6, REQ-MDL-005, REQ-AEM-013, 06 §6.4, the E_SCLKS comment, C6's §7 text beside them; D3C1/D3C2 in the merged default build | R430-2 (rounds 2 and 2b; round 1 by R430-1) | a90ca735844a3e7a5bdfd2d1baeba24c95608992 |
| RTL | CLEAN | `hdl/` diff and code tokens against main; ROM, ltn and image regeneration at six revisions; program maps; overlap check; `lint_hdl.sh` | R430-2 | a90ca735844a3e7a5bdfd2d1baeba24c95608992 |
| Robustness | CLEAN (S1 suggestion) | merge redone; patch-ids; `git apply --check` of 207 patches at four revisions; 22-patch word plant at three revisions; three probes | R430-2 | a90ca735844a3e7a5bdfd2d1baeba24c95608992 |
| Tests | CLEAN | `run_suites.sh`; 14 campaigns (dispatch, AECP, D3, notify, ACMP, GSI, name-write, MAAP, ADP, SRP, retry, SRP admission, descriptor-guard, nvm_port figures) with README comparisons | R430-2 | a90ca735844a3e7a5bdfd2d1baeba24c95608992 |
| Docs | CLEAN | `make check` and CI docs gates; build numbering across bench, Makefile, README, 06/08/09/00; PR body Round 2/2b figures and line map; author r2/r2b packets | R430-2 | a90ca735844a3e7a5bdfd2d1baeba24c95608992 |

## Real limits

- **Specification text:** the IEEE 1722.1-2021 and Milan v1.2 texts are not on this host.
  The clause credits were not re-read in the specifications this round. They are unchanged
  since R430-1 and the manager's clause ruling, and the merge does not touch them.
- **Inputs identical to main:** the non-`tb/pp_top` campaigns (MAAP, ADP, SRP, retry, SRP
  admission, descriptor guard, nvm_port) read inputs byte-identical to main `2ebd4fe8`'s
  (`git diff 2ebd4fe8 a90ca735` is empty for their tb directories, `scripts/` and every
  `.sv`). I re-ran them anyway, and they confirm main's state as well as the merge's.
- **SRP campaign in chunks:** it ran as six label chunks. The 65/65 assertion coverage was
  rebuilt from the chunks' tags, not printed by one whole run.
- **D3 campaign restart:** a first `--jobs 2` run was stopped after 26 arms and restarted
  whole with `--jobs 8`. Only the complete second run is counted
  (`receipts/d3-partial-abandoned.log` is kept for transparency).
- **Job cap:** builds ran with Verilator's `-j 0` capped by a wrapper (1-4 jobs), so that at
  most 16 jobs ran at once. This changes parallelism only.
- **Not run here (manager-owned):** the parent consumer gates, the donor bank, hosted/act
  acceptance and the final current-dev candidate. No physical calibration, no hardware;
  field skips are not hardware proof.

## Pending manager duties

- Run the donor bank (9) and the parent consumer set (16, `test_builder.py` whole) at
  milan-fpga dev `cdf49d1a` with `parent-adoption-c4c6-ea3fb388.patch`. The author's gate 6
  did not complete `test_baremetal_profile_contract` within one foreground command.
- Confirm hosted `hdl` runs 37034569811 (push) and 37034574936 (pull_request) at this head
  finish green. `suites` was still running its dispatch step at the end of this review.
- Build the final current-dev candidate at the merge turn (source base `2ebd4fe8`, live dev
  `cdf49d1a`), and carry the four SUGGESTIONs at the owner's discretion.

## Packet

- `scripts/`: `rommap.py`, `plant_words.py`, `apply_check.sh`, `compare_readme.py`,
  `probe_default_build.sh`, `probe_fmtb.sh`, `verilator-capped`, `bg.sh`, `wait.sh`, and
  `RUN.md` (the exact command behind every receipt).
- `receipts/`: the raw logs, rc files, comparisons and per-campaign `results/*.json`.
  Every published file is listed in `MANIFEST.sha256`. Disposable trees stayed under
  `scratch/` and are not published.
- The review clone was never modified. At the end it is at the exact head and tree, with a
  clean `status --porcelain --ignored`. Index equals `ls-tree`, there are 0 blob mismatches,
  and the modes are 459 × 100644 and 13 × 100755. There are no gitlinks and no
  `.gitmodules` (`receipts/clone-integrity.txt`).

R430-2 FINISHED
