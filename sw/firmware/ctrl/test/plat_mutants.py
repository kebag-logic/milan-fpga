# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""plat_mutants.py - the split platform's planted defects (#665), in the control campaign's table.

ctrl_mutants.py plants each into a copy of sw/firmware/ctrl and requires the
named GoogleTest test of the named arm to fail on the check's own words
(ctrl_mutants.campaign). The arms are plat_arms.py's: `plat` (the CSR window,
the console, the MMIO platform), `platboot1` and `platboot2` (the boot at one
and two interfaces). The CSR initialisation's trace against milan_baremetal.c
carries its own three plants (plat_trace.py).

The table holds the platform's named controls: a CSR write skipped, reordered
or wrong, caught by the write list; a console that blocks past #397's tick
rule (input or output past its per-pass slice, a write into a full FIFO, a
command run without room), caught by the pass bound; a console that reads past
a command's terminator, caught by AddressSanitizer in the test that sent the
line; the boot's order of Milan v1.2 5.6.1, caught by the step order, the
saved state's place among the steps by the flash's accesses in that order;
and the saved state's write-back, caught by a bind after ready reaching the
flash.
"""
from __future__ import annotations

#: The test files whose every test a defect here must name.
SOURCES = ("test_plat.cpp", "test_plat_mmio.cpp", "test_plat_boot.cpp", "test_plat_phy.cpp")
CSR = "plat/ctrl_plat_csr.c"
CONSOLE = "plat/ctrl_plat_console.c"
PLAT = "plat/ctrl_plat.c"
PHY = "plat/ctrl_plat_phy.c"
C2 = "Plat.C2PolicyIsConfigureFabricsFifteenWritesInOrder"
K4 = "Plat.K4EachPassIsBounded"


#: The reorder plant's two writes, as ctrl_plat_csr.c holds them and swapped.
EID = ("\twr(csr, CTRL_PLAT_CSR_ADP_EID_LO, p->entity_id_lo);\n",
       "\twr(csr, CTRL_PLAT_CSR_ADP_EID_HI, p->entity_id_hi);\n")
#: Steps 6-7 and the open, as ctrl_plat.c holds them: the saved state's boot, its service's binding, the mailbox.
SAVED = "\tnvm_store_boot(env->flash, &p->binding.port);\n"
TICK = "\t(void)ctrl_loop_add_tick(&p->app.loop, nvm_store_tick);\n"
STEP = "\t(void)ctrl_loop_set_step(&p->app.loop, ctrl_plat_phy_store_step, &p->phy, nvm_store_clock, NULL);\n"
SERVICE = TICK + STEP
OPEN = ("\tif (!ctrl_app_open_held(&p->app, &p->config)) {\n"
        "\t\treturn reach(p, CTRL_PLAT_MAILBOX, \"Milan split: mailbox contract mismatch; entity disabled\\r\\n\");\n"
        "\t}\n")


def mutants(mutant: type) -> tuple:
    """The table, built with the campaign's Mutant (ctrl_mutant.py)."""
    return csr_mutants(mutant) + console_mutants(mutant) + boot_mutants(mutant) + phy_mutants(mutant)


