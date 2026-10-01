# [A471] Round 3 handoff, lane C5b (AECP dispatch and response, PR #138)

Status: REVIEW READY at head `441d64630aa0143fa43f1049a6860cd9ed60e71e` (not pushed). Items 1-3
are done in the assignment's order; no STOP condition arose (no port, parameter, RTL or other
parent-visible processor change). Every processor suite, entry point and campaign is rc 0 / KILLED
in full at the head, and the sixteen parent consumer commands are rc 0 with the C4 disposition
line applied. A host reboot at about 12:02 cut the session during the D3 campaign's second
chunk; that chunk ran again whole (62 mutants, rc 0) and its partial output is not counted.

- Branch `c5b-aecp-dispatch`, start head `2acd4025782bff4aabbae73252476be34ea8b00d`.
- Assignment: issue #76 comment 5927100611. TAKEN posted as issue #76 comment 5927106731;
  REVIEW READY (head `441d646`) as issue #76 comment 5932625763.
- Items: (1) merge `main` `3f3ea56b`; (2) R417-2 F1 README mutation record #53 arm count;
  (3) R417-2 S3 CI step for `make -C tb/pp_top aecp-dispatch-mutants`, S1 and S2 if cheap.

## 1. Merge resolution

Commit `a8fe574` (parents `2acd4025`, `3f3ea56b`), a merge commit; merge base `d5f73bac`.
Main brought PR #137 (lane C4, ACMP coverage): `tb/acmp_listener`, `tb/acmp_nvm`,
`tb/rx_validator` (the 96-byte ACMPDU), `tb/maap/README.md`, 00 GAP-15's row, 09's V3 row,
`tb/pp_top/acmp_mutants.py` (an inline-edit campaign, 19 rows), the wrap's four
`acmp_bound_*_o` taps and pp_top section AC (AI/AS legs, `--acmp-only`). Main changed no
`hdl/`, `.github/`, `.gitattributes`, `scripts/` or Makefile.

Conflicts, both in tb/pp_top, resolved keeping both sides:

| File | Lane | Main | Resolution |
|---|---|---|---|
| `tb/pp_top/sim_main.cpp`, the helper after `run_dr3a` | `run_aecp_dispatch_focus` (A5b + M9, `--aecp-dispatch-only`) | `run_acmp` (section AC, `--acmp-only`) | both functions, the lane's first, each whole |
| `tb/pp_top/sim_main.cpp` `main()` `one_section` | `... adp_only \|\| maap_only \|\| aecp_only` | `... acmp_only \|\| adp_only \|\| maap_only` | one OR of all seven flags, split over two lines; main's `if (!one_section \|\| acmp_only) run_acmp(h);` (auto-merged) and the lane's `aecp_only` calls kept |
| `tb/pp_top/README.md` tail | section AX | section AC | both: AC first (it runs after D3, inside the default build), then AX (after AD) |

Auto-merged: `docs/00_MILAN_COMPLIANCE_REVIEW.md`, `docs/architecture/09_verification.md`,
`tb/pp_top/pp_top_wrap.sv`.

Checks at the merge (scratch scripts outside the tree):
- 54 lane-only files equal `2acd4025`, 7 main-only files equal `3f3ea56b`; `hdl/`, `.github/`,
  `.gitattributes`, `scripts/` equal the lane side.
- In each of the five both-sided files, every line either side added is in the merge, except
  the two `one_section` lines replaced by their union.
- Moved patches: none. Every patch targets `hdl/`, which main did not touch; `git apply --check`
  passes for all 163 (35 aecp_dispatch, 28 adp_engine, 27 maap, 73 srp_top), with the same
  offsets as at `2acd4025`. Every edit of main's `acmp_mutants.py` (19 rows) finds its old text
  exactly once at the merge, including the `hdl/top/protocol_processor_top.sv` anchors the
  lane's comment changes could have moved.
