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
flash; and the console's milan_lat under gptp.latency_writable (#878), caught
by its write list and its answer, and the key reaching a build that leaves it
off, caught by that build's refusal.
"""
from __future__ import annotations

#: The test files whose every test a defect here must name.
SOURCES = ("test_plat.cpp", "test_plat_mmio.cpp", "test_plat_boot.cpp", "test_plat_phy.cpp", "test_plat_phy_mii.cpp")
CSR = "plat/ctrl_plat_csr.c"
CONSOLE = "plat/ctrl_plat_console.c"
PLAT = "plat/ctrl_plat.c"
FACE = "aecp/aecp_face.c"
#: GET_AS_PATH's count read, as aecp_face.c holds it (#897).
AS_PATH_COUNT = "if (!gsi(f, interface, 2u, AVB_INTERFACE, index, 0u, 0u, 0u, &n) || n > capacity) {"
PHY = "plat/ctrl_plat_phy.c"
#: THE STEP's client, a call owing no centisecond step (#665's ruling of 2026-11-17): its test and its frame.
YIELD = "\tif (!nvm_store_owed() && owes(ctx)) {\n"
FRAME = "\t\treturn ctrl_plat_phy_step(ctx, (int32_t)(deadline - nvm_store_clock(NULL)));\n"
C2 = "Plat.C2PolicyIsConfigureFabricsFifteenWritesInOrder"
K4 = "Plat.K4EachPassIsBounded"
K7 = "Plat.K7MilanLatWritesThePairAndReadsItBack"


#: The reorder plant's two writes, as ctrl_plat_csr.c holds them and swapped.
EID = ("\twr(csr, CTRL_PLAT_CSR_ADP_EID_LO, p->entity_id_lo);\n",
       "\twr(csr, CTRL_PLAT_CSR_ADP_EID_HI, p->entity_id_hi);\n")
#: milan_lat's two writes, as ctrl_plat_csr.c holds them (#878).
LAT = ("\twr(csr, CTRL_PLAT_CSR_PTP_ILAT, ingress_ns);\n", "\twr(csr, CTRL_PLAT_CSR_PTP_ELAT, egress_ns);\n")
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
    return (csr_mutants(mutant) + console_mutants(mutant) + lat_mutants(mutant) + boot_mutants(mutant)
            + phy_mutants(mutant) + mii_mutants(mutant))


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


def lat_mutants(mutant: type) -> tuple:
    """The console's milan_lat under gptp.latency_writable (#878): a direction crossed, a value or a field past the
    command accepted, an answer that is not the read back, and the key reaching a build that leaves it off."""
    m = mutant
    return (
        m("plat-lat-directions-crossed", CSR, LAT[0] + LAT[1],
          LAT[0].replace("ILAT", "ELAT") + LAT[1].replace("ELAT", "ILAT"),
          "plat", K7, "K7 ingress to 0x540, egress to 0x544"),
        m("plat-lat-wide-value-accepted", CONSOLE, "if (v > 0xffffu) {", "if (v > 0x1ffffu) {",
          "plat", K7, "K7 a value past 65535 is refused"),
        m("plat-lat-third-field-accepted", CONSOLE, "if (!number(c, &at, &egress) || at != c->len) {",
          "if (!number(c, &at, &egress)) {", "plat", K7, "K7 a third field is refused"),
        m("plat-lat-answer-not-read-back", CSR, "\treturn rd(csr, CTRL_PLAT_CSR_GPTP_LAT);\n",
          "\treturn ((uint32_t)ingress_ns << 16) | egress_ns;\n",
          "plat", K7, "K7 the answer is GPTP_LAT read back"),
        m("plat-lat-key-reaches-every-build", "plat/ctrl_plat_csr.h", "#define CTRL_PLAT_CSR_H\n",
          "#define CTRL_PLAT_CSR_H\n#define CTRL_PLAT_LAT_WRITABLE 1\n",
          "plat", "Plat.K8MilanLatIsNoCommandWithoutTheKey", "K8 without the key milan_lat is refused"),
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
        m("plat-loop-before-ready", PLAT, "\tif (ctrl_plat.stage != CTRL_PLAT_READY) {",
          "\tif (ctrl_plat.stage < CTRL_PLAT_MAILBOX) {",
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
        # GET_AS_PATH is the datapath's sequence through the face (#897): the old stub's unavailable answer restored
        m("plat-as-path-unavailable", FACE, AS_PATH_COUNT, AS_PATH_COUNT.replace("if (!gsi(", "if (f != NULL || !gsi("),
          "platboot1", "Boot.B24GetAsPathAnswersTheDatapathsSequence", "B24 GET_AS_PATH answers SUCCESS",
          also=(("platboot2", "Boot.B24GetAsPathAnswersTheDatapathsSequence", "B24 GET_AS_PATH answers SUCCESS"),)),
    ) + reboot_mutants(mutant)


#: The REBOOT's sequence in ctrl_plat.c (#871): its receive gate, the loop's stop, ADP's SHUTDOWN once every
#: other ring has drained, the drained ADP ring and the port's write.
TAKEN = "\town->fn(own->ctx, f);\n"
GATE = "\treturn !aecp_reboot_accepted(&ctrl_plat.aecp.core) && (own->ready == NULL || own->ready(own->ctx));\n"
DUE = "\t} else if (aecp_reboot_due(&ctrl_plat.aecp.core)) {\n"
DEPART = "\t} else if (ctrl_plat.reboot != 0u) {\n\t\tdepart(&ctrl_plat);\n"
OTHERS = "\t\t\tif (ch != MBX_CH_ADP && !drained(ch)) {\n"
SHUTDOWN = "\t\tadp_mbx_set_enable(&p->app.adp, false);\n"
OWED = "\t\t\towed = owed || p->app.adp.ifs[i].adp.departing_owed != 0u;\n"
DRAINED = "\t\tif (owed || !drained(MBX_CH_ADP)) {\n"
FIRE = "\t\tctrl_plat_io_write32(p->env->reboot, 1u);\n"


def reboot_mutants(mutant: type) -> tuple:
    """The REBOOT's (IEEE 1722.1-2021 7.4.43): the reset before the response or the DEPARTING, frames taken after
    the SUCCESS or sent after the DEPARTING (REQ-FWX-001), the request ignored, a REBOOT with no port, and a loop
    stopped at the reset, which tears the journal write in progress."""
    m = mutant
    return (
        m("plat-reboot-before-the-response", PLAT, TAKEN,
          TAKEN + "\tif (aecp_reboot_accepted(&ctrl_plat.aecp.core)) {\n"
                  "\t\tctrl_plat_io_write32(ctrl_plat.env->reboot, 1u);\n\t}\n",
          "platboot1", "Boot.B12TheResetWaitsForTheResponseToLeave",
          "B12 no reset while the mailbox holds the response"),
        m("plat-reboot-ignored", PLAT, FIRE, "",
          "platboot1", "Boot.B11ARebootIsAnsweredNotifiedDepartsAndThenResets", "B11 the reset port is written once",
          also=(("platboot1", "Boot.B15TheResetRestoresTheSavedStateAndAdvertisesAgain",
                 "B15 the REBOOT fires the reset port"),
                ("platboot1", "Boot.B16ARebootDuringTheJournalWriteKeepsTheChange",
                 "B16 the REBOOT fires the reset port"))),
        m("plat-reboot-without-departing", PLAT, SHUTDOWN, "",
          "platboot1", "Boot.B11ARebootIsAnsweredNotifiedDepartsAndThenResets",
          "B11 every interface sends ENTITY_DEPARTING"),
        m("plat-reboot-departing-owed-ignored", PLAT, OWED, "\t\t\towed = owed || false;\n",
          "platboot1", "Boot.B18ADepartingTheRingRefusedHoldsTheReset",
          "B18 ENTITY_DEPARTING leaves before the reset"),
        m("plat-reboot-before-departing-left", PLAT, DRAINED, "\t\tif (owed) {\n",
          "platboot1", "Boot.B12TheResetWaitsForTheResponseToLeave",
          "B12 no reset while the mailbox holds ENTITY_DEPARTING"),
        m("plat-reboot-without-a-port", PLAT, "p->aecp_config.reboot = p->env->reboot != 0u;",
          "p->aecp_config.reboot = true;",
          "platboot1", "Boot.B14WithoutAResetPortRebootIsNotImplemented",
          "B14 without a reset port REBOOT is NOT_IMPLEMENTED"),
        m("plat-reboot-under-another-lock", "aecp/aecp_commands.c",
          "\tif (aecp_foreign_lock(a)) {\n\t\treturn AECP_ENTITY_LOCKED;\n\t}\n\ta->notify = true;\n",
          "\ta->notify = true;\n",
          "platboot1", "Boot.B13RefusalsLeaveTheEntityInService",
          "B13 ENTITY_LOCKED under another controller's lock"),
        m("plat-reboot-stops-the-store", PLAT, "\t\tnvm_store_service();\n", "",
          "platboot1", "Boot.B16ARebootDuringTheJournalWriteKeepsTheChange",
          "B16 the change made before the REBOOT is kept"),
        m("plat-reboot-hides-the-drain", PLAT, "\taecp_face_status(&p->face, restore, nvm, dirty);\n", "",
          "platboot1", "Boot.B16ARebootDuringTheJournalWriteKeepsTheChange",
          "B16 the drain ends because the write completed, not at its deadline"),
        m("plat-reboot-serves-the-loop-after-the-port", PLAT, DEPART,
          DEPART + "\t\tif (ctrl_plat.reboot == 3u) {\n\t\t\tctrl_loop_step(&ctrl_plat.app.loop);\n\t\t}\n",
          "platboot1", "Boot.B17NothingIsTakenOrSentOnceTheResetPortFired",
          "B17 nothing is sent once the reset port fired"),
        # REQ-FWX-001, the processor's parity in the window from the SUCCESS to the port
        m("plat-reboot-takes-frames-after-the-success", PLAT, GATE,
          "\treturn own->ready == NULL || own->ready(own->ctx);\n",
          "platboot1", B19, "B19 no ADP frame is taken after the REBOOT's SUCCESS",
          also=tuple(("platboot1", B19, f"B19 no {n} frame is taken after the REBOOT's SUCCESS")
                     for n in ("ACMP", "MAAP", "SRP")) +
          (("platboot1", B19, "B19 a BIND_RX after the REBOOT's SUCCESS is not applied"),)),
        # The loop serviced after the DEPARTING, caught on NoOtherChannelTransmitsAfterTheDeparting's ACMP, MAAP and
        # SRP words. NoOtherChannelTransmitsAfterTheDeparting's AECP check has no defect of its own, because AECP starts
        # no frame after its SUCCESS; each of its three layers carries one: this one (the loop's stop),
        # plat-reboot-takes-aecp-frames-after-the-success (the receive gate, on
        # NoFrameOfAnyChannelIsTakenFromTheSuccess's and TheGateHoldsWhileTheResponseCannotBeHandedOver's AECP words)
        # and reboot-serves-after-its-success, reboot-probes-after-its-success and reboot-retries-after-its-success in
        # aecp_reboot_mutants.py (AECP's own silence)
        m("plat-reboot-transmits-after-the-departing", PLAT, DEPART,
          DEPART + "\t\tif (ctrl_plat.reboot != 3u) {\n\t\t\tctrl_loop_step(&ctrl_plat.app.loop);\n\t\t}\n",
          "platboot1", B20, "B20 no other channel starts a transmission after ENTITY_DEPARTING",
          also=tuple(("platboot1", B20, f"B20 no {n} transmission starts after ENTITY_DEPARTING")
                     for n in ("ACMP", "MAAP", "SRP"))),
        m("plat-reboot-departs-before-the-rings-drain", PLAT, OTHERS,
          "\t\t\tif (ch != MBX_CH_ADP && !drained(ch) && false) {\n",
          "platboot1", B21, "B21 no ENTITY_DEPARTING while the ACMP ring holds a frame",
          also=tuple(("platboot1", B21, f"B21 no ENTITY_DEPARTING while the {n} ring holds a frame")
                     for n in ("MAAP", "SRP"))),
        # the gate from the SUCCESS itself, not from the handover of its frames
        m("plat-reboot-accepted-at-the-handover", "aecp/aecp.c", ACCEPTED, "\treturn a->reboot >= 2u;\n",
          "platboot1", B22, "B22 no MAAP frame queued with the REBOOT is taken",
          also=(("platboot1", B22, "B22 no SRP frame queued with the REBOOT is taken"),) +
          tuple(("platboot1", B23, f"B23 no {n} frame is taken while the REBOOT's SUCCESS waits to be handed over")
                for n in ("ADP", "ACMP", "MAAP", "SRP"))),
    ) + channel_gate_mutants(mutant) + channel_wait_mutants(mutant)


#: The REBOOT's tests that name a channel in their words
B19 = "Boot.B19NoFrameOfAnyChannelIsTakenFromTheSuccess"
B20 = "Boot.B20NoOtherChannelTransmitsAfterTheDeparting"
B21 = "Boot.B21TheDepartingWaitsForEveryOtherRing"
B22 = "Boot.B22TheGateHoldsInThePassThatTakesTheReboot"
B23 = "Boot.B23TheGateHoldsWhileTheResponseCannotBeHandedOver"
#: AECP's acceptance of a REBOOT, which the gate reads (aecp/aecp.c)
ACCEPTED = "\treturn a->reboot != 0u;\n"
#: Each channel by its contract constant and the name its tests' words carry
CHANNELS = (("MBX_CH_ADP", "ADP"), ("MBX_CH_ACMP", "ACMP"), ("MBX_CH_AECP", "AECP"), ("MBX_CH_MAAP", "MAAP"),
            ("MBX_CH_SRP", "SRP"))


def channel_gate_mutants(mutant: type) -> tuple:
    """The receive gate open on one channel only. AECP's own ready refuses a command from the SUCCESS too
    (aecp.c), so AECP's defect opens both: its channel is taken whatever either says."""
    out = []
    for const, name in CHANNELS:
        if name == "AECP":
            new = ("\treturn own == &ctrl_plat.rx[MBX_CH_AECP] || (!aecp_reboot_accepted(&ctrl_plat.aecp.core) && "
                   "(own->ready == NULL || own->ready(own->ctx)));\n")
        else:
            new = (f"\treturn (own == &ctrl_plat.rx[{const}] || !aecp_reboot_accepted(&ctrl_plat.aecp.core)) && "
                   "(own->ready == NULL || own->ready(own->ctx));\n")
        out.append(mutant(f"plat-reboot-takes-{name.lower()}-frames-after-the-success", PLAT, GATE, new,
                          "platboot1", B19, f"B19 no {name} frame is taken after the REBOOT's SUCCESS",
                          also=(("platboot1", B23,
                                 f"B23 no {name} frame is taken while the REBOOT's SUCCESS waits to be handed over"),)))
    return tuple(out)


