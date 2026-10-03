# [A514] Lane C7 (counters), round 4 (merge of main): handoff

Branch `c7-counters` from `9758a98` (round 3, pushed). Issues #44, #78, #79. PR #147.
Assignment: #79 comment 5965782033 (merge `main` `ddb3119d`, PR #145, lane P2: NVM port
deadline). TAKEN posted: #79 comment 5965784398.

Status: DONE. Head `af751a5aa9a809c982949cfb838a0de1fffc3e46`, one merge commit on
`9758a98` (local, not pushed; the PR body is handed over as `PR-BODY.md`, new "Round 4"
section). Every gate rc 0 (below). REVIEW READY posted on #79 (comment 5966458578) with
head `af751a5aa9a809c982949cfb838a0de1fffc3e46`.

| Commit | Item |
|---|---|
| `af751a5` | 1. merge of `main` `ddb3119d` (`--no-ff`; parents `9758a98`, `ddb3119d`), with the 09 renumbering and its one citation |

Item 2 (re-measure) adds no commit: every run happened in the scratch area.

No STOP condition met: nothing beyond the merge. No port, parameter or register is added
by this lane; the one new top parameter, `NVM_MEM_TMO_CYC_P`, is main's (P2's).

## 0. Design

The round is a merge. The two sides meet in seven files and add to each other without a
semantic overlap: P2 (PR #145) gives the NVM port a device-face deadline
(`NVM_MEM_TMO_CYC_P`, `T-NVM-PORT-DEADLINE`, `err_cause` 3 DEADLINE); this lane documents
and grades the counters face (`ctr_*`) and removed the dead GPTP_GM_CHANGED tick. Every
file keeps both sides. Decisions where the assignment left a choice:

1. **09: P2 keeps §8.6, the counters face becomes §8.7, placed after it.** The only
   textual conflict. P2's §8.6 and its back-reference at `09:215` ("§8.6's") are P2's
   and unchanged. The counters section is moved whole, heading renumbered, body
   byte-identical.
2. **Citations of the moved section: one.** A search of the merged tree for every
   spelling (`§8.6`, `09 §8.6`, `#86-…`, `counters-face` anchors into 09, section-range
   citations) finds one citation of the counters section, the GAP-05 "Verified by" cell
   at `docs/00_MILAN_COMPLIANCE_REVIEW.md:539`; its text and anchor move to
   `[09 §8.7](architecture/09_verification.md#87-the-counters-face-issues-44-79)`. The
   other `§8.6` hits are P2's own, Milan §5.3.8.6, 802.1Q §35.2.2.8.6 and the parent's
   D3 contract §8.6, none of them 09. The PR body's earlier sections, which say "09
   §8.6" as a record of rounds 1 and 2, are not rewritten; Round 4 states the move.
3. **The top, 01, 02, 07, 08 and integrator.md merge without conflict**, and each keeps
   both sides exactly: for each file the merged result differs from main by exactly the
   lane's lines and from the lane by exactly main's (`git diff` line counts: top 4/17, 01
   38/1, 02 236/38, 07 38/17, 08 8/25, integrator 97/3). Checked as text, not only as
   counts:
   - the top: `NVM_MEM_TMO_CYC_P` (`protocol_processor_top.sv:161-173`, bound at
     `:2883-2885`) beside the lane's counters banner (`:382`) and the removed
     `adp_gm_tick_nc_w` and `.gm_changed_tick_o` (round 1; the module port went in
     round 1, so these two lines are part of that, not a new change);
   - 02: P2's §8 deadline (`02:578-`, anchor `sec-02-nvm-deadline` at `:607`) beside the
     lane's §4.3 to §4.6 (`ctr` face at `:410`);
   - integrator.md: P2's `NVM_MEM_TMO_CYC_P` parameter row (`:99`) and NVM-device tie-off
     row (`:387`) beside the lane's Counters tie-off row (`:389`) and §7.1 (`:407-`);
   - F01.5: P2's `P-NVM-MEM-TMO-CYC` row (`01:181`) beside the lane's round-3 cells
     (`01:154-159`);
   - 07 and 08: P2's deadline text beside the lane's F07.10 / T-CTR-OBSERVE edits.
   - No merged text contradicts P2: no "no deadline of its own", "quarantined until
     reset", "Code 3 … never produced" or "3 reserved" remains anywhere in `docs`, `hdl`
     or `tb/pp_top`.
4. **No STOP condition met.** No port, parameter or register is added or changed by this
   lane; `NVM_MEM_TMO_CYC_P` is main's (P2's, already ruled on #15 and adopted by the
   parent patch `parent-adoption-p2-cdf49d1a.patch`). Nothing beyond the merge and its
   one citation.

