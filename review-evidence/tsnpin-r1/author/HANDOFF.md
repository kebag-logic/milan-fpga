# HANDOFF — [A767] tsn-c-stack pin move 70936b77 → 715589c (#665)

Status: REVIEW READY. Every gate below ran on a clean clone of the final head and is rc 0; the full sweep is 65 of 65.

- Lane: branch `tsn-c-stack-pin-715589c`, base `dev-soft-core` `1d6bf5556a` (unchanged on the remote).
- Head: `50e2a722ef2671b3f5b017f97b1c7d41705c4f32` (eight commits on the base; no merge, rebase, force or amend; nothing pushed).
- TAKEN: #665 issuecomment-6792567545.
- REVIEW READY: #665 issuecomment-6804604273 (head `50e2a722`).
- Receipts: receipts/INDEX.md, generated from the files present (host paths replaced by placeholders; files over 200 KB listed by sha256 in receipts/LARGE-FILES.md).
- Donor: kebag-logic/tsn-c-stack `main` `715589c1db7cf67e2f3259fd7083ebc7f0923376`:
  `git -C third_party/tsn-c-stack merge-base --is-ancestor 70936b77 715589c` rc 0, and `715589c` is
  `origin/main` (receipts/pin/).
- Adopted donor PRs: #29 (#27), #30, #28 (#26), #33 (#31), #34 (#32).
- Nothing inside the submodule was edited; no donor fault was found.

## Commits

| # | Commit | Subject |
|---|---|---|
| 1 | `66bc6e82` | Move tsn-c-stack to main 715589c and plant the campaign's ACMP defects on the lines it changed |
| 2 | `d504f119` | Keep an ACMP command the core declines at its owed bound and offer it again after the next poll that sends an owed frame |
| 3 | `0ca18868` | Refuse the 64-bit shift helper in the split platform's RV32I build, which no field write calls since tsn-c-stack#27 |
| 4 | `80850cd2` | Name tsn-c-stack 715589c in the submodule reference, its diagram and the firmware's links, and the helpers the size fixture now reaches |
| 5 | `1cc231a7` | Record the firmware coverage ratchet at tsn-c-stack 715589c, with the ACMP adapter's kept command covered |
| 6 | `f42198ce` | Ledger the target platform's struct at its size with tsn-c-stack 715589c, and state each split point's plan at both pins |
| 7 | `dc5ebf55` | Hold the ACMP owed frames' and kept command's plants in their own table, so acmp_mutants.py stays under the Python gate's module length |
| 8 | `50e2a722` | Name the checks the walk leaves to catch two ACMP plants: the stack's own A17 words, and C2's accesses where GET_RX_STATE marks no sink |

Commits 7 and 8 answer the gate pass itself: at `f42198ce` the Python idiom gate refused `acmp_mutants.py`
at 1044 lines ("long module 11 > ratchet 10"; Rule 12: new Python complies at once), and at `dc5ebf55` the
control campaign caught 577 of 579, two plants caught by checks other than the ones their kills name
(receipts/superseded-heads/). The final pass ran once more, whole, at `50e2a722`.

## Changes (file:line at the head, reason)

| Where | Change | Reason |
|---|---|---|
| `third_party/tsn-c-stack` | gitlink `70936b77` → `715589c1` | the pin move (#859 round 4 ruling item 1; tsn-c-stack#34 round 2 ruling item 3) |
| `sw/firmware/ctrl/test/acmp_mutants.py` (A3 `:140-:174`, A14 `:357`, A15 `:389`, A17 `:418`, A22 `:576`, A24 `:664`, C `:780`), `acmp_owed_mutants.py` (A19 `:29-:52`) and `acmp_review_mutants.py:77-:150` | 17 plants re-anchored on the stack's own `715589c` text of the same plant (`tests/mutations.json` at `715589c`, same name, same defect: the walk's `mark()` lines, `release[k / 32u]`, `respond(..., k + 1u)`, `busy_declined`, `probe_held`) | at the new pin their old text occurs 0 times; the campaign would refuse them |
| `sw/firmware/ctrl/test/acmp_owed_mutants.py:36-:41` | `acmp-full-queue-acts` kills `AcmpCore.A19AFullQueueDeclinesTheCommandBeforeItActs` ("…is declined before it changes anything") and `AcmpOwed.HeldEgressDefersTheCommandBehindTheOwedSet` ("is declined to the port, not taken") | #28 renamed the test and the defect is now a decline, not a drop |
| `sw/firmware/ctrl/test/ctrl_mutants.py:607-:616`, `:766-:768` | `ACMP_FINISH` gains the walk's `marked()` skip; `ACMP_FINISH_CLEAR` holds the marks' reset; the plant moves `publish()` after the report loop, before the reset | #32's walk-only `finish()` |
| `sw/firmware/ctrl/acmp/acmp_mbx.c:108-:128` | `on_frame` keeps a record `acmp_rx` declines (`memcpy` of `f->len` bytes, at most `MBX_CH_ACMP_MAX_FRAME_BYTES`, which `mbx_rx_take` enforces); `on_rx_ready` holds the acmp ring while one is kept | #28 port contract: keep a declined frame; deliver no later ACMP frame before it (PORTING "ACMP owed bound") |
| `sw/firmware/ctrl/acmp/acmp_mbx.c:152-:165` | `on_poll` offers the kept record again when the poll sent an owed frame (`owed_count` fell), in that pass, before the next timer service; returns `owed_count != 0` | #28: deliver it again after each accepting poll, before `acmp_timer_expired` |
| `sw/firmware/ctrl/acmp/acmp_mbx.c:197` | `ctrl_loop_set_rx_ready(l, MBX_CH_ACMP, on_rx_ready)` | the loop's existing ready hook; the service loop is not edited |
| `sw/firmware/ctrl/acmp/acmp_mbx.h:28-:52`, `:194-:195`, `:205-:217` | THE KEPT COMMAND (contract, bound n + 1 + f + r, the stated one-pass deviation, the pass accounting), `ACMP_MBX_KEPT_PASSES`, `struct acmp_mbx_kept` | the adapter's documented service figures |
| `sw/firmware/ctrl/test/test_acmp_mbx.cpp:1121-:1248` | K1, K2, K3 (below) | tests of the kept command |
| `sw/firmware/ctrl/test/acmp_owed_mutants.py:60-:103` | `acmp-poll-owes-nothing` re-anchored on the new return; eight kept-command plants | each new branch's defect |
| `sw/firmware/ctrl/test/acmp_owed_mutants.py` (new), `acmp_mutants.py:15`, `:961` | the owed frames' (A19, E1, E2) and the kept command's 16 plants, moved unchanged out of `acmp_mutants.py` and appended to its table (the same 284 plants, checked by set equality) | `scripts/check_py_idiom.py`: no new module over 1000 lines (`acmp_mutants.py` is 961) |
| `sw/firmware/ctrl/test/acmp_mutants.py:403-:406` | `acmp-timer-port-called-every-time` kills A17 on "A17 a change that leaves an interface's earliest deadline keeps its timer" | the stack's own kill for the same plant at `715589c`: #32's walk re-arms only marked interfaces, so the old words are no longer the check that fails |
| `sw/firmware/ctrl/test/acmp_review_mutants.py:224-:233` | `acmp-admit-on-every-entry`'s adapter kill moves from C1 (GET_RX_STATE) to C2 (PROBE_TX_RESPONSE) in the same test | #32: an entry admits only the sinks it marks; a GET_RX_STATE marks none, a PROBE_TX_RESPONSE marks its bound sink, whose path exceeds its access bound (receipts/superseded-heads/two-escapes-every-failing-check.log) |
| `sw/firmware/ctrl/test/plat_arms.py:111-:112`, `:157-:159` | the `platrv32` arm refuses `__lshrdi3` among the split platform's open symbols | #29's purpose (#27): no field write calls the 64-bit shift helper; the hot list that carried its entry is not on this base |
| `sw/firmware/ctrl/test/ctrl_mutants.py:276-:283`, `:910`; `ctrl_mutant.py:18` | plant `wire-put-be-shifts-64-bits` (the `70936b77` per-byte `wire_put_be`), the campaign's `platrv32` arm, `WIRE_H` | the check's planted defect |
| `docs/reference/SUBMODULES.md:27`, `:544-:555`, `:587-:589`, `:597`, `:642`; `docs/diagrams/submodule_boundaries.{drawio,svg,png}`, `PNG_MANIFEST.json` | pin row, adoption table (29, 30, 28, 33, 34), pin sentence; diagram regenerated by `submodule_boundaries.gen.py` | docs naming the old pin |
| `docs/design/MAILBOX_SPLIT.md:122`, `:338`, `:535`, `:583-:587`; `sw/firmware/ctrl/README.md` (8 links, `:328`, `:690-:693`); `sw/firmware/ctrl/maap/README.md:19`; `sw/firmware/gtest/README.md:246-:299` | stack links at `715589c`; the kept command in the adapter row and the ACMP section; the size fixture's helpers (452 B, no `__lshrdi3`, measured) | docs naming the old pin, and the adopted behaviour |
| `sw/firmware/gtest/coverage.ratchet` | written by `fw_coverage.py --write`: `acmp_mbx.c` 93/93, 36/36; `acmp.c` 847/847, 436/436; `wire.h` 14/14; `ctrl_app_aecp.c` 165/165 | the generator's measurement at the pin (the `ctrl_app_aecp.c` line is this host's gcov: the base measures 165 too, receipts/coverage/) |
| `sw/litex/ctrl_memory.py:217`, `sw/litex/ctrl_memory_ledger.py:26`, `docs/design/SPLIT_CONTROL_MEMORY.md:97` | `ctrl_plat` sizes 18,584 / 20,072 / 19,240 / 21,384 (were 18,432 / 19,928 / 19,088 / 21,240) | the platform's override is keyed on `sizeof(struct ctrl_plat)`, which the pin and the kept record grow; at the old key the head's 8x8/2if platform image is refused by name |
| `docs/design/SPLIT_CONTROL_MEMORY.md:296-:310` | both images' plans at both pins | the ROM/RAM ledger of the pin move |

