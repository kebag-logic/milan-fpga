# #936 round 1 handoff ([A793])

Lane `936-stream-notice` on dev-soft-core `70f4056f`. Nothing pushed; the manager pushes and opens the PR.

Public record on #936: TAKEN issuecomment-6932988493; STOP issuecomment-6935670442 (02:05); the manager's ruling
issuecomment-6938589620 (04:42: the `backlog-owed` rows are the base's seven held-egress rows, graded by the egress
ledger, not a STOP; continue to REVIEW READY). REVIEW READY posted: issuecomment-6953386992 (head `7cfb8a04`), text
in `comments/REVIEW-READY.md`. Three author comments in all; nothing pushed.

Two host restarts cut the round: about 05:40 (resumed 05:43) and the owner's maintenance 07:25-08:00 (resumed about
08:14). After each, every sub-unit without a recorded rc was treated as cut: its half-written output removed and the
job re-run. Details of the second resume, including a CPU-booking correction, under [Restarts](#restarts).

## Commits

| Commit | What |
|---|---|
| `d3c528fc` | firmware: SRP records each STREAM_OUTPUT declaration change, the composition raises its GET_STREAM_INFO notice; unit tests; 11 SRP + 4 AECP plants |
| `428f125d` | twin: `stream-output-0-notices` deleted, `stream-output-0-dest-mac` owed row, `output-notice-dropped` plant, `vanished-owed` re-aimed |
| `feaf5d9a` | docs: SRP, AECP and twin READMEs |
| `3f253fd4` | twin Makefile comment: twenty-one plants |
| `73e30fb2` | ledger: `ctrl_plat` +64 B at both two-interface points; the size fixture's `8x8-two-interfaces` entry 59.0 -> 59.5 (owner's loose block-RAM decision) |
| `77c1aad7` | fix found by the final-head gates: the attach clears `srp_noticed` (a recomposition kept a stale record); two insertions in `declare_sources` moved so three existing SRP plants keep their anchors (no behaviour change); new plant `talker-notice-kept-across-a-recomposition` |
| `f3be8e69` | fix found by the final-head SRP campaign: my plant table's constant `MOVED` shadowed the existing test-name constant `MOVED`, so two existing plants ran 0 tests (escaped); renamed `NOTICE_MOVED` |
| `b496c99e` | fix found by the final-head docs job: the test-evidence ratchet (`scripts/measure_test_evidence.py`) read the dest-MAC row's cause text `hdl/milan/...` as a DUT-source path and flagged `twin_compare.py` as an unexplained DUT reader; the cause now names the file, generate block and selector without the path |
| `7cfb8a04` | fix found writing this handoff: `SPLIT_CONTROL_MEMORY.md` (section 3 and the "At #936's head" table) and the fixture entry's reason in `ctrl_memory.py` stated `73e30fb2`'s image sizes, 8 B short of the final image's at most points since `77c1aad7`'s attach clear (every-port 127,124 -> 127,132 B), and missed that `valid-destinations` (126,992 B) is past 59.0 too; the sram sentence now reads 0 to 64 B. The reason is the `Ledgered.owed` string, which nothing reads |

**Final head: `7cfb8a04`.** `77c1aad7..7cfb8a04` changes `srp_talker_mutants.py`, `twin_compare.py` text,
`SPLIT_CONTROL_MEMORY.md` and the unread `owed` string in `ctrl_memory.py`: no image input. The gates ran at
`b496c99e`. Re-run at `7cfb8a04`: the docs jobs, firmware-unit, the twin, and elaborate's builder legs and LiteX
aggregate (`test_ctrl_memory`). The release, platform and fixture images are rebuilt and compared by hash.

## Spec decision

The notice is obliged.

- Milan v1.2 5.4.5.2 and Table 5.22: GET_STREAM_INFO's unsolicited triggers for a Stream Output include its "MSRP
  Talker attribute declaration state", the MSRP failure code and bridge ID, the Stream ID, destination MAC and VLAN ID.
- IEEE 1722.1-2021 7.5.2 ties "MSRP Talker Advertisements or Failures" to GET_STREAM_INFO notices.
- Milan v1.2 5.4.5.1: the notice goes to every registered controller.
- The release processor sends one at each Talker declaration and withdrawal
  (`protocol-processor/hdl/top/protocol_processor_top.sv:3679-3684`). The split sent none: no firmware caller passed
  STREAM_OUTPUT (type 6) to `aecp_changed`.