def channel_wait_mutants(mutant: type) -> tuple:
    """The DEPARTING's wait skipping one ring. AECP's ring holds only the REBOOT's own frames once the loop has
    stopped, which aecp_reboot_due waits for, so skipping it alone changes nothing and it has no defect here."""
    return tuple(mutant(f"plat-reboot-departs-past-the-{name.lower()}-ring", PLAT, OTHERS,
                        f"\t\t\tif (ch != MBX_CH_ADP && ch != {const} && !drained(ch)) {{\n",
                        "platboot1", B21, f"B21 no ENTITY_DEPARTING while the {name} ring holds a frame")
                 for const, name in CHANNELS if name not in ("ADP", "AECP"))


#: The latched loss's publication and the second BMSR read, as ctrl_plat_phy.c's take() holds them (#919).
LATCHED = "\t\t\t\tpublish(phy, 0u);\n"
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
        *step_yield_mutants(mutant),
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
        m("plat-phy-turnaround-driven", PHY, READ_DRIVEN, READ_DRIVEN.replace(";", " + 1u;"), "platboot1",
          "PlatPhy.P6FramesAreClause22Reads", P6),
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
    ) + advertisement_mutants(mutant)


#: THE ADVERTISEMENT's writes and decisions (#840 on the split, #919), as ctrl_plat_phy.c's take() holds them.
ANAR_MASK = "(uint32_t)phy->local & ~(CTRL_PLAT_PHY_ANAR_BELOW_GIGABIT | CTRL_PLAT_PHY_ANAR_RESERVED)"
GCTRL_SET = "((uint32_t)phy->gig & CTRL_PLAT_PHY_GCTRL_MASTER_SLAVE) | CTRL_PLAT_PHY_GCTRL_1000_FULL :"
RESTART_BITS = "| CTRL_PLAT_PHY_BMCR_AN_ENABLE | CTRL_PLAT_PHY_BMCR_AN_RESTART) &"
HELD = ("(phy->adv & CTRL_PLAT_PHY_ADV_RENEGOTIATE) == 0u &&\n"
        "\t\t    gigabit_only((uint32_t)phy->local, (uint32_t)phy->gig)")
