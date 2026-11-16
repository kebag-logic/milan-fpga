[A792] REVIEW READY
Commit: `37255683`, branch `929-base-gates`: five commits on dev-soft-core `70f4056f` (`08ba6efa`, `6b8e5042`, `becca95f`, `a9a48546`, `37255683`). Not pushed; the manager pushes and opens the PR.

Reproduced at `70f4056f` on clean clones, then fixed at the cause:
1. **Twin, owed row `split-talker-failed`** (`make -C tb/verilator/milan_dp twin` exit 2: "owed row split-talker-failed does not hold").
   - The row owed the split's Talker Failed from boot, caused by "no SRP adapter entry takes MAAP's allocation".
   - #895 added that entry (`srp_mbx_allocation`). At the base the split declares no Talker Failed in this stimulus. Its Talker Advertise for STREAM_OUTPUT 0's stream runs from 5190 ms to its Leave at 20190 ms (the fabric's: 5200 to 20000 ms). Both halves pass the Table 10-3 grade, and the remaining count differences come from each half's own timers.
   - The owed difference has gone, so the row is deleted, as the twin's rule asks.
   - #932 does not move this: at its head `09a948d4` both twin captures are byte-identical to the base's.
   - Plant `talker-failed-back` (new) re-encodes the split's Advertise as Talker Failed, code 2, and is refused by name. The words of `srp-plus-k` and `leave-all-declaration` are restated to the findings that now refuse them.
2. **`dynmap-mutants`, listener control on a fresh clone** ("[FAIL] the unmutated gateware does NOT pass the listener leg (caught)").
   - The leg builds keep their generated inputs with `-o`, and a fresh clone has never made `milan_dp_render`'s `ltn_rom.hex`, `ucode.hex` or `tdm8r_aemi.bin` (nor `capture_coherence`'s two).
   - The campaign now makes each selected leg's inputs through that suite's own rules before its control, and refuses a leg whose inputs are absent.
   - Plants on a fresh clone, each caught by name: make skipped ("[FAIL] the listener leg's inputs are not made: its suite did not make ltn_rom.hex, ucode.hex, tdm8r_aemi.bin"); the step removed (the base's failure back).
3. **`srp_mbx.cpp` at the 8x8 entity**: `StartupDeclaresTalkersDomainAndVlan` (8x8, one and two interfaces) and `OneLoopOwnsTheGlobalCentisecondDispatch` (8x8, two interfaces) failed.
   - Both tests were written for the 1x1 entity's two sources; the 8x8 entity has nine.
   - The firmware follows its rule (Advertise when allocated and admitted, else Failed with code 2 when unallocated; IEEE 802.1Q-2018 35.2.2.8.7, Table 35-6), so these were test defects:
     - the startup test now holds each source by its own StreamID;
     - the dispatch test's two adapters now share two of the shape's SRP pools (a 1x1-sized pool refused the second `srp_mbx_init`).
   - `srp_mbx.cpp` now runs at 8x8 at both interface counts in `firmware-unit`.
   - Three new 8x8 plants in the two-interface campaign, each caught by name: `startup-8x8-sources-past-two-undeclared`, `startup-8x8-failure-code-past-two`, `duplicate-tick-owner-8x8`. The first two escape at 1x1, so only the 8x8 arm catches them.

Validation (clean clones of `37255683` unless named):
- `make -C tb/verilator/milan_dp twin`: rc 0, 0 findings. `twin-plants`: rc 0, 21 plants refused both ways, none escaped.
- `make -C tb/verilator/milan_dp dynmap-mutants DYNMAP_MUTANT_JOBS=8` from a fresh clone: rc 0, every leg's control `[PASS]` (the listener's included), `71 checks: 71 PASS, 0 FAIL` (66 of 66 mutants caught).
- Workflow replays, step by step, each job on its own fresh clone: 88 steps rc 0, 56 hosted-only steps not run with their reasons, 0 bad.
  - rtl-fast: `changes`, `firmware-unit`, `firmware-srp-mutants`, `firmware-control-mutants`, `firmware-aecp-mutants`, `firmware-boundary`, `firmware-verilator`, `split-cdc`;
  - docs: all six jobs.
  - Within `firmware-unit`, `test_ctrl_firmware` PASS (four `srp_mbx` arms `[ok]`, 1x1 and 8x8) and `firmware coverage: PASS (39 files)`. The SRP campaign: 424 caught, 0 escaped (the base's 421 plus the three 8x8 plants).
  - `firmware-boundary` ran with the LiteX packages the hosted job installs. A first replay without them refused at `sw/litex/test_ctrl_memory.py` (no `migen`), an environment gap; its logs are kept.
- Images:
  - The release image is byte-identical to the base's: `bios.bin`, the disassembly and the debug-stripped ELF at both configs. Only the ELFs' debug sections differ, by the clone path.
  - No split image changes: `plat_ledger` PASS at all four points, and every point's ELF, stripped ELF and loadable binary are identical to the base's.
- The sweep's milan_dp suite: its make database differs from the base's only in `TWIN_CAPTURE_PLANTS`, so every swept recipe is unchanged. The native sweep was not run.

Acceptance criteria (#929): each of the three gates passes from a clean clone of the head, as above.

Open risks/questions:
- `stream-output-0-notices` (twin) still holds by its values, but its stated cause was stale since #895. It now reads: the split's Talker declares and withdraws, and no GET_STREAM_INFO notice of STREAM_OUTPUT 0 is sent at either change (Milan v1.2 5.4.5.2, Table 5.22). No issue owns that notice; it needs one.
- The twin compares Talker declarations by type and StreamID, not TSpec, and the halves' MaxFrameSize differs: 217 for the split (Milan v1.2 4.3.3.2 Table 4.4 at 8 channels), 73 for the fabric (the same formula at 2).
  - The twin builds both datapaths at `TALKER_WIRE_CHANS_P` 2, where the shipping AX shape uses 8, and the fabric's source 0 declares its `LWSRP_TSPEC` word. Which of the two sets the 73 is not diagnosed.
  - The deleted row pinned each half's value but never compared them. This needs an issue.
- The milan_dp README's SRP-transmit section still describes the boot-time Talker Failed from before #895; not changed here.
