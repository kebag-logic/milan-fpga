/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/* Pin-level Clause-22 peer for the unchanged firmware translation unit. */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include "milan_baremetal.c"

static uint16_t registers[32];
static unsigned int clock_bit;
static unsigned int previous_pins;
static unsigned int command_bits;
static unsigned int reply_bit;
static unsigned int transfers;
static unsigned int target_address = 7;
static unsigned int input_word;
static unsigned int status_word;
static unsigned int ups;
static unsigned int downs;
static unsigned int publishes;
static int latched_down;
static int acknowledge = 1;
static uint64_t delay_cycles;

void nvm_host_tick(int cycles)
{
	assert(cycles >= 32);
	delay_cycles += (unsigned int)cycles;
}

void milan_mac_phy_mdio_w_write(uint32_t value)
{
	if ((value & 1u) && !(previous_pins & 1u)) {
		assert(clock_bit < 64u);
		if (clock_bit < 46u) {
			assert(value & 2u);
			if (clock_bit < 32u)
				assert(value & 4u);
			else
				command_bits = (command_bits << 1) | ((value >> 2) & 1u);
			reply_bit = 1;
		} else {
			unsigned int addressed = ((command_bits >> 5) & 31u) == target_address;

			assert(!(value & 2u));
			assert((command_bits >> 10) == 6u);
			if (clock_bit == 46u) {
				unsigned int reg = command_bits & 31u;

				input_word = registers[reg];
				if (reg == 1u && latched_down && addressed) {
					input_word &= ~4u;
					latched_down = 0;
				}
			}
			reply_bit = clock_bit < 48u ? (clock_bit == 46u) :
				((input_word >> (63u - clock_bit)) & 1u);
			if (!addressed || !acknowledge)
				reply_bit = 1;
		}
		++clock_bit;
	}
	if (!(value & 1u) && clock_bit == 64u) {
		clock_bit = 0;
		command_bits = 0;
		++transfers;
	}
	previous_pins = value;
}

uint32_t milan_mac_phy_mdio_r_read(void)
{
	return reply_bit;
}

void milan_mac_link_status_write(uint32_t value)
{
	assert(value < 16u);
	if ((status_word ^ value) & 1u) {
		if (value & 1u)
			++ups;
		else
			++downs;
	}
	status_word = value;
	++publishes;
	printf("PHY_PUBLISH value=%u up=%u down=%u\n", value, ups, downs);
}

static void expect_poll(uint64_t now, unsigned int expected)
{
	unsigned int before = publishes;

	phy_link_tick(now);
	assert(publishes == before + 1u);
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
		static const uint16_t peer_modes[4] = {0x101, 0x81, 0x41, 0x21};
		static const unsigned int expected[4] = {11, 3, 9, 1};

		registers[5] = peer_modes[i];
		now += 125000000u;
		expect_poll(now, expected[i]);
	}
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
