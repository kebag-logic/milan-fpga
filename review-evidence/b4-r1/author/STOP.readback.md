[A468] STOP

Refs #451, the timing item. Local head `35a8b04da191f5189cb81db455afdbb9ee9b43d6` on `b4-bench-1001`: one commit on dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`, with a one-line subject. It adds `docs/findings/451_TDM8_TIMING_SOC_BOARD.md` and one row in `docs/findings/README.md`. Nothing was pushed, and no PR was opened.

**The timing measurement did not run. It needs the owner.** The SoC board's serial console stands at a login prompt, not a root shell, and this lane holds no credential. None is recorded in the project, so nothing was guessed. A key-based remote login over the SoC board's USB network link was refused, and no password was offered. Every timing step reads the SoC board's own state or records McASP0, so the run stopped before its first SoC board command.

What reached the SoC board: the console tool's readiness probe sent one carriage return and one shell `printf` line, saw the login prompt, and stopped. At a login prompt that line can be taken as a login name. No password was sent, and nothing else reached the console. The SoC board answers on its USB network link, and its USB Audio card is present on the bench host. The bridge state is unknown, because there is no shell to read it.

| #451 timing item | Verdict | Evidence |
|---|---|---|
| Identity gate, dev `ec0cc0c1` | PASS | VERSION `00020060`; AEM CRC32 `93742dd2` (7,352 B); entity `020000fffe000001`; ENTITY (312 B) and CONFIGURATION (106 B) byte-equal to the QSPI AEM bytes; grader 10/10; ROM `acad92b9` (53,344 B); QSPI payload `d178f19a` (3,825,788 B). All equal lane B3's readback |
| Framing: McASP0 configuration and capture parameters | NOT RUN | No shell on the SoC board |
| Bit-exact decode of the DUT's frames, all eight slots, in order | NOT RUN | Same |
| fs and BCLK = 256 x fs from a capture of at least 10 minutes | NOT RUN | Same |
| FSYNC pulse width, edge timing, levels and absolute ppm | Not shown by the SoC board | #626 |

Per-run table: no run was made, so there is no per-run row.

The bench as found shows a DUT reset since lane B3. The NVM reads `backed=1 dirty=0 stale=0 pend=0` with 0 commits, slot B seq 236 authoritative, and `PP_STAT` `5b000444`. All 18 queried stream states were unbound, both DUT maps were empty, and the DUT was on clock source 0 at 48 kHz with SYNC=1, ASCAPABLE=1, TU=0. The controller host had been restarted: its NIC clock read 0 ppb with timestamping off. `SLIP_TDM` rose by 69 in 136.3 s (0.506/s, 10.55 ppm, +-0.15 ppm for one count), in line with the -10.64 ppm plan. That counter is a DUT-side comparison, not a SoC board measurement.

Bench as left:
- **DUT.** Unchanged: read commands only. The census equals the start in 32 of 33 entries; the other is the live propagation delay. Every control word and `PP_STAT` are unchanged.
- **Controller.** No gPTP daemon was started, and the NIC clock and timestamping are as found. The staging directory was removed.
- **SoC board.** No command ran.
- **Bench lock.** Free.

No flash, reset, power, wiring, instrument, USB gadget or UDC action occurred.

Owner item: a root shell on the SoC board's serial console, with the bridge state known. The assignment can then run unchanged. Its 10-minute capture is 921.6 MB, more than the SoC board's temporary storage (209,560 KiB in lane B3's log), so it has to stream off the board as it records.

Validation at `35a8b04d`, all rc 0, unpiped, from the physical `/data` lane path, with the Markdown gates in the pinned Markdown environment:
- `scripts/docs_check.py`;
- `scripts/check_doc_style.py`;
- `scripts/gen_toc.py --check`, plus `--verify-anchors`;
- `scripts/check_em_dash.py --base e4b771f9`: 0 findings over 160 added lines;
- `scripts/check_doc_paths.py`;
- `scripts/ci_scope.py --selftest`;
- `scripts/check_baremetal_only.py --check`;
- `scripts/check_feature_status.py --self-test` (46/46);
- `git diff --check`, and `git diff --check e4b771f9 HEAD`.

The page's four tables and the index table have a constant cell count, rendered and in the source.

Packet `b4-a468` holds the handoff, the PR body, the manifest, the redacted evidence, the tools and the raw-artifact index. No issue closure or review approval is claimed.