- The issue's "7.4.40" is GET_AVB_INFO in the 2021 edition; GET_STREAM_INFO is 7.4.16. Recorded in the PR body.

## Changes (file:line at `7cfb8a04`)

- `sw/firmware/ctrl/srp/srp_mbx.h:84-91`: `shown`, `shown_advertise`, `noticed`, `shown_vid` in `struct srp_interface`.
  Why: the adapter must compare what TALKER_DECL now publishes against what the STREAM_OUTPUT last showed.
- `sw/firmware/ctrl/srp/srp_mbx.c:342-355` (`declare_sources`, after `mbx_pub_talker_decl`): a source is recorded in
  `noticed` when declared or withdrawn, when still declared with its type swapped Advertise/Failed (once lwSRP made the
  swap), or when still declared on another VID (an adopted Domain's). A reset that declares an unchanged source again
  records nothing; a failed creation returns before this, so it records once it succeeds. Why: Table 5.22's
  declaration-state, failure and VLAN triggers, from where the declaration changes.
- `sw/firmware/ctrl/app/ctrl_app.h:100-101`, `ctrl_app_srp.c:66-67` (delivery takes and clears each interface's record
  into `ctrl_app.srp_noticed`), `ctrl_app_srp.c:141` (attach clears it). Why: the AECP bridge reads one record, and a
  recomposed application keeps none of an earlier SRP instance's.
- `sw/firmware/ctrl/app/ctrl_app_aecp.c:206-214`: the bridge raises `aecp_changed(core, 6, n, 1)` (STREAM_OUTPUT n,
  STREAM_INFO) for each recorded source and clears the record. Why: AECP's existing notice path and its pacing (THE
  RETRY) send it to every registered controller; no new path or pacing.
- Tests: `srp_talker.cpp:631` `DeclarationAndWithdrawalAreNoticed`, `:659` `TypeSwapIsNoticed`, `:705`
  `AdoptedDomainVidIsNoticed`, `:722` `ResetNoticesNothingUnchanged`; `srp_gate.hpp:349`
  `SrpGate.F936AProbeAndItsExpiryEachNoticeTheSource` (a real PROBE_TX through MAAP's DA gate and its 15 s expiry,
  over a poisoned record); `test_aecp.cpp:754` `App.SrpDeclarationChangeIsItsStreamOutputsNotice`.
- Plants: `srp_talker_mutants.py` `notice_defects()`, 12 `talker-notice-*` (declaration-missed, withdrawal-missed,
  record-dropped, every-declared-source, swap-missed, refused-swap-noticed, vid-missed, vid-on-every-domain,
  reset-forgets-what-was-shown, not-taken, kept-across-a-recomposition, record-kept), in both SRP campaigns;
  `aecp_mutants.py` 4 `app-output-notice-*` (dropped, as-an-input, next-source, kept). Each must be caught by its
  test's words.
- Twin (`tb/verilator/milan_dp/`): `stream-output-0-notices` deleted (the split now sends the fabric's four notices of
  STREAM_OUTPUT 0 at the same changes to the same controllers); `stream-output-0-dest-mac` owes the one byte group that
  still differs (the finding); capture plant `output-notice-dropped` (the defect back); `vanished-owed` re-aimed at
  the new row; Makefile, README.
- Ledger (`73e30fb2`): `ctrl_plat` 19,136 / 20,416 B at 1x1/2if and 8x8/2if; the size fixture's `8x8-two-interfaces`
  entry 59.5 RAMB36, by #665 issuecomment-6892332745 (an image past its entry raises it at the next half tile, as
  S14 debt). Docs: `SPLIT_CONTROL_MEMORY.md` sections 3 and 5, `MARK_II_AREA_PLAN.md`, the budget README.

No RTL, mailbox-contract or CPU-budget-bound change.

## Images (at `b496c99e`; identical at `7cfb8a04`, by hash)

- Release image byte-identical to the base: `bios.bin` 1x1 `860d4771…`, 8x8 `d8851b6d…`; disassembly and the
  debug-stripped ELF identical; the whole ELF differs in debug sections only (receipt `final/images/`).
- Split product ROM banking unchanged (1x1/1if 64+32+16+4 KiB, 8x8/1if one 128 KiB bank): no route owed.
- `plat_ledger.py` PASS: 1x1/1if 117,688 B 43 RAMB36; 1x1/2if 119,296 B 44; 8x8/1if 130,384 B 56; 8x8/2if
  131,968 B 60.5. `ctrl_plat` 17,536 / 19,136 / 18,240 / 20,416 B.