#: The repair's restart, as ctrl_plat_phy.c's take() decides it and takes it, and the defect of a restart marked
#: taken before the read-back verifies, so the repair of a dropped write restarts nothing (#919).
REPAIR = ("\t\tif (" + HELD + ") {\n\t\t\tnext = CTRL_PLAT_PHY_ADV_CHECK_LOCAL;\n\t\t}\n\t\tbreak;\n"
          "\tcase CTRL_PLAT_PHY_ADV_RESTART:\n\t\tphy->adv &= (uint8_t)~CTRL_PLAT_PHY_ADV_RENEGOTIATE;\n")
RESTARTED_EARLY = ("\t\tif ((phy->adv & 0x8u) != 0u || (" + HELD + ")) {\n\t\t\tnext = CTRL_PLAT_PHY_ADV_CHECK_LOCAL;\n"
                   "\t\t}\n\t\tbreak;\n\tcase CTRL_PLAT_PHY_ADV_RESTART:\n\t\tphy->adv |= 0x8u;\n")
#: THE OUTCOME's judgement (#919): a completed negotiation sharing no 1000BASE-T mode, the advertisement verified.
OUTCOME = "if (next != CTRL_PLAT_PHY_IDLE && phy->adv == 0u) {"
OUTCOME_OWED = ("\t\t\t\tphy->adv = CTRL_PLAT_PHY_ADV_OWED | CTRL_PLAT_PHY_ADV_RENEGOTIATE;\n"
                "\t\t\t\tif (phy->renegotiations")