def csr_mutants(mutant: type) -> tuple:
    """The CSR window's: a CSR write skipped, reordered or wrong, the identity and the time of day."""
    m = mutant
    return (
        # the CSR initialisation: skipped, reordered, wrong
        m("plat-policy-write-skipped", CSR, "\twr(csr, CTRL_PLAT_CSR_LWSRP_VID, p->sr_vid);\n", "",
          "plat", C2, "C2 configure_fabric's writes, in its order, from the policy"),
        m("plat-policy-writes-reordered", CSR, EID[0] + EID[1], EID[1] + EID[0],
          "plat", C2, "C2 configure_fabric's writes, in its order, from the policy"),
        m("plat-policy-word-wrong", CSR, "p->lwsrp_ctrl_reset | CTRL_PLAT_LWSRP_LIVE", "p->lwsrp_ctrl_reset | 0x2u",
          "plat", C2, "C2 configure_fabric's writes, in its order, from the policy"),
        m("plat-policy-advertiser-left-on", CSR, "rd(csr, CTRL_PLAT_CSR_ADP_CTRL) & ~1u",
          "rd(csr, CTRL_PLAT_CSR_ADP_CTRL) | 1u", "plat", C2, "C2 no fabric advertiser beside the core"),
        m("plat-identity-unchecked", CSR, "return id == CTRL_PLAT_MILAN_ID;", "return id != 0u;",
          "plat", "Plat.C1IdentityIsMilnAndReadsVersion", "C1 any other ID is refused",
          also=(("platboot1", "Boot.B2ForeignWindowStopsAtIdentity", "B2 a foreign window stops the boot"),)),
        m("plat-status-pair-high-first", CSR,
          "\ts->gm_lo = rd(csr, CTRL_PLAT_CSR_GM_LO);\n\ts->gm_hi = rd(csr, CTRL_PLAT_CSR_GM_HI);\n",
          "\ts->gm_hi = rd(csr, CTRL_PLAT_CSR_GM_HI);\n\ts->gm_lo = rd(csr, CTRL_PLAT_CSR_GM_LO);\n",
          "plat", "Plat.C3StatusIsReadInMilanStatusOrder", "C3 each pair low then high"),
        m("plat-tod-no-snapshot", CSR, "\twr(csr, CTRL_PLAT_CSR_PTP_CMD, CTRL_PLAT_PTP_SNAPSHOT);\n", "",
          "plat", "Plat.C4TimeOfDayIsSnapshotThenAgreeingHighWords", "C4 the snapshot strobe comes first"),
        m("plat-tod-torn-accepted", CSR, "if (rd(csr, CTRL_PLAT_CSR_TOD_RD_HI) == hi) {",
          "if (rd(csr, CTRL_PLAT_CSR_TOD_RD_HI) == hi || true) {",
          "plat", "Plat.C4TimeOfDayIsSnapshotThenAgreeingHighWords", "C4 the agreeing high word"),
    )