- `make -C tb/pp_top` rc 0: 8,605 checks = 8,367 default (8,324 + AC's 43) + 20 fixture + 218 line.

## 2. R417-2 F1

Commit `0de4234`. `tb/pp_top/README.md:838`, the `lk-prefix-zero-body` row (the issue #53
reproduction): the stray `|` before the count is removed, so the row has the header's four
cells and renders `7` under "Failing checks".

- Re-measured at the merge `a8fe574`: `aecp_dispatch_mutants.py` in three `--only` chunks,
  35 of 35 KILLED, controls `aecp-dispatch` (x3), `aecp-line`, `line-guards` PASS;
  `lk-prefix-zero-body` fails 7 (LK1/LK3's five non-zero bodies, LK3b, LK3c), as before the
  merge. Every other arm's count equals its README cell (a scratch script compares the
  campaign's `results.json` with the table: 35 rows, 0 differ).
- A table-shape scan (scratch `md_table_cells.py`, GFM cell splitting) over every markdown file
  the PR changes (`git diff --name-only 0451d83d`, 13 files) finds this row before the fix and
  two rows after it, both older than the lane base `0451d83d` and outside this lane's lines:
  `docs/guides/integrator.md:365` (`d3_unflushed_o`, from 39789f98) and
  `tb/pp_top/README.md:672` (M12, from 2ca3e9b8); each has a `||` inside a code span. Left
  as they are (not this lane's rows); recorded here for the manager.
- The reviewer's own verification command (the R417-2 packet's `check_md_table_cells.py
  tb/pp_top/README.md`, run read-only from the packet) reports 0 rows off their header at
  `441d646` and 1 at `2acd4025` (`:838`, this row). It does not split on a `|` inside a code
  span, so it does not flag `:672`; GFM itself does split there unless the pipe is escaped.
- `make check` rc 0.

## 3. R417-2 S3, S1, S2

All three taken. No RTL change; no port, parameter or parent-visible change.

- **S3** (commit `d6b2a23`): `.github/workflows/hdl.yml`, job `suites`, a step "AECP dispatch
  mutation campaign" after the ADP campaign, in the form of the SRP, MAAP and ADP steps
  (`export PATH="$HOME/verilator/bin:$PATH"`, then `make -C tb/pp_top aecp-dispatch-mutants`).
  `tb/pp_top/README.md`'s campaign paragraph says the HDL workflow runs it (as
  `tb/srp_top/README.md` does for its campaign). The workflow parses (YAML load: the step sits
  between "ADP mutation campaign" and "Traceability matrix"). The exact CI command ran at the
  head in one invocation (gate table below). The hosted run is the manager's: nothing is pushed.
- **S1** (commit `d2b3326`): `scripts/check_m9_opcodes.py` `RE_DECLARED` keys on
  `\b(?:localparam|parameter)\b`, so an `OP_*_C` the `parameter` keyword declares is counted
  and, since `RE_ENGINE` reads only `localparam logic [15:0] ... = 16'hXXXX;`, refused as
  unparsed instead of dropping out of the comparison. A ninth selftest fixture
  (`parameter logic [15:0] OP_GET_NAME_C = 16'h0011;` beside a bench without 0x0011) must fail;
  the docstrings say nine fixtures, seven failing. The suggestion's other form
  (`OP_[A-Z0-9_]+_C\s*=` anywhere) was not used: it would also match a comparison `OP_X_C ==`.
  Evidence (scratch copies of the script, the engine and the bench):
  - selftest 9 of 9; the gate passes at the head (30 opcodes);
  - the old pattern on the new selftest: 8 of 9, "an OP_*_C parameter fails" (so the fixture
    is load-bearing);
  - a new `parameter logic [15:0] OP_PROBE_NEW_C = 16'h0077;` added to a copy of the engine:
    the old gate PASSES (30 opcodes, silent), the new gate FAILS naming `OP_PROBE_NEW_C`;
  - the engine's `OP_GET_NAME_C` rewritten with `parameter`: the new gate names it unparsed
    and 0x0011 unmatched;
  - the reviewer's packet probe `probe_m9_gate_forms.py` at `441d646`: "9 forms, 0
    unexpected" (the `parameter` form now fails as the probe expects).
- **S2** (commit `441d646`): 07 §3.3.1, the sentences on the legal line (`P-DESC-LINE-BYTES`,
  576..1008, the elaboration refusal and the reasons for both bounds) move after the 530-byte
  worst case and the Annex C comparison, so "That worst case" again follows "the largest
  descriptor §3.2 can produce". No word changed (a word diff shows the move only).
- `make check` rc 0, `git diff --check` rc 0 before each commit.

## Parent-visible list (supersedes round 2's at `441d646`)

Round 3 changes no RTL, port, register or parameter (`git diff 2acd4025 441d646 -- hdl` is
empty). Items 1-8 and 11 are round 2's, still true at this head; 9, 10 and 12-14 are new or moved.

1. No port, register or parameter of `protocol_processor_top` is added or removed.
   `DESC_LINE_BYTES_P` has a stated and enforced legal range, a multiple of 8 from 576 to 1008
   (`P-DESC-LINE-BYTES`, F01.5); any other line is refused at elaboration naming
   `DESC_LINE_BYTES_P` (a Verilator USERERROR warning: fatal to a zero-warning lint or
   synthesis, not to a `-Wno-fatal` simulation build). The parent's 576 is the floor.
2. The response buffer is exactly the `16 + DESC_LINE_BYTES_P` reservation at `RESP_BASE_P`;
   nothing is written past it. No change at 576.
3. SET_CONTROL's out-of-range BAD_ARGUMENTS carries the value in force (IEEE 1722.1-2021
   7.4.25.1).