Clauses: none change. The counters semantics stay those of rounds 1 to 3 (Milan v1.2
§5.4.2.25, Tables 5.1, 5.13 to 5.17 and 5.22; IEEE 1722.1-2021 §7.4.42, Tables 7-152 to
7-159). P2's deadline is processor issue #15's ruling.

## 1. Item 1: merge of `main` `ddb3119d`

Merge commit `af751a5` (`git merge --no-ff`, parents `9758a98` and `ddb3119d`; no rebase,
nothing amended). Merge base `c74711d4` (round 1's manager merge brought it in).

| File | Resolution | Where |
|---|---|---|
| `docs/architecture/09_verification.md` | conflict: P2's §8.6 kept as is; the counters section follows it as §8.7, body unchanged | `09:323` (§8.6, P2), `09:352` (§8.7, this lane) |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md` | the one citation moved: GAP-05 "Verified by" now `[09 §8.7](architecture/09_verification.md#87-the-counters-face-issues-44-79)` | `00:539` |
| `hdl/top/protocol_processor_top.sv` | clean: P2's `NVM_MEM_TMO_CYC_P` and its binding beside this lane's banner and tick removal | `:161-173`, `:2883-2885`; `:382`, the former `:1838`/`:1932` lines |
| `docs/architecture/02_interfaces.md` | clean: P2's §8 (`err_cause` 3 DEADLINE, the port's deadline, §8.2 drain row) beside §4.3 to §4.6 | `:578-`, `:607`, `:709`; `:344-`, `:410-` |
| `docs/guides/integrator.md` | clean: P2's parameter row and NVM tie-off row beside the counters row and §7.1 | `:99`, `:387`; `:389`, `:407-` |
| `docs/architecture/01_overview.md` | clean: P2's `P-NVM-MEM-TMO-CYC` row beside the round-3 F01.5 cells | `:181`; `:154-159` |
| `docs/architecture/07_memory_maps.md`, `08_timing.md` | clean, both sides kept | P2: 07 §5.3 rows and "What the deadline does not do", 08 F08.1 `T-NVM-PORT-DEADLINE` and the quarantine paragraph |
| the rest of main (`hdl/acmp`, `hdl/aecp`, `hdl/packet_engine` NVM files, `tb/nvm_port`, `tb/acmp_nvm`, figure 21) | main only, taken as is | |

`git diff ddb3119d af751a5` is this lane's PR diff (51 files, +1,452 / -287, the same
counts as `c74711d4..9758a98`); `git diff 9758a98 af751a5` is main's P2 delta (25 files,
+4,174 / -347) plus the renumbering.

Tests: none new (a merge). The checks that hold the resolution: `make check`'s `links`
(every anchor resolves: the moved citation's `#87-…` anchor, P2's `#sec-02-nvm-deadline`)
and `params` (top, guide and figure 21 agree on 28 parameters); the whole suite sweep and
every campaign that builds the merged top (item 2).

## 2. Item 2: re-measure

What the assignment asks, and where each is answered:

| Asked | Done | Result |
|---|---|---|
| every processor suite | `run_suites.sh`, fresh archive of `af751a5` | rc 0, 1,020,227 checks (Gates) |
| `git apply --check` on every campaign patch | every `tb/**/*.patch`, clone at `af751a5` | 224 of 224 |
| the ctr campaign | `ctr_mutants.py --jobs 5` | 17 of 17 KILLED, record byte-identical to rounds 2 and 3 |
| every campaign that reads a merged file | every `tb/pp_top` campaign (each builds the merged top; d3 also builds `tb/acmp_nvm`, which P2 changed) | all KILLED, every failing-check count equal to its README record |
| the docs and figure gates | `make check` (mermaid, wavedrom, links, matrix, modmatrix, params, stale), stale negative control, `make -C tb/nvm_port figures`, the round-3 figure-label search | all rc 0 |
| the parent consumer set (16) at dev `1269cdaf` + c8 + p2 | scratch parent | 16 of 16 rc 0 |