P18 = "PlatPhy.P18TheRestartIsVerifiedByItsOutcome"
P18_PACED = ("platboot1", "PlatPhy.P18OneRestartAPollUntilOneTakes", "P18 one restart a poll, paced like the poll")
READ_DRIVEN = "uint32_t driven = CTRL_PLAT_PHY_PREAMBLE_BITS + CTRL_PLAT_PHY_COMMAND_BITS;"
P6 = "P6 every frame a Clause-22 read or write, driven as 22.2.4.5 drives it"
P11 = "PlatPhy.P11TheBootAdvertisesGigabitOnly"


def step_yield_mutants(mutant: type) -> tuple:
    """THE STEP's client in a call owing no centisecond step: the PHY's owed frame, never the save's extra step
    beside it or before it, and that step where no frame is owed (#919, #920; #665's ruling of 2026-11-17)."""
    m = mutant
    return (
        m("plat-phy-frame-yields-to-the-extra-step", PHY, YIELD,
          "\tif (false && !nvm_store_owed() && owes(ctx)) {\n", "platboot1", "Phy.L5ASaveKeepsThePollItsPeriod",
          "L5 a loss during a save is published within one poll period"),
        m("plat-phy-frame-beside-the-extra-step", PHY, FRAME,
          FRAME.replace("NULL)));", "NULL))) | nvm_store_step(NULL, deadline);"), "platboot1",
          "Phy.B12StepCarriesTheStoresSaveOrAPhyFrame",
          "B12 the yielding call leaves the store's step count unchanged"),
        m("plat-phy-frame-before-the-centisecond-step", PHY, YIELD, "\tif (owes(ctx)) {\n", "platboot1",
          "Phy.L6AProbeThatAlwaysMissesLeavesTheSaveItsWorstCase", "L6 the save is durable while every probe misses"),
        m("plat-phy-extra-step-never-taken", PHY, YIELD, "\tif (!nvm_store_owed() && (owes(ctx) || true)) {\n",
          "platboot1",
          "Phy.B12StepCarriesTheStoresSaveOrAPhyFrame", "B12 a call with no frame owed takes the extra step"),
    )

