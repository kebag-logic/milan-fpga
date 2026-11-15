// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_plat_phy.c - the split placement's PHY poll (see ctrl_plat_phy.h).

#include "ctrl_plat_phy.h"

#include <stddef.h>

#include "ctrl_plat_io.h"
#include "nvm_store.h"

void ctrl_plat_phy_arm(struct ctrl_plat_phy *phy, const struct ctrl_plat_phy_bus *bus)
{
	*phy = (struct ctrl_plat_phy){.bus = *bus, .armed = bus->mdio_w != 0u};
	// at least a half period's cycles, one a turn: ceil(cpu_hz / CTRL_PLAT_PHY_HALF_HZ)
	phy->spin = (bus->cpu_hz + CTRL_PLAT_PHY_HALF_HZ - 1u) / CTRL_PLAT_PHY_HALF_HZ;
}

static void spin(uint32_t turns)
{
	for (volatile uint32_t n = turns; n != 0u; n = n - 1u) {
	}
}

// One bit period (THE BIT): the pins with MDC low, a half period, the sample, MDC high, a half period, MDC low.
static uint32_t bit(const struct ctrl_plat_phy *phy, bool drive, uint32_t out)
{
	const uint32_t pins = (drive ? CTRL_PLAT_PHY_OE : 0u) | (out != 0u ? CTRL_PLAT_PHY_OUT : 0u);
	ctrl_plat_io_write32(phy->bus.mdio_w, pins);
	spin(phy->spin);
	const uint32_t in = ctrl_plat_io_read32(phy->bus.mdio_r) & 1u;
	ctrl_plat_io_write32(phy->bus.mdio_w, pins | CTRL_PLAT_PHY_MDC);
	spin(phy->spin);
	ctrl_plat_io_write32(phy->bus.mdio_w, pins);
	return in;
}

// One Clause-22 read of `reg` at the poll's address: the preamble, ST OP PHYAD REGAD driven, the turnaround
// released, the 16 data bits, the pins released. A PHY that does not pull the turnaround's second bit low did not
// answer: -1, never a value (the release's acknowledgement rule).
static int32_t frame(struct ctrl_plat_phy *phy, uint32_t reg)
{
	const uint32_t command = CTRL_PLAT_PHY_READ_OP << 10 | (uint32_t)phy->address << 5 | reg;
	for (uint32_t i = 0; i < CTRL_PLAT_PHY_PREAMBLE_BITS; ++i) {
		(void)bit(phy, true, 1u);
	}
	for (uint32_t i = CTRL_PLAT_PHY_COMMAND_BITS; i != 0u; --i) {
		(void)bit(phy, true, command >> (i - 1u) & 1u);
	}
	(void)bit(phy, false, 0u);
	const uint32_t ack = bit(phy, false, 0u);
	uint32_t value = 0;
	for (uint32_t i = 0; i < CTRL_PLAT_PHY_DATA_BITS; ++i) {
		value = value << 1 | bit(phy, false, 0u);
	}
	ctrl_plat_io_write32(phy->bus.mdio_w, 0u);
	++phy->frames;
	return ack != 0u ? -1 : (int32_t)value;
}

static void publish(const struct ctrl_plat_phy *phy, uint32_t word)
{
	ctrl_plat_io_write32(phy->bus.link_status, word);
}

static uint32_t word(uint32_t speed, bool full)
{
	return CTRL_PLAT_PHY_LINK_UP | speed << CTRL_PLAT_PHY_SPEED_LSB | (full ? CTRL_PLAT_PHY_FULL_DUPLEX : 0u);
}

// The poll's end: its word published, and kept as the word the next poll's latched loss is judged against.
static void finish(struct ctrl_plat_phy *phy, uint32_t status)
{
	publish(phy, status);
	phy->published = status;
	phy->stage = CTRL_PLAT_PHY_IDLE;
}

