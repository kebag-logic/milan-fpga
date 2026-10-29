// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_plat_main.c - main() of the split image, which ctrl_split_start.S calls
// after it sets the stack, copies .data and clears .bss (#665).
//
// It holds only what is the target's: the generated policy and streams
// (ctrl_plat_policy_gen.h), the bus map from the SoC's csr.csv
// (ctrl_plat_map_gen.h), the LiteSPI flash port and the endless loop. The
// boot it runs is ctrl_plat.c's. main() never returns: after a refused stage
// the console still answers (ctrl_plat.h).

#include "ctrl_plat.h"
#include "ctrl_plat_map_gen.h"
#include "ctrl_plat_policy_gen.h"
#include "nvm_flash_litespi.h"

static const struct ctrl_plat_policy policy = CTRL_PLAT_POLICY_INIT;
static const struct ctrl_plat_stream streams[CTRL_SRP_SOURCES] = CTRL_PLAT_STREAMS_INIT;
static struct ctrl_plat_env env = {
	.flash = &nvm_flash_litespi, .csr = CTRL_PLAT_CSR_BASE,
	.uart = {CTRL_PLAT_UART_RXTX, CTRL_PLAT_UART_TXFULL, CTRL_PLAT_UART_RXEMPTY, CTRL_PLAT_UART_EV_PENDING},
	.policy = &policy, .streams = streams, .aaf_outputs = CTRL_PLAT_AAF_OUTPUTS,
	.crf_output = CTRL_PLAT_CRF_OUTPUT, .link_rate_bps = CTRL_PLAT_LINK_BPS,
};

int main(void)
{
	ctrl_plat_generated_image(&env);
	nvm_flash_litespi_power_on();
	(void)ctrl_plat_boot(&env);
	for (;;) {
		ctrl_plat_step();
	}
}
