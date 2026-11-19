// diag_quick.c - a quick host test of the F-G4 diagnostic (scratch, not the repository's): the split's PHY poll
// (plat/ctrl_plat_phy.c) on a pin-level Clause-22 PHY at address 1 that keeps its defaults unless a whole,
// well-formed write lands (ST 01, OP 01, its address, TA 10, 16 data bits, sampled on MDC's rising edges), then the
// console's milan_phy (plat/ctrl_plat_console.c) typed and its line checked.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "ctrl_plat_console.h"
#include "ctrl_plat_io.h"
#include "ctrl_plat_phy.h"
#include "ctrl_plat_csr.h"
#include "nvm_store.h"

enum { MDIO_W = 0x1004, MDIO_R = 0x1008, LINK = 0x101c, RXTX = 0x2000, TXFULL = 0x2004, RXEMPTY = 0x2008,
       EVP = 0x200c };

// the PHY: registers, and the frame decoder
static uint16_t regs[32];
static unsigned edge, previous, command, data, input, reply = 1, writes_landed;
static const unsigned address = 1;
// the UART
static const char *typed = "";
static char out[2048];
static size_t out_n;
static uint64_t now_us;

static void rise(uint32_t v)
{
	if (edge < 46u) {
		if (edge >= 32u) command = command << 1 | ((v >> 2) & 1u);
		reply = 1;
	} else if ((command >> 10) == 5u) {
		data = (data << 1 | ((v >> 2) & 1u)) & 0x3ffffu;
		reply = 1;
	} else {
		const int mine = ((command >> 5) & 31u) == address;
		if (edge == 46u) input = regs[command & 31u];
		reply = edge == 46u ? 0u : edge == 63u ? 1u : (input >> (62u - edge)) & 1u;
		if (!mine) reply = 1;
	}
	++edge;
}

uint32_t ctrl_plat_io_read32(uintptr_t a)
{
	if (a == MDIO_R) return reply;
	if (a == RXEMPTY) return *typed == '\0';
	if (a == RXTX) return (uint8_t)*typed++;
	return 0;
}

void ctrl_plat_io_write32(uintptr_t a, uint32_t v)
{
	if (a == RXTX) {
		if (out_n + 1 < sizeof out) out[out_n++] = (char)v;
		return;
	}
	if (a != MDIO_W) return;
	if ((v & 1u) && !(previous & 1u)) rise(v);
	if (!(v & 1u) && edge == 64u) {
		if ((command >> 10) == 5u && ((command >> 5) & 31u) == address && (data >> 16) == 2u) {
			const unsigned reg = command & 31u;
			regs[reg] = (uint16_t)(reg == 0u ? (data & 0xffffu & ~0x8200u) : (data & 0xffffu));
			++writes_landed;
		}
		edge = command = data = 0;
		reply = 1;
	}
	previous = v;
}

// the store and the CSR window the two units reference, stubbed
static struct nvm_status store_status;
bool nvm_store_owed(void) { return false; }
const struct nvm_status *nvm_store_status(void) { return &store_status; }
bool nvm_store_step(void *ctx, uint32_t deadline) { (void)ctx; (void)deadline; return false; }
uint32_t nvm_store_clock(void *ctx) { (void)ctx; return (uint32_t)now_us; }
void ctrl_plat_csr_status(uintptr_t csr, struct ctrl_plat_status *s) { (void)csr; memset(s, 0, sizeof *s); }
bool ctrl_plat_csr_tod(uintptr_t csr, uint64_t *ns) { (void)csr; *ns = 0; return false; }

static uint64_t clock_us(void *ctx) { (void)ctx; return now_us; }

static int fails;
static void expect(const char *what, const char *needle)
{
	const int ok = strstr(out, needle) != NULL;
	printf("[%s] %s: %s\n", ok ? "ok" : "FAIL", what, needle);
	fails += !ok;
}

int main(void)
{
	// an RTL8211E's defaults, link up at 1000BASE-T full duplex (#590's board probe: BMSR 0x796d, PHYID1 0x001c)
	regs[0] = 0x1140; regs[1] = 0x796d; regs[2] = 0x001c; regs[4] = 0x01e1; regs[5] = 0x01e1;
	regs[9] = 0x0300; regs[10] = 0x3c00; regs[15] = 0x3000;
	struct ctrl_plat_phy phy;
	const struct ctrl_plat_phy_bus bus = {MDIO_W, MDIO_R, LINK};
	ctrl_plat_phy_arm(&phy, &bus, clock_us, NULL);
	for (int call = 0; call < 400; ++call) {   // two polls' worth of calls, the room always there
		(void)ctrl_plat_phy_step(&phy, 100000);
		now_us += 1000u;
	}
	struct ctrl_plat_console c;
	const struct ctrl_plat_uart uart = {RXTX, TXFULL, RXEMPTY, EVP};
	ctrl_plat_console_init(&c, &uart, 0x90000000u);
	out_n = 0;
	memset(out, 0, sizeof out);
	typed = "milan_phy\r";
	for (int pass = 0; pass < 64; ++pass) (void)ctrl_plat_console_poll(&c);
	printf("%s", out);
	expect("armed, found at the PHY's address", "PHY_ARMED=1 FOUND=1 ADDR=1 ");
	expect("idle, verified, no renegotiation", "STAGE=0 ADV=0 RENEG=0 ");
	expect("three writes, one restart", "WRITES=3 RESTARTS=1 ");
	expect("published 1000BASE-T full duplex up", "LINK=0000000d ");
	expect("registers 4 and 9 before the writes", "R4_BEFORE=000001e1 R9_BEFORE=00000300 ");
	expect("their read-back", "R4=00000001 R9=00000200 ");
	expect("the latest poll's register 9 and 4", "R9_NOW=00000200 R4_NOW=fffffffe ");
	expect("register 0 before the restart", "R0=00001140 ");
	printf("the PHY took %u writes; diag_quick: %s\n", writes_landed, fails == 0 && writes_landed == 3 ? "PASS" : "FAIL");
	return fails == 0 && writes_landed == 3 ? 0 : 1;
}
