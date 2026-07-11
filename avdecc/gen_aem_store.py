#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
gen_aem_store.py - generate the HW AEM descriptor store from the entity model.

Single source of truth for the Milan v1.2 HW entity (the "one config, one AVB
interface, one audio unit, one stream output" scope). It is a TRIMMED derivative
of avdecc/milan-v12-entity.json (the full software model): descriptors NOT in
scope are dropped and the ENTITY counts/caps are adjusted to keep the tree
closed (no dangling STREAM_PORT/CLUSTER/CONTROL references).

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
ENTITY, CONFIGURATION, AUDIO_UNIT, STREAM_OUTPUT, AVB_INTERFACE = (
    0x0000, 0x0001, 0x0002, 0x0006, 0x0009)

NO_STRING = 0xFFFF

# Sampling rates: pull=0 | base freq (Table 7.5 encoding)
RATES = [0x0000BB80, 0x00017700, 0x0002EE00]          # 48 k / 96 k / 192 k
# AAF PCM 32-bit 8ch stream formats (from milan-v12-entity.json, byte-exact)
FORMATS = [0x0205022002006000, 0x020702200200C000, 0x0209022002018000]

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
    b += be16(NO_STRING) + be16(NO_STRING)  # vendor/model name string refs
    b += cstr("0.1.0")                  # firmware_version
    b += cstr("")                       # group_name         (SET_NAME idx 1)
    b += cstr("AX7101-0001")            # serial_number
    b += be16(1)                        # configurations_count
    b += be16(0)                        # current_configuration (overlay)
    return b

def d_configuration():
    counts = [(AUDIO_UNIT, 1), (STREAM_OUTPUT, 1), (AVB_INTERFACE, 1)]
    b = be16(CONFIGURATION) + be16(0)
    b += cstr("Default")                # object_name (SET_NAME)
    b += be16(NO_STRING)
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
    b += be16(0) * 32                   # all 16 number_of/base pairs = 0
    b += be32(RATES[0])                 # current_sampling_rate (SET_SAMPLING_RATE)
    b += be16(144)                      # sampling_rates_offset (fixed)
    b += be16(len(RATES))
    assert len(b) == 144
    for r in RATES:
        b += be32(r)
    return b

def d_stream_output():
    b = be16(STREAM_OUTPUT) + be16(0)
    b += cstr("Stream Output 0")        # object_name (SET_NAME)
    b += be16(NO_STRING)
    b += be16(0)                        # clock_domain_index
    b += be16(0x0002)                   # stream_flags: CLASS_A
    b += be64(FORMATS[0])               # current_format (SET_STREAM_FORMAT)
    b += be16(132)                      # formats_offset (fixed)
    b += be16(len(FORMATS))
    b += (be64(0) + be16(0)) * 4        # backup talkers 0..2 + backedup
    b += be16(0)                        # avb_interface_index
    b += be32(0)                        # buffer_length
    assert len(b) == 132
    for f in FORMATS:
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

# ------------------------------------------------------------- assembly ----
DESCS = [
    (ENTITY,        0, d_entity()),
    (CONFIGURATION, 0, d_configuration()),
    (AUDIO_UNIT,    0, d_audio_unit()),
    (STREAM_OUTPUT, 0, d_stream_output()),
    (AVB_INTERFACE, 0, d_avb_interface()),
]

rom = b""
directory = []           # (type, index, base, length)
for t, i, img in DESCS:
    directory.append((t, i, len(rom), len(img)))
    rom += img
ROM_SIZE = len(rom)

def base_of(t):
    return next(b for (tt, _, b, _) in directory if tt == t)

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
    "NAME_ENTITY_0":  E + 48,                       # entity_name
    "NAME_ENTITY_1":  E + 180,                      # group_name
    "NAME_CONFIG":    base_of(CONFIGURATION) + 4,
    "NAME_AUDIO":     base_of(AUDIO_UNIT) + 4,
    "NAME_STREAM":    base_of(STREAM_OUTPUT) + 4,
    "NAME_AVBIF":     base_of(AVB_INTERFACE) + 4,
    "SAMPLING_RATE":  base_of(AUDIO_UNIT) + 136,
    "STREAM_FORMAT":  base_of(STREAM_OUTPUT) + 74,
}

# ------------------------------------------------------------- emitters ----
def emit_svh(path):
    lines = []
    a = lines.append
    a("// GENERATED by avdecc/gen_aem_store.py - DO NOT EDIT.")
    a("// Trimmed Milan v1.2 HW entity: ENTITY, CONFIGURATION, AVB_INTERFACE,")
    a("// AUDIO_UNIT, STREAM_OUTPUT (one each). See avdecc/milan-v12-entity.json.")
    a("")
    a(f"localparam int unsigned AEM_ROM_BYTES_C = {ROM_SIZE};")
    a(f"localparam int unsigned AEM_DESC_N_C    = {len(directory)};")
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
    a("// Value validation tables")
    a(f"localparam [31:0] AEM_RATES_C [0:{len(RATES)-1}] = "
      "'{" + ", ".join(f"32'h{r:08X}" for r in RATES) + "};")
    a(f"localparam [63:0] AEM_FMTS_C  [0:{len(FORMATS)-1}] = "
      "'{" + ", ".join(f"64'h{f:016X}" for f in FORMATS) + "};")
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
            "rates": RATES,
            "formats": FORMATS,
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