Beyond the list, because the top changed: the hdl workflow's other jobs (yosys
portability; the srp_top, maap and adp campaigns), and an out-of-context synthesis of the
lane's RTL delta on the new base (Out-of-context cost).

Campaigns that read no merged file and were not re-run: `tb/srp_admission/mutants.py`,
`tb/acmp_talker/retry_mutants.py`, `tb/desc_store/lint_suppression.py`. Their Makefile
source lists name none of the merged files (`hdl/top`, the four NVM modules, or a doc),
and their inputs are byte-identical at `9758a98`, `ddb3119d` and `af751a5`.

A first sweep attempt stopped mid-run with no rc and no output after `srp_stream_fsms`
(every suite it reached passed; log kept as `logs/sweep-interrupted.log`). The service's
`memory.events` shows no OOM kill; it stopped the moment a `timeout`-bounded wait of mine
expired, the only event at that time, so every later wait is a plain polling loop. The
re-run, from a fresh `git archive`, is the result recorded below.

## Parent-visible list

- **No interface change from this lane.** The lane's own diff against main is the same
  as before the merge (`git diff ddb3119d af751a5`: 51 files, +1,452 / -287, as
  `c74711d4..9758a98`; its `hdl` part has the same stable patch-id, `e368d122…`, at both
  bases). The `ctr_*` face, `KL_pp_shadow` and the parent's GET_COUNTERS path are
  untouched. Gate 8 counts the same 1,756 processor ports.
- **What the merge brings is main's (P2's) and already adopted by the parent patch:**
  `NVM_MEM_TMO_CYC_P` (default `CLK_HZ_P`), `err_cause` 3 DEADLINE, `T-NVM-PORT-DEADLINE`.
  `parent-adoption-p2-cdf49d1a.patch` (sha256 `590f791d…`) applies after
  `parent-adoption-c8-cdf49d1a.patch` (sha256 `aa5a88eb…`, unchanged) at dev `1269cdaf`.
- **A section number the parent may cite moves:** 09's counters section is now **§8.7**
  (`#87-the-counters-face-issues-44-79`); §8.6 is P2's NVM port section. Nothing else
  this lane wrote moves; no other anchor changes.
