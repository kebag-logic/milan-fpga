[R334] POSITIVE - exact head 83c84b19e09d397ed2eb6f5ace337686ce0ef86b

Internal independent review, round R334-2 (delta), of processor PR #121 for issue #120
(`Mister-M-alt/protocol-processor-control-plane-avb-milan`). Exact head
`83c84b19e09d397ed2eb6f5ace337686ce0ef86b`, tree `7e6d16f3b5dfd3c4f1a0bc9ddb872f1156a1aea9`.
This round is one commit on `a9b7874d415d935949becd7ccfd58799927efb08`. Source base
`0922e43408f891fc0b84a84691df86b4fd0f1c0d`.

## Verdict in one paragraph

Round 3 changes exactly two test-harness files and nothing else: `hdl/`, `docs/`, `syn/`,
`scripts/`, `.github/` and every other `tb/` suite are byte-identical to `a9b7874d`. In
`tb/pp_top/pp_top_wrap.sv`, the two added harness ports and their `//!` contracts now sit
**before** the existing effect bundle. That bundle again covers `dbg_dyn_writes_o`,
`aecp_nvm_stb_o`, `aecp_nvm_mark_o` and `dbg_notify_enq_o` contiguously. The parent's
accepted port parser reports **162** undocumented ports for the file, as at base (round 2
reported 165). **My round-1 finding R334-F1 is closed.** In `tb/pp_top/sim_main.cpp`,
`run_name_writes` carries `[[maybe_unused]]`. The fixture build's only C++ warning
(`-Wunused-function`) is gone, and the default build still calls the function. Fresh
builds show 0 C++ compiler warnings in both builds at head. The simulator lint set is
identical at base, round 2 and head. The simulation transcripts at round 2 and head are
byte-identical: 7731 + 20 = 7751/0, NW 85/0, and the same latency lines. The port set is
unchanged; only the declaration order changed. I found no open MINOR, MAJOR or BLOCKER
finding. One new SUGGESTION is recorded below.

## 1. Reconstructed scope and authorities (delta)

- `AGENTS.md` / `CONTRIBUTING.md`: not present in this repository at head. The conventions
  live in `README.md`, `docs/README.md` and `hdl/README.md`, and all three are unchanged
  since my full round-1 pass at `a9b7874d`.
- Issue #120 (frozen acceptance, unchanged): one output `aecp_name_wr_o`, pulsing on the
  store's accepted live name-lane write, with no other behaviour change. The manager
  correction (5845334300) sets the parent consumer bar with an explicit open
  `.aecp_name_wr_o()` in the parent.
- Round-3 assignment (5846001897, executor [A336]) has two items:
  1. R334-F1: the parent parser must report 162 undocumented for `pp_top_wrap.sv`, with
     the bundle contiguous again.
  2. R335-F1: both `pp_top` builds must be warning-free, with the scenario still running
     in the default build.

  The round-1 suggestions were routed to the processor residue. Donor gates and the 12
  parent consumer commands are to be rerun with the parent patch.
- Author readiness (5846167338) and PR body "Round 3" section: both claims are
  checked below.
- Parent authorities, fetched read-only at parent dev `7eb3b0d4`:
  - `scripts/check_port_contracts.py` (`scan_ports`) and `scripts/sv_ports.py` (the
    bundle rule and its four boundaries);
  - `check_cpp_idiom.py`, `check_py_idiom.py` and `measure_test_evidence.py`, with the
    helper modules they import;
  - `hdl/milan/KL_pp_shadow.sv`.

  Every blob id matches the parent tree listing (`receipts/00-fetch-parent.log`).
- History: `a9b7874d..83c84b19` is one commit, `83c84b1`, which touches
  `tb/pp_top/pp_top_wrap.sv` (+9/−9) and `tb/pp_top/sim_main.cpp` (+1/−1)
  (`receipts/02-delta.log`, `receipts/02-delta.diff`).
- Public evidence: `kebag-logic/milan-fpga@356583ef…/review-evidence/pp120-r1`. The author
  folders `author`, `author-r2` and `author-r3` hold 176 entries with 0 hash mismatches.
  The published `author-r3/round3.patch` equals the exact delta (`receipts/09-*`). I found no
  manager-produced bank receipts in that tree and no manager evidence comment on the issue
  or PR beyond the assignment and review-start notices. The manager's same-head banks are
  therefore taken as stated in the assignment, not independently inspected.

## 2. Verification of the round-3 claims

**(a) Parent port parser at 162, with the bundle covering its four ports.** I ran
`check_port_contracts.scan_ports` on `tb/pp_top/pp_top_wrap.sv` (`receipts/03-parent-rules.log`):

