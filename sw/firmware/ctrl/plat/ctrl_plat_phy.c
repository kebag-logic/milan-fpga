// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_plat_phy.c - the split placement's PHY poll (see ctrl_plat_phy.h).

#include "ctrl_plat_phy.h"

#include <stddef.h>
#include <string.h>

#include <generated/soc.h>

#include "ctrl_plat_io.h"
#include "nvm_store.h"

// THE BIT: a half period's turns at one cycle a turn of the clock the CPU runs on, the SoC's (CONFIG_CLOCK_FREQUENCY:
// the split CPU runs on the bus clock, milan_soc.CTRL_CPU_CD), and the run, in microseconds, past which a turn alone
// holds 200 ns: ceil(turns us / 200 ns)
#define CYCLES_HALF ((CONFIG_CLOCK_FREQUENCY + CTRL_PLAT_PHY_HALF_HZ - 1u) / CTRL_PLAT_PHY_HALF_HZ)
#define TIMED_ONE ((CTRL_PLAT_PHY_CALIBRATION_TURNS * 1000000u + CTRL_PLAT_PHY_HALF_HZ - 1u) / CTRL_PLAT_PHY_HALF_HZ)

static void spin(uint32_t turns)
{
	for (volatile uint32_t n = turns; n != 0u; n = n - 1u) {
	}
}

void ctrl_plat_phy_arm(struct ctrl_plat_phy *phy, const struct ctrl_plat_phy_bus *bus, uint64_t (*clock)(void *ctx),
		       void *ctx)
{
	memset(phy, 0, sizeof *phy);
	if (bus->mdio_w == 0u) {
		return;
	}
	phy->bus = *bus;
	phy->clock = clock;
	phy->ctx = ctx;
	// THE BIT: CYCLES_HALF turns, or one where a timed run of more than TIMED_ONE us (at least TIMED_ONE, less the
	// clock's resolution) shows a turn alone holds 200 ns
	phy->spin = CYCLES_HALF;
	const uint32_t before = (uint32_t)clock(ctx);
	spin(CTRL_PLAT_PHY_CALIBRATION_TURNS);
	if ((uint32_t)clock(ctx) - before > TIMED_ONE) {
		phy->spin = 1u;
	}
}

// One bit period (THE BIT): the pins with MDC low (the bit before's falling edge), a half period, the sample, MDC
// high, a half period; the next bit's first write, or the frame's release, lowers MDC.
static uint32_t bit(const struct ctrl_plat_phy *phy, bool drive, uint32_t out)
{
	const uint32_t pins = (drive ? CTRL_PLAT_PHY_OE : 0u) | (out != 0u ? CTRL_PLAT_PHY_OUT : 0u);
	ctrl_plat_io_write32(phy->bus.mdio_w, pins);
	spin(phy->spin);
	const uint32_t in = ctrl_plat_io_read32(phy->bus.mdio_r) & 1u;
	ctrl_plat_io_write32(phy->bus.mdio_w, pins | CTRL_PLAT_PHY_MDC);
	spin(phy->spin);
	return in;
}

// One Clause-22 read of `reg` at the poll's address, its 64 bit periods in one pass: the preamble's ones and ST OP
// PHYAD REGAD driven, then the turnaround and the 16 data bits released, the pins released after. The last 32
// samples stay in `value`: the turnaround's second bit at bit 16, D15 to D0 below it. A PHY that does not pull that
// turnaround bit low did not answer: -1, never a value (the release's acknowledgement rule).
static int32_t frame(const struct ctrl_plat_phy *phy, uint32_t reg)
{
	// the 64 bits as a shift register of two words: the preamble's 32 ones, then ST OP PHYAD REGAD, then zeros
	uint32_t hi = ~0u;
	uint32_t lo = (CTRL_PLAT_PHY_READ_OP << 10 | (uint32_t)phy->address << 5 | reg) << (32u - CTRL_PLAT_PHY_COMMAND_BITS);
	uint32_t value = 0;
	for (uint32_t k = 0; k < 64u; ++k) {
		value = value << 1 | bit(phy, k < CTRL_PLAT_PHY_PREAMBLE_BITS + CTRL_PLAT_PHY_COMMAND_BITS, hi >> 31);
		hi = hi << 1 | lo >> 31;
		lo <<= 1;
	}
	ctrl_plat_io_write32(phy->bus.mdio_w, 0u);
	return (value & 1u << CTRL_PLAT_PHY_DATA_BITS) != 0u ? -1 : (int32_t)(value & 0xffffu);
}