4. The locked refusals of SET_SAMPLING_RATE, SET_CLOCK_SOURCE and SET_CONTROL carry the value
   in force.
5. GET_AUDIO_MAP pages of 63..71 records are served whole (above cdl 524; slot 4 from 66);
   above 71 NO_RESOURCES with count 0; `P-MAP-SUBSET-CH-MAX` = 71.
6. READ_DESCRIPTOR of configuration-0 AUDIO_UNIT, CLOCK_DOMAIN and STREAM_INPUT/OUTPUT carries
   the value a SET or the D3 restore stored; otherwise, or for a STREAM too short for the lane,
   the image unchanged.
7. Observation, no processor action: the nxndv shape's STREAM_INPUT 1 face/image
   `current_format` disagreement before a SET.
8. The lane's mutation driver is `protocol-processor/tb/pp_top/aecp_dispatch_mutants.py`
   (`aecp_dispatch_mutations/`, `aecp-dispatch-mutants`); with `tb/pp_top/line_guards.py`
   neither is a DUT-source reader, so no `DUT_READER_DISPOSITIONS` entry for this lane.
9. NEW: this head carries processor `main` `3f3ea56b` (#137, lane C4), merged. Its
   `tb/pp_top/acmp_mutants.py` needs the parent's `DUT_READER_DISPOSITIONS` line that
   `parent-c4-disposition.patch` adds to `scripts/measure_test_evidence.py`; the consumer set
   below ran with it applied (without it the gate is rc 1 naming that file UNEXPLAINED; with
   it the ratchet reports it can be lowered to 72, the parent's edit). Its other items (the wrap's `acmp_bound_*_o` taps are bench-only)
   are that lane's to list.
10. NEW: the processor's HDL workflow runs `make -C tb/pp_top aecp-dispatch-mutants` (CI only;
    nothing the parent builds or reads).
11. Rows that can cite the grading at adoption (`docs/reference/MILAN_COMPLIANCE_MATRIX.md`):
    5.4.2.4 (AX RD0..RD4, OV, RB), 5.4.2.13-.18 (AX LK incl. LK3b/LK3c), 5.4.2.26 (AX PG),
    9.3.5.3.3 (A5b, M9).
12. MOVED: processor suite totals at this head: `tb/pp_top` 8,605 over three builds
    (8,367 + 20 + 218; AC adds 43), `tb/acmp_listener` 2,988, `tb/rx_validator` 555,
    `tb/ucpu` 398; the 33 suites 1,018,518.
13. NEW: `scripts/check_m9_opcodes.py` also refuses a `parameter`-keyword `OP_*_C`; its
    selftest is nine fixtures, seven failing (processor-internal pre-gate of `run_suites.sh`).
14. Docs only: 07 §3.3.1's sentence order (S2); the pp_top README's mutation-table cell (F1).

## Environment

- Verilator 5.052 (`/usr/bin/verilator`, sha256 `098b09b1...a417581`) behind a scratch wrapper
  outside every tree (`$VALIDATION_STORAGE/c5b-a471/bin/verilator`) that rewrites `-j N`/`-jN` to
  `-j 8`; nothing else changes. Yosys 0.66. The parent's `xvlog_gate.py` finds Vivado `xvlog`
  itself. Heavy builds ran one at a time.
- Commands longer than the 600 s bound on one foreground command were started detached
  (`setsid nohup`, output to a scratch log ending `rc=N seconds=S`) and awaited in the foreground
  before anything else heavy started; nothing is left running. The make-target campaigns ran
  as the workflow's exact commands, with `MUTANT_OUTPUT` pointed at scratch.
- The host reboot at about 12:02 killed the D3 campaign's second chunk mid-run (19 of its
  mutants had printed KILLED). That partial log is kept aside
  (`logs/d3-mutants-c2-cut-by-reboot.log`) and not counted; the chunk's 62 mutants ran again
  as one invocation, rc 0.
