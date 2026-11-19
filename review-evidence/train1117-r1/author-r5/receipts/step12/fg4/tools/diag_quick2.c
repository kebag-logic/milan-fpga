// diag_quick2.c - a quick host test of the second F-G4 diagnostic (scratch, not the repository's): the split's PHY
// poll (plat/ctrl_plat_phy.c) on one pin-level Clause-22 bus carrying two PHYs, at addresses 1 and 3, open drain
// (a PHY drives only its own address's turnaround and data), each keeping its defaults unless a whole, well-formed
// write to its address lands; then the console's milan_phy and milan_mdio typed and their lines checked.
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

// the two PHYs' registers, and the bus's frame decoder
static uint16_t regs[32][32];
static const int present[32] = {[1] = 1, [3] = 1};
static unsigned edge, previous, command, data, input, reply = 1, writes_landed[32];
// the UART
static const char *typed = "";
static char out[4096];
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
		const unsigned a = (command >> 5) & 31u;
		if (edge == 46u) input = regs[a][command & 31u];
		reply = edge == 46u ? 0u : edge == 63u ? 1u : (input >> (62u - edge)) & 1u;
		if (!present[a]) reply = 1;
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
		const unsigned addr = (command >> 5) & 31u;
		if ((command >> 10) == 5u && present[addr] && (data >> 16) == 2u) {
			const unsigned reg = command & 31u;
			regs[addr][reg] = (uint16_t)(reg == 0u ? (data & 0xffffu & ~0x8200u) : (data & 0xffffu));
			++writes_landed[addr];
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

static void type(struct ctrl_plat_console *c, const char *line)
{
	out_n = 0;
	memset(out, 0, sizeof out);
	typed = line;
	for (int pass = 0; pass < 64; ++pass) (void)ctrl_plat_console_poll(c);
	printf("%s", out);
}

int main(void)
{
	// address 1: link up at 1000BASE-T full duplex, its partner offering 1000BASE-T full and half (register 10
	// 0x3c00 | 0x0c00 = 0x3c00 holds both bits 11 and 10); address 3: a second PHY, link down, its own identity
	const uint16_t a1[] = {[0] = 0x1140, [1] = 0x796d, [2] = 0x001c, [3] = 0xc915, [4] = 0x05e1, [5] = 0xc1e1,
			       [6] = 0x000f, [9] = 0x0200, [10] = 0x3c00, [15] = 0x2000, [17] = 0xbc00};
	const uint16_t a3[] = {[0] = 0x1140, [1] = 0x7949, [2] = 0x0141, [3] = 0x0dd1, [4] = 0x0de1, [9] = 0x0300,
			       [15] = 0x3000};
	memcpy(regs[1], a1, sizeof a1);
	memcpy(regs[3], a3, sizeof a3);
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
	type(&c, "milan_phy\r");
	expect("found at the first answering address", "PHY_ARMED=1 FOUND=1 ADDR=1 ");
	expect("the partner's 1000BASE-T ability as the poll read it", " R10_NOW=00003c00\r\n");
	type(&c, "milan_mdio\r");
	expect("addresses 1 and 3 answer", "MDIO_ACK=0000000a\r\n");
	expect("address 0 unacknowledged", "A=0 R0=ffffffff R1=ffffffff R2=ffffffff");
	expect("address 1 after the advertisement",
	       "A=1 R0=00001140 R1=0000796d R2=0000001c R3=0000c915 R4=00000401 R5=0000c1e1 R6=0000000f R9=00000200 "
	       "R10=00003c00 R15=00002000 R17=0000bc00 R31=00000000\r\n");
	expect("address 3 untouched", "A=3 R0=00001140 R1=00007949 R2=00000141 R3=00000dd1 R4=00000de1 R5=00000000");
	const int lines = (int)(strstr(out, "A=4") == NULL);
	printf("[%s] no line for an address that did not answer past 1\n", lines ? "ok" : "FAIL");
	fails += !lines;
	const int ok = fails == 0 && writes_landed[1] == 3u && writes_landed[3] == 0u;
	printf("address 1 took %u writes, address 3 %u; diag_quick2: %s\n", writes_landed[1], writes_landed[3],
	       ok ? "PASS" : "FAIL");
	return ok ? 0 : 1;
}
