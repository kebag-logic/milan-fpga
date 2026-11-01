#!/usr/bin/env python3
"""One-off: the short behaviour notes of the generated page, curated from the
design record. Each is a paragraph the concise-prose gate reads."""
import json, sys
p = sys.argv[1] + "/scripts/register_descriptions.json"
d = json.load(open(p, encoding="utf-8"))
d["page"]["intro"] = [
    "The register offsets below are a stable ABI.",
    "No register was removed. Every word still decodes, and RW words still store.",
    "**Bus:** AXI4-Lite, 32-bit data, little-endian.",
    "The LiteX product maps the 64 KiB window at `0x9000_0000`.",
    "Writes to read-only fields are ignored. Unmapped offsets read 0.",
    "`SLVERR` is never raised: every access answers OKAY.",
    "Reserved read-only bits read 0. Reserved R/W bits store what is written.",
    "Plain-RW words read from a write-through shadow RAM.",
    "After reset, `*READY` stays low for about 513 clocks. The defaults ROM loads the shadow meanwhile.",
    "64-bit reads are not atomic on the bus. For time of day, use the snapshot latch.",
    "`VERSION` tracks the map: additive changes bump minor, breaking ones major.",
    "`W1S` command strobes read back 0.",
    "The protocol processor runs the control plane, not this block.",
    "`KL_pp_shadow` wraps it; these registers are its CSR projection.",
    "The AEM descriptor tree has no CSR here. The processor fetches it from main memory.",
    "`PP_CTRL[0]` or `ADP_CTRL[0]` enables the entity.",
    "Queue 4 is the highest priority, queue 0 the lowest.",
]
notes = d["page"]["notes"]
for item in notes:
    if isinstance(item, dict) and item.get("heading", "").startswith("A group can be"):
        item["intro"] = ["A pruned block keeps its window. Its read-only words read a structural zero.",
                         "No capability bit says so. Check the build plan, not the register."]
        item["rows"] = item["rows"] + [
            {"when": {"I2SPB_P": 0}, "text": "This build sets `I2SPB_P` to 0. The `I2SPB_*` words read a structural zero."},
            {"when": {"LPF_P": 0}, "text": "This build sets `LPF_P` to 0. `LPF_CTRL` reaches no filter."}]
