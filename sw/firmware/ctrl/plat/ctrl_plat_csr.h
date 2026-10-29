// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_plat_csr.h - the datapath CSR window in the split placement (#665 S3).
//
// The split image keeps the Milan CSR map (docs/design/SPLIT_CONTROL_MEMORY.md
// section 4). Its control firmware programs the generated identity and the
// static product policy there at boot (REQUIREMENTS.md:22-23; step 3 of the
// boot sequence, docs/ARCHITECTURE_HW_SW_SPLIT.md section 2), with the writes
// sw/firmware/milan_baremetal/milan_baremetal.c's configure_fabric() makes in
// the all-fabric image, in its order and from the same derivation
// (sw/litex/boot_policy.py). It also reads the status the console reports.
// Offsets are docs/reference/REGISTER_MAP.md's.
//
// Unlike the all-fabric firmware, the split never sets the two compatibility
// enables, ADP_CTRL[0] and PP_CTRL[0]: the core owns ADP and AECP, so a fabric
// advertiser or processor enabled beside it would be a second owner
// (ARCHITECTURE_HW_SW_SPLIT.md section 1). The policy clears both, as
// configure_fabric() does before its AEM check, and nothing here sets them.

#ifndef CTRL_PLAT_CSR_H
#define CTRL_PLAT_CSR_H

#include <stdbool.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define CTRL_PLAT_CSR_ID          0x000u
#define CTRL_PLAT_CSR_VERSION     0x004u
#define CTRL_PLAT_CSR_MAC_CTRL    0x100u
#define CTRL_PLAT_CSR_MAC_ADDR_LO 0x108u
#define CTRL_PLAT_CSR_MAC_ADDR_HI 0x10cu
#define CTRL_PLAT_CSR_PTP_CTRL    0x500u
#define CTRL_PLAT_CSR_PTP_CMD     0x520u
#define CTRL_PLAT_CSR_TOD_RD_LO   0x530u
#define CTRL_PLAT_CSR_TOD_RD_HI   0x534u
#define CTRL_PLAT_CSR_ADP_CTRL    0x600u
#define CTRL_PLAT_CSR_ADP_EID_LO  0x604u
#define CTRL_PLAT_CSR_ADP_EID_HI  0x608u
#define CTRL_PLAT_CSR_ADP_MID_LO  0x60cu
#define CTRL_PLAT_CSR_ADP_MID_HI  0x610u
#define CTRL_PLAT_CSR_GM_LO       0x624u
#define CTRL_PLAT_CSR_GM_HI       0x628u
#define CTRL_PLAT_CSR_AAF_CTRL    0x654u
#define CTRL_PLAT_CSR_LWSRP_CTRL  0x680u
#define CTRL_PLAT_CSR_LWSRP_VID   0x684u
#define CTRL_PLAT_CSR_MAAP_CTRL   0x6ccu
#define CTRL_PLAT_CSR_PDELAY      0x6e4u
#define CTRL_PLAT_CSR_TCAM_CTRL   0x700u
#define CTRL_PLAT_CSR_PARENT_LO   0x730u
#define CTRL_PLAT_CSR_PARENT_HI   0x734u
#define CTRL_PLAT_CSR_CRF_TX_CTRL 0x750u
#define CTRL_PLAT_CSR_CLKV_STAT   0x77cu
#define CTRL_PLAT_CSR_AS_PATH_CMD 0x7e4u
#define CTRL_PLAT_CSR_GPTP_LAT    0x7f0u
#define CTRL_PLAT_CSR_PP_CTRL     0x920u
#define CTRL_PLAT_CSR_PP_STAT     0x924u

