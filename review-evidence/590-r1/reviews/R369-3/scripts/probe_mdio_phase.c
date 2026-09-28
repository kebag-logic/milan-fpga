/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * Reviewer probe: the unchanged firmware translation unit against two
 * Clause-22 peers that differ only in WHEN the PHY changes MDIO.
 *
 *   PEER_PHASE == 0  the committed host/simulation peer convention: at MDC
 *                    rising edge k the peer starts presenting frame bit k.
 *   PEER_PHASE == 1  IEEE 802.3 Clause 22.3.4: the station samples bit k at
 *                    rising edge k, so a PHY-sourced bit k is driven after
 *                    rising edge k-1 (0..300 ns clock-to-output); at rising
 *                    edge k the PHY starts presenting bit k+1.
 *
 * Frame positions: 0..31 preamble, 32..45 ST/OP/PHYAD/REGAD, 46 TA1 (Z),
 * 47 TA2 (0), 48..63 D15..D0, 64 idle (Z).  Z reads 1 (board pull-up).
 *
 * Each peer is also read by the LiteX BIOS reference algorithm
 * (libliteeth/mdio.c: two turnaround clocks, then sample with MDC low BEFORE
 * each rising edge), which is the reader already proven on the boards.
 */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include "milan_baremetal.c"

#ifndef PEER_PHASE
#error "define PEER_PHASE"
#endif

static uint16_t registers[32];
static unsigned int clock_bit;
static unsigned int previous_pins;
static unsigned int command_bits;
static unsigned int reply_bit = 1;
static unsigned int input_word;
static unsigned int target_address = 1;
static unsigned int status_word = 13;

void nvm_host_tick(int cycles)
{
	(void)cycles;
}

static unsigned int frame_bit(unsigned int position)
{
	if (position < 46u || position == 46u || position >= 64u)
		return 1u; /* not driven by the PHY: pull-up */
	if (position == 47u)
		return 0u;
	return (input_word >> (63u - position)) & 1u;
}

void milan_mac_phy_mdio_w_write(uint32_t value)
{
	if ((value & 1u) && !(previous_pins & 1u)) {
		if (clock_bit < 46u) {
			if (clock_bit >= 32u)
				command_bits = (command_bits << 1) | ((value >> 2) & 1u);
		} else if (clock_bit == 46u) {
			input_word = registers[command_bits & 31u];
		}
		if (((command_bits >> 5) & 31u) != target_address && clock_bit >= 45u)
			reply_bit = 1u;
		else
			reply_bit = frame_bit(clock_bit + (unsigned int)PEER_PHASE);
		if (clock_bit < 45u)
			reply_bit = 1u;
		++clock_bit;
	}
	if (!(value & 1u) && clock_bit >= 64u) {
		clock_bit = 0;
		command_bits = 0;
	}
	previous_pins = value;
}

uint32_t milan_mac_phy_mdio_r_read(void)
{
	return reply_bit;
}

void milan_mac_link_status_write(uint32_t value)
{
	status_word = value;
}

/* LiteX libliteeth/mdio.c mdio_read(), transcribed onto the same pins. */
static void litex_clock(unsigned int pins)
{
	milan_mac_phy_mdio_w_write(pins);
	milan_mac_phy_mdio_w_write(pins | 1u);
	milan_mac_phy_mdio_w_write(pins);
}

static unsigned int litex_read(unsigned int phyadr, unsigned int reg)
{
	uint32_t word = 0xffffffffu;
	unsigned int cmd = (1u << 12) | (2u << 10) | (phyadr << 5) | reg;
	unsigned int i;

	for (i = 0; i < 32u; ++i)
		litex_clock(2u | ((word >> 31) & 1u ? 4u : 0u));
	for (i = 0; i < 14u; ++i)
		litex_clock(2u | (((cmd >> (13u - i)) & 1u) ? 4u : 0u));
	litex_clock(0); /* turnaround, two clocks */
	litex_clock(0);
	word = 0;
	for (i = 0; i < 16u; ++i) {
		word <<= 1;
		if (milan_mac_phy_mdio_r_read() & 1u)
			word |= 1u;
		litex_clock(0);
	}
	litex_clock(0);
	litex_clock(0);
	clock_bit = 0;
	command_bits = 0;
	return word;
}

int main(void)
{
	uint64_t now = 1;
	int fw;
	unsigned int ref;

	/* 1000BASE-T full duplex, link up, autonegotiation complete. */
	registers[0] = 0x1140;
	registers[1] = 0x796d;
	registers[2] = 0x001c;
	registers[3] = 0xc915;
	registers[4] = 0x01e1;
	registers[5] = 0xc5e1;
	registers[9] = 0x0300;
	registers[10] = 0x3c00;
	registers[15] = 0x3000;
	phy_address = target_address;

	ref = litex_read(target_address, 1);
	fw = phy_mdio_read(1);
	printf("PHASE=%d BMSR true=0x%04x litex_reader=0x%04x firmware_reader=%s0x%04x\n",
	       PEER_PHASE, registers[1], ref, fw < 0 ? "-ack " : "",
	       (unsigned int)(fw < 0 ? 0 : fw));
	ref = litex_read(target_address, 2);
	fw = phy_mdio_read(2);
	printf("PHASE=%d PHYID1 true=0x%04x litex_reader=0x%04x firmware_reader=%s0x%04x\n",
	       PEER_PHASE, registers[2], ref, fw < 0 ? "-ack " : "",
	       (unsigned int)(fw < 0 ? 0 : fw));

	phy_found = 0;
	phy_address = 0;
	phy_last_poll = 0;
	for (int i = 0; i < 40; ++i) {
		phy_link_tick(now);
		now += 130000000u;
	}
	printf("PHASE=%d published link_status=%u (expected 13: up, 1000, full) "
	       "phy_found=%d phy_address=%u\n",
	       PEER_PHASE, status_word, phy_found, phy_address);
	return 0;
}