def console_mutants(mutant: type) -> tuple:
    """The console's: its lines, its numbers, and a duty that holds the pass past #397's tick rule."""
    m = mutant
    return (
        # the console's lines
        m("plat-status-aem-inverted", CONSOLE, "c->aem_loaded ? \" AEM=loaded\\r\\n\" : \" AEM=disabled\\r\\n\"",
          "c->aem_loaded ? \" AEM=disabled\\r\\n\" : \" AEM=loaded\\r\\n\"",
          "plat", "Plat.K1MilanStatusAnswersTheGradersLines", "K1 milan_status's lines, field for field"),
        m("plat-tod-torn-printed", CONSOLE, "\t\tctrl_plat_console_puts(c, \"TAI_NS=none\\r\\n\");\n",
          "\t\tctrl_plat_console_puts(c, \"TAI_NS=0x0000000000000000\\r\\n\");\n",
          "plat", "Plat.K2MilanGettimeAnswersTaiNs", "K2 a torn read prints no number"),
        m("plat-prefix-is-a-command", CONSOLE, "return n == c->len && command[n] == '\\0';", "return n == c->len;",
          "plat", "Plat.K3LinesEndOnceAndOthersAreRefused", "K3 a prefix is no command"),
        m("plat-overflow-kept", CONSOLE, "\t\tc->discarding = true;\n\t\tc->len = 0;\n", "\t\tc->len = 0;\n",
          "plat", "Plat.K3LinesEndOnceAndOthersAreRefused", "K3 an overflowed line is dropped whole"),
        # a NUL where a command's name ends, compared past the command's terminator: AddressSanitizer's report
        # aborts the run, and the harness names the test the line was sent in
        m("plat-command-read-past-its-end", CONSOLE,
          "while (n < c->len && command[n] != '\\0' && command[n] == c->line[n]) {",
          "while (n < c->len && command[n] == c->line[n]) {",
          "plat", "Plat.K3LinesEndOnceAndOthersAreRefused", "crashed on signal 6"),
        m("plat-dec-leading-zeros", CONSOLE, "if (digit != '0' || !leading || tens[k] == 1u) {",
          "if (digit != '0' || leading || tens[k] == 1u) {",
          "plat", "Plat.K6NumbersAtTheirEdges", "K6 no leading zeros"),
        m("plat-hex-seven-digits", CONSOLE, "for (int shift = 28; shift >= 0; shift -= 4) {",
          "for (int shift = 24; shift >= 0; shift -= 4) {",
          "plat", "Plat.K6NumbersAtTheirEdges", "K6 eight lower-case digits"),
        m("plat-ring-drop-uncounted", CONSOLE, "\t\t++c->dropped;\n", "",
          "plat", "Plat.K5TextPastTheRingIsDroppedAndCounted", "K5 the ring holds TX_BYTES and drops the rest"),
        # the console's bound: a duty that holds the pass past #397's tick rule
        m("plat-tx-unbounded", CONSOLE, "for (unsigned n = 0; n < CTRL_PLAT_TX_PER_PASS && c->head != c->tail; ++n) {",
          "for (unsigned n = 0; n < CTRL_PLAT_TX_BYTES && c->head != c->tail; ++n) {", "plat", K4,
          "K4 at most TX_PER_PASS bytes out"),
        m("plat-rx-unbounded", CONSOLE, "while (taken < CTRL_PLAT_RX_PER_PASS && !c->waiting) {",
          "while (!c->waiting) {", "plat", K4, "K4 at most RX_PER_PASS bytes in"),
        m("plat-tx-into-full-fifo", CONSOLE,
          "\t\tif (ctrl_plat_io_read32(c->uart.txfull) != 0u) {\n\t\t\tbreak;\n\t\t}\n",
          "\t\t(void)ctrl_plat_io_read32(c->uart.txfull);\n", "plat", K4, "K4 never into a full FIFO"),
        m("plat-command-without-room", CONSOLE, "if (c->waiting && room(c) >= CTRL_PLAT_RESPONSE_MAX) {",
          "if (c->waiting) {", "plat", K4, "K4 a command runs only with room for the longest response"),
        m("plat-input-while-waiting", CONSOLE, "while (taken < CTRL_PLAT_RX_PER_PASS && !c->waiting) {",
          "while (taken < CTRL_PLAT_RX_PER_PASS) {", "plat", K4, "K4 no input is taken while a line waits"),
        m("plat-slice-not-owed", CONSOLE,
          "return c->waiting || taken == CTRL_PLAT_RX_PER_PASS || c->head != c->tail;",
          "return c->waiting || c->head != c->tail;", "plat", K4, "K4 a full slice of input is owed another pass"),
        # the MMIO platform
        m("plat-mmio-read-neighbour", "plat/ctrl_plat_mmio.c", "return *(volatile uint32_t *)address;",
          "return *((volatile uint32_t *)address + 1);",
          "plat", "PlatMmio.I1ReadIsTheWordAtTheAddress", "I1 a read returns the word at the address"),
        m("plat-mmio-write-neighbour", "plat/ctrl_plat_mmio.c", "*(volatile uint32_t *)address = value;",
          "*((volatile uint32_t *)address + 1) = value;",
          "plat", "PlatMmio.I2WriteIsTheWordAtTheAddressAlone", "I2 a write lands in the word at the address"),
    )