MOD = {
 "ident": ["The interrupt line is `|(IRQ_STATUS & IRQ_MASK)`.",
           "The ENTITY descriptor's `firmware_version` is derived from `VERSION`.",
           "`CLS_*`, the CBS window and `PTP_ILAT`/`PTP_ELAT` are inert scratch since `0x0056`."],
 "mac": ["`MAC_CTRL` resets to `0x13`: tx_en, rx_en and is_1g.",
         "`is_1g` follows `MAC_STATUS` speed unless `MAC_CTRL[5]` is set.",
         "The address filter applies only once `TCAM_CTRL[1]` is set. Decision order per frame:",
         "- A one-beat runt is always swallowed.",
         "- `promisc` accepts, outranking a TCAM drop entry.",
         "- A TCAM hit: `ACTION[0]` decides.",
         "- `addr_filter_en`: broadcast accepted, group by `allmulti` or hash, unicast on exact match.",
         "- Otherwise `TCAM_CTRL[0]` decides.",
         "The multicast bucket is a 6-bit XOR of the MAC."],
 "stats": ["Write `STATS_CTRL[0]` to latch a coherent snapshot, then read the `STATn` words.",
           "A MAC reinit release zeroes the snapshot. All zero means no valid snapshot.",
           "Read `STATS_CAP` before believing a zero. 0 there means no event source.",
           "A board build with the LiteEth MAC reports `0x1B8`."],
 "cls": ["These words are inert scratch since `0x0056`: no classifier is instantiated.",
         "They store and read back, and reach no logic."],
 "cbs": ["This window is inert scratch since `0x0056`: no shaper is elaborated.",
         "It keeps its geometry, its reset image and its readback.",
         "`CAP[8]` reads 0 for the same reason."],
 "ptp": ["`PTP_PPS_*` is a comparator in the PHC's clock domain. It fires when PHC time reaches the target.",
         "`PTP_CMD` strobes cross into the PTP domain with an apply strobe.",
         "`PTP_ILAT` and `PTP_ELAT` are inert; the gPTP plane publishes its corrections at `GPTP_LAT`."],
 "adp": ["The protocol processor sends ADP. These words are its CSR face.",
         "`ADP_CTRL[0]` and `PP_CTRL[0]` are ORed: either starts the entity.",
         "`entity_capabilities`, `valid_time`, `association_id` and `controller_capabilities` no longer reach the wire.",
         "`available_index` increments after every ENTITY_AVAILABLE sent.",
         "A frozen `ADP_STATUS` means no ADPDUs are leaving."],
 "aecp": ["The AECP and ACMP counter words are structural zeros.",
          "The entity-lock level, the AAF talker words and `ACMP_TALKER[1]` are live.",
          "Talker index 0 of the `0x800` window aliases the AAF words."],
 "lwsrp": ["The processor owns SRP; the lwSRP engine is deleted.",
           "State words are live. PDU counters are structural zeros, and provisioning words are inert.",
           "The licence needs ACTIVE and the real per-source grant (#551).",
           "`LWSRP_STATUS[8]` reads 0 until a Listener Ready or Ready Failed registers."],
 "acmpl": ["`ACMPL_STATE` no longer tracks PROBING or SETTLED: take `bound` as the truth.",
           "The bind record carries the bound stream_id, DMAC and VLAN.",
           "`CTLR_DIAG` is a structural zero: its source was deleted.",
           "The departing-controller monitor lives in the protocol processor."],
 "tcam": ["A ternary CAM accepts or drops RX frames by DMAC.",
          "Key and mask are `{HI[15:0], LO}`, compared MSB-first against the destination MAC.",
          "Set the key, mask and action words, then commit with `TCAM_CMD[16]`."],
 "link": ["`KL_link_guard` supervises link bounces; firmware has recovery strobes here.",
          "`LINK_CTRL[1]` is stored as 0 while `ETH_GUARD[0]` is 1."],
 "overlay": ["Firmware may write the board-name overlay.",
             "The fabric gPTP plane publishes live parent topology directly."],
 "crf": ["`KL_crf_rx` validates each PDU of the followed CRF stream. The profile is Milan v1.2 7.3.2.",
         "The SID pair is the manual lever. A CRF sink bind wins.",
         "A stopped sink keeps observing and counting, while consumption gates.",
         "A Controller Unbind never counts as interrupted (Table 5.6)."],
 "crft": ["`KL_crf_tx` emits the CRF AUDIO_SAMPLE stream at 500 PDU/s."],
 "bdbg": ["All three words are structural zeros. They belonged to the deleted AECP builder.",
          "`LINKG_STAT` is live: see its row."],
 "clkv": ["`tu` is the AVTP timestamp-uncertain bit on every outgoing stream frame.",
          "`CLKV_STAT[1]` and `[16]` are the live sync and asCapable levels.",
          "With the gPTP plane off, sync and asCapable stay 0. `tu` stays 1.",
          "`CLKV_TUCNT` moving means `tu` = 1 was seen in a one-second interval."],
 "rest": ["This port is dead. Writes are accepted, the ack never asserts, nothing is restored.",
          "Bindings persist through the processor's restore walk and `KL_nvm_backend`.",
          "See `PP_NVM_*` and `PP_STAT` for the live saved-state path."],
 "jnl": ["Writes here are accepted and discarded.", "`JNL_STAT` and `JNL_SEQ` read structural zeros."],
 "aemp": ["Writes here are accepted and discarded.", "`AEMP_CTRL` reads a structural zero. The layout is kept as ABI."],
 "guard": ["The guard is armed at power-on. Software disarms it with the unlock word.",
           "It drops `PHY_RESET` writes and stores `LINK_CTRL[1]` as 0.",
           "The link guard's automatic recovery is not gated.",
           "Nothing in the SoC consumes the exported level. So `milan_mac_phy_crg_reset` is not gated."],
 "asp": ["`GET_AS_PATH` returns the fabric engine's bounded pathTrace, eight identities at most.",
         "These addresses stay allocated so the map does not shift. Writes are discarded."],
 "gptpd": ["These tell link silence from traffic the plane refused (#207)."],
 "gptpl": ["This is the only live latency-correction publication (#358).",
           "One word, so a reader never pairs two builds' values."],
 "strm": ["One select word and one word block view any stream.",
          "`STRM_SEL[8]` picks the direction and `STRM_SEL[3:0]` the stream.",
          "A word that does not exist for the selection reads `0xDEADDEAD`.",
          "An index out of range reads 0. Writes are ignored.",
          "Index 0 is a hard alias of the flat registers.",
          "The shipping AX7101 has one AAF stream. The 8x8 config declares eight.",
          "The ACMP context read and SRP row port are dead. Their words read 0.",
          "A `SNAP` latches `STATE`, `CNT0..9` and `PDUS` as one coherent set.",
          "`CTRL` and `FMT` reads go live to the context RAM. They take at least four clocks."],
 "ltap": ["Two chains measure per-stage AAF latency, in axis_clk cycles.",
          "TX stages: `CAP`, `PKT_SOF`, `PKT_EOF`, `MAC_TX`. RX stages: `MAC_RX`, `ACCEPT`, `DEPKT`, `FABRIC_RENDER`.",
          "Each chain follows one tagged frame at a time.",
          "A timeout of about 0.5 ms re-arms the token."],
 "aprb": ["This probe shows what the parser saw before any match.",
          "The `SID` and `INFO` latch only follows stream subtypes."],
 "gap": ["These words are retired. They read 0 and ignore writes."],
 "slip": ["Two 48 kHz grids meet at the capture crossbar. These words count their slips.",
          "They are live and read-only. Read twice and difference for a rate.",
          "`SLIP_LB` reads 0 on a shape without the loopback lane."],
 "render": ["`STRM_SEL[3:0]` selects the listener, with `STRM_SEL[8]` at 0.",
            "Talker selections and indices out of range read 0.",
            "Refused PDUs and slips do not raise `STREAM_INTERRUPTED`."],
 "aafm": ["The meter measures the selected AAF Stream Input's media clock.",
          "`AAFM_RATE` is signed ns of error per 512 ms. 1 ppm is 512 units."],
 "mcsrv": ["The servo engages when the stored source is CRF. An AAF source also engages it.",
           "At INTERNAL it stays idle and moves nothing."],
 "chmap": ["`CHMAP_CTRL[0]` at 0 selects the fixed paths. 1 selects the programmable crossbars.",
           "`CHMAP_WORD` reads back the last committed word, not the map RAM.",
           "The render side writes by cluster key. It reads by physical key.",
           "A cluster key with no projection changes no render word."],
 "pp": ["This window is always decoded. The processor is the control plane.",
        "Read `PP_STAT[31:24]` first: 0 means the gateware predates this group.",
        "`restore_done` means the walk ended, not that state came back.",
        "A device with no record reads `nvm_blank`. Read the verdict bits with it.",
        "`PP_NVM_*` is a control tuple, never a data window."],
}
keys = {m["key"] for m in d["modules"]}
extra = set(MOD) - keys
if extra:
    raise SystemExit(f"unknown module keys {extra}; known {sorted(keys)}")