- Size fixture (rom / sram / RAMB36): 1x1/1if 112,624 / 55,216 / 41.0; 1x1/2if 114,208 / 57,408 / 42.5; 8x8/1if
  125,280 / 96,320 / 55.0; 8x8/2if 126,824 / 113,280 / 59.0; every-port arm 127,132 rom, 59.5; valid-destinations
  arm 126,992 rom, 59.5. Both arms are past 59.0 (126,976 B) and inside 59.5.

## Harness

The CPU service-budget harness on the final image, CPU 100 MHz on sys, bus 100 MHz. Arm A's builds are of `77c1aad7`, and
their `ctrl_app.elf` equals `7cfb8a04`'s by sha256. The variant arms ran on clean clones of `b496c99e`, which
`7cfb8a04` changes no image input of (every fixture and ledger image identical, by sha256). Arm A's groups were run in parts across the two restarts; each complete part's
script and log are graded together by `run.py --reuse-build --regrade` over one directory of all groups.

| Run | Result |
|---|---|
| arm A, 1x1/1if, 96 groups | 0 refusals; 7 budget misses, the seven held-egress rows (below); 0 of 130,941 work passes over the 2 ms share; no `STATED` line (the stated costs hold); 0 save misses |
| arm A, 8x8/1if, 95 groups | 0 refusals; 7 budget misses, the seven held-egress rows; 0 of 263,828 passes over the share; `STATED` lines: polls base (77, at most 24,541 against 22,500), ACMP item (3, at most 7,030 against 5,500), declined ACMP offer (4, at most 2,380 against 2,000), the 1x1/1if stated costs this point reports past (`ctrl_service_budget/README.md`); the base's `backlog-owed` group reports the same two kinds |
| egress ledger, 8x8/1if (PR #914's tool at `8883d499`) | PASS: all seven rows within their figures, 0.136 to 0.314 ms to spare; no new budget miss. The base passes too |
| `answering-later`, 1x1/1if and 8x8/1if | 8 groups each, 0 refusals, 0 misses; the retried notice committed 7.899 to 8.301 ms (1x1) and 7.798 to 8.246 ms (8x8) after its port's answer, bound 20 ms |
| `answering-every-port`, 1x1/1if | 16 groups, 0 refusals, 0 misses; 192 notices committed 1.856 to 27.073 ms after their port's answer, bound 140 ms. At 8x8/1if the arm refuses the point by name at this base |
| `valid-destinations`, 1x1/1if | 2 groups, 0 refusals, 0 misses; the Talker declare rows 0.658 and 186.953 ms, the withdraw 189.315 ms, bound 220 ms |
| `valid-destinations`, 8x8/1if | 2 groups, 0 refusals, 0 misses; the nine Talker declare rows at most 189.423 ms, the withdraw 170.374 ms, bound 220 ms. `STATED` reports: build-one passes 81,473 to 92,226 CPU cycles against the 1x1/1if 73,500; THE RETRY's refused-attempt rounds 11,922 to 12,537 against 11,900; one tier-2 slice of THE TRANSMIT's build, 92,226, against THE TIERS' 90,000. The base (`70f4056f`, the same arm) reports the tier-2 slice (91,604) and build-one passes (18, 81,352 to 91,604) too, and no refused-attempt round (its longest round 2,174). The rounds are new: THE RETRY attempting the new STREAM_OUTPUT notices' GET_STREAM_INFO, refused because this arm's fixture leaves the gather window unanswered (`aecp_face.c` `gsi`), retried at AECP's backoff. At 1x1/1if the same rounds are at most 9,015, within 11,900. `receipts/final/budget/vd-8x8-1if-vs-base.md` |

The seven held-egress rows against the base, each the harness's own grade of `backlog-owed` (the base run with
`--groups backlog-owed` on a clean clone of `70f4056f`): at 8x8/1if, -0.006 to +0.066 ms, inside the ledger. At
1x1/1if, which has no ledger (`egress_ledger.py` refuses the point), +0.132 to +0.151 ms: the service behind the 60 ms
hold grows 3.6 to 8.7 %. Table: `receipts/final/budget/held-egress-vs-base.md`. Per the ruling these are the base's
rows, graded by the ledger; the 1x1 growth is reported, not graded.