static uint32_t up(uint32_t speed, uint32_t full)
{
	return CTRL_PLAT_PHY_LINK_UP | speed << CTRL_PLAT_PHY_SPEED_LSB | (full != 0u ? CTRL_PLAT_PHY_FULL_DUPLEX : 0u);
}

// The highest mode the advertisement and the link partner's ability share (22.2.4.3), or link down.
static uint32_t common_mode(uint32_t common)
{
	if ((common & CTRL_PLAT_PHY_AN_100_FULL) != 0u) {
		return up(CTRL_PLAT_PHY_SPEED_100, 1u);
	}
	if ((common & CTRL_PLAT_PHY_AN_100_HALF) != 0u) {
		return up(CTRL_PLAT_PHY_SPEED_100, 0u);
	}
	if ((common & CTRL_PLAT_PHY_AN_10_FULL) != 0u) {
		return up(CTRL_PLAT_PHY_SPEED_10, 1u);
	}
	return (common & CTRL_PLAT_PHY_AN_10_HALF) != 0u ? up(CTRL_PLAT_PHY_SPEED_10, 0u) : 0u;
}

// The register each stage's frame reads, in enum ctrl_plat_phy_stage's order.
static const uint8_t regs[] = {0u, CTRL_PLAT_PHY_PHYID1, CTRL_PLAT_PHY_BMSR, CTRL_PLAT_PHY_BMSR, CTRL_PLAT_PHY_BMCR,
			       CTRL_PLAT_PHY_ESTAT, CTRL_PLAT_PHY_GCTRL, CTRL_PLAT_PHY_GSTAT, CTRL_PLAT_PHY_ANAR,
			       CTRL_PLAT_PHY_ANLPAR};

// The frame `stage` names, and what it decides: the next stage, by default the one after it, or the poll's end,
// its word published and kept as the word the next poll's latched loss is judged against (link down unless
// resolved). A probe that missed ends so, with link down.
static void take(struct ctrl_plat_phy *phy)
{
	const uint32_t stage = phy->stage;
	const int32_t v = frame(phy, regs[stage]);
	const uint32_t u = (uint32_t)v;
	uint32_t next = stage + 1u;
	uint32_t status = 0u;
	switch (stage) {
	case CTRL_PLAT_PHY_PROBE:
		if ((uint32_t)v - 1u < 0xfffeu) {   // 1 to 0xfffe: not 0, all ones, or unacknowledged (-1)
			phy->found = true;
			break;
		}
		// no PHY here: the next address, at once, and link down meanwhile (nothing is published up before a PHY is
		// found, so the word kept stays the release's, 0)
		phy->address = (uint8_t)((phy->address + 1u) % CTRL_PLAT_PHY_ADDRESSES);
		phy->polled = false;
		next = CTRL_PLAT_PHY_IDLE;
		break;
	case CTRL_PLAT_PHY_STATUS:
	case CTRL_PLAT_PHY_CURRENT:
		// a loss latched while the link was published up is published first; a second read then gives the
		// current state, unless the link stood up through the latch or the read failed
		if (stage == CTRL_PLAT_PHY_STATUS && v >= 0) {
			if ((u & CTRL_PLAT_PHY_BMSR_LINK) == 0u && (phy->published & CTRL_PLAT_PHY_LINK_UP) != 0u) {
				ctrl_plat_io_write32(phy->bus.link_status, 0u);
				phy->published = 0u;
			}
			if ((phy->published & CTRL_PLAT_PHY_LINK_UP) == 0u) {
				break;
			}
		}
		phy->bmsr = v;
		// link down, all ones or unacknowledged (u at least 0xffff) is the poll's end, link down
		next = (u & CTRL_PLAT_PHY_BMSR_LINK) == 0u || u >= 0xffffu ? CTRL_PLAT_PHY_IDLE : CTRL_PLAT_PHY_CONTROL;
		break;
	case CTRL_PLAT_PHY_CONTROL: {
		// BMCR (22.2.4.1): the forced mode with autonegotiation off; else the extended status once it is complete
		const uint32_t bmsr = (uint32_t)phy->bmsr;
		next = CTRL_PLAT_PHY_IDLE;
		if (v >= 0 && (u & CTRL_PLAT_PHY_BMCR_AN_ENABLE) == 0u) {
			status = up((u & CTRL_PLAT_PHY_BMCR_SPEED_MSB) != 0u ? CTRL_PLAT_PHY_SPEED_1000 :
				    (u & CTRL_PLAT_PHY_BMCR_SPEED_LSB) != 0u ? CTRL_PLAT_PHY_SPEED_100 : CTRL_PLAT_PHY_SPEED_10,
				    u & CTRL_PLAT_PHY_BMCR_FULL);
		} else if (v >= 0 && (bmsr & CTRL_PLAT_PHY_BMSR_AN_DONE) != 0u) {
			next = (bmsr & CTRL_PLAT_PHY_BMSR_EXTENDED) != 0u ? CTRL_PLAT_PHY_EXTENDED : CTRL_PLAT_PHY_LOCAL;
		}
		break;
	}
	case CTRL_PLAT_PHY_EXTENDED:
		next = v < 0 ? CTRL_PLAT_PHY_IDLE :
		       (u & CTRL_PLAT_PHY_ESTAT_1000T) != 0u ? CTRL_PLAT_PHY_GIG_LOCAL : CTRL_PLAT_PHY_LOCAL;
		break;
	case CTRL_PLAT_PHY_GIG_LOCAL:
	case CTRL_PLAT_PHY_LOCAL:
		phy->local = v;
		break;
	case CTRL_PLAT_PHY_GIG_PEER: {
		// 1000BASE-T (40.5.1.1): GCTRL's advertisement two bits below GSTAT's partner ability; a fault is no link
		const uint32_t common = (uint32_t)phy->local << 2 & u;
		next = CTRL_PLAT_PHY_IDLE;
		if (phy->local >= 0 && v >= 0 && (u & CTRL_PLAT_PHY_GSTAT_FAULT) == 0u) {
			next = (common & (CTRL_PLAT_PHY_G_1000_FULL | CTRL_PLAT_PHY_G_1000_HALF)) != 0u ? CTRL_PLAT_PHY_IDLE :
			       CTRL_PLAT_PHY_LOCAL;
			status = next != CTRL_PLAT_PHY_IDLE ? 0u :
				 up(CTRL_PLAT_PHY_SPEED_1000, common & CTRL_PLAT_PHY_G_1000_FULL);
		}
		break;
	}
	default:   // CTRL_PLAT_PHY_PEER
		next = CTRL_PLAT_PHY_IDLE;
		status = phy->local < 0 || v < 0 ? 0u : common_mode((uint32_t)phy->local & u);
		break;
	}
	if (next == CTRL_PLAT_PHY_IDLE) {
		ctrl_plat_io_write32(phy->bus.link_status, status);
		phy->published = status;
	}
	phy->stage = (uint8_t)next;
}

