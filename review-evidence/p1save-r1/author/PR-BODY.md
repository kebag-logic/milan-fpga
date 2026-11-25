[A844] Give the binding class a 100 ms first-dirty window on the delta-frame save (#1009, #876)

Refs #1009 (the save-policy ruling of comment 7170938286), #876. Not "Closes": acceptance 1 and 3 on the board are
pending (see "Before it lands").

Milan v1.2 5.5.3.5.3 saves the binding parameters before the BIND_RX_RESPONSE and 5.3.8.3 counts the started and
stopped state with them. The store started a whole 1,000 ms first-dirty window after a bind, so a binding was durable
about 1.0 s after its response (1.49 s on the board, with the part's busy time). Binding-class changes now get a
100 ms window; every other class keeps 1,000 ms. Strict save-before-response is #1012.

## The change

`sw/firmware/ctrl_nvm`: the store keeps one deadline, the earliest end of the open windows, a window per class
(`NVM_BIND_DEBOUNCE_MS`, 100 ms for the BINDING block's records: bind, unbind, started and stopped; 1,000 ms for every
other record, DR2a amended for that class only):

- a window starts at its class's first change and is not restarted; a later change of a class brings its end nearer,
  never later, so a binding change inside another record's window ends it 100 ms after itself;
- a save captures everything dirty; a change a running capture takes joins it, a binding change marked while a save is
  in flight opens the next 100 ms window, and any other such change starts the next save at the first idle step, as
  #920 ruled;
- the idle full-room commit keeps a room of two of the largest frames (or half the room, if less): 6 pages at 8x8,
  2 at 1x1 and the Arty shapes.

It builds on the delta-frame save of the same branch (a save writes only the bytes the older slot lacks, as one frame in
that slot's erased room, no erase; `KLJ3` minor 1, `KLD3` frames; a previous-minor container is written whole at its
slot's first save): the two-slot atomicity, blank check and verify are unchanged.

## Measured (save harness, the split CPU running the image's firmware, flash busy times modelled)

`tb/verilator/ctrl_service_budget`, `BUDGET_FLASH_US=120000:500` (erase 120 ms, page program 0.5 ms), calibrated on the
base image's whole save: 1,451.5 ms in the harness, 1.490 to 1.502 s on the board.

| BIND_RX response to durable | 8x8/1if | 1x1/1if | Acceptance |
|---|---:|---:|---:|
| a delta frame | 134.3 ms | 116.1 ms | 250 ms |
| a whole commit | 561.5 ms | 305.2 ms | 800 ms |
| 64 binds, 10 ms apart, the latest | 155.3 ms | 46.9 ms | 250 ms |

The burst is 6 saves at both shapes, every one a frame with no erase, every sink as last commanded at the cut. With the
flash modelled, #920's groups stay within their 5 s: `save-burst` 1,507.9 ms and `save-flight` 964.7 ms at 8x8/1if,
1,230.6 ms and 402.1 ms at 1x1/1if; no budget miss. A swept cut from 0 to 3 s after the response boots old or new at
every cut, never neither, and always the new binding from the gate value on (250 ms for a frame, 800 ms for a whole
commit).

Memory against `dev-soft-core` `5de21ff3` (the platform ledger): +2,432 B of `rom`, +80 B of `sram`, **+0.5 RAMB36 at
every point** (8x8: 59.5 -> 60.0 and 64.5 -> 65.0; 1x1: 45.5 -> 46.0 and 46.5 -> 47.0), the binding window itself
+128 B of `rom`. The ledger records the half tile at both 8x8 points as S14 debt (`sw/litex/ctrl_memory.py`,
`docs/design/SPLIT_CONTROL_MEMORY.md`).

**Ledger:** the size fixture's 8x8 two-interface `declaring-outputs` arm plans 62.5 against its 62.0 entry (128 B of
`rom` over). The entry is raised to 62.5 as S14 debt (6.5 at that fixture point); the routed images add 1.0 tile (8x8/1if)
and 1.5 tiles (1x1/1if) over their base, recorded as S14 debt too. #1012 holds the strict save-before-response order.

## Tests

- `sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32`: PASS, five shapes, 162 checks each;
  `--self-test`: PASS, every planted defect reddened (189), the window's nine among them
  (`test/test_nvm_window.cpp`, 7 checks; `test_nvm_delta.cpp`'s swept cut with the time from which every cut boots the
  new binding: 250 ms for a frame, 800 ms for a whole commit, also after a full room's commit);
- coverage: `nvm_store.c` 679/679 lines, 435/435 branches, 100 % after the nine excluded arcs; `fw_coverage.py --check`
  PASS;
- `tb/verilator/ctrl_service_budget/selftest.py` PASS; `test_ctrl_firmware.py --require-rv32`, `plat_ledger.py`,
  `test_ctrl_memory.py`, the documentation checks PASS.

## Before it lands (the acceptance's board and route items)

- on-board BIND_RX response to durable with the flash's busy time, at 8x8/1if and 1x1/1if (frame <= 250 ms, whole
  commit <= 800 ms); the power-cycle cases with the cut right after the bind's response, one of them on a full-room
  commit: prepared, not run;
- fit and timing: the 8x8/1if and 1x1/1if images are built, signed off (every corner WNS and WHS >= +0.030 ns), routed
  without errors and identity-gated (`receipts/window/images.txt`); 8x8 Slow WNS +0.050 ns, 1x1 +0.185 ns; the 8x8
  two-interface fit is the ledger's (65.0 RAMB36).
