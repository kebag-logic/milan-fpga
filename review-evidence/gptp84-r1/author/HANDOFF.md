# [A655] #84 + #85 handoff

Status: **REVIEW READY** (Round 1b). The manager ruled on the STOP: land
both #84 and #85 with a parent companion. The head is unchanged because no
source change was needed. The companion is `parent-adoption-gptp_shadow-85.patch`
in this directory. With it applied and committed on a local parent snapshot,
the full parent consumer list passes 11/11 rc 0. The companion rides the next
gptp-processor pin adoption in the parent.

- Repository: FPGA-gPTP (the gptp-processor submodule of milan-fpga)
- Branch: `84-85-tu-pathtrace` (local, not pushed; no PR created)
- Base: main `43acfbcc098f5af1be20a4a5458770ead3717622`
- Commit 1 (#84): `4d6288e82ebf40d10d7521a7a675feacd502b847`
- Commit 2 (#85), **head**: `53ac2e9d75ceb381c2d2b04854e760304d9ae43f`
- Issue comments: TAKEN `issuecomment-6257183580`; STOP `issuecomment-6259142231`;
  ruling ([A10]) `issuecomment-6259159680`; REVIEW READY `issuecomment-6259550165`
- Receipts: `receipts/` with `receipts/INDEX.md` generated from the files present;
  run conditions in `receipts/environment.md`

## Parent companion (Round 1b)

Ruling `issuecomment-6259159680`: land both; the parent's tests follow the
standard. Before the companion, at head, 10 of the 11 parent consumer gates
passed. gptp_shadow fails 4 of its
309 checks, all of them expectations of the pre-#85 path, at parent
`tb/verilator/gptp_shadow/sim_main.cpp` (dev e9cbb676):

| Line | Check | Expects | Head publishes | Why head is right |
|---|---|---:|---:|---|
| 891 | published full path count | 3 | 4 | received [GM, hop, src] + thisClock |
| 930 | explicit one-entry PathTrace publishes count one | 1 | 2 | [GM] + thisClock |
| 943 | present path restored for servo controls | 3 | 4 | as line 891 |
| 1003 | better Announce preserves full path count | 3 | 4 | as line 891 |

(802.1AS-2020 10.3.13.2.4 f) 5): receivedPathTrace is copied to pathTrace and,
if it is not empty, thisClock is appended; 10.3.9.23.)

`parent-adoption-gptp_shadow-85.patch` (copy in `receipts/parent-adoption/`)
changes seven lines of parent `tb/verilator/gptp_shadow/sim_main.cpp`. Its
header has one row per expectation, each citing IEEE 802.1AS-2020 10.3.9.23 /
10.3.13.2.4 f) 5):

| Parent line | Change |
|---|---|
| 891 | `published full path count` 3 -> 4 |
| 930 | `explicit one-entry PathTrace publishes count two` 1 -> 2, plus new `explicit one-entry PathTrace ends with thisClock` (`pub_path_tail0_o == OUR_CID`) |
| 943 | `present path restored for servo controls` 3 -> 4 |
| 1003 | `better Announce preserves full path count` 3 -> 4 |

Adoption snapshot: local commit `28e1085f`, on top of the head snapshot
`0edefe5d`. Its diff from dev `e9cbb676` is exactly the gitlink (53ac2e9d) and
the patch. Never pushed.

The new parent check and its planted mutants are in
`receipts/parent-adoption-mutants/`. Each arm applies the companion and plants
one gptp-processor mutant, then runs the shadow suite alone:

| Arm | Result | Failing words |
|---|---|---|
| unmutated control | rc 0, 310/310 | none |
| the received path is published without thisClock (`path_append_w = 1'b0`) | rc 2, 305/310 | `explicit one-entry PathTrace ends with thisClock got 0000000000000000 exp 02a1b2fffec3d4e5`, plus the four counts (e.g. `published full path count got ...03 exp ...04`) |
| the appended entry is the announcing source (`<= frame_cid_r`) | rc 2, 309/310 | `explicit one-entry PathTrace ends with thisClock got 00aaccfffe010205 exp 02a1b2fffec3d4e5` |

