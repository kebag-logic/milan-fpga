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
