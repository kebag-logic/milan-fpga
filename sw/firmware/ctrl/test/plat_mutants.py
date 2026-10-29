# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""plat_mutants.py - the split platform's planted defects (#665 S3), in the control campaign's table.

ctrl_mutants.py plants each into a copy of sw/firmware/ctrl and requires the
named GoogleTest test of the named arm to fail on the check's own words
(ctrl_mutants.campaign). The arms are plat_arms.py's: `plat` (the CSR window,
the console, the MMIO platform), `platboot1` and `platboot2` (the boot at one
and two interfaces). The CSR initialisation's trace against milan_baremetal.c
carries its own three plants (plat_trace.py).

The table holds S3's named controls: a CSR write skipped, reordered or wrong,
caught by the write list; a console that blocks past #397's tick rule (input
or output past its per-pass slice, a write into a full FIFO, a command run
without room), caught by the pass bound; and the boot's order of Milan v1.2
5.6.1, caught by the step order.
"""
from __future__ import annotations

#: The test files whose every test a defect here must name.
SOURCES = ("test_plat.cpp", "test_plat_mmio.cpp", "test_plat_boot.cpp")
CSR = "plat/ctrl_plat_csr.c"
CONSOLE = "plat/ctrl_plat_console.c"
PLAT = "plat/ctrl_plat.c"
C2 = "Plat.C2PolicyIsConfigureFabricsFifteenWritesInOrder"
K4 = "Plat.K4EachPassIsBounded"


def mutants(mutant: type) -> tuple:
    """The table, built with the campaign's Mutant (ctrl_mutant.py)."""
    m = mutant
    return (
        # the CSR initialisation (S3: skipped, reordered, wrong)
        m("plat-policy-write-skipped", CSR, "\twr(csr, CTRL_PLAT_CSR_LWSRP_VID, p->sr_vid);\n", "",
          "plat", C2, "C2 configure_fabric's writes, in its order, from the policy"),
        m("plat-policy-writes-reordered", CSR,
          "\twr(csr, CTRL_PLAT_CSR_ADP_EID_LO, p->entity_id_lo);\n\twr(csr, CTRL_PLAT_CSR_ADP_EID_HI, p->entity_id_hi);\n",
          "\twr(csr, CTRL_PLAT_CSR_ADP_EID_HI, p->entity_id_hi);\n\twr(csr, CTRL_PLAT_CSR_ADP_EID_LO, p->entity_id_lo);\n",
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
