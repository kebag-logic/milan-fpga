// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_plat_phy.h - the split placement's PHY poll (#919, part of #665): the
// release's phy_link_tick (sw/firmware/milan_baremetal/milan_baremetal.c) on
// the split's control loop. It reads the PHY's Clause-22 registers through
// the SoC's MDIO bit-bang pair and publishes the resolved link, speed and
// duplex to milan_mac_link_status, the datapath's link input (REQ-MAC-03).
// Without it that word keeps its reset value, link up, and no consumer of the
// datapath's effective link (the AVB_INTERFACE LINK_UP and LINK_DOWN
// counters and their GET_COUNTERS notification, the gPTP plane's port
// enable, the mailbox's LINK level and event) sees a link change.
//
// THE POLL, as the release's: no PHY found, one address probed per
// opportunity (PHYID1, register 2), a miss publishing link down and moving to
// the next address at once, with no blocking scan; found, BMSR (register 1),
// whose link status latches low (IEEE 802.3 22.2.4.2.13): a loss latched while
// the link was published up is published first, link down, and a second BMSR
// read then gives the current state, so a loss that recovered between two
// polls publishes both edges; a link up is resolved from BMCR (register 0),
// the forced mode when autonegotiation is off, else, once it is complete, the
// 1000BASE-T control and status (9, 10) where the extended status (15) offers
// 1000BASE-T, then the advertisement and the link partner's ability (4, 5),
// the highest common mode; incomplete negotiation, an unacknowledged read and
// a peer's master-slave fault stay link down. Registers are read in the
// release's order, both of each pair before either is judged.
//
// THE PACE. A poll starts CTRL_PLAT_PHY_POLL_US after the last one started,
// the release's PHY_POLL_NS by its own derivation: half the writer's 250 ms
// heartbeat (MILAN_NVM_HEARTBEAT_MS, scripts/nvm_shape.py), the service
// allowance the release's poll rides on and the period its link publication
// is graded to (docs/findings/397_SERVICE_BUDGET.md, "PHY poll derivation and
// simulation"); the other half is the poll's own transactions. A probe that
// misses is due again at once, as the release's.
//
// THE STEP (ctrl_loop.h). A poll is up to nine register reads, each a whole
// Clause-22 frame of 65 bit periods, too long to stand beside the records of
// a pass (it would lengthen every one still waiting, as a flash step would),
// and IEEE 802.3 22.2.2.13 gives MDC no maximum high or low time, so a poll
// may stop between two frames. So a poll is resumable, one frame at a time,
// and each frame is THE STEP's work: the platform binds ctrl_plat_phy_store_step
// as THE STEP's client, which takes the saved-state store's owed step first,
// as nvm_store_step alone would, and the PHY's next frame only in a call where
// the store took no step of a save (none, or one from its OFF, IDLE or HELD
// phase, which touches no flash and no record), with CTRL_PLAT_PHY_STEP_US
// still left before the pass's deadline. No pass carries a save's step and a
// frame, no frame stands beside an input, and the store's steps come first, so
// its worst cases in nvm_store.h stand. While a poll owes a frame the client
// reports a step owed, so under input that never leaves a pass empty its frames
// ride THE STEP's age limit: one in each pass given whole to an aged step whose
// store step is an idle one, every CTRL_LOOP_STEP_AGE + 1 centiseconds.
//
// THE BIT, as the release's phy_mdio_bit: the pins written with MDC low, a
// half period, the MDIO pin sampled, MDC raised, a half period, MDC lowered.
// The PHY drives each bit after an MDC rising edge, at most 300 ns later
// (IEEE 802.3 22.3.4), and the sample follows that edge by both halves; MDC
// is high and low at least 160 ns each in a period of at least 400 ns
// (22.2.2.13). So each half spins at least 200 ns, counting the bus accesses
// as none: ceil(CONFIG_CLOCK_FREQUENCY / CTRL_PLAT_PHY_HALF_HZ) turns, a turn
// taking at least one cycle of the clock the CPU runs on; or one turn, where arming times a run of
// CTRL_PLAT_PHY_CALIBRATION_TURNS turns on the arming clock and finds a turn
// alone is that long: the run's time, less the clock's one microsecond of
// resolution, over its turns, at least 200 ns. On the split CPU a turn, a load
// and a store of its counter, takes about 27 cycles, so one turn a half.