// The highest mode the advertisement and the link partner's ability share (22.2.4.3), or link down.
static uint32_t common_mode(uint32_t common)
{
	if ((common & CTRL_PLAT_PHY_AN_100_FULL) != 0u) {
		return word(CTRL_PLAT_PHY_SPEED_100, true);
	}
	if ((common & CTRL_PLAT_PHY_AN_100_HALF) != 0u) {
		return word(CTRL_PLAT_PHY_SPEED_100, false);
	}
	if ((common & CTRL_PLAT_PHY_AN_10_FULL) != 0u) {
		return word(CTRL_PLAT_PHY_SPEED_10, true);
	}
	return (common & CTRL_PLAT_PHY_AN_10_HALF) != 0u ? word(CTRL_PLAT_PHY_SPEED_10, false) : 0u;
}

// BMCR (22.2.4.1): the forced mode with autonegotiation off; else the extended status once negotiation is complete
static void control(struct ctrl_plat_phy *phy, int32_t value)
{
	const uint32_t c = (uint32_t)value;
	if (value < 0) {
		finish(phy, 0u);
	} else if ((c & CTRL_PLAT_PHY_BMCR_AN_ENABLE) == 0u) {
		const uint32_t speed = (c & CTRL_PLAT_PHY_BMCR_SPEED_MSB) != 0u ? CTRL_PLAT_PHY_SPEED_1000 :
				       (c & CTRL_PLAT_PHY_BMCR_SPEED_LSB) != 0u ? CTRL_PLAT_PHY_SPEED_100 :
				       CTRL_PLAT_PHY_SPEED_10;
		finish(phy, word(speed, (c & CTRL_PLAT_PHY_BMCR_FULL) != 0u));
	} else if (((uint32_t)phy->bmsr & CTRL_PLAT_PHY_BMSR_AN_DONE) == 0u) {
		finish(phy, 0u);
	} else {
		phy->stage = ((uint32_t)phy->bmsr & CTRL_PLAT_PHY_BMSR_EXTENDED) != 0u ? CTRL_PLAT_PHY_EXTENDED :
			     CTRL_PLAT_PHY_LOCAL;
	}
}

// BMSR: a loss latched while the link was published up is published first; a second read then gives the
// current state unless the link stood up through the latch
static void status(struct ctrl_plat_phy *phy, int32_t value)
{
	if (value >= 0 && ((uint32_t)value & CTRL_PLAT_PHY_BMSR_LINK) == 0u && (phy->published & CTRL_PLAT_PHY_LINK_UP) != 0u) {
		publish(phy, 0u);
		phy->published = 0u;
	}
	if (value >= 0 && (phy->published & CTRL_PLAT_PHY_LINK_UP) == 0u && phy->stage == CTRL_PLAT_PHY_STATUS) {
		phy->stage = CTRL_PLAT_PHY_CURRENT;
		return;
	}
	phy->bmsr = value;
	if (value >= 0 && value != 0xffff && ((uint32_t)value & CTRL_PLAT_PHY_BMSR_LINK) != 0u) {
		phy->stage = CTRL_PLAT_PHY_CONTROL;
	} else {
		finish(phy, 0u);
	}
}

