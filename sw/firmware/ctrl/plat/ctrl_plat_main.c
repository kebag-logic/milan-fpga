// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_plat_main.c - main() of the split image, which ctrl_split_start.S calls
// after it sets the stack, copies .data and clears .bss (#665).
//
// It holds only what is the target's: the generated policy and streams
// (ctrl_plat_policy_gen.h), the bus map from the SoC's csr.csv
// (ctrl_plat_map_gen.h: the devices, the PHY's MDIO pair and link-status word
// among them), the LiteSPI flash port and the endless loop. The boot it runs is ctrl_plat.c's. main() never returns: after
// a refused stage the console still answers (ctrl_plat.h).

#include "ctrl_plat.h"
#include "ctrl_plat_map_gen.h"
#include "ctrl_plat_policy_gen.h"
#include "nvm_flash_litespi.h"
#ifdef CTRL_PLAT_LEDS
#include "ctrl_plat_io.h"
#include "ctrl_plat_leds.h"
#include "ctrl_plat_leds_ports.h"
#endif

static const struct ctrl_plat_policy policy = CTRL_PLAT_POLICY_INIT;
static const struct ctrl_plat_stream streams[CTRL_SRP_SOURCES] = CTRL_PLAT_STREAMS_INIT;
static struct ctrl_plat_env env = {
	.flash = &nvm_flash_litespi, .csr = CTRL_PLAT_CSR_BASE,
	.uart = {CTRL_PLAT_UART_RXTX, CTRL_PLAT_UART_TXFULL, CTRL_PLAT_UART_RXEMPTY, CTRL_PLAT_UART_EV_PENDING},
	.policy = &policy, .streams = streams, .aaf_outputs = CTRL_PLAT_AAF_OUTPUTS,
	.crf_output = CTRL_PLAT_CRF_OUTPUT, .link_rate_bps = CTRL_PLAT_LINK_BPS,
	.reboot = CTRL_PLAT_REBOOT,
	.phy = {CTRL_PLAT_PHY_MDIO_W, CTRL_PLAT_PHY_MDIO_R, CTRL_PLAT_LINK_STATUS},
};

#ifdef CTRL_PLAT_LEDS
// #1018: the SoC has the status LEDs (CTRL_PLAT_LEDS, the map header's), so
// LD2 and LD3 are written every CTRL_PLAT_LEDS_PERIOD_MS from a centisecond
// tick, once the boot reached READY (ctrl_plat_leds.h). A refused boot leaves
// both dark.
static void leds_tick(void)
{
	static unsigned centis;
	if (++centis < CTRL_PLAT_LEDS_PERIOD_MS / 10u) {
		return;
	}
	centis = 0u;
	ctrl_plat_io_write32(CTRL_PLAT_LEDS,
			    ctrl_plat_leds_word(&ctrl_plat.aecp.core, ctrl_plat_leds_counter_pair, ctrl_plat_leds_stream));
}
#endif

int main(void)
{
	ctrl_plat_generated_image(&env);
	nvm_flash_litespi_power_on();
#ifdef CTRL_PLAT_LEDS
	if (ctrl_plat_boot(&env) == CTRL_PLAT_READY) {
		(void)ctrl_loop_add_tick(&ctrl_plat.app.loop, leds_tick);
	}
#else
	(void)ctrl_plat_boot(&env);
#endif
	for (;;) {
		ctrl_plat_step();
	}
}