No harness group registers a controller while its Talker declares, so no row times the new GET_STREAM_INFO notice of
a STREAM_OUTPUT itself: its record's cost is inside the SRP rows' passes (`valid-destinations`, arm A's `srp`), and
it is sent by AECP's notice path, which the notice rows time.

## Gates at `b496c99e` (clean clones)

Every job replayed step by step on its own fresh clone of `b496c99e` (`run_wf.py`). Each `run:` step has rc 0 or a
stated reason for not running; the reasons are tool installs this host already has, and the hosted step-context
recorders. Verified by `verify_sel.py`; tables in `receipts/final/workflows/`.

| Gate | Result |
|---|---|
| rtl-fast `firmware-unit` | PASS. Control-plane firmware suites and RV32 builds, saved-state store (526 tests, 5 shapes), `fw_coverage.py --check`: PASS (39 files) |
| rtl-fast `firmware-srp-mutants` | PASS, both SRP campaigns: 445 defects caught, none escaped; all 12 `talker-notice-*` in each campaign caught by their tests' words |
| rtl-fast `firmware-aecp-mutants` | PASS: 303 caught, none escaped; the 4 `app-output-notice-*` caught by `App.SrpDeclarationChangeIsItsStreamOutputsNotice` |
| rtl-fast `firmware-control-mutants` | PASS: 716 of 716 caught |
| rtl-fast `firmware-boundary`, `firmware-verilator`, `split-cdc` | PASS (10 steps rc 0) |
| docs `wire-accountability`, `docs-check-no-git`, `docs-gates-0/1/2`, `docs-check` | PASS (61 steps rc 0) |
| rtl `verilator-shards` 1, 4, 6, 10, 17 of 19 (the shards that build the split firmware: `milan_dp__0..3`, `mbx`) | PASS: 28 suites, 0 failed, 763,945 checks (shard 1: 9 suites 28,931; 4: 1, 3,634; 6: 5, 205,129; 10: 6, 3,039; 17: 7, 523,212) |
| twin (`make twin`) | 1 finding, `split-talker-failed` (PR #935's stale row); `stream-output-0-dest-mac` holds |
| twin plants (`make twin-plants`) | rc 2 only for `srp-plus-k` (ESCAPED by its stale words, PR #935's); with `TWIN_PLANTS="byte-flip missing-notification"` the 20 other plants are each refused in both runs (40 of 40), rc 0, tree clean |
| release image | byte-identical (above) |
| `plat_ledger.py`, size fixture | PASS (above) |

At `7cfb8a04` (re-run there, each on a fresh clone): the docs jobs PASS (61 steps rc 0); firmware-unit PASS
(coverage 39 files); the twin 1 finding (`split-talker-failed`, #935's), 20 plants refused both ways (40 of 40), tree
clean; the release image byte-identical to the base (`bios.bin`, disassembly and stripped ELF; the whole ELF's debug
sections carry the clone's path); the platform's 24 and the fixture's 6 image hashes identical to `b496c99e`'s;
`plat_ledger` PASS; fixture sizes identical. Elaborate's gates (new at this head, since `ctrl_memory.py` and its test
changed): the builder legs (`ci_builder_legs.py run all -- test_builder.py --require-elaboration --require-rv32`)
PASS, 2 arms not run for the test's own recorded reasons (a MAKEFLAGS mutation this make cannot carry; a calibration
report from a build tree this host has not); `run_litex_sims.sh --selftest` PASS and the aggregate 8 of 8 PASS,
`test_ctrl_memory` included. Its first run was voided: the builder legs refused on `tsn-c-stack`'s origin (the clone
tool's), and `test_soc_timing_cuts` timed out at the hosted 900 s at load 150, an unknown; re-run with each origin
restored and a 3,600 s clock.

Scratch merge with PR #935 (`32919b5f` = `b496c99e` + `37255683`, conflicts resolved as under Open risks, not
pushed): twin 0 findings; all 22 plants refused in both runs (44 of 44), `srp-plus-k`, `talker-failed-back` and
`output-notice-dropped` included; tree clean.

## Findings

- The split's declaring STREAM_OUTPUT answers `stream_dest_mac` 0 with STREAM_DEST_MAC_VALID set (RTL, no owner
  issue); in PR-BODY.md, with the twin's bytes and the cause lines in `hdl/milan/milan_datapath.sv`.
- The twin's `split-talker-failed` row and the `srp-plus-k` plant's words are stale at the base: PR #935's (#929).

## Open risks

- Lane conflicts (`git merge-tree` of `b496c99e` with each open head, 09:5x):
  - PR #935 (`37255683`): text conflicts in the twin's `Makefile`, `README.md` and `twin_compare.py`. Resolved in a
    scratch merge by keeping this PR's dest-MAC row, #935's deletion of `split-talker-failed`, and both new plants
    (twin evidence below).
  - PR #932 (`0fdfdba7`): text conflicts in the memory ledger (`sw/litex/ctrl_memory.py`, `ctrl_memory_ledger.py`,
    `test_ctrl_memory.py`, `docs/design/SPLIT_CONTROL_MEMORY.md`); whichever lands second re-measures its figures.
    Its `srp_mbx.c`/`.h` and SRP README changes merge cleanly with these.
  - PR #914 (`8883d499`): merges cleanly as text; it shares `srp_mbx.c`/`.h`, `test_aecp.cpp`, the SRP/AECP READMEs,
    the budget README and `SPLIT_CONTROL_MEMORY.md`.
