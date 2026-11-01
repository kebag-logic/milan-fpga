/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/* The unchanged firmware translation unit's PHY poll against the pin-level
 * Clause-22 peer in phy_peer.h. */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include "milan_baremetal.c"
#include "phy_peer.h"

static uint64_t delay_cycles;

void nvm_host_tick(int cycles)
{
	assert(cycles >= 32);
	delay_cycles += (unsigned int)cycles;
}

static void expect_poll(uint64_t now, unsigned int expected)
{
	unsigned int before = publishes;

	phy_link_tick(now);
	assert(publishes > before);
	assert(status_word == expected);
}

int main(void)
{
	uint64_t now = 1;
	unsigned int i;
	unsigned int count;
	unsigned int up_before;
	unsigned int down_before;

	/* Standard 1000BASE-T full-duplex negotiation, at a nonzero address. */
	registers[0] = 0x1000;
	registers[1] = 0x0124;
	registers[2] = 0x001c;
	registers[4] = 0x01e1;
	registers[5] = 0x01e1;
	registers[9] = 0x0300;
	registers[10] = 0x0c00;
	registers[15] = 0x3000;
	for (i = 0; i < target_address; ++i)
		expect_poll(now++, 0);
	expect_poll(now, 13);
	count = transfers;
	phy_link_tick(now + 124999999u);
	assert(transfers == count);
	now += 125000000u;
	expect_poll(now, 13);
	up_before = ups;
	down_before = downs;
	registers[1] &= ~4u;
	now += 125000000u;
	expect_poll(now, 0);
	now += 125000000u;
	expect_poll(now, 0);
	registers[1] |= 4u;
	latched_down = 1;
	now += 125000000u;
	expect_poll(now, 13);
	now += 125000000u;
	expect_poll(now, 13);
	assert(ups == up_before + 1u && downs == down_before + 1u);
	/* Negotiated 100/10, full/half; no extended-status register on MII. */
	registers[1] = 0x24;
	for (i = 0; i < 4; ++i) {
		static const uint16_t peer_modes[4] = {
			0x101, 0x81, 0x41, 0x21
		};
		static const unsigned int expected[4] = {
			11, 3, 9, 1
		};

		registers[5] = peer_modes[i];
		now += 125000000u;
		expect_poll(now, expected[i]);
	}
	/* NAK after BMSR and BMCR succeed: 0xffff would falsely resolve 100FD. */
	registers[5] = 0x101;
	nak_register = 5;
	now += 125000000u;
	expect_poll(now, 0);
	nak_register = 32;
	now += 125000000u;
	expect_poll(now, 11);
	/* A brief loss recovered before this poll. Publish both edges now. */
	registers[1] = 0x24;
	registers[5] = 0x101;
	latched_down = 1;
	up_before = ups;
	down_before = downs;
	now += 200000000u;
	expect_poll(now, 11);
	assert(ups == up_before + 1u && downs == down_before + 1u);
	now += 125000000u;
	expect_poll(now, 11);
	assert(ups == up_before + 1u && downs == down_before + 1u);
	/* Forced 100 full; incomplete negotiation; missing ACK; clock rewind. */
	registers[0] = 0x2100;
	now += 125000000u;
	expect_poll(now, 11);
	registers[0] = 0x1000;
	registers[1] = 4;
	now += 125000000u;
	expect_poll(now, 0);
	acknowledge = 0;
	now += 125000000u;
	expect_poll(now, 0);
	acknowledge = 1;
	registers[1] = 0x24;
	registers[5] = 0x101;
	expect_poll(1, 11);
	printf("PHY_OK transfers=%u delay_cycles=%llu\n", transfers,
	       (unsigned long long)delay_cycles);
	return 0;
}
