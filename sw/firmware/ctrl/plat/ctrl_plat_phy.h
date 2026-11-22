// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_plat_phy.h - the split placement's PHY poll (#919, part of #665): the
// release's phy_link_tick (sw/firmware/milan_baremetal/milan_baremetal.c) on
// the split's control loop. It reads the PHY's Clause-22 registers through
// the SoC's MDIO bit-bang pair and publishes the resolved link, speed and
// duplex to milan_mac_link_status, the datapath's link input (REQ-MAC-03).
// Without it that word keeps its reset value, link down where the poll owns it
// (#972), and no consumer of the datapath's effective link (the AVB_INTERFACE
// LINK_UP and LINK_DOWN counters and their GET_COUNTERS notification, the gPTP
// plane's port enable, the mailbox's LINK level and event, which the split's
// MAAP, ADP and SRP follow) sees a link.
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
// THE ADVERTISEMENT (#840), the release's PHY init: the MAC runs at 1 Gb/s
// only, so a PHY with 1000BASE-T full duplex ability (the extended status,
// 22.2.4.4.3, behind BMSR's extended capability) advertises 1000BASE-T full
// duplex alone: register 9 keeps its MASTER-SLAVE bits and advertises full
// duplex (Table 40-3), register 4 drops 10BASE-T, 100BASE-TX and 100BASE-T4
// and the reserved bit 14 (Table 28B-1, Table 28-2), then register 0 enables
// and restarts autonegotiation with reset and isolate clear (22.2.4.1), as
// 28.2.4.1.3 asks after a change. A partner without 1000BASE-T then gets no
// link, published down, rather than a 100 Mb/s link the MAC is silent on. A
// PHY without that ability is a 10/100 PHY and is never written. It is done
// in the poll's first frames after its first BMSR read, before the current
// state is resolved, as the release's (so a link the PHY formed before the
// restart is never published), at boot and again after every link loss,
// a published link going down (#919): registers 4 and 9 are read, written
// and read back, and the poll owes it again until the read-back holds the
// advertisement (verified). Negotiation restarts after every write that
// repaired the advertisement, the registers as read not holding it (a PHY
// reset to its defaults, a write the PHY dropped), so the abilities in force
// are always the ones written and verified (28.2.4.1.3: a changed
// advertisement is negotiated again). A PHY that still held the advertisement,
// at boot as after a loss, is written and not restarted (#972): the boot forms
// the link once, where the release's init restarts negotiation at every boot
// whatever the PHY held, and a restart, which latches a loss of its own, never
// restarts again. Holding it is BMCR as read negotiating, autonegotiation
// enabled (0.12) with reset (0.15) and isolate (0.10) clear, and registers 4
// and 9 as read the advertisement (#840): a PHY forced to a mode with
// autonegotiation off (22.2.4.1.4), isolated (22.2.4.1.6) or resetting is
// restarted, whatever 4 and 9 hold. A negotiation in force that predates the
// advertisement is THE OUTCOME's, below; a PHY that never takes a write is
// restarted at each try.
//
// THE LINK BEFORE THE FIRST POLL (#972). Where this poll owns the word, the
// split placement with an MDIO pair, milan_mac_link_status resets to link
// down (milan_soc.py's MilanMAC, sw/litex/mac_link_status.py), and arming
// publishes link down again before the poll's first frame, for a CPU reset
// alone (LiteX's cpu_rst), which keeps the word. So the datapath's effective
// link, which the gPTP plane's port and the mailbox's LINK level follow (the
// split builds no fabric MAAP engine), is down from reset until a poll publishes
// the PHY's verified link: nothing is sent on a link the advertisement then
// renegotiates, on a reload that kept the PHY's link, or by a boot refused
// before the arm (the CSR identity check), and ADP starts DOWN and draws its
// LINK_UP delay on the published link (Milan v1.2 5.6.3.5.3). A bus with no
// MDIO pair has no owner here and publishes nothing: its word resets to link
// up, the only link such a board has, as the all-fabric placement's does.
// An unacknowledged read writes nothing; the next poll retries.
//
// THE OUTCOME. The restart's own write is never read back: its bit clears
// itself (22.2.4.1.7), so a restart the PHY dropped leaves the negotiation
// before it in force while 4 and 9 read back. So the restart is verified by
// what it negotiates: a negotiation complete (BMSR's autonegotiation complete)
// on a link up that shares no 1000BASE-T mode in 9 and 10 (40.5.1.1), while the
// advertisement is verified, is that earlier negotiation. Its link is resolved
// as the release resolves it, from 4 and 5, which share no mode below 1000
// Mb/s, so it is published down, and the advertisement is owed again with its
// restart taken whatever the PHY holds, by the next poll, counted
// (renegotiations). A restart that took drops the link until the negotiation
// completes, and the check waits for both: a poll that restarted negotiation
// reads BMSR again after the restart and resolves from that, never from the
// read before it. So it restarts at most once a poll and never during a
// negotiation. BMCR not negotiating on a PHY the advertisement is for, a
// forced mode, isolate or a reset, is no negotiation in force either: link
// down, the advertisement owed again with its restart, counted, so a forced
// mode is never published up (#840), a restart the PHY lost included. On a PHY
// the advertisement is not for, a forced mode is published as the release
// publishes it.
//
// THE PACE. A poll starts CTRL_PLAT_PHY_POLL_US after the last one started,
// the release's PHY_POLL_NS by its own derivation: half the writer's 250 ms
// heartbeat (MILAN_NVM_HEARTBEAT_MS, scripts/nvm_shape.py), the service
// allowance the release's poll rides on and the period its link publication
// is graded to (docs/findings/397_SERVICE_BUDGET.md, "PHY poll derivation and
// simulation"); the other half is the poll's own transactions. A probe that
// misses is due again at once, as the release's.
//
// THE STEP (ctrl_loop.h). A poll is up to nine register reads, and nine more
// frames where the advertisement is owed, six reads (15, 4, 9, 0, then 4 and 9
// back) and three writes (9, 4, 0; the restart's write omitted where the PHY
// still held the advertisement), each a whole Clause-22 frame of 64 bit periods
// (CTRL_PLAT_PHY_FRAME_BITS), too long to stand beside the records of
// a pass (it would lengthen every one still waiting, as a flash step would),
// and IEEE 802.3 22.2.2.13 gives MDC no maximum high or low time, so a poll
// may stop between two frames. So a poll is resumable, one frame at a time,
// and each frame is THE STEP's work: the platform binds ctrl_plat_phy_store_step
// as THE STEP's client. A call that owes the store a centisecond's step takes it
// first, as nvm_store_step alone would, and the PHY's next frame only where that
// step was none of a save (none, or one from its OFF, IDLE or HELD phase, which
// touches no flash and no record). A call that owes no centisecond's step takes
// an owed frame, and the store takes none of its steps past the centisecond's
// (#920) in that call; a call that owes neither takes the store's. Each frame
// needs CTRL_PLAT_PHY_STEP_US still left before the pass's deadline. No call
// carries a save's step and a frame, no frame stands beside an input, and the
// centisecond's step keeps its first place, so the store's slowest pace and its
// worst cases in nvm_store.h stand, and the heaviest call is still a save's
// step. The poll keeps its period through a save: its 125 ms publishes the loss
// BMSR latched (IEEE 802.3 22.2.4.2.13) and the link's return that re-enables
// the gPTP port (IEEE 802.1AS-2011 10.2.4.11; Milan v1.2 4.2.6.2.5), which may
// not wait a save's 1 to 22 s (#665's ruling of 2026-11-17). While a poll owes a
// frame the client reports a step owed, so under input that never leaves a pass
// empty its frames ride THE STEP's age limit: one in each pass given whole to an
// aged step whose store step is an idle one, every CTRL_LOOP_STEP_AGE + 1
// centiseconds.
//
// THE BIT, the release's phy_mdio_bit with its last write folded into the
// next bit's first: the pins written with MDC low, which lowers the bit
// before's MDC with this bit's value, a half period, the MDIO pin sampled,
// MDC raised, a half period; the frame's release lowers its last. The PHY
// drives each bit after an MDC rising edge, at most 300 ns later (IEEE 802.3
// 22.3.4), and the sample follows that edge by both halves; the STA's own bit
// changes a half period after the edge it was sampled on and a half period
// before the next, past 22.3.4's 10 ns of hold and setup; MDC is high and low
// at least 160 ns each in a period of at least 400 ns (22.2.2.13). So each
// half spins at least 200 ns, counting the bus accesses as none:
// ceil(CONFIG_CLOCK_FREQUENCY / CTRL_PLAT_PHY_HALF_HZ) turns, a turn taking at
// least one cycle of the clock the CPU runs on; or one turn, where arming
// times a run of CTRL_PLAT_PHY_CALIBRATION_TURNS turns on the arming clock and
// finds a turn alone is that long: the run's time, less the clock's one
// microsecond of resolution, over its turns, at least 200 ns. On the split CPU
// a turn, a load and a store of its counter, takes about 27 cycles, so one
// turn a half.

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
#define CTRL_PLAT_PHY_BMCR_RESET 0x8000u
#define CTRL_PLAT_PHY_BMCR_SPEED_LSB 0x2000u
#define CTRL_PLAT_PHY_BMCR_AN_ENABLE 0x1000u
#define CTRL_PLAT_PHY_BMCR_ISOLATE 0x0400u
#define CTRL_PLAT_PHY_BMCR_AN_RESTART 0x0200u
#define CTRL_PLAT_PHY_BMCR_FULL 0x0100u
#define CTRL_PLAT_PHY_BMCR_SPEED_MSB 0x0040u
#define CTRL_PLAT_PHY_ESTAT_1000T 0x3000u
#define CTRL_PLAT_PHY_ESTAT_1000T_FULL 0x2000u
// THE ADVERTISEMENT's fields: register 4's 10BASE-T, 100BASE-TX and 100BASE-T4 bits (5 to 9) and its reserved
// bit 14; register 9's MASTER-SLAVE bits (12 to 10) and its 1000BASE-T full and half duplex.
#define CTRL_PLAT_PHY_ANAR_BELOW_GIGABIT 0x03e0u
#define CTRL_PLAT_PHY_ANAR_RESERVED 0x4000u
#define CTRL_PLAT_PHY_GCTRL_MASTER_SLAVE 0x1c00u
#define CTRL_PLAT_PHY_GCTRL_1000_FULL 0x0200u
#define CTRL_PLAT_PHY_GCTRL_1000_HALF 0x0100u
#define CTRL_PLAT_PHY_GSTAT_FAULT 0x8000u
#define CTRL_PLAT_PHY_G_1000_FULL 0x0800u   // GCTRL's advertisement, shifted onto GSTAT's partner bits
#define CTRL_PLAT_PHY_G_1000_HALF 0x0400u
#define CTRL_PLAT_PHY_AN_100_FULL 0x0100u
#define CTRL_PLAT_PHY_AN_100_HALF 0x0080u
#define CTRL_PLAT_PHY_AN_10_FULL 0x0040u
#define CTRL_PLAT_PHY_AN_10_HALF 0x0020u
// A frame's fields (22.2.4.5): ST 01 and OP 10 (read) above the address and the register, 14 bits after the
// 32-bit preamble, then the turnaround's two bits and 16 data bits; a write's ST 01 and OP 01, its turnaround 10
// and its data driven too, the whole frame's 64 bits.
#define CTRL_PLAT_PHY_READ_OP 0x6u
#define CTRL_PLAT_PHY_WRITE_OP 0x5u
#define CTRL_PLAT_PHY_WRITE_TA 0x2u
#define CTRL_PLAT_PHY_PREAMBLE_BITS 32u
#define CTRL_PLAT_PHY_COMMAND_BITS 14u
#define CTRL_PLAT_PHY_DATA_BITS 16u
#define CTRL_PLAT_PHY_FRAME_BITS 64u
// THE ADVERTISEMENT's state (struct ctrl_plat_phy's adv), 0 once verified: owed; owed with its restart taken
// whatever the PHY holds (THE OUTCOME's); not the PHY's, a 10/100 PHY never written.
#define CTRL_PLAT_PHY_ADV_OWED 0x1u
#define CTRL_PLAT_PHY_ADV_RENEGOTIATE 0x2u
#define CTRL_PLAT_PHY_ADV_NONE 0x4u
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
// the PHY grade, which fails a frame over this figure), reads and the advertisement's writes alike: 14,537 CPU
// cycles at 1x1/1if, 145.37 us, and 14,545 at 8x8/1if, 145.45 us (14,537 and 14,512 before the advertisement). A
// frame is taken only while this much of the pass's share is left. It is under a fifth of a store's
// read-back step (0.77 ms, nvm_store.h), so a step call that carries a frame and an idle store step is lighter than
// one that carries a save's flash step, which the CPU budget harness measures in every pass class THE STEP enters.
#define CTRL_PLAT_PHY_STEP_US 155u

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
	CTRL_PLAT_PHY_PEER,        // the link partner's ability
	// THE ADVERTISEMENT, after STATUS where it is owed, then the stage STATUS chose
	CTRL_PLAT_PHY_ADV_ABILITY,      // the extended status: 1000BASE-T full duplex ability
	CTRL_PLAT_PHY_ADV_LOCAL,        // register 4, as the PHY holds it
	CTRL_PLAT_PHY_ADV_GIG,          // register 9
	CTRL_PLAT_PHY_ADV_CONTROL,      // register 0
	CTRL_PLAT_PHY_ADV_SET_GIG,      // write 9: MASTER-SLAVE kept, 1000BASE-T full duplex
	CTRL_PLAT_PHY_ADV_SET_LOCAL,    // write 4: no 10/100, no reserved bit
	CTRL_PLAT_PHY_ADV_RESTART,      // write 0: autonegotiation enabled and restarted
	CTRL_PLAT_PHY_ADV_CHECK_LOCAL,  // read 4 back
	CTRL_PLAT_PHY_ADV_CHECK_GIG     // read 9 back: verified, or owed again
};