- The `answering-every-port` arm refuses 8x8/1if at this base by name (the model holds 40 notices, not
  AECP_NOTICES_MOST), unchanged here.
- The held-egress rows at 1x1/1if grow 0.132 to 0.151 ms over the base's (no ledger there; reported, not graded).
  Whether 1x1/1if needs a figure is the owner's.
- New 8x8/1if `STATED` reports in `valid-destinations`: 21 THE RETRY rounds of one refused attempt, 11,922 to 12,537
  cycles against the one-interface 11,900 (none at the base; at 1x1/1if within, at most 9,015). Reported like the
  point's other costs past the one-interface ones; whether 8x8/1if's round needs its own figure is #894's (the 8x8
  owner's).
- No harness row times the new STREAM_OUTPUT notice itself (no group registers a controller while its Talker
  declares); a dedicated row would be a harness change outside #936.

## Receipts

`receipts/INDEX.md` lists every file under `receipts/`, generated from the files present. The final head's evidence
is under `receipts/final/`: `workflows/` (every step log and the verification tables at `b496c99e`),
`head-7cfb8a04/` (the re-runs there), `budget/` (each arm's console, table, results summary, the egress ledger and
the base comparison), `twin/` (with the #935 merge), `images/`, `tools/` and `restarts/`. Earlier receipts, the
STOP's included, are at the top level and under `earlier/`.

## Restarts

- **First (about 05:40, resumed 05:43).** Every unit killed; every job without a recorded rc re-run.
- **Second (owner maintenance 07:25-08:00, resumed about 08:14).** Every unit killed; every sub-unit without a
  recorded rc treated as cut, its half-written output removed and the job re-run. Arm A's group logs that had
  completed with their run (`fin-*`, 30 at 1x1 and 28 at 8x8/1if) were kept; the rest re-run. The host has 96 CPUs;
  sessions use 64-95.
- **Booking.** At 08:15 the queue runner started 21 units because `cpu_ranges.py pick` answered for each: the owner's
  `pool-spill.sh` (changed 08:12, "use all processors") widens every pinned process to all CPUs each minute, so the
  picker sees no booking. I stopped 10 of them by name and capped the lane at 8 concurrent units. I briefly re-pinned
  the other 8 before finding the owner's rule, then stopped re-pinning. From 11:07 the 1-minute load gate was raised
  from 80 to 250: other lanes held the host at 150 to 240 and my arms had waited an hour at 3 of 8 units. The cap
  counted only `j-*` units at first, so one `k-*` unit ran as the ninth.
- **Replay defects found and fixed** (my scratch tools, not the repository):
  - The first shard replay ran no suite. The skip list I inherited from another lane skipped every step of
    `verilator-shards`, with that lane's reason. Voided; the shards re-run with only installs skipped.
  - The sweep and the builder legs refused on `tsn-c-stack`'s origin, which the replay and clone tools had pointed
    at the lane's module stores. Voided; each submodule's origin is now its `.gitmodules` URL.
  - The batch tool's clone cleanup would have removed a concurrent shard's clone.
  - `test_soc_timing_cuts` timed out at the hosted 900 s at load 150. Voided; re-run with a 3,600 s clock.
- Full timeline: `receipts/final/restarts/second-restart.md`.
