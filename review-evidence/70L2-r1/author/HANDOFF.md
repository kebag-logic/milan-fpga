# [A448] #70 lane 2: parent pin adoption of processor PRs #132 and #133 (`b2db3a97`)

Status: **REVIEW READY** at head `597dba8593553ad85b1e94936b016907c4d2003a`
(branch `70-lane2-pin-d352`, local only, 21 commits on dev `79c36963`;
processor pin `b2db3a970cedbbff2f8ba813acb96122c442bc58`). The ruling
[5894183475](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5894183475)
on this lane's STOP is implemented: option 1 (gate 1b keeps the pinned
`aem_loaded` slot across a call, with planted controls), the AEM-first reorder,
and processor `b2db3a97` with C1's declared parent edits. At the head: the full
gate bank rc 0, the five native groups rc 0 (at `18199bac`; the only later
commit re-records the receipt and three documents), the capture receipt
re-recorded with `check_nvm_capture` rc 0, and the 3-seed sweep (section Item 5).
One decision the ruling did not spell out is flagged for the reviewers: the
service grader now charges each duty from the writer's first heartbeat
opportunity (section "The service grader under the AEM-first order").

- Assignment: [#70 5888775832](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5888775832);
  scope record [5880276193](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5880276193);
  rulings 5862405632, 5863247772, 5868716535, 5873060660, 5873580810 and
  [5894183475](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5894183475);
  processor PR #132 body ("Parent-visible for pin adoption: rounds 1-6,
  consolidated") and merge bar 5888737365; processor PR #133 body (section 4
  and the composed-head note).
- Branch `70-lane2-pin-d352`, base dev `79c36963660c10e4c1c11a744fb5bff41a552b8b`.
- TAKEN: [5888808563](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5888808563).
- STOP: [5894165470](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5894165470) (`STOP.md`), at `3852b27c`.
- REVIEW READY: [5902107952](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5902107952) (`REVIEW-READY.md`), posted 2026-09-30 at head `597dba85`.
- Sessions: the first was cut by the 12 GiB memory cap (not a gate failure);
  the second ended at the STOP; the third implements the ruling. Heavy work ran
  one job at a time, `make` at `-j8`, Vivado seeds one at a time.

## Commits (one per item)

| # | Commit | Item |
|---|---|---|
| 1 | `43ff243592c777334008df7e6596db4ea537cd8d` | 1. Pin `d352bbaa`, ROM digests, boundary diagram and manifest, submodule ledger |
| 2 | `0a2ace1cd85268cfb46fb00b85eaac82c0bc1589` | 2. The five round-1 ports in the glue, `pend_i`, `PP_STAT[22:16]` |
| 3 | `862dd4da80d367dd3c48c9ed1999f5fd8f7b8f3e` | 2. `NVM_RS_AGG_CYC_P` / `NVM_RETRY_BACKOFF_CYC_P` derived from the parent clock |
| 4 | `a8668505cf0ec8fb7358a49765f2ed0fbe01064b` | 2. `d3_mutants.py` disposition row |
| 5 | `d5eff227c978f8ac4a066b41d16a04b0b5230863` | 2. Walk in `gmstep`, `gptp`/`gptp-lat`, `ax1x1gptp` |
| 6 | `f43ff09d9c200b25a8a4d86fa940d2a74a37a688` | 2. Image-less legs (`sim_main` main/`nolpf`/`ax1x1`, `aclk`) end on either terminal, grade CLOSED |
| 7 | `9cb94bdbcb96e6c2232f0908dec8459200d6cd9e` | 2. `sim_nxn` legs: hold arm, word-37 counter, degrade arm retired, wedged-memory arm moved, word 36 |
| 8 | `f827d8ed9c8a44d8fced845f300bb6b62c67ea9f` | 2. `milan_dp_render` T8 settle |
| 9 | `1c89332dbc067fa5701d0939ac23ca803612ac94` | 2. `pp_shadow` K/K10/K12, M2, P3 |
| 10 | `ac26999e5a995be6452a1cd984c1ff080ca86280` | 2. `nvm_cosim`: `rs_agg_i`, `wr_chg_o`, backoff and deadline derivation, B1-B4 window |
| 11 | `4333a5a0c391df7d008f91f6ac5eaf8cc4ffe85f` | 3. Firmware: walk on every boot path, terminal-aware wait; host test with failing arms |
| 12 | `3852b27cfec53b381447780ce581161cc2140c8a` | 4. Docs |
| 13 | `2091972791d618edd4445f71cd63c64bfbd0d176` | Ruling, option 1: gate 1b keeps the pinned `aem_loaded` slot across a call; five planted pin breaks; the soundness comment at the rule; the firmware page's resolver section |
| 14 | `a6dc7f49aa797db90a31205efa19b43084d553ee` | Ruling: the AEM-first order (firmware, ledger fact, order block) and every statement that called it open |
| 15 | `504396aa721dd505ae36cb48ecd5546114a91c4b` | Ruling: pin `b2db3a97`, ROM digest rows, boundary diagram and manifest, submodule ledger |
| 16 | `376391bb417e4aff49d38e6dcc4fee49c384a886` | C1's declared edits: crflic `[C]` `>= 3`, the restart check, the `milan_dp` README `[C]` row, "What it cannot show" and the failing-arm row |
| 17 | `73e50787797d30945745fb3d453a6cf2a3e9c19c` | C1's declared parent documents: `ieee8021q.md` MRP-4..MRP-7, the compliance matrix 4.2.7.1 and 4.2.7.3/4.4.1, CHANGELOG, the two "adopts" statements |
| 18 | `1b9723928c4bd6212d85c29faa3c4aca9f0e934f` | The recorded nit: the `KL_pp_shadow` instance comment names the three processor times by role, not value |
| 19 | `b61f1d3c90e9ae4787a8e0704d33236fb150b8c6` | The four rows of commit 17 without em dashes (the Markdown em-dash gate) |
| 20 | `18199bacae847f8f3c1a31ee9b62d0086c8abf41` | The service grader charges each duty from the writer's first heartbeat opportunity, with three controls (see its section) |
| 21 | `597dba8593553ad85b1e94936b016907c4d2003a` | The capture receipt and the service figures re-recorded from the native run at commit 20 |

Every commit is one line, no body, no trailer (`git log --format=%b` is empty
for all 21).

## Item 1: the pin, and every digest and ledger it moves