## New checks (planted mutant, failing words)

Each was planted in a scratch campaign at a snapshot of the change, and the full control campaign at the final head caught 579 of 579.

| Check | Plant | Failing words |
|---|---|---|
| K1 `AcmpMailbox.K1ACommandDeclinedAtTheOwedBoundIsKeptAndAnsweredInArrivalOrder` | `acmp-kept-dropped` (`acmp_rx(...) \|\| true`: a declined record dropped) | "K1 the first command behind the full owed set is declined once and kept, the second left in the ring" (and K2's "declined, binds nothing and is kept") |
| K1 | `acmp-kept-passed` (ready hook always true) | "…the second left in the ring" |
| K1 | `acmp-kept-never-offered` (`&& false` on the re-offer) | "K1 the kept command is answered in pass ACMP_OWED_MAX + 1 after the room returns" |
| K1 | `acmp-kept-after-it-is-taken` (the clear dropped) | "K1 the command kept behind it in pass n + 1 + f, f = 1: the response ahead of it" |
| K1 | `acmp-kept-offered-on-a-refused-poll` (`owed_count < owed \|\| true`) | "K1 the first command behind the full owed set is declined once and kept" |
| K1 (acmpif2, two interfaces) | `acmp-kept-on-interface-zero` | "K1 on the interface it arrived on" |
| K2 `AcmpMailbox.K2ABindDeclinedAtTheFullSetWaitsForTwoSlotsAndLosesNoProbe` | `acmp-kept-dropped-when-declined-again` | "K2 offered again after the first send, one slot free: declined again and still kept" |
| K3 `AcmpMailbox.K3AStartDropsTheKeptCommand` | `acmp-kept-survives-a-start` (`memset` short of `kept`) | "K3 a start keeps no command from the run before" |
| E1 (existing) | `acmp-poll-owes-nothing` re-anchored | "E1 nothing reported yet, and the loop does not sleep while frames are owed" |
| `platrv32` arm | `wire-put-be-shifts-64-bits` (the per-byte `wire_put_be` of `70936b77`) | "the split platform calls __lshrdi3, the 64-bit shift helper (tsn-c-stack#27)" |
| the platform's override at 8x8/2if | the old key, `ctrl_plat` 21,240 (the image at the head) | "allocation over budget: the override 'platform-8x8-two-interfaces' is for the target platform's 8x8, two interfaces image alone, the one carrying {'nvm_stage': 13264, 'ctrl_plat': 21240}; this image carries {'nvm_stage': 13264, 'ctrl_plat': 21384}" |

Scratch subset campaigns (receipts/scratch-campaigns/): the nine adapter plants 9 of 9 caught (two first
escaped because the plant did not compile under `-Werror`; their text was fixed, then 2 of 2); the 18
re-anchored plants 18 of 18; `wire-put-be-shifts-64-bits` 1 of 1.

## Parent consumer bar at the moved pin

| Gate at `50e2a722` | Result (from its log) |
|---|---|
| `firmware-unit` | every step rc 0: `tally_selftest.py`, `fw_rv32_selftest.py --require-rv32`, `test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4` PASS, `test_ctrl_nvm.py --require-rv32`, `fw_coverage.py --selftest` and `--check` ("firmware coverage: PASS (35 files)") |
| `firmware-control-mutants` (`--shard 1/4`) | "mutants: 579 of 579 caught"; `test_ctrl_firmware: PASS` |
| `firmware-aecp-mutants` (`--shard 2/4`) | `test_ctrl_firmware: PASS` |
| `firmware-srp-mutants` (`--shard 3/4`) | 280 `[ok]` lines, both pin controls; `test_ctrl_firmware: PASS` |
| `firmware-boundary` (LiteX venv) | "ctrl_boundary: 3258 compiled sources of 3506 recorded invocations … PASS" |
| `firmware-verilator` (LiteX venv) | "ctrl_boundary: 1019 compiled sources of 1127 recorded invocations … PASS" |
| `test_ctrl_firmware.py --require-rv32 --self-test` | its four shards above, all PASS |
| `fw_coverage.py --check` | PASS (35 files, every one 100 % after the exclusions) |
| image ROM/RAM ledger | above: no point's plan moves |

The S2 harness, `test_builder.py`, `behave` and `git diff --check` are in the gate table.

## ROM/RAM ledger (1x1, 8x8, 32x32) against 70936b77

Planned by `ctrl_memory.plan`, each pin's image linked with one runtime (`runtime_ssp.py`), at
dev-soft-core `1d6bf555` (pin `70936b77`) and with the move (receipts/ledger/).

The size fixture (`ctrl_srp_image.py --with-aecp --layout split`):

| Point | text B (70936b77 -> 715589c) | `rom` need B | `sram` need B | `rom` banks | `sram` banks | RAMB36 equivalents | `rom` left before its next granule | `__lshrdi3` |
|---|---:|---:|---:|---|---|---:|---:|---|
| 1x1, one interface (shipping) | 92,200 -> 92,600 (+400) | 104,456 -> 104,856 (+400) | 46,272 -> 46,416 (+144) | [65536, 32768, 8192] -> [65536, 32768, 8192] | [32768, 8192, 4096, 2048] -> [32768, 8192, 4096, 2048] | 37.5 -> 37.5 | 2,040 -> 1,640 | defined -> absent |
| 1x1, two interfaces | 93,784 -> 94,152 (+368) | 106,040 -> 106,408 (+368) | 57,648 -> 57,792 (+144) | [65536, 32768, 8192] -> [65536, 32768, 8192] | [32768, 16384, 8192, 2048] -> [32768, 16384, 8192, 2048] | 40.5 -> 40.5 | 456 -> 88 | defined -> absent |
| 8x8, one interface | 92,316 -> 92,708 (+392) | 118,176 -> 118,568 (+392) | 86,848 -> 86,992 (+144) | [65536, 32768, 16384, 4096] -> [65536, 32768, 16384, 4096] | [65536, 16384, 4096, 2048] -> [65536, 16384, 4096, 2048] | 50.5 -> 50.5 | 608 -> 216 | defined -> absent |
| 8x8, two interfaces (ledgered 57.5) | 93,976 -> 94,356 (+380) | 119,832 -> 120,216 (+384) | 113,008 -> 113,152 (+144) | [65536, 32768, 16384, 4096, 2048] -> [65536, 32768, 16384, 4096, 2048] | [65536, 32768, 16384] -> [65536, 32768, 16384] | 57.5 -> 57.5 | 1,000 -> 616 | defined -> absent |

The target platform (`ctrl_plat_image.py`, against the split SoC exports of S2's runs at 1x1 and 8x8):

| Point | Platform `rom` need B (70936b77 -> 715589c) | `sram` need B | `rom` banks | `sram` banks | RAMB36 | `ctrl_plat` B | `__lshrdi3` |
|---|---:|---:|---|---|---:|---:|---|
| 1x1_tdm8-if1 | 109,560 -> 109,920 (+360) | 47,168 -> 47,328 (+160) | [65536, 32768, 8192, 4096] -> [65536, 32768, 8192, 4096] | [32768, 16384] -> [32768, 16384] | 39.0 -> 39.0 | 18,432 -> 18,584 (+152) | defined -> absent |
| 1x1_tdm8-if2 | 111,200 -> 111,504 (+304) | 58,592 -> 58,736 (+144) | [65536, 32768, 8192, 4096, 2048] -> [65536, 32768, 8192, 4096, 2048] | [32768, 16384, 8192, 2048] -> [32768, 16384, 8192, 2048] | 42.0 -> 42.0 | 19,928 -> 20,072 (+144) | defined -> absent |
| 8x8-if1 | 123,304 -> 123,672 (+368) | 87,760 -> 87,904 (+144) | [65536, 32768, 16384, 8192, 2048] -> [65536, 32768, 16384, 8192, 2048] | [65536, 16384, 4096, 2048] -> [65536, 16384, 4096, 2048] | 52.0 -> 52.0 | 19,088 -> 19,240 (+152) | defined -> absent |
| 8x8-if2 | 125,048 -> 125,360 (+312) | 113,936 -> 114,080 (+144) | [65536, 32768, 16384, 8192, 4096] -> [65536, 32768, 16384, 8192, 4096] | [65536, 32768, 16384] -> [65536, 32768, 16384] | 59.0 -> 59.0 | 21,240 -> 21,384 (+144) | defined -> absent |

- **No point's RAMB36 plan moves** at either image: every bank is the one it was at `70936b77`, so no STOP.
- Code size against `70936b77`: `rom` +368 to +400 B (fixture), +304 to +368 B (platform); `sram` +144 B
  (+160 at the platform's 1x1/1if); `struct ctrl_plat` +144 to +152 B. The size fixture of `ctrl_image.py`
  (RV32I, `--base 1d6bf555`): text +652 B, bss +144 / +160 B; helpers 452 B with no `__lshrdi3`.
- **The +132 B over-granule ROM effect** #34's PR body names is the 8x8/2if `answering-every-port` arm of
  S2b's harness (issuecomment-6778599191 item 5). That arm is not on `dev-soft-core`, so it cannot be
  measured here; S2b owes it at its sync onto this pin. On this base the tightest margin is the fixture's
  1x1/2if, 88 B of `rom` before its next granule (456 B at `70936b77`).
- **32x32:** no 32x32 shape on `dev-soft-core` (no config, no ledger point); S15 adds it and rebuilds its
  image on this pin (#859 round 4 ruling item 1). The stack's walk and mask widths at 32 sinks are the
  stack's own tests (`AcmpWalk`, `acmp_wide`), in tsn-c-stack's CI at `715589c`.
- The platform's 8x8/2if override was keyed on `ctrl_plat` 21,240 B; at the head that image carries
  21,384 B, and `ctrl_plat_image.py` refuses it by name until the key is re-measured (receipts/ledger/
  platform-c3-refusal/). With the key at 21,384 B it plans 59.0, its ledgered tiles; `test_ctrl_memory.py`
  passes with its planted ledgers (receipts/ledger/test_ctrl_memory-at-change.log).

## S2 harness and load_grade.py (recorded, not graded)

Run as its README runs it (`run.py --point 1x1|8x8 --record-budget-findings`), every group, at
`1d6bf555` (pin `70936b77`) and at the change; recorded, not graded: S2b (#810) owns the grade and the
service loop. `load_grade.py` is not on `dev-soft-core` (S2b's branch adds it), so it cannot be run here.

| Point | Groups | T_svc misses at 70936b77 | at 715589c | rc |
|---|---:|---|---|---|
| 1x1/1if | 18 | 34 of 141 instances, 13 of 81 paths | 35 of 141, 14 of 81 | 0, 0 |
| 8x8/2if | 17 | 63 of 182 instances, 31 of 129 paths | 59 of 182, 31 of 129 | 0, 0 |

- **"an ACMP command behind the owed input"** (#26's last acceptance item): at `70936b77` "at least
  362.726 ms, NEVER ANSWERED" (1x1) and "at least 370.366 ms, NEVER ANSWERED" (8x8); at the change every one
  of the four commands is answered, the worst after 104.915 ms (1x1) and 137.688 ms (8x8). Both are over the
  harness's 20 ms ceiling and within Milan v1.2 Table 5.26's 200 ms command timeout.
- **GET_TX_STATE at 1x1** moves from 9.454 ms (fits) to 10.384 ms, over T_svc 10 ms: the one row that
  crosses at 1x1. At 8x8 the misses fall by four (ENTITY_AVAILABLE and the MAAP release rows).
- The head-side runs used the clean clone of `f42198ce`; the later commits change only Python plant tables.
  At the final head S2's build was made again: the image is byte-identical, the re-simulated `adp-gm` group's
  log is byte-identical, and every recorded group regrades to an identical table (receipts/s2/).

### 1x1/1if: S2's paths at 70936b77 and at 715589c (recorded, not graded)

| Path | Interface | ms (bound) at 70936b77 | Verdict | ms (bound) at 715589c | Verdict | Instances, misses (old -> new) |
|---|---:|---:|---|---:|---|---|
| BIND_RX | 0 | 0.983 (2.492) | fits | 0.814 (2.220) | fits | 2, 0 -> 2, 0 |
| DISCONNECT_TX | 0 | 9.418 (14.248) | fits | 8.651 (15.427) | fits | 1, 0 -> 1, 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | 8.723 (14.041) | fits | 6.429 (15.388) | fits | 1, 0 -> 1, 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | 15.328 (30.841) | MISS T_svc | 11.811 (15.328) | MISS T_svc | 2, 1 -> 2, 1 |
| GET_RX_STATE | 0 | 9.645 (16.045) | fits | 8.991 (15.459) | fits | 1, 0 -> 1, 0 |
| GET_TX_CONNECTION | 0 | 9.415 (14.248) | fits | 8.654 (15.425) | fits | 1, 0 -> 1, 0 |
| GET_TX_STATE | 0 | 9.454 (14.279) | fits | 10.384 (15.459) | MISS T_svc **changed** | 1, 0 -> 1, 1 |
| PROBE_TX | 0 | 8.134 (14.384) | fits | 7.409 (12.100) | fits | 1, 0 -> 1, 0 |
| PROBE_TX_RESPONSE | 0 | 12.514 (15.891) | MISS T_svc | 11.889 (15.505) | MISS T_svc | 1, 1 -> 1, 1 |
| TMR_DELAY | 0 | 0.981 (13.849) | fits | 1.341 (13.464) | fits | 1, 0 -> 1, 0 |
| TMR_NO_ADP (H-DISC) | 0 | 2.134 (13.848) | fits | 2.168 (11.758) | fits | 1, 0 -> 1, 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | 1.339 (14.309) | fits | 3.409 (28.352) | fits | 2, 0 -> 2, 0 |
| the second TMR_NO_RESP | 0 | 0.700 (13.572) | fits | 1.181 (13.272) | fits | 1, 0 -> 1, 0 |
| TMR_NO_TK | 0 | 1.990 (12.078) | fits | 1.467 (26.739) | fits | 1, 0 -> 1, 0 |
| TMR_RETRY | 0 | 0.748 (11.795) | fits | 2.580 (26.438) | fits | 1, 0 -> 1, 0 |
| UNBIND_RX | 0 | 9.599 (16.346) | fits | 8.796 (14.212) | fits | 1, 0 -> 1, 0 |
| RCV_ADP_DISCOVER | 0 | 0.224 (1.144) | fits | 0.203 (1.132) | fits | 2, 0 -> 2, 0 |
| GM_CHANGE | 0 | 0.077 (1.022) | fits | 0.083 (1.044) | fits | 1, 0 -> 1, 0 |
| LINK_DOWN | 0 | 0.065 (3.101) | fits | 0.068 (3.453) | fits | 2, 0 -> 2, 0 |
| LINK_UP | 0 | 0.077 (3.241) | fits | 0.083 (3.209) | fits | 6, 0 -> 6, 0 |
| TMR_ADVERTISE expiry | 0 | 0.786 (1.718) | fits | 0.837 (1.786) | fits | 1, 0 -> 1, 0 |
| TMR_DELAY expiry | 0 | 0.944 (2.831) | fits | 0.825 (2.741) | fits | 5, 0 -> 5, 0 |
| entity_available | 0 | 2.141 (2.923) | fits | 2.082 (2.864) | fits | 1, 0 -> 1, 0 |
| get_avb_info | 0 | 2.162 (2.944) | fits | 2.121 (2.903) | fits | 1, 0 -> 1, 0 |
| get_configuration | 0 | 2.104 (2.886) | fits | 2.056 (2.838) | fits | 1, 0 -> 1, 0 |
| get_counters | 0 | 2.392 (3.173) | fits | 2.665 (3.447) | fits | 1, 0 -> 1, 0 |
| get_name | 0 | 2.261 (3.043) | fits | 2.222 (3.004) | fits | 1, 0 -> 1, 0 |
| lock_entity | 0 | 2.266 (3.230) | fits | 2.220 (3.163) | fits | 1, 0 -> 1, 0 |
| MVU GET_MILAN_INFO | 0 | 1.735 (2.517) | fits | 1.689 (2.471) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (312 B) | 0 | 2.797 (3.579) | fits | 2.752 (3.534) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (106 B) | 0 | 2.344 (3.125) | fits | 2.303 (3.084) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (86 B) | 0 | 2.621 (3.403) | fits | 2.271 (3.053) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (72 B) | 0 | 2.284 (3.066) | fits | 2.556 (3.338) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (452 B) | 0 | 3.106 (3.888) | fits | 3.065 (3.847) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (20 B) | 0 | 2.175 (2.956) | fits | 2.133 (2.915) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (148 B) | 0 | 2.437 (3.219) | fits | 2.395 (3.177) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (90 B) | 0 | 2.362 (3.144) | fits | 2.320 (3.102) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (113 B) | 0 | 2.409 (3.191) | fits | 2.368 (3.150) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (82 B) | 0 | 2.651 (3.433) | fits | 2.614 (3.396) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (146 B) | 0 | 2.741 (3.523) | fits | 2.706 (3.488) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (102 B) | 0 | 2.343 (3.124) | fits | 2.301 (3.083) | fits | 1, 0 -> 1, 0 |
| register_unsolicited | 0 | 1.413 (2.187) | fits | 1.370 (2.143) | fits | 1, 0 -> 1, 0 |
| set_name | 0 | 2.756 (4.144) | fits | 2.698 (4.066) | fits | 1, 0 -> 1, 0 |
| unknown_command | 0 | 2.099 (2.881) | fits | 2.055 (2.837) | fits | 1, 0 -> 1, 0 |
| unlock_entity | 0 | 2.578 (3.543) | fits | 2.220 (3.162) | fits | 1, 0 -> 1, 0 |
| add_audio_mappings | 0 | 4.730 (5.543) | fits | 4.365 (5.179) | fits | 1, 0 -> 1, 0 |
| remove_audio_mappings | 0 | 4.750 (5.565) | fits | 4.385 (5.202) | fits | 1, 0 -> 1, 0 |
| set_clock_source | 0 | 4.544 (5.164) | fits | 4.180 (4.801) | fits | 1, 0 -> 1, 0 |
| set_control_identify_on | 0 | 4.377 (5.163) | fits | 4.014 (4.801) | fits | 2, 0 -> 2, 0 |
| set_sampling_rate | 0 | 4.386 (4.986) | fits | 4.026 (4.627) | fits | 1, 0 -> 1, 0 |
| an ACMP command behind a full acmp ring | 0 | 37.281 (41.386) | MISS ceiling | 33.075 (36.664) | MISS ceiling | 1, 1 -> 1, 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | 42.055 (53.150) | MISS ceiling | 37.086 (47.635) | MISS ceiling | 1, 1 -> 1, 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | 38.615 (55.069) | MISS ceiling | 33.363 (53.731) | MISS ceiling | 1, 1 -> 1, 1 |
| an event behind 15 others | 0 | 9.348 (17.383) | fits | 8.632 (15.938) | fits | 1, 0 -> 1, 0 |
| a response with 7 frames owed ahead of it | 0 | 93.481 (96.134) | MISS ceiling | 94.143 (95.734) | MISS ceiling | 1, 1 -> 1, 1 |
| an ACMP command behind the owed input | 0 | at least 362.726 | NEVER ANSWERED | 104.915 (105.904) | MISS ceiling **changed** | 4, 4 -> 4, 4 |
| SET_NAME fan-out to one registered controller | 0 | 2.989 (4.159) | fits | 2.904 (4.078) | fits | 1, 0 -> 1, 0 |
| ANNOUNCE (TMR expiry) | 0 | 1.593 (3.504) | fits | 1.004 (3.263) | fits | 1, 0 -> 1, 0 |
| conflicting PROBE -> DEFEND | 0 | 0.458 (1.359) | fits | 0.408 (1.322) | fits | 1, 0 -> 1, 0 |
| first PROBE (LINK_UP) | 0 | 0.531 (3.241) | fits | 0.500 (3.209) | fits | 1, 0 -> 1, 0 |
| last PROBE retransmission (TMR expiry) | 0 | 1.443 (3.504) | fits | 0.852 (3.263) | fits | 1, 0 -> 1, 0 |
| PROBE retransmission (TMR expiry) | 0 | 1.054 (2.615) | fits | 1.520 (3.436) | fits | 2, 0 -> 2, 0 |
| ACMP record released under the composed load, first | 0 | 9.065 | fits | 8.038 | fits | 5, 0 -> 5, 0 |
| ACMP record released under the composed load, last | 0 | 85.791 | MISS ceiling | 79.989 | MISS ceiling | 5, 4 -> 5, 4 |
| ADP record released under the composed load, first | 0 | 9.056 | fits | 8.062 | fits | 5, 0 -> 5, 0 |
| ADP record released under the composed load, last | 0 | 49.690 | MISS T_svc | 43.836 | MISS T_svc | 5, 4 -> 5, 4 |
| AECP record released under the composed load, first | 0 | 9.101 | fits | 8.073 | fits | 5, 0 -> 5, 0 |
| AECP record released under the composed load, last | 0 | 254.111 | MISS ceiling | 245.188 | MISS ceiling | 5, 4 -> 5, 4 |
| MAAP record released under the composed load, first | 0 | 9.090 | fits | 8.063 | fits | 5, 0 -> 5, 0 |
| MAAP record released under the composed load, last | 0 | 49.726 | MISS T_svc | 43.873 | MISS T_svc | 5, 4 -> 5, 4 |
| SRP record released under the composed load, first | 0 | at least 578.600 | STARVED: never released | at least 573.349 | STARVED: never released | 5, 4 -> 5, 4 |
| SRP record released under the composed load, last | 0 | at least 578.580 | STARVED: never released | at least 573.329 | STARVED: never released | 5, 4 -> 5, 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | 3.252 (4.654) | fits | 3.231 (4.630) | fits | 1, 0 -> 1, 0 |
| Listener Ready RX (registrar) | 0 | 1.904 (1.905) | fits | 1.907 (1.908) | fits | 1, 0 -> 1, 0 |
| malformed MRPDU discard | 0 | 1.582 (1.583) | fits | 1.587 (1.588) | fits | 2, 0 -> 2, 0 |
| startup declarations (LINK_UP) | 0 | 2.867 (3.241) | fits | 2.835 (3.209) | fits | 1, 0 -> 1, 0 |

### 8x8/2if: S2's paths at 70936b77 and at 715589c (recorded, not graded)

| Path | Interface | ms (bound) at 70936b77 | Verdict | ms (bound) at 715589c | Verdict | Instances, misses (old -> new) |
|---|---:|---:|---|---:|---|---|
| BIND_RX | 0 | 1.431 (4.680) | fits | 0.837 (3.358) | fits | 1, 0 -> 1, 0 |
| BIND_RX | 1 | 16.944 (37.100) | MISS T_svc | 15.393 (35.662) | MISS T_svc | 1, 1 -> 1, 1 |
| DISCONNECT_TX | 0 | 16.511 (36.512) | MISS T_svc | 17.162 (37.162) | MISS T_svc | 1, 1 -> 1, 1 |
| DISCONNECT_TX | 1 | 5.052 (25.052) | fits | 7.328 (27.328) | fits | 1, 0 -> 1, 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | 22.883 (53.525) | MISS ceiling | 18.200 (27.797) | MISS T_svc **changed** | 1, 1 -> 1, 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | 24.163 (53.525) | MISS ceiling | 18.687 (27.797) | MISS T_svc **changed** | 1, 1 -> 1, 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | 17.759 (26.082) | MISS T_svc | 18.445 (27.714) | MISS T_svc | 1, 1 -> 1, 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | 19.006 (26.082) | MISS T_svc | 18.893 (27.714) | MISS T_svc | 1, 1 -> 1, 1 |
| GET_RX_STATE | 0 | 16.751 (36.632) | MISS T_svc | 17.484 (37.225) | MISS T_svc | 1, 1 -> 1, 1 |
| GET_RX_STATE | 1 | 5.834 (33.936) | fits | 4.496 (32.453) | fits | 1, 0 -> 1, 0 |
| GET_TX_CONNECTION | 0 | 16.522 (36.523) | MISS T_svc | 15.036 (35.037) | MISS T_svc | 1, 1 -> 1, 1 |
| GET_TX_CONNECTION | 1 | 1.753 (21.754) | fits | 3.620 (23.620) | fits | 1, 0 -> 1, 0 |
| GET_TX_STATE | 0 | 18.724 (38.717) | MISS T_svc | 15.087 (35.078) | MISS T_svc | 1, 1 -> 1, 1 |
| GET_TX_STATE | 1 | 8.902 (28.896) | fits | 3.660 (23.651) | fits | 1, 0 -> 1, 0 |
| PROBE_TX | 0 | 16.870 (36.550) | MISS T_svc | 17.595 (37.183) | MISS T_svc | 1, 1 -> 1, 1 |
| PROBE_TX | 1 | 5.416 (25.086) | fits | 7.793 (27.374) | fits | 1, 0 -> 1, 0 |
| PROBE_TX_RESPONSE | 0 | 4.026 (21.423) | fits | 3.406 (20.353) | fits | 1, 0 -> 1, 0 |
| PROBE_TX_RESPONSE | 1 | 7.151 (28.764) | fits | 5.854 (27.414) | fits | 1, 0 -> 1, 0 |
| TMR_DELAY | 0 | 1.488 (21.472) | fits | 0.892 (23.263) | fits | 1, 0 -> 1, 0 |
| TMR_DELAY | 1 | 3.215 (48.247) | fits | 6.668 (46.260) | fits | 1, 0 -> 1, 0 |
| TMR_NO_ADP (H-DISC) | 0 | 2.155 (23.117) | fits | 6.232 (45.204) | fits | 1, 0 -> 1, 0 |
| TMR_NO_ADP (H-DISC) | 1 | 2.558 (50.758) | fits | 3.375 (19.574) | fits | 1, 0 -> 1, 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | 3.142 (24.594) | fits | 6.568 (42.758) | fits | 1, 0 -> 1, 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | 7.910 (49.183) | fits | 6.197 (42.758) | fits | 1, 0 -> 1, 0 |
| the second TMR_NO_RESP | 0 | 2.515 (24.314) | fits | 1.452 (42.387) | fits | 1, 0 -> 1, 0 |
| the second TMR_NO_RESP | 1 | 7.659 (44.813) | fits | 4.959 (42.387) | fits | 1, 0 -> 1, 0 |
| TMR_NO_TK | 0 | 4.097 (24.646) | fits | 8.462 (46.393) | fits | 1, 0 -> 1, 0 |
| TMR_NO_TK | 1 | 3.368 (24.576) | fits | 0.911 (23.283) | fits | 1, 0 -> 1, 0 |
| TMR_RETRY | 0 | 0.359 (24.276) | fits | 5.018 (42.303) | fits | 1, 0 -> 1, 0 |
| TMR_RETRY | 1 | 8.906 (45.747) | fits | 1.763 (19.198) | fits | 1, 0 -> 1, 0 |
| UNBIND_RX | 0 | 14.530 (34.731) | MISS T_svc | 10.779 (31.135) | MISS T_svc | 1, 1 -> 1, 1 |
| UNBIND_RX | 1 | 13.468 (25.452) | MISS T_svc | 11.974 (24.118) | MISS T_svc | 1, 1 -> 1, 1 |
| RCV_ADP_DISCOVER | 0 | 0.199 (2.379) | fits | 0.622 (2.833) | fits | 2, 0 -> 2, 0 |
| RCV_ADP_DISCOVER | 1 | 0.375 (2.379) | fits | 0.796 (2.833) | fits | 1, 0 -> 1, 0 |
| GM_CHANGE | 0 | 0.079 (2.207) | fits | 0.498 (2.656) | fits | 1, 0 -> 1, 0 |
| GM_CHANGE | 1 | 0.171 (2.207) | fits | 0.584 (2.656) | fits | 1, 0 -> 1, 0 |
| LINK_DOWN | 0 | 0.063 (12.989) | fits | 0.484 (12.950) | fits | 1, 0 -> 1, 0 |
| LINK_DOWN | 1 | 5.063 (12.989) | fits | 5.460 (12.950) | fits | 1, 0 -> 1, 0 |
| LINK_UP | 0 | 0.078 (12.213) | fits | 0.489 (12.146) | fits | 5, 0 -> 5, 0 |
| LINK_UP | 1 | 0.862 (12.213) | fits | 1.225 (12.146) | fits | 5, 0 -> 5, 0 |
| TMR_ADVERTISE expiry | 0 | 0.266 (2.291) | fits | 0.548 (2.611) | fits | 1, 0 -> 1, 0 |
| TMR_ADVERTISE expiry | 1 | 0.172 (2.291) | fits | 0.456 (2.611) | fits | 1, 0 -> 1, 0 |
| TMR_DELAY expiry | 0 | 1.453 (5.908) | fits | 1.060 (5.510) | fits | 5, 0 -> 5, 0 |
| TMR_DELAY expiry | 1 | 0.848 (4.908) | fits | 0.378 (2.699) | fits | 5, 0 -> 5, 0 |
| entity_available | 0 | 2.496 (4.124) | fits | 2.438 (4.108) | fits | 1, 0 -> 1, 0 |
| entity_available | 1 | 2.927 (4.558) | fits | 2.433 (4.104) | fits | 1, 0 -> 1, 0 |
| get_avb_info | 0 | 4.588 (6.705) | fits | 2.576 (4.246) | fits | 1, 0 -> 1, 0 |
| get_avb_info | 1 | 2.618 (4.250) | fits | 2.571 (4.241) | fits | 1, 0 -> 1, 0 |
| get_configuration | 0 | 2.894 (4.524) | fits | 2.409 (4.079) | fits | 1, 0 -> 1, 0 |
| get_configuration | 1 | 2.889 (4.520) | fits | 2.834 (4.504) | fits | 1, 0 -> 1, 0 |
| get_counters | 0 | 2.772 (4.402) | fits | 4.477 (8.203) | fits | 1, 0 -> 1, 0 |
| get_counters | 1 | 2.768 (4.400) | fits | 3.149 (4.820) | fits | 1, 0 -> 1, 0 |
| get_name | 0 | 3.039 (4.668) | fits | 2.984 (4.654) | fits | 1, 0 -> 1, 0 |
| get_name | 1 | 3.048 (4.680) | fits | 2.565 (4.236) | fits | 1, 0 -> 1, 0 |
| lock_entity | 0 | 3.356 (5.212) | fits | 2.868 (4.745) | fits | 1, 0 -> 1, 0 |
| lock_entity | 1 | 2.925 (4.936) | fits | 2.869 (4.881) | fits | 1, 0 -> 1, 0 |
| MVU GET_MILAN_INFO | 0 | 2.204 (3.833) | fits | 1.726 (3.396) | fits | 1, 0 -> 1, 0 |
| MVU GET_MILAN_INFO | 1 | 1.778 (3.408) | fits | 1.722 (3.392) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (312 B) | 0 | 3.599 (5.229) | fits | 3.534 (5.204) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (312 B) | 1 | 3.590 (5.220) | fits | 3.531 (5.201) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (106 B) | 0 | 3.134 (4.764) | fits | 2.653 (4.323) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (106 B) | 1 | 2.697 (4.327) | fits | 2.649 (4.319) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (86 B) | 0 | 2.697 (4.327) | fits | 2.650 (4.320) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (72 B) | 0 | 2.668 (4.298) | fits | 2.621 (4.291) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (452 B) | 0 | 3.490 (5.120) | fits | 3.443 (5.113) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (20 B) | 0 | 2.569 (4.198) | fits | 2.521 (4.191) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (148 B) | 0 | 2.794 (4.424) | fits | 2.747 (4.417) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (148 B) | 1 | 3.350 (6.883) | fits | 2.745 (4.416) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (90 B) | 0 | 2.832 (4.462) | fits | 3.214 (4.884) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (113 B) | 0 | 2.871 (4.501) | fits | 2.824 (4.494) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (96 B) | 0 | 2.837 (4.466) | fits | 2.789 (4.459) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (146 B) | 0 | 2.801 (4.431) | fits | 2.754 (4.424) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (102 B) | 0 | 4.341 (7.990) | fits | 2.670 (4.340) | fits | 1, 0 -> 1, 0 |
| register_unsolicited | 0 | 2.199 (3.822) | fits | 1.723 (3.388) | fits | 1, 0 -> 1, 0 |
| register_unsolicited | 1 | 1.760 (3.389) | fits | 2.144 (3.815) | fits | 1, 0 -> 1, 0 |
| set_name | 0 | 4.337 (7.343) | fits | 4.279 (7.299) | fits | 1, 0 -> 1, 0 |
| set_name | 1 | 3.959 (6.645) | fits | 3.901 (6.587) | fits | 1, 0 -> 1, 0 |
| unknown_command | 0 | 2.455 (4.083) | fits | 2.409 (4.079) | fits | 1, 0 -> 1, 0 |
| unknown_command | 1 | 2.884 (4.516) | fits | 2.404 (4.075) | fits | 1, 0 -> 1, 0 |
| unlock_entity | 0 | 3.356 (5.211) | fits | 3.296 (5.172) | fits | 1, 0 -> 1, 0 |
| unlock_entity | 1 | 2.924 (4.930) | fits | 2.869 (4.879) | fits | 1, 0 -> 1, 0 |
| set_clock_source | 0 | 8.126 (9.607) | fits | 7.509 (9.032) | fits | 1, 0 -> 1, 0 |
| set_clock_source | 1 | 7.725 (9.207) | fits | 8.293 (11.893) | fits | 1, 0 -> 1, 0 |
| set_control_identify_on | 0 | 9.118 (12.805) | fits | 8.896 (12.663) | fits | 2, 0 -> 2, 0 |
| set_control_identify_on | 1 | 9.308 (12.995) | fits | 6.843 (8.534) | fits | 2, 0 -> 2, 0 |
| set_sampling_rate | 0 | 8.269 (11.769) | fits | 7.886 (11.465) | fits | 1, 0 -> 1, 0 |
| an ACMP command behind a full acmp ring | 0 | 58.721 (64.547) | MISS ceiling | 50.281 (55.301) | MISS ceiling | 1, 1 -> 1, 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | 47.983 (66.599) | MISS ceiling | 39.365 (59.334) | MISS ceiling | 1, 1 -> 1, 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | 53.763 (68.398) | MISS ceiling | 40.657 (58.497) | MISS ceiling | 1, 1 -> 1, 1 |
| an event behind 15 others | 0 | 14.843 (28.667) | MISS T_svc | 20.637 (33.358) | MISS T_svc | 1, 1 -> 1, 1 |
| a response with 7 frames owed ahead of it | 0 | 118.769 (124.507) | MISS ceiling | 111.934 (116.885) | MISS ceiling | 1, 1 -> 1, 1 |
| an ACMP command behind the owed input | 0 | at least 370.366 | NEVER ANSWERED | 137.688 (142.098) | MISS ceiling **changed** | 4, 4 -> 4, 4 |
| ANNOUNCE (TMR expiry) | 0 | 2.671 (6.719) | fits | 1.878 (5.410) | fits | 1, 0 -> 1, 0 |
| ANNOUNCE (TMR expiry) | 1 | 2.570 (6.675) | fits | 2.742 (5.485) | fits | 1, 0 -> 1, 0 |
| conflicting PROBE -> DEFEND | 0 | 1.079 (3.051) | fits | 0.605 (2.591) | fits | 1, 0 -> 1, 0 |
| conflicting PROBE -> DEFEND | 1 | 1.077 (3.078) | fits | 1.034 (3.061) | fits | 1, 0 -> 1, 0 |
| first PROBE (LINK_UP) | 0 | 0.761 (7.313) | fits | 1.122 (7.284) | fits | 1, 0 -> 1, 0 |
| first PROBE (LINK_UP) | 1 | 0.762 (6.919) | fits | 1.134 (7.328) | fits | 1, 0 -> 1, 0 |
| last PROBE retransmission (TMR expiry) | 0 | 2.522 (6.719) | fits | 1.730 (5.410) | fits | 1, 0 -> 1, 0 |
| last PROBE retransmission (TMR expiry) | 1 | 2.420 (6.675) | fits | 2.594 (5.485) | fits | 1, 0 -> 1, 0 |
| PROBE retransmission (TMR expiry) | 0 | 2.111 (6.122) | fits | 2.530 (5.075) | fits | 2, 0 -> 2, 0 |
| PROBE retransmission (TMR expiry) | 1 | 2.287 (6.357) | fits | 1.822 (5.958) | fits | 2, 0 -> 2, 0 |
| ACMP record released under the composed load, first | 0 | 14.288 | MISS T_svc | 12.660 | MISS T_svc | 4, 4 -> 4, 3 |
| ACMP record released under the composed load, last | 0 | 104.248 | MISS ceiling | 89.225 | MISS ceiling | 4, 4 -> 4, 4 |
| ADP record released under the composed load, first | 0 | 14.331 | MISS T_svc | 12.703 | MISS T_svc | 4, 4 -> 4, 3 |
| ADP record released under the composed load, last | 0 | 64.292 | MISS T_svc | 48.438 | MISS T_svc | 2, 2 -> 2, 2 |
| ADP record released under the composed load, last | 1 | 48.027 | MISS T_svc | 41.799 | MISS T_svc | 2, 2 -> 2, 2 |
| AECP record released under the composed load, first | 0 | 14.324 | MISS T_svc | 12.696 | MISS T_svc | 4, 4 -> 4, 3 |
| AECP record released under the composed load, last | 1 | 315.049 | MISS ceiling | 296.145 | MISS ceiling | 4, 4 -> 4, 4 |
| MAAP record released under the composed load, first | 0 | 14.314 | MISS T_svc | 12.686 | MISS T_svc | 4, 4 -> 4, 3 |
| MAAP record released under the composed load, last | 0 | 59.158 | MISS ceiling | 47.746 | MISS T_svc **changed** | 4, 4 -> 4, 4 |
| SRP record released under the composed load, first | 0 | at least 593.749 | STARVED: never released | at least 580.642 | STARVED: never released | 4, 4 -> 4, 4 |
| SRP record released under the composed load, last | 1 | at least 593.729 | STARVED: never released | at least 580.622 | STARVED: never released | 4, 4 -> 4, 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | 8.322 (10.070) | fits | 8.246 (10.051) | fits | 1, 0 -> 1, 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | 8.552 (10.218) | fits | 8.476 (10.195) | fits | 1, 0 -> 1, 0 |
| Listener Ready RX (registrar) | 0 | 3.308 (3.309) | fits | 3.784 (3.784) | fits | 1, 0 -> 1, 0 |
| Listener Ready RX (registrar) | 1 | 3.376 (3.377) | fits | 3.411 (3.412) | fits | 1, 0 -> 1, 0 |
| malformed MRPDU discard | 0 | 3.063 (3.064) | fits | 2.585 (2.586) | fits | 1, 0 -> 1, 0 |
| malformed MRPDU discard | 1 | 3.215 (3.216) | fits | 3.250 (3.251) | fits | 1, 0 -> 1, 0 |
| startup declarations (LINK_UP) | 0 | 6.824 (7.313) | fits | 6.768 (7.284) | fits | 1, 0 -> 1, 0 |
| startup declarations (LINK_UP) | 1 | 6.486 (6.921) | fits | 6.439 (6.903) | fits | 1, 0 -> 1, 0 |

## Gate table (clean clone of the final head)

`verify_wf.py` over every `run:` step of `docs.yml`, `rtl-fast.yml`, `elaborate.yml` and `rtl.yml` (the four
workflows a pull request to `dev-soft-core` triggers) at `50e2a722`: **139 steps ran, rc 0; 226 not run, each
with its reason in `not_run.json`; 0 bad** (receipts/gates/verify-final.md, the step logs in
receipts/gates/workflows/). Each job ran on its own fresh clean clone; every clone's tree after the job is
clean (`docs-check-no-git` removes `.git` by design, so its after-check cannot run; its three steps are rc 0).

| Gate | Where | Result |
|---|---|---|
| every `run:` step of `docs.yml` | wire-accountability, docs-check-no-git, docs-gates-0/1/2, docs-check | all rc 0 (runner and verifier adapted from the earlier lanes' `run_docs_yml.py`/`verify_docs_yml.py`, receipts/tools/gates/) |
| `rtl-fast.yml` | changes, verilator-lint ("LINT GATE: PASS (89 violation(s) <= ratchet 89 …)"), bdd-conformance, yosys-tool, yosys-elaboration, publication-census ("0 of 57 rule(s) no arm proves"), split-cdc ("checks: 13 failures: 0"), the six firmware jobs, rtl-fast | all rc 0 |
| `elaborate.yml` | elaborate-gates-0, elaborate-gates-1 (the LiteX simulation aggregate, `test_ctrl_memory.py` among them), elaborate | all rc 0 (LiteX venv) |
| `rtl.yml` (a pull request's jobs) | full-ci-gate, yosys-tool, yosys-shards 0-3 | all rc 0; `verilator-shards` is the sweep below |
| the full sweep, four `native-shards.py` units | shards on 8-15, 24-31, 48-51, 64-71 (`capture_coherence`'s shard on 4 CPUs), MAKEFLAGS `-j4 --no-print-directory` | **65 of 65 suites, 2,192,899 checks, 0 failures, 0 timed out** (15 + 17 + 17 + 16); preflight logs pass, no #833 re-run needed |
| `test_ctrl_firmware.py --require-rv32 --self-test` | the four firmware shards | PASS, PASS, PASS, PASS |
| `fw_coverage.py --check` | firmware-unit | PASS (35 files) |
| every firmware mutant driver | control 579/579; AECP; SRP and pin controls | PASS |
| S2's harness, 1x1/1if and 8x8/2if | at `f42198ce`'s clean clone, then at `50e2a722`: S2 rebuilt, image byte-identical (`62740b8f…`, `4047227d…`), `adp-gm` re-simulated byte-identical, all groups regraded to an identical `table.md` | rc 0 at both points (recorded, not graded) |
| `test_builder.py --require-rv32` | docs-gates-1/2 legs ("ALL GATES PASS EXCEPT 1 / 16 NOT RUN": no LiteX in that job, as hosted); again with the LiteX interpreter and HOME on a clean clone | leg 0 "ALL GATES PASS"; leg 1 "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11 needs a placed hardware build's report, not on this host) |
| `cd tests && behave` | bdd-conformance | "508 scenarios passed, 0 failed, 0 skipped" |
| `git diff --check` against the merge base `1d6bf555` | clean clone of `50e2a722` | rc 0, no output |

Not run (each with its reason in `not_run.json`): hosted orchestration (step records, artifact uploads,
fail-fast and cancellation), installs the host already carries (apt, sudo, the RV32 SDK download: the
pinned SDK is the host's, linked into the runner's HOME), and `rtl.yml`'s workers whose suites the sweep
runs, its unions and the scheduled `physical-gptp`.

## Open risks / questions

- The kept command offers only the kept record after an accepting poll; the records behind it are offered by
  the next passes' receive service, after their timer service (stated in `acmp_mbx.h`). The contract's
  "offer the waiting frames until one is declined" would need records taken from the poll, outside the
  loop's per-pass receive budget; the one-pass delay arises only behind a kept BIND_RX that is only answered.
  A reviewer may rule otherwise; that is a decision, not a hidden assumption.
- The hot list for #29 is on S2b's line; S2b drops its `__lshrdi3` entry when it syncs onto this pin.
- 32x32: not on this base (S15).
- S2 records, for S2b: GET_TX_STATE at 1x1 crosses T_svc (9.454 → 10.384 ms); the owed-input row is answered
  (104.915 / 137.688 ms) but over the harness's 20 ms ceiling.
- `ci/image/exec-audit-receipt.json` keeps `70936b77` (a receipt of an earlier audit, not a pin statement).
- Scratch to keep or delete: the lane's scratch is about 13 GB; the superseded gate roots hold logs only.