| Revision | Ports | Undocumented |
|---|---|---|
| base | 209 | 162 |
| round 2 | 211 | 165 |
| head | 211 | **162** |

At head, no port is newly undocumented against base. Per-port attribution from
`sv_ports.declarations`:
- `aecp_name_wr_o` → its own "Processor event on clk_i…" run;
- `dbg_name_live_we_o` → its own "Independent clk_i observation…" run;
- `dbg_dyn_writes_o`, `aecp_nvm_stb_o`, `aecp_nvm_mark_o`, `dbg_notify_enq_o` → the
  "the SET_CLOCK_SOURCE refusal contract…" bundle.

At round 2, the last three were UNDOCUMENTED.

The gated `hdl/` files are unchanged since round 2 (store 28/0, engine 152/15, top 206/2,
`desc_mem_guard/wrap.sv` 31/31). So the parent processor ratchet is unaffected, and the
consumer evidence at head shows `protocol-processor 111 <= 111`.

Disposable probe (`receipts/07-bundle-probe.log`):
- The blank line the commit added at `:320` is not load-bearing: removing it still gives 162.
- Deleting the bundle's `//!` run makes the parser report the four effect ports
  undocumented (166). So the probe is able to fail.

**(b) Both `pp_top` builds warning-free; the scenario still runs in the default build.**
Each revision was built fresh from a clean scratch export with the Makefile's own `run`
target and the pinned simulator (`receipts/04-*`, `receipts/05-compare.log`):

| Revision | Default build: C++ warnings | Fixture build: C++ warnings |
|---|---|---|
| base | 0 | 0 |
| round 2 | 0 | **1** — `sim_main.cpp:9744:13: 'void run_name_writes(H&)' defined but not used [-Wunused-function]` |
| head | 0 | **0** |

- The simulator lint warnings (21 pre-existing PINMISSING/PINCONNECTEMPTY kinds on
  deliberately unconnected top outputs) are identical at base, round 2 and head in both
  builds, after normalising line numbers.
- The default build still calls `run_name_writes(h)` (`sim_main.cpp:9782`, unchanged). The
  default transcript prints `NW: 85 checks, 0 failures`, and `make name-writes` prints the
  same.
- Disposable compiler probe (`receipts/06-cxx-probe.log`): removing the attribute from a
  copy of head reproduces exactly the round-2 fixture warning, and the published head
  compiles with 0 own-file warnings in both configurations.

**(c) No behaviour change.**
- `hdl/` is byte-identical to round 2 (tree `f383eaca…`), as are `docs/`, `syn/`,
  `scripts/`, `.github/`, the pp_top `Makefile`, `README.md` and `name_wr_mutant.py`.
- In the wrapper, the set of port declarations (type, width, name) is identical as a
  multiset (211). Only the order of `aecp_name_wr_o`, `dbg_name_live_we_o` and
  `dbg_dyn_writes_o` changed. The module body after the header is token-identical. The
  wrapper is the simulation top, bound by name from C++, and nothing instantiates it
  positionally.
- In `sim_main.cpp`, the comment- and whitespace-stripped text is identical once the one
  `[[maybe_unused]] ` token is removed (`receipts/02-delta.log`).
- The complete default and fixture simulation transcripts are byte-identical between round
  2 and head. Against base, head adds only the `NW` line and the tally lines
  (7646→7731 default, 7666→7751 total). The latency lines `[B4] 2363 clocks` and
  `[B4b] 7523 clocks` are unchanged.

**(d) Donor gates.** My own runs at head (`receipts/04-head-*`, `receipts/08-gates.log`):
- pp_top 7751/0 (7731 + 20);
- `make name-writes` 85/0;
- the PR's own mutation campaign: the decode mutant builds and fails; golden and restored
  pass;
- HDL lint 40/40 OK;
- links, matrix, module-matrix, parameter inventory and uPC map all return 0;
- `make stale` is clean, and `git diff --check` is clean both round2..head and base..head.

Every other donor suite (desc_store, desc_mem_guard, ucpu, acmp_nvm, timer_map and so on)
has byte-identical inputs to round 2, where I ran them (R334-1). The author's round-3 bank
(`author-r3/gates/results.json`) covers 14 commands, all rc 0, including
`run_suites.sh 1014722/0`, `make check`, the synthesis run and `nvm_port` figures.

