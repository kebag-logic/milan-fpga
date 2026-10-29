// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_plat_console.h - the split image's UART console (#665 S3, decision D6).
//
// The split image has no BIOS and no libmilan_baremetal, so it has no console
// unless its control firmware brings one (docs/design/SPLIT_CONTROL_MEMORY.md
// section 4). D6 (#665, issuecomment-6409738976) keeps only what the release
// graders read: scripts/baremetal_uart_smoke.py sends milan_status and
// milan_gettime and parses their lines, and the #396 plan counts boot banners.
// So this console answers those two commands in the lines milan_baremetal.c
// prints for them, and nothing else: every other line is refused with one
// short line.
//
// THE BOUND (#397's one-hart rule). The console is one of the event loop's
// polls (ctrl_loop.h) and never waits on the UART. A pass takes at most
// CTRL_PLAT_RX_PER_PASS bytes from the receive FIFO and stops at the end of a
// line, runs at most one command, and hands at most CTRL_PLAT_TX_PER_PASS
// bytes to the transmit FIFO while it has room. A command's whole response is
// formatted into the transmit ring in the pass that runs it, so the command is
// run only when the ring has room for the longest response; until then its
// line waits and no more input is taken. The poll returns true while bytes or
// a command are still owed, or after a full slice of input, so the loop does
// not sleep on them. The UART raises no mailbox interrupt: the split image
// defines no CTRL_MBX_WFI (mbx_plat_mmio.c), so its loop never sleeps and
// this poll runs every pass.
//
// The UART is LiteX's (litex/soc/cores/uart.py), polled, its four registers'
// addresses from the SoC's csr.csv (ctrl_plat_gen.py): a byte is read from
// RXTX while RXEMPTY is clear and released by writing the RX event bit to
// EV_PENDING, the FIFO's pop when the UART is built without rx_fifo_rx_we
// (the generator refuses a csr.csv that says otherwise); a byte is written to
// RXTX while TXFULL is clear.

#ifndef CTRL_PLAT_CONSOLE_H
#define CTRL_PLAT_CONSOLE_H

#include <stdbool.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define CTRL_PLAT_LINE_MAX 32u        // a longer line is discarded through its end
#define CTRL_PLAT_RX_PER_PASS 16u     // the UART's receive FIFO depth
#define CTRL_PLAT_TX_PER_PASS 16u     // and its transmit FIFO's
#define CTRL_PLAT_TX_BYTES 512u       // the transmit ring, a power of two
// The longest response one command queues: milan_status's three lines with
// every field at its widest. The ring holds it with room to spare.
#define CTRL_PLAT_RESPONSE_MAX 320u
#define CTRL_PLAT_UART_EV_RX 0x2u     // EV_PENDING's RX event bit

// The UART's registers, by bus address.
struct ctrl_plat_uart {
	uintptr_t rxtx;
	uintptr_t txfull;
	uintptr_t rxempty;
	uintptr_t ev_pending;
};

struct ctrl_plat_console {
	struct ctrl_plat_uart uart;
	uintptr_t csr;                 // the datapath CSR window the status reads
	bool aem_loaded;               // milan_status's AEM field: the image verified
	char line[CTRL_PLAT_LINE_MAX];
	uint8_t len;
	bool discarding;               // a line overflowed and is dropped to its end
	bool waiting;                  // a complete line waits for ring room
	uint8_t tx[CTRL_PLAT_TX_BYTES];
	uint16_t head;                 // next byte the ring takes
	uint16_t tail;                 // next byte the UART is given
	uint32_t commands;             // lines run as a command
	uint32_t refused;              // lines that were no command
	uint32_t overflows;            // lines longer than CTRL_PLAT_LINE_MAX
	uint32_t dropped;              // text bytes the ring had no room for
};

void ctrl_plat_console_init(struct ctrl_plat_console *c, const struct ctrl_plat_uart *uart, uintptr_t csr);

// Queue text for the UART; bytes past the ring's room are dropped and counted.
void ctrl_plat_console_puts(struct ctrl_plat_console *c, const char *text);

// One pass (a ctrl_poll_fn, ctx the console); true while output or a command
// is owed.
bool ctrl_plat_console_poll(void *ctx);

#ifdef __cplusplus
}
#endif

#endif // CTRL_PLAT_CONSOLE_H