Earlier measurements, kept for the record: #84 alone (gitlink `4d6288e8`)
passed gptp_shadow 309/309 (`receipts/parent-84only/`). The uncommitted
demonstration of the same patch passed the suite 310/310, and its mutation arm
refused the uncommitted edit by design (`receipts/parent-companion-demo/`).

No port or parameter changes (parent `check_port_contracts.py` passes at
head). The *meaning* of `pub_path_count_o`/`pub_path_o` changes, as #85
requires: the count now includes thisClock. That is the parent-visible change.

## Changes

### Commit 1, #84: the grandmaster role is synchronised

- `hdl/ucode/gen_gptp_ucode.py:1738` `prog_become` sets sync-ok with the
  master bit: `e_flags(p, andm=FL_ASCAP_C, orm=FL_AMGM_C | FL_SYNCOK_C)`. The
  becoming-grandmaster commit also changes the published grandmaster identity,
  which arms the parent's 0.25 s Annex B.1.1 holdover (`KL_ptp_clock_validity`
  `gm_id_i != gm_r` and the shadow's `pub_disc_o`); nothing in the parent was
  changed, so that holdover stays.
- `hdl/ucode/gen_gptp_ucode.py:1990` `prog_leg_srto`: a Sync receipt timeout
  no longer clears a master's sync-ok. BECOME disarms timer slot 4, but
  `KL_gptp_timer` cannot recall an expiry already queued behind BECOME's event,
  so the leg keeps bit 3 exactly where bit 1 stands:
  `flags & ((flags << 2) | 7)`, `:2002`. Branch-free because the ROM packer has
  no gap for the 9-word gated form (7 words fit; measured: first-fit-decreasing
  refuses 8 or more).
- `hdl/ucode/gen_gptp_ucode.py:505` `SYNCOK_BY_AMGM_C = 2` with an assert that
  it carries bit 1 onto bit 3.
- Images regenerated by their own recipes: `tb/verilator/engine/gptp_ucode.hex`,
  `tb/verilator/ucpu/gptp_ucode.hex`, `tb/tsngen/gptp_ucode.hex`,
  `syn/ooc/work/gptp_ucode.hex` (1015 of 1024 words used).
- Docs: `docs/INTEGRATION.md:536` "Grandmaster synchronization", `:302`;
  `docs/HDL_DEVELOPER.md:137`; `docs/TEST_DEVELOPER.md:117-119`;
  `docs/SOURCE_EVIDENCE.md` anchor moved.
- Tests: `tb/verilator/engine/sim_main.cpp` (below) and
  `tb/verilator/engine/mutants.py` (below).

Scope boundary kept: before mastership (no asCapable port yet) the #82 self
publication still carries flags gmPresent alone, so tu stays 1 there. #82's
published contract names those reset flags; changing them was not asked.

### Commit 2, #85: received pathSequence plus thisClock

- `hdl/top/KL_gptp_engine.sv:727-730` `path_append_w`/`path_trace_count_w`:
  append when the received path is nonempty and shorter than eight entries.