**(e) Parent consumer commands, with the whole project judged.** From the public round-3
receipts (`author-r3/consumer/*`):
- All 12 prescribed commands return rc 0. The run used parent `7eb3b0d4`, the processor
  gitlink at `83c84b19`, and the supplied patch (SHA-256 `1de2a73a…`, the same as round 2:
  `KL_pp_shadow.sv` open port plus the `measure_test_evidence.py` reader disposition),
  with argv matching the supplied list.
- pp_shadow is 402/0 in each of three builds.
- Port contracts: processor 111 ≤ 111.
- Evidence ratchet: 0 ≤ 0 unexplained DUT-source readers and 3 ≤ 3 wall-clock files.
  `name_wr_mutant.py` still reads DUT source (`reads_dut_source=True`), so the parent
  disposition line remains required.
- Parent lint gate: 90 ≤ 90.
- Builder: "ALL GATES PASS EXCEPT 1 NOT RUN". Gate 11, utilization calibration, is SKIP
  because the real report is absent, and that is not coverage.

Two non-green attempts are disclosed in the evidence, and I checked both:
- An incomplete-setup run of command 01 returned rc 2. The gate correctly refused an empty
  population ("no tracked C or C++ under gptp-processor/tb/") before the submodules were
  populated.
- A shared-tally `pp_top` attempt returned rc 2 with "FAIL: 4 build tallies, expected 2".
  Two concurrent runs appended to the same `obj_dir/build_tally.txt`. That mechanism is
  pre-existing at base (`Makefile:65,73`), and this PR does not touch it. The sequential
  rerun passes.

Hosted CI at the exact head: the `hdl` push and pull_request runs executed 6 jobs, all
successful. The only skipped step is the cached simulator build (`receipts/09-*`).

## 3. Findings

No open MINOR, MAJOR or BLOCKER finding at this head.

### R334-S4 — SUGGESTION — Tests
- **Where:** `tb/pp_top/sim_main.cpp:9744` (`[[maybe_unused]] static void run_name_writes`).
  The call is at `:9782`.
- **What:** the attribute silences `-Wunused-function` in *both* builds. In the default
  build the function must be called. With the attribute, deleting that call compiles
  silently (probe arm C, 0 warnings), and the tally would drop from 7751 to 7666 while
  still printing PASS; nothing in the processor gates floors the pp_top check count.
  Guarding the definition with `#ifndef PP_TOP_SRP_DOM_DEF_VID` instead (arm D) keeps both
  builds warning-free and keeps the default-build diagnostic live. The published form has
  the offsetting merit that the fixture build still type-checks the function. So this is
  a hardening option, not a defect. Warnings are not fatal in either form (`-Wno-fatal`,
  no `-Werror`).
- **Verification:** `scripts/06-cxx-probe.sh`.

Round-1 suggestions R334-S1, S2 and S3 were routed to the processor residue by the
round-3 assignment. Their subjects (`hdl/`, `tb/pp_top/README.md`, `docs/`) are unchanged at
head, and they remain suggestions.

## 4. Prior public findings at this head

I read these only after my own pass, verdict and ledger were written. The public
evidence `reviews/` folder was fetched after that point as well, and all 355 manifest
entries verify with 0 mismatches (`receipts/11-reviews-fetch.log`).

| Prior finding | Status at `83c84b19` | Reviewer evidence |
|---|---|---|
| R334-1 F1 (MINOR; Docs, Tests): harness bundle detached, 165 vs 162 undocumented | **CLOSED** | parser 162 at head, all six effect/name ports attributed, with the bundle covering its four ports (`receipts/03-*`); negative control bites (`07-*`); NW 85/0 and pp_top 7751/0 (`04-head-*`) |
| R334-1 S1/S2/S3 (SUGGESTION) | Open as suggestions, routed to processor residue | subjects unchanged at head |
| R335-1 F1 (MINOR; Tests): `-Wunused-function` for `run_name_writes` in the fixture build | **RESOLVED** | its required outcome allowed `[[maybe_unused]]`; fresh builds give 0 C++ warnings in both builds, as at base, with pp_top 7751/0 and name-writes 85/0 (`receipts/05-compare.log`); removing the attribute reproduces the warning (`06-*`) |
| R335-1 S1/S2 (SUGGESTION) | Open as suggestions, routed to processor residue | subjects unchanged at head (same topics as R334-1 S1/S3) |
| Manager round-2 items 1–4 (at `691f1d2b`) | Remain RESOLVED | parent C++ and Python scanners give 0 on every rule at head, with no function over 100 lines (`receipts/03-*`); consumer 01/02/08/10 rc 0 at head; `hdl/` unchanged |

There are no formal PR reviews and no inline review comments on PR #121.