// A poll is due once the last one started CTRL_PLAT_PHY_POLL_US ago (wrap-safe: a clock that went back is a
// long time ago), at once before the first and after a probe that missed
static bool due(const struct ctrl_plat_phy *phy, uint32_t now)
{
	return !phy->polled || now - phy->started >= CTRL_PLAT_PHY_POLL_US;
}

bool ctrl_plat_phy_step(struct ctrl_plat_phy *phy, int32_t room)
{
	if (phy->clock == NULL) {
		return false;
	}
	const uint32_t now = (uint32_t)phy->clock(phy->ctx);
	if (phy->stage == CTRL_PLAT_PHY_IDLE && !due(phy, now)) {
		return false;
	}
	// a frame only with its stated cost left (THE STEP); else it stays owed
	if (room >= (int32_t)CTRL_PLAT_PHY_STEP_US) {
		if (phy->stage == CTRL_PLAT_PHY_IDLE) {
			phy->polled = true;
			phy->started = now;
			phy->stage = phy->found ? CTRL_PLAT_PHY_STATUS : CTRL_PLAT_PHY_PROBE;
		}
		take(phy);
	}
	return phy->stage != CTRL_PLAT_PHY_IDLE || due(phy, now);
}

// A store step from a save's phases, CAPTURE to VERIFY, touches the flash or a record; one from OFF, IDLE or HELD
// only judges whether a save is due (nvm_store.c, nvm_step)
_Static_assert(NVM_P_OFF < NVM_P_CAPTURE && NVM_P_IDLE < NVM_P_CAPTURE && NVM_P_HELD > NVM_P_VERIFY &&
	       NVM_P_VERIFY - NVM_P_CAPTURE == 7, "a save's phases are CAPTURE to VERIFY, and only they");

bool ctrl_plat_phy_store_step(void *ctx, uint32_t deadline)
{
	const struct nvm_status *s = nvm_store_status();
	const uint32_t steps = s->steps;
	const bool saving = (uint32_t)s->phase - NVM_P_CAPTURE <= (uint32_t)(NVM_P_VERIFY - NVM_P_CAPTURE);
	const bool store = nvm_store_step(NULL, deadline);
	// a call whose store took a step of its save leaves the PHY no room: its frame waits for the next call
	return ctrl_plat_phy_step(ctx, saving && s->steps != steps ? 0 : (int32_t)(deadline - nvm_store_clock(NULL))) ||
	       store;
}
