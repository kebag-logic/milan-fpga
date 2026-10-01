# HANDOFF — [A465] round 2, lane C5b (AECP dispatch), PR #138

Status: DONE. Head `2acd4025782bff4aabbae73252476be34ea8b00d` (not pushed; no PR edited).

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Branch: c5b-aecp-dispatch, start 54c1e2b11c90e7063fc5882b15ddea5e4335d411
- Assignment: issue #76 comment 5921225908
- TAKEN: issue #76 comment 5921229302
- REVIEW READY: issue #76 comment 5924903130, head `2acd402`

## 1. Merge of main d5f73bac

Commit `a4ba9f7` (parents 54c1e2b1, d5f73bac), a merge commit. Main brought #135 (MAAP
coverage, lane C2) and #136 via its own merge: `hdl/maap/KL_pp_maap.sv`, `tb/maap` (a new
patch campaign, 26 patches), `tb/rx_validator`, `.gitattributes` (the `tb/maap/mutations`
entry), `.github/workflows/hdl.yml` (the MAAP campaign step), 00 REQ-MAAP-007, 11, and
pp_top's `maap-internal` mode (section MP, MP7).

Conflicts, all in tb/pp_top, all resolved keeping both sides:

| File | Ours (lane) | Theirs (main) | Resolution |
|---|---|---|---|
| `tb/pp_top/Makefile` `.PHONY` | `aecp-dispatch aecp-mutants` | `maap-internal` | all five targets |
| `tb/pp_top/sim_main.cpp` `main()` | `aecp_only` in `one_section` | `maap_only` in `one_section`, `if (maap_only) run_maap_internal(h);` | `one_section` ORs both; main's `run_maap_internal` line kept |
| `tb/pp_top/README.md` tail | section AX | section MP | both: MP first (its run order, inside the main run), then AX (after AD) |

Auto-merged: `docs/00_MILAN_COMPLIANCE_REVIEW.md` (the lane's rows and main's REQ-MAAP-007).

Moved patches: none. Every lane patch (`tb/pp_top/aecp_mutations/`) targets `hdl/aecp` or
`hdl/top`, which are byte-identical to 54c1e2b in the merge; every main patch
(`tb/maap/mutations/`) targets `hdl/maap` or `hdl/packet_engine/KL_pp_rx_validator.sv`,
byte-identical to d5f73bac. `git apply --check` passes for all 29 lane, 26 MAAP, srp_top
and adp_engine patches at the merge; their hunk offsets are the same as on each side
(pre-existing, e.g. the lane's `lk-*` at +195, main's MAAP patches at +11..+72).

Validation at the merge: `make -C tb/pp_top` rc 0, 8,315 checks (8,295 default + 20 fixture).

## 2. SET_CONTROL out-of-range BAD_ARGUMENTS body (R416-1 F1, R417-1 F2)

Commit `b0b30ea`. Clause: IEEE 1722.1-2021 7.4.25.1 ("the old value if it fails"); the
behaviour was already conformant at 54c1e2b1 (`gen_ucode.py` E_SCTRL out-of-range arm
branches to the shared `SCTRL_EMIT` tail); this item grades it. No RTL change.

- Tests (`tb/pp_top/sim_main.cpp:10819`, section AX, `sctrl_out_of_range_carries_255()` after LK3,
  where IDENTIFY holds 255 and the bench holds the lock):
  - **LK3b**: the holder, under its own lock, sends SET_CONTROL(128): BAD_ARGUMENTS at cdl 17
    carrying 255, byte-exact; no dynamic-store write, NVM mark or notification.
  - **LK3c**: lock released, a second controller sends SET_CONTROL(128): the same, plus no
    unsolicited frame at the registered holder (a notification would reach it, since
    notifications go to every registered controller but the requester); GET and the face
    still read 255.
  - The refusal checks share one helper `refused()`; `foreign()` (LK1/LK3/LK4) now calls it
    after taking the lock, with the same check labels.
- Mutant `sctrl-badarg-zero-body` (`tb/pp_top/aecp_mutations/sctrl-badarg-zero-body.patch`,
  `aecp_dispatch_mutations/` since item 5;
  the out-of-range `BRANCH SCTRL_EMIT` -> `BRANCH E_BADARG1`, the same change as the
  reviewer probe): KILLED, 2 failing checks (LK3b and LK3c byte-exact).