struct ctrl_plat_phy {
	struct ctrl_plat_phy_bus bus;
	uint64_t (*clock)(void *ctx);   // the pace's clock, microseconds; NULL while not armed
	void *ctx;
	bool found;             // a PHY answered PHYID1 at `address`
	bool polled;            // a poll has started since the last probe that missed (the release's phy_last_poll)
	uint8_t stage;          // enum ctrl_plat_phy_stage
	uint8_t address;
	uint8_t adv;            // THE ADVERTISEMENT: 0 verified, else CTRL_PLAT_PHY_ADV_* (owed, or not the PHY's)
	uint8_t resume;         // the stage the poll takes after the advertisement
	uint16_t renegotiations;   // THE OUTCOME's restarts owed, saturating
	uint32_t spin;          // the turns of a half period
	uint32_t started;       // the clock as the last poll took its first frame, in microseconds
	uint32_t published;     // the word last published by a poll
	int32_t bmsr;           // the BMSR the poll resolves
	int32_t local;          // the first of a pair, read before the second; register 4 for the advertisement
	int32_t gig;            // register 9 as read for the advertisement
	int32_t control;        // register 0 as read for the advertisement
};

// Arm the poll on `bus`: called once the CSR window passed its identity check, so nothing touches the MDIO pins
// of a fabric that failed it. It publishes link down first (THE LINK BEFORE THE FIRST POLL). A bus with no MDIO pair
// arms nothing and publishes nothing. `clock` (microseconds, counting up; the flash port's, which THE STEP's deadline
// is read on) paces the poll and times the spin's turns (THE BIT).
void ctrl_plat_phy_arm(struct ctrl_plat_phy *phy, const struct ctrl_plat_phy_bus *bus, uint64_t (*clock)(void *ctx),
		       void *ctx);

// The PHY's share of THE STEP, `room` microseconds left of the pass's share: the poll's next frame when one is owed
// on the arming clock and CTRL_PLAT_PHY_STEP_US are left, at most one a call. True while a frame is owed: a poll in
// progress, a poll due, or a probe that missed. An unarmed poll owes nothing and touches nothing.
bool ctrl_plat_phy_step(struct ctrl_plat_phy *phy, int32_t room);

// THE STEP's client the platform binds (ctrl_loop_set_step, with nvm_store_clock): where a centisecond's step is
// owed (nvm_store_owed), the saved-state store's step, as nvm_store_step, then the PHY's frame only where that step
// was none of a save; where none is owed, the PHY's owed frame, and the store's step only where no frame is owed;
// ctx is the struct ctrl_plat_phy. True while either owes one.
bool ctrl_plat_phy_store_step(void *ctx, uint32_t deadline);

#ifdef __cplusplus
}
#endif

#endif // CTRL_PLAT_PHY_H