- **Tallies:** `tb/pp_top` 9,196 and `tb/adp_engine` 1,328, unchanged; the sweep is
  1,020,227 (round 3's 1,019,116 plus P2's +28 in `tb/acmp_nvm` and +1,083 in
  `tb/nvm_port`); the ctr campaign 17 arms, record unchanged; `make check` now counts
  1,105 links and 28 parameters (P2's).

## Gates

All with the pinned Verilator 5.050 (wrapper sha256 `905795b9…`), each run with its own
log and rc under the scratch area `$VALIDATION_STORAGE/c7-a514/` (`logs/`, `gates/`, campaign
outputs in `out/`), every heavy one under the round-2 memory guard (`guarded.py`: samples
the service cgroup, kills its own command above 10.5 GB anonymous; none tripped). Peak
anonymous memory is the whole service's at that moment, so it includes whatever ran
beside the run.

### Processor suites and entry points

| Command | Where | Result |
|---|---|---|
| `./scripts/run_suites.sh` | fresh `git archive` of `af751a5` | rc 0: 33 suites, **1,020,227** checks, 0 failing; UPC map, M9 opcode selftest (9/9) and M9 opcode gates PASS. Against round 3 only P2's suites moved: `tb/acmp_nvm` 360 → 388, `tb/nvm_port` 136 → 1,219 (+1,111 in all); `tb/pp_top` 9,196, `tb/adp_engine` 1,328 and every other suite as round 3; 861 s, peak 6.3 GB |
| `./scripts/lint_hdl.sh` | clone at `af751a5` | rc 0, 41 of 41 |
| `make check` | same clone | rc 0: 41 mermaid + 18 wavedrom blocks, 1,105 links, 115 REQ rows, 17 GAP findings, 94 module rows 0 untested, parameters top 28 = guide 28 = figure 21 28; `stale` silent (pass) |
| `make stale`, negative control | same clone | rc 2 with one uncommitted byte appended to `01-top-level.drawio` ("STALE: docs/diagrams/01-top-level.svg (uncommitted source edit newer than the export)"); rc 0 after `git checkout` |
| `make -C tb/nvm_port figures` (the CI figure gate) | same clone, `refs/pull/13/head` fetched as CI does (`5121dcef`) | rc 0, "all measured figures agree with the tree": 160 Verilator builds (1 baseline + 7 for `make run` + 12 arms + 126 mutations + 9 models + 5 matrix), baseline 393/393; 1,033 s |
| `./syn/yosys/run.sh` (the portability job) | same clone; yosys 0.66, sv2v 0.0.13 | rc 0: 36 of 36 tops elaborate; `KL_aecp_engine` through `synth_xilinx` with its 6 RAMB36 asserted; 96 s |
| `git diff --check c74711d4 HEAD`, `9758a98 HEAD`, `ddb3119d HEAD` | tree | rc 0, rc 0, rc 0 |
| `git apply --check`, every campaign patch in `tb/` | clone at `af751a5` | 224 of 224 |
| figure-label search (round 3's) | tree | no SVG names "adapter", "Counters subsystem", "counter banks" or "to SMs / counters" (figure 21, which P2 re-exported, included); R442-2's draw.io grep prints the same four labels as round 3, none an in-processor counter block or adapter |

### Mutants

Every `tb/pp_top` campaign builds the merged top, so each was re-run, from one `git
archive` of `af751a5` (each driver plants its arms in copies of its own). "As recorded"
means every arm's failing-check count equals the count in its suite's README record.

| Campaign | Result |
|---|---|
| `tb/pp_top/ctr_mutants.py --jobs 5` | rc 0: control PASS, 17 of 17 KILLED by their named checks; the printed record is byte-identical to rounds 2 and 3 (sha256 `0fd23cc6151456beb54d51c9238ed820de4af232423cd4ec1789f6ee6c8cbdc5`, 11,104 B); 117 s |
| `tb/pp_top/aecp_mutants.py --jobs 4` | rc 0: 5 controls PASS, 55 of 55 KILLED, as recorded ("60 checks: 60 PASS"); 371 s |
| `tb/pp_top/aecp_dispatch_mutants.py --jobs 4` | rc 0: 4 controls PASS (aecp-dispatch, aecp-line, d3, line-guards), 37 of 37 KILLED, as recorded; 344 s |
| `tb/pp_top/d3_mutants.py --jobs 4` | rc 0: 87 of 87 KILLED, the three goldens PASS (`tb/pp_top`, `tb/acmp_nvm` at P2's head, `tb/rx_validator`), as recorded; 1,568 s |
| `tb/pp_top/notify_mutants.py --jobs 4` | rc 0: 40 of 40 KILLED, goldens PASS, as recorded; 322 s |
| `tb/pp_top/acmp_mutants.py --jobs 4` | rc 0: 19 of 19 KILLED (14 `tb/pp_top`, 4 `tb/acmp_listener`, 1 `tb/rx_validator`), goldens PASS, as recorded; 131 s |
| `tb/pp_top/gsi_mutants.py --jobs 4` | rc 0: golden PASS, 20 variants detected by their named checks, restored PASS; 388 s |
| `tb/pp_top/name_wr_mutant.py` | rc 0: the decode mutant killed, golden and restored PASS; 43 s |
| `make -C tb/srp_top mutants` (hdl workflow) | rc 0: 11 controls PASS, 78 arms KILLED, assertion coverage 65/65 ("90 checks: 90 PASS"); 521 s |
| `make -C tb/maap mutants` (hdl workflow) | rc 0: 3 controls PASS, 29 KILLED; 75 s |
| `make -C tb/adp_engine mutants` (hdl workflow) | rc 0: 2 controls PASS, 30 KILLED; every verdict line identical to round 1's run; 118 s |

The per-arm ctr record (unchanged since round 2): `ctr-avb-not-supported` 9,
`ctr-ckd-not-supported` 3, `ctr-index-from-type` 18, `ctr-block-beats-swapped` 9,
`ctr-locate-ignored` 1, `ctr-notify-avb-dropped` 6, `ctr-notify-avb-as-clock` 8,
`ctr-notify-ckd-dropped` 1, `ctr-notify-one-window` 3, `ctr-notify-no-window` 5,
`ctr-change-type-from-index` 8, `ctr-notify-avb-any-index` 1, `ctr-notify-ckd-any-index` 1,
`ctr-notify-stri-past-shape` 1, `ctr-notify-stro-past-shape` 1, `store-counts-domain-strobes`
7, `store-link-detector-resets-up` 11 failing checks.

The merge adds no test, so no new mutant: the tests that hold the counters face (K1 to
K17, U9) and each one's failing mutants are rounds 1 and 2's, re-run above unchanged.

### Parent consumer gates (dev `1269cdaf` + c8 + p2)

Scratch parent `$VALIDATION_STORAGE/c7-a514/parent`: `git archive` of the trusted checkout
(HEAD `1269cdafb4bb964c757baae0f0c5a932d43f540b`), `git init` and commit; `external`
`efeb541a`, `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e` cloned from
the round-1 local mirrors at their pins (the same pins as at `cdf49d1a`);
`protocol-processor` a clone of this branch at `af751a5`, its gitlink committed;
`git submodule init`; then `parent-adoption-c8-cdf49d1a.patch` (sha256 `aa5a88eb…`, 8.3 KB,
7 files) and `parent-adoption-p2-cdf49d1a.patch` (sha256 `590f791d…`, 11.6 KB,
`docs/design/SAVED_STATE_MATERIALIZATION.md`) with `git apply --check` then `git apply`,
in that order. dev `1269cdaf` already carries the c4c6 adaptation, so that patch is not
applied. The trusted checkout is untouched (HEAD `1269cdaf`, `git status` empty after the
run).

| # | Gate | Result at `af751a5` |
|---|---|---|
| 1 | `check_cpp_idiom.py` | rc 0, every ratchet held; 169 translation units (P2's `fuzz_main.cpp` is the new one); multi-declarator 0 <= 0 |
| 2 | `check_py_idiom.py` | rc 0, every ratchet held |
| 3 | `xvlog_gate.py --check` (alone in this service, last) | rc 0, 4 findings == ratchet (0 hdl/, 4 pinned processors); 145 s |
| 4 | `check_rtl_source_lists.py` | rc 0: 107 files; protocol-processor 36/42 tops, 6 recorded |
| 5 | `pp_srcs.py --check --selftest` | rc 0 |
| 6 | `sw/builder/test_builder.py` (no other parent gate beside it) | rc 0: ALL GATES PASS EXCEPT 1 NOT RUN (gate 11, a board report not on this host); 1,300 s |
| 7 | `make -C tb/verilator/pp_shadow -j16` | rc 0: 606, 606, 646 and 311 checks, 0 failures; 230 s |
| 8 | `check_port_contracts.py` | rc 0: protocol-processor 1,756 ports, 111 <= 111 undocumented |
| 9 | `measure_naming.py --check` | rc 0, 96 recorded |
| 10 | `measure_test_evidence.py --check` | rc 0, 0 <= 0 unexplained DUT-source readers |
| 11 | `docs_check.py` | rc 0, 0 findings (185 md files) |
| 12 | `lint_rtl.py --check` | rc 0, 90 <= 90 |
| 13 | `make -C tb/verilator/nvm_cosim lint` | rc 0 |
| 14 | `make -C tb/verilator/nvm_cosim quick` | rc 0, 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j16` | rc 0, 9 RESULT PASS, 0 FAIL; `[CTRS2]` reads mask 0x23 and LINK_UP = LINK_DOWN + 1 through this processor; 1,543 s |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | rc 0, leg defects 5/5; 342 s |

## Out-of-context cost

The lane's RTL delta is unchanged by the merge (stable patch-id `e368d122…` at both
bases): the removed `KL_adp_engine.gm_changed_tick_o` (one flop per interface, a copy of
`gm_change_i` that reached no port), the top's `adp_gm_tick_nc_w` and its connection, and
comments. Round 1 measured it at 0 on base `88969246`. Because the top changed under it,
it was measured again on the new base with the same recipe
(`syn/ooc/protocol_processor_ooc.tcl`: the complete processor, default 8-in / 8-out shape,
`xc7a100tfgg484-2`, 10 ns clock, Vivado 2026.1), each in an empty build directory, one at a
time with nothing else of this service running:

| Resource | Base `ddb3119d` | Head `af751a5` | Delta |
|---|---:|---:|---:|
| Slice LUTs | 30,701 | 30,658 | -43 |
| Registers | 32,025 | 31,944 | -81 |
| LUT as distributed RAM | 1,222 | 1,222 | 0 |
| RAMB36 / RAMB18 / DSP | 23 / 2 / 4 | 23 / 2 / 4 | 0 |
| `u_adp` LUTs / registers | 865 / 507 | 865 / 507 | 0 |

Attribution, measured:
- **Reproducible:** the base, synthesised twice, gives byte-identical utilization reports
  (date lines aside).
- **The logic edit, not the comments:** the lane's delta was split in two and each half
  synthesised on the base. Logic only (the tick port, flop, wire and connection removed;
  comments as main) gives reports identical to the head's. Comments only gives reports
  identical to the base's.
- **Where it lands:** not in `u_adp`, which is identical, but spread over modules the
  change does not touch: the top's own registers -86 and LUTs +22, `u_aecp`'s response
  buffer -88 LUTs, the CA originator +38, the dispatch FIFOs +29, MAAP -31, the SRP
  encoder +18 and talker +26, and moves of a few LUTs elsewhere. The flop itself was
  already trimmed in the base (it reached no port), so this is the synthesis tool taking a
  different path through a netlist with one port fewer, the effect `syn/ooc/README.md`
  already records for another change ("LUT moves of a few tens in modules the change does
  not touch").
- Both builds have negative OOC slack at 10 ns (WNS -9.642 ns base, -9.844 ns head), so
  this makes no routed-timing or hardware claim.

So the lane's RTL costs nothing and, on this base, synthesises 43 LUTs and 81 registers
smaller. The record in `syn/ooc/README.md` (round 1, base `88969246`, delta 0) is not
edited: that is text beyond the merge. The host also ran another service's Vivado jobs
during these runs; the base's identical re-run shows that did not move the result.

## What remains

- Unchanged from round 3, outside the assignment, left as found:
  - `docs/00_MILAN_COMPLIANCE_REVIEW.md:366`, REQ-ADP-009's mechanism cell "GPTP adapter
    event" (the landed source is `gm_change_i`).
  - F03.1's descriptor image on chip (noted under the figure and in
    `docs/guides/hdl-engineer.md:255`).
  - R443-2 S1 (zero identity) and S2 (F09.1 "mask ROMs").
  - `docs/diagrams/README.md` says the draw.io CLI hangs headless; on this host it
    completes.
  - The redundancy seam (one AVB_INTERFACE and one CLOCK_DOMAIN notification slot,
    interface-0 inputs), recorded for processor #69.
- New this round, not edited (beyond the merge): `syn/ooc/README.md` records round 1's
  measurement on the old base; the new base's figure is above and in the PR body.
- Not run: hosted CI (the manager's); campaigns whose inputs no side changed
  (`tb/srp_admission`, `tb/acmp_talker` retry, `tb/desc_store` lint suppression).

## Housekeeping

- The lane tree is clean: `git status --short --ignored` prints nothing at `af751a5`.
  Every build, run and synthesis happened in the scratch area.
- Scratch `$VALIDATION_STORAGE/c7-a514/`: `pp-head2/` (sweep archive), `pp-clone/` (docs,
  lint, figures, yosys), `camp/` (campaign archive), `parent/` (consumer gates),
  `ooc-*` (synthesis trees and reports), `logs/`, `gates/`, `out/`.
- PR-BODY.md: Round 4 appended; only additions to the earlier sections (`diff` against
  round 3's file shows no removed line).
