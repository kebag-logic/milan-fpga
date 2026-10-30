[A700c] REVIEW READY
Commit: `667b9bbc02b99a08d71efab750f95e8702cbbe57` (branch `787-reboot-reset`, on `0d4be94c`, base dev `1e80128f`; not pushed). Processor pin: `a9e84b66`, the merge commit of processor PR #209 (#203). It merged during this round, and its tree is the reviewed head `013ee63f`'s.

Changed:
- **The silicon defect** (issuecomment-6518083444). `KL_reboot_ctrl` held the PHY in reset two clocks after `reboot_req_o`, while ENTITY_DEPARTING was still in the SoC's MAC (`mac_tx_cdc`, `tx_sf`, LiteEth's crossing and pipeline, the PHY stage). The cause is confirmed by test: `pp_shadow` `[RB]`, graded at a MAC model's wire-side output, fails 10 of 69 on the unfixed RTL with the DEPARTING lost in the MAC.
- **The fix.** A new EGRESS phase between the saved-state drain and the PHY hold. An account from reset counts frames in at the datapath's MAC port and out at the MAC's PHY interface. The phase ends on a tick once nothing is half taken at the port and nothing is in the MAC, and the path has stayed so since the previous tick (a whole quiet millisecond for the PHY's own transmit path), or at its bound.
- **Signal used.** Frames are counted in on the datapath's own `m_axis_mac_tx` handshake (the RMON tap). They are counted out on a new reset-less toggle, `ethtxend_tgl`, which `MilanMAC` flips on each frame's last octet at LiteEth's `phy.sink`: the GMII/MII transmit stream one register stage before the pads, the seam `KL_gptp_gmii_launch` already reads. It arrives as `i_ethtxend_tgl`, toggle plus three-flop sync. Everything is parent code; there is no submodule change.
- **The bound, derived and not mirrored.** `T_EGRESS_MS_C` = ceil(octets x 8 / slowest rate) ms + the quiet ms. The SoC's `_mac_tx_egress_octets` computes the octets from the named depths its FIFOs are built with: every transmit buffer, each buffered frame's framing, and one maximum envelope frame (IEEE 802.3-2022 3.2.1, 3.2.2, Table 4-2). That is 11,656 octets, giving 2 ms on the AX7101 at 1 Gb/s and 11 ms on the Arty at 10 Mb/s. The builder evaluates the same definitions, so gate 23m holds the Instance to them.
- **The bound restated.** From `reboot_req_o` to the IPROG word: drain + egress + hold + 3 ms + 8 clocks. That is 13,505 ms on the AX7101 (13,502 before), 13,514 ms on the Arty, and 13,531 ms at the datapath default.
- **The MAC port is not gated.** A first version stopped it during the wait, but builder gate 1b holds the MAC handshake direct (the gPTP plane's direct path, #187), so the stop was removed rather than the check. Every frame the REBOOT owes was handed over before the request, so the account already holds it.
- **The re-pin** to the merge commit: ROM ledger rows (byte-identical digests) and the boundary diagram through their generators, plus the pin table.

Validation (each in a clean clone; receipts in the handoff):
- Full sweep, 4 shard units at `e12147d4`: 65 of 65 suites, 2,192,196 checks, 0 failures; `reboot_ctrl` 298, `pp_shadow` 2,514.
- rtl-fast replica at `e12147d4`: success, 12 of 12 jobs; behave 14 features, 508 scenarios. Yosys at `e12147d4`: 61 of 61 tops; `KL_reboot_ctrl` 245 cells.
- At the head `667b9bbc`:
  - the static and pin-record bank, 32 of 32, with the builder bank ALL PASS except 2 arms this host cannot exercise;
  - the docs workflow, 44 steps, 0 failed;
  - the campaigns: `make -C tb/verilator/reboot_ctrl` (221 + 46 checks, 30 of 30 mutants killed), `[RB]` (68 checks), `make -C tb/verilator/pp_shadow reboot-mutant` (6 of 6), the #396 planner (123 tests) and its behave feature (189 scenarios), the UART smoke, the LiteX simulations (7 of 7) and `gen_mac_tx_model.py --check`.
- From `e12147d4` to the head only a mutant driver, three documents, the pin records and the gitlink (identical tree) change, and every gate that reads them ran at the head.

Acceptance criteria, issuecomment-6518083444:
- (1) met: no PHY hold and no IPROG wait until every frame given to the MAC has reached its PHY, within the derived bound; the 13,502 ms bound is restated.
- (2) met: `[RB]` at the wire side shows SUCCESS, the notification and ENTITY_DEPARTING whole and in order before the PHY hold, which follows the request. Without advertising there is no DEPARTING, and the hold waits for the last started frame. With a dead transmit clock the hold comes at the bound.
- (3) met: the PHY hold on the request alone, a drain that ignores the MAC FIFO, and a drain with no bound are each killed in `[RB]` and in `reboot_ctrl` by their named checks.
- (4) met: the re-pin round as assigned. The early-request arm is killed by "the PHY hold follows the processor's REBOOT request".

Open risks/questions:
- No Vivado this round, by the assignment. The shipping build gains about 41 LUTs and 14 FFs (Yosys `synth_xilinx`), so the post-#814 route must confirm slices and timing, and xvlog runs then.
- The bench decides the end-to-end claim: the DEPARTING on the wire, then the 50 soft resets.
- A frame another source starts on the clock the wait ends is lost with the reset, as at a cut.
