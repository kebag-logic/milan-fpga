#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
gen_aem_store.py - generate the HW AEM descriptor store from the entity model.

Single source of truth for the Milan v1.2 HW entity. Since the FR-ENUM-02
close-out this is the FULL mandatory descriptor set of
avdecc/milan-v12-entity.json: ENTITY, CONFIGURATION, AUDIO_UNIT,
STREAM_INPUT x2 (AAF + CRF), STREAM_OUTPUT, AVB_INTERFACE, CLOCK_SOURCE x3,
CLOCK_DOMAIN, CONTROL (IDENTIFY), LOCALE, STRINGS, STREAM_PORT_IN/OUT,
AUDIO_CLUSTER x16, AUDIO_MAP x2.

Documented deviation from the JSON: AUDIO_UNIT external in/out ports stay 0
(the JSON says 8 but defines no EXTERNAL_PORT descriptors — advertising them
would dangle and fail controller enumeration; the tree stays closed).

Byte layouts mirror IEEE 1722.1-2021 clause 7.2 exactly as encoded by the
reference implementation (pipewire module-avb aecp-aem-descriptors.h).

Outputs (all generated, do not edit):
  hdl/aecp/gen/aecp_aem_rom.svh   - ROM init + directory + dyn-overlay map (SV)
  tb/verilator/aecp/aem_golden.h  - golden descriptor images (C, for the TB)
  avdecc/aem_rom.json             - same content for the python controller

