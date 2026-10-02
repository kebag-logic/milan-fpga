# [A489] Lane C6 round 4 (merge only) handoff: notifications and Identify

Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, branch `c6-notifications`
(PR #139). Round-4 start `9624ef4c452d708de68a901d5e645bdfa1f5d6f5` (origin URL and HEAD
confirmed). Assignment: #80 comment 5939839032 (merge only). Reviews at the start head:
R420-3 (#139 comment 5939598551) and R421-3 (#139 comment 5939832953), both POSITIVE.
Roles: executor [A489], manager [A10], reviewers [R420] (internal), [R421] (external).

## Status

Head `651839e1ce9d3a36adfbfae0297dd091a02a2def` (tree `8599a8b0a1649becc2bb5303b3762c3f8c9622f5`),
one merge commit on `9624ef4`, no rebase, no other commit; the lane tree is clean. TAKEN posted
on #80 (comment 5939857154). REVIEW READY: see the last line of this file.

| Item | State |
|---|---|
| 1. Merge main `16ea10ac` (`--no-ff`), keeping both sides; regenerate ROMs and tables | committed `651839e1` (parents `9624ef4c`, `16ea10ac`) |
| 2. Re-measure at the merge commit: every suite, every campaign, both reviewers' round-3 probes | done, all rc 0 (below) |
| 3. Parent consumer gates at milan-fpga dev `7f0927bb` with the combined C4 + C6 patch | done, 16 of 16 rc 0 (below) |

No STOP condition was met: no port, parameter or parent-visible change (list below).

## Merge resolution

`git fetch origin main` gave `16ea10ace6c755c91bb9e864b2b855acb240b09b` (PR #138, lane C5b,
AECP dispatch; merge base with the lane `3f3ea56b`). `git merge --no-ff --no-commit`, resolved,
then merge commit `651839e1`. `git merge-tree --write-tree 16ea10ac 651839e1` gives
`8599a8b0`, the head's own tree: the merge tree equals the head.

Main touched 60 files; 14 are shared with the lane. Ten merged with no textual conflict
(`docs/00_MILAN_COMPLIANCE_REVIEW.md`, `docs/architecture/01_overview.md`, `03_packet_engine.md`,
`06_aecp_engine.md`, `09_verification.md`, `docs/guides/integrator.md`,
`hdl/aecp/KL_aecp_engine.sv`, `hdl/aecp/ucode/gen_ucode.py`, `hdl/top/protocol_processor_top.sv`,
`tb/ucpu/sim_main.cpp`: separate hunks). Four conflicted, each resolved by keeping both sides:

| File | Conflict | Resolution |
|---|---|---|
| `tb/pp_top/Makefile` | both sides took the bench from two builds to three: the lane's identify build (`obj_idn`, `identify-build`, `identify`), main's line build (`LINE_FIXTURE` 584, `LINE_VFLAGS`, `obj_line`, `line-build`, `aecp-line`, `aecp-dispatch`, `aecp-dispatch-mutants`, `line-guards` in `run`) | four builds in `run`: default, fixture, identify (third), line (fourth); the awk tally requires 4; `clean` removes all four model dirs; `.PHONY` the union; the header says four |
| `tb/pp_top/sim_main.cpp` `main()` | build selection (`PP_TOP_EN_IDENT` / `PP_TOP_DESC_LINE_BYTES`), flags (`ident_only`, `notify_only` / `aecp_only`), `one_section`, the section calls, the build-line printf | both `#elif` arms; the union of the flags; main's `run_aecp_response` after AD, then the lane's ID0, NP, ST, RN (main's order first, then the lane's, as in round 2); main's printf shape (with `DESC_LINE_BYTES_P`); "four builds" in the tally comment and in the file header (`:20-25`) |
| `tb/pp_top/sim_main.cpp`, end of the sections | main's section AX code / the lane's `#include "notify_phases.hpp"` | AX first, then the include |
| `tb/pp_top/pp_top_wrap.sv` | banner, port list, parameter overrides, `dbg_*` assigns | both: the lane's three `dbg_ident_gap_*` taps and main's seven AX taps; both `ifdef` overrides; the banner names the three re-built parameters and the third and fourth builds |
| `tb/pp_top/README.md` | the `make` paragraph; both sides appended a section at the end | four builds (DV, ID, AX); main's section AX first, then "Lane C6", both whole |

`.gitattributes` and `.github/workflows/hdl.yml` came from main alone, so every main entry and
CI step (the `aecp-dispatch-mutants` campaign) is kept.

Three further edits keep both sides working (all in the merge commit):

1. **A ROM collision the textual merge did not show.** The lane placed `E_IDNOTIF` (IEEE
   1722.1-2021 §7.4.39.1, Figure 7-61; 6 words) at ROM word 2000 and `E_SINFOUNS` (§7.4.15.1,
   Figure 7-40; 21 words) at 2016. Main placed `E_RDESCAU` at 2000 and `E_RDESCCD` at 2024
   (READ_DESCRIPTOR's current-value overlays, §7.2.3/§7.2.32, #82). `gen_ucode.py`'s `place()`
   refused the merged file: `AssertionError: overlap at 2000`. Main's layout is kept; the lane's
   two bodies move together into main's free 456..511 run after `E_COPYT`, each on a 16-word
   boundary: `E_IDNOTIF` 464, `E_SINFOUNS` 480.
   - `hdl/aecp/ucode/gen_ucode.py:230-235` (comment and entry points; the `place()` calls at
     `:1028` and `:2292` are unchanged);
   - `hdl/aecp/KL_aecp_engine.sv:895,897` (`UPC_IDNOTIF_C`, `UPC_SINFOUNS_C`);
   - `tb/ucpu/sim_main.cpp:52-53` (the bench's mirror).
   Neither body branches, so it is position-independent. The regenerated ROM equals main's word
   for word except the 27 relocated words (464..500), and those equal the lane's bodies word for
   word (`receipts/ucode-merge-compare.txt`). `check_upc_map.py`: PASS (60 engine constants, 88
   entry points); `check_m9_opcodes.py`: PASS (30 opcodes). Graded at the new addresses by
   `tb/ucpu` N6/N7, `tb/pp_top` ID1 (IDENTIFY_NOTIFICATION byte-exact) and NP3 (the unsolicited
   SET_STREAM_INFO byte-exact), and by the controls `stream_info_get_body` (NP3) and the 21 ident
   controls, all KILLED.
2. **`tb/pp_top/notify_mutants.py:262` tally pattern.** Main's build line now carries
   `DESC_LINE_BYTES_P`; the driver's `TALLY` takes the new shape. Without it every pp_top run
   would read as incomplete and no mutant could be KILLED.
3. **`notify_mutants.py:236-239` `set_control_ignores_lock` re-anchored.** Main's #53 rewrote
   E_SCTRL (every refusal carries the value in force, IEEE 1722.1-2021 §7.4.25.1); the
   found-control lock check is now `CHECK_LOCK ra=15, imm=SCTRL_EMIT` (main's own
   `lk-sctrl-lock-nop.patch` plants the same NOP). The control NOPs that word in place, as
   before; RN kills it (1 failing check, as recorded).

Ordinals: main's text named the line build "the third"; it now says "the fourth"
(`tb/pp_top/README.md` section DV's build table, which gains the identify row, and the AX
paragraph; the wrap's override comment). The lane's "third build" for section ID stands
everywhere (docs 00, 06, 09, the README, `notify_phases.hpp`, `notify_mutants.py`).

Re-anchoring on the merged tree (scratch export, no build): `notify_mutants.py` 40 mutants / 43
anchors, `d3_mutants.py` 83 / 92, `acmp_mutants.py` 19 / 19, each exactly once; `gsi_mutants.py`
20 at their stated counts; `git apply --check` clean for every patch:
`tb/pp_top/aecp_dispatch_mutations` 35, `tb/adp_engine/mutations` 28, `tb/maap/mutations` 27,
`tb/srp_top/mutations` 73. Main's patches apply with line offsets (git apply's default), unedited.

Generated ROMs and tables regenerated from their generators: `ucode.hex` (`gen_ucode.py`, 2048
words, 88 programs; sha256 `23d2213d…` at the merge), `ltn_rom.hex` and the descriptor image
(every suite's Makefile), the module matrix (`gen_matrix.py --check`: 94 rows, 0 untested), the
WaveDrom SVGs (`render-wavedrom.py --check`: 18 blocks). No tracked file changed.

## Round-4 items

Merge only: no new test, no new mutant and no RTL behaviour change. The only RTL edits are
the two entry-point constants above (item 1 of the merge resolution, clause §7.4.39.1 and
§7.4.15.1 for the bodies, §7.2.3/§7.2.32 for main's overlays that keep their words). Failing
arms and mutants: every campaign was re-run at the merge (below); every lane and main control
is KILLED with the same failing-check count as recorded.

## Parent-visible list, round 4

Read against the parent at milan-fpga dev `7f0927bb`. Round 4 adds no top port, no top parameter,
no register and no module port (`git diff 9624ef4c 651839e1 -- hdl/top` changes comments only,
main's; no `input`/`output`/`parameter` line). Nothing changes at the parent's setting
(`EN_IDENTIFY_NOTIF_P` = 0). `parent-adoption-c4c6-ea3fb388.patch` is unchanged (sha256
`67bcd69852e5d090abc635e8dd66e5159667847ebf83d85aba9599d7cff7bd7c`).

| # | Change | Parent effect | Parent disposition |
|---|---|---|---|
| 1 | `E_IDNOTIF` 2000 to 464, `E_SINFOUNS` 2016 to 480 (generator, engine localparams) | internal constants; the parent builds `ucode.hex` from the generator as before; at 0 `E_IDNOTIF` is never dispatched, and the SET_STREAM_INFO push is byte-identical (NP3) | none |
| 2 | `tb/pp_top` builds four times; `notify_mutants.py` reads the new build line and re-anchors one control | test code in the processor's suite; the combined patch's disposition covers the driver as a whole | none |
| 3 | main's C5b changes arrive with the merge (`DESC_LINE_BYTES_P` range refused at elaboration, response buffer exactly 16 + line, `aecp_dispatch_mutants.py`, `line_guards.py`, `check_m9_opcodes.py`) | #138's, not this lane's; the 16 consumer gates pass with them and the unchanged patch; measure_test_evidence finds 0 unexplained DUT-source readers | none needed by this lane |

## Gates

Verilator 5.050 (the CI pin, `$VALIDATION_TOOLS/verilator-v5.050`) behind a scratch shim
capping `-j 0` at 8; one heavy command of mine at a time (the host was shared with another
lane's campaign). Yosys 0.66, sv2v 0.0.13. Every processor command ran on a `git archive
651839e1` export under `$VALIDATION_STORAGE/c6r4/head`, except `make -C tb/nvm_port figures`, which
reads pinned git revisions (`git show <rev>:tb/nvm_port/sim_main.cpp`) and ran in a scratch
shared clone at `651839e1` (clean after). The lane tree's `git status` stayed empty. Receipts:
`receipts/` (the home-directory prefix written `~`). Commands past the 10-minute foreground
limit (run_suites, the GSI, SRP-admission and SRP campaigns, five d3 chunks, the builder tests,
`milan_dp`) were moved to the background by the harness and waited on in the foreground; each
finished rc 0, and nothing of mine ran beside them.

### Processor, at the merge `651839e1` (all rc 0)

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | UPC map PASS (60 constants, 88 entry points); M9 selftest 9/9 and PASS (30 opcodes); 33 suites, 1,018,785 checks, 0 failing (round 3: 1,018,160). `pp_top` 8,855 (default 8,439, fixture 20, identify 178, line 218), `ucpu` 408, `aecp_notify` 14, `originator` 107; 12 min 43 s. `receipts/run_suites-651839e.log` |
| `./scripts/lint_hdl.sh` | 0 | 41 modules LINT OK; `KL_aecp_notify`, `KL_aecp_engine`, `protocol_processor_top` 0 findings at `-GEN_IDENTIFY_NOTIF_P=1` (`receipts/lint_hdl-651839e.log`, `lint-en1-651839e.log`) |
| `make lint wavedrom-check links matrix modmatrix params` (export); `make stale` (lane tree, read-only) | 0, 0 | 41 mermaid + 18 wavedrom, links 1,012, 115 REQ / 17 GAP, 94 rows 0 untested, parameters 27 = 27 = 27; stale clean |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `./syn/yosys/run.sh` | 0 | 36 tops YOSYS OK and the Xilinx memory-map check; 85 s (`receipts/yosys-651839e.log`) |
| `git diff --check` `9624ef4c..`, `16ea10ac..`, `3f3ea56b..651839e1` | 0, 0, 0 | |

**No arm lost** (`receipts/pp_top-sections-main-lane-merge.txt`; `tb/pp_top` run at main
`16ea10ac`, at the lane head `9624ef4c` and at the merge): every section line of main's and of
the lane head's is in the merge's, unchanged, and the merge has none of its own.

| Build | main | lane head | merge |
|---|---:|---:|---:|
| default | 8,367 | 8,044 | 8,439 = 8,367 + ID0 3 + NP 47 + ST 18 + RN 4 |
| fixture | 20 | 20 | 20 |
| identify (ID) | - | 178 | 178 |
| line (AX) | 218 | - | 218 |
| total | 8,605 | 8,242 | 8,855 |

`tb/ucpu`: base `3f3ea56b` 386, main 398 (+12), lane 396 (+10), merge 408.

### Mutation campaigns at `651839e1` (all rc 0)

| Campaign | Result |
|---|---|
| `notify_mutants.py --jobs 1` (four `--only` chunks: 10, 11, 8, 11) | five goldens PASS; **40 of 40 KILLED**; every failing-check count equals the README record mutant by mutant (`receipts/notify-mutants-651839e.json`, `.stdout`); 4 + 5 + 2.5 + 3 min |
| `aecp_dispatch_mutants.py` (three `--only` chunks: 12, 12, 11) | positive controls `aecp-dispatch`, `aecp-line`, `line-guards` PASS; **35 of 35 KILLED**; every count equals main's README record (`receipts/aecp-dispatch-mutants-651839e.stdout`); 3 + 3.5 + 2.5 min |
| `acmp_mutants.py --jobs 1` | goldens `acmp_listener`, `pp_top`, `rx_validator` PASS; 19 of 19 KILLED; the pp_top counts equal the record; 5.5 min |
| `d3_mutants.py --jobs 1` (six `--only` chunks: 12, 15, 15, 15, 15, 11) | **83 of 83 KILLED**; goldens PASS in every chunk; the 59 recorded pp_top counts unchanged (`receipts/d3-mutants-651839e-chunk{1-6}.stdout`); 1 + 18 + 18 + 19 + 19 + 14 min |
| `make -C tb/adp_engine mutants` | 2 controls PASS; 30 of 30 KILLED; 32 checks, 0 FAIL; 6.5 min |
| `make -C tb/maap mutants` | 3 controls PASS (maap 196, pp_top maap-internal 34, rx_validator 555); 29 of 29 KILLED; 32 checks, 0 FAIL; 4.5 min |
| `make -C tb/srp_top mutants` | 11 controls PASS; 78 of 78 KILLED; assertion coverage 65/65; 90 checks, 0 FAIL; 31 min |
| `gsi_mutants.py` | 20 of 20 detected by named checks; golden and restored PASS; 14 min |
| `tb/acmp_talker/retry_mutants.py` | 62 KILLED; 7 equivalence and 1 performance controls retained; baseline and restored rc 0; 6.5 min |
| `tb/srp_admission/mutants.py` | 3 controls PASS; 3 defects x 3 suites PASS (12/12); 12.5 min |
| `tb/pp_top/name_wr_mutant.py` | decode defect killed; golden and restored PASS |
| `make -C tb/nvm_port figures` (scratch clone) | every measured figure agrees with the tree; 2 waivers printed with their reasons; 4 min |

### Both reviewers' round-3 probes, re-run unchanged at `651839e1`

Read-only scripts from the review packets, run on copies of the merge export; outputs in
scratch, receipts in `receipts/reviewer-probes/`. Each result equals the reviewer's own receipt
at `9624ef4` once the build line's new `, DESC_LINE_BYTES_P 576` field is removed.

- R420-3 `run_probes.sh` (RP3a-RP3j): 600 checks, 0 failures; log identical.
- R420-3 `boundary_control.sh` (S1): section ID 178/0 under the control; the probes fail RP3j
  w=1 k=-2 only (597 checks, 1 failure); log identical.
- R420-3 `r420_2_probes_unchanged.py`: the six records equal the reviewer's JSON (RP1 15,301;
  RP2 3 frames; RS1/RS2 smallest gap 15,232; `hold_ignores_gap` KILLED by ID3f, ID7r, ID8q, ID8r;
  `burst_deadline_one_tick_short` passes ID; `wait_ignores_gap` x2 REFUSED, anchor gone).
- R421-3 `r421_arms.py`: 188 checks, 0 failures; log identical.
- R421-3 random-press probe (`r421_3_random.py`, `run_random.sh`, 16 campaigns x 200 steps):
  all rc 0; all 16 logs identical (smallest gap 15,230; no press lost). A first attempt ran the
  binary from the lane tree's root, where it found no ROM images and could not write its tally
  (all 16 rc 1, nothing written to the lane tree); re-run from the bench directory, as the
  script's own wrapper does after its build.
- R421-3 `r421_3_probes.py` (latch mutants; `--jobs 2`, `VJOBS=4` for the memory cap, where
  the reviewer used 8 x 1): the same 9 records as the reviewer's, as a set
  (`p_wait_latch_always` SURVIVES, equivalent; `c_press_not_latched` KILLED by section ID only).
- R421-3 `r421_3_ft_sweep.sh`: nine phases, both lower bounds hold; output identical.

### Parent consumer set at milan-fpga dev `7f0927bb`

Scratch copy `$VALIDATION_STORAGE/c6r4-parent/src`; the trusted checkout was not touched (HEAD
`7f0927bb`, status empty before and after). Commits:
1. `c5137b7`: `git archive 7f0927bb` of the trusted checkout; `external` (`efeb541`),
   `gptp-processor` (`5dce647`) and `third_party/verilog-axis` (`48ff7a7`) cloned at their
   recorded pins from round 3's scratch clones of the `.gitmodules` URLs (origin URLs reset to
   those URLs); `protocol-processor` a shared clone of this lane at `651839e1`. `git submodule
   init` registers them, with no fetch. Its 983-entry index equals the trusted tree's except the
   processor gitlink (`b2db3a97` there, `651839e1` here).
2. `5f40606`: `git apply parent-adoption-c4c6-ea3fb388.patch` (unchanged, from this directory;
   `git apply --check` clean). The scratch tree was clean after every gate.

| # | Command | rc | Result |
|---:|---|---:|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0 | multi-declarator 0 <= 0, long function 0 <= 0, build without warnings 0 <= 0 |
| 2 | `python3 scripts/check_py_idiom.py` | 0 | too many parameters 7 <= 7, global statement 0 <= 0, over-long line 0 <= 0 |
| 3 | `python3 scripts/check_rtl_source_lists.py` | 0 | OK: 107 files, 4 of 4 consumer lists; protocol-processor 36/42 tops, 6 recorded |
| 4 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | OK |
| 5 | `python3 scripts/check_port_contracts.py` | 0 | 3,793 first-party ports (protocol-processor 1,752, as at round 3); undocumented protocol-processor 111 <= 111 |
| 6 | `python3 scripts/measure_naming.py --check` | 0 | PASS: 96 candidates, all recorded |
| 7 | `python3 scripts/measure_test_evidence.py --check` | 0 | PASS: 72 <= 77 without a mutation arm (73 at round 3; C5b's campaign), 10 <= 10, 0 <= 0 unexplained DUT-source readers, 3 <= 3 |
| 8 | `python3 scripts/docs_check.py` | 0 | 0 findings across 184 md + 955 scrubbed files; scrub self-test 23/23; routing 4/4 |
| 9 | `python3 scripts/xvlog_gate.py --check` | 0 | PASS: 4 findings == ratchet (hdl/ 0, pinned processors 4); 2.5 min |
| 10 | `python3 sw/builder/test_builder.py` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11: the calibration report needs a local mf48 build tree, as in rounds 1-3); 17 min |
| 11 | `python3 scripts/lint_rtl.py --check` | 0 | PASS: 90 <= 90 (17 waived, 0 justified lint_off) |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 | 311 checks, 0 failures; RESULT: PASS; 3.5 min |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | both lint passes |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 checks, 315 PASS |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0 | 9 RESULT: PASS, 0 FAIL (182 + 182; milan_datapath 235, 235, 232; media_aclk 191); the 6 + 6 mutant arms pass; 27 min |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | tdm8_render 65 and 152 checks, 0 failures; 5 of 5 leg-defect arms caught; 5.5 min |

Logs over 200 KB, not copied:

| Log | Bytes | sha256 |
|---|---:|---|
| parent `pp_shadow` (gate 12) | 308,347 | `e565f33aa878d0e29ee0117a4ca9838824f69c472dca37449c1f26b9e1619476` |
| parent `milan_dp` (gate 15) | 2,001,578 | `450878771c9da4b6c83aecbb4fc238fd3165d240c2779a24da310c190c4041a7` |

Receipts for gates 1-11, 13, 14 and 16: `receipts/parent-gates/`.

## PR-BODY.md

`PR-BODY.md` in this directory keeps the `[A463]` first line and the four `Closes` lines and gains
a "Round 4" section (the merge with clause references, the parent-visible list, validation, what
remains). It is 64,841 characters, 695 under GitHub's 65,536-character body limit: any further
round should move older rounds' detail out rather than append.

## What remains

- Hosted CI on the PR, and the delta review of the merge.
- **Processor `main` moved again after the assignment:** `03c842a7` (#140, lane C5a, AECP
  deadlines; 18 commits past `16ea10ac`; merged 2026-10-01T23:21Z). This round merges
  `16ea10ac` only, as assigned, and no other merge was made. Against `16ea10ac` the merge tree
  equals the head; against `03c842a7` a further merge-only round is the manager's call.
- The parent adopts `parent-adoption-c4c6-ea3fb388.patch` (unchanged) when it moves its
  processor pin past this head.
- Retained, unchanged: R420-1 S1 and R420-1 S4 (`tb/pp_top/README.md`). Round 3's SUGGESTIONs
  R420-3 S1 (a 1-clock press on the expiry edge) and R421-3 S1 (FT4 at phase 99,999) are not
  taken in this merge-only round; both reviewers' probes still show the behaviour they cover.
- The lane tree carries ignored build products from earlier rounds (`tb/*/obj_dir`, the latest
  2026-10-01 07:58); untouched, untracked and not part of any commit.
- No hardware was used. Simulation only; the parent keeps the parameter at 0.

REVIEW READY posted once on #80 (comment 5944142914) at `651839e1ce9d3a36adfbfae0297dd091a02a2def`,
after this file and PR-BODY.md were final. Nothing pushed (the branch on origin is still `9624ef4c`).
