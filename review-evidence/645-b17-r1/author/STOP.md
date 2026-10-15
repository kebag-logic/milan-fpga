[A619] STOP

Head: no commit. Branch `645-b17-bench` is still at dev `f6260253`: the lane stopped before the probe, so there is no findings section and no per-cycle table. Nothing is pushed.

**Why.** The bench's SoC board serial console shows a login prompt, not the root shell the bench rules require. The owner's rule is to stop there: the manager logs in, and no credential is ever typed or stored. The check sent one empty line, which reprinted the prompt, and sent nothing else to the board.

**Done before the stop** (read-only, each under the bench lock):
- **Identity gate: PASS** (07:26:41 to 07:26:47 UTC), 11 of 11 checks:
  - over ATDECC: entity_id `020000fffe000001`, "Milan FPGA 1x1 TDM8", firmware_version `2.96.0`, serial `AX7101-0001`;
  - on the console: `ID=4d494c4e VERSION=00020060`, and AEM CRC `5ba355eb` over 7,512 B;
  - live ENTITY and CONFIGURATION equal the QSPI AEM bytes; CLOCK_SOURCE 0 to 2 present and 3 absent; GET_CLOCK_SOURCE 0; UART grader 10/10.
- **As found** (07:27:44 UTC):
  - the DUT is on CLOCK_SOURCE 0 (INTERNAL), with the servo IDLE;
  - the DUT's STREAM_INPUT 0 is already bound to the reference peer's STREAM_OUTPUT 0 (flags `0x0002`). Both formats are `0205022001006000`, so the binding rule sets nothing;
  - the peer's STREAM_INPUT 0 and 8 hold the DUT's AAF and CRF talkers (`0x0082`), and the peer's clock source is 1;
  - `SLIP_LB` reads `0x000000d0` (208 dups, 0 skips; B15 ended at 152), and `SLIP_TDM` reads 0.

  So the ruling's probe state is the as-found state. A resumed cycle would unbind it, poll for at least 5 s, re-bind and hold for at least 30 s, ending bound as found.
- No bind, unbind, format, clock-source, map or register write was made, on the DUT or the peer. No cycle ran. The controller staging was removed, and the bench lock is free.

**Decision needed** (either one):
1. the manager logs in on the SoC board's console, and the lane then resumes as assigned; or
2. a ruling that B17 runs without the SoC board. The probe does not use the board: there is no tone and no TDM capture, and B14 ran without it under its ruling.

**From TAKEN, for the same ruling if wanted.** B14's settle boundary is the first poll that saw LOCKED, plus 4.096 s, plus 0.5 s (`docs/findings/B14_BENCH_5603C353.md:80`). At INTERNAL the servo reads IDLE, and no bind arms the settle recentre (`docs/design/MEDIA_CLOCK_FOLLOWING.md:1088-1096`, `:1187-1188`). So under B14's definition the boundary is expected to be undefined in every cycle. As stated, I would record it so and STOP on any slip, rather than substitute a boundary.

The handoff (identity records, as-found reads and tools with their origin hashes) is `HANDOFF.md` in the lane's output directory. Stopping here.