Run from the repo root:  python3 avdecc/gen_aem_store.py
"""
import json
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ---------------------------------------------------------------- model ----
# Descriptor type codes (IEEE 1722.1-2021 Table 7.1)
ENTITY, CONFIGURATION, AUDIO_UNIT, STREAM_INPUT, STREAM_OUTPUT = (
    0x0000, 0x0001, 0x0002, 0x0005, 0x0006)
AVB_INTERFACE, CLOCK_SOURCE, LOCALE, STRINGS = 0x0009, 0x000A, 0x000C, 0x000D
STREAM_PORT_INPUT, STREAM_PORT_OUTPUT = 0x000E, 0x000F
AUDIO_CLUSTER, AUDIO_MAP, CONTROL, CLOCK_DOMAIN = 0x0014, 0x0017, 0x001A, 0x0024

NO_STRING = 0xFFFF

# Sampling rates: pull=0 | base freq (Table 7.5 encoding)
RATES = [0x0000BB80, 0x00017700, 0x0002EE00]          # 48 k / 96 k / 192 k
# AAF PCM 32-bit 8ch stream formats (from milan-v12-entity.json, byte-exact)
FORMATS = [0x0205022002006000, 0x020702200200C000, 0x0209022002018000]
#! talker truth (2026-07-18): the framer is a STEREO 48k device (Pmod I2S2 /
#! tone path both 2ch, fs fixed by the divider chain) - STREAM_OUTPUT must
#! DECLARE exactly what the wire carries or format-matching controllers
#! strand every listener (user bugs 5/6)
OUT_FORMATS = [0x0205022000806000]
# CRF AUDIO_SAMPLE media-clock formats (milan-v12-entity.json STREAM_INPUT[1])
CRF_FORMATS = [0x041060010000BB80, 0x0410600100017700, 0x041060010002EE00]
# IDENTIFY control (pipewire aecp-aem-controls.h, byte-exact)
CTRL_TYPE_IDENTIFY = 0x90E0F00000000001
CTRL_LINEAR_UINT8 = 0x0001

def cstr(s, n=64):
    b = s.encode()[: n]
    return b + bytes(n - len(b))

def be16(v): return struct.pack(">H", v & 0xFFFF)
def be32(v): return struct.pack(">I", v & 0xFFFFFFFF)
def be64(v): return struct.pack(">Q", v & 0xFFFFFFFFFFFFFFFF)

def d_entity():
    """ENTITY descriptor (312 B). Runtime fields are zero here and overlaid
    from the ADP CSR group at read time (see OVERLAYS) so ADP and AEM can
    never disagree."""
    b = be16(ENTITY) + be16(0)
    b += be64(0)                        # entity_id          (overlay)
    b += be64(0)                        # entity_model_id    (overlay)
    b += be32(0)                        # entity_capabilities(overlay)
    b += be16(0)                        # talker_stream_sources (overlay)
    b += be16(0)                        # talker_capabilities   (overlay)
    b += be16(0)                        # listener_stream_sinks (overlay)
    b += be16(0)                        # listener_capabilities (overlay)
    b += be32(0)                        # controller_capabilities (overlay)
    b += be32(0)                        # available_index    (overlay, live)
    b += be64(0)                        # association_id     (overlay)
    b += cstr("Milan FPGA Talker")      # entity_name        (SET_NAME idx 0)
    b += be16(2) + be16(0)              # vendor->STRINGS[2], model->STRINGS[0]
    b += cstr("0.1.0")                  # firmware_version
    b += cstr("")                       # group_name         (SET_NAME idx 1)
    b += cstr("AX7101-0001")            # serial_number
    b += be16(1)                        # configurations_count
    b += be16(0)                        # current_configuration (overlay)
    return b

def d_configuration():
    # top-level counts per milan-v12-entity.json (sub-tree types — STREAM_PORT,
    # AUDIO_CLUSTER, AUDIO_MAP, STRINGS — are reached via their parents)
    counts = [(AUDIO_UNIT, 1), (STREAM_INPUT, 2), (STREAM_OUTPUT, 1),
              (AVB_INTERFACE, 1), (CLOCK_DOMAIN, 1), (CLOCK_SOURCE, 3),
              (CONTROL, 1), (LOCALE, 1)]
    b = be16(CONFIGURATION) + be16(0)
    b += cstr("Default")                # object_name (SET_NAME)
    b += be16(1)                        # localized_description -> STRINGS[1]
    b += be16(len(counts))              # descriptor_counts_count
    b += be16(74)                       # descriptor_counts_offset (fixed)
    assert len(b) == 74
    for t, c in counts:
        b += be16(t) + be16(c)
    return b

def d_audio_unit():
    b = be16(AUDIO_UNIT) + be16(0)
    b += cstr("Audio Unit")             # object_name (SET_NAME)
    b += be16(NO_STRING)
    b += be16(0)                        # clock_domain_index
    b += be16(1) + be16(0)              # stream input ports: 1 @ base 0
    b += be16(1) + be16(0)              # stream output ports: 1 @ base 0
    b += be16(0) * 28                   # ext/int ports, controls, DSP: none
                                        # (JSON says 8 ext in/out — deviation,
                                        # see header: no EXTERNAL_PORT descs)
    b += be32(RATES[0])                 # current_sampling_rate (SET_SAMPLING_RATE)
    b += be16(144)                      # sampling_rates_offset (fixed)
    b += be16(len(RATES))
    assert len(b) == 144
    for r in RATES:
        b += be32(r)
    return b

def d_stream(dtype, index, name, flags, formats, buffer_len=0):
    b = be16(dtype) + be16(index)
    b += cstr(name)                     # object_name (SET_NAME)
    b += be16(NO_STRING)
    b += be16(0)                        # clock_domain_index
    b += be16(flags)                    # stream_flags
    b += be64(formats[0])               # current_format (SET_STREAM_FORMAT)
    b += be16(132)                      # formats_offset (fixed)
    b += be16(len(formats))
    b += (be64(0) + be16(0)) * 4        # backup talkers 0..2 + backedup
    b += be16(0)                        # avb_interface_index
    b += be32(buffer_len)               # buffer_length
    assert len(b) == 132
    for f in formats:
        b += be64(f)
    return b

def d_avb_interface():
    b = be16(AVB_INTERFACE) + be16(0)
    b += cstr("AVB Interface 0")        # object_name (SET_NAME)
    b += be16(NO_STRING)
    b += bytes(6)                       # mac_address (overlay)
    b += be16(0x0007)                   # GPTP_GM_SUPPORTED|GPTP|SRP
    b += be64(0)                        # clock_identity (overlay: MAC->EUI64)
    b += bytes([0xF8, 0xF8])            # priority1, clock_class
    b += be16(0x436A)                   # offset_scaled_log_variance
    b += bytes([0x21, 0xF8, 0x00])      # clock_accuracy, priority2, domain
    b += bytes([0x00, 0x00, 0x00])      # log sync/announce/pdelay intervals
    b += be16(0)                        # port_number
    assert len(b) == 98
    return b

def d_clock_source(index, name, cs_type, loc_type, loc_index):
    b = be16(CLOCK_SOURCE) + be16(index)
    b += cstr(name)                     # object_name
    b += be16(NO_STRING)
    b += be16(0x0002)                   # clock_source_flags (STREAM_ID)
    b += be16(cs_type)                  # INTERNAL=0 / INPUT_STREAM=2
    b += be64(0)                        # clock_source_identifier
    b += be16(loc_type)                 # location: descriptor holding the source
    b += be16(loc_index)
    assert len(b) == 86
    return b

def d_clock_domain():
    sources = [0, 1, 2]
    b = be16(CLOCK_DOMAIN) + be16(0)
    b += cstr("Clock Reference Format") # object_name
    b += be16(NO_STRING)
    b += be16(0)                        # clock_source_index (SET_CLOCK_SOURCE)
    b += be16(76)                       # clock_sources_offset (fixed)
    b += be16(len(sources))
    assert len(b) == 76
    for s in sources:
        b += be16(s)
    return b

def d_control_identify():
    b = be16(CONTROL) + be16(0)
    b += cstr("Identify")               # object_name
    b += be16(NO_STRING)
    b += be32(500)                      # block_latency
    b += be32(500)                      # control_latency
    b += be16(0)                        # control_domain
    b += be16(CTRL_LINEAR_UINT8)        # control_value_type
    b += be64(CTRL_TYPE_IDENTIFY)       # control_type EUI-64
    b += be32(3)                        # reset_time (advisory; Milan: stays
                                        # in identify while current != 0)
    b += be16(104)                      # values_offset (fixed)
    b += be16(1)                        # number_of_values
    b += be16(NO_STRING) + be16(0) + be16(0)   # signal type/index/output
    assert len(b) == 104
    b += bytes([0, 255, 255, 0, 0])     # min/max/step/default/current (SET_CONTROL)
    b += be16(0)                        # unit (unitless)
    b += be16(NO_STRING)                # value string ref
    return b

def d_locale():
    b = be16(LOCALE) + be16(0)
    b += cstr("en-EN")                  # locale_identifier
    b += be16(1)                        # number_of_strings (STRINGS descriptors)
    b += be16(0)                        # base_strings
    assert len(b) == 72
    return b

def d_strings():
    strs = ["Milan FPGA Talker", "48/96/192 kHz", "Kebag Logic",
            "", "", "", ""]
    b = be16(STRINGS) + be16(0)
    for s in strs:
        b += cstr(s)
    assert len(b) == 452
    return b

def d_stream_port(dtype, flags, n_clusters, base_cluster, n_maps, base_map):
    b = be16(dtype) + be16(0)
    b += be16(0)                        # clock_domain_index
    b += be16(flags)                    # port_flags
    b += be16(0) + be16(0)              # controls
    b += be16(n_clusters) + be16(base_cluster)
    b += be16(n_maps) + be16(base_map)
    assert len(b) == 20
    return b

def d_audio_cluster(index, name, signal_type):
    b = be16(AUDIO_CLUSTER) + be16(index)
    b += cstr(name)                     # object_name
    b += be16(NO_STRING)
    b += be16(signal_type)              # 0xFFFF (input) / AUDIO_UNIT (output)
    b += be16(0) + be16(0)              # signal_index, signal_output
    b += be32(500) + be32(500)          # path/block latency
    b += be16(1)                        # channel_count
    b += bytes([0x40])                  # format MBLA (1722.1-2021 §7.2.16:
                                        # the descriptor ENDS at format u8 -
                                        # la_avdecc flagged the 3 stray bytes
                                        # of the former aes3_* tail)
    assert len(b) == 87
    return b

def d_audio_map(index):
    n = 8
    b = be16(AUDIO_MAP) + be16(index)
    b += be16(8)                        # mappings_offset (fixed, from desc start)
    b += be16(n)
    assert len(b) == 8
    for ch in range(n):                 # stream 0 ch -> cluster ch, channel 0
        b += be16(0) + be16(ch) + be16(ch) + be16(0)
    return b

# ------------------------------------------------------------- assembly ----
DESCS = [
    (ENTITY,        0, d_entity()),
    (CONFIGURATION, 0, d_configuration()),
    (AUDIO_UNIT,    0, d_audio_unit()),
    (STREAM_INPUT,  0, d_stream(STREAM_INPUT, 0, "Stream 1", 0x0003,
                                FORMATS, 2126000)),
    (STREAM_INPUT,  1, d_stream(STREAM_INPUT, 1, "CRF", 0x0003,
                                CRF_FORMATS, 2126000)),
    (STREAM_OUTPUT, 0, d_stream(STREAM_OUTPUT, 0, "Stream Output 0", 0x0002,
                                OUT_FORMATS)),
    (AVB_INTERFACE, 0, d_avb_interface()),
    (CLOCK_SOURCE,  0, d_clock_source(0, "Internal", 0x0000, CLOCK_SOURCE, 0)),
    (CLOCK_SOURCE,  1, d_clock_source(1, "Stream Clock", 0x0002, STREAM_INPUT, 0)),
    (CLOCK_SOURCE,  2, d_clock_source(2, "CRF Clock", 0x0002, STREAM_INPUT, 1)),
    (CLOCK_DOMAIN,  0, d_clock_domain()),
    (CONTROL,       0, d_control_identify()),
    (LOCALE,        0, d_locale()),
    (STRINGS,       0, d_strings()),
    (STREAM_PORT_INPUT,  0, d_stream_port(STREAM_PORT_INPUT,  0x0001, 8, 0, 1, 0)),
    (STREAM_PORT_OUTPUT, 0, d_stream_port(STREAM_PORT_OUTPUT, 0x0000, 8, 8, 1, 1)),
] + [
    (AUDIO_CLUSTER, k, d_audio_cluster(k, "Input", NO_STRING)) for k in range(8)
] + [
    (AUDIO_CLUSTER, k, d_audio_cluster(k, "Output", AUDIO_UNIT)) for k in range(8, 16)
] + [
    (AUDIO_MAP, 0, d_audio_map(0)),
    (AUDIO_MAP, 1, d_audio_map(1)),
]

rom = b""
directory = []           # (type, index, base, length)
for t, i, img in DESCS:
    directory.append((t, i, len(rom), len(img)))
    rom += img
ROM_SIZE = len(rom)

def base_of(t, i=0):
    return next(b for (tt, ii, b, _) in directory if tt == t and ii == i)

# Dynamic read overlays: (rom_addr, nbytes, source). Sources are resolved by
# KL_aecp_aem_dyn_mux from the live CSR/state wires.
E = base_of(ENTITY); A = base_of(AVB_INTERFACE)
OVERLAYS = [
    (E + 4,   8, "ENTITY_ID"),
    (E + 12,  8, "MODEL_ID"),
    (E + 20,  4, "ECAPS"),
    (E + 24,  2, "TALKER_SRC"),
    (E + 26,  2, "TALKER_CAP"),
    (E + 28,  2, "LISTEN_SINK"),
    (E + 30,  2, "LISTEN_CAP"),
    (E + 32,  4, "CTRL_CAP"),
    (E + 36,  4, "AVAIL_IDX"),
    (E + 40,  8, "ASSOC_ID"),
    (E + 310, 2, "CURRENT_CFG"),
    (A + 72,  6, "MAC"),
    (A + 80,  8, "CLOCK_ID"),
]
SRC_IDS = {name: n for n, name in enumerate(
    ["ENTITY_ID", "MODEL_ID", "ECAPS", "TALKER_SRC", "TALKER_CAP",
     "LISTEN_SINK", "LISTEN_CAP", "CTRL_CAP", "AVAIL_IDX", "ASSOC_ID",
     "CURRENT_CFG", "MAC", "CLOCK_ID"])}

# SET_* write-back targets (rom_addr of the field inside its descriptor)
WB = {
    "SAMPLING_RATE":   base_of(AUDIO_UNIT) + 136,
    "STREAM_FORMAT":   base_of(STREAM_OUTPUT) + 74,   # STREAM_OUTPUT[0] current
    "STREAM_IN0_FMT":  base_of(STREAM_INPUT, 0) + 74,
    "STREAM_IN1_FMT":  base_of(STREAM_INPUT, 1) + 74,
    "CLOCK_SRC_IDX":   base_of(CLOCK_DOMAIN) + 70,    # clock_source_index
    "CONTROL_CUR":     base_of(CONTROL) + 108,        # IDENTIFY current_value
    "AUDIO_MAP_0":     base_of(AUDIO_MAP, 0),         # GET_AUDIO_MAP source
    "AUDIO_MAP_1":     base_of(AUDIO_MAP, 1),
}

# SET/GET_NAME directory: (type, index, name_index) -> object_name rom addr.
# ENTITY carries two names (entity_name / group_name); every other named
# descriptor has object_name at base+4, name_index 0.
NAMED = [(ENTITY, 0, 0, E + 48), (ENTITY, 0, 1, E + 180)] + [
    (t, i, 0, b + 4)
    for (t, i, b, _) in directory
    if t in (CONFIGURATION, AUDIO_UNIT, STREAM_INPUT, STREAM_OUTPUT,
             AVB_INTERFACE, CLOCK_SOURCE, CLOCK_DOMAIN, CONTROL, AUDIO_CLUSTER)
]

# ------------------------------------------------------------- emitters ----
def emit_svh(path):
    lines = []
    a = lines.append
    a("// GENERATED by avdecc/gen_aem_store.py - DO NOT EDIT.")
    a("// Milan v1.2 HW entity, FULL mandatory descriptor set (FR-ENUM-02).")
    a("// See avdecc/milan-v12-entity.json.")
    a("")
    a(f"localparam int unsigned AEM_ROM_BYTES_C = {ROM_SIZE};")
    a(f"localparam int unsigned AEM_DESC_N_C    = {len(directory)};")
    a("// Scratch tail (zero-init RAM past the descriptor image): Milan MVU")
    a("// media_clock_domain_name (64 B, Milan 1.3 §5.4.4.4)")
    a("localparam int unsigned AEM_STORE_BYTES_C = AEM_ROM_BYTES_C + 64;")
    a(f"localparam [15:0] WB_MCR_DOMNAME_C = 16'd{ROM_SIZE};")
    a("")
    a("// Descriptor directory: {type[15:0], index[15:0], base[15:0], len[15:0]}")
    a(f"localparam [63:0] AEM_DIR_C [0:{len(directory)-1}] = '{{")
    for n, (t, i, b, l) in enumerate(directory):
        sep = "," if n < len(directory) - 1 else ""
        a(f"  64'h{t:04X}_{i:04X}_{b:04X}_{l:04X}{sep}")
    a("};")
    a("")
    a("// ROM image (network byte order, addr 0 = first byte of ENTITY)")
    a(f"localparam [7:0] AEM_ROM_INIT_C [0:{ROM_SIZE-1}] = '{{")
    row = []
    for n, byte in enumerate(rom):
        row.append(f"8'h{byte:02X}")
        if len(row) == 16:
            sep = "," if n < ROM_SIZE - 1 else ""
            a("  " + ",".join(row) + sep)
            row = []
    if row:
        a("  " + ",".join(row))
    a("};")
    a("")
    a("// Dynamic read-overlay sources")
    for name, n in SRC_IDS.items():
        a(f"localparam [3:0] OVL_{name}_C = 4'd{n};")
    a("")
    a("// overlay lookup: rom addr -> {hit, source[3:0], byte_of_source[2:0]}")
    a("// byte_of_source 0 = MOST significant byte of the source value.")
    a("function automatic [7:0] aem_ovl_lookup(input [15:0] addr);")
    a("  begin")
    a("    aem_ovl_lookup = 8'h00;  // hit=0")
    for base, nb, src in OVERLAYS:
        a(f"    if (addr >= 16'd{base} && addr < 16'd{base + nb})")
        a(f"      aem_ovl_lookup = {{1'b1, OVL_{src}_C, 3'(addr - 16'd{base})}};")
    a("  end")
    a("endfunction")
    a("")
    a("// SET_* write-back base addresses")
    for k, v in WB.items():
        a(f"localparam [15:0] WB_{k}_C = 16'd{v};")
    a("")
    a("// SET/GET_NAME lookup: (type, index, name_index) -> {valid, rom addr}")
    a("function automatic [16:0] aem_name_lookup(input [15:0] t,")
    a("                                          input [15:0] idx,")
    a("                                          input [15:0] nidx);")
    a("  begin")
    a("    aem_name_lookup = 17'd0;")
    for t, i, nidx, addr in NAMED:
        a(f"    if (t == 16'h{t:04X} && idx == 16'd{i} && nidx == 16'd{nidx})")
        a(f"      aem_name_lookup = {{1'b1, 16'd{addr}}};")
    a("  end")
    a("endfunction")
    a("")
    a("// Value validation tables")
    a(f"localparam [31:0] AEM_RATES_C [0:{len(RATES)-1}] = "
      "'{" + ", ".join(f"32'h{r:08X}" for r in RATES) + "};")
    a(f"localparam [63:0] AEM_FMTS_C  [0:{len(FORMATS)-1}] = "
      "'{" + ", ".join(f"64'h{f:016X}" for f in FORMATS) + "};")
    a(f"localparam [63:0] AEM_CRF_FMTS_C [0:{len(CRF_FORMATS)-1}] = "
      "'{" + ", ".join(f"64'h{f:016X}" for f in CRF_FORMATS) + "};")
    a("")
    with open(path, "w") as f:
        f.write("\n".join(lines))

def emit_c_golden(path):
    with open(path, "w") as f:
        f.write("// GENERATED by avdecc/gen_aem_store.py - DO NOT EDIT.\n")
        f.write("#pragma once\n#include <cstdint>\n\n")
        f.write(f"static const unsigned AEM_ROM_BYTES = {ROM_SIZE};\n")
        f.write("static const uint8_t AEM_ROM[] = {\n")
        for n in range(0, ROM_SIZE, 16):
            f.write("  " + ",".join(f"0x{b:02X}" for b in rom[n:n+16]) + ",\n")
        f.write("};\n\n")
        f.write("struct AemDirEnt { uint16_t type, index, base, len; };\n")
        f.write("static const AemDirEnt AEM_DIR[] = {\n")
        for t, i, b, l in directory:
            f.write(f"  {{0x{t:04X}, {i}, {b}, {l}}},\n")
        f.write("};\n")

def emit_json(path):
    with open(path, "w") as f:
        json.dump({
            "rom_hex": rom.hex(),
            "directory": [
                {"type": t, "index": i, "base": b, "len": l}
                for (t, i, b, l) in directory],
            "overlays": [
                {"addr": a_, "bytes": n, "source": s} for (a_, n, s) in OVERLAYS],
            "writeback": WB,
            "named": [
                {"type": t, "index": i, "name_index": n, "addr": a_}
                for (t, i, n, a_) in NAMED],
            "rates": RATES,
            "formats": FORMATS,
            "crf_formats": CRF_FORMATS,
        }, f, indent=1)

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "hdl/aecp/gen"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "tb/verilator/aecp"), exist_ok=True)
    emit_svh(os.path.join(ROOT, "hdl/aecp/gen/aecp_aem_rom.svh"))
    emit_c_golden(os.path.join(ROOT, "tb/verilator/aecp/aem_golden.h"))
    emit_json(os.path.join(HERE, "aem_rom.json"))
    print(f"[gen_aem_store] {len(directory)} descriptors, ROM {ROM_SIZE} B")
    for t, i, b, l in directory:
        print(f"  type 0x{t:04X} idx {i}: base {b:4d} len {l}")