// ID's value in every Milan datapath ('MILN'), as milan_init() checks it.
#define CTRL_PLAT_MILAN_ID 0x4d494c4eu
// PTP_CMD's snapshot strobe: TOD_RD_LO/HI then hold the time it was taken.
#define CTRL_PLAT_PTP_SNAPSHOT 0x4u
// LWSRP_CTRL[1:0], ORed onto the generated reset word: live admission enable
// and live talker admission arm (REGISTER_MAP.md 0x680), as configure_fabric()
// writes them.
#define CTRL_PLAT_LWSRP_LIVE 0x3u
// How many HI, LO, HI reads one time-of-day read may take before it gives up.
// The snapshot holds the registers still once it has landed, so a second read
// only follows a snapshot that was still landing at the first.
#define CTRL_PLAT_TOD_TRIES 3u
// The wait between the snapshot strobe and the first read, in spin turns: at
// least the 128 turns of the BIOS's cdelay(128) in milan_baremetal.c's
// gettime_ns(), each turn a load and a store of the counter.
#define CTRL_PLAT_SNAPSHOT_SPIN 128u

// The generated identity and static product policy of one shape: every word
// configure_fabric() writes, as sw/litex/boot_policy.py's fabric_constants()
// names them (ctrl_plat_gen.py writes CTRL_PLAT_POLICY_INIT from it).
struct ctrl_plat_policy {
	uint32_t entity_id_lo;      // MILAN_ENTITY_ID_LO, ADP_EID_LO
	uint32_t entity_id_hi;      // MILAN_ENTITY_ID_HI, ADP_EID_HI
	uint32_t model_id_lo;       // MILAN_MODEL_ID_LO, ADP_MID_LO
	uint32_t model_id_hi;       // MILAN_MODEL_ID_HI, ADP_MID_HI
	uint32_t station_mac_lo;    // MILAN_STATION_MAC_LO, MAC_ADDR_LO
	uint32_t station_mac_hi;    // MILAN_STATION_MAC_HI, MAC_ADDR_HI
	uint32_t mac_ctrl_set;      // MILAN_MAC_CTRL_SET, ORed into MAC_CTRL
	uint32_t tcam_ctrl;         // MILAN_TCAM_CTRL_BOOT
	uint32_t aaf_ctrl;          // MILAN_AAF_CTRL_BOOT
	uint32_t sr_vid;            // MILAN_SR_VID, LWSRP_VID
	uint32_t lwsrp_ctrl_reset;  // MILAN_LWSRP_CTRL_RESET, with CTRL_PLAT_LWSRP_LIVE
	uint32_t maap_ctrl;         // MILAN_MAAP_CTRL_BOOT
	uint32_t crf_tx_ctrl;       // MILAN_CRF_TX_CTRL_BOOT
};

// The words the console's status line prints, read as milan_baremetal.c's
// milan_status_handler() reads them: the gPTP publication first, each 64-bit
// pair low word then high word, then identity and control.
struct ctrl_plat_status {
	uint32_t gm_lo;
	uint32_t gm_hi;
	uint32_t parent_lo;
	uint32_t parent_hi;
	uint32_t pdelay_ns;
	uint32_t as_path;
	uint32_t clkv_stat;
	uint32_t gptp_lat;
	uint32_t id;
	uint32_t version;
	uint32_t ptp_ctrl;
	uint32_t adp_ctrl;
	uint32_t pp_ctrl;
	uint32_t pp_stat;
};

// ID, then VERSION into *version. True only when ID is 'MILN': a window that
// answers anything else is not a Milan datapath, and the platform writes
// nothing to it (milan_init()'s check).
bool ctrl_plat_csr_identity(uintptr_t csr, uint32_t *version);

// configure_fabric()'s fifteen writes, in its order, with p's words: the two
// compatibility enables cleared, the entity and model identity, the station
// MAC, the accept-all receive posture, then AAF, lwSRP, MAAP and the CRF
// talker's boot words.
void ctrl_plat_csr_policy(uintptr_t csr, const struct ctrl_plat_policy *p);

// The status words, in milan_status_handler()'s order.
void ctrl_plat_csr_status(uintptr_t csr, struct ctrl_plat_status *s);

// The PHC's time of day in nanoseconds: the snapshot strobe, the spin, then
// HI, LO, HI until both HI agree, at most CTRL_PLAT_TOD_TRIES times. False,
// with *ns unwritten, when they never agree.
bool ctrl_plat_csr_tod(uintptr_t csr, uint64_t *ns);

#ifdef __cplusplus
}
#endif

#endif // CTRL_PLAT_CSR_H
