/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/* Review probe: the unchanged firmware translation unit against a Clause-22
 * peer whose read-data timing is selectable.
 *   PEER_STD=0  the lane's peer model: bit k appears in response to rising
 *               edge k and is read during that same high phase.
 *   PEER_STD=1  IEEE 802.3 22.3.4: the STA samples bit k at rising edge k;
 *               the PHY launches it 0..300 ns after rising edge k-1, so the
 *               value visible after rising edge k is frame bit k+1.
 * Registers model a typical gigabit PHY with link up and 1000FD negotiated. */
#include <stdint.h>
#include <stdio.h>
#include "milan_baremetal.c"

#ifndef PEER_STD
#define PEER_STD 1
#endif

static uint16_t registers[32];
static unsigned int clock_bit, previous_pins, command_bits, reply_bit;
static unsigned int input_word, last_status = 0xffu;
static const unsigned int target_address = 1;

void nvm_host_tick(int cycles) { (void)cycles; }

static unsigned int frame_bit(unsigned int b)
{
	if (b <= 46u || b >= 64u)
		return 1u;              /* released: pull-up */
	if (b == 47u)
		return 0u;              /* TA second bit */
	return (input_word >> (63u - b)) & 1u;
}

void milan_mac_phy_mdio_w_write(uint32_t value)
{
	if ((value & 1u) && !(previous_pins & 1u)) {
		if (clock_bit >= 32u && clock_bit < 46u)
			command_bits = (command_bits << 1) | ((value >> 2) & 1u);
		if (clock_bit == 45u) {
			/* the register address is complete at edge 45 */
			input_word = registers[command_bits & 31u];
		}
		{
			unsigned int addressed = ((command_bits >> 5) & 31u) == target_address;
			unsigned int b = PEER_STD ? clock_bit + 1u : clock_bit;

			reply_bit = (clock_bit >= 45u && addressed) ? frame_bit(b) : 1u;
			if (clock_bit < 45u)
				reply_bit = 1u;
		}
		++clock_bit;
	}
	if (!(value & 1u) && clock_bit == 64u) {
		clock_bit = 0;
		command_bits = 0;
	}
	previous_pins = value;
}

uint32_t milan_mac_phy_mdio_r_read(void) { return reply_bit; }

void milan_mac_link_status_write(uint32_t value) { last_status = value; }

int main(void)
{
	uint64_t now = 1;
	unsigned int i;
	int direct;

	registers[0] = 0x1140;  /* AN enable, 1000 full */
	registers[1] = 0x796d;  /* link up, AN complete, extended status */
	registers[2] = 0x001c;
	registers[3] = 0xc915;
	registers[4] = 0x01e1;
	registers[5] = 0xc5e1;
	registers[9] = 0x0300;
	registers[10] = 0x3c00;
	registers[15] = 0x3000;
	for (i = 0; i < 40u; ++i) {
		phy_link_tick(now);
		now += 130000000ull;
	}
	phy_address = target_address;
	direct = phy_mdio_read(1);
	printf("PROBE peer_std=%d found=%d address=%u published=%u expected=13 "
	       "bmsr_read=0x%04x bmsr_true=0x%04x\n", PEER_STD, phy_found,
	       phy_address, last_status, (unsigned int)direct & 0xffffu,
	       registers[1]);
	return last_status == 13u ? 0 : 1;
}