def boot_mutants(mutant: type) -> tuple:
    """The boot's: its order (Milan v1.2 5.6.1), each stage's refusal, and the platform's ports."""
    m = mutant
    return (
        # the boot's order (Milan v1.2 5.6.1, ARCHITECTURE_HW_SW_SPLIT.md section 2)
        m("plat-adp-before-aecp", PLAT,
          "\tif (!ctrl_app_open_aecp(&p->bridge)) {",
          "\tctrl_app_release_adp(&p->app);\n\tif (!ctrl_app_open_aecp(&p->bridge)) {",
          "platboot1", "Boot.B1ReachesReadyInStepOrder", "B1 ADP's first timer after the face commit",
          also=(("platboot1", "Boot.B6UnacknowledgedFaceStopsAtAecp", "B6 ADP never starts"),)),
        m("plat-adp-not-held", PLAT, "\tif (!ctrl_app_open_held(&p->app, &p->config)) {",
          "\tif (!ctrl_app_open(&p->app, &p->config)) {",
          "platboot1", "Boot.B1ReachesReadyInStepOrder", "B1 ADP's first timer after the face commit"),
        m("app-adp-hold-ignored", "app/ctrl_app.c", "\tadp_mbx_set_enable(&app->adp, !app->adp_held);\n",
          "\tadp_mbx_set_enable(&app->adp, true);\n",
          "platboot1", "Boot.B1ReachesReadyInStepOrder", "B1 ADP's first timer after the face commit",
          also=(("platboot1", "Boot.B6UnacknowledgedFaceStopsAtAecp", "B6 ADP never starts"),)),
        m("plat-no-one-maap-owner", PLAT, "\t\tallocation(p, i, 0, 0, false);\n", "",
          "platboot1", "Boot.B1ReachesReadyInStepOrder", "B1 the mailbox only after the policy and the one MAAP owner",
          also=(("platboot1", "Boot.B3RefusedImageStopsAtImage", "B3 after the policy and the one MAAP owner"),)),
        m("plat-maap-port-unrefused", PLAT, "maap_csr_init(&p->maap_csr, port, env->aaf_outputs,",
          "maap_csr_init(&p->maap_csr, port, env->aaf_outputs > 8u ? 8u : env->aaf_outputs,",
          "platboot1", "Boot.B4RefusedStreamCountStopsAfterThePolicy", "B4 MAAP's port refuses nine AAF outputs"),
        m("plat-image-unchecked", PLAT, "\tif (!p->console.aem_loaded) {", "\tif (!p->console.aem_loaded && false) {",
          "platboot1", "Boot.B3RefusedImageStopsAtImage", "B3 a refused image stops the boot"),
        m("plat-mailbox-unchecked", PLAT, "\tif (!ctrl_app_open_held(&p->app, &p->config)) {",
          "\tif (!ctrl_app_open_held(&p->app, &p->config) && false) {",
          "platboot1", "Boot.B5OtherContractStopsAtMailbox", "B5 another contract stops the boot"),
        m("plat-aecp-unchecked", PLAT, "\tif (!ctrl_app_open_aecp(&p->bridge)) {",
          "\tif (!ctrl_app_open_aecp(&p->bridge) && false) {",
          "platboot1", "Boot.B6UnacknowledgedFaceStopsAtAecp", "B6 no acknowledgement, no AECP"),
        # steps 6-7: the saved state before the mailbox opens, and its write-back bound to the loop
        m("plat-saved-state-after-mailbox-open", PLAT, SAVED + SERVICE + OPEN, SERVICE + OPEN + SAVED,
          "platboot1", "Boot.B1ReachesReadyInStepOrder",
          "B1 the saved state is read before the mailbox's first access"),
        m("plat-store-tick-unbound", PLAT, TICK, "",
          "platboot1", "Boot.B10ABindAfterReadyIsWrittenBackThroughTheLoop",
          "B10 the bind is written back by the store's service on the loop's tick"),
        m("plat-store-step-unbound", PLAT, STEP, "",
          "platboot1", "Boot.B10ABindAfterReadyIsWrittenBackThroughTheLoop",
          "B10 the bind is written back by the store's service on the loop's tick"),
        m("plat-loop-before-ready", PLAT, "\tif (ctrl_plat.stage == CTRL_PLAT_READY) {",
          "\tif (ctrl_plat.stage >= CTRL_PLAT_MAILBOX) {",
          "platboot1", "Boot.B7OnlyAReadyBootServicesTheLoop", "B7 and never services the loop"),
        # the platform's ports
        m("plat-source-past-count", PLAT, "out->dest_mac_valid = a->valid && n < a->count;",
          "out->dest_mac_valid = a->valid;",
          "platboot1", "Boot.B8PlatformPortsAnswerAsDocumented", "B8 a source past the reported count"),
        m("plat-source-address", PLAT, "stream_id(p, n), a->base + n,", "stream_id(p, n), a->base,",
          "platboot1", "Boot.B8PlatformPortsAnswerAsDocumented", "B8 source n holds base + n"),
        m("plat-window-interface-ignored", PLAT, "\tif (interface == 0u) {\n\t\tctrl_plat_io_write32(",
          "\tif (interface < 2u) {\n\t\tctrl_plat_io_write32(",
          "platboot2", "Boot.B8PlatformPortsAnswerAsDocumented", "B8 and nothing reaches interface 0's"),
        m("plat-licence-sticky", PLAT, ": p->licences[interface] & ~(1u << n);", ": p->licences[interface];",
          "platboot1", "Boot.B8PlatformPortsAnswerAsDocumented", "B8 a revocation clears it"),
        m("plat-source-vid", PLAT, "\t\t\tv->vlan_id = (uint16_t)p->env->policy->sr_vid;\n", "",
          "platboot1", "Boot.B9SrpSourcesCarryTheGeneratedStreams", "B9 on the SR class VID"),
    )