| Ledger | Change | Evidence |
|---|---|---|
| Gitlink | `protocol-processor` `c951a9ff` -> `d352bbaa` (commit 1; PR #132's merge, 24 commits on `c951a9ff`) -> `b2db3a97` (commit 15; PR #133's merge onto `d352bbaa`) | `git submodule status`; `merge-base --is-ancestor` `c951a9ff d352bbaa` and `d352bbaa b2db3a97` rc 0 |
| `syn/yosys/rom_digests.tsv` | two rows each for `d352bbaa` and `b2db3a97` by `syn/yosys/ooc.sh --record-rom-digests` (rc 0; the script reads the staged gitlink). `ltn_rom.hex` `23cc67ee...` and `ucode.hex` `23605682...` equal the `c951a9ff` rows: PR #132's `gen_ucode.py` edit is comments only and PR #133 touches no generator; the ledger is keyed by pin | `syn/yosys/rom_digests.tsv:42-43`, `:50-51` |
| The five RTL source lists | derived, nothing recorded moves: `scripts/check_rtl_source_lists.py` rc 0, "107 files in the milan_datapath closure, 4 of 4 consumer list(s) carry all of them; protocol-processor 36/42 tops, 6 recorded" (the new `KL_aecp_nvm_writer` is in the processor's own tops array); `scripts/pp_srcs.py --check --selftest` rc 0 | gate logs |
| Boundary diagram and manifest | `docs/diagrams/submodule_boundaries.gen.py` regenerated `.drawio`, `.svg`, `.png` and `PNG_MANIFEST.json`; `--check` rc 0 "4 exact gitlinks, decoded PNG"; the PNG was inspected (processor box reads `pin b2db3a970ced`) | `docs/diagrams/PNG_MANIFEST.json:11-14` |
| `docs/reference/SUBMODULES.md` | pin row and the adoption list, both PRs (`:25`, `:83-91`); `scripts/check_submodule_docs.py` rc 0 | |

## Item 2: the consolidated list, as product changes

Contract: `docs/design/SAVED_STATE_MATERIALIZATION.md` section 5.2 (the parent glue)
and 8.7 (the status), processor PR #132's consolidated list.

- **The five round-1 ports** (`hdl/milan/KL_pp_shadow.sv`): new outputs
  `restore_closed_o`, `restore_rb_o`, `rs_cause_o[2:0]`, `restore_cause_o[1:0]`
  (`:687-696`) connected straight from the processor (`:1242-1250`), with
  `d3_unflushed_o` on `d3_unflushed_w` (`:960`, `:1250`). Carried through
  `hdl/milan/milan_datapath.sv` (`:2242-2247`, `:2746-2749`, `:7724-7727`) into
  `hdl/common/csr/milan_csr.sv` (`:657-667` ports, `:2229-2236` read mux):
  `PP_STAT[16]` CLOSED, `[17]` roll-back, `[20:18]` the D3 cause, `[22:21]` the
  binding cause, `[23]` reserved 0. No new CSR (section 5.2). No open port:
  `nvm_cosim` lint 0 PINMISSING, `pp_shadow` and every `milan_dp` build elaborate
  `milan_datapath` under their strict lint, `lint_rtl.py --check` 90 <= 90.
- **Pending** (`KL_pp_shadow.sv:981`):
  `pend_i = (|nvm_unflushed_w) | d3_unflushed_w | aecp_live_wr_w | aecp_live_pend_r`.
  Section 5.2: the D3 term replaces `aecp_dyn_dirty_o` for the scalar groups;
  the live name/map terms stay until stage 3 (no writer yet). `aecp_dyn_dirty_o`
  is still exported as a diagnostic. Leaving it in would have held pending at 1
  over every durable scalar: it is set by any persisted-row write, restore
  writes included (`protocol-processor/hdl/aecp/KL_aecp_dyn_state.sv:327`) and
  never clears.
- **The combined verdicts**: `restore_done_o`, `restore_busy_o` and
  `restore_fail_o` are the processor's combined levels; `restore_blank_o`
  (`:1505`) is the processor's combined blank. The blind-walk latch is unchanged
  (section 5.2), so a blind walk still reads blank beside the wrapper's fail, as
  it did at base. I did NOT gate blank on the wrapper's own fail: that would have
  changed `PP_STAT[7]` for blind walks, which the list does not ask for.
- **`NVM_RS_AGG_CYC_P`, `NVM_RETRY_BACKOFF_CYC_P`** (and `NVM_RS_TMO_CYC_P`):
  not bound at the instance, on purpose (`KL_pp_shadow.sv:1098-1105`, the
  `CLK_HZ_P` banner `:184-186`): the processor derives all three from `CLK_HZ_P`,
  which is bound to this wrapper's clock, `MILAN_CLK_FREQ_HZ` in
  `milan_datapath.sv:7466` (the `axis_clk` frequency, `:66-67`). A literal or a
  second copy of the formula here would be the restatement the assignment rules
  out. The processor grades its own derivations at a nominal clock with no
  override (`tb/pp_top` D3R13, S10).
- **The counter** (snapshot word 37, host word `0x20025`): parent-visible through
  `PP_SPADDR`/`PP_SPDATA`, no RTL change needed. Graded in every `sim_nxn` leg
  (`tb/verilator/milan_dp/sim_nxn.cpp:2359-2375`): a second AECP command during
  the hold moves word 37 by exactly 1, read over a posted access that did not
  error. Documented in `docs/reference/REGISTER_MAP.md` (the `PP_SPADDR` row and
  the two-walk paragraph).
- **The disposition row**: `scripts/measure_test_evidence.py:597-600`;
  `--check` rc 1 before ("1 unexplained DUT-source reader"), rc 0 after.
- **Harnesses** (each graded, not only started):
  - `gmstep` (`sim_gmstep.cpp:812-830`, called `:1205`), `gptp`/`gptp-lat`
    (`sim_gptp.cpp:1001-1021`, `:1759`), `ax1x1gptp` (`sim_ax1x1gptp.cpp:690-712`,
    at the top of `configure()`, so every boot of the harness walks once): each
    checks `PP_STAT` done 1, CLOSED 0 before the first AECP command.
  - Image-less legs (`sim_main.cpp:246-273`, `sim_aclk.cpp:1219-1246`): the wait
    ends on either terminal, and two checks name the one they reach: CLOSED with
    busy 0, done 0, fail 1, and D3 cause 7 at `PP_STAT[20:18]`, read through the
    new bits.
  - `sim_nxn` legs: `prove_aecp_is_held_until_the_restore()` replaces the
    retired degrade arm (`:2341-2375`; hold, drop counted in word 37); the walk
    starts once the descriptor memory answers (`:2510-2527`) and the held
    `READ_DESCRIPTOR` is answered at the release with `SUCCESS`; the
    wedged-memory arm runs inside the image arm before the `NOTIFY_TIMED_TB`
    return (`:2471-2474`), heals to `SUCCESS`, and reads word 36 at the wedge
    (fault set) and after the heal (clear) (`:2417-2432`), R391-5 S2's second
    option. The three stale comments are rewritten (`:2549-2559`, `:2587-2589`).
  - `milan_dp_render` T8 (`sim_tdm8_render.cpp:2102-2109`): one commit-to-pin
    bound (`kFrameAxis + kCdcFloorAxis + kBitAxis`, the constants T14 grades) is
    waited out before collecting.
  - `pp_shadow` (`sim_main.cpp`): the pending boots walk before the enable and
    grade DEFAULTS on the deadlines (`:1388-1403`); M2 walks after the handover
    (`:3699-3703`), `restore_walk_completes()` ORs `PP_CTRL[1]` in (`:3747`);
    P3 expects blank 0 on the refusal (`:3828-3832`) with its banner updated.
  - `nvm_cosim` (`cosim_top.sv`): `.rs_agg_i (1'b0)` (`:278`), `wr_chg_o` on the
    named no-connect `wr_chg_nc_w` (`:183-184`, `:227`), `RS_TMO_CYC_P` and
    `RETRY_BACKOFF_CYC_P` in the top's ceil forms (`:265-270`); B1-B4 give-up
    window 2,000 ms (`cosim_cases.cpp:488`).

## Item 3: firmware (#70 5880276193 item 2) and its host test

Contract: D3 section 5.3 change 2 (`nvm_boot` starts the walk on EVERY path),
the scope record's item 2, and the consolidated list's firmware bullets.

- **Every boot path that enables the entity starts the walk**
  (`sw/firmware/milan_baremetal/milan_baremetal.c`): the persistence-disabled
  path (a record set that does not match the generated shape) now runs the walk
  blind before it returns (`:1460-1472`), as the refused-window path does; the
  writer stays unstarted (`nvm_started` 0, no heartbeat), so the disabled-writer
  console contract is unchanged.
- **The wait ends at the terminal** (`:1361-1386`): `nvm_restore_ended()` is
  `PP_STAT` done OR CLOSED (`MILAN_PP_STAT_RESTORE_CLOSED`, `:155-159`). CLOSED
  never raises done, so a done-only wait spends its whole 3,000 ms timeout on it.
  The same test guards the end-of-boot re-walk (`:1566-1567`). The boot line adds
  `closed`, `rolled_back` and both causes (`:1569-1579`). The bounded wait is
  unchanged: `MILAN_NVM_RESTORE_TIMEOUT_MS` = 3,000 covers PR #132's 1,000 ms plus
  two per-wait deadlines (1,060 ms with margin).
- **Stale comment** (D3 section 18.2's table, "when their owning files change"):
  the debounce comment now cites the ruled DR2a windows (`:342-349`).
  `scripts/nvm_shape.py:146` is not touched by this lane, so its row stays open.
- **Host test** `sw/firmware/nvm_hosttest/test_boot_walk.py`, wired into
  `test_nvm_firmware.py` (`:620`, `:631`, `:639`). The host model
  (`nvm_host.c`) counts `PP_CTRL[1]` rising edges (`walks=`, `:330`), flags an
  entity enable raised before any walk (`enable_first=`, `:324`) and can end the
  walk CLOSED (`--walk-closed`, `:730`; `PP_STAT[16]`, `:439`). Per shape, five
  boot paths: cold boot, every window load refused, persistence disabled
  (planted), and cold and persistence-disabled with a CLOSED restore. Each must
  start exactly one walk, never enable first, and end its wait at the terminal.
  - Shipping firmware: 5 shapes x 5 paths, 0 findings ("each starts one walk
    before the enable").
  - **Failing arm, the dev base firmware itself** (`79c36963`), 1x1 TDM8
    shape: 9 findings, rc 1 - `persistence disabled: walks=0`,
    `enable_first=1`, `done=0`, `fail=0`; `cold boot, CLOSED restore: the
    restore wait ran out its timeout`; the same four on the CLOSED
    persistence-disabled path (`logs/bootwalk-dev-base.log`).
  - **Planted controls** under `--self-test`: `shape_path_skips_walk` (the dev
    early return) caught by 8 findings, first `persistence disabled: walks=0`;
    `wait_on_done_only` caught by 2, first `cold boot, CLOSED restore: the
    restore wait ran out its timeout`.

## The STOP (resolved by the ruling)

At `3852b27c` the AEM-first reorder (PR #132's list, Firmware, round 1; D3
section 5.3 change 1) was refused by builder gate 1b: "the compiled firmware
enters entity_advertise() with [None] rather than with the one value
load_aem_image() handed back" (`logs/gate1b-aem-first-refusal.log`), because
the resolver dropped every static's slot at a call and `aem_loaded` is stored
before `call nvm_boot` and reloaded after it. The lane published the conflict
(`STOP.md`, options 1-3) rather than choose; the manager ruled option 1 plus
the `b2db3a97` adoption. The refused patch is `aem-first-order.patch`; it
landed unchanged as commit 14 once commit 13 was in.

## The ruling, implemented (option 1 and `b2db3a97`)

Ruling [5894183475](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5894183475).

### Gate 1b keeps the pinned verdict across a call (commit 13)

- **The rule** (`sw/builder/test_builder.py:1632-1642`, the soundness argument
  in one comment at the call rule): `_rv32_forget_symbols(state, kept)` drops
  every static's slot at a call except those in `kept` (`:1800`); an unplaced
  store still drops every slot. `kept` is threaded through `rv32_step`,
  `rv32_run` and `rv32_unit` (`:1895`), default empty, so every existing caller
  keeps today's forget-on-call rule.
- **The pins** (`aem_verdict_pins()`, `:6571`), read on the source the census
  compiled and the firmware's other units, so at the same head as the code the
  resolver walks:
  1. one write, `aem_loaded = load_aem_image();` (`verdict_is_the_verifiers()`,
     `:6526`, over `verdict_write_re`, `:6521`);
  2. no unary `&aem_loaded` (`verdict_address_taken()`, `:6534`);
  3. a file-scope static of the one translation unit: declared once as
     `static int aem_loaded;`, emitted with internal linkage (defined here, no
     `.globl`, a `.comm` only with `.local`), and named by no other unit the
     Makefile's `OBJECTS` links (`other_units()`, `:6553`).

  `assert_resolved_boot_flow()` keeps `{"aem_loaded"}` only when the list is
  empty (`:6667`) and, when it refuses on the verdict, names every broken pin
  in the message. The two source rules now read the same two definitions
  (`:11438`, `:11445`), messages unchanged. Every caller hands the source it
  compiled (`source=`), the boot contract also its Makefile's units.
- **Planted controls** (`:14134-14223`), on an AEM-first base built from the
  shipping source by `aem_first()` (`:14145`; the identity once the firmware is
  in that order, which is why they already bite at commit 13, before the
  reorder):
  - the base is ACCEPTED with the slot kept (`kept == ["aem_loaded"]`);
  - the same assembly with no source handed in (forget-on-call) is REFUSED on
    the verdict: the STOP's refusal, reproduced as a control;
  - five pin breaks, each REFUSED on the verdict with its pin named:
    `aem_loaded = 0;` inside `nvm_boot()` and `aem_loaded = 1;` in the UART
    status handler (pin 1), `int *clear_p = &aem_loaded; *clear_p = 0;` inside
    `nvm_boot()` (pin 2), `int aem_loaded;` without `static` (pin 3, linkage),
    and a second unit `milan_verdict.c` declaring `extern int aem_loaded;`
    (pin 3, second unit). The whole boot contract refuses a second object
    earlier still (`assert_single_translation_unit()`), so that control is
    measured on the resolver directly.
  - Measured: gate 1b alone at commit 13 (dev order), rc 0, 825 s, and at
    commit 14 (AEM-first), rc 0, 809 s, both reading "it kept the slot of
    aem_loaded across a call under the verdict's three pins, accepted the
    AEM-first base only with it kept, and refused 5/5 planted pin breaks on
    the verdict, each naming its pin". The full bank's receipt is below.
- **Docs**: `docs/integration/BAREMETAL_FIRMWARE.md:922-936` (the resolver's
  one kept slot and its controls) and the rules table row `:1542`.

### The AEM-first order (commit 14)

- `milan_init()` now reads `configure_fabric(); aem_loaded = load_aem_image();
  nvm_boot(); entity_advertise(aem_loaded);`
  (`sw/firmware/milan_baremetal/milan_baremetal.c:1667-1677`), D3 section 5.3
  change 1; the ledger fact `firmware_boot_order`
  (`docs/reference/milan_feature_status.json:41-46`) and the order block
  (`docs/integration/BAREMETAL_FIRMWARE.md:137-145`) move with it;
  `check_feature_status.py` rc 0.
- Statements that called the order open are now current: the D3 page status
  header, FASTCONNECT's reconciliation note, the compliance matrix section 1.7
  and two rows, the roadmap, README, the firmware page's boot list (steps 3/4)
  and saved-state paragraph, the ledger summary, CHANGELOG.
- The host test (`test_boot_walk.py`) still passes on all five shapes with both
  planted controls caught at this order.

### The service grader under the AEM-first order (commit 20, `18199bac`)

**What the first native run found.** The five native groups were first run at
`b61f1d3c` (`run_native.py`, 20:26 CEST start). The 8x8 `queued-short` service
arm, the first to finish, was refused with exactly two findings: "over-budget
tick stretch: aem_copy_crc" and "over-budget PHY service stretch:
aem_copy_crc", and the runner's STOP stopped the rest (`native-b61f1d3c/`: its
commands, build logs and the arm's raw UART log, `service-8x8-queued-short-raw.log.gz`,
raw SHA-256 `017e95da...`). The boot itself was healthy: `walk done=1 fail=0 ...
closed=0`, the AEM copied before the walk.

**Why.** `tb/verilator/fw_service_budget/run.py:296-298` defines the AEM duty as
the first AEM read to the entity enable, and grades every duty but boot and the
heartbeat row for a tick stretch. In the old order the AEM copy came after
`nvm_boot()` had armed the writer (the first heartbeat opportunity), so the row
held the copy/CRC alone (137 ms at 8x8, graded 387 ms against 500). Under the
ruled order it starts in the pre-heartbeat prefix and holds the copy, the CRC
and all of `nvm_boot()` up to the walk: 1,015 ms with no opportunity, because
none exists before the writer does. The harness README already states the rule
this breaks: "Boot's pre-heartbeat prefix precedes writer liveness arming. The
boot row must not be interpreted as an armed-writer gap", and "Startup AEM and
restore report isolated service-plus-poll costs ... Those costs exclude
intervening startup work".

**The change** (`run.py`, `armed_bound()` and `service_findings()`; README
"Markers and heartbeat opportunities"): the enforce-service verdict charges
every duty's tick and PHY stretch from the writer's first heartbeat
opportunity; a duty that starts armed keeps its whole span (so every old-order
row grades exactly as before, and the three recorded old-order oracle traces in
`oracle.json` are untouched: `grade()` is unchanged). A duty that begins
unarmed records `armed_start_sys_cycle`, `armed_no_tick_ms` and
`armed_period_bound_ms` in its receipt. Nothing else in the grader moves.

- **Controls** (`armed_controls()`, in `--self-test`, 50 checks, 0 failures):
  the measured 8x8 AEM row with its 1,015 ms unarmed prefix and 1 ms service
  after arming passes and records the armed bound (251 ms); the same row armed
  at one opportunity and then unserviced for 25,000,001 cycles is refused on
  both stretches; a row that starts armed keeps its whole-span refusal. Three
  planted wrong rules were each refused by name: today's whole-span rule ("the
  unarmed AEM prefix was charged as an armed gap"), never grading an unarmed
  row ("armed bound not recorded"), and clipping even an armed row ("a duty
  that starts armed lost its whole-span bound").
- **Failing arm, real evidence**: the retained 8x8 `queued-short` raw log
  regraded under today's rule gives exactly the two findings above; under the
  new rule, none (AEM row: 1,019.77 ms long, 1,015.35 ms unarmed, armed
  no-tick 3.16 ms, armed bound 253.16 ms; the restore walk unchanged).
- **This is a decision the ruling did not spell out**, so it is published in
  REVIEW READY and the PR body for the reviewers: the alternative, a firmware
  heartbeat before the writer exists, has no writer to beat for.

### Processor `b2db3a97` (commits 15-17, 19)

- **Gitlink** `d352bbaa` -> `b2db3a97` (processor `main`, the merge of PR #133
  onto `d352bbaa`; `merge-base --is-ancestor d352bbaa b2db3a97` rc 0). C1's
  RTL: `hdl/srp/KL_srp_{encoder,talker_fsm,top,vlan}.sv`; the processor top
  changes one comment (the `srp_active_o` term). No port or parameter moves:
  `check_port_contracts.py`, `check-integrator-params.py` (26/26/26) and
  `check_rtl_source_lists.py` rc 0 unchanged.
- **ROM digests**: `syn/yosys/ooc.sh --record-rom-digests` rc 0 adds two rows
  for `b2db3a97` (`syn/yosys/rom_digests.tsv:42-43`), content equal to the
  `d352bbaa` and `c951a9ff` rows (PR #133 touches no ROM generator); the ledger
  is keyed by pin, so the rows are needed.
- **Diagram and ledger**: regenerated `.drawio`, `.svg`, `.png` and
  `PNG_MANIFEST.json` (`--check` rc 0; the PNG reads `pin b2db3a970ced`);
  `docs/reference/SUBMODULES.md:25`, `:83-91`.
- **crflic** (`tb/verilator/milan_dp/sim_crf_licence.cpp`): the two counts are
  `>= 3` (`:966`, `:969`, C1's `:953,956`), and a new check grades the restart
  itself (`:970-974`, fed by `:708-711` and `:765`, reset per phase `:954-955`): every DUT LeaveAll that
  follows a switch LeaveAll comes at least 10 s after it, over at least two
  such pairs. At `b2db3a97`: 416 checks, 0 failures, 3 and 3 LeaveAlls, the
  soonest DUT LeaveAll 10,210 ms after the switch's. **Failing arm**, the same
  leg at the previous pin `d352bbaa` in a fresh object directory
  (`CRFLIC_MDIR=obj_crflic_prevpin`), pin restored after: 1 of 416 fails,
  exactly the restart check, with 5 and 5 LeaveAlls and the soonest DUT
  LeaveAll 2,210 ms after the switch's (`logs/crflic-restart-arm-d352bbaa.log`,
  raw log SHA-256 `aaafe23b...`).
- **The README** (`tb/verilator/milan_dp/README.md`): the `[C]` row (at least
  three of each, the restart and why), "What it cannot show" (the restart is
  implemented and measured; the draw's upper bound is not), and the failing-arm
  row beside the `424c688f` one. The walk-starter paragraph (PR #133's composed
  note, `:633-637`) and the `[AECP]` paragraph (`:877-883`) were already
  rewritten by commits 5-7 for PR #132.
- **Parent documents** (PR #133 section 4): `docs/traceability/ieee8021q.md`
  MRP-4 (the MVRP-join term and the VLAN-table overflow), MRP-5 (the restart
  implemented; three cycles), MRP-6/MRP-7 (the Table 4.3 grading);
  `docs/reference/MILAN_COMPLIANCE_MATRIX.md` 4.2.7.1 and 4.2.7.3/4.4.1;
  CHANGELOG; the D3 page and FASTCONNECT now say the lane adopts `b2db3a97`.

## Item 4: documentation

D3 lane 1 is described as in the product wherever a current-state statement
said otherwise; dated findings pages and old CHANGELOG entries record what was
measured then and are left as they are.

| Page | What changed |
|---|---|
| `docs/reference/MILAN_COMPLIANCE_MATRIX.md` | section 1.7: the binding persists on silicon; the scalar rows are `partial` (D3 writer, desk only; cold cycle open on #70; the firmware loads the AEM image first since commit 14); rows 4.2.7.1 and 4.2.7.3/4.4.1 cite PR #133 (commits 17, 19); maps and names `missing` with their lanes; the Auto Connect row no longer says the binding does not survive |
| `docs/reference/REGISTER_MAP.md` | the two-walk paragraph after the verdict table; `PP_CTRL[1]` (AECP hold, AEM first, CLOSED, both deadlines); `PP_STAT` `[1]`-`[4]`, `[7]`, `[11]` and the new `[16]`, `[17]`, `[20:18]`, `[22:21]`, `[23]`; `PP_SPADDR` word 37; VERSION stays `0x0060`, the release step owns the bump (the page's own precedent) |
| `docs/design/SAVED_STATE_MATERIALIZATION.md` | status header (stage 1 implemented at pin `b2db3a97`; the AEM-first order adopted; names and maps not implemented); section 1's record writers, `pend_i` composition and the "how a change is seen" table |
| `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` | the known-limitation note; section 6.1's pending sources; section 11's scalar rows (the D3 writer, retired at the window write); section 13 D1 and D3 status; section 17; section 18's capture identities and three rows and section 20 item 6 (commit 21); section 20 item 1 |
| `docs/design/SAVED_STATE_FASTCONNECT.md` | section 1 status rows (two record classes; the absent managers are names and maps) and the reconciliation-pin note (`b2db3a97`, AEM first) |
| `docs/integration/BAREMETAL_FIRMWARE.md` | the boot paragraph (terminal-aware wait, every path walks, the boot line's new fields, the AEM image first), the boot list and order block, the store sentence, and the resolver's kept slot with its rules-table row (commit 13) |
| `docs/integration/INTEGRATION_GUIDE.md`, `docs/limitations/TROUBLESHOOTING.md` (section 27 and two boundary notes), `docs/overview/ARCHITECTURE.md`, `docs/overview/FULL_FPGA_SOLUTION.md`, `docs/fpga/FPGA_DESIGN.md`, `docs/reference/FR_NFR.md`, `docs/MILAN_V12_ROADMAP.md`, `docs/testing/TESTING.md`, `README.md` | current-state persistence statements, AECP hold and the CLOSED terminal |
| `docs/reference/milan_feature_status.json` | the `state.nonvolatile-persistence` summary (status stays `partial`) |
| `CHANGELOG.md` | "Unreleased - processor pin b2db3a97" |
| `docs/findings/397_SERVICE_BUDGET.md` | the re-measured head, pin and firmware; restore handshakes; the AEM row's span and unarmed part; seven regenerated tables (commit 21) |
| `docs/traceability/ieee8021q.md` | MRP-4 to MRP-7 (commits 17, 19) |
| `docs/reference/SUBMODULES.md` | the pin row and both PRs (commit 15) |
| `tb/verilator/fw_service_budget/README.md` | the armed-stretch rule (commit 20) |
| `tb/verilator/milan_dp/README.md`, `tb/verilator/pp_shadow/README.md`, `tb/verilator/nvm_cosim/README.md`, `sw/firmware/nvm_hosttest/README.md` | the arms this lane changed |

## Item 5: timing and area

### Out-of-context area

Instrument: `syn/ooc/pp_shadow_ooc.tcl` at the head, `KL_pp_shadow` at the
shipping 1x1 arrays (`PP_N_IN=2 PP_N_OUT=2`: the 1x1 TDM8 shape's
`ADP_LISTENER_SINK_C` and `ADP_TALKER_SRC_C`, `configs/generated/
endstation_ax7101_1x1_tdm8/gen/adp_shape_defaults.svh:24,27`, which
`milan_datapath.sv:7484-7485` binds as `N_STREAM_IN_P`/`N_STREAM_OUT_P`), part
`xc7a100tfgg484-2`, the script's 100 MHz out-of-context clock, run by
`ooc_session.sh` under `flock /tmp/milan-vivado.lock` (held 01:03:01 to 01:05:25
CEST at `597dba85`, dirty 0). Vivado 2026.1, rc 0, 144 s, no critical warning
(the one `CRITICAL WARNING` string in `ooc.log` is the echoed script comment at
its line 43). Reports in `ooc-597dba85/`: `util.rpt` SHA-256 `32704f95...`,
`util_hier.rpt` `99e825af...`. The same instrument's run at `3852b27c`
(processor `d352bbaa`) is kept in `ooc/` for the C1 delta.

| Instance | LUT (of which LUTRAM) | FF | RAMB36 | RAMB18 | DSP | At `d352bbaa` (LUT / FF) | C1 delta |
|---|---|---|---|---|---|---|---|
| `KL_pp_shadow` (whole plane) | 25,668 (1,422) | 25,937 | 16 | 2 | 8 | 25,623 / 25,881 | +45 / +56 |
| `u_pp` (`protocol_processor_top`) | 24,659 (1,422) | 24,645 | 15 | 1 | 4 | 24,612 / 24,589 | +47 / +56 |
| `u_pp/u_srp` (`KL_srp_top`, C1's RTL) | 4,625 (186) | 6,438 | 0 | 1 | 2 | 4,532 / 6,381 | +93 / +57 |
| `u_pp/u_aecp/u_d3` (`KL_aecp_nvm_writer`, D3 lane 1) | 912 (0) | 488 | 0 | 0 | 0 | 913 / 488 | -1 / 0 |
| `u_nvm` (`KL_nvm_backend`) | 923 (0) | 932 | 0 | 0 | 4 | 925 / 932 | -2 / 0 |

The lane-1 delta itself is PR #132's same-session base/head measurement on the
processor's instrument, +1,031 LUT / +559 FF / 0 BRAM / 0 DSP at 1x1 (its round
5 and 6 DR4 lines). C1 adds +93 LUT / +57 FF in the SRP engine (the VLAN sent
tracking and the licence term) and no BRAM or DSP. The parent glue this lane
adds is wiring and a changed OR term in `pend_i`, so it adds no measurable
logic. The timing section of the out-of-context run (100 MHz, no placement, no
clock source) is not a signoff figure and is not used; the sweep below is.

### Firmware size

PR #132 leaves the firmware size to this lane. Matched comparison, same
toolchain and flags: the firmware is compiled into the BIOS ROM by every
shipping build, and the dev sweep `tdm8dev13eda870` compiled the base firmware
(`git diff 13eda870 79c36963 -- sw/firmware` is empty) with a generated
`csr.h` that differs from this sweep's only in its timestamp line.
`riscv64-elf-size`:

| Object | dev `13eda870` (base firmware) | STOP head `3852b27c` | head `597dba85` (seed `asl`) | Delta to base |
|---|---|---|---|---|
| `libmilan_baremetal/milan_baremetal.o` text | 15,774 B | 16,037 B | 16,061 B | +287 B |
| `bios/bios.elf` text / data / bss | 52,756 / 584 / 2,164 B | 52,964 / 584 / 2,164 B | 52,988 / 584 / 2,164 B | +232 B text |

The AEM-first reorder and its comment add 24 B of text over the STOP head.

The ROM region is 0x20000 (131,072 B, `litex.log` "rom Region added ... Size:
0x00020000"), so text plus data stays at about 41% of it.

### Place sweep

Recipe: PR #615's (`sw/litex/sweep.sh ax7101`, the shipping AX7101 1x1 TDM8
shape, `--vivado-max-threads 32`, the three place directives), run by
`sweep_serial.sh` in this packet: it evaluates `sweep.sh` without its final
`main` line and calls sweep.sh's own `setup_env`, `board_shape`, `check_shape`
(the shape gate passed: `num-streams 1, l2 0, render-lpf False ==
endstation_ax7101_1x1_tdm8.yaml`), `entity_defs` and `build_base`, then runs the
three seeds ONE AT A TIME in the foreground with sweep.sh's `$BASE`, directive
and output directory. The only difference from `sweep.sh` is the serial order:
a seed peaks at about 7.8 GB (`Memory (MB): peak` in `vivado.log`) and this
session runs under a 12 GiB cap. Lock: `flock /tmp/milan-vivado.lock` held from
01:05:41 to 03:11:26 CEST on 2026-09-30, head
`597dba8593553ad85b1e94936b016907c4d2003a`, dirty 0, after the out-of-context
run and after the gate bank (nothing else heavy ran beside it). Tag
`a448s597d`, work directory `~/litex-milan/work/build_ax7101_{asl,eto,eppo}_a448s597d`.
Tabulated by `sweep_table.py` into `sweep-a448s597d.json` (SHA-256
`4840b80b...`; every value read from the build's own
`*_signoff_{Slow,Fast}_{0C,85C}_timing.rpt`, Design Timing Summary).

| Seed | Directive | Slow 0C WNS / WHS | Slow 85C WNS / WHS | Fast 0C WNS / WHS | Fast 85C WNS / WHS | Worst WNS | Worst WHS | Floor | Refusal gate | s |
|---|---|---|---|---|---|---|---|---|---|---|
| asl | AltSpreadLogic_high | +0.064 / +0.065 | +0.064 / +0.065 | +1.513 / +0.034 | +1.513 / +0.034 | +0.064 | +0.034 | meets | accepted | 2,150 |
| eto | ExtraTimingOpt | +0.034 / +0.065 | +0.034 / +0.065 | +1.513 / +0.034 | +1.513 / +0.034 | +0.034 | +0.034 | meets | accepted | 2,952 |
| eppo | ExtraPostPlacementOpt | +0.135 / +0.053 | +0.135 / +0.053 | +1.660 / +0.014 | +1.660 / +0.014 | +0.135 | +0.014 | meets | accepted | 2,442 |

- **Verdict: every seed meets WNS >= +0.030 ns and WHS >= 0 at every declared
  corner**, TNS and THS 0 with 0 failing endpoints at every corner; the floor
  STOP does not apply. `eto` holds the least margin (+0.034 ns). At the STOP
  head (`3852b27c`, processor `d352bbaa`, dev-order firmware) the same recipe
  read +0.174 / +0.247 / +0.070 worst WNS and +0.028 / +0.032 / +0.058 worst WHS
  (`sweep-a448s3852.json`); place-and-route seeds move by more than that between
  any two builds, so no attribution is claimed.
- **One critical warning, `eto`**: `[Route 35-39] The design did not meet
  timing requirements`, at the router's end (`Route 35-20` WNS -0.248 ns, TNS
  -0.576 ns). The flow's post-route `phys_opt_design -directive
  AggressiveExplore` then closed it (`Physopt 32-669` WNS 0.034, TNS 0.000,
  WHS 0.034) before the route checkpoint, the signoff reports and the
  bitstream. `asl` and `eppo` met at the router (`Route 35-20` WNS +0.064 and
  +0.135) and carry no critical warning (the one other `CRITICAL WARNING` string
  in each `vivado.log` is the echoed IOB-pack script comment). Route 35-39 is
  not one of the refused diagnostics.
- **Refusal gate (#607)**, per seed: the launch log carries the gate's own pass
  line `[constraints] .../gateware/vivado.log: no 12-4739, 20-1307 or 12-5201
  diagnostics` and the layout line `[milan] flash-boot layout (baremetal)`;
  `vivado.log` has 0 of each refused diagnostic; `flashboot_layout.json`
  present; one `alinx_ax7101.bit`, no `.bit.rejected`; 17 signoff files;
  `CONSTRAINTS: quasi_static cells=112 setup=4 hold=3`, the count PR #615
  recorded.
- **Ethernet crossings**: all four `eth_clocks0_rx` pairs read `Max Delay
  Datapath Only` at 8.00 ns in every seed's clock-interaction report, worst
  setup slack +5.63 ns.
- **Bitstreams** (3,825,992 B each): asl `9234a5c9ae3b253c18283def8693919b6a12c372982264e3f63ccc94b70e33bb`,
  eto `37527cdf44a74db84cbb6ed0ae5b0d3c79b6c7dc6f14e6acf008417c958d9a4d`,
  eppo `5028c9d16493b5c84afd38decb5cfceae1239e8cc97794307ddb1ed6179c010a`.
- **Post-place utilization** (`*_utilization_place.rpt`): Slice LUTs 50,265 /
  50,245 / 50,128 of 63,400 (79.3% at most), registers 58,796 / 58,795 /
  58,795, slices 15,829 / 15,833 / 15,844, BRAM tiles 92.5, DSP 14. Against
  the STOP-head sweep (`d352bbaa`): +54 / +42 / +120 LUTs and +53 / +52 / +53
  registers, in line with C1's out-of-context +93 LUT / +57 FF. No sweep with
  this base's inputs exists, so a matched delta against the base is not
  claimed.

## Native service and capture

PR #609's recipe (`run_native.py`, its runner with this lane's root, head,
pin and scratch, no `taskset`, and at most six simulations beside the
serialized builds under this session's 12 GiB cap; `run_capture_native.py`,
PR #609's with this lane's root). Arguments, environment and STOP conditions
are PR #609's.

- **First run, at `b61f1d3c`** (before commit 20): stopped by the 8x8
  `queued-short` arm's two stretch findings, the reason for commit 20 (see
  "The service grader under the AEM-first order"). Retained in
  `native-b61f1d3c/` (`native-commands.json` SHA-256 `bb571a35...`).
- **The bank, at `18199bacae847f8f3c1a31ee9b62d0086c8abf41`**, 20:17 to 22:48
  CEST: `ALL NATIVE MEASUREMENTS COMPLETE: 25 arms`, 65 commands (25 builds, 25
  measurements, 15 immediate regrades), every rc 0, one head, 52,078 command
  seconds (`native-18199bac/native-commands.json` SHA-256 `2b4130c7...`; 138
  retained artifacts, none over 200 KB, `native-artifacts.json` `365c3c6b...`).
  No STOP condition occurred: the worst 8x8 capture is 13.23352 ms (< 24.5 ms)
  and the largest MDIO charge is 1.95488 ms (< 50 ms).

| Group | Arms | Result |
|---|---|---|
| service 8x8 | 6 plans | every plan `PASS: measurement evidence`, 0 service findings, zero unbacked cycles; boot `walk done=1 fail=0 ... closed=0`, the AEM copied before the walk; heartbeat maxima 257.67-304.50 ms |
| service 1x1 | 6 plans | the same; heartbeat maxima 250.46-265.42 ms |
| service mutations | 4 | `remove-dispatch` 1,051 (`queued-builtins`) and 350 (`queued-short`) per-line findings plus backing loss; `late-sample` "PHY initial gigabit negotiation was not published"; `no-publish` "missing publication caught by target simulation" (PR #609's signatures) |
| capture arms | 6 | 16 captures each, every byte and traffic oracle met (table below) |
| capture controls | 3 | `byte-only` 24.29460 to 24.29633 ms, 1.8358x the word path (>= 1.5x); `skip-copy` and `no-traffic` caught by their named oracles |

The only budget findings are the page's measurement-only whole-command
comparison (`milan_nvm` over 500 ms at 8x8), as in PR #609's receipts; the
enforced verdict has none.

Capture figures, 16 captures per arm, 49 ms floor over the arm maximum:

| Shape | CPU MHz | Traffic | ms, min to max | Ratio | Committed before |
|---|---|---|---|---|---|
| 1x1 | 50 | on | 3.87674 to 3.88779 | 12.6036x | identical |
| 1x1 | 50 | off | 3.82856 to 3.83356 | 12.7819x | 3.82856 to 3.84214 |
| 8x8 | 50 | on | 13.21274 to 13.23352 | 3.7027x | identical |
| 8x8 | 50 | off | 13.05048 to 13.07044 | 3.7489x | 13.04976 to 13.06923 |
| 8x8 | 100 (comparison) | on | 9.94496 to 9.95772 | 4.9208x | 9.94138 to 9.95464 |
| 8x8 | 100 (comparison) | off | 9.93764 to 9.94094 | 4.9291x | identical |

The published maxima for both contract points are unchanged (1x1 3.88779 ms,
8x8 13.23352 ms); the non-contract 100 MHz maximum moves to 9.95772 ms.

**The receipt re-record** (commit 21, `597dba85`): `record_capture_receipt.py`
rebuilt `tb/verilator/nvm_capture_cpu/measurements.json` from the six arms:
every graded field is the arm's `measurement.json`, re-graded from its raw
`capture.log` with the harness's grader; every identity is derived from the
build as PR #609's `compare_previous.py` derives it; census, clocks and
harness digests were recomputed and equal the committed ones. Moved: date,
base `18199bac`, tree `2458ac0e`, firmware `a73ecc25...`, processor pin
`b2db3a97`, the instrumented firmware and BIOS digests, the three rows above,
the 100 MHz maximum, the assignment link and the provenance sentence;
unchanged: CPU netlist `c208df0b...`, gPTP microcode and config digests.
`check_nvm_capture.py` rc 0: "PASS: capture census, clocks, both timing arms
and receipt agree", every control detected.

**Documents that quote these figures**: `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md`
section 18 (identities, the three rows) and section 20 item 6 (the 100 MHz
maximum); `docs/findings/397_SERVICE_BUDGET.md`, whose seven tables are
regenerated by `gen_397_tables.py` from the twelve receipts. That generator was
first validated by reproducing all 84 table rows of the page at its previous
measured head, verbatim, from PR #609's retained receipts. The page's header
names the measured head, pin and firmware; restore now carries 42 and 144
backend handshakes (binding and D3 walk); the AEM row is labelled "AEM read to
entity enabled" and its unarmed part is stated.

## Suite and gate table at the head

Head `597dba8593553ad85b1e94936b016907c4d2003a`, clean (`git status
--porcelain --untracked-files=no` empty before and after; the receipt's
`head_after` equal, `clean_after` true), physical path
`$LANES/70-lane2-pin`, every gate run serially by `run_gates.py`
(never piped; stdout and stderr to one log per gate under
`$VALIDATION_STORAGE/a448-gates-597dba85/`, outside this packet; the receipt
`gates-597dba85.json`, SHA-256 `ccc6ba8f...`, records command, rc, seconds, log
size and SHA-256). The pinned Verilator wrapper of the manager's consumer bank
is first on PATH; the Markdown gates run under the pinned environment; the
builder banks under the LiteX interpreter. 34 gates, all rc 0, from 22:50 CEST on
2026-09-29 to 01:02 CEST on 2026-09-30.

| Gate | Command | rc | s | Log SHA-256 |
|---|---|---|---|---|
| `lint_rtl` | `python3 scripts/lint_rtl.py --check` | 0 | 4 | `75be251ed2de` |
| `xvlog_gate` | `python3 scripts/xvlog_gate.py --check` | 0 | 139 | `a10358897cb2` |
| `check_rtl_source_lists` | `python3 scripts/check_rtl_source_lists.py` | 0 | 2 | `b8372555c3e3` |
| `pp_srcs` | `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0 | `fad5e1b9dd5f` |
| `check_port_contracts` | `python3 scripts/check_port_contracts.py` | 0 | 2 | `661d2eaf8202` |
| `measure_naming` | `python3 scripts/measure_naming.py --check` | 0 | 0 | `f9611085771f` |
| `measure_test_evidence` | `python3 scripts/measure_test_evidence.py --check` | 0 | 6 | `ccb36c8d883b` |
| `check_cpp_idiom` | `python3 scripts/check_cpp_idiom.py` | 0 | 1 | `43833ab7c3d7` |
| `check_py_idiom` | `python3 scripts/check_py_idiom.py` | 0 | 4 | `99573b47f33b` |
| `check_feature_status` | `python3 scripts/check_feature_status.py` | 0 | 1 | `802f5eeb2f0a` |
| `check_submodule_docs` | `python3 scripts/check_submodule_docs.py` | 0 | 0 | `dffc750855c2` |
| `submodule_boundaries` | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | 0 | `905777610f39` |
| `check_baremetal_only` | `python3 scripts/check_baremetal_only.py --check` | 0 | 15 | `a0a06c54bb2f` |
| `ci_scope` | `python3 scripts/ci_scope.py --selftest` | 0 | 3 | `50102b9882b9` |
| `integrator_params` | `python3 protocol-processor/scripts/check-integrator-params.py` | 0 | 0 | `aa8920d8ffe7` |
| `diff-check` | `git diff --check 79c36963660c10e4c1c11a744fb5bff41a552b8b HEAD` | 0 | 0 | `e3b0c44298fc` |
| `md-docs_check` | `<md python> scripts/docs_check.py` | 0 | 4 | `c983a535ee13` |
| `md-check_doc_paths` | `<md python> scripts/check_doc_paths.py` | 0 | 0 | `0f9fa704b411` |
| `md-check_doc_style` | `<md python> scripts/check_doc_style.py` | 0 | 0 | `1491d3f6bec0` |
| `md-check_archive` | `<md python> scripts/check_archive.py` | 0 | 0 | `69d45782911c` |
| `md-gen_toc` | `<md python> scripts/gen_toc.py --check` | 0 | 3 | `7bd517fdaeda` |
| `md-check_em_dash` | `<md python> scripts/check_em_dash.py --base 79c36963660c10e4c1c11a744fb5bff41a552b8b` | 0 | 3 | `b135982a46e0` |
| `check_nvm_capture` | `python3 scripts/check_nvm_capture.py` | 0 | 1 | `9a4196c774ce` |
| `fw_service_budget-selftest` | `python3 tb/verilator/fw_service_budget/run.py --self-test` | 0 | 1 | `e2f86b12b29f` |
| `host-firmware-selftest` | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | 68 | `ad6c0b73230d` |
| `builder-present` | `<litex python> -B sw/builder/test_builder.py --require-elaboration --require-rv32` | 0 | 944 | `e322b012ac92` |
| `builder-absent` | `<litex python> -B full-builder-absent.py` | 0 | 656 | `16e22fe9e969` |
| `nvm_cosim-full` | `make -C tb/verilator/nvm_cosim` | 0 | 345 | `5e5eefc1ecdb` |
| `nvm_cosim-lint` | `make -C tb/verilator/nvm_cosim lint` | 0 | 0 | `35289c01eaca` |
| `pp_shadow` | `make -C tb/verilator/pp_shadow -j8` | 0 | 206 | `9e2f8635afaa` |
| `milan_dp_render` | `make -C tb/verilator/milan_dp_render -j8` | 0 | 316 | `abf8e5646dd0` |
| `yosys-portability` | `bash syn/yosys/run.sh` | 0 | 660 | `a685ea0b7068` |
| `milan_dp` | `make -C tb/verilator/milan_dp -j8` | 0 | 1472 | `cedd7d12360b` |
| `milan_dp-ax1x1gptp` | `make -C tb/verilator/milan_dp ax1x1gptp` | 0 | 3065 | `5d38e55c2f08` |
| the five native groups | `run_native.py` (PR #609's recipe) at `18199bac` | 0 | 9,060 wall | `native-18199bac/native-commands.json` `2b4130c7...` |

Readings behind the rc 0 lines:

- `builder-present`: gate 1b reads "it kept the slot of aem_loaded across a
  call under the verdict's three pins, accepted the AEM-first base only with it
  kept, and refused 5/5 planted pin breaks on the verdict, each naming its
  pin"; closes "ALL GATES PASS EXCEPT 1 NOT RUN", the recorded gate-11
  calibration arm (its `mf48` build tree is not on disk), as at `3852b27c`.
- `builder-absent`: "FULL BUILDER ABSENT PASS: all three cross-compiler
  candidates hidden", its recorded compiler-dependent omissions listed.
- `milan_dp` (checks/failures per leg): `gmstep` 104/0 with its mutant
  campaign, `gptp` 182/0, `gptp-lat` 182/0, `obj_dir` 235/0, `notify` 382/0,
  `crflic` 416/0 (the restart check: 3 DUT LeaveAlls after a switch LeaveAll,
  the soonest 10,210 ms after it), `nxn` 1,845/0, `nxndv` 1,847/0, `nxn8`
  3,525/0, `nxn4c` 1,845/0, `nolpf` 235/0, `prune` 33/0, `ax1x1` 232/0, `aclk`
  191/0. Every leg that serves the image reads `[BOOT] PP_STAT the restore walk
  sequenced (done 1, CLOSED 0) = 0x4`.
- `milan_dp-ax1x1gptp`: 139 checks, 0 failures, negative control 0, the walk
  check at both boots.
- `milan_dp_render`: 65/0 and 152/0, and the 5 leg-defect arms.
- `nvm_cosim-full`: 465 checks, 465 PASS; 39 of 39 mutants killed by their
  named check. `nvm_cosim-lint`: 0 `PINMISSING`.
- `pp_shadow`: 606, 606, 646 and 311 checks, 0 failures.
- `check_nvm_capture`: "PASS: capture census, clocks, both timing arms and
  receipt agree", every control detected.
- `fw_service_budget-selftest`: 50 grading checks and 14 flash checks, 0
  failures. `host-firmware-selftest`: five boot paths on all five shapes, both
  planted controls caught.
- `lint_rtl` 90 <= 90; `xvlog_gate`; `check_rtl_source_lists` 107 files, 4 of 4
  consumers, processor 36/42 tops; `measure_test_evidence` 0 unexplained
  DUT-source readers.

## Head and tree

- Head `597dba8593553ad85b1e94936b016907c4d2003a`, tree
  `c0b06e6e3b9a39f8c8f555e89957edf9a920beff`, on dev
  `79c36963660c10e4c1c11a744fb5bff41a552b8b`; 21 commits, each a one-line
  subject with an empty body and no trailer (`git log --format=%b` empty for
  every one). `git status --porcelain` empty (tracked and untracked).
- Gitlinks: `protocol-processor` `b2db3a970cedbbff2f8ba813acb96122c442bc58`
  (checked out, clean, `rev-parse --show-toplevel` is the submodule),
  `gptp-processor` `5dce647a` and `third_party/verilog-axis` `48ff7a7e`
  unchanged from base; `external` uninitialised, as at base.
- Local only: no push, no PR. `origin` is
  `https://github.com/kebag-logic/milan-fpga.git`.

## Packet index

- Comments as posted: `TAKEN.md`, `STOP.md`, `REVIEW-READY.md`; this file and
  `PR-BODY.md`.
- The STOP's evidence: `aem-first-order.patch` (the refused, later landed
  reorder), `logs/gate1b-aem-first-refusal.log`, `logs/bootwalk-dev-base.log`,
  `run_service_probe.py`, `service-probe.json`, `native/` (the STOP-head probe).
- Gate banks: `run_gates.py`, `full-builder-absent.py`; receipts
  `gates-3852b27c.json`, `gates-3852b27c-resume.json` (the STOP head),
  `gates-1b972392.json` (a bank stopped after its light gates when
  `md-check_em_dash` found four pre-existing em dashes in the rows commit 17
  edited; commit 19 fixed them) and `gates-597dba85.json` (the head).
- Native groups: `run_native.py`, `run_capture_native.py`; `native-b61f1d3c/`
  (the first run, stopped by the stretch findings) and `native-18199bac/` (the
  bank: commands, artifacts, every retained log, receipt and spec, gzip-split
  under 200 KB); `record_capture_receipt.py` (the receipt re-record);
  `gen_397_tables.py` (the service page's tables).
- Crflic restart arm: `logs/crflic-restart-arm-d352bbaa.log`.
- Vivado: `vivado_session.sh` and `ooc/` (the STOP head), `ooc_session.sh` and
  `ooc-597dba85/` (the head); `sweep_serial.sh`, `sweep_table.py`,
  `sweep-a448s3852.json` (the STOP head) and `sweep-a448s597d.json` (the head).
- Gate logs, build trees, native scratch and bitstreams stay outside the
  packet; their SHA-256 values are in the receipts and above.