## 5. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | SET/GET_NAME wire behaviour unchanged: `hdl/` and `gen_ucode.py` identical to round 2; NW 85/0 and pp_top 7751/0 transcripts byte-identical to round 2 (`receipts/04-*`, `05-*`) | R334-2 (delta), on R334-1 full | 83c84b19e09d397ed2eb6f5ace337686ce0ef86b |
| RTL | CLEAN | `hdl/` tree identical to round 2 (`receipts/02-delta.log`); lint 40/40 (`08-*`); simulator lint set identical base/r2/head (`05-*`); wrapper port set and body token-identical | R334-2 (delta), on R334-1 full | 83c84b19e09d397ed2eb6f5ace337686ce0ef86b |
| Robustness | CLEAN | Refusal/stall/abort/recovery NW scenarios still run and pass in the default build; fixture build unchanged (20/0); disclosed rc 2 attempts classified (refused population; pre-existing shared tally file) | R334-2 (delta), on R334-1 full | 83c84b19e09d397ed2eb6f5ace337686ce0ef86b |
| Tests | CLEAN | `sim_main.cpp` delta, both fresh builds (0 C++ warnings), compiler probe arms A–D, shipped decode mutant killed at head, `pp_top_wrap.sv` harness contracts via parent parser; R334-S4 is advisory | R334-2 | 83c84b19e09d397ed2eb6f5ace337686ce0ef86b |
| Docs | CLEAN | `pp_top_wrap.sv` `//!` bundle attribution (162, all six effect/name ports documented), negative-control probe, docs gates, PR body round-3 claims | R334-2 | 83c84b19e09d397ed2eb6f5ace337686ce0ef86b |

## 6. Real limits

- The prescribed simulator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`
  **does not exist**. I used the pinned 5.050 installation (rev v5.050, `verilator_bin`
  SHA-256 `44898b22…`) through a packet-local wrapper. That is the same installation that the
  same-head manager wrapper `$VALIDATION_STORAGE/pp120-manager-83c84b19/pinned-tool-bin/verilator`
  targets (`receipts/00-identity.txt`). Scratch copies cap simulator build parallelism at
  `-j 8`; nothing else was changed.
- I did **not** execute the parent consumer commands or any full bank (out of scope). My
  consumer evidence is the public round-3 receipts, plus the parent's own per-file scanners
  applied to the processor files.
- I found no manager-produced bank receipts in the public tree. The manager's same-head
  source/builder/native banks are taken as stated, not inspected.
- Builder gate 11 (utilization calibration) is SKIP. That is not coverage. Physical
  calibration is NOT RUN, and field skips are not hardware proof.
- The donor suites other than pp_top were not rerun this round, because their inputs are
  byte-identical to round 2, where I ran them.
- The review clone was never written. It re-verifies as byte-exact: HEAD, tree, index ==
  tree, 248 blobs and modes, no residue, 0 gitlinks (none required)
  (`receipts/10-restore-verify.log`).
- Receipts have the host home directory replaced by `$HOME` and the packet path by
  `<packet>`.

## 7. Pending manager duties

- Build and validate the final current-dev candidate at the merge turn (source base
  `0922e434`, live parent dev `7eb3b0d4`). Own hosted/act acceptance.
- The parent pin bump must carry the open `.aecp_name_wr_o()` line (or the real #502
  connection) and the `name_wr_mutant.py` reader disposition. Without them, parent strict
  lint and the evidence ratchet fail.
- Obtain the second independent positive review. Physical calibration and hardware remain
  open.

## 8. Receipts

Every published file is listed in `MANIFEST.sha256`. The scripts are portable: paths are
packet-relative, and the clone path can be overridden with `CLONE=`. Run order:

| Scripts | Purpose |
|---|---|
| `00-fetch-parent.sh`, `00-identity.sh`, `01-export.sh` | setup |
| `02-delta.py` | delta, port set and token checks |
| `03-parent-rules.py` | parent scanners |
| `04-pp_top.sh base\|r2\|head` | fresh suite builds and runs |
| `05-compare.py` | warning sets and transcripts |
| `06-cxx-probe.sh` | compiler probe arms A–D |
| `07-bundle-probe.py` | bundle probe with negative control |
| `08-gates.sh` | shipped mutant, lint and docs gates |
| `09-public-evidence.sh` | public evidence and hosted CI |
| `10-restore-verify.sh` | clone integrity |
| `11-reviews-fetch.sh` | deferred `reviews/` hashes, run after the verdict |

`tools/verilator` is the packet-local wrapper for the pinned simulator.

R334-2 FINISHED