#: The latched loss's publication and the second BMSR read, as ctrl_plat_phy.c's status() holds them (#919).
LATCHED = "\t\t\t\tctrl_plat_io_write32(phy->bus.link_status, 0u);\n\t\t\t\tphy->published = 0u;\n"
CURRENT = "\t\t\tif ((phy->published & CTRL_PLAT_PHY_LINK_UP) == 0u) {\n\t\t\t\tbreak;\n\t\t\t}\n"
#: The sample before MDC's rise, as ctrl_plat_phy.c's bit() holds it, and the release's late-sample defect.
SAMPLE = ("\tconst uint32_t in = ctrl_plat_io_read32(phy->bus.mdio_r) & 1u;\n"
          "\tctrl_plat_io_write32(phy->bus.mdio_w, pins | CTRL_PLAT_PHY_MDC);\n\tspin(phy->spin);\n")
LATE = ("\tctrl_plat_io_write32(phy->bus.mdio_w, pins | CTRL_PLAT_PHY_MDC);\n\tspin(phy->spin);\n"
        "\tconst uint32_t in = ctrl_plat_io_read32(phy->bus.mdio_r) & 1u;\n")
ARM = "\tctrl_plat_phy_arm(&p->phy, &env->phy, env->flash->now_us, env->flash->ctx);\n"
IDENTITY = "\tif (!ctrl_plat_csr_identity(env->csr, &p->version)) {\n"
L2 = "L2 a loss that recovered between two polls moves LINK_DOWN and LINK_UP by one each"
P3 = "P3 a loss that recovered between two polls publishes link down, then link up"


#: The map generator's PHY rows (#919), as ctrl_plat_gen.py holds them.
GEN = "plat/ctrl_plat_gen.py"
PARTIAL = "    if any(phy) and not all(phy):\n"