- Scratch parent `$VALIDATION_STORAGE/c5b-a471/parent-e4b771f9`: a `git archive` export of the
  trusted milan-fpga dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`, committed locally; its
  976 regular files equal the trusted index (blob for blob). `gptp-processor` `5dce647a` and
  `third_party/verilog-axis` `48ff7a7e` at their recorded pins; `protocol-processor` a scratch
  clone of this lane at `441d646`, gitlink committed at it; `external` recorded, uninitialized.
  `parent-c4-disposition.patch` applied with `git apply` and committed (`d390e67`, one file,
  +4). The trusted checkout was only read.
- Receipts in `receipts/` here (all small): `merge-a8fe574.txt`,
  `aecp-dispatch-mutants-merge-a8fe574.txt`, `suites-441d646.txt`, `entry-points-441d646.txt`,
  `aecp-dispatch-mutants-441d646.txt` and `.json`, `acmp-mutants-441d646.txt`,
  `d3-mutants-441d646.txt`, `other-mutants-441d646.txt`, `s1-probe-441d646.txt`,
  `parent-gates-441d646.txt`. Full logs stay under `$VALIDATION_STORAGE/c5b-a471/logs`.

## Suite table (head `441d646`)

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh`, one invocation, on a clean `git archive` export of the head | 0 | pre-gates: 58 engine constants and 86 entry points agree; M9 selftest 9 of 9; 30 opcodes swept. 33 suites, 1,018,518 checks, 0 failing (`tb/pp_top` 8,605 = 8,367 + 20 + 218; `tb/acmp_listener` 2,988; `tb/acmp_nvm` 360; `tb/rx_validator` 555; `tb/srp_admission` 991,231; `tb/ucpu` 398) |
| `./scripts/lint_hdl.sh` | 0 | 41 modules LINT OK |
| `make check` | 0 | 41 mermaid + 18 WaveDrom; links 994; matrix 115 REQ / 17 GAP; modmatrix 94 rows, 0 untested; parameters 26/26/26; stale |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `./syn/yosys/run.sh` (on the export) | 0 | 36 tops YOSYS OK; `KL_aecp_engine` Xilinx map OK |
| `make -C tb/pp_top fixture-guards`, `line-guards` (inside the pp_top `make`) | 0 | 4 cases PASS; 6 cases, 0 failing (pp_top's 20 and 218 are its VID-fixture and line builds) |
| `python3 tb/desc_store/test_gen_desc_image.py` | 0 | 6 tests OK |
| `git diff --check 0451d83d HEAD`; `git diff --check 3f3ea56b HEAD` | 0 | |
| `make -C tb/nvm_port figures` (after `git fetch origin refs/pull/13/head`, as the workflow does) | 0 | 46 builds; baseline 136/0; 47 figure rows, all `[ok ]` |

## Mutant table (head `441d646`)

| Driver | rc | Result |
|---|---:|---|
| `make -C tb/pp_top aecp-dispatch-mutants` (the new CI step's command, one invocation, 7 min 50 s) | 0 | 35 of 35 KILLED by their named checks; controls `aecp-dispatch`, `aecp-line`, `line-guards` PASS; every count equals its README cell (`lk-prefix-zero-body` 7) |
| the same driver at the merge `a8fe574`, three `--only` chunks | 0 each | 35 of 35 KILLED; controls PASS |
| `tb/pp_top/acmp_mutants.py --jobs 1 --only`, two chunks (main's C4 campaign) | 0 each | 19 of 19 rows KILLED (7 + 12); goldens `acmp_listener`, `pp_top`, `rx_validator` PASS |
| `tb/pp_top/d3_mutants.py --jobs 1 --only`, two chunks (21; 62) | 0 each | 83 of 83 KILLED; goldens PASS in both |
| `tb/pp_top/gsi_mutants.py` (one invocation, 16 min) | 0 | 20 detected by named checks; golden and restored PASS |
| `tb/pp_top/name_wr_mutant.py` | 0 | decode killed; golden and restored PASS |
| `make -C tb/maap mutants` (one invocation) | 0 | 29 of 29 arm rows KILLED (27 labels); controls `maap`, `pp_top maap-internal`, `rx_validator` (555/0) PASS |
| `make -C tb/srp_top mutants` (one invocation, 32 min) | 0 | 78 of 78 KILLED; 11 controls PASS |
| `make -C tb/adp_engine mutants` (one invocation) | 0 | 30 of 30 KILLED; controls `adp_engine`, `pp_top adp-config` PASS |
| `tb/srp_admission/mutants.py` (one invocation, 12 min) | 0 | 12 of 12 PASS (3 controls; 3 arms x 3 suites detected) |
| `tb/acmp_talker/retry_mutants.py` (one invocation, all mutations) | 0 | 62 killed; 7 equivalence and 1 performance controls; baseline and restored rc 0 |
| `tb/desc_mem_guard/mutate.py` | 0 | hold-deleted mutant detected |
| `tb/ucpu` by hand in scratch | — | golden 398/0; D8 flag ignored 2 (P11b); batch exception dropped 2 (P11c); `rd-tail-uncut` 1 (P9b) |
| `scripts/check_m9_opcodes.py` S1 probe (scratch copies) | — | new 9/9 and PASS; old 8/9 on the new fixtures; a `parameter` `OP_PROBE_NEW_C`: old PASS (silent), new FAIL naming it |

## Parent consumer gate table (scratch parent at milan-fpga dev `e4b771f9` + `parent-c4-disposition.patch`, gitlink `441d646`)

| Command | rc | Result |
|---|---:|---|
| `python3 scripts/check_cpp_idiom.py` | 0 | build without warnings: 0 <= 0 |
| `python3 scripts/check_py_idiom.py` | 0 | over-long line: 0 <= 0 |
| `python3 scripts/xvlog_gate.py --check` | 0 | PASS, 4 findings == ratchet (0 `hdl/`, 4 pinned processors) |
| `python3 scripts/check_rtl_source_lists.py` | 0 | 107 files in the closure, 4 of 4 lists; processor 36/42 tops, 6 recorded |
| `python3 scripts/pp_srcs.py --check --selftest` | 0 | 46 sources derived; self-test passed |
| `python3 sw/builder/test_builder.py` | 0 | all gates pass except gate 11, not run (hardware build tree absent); 1160 s, detached + awaited |
| `make -C tb/verilator/pp_shadow -j8` | 0 | PASS (646/606/311 checks shown last, 0 failures in each of the four builds) |
| `python3 scripts/check_port_contracts.py` | 0 | 3789 ports; processor 111 <= 111 undocumented |
| `python3 scripts/measure_naming.py --check` | 0 | 96 recorded |
| `python3 scripts/measure_test_evidence.py --check` | 0 | 72 <= 77 without a mutation arm, 10 <= 10 unseeded, 0 <= 0 unexplained DUT-source readers, 3 <= 3 wall-clock |
| `python3 scripts/docs_check.py` | 0 | 0 findings |
| `make -C tb/verilator/nvm_cosim lint` | 0 | both lint invocations clean |
| `make -C tb/verilator/nvm_cosim quick` | 0 | 315 checks |
| `make -C tb/verilator/milan_dp -j8` | 0 | every leg RESULT: PASS (9), nxndv 1,847 checks, 0 failures; 1578 s, detached + awaited |
| `make -C tb/verilator/milan_dp_render -j8` | 0 | RESULT: PASS |
| `python3 scripts/lint_rtl.py --check` | 0 | 90 <= ratchet 90 |

Control: the parent's `measure_test_evidence.py --check` without the patch (the e4b771f9 script
as a scratch copy, removed after) is rc 1, `protocol-processor/tb/pp_top/acmp_mutants.py:
UNEXPLAINED`, so the disposition line is load-bearing at this head. With it, the ratchet also
reports "the mutation ratchet can be lowered to 72" (round 2: 73 <= 77), from C4's new arms;
that is the parent's to lower.

## Working tree

`git status --porcelain` is empty at `441d646`. The suites' ignored build outputs (`obj_*`,
generated ROMs, `tb/desc_store/image.*`, `__pycache__`, `.venv-wavedrom`) were present at the
start and are git-ignored; a `scripts/__pycache__` this round's probe import created was
removed. Every scratch file of this round is under `$VALIDATION_STORAGE/c5b-a471`.

## What remains

- #76's requirement tickets #38, #51, #60 are their own issues; the model rules L1-L10 are the
  consumer's (07 section 3.1); #38, #39, #60, #89 unchanged.
- GET_AUDIO_MAP at most 71 records per page (Milan permits subsets of 176); the GET/SET family
  and the READ_DESCRIPTOR overlay address configuration 0 only; the AUDIO_UNIT and CLOCK_DOMAIN
  too-short guards stay ungraded (unreachable); maps and names persistence under GAP-09 (#70).
- Two pre-lane markdown rows split on a `||` inside a code span (`docs/guides/integrator.md:365`,
  `tb/pp_top/README.md:672`); outside this lane's lines, left for the manager.
- The parent's test-evidence ratchet can be lowered 77 -> 72 (C4's arms): the parent's edit.
- Manager duties: the hosted CI run (including the new AECP campaign step), the merge-turn
  candidate, the round-3 reviews. Nothing was pushed.
- No hardware; the parent builder's gate 11 not run (hardware build tree absent).