LEADS = {"stats": ["Lane sources:"], "crf": ["The Stream Input counter block:"],
         "aprb": ["Reading the failure modes, listener bound and nothing accepted:"],
         "slip": ["What each event counts:", "Reading the pair:"], "render": ["`RENDER_STAT` bits:"],
         "aafm": ["`AAFM_STAT` bits:"], "pp": ["Read the restore verdict from three bits:"],
         "acmpl": ["Words free in this group:"], "chmap": ["Words free in this group:"]}
for m in d["modules"]:
    new = MOD.get(m["key"], [])
    leads = list(LEADS.get(m["key"], []))
    kept = []
    for item in m.get("notes", []):
        if isinstance(item, dict) and item.get("table", [[""]])[0][0] == "q":
            continue  # the generator prints this table from the RTL
        if isinstance(item, dict) and "table" in item and leads:
            kept.append(leads.pop(0))
        kept.append(item)
    m["notes"] = new + kept
d.setdefault("soc_notes", [])
d["soc_notes"] = ["The bridge bank sits on the CSR window's last page.",
                  "Its counters saturate at `0xFFFF`. Read that as at least 65,535."] + d["soc_notes"]
json.dump(d, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open(p, "a", encoding="utf-8").write("\n")
print("modules without notes:", sorted(keys - set(MOD)))
