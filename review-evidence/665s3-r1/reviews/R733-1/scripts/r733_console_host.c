// Reviewer probe: the split console on a host register file with a live-looking datapath (an locked gPTP
// publication, a measured pdelay, an advancing PHC), its transcript for the smoke grader's own grade().
#include <stdint.h>
#include <stdio.h>
#include "ctrl_plat_console.h"
#include "ctrl_plat_csr.h"
#include "ctrl_plat_io.h"
#define CSR 0x90000000u
#define UART 0xf0001800u
static uint32_t regs[0x4000];
static const char *in;
static uint64_t phc = 0x1234567800000000ull;
uint32_t ctrl_plat_io_read32(uintptr_t a)
{
	if (a == UART + 0x8u) return *in == '\0';                 // RXEMPTY
	if (a == UART + 0x0u) return (uint8_t)*in;               // RXTX
	if (a == UART + 0x4u) return 0u;                         // TXFULL
	if (a >= CSR && a < CSR + sizeof regs) {
		if (a == CSR + CTRL_PLAT_CSR_TOD_RD_HI) return (uint32_t)(phc >> 32);
		if (a == CSR + CTRL_PLAT_CSR_TOD_RD_LO) return (uint32_t)phc;
		return regs[(a - CSR) / 4u];
	}
	return 0u;
}
void ctrl_plat_io_write32(uintptr_t a, uint32_t v)
{
	if (a == UART + 0x10u) { if (*in) ++in; return; }       // EV_PENDING pops
	if (a == UART + 0x0u) { putchar((int)v); return; }
	if (a == CSR + CTRL_PLAT_CSR_PTP_CMD) { phc += 123456789u; return; }
	if (a >= CSR && a < CSR + sizeof regs) regs[(a - CSR) / 4u] = v;
}
int main(int argc, char **argv)
{
	regs[CTRL_PLAT_CSR_ID / 4] = CTRL_PLAT_MILAN_ID;
	regs[CTRL_PLAT_CSR_VERSION / 4] = 0x00020060u;
	regs[CTRL_PLAT_CSR_PTP_CTRL / 4] = 0x1u;
	regs[CTRL_PLAT_CSR_ADP_CTRL / 4] = 0x0u;   // the split never sets ADP_CTRL[0]
	regs[CTRL_PLAT_CSR_PP_CTRL / 4] = 0x0u;
	regs[CTRL_PLAT_CSR_GM_LO / 4] = 0x00fffe01u; regs[CTRL_PLAT_CSR_GM_HI / 4] = 0x001bc500u;
	regs[CTRL_PLAT_CSR_PARENT_LO / 4] = 0x00fffe02u; regs[CTRL_PLAT_CSR_PARENT_HI / 4] = 0x001bc500u;
	regs[CTRL_PLAT_CSR_PDELAY / 4] = 412u;
	regs[CTRL_PLAT_CSR_AS_PATH_CMD / 4] = 0x12u;                // count 2, generation 1
	regs[CTRL_PLAT_CSR_CLKV_STAT / 4] = (1u << 16) | (1u << 1);  // ASCAPABLE, SYNC, not TU
	regs[CTRL_PLAT_CSR_GPTP_LAT / 4] = 0x00000123u;
	struct ctrl_plat_uart u = {UART, UART + 0x4u, UART + 0x8u, UART + 0x10u};
	static struct ctrl_plat_console c;
	ctrl_plat_console_init(&c, &u, CSR);
	c.aem_loaded = argc > 1 && argv[1][0] == '1';
	const char *lines[] = {"milan_status\r\n", "milan_gettime\r\n", "milan_gettime\r\n"};
	for (unsigned k = 0; k < 3; ++k) {
		printf("@@CMD %u\n", k);
		in = lines[k];
		for (unsigned pass = 0; pass < 200; ++pass) (void)ctrl_plat_console_poll(&c);
		printf("@@END\n");
	}
	fprintf(stderr, "commands %u refused %u dropped %u\n", c.commands, c.refused, c.dropped);
	return 0;
}
