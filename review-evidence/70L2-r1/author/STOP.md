[A448] STOP
Head: `3852b27cfec53b381447780ce581161cc2140c8a` (branch `70-lane2-pin-d352`, local only, 12 commits on dev `79c36963`; processor pin `d352bbaa`).

**Why.** One item of processor PR #132's consolidated list, the firmware's AEM-first boot order (list, Firmware, round 1; `SAVED_STATE_MATERIALIZATION.md` section 5.3 change 1: `configure_fabric`, `load_aem_image`, `nvm_boot`, `entity_advertise`), conflicts with a required gate. The three-line reorder with its ledger fact and order block passes `check_feature_status.py`, but the full builder bank with the RV32 compiler present refuses it in gate 1b (`sw/builder/test_builder.py` `assert_resolved_boot_flow`, `:6634`): "the compiled firmware enters entity_advertise() with [None] rather than with the one value load_aem_image() handed back". The resolver forgets every static symbol slot across a call (`:1627-1630`), `aem_loaded` is a file-scope static stored before `call nvm_boot` and reloaded after it, and the source rules pin that static to one assignment `aem_loaded = load_aem_image();` (`:11308-11317`), no address taken (`:11323`) and one call `entity_advertise(aem_loaded)` (`:11429-11435`). No firmware-only spelling satisfies both. Changing the gate's soundness rule or the contract's order is outside this lane, so per AGENTS.md section 2 I am publishing the conflict for a decision.

**Cost at this head.** The walk starts before the image is in DRAM, so at `d352bbaa` it ends CLOSED (D3 cause 7) on every product boot: listener released, AECP held and ADP dark until reset. A native `service-1x1-all` probe shows it end to end: `walk done=0 fail=1 blank=0 backed=1 closed=1 rolled_back=0 cause=7/0`, `PP_STAT=5b1d0448`, then `AEM 7352 B copied` after the walk; `fw_service_budget/run.py:277` refuses (`walk done=1 fail=0` required). So the five native groups cannot pass and the capture re-measure would measure a held AECP; `check_nvm_capture` is rc 1 ("product firmware changed; remeasure the copy") and is not re-recorded.

**Options (decision needed):**
1. *(recommended)* Gate 1b keeps the `aem_loaded` symbol slot across a call once the source rules have pinned it (one assignment, the verifier's; no address taken; a file-scope static of the one translation unit), with a planted control that a callee writing `aem_loaded` is still refused. The reorder then lands unchanged.
2. Firmware carries the verdict in a local of `milan_init()`: changes the gate's literal anchors (`static int aem_loaded;`, the single assignment) and the UART status's source.
3. Contract: enable before the walk (`load_aem_image`, `entity_advertise`, `nvm_boot`), relying on ADP taking `entity_enable && restore_done`; changes section 5.3 change 1 and the ledger order.

**Everything else is done at this head.** Items 1, 2 (the list minus the boot order), 3 (every boot path starts the walk, the persistence-disabled path blind; `test_boot_walk.py` fails 9 checks on the dev firmware and catches both planted controls) and 4. Gates at the head, rc 0 unless stated:
- builder bank with the RV32 compiler present and with every candidate hidden;
- `milan_dp`, every leg (the image legs read `[BOOT] PP_STAT ... (done 1, CLOSED 0)`, the image-less legs CLOSED), `ax1x1gptp` 139/0, `milan_dp_render`;
- `nvm_cosim` 465/465 with 39 of 39 mutants killed, its lint, `pp_shadow`;
- firmware host tests on all five shapes; yosys, lint, `xvlog`, source-list, port-contract, naming, evidence-classifier, idiom, feature-status, submodule and diagram gates; the Markdown gates in the pinned environment;
- `check_nvm_capture` rc 1, and the five native groups not run: both are the block above.

**Timing and area (item 5): the floor holds, no STOP.** 3-seed AX7101 1x1 TDM8 sweep at the head (PR #615's recipe, 32 threads, seeds run one at a time under the Vivado lock), worst over the four declared corners:

| Seed | Worst WNS ns | Worst WHS ns | #607 refusal gate |
|---|---|---|---|
| AltSpreadLogic_high | +0.174 | +0.028 | accepted |
| ExtraTimingOpt | +0.247 | +0.032 | accepted |
| ExtraPostPlacementOpt | +0.070 | +0.058 | accepted |

TNS and THS are 0; each log has 0 critical warnings, 0 of 12-4739/20-1307/12-5201 and 112 quasi-static cells. Post-place is at most 50,211 of 63,400 LUTs. Out-of-context `KL_pp_shadow` at 1x1: 25,623 LUT / 25,881 FF, of which the D3 writer is 913 / 488. Firmware: +263 B of text against the base firmware, same toolchain.

Packet: HANDOFF.md and PR-BODY.md in the lane's packet (per-item file:line, the refusal log, the reorder patch, the probe's UART log, the sweep table). No push, no PR. After the ruling the lane needs one firmware commit (plus a builder commit under option 1), then at that head the gate bank, the five native groups, the capture re-measure and `check_nvm_capture`, and the sweep again (the firmware is in the bitstream's BIOS ROM).