- `hdl/top/KL_gptp_engine.sv:981-988`: region 3 word 7 (the BTCA `take`
  staging write) publishes count + 1 and puts `rom_clock_id_w` (thisClock,
  the same configuration value #82 publishes at reset) in the slot after the
  received entries. An absent TLV stays count 0. Eight or more received
  entries publish their first eight (unchanged), which are also pathTrace's
  first eight: the eight-entry ABI cannot carry a ninth.
- Comments: `hdl/top/KL_gptp_engine.sv:118` (port doc), `:714-724`, `:972-976`;
  `hdl/ucode/gen_gptp_ucode.py:1627-1629` (address 7 comment; image unchanged).
- Docs: `docs/INTEGRATION.md:466` "Path of an elected peer";
  `docs/HDL_DEVELOPER.md:206-212`; `docs/TEST_DEVELOPER.md:120-122`;
  `docs/SOURCE_EVIDENCE.md` engine anchors re-pointed by content.
- Existing engine expectations of the received-only path now expect thisClock
  appended (e.g. `sim_main.cpp:2521`, `:2602`, `:2712`, `:2896`, `:5027`); the
  three #82 transition checks expect `{..., thisClock}`.

## New checks, their planted mutants and failing words

All arms are in `tb/verilator/engine/mutants.py`; every one is caught at head
and fails every check it names (the arm's named verdict now also covers `#84 `
and `#85 ` controls, `mutants.py:733`). Failing lines with got/exp are in
`receipts/lane-head/engine-mutants/mut-*.log`.

### #84 (grandmaster role, change of grandmaster)

| Check (sim_main.cpp) | Mutant (mutants.py) | Failing words |
|---|---|---|
| `#84 first mastership: the master flags carry sync-ok` (:1809; both passes) | becoming grandmaster clears sync-ok (:495) | `got 0000000000000007 exp 000000000000000f`; p1 255 pass `got ...06 exp ...0e` |
| `#84 takeover: its commit names thisClock with sync-ok` (:3813), the peer-to-thisClock change | same (:495) | `got 0 exp 1` |
| `#84 every master cycle publishes sync-ok` (:5198 phase 37, per-cycle grade at :627; both passes) | same (:495); a queued receipt timeout clears a master's sync-ok (:503) | `got 000000000679530e exp 0`; `got 000000000003d794 exp 0` |
| `#84 takeover: a queued receipt timeout keeps sync-ok` (:3819) | a queued receipt timeout clears a master's sync-ok (:503) | `got 1 exp 2` |
| `#84 takeover: the queued receipt timeout commits after it` (:3817) | the receipt timeout publishes nothing (:509) | `got 0 exp 1` |
| `#84 takeover: nothing commits while dispatch is held` (:3801) | dispatch ignores a busy serializer (:516, RTL) | `got 127 exp 126` (hex) |
| `#84 master cycles were graded` (both passes) | mastership never publishes the master bit (:520) | `got 0 exp 1` |
| `#84 every handover to a peer grandmaster clears sync-ok` (both passes), the thisClock-to-peer change | a handover to a peer keeps sync-ok (:525) | `got 10 exp 0`; p1 255 `got 2 exp 0` |
| `#84 the run hands mastership to a peer` | a winning peer's grandmaster is not published (:384, list extended) | `got 0 exp 1` |

The takeover case (phase 19, `sim_main.cpp:3781`) stalls a Pdelay response so
the degrading Announce waits until the 375 ms Sync receipt watch has expired:
the timeout's event is then queued behind BECOME's, which is the race the
`prog_leg_srto` change closes.

### #85 (direct and multi-hop grandmaster)

New phase 8n `append_thisclock_to_each_received_path` (`sim_main.cpp:2433`,
probe `:2464`) and whole-run phase 38 (`:5221`); expected paths are written out
literally.

| Check | Mutant (mutants.py, RTL) | Failing words |
|---|---|---|
| `#85 direct grandmaster: count`, `: tail 1`, `: its commit names the grandmaster and path` ([GM] gives [GM, thisClock]) | the received path is published without thisClock (:532) | `count got 1 exp 2`; `tail 1 got 0 exp 02a1b2fffec3d4e5` |
| `#85 multi-hop grandmaster: count`, `: tail 5`, `: its commit ...` (four bridges: [GM,B1,B2,B3,SRC] gives six entries, thisClock last) | same (:532) | `count got 5 exp 6`; `tail 5 got 0 exp 02a1b2fffec3d4e5` |
| `#85 seven received entries: count`, `: tail 7`, `: its commit ...` | same (:532); seven received entries leave thisClock out (:571) | `count got 7 exp 8`; `tail 7 got 0 exp 02a1b2fffec3d4e5` |
| `#85 every peer path ends with thisClock` (both passes) | same (:532); thisClock lands one slot early (:578); the appended entry is the announcing source (:595) | `got 169 exp 0`; p1 255 `got 30 exp 0` (hex) |
| `#82 peer wins / warm reset: the live peer / Pdelay loss: once capable` (expect `{..., thisClock}`) | same (:532) | listed and failing in the same run |
| `#85 absent path: count`, `: its commit ...` | thisClock is appended to an absent path (:558) | `count got 1 exp 0` |
| `#85 eight received entries: count`, `: its commit ...` | eight received entries take a ninth (:564) | `count got 9 exp 8` |
| `#85 direct grandmaster: tail 1`, `#85 multi-hop grandmaster: tail 5` (identity) | the appended entry is the announcing source (:595) | `got 00e5e5fffe000001 exp 02a1b2fffec3d4e5` |
| `#85 direct grandmaster: tail 2..7`, `#85 multi-hop grandmaster: tail 6, 7` | thisClock fills every later slot (:584) | `got 02a1b2fffec3d4e5 exp 0` |
| `#85 multi-hop: tail 1..4`, `#85 seven: tail 1..6`, `#85 eight: tail 1..7` | the received entries are not copied (:601) | e.g. `tail 1 got 0 exp 00e6e6fffe0000b1` |
| `#85 peer commits with a path were graded` (both passes) | every received path is published empty (:622) | `got 0 exp 1` |
| `#85 <probe>: elected` | a winning peer's grandmaster is not published (:384, list extended) | caught |
| `#85 <probe>: the degraded grandmaster yields` | the self publication keeps the departed grandmaster (:401, list extended) | caught |
| `adopt appends thisClock as path tail 4`, `worse ... tail 4`, `parent refresh appends thisClock`, `unknown before path ... tail 3`, `post-release C appends thisClock` | the received path is published without thisClock (:532) | listed there |

Not armed, recorded in `mutants.py:46`: an absent path's tail words. The
engine's own simulation assertion stops the run on count zero with a nonzero
tail, so such a mutant aborts (measured: `$error` stops the model) and an
abort is not a catch; the absent probe grades its count and commit instead.

### Existing arms changed

- Removed: "becoming grandmaster keeps sync-ok" (it planted what #84 now
  requires); its inverse is the first #84 arm above.
- Re-pointed to moved text, still caught: "a receipt timeout unlocks the servo"
  (:265, made word-neutral for the packer), "becoming grandmaster unlocks the
  servo" (:273), "mastership sets the microcode's presence bit" (:488).

## Base and head records (repository gates)

Every target of the Makefile's `all` recipe, one by one, plus the OOC
clock-order selftest; all rc 0. Receipts: `receipts/lane-base/`,
`receipts/lane-head/`.

| Gate | Base 43acfbcc | Head 53ac2e9d |
|---|---|---|
| `make contract` | rc 0, PASS | rc 0, PASS |
| `make lint` | rc 0 | rc 0 |
| `make docs` (incl. diagrams-check) | rc 0, 20 exact evidence | rc 0, 20 exact evidence |
| `make diagrams-check` | rc 0 | rc 0 |
| `syn/ooc/check_ooc_clock.py --selftest` | rc 0 (30 arms) | rc 0 (30 arms) |
| `make -C tb/verilator/ucpu` | rc 0, 768/768 | rc 0, 768/768 |
| `make -C tb/verilator/parser` (run + mutants) | rc 0, 337/337, 9/9 | rc 0, 337/337, 9/9 |
| `make -C tb/verilator/engine run` (4 passes) | rc 0, 1642 x3, 46 | rc 0, 1703 x3, 53 |
| engine mutation arm | 58/58 caught, 20 controls pass | 72/72 caught, 24 controls pass |
| `make -C tb/verilator/gaskets` | rc 0, 81/81, 5/5 | rc 0, 81/81, 5/5 |
| `make -C tb/tsngen` | rc 0, 288/288, 4/4 | rc 0, 288/288, 4/4 |
| `make -C bench/arty test` | rc 0 | rc 0 |

`make ooc` needs Vivado, absent here; not run at either revision.

## Parent consumer gate table (scratch-parent, committed local snapshots)

Parent milan-fpga dev `e9cbb676`, submodules initialised at their pins; the
gptp-processor gitlink set and committed locally (never pushed): base snapshot
`f3379118` (gitlink 43acfbcc), head snapshot `0edefe5d` (gitlink 53ac2e9d),
adoption snapshot `28e1085f` (gitlink 53ac2e9d plus the companion patch).
Commands from the manager template, same PATH shape and VERILATOR_ROOT.
Receipts: `receipts/parent-base/`, `receipts/parent-head/`,
`receipts/parent-adoption/`.

| # | Gate | Base | Head | Adoption (head + companion) |
|---:|---|---|---|---|
| 1 | `scripts/check_cpp_idiom.py` | rc 0 (multi-declarator 0 <= 0, long function 0 <= 0) | rc 0 (same) | rc 0 (same) |
| 2 | `scripts/check_py_idiom.py` | rc 0 (over-long line 0 <= 0, long function 9 <= 9) | rc 0 (same) | rc 0 (same) |
| 3 | `scripts/xvlog_gate.py --check` | rc 0 (no Vivado: skip marker; pins proved) | rc 0 (same) | rc 0 (same) |
| 4 | `scripts/check_rtl_source_lists.py` | rc 0 | rc 0 | rc 0 |
| 5 | `sw/builder/test_builder.py` (2 legs + union) | rc 0 + rc 0, union pass, 103 gates once, 1 NOT RUN (gate 11, hardware build tree) | rc 0 + rc 0, union pass, same digest `8800c441...` | rc 0 (1082 s) + rc 0 (335 s), union pass, same digest `8800c441...` |
| 6 | `make -C tb/verilator/gptp_shadow -j8` | rc 0, 309/309, RESULT: PASS | **rc 2, 305/309**: lines 891, 930, 943, 1003 above | rc 0, 310/310, mutation arm `controls: 9 failures: 0`, RESULT: PASS |
| 7 | `scripts/check_port_contracts.py` | rc 0 | rc 0 | rc 0 |
| 8 | `scripts/measure_naming.py --check` | rc 0 | rc 0 | rc 0 |
| 9 | `scripts/measure_test_evidence.py --check` | rc 0 | rc 0 | rc 0 |
| 10 | `scripts/docs_check.py` | rc 0 | rc 0 | rc 0 |
| 11 | `scripts/lint_rtl.py --check` | rc 0 | rc 0 | rc 0 |

Adoption: **11/11 rc 0** (`receipts/parent-adoption/rc.txt`,
`receipts/parent-adoption/builder/union.txt`).

## Method notes and deviations

- `test_baremetal_profile_contract` (builder leg 0) took 1087 s at base and
  1263 s at head, more than one foreground command allows, and it is one
  indivisible parent gate. It ran as a background job while the session
  polled in the foreground until it finished; every other command ran in the
  foreground. Leg 1 (the other 102 gates) ran in the foreground (478 s).
  The adoption snapshot ran the same way: leg 0 took 1082 s in the
  background, and nothing else ran in that checkout meanwhile. Leg 1 took
  335 s in the foreground.
  Legs follow the parent's own measured partition; the parent's
  `ci_builder_legs.union()` judged them (`builder/union.txt`).
- The engine mutation arm ran as 24 parallel slices of the repository's own
  `mutants.py` functions (each slice repeats the unmutated control), because
  the sequential arm exceeds one foreground command.
- Temporary files: the lane base gates and the base snapshot's leg 0 used the
  tools' default temporary directory; all other cited runs used the lane's
  scratch (TMPDIR).
- History, never pushed: the two commits were first `f66363d`/`07bbca6`. A
  125-column comment line (parent Python idiom ratchet) and a
  multi-declarator line (parent C++ idiom ratchet) were found by the parent
  gates and fixed by amending; intermediate SHAs `7ae95e6` and these are
  superseded and not cited.
- The head snapshot's tsn-c-stack checkout was cloned from the local scratch
  parent; its origin URL was set to the canonical one so the parent's
  receipt identity check accepts it (same pinned commit).
- The parent was never pushed; its only commits are the local gitlink
  snapshots named above and the adoption snapshot `28e1085f`. Every
  Round 1b run used the lane's scratch as TMPDIR.
- Receipt scrubbing: the `parent-c` checkout (head and adoption snapshots)
  is now `<parent-c-checkout>`. `receipts/parent-head/06.log` was rescrubbed
  from its scratch log, because the earlier rules had rendered that path as
  `<parent-base-snapshot>-c`.

## Open points for review

- Received paths of eight or more entries still publish their first eight,
  without thisClock: the eight-entry ABI is the parent's, and widening it
  would be a port change (STOP condition 5).
- The pre-mastership self publication (no asCapable port) keeps tu = 1. If
  the owner wants tu = 0 there too, that changes #82's reset flags.

## Comments posted on #84

- STOP: `issuecomment-6259142231` (2026-10-19T03:40Z); its text is `receipts/stop-comment.md`.
- REVIEW READY: `issuecomment-6259550165` (2026-10-19, after the ruling), head
  `53ac2e9d75ceb381c2d2b04854e760304d9ae43f`; its text is
  `receipts/review-ready-comment.md`.