- Count changes in existing arms from the new checks: `lk-sctrl-lock-nop` 9 -> 12 (LK3b, LK3c
  and LK3c's GET/face carry the 0 that LK3 wrote), `lk-prefix-zero-body` 5 -> 7 (LK3b, LK3c:
  the base's out-of-range arm was the zero stub). README table and prose updated.
- AX: 189 -> 198 checks. Docs: 06 section 6.8 (LK3b/LK3c), 09 section 8.1 Identify row.
- Campaign at this state: 30 of 30 KILLED, control PASS (6 min 22 s).

## 3. Line-size contract (R416-1 F2, R417-1 F1)

Commit `f7fa70b`. R417-1 F1's first option, as assigned.

- RTL (`hdl/aecp/KL_aecp_engine.sv:903` `RESP_BUF_C`, `:907`, `:927-940` the guards; the
  buffer reaches the µCPU at `:1690` and the response buffer at `:2007`):
  - `RESP_BUF_C = 16 + LINE_BYTES_P` (was rounded up to 16). The response buffer, the
    Δ8 APPEND cap (`RESP_D8_CAP_BYTES_P`, unchanged wiring) and the buffer's drop fence are
    now exactly the documented `16 + DESC_LINE_BYTES_P` reservation. No change at the
    default 576 (592 either way).
  - Legal line: a multiple of 8 from `LINE_MIN_BYTES_C` = 24 + 8·71 − 16 = 576 to
    `LINE_MAX_BYTES_C` = 1024 − 16 = 1008 (`RESP_CURSOR_BYTES_C`, the 10-bit cursor). Three
    elaboration guards, each naming `DESC_LINE_BYTES_P`: `gen_g_line_step`,
    `gen_g_gamap_page_fit` (the floor, now `16 + LINE_BYTES_P < 24 + 8·GAMAP_PAGE_MAX_C`),
    `gen_g_line_ceiling`. The µCPU's own 524..1024 guard stays.
  - Clause: Milan v1.2 5.4.1 (the Δ8 permission), 5.4.2.26; the reservation contract of
    the integrator guide section 5 and 07 section 3.3.2.
  - Verilator reports an elaboration `$error` as `%Warning-USERERROR`, so a `-Wno-fatal`
    build carries past it (why R417-1's probe at 561 elaborated). The refusal is a lint
    (zero warnings) or synthesis failure; the in-tree check is therefore a lint.
- Tests:
  - `tb/pp_top/line_guards.py` (`make line-guards`, run by `make`): lints the real top with
    `lint_hdl.sh`'s flags at 576, 584, 1008 (clean) and 568, 1016, 580 (refused by the
    engine's message naming `DESC_LINE_BYTES_P`). Sources come from the Makefile; the script
    reads no DUT file (the parent's DUT-reader heuristic does not match it).
  - A third pp_top build, `obj_line` (`LINE_FIXTURE = 584`, `make aecp-line` alone), runs
    section AX at the non-default line: OV1/OV5 read a 584-byte whole-line descriptor
    (cdl 600, frame 626).
  - Section AX **RB** (`tb/pp_top/sim_main.cpp:11162`; the counters at `:845`), in both the
    default and the line build: the response-memory model now
    counts every strobed byte outside the reservation instead of dropping it unseen; RB
    requires none, the top's elaborated line (`dbg_desc_line_bytes_o`, a new wrap tap) equal
    to the bench's, and OV1's whole-line response to reach the reservation's last byte.
  - AX: 198 -> 201 checks per build. pp_top: 8,528 (8,307 + 20 + 201).
- Mutants (all KILLED): `line-floor-rounded` 1 (`line guard 568`), `line-ceiling-dropped` 1
  (`line guard 1016`: only the µCPU's message, which does not name the parameter),
  `line-buffer-fixed-592` 7 (OV1 at 584), `rb-rounded-buffer-no-page-cap` 10 (RB: 8 bytes
  past 600). The RB arm is two sites by necessity: at a legal line the page cap and the
  store's line bound keep every writer inside 16 + line, and the buffer drops past it.
  Scratch probes at the line build: the rounding alone, 201 checks 0 failures (equivalent);
  `pg-cap-dropped` alone, RB clean (72 records, 600 bytes) and 9 PG failures.
- Docs: F01.5 new row `P-DESC-LINE-BYTES` (576; a multiple of 8, 576..1008) and
  `P-MAP-SUBSET-CH-MAX` reworded; integrator guide `DESC_LINE_BYTES_P` row and section 5
  reservation row; 06 section 3 (ceiling, floor 576); 07 sections 3.3.1 (the range) and
  3.3.2 (the buffer is the reservation); top banner comments; tb/pp_top README (builds, AX
  OV/RB, line guards, mutation table and prose).
- Parent: `PP_DESC_LINE_BYTES_P` = 576 lints clean and is the floor.

## 4. .gitattributes whitespace exemption (R416-1 F3)

Commit `a91fe0e`: `tb/pp_top/aecp_mutations/*.patch whitespace=-blank-at-eol,-blank-at-eof`,
the form of the srp_top, maap and adp_engine entries (renamed with the directory in item 5).
`git diff --check 0451d83d HEAD` rc 2 (7 hits, all in these patches) -> rc 0; every patch
still passes `git apply --check`, context spaces untouched.

## 5. Mutation driver rename

Commit `9437b16`: `tb/pp_top/aecp_mutants.py` -> `tb/pp_top/aecp_dispatch_mutants.py`,
`tb/pp_top/aecp_mutations/` -> `tb/pp_top/aecp_dispatch_mutations/` (34 patches), make target
`aecp-mutants` -> `aecp-dispatch-mutants`, output variable `AECP_MUTANT_OUTPUT` ->
`AECP_DISPATCH_MUTANT_OUTPUT` (default `/tmp/aecp-dispatch-mutants`), scratch prefix
`aecp-dispatch-mutants-`. Updated: the driver, the Makefile (and its comments), the README
section, the sim_main comment, `.gitattributes`. No CI step existed for this driver, so
none changed. No reference to the old names remains in the tree. The names `aecp_mutants.py`
and `aecp-mutants` are free for lane C5a.

(The first commit attempt captured only the renames because `git add` refused the vanished
old directory; it was amended at once, before anything else, to include the content
edits. Nothing was pushed.)

Campaign after the rename, in two `--only` chunks (17 + 17 arms): 34 of 34 KILLED, controls
`aecp-dispatch`, `aecp-line`, `line-guards` PASS; counts equal the README table.

## 6. Suggestions

All four taken (one in part):

| Suggestion | Disposition | Commit |
|---|---|---|
| R416-1 S2 (`check_m9_opcodes.py` robustness and wording) | Taken. Every `OP_*_C` localparam is counted after comments are stripped (`RE_DECLARED`); one written in any other form fails as unparsed, and one opcode under two names fails. Selftest 6 -> 8 fixtures (two new failing ones); docstrings state "eight fixed fixtures, six of which must fail". A scratch copy with `OP_GET_NAME_C = 16'd17` fails naming it. | `44fda60` |
| R417-1 S1 (the selftest count in the docstrings) | Taken, same commit. | `44fda60` |
| R417-1 S2 (READ_DESCRIPTOR after the D3 restore) | Taken: pp_top AX **RD3** (`tb/pp_top/sim_main.cpp:11096`). RD1's rows reach the device (premise: `d3_unflushed_o` clear, port idle), a power cycle carries the NVM device, both restore walks write the rows back; with no SET since the reset the GETs read 48000, 1 and the 2ch format and each READ_DESCRIPTOR carries them (AUDIO_UNIT 0, CLOCK_DOMAIN 0, STREAM_INPUT 0, STREAM_OUTPUT 1; STREAM_OUTPUT 0 still its image). | `2acd402` |
| R416-1 S1 (the too-short guards) | Taken for the STREAM guard (`E_RDESCSF`, `hdl/aecp/ucode/gen_ucode.py:1200`, both stream types): pp_top AX **RD4** (`tb/pp_top/sim_main.cpp:11129`) shortens configuration 0's STREAM_OUTPUT index-map length to 80 (outside the header checksum), power-cycles, sets STREAM_OUTPUT 1's format, and requires READ_DESCRIPTOR to be the 80 image bytes whole. Arm `rd-str-short-guard-nop` KILLED (1: no response inside the bound; the TAIL count 80 - 88 wraps). Retained for the AUDIO_UNIT and CLOCK_DOMAIN guards: unreachable by any SET or restore, because SET_SAMPLING_RATE walks the AUDIO_UNIT's own list (from sampling_rates_offset, at or past 144) and SET_CLOCK_SOURCE checks the CLOCK_DOMAIN's own clock_sources_count (@74), which a descriptor short of its lane (144, 72) does not hold, and the restore rules judge the same fields; a stream format is judged by the integrator's face. The reviewer's three-guard probe fails only RD4 here, which bears that out. | `2acd402` |

Count changes from RD3 (campaign at `2acd402`): `rd-base-no-overlay` 5 -> 9, `rd-au-image-only`
1 -> 2, `rd-cd-image-only` 2 -> 3, `rd-str-unset-overlays` 3 -> 4, `rd-so-reads-input-row` 2 -> 4,
`rd-tail-uncut` 5 -> 9 (each + its RD3 reads). AX: 201 -> 218 checks per build.

## Parent-visible list (supersedes round 1's at the new head)

1. No port, register or parameter of `protocol_processor_top` is added or removed.
   `DESC_LINE_BYTES_P` has a stated and enforced legal range: a multiple of 8 from 576 to
   1008 (`P-DESC-LINE-BYTES`, F01.5); any other line is refused at elaboration with a
   message naming `DESC_LINE_BYTES_P` (lane base: every line elaborated; round 1's head:
   refused below 561 and above 1008, the latter only through `RESP_D8_CAP_BYTES_P`'s
   message). The parent's `PP_DESC_LINE_BYTES_P` = 576 is the floor. The refusal is a
   Verilator USERERROR warning: fatal to a zero-warning lint or synthesis, not to a
   `-Wno-fatal` simulation build.
2. The response buffer is exactly the `16 + DESC_LINE_BYTES_P` reservation at
   `RESP_BASE_P` (it was rounded up to 16); nothing is written past it. No change at 576.
3. NEW: SET_CONTROL's out-of-range BAD_ARGUMENTS now carries the value in force (before:
   zero), IEEE 1722.1-2021 7.4.25.1: SET_CONTROL(IDENTIFY, 128) while identifying gets 255.
4. The locked refusals of SET_SAMPLING_RATE, SET_CLOCK_SOURCE, SET_CONTROL carry the value
   in force (round 1).
5. GET_AUDIO_MAP pages of 63..71 records served whole (above cdl 524; slot 4 from 66);
   above 71 NO_RESOURCES with count 0; `P-MAP-SUBSET-CH-MAX` = 71 (round 1).
6. READ_DESCRIPTOR of configuration-0 AUDIO_UNIT, CLOCK_DOMAIN, STREAM_INPUT/OUTPUT carries
   the stored value a SET or the D3 restore wrote (both now graded: RD1, RD3); before
   either, or for a STREAM too short for the lane (RD4), the image unchanged.
7. Observation (no processor action): the nxndv shape's STREAM_INPUT 1 face/image
   `current_format` disagreement before a SET (round 1).
8. Mutation driver renamed to `protocol-processor/tb/pp_top/aecp_dispatch_mutants.py`
   (`aecp_dispatch_mutations/`, `aecp-dispatch-mutants`); new `tb/pp_top/line_guards.py`.
   Neither is a DUT-source reader: the parent's `measure_test_evidence.py --check` at
   e4b771f9 with this head counts 0 unexplained readers, so no `DUT_READER_DISPOSITIONS`
   entry is needed. The names `aecp_mutants.py` / `aecp-mutants` belong to lane C5a.
9. This head carries processor `main` `d5f73bac` (#135, #136); their own parent-visible
   items are that lane's.
10. Processor totals: `tb/pp_top` 8,562 over three builds (8,324 + 20 + 218), `tb/ucpu` 398,
    the 33 suites 1,017,973.
11. Parent matrix rows that can cite the grading at adoption
    (`docs/reference/MILAN_COMPLIANCE_MATRIX.md`): 5.4.2.4 (AX RD0..RD4, OV, RB), 5.4.2.13-.18
    (AX LK incl. LK3b/LK3c), 5.4.2.26 (AX PG), 9.3.5.3.3 (A5b, M9).

## Environment

- Verilator 5.052 (system), run through a scratch wrapper outside every tree
  (`$VALIDATION_STORAGE/c5b-a465/bin/verilator`) that rewrites the suites' `-j 0` to `-j 8`;
  nothing else changes. Yosys 0.66. Vivado 2026.1 `xvlog` (found by the parent gate itself).
  Heavy builds ran one at a time.
- Commands bounded by the 600 s foreground limit were chunked with the drivers' own
  `--only`. The two drivers without `--only` (`gsi_mutants.py`, `srp_admission/mutants.py`)
  and the two long parent commands (`test_builder.py`, `milan_dp`) were started in the
  background and awaited in the foreground (`tail --pid`) before anything else heavy ran;
  nothing was left running.
- Scratch parent `$VALIDATION_STORAGE/c5b-a465/parent-e4b771f9`: a `git archive` export of the
  trusted milan-fpga dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b` (regular-file index
  identical to the trusted checkout's, 976 entries), committed locally; `gptp-processor`
  at `5dce647a` and `third_party/verilog-axis` at `48ff7a7e` cloned at their recorded pins
  (from round 1's scratch copies, commit hashes verified); `protocol-processor` a scratch
  clone of this lane checked out at `2acd402`, gitlink staged and committed at it; `external`
  recorded and uninitialized, as in the trusted checkout. `git submodule status` shows the
  three project/third-party submodules at their gitlinks. No adaptation patch: e4b771f9
  carries the #132 + C1 adaptation. The trusted checkout was only read. (A symlink to the
  lane tree was tried first; git refuses a symlinked submodule path, so the parent's
  pinned-submodule assertion cannot see it.)
- Receipts in `receipts/` here (all small): `suites-2acd402.txt`,
  `aecp-dispatch-mutants-2acd402.txt` and `.json`, `d3-mutants-2acd402.txt`,
  `other-mutants-2acd402.txt`, `parent-gates-2acd402.txt`. Full logs stay in
  `$VALIDATION_STORAGE/c5b-a465/logs` and the campaign output directories beside it.

## Gates

### Processor suites (head `2acd402`)

| Command | rc | Result |
|---|---:|---|
| `run_suites.sh` pre-gates: `check_upc_map.py`, `check_m9_opcodes.py --selftest`, plain | 0 | 58 engine constants and 86 entry points agree; selftest 8 of 8; 30 opcodes swept |
| `make` in each of the 33 `tb/*/` suites, in the lane tree | 0 each | 1,017,973 checks, 0 failing |
| the same 33, on a clean `git archive` export of `2acd402` | 0 each | 1,017,973 checks, 0 failing (pp_top 8,562 = 8,324 + 20 + 218; srp_admission 991,231; ucpu 398; rx_validator 497; maap 196) |
| `./scripts/lint_hdl.sh` | 0 | 41 modules LINT OK |
| `make check` | 0 | 41 mermaid + 18 WaveDrom, links 994, matrix 115 REQ / 17 GAP, modmatrix 94 rows 0 untested, parameters 26/26/26 |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `./syn/yosys/run.sh` (on the export) | 0 | 36 tops YOSYS OK, `KL_aecp_engine` Xilinx map OK |
| `make -C tb/pp_top fixture-guards`, `line-guards` (inside `make`) | 0 | 4 cases PASS; 6 cases, 0 failing |
| `tb/desc_store/test_gen_desc_image.py` | 0 | OK |
| `git diff --check 0451d83d HEAD` | 0 | (rc 2 at 54c1e2b1) |

`run_suites.sh` as one invocation needs more than the 600 s bound (pp_top alone is about
5 min, srp_top about 3); its two pre-gates and the same `make` in each suite ran as
separate commands, twice (lane tree and clean export).

### Mutation campaigns (head `2acd402`)

| Driver | rc | Result |
|---|---:|---|
| `make -C tb/pp_top aecp-dispatch-mutants` (one invocation) | 0 | 35 of 35 KILLED by their named checks; controls `aecp-dispatch`, `aecp-line`, `line-guards` PASS |
| `tb/pp_top/d3_mutants.py --jobs 1 --only <chunk>` x14 | 0 each | 83 of 83 KILLED; goldens PASS in every chunk |
| `tb/pp_top/gsi_mutants.py` | 0 | 20 detected; golden and restored PASS |
| `tb/pp_top/name_wr_mutant.py` | 0 | decode killed; golden and restored PASS |
| `tb/maap/mutants.py --only` x2 (main's new campaign) | 0 each | 29 of 29 arm rows KILLED (27 labels; two also on rx_validator and pp_top `maap-internal`); controls PASS |
| `tb/srp_top/mutants.py --only` x8 | 0 each | 78 of 78 arm rows KILLED; controls PASS |
| `tb/adp_engine/mutants.py --only` x3 | 0 each | 30 of 30 KILLED; controls PASS |
| `tb/srp_admission/mutants.py` | 0 | 12 of 12 PASS (controls and 3 arms x 3 suites) |
| `tb/acmp_talker/retry_mutants.py --only` x2 | 0 each | 62 killed, 7 equivalence controls, 1 performance control; baseline and restored rc 0 |
| `tb/desc_mem_guard/mutate.py` | 0 | hold-deleted mutant detected |
| `make -C tb/nvm_port figures` | 0 | figures agree |
| tb/ucpu by hand in scratch | — | golden 398/0; D8 flag ignored 2 (P11b); batch exception dropped 2 (P11c); TAIL uncut 1 (P9b) |

### Parent consumer set (scratch parent at milan-fpga dev `e4b771f9`, gitlink `2acd402`)

| Command | rc | Result |
|---|---:|---|
| `python3 scripts/check_cpp_idiom.py` | 0 | build without warnings: 0 <= 0 |
| `python3 scripts/check_py_idiom.py` | 0 | over-long line: 0 <= 0 |
| `python3 scripts/xvlog_gate.py --check` | 0 | PASS, 4 findings == ratchet (0 hdl/, 4 pinned processors) |
| `python3 scripts/check_rtl_source_lists.py` | 0 | 107 files in the closure, 4 of 4 lists |
| `python3 scripts/pp_srcs.py --check --selftest` | 0 | |
| `python3 sw/builder/test_builder.py` | 0 | all gates pass except gate 11, not run (hardware build tree absent); 1076 s, background + awaited |
| `make -C tb/verilator/pp_shadow -j8` | 0 | PASS (606/606/646/311 checks, 0 failures) |
| `python3 scripts/check_port_contracts.py` | 0 | |
| `python3 scripts/measure_naming.py --check` | 0 | 96 recorded |
| `python3 scripts/measure_test_evidence.py --check` | 0 | 73 <= 77 unarmed, 10 <= 10 unseeded, 0 <= 0 unexplained DUT-source readers, 3 <= 3 wall-clock |
| `python3 scripts/docs_check.py` | 0 | 0 findings |
| `make -C tb/verilator/nvm_cosim lint` | 0 | |
| `make -C tb/verilator/nvm_cosim quick` | 0 | 315 checks |
| `make -C tb/verilator/milan_dp -j8` | 0 | every leg RESULT: PASS (nxndv 1,847 checks, 0 failures); 1506 s, background + awaited |
| `make -C tb/verilator/milan_dp_render -j8` | 0 | RESULT: PASS |
| `python3 scripts/lint_rtl.py --check` | 0 | 90 <= ratchet 90 |

## Working tree

`git status --porcelain` is empty at the head. The ignored build outputs of the suites
(`obj_*`, generated ROMs, `tb/desc_store/image.*`, `__pycache__`, `.venv-wavedrom`) were
already present at the start (round 1's) and are git-ignored; every scratch file of this
round is under `$VALIDATION_STORAGE/c5b-a465`.

## What remains

- #76's requirement tickets #38, #51, #60 are their own issues.
- The model rules L1-L10 are the consumer's (07 section 3.1); #38, #39, #60, #89 unchanged.
- GET_AUDIO_MAP carries at most 71 records per page (Milan permits subsets of 176): the
  page cap is fixed at the smallest legal line's reservation.
- The GET/SET family and the READ_DESCRIPTOR overlay address configuration 0 only.
- The AUDIO_UNIT and CLOCK_DOMAIN too-short guards stay ungraded (unreachable, item 6).
- Persisting and restoring maps and names stays under GAP-09 (#70).
- No hardware; the parent builder's gate 11 not run (hardware build tree absent).
- Manager duties: hosted CI, the merge-turn candidate, the reviews of round 2.
