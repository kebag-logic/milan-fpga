[A681] STOP (owner decision D4: the measured rows miss T_svc = 10 ms)

Head: `d58c8e22e9bd96237b9a28ea1ddd55b0426380c4` on `665-s2-cpu-budget`, one commit on `dev-soft-core` `e76a755a`. It is not pushed; the manager pushes. The PR targets `dev-soft-core`.

Changed: new files under `tb/verilator/ctrl_service_budget/` only. No shipping RTL, SoC, firmware, CI or workflow file changed.
- A test-only SoC: the shipping cacheless VexiiRiscv (CPU at 50 MHz, bus at 100 MHz), `CtrlMemory`, and the harness's own `KL_mbx` behind `KL_mbx_wb`, driven from the testbench.
- It runs `ctrl_srp_image.py --with-aecp --layout split` unmodified.
- Every figure is an observed clock count, graded against FR_NFR 3.4.1. The README carries the full tables.

**Measured** (arm A, the image as linked; 1x1 is one interface, 8x8 is two)

| Figure | 1x1 | 8x8 |
|---|---|---|
| Mailbox read / write | 9 / 9 CPU cycles (0.18 us) | same |
| BRAM fetch / flash-window read | 9.1 / 263 CPU cycles | same |
| Fetch share of CPU bus transactions | 0.86 to 0.89 | 0.85 to 0.89 |
| Idle pass | 1.31 to 1.45 ms | 2.04 to 3.71 ms |
| Worst pass | 31.04 ms | 59.79 ms |
| Composed maximum | 27.83 ms | 42.82 ms |

| Backlog row (`MAILBOX_SPLIT.md:753-758`), ms | 1x1 | 8x8 |
|---|---:|---:|
| an event behind 15 others | 14.12 | 40.51 |
| an ACMP command behind a full acmp ring | 60.35 | 101.98 |
| an ENTITY_AVAILABLE behind a full adp ring | 43.90 | 48.63 |
| a response with 7 frames owed ahead | 75.76 | 98.93 |

T_svc misses: 10 of the 1x1 probes and 44 of the 8x8 probes. Every probe was measured.
- 1x1: the ADP rows fit (0.08 to 0.87 ms). AECP takes 2.5 to 6.2 ms, and SRP and MAAP fit.
- 8x8: LINK_UP (32.5 / 41.7 ms), LINK_DOWN (18.4 / 26.8 ms), SRP startup, MAAP's first PROBE and one AECP GET_CONFIGURATION (14.8 ms) miss.
- ACMP misses mostly through AECP's change-notice retry, below.

A labelled second arm answers the fixture's four observation callbacks (test code only). With it:
- every ACMP path fits at 1x1 (0.19 to 1.94 ms) and at 8x8 (up to 5.8 ms);
- the composed maximum is 13.70 ms (1x1) and 26.04 ms (8x8);
- the ADP-ring row is 7.90 / 15.28 ms;
- the other backlog rows are unchanged.

**Decision input**
- D4: per-pass CPU work, not mailbox accesses, sets the time. The consumers, in order:
  - byte-loop `memset` and `memcpy` (each AECP response zeroes its 1,514-byte frame, `aecp.c:58`, and 1,476-byte payload, `aecp_commands.c:555`: about 154,000 cycles per READ_DESCRIPTOR pass);
  - lwSRP `mrp_mad` at link-up (474,000 cycles at 8x8);
  - the two AECP polls (47,000 cycles of every 1x1 pass, 94,000 at 8x8);
  - software multiply and divide.
- The admitted backlog is already min(burst, ring room): 8 ADP, 12 GET_RX_STATE, 16 AECP and 7 MAAP records. A smaller backlog cannot shorten a single 40 ms pass.
- The #397 one-hart rule fails: a pass is the only tick opportunity, and single passes reach 31 ms (1x1) and 60 ms (8x8).
- AECP retries each pending change notice every 1 ms with no backoff while a port reports unavailable (`aecp.c:461-495`). After a bind, every 1x1 pass costs 21 to 31 ms.
- D5: the shipping core already misses at both points.
- D3 / S14: a flash-window read costs about 29 times a BRAM fetch on the product's 1x SPI, and the core is fetch-bound, so no T_svc path can fetch from flash. The image fetches 11.2 to 11.4 KB of code before the mailbox opens and at least 40.5 KB (1x1) / 43.1 KB (8x8) after it.

**Defects found, each for a new issue**
1. The CPU generator decodes a region whose size is not a power of two wrongly.
   - For the split SoC's 224 KiB `rom` it emits `(address & 0xfffc8000) == 0`, and the shipping split region list produces the same decode.
   - The split image takes an instruction access fault at its first call above 0x8000 and reboots forever.
   - The harness hands the generator power-of-two covers. Its netlist differs only in decode lines, and `--cpu-regions as-built` reproduces the fault.
   - This needs fixing before M8a-2's boot.
2. The linked image addresses placeholder devices: mailbox 0x80000000, LiteSPI master 0xf0003000, timer0 0xf0003800, flash 0x20000000. The test SoC places its devices there. S3 owns the real addresses.
3. #723 is still open. The harness adds `-fno-stack-protector` to the runtime recipe's compiles, and changes nothing else.

**Validation** (all rc 0 at the head, foreground, unpiped)
- `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test`: 19 checks, and 12/12 marker, clock-ratio and deadline mutants caught, each by a named check. The checks include a planted over-budget path.
- The planted slow ADP handler (`--mutation slow-adp-rx`) measures 24.614 ms, against 0.294 ms unplanted: `CONTROL slow-adp-rx caught`.
- `--cpu-regions as-built`: `CONTROL as-built caught: an instruction access fault (cause 1)`.
- Both points and the second arm were regraded at the head, byte-identical to the measuring runs. A rebuild at the head gives byte-identical native models.
- `cd tests && behave`: 406 scenarios.
- The docs gates (`docs_check`, doc paths, doc style, archive, em dash with base `e76a755a`, `gen_toc`), the Python and C++ idiom gates with their self-tests, hygiene, TODO ownership, the SoC and RTL source lists, and `git diff --check`.

**Acceptance:** met, except two items.
- The ADP SHUTDOWN row has no input in the fixture and is not measured.
- The rows miss T_svc. That is this STOP, so the PR body says "Relates to #665".

**Open risks/questions**
- Each probe measures one phase, so each also reports a pass bound.
- Ends are mailbox commits; wire time is not included.
- Flash program waits are zero.
- No CI job runs the self-test, because registering it is a CI change outside this lane.

HANDOFF, PR body and receipts, with a generated index, are in the evidence packet.
