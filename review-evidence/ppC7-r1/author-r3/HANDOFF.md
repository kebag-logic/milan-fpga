# [A513] Lane C7 (counters), round 3: handoff

Branch `c7-counters` from `81edaaa` (pushed, the round-2 head). Issues #44, #78, #79. PR #147.
Assignment: #79 comment 5965236068. Reviews: R442-2 (#147 comment 5965229967, NEGATIVE,
one MINOR: F1; S1 taken) and R443-2 (#147 comment 5965207553, POSITIVE).
TAKEN posted: #79 comment 5965239510.

Status: DONE. Head `9758a98aeee958be7dcdc171943550227e73aaf7` (local, two commits on
`81edaaa`, not pushed; the PR body is handed over as `PR-BODY.md`, "Round 3" section, plus a
four-line correction inside Round 2's item 2). Every gate rc 0 (below). REVIEW READY posted
on #79 (comment 5965765071, 2026-10-03 07:00 CEST) with head
`9758a98aeee958be7dcdc171943550227e73aaf7`.

| Commit | Item |
|---|---|
| `0bcf856` | 1. R442-2 F1: F01.1, F01.2 and F03.1 redrawn to the landed top |
| `9758a98` | 2. R442-2 S1: F01.5 lists no "counters" |

No STOP condition met: the round changes three draw.io sources, their three SVG exports
and four rows of F01.5, nothing else. `git diff 81edaaa 9758a98 -- hdl tb scripts syn
Makefile .github` is empty.

## 0. Design

The round is figures and one table. Decisions taken where the finding left a choice:

1. **Redraw, not a "superseded" note.** R442-2 F1 accepts a note as the minimum; the
   assignment asks for the redraw, so each figure is edited in its draw.io source and
   re-exported. The draw.io CLI completes headless on this host
   (`xvfb-run -a drawio --no-sandbox -x -f svg --crop`, the Makefile's own fallback rule;
   about 3 minutes per figure because the display-less first attempt waits before the
   fallback). The SVGs are the CLI's output, never edited. Each was rendered to PNG
   (`drawio -x -f png`, and `rsvg-convert` on the committed SVG) and inspected for
   overlap, clipped text and edges through boxes, as `docs/diagrams/README.md` requires.
2. **F01.2: one faces group, as F01.3 and 01's block table already have it.** The landed
   top reaches the external engines through the faces of 02 §4: `srp` and `maap` as class B
   (02 §1, §4.1, §4.2), gPTP, AVTP and media clocking as class-D levels and one-cycle
   strobes (02 §4.3 to §4.5), and the `gsi_*` and `ctr_*` word read faces (02 §4.3, §4.6).
   The group holds exactly those three faces, the same split as the block-table row
   `01:92` and F01.3's `faces` node. The counters block is removed rather than kept as an
   in-core "read face" box: the read face is a face, so it sits in the faces group, and
   the "GET_COUNTERS read path" row (`01:86`) is drawn as the `words` edge from the read
   faces into the AECP engine, F01.3's `faces -- "gsi / ctr read words" --> ucpu`. The SRP
   engine (10) and the MAAP engine (11) are named inside the class-B face box as their
   in-core servers (SRP by default, `P-EN-SRP-ENGINE` = 1; MAAP opt-in,
   `cfg_maap_internal_i`), so the figure no longer shows an "SRP/MAAP adapter".
3. **F03.1: the three relabels R442-2 asked for, nothing more.** The counter-banks store
   goes; the event source names the 02 §5 producers (the integrator's strobes and level
   edges; the SRP, MAAP and ADP engines' events); the router's output is "to SMs /
   notifications". The figure still draws the descriptor image on chip. That is a
   different, older divergence: the note under F03.1 (`03:18-22`) and
   `docs/guides/hdl-engineer.md:255` say so. Moving the image off chip would make that
   note and that guide row wrong, and editing them is text beyond the figures (the
   assignment's STOP line), so it is left as it is and recorded under "What remains".
4. **F01.1: "GET_COUNTERS reporting", and the edge classes.** Besides the "counters" →
   "GET_COUNTERS reporting" change R442-2 asked for, the gPTP, AVTP and media-clock edges
   were tagged `B/C/D`, a class-B face (an adapter op table) that the landed top does not
   have (02 §1, F02.9). They now carry their landed classes: gPTP `D · gsi · ctr`
   (levels and strobes in; GET_AVB_INFO/GET_AS_PATH words; the AVB_INTERFACE counters on
   the `ctr` face, 02 §4.3), AVTP `D · gsi · ctr` (02 §4.4), media clock `D · ctr` (the
   clock-source level out; LOCKED/UNLOCKED on the `ctr` face, 02 §4.5). The srp/maap edge
   keeps `B/C/D` (F02.9: `srp` B+C+D, `maap` B+C).
5. **F01.5 (S1).** The reviewer's suggested text. The processor's only per-object counter
   state is the notification block's one-second slot per served descriptor:
   `N_CTR_DESC_C = N_STREAM_IN_P + N_STREAM_OUT_P + 2` (`hdl/aecp/KL_aecp_notify.sv:382-385`),
   one per stream index plus AVB_INTERFACE 0 and CLOCK_DOMAIN 0. So the stream rows scale
   "counter-notification slots", and the clock-domain row drops "counters" (one slot,
   whatever P-N-CLOCK-DOMAINS is). S1 also names the P-N-AVB-INTERFACES row, whose
   "counters" sits in the range cell's redundancy-seam note; it becomes
   "counter-notification slots" too, which is the seam #69 owns (one AVB_INTERFACE slot
   today). F01.5 now names no "counters" in any cell.

Clauses: no counter or interface semantics change. The figures follow 02 §1 and §4.1 to
§4.6 and 02 §5's event catalog; the owner decision of 2026-09-19 (#44 comment 5740180072,
#79 comment 5740180166: the integrator keeps every counter); Milan v1.2 §5.4.2.25 and
IEEE 1722.1-2021 §7.4.42 (GET_COUNTERS) as the processor's only counter duty.

## 1. Item 1: R442-2 F1 (commit `0bcf856`)

| Figure | Change | Where |
|---|---|---|
| F01.2 | "Counters subsystem" block (`ctrs`) and its edge `e14` removed | `docs/diagrams/src/01-top-level.drawio` (was `:63-65`, `:135`) |
| F01.2 | "External-engine adapters" group and its four adapter boxes replaced by the group `faces`, "External-engine faces (02 §4)", with `f-srp` "srp · maap faces (class B) / in core: SRP engine (10, default), / MAAP engine (11, opt-in)", `f-lvl` "gPTP · AVTP · media clock / class-D levels + change strobes", `f-rd` "gsi · ctr read faces / GET_* words + change strobes" | `01-top-level.drawio:80-91` |
| F01.2 | new edge `e14` `words`, `f-rd` → AECP engine, through the gutters x=1040, y=565, x=960 | `01-top-level.drawio:129-131` |
| F01.2 | `e22` `events` now leaves the `faces` group | `01-top-level.drawio:150` |
| F03.1 | "counter banks" store (`ram4`) removed; the state-RAM group narrowed to its three RAMs; `d16` "RAM ports" re-pointed into it | `docs/diagrams/src/03-shared-datapath.drawio:53-55`, `:109-111` |
| F03.1 | "adapter events / srp · maap · gptp · avtp · mclk" → `evsrc` "integrator strobes + level edges / SRP · MAAP · ADP engine events" | `03-shared-datapath.drawio:72-74`, `:117` |
| F03.1 | "to SMs / counters" → "to SMs / notifications" (label moved onto the horizontal run, clear of the TX arbiter) | `03-shared-datapath.drawio:118-120` |
| F01.1 | processor box: "GET_COUNTERS reporting", not "counters" (four lines, so it does not wrap) | `docs/diagrams/src/01-system-context.drawio:25` |
| F01.1 | gPTP, AVTP, media-clock edges `B/C/D` → `D · gsi · ctr`, `D · gsi · ctr`, `D · ctr`; all four engine-edge labels placed on their upper segments | `01-system-context.drawio:61-72` |
| F01.1 | legend line: "gsi · ctr: the read faces of 02 §4.3 and §4.6; gPTP, AVTP and media clocking have no class-B face" | `01-system-context.drawio:52-53` |
| all three | re-exported with `make docs/diagrams/<name>.svg` | `docs/diagrams/01-system-context.svg`, `01-top-level.svg`, `03-shared-datapath.svg` |

Tests: none apply (figures). The gates that hold them: `make check`'s `stale` (export
not older than its source) and `lint`; the reviewer's label grep; the inspection renders.

| Check | Its failing "mutant" |
|---|---|
| `make stale` | an uncommitted edit to `01-top-level.drawio` newer than its export: rc 2, "STALE: docs/diagrams/01-top-level.svg (uncommitted source edit newer than the export)"; reverted, rc 0 |
| R442-2's grep over the three sources | at `81edaaa` it printed the counters block, the counter banks, "to SMs / counters" and the adapters; at head it prints four labels, none an in-processor counter block or adapter (below) |

R442-2's verification grep at head
(`grep -o 'value="[^"]*"' docs/diagrams/src/{01-top-level,03-shared-datapath,01-system-context}.drawio | grep -iE 'counter|gptp.*adapter|avtp|media-clock.*adapter'`):
- `01-top-level.drawio`: "gPTP · AVTP · media clock / class-D levels + change strobes" (the landed levels face);
- `01-system-context.drawio`: the processor box ("GET_COUNTERS reporting", the reviewer's own text); "AVTP streaming engine (1722-2016, CBS)" (the external engine, unchanged); the legend line naming AVTP.

In the three SVG exports no "adapter", "Counters subsystem", "counter banks" or
"to SMs / counters" remains; the five hand-authored SVGs (20 to 24) name none either.

## 2. Item 2: R442-2 S1 (commit `9758a98`)

| Row | Before | After | Where |
|---|---|---|---|
| P-N-AVB-INTERFACES (range) | keys registry/ADP/counters/records | keys registry/ADP/counter-notification slots/records | `docs/architecture/01_overview.md:154` |
| P-N-STREAM-IN (affects) | sink records, discovery SMs, counters | sink records, discovery SMs, counter-notification slots | `01_overview.md:155` |
| P-N-STREAM-OUT (affects) | source records, DA timers, counters | source records, DA timers, counter-notification slots | `01_overview.md:156` |
| P-N-AUDIO-UNITS / P-N-CLOCK-DOMAINS / P-N-CLOCK-SOURCES (affects) | overlay, counters; MVU MCR deferred … | overlay; MVU MCR deferred … | `01_overview.md:159` |

Source of the slot count: `hdl/aecp/KL_aecp_notify.sv:382-385`, decode `:488-507` (graded
by K17 since round 2).

## Parent-visible list

- **No interface change.** No port, parameter or register of `protocol_processor_top`
  changes; the `ctr_*` face, `KL_pp_shadow` and the parent's GET_COUNTERS path are
  untouched. Both adoption patches are unchanged (sha256 `67bcd698…` and `aa5a88eb…`)
  and apply, c4c6 then c8.
- **No RTL, test, script or build change**: `git diff 81edaaa 9758a98 -- hdl tb scripts
  syn Makefile .github` is empty. Gate 8 counts the same 1,756 processor ports.
- **Figures and text the parent cites move:** F01.1, F01.2 and F03.1 (the draw.io sources
  and the SVG exports); F01.5's P-N-AVB-INTERFACES, P-N-STREAM-IN, P-N-STREAM-OUT and
  P-N-CLOCK-DOMAINS rows. No anchor and no heading changes.
- **Tallies:** unchanged. `tb/pp_top` 9,196; `tb/adp_engine` 1,328; sweep 1,019,116; the
  ctr campaign 17 arms.

## Gates

All with the pinned Verilator 5.050 (wrapper sha256 `905795b9…`), each command with its own
log and rc under the scratch area `$VALIDATION_STORAGE/c7-a513/` (`logs/`, `gates/`), heavy ones
under the round-2 memory guard (`guarded.py`: samples the service cgroup, kills its own
command above 10.5 GB anonymous; none tripped). draw.io is `drawio-desktop` 30.2.4.

### Processor suites and entry points

| Command | Where | Result |
|---|---|---|
| `./scripts/run_suites.sh` | `git archive` of `9758a98` | rc 0: 33 suites, **1,019,116** checks, 0 failing; every per-suite tally equal to round 2 (`tb/pp_top` 9,196, `tb/adp_engine` 1,328); the UPC map, M9 opcode selftest and M9 opcode gates PASS; 771 s, peak anon 2.8 GB |
| `./scripts/lint_hdl.sh` | clone at `9758a98` | rc 0, 41 of 41 |
| `make check` | clone at `9758a98` | rc 0: 41 mermaid + 18 wavedrom blocks, 1,095 links, 115 REQ rows, 17 GAP findings, 94 module rows 0 untested (`gen_matrix.py --check`), 27 parameters; `stale` silent (pass) |
| `make stale`, negative control | same clone | rc 2 with one uncommitted byte appended to `01-top-level.drawio` ("STALE: docs/diagrams/01-top-level.svg (uncommitted source edit newer than the export)"); rc 0 after `git checkout` of it |
| `make -C tb/nvm_port figures` (the CI figure gate) | same clone, with `refs/pull/13/head` fetched as CI does | rc 0, "all measured figures agree with the tree", 235 s |
| `git diff --check c74711d4 HEAD`, `git diff --check 81edaaa HEAD` | tree | rc 0, rc 0 |
| `git apply --check`, every campaign patch in `tb/` | clone at `9758a98` | 224 of 224 |
| R442-2's figure-label grep | tree | four labels, none an in-processor counter block or adapter (item 1) |
| SVG label search (`adapter`, `Counters subsystem`, `counter banks`, `to SMs / counters`) | the three exports and the five hand-authored SVGs 20 to 24 | no hit |

### Mutants

| Campaign | Result |
|---|---|
| `tb/pp_top/ctr_mutants.py --jobs 8` (archive of `9758a98`, pinned to CPUs 0-3) | rc 0: control PASS, 17 of 17 KILLED, each by its named check; 341 s; printed record byte-identical to round 2's `--jobs 1` and `--jobs 8` records (sha256 `0fd23cc6151456beb54d51c9238ed820de4af232423cd4ec1789f6ee6c8cbdc5`, 11,104 B); peak anon 9.8 GB for the service (test_builder ran beside it) |
| other campaigns | not re-run: `hdl/` and `tb/` are byte-identical to `81edaaa`, where round 2 recorded them |

The per-arm record is round 2's, unchanged (same bytes): `ctr-avb-not-supported` 9,
`ctr-ckd-not-supported` 3, `ctr-index-from-type` 18, `ctr-block-beats-swapped` 9,
`ctr-locate-ignored` 1, `ctr-notify-avb-dropped` 6, `ctr-notify-avb-as-clock` 8,
`ctr-notify-ckd-dropped` 1, `ctr-notify-one-window` 3, `ctr-notify-no-window` 5,
`ctr-change-type-from-index` 8, `ctr-notify-avb-any-index` 1, `ctr-notify-ckd-any-index` 1,
`ctr-notify-stri-past-shape` 1, `ctr-notify-stro-past-shape` 1, `store-counts-domain-strobes`
7, `store-link-detector-resets-up` 11 failing checks.

The figures have no test of their own; their gate and its failing input are under item 1
(`stale` and the negative control; the label grep before and after).

### Parent consumer gates (dev `cdf49d1a` + c4c6 + c8)

Scratch parent `$VALIDATION_STORAGE/c7-a513/parent`: `git archive` of the trusted checkout,
`git init` and commit; `external` `efeb541a`, `gptp-processor` `5dce647a`,
`third_party/verilog-axis` `48ff7a7e` cloned from the round-1 local mirrors at their pins;
`protocol-processor` a clone of this branch at `9758a98`, its gitlink committed;
`git submodule init`; then `parent-adoption-c4c6-ea3fb388.patch` (sha256 `67bcd698…`) and
`parent-adoption-c8-cdf49d1a.patch` (`aa5a88eb…`) with `git apply`, in that order. The
trusted checkout is untouched (HEAD `cdf49d1a`, `git status` empty after the run).

| # | Gate | Result at `9758a98` |
|---|---|---|
| 1 | `check_cpp_idiom.py` | rc 0, every ratchet held; 168 translation units; multi-declarator 0 <= 0 |
| 2 | `check_py_idiom.py` | rc 0, every ratchet held |
| 3 | `xvlog_gate.py --check` (alone, last) | rc 0, 4 findings == ratchet (0 hdl/, 4 pinned processors); 140 s |
| 4 | `check_rtl_source_lists.py` | rc 0: 107 files; protocol-processor 36/42 tops, 6 recorded |
| 5 | `pp_srcs.py --check --selftest` | rc 0 |
| 6 | `sw/builder/test_builder.py` (no other parent gate beside it) | rc 0: ALL GATES PASS EXCEPT 1 NOT RUN (gate 11, a board report not on this host); 1,099 s |
| 7 | `make -C tb/verilator/pp_shadow -j16` | rc 0: 606, 606, 646 and 311 checks, 0 failures; 219 s |
| 8 | `check_port_contracts.py` | rc 0: protocol-processor 1,756 ports |
| 9 | `measure_naming.py --check` | rc 0, 96 recorded |
| 10 | `measure_test_evidence.py --check` | rc 0, 0 <= 0 unexplained DUT-source readers |
| 11 | `docs_check.py` | rc 0, 0 findings (185 md files) |
| 12 | `lint_rtl.py --check` | rc 0, 90 <= 90 |
| 13 | `make -C tb/verilator/nvm_cosim lint` | rc 0 |
| 14 | `make -C tb/verilator/nvm_cosim quick` | rc 0, 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j16` | rc 0, 9 RESULT PASS, 0 FAIL; `[CTRS2]` reads mask 0x23 and LINK_UP = LINK_DOWN + 1; 1,476 s |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | rc 0, leg defects 5/5; 340 s |

## Out-of-context cost

No RTL changes: `git diff 81edaaa 9758a98 -- hdl` is empty, so the elaborated source is
identical and the cost is 0 by construction. No synthesis was run. Round 1's measured
record stands.

## What remains

- Outside the assignment (STOP line: figures and F01.5), left as found and recorded in the
  PR body:
  - `docs/00_MILAN_COMPLIANCE_REVIEW.md:366`, REQ-ADP-009's mechanism cell "GPTP adapter
    event": text naming a removed adapter (the landed source is `gm_change_i`). Neither
    round-2 review named it.
  - F03.1's descriptor image on chip (noted under the figure and in
    `docs/guides/hdl-engineer.md:255`).
  - R443-2 S1 (zero identity) and S2 (F09.1 "mask ROMs"): not taken by the assignment.
  - `docs/diagrams/README.md` says the draw.io CLI hangs headless on the development
    machine; on this host it completes (about 3 minutes a figure through the Makefile
    rule). Not edited (text beyond the figures).
- Not run: the other mutation campaigns and the off-vendor yosys elaboration (inputs
  byte-identical to `81edaaa`); hosted CI (the manager's).

## Housekeeping

- The lane tree is clean: `git status --short --ignored` prints nothing at `9758a98`. Every
  render, build and run happened in the scratch area.
- Scratch: `$VALIDATION_STORAGE/c7-a513/` (renders in `render/`, runs in `logs/` and `gates/`,
  the parent copy in `parent/`, the archive `pp-head/`, the clone `pp-clone/`).
- PR-BODY.md: 39.5 KB, under 65,536; only additions to the earlier sections (`diff`
  against round 2's file shows no removed line).