def advertisement_mutants(mutant: type) -> tuple:
    """THE ADVERTISEMENT's: the release's PHY init's writes, each property its own defect, and the split's rules,
    written and verified at boot and after every link loss, restarted after every repair, and its restart verified by
    the negotiation's outcome."""
    m = mutant
    return (
        # #840's named defect: 100BASE-TX left advertised
        m("plat-phy-100base-tx-advertised", PHY, ANAR_MASK, ANAR_MASK.replace("CTRL_PLAT_PHY_ANAR_BELOW_GIGABIT",
                                                                              "0x0260u"),
          "platboot1", P11, "P11 no 100BASE-TX advertised"),
        m("plat-phy-10base-t-advertised", PHY, ANAR_MASK, ANAR_MASK.replace("CTRL_PLAT_PHY_ANAR_BELOW_GIGABIT",
                                                                            "0x0380u"),
          "platboot1", P11, "P11 no 10BASE-T advertised"),
        m("plat-phy-reserved-kept", PHY, ANAR_MASK, ANAR_MASK.replace(" | CTRL_PLAT_PHY_ANAR_RESERVED", ""),
          "platboot1", P11, "P11 reserved bit 14 cleared"),
        m("plat-phy-half-duplex-advertised", PHY, GCTRL_SET,
          GCTRL_SET.replace(" :", " | CTRL_PLAT_PHY_GCTRL_1000_HALF :"), "platboot1", P11,
          "P11 no 1000BASE-T half duplex advertised"),
        m("plat-phy-master-slave-dropped", PHY, GCTRL_SET, GCTRL_SET.replace("(uint32_t)phy->gig &", "0u &"),
          "platboot1", P11, "P11 MASTER-SLAVE kept"),
        m("plat-phy-test-mode-kept", PHY, GCTRL_SET,
          GCTRL_SET.replace("CTRL_PLAT_PHY_GCTRL_MASTER_SLAVE)", "(CTRL_PLAT_PHY_GCTRL_MASTER_SLAVE | 0xe000u))"),
          "platboot1", P11, "P11 the test mode cleared"),
        m("plat-phy-not-restarted", PHY, RESTART_BITS, RESTART_BITS.replace(" | CTRL_PLAT_PHY_BMCR_AN_RESTART", ""),
          "platboot1", P11, "P11 autonegotiation restarted"),
        m("plat-phy-reset-kept", PHY, "~(CTRL_PLAT_PHY_BMCR_RESET | CTRL_PLAT_PHY_BMCR_ISOLATE)",
          "~CTRL_PLAT_PHY_BMCR_ISOLATE", "platboot1", P11, "P11 reset cleared"),
        m("plat-phy-boot-restart-dropped", PHY,
          "\tphy->ctx = ctx;\n\tphy->adv = CTRL_PLAT_PHY_ADV_OWED | CTRL_PLAT_PHY_ADV_RENEGOTIATE;\n",
          "\tphy->ctx = ctx;\n\tphy->adv = CTRL_PLAT_PHY_ADV_OWED;\n", "platboot1", P11,
          "P11 the boot restarts negotiation whatever the PHY holds"),
        m("plat-phy-write-released", PHY, "\t\tdriven = CTRL_PLAT_PHY_FRAME_BITS;\n",
          "\t\tdriven = CTRL_PLAT_PHY_PREAMBLE_BITS + CTRL_PLAT_PHY_COMMAND_BITS;\n", "platboot1",
          "PlatPhy.P6FramesAreClause22Reads", P6),
        # a 10/100 PHY written
        m("plat-phy-mii-written", PHY,
          "\t\tif ((u & CTRL_PLAT_PHY_BMSR_EXTENDED) == 0u) {\n\t\t\tphy->adv = CTRL_PLAT_PHY_ADV_NONE;\n",
          "\t\tif (false) {\n\t\t\tphy->adv = CTRL_PLAT_PHY_ADV_NONE;\n", "platboot1",
          "PlatPhy.P12A10100PhyIsNeverWritten",
          "P12 a PHY without BMSR's extended capability is never written"),
        m("plat-phy-10-100-written", PHY, "if (v >= 0 && (u & CTRL_PLAT_PHY_ESTAT_1000T_FULL) == 0u) {",
          "if (v >= 0 && false) {", "platboot1", "PlatPhy.P12A10100PhyIsNeverWritten",
          "P12 a PHY without 1000BASE-T full duplex ability is never written"),
        # the split's rules: after every loss, verified, its restart once a time it is owed
        m("plat-phy-advertised-once", PHY, "\t\tphy->adv = CTRL_PLAT_PHY_ADV_OWED;\n", "\t\t(void)0;\n", "platboot1",
          "PlatPhy.P13ALossWritesAndVerifiesItAgain", "P13 after a link loss the advertisement is written again"),
        m("plat-phy-restart-every-loss", PHY, HELD, "false", "platboot1", "PlatPhy.P13ALossWritesAndVerifiesItAgain",
          "P13 a loss with the advertisement held restarts nothing"),
        m("plat-phy-reset-phy-not-restarted", PHY, HELD, "(phy->adv & CTRL_PLAT_PHY_ADV_RENEGOTIATE) == 0u",
          "platboot1",
          "PlatPhy.P14AResetPhyIsAdvertisedAgain", "P14 a PHY that lost the advertisement is written and restarted"),
        # a PHY that lost one register alone behind a loss, its decision reading that register as held
        m("plat-phy-lost-local-not-restarted", PHY, HELD, HELD.replace("(uint32_t)phy->local,", "0u,"), "platboot1",
          "PlatPhy.P14AResetPhyIsAdvertisedAgain",
          "P14 a PHY that lost the advertisement is written and restarted once, register 4 alone"),
        m("plat-phy-lost-gig-not-restarted", PHY, HELD,
          HELD.replace("(uint32_t)phy->gig)", "CTRL_PLAT_PHY_GCTRL_1000_FULL)"), "platboot1",
          "PlatPhy.P14AResetPhyIsAdvertisedAgain",
          "P14 a PHY that lost the advertisement is written and restarted once, register 9 alone"),
        # the restart marked taken before verification, so a repair is never negotiated
        m("plat-phy-restarted-before-verified", PHY, REPAIR, RESTARTED_EARLY, "platboot1",
          "PlatPhy.P17TheRepairedAdvertisementIsTheOneInForce", "P17 the repair restarts negotiation itself",
          also=(("platboot1", "PlatPhy.P15AnUnverifiedAdvertisementStaysOwed",
                 "P15 and negotiation restarts after every repaired write"),)),
        m("plat-phy-advertisement-unverified", PHY,
          "if (phy->local >= 0 && v >= 0 && gigabit_only((uint32_t)phy->local, u)) {", "if (true) {", "platboot1",
          "PlatPhy.P15AnUnverifiedAdvertisementStaysOwed",
          "P15 an advertisement that does not read back is written again each poll"),
        m("plat-phy-written-before-read", PHY, "if (phy->local < 0 || phy->gig < 0 || v < 0) {", "if (false) {",
          "platboot1", "PlatPhy.P16AnUnacknowledgedReadWritesNothing", "P16 no write before its read"),
        # THE OUTCOME: a restart the PHY lost, seen by what it negotiates
        m("plat-phy-outcome-unchecked", PHY, OUTCOME, "if (false) {", "platboot1", P18,
          "P18 no link at 100 after recovery", also=(P18_PACED,)),
        m("plat-phy-outcome-not-renegotiated", PHY, OUTCOME_OWED,
          OUTCOME_OWED.replace(" | CTRL_PLAT_PHY_ADV_RENEGOTIATE", ""), "platboot1", P18, "P18 one extra restart",
          also=(P18_PACED,)),
        m("plat-phy-outcome-uncounted", PHY, "\t\t\t\t\t++phy->renegotiations;\n", "", "platboot1", P18,
          "P18 the outcome's restart is counted"),
        m("plat-phy-outcome-count-wraps", PHY, "\t\t\t\tif (phy->renegotiations != 0xffffu) {\n",
          "\t\t\t\tif (true) {\n", "platboot1", "PlatPhy.P18OneRestartAPollUntilOneTakes",
          "P18 the count saturates at 0xffff"),
        m("plat-phy-outcome-at-gigabit", PHY, OUTCOME, "if (phy->adv == 0u) {", "platboot1",
          "PlatPhy.P18OnlyAMissingGigabitLinkOwesARestart", "P18 a negotiation at 1000BASE-T owes no restart"),
        m("plat-phy-resolved-before-restart", PHY, "\t\tphy->resume = CTRL_PLAT_PHY_CURRENT;\n", "", "platboot1",
          "PlatPhy.P17TheRepairedAdvertisementIsTheOneInForce", "P17 the repair restarts negotiation itself"),
        m("plat-phy-outcome-on-unadvertised", PHY, OUTCOME,
          OUTCOME.replace("phy->adv == 0u", "(phy->adv & CTRL_PLAT_PHY_ADV_OWED) == 0u"), "platboot1",
          "PlatPhy.P18OnlyAMissingGigabitLinkOwesARestart", "P18 a PHY the advertisement is not for owes no restart"),
    )


