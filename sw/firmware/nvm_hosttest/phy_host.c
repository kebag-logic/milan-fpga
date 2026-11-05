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

/* The index of the last write the peer took for `reg`, or -1. */
static int last_write(unsigned int reg)
{
	int found = -1;
	unsigned int i;

	for (i = 0; i < writes; ++i)
		if (written_register[i] == reg)
			found = (int)i;
	return found;
}

/* #840: the PHY init's writes, each property asserted by its own name.
 * Register 9 and register 4 carry the advertisement (IEEE 802.3-2022
 * Table 40-3, 28.2.4.1.3), and register 0 then restarts auto-negotiation
 * (22.2.4.1.7) once, after both. */
static void expect_gigabit_only_advertisement(void)
{
	const int at4 = last_write(4);
	const int at9 = last_write(9);
	const int at0 = last_write(0);
	const unsigned int adv = at4 < 0 ? 0x03e0u : written_value[at4];
	const unsigned int gig = at9 < 0 ? 0u : written_value[at9];
	const unsigned int ctl = at0 < 0 ? 0u : written_value[at0];
	const int no_10base_t_advertised = at4 >= 0 && !(adv & 0x0060u);
	const int no_100base_tx_advertised = at4 >= 0 && !(adv & 0x0180u);
	const int no_100base_t4_advertised = at4 >= 0 && !(adv & 0x0200u);
	const int selector_kept = at4 >= 0 && (adv & 0x401fu) == 0x0001u;
	const int gigabit_full_duplex_advertised = at9 >= 0 && (gig & 0x0200u);
	const int no_gigabit_half_duplex_advertised = at9 >= 0 && !(gig & 0x01ffu);
	const int auto_negotiation_restarted = at0 >= 0 &&
		(ctl & 0x9600u) == 0x1200u && restarts == 1u;
	const int restart_after_advertisement = at0 > at4 && at0 > at9;

	assert(no_10base_t_advertised);
	assert(no_100base_tx_advertised);
	assert(no_100base_t4_advertised);
	assert(selector_kept);
	assert(gigabit_full_duplex_advertised);
	assert(no_gigabit_half_duplex_advertised);
	assert(auto_negotiation_restarted);
	assert(restart_after_advertisement);
	printf("PHY_ADVERTISEMENT writes=%u reg9=0x%04x reg4=0x%04x reg0=0x%04x restarts=%u\n",
	       writes, gig, adv, ctl, restarts);
}

int main(void)
{
	uint64_t now = 1;
	unsigned int i;
	unsigned int count;
	unsigned int up_before;
	unsigned int down_before;

	/* Standard 1000BASE-T full-duplex negotiation, at a nonzero address.
	 * Register 4 starts advertising every 10/100 mode, 100BASE-T4 and both
	 * pause bits, so each bit the PHY init must clear or keep is graded. */
	registers[0] = 0x1000;
	registers[1] = 0x0124;
	registers[2] = 0x001c;
	registers[4] = 0x0fe1;
	registers[5] = 0x01e1;
	registers[9] = 0x0300;
	registers[10] = 0x0c00;
	registers[15] = 0x3000;
	for (i = 0; i < target_address; ++i)
		expect_poll(now++, 0);
	/* #840: a register the PHY init reads is not acknowledged, so the init
	 * writes nothing and the next poll retries it: first the ability
	 * register 15, then the 1000BASE-T control register 9. */
	nak_register = 15;
	expect_poll(now, 0);
	{
		const int no_write_before_its_ability_read = writes == 0u;

		assert(no_write_before_its_ability_read);
	}
	nak_register = 9;
	now += 125000000u;
	expect_poll(now, 0);
	{
		const int no_write_before_its_read = writes == 0u;

		assert(no_write_before_its_read);
	}
	nak_register = 32;
	now += 125000000u;
	{
		unsigned int before = publishes;

		phy_link_tick(now);
		expect_gigabit_only_advertisement();
		assert(publishes > before);
		assert(status_word == 13u);
	}
	count = transfers;
	phy_link_tick(now + 124999999u);
	assert(transfers == count);
	now += 125000000u;
	expect_poll(now, 13);
	{
		const int advertised_once = writes == 3u && restarts == 1u;

		assert(advertised_once);
	}
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
	/* #840: against the firmware's own advertisement, a partner offering
	 * 10/100 and no 1000BASE-T shares no mode, so the poll publishes no
	 * link, with and without the extended-status register. */
	registers[5] = 0x01e1;
	registers[10] = 0;
	now += 125000000u;
	{
		unsigned int before = publishes;
		int no_link_without_1000base_t;

		phy_link_tick(now);
		no_link_without_1000base_t = publishes > before && status_word == 0u;
		assert(no_link_without_1000base_t);
	}
	registers[1] = 0x24;
	now += 125000000u;
	expect_poll(now, 0);
	registers[10] = 0x0c00;
	/* The resolution arms below grade a PHY whose register 4 still
	 * advertises 10/100, as before the PHY init wrote it. */
	registers[4] = 0x01e1;
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
	/* #840: a PHY without 1000BASE-T full duplex ability (IEEE 802.3-2022
	 * 22.2.4.2.16, 22.2.4.4.3), as the 10/100 PHY of an MII build, keeps its
	 * own advertisement. Each is discovered afresh, is never written, and
	 * links at 100BASE-TX full duplex as before the PHY init: first without
	 * the extended-status register (its register 15 would claim the ability
	 * if read), then with one lacking bit 15.13. */
	for (i = 0; i < 2u; ++i) {
		const unsigned int writes_before = writes;
		const unsigned int restarts_before = restarts;
		unsigned int probe;
		int not_written;

		phy_found = 0;
		phy_address = 0;
		phy_advertised = 0;
		phy_published = 0;
		phy_last_poll = 0;
		registers[0] = 0x1000;
		registers[1] = i ? 0x0124 : 0x0024;
		registers[4] = 0x01e1;
		registers[5] = 0x01e1;
		registers[9] = 0x0300;
		registers[10] = 0;
		registers[15] = i ? 0x1000 : 0x3000;
		for (probe = 0; probe < target_address; ++probe)
			expect_poll(now++, 0);
		phy_link_tick(now);
		not_written = writes == writes_before && restarts == restarts_before &&
			registers[4] == 0x01e1 && registers[9] == 0x0300;
		if (i) {
			const int no_write_without_1000base_t_full_ability = not_written;

			assert(no_write_without_1000base_t_full_ability);
		} else {
			const int no_write_without_extended_status = not_written;

			assert(no_write_without_extended_status);
		}
		assert(status_word == 11u);
		now += 125000000u;
		expect_poll(now, 11);
	}
	printf("PHY_OK transfers=%u delay_cycles=%llu\n", transfers,
	       (unsigned long long)delay_cycles);
	return 0;
}