def phy_mutants(mutant: type) -> tuple:
    """The PHY poll's (#919): the four the issue names (no poll, the loss not latched, an edge not counted, the
    cease not ended on link-up), each reproducing the bench's symptom, then the poll's own rules."""
    m = mutant
    return (
        # no poll: the PHY never armed, so milan_mac_link_status keeps its reset value
        m("plat-phy-never-armed", PLAT, ARM, "", "platboot1", "Phy.L1ReadyLoopPublishesTheLink",
          "L1 the ready loop publishes the PHY's link"),
        # the loss BMSR latched between two polls never published
        m("plat-phy-loss-not-latched", PHY, LATCHED, "\t\t\t\tphy->published = 0u;\n", "platboot1",
          "PlatPhy.P3LatchedLossPublishesBothEdges", P3, also=(("platboot1", "Phy.L2EveryEdgeIsCounted", L2),)),
        # an edge not counted: the whole poll in one call, so the loss's word and the current state's land in
        # the same turn and the datapath's synchronised level never sees the loss
        m("plat-phy-edge-not-counted", PHY, "\t\ttake(phy);\n\t}\n",
          "\t\tdo {\n\t\t\ttake(phy);\n\t\t} while (phy->stage != CTRL_PLAT_PHY_IDLE);\n\t}\n",
          "platboot1", "Phy.L2EveryEdgeIsCounted", L2,
          also=(("platboot1", "PlatPhy.P7OneFrameACallWithItsRoom", "P7 one frame a call"),)),
        # the cease not ended on link-up: the second BMSR read dropped, so the poll after the link's return
        # resolves the latched loss and publishes it down, a period late for the gPTP plane's toggle
        m("plat-phy-cease-not-ended", PHY, CURRENT, "", "platboot1", "Phy.L4ReturnEndsTheCeaseWithinAPoll",
          "L4 the first poll after the link's return publishes it up",
          also=(("platboot1", "PlatPhy.P3LatchedLossPublishesBothEdges", P3),)),
        # the counter change of a link edge dropped before AECP: no notification
        m("plat-link-counter-change-dropped", "app/ctrl_app_aecp.c",
          "\t\tctrl_app_aecp_changed(c, e->desc_type, e->desc_index, 8u);\n", "\t\t(void)c;\n", "platboot1",
          "Phy.L3EachEdgeNotifiesTheCounters", "L3 each link edge sends one unsolicited GET_COUNTERS"),
        # the bus map: the rows' addresses dropped, some rows accepted, none refused
        m("plat-map-phy-rows-ignored", GEN, "if all(phy) else 0:08X}u", "if False else 0:08X}u", "platmap",
          "PlatMap.M1AllThreeRowsGiveTheirAddresses", "M1 the PHY's three rows give their addresses"),
        m("plat-map-partial-accepted", GEN, PARTIAL, "    if False:\n", "platmap", "PlatMap.M3SomeRowsAreRefused",
          "M3 some but not all of the PHY's rows are refused"),
        m("plat-map-absent-refused", GEN, PARTIAL, "    if not all(phy):\n", "platmap", "PlatMap.M2NoRowsGiveZero",
          "M2 a SoC with no MDIO gives 0 for each"),
        # the guard and the paths
        # the poll armed before the identity check: a foreign window's pins bit-banged
        m("plat-phy-unguarded", PLAT, IDENTITY, ARM + IDENTITY, "platboot1", "Phy.B11ArmedPastTheIdentityCheck",
          "B11 a foreign window's MDIO pins are never touched"),
        m("plat-phy-refused-stage-unpolled", PLAT,
          "\t\t(void)ctrl_plat_phy_step(&ctrl_plat.phy, CTRL_LOOP_SHARE_US);\n", "",
          "platboot1", "Phy.B11ArmedPastTheIdentityCheck",
          "B11 a stage refused past the identity check keeps publishing the link"),
        m("plat-phy-beside-a-save-step", PHY, "saving && s->steps != steps ? 0 :",
          "saving && s->steps != steps && false ? 0 :",
          "platboot1", "Phy.B12StepCarriesTheStoresSaveOrAPhyFrame",
          "B12 a call whose store takes a step of its save carries no PHY frame"),
        m("plat-phy-store-owed-dropped", PHY, "(int32_t)(deadline - nvm_store_clock(NULL))) ||\n\t       store;",
          "(int32_t)(deadline - nvm_store_clock(NULL))) ||\n\t       (false && store);", "platboot1",
          "Phy.B12StepCarriesTheStoresSaveOrAPhyFrame", "B12 the client owes a step while the store owes one"),
        m("plat-phy-after-an-idle-step-refused", PHY, "saving && s->steps != steps ? 0 :",
          "(saving || true) && s->steps != steps ? 0 :", "platboot1", "Phy.B12StepCarriesTheStoresSaveOrAPhyFrame",
          "B12 a call whose store step is an idle one carries one PHY frame"),
        # the poll's rules
        m("plat-phy-probe-scans", PHY, "\t\tphy->polled = false;\n\t\tnext = CTRL_PLAT_PHY_IDLE;\n",
          "\t\tphy->polled = false;\n\t\tif (phy->address != 0u) {\n\t\t\tphy->stage = CTRL_PLAT_PHY_PROBE;\n"
          "\t\t\ttake(phy);\n\t\t\treturn;\n\t\t}\n\t\tnext = CTRL_PLAT_PHY_IDLE;\n",
          "platboot1", "PlatPhy.P1OneAddressIsProbedACall", "P1 one address an opportunity, no scan in one call"),
        m("plat-phy-late-sample", PHY, SAMPLE, LATE, "platboot1", "PlatPhy.P1OneAddressIsProbedACall",
          "P1 the PHY found at its address publishes its link"),
        m("plat-phy-unpaced", PHY, "now - phy->started >= CTRL_PLAT_PHY_POLL_US", "now - phy->started >= 1u",
          "platboot1",
          "PlatPhy.P2PollsArePaced", "P2 no poll before CTRL_PLAT_PHY_POLL_US",
          also=(("platboot1", "Phy.L1ReadyLoopPublishesTheLink", "L1 a poll a period"),)),
        m("plat-phy-wrap-unsafe", PHY, "now - phy->started >= CTRL_PLAT_PHY_POLL_US",
          "now >= phy->started + CTRL_PLAT_PHY_POLL_US", "platboot1", "PlatPhy.P10TheClockWraps",
          "P10 a clock that went back makes a poll due at once"),
        m("plat-phy-common-mode-misread", PHY, "\tif ((common & CTRL_PLAT_PHY_AN_100_FULL) != 0u) {",
          "\tif ((common & CTRL_PLAT_PHY_AN_100_HALF) != 0u && false) {", "platboot1",
          "PlatPhy.P4ResolvedModesAreTheReleases", "P4 the highest common mode of 4 and 5"),
        m("plat-phy-fault-ignored", PHY, " && (u & CTRL_PLAT_PHY_GSTAT_FAULT) == 0u", "", "platboot1",
          "PlatPhy.P4ResolvedModesAreTheReleases", "P4 a master-slave configuration fault is link down"),
        m("plat-phy-ack-ignored", PHY,
          "return (value & 1u << CTRL_PLAT_PHY_DATA_BITS) != 0u ? -1 : (int32_t)(value & 0xffffu);",
          "return (int32_t)(value & 0xffffu);",
          "platboot1", "PlatPhy.P5ErrorsAreLinkDown", "P5 a NAKed register is link down"),
        m("plat-phy-turnaround-driven", PHY, "k < CTRL_PLAT_PHY_PREAMBLE_BITS + CTRL_PLAT_PHY_COMMAND_BITS, hi",
          "k < CTRL_PLAT_PHY_PREAMBLE_BITS + CTRL_PLAT_PHY_COMMAND_BITS + 1u, hi", "platboot1",
          "PlatPhy.P6FramesAreClause22Reads",
          "P6 every frame a Clause-22 read, driven then released"),
        m("plat-phy-no-deadline", PHY, "room >= (int32_t)CTRL_PLAT_PHY_STEP_US", "room >= -1000000",
          "platboot1", "PlatPhy.P7OneFrameACallWithItsRoom",
          "P7 a frame is taken only with CTRL_PLAT_PHY_STEP_US left"),
        m("plat-phy-not-owed", PHY, "\treturn phy->stage != CTRL_PLAT_PHY_IDLE || due(phy, now);",
          "\treturn false;", "platboot1", "PlatPhy.P8OwedWhileAFrameIsDue",
          "P8 a probe that missed owes the next"),
        m("plat-phy-half-period-short", PHY,
          "(CONFIG_CLOCK_FREQUENCY + CTRL_PLAT_PHY_HALF_HZ - 1u) / CTRL_PLAT_PHY_HALF_HZ)",
          "(CONFIG_CLOCK_FREQUENCY + CTRL_PLAT_PHY_HALF_HZ - 1u) / CTRL_PLAT_PHY_HALF_HZ / 2u)", "platboot1",
          "PlatPhy.P9NoMdioArmsNothing",
          "P9 the half period at 100 MHz: 200 ns, 20 turns"),
        m("plat-phy-timed-run-ignored", PHY, "\t\tphy->spin = 1u;\n", "", "platboot1", "PlatPhy.P9NoMdioArmsNothing",
          "P9 a run of 277 us: one turn holds 200 ns"),
        m("plat-phy-timed-resolution-ignored", PHY, "- before > TIMED_ONE) {", "- before >= TIMED_ONE) {", "platboot1",
          "PlatPhy.P9NoMdioArmsNothing", "P9 a run of 205 us bounds a turn under 200 ns"),
    )