def mii_mutants(mutant: type) -> tuple:
    """The MII-only policy, including loss, readback and THE STEP's room (#878)."""
    m = mutant
    advertised = "const uint32_t advertised = CTRL_PLAT_PHY_AN_100_FULL;"
    return (
        m("mii-advertises-ten", PHY, advertised,
          "const uint32_t advertised = CTRL_PLAT_PHY_AN_100_FULL | CTRL_PLAT_PHY_AN_10_FULL;",
          "platmii", "ArtyPhy.BootAdvertisesOnly100FullWithoutGigabitRegisters", "MII only 100 full advertised",
          also=(("platmii", "ArtyPhy.TenOnlyPartnerNeverPublishesUp", "MII no unsupported negotiation"),)),
        m("mii-advertises-half", PHY, advertised,
          "const uint32_t advertised = CTRL_PLAT_PHY_AN_100_FULL | CTRL_PLAT_PHY_AN_100_HALF;",
          "platmii", "ArtyPhy.HalfDuplexPartnerNeverPublishesUp", "MII no unsupported negotiation"),
        m("mii-loss-not-latched", PHY, LATCHED, "\t\t\t\tphy->published = 0u;\n",
          "platmii", "ArtyPhy.LatchedLossRechecksWithoutAnotherRestart", "MII both link edges"),
        m("mii-advertised-once", PHY, "\t\tphy->adv = CTRL_PLAT_PHY_ADV_OWED;\n", "\t\t(void)0;\n",
          "platmii", "ArtyPhy.ResetAdvertisementIsRepairedAndRenegotiated", "MII only 100 full advertised"),
        m("mii-readback-unchecked", PHY, "if (v >= 0 && gigabit_only(u, 0u)) {", "if (true) {",
          "platmii", "ArtyPhy.DroppedAdvertisementStaysOwedUntilReadback", "MII advertisement remains owed"),
        m("mii-unacknowledged-local-written", PHY,
          "next = phy->local < 0 || v < 0 ? phy->resume : CTRL_PLAT_PHY_ADV_SET_LOCAL;",
          "next = v < 0 ? phy->resume : CTRL_PLAT_PHY_ADV_SET_LOCAL;",
          "platmii", "ArtyPhy.UnacknowledgedAdvertisementWritesNothing", "MII no write before read acknowledgement"),
        m("mii-no-room-ignored", PHY, "if (room >= (int32_t)CTRL_PLAT_PHY_STEP_US) {", "if (room >= 0) {",
          "platmii", "ArtyPhy.NoFrameWithoutStepBudget", "MII no frame without room"),
    )