// The frame `stage` names, and what it decides
static void take(struct ctrl_plat_phy *phy)
{
	switch (phy->stage) {
	case CTRL_PLAT_PHY_PROBE: {
		const int32_t id = frame(phy, CTRL_PLAT_PHY_PHYID1);
		if (id <= 0 || id == 0xffff) {
			// no PHY here: the next address, at once, and link down meanwhile
			phy->address = (uint8_t)((phy->address + 1u) % CTRL_PLAT_PHY_ADDRESSES);
			phy->polled = false;
			phy->stage = CTRL_PLAT_PHY_IDLE;
			publish(phy, 0u);
		} else {
			phy->found = true;
			phy->stage = CTRL_PLAT_PHY_STATUS;
		}
		break;
	}
	case CTRL_PLAT_PHY_STATUS:
	case CTRL_PLAT_PHY_CURRENT:
		status(phy, frame(phy, CTRL_PLAT_PHY_BMSR));
		break;
	case CTRL_PLAT_PHY_CONTROL:
		control(phy, frame(phy, CTRL_PLAT_PHY_BMCR));
		break;
	case CTRL_PLAT_PHY_EXTENDED: {
		const int32_t e = frame(phy, CTRL_PLAT_PHY_ESTAT);
		if (e < 0) {
			finish(phy, 0u);
		} else {
			phy->stage = ((uint32_t)e & CTRL_PLAT_PHY_ESTAT_1000T) != 0u ? CTRL_PLAT_PHY_GIG_LOCAL :
				     CTRL_PLAT_PHY_LOCAL;
		}
		break;
	}
	case CTRL_PLAT_PHY_GIG_LOCAL:
	case CTRL_PLAT_PHY_LOCAL:
		phy->local = frame(phy, phy->stage == CTRL_PLAT_PHY_LOCAL ? CTRL_PLAT_PHY_ANAR : CTRL_PLAT_PHY_GCTRL);
		++phy->stage;
		break;
	case CTRL_PLAT_PHY_GIG_PEER: {
		// 1000BASE-T (40.5.1.1): GCTRL's advertisement two bits below GSTAT's partner ability; a fault is no link
		const int32_t peer = frame(phy, CTRL_PLAT_PHY_GSTAT);
		if (phy->local < 0 || peer < 0 || ((uint32_t)peer & CTRL_PLAT_PHY_GSTAT_FAULT) != 0u) {
			finish(phy, 0u);
			break;
		}
		const uint32_t common = (uint32_t)phy->local << 2 & (uint32_t)peer;
		if ((common & (CTRL_PLAT_PHY_G_1000_FULL | CTRL_PLAT_PHY_G_1000_HALF)) != 0u) {
			finish(phy, word(CTRL_PLAT_PHY_SPEED_1000, (common & CTRL_PLAT_PHY_G_1000_FULL) != 0u));
		} else {
			phy->stage = CTRL_PLAT_PHY_LOCAL;
		}
		break;
	}
	default: {   // CTRL_PLAT_PHY_PEER
		const int32_t peer = frame(phy, CTRL_PLAT_PHY_ANLPAR);
		finish(phy, phy->local < 0 || peer < 0 ? 0u : common_mode((uint32_t)phy->local & (uint32_t)peer));
		break;
	}
	}
}

// A poll is due once the last one started CTRL_PLAT_PHY_POLL_US ago (wrap-safe: a clock that went back is a
// long time ago), at once before the first and after a probe that missed
static bool due(const struct ctrl_plat_phy *phy, uint32_t now)
{
	return !phy->polled || now - phy->started >= CTRL_PLAT_PHY_POLL_US;
}

bool ctrl_plat_phy_step(struct ctrl_plat_phy *phy, uint32_t now, uint32_t deadline)
{
	if (!phy->armed) {
		return false;
	}
	const bool owed = phy->stage != CTRL_PLAT_PHY_IDLE || due(phy, now);
	if (!owed) {
		return false;
	}
	if ((int32_t)(deadline - now) < (int32_t)CTRL_PLAT_PHY_STEP_US) {
		++phy->deferred;
		return true;
	}
	if (phy->stage == CTRL_PLAT_PHY_IDLE) {
		phy->polled = true;
		phy->started = now;
		phy->stage = phy->found ? CTRL_PLAT_PHY_STATUS : CTRL_PLAT_PHY_PROBE;
	}
	take(phy);
	return phy->stage != CTRL_PLAT_PHY_IDLE || due(phy, now);
}

// Whether a store step from `phase` touches the flash or a record: every phase but OFF, IDLE and HELD, whose
// steps only judge whether a save is due (nvm_store.c, nvm_step)
static bool saving(enum nvm_phase phase)
{
	return phase != NVM_P_OFF && phase != NVM_P_IDLE && phase != NVM_P_HELD;
}

bool ctrl_plat_phy_store_step(void *ctx, uint32_t deadline)
{
	const struct nvm_status *s = nvm_store_status();
	const uint32_t steps = s->steps;
	const bool heavy = saving(s->phase);
	const bool store = nvm_store_step(NULL, deadline);
	const uint32_t now = nvm_store_clock(NULL);
	// a call whose store took a step of its save leaves the PHY no room: its frame waits for the next call
	return ctrl_plat_phy_step(ctx, now, heavy && s->steps != steps ? now : deadline) || store;
}