#ifndef CTRL_PLAT_PHY_H
#define CTRL_PLAT_PHY_H

#include <stdbool.h>
#include <stdint.h>

#include "nvm_shape_gen.h"   // MILAN_NVM_HEARTBEAT_MS, the writer's waits (nvm_shape.h)

#ifdef __cplusplus
extern "C" {
#endif

// The SoC's MDIO bit-bang pair (LiteEth's LiteEthPHYMDIO, milan_mac_phy_mdio_w and _r) and the link-status word
// (milan_soc.py MilanMAC link_status, MAC_STATUS 0x110 in docs/reference/REGISTER_MAP.md). Bus addresses; a bus
// whose mdio_w is 0 has no MDIO, and the poll touches nothing (the release's CSR_MILAN_MAC_PHY_MDIO_W_ADDR guard).
struct ctrl_plat_phy_bus {
	uintptr_t mdio_w;       // [0] MDC, [1] the output enable, [2] the driven MDIO bit
	uintptr_t mdio_r;       // [0] the MDIO pin
	uintptr_t link_status;  // [0] link up, [2:1] speed (0 10, 1 100, 2 1000 Mb/s), [3] full duplex
};

// mdio_w's fields.
#define CTRL_PLAT_PHY_MDC 0x1u
#define CTRL_PLAT_PHY_OE 0x2u
#define CTRL_PLAT_PHY_OUT 0x4u
// link_status's fields.
#define CTRL_PLAT_PHY_LINK_UP 0x1u
#define CTRL_PLAT_PHY_SPEED_LSB 1u
#define CTRL_PLAT_PHY_FULL_DUPLEX 0x8u
#define CTRL_PLAT_PHY_SPEED_10 0u
#define CTRL_PLAT_PHY_SPEED_100 1u
#define CTRL_PLAT_PHY_SPEED_1000 2u
// The Clause-22 registers the poll reads (IEEE 802.3 22.2.4) and the bits it judges.
#define CTRL_PLAT_PHY_BMCR 0u
#define CTRL_PLAT_PHY_BMSR 1u
#define CTRL_PLAT_PHY_PHYID1 2u
#define CTRL_PLAT_PHY_ANAR 4u
#define CTRL_PLAT_PHY_ANLPAR 5u
#define CTRL_PLAT_PHY_GCTRL 9u
#define CTRL_PLAT_PHY_GSTAT 10u
#define CTRL_PLAT_PHY_ESTAT 15u
#define CTRL_PLAT_PHY_BMSR_LINK 0x0004u
#define CTRL_PLAT_PHY_BMSR_AN_DONE 0x0020u
#define CTRL_PLAT_PHY_BMSR_EXTENDED 0x0100u
#define CTRL_PLAT_PHY_BMCR_SPEED_LSB 0x2000u
#define CTRL_PLAT_PHY_BMCR_AN_ENABLE 0x1000u
#define CTRL_PLAT_PHY_BMCR_FULL 0x0100u
#define CTRL_PLAT_PHY_BMCR_SPEED_MSB 0x0040u
#define CTRL_PLAT_PHY_ESTAT_1000T 0x3000u
#define CTRL_PLAT_PHY_GSTAT_FAULT 0x8000u
#define CTRL_PLAT_PHY_G_1000_FULL 0x0800u   // GCTRL's advertisement, shifted onto GSTAT's partner bits
#define CTRL_PLAT_PHY_G_1000_HALF 0x0400u
#define CTRL_PLAT_PHY_AN_100_FULL 0x0100u
#define CTRL_PLAT_PHY_AN_100_HALF 0x0080u
#define CTRL_PLAT_PHY_AN_10_FULL 0x0040u
#define CTRL_PLAT_PHY_AN_10_HALF 0x0020u
// A frame's fields (22.2.4.5): ST 01 and OP 10 (read) above the address and the register, 14 bits after the
// 32-bit preamble, then the turnaround's two bits and 16 data bits.
#define CTRL_PLAT_PHY_READ_OP 0x6u
#define CTRL_PLAT_PHY_PREAMBLE_BITS 32u
#define CTRL_PLAT_PHY_COMMAND_BITS 14u
#define CTRL_PLAT_PHY_DATA_BITS 16u
#define CTRL_PLAT_PHY_ADDRESSES 32u
// A half period's least length, as the reciprocal of a time: 1 / 200 ns (the file's head, THE BIT).
#define CTRL_PLAT_PHY_HALF_HZ 5000000u
// The turns arming times (THE BIT): long against the clock's microsecond, short beside the boot.
#define CTRL_PLAT_PHY_CALIBRATION_TURNS 1024u

// THE PACE: the release's PHY_POLL_NS, as milan_baremetal.c derives it, in microseconds.
#define CTRL_PLAT_PHY_POLL_US (MILAN_NVM_HEARTBEAT_MS * 1000u / 2u)
// One frame's stated cost in microseconds on the split CPU (THE STEP): the most measured, plus 5 %, rounded up to
// 5 us, the margin holding the call's few instructions around the frame's pins. Measured by the split boot
// simulation on the platform image, from a frame's first pin write to its release (tb/verilator/ctrl_split_boot,
// the PHY grade, which fails a frame over this figure): 16,784 CPU cycles at 1x1/1if, 167.84 us. A frame is taken
// only while this much of the pass's share is left.
#define CTRL_PLAT_PHY_STEP_US 180u

// Where a poll is: idle, or the frame it takes next.
enum ctrl_plat_phy_stage {
	CTRL_PLAT_PHY_IDLE = 0,
	CTRL_PLAT_PHY_PROBE,       // PHYID1 at the address under test
	CTRL_PLAT_PHY_STATUS,      // BMSR
	CTRL_PLAT_PHY_CURRENT,     // BMSR again: the current state
	CTRL_PLAT_PHY_CONTROL,     // BMCR
	CTRL_PLAT_PHY_EXTENDED,    // the extended status
	CTRL_PLAT_PHY_GIG_LOCAL,   // the 1000BASE-T control
	CTRL_PLAT_PHY_GIG_PEER,    // the 1000BASE-T status
	CTRL_PLAT_PHY_LOCAL,       // the advertisement
	CTRL_PLAT_PHY_PEER         // the link partner's ability
};

struct ctrl_plat_phy {
	struct ctrl_plat_phy_bus bus;
	uint64_t (*clock)(void *ctx);   // the pace's clock, microseconds; NULL while not armed
	void *ctx;
	bool found;             // a PHY answered PHYID1 at `address`
	bool polled;            // a poll has started since the last probe that missed (the release's phy_last_poll)
	uint8_t stage;          // enum ctrl_plat_phy_stage
	uint8_t address;
	uint32_t spin;          // the turns of a half period
	uint32_t started;       // the clock as the last poll took its first frame, in microseconds
	uint32_t published;     // the word last published by a poll
	int32_t bmsr;           // the BMSR the poll resolves
	int32_t local;          // the first of a pair, read before the second
};

// Arm the poll on `bus`: called once the CSR window passed its identity check, so nothing touches the MDIO pins
// of a fabric that failed it. A bus with no MDIO pair arms nothing. `clock` (microseconds, counting up; the flash
// port's, which THE STEP's deadline is read on) paces the poll and times the spin's turns (THE BIT).
void ctrl_plat_phy_arm(struct ctrl_plat_phy *phy, const struct ctrl_plat_phy_bus *bus, uint64_t (*clock)(void *ctx),
		       void *ctx);

// The PHY's share of THE STEP, `room` microseconds left of the pass's share: the poll's next frame when one is owed
// on the arming clock and CTRL_PLAT_PHY_STEP_US are left, at most one a call. True while a frame is owed: a poll in
// progress, a poll due, or a probe that missed. An unarmed poll owes nothing and touches nothing.
bool ctrl_plat_phy_step(struct ctrl_plat_phy *phy, int32_t room);

// THE STEP's client the platform binds (ctrl_loop_set_step, with nvm_store_clock): the saved-state store's step,
// as nvm_store_step, then the PHY's frame only where the store took none; ctx is the struct ctrl_plat_phy. True
// while either owes one.
bool ctrl_plat_phy_store_step(void *ctx, uint32_t deadline);

#ifdef __cplusplus
}
#endif

#endif // CTRL_PLAT_PHY_H
