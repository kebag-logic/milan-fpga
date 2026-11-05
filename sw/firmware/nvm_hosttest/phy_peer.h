/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/* Pin-level Clause-22 peer behind the firmware's three MDIO and link-status
 * accessors, shared by phy_host.c and the PHY build of nvm_host.c. */
#ifndef PHY_PEER_H
#define PHY_PEER_H
#include <assert.h>
#include <stdint.h>
#include <stdio.h>

void milan_mac_phy_mdio_w_write(uint32_t value);
uint32_t milan_mac_phy_mdio_r_read(void);
void milan_mac_link_status_write(uint32_t value);

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
static unsigned int nak_register = 32;
/* #840: the Clause-22 writes this PHY accepted, in order, and the
 * auto-negotiation restarts they requested (IEEE 802.3 22.2.4.1.7). */
static unsigned int write_bits;
static unsigned int writes;
static unsigned int written_register[64];
static unsigned int written_value[64];
static unsigned int restarts;

/* IEEE 802.3 22.2.4.5: a write's TA is 10 and its data follows, all driven
 * by the station. Bit 0.9 self-clears once the restart is taken. */
static void phy_peer_write_bit(uint32_t value)
{
	unsigned int reg = command_bits & 31u;

	assert(value & 2u);
	write_bits = (write_bits << 1) | ((value >> 2) & 1u);
	reply_bit = 1;
	if (clock_bit != 63u || ((command_bits >> 5) & 31u) != target_address ||
	    !acknowledge)
		return;
	assert((write_bits >> 16) == 2u);
	assert(writes < 64u);
	written_register[writes] = reg;
	written_value[writes] = write_bits & 0xffffu;
	++writes;
	registers[reg] = (uint16_t)(write_bits & 0xffffu);
	if (reg == 0u && (registers[0] & 0x0200u)) {
		++restarts;
		registers[0] &= (uint16_t)~0x0200u;
	}
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
			write_bits = 0;
			reply_bit = 1;
		} else if ((command_bits >> 10) == 5u) {
			phy_peer_write_bit(value);
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
			/* IEEE 802.3 22.3.4: edge k launches frame bit k+1.
			 * Edge 46 launches TA zero; edge 47 launches D15. */
			reply_bit = clock_bit == 46u ? 0u : clock_bit == 63u ? 1u :
				((input_word >> (62u - clock_bit)) & 1u);
			if (!addressed || !acknowledge || (command_bits & 31u) == nak_register)
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

#endif
