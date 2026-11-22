[A820] TAKEN
Branches:
- milan-fpga `pf-972-1`, new from `dd163e41`, with the tsn-c-stack submodule at its pin `715589c1` and the ADP draws unchanged (the ruling on #970);
- tsn-c-stack, a new branch from main `715589c1` for R887-1-F1.

Round-1 branch `pf-970-1` and tsn-c-stack#35 are not continued.

Authoritative references: #972's acceptance; the [A10] ruling on #970; Milan v1.2 5.6.3.5.2, 5.6.3.5.3, 5.6.3.5.7 and Table 5.50; IEEE 1722.1-2021 6.2.4.2.2 and 6.2.2.16; IEEE 802.3 22.2.4.2.13 and 28.2.4.1.3; #840; #919.

Interpreted scope (milan-fpga):
- The boot path forms the link once. The split's PHY poll stops restarting autonegotiation at every boot whatever the PHY held (`ctrl_plat_phy.c`, THE ADVERTISEMENT). At boot, as after a link loss, the advertisement is still written and read back. Negotiation restarts only when registers 4 and 9 did not hold it. THE OUTCOME check stays as the backstop: a negotiation in force that shares no 1000BASE-T mode is still published down and restarted. So #840's link-speed behaviour is unchanged: 1000BASE-T full duplex only, a 100BASE-TX-only partner gets no link.
- The datapath does not transmit before the firmware has published the link. The poll publishes link down as it arms, right after the CSR identity check and before its first MDIO frame. Today the first publication waits for the first probe's miss, just before READY (27.3 ms after reset at 1x1 in the split boot simulation). Until a poll publishes the PHY's verified link, the datapath therefore sees link down: no gPTP, no mailbox LINK, and ADP starts DOWN instead of drawing a startup delay on the reset value's link.
- Tests: a host test of both paths, restart and no restart, the early publication and the OUTCOME backstop, each with planted defects; the split boot simulation's PHY grade extended to require the arm's publication before any frame, with a plant.
- Salvaged from #970: the grandmaster-order tests (both orders), restated to Milan's literal 4,000 ms and 2,000 ms draws, uniform over their ranges, with their plants.
- The FR_NFR derivation of the declared 6.0 s discovery time, each term cited to its source, and its use where the discovery time is stated.

Interpreted scope (tsn-c-stack): an assertion that GM_CHANGE in WAITING enters DELAY with the 0 to 4 s draw kind (Milan v1.2 5.6.3.5.7), and a planted defect it catches (R887-1-F1). Constants unchanged; the stack's own gates.

Material assumption and open decision: the link-status word's reset value is link up (`milan_soc.py`, MilanMAC `link_status`, kept for builds whose software never writes it). Between the datapath's reset release and the arm's write, about 2.6 ms at 1x1, the datapath still sees the reset value. On a power-up or a REBOOT the PHY has no link in that window, since its reset and autonegotiation take seconds. A gateware reload that keeps the PHY's link could still let one frame out. Closing that window would mean changing the reset value, which is gateware (RTL) and outside this lane. I will measure the window and report it rather than change it.

Validation plan:
- the firmware gate's four shards with the new tests and plants, and `fw_coverage.py`;
- the split boot simulation at 1x1 and 8x8 and its self-test;
- the twin;
- the CPU service-budget rows at 1x1/1if and 8x8/1if, base against head;
- the images at every ledger point, with an image diff;
- the docs workflow steps and both builder legs;
- for the stack: `validate.py --graphs` and `baremetal.py`.

The bench re-run is the manager's, after merge.
Blockers: none.
