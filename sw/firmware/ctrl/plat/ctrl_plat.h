// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_plat.h - the split placement's control firmware on its target: the
// boot sequence and the composition of F0-F5 and F1 on the MMIO HAL (#665).
//
// THE BOOT, in the order of docs/ARCHITECTURE_HW_SW_SPLIT.md section 2, which
// Milan v1.2 5.6.1 orders (step 1, the bitstream, precedes the firmware):
//   2-3  the CSR window's identity is checked, then the generated identity and
//        static product policy are written (ctrl_plat_csr.h); the policy keeps
//        the fabric's advertiser and processor off, and nothing sets them;
//        MAAP's allocation port then takes the stream addresses away from the
//        fabric allocator before the core's MAAP starts (one MAAP owner);
//   4    the generated AEM image's CRC and form are verified (aecp_image.h);
//   5    it is installed for the core's AECP owner: the application, AECP and
//        contract 2.3's face are composed (ctrl_app.h, ctrl_app_aecp.h);
//   6-7  the saved state is read and validated, and the accepted bindings then
//        the D3 transaction applied, through the state port (nvm_store.h);
//   8    the mailbox opens with ADP held (ctrl_app_open_held), SRP attaches,
//        and AECP is released only at an accepted terminal with every
//        interface's face acknowledged (ctrl_app_open_aecp);
//   9    ADP starts last, once AECP and ACMP accept requests
//        (ctrl_app_release_adp). The console and the store's service joined
//        the loop at composition, and the loop is first serviced now.
// A stage that refuses stops the boot there: nothing after it runs, ADP never
// starts, the loop is never serviced, and only the console answers, as the
// all-fabric image keeps its BIOS console when its fabric stays disabled.
//
// THE PORTS. MAAP's allocation reaches the datapath's existing stream window
// through maap_csr_allocation (maap/README.md, "Integration") on interface
// 0's CSR window; the datapath has one window, so another interface's writes
// are dropped and counted. The platform's ACMP owner reports each talker
// source's stream from its generated identity and that allocation. SRP's
// sources are configured at boot from the generated stream table; SRP's
// licences reach the fabric through the publication block (srp_mbx.c), and
// the platform's licence port records them.

#ifndef CTRL_PLAT_H
#define CTRL_PLAT_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#include "acmp_nvm.h"
#include "ctrl_app_aecp.h"
#include "ctrl_plat_console.h"
#include "ctrl_plat_csr.h"
#include "maap_csr.h"
#include "nvm_flash.h"
#include "srp_mbx.h"

#ifdef __cplusplus
extern "C" {
#endif

// The stage the boot reached; CTRL_PLAT_READY is the control application's
// ready state, every other value names the stage that refused.
enum ctrl_plat_stage {
	CTRL_PLAT_IDENTITY = 0,  // the CSR window is not a Milan datapath
	CTRL_PLAT_IMAGE,         // the AEM image's CRC or form was refused
	CTRL_PLAT_COMPOSE,       // a module refused its configuration
	CTRL_PLAT_MAILBOX,       // the bitstream carries another mailbox contract
	CTRL_PLAT_SRP,           // SRP refused its configuration or attachment
	CTRL_PLAT_AECP,          // AECP was not released (CLOSED, or no face acknowledgement)
	CTRL_PLAT_READY          // ADP started: the entity is ready
};

// One talker source's stream, from the builder's lwSRP table
// (ctrl_plat_gen.py): its STREAM_OUTPUT's unique ID and its TSpec.
struct ctrl_plat_stream {
	uint16_t unique_id;
	uint16_t max_frame_size;
	uint16_t max_interval_frames;
	uint8_t priority_and_rank;
};

// What the target and a host test supply: the devices and the generated words.
struct ctrl_plat_env {
	const struct nvm_flash *flash;              // F1's flash port
	uintptr_t csr;                              // the datapath CSR window
	struct ctrl_plat_uart uart;
	const struct ctrl_plat_policy *policy;      // the generated identity and boot policy
	const struct ctrl_plat_stream *streams;     // CTRL_SRP_SOURCES entries
	unsigned aaf_outputs;                       // STREAM_OUTPUTs before the CRF output
	bool crf_output;                            // a CRF Media Clock Output follows them
	uint32_t link_rate_bps;
	const uint8_t *aem;                         // the paired AEM image (step 4)
	size_t aem_bytes;
	uint32_t aem_crc;
};

// The allocation MAAP last reported on one interface.
struct ctrl_plat_allocation {
	uint64_t base;
	uint16_t count;
	bool valid;
};

struct ctrl_plat {
	enum ctrl_plat_stage stage;
	const struct ctrl_plat_env *env;
	uint32_t version;                           // VERSION, read with ID
	struct ctrl_plat_console console;
	struct maap_csr maap_csr;
	struct ctrl_plat_allocation allocation[MBX_N_IF];
	uint32_t csr_dropped;                       // MAAP port writes with no window
	uint32_t licences[MBX_N_IF];                // SRP's last licence per source, bit s source s
	struct ctrl_app app;
	struct ctrl_app_config config;
	struct acmp_config acmp;
	struct acmp_env acmp_env;
	struct ctrl_app_aecp bridge;
	struct aecp_mbx aecp;
	struct aecp_config aecp_config;
	struct aecp_ports aecp_platform;
	struct aecp_face face;
	struct aecp_nvm state;
	struct acmp_nvm binding;
	struct srp_mbx srp;
	struct srp_mbx_config srp_config;
	struct srp_source sources[MBX_N_IF][CTRL_SRP_SOURCES];
};

// The image's one instance, with every pool the generated shape sizes.
extern struct ctrl_plat ctrl_plat;

// The image this firmware was generated with, into env's aem fields.
void ctrl_plat_generated_image(struct ctrl_plat_env *env);

// Run the boot to its ready state or to the stage that refused, and return it.
// env must outlive the image.
enum ctrl_plat_stage ctrl_plat_boot(const struct ctrl_plat_env *env);

// One turn of the image: a loop step once ready, else the console alone.
void ctrl_plat_step(void);

// The boot's console lines (the #396 plan counts the first as one boot).
#define CTRL_PLAT_BANNER "Milan split control firmware: boot\r\n"
#define CTRL_PLAT_READY_LINE "Milan split control firmware: ready\r\n"

#ifdef __cplusplus
}
#endif

#endif // CTRL_PLAT_H
