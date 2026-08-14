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

The ENTITY descriptor's firmware_version (7.2.1 Table 7-2, offset 116, 64
octets) is DERIVED from the gateware's own VERSION parameter, not declared -
see firmware_version_string() for why that is not a style preference.

Since the endstation-builder round (gaps item 4) the model can also be built
from a builder-emitted AEM overlay (sw/builder/endstation_builder.py):
  python3 avdecc/gen_aem_store.py --overlay <aem_overlay.json> [--out-dir D]

NO RTL CONSUMES THIS MODEL ANY MORE (2026-08-12).  The whole IEEE 1722.1
control plane that used to serve it — hdl/ieee17221/aecp/** — is DELETED and
the protocol-processor submodule is the control plane now.  This gateware
answers NO AECP/AEM command, so the descriptor set below is a DECLARATIVE
MODEL, not something a controller can read back off this device:

  * the two file targets that made it RTL are gone with the plane.  The
    default run no longer writes hdl/ieee17221/aecp/gen/aecp_aem_rom.svh
    (the directory does not exist) and no longer writes
    tb/verilator/aecp/aem_golden.h (that whole suite is deleted).  A code
    path whose only destination is a deleted directory is worse than no
    path: it fails at runtime, or worse, resurrects the directory.
  * what the model IS still good for: it is the single declarative entity
    definition the ADP shape counts (talker_stream_sources /
    listener_stream_sinks) and the ADP capability words are DERIVED from,
    and the builder's own self-consistency gates read it.  Those counts DO
    reach the gateware, through hdl/common/csr/gen/adp_shape_defaults.svh.

Outputs (all generated, do not edit):
  avdecc/aem_rom.json             - the model for the python controller and
                                    avdecc/pack_aem_bin.py (aem_rom.bin for a
                                    SOFTWARE responder).  The default target.
  <out-dir>/aecp_aem_rom.svh      - only under --out-dir, only for a caller
  <out-dir>/aem_rom.json            that wants the text in a scratch
                                    directory (the builder gates do).  This
                                    is NOT installed into any RTL tree.

THE AUDIO_MAP BOUNDS GATE (2026-07-28, defect B).  build_model() now REFUSES a
model whose AUDIO_MAPs leave the bounds of the ports that own them, and emits
the per-port serving tables (AEM_SMAP_*) the RTL needs to answer GET_AUDIO_MAP
from the ADDRESSED PORT's own base_map instead of a hardcoded descriptor index.
The two are one change: the tables cannot be built without checking that each
port's base_map names a descriptor that exists and holds what it claims, and
without the tables the RTL had nothing to select by but a constant.
See static_map_tables() for the clause behind each bound.

  python3 avdecc/gen_aem_store.py --self-test   # prove the gate bites

Run from the repo root:  python3 avdecc/gen_aem_store.py
"""
import argparse
import json
import os
import re
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# --------------------------------------------------------- firmware version --
#: The gateware's version lives in exactly ONE place: the `VERSION` parameter
#: behind the read-only 0x004 register in hdl/common/csr/milan_csr.sv, whose
#: `//!` comment IS the gateware changelog (docs/reference/REGISTER_MAP.md
#: 0x004).  The ENTITY descriptor's firmware_version field is what every
#: controller on the segment reads that version AS - it is the first string
#: Hive shows next to the entity - so it must be DERIVED from the parameter,
#: never declared beside it.
#:
#: Until 2026-07-28 nothing connected the two: all three configs/endstation_*
#: .yaml hardcoded `firmware_version: "0.1.0"` and this generator stamped that
#: string into the descriptor, so every board we ship told every controller it
#: ran firmware 0.1.0 while the fabric was at 0x0001_0016.  Same class of
#: defect as the ADP shape registers (docs/findings/ADP_SHAPE_STATIC_0727.md):
#: a hand-typed declaration that no gate could compare against the fabric.
MILAN_CSR_SV = os.path.join(ROOT, "hdl/common/csr/milan_csr.sv")

_VERSION_RE = re.compile(
    r"parameter\s+logic\s*\[31:0\]\s+VERSION\s*=\s*32'h([0-9A-Fa-f_]+)")


def rtl_version(path=None):
    """`(major, minor)` as milan_csr.sv's VERSION parameter defines them.

    The field split is the register map's, not this function's:
    docs/reference/REGISTER_MAP.md 0x004 documents `[31:16] major, [15:0]
    minor`.  The minor is a FLAT incrementing ABI number - the register map's
    changelog is keyed on it one entry at a time ("0x0016 = ...", "0x0015 =
    ...") and software feature-gates on it with `>=` - so it is one integer,
    not a packed pair of sub-fields, and rendering it as one decimal integer
    is a re-encoding of the documented field rather than a reinterpretation
    of it.  32'h0001_0016 -> (1, 22).
    """
    src = path or MILAN_CSR_SV
    m = _VERSION_RE.search(open(src).read())
    if not m:
        raise ValueError(
            f"{src}: no `parameter logic [31:0] VERSION = 32'h...` - the "
            "gateware version has no single source of truth any more")
    v = int(m.group(1).replace("_", ""), 16)
    return (v >> 16) & 0xFFFF, v & 0xFFFF


def firmware_version_string(rev=0, path=None):
    """The ENTITY descriptor's firmware_version value: `major.minor.rev`.

    IEEE 1722.1-2021 7.2.1 Table 7-2 offset 116: "64-octet UTF-8 string
    containing the firmware version of the ATDECC Entity" - the standard
    fixes the size and the encoding and says nothing about the syntax, and
    the Milan end-station validation test plan v1.9 (test macro 3) reads the
    field into the enumeration model without constraining its value.  So the
    syntax is ours to choose and the only real requirement is the one the
    standard cannot state: it has to be TRUE.

    major and minor come from the fabric.  `rev` is the one component the
    32-bit register does not carry - a firmware respin that changes no CSR
    ABI - and comes from the optional `entity.firmware_rev` config key,
    default 0.  32'h0002_0043 -> "2.67.0".

    Versioning policy (USER 2026-08-11): MAJOR = entire redesign of blocks
    (0x0002 = the scenario-B era); MINOR = compliance fixes, flat and
    continuous across majors; REV = the patch component, bug-fix respins.
    """
    major, minor = rtl_version(path)
    return f"{major}.{minor}.{int(rev)}"


# ---------------------------------------------------------------- model ----
# Descriptor type codes (IEEE 1722.1-2021 Table 7.1)
ENTITY, CONFIGURATION, AUDIO_UNIT, STREAM_INPUT, STREAM_OUTPUT = (
    0x0000, 0x0001, 0x0002, 0x0005, 0x0006)
AVB_INTERFACE, CLOCK_SOURCE, LOCALE, STRINGS = 0x0009, 0x000A, 0x000C, 0x000D
STREAM_PORT_INPUT, STREAM_PORT_OUTPUT = 0x000E, 0x000F
AUDIO_CLUSTER, AUDIO_MAP, CONTROL, CLOCK_DOMAIN = 0x0014, 0x0017, 0x001A, 0x0024

NO_STRING = 0xFFFF

# Sampling rates: pull=0 | base freq (Table 7.5 encoding; pull 0 => the
# encoded 32-bit value IS the base frequency in Hz)
RATES = [0x0000BB80, 0x00017700, 0x0002EE00]          # 48 k / 96 k / 192 k
# AAF PCM 32-bit 8ch stream formats (from milan-v12-entity.json, byte-exact)
#! 8ch default restored (2026-07-20, internal COMPLIANCE es-4.4 expects the classic
#! 0205022002006000 default): the monitor now ADAPTS to any wire channel
#! count 1..8 under the declared format, so a pure-ACMP 2ch connect works
#! against the 8ch default. 2ch stays in the supported list.
#! Milan v1.2 6.4, third paragraph (2026-07-21, USER-caught): a Stream
#! Input advertising a 48 kHz Base format SHALL "advertise support for all
#! the other 48kHz ... Base formats in this Stream Input", and 6.2 fixes
#! what "all" is - "number of channels = N, where N is an element from
#! {1, 2, 4, 6, 8}". Entry 1 is the ut-bit (qword bit 52, IEEE 1722-2016
#! Annex I.2.4) "up to 8" string, which covers that whole family in ONE
#! entry: 6.5 says "it should use the ut bit ... to describe all the
#! related formats using a single ATDECC format string" and 5.3.3.4 says a
#! controller must read it that way. 96k/192k entries DROPPED: the render
#! path is 48k-only and each advertised rate drags its own full-family
#! obligation (talker-truth honesty, listener edition).
#! The config-driven path does not restate any of this - the completion is
#! derived in endstation_builder.base_format_complete() and arrives here
#! through the overlay; these constants are the builtin model's own.
#! order matters: FORMATS[0] is the RESET default of the dynamic store.
#! 2ch-first (kernel-shield lesson 2026-07-19, re-learned 2026-07-21: an
#! 8ch default + reboot + pure-ACMP bind starved the render at 1/4 rate);
#! the ut entry keeps the full Milan 6.4 1..8ch family coverage.
FORMATS = [0x0205022000806000, 0x0215022002006000]
#! talker truth (2026-07-18): the framer is a STEREO 48k device (Pmod I2S2 /
#! tone path both 2ch, fs fixed by the divider chain) - STREAM_OUTPUT must
#! DECLARE exactly what the wire carries or format-matching controllers
#! strand every listener (user bugs 5/6)
OUT_FORMATS = [0x0205022000806000]
# CRF AUDIO_SAMPLE media-clock formats (milan-v12-entity.json STREAM_INPUT[1])
#! 48k only (the CRF engine validates base 48000/pull 0 - advertising
#! unlockable rates is the same honesty violation)
CRF_FORMATS = [0x041060010000BB80]
# IDENTIFY control (pipewire aecp-aem-controls.h, byte-exact)
CTRL_TYPE_IDENTIFY = 0x90E0F00000000001
CTRL_LINEAR_UINT8 = 0x0001

def cstr(s, n=64):
    b = s.encode()[: n]
    return b + bytes(n - len(b))

def be16(v): return struct.pack(">H", v & 0xFFFF)
def be32(v): return struct.pack(">I", v & 0xFFFFFFFF)
def be64(v): return struct.pack(">Q", v & 0xFFFFFFFFFFFFFFFF)

def d_entity(e):
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
    b += cstr(e["name"])                # entity_name        (SET_NAME idx 0)
    b += be16(2) + be16(0)              # vendor->STRINGS[2], model->STRINGS[0]
    b += cstr(e["firmware_version"])    # firmware_version
    b += cstr(e["group_name"])          # group_name         (SET_NAME idx 1)
    b += cstr(e["serial_number"])       # serial_number
    b += be16(1)                        # configurations_count
    b += be16(0)                        # current_configuration (overlay)
    return b

def d_configuration(n_inputs, n_outputs, n_clk_sources):
    # top-level counts per milan-v12-entity.json (sub-tree types — STREAM_PORT,
    # AUDIO_CLUSTER, AUDIO_MAP, STRINGS — are reached via their parents)
    counts = [(AUDIO_UNIT, 1), (STREAM_INPUT, n_inputs),
              (STREAM_OUTPUT, n_outputs),
              (AVB_INTERFACE, 1), (CLOCK_DOMAIN, 1),
              (CLOCK_SOURCE, n_clk_sources),
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

def d_audio_unit(rates, current_rate, n_in_ports, n_out_ports):
    b = be16(AUDIO_UNIT) + be16(0)
    b += cstr("Audio Unit")             # object_name (SET_NAME)
    b += be16(NO_STRING)
    b += be16(0)                        # clock_domain_index
    b += be16(n_in_ports) + be16(0)     # stream input ports @ base 0
    b += be16(n_out_ports) + be16(0)    # stream output ports @ base 0
    b += be16(0) * 28                   # ext/int ports, controls, DSP: none
                                        # (JSON says 8 ext in/out — deviation,
                                        # see header: no EXTERNAL_PORT descs)
    b += be32(current_rate)             # current_sampling_rate (SET_SAMPLING_RATE)
    b += be16(144)                      # sampling_rates_offset (fixed)
    b += be16(len(rates))
    assert len(b) == 144
    for r in rates:
        b += be32(r)
    return b

def d_stream(dtype, index, name, flags, formats, buffer_len=0):
    b = be16(dtype) + be16(index)
    b += cstr(name)                     # object_name (SET_NAME)
    b += be16(NO_STRING)
    b += be16(0)                        # clock_domain_index
    b += be16(flags)                    # stream_flags
    b += be64(formats[0])               # current_format (SET_STREAM_FORMAT)
    #! CONSTRAINT (1722.1-2021 7.2.6 Table 7-8): formats_offset is 138 and the
    #! descriptor is 138 + 8*N + 2*R octets.  1722.1-2013 ended this descriptor
    #! at buffer_length (formats at 132); 2021 appends redundant_offset (132),
    #! number_of_redundant_streams (134) and timing (136) BEFORE the formats
    #! array, and Milan v1.2 5.3.3.4 binds these descriptors to "[ATDECC,
    #! Clause 7.2.6]" with [ATDECC] = IEEE Std 1722.1-2021 (Milan v1.2 clause
    #! 2, References).  Emitting the 2013 layout hands a 2021 controller the
    #! first two octets of formats[0] as `timing`.
    #! Milan v1.2 Annex C Table C.1 shows a THIRD layout (formats at 136, no
    #! timing field) - it is the pre-2021 Avnu redundancy extension, is
    #! optional here ("A PAAD-AE MAY use the extension ... and SHALL use it
    #! for the Streams that are part of the redundant pair", 5.3.3.4), and
    #! this entity declares no redundant pair, so 7.2.6 governs unmodified.
    b += be16(138)                      # formats_offset (fixed)
    b += be16(len(formats))
    b += (be64(0) + be16(0)) * 4        # backup talkers 0..2 + backedup
    b += be16(0)                        # avb_interface_index
    b += be32(buffer_len)               # buffer_length
    #! R = 0: no redundant association is declared, so redundant_offset points
    #! at the empty array just past the formats (Table 7-8: "138 + 8*N").
    b += be16(138 + 8 * len(formats))   # redundant_offset
    b += be16(0)                        # number_of_redundant_streams (R)
    #! timing = 0 is only readable because TIMING_FIELD_VALID (Table 7-9 bit 2,
    #! mask 0x2000 - the table numbers bits MSB-first) is CLEAR in every
    #! stream_flags word this model emits: there is no TIMING descriptor in
    #! this entity, so there is no index to name.
    assert not (flags & 0x2000), (
        f"stream_flags 0x{flags:04X} sets TIMING_FIELD_VALID (7.2.6.1) but "
        "this model defines no TIMING descriptor for `timing` to reference")
    b += be16(0)                        # timing
    assert len(b) == 138
    for f in formats:
        b += be64(f)
    return b

def d_avb_interface(gp=None):
    """gp = the config's `gptp:` section (overlay key "gptp"), the SAME
    source that generates the board's ptp4l config - so the descriptor can
    no longer claim one clock while the daemon runs another. Absent (legacy
    overlays / builtin spec) keeps the historical constants BYTE-EXACTLY:
    those shapes' entity_model_id predates the section, and controllers
    cache descriptor content by model id, so their bytes must not move."""
    gp = gp or {}
    b = be16(AVB_INTERFACE) + be16(0)
    b += cstr("AVB Interface 0")        # object_name (SET_NAME)
    b += be16(NO_STRING)
    b += bytes(6)                       # mac_address (overlay)
    b += be16(0x0007)                   # GPTP_GM_SUPPORTED|GPTP|SRP
    b += be64(0)                        # clock_identity (overlay: MAC->EUI64)
    b += bytes([int(gp.get("priority1", 0xF8)),
                int(gp.get("clock_class", 0xF8))])
    b += be16(int(gp.get("offset_scaled_log_variance", 0x436A)))
    b += bytes([int(gp.get("clock_accuracy", 0x21)),
                int(gp.get("priority2", 0xF8)),
                int(gp.get("domain", 0))])
    # log intervals are SIGNED octets (1722.1 7.2.8: log base 2 periods)
    b += bytes([int(gp.get("log_sync_interval", 0)) & 0xFF,
                int(gp.get("log_announce_interval", 0)) & 0xFF,
                int(gp.get("log_pdelay_interval", 0)) & 0xFF])
    b += be16(0)                        # port_number
    #! CONSTRAINT (1722.1-2021 §7.2.8 Table 7-13): the descriptor is 102
    #! octets and ends at base_control (offset 100).  1722.1-**2013** ended it
    #! at port_number, and this generator asserted 98 - the 2013 length - until
    #! 2026-08-13.  2021 appends number_of_controls (98) and base_control (100),
    #! and Milan v1.2 5.3.3.5 binds this descriptor to "[ATDECC, Clause 7.2.8]"
    #! with [ATDECC] = IEEE Std 1722.1-2021 (Milan v1.2 clause 2, References),
    #! so 98 was a compliance defect and not a choice.  A 2021 controller
    #! reading a 98-octet AVB_INTERFACE takes its number_of_controls from
    #! whatever the store holds past the descriptor's end.
    #!
    #! number_of_controls = 0 / base_control = 0: THE INTERFACE OWNS NO
    #! CONTROL, and that is a claim about THIS entity, not a placeholder.  The
    #! model defines exactly one CONTROL descriptor - the IDENTIFY at index 0
    #! (d_control_identify) - and it is the CONFIGURATION's child, not this
    #! interface's:
    #!   * Milan v1.2 5.3.2 lists "IDENTIFY" CONTROL (0..*) as a direct child
    #!     of CONFIGURATION, a sibling of AVB_INTERFACE, and then forbids the
    #!     other reading outright: "A descriptor from one subtree shall not be
    #!     contained in another subtree.  In other words, each of the
    #!     descriptors above ... shall have one, and only one, parent
    #!     descriptor."  Milan v1.2 Annex C's worked model draws the same edge
    #!     (CONTROL.0 / IDENTIFY hanging off CONFIGURATION.0).
    #!   * d_configuration already claims it: CONTROL is one of the top-level
    #!     types 1722.1-2021 7.2.2 enumerates for descriptor_counts, and the
    #!     counts list carries (CONTROL, 1).  Declaring number_of_controls = 1
    #!     here would give that one descriptor two parents - a defect of its
    #!     own, and one no controller could resolve, since base_control would
    #!     name index 0 in the same index space the configuration counts.
    #!   * 7.2.22 agrees from the CONTROL's own side: "If a control does not
    #!     act on a signal, for example an IDENTIFY control, then the
    #!     signal_type and signal_index is set to INVALID and zero" - which is
    #!     what d_control_identify writes.  The IDENTIFY acts on the PAAD, not
    #!     on this interface's signal.
    #! base_control = 0 with a zero count is this file's standing convention
    #! for an empty base index (d_audio_unit's controls, d_stream_port's), and
    #! 7.2.3's base-index rule only defines it "with consecutively increasing
    #! indicies" for descriptors the parent actually has - with none, it names
    #! nothing and the count is what a controller reads first.
    #!
    #! WHAT THIS COSTS, said rather than buried: the four new octets move
    #! EVERY shape's AVB_INTERFACE bytes, including the pre-gptp-section shapes
    #! whose bytes the docstring above pins.  That warning is about the gPTP
    #! FIELD VALUES and it still holds; the length is a separate obligation and
    #! it wins, because 1722.1-2021 6.2.2.8 makes this a model-structure change
    #! ("The structure of an ATDECC Entity model is considered changed if any
    #! descriptor fields in the ATDECC Entity are different excluding the
    #! following fields" - no field added here is on that list) and therefore
    #! "shall use a new unique entity_model_id".  The id is hashed from the
    #! CONFIG shape (endstation_builder.model_shape), never from these bytes,
    #! so nothing rotates it automatically: the shapes carrying a hash-derived
    #! id and endstation_arty_current's pinned 0x001BC50AC1000001 need the
    #! rotation done at the config tier.  Shipping the 2013 length to keep a
    #! stale id would be trading a cache miss for a wire defect.
    b += be16(0)                        # number_of_controls (7.2.8: "within
                                        # this interface" - see above: none)
    b += be16(0)                        # base_control (no controls to index)
    assert len(b) == 102
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

def d_clock_domain(n_sources):
    sources = list(range(n_sources))
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

def d_strings(strs):
    assert len(strs) == 7
    b = be16(STRINGS) + be16(0)
    for s in strs:
        b += cstr(s)
    assert len(b) == 452
    return b

def d_stream_port(dtype, index, flags, n_clusters, base_cluster, n_maps, base_map):
    b = be16(dtype) + be16(index)
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
    b += bytes([0x40])                  # format MBLA, offset 86 (Table 7-28)
    # 1722.1-2021 Table 7-27 CONTINUES past format. The comment that used to
    # sit here said "the descriptor ENDS at format u8" and cited 2021 for it,
    # which is backwards: 2013 Table 7.27 ends at format for 87 octets and
    # 2021 ADDS aes3_data_type_reference (offset 87, length 1) and
    # aes3_data_type (offset 88, length 2) for 90. What la_avdecc "flagged"
    # was a TRACE-level "Remaining bytes in buffer" line - its own constant is
    # the 2013 one (AecpAemReadAudioClusterDescriptorResponsePayloadSize =
    # common + 83) and its length test is a MINIMUM (`<`), so the surplus was
    # never an error. Truncating to 87 to silence a trace message put the
    # device on the superseded layout, which Milan v1.2 §5.3.3.4 does not
    # allow, and then the comment made that look deliberate.
    #
    # Both fields are zero here and that is their specified value: Table 7-27
    # defines them "when format is IEC_60958", and this cluster's format is
    # MBLA.
    b += bytes([0x00])                  # aes3_data_type_reference @87
    b += be16(0)                        # aes3_data_type @88
    assert len(b) == 90
    return b

def d_audio_map(index, rows):
    b = be16(AUDIO_MAP) + be16(index)
    b += be16(8)                        # mappings_offset (fixed, from desc start)
    b += be16(len(rows))
    assert len(b) == 8
    for (stream, ch, cluster_off, cluster_ch) in rows:
        # cluster_offset RELATIVE to the owning port's base_cluster
        # (1722.1-2021 7.2.19)
        b += be16(stream) + be16(ch) + be16(cluster_off) + be16(cluster_ch)
    return b


def fmt_channels(fmt):
    """stream_format -> channels_per_frame, or None when the format carries no
    audio channels. IEEE 1722-2016 7.3.1: the AAF subtype is the top octet
    (0x02 = AAF) and channels_per_frame is bits 31:22 of the 64-bit word - the
    same field KL_aecp_response_builder validates a SET_STREAM_FORMAT on. CRF
    (0x04) carries a clock, not channels: there is no channel bound to check."""
    if (fmt >> 56) != 0x02:
        return None
    return (fmt >> 22) & 0x3FF


#! Milan v1.2 6.2 + Table 6.1: "number of channels = N, where N is an element
#! from {1, 2, 4, 6, 8}". These five, at one sampling rate, are what 6.4 means
#! by "all the other 48kHz ... Base formats".
MILAN_BASE_CHANNELS = (1, 2, 4, 6, 8)


def base_channel_cover(fmts, rate_fmt=0x0205022000006000):
    """The 48 kHz Milan Base channel counts an advertised formats list covers.

    IEEE 1722-2016 Annex I.2.4: "The ut field is used to determine if the AAF
    stream source or sink is capable of sourcing or sinking a stream with less
    than the number of channels indicated by the channels_per_frame field.
    When set to one (1) the stream source or sink is capable of using fewer
    channels than specified." So ONE ut entry advertises every Base count up
    to its own - which is what Milan 6.5 recommends ("it should use the ut bit
    ... to describe all the related formats using a single ATDECC format
    string") and 5.3.3.4 confirms a controller must read ("a single entry in
    the formats list can describe a range of formats when using the "up to"
    bit"). `rate_fmt` is the 48 kHz AAF PCM32 stem with channels zeroed."""
    got = set()
    for f in fmts:
        n = int(str(f), 16) if isinstance(f, str) else int(f)
        ut, ch = (n >> 52) & 1, (n >> 22) & 0x3FF
        if n & ~((1 << 52) | (0x3FF << 22)) != rate_fmt:
            continue
        got |= {c for c in MILAN_BASE_CHANNELS if c <= ch} if ut \
            else {ch} & set(MILAN_BASE_CHANNELS)
    return got


#! The RTL's port-index mux width (KL_aecp_response_builder w_smap_pi is 5 b)
SMAP_MAX_PORTS = 32
#! IEEE Std 1722.1-2021 Table 7-32, AUDIO_MAP descriptor, number_of_mappings:
#!   "The number of channel mappings within the descriptor. The value of this
#!    field is referred to as N. The maximum value of this field is 62 for this
#!    version of AEM."
#! This bounds the DESCRIPTOR, which is what this function builds. Do not
#! confuse it with Milan v1.2 5.4.2.26's 176, which bounds the number of
#! DYNAMIC mappings a GET_AUDIO_MAP RESPONSE may carry for one map_index -
#! a different object, on ports that have no Audio Map descriptor at all.
#! (An earlier version of this constant was derived from the MTU and came out
#! at 181, which would have accepted a descriptor the standard forbids.)
SMAP_MAX_ROWS = 62


#: The stream_channel deviations the deployed model carries today, recorded as
#: data so that a NEW one fails instead of joining it silently. Measured
#: 2026-07-28 by this gate on its first run.
#:
#: THIS IS A COHERENCE FINDING, NOT A PROVEN VIOLATION, and the difference is
#: recorded because the standards were read rather than paraphrased: no clause
#: of 1722.1-2021 7.2.19 or 7.2.13 bounds a STATIC AUDIO_MAP's
#: mapping_stream_channel by anything. The nearest normative sentence is Milan
#: v1.2 5.4.2.27, and it governs the ADD_AUDIO_MAPPINGS COMMAND on dynamic
#: ports: "A PAAD-AE shall treat as invalid a mapping that references a channel
#: of a Stream Input/Output that does not exist in the currently set format for
#: this Stream Input/Output." For the descriptor the spec is SILENT.
#:
#: What is nonetheless true: the deployed STREAM_PORT_OUTPUT[0] publishes
#: mappings onto stream channels 2..7 of a STREAM_OUTPUT whose ONLY advertised
#: format is 2-channel AAF, so six of its eight mappings name channels that
#: exist in no format the talker offers - the map cannot be acted on whatever
#: the format is set to. OWNER: the NxN talker work roadmap item 5 owns - the
#: AUDIO_MAP is generated from the port's CLUSTER count (endstation_builder.py:
#: one mapping per cluster) with nothing consulting channels_per_frame.
#: Down-declaring is NOT the fix (USER, commit e103d8e: the device declares
#: what it IS); the map has to be built from min(clusters, widest advertised
#: channels) or the talker has to grow.
KNOWN_MAP_DEVIATIONS = {
    "STREAM_PORT_OUTPUT[0] AUDIO_MAP[1] mapping (0,%d,%d,0): stream_channel "
    "%d >= 2, the widest channels_per_frame stream 0 advertises "
    "(['0x205022000806000']) - 7.2.6 / IEEE 1722-2016 7.3.1" % (c, c, c)
    for c in range(2, 8)
}


def assert_no_map_deviations(M, allow=KNOWN_MAP_DEVIATIONS):
    """Raise unless this model's AUDIO_MAP deviations are exactly the recorded
    ones. Separated from build_model so the tree keeps building while the
    deviation is open (roadmap item 00's pattern: a deviation that FAILS
    something is a finding, a deviation in a comment is not), and so a NEW
    deviation cannot join the recorded set unnoticed."""
    got = set(M["SMAP"]["DEVIATIONS"])
    new = got - set(allow)
    if new:
        raise ValueError("AUDIO_MAP deviations not on the recorded list:\n  "
                         + "\n  ".join(sorted(new)))
    return sorted(got)


def static_map_tables(spec, base_of, n_str_in, n_str_out):
    """Per-STREAM_PORT static AUDIO_MAP serving tables, AND the model-tier
    bounds gate that makes them checkable (defect B, 2026-07-28).

    WHY A GATE AND NOT JUST A TABLE.  GET_AUDIO_MAP answers with mappings the
    controller then uses to address AUDIO_CLUSTERs, and IEEE Std 1722.1-2021
    Table 7-33 / Table 7-162 define mapping_cluster_offset verbatim as

        "The offset from the base_cluster of the STREAM_PORT_INPUT or
         STREAM_PORT_OUTPUT for mapping[0]."

    The offsets are therefore PORT-RELATIVE. A model may write the SAME
    offsets on two ports and mean two different global clusters, which is
    exactly why no comparison of one declaration against another can see a
    wrong offset: it has to be compared against THE PORT'S OWN
    number_of_clusters. Nothing did that until now, and on 2026-07-28 a
    controller-grade check read 8 mappings with cluster_offset 0..7 out of a
    port declaring number_of_clusters = 2.

    Every bound here is the bound of a DIFFERENT descriptor:
      base_map                names an AUDIO_MAP this model defines   (7.2.13)
      number_of_maps == 1     the static serving path answers map_index 0 only
                              (7.4.44.1: any other index is BAD_ARGUMENT)
      number_of_mappings      <= 62                          (Table 7-32)
      cluster_offset          < the OWNING port's number_of_clusters
                                (Table 7-33 quoted above)
      cluster_channel         < that AUDIO_CLUSTER's channel_count    (7.2.16
                                Table 7-27: "The number of channels within the
                                cluster", descriptor offset 84)
      stream_index            < the stream descriptors this direction has
                                                                     (7.2.13)

    THE DUPLICATE RULE IS DIRECTION-ASYMMETRIC, and reading 7.2.19 rather than
    restating it is what caught that. Verbatim, for STREAM_PORT_INPUT:

        "There is at most one entry for each mapping_cluster_offset and
         mapping_cluster_channel, but there may be multiple entries for each
         mapping_stream_index and mapping_stream_channel."

    and for STREAM_PORT_OUTPUT the two halves swap:

        "There is at most one entry for each mapping_stream_index and
         mapping_stream_channel across the entire Configuration, but there may
         be multiple entries for each mapping_cluster_offset and
         mapping_cluster_channel."

    The first version of this gate applied the INPUT rule to BOTH directions
    (unique cluster channel), which the OUTPUT paragraph explicitly permits -
    it would have refused a conformant model. The output rule is also scoped
    "across the entire Configuration", so it is checked across all output
    ports together rather than per port.

    WHERE THE STANDARD IS SILENT, and it is said rather than filled in: no
    clause bounds a STATIC AUDIO_MAP's mapping_stream_channel by the stream's
    format. The nearest normative sentence is Milan v1.2 5.4.2.27, and it is
    about the DYNAMIC command, not the descriptor: "A PAAD-AE shall treat as
    invalid a mapping that references a channel of a Stream Input/Output that
    does not exist in the currently set format for this Stream Input/Output."
    Applying that to a static descriptor would bound a permanent structure by
    a runtime value, so this gate bounds by the WIDEST format the descriptor
    advertises and RECORDS rather than raises - see KNOWN_MAP_DEVIATIONS.

    Returns the emit dict; raises ValueError naming the offending port.
    """
    maps = spec["audio_maps"]
    deviations = []
    #! d_audio_cluster fixes channel_count = 1 for every cluster this model
    #! emits, so the 7.2.16 bound is "cluster_channel must be 0". Read from the
    #! encoder rather than restated, so a future multi-channel cluster moves
    #! both together.
    cluster_channel_count = 1

    def one(direction, ports, n_streams, stream_specs):
        addr, rows_n, moff = [], [], []
        #! 7.2.19 OUTPUT rule: "at most one entry for each
        #! mapping_stream_index and mapping_stream_channel ACROSS THE ENTIRE
        #! CONFIGURATION" - so this set spans all output ports, not one.
        cfg_stream_ch = {}
        for k, p in enumerate(ports):
            tag = f"STREAM_PORT_{direction}[{k}]"
            if p.get("map_mode", "static") == "dynamic":
                #! 7.2.13: "These Entities set the number_of_maps field to
                #! zero (0) and the base_map field is ignored when read." The
                #! mappings are runtime state, not a descriptor; ROWS = 0
                #! tells the RTL there is no static map to serve here.
                addr.append(0)
                rows_n.append(0)
                moff.append(0)
                continue
            if p["maps"] != 1:
                raise ValueError(
                    f"{tag} declares number_of_maps={p['maps']}; the static "
                    "GET_AUDIO_MAP path serves map_index 0 only, so any other "
                    "count advertises pages the entity cannot answer "
                    "(7.2.13 number_of_maps / 7.4.44.1 paging)")
            bm = p["base_map"]
            if not 0 <= bm < len(maps):
                raise ValueError(
                    f"{tag} base_map={bm} names an AUDIO_MAP this model does "
                    f"not define (it defines {len(maps)}: 0..{len(maps) - 1}) "
                    "- 7.2.13 base_map addresses a descriptor that must exist")
            rows = maps[bm]
            if len(rows) > SMAP_MAX_ROWS:
                raise ValueError(
                    f"{tag} AUDIO_MAP[{bm}] has {len(rows)} mappings; "
                    f"1722.1-2021 Table 7-32: \"The maximum value of this "
                    f"field is {SMAP_MAX_ROWS} for this version of AEM\"")
            seen = set()
            for (si, sc, co, cc) in rows:
                where = f"{tag} AUDIO_MAP[{bm}] mapping ({si},{sc},{co},{cc})"
                if co >= p["clusters"]:
                    raise ValueError(
                        f"{where}: cluster_offset {co} >= this port's "
                        f"number_of_clusters {p['clusters']}. 1722.1-2021 "
                        "Table 7-33: mapping_cluster_offset is \"The offset "
                        "from the base_cluster of the STREAM_PORT_INPUT or "
                        "STREAM_PORT_OUTPUT\" - PORT-RELATIVE (this port's "
                        f"base_cluster is {p['base_cluster']}), not a global "
                        "AUDIO_CLUSTER index")
                if cc >= cluster_channel_count:
                    raise ValueError(
                        f"{where}: cluster_channel {cc} >= channel_count "
                        f"{cluster_channel_count} of the AUDIO_CLUSTER at "
                        f"base_cluster+{co} (7.2.16 Table 7-27 channel_count: "
                        "\"The number of channels within the cluster\")")
                if si >= n_streams:
                    raise ValueError(
                        f"{where}: stream_index {si} >= the {n_streams} "
                        f"stream descriptors this direction has (7.2.13)")
                #! THE BOUND AT THIS TIER IS THE FORMAT *LIST*, NOT
                #! current_format.  A static AUDIO_MAP is a property of the
                #! port and outlives any one SET_STREAM_FORMAT, and the
                #! deployed model proves the difference is not hypothetical:
                #! the arty_current listener's formats are
                #! [0205022000806000 (2ch), 0215022002006000 (ut, 8ch)] with
                #! formats[0] - the reset default - carrying TWO channels,
                #! while its 8-cluster port maps stream channels 0..7. Bound
                #! by the widest format the descriptor advertises and the map
                #! is conformant; bound by the current one and a conformant
                #! model is refused for being narrowly configured today. The
                #! live controller check (tb/tools/hive_compliance.py C9) uses
                #! the CURRENT format because on the wire there is only one.
                #! The only normative sentence in reach is Milan v1.2 5.4.2.27
                #! and it governs ADD_AUDIO_MAPPINGS, not the descriptor: "A
                #! PAAD-AE shall treat as invalid a mapping that references a
                #! channel of a Stream Input/Output that does not exist in the
                #! currently set format for this Stream Input/Output." For a
                #! STATIC AUDIO_MAP the standard is SILENT.
                chans = [fmt_channels(f) for f in stream_specs[si]["formats"]]
                chans = [c for c in chans if c is not None]
                if not chans:
                    raise ValueError(
                        f"{where}: stream {si} ('{stream_specs[si]['name']}') "
                        "advertises no audio format with channels (CRF carries "
                        "a clock, not channels), so no channel of it can be "
                        "mapped to a cluster - 7.2.6 current_format / IEEE "
                        "1722-2016 7.3.1 channels_per_frame")
                if sc >= max(chans):
                    #! RECORDED, not raised: the deployed model violates this
                    #! one today (see KNOWN_MAP_DEVIATIONS) and the fix is a
                    #! product decision owned elsewhere. assert_no_map_
                    #! deviations() is what turns it into a failure, and it
                    #! fails on any deviation that is not the recorded one.
                    deviations.append(
                        f"{where}: stream_channel {sc} >= {max(chans)}, the "
                        f"widest channels_per_frame stream {si} advertises "
                        f"({[hex(f) for f in stream_specs[si]['formats']]}) - "
                        "7.2.6 / IEEE 1722-2016 7.3.1")
                #! 7.2.19, and the two directions are NOT the same rule.
                if direction == "INPUT":
                    #! "There is at most one entry for each
                    #!  mapping_cluster_offset and mapping_cluster_channel,
                    #!  but there may be multiple entries for each
                    #!  mapping_stream_index and mapping_stream_channel."
                    if (co, cc) in seen:
                        raise ValueError(
                            f"{where}: 1722.1-2021 7.2.19 for a "
                            "STREAM_PORT_INPUT - \"There is at most one entry "
                            "for each mapping_cluster_offset and "
                            f"mapping_cluster_channel\" - and ({co},{cc}) is "
                            "already mapped in this map")
                    seen.add((co, cc))
                else:
                    #! "There is at most one entry for each
                    #!  mapping_stream_index and mapping_stream_channel ACROSS
                    #!  THE ENTIRE CONFIGURATION, but there may be multiple
                    #!  entries for each mapping_cluster_offset and
                    #!  mapping_cluster_channel."
                    if (si, sc) in cfg_stream_ch:
                        raise ValueError(
                            f"{where}: 1722.1-2021 7.2.19 for a "
                            "STREAM_PORT_OUTPUT - \"There is at most one "
                            "entry for each mapping_stream_index and "
                            "mapping_stream_channel across the entire "
                            f"Configuration\" - and ({si},{sc}) is already "
                            f"mapped by {cfg_stream_ch[(si, sc)]}")
                    cfg_stream_ch[(si, sc)] = where
            addr.append(base_of(AUDIO_MAP, bm))
            rows_n.append(len(rows))
            #! the descriptor's OWN mappings_offset, read back from the bytes
            #! this model just encoded (7.2.19: the mappings "shall be
            #! accessed by using the mappings_offset field"). Table 7-32 fixes
            #! it at 8 "for this version of AEM"; deriving it means the RTL
            #! does not carry a second copy of that 8.
            img = d_audio_map(bm, rows)
            moff.append((img[4] << 8) | img[5])
        return addr, rows_n, moff

    if len(spec["ports_in"]) > SMAP_MAX_PORTS or \
            len(spec["ports_out"]) > SMAP_MAX_PORTS:
        raise ValueError(
            f"more than {SMAP_MAX_PORTS} STREAM_PORTs in one direction: the "
            "RTL GET_AUDIO_MAP port-index mux is 5 bits wide")
    in_addr, in_rows, in_moff = one("INPUT", spec["ports_in"], n_str_in,
                                    spec["stream_inputs"])
    out_addr, out_rows, out_moff = one("OUTPUT", spec["ports_out"], n_str_out,
                                       spec["stream_outputs"])
    return dict(IN_N=len(in_addr), OUT_N=len(out_addr),
                IN_ADDR=in_addr or [0], IN_ROWS=in_rows or [0],
                IN_MOFF=in_moff or [0],
                OUT_ADDR=out_addr or [0], OUT_ROWS=out_rows or [0],
                OUT_MOFF=out_moff or [0],
                DEVIATIONS=deviations)

# ----------------------------------------------------------------- specs ----
def builtin_spec():
    """Today's flashed model (milan-v12-entity.json shape) expressed as a
    build_model() spec — byte-identical to the pre-refactor hardcoded
    assembly. The endstation builder's arty_current overlay maps onto this
    exact spec (test-gated)."""
    return dict(
        entity=dict(name="Milan FPGA Talker",
                    firmware_version=firmware_version_string(),
                    group_name="", serial_number="AX7101-0001",
                    vendor_name="Kebag Logic"),
        rates=list(RATES), current_rate=RATES[0],
        rates_string="48/96/192 kHz",
        stream_inputs=[
            dict(name="Stream 1", kind="aaf", formats=list(FORMATS),
                 buffer=2126000),
            dict(name="CRF", kind="crf", formats=list(CRF_FORMATS),
                 buffer=2126000)],
        stream_outputs=[dict(name="Stream Output 0", formats=list(OUT_FORMATS))],
        clock_sources=[
            dict(name="Internal", cs_type=0x0000, raw_type="internal",
                 loc_type=CLOCK_SOURCE, loc_index=0),
            dict(name="Stream Clock", cs_type=0x0002, raw_type="input_stream",
                 loc_type=STREAM_INPUT, loc_index=0),
            dict(name="CRF Clock", cs_type=0x0002, raw_type="crf",
                 loc_type=STREAM_INPUT, loc_index=1)],
        ports_in=[dict(clusters=8, base_cluster=0, maps=1, base_map=0)],
        ports_out=[dict(clusters=8, base_cluster=8, maps=1, base_map=1)],
        audio_maps=[[[0, ch, ch, 0] for ch in range(8)],
                    [[0, ch, ch, 0] for ch in range(8)]],
        # D10 role names for the DEPLOYED arty shape, and the reason this
        # list is written out rather than computed: this spec is the
        # pre-builder model, and endstation_arty_current.yaml must reproduce
        # it byte-for-byte through the overlay path (test_builder gate 10).
        # The arty routes a 2-channel Philips I2S link (Pmod I2S2: CS4344 DAC
        # out, ADC in), so clusters 0..1 per direction are PHYSICAL and 2..7
        # are the virtual tail of the Milan 6.4 up-to-8 family.
        cluster_names_in=[f"I2S Out {n}" for n in range(2)]
                         + [f"Virtual Out {n}" for n in range(2, 8)],
        cluster_names_out=[f"I2S In {n}" for n in range(2)]
                          + [f"Virtual In {n}" for n in range(2, 8)],
    )

def _out_identity_offset(p):
    """Identity image origin for a dynamic output port: the port-relative
    offset of its PRIMARY pool segment (the same segment the static map
    wired at power-on - the builder's primary_role, carried by the
    overlay). Ports without pools start at 0."""
    prim = p.get("primary_role")
    for g in p.get("pool", []):
        if g["role"] == prim:
            return int(g["offset"])
    return 0


def _out_cluster_sources(ovl, j, p):
    """Capture-crossbar source templates for a dynamic OUTPUT port's
    clusters, derived from the overlay's D8 role pool. One dict per
    cluster: {src, idxh, idx, half, valid} in KL_chan_map_capture bucket
    terms (1 I2S / 2 TDM / 3 RING / 4 TONE / 5 LOOP). Bounds are the
    fabric's: 16 ring pairs, 4 TDM pairs, 8 loopback streams x 4 pairs.
    Ports without role pools return None (the ring-identity default)."""
    if p.get("map_mode", "static") != "dynamic" or not p.get("pool"):
        return None
    # the received stream channel space, mirroring the builder's
    # cluster_names() walk: loopback cluster n of port j starts at rx
    # stream j channel 0
    rx = []
    for si, s in enumerate(ovl["stream_inputs"]):
        if s.get("kind", "aaf") != "aaf":
            continue
        ch = (int(s["formats"][0], 16) >> 22) & 0x3FF
        rx.extend((si, c) for c in range(ch))
    # global host-channel prefix across the OUTPUT ports before this one
    host_pfx = 0
    for q in ovl["stream_ports"]["output"][:j]:
        host_pfx += sum(g["width"] for g in q.get("pool", [])
                        if g["role"] == "host")
    # task #65: what the BITSTREAM behind this model actually elaborates.
    # A template's `valid` is what the identity image below tests before it
    # wires a stream channel to a cluster, so this is the join between the
    # model and the gateware - and it is exactly what was missing when every
    # talker woke mapped to a loopback cluster no fabric could feed.
    fab = ovl.get("cluster_fabric") or {}
    lb_lane = bool(fab.get("loopback_lane", True))
    pb_rings = fab.get("playback_rings")
    srcs = []
    for g in p["pool"]:
        for n in range(g["width"]):
            if g["role"] == "physical":
                # capture phys channel (role_pool first=0). UNIFORM across
                # every front-end shape, because milan_datapath feeds the
                # slot-indexed bucket from aafcap_* whatever the front end is,
                # and an I2S-only capture parks at slot 0.
                #
                # This used to special-case channels 0..1 onto src=1 (the
                # single-pair I2S hold) and the rest onto src=2 offset by two,
                # which described the Arty BLEND topology and nothing else. It
                # was wrong two ways on a solo TDM master: the first two
                # channels aliased one hold that ignores idx, and the rest were
                # offset past their real slots. Nothing caught it because no
                # shipping config reaches this branch - the role-pool shapes
                # declare 0 physical channels and the shapes that declare
                # physical channels use the default (non-pool) policy.
                a = n
                srcs.append(dict(src=2, idxh=0, idx=a // 2, half=a % 2,
                                 valid=a // 2 < 4))   # 4 pair holds in fabric
            elif g["role"] == "host":
                if pb_rings is None:
                    # undeclared: the fabric maximum, exactly as before -
                    # including `half` off the GLOBAL channel index, which is
                    # only the same parity as n when every preceding host pool
                    # was even-width. Keep it exact.
                    gch = host_pfx + n
                    idx, half, ok = gch // 2, gch % 2, gch // 2 < 16
                else:
                    # DECLARED ring count. KL_pcm_tx serves pb_rings rings of
                    # this port's wire width, and the chmap can place ANY ring
                    # pair on ANY talker slot - so talker j draws on ring
                    # (j mod pb_rings) and its host cluster n is that ring's
                    # pair n//2. The old global stride assumed one ring PER
                    # talker: with the shipping single ring it pointed talkers
                    # 1..3 at ring pairs that are not elaborated and left 4..7
                    # with no template at all, which is the same "declared but
                    # unbuildable" defect one bucket over.
                    pps = max(1, g["width"] // 2)
                    idx = (j % pb_rings) * pps + n // 2
                    half = n % 2
                    ok = idx < pb_rings * pps and idx < 16
                srcs.append(dict(src=3, idxh=0, idx=idx, half=half,
                                 valid=ok))
            elif g["role"] == "pilot":
                srcs.append(dict(src=4, idxh=0, idx=0, half=0, valid=True))
            elif g["role"] == "loopback":
                if rx:
                    start = next((k for k, (si, c) in enumerate(rx)
                                  if si == j and c == 0), 0)
                    si, c = rx[(start + n) % len(rx)]
                else:
                    si, c = 0, n
                srcs.append(dict(src=5, idxh=si, idx=c // 2, half=c % 2,
                                 # the LOOP bucket only exists when
                                 # milan_datapath was built with LOOPBACK_P
                                 valid=lb_lane and si < 8 and c < 8))
            else:                # virtual: nothing behind it
                srcs.append(dict(src=0, idxh=0, idx=0, half=n % 2,
                                 valid=False))
    return srcs


def spec_from_overlay(ovl):
    """Map a builder-emitted AEM overlay (kebag-logic/aem-overlay 2.x, see
    sw/builder/endstation_builder.py emit_aem_overlay) onto a build_model()
    spec. Structure (N ports/streams) is fully consumed, including a CRF
    Media Clock Output (Milan 7.2.3: stream_outputs entry kind "crf" —
    appended after the AAF talkers, no STREAM_PORT/cluster/map, mirroring
    the CRF sink). Multi-stream shapes additionally emit the per-descriptor
    format tables (AEM_STRIN_*/AEM_STROUT_*, gated behind the stream count
    so the deployed shape's svh stays byte-identical — see emit_svh)."""
    if ovl.get("_schema") != "kebag-logic/aem-overlay":
        raise ValueError("not a kebag-logic/aem-overlay document")
    if not str(ovl.get("_schema_version", "")).startswith("2."):
        raise ValueError(f"overlay schema {ovl.get('_schema_version')} "
                         "(this consumer speaks 2.x)")
    ent = ovl["entity"]
    rates_hz = [int(r) for r in ovl["sampling_rates_hz"]]
    if any(hz not in (48000, 96000, 192000) for hz in rates_hz):
        raise ValueError(f"unsupported sampling rates {rates_hz}")
    if "firmware_version" not in ent:
        # No default here on purpose: the "0.1.0" that used to sit in this
        # position is exactly how a shape with no declared version shipped a
        # wrong one to every controller.  An overlay that cannot say what
        # firmware it is does not get a descriptor set.
        raise ValueError(
            "overlay entity has no firmware_version - the builder derives it "
            "from hdl/common/csr/milan_csr.sv VERSION (firmware_version_"
            "string()); regenerate the overlay")
    if not any(s["kind"] == "crf" for s in ovl["stream_inputs"]):
        raise ValueError("overlay without a CRF sink is not expressible in "
                         "the svh consumer today (AEM_CRF_FMTS_C)")
    cs_type = {"internal": 0x0000, "input_stream": 0x0002, "crf": 0x0002}
    loc_type = {"CLOCK_SOURCE": CLOCK_SOURCE, "STREAM_INPUT": STREAM_INPUT}
    stream_flags_in = 0x0003
    return dict(
        entity=dict(name=ent["name"],
                    firmware_version=ent["firmware_version"],
                    group_name=ent.get("group_name", ""),
                    serial_number=ent["serial_number"],
                    vendor_name=ent.get("vendor_name", "Kebag Logic")),
        gptp=ovl.get("gptp"),           # AVB_INTERFACE clock attributes
                                        # (single source with gptp.cfg)
        rates=rates_hz,                 # pull-0 encoding == Hz value
        current_rate=int(ovl["current_sampling_rate_hz"]),
        rates_string="/".join(str(hz // 1000) for hz in rates_hz) + " kHz",
        stream_inputs=[
            dict(name=s["name"], kind=s["kind"],
                 formats=[int(f, 16) for f in s["formats"]],
                 buffer=int(s.get("buffer_length_ns", 2126000)))
            for s in ovl["stream_inputs"]],
        stream_outputs=[
            dict(name=s["name"], kind=s.get("kind", "aaf"),
                 formats=[int(f, 16) for f in s["formats"]])
            for s in ovl["stream_outputs"]],
        clock_sources=[
            dict(name=c["name"], cs_type=cs_type[c["type"]],
                 raw_type=c["type"],
                 loc_type=loc_type[c["location_type"]],
                 loc_index=int(c["location_index"]))
            for c in ovl["clock_sources"]],
        ports_in=[dict(clusters=p["clusters"], base_cluster=p["base_cluster"],
                       maps=p["maps"], base_map=p["base_map"],
                       map_mode=p.get("map_mode", "static"),
                       map_page=p.get("map_page"))
                  for p in ovl["stream_ports"]["input"]],
        ports_out=[dict(clusters=p["clusters"], base_cluster=p["base_cluster"],
                        maps=p["maps"], base_map=p["base_map"],
                        map_mode=p.get("map_mode", "static"),
                        stream_index=p.get("stream_index", j),
                        cluster_sources=_out_cluster_sources(ovl, j, p),
                        identity_offset=_out_identity_offset(p))
                   for j, p in enumerate(ovl["stream_ports"]["output"])],
        audio_maps=[m["mappings"] for m in
                    sorted(ovl["audio_maps"], key=lambda m: m["index"])],
        # D10 cluster names (overlay 2.1+). An older 2.0 overlay carries no
        # audio_clusters list and falls back to the pre-rename "Input"/
        # "Output", so a stale overlay still builds a valid - if mute - model.
        cluster_names_in=[c["name"] for c in
                          sorted(ovl.get("audio_clusters", []),
                                 key=lambda c: c["index"])
                          if c["direction"] == "input"] or None,
        cluster_names_out=[c["name"] for c in
                           sorted(ovl.get("audio_clusters", []),
                                  key=lambda c: c["index"])
                           if c["direction"] == "output"] or None,
        _stream_flags_in=stream_flags_in,
    )

# ------------------------------------------------------------- assembly ----
def two_level_directory(directory):
    """Level-1 (type-direct-indexed) view of the descriptor directory.

    Derives, per descriptor type, {row of its first entry, entry count} and
    ASSERTS the layout the RTL's direct-indexed lookup depends on: each
    type's entries form ONE contiguous run of AEM_DIR_C rows, zero-based
    and ascending in descriptor_index. build_model's append order gives
    this structurally today; the assert turns a future interleave into a
    loud generator refusal instead of a silent mis-serve by the accessor.

    The table is zero-padded to a power of two (1 << AW rows) so the RTL
    can index it with the type's low bits unclamped: an absent type reads
    count 0 (miss) and a type at/above N is excluded by one range check.
    """
    runs = {}                       # type -> [first row, count]
    prev_t = None
    for row, (t, i, _b, _l) in enumerate(directory):
        if t not in runs:
            runs[t] = [row, 0]
        elif prev_t != t:
            raise ValueError(
                f"descriptor type 0x{t:04X} rows are not contiguous in the "
                f"directory (row {row} re-opens a run closed at row "
                f"{runs[t][0] + runs[t][1]}) - the two-level accessor "
                "needs one run per type; fix build_model's append order")
        if i != runs[t][1]:
            raise ValueError(
                f"type 0x{t:04X} descriptor_index not zero-based ascending: "
                f"row {row} carries index {i}, expected {runs[t][1]}")
        runs[t][1] += 1
        prev_t = t
    max_t = max(runs)
    if max_t >= 256:
        raise ValueError(
            f"descriptor type 0x{max_t:04X} would need a {max_t + 1}-row "
            "direct-indexed level-1 table - add a sparse first level "
            "before building models with types this high")
    aw = max(1, (max_t).bit_length())
    n = 1 << aw
    return dict(AW=aw, N=n,
                CNT=[runs.get(t, [0, 0])[1] for t in range(n)],
                ROW=[runs.get(t, [0, 0])[0] for t in range(n)])


def _two_level_resolve(l1, directory, t, i):
    """The RTL accessor's answer, modelled bit-for-bit: (found, base, len)."""
    if t >= l1["N"]:
        return (0, 0, 0)
    cnt, row = l1["CNT"][t], l1["ROW"][t]
    if i >= cnt:
        return (0, 0, 0)
    _t, _i, b, l = directory[row + i]
    return (1, b, l)


def check_two_level(l1, directory):
    """1:1 equivalence gate: the two-level resolve answers EXACTLY like the
    linear scan it replaces, hits and misses alike, for every directory
    entry plus a fence of miss probes (index past each run, absent types,
    types past the table). Raises on the first divergence."""
    def linear(t, i):
        f = (0, 0, 0)
        for (tt, ii, b, l) in directory:
            if tt == t and ii == i:
                f = (1, b, l)
        return f

    probes = set()
    for (t, i, _b, _l) in directory:
        probes |= {(t, i), (t, i + 1), (t, 0xFFFF)}
    for t in range(l1["N"] + 4):
        probes |= {(t, 0), (t, 1)}
    probes.add((0xFFFF, 0))
    for (t, i) in sorted(probes):
        want = linear(t, i)
        got = _two_level_resolve(l1, directory, t, i)
        if got != want:
            raise ValueError(
                f"two-level directory diverges from the linear scan at "
                f"type 0x{t:04X} index {i}: linear {want}, two-level {got}")


def named_structure(l1, directory, named):
    """Split the SET/GET_NAME table into the structural rule + exceptions.

    Structural: a type whose EVERY directory entry is named, at name_index
    0, with object_name at descriptor base + 4 - resolvable through the
    two-level directory (mask hit -> AEM_DIR_C[row + index].base + 4).
    Everything else (ENTITY's two names at 48/180) stays an explicit
    emitted match line. Returns (mask, exceptions); raises if the split
    does not reproduce the NAMED list 1:1, hits and misses alike."""
    base = {(t, i): b for (t, i, b, _l) in directory}
    per_type = {}
    for (t, i, nidx, addr) in named:
        per_type.setdefault(t, []).append((i, nidx, addr))
    mask, exc = 0, []
    for t, entries in sorted(per_type.items()):
        structural = (
            t < l1["N"]
            and all(nidx == 0 and addr == base[(t, i)] + 4
                    for (i, nidx, addr) in entries)
            and sorted(i for (i, _n, _a) in entries)
            == list(range(l1["CNT"][t])))
        if structural:
            mask |= 1 << t
        else:
            exc += [(t, i, nidx, addr) for (i, nidx, addr) in entries]
    check_named(l1, directory, named, mask, exc)
    return mask, exc


def check_named(l1, directory, named, mask, exc):
    """1:1 equivalence gate for the name split: mask + exceptions answer
    EXACTLY like the flat NAMED table, hits and misses alike."""
    def resolve(t, i, nidx):
        for (et, ei, en, ea) in exc:
            if (t, i, nidx) == (et, ei, en):
                return (1, ea)
        if (t < l1["N"] and nidx == 0 and (mask >> t) & 1
                and i < l1["CNT"][t]):
            return (1, directory[l1["ROW"][t] + i][2] + 4)
        return (0, 0)

    want = {(t, i, n): a for (t, i, n, a) in named}
    probes = set(want)
    for (t, i, n) in list(want):
        probes |= {(t, i + 1, n), (t, i, n + 1), (t, 0xFFFF, n)}
    for t in range(l1["N"] + 4):
        probes.add((t, 0, 0))
    for key in sorted(probes):
        got = resolve(*key)
        exp = (1, want[key]) if key in want else (0, 0)
        if got != exp:
            raise ValueError(
                f"structural name lookup diverges from the NAMED table at "
                f"type 0x{key[0]:04X} index {key[1]} name_index {key[2]}: "
                f"table {exp}, structural {got}")


def build_model(spec):
    """Assemble ROM + directory + overlay/write-back/name tables from a spec
    (builtin_spec() or spec_from_overlay()). Returns the model dict the
    emitters consume."""
    si, so = spec["stream_inputs"], spec["stream_outputs"]
    descs = [
        (ENTITY,        0, d_entity(spec["entity"])),
        (CONFIGURATION, 0, d_configuration(len(si), len(so),
                                           len(spec["clock_sources"]))),
        (AUDIO_UNIT,    0, d_audio_unit(spec["rates"], spec["current_rate"],
                                        len(spec["ports_in"]),
                                        len(spec["ports_out"]))),
    ]
    for k, s in enumerate(si):
        descs.append((STREAM_INPUT, k,
                      d_stream(STREAM_INPUT, k, s["name"], 0x0003,
                               s["formats"], s["buffer"])))
    for k, s in enumerate(so):
        # CRF Media Clock Output (Milan 7.2.3): CLOCK_SYNC_SOURCE|CLASS_A
        # (1722.1 7.2.6.1 - the stream IS a clock sync source; Milan 7.3.3
        # mandates Class A). AAF outputs keep the deployed CLASS_A-only word.
        # Both get clock_domain_index 0 (7.2.6): 7.2.9.2 has no OUTPUT_STREAM
        # CLOCK_SOURCE type - domain membership is the STREAM field itself.
        flags = 0x0003 if s.get("kind", "aaf") == "crf" else 0x0002
        descs.append((STREAM_OUTPUT, k,
                      d_stream(STREAM_OUTPUT, k, s["name"], flags,
                               s["formats"])))
    descs.append((AVB_INTERFACE, 0, d_avb_interface(spec.get("gptp"))))
    for k, cs in enumerate(spec["clock_sources"]):
        descs.append((CLOCK_SOURCE, k,
                      d_clock_source(k, cs["name"], cs["cs_type"],
                                     cs["loc_type"], cs["loc_index"])))
    descs.append((CLOCK_DOMAIN, 0, d_clock_domain(len(spec["clock_sources"]))))
    descs.append((CONTROL, 0, d_control_identify()))
    descs.append((LOCALE, 0, d_locale()))
    descs.append((STRINGS, 0, d_strings(
        [spec["entity"]["name"], spec["rates_string"],
         spec["entity"]["vendor_name"], "", "", "", ""])))
    # map_mode (gaps item 8, dynamic audio maps): a "dynamic" port carries
    # NO AUDIO_MAP descriptor and advertises number_of_maps=0 / base_map=0 -
    # the 1722.1-2021 7.2.13 dynamic-mapping capability signal ("These
    # Entities set the number_of_maps field to zero (0) and the base_map
    # field is ignored"). Milan v1.2 5.3.3.9 makes that the SHALL on the
    # listener side ("The Stream Port Input of a Configuration shall not
    # contain any AUDIO_MAP descriptor. Note: this means that a PAAD-AE
    # implements dynamic mappings on all of its Stream Port Inputs"), so
    # ANY subset of the input ports may be dynamic (roadmap 23). Outputs
    # stay static: 5.3.3.9 leaves them free and 5.4.2.26-28 mandate
    # NOT_SUPPORTED for a Stream Port Output that HAS Audio Maps.
    for k, p in enumerate(spec["ports_in"]):
        dyn = p.get("map_mode", "static") == "dynamic"
        descs.append((STREAM_PORT_INPUT, k,
                      d_stream_port(STREAM_PORT_INPUT, k, 0x0001,
                                    p["clusters"], p["base_cluster"],
                                    0 if dyn else p["maps"],
                                    0 if dyn else p["base_map"])))
    # Outputs MAY be dynamic too (USER 08-01): Milan 5.3.3.9 leaves them
    # free, and 5.4.2.26-28 make GET/ADD/REMOVE_AUDIO_MAPPINGS a SHALL for
    # "each Stream Port Output that has no Audio Map" - so a dynamic output
    # port drops its AUDIO_MAP descriptor and signals 7.2.13 exactly like a
    # dynamic input.
    for k, p in enumerate(spec["ports_out"]):
        dyn = p.get("map_mode", "static") == "dynamic"
        descs.append((STREAM_PORT_OUTPUT, k,
                      d_stream_port(STREAM_PORT_OUTPUT, k, 0x0000,
                                    p["clusters"], p["base_cluster"],
                                    0 if dyn else p["maps"],
                                    0 if dyn else p["base_map"])))
    n_in = sum(p["clusters"] for p in spec["ports_in"])
    n_out = sum(p["clusters"] for p in spec["ports_out"])
    # AUDIO_CLUSTER object_names (builder D10). Before 2026-07-28 every
    # cluster of every shape was literally named "Input" or "Output", which
    # told a controller operator nothing: on an 8x8 board Hive showed eighty
    # identical rows and no way to tell a pilot tone from a dead TDM slot
    # from a loopback lane. Names now come from the cluster's ROLE (the
    # builder's cluster_names(); the overlay carries them per cluster).
    # 1722.1-2021 6.2.2.8 lists object_name among the fields EXCLUDED from
    # "the structure of the data model", so this rename does NOT bump any
    # entity_model_id - and the descriptor is fixed-width (cstr pads to 64),
    # so no offset, length or directory entry moves either.
    names_in = spec.get("cluster_names_in") or ["Input"] * n_in
    names_out = spec.get("cluster_names_out") or ["Output"] * n_out
    if len(names_in) != n_in or len(names_out) != n_out:
        raise ValueError(f"cluster name count {len(names_in)}/{len(names_out)}"
                         f" != cluster count {n_in}/{n_out}")
    for k in range(n_in):
        descs.append((AUDIO_CLUSTER, k,
                      d_audio_cluster(k, names_in[k], NO_STRING)))
    for k in range(n_in, n_in + n_out):
        descs.append((AUDIO_CLUSTER, k,
                      d_audio_cluster(k, names_out[k - n_in], AUDIO_UNIT)))
    for k, rows in enumerate(spec["audio_maps"]):
        descs.append((AUDIO_MAP, k, d_audio_map(k, rows)))

    rom = b""
    directory = []           # (type, index, base, length)
    for t, i, img in descs:
        directory.append((t, i, len(rom), len(img)))
        rom += img
    # The svh addresses the store with 16-bit words throughout (AEM_DIR_C
    # {type, index, base, len}, the overlay/write-back/name tables, the MVU
    # scratch tail), so a ROM past 64 KiB would silently wrap instead of
    # failing. Say so here: the builder catches this as aem_rom_unsupported
    # and marks the shape "planned" rather than emitting a broken ROM.
    # Growing past this is D6's job (BRAM hot stub + DRAM bulk tree).
    if len(rom) + 64 > 0x10000:
        raise ValueError(
            f"AEM ROM {len(rom)} B + 64 B MVU scratch exceeds the 16-bit "
            f"store address space (65536 B) - {len(directory)} descriptors, "
            f"{n_in + n_out} AUDIO_CLUSTERs at {len(d_audio_cluster(0, '', 0))}"
            " B each. A model this large is the D6 split (BRAM hot stub + "
            "DRAM bulk descriptor tree), not a wider ROM")

    def base_of(t, i=0):
        return next(b for (tt, ii, b, _) in directory if tt == t and ii == i)

    # Dynamic read overlays: (rom_addr, nbytes, source). Sources are resolved
    # by KL_aecp_aem_dyn_mux from the live CSR/state wires.
    E = base_of(ENTITY); A = base_of(AVB_INTERFACE)
    overlays = [
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
        (E + 48,  8, "ENT_NAME8"),   # first 8 chars of entity_name: board name
                                     # ("ARTY"/"ALINX") from the CSR, S50-set
        (E + 310, 2, "CURRENT_CFG"),
        (A + 70,  6, "MAC"),
        (A + 78,  8, "CLOCK_ID"),
    ]

    # SET_* write-back targets (rom_addr of the field inside its descriptor).
    # NOTE: the legacy WB_STREAM_FORMAT_C symbol reaches STREAM_OUTPUT[0]
    # only; multi-stream shapes get the per-descriptor WB_STRIN/STROUT_FMT_
    # ADDR_C arrays (PER_STREAM below) the gated RTL path indexes instead.
    wb = {
        "SAMPLING_RATE":   base_of(AUDIO_UNIT) + 136,
        "STREAM_FORMAT":   base_of(STREAM_OUTPUT) + 74,   # STREAM_OUTPUT[0] current
    }
    for k in range(len(si)):
        wb[f"STREAM_IN{k}_FMT"] = base_of(STREAM_INPUT, k) + 74
    wb["CLOCK_SRC_IDX"] = base_of(CLOCK_DOMAIN) + 70      # clock_source_index
    wb["CONTROL_CUR"] = base_of(CONTROL) + 108            # IDENTIFY current_value
    for k in range(len(spec["audio_maps"])):
        wb[f"AUDIO_MAP_{k}"] = base_of(AUDIO_MAP, k)      # GET_AUDIO_MAP source

    # SET/GET_NAME directory: (type, index, name_index) -> object_name addr.
    # ENTITY carries two names (entity_name / group_name); every other named
    # descriptor has object_name at base+4, name_index 0.
    named = [(ENTITY, 0, 0, E + 48), (ENTITY, 0, 1, E + 180)] + [
        (t, i, 0, b + 4)
        for (t, i, b, _) in directory
        if t in (CONFIGURATION, AUDIO_UNIT, STREAM_INPUT, STREAM_OUTPUT,
                 AVB_INTERFACE, CLOCK_SOURCE, CLOCK_DOMAIN, CONTROL,
                 AUDIO_CLUSTER)
    ]

    # svh validation tables: first AAF input / the CRF input (the legacy
    # single-stream symbols, always emitted — the RTL default/reset reach)
    fmts = next(s["formats"] for s in si if s.get("kind", "aaf") == "aaf")
    crf_fmts = next(s["formats"] for s in si if s.get("kind") == "crf")

    # Per-descriptor stream-format tables (item-4 follow-up): kind flag,
    # reference entry (formats[0] = the current/base format the RTL
    # validates against) and SET/GET write-back address per STREAM_INPUT/
    # STREAM_OUTPUT descriptor. EMIT gates the svh block behind the stream
    # count so the deployed 1-AAF-in/1-out shape's svh (and the RTL path it
    # compiles) stays byte-identical (see emit_svh).
    per_stream = dict(
        IN_CRF=[s.get("kind", "aaf") == "crf" for s in si],
        IN_FMT0=[s["formats"][0] for s in si],
        OUT_FMT0=[s["formats"][0] for s in so],
        IN_WB=[base_of(STREAM_INPUT, k) + 74 for k in range(len(si))],
        OUT_WB=[base_of(STREAM_OUTPUT, k) + 74 for k in range(len(so))],
        EMIT=(len(si) > 2 or len(so) > 1),
    )

    # Dynamic-map engine constants (gaps item 8, generalized to EVERY
    # STREAM_PORT_INPUT by roadmap 23). Gated exactly like PER_STREAM:
    # emitted ONLY when at least one input port is map_mode dynamic, so a
    # fully static shape's svh (and the RTL path it compiles) stays
    # byte-identical. Milan 5.4.2.26 partitioning: a port's cluster channels
    # (mono clusters, d_audio_cluster channel_count=1 => keys == clusters)
    # are split into fixed subsets of PAGE keys; number_of_maps =
    # ceil(clusters/PAGE) is returned per port no matter the live mapping
    # count. PAGE is capped at 9 by the RTL const-scratch: the page walk's
    # last row starts at 6 + 8*(PAGE-1) and is 8 bytes long, so 8*PAGE + 5
    # must stay inside const_q's 80 bytes. It is SHARED by every dynamic
    # port (the RTL page origin is a constant multiply); per-port cluster
    # counts may still differ.
    #
    # The store key is the GLOBAL cluster index (base_cluster + offset),
    # which is exactly the render crossbar's map-RAM address - one key space
    # for the model, the fabric and the CSR 0x900 debug port alike.
    pin, pout = spec["ports_in"], spec["ports_out"]
    dyn_in = [p for p in pin if p.get("map_mode", "static") == "dynamic"]
    dynmap = dict(EMIT=bool(dyn_in))
    if dynmap["EMIT"]:
        explicit = {int(p["map_page"]) for p in dyn_in if p.get("map_page")}
        if len(explicit) > 1:
            raise ValueError("every dynamic STREAM_PORT_INPUT must share one "
                             f"map_page (RTL partition constant): "
                             f"{sorted(explicit)}")
        page = explicit.pop() if explicit \
            else min(max(p["clusters"] for p in dyn_in), 8)
        if not 1 <= page <= 9:
            raise ValueError(f"map_page {page} outside 1..9 (the RTL "
                             "GET_AUDIO_MAP const-scratch bound)")
        keys = max(p["base_cluster"] + p["clusters"] for p in dyn_in)
        if keys > 64:
            raise ValueError(f"{keys} dynamic cluster keys exceeds the 64-key "
                             "render map address space (chmap64)")

        def _dyn(p):
            return p.get("map_mode", "static") == "dynamic"

        # A mapping may reference ANY STREAM_INPUT (1722.1-2021 Table 7-33:
        # mapping_stream_index is "the STREAM_INPUT or STREAM_OUTPUT
        # descriptor index for the stream carrying this channel"), so the
        # engine validates the stream channel against THAT stream's current
        # format (Milan 5.3.10.1 / 5.4.2.27). CRF inputs carry no audio
        # channels and are not mappable.
        si_aaf = [s.get("kind", "aaf") == "aaf" for s in si]
        si_ch = [((s["formats"][0] >> 22) & 0x3FF) if a else 0
                 for s, a in zip(si, si_aaf)]
        dynmap.update(
            KEYS=keys, PAGE=page,
            NPORTS=len(pin),
            PDYN=[_dyn(p) for p in pin],
            PBASE=[p["base_cluster"] for p in pin],
            PCLS=[p["clusters"] for p in pin],
            #: dynamic -> ceil(clusters/PAGE) partitions; static -> its
            #: declared AUDIO_MAP count (GET serves the ROM descriptor)
            PNMAPS=[(-(-p["clusters"] // page) if _dyn(p) else p["maps"])
                    for p in pin],
            NSTRIN=len(si), SAAF=si_aaf, SCH=si_ch,
            PHYS=CHMAP_PHYS_DEPTH)

    # Talker-side dynamic-map engine constants (USER 08-01: "enable dynamic
    # mapping on stream_output as well"). Gated like DYNMAP: emitted only
    # when at least one OUTPUT port is map_mode dynamic. The engine's key is
    # the port's STREAM channel (Milan 5.4.2.26 note: "at most one dynamic
    # mapping per Stream Output's channel" - the stream channel is the
    # natural unique key), 8 keys per port (the DMAP_CHMAX ch[2:0] fabric
    # bound). Vendor validity rules (1722.1-2021 7.4.45.1 says validity "is
    # governed by a set of vendor defined rules"):
    #   * mapping_stream_index must be the port's OWN stream (the capture
    #     crossbar routes port j's clusters into stream j - 1:1 fabric);
    #   * records arrive in L/R-adjacent pairs mapping stream channels
    #     {2m, 2m+1} to the two halves of ONE source pair (the capture map
    #     is PAIR-slot granular; a half-armed slot would make GET report a
    #     route that carries no audio - the same wire-truth refusal the
    #     input side applies to keys past the render crossbar);
    #   * a cluster is projectable only where CSRC marks a live source
    #     behind it (ring/tone/loopback/physical bounds, resolved HERE).
    # The partition of 5.4.2.26 is over the Stream Output's channels: <= 8
    # of them, so every port is a single page (number_of_maps = 1).
    dyn_out = [p for p in pout if p.get("map_mode", "static") == "dynamic"]
    odmap = dict(EMIT=bool(dyn_out))
    if odmap["EMIT"] and not dynmap["EMIT"]:
        # the RTL nests `AEM_ODYNMAP inside `AEM_DYNMAP (the walk states are
        # shared), and Milan 5.3.3.9 makes dynamic INPUTS mandatory anyway
        raise ValueError("dynamic STREAM_PORT_OUTPUTs require dynamic "
                         "STREAM_PORT_INPUTs (Milan 5.3.3.9 mandates them)")
    if odmap["EMIT"]:
        so_ch = [((s["formats"][0] >> 22) & 0x3FF) for s in so]
        # packetizer pair-slot base per STREAM_OUTPUT (its prefix-sum space)
        slotb_str, acc = [], 0
        for c in so_ch:
            slotb_str.append(acc)
            acc += (c + 1) // 2
        pcbase, csrc, init = [], [], []
        for j, p in enumerate(pout):
            pcbase.append(len(csrc))
            stream = p.get("stream_index", j)
            srcs = p.get("cluster_sources")
            if srcs is None:
                # default policy (no role pools declared): the port's
                # clusters are its talker's own ALSA-ring pairs in order -
                # cluster c = ring pair (slot base + c//2), half c%2
                srcs = [dict(src=3, idxh=0, idx=slotb_str[stream] + c // 2,
                             half=c % 2, valid=slotb_str[stream] + c // 2 < 16)
                        for c in range(p["clusters"])]
            if len(srcs) != p["clusters"]:
                raise ValueError(
                    f"ports_out[{j}]: {len(srcs)} cluster_sources for "
                    f"{p['clusters']} clusters")
            csrc.extend(srcs)
            # identity image: stream channel c <- the port's primary
            # cluster run (offset c of the identity rows the static map
            # declared), kept only where the source pair really projects
            ic0 = p.get("identity_offset", 0)
            for c in range(8):
                co = ic0 + c
                ok = (c < so_ch[stream] and co < p["clusters"]
                      and srcs[co].get("valid", True)
                      and (srcs[co]["src"] == 4 or srcs[co]["half"] == c % 2))
                init.append(dict(v=ok, co=co if ok else 0))
        odmap.update(
            KEYS=8 * len(pout), NPORTS=len(pout),
            PDYN=[p.get("map_mode", "static") == "dynamic" for p in pout],
            PCLS=[p["clusters"] for p in pout],
            PCBASE=pcbase,
            PSTR=[p.get("stream_index", j) for j, p in enumerate(pout)],
            SLOTB=[slotb_str[p.get("stream_index", j)]
                   for j, p in enumerate(pout)],
            SCH=[so_ch[p.get("stream_index", j)]
                 for j, p in enumerate(pout)],
            CSRC=csrc, INIT=init)

    # Static AUDIO_MAP serving tables + the model's own bounds gate (defect B,
    # 2026-07-28). Emitted for EVERY shape, static or dynamic, because the
    # static GET_AUDIO_MAP path exists in every build - the tables are what let
    # it answer from the ADDRESSED PORT'S OWN base_map instead of a hardcoded
    # descriptor index (defect A).
    smap = static_map_tables(spec, base_of, len(si), len(so))

    # Two-level directory (accessor area lever): derive the level-1 table,
    # prove it answers exactly like the linear scan, and split the NAMED
    # table into structural-rule + exceptions. All three raise on a model
    # whose layout the direct-indexed RTL could mis-serve.
    l1 = two_level_directory(directory)
    check_two_level(l1, directory)
    name_mask, name_exc = named_structure(l1, directory, named)

    #  the CLOCK_SOURCE shape travels with the model, because the RTL needs
    #  two facts about it that no other field carries: how many sources the
    #  configuration declares, and which one is the CRF
    _cs_list = spec["clock_sources"]
    return dict(rom=rom, directory=directory, ROM_SIZE=len(rom),
                OVERLAYS=overlays, WB=wb, NAMED=named,
                N_CLKSRC=len(_cs_list),
                CRF_CLKSRC=next((i for i, c in enumerate(_cs_list)
                                 if c.get("raw_type") == "crf"), None),
                L1=l1, NAME_MASK=name_mask, NAME_EXC=name_exc,
                RATES=spec["rates"], FORMATS=fmts, CRF_FMTS=crf_fmts,
                PER_STREAM=per_stream, DYNMAP=dynmap, ODMAP=odmap, SMAP=smap)

#: Render-crossbar DEPTH: how many physical output channels
#: KL_chan_map_render holds a map word for, i.e. milan_datapath's
#: CHMAP_PHYS_C (2 I2S + 8 TDM). sw/builder/test_builder.py gate 17c asserts
#: this equals that localparam, so the AEM refusal and the fabric write gate
#: can never disagree about which keys exist.
#:
#: NOT the same number as audio_interface.physical_channels.render, which is
#: how many of those channels reach a PIN on a given board (arty_4x4 says 2,
#: ax7101_8x8 says 0). A key inside the crossbar but past the routed width
#: still maps onto a parked wire - that is the separate, pre-existing
#: "audio_interface unbacked by fabric" gap, flagged in
#: docs/MILAN_COMPLIANCE_GAPS.md and deliberately NOT silently closed here.
CHMAP_PHYS_DEPTH = 10

SRC_IDS = {name: n for n, name in enumerate(
    ["ENTITY_ID", "MODEL_ID", "ECAPS", "TALKER_SRC", "TALKER_CAP",
     "LISTEN_SINK", "LISTEN_CAP", "CTRL_CAP", "AVAIL_IDX", "ASSOC_ID",
     "CURRENT_CFG", "MAC", "CLOCK_ID", "ENT_NAME8"])}

# Module-level model = the builtin shape (import-compatible aliases: the
# builder test gate and the doc generator read these).
_M = build_model(builtin_spec())
rom = _M["rom"]
directory = _M["directory"]
ROM_SIZE = _M["ROM_SIZE"]
OVERLAYS = _M["OVERLAYS"]
WB = _M["WB"]
NAMED = _M["NAMED"]

def base_of(t, i=0):
    return next(b for (tt, ii, b, _) in directory if tt == t and ii == i)

# ------------------------------------------------------------- emitters ----
def emit_svh(M, path):
    """Write the ROM include. The text itself comes from emit_svh_text() so a
    caller that wants the bytes without a file (sw/builder/endstation_builder
    .py emit_aem_rom_svh) gets the SAME generator, not a second one."""
    with open(path, "w") as f:
        f.write(emit_svh_text(M))

def emit_svh_text(M):
    rom_, directory_ = M["rom"], M["directory"]
    rom_size = M["ROM_SIZE"]
    lines = []
    a = lines.append
    a("// GENERATED by avdecc/gen_aem_store.py - DO NOT EDIT.")
    a("// Milan v1.2 HW entity, FULL mandatory descriptor set (FR-ENUM-02).")
    a("// See avdecc/milan-v12-entity.json.")
    a("//")
    a("// NOT COMPILED BY ANY RTL (2026-08-12). This is a rendering of the")
    a("// DECLARATIVE entity model. The IEEE 1722.1 control plane that used to")
    a("// `include it (hdl/ieee17221/aecp/**, KL_aecp_aem_store) is DELETED and")
    a("// the protocol-processor submodule is the control plane now, so NO")
    a("// controller can READ_DESCRIPTOR any of the descriptors below off this")
    a("// gateware. What DOES reach silicon from this same model is the ADP")
    a("// shape - talker_stream_sources / listener_stream_sinks and the two")
    a("// capability words - via hdl/common/csr/gen/adp_shape_defaults.svh.")
    a("")
    a(f"localparam int unsigned AEM_ROM_BYTES_C = {rom_size};")
    a(f"localparam int unsigned AEM_DESC_N_C    = {len(directory_)};")
    a("// Scratch tail (zero-init RAM past the descriptor image): Milan MVU")
    a("// media_clock_domain_name (64 B, Milan 1.3 §5.4.4.4)")
    a("localparam int unsigned AEM_STORE_BYTES_C = AEM_ROM_BYTES_C + 64;")
    a(f"localparam [15:0] WB_MCR_DOMNAME_C = 16'd{rom_size};")
    a("")
    a("// Descriptor directory: {type[15:0], index[15:0], base[15:0], len[15:0]}")
    a(f"localparam [63:0] AEM_DIR_C [0:{len(directory_)-1}] = '{{")
    for n, (t, i, b, l) in enumerate(directory_):
        sep = "," if n < len(directory_) - 1 else ""
        a(f"  64'h{t:04X}_{i:04X}_{b:04X}_{l:04X}{sep}")
    a("};")
    a("")
    l1 = M["L1"]

    def rows16(vals):
        for k in range(0, len(vals), 8):
            chunk = ", ".join(f"16'd{v}" for v in vals[k:k + 8])
            yield "  " + chunk + ("," if k + 8 < len(vals) else "")
    a("// Level 1 of the directory (type-direct-indexed): per-type runs in")
    a("// AEM_DIR_C are CONTIGUOUS, ZERO-BASED and ASCENDING (generator-")
    a("// asserted 1:1 against the linear scan - gen_aem_store.py")
    a("// check_two_level), so (type, index) resolves by ROM indexing alone:")
    a("//   hit = index < AEM_L1_CNT_C[type],")
    a("//   {base, len} = AEM_DIR_C[AEM_L1_ROW_C[type] + index][31:0].")
    a("// Zero-padded to 1 << AEM_L1_AW_C rows: an absent type reads count 0.")
    a(f"localparam int unsigned AEM_L1_AW_C = {l1['AW']};")
    a(f"localparam int unsigned AEM_L1_N_C  = {l1['N']};")
    a(f"localparam [15:0] AEM_L1_CNT_C [0:{l1['N'] - 1}] = '{{")
    for line in rows16(l1["CNT"]):
        a(line)
    a("};")
    a(f"localparam [15:0] AEM_L1_ROW_C [0:{l1['N'] - 1}] = '{{")
    for line in rows16(l1["ROW"]):
        a(line)
    a("};")
    a("")
    a("// ROM image (network byte order, addr 0 = first byte of ENTITY)")
    a(f"localparam [7:0] AEM_ROM_INIT_C [0:{rom_size-1}] = '{{")
    row = []
    for n, byte in enumerate(rom_):
        row.append(f"8'h{byte:02X}")
        if len(row) == 16:
            sep = "," if n < rom_size - 1 else ""
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
    for base, nb, src in M["OVERLAYS"]:
        a(f"    if (addr >= 16'd{base} && addr < 16'd{base + nb})")
        a(f"      aem_ovl_lookup = {{1'b1, OVL_{src}_C, 3'(addr - 16'd{base})}};")
    a("  end")
    a("endfunction")
    a("")
    a("// SET_* write-back base addresses")
    for k, v in M["WB"].items():
        a(f"localparam [15:0] WB_{k}_C = 16'd{v};")
    a("")
    a("// SET/GET_NAME qualifier: (type, index, name_index) + the directory")
    a("// oracle's REGISTERED answer -> {valid, rom addr}. Reads no ROM of")
    a("// its own (the level-2 directory is block RAM; a second read port")
    a("// here would be a second BRAM or a distributed copy): a masked")
    a("// type's object_name sits at descriptor base + 4, name_index 0, for")
    a("// every index of its run (generator-asserted 1:1 against the NAMED")
    a("// table - gen_aem_store.py named_structure/check_named), so the")
    a("// accessor's (found, base) for the SAME (type, index) already carry")
    a("// the lookup. Exceptions (ENTITY's entity_name/group_name) are")
    a("// constant matches. CALLER CONTRACT: acc_found/acc_base must be")
    a("// KL_aecp_accessor's answer for this (t, idx) at config 0.")
    l1_aw = M["L1"]["AW"]
    a(f"localparam [{M['L1']['N'] - 1}:0] AEM_NAMED_MASK_C = "
      f"{M['L1']['N']}'h{M['NAME_MASK']:X};")
    a("function automatic [16:0] aem_name_qual(input [15:0] t,")
    a("                                        input [15:0] idx,")
    a("                                        input [15:0] nidx,")
    a("                                        input        acc_found,")
    a("                                        input [15:0] acc_base);")
    a("  begin")
    a("    aem_name_qual = 17'd0;")
    for t, i, nidx, addr in M["NAME_EXC"]:
        a(f"    if (t == 16'h{t:04X} && idx == 16'd{i} && nidx == 16'd{nidx})")
        a(f"      aem_name_qual = {{1'b1, 16'd{addr}}};")
    a("    if (t < 16'(AEM_L1_N_C) && nidx == 16'd0 &&")
    a(f"        AEM_NAMED_MASK_C[t[{l1_aw - 1}:0]] && acc_found)")
    a("      aem_name_qual = {1'b1, acc_base + 16'd4};")
    a("  end")
    a("endfunction")
    a("")
    a("// Value validation tables")
    # The COUNT, not just the table. KL_aecp_response_builder used to compare
    # a SET_SAMPLING_RATE against AEM_RATES_C[0], [1] and [2] literally, which
    # only worked while every config advertised exactly three rates: the 8x8
    # ship config honestly advertises ONE (audio_unit_rates_hz: [48000]), so
    # [1] and [2] read off the end of a [0:0] array - Verilator SELRANGE, and
    # in synthesis an out-of-range read is simply zero, so the check "passed"
    # by accident rather than by construction. Emit the bound and let the RTL
    # loop over it.
    # CLOCK_SOURCE shape. Emitted UNCONDITIONALLY (not inside the per-stream
    # block below): every shape has a CLOCK_DOMAIN, and the two facts the RTL
    # needs about it - how many sources exist, and which one is the CRF - were
    # hardcoded as "3" and "2" until 0x0042. Those literals are only right for
    # a 1-listener shape: the CLOCK_SOURCE set is internal, then ONE PER AAF
    # LISTENER, then CRF, so an 8-listener shape has 10 sources with CRF at 9.
    # A controller could not select the CRF clock there, and the servo would
    # have engaged on "Stream Clock 1" instead. Derive, never mirror.
    _n_cs, _crf_ix = M["N_CLKSRC"], M["CRF_CLKSRC"]
    a("// CLOCK_SOURCE set: count, and the index of the CRF source")
    a("// (AEM_CRF_CLKSRC_C = 16'hFFFF when this shape declares no CRF source)")
    a(f"localparam int unsigned AEM_N_CLKSRC_C = {_n_cs};")
    a(f"localparam [15:0] AEM_CRF_CLKSRC_C = 16'd{_crf_ix};"
      if _crf_ix is not None else
      "localparam [15:0] AEM_CRF_CLKSRC_C = 16'hFFFF;")
    a("")
    a(f"localparam int AEM_RATES_N_C = {len(M['RATES'])};")
    a(f"localparam [31:0] AEM_RATES_C [0:{len(M['RATES'])-1}] = "
      "'{" + ", ".join(f"32'h{r:08X}" for r in M["RATES"]) + "};")
    a(f"localparam [63:0] AEM_FMTS_C  [0:{len(M['FORMATS'])-1}] = "
      "'{" + ", ".join(f"64'h{f:016X}" for f in M["FORMATS"]) + "};")
    a(f"localparam [63:0] AEM_CRF_FMTS_C [0:{len(M['CRF_FMTS'])-1}] = "
      "'{" + ", ".join(f"64'h{f:016X}" for f in M["CRF_FMTS"]) + "};")
    a("")
    ps = M["PER_STREAM"]
    if ps["EMIT"]:
        n_in, n_out = len(ps["IN_FMT0"]), len(ps["OUT_FMT0"])
        a("// Per-descriptor stream-format tables (multi-stream shapes only:")
        a("// the deployed 1-AAF-in/1-out shape keeps the legacy layout above")
        a("// byte-identical; KL_aecp_response_builder switches on this define)")
        a("`define AEM_PER_STREAM_FMT")
        a(f"localparam int unsigned AEM_N_STRIN_C  = {n_in};")
        a(f"localparam int unsigned AEM_N_STROUT_C = {n_out};")
        a(f"localparam bit AEM_STRIN_CRF_C [0:{n_in-1}] = "
          "'{" + ", ".join("1'b1" if c else "1'b0" for c in ps["IN_CRF"])
          + "};")
        a(f"localparam [63:0] AEM_STRIN_FMT_C [0:{n_in-1}] = "
          "'{" + ", ".join(f"64'h{f:016X}" for f in ps["IN_FMT0"]) + "};")
        a(f"localparam [63:0] AEM_STROUT_FMT_C [0:{n_out-1}] = "
          "'{" + ", ".join(f"64'h{f:016X}" for f in ps["OUT_FMT0"]) + "};")
        a(f"localparam [15:0] WB_STRIN_FMT_ADDR_C [0:{n_in-1}] = "
          "'{" + ", ".join(f"16'd{v}" for v in ps["IN_WB"]) + "};")
        a(f"localparam [15:0] WB_STROUT_FMT_ADDR_C [0:{n_out-1}] = "
          "'{" + ", ".join(f"16'd{v}" for v in ps["OUT_WB"]) + "};")
        a(f"localparam [15:0] WB_STRIN_FMT_CRF_C = 16'd{ps['IN_WB'][-1]};"
          "  // the CRF sink = the LAST STREAM_INPUT (Table 5.22 push arm)")
        a("")
    sm = M["SMAP"]
    a("// Static AUDIO_MAP serving tables (GET_AUDIO_MAP, 1722.1-2021 7.4.44).")
    a("// Per STREAM_PORT: the ROM address of the AUDIO_MAP that port's OWN")
    a("// base_map names, THAT descriptor's own number_of_mappings, and its")
    a("// own mappings_offset - because 7.2.19 says the mappings field \"shall")
    a("// be accessed by using the mappings_offset field\". All three used to")
    a("// be hardcoded in the RTL (descriptor index 1, 8 mappings, offset 8,")
    a("// 64 bytes), which on an 8x8 shape served STREAM_PORT_INPUT[1]'s")
    a("// 72-byte map to STREAM_PORT_OUTPUT[0] and read 48 B past its")
    a("// 24-byte one. ROWS = 0 marks a port with no static map - 7.2.13:")
    a("// \"These Entities set the number_of_maps field to zero (0) and the")
    a("// base_map field is ignored when read.\" On a STREAM_PORT_OUTPUT that")
    a("// DOES have a map, ROWS != 0 is also the condition under which Milan")
    a("// v1.2 5.4.2.26 requires NOT_SUPPORTED rather than a served map.")
    a(f"localparam int unsigned AEM_SMAP_IN_N_C  = {sm['IN_N']};")
    a(f"localparam int unsigned AEM_SMAP_OUT_N_C = {sm['OUT_N']};")
    for nm in ("IN_ADDR", "IN_ROWS", "IN_MOFF",
               "OUT_ADDR", "OUT_ROWS", "OUT_MOFF"):
        v = sm[nm]
        a(f"localparam [15:0] AEM_SMAP_{nm}_C [0:{len(v)-1}] = "
          "'{" + ", ".join(f"16'd{x}" for x in v) + "};")
    a("")
    dm = M["DYNMAP"]
    if dm["EMIT"]:
        def arr(t, name, vals, fmt=None):
            if fmt is None:
                fmt = (lambda v: f"32'd{v}") if t == "[31:0]" else str
            a(f"localparam {t} {name} [0:{len(vals)-1}] = "
              "'{" + ", ".join(fmt(v) for v in vals) + "};")

        a("// Dynamic audio-map engine (gaps item 8, roadmap 23): every")
        a("// map_mode-dynamic STREAM_PORT_INPUT carries no AUDIO_MAP")
        a("// descriptor and advertises number_of_maps=0 (1722.1-2021")
        a("// 7.2.13); ADD/REMOVE/GET are served by the RTL mappings store")
        a("// per Milan 5.4.2.26-28. Fully static shapes never emit this.")
        a("// The store key is the GLOBAL cluster index (PBASE + offset) =")
        a("// the render crossbar map-RAM address.")
        a("`define AEM_DYNMAP")
        a(f"localparam int unsigned AEM_DMAP_KEYS_C  = {dm['KEYS']};"
          "   // global dynamic cluster keys (mono clusters)")
        a(f"localparam int unsigned AEM_DMAP_PAGE_C  = {dm['PAGE']};"
          "   // GET_AUDIO_MAP fixed partition size (shared)")
        #: A-F13: the GET page scan writes 6 + 8*PAGE bytes into an 80-byte
        #: const scratch, so PAGE > 9 would run off the end of const_q at
        #: RUNTIME. Codegen already refuses it; this makes a hand-edited svh
        #: die at ELABORATION instead, which is the only place left to catch
        #: it once the file is on disk.
        #: ONE string literal: SystemVerilog has no C-style adjacent
        #: string-literal concatenation, so a split message is a syntax error.
        a("if (AEM_DMAP_PAGE_C > 9) $error(\"AEM_DMAP_PAGE_C %0d exceeds "
          "the GET_AUDIO_MAP const-scratch bound of 9 (8*PAGE + 5 <= 79)\","
          " AEM_DMAP_PAGE_C);")
        a(f"localparam int unsigned AEM_DMAP_PHYS_C  = {dm['PHYS']};"
          "   // render crossbar depth (CHMAP_PHYS_C)")
        a(f"localparam int unsigned AEM_DMAP_NPORTS_C = {dm['NPORTS']};"
          "   // STREAM_PORT_INPUT descriptors")
        arr("bit", "AEM_DMAP_PDYN_C", dm["PDYN"],
            lambda v: "1'b1" if v else "1'b0")
        arr("[31:0]", "AEM_DMAP_PBASE_C", dm["PBASE"])
        arr("[31:0]", "AEM_DMAP_PCLS_C", dm["PCLS"])
        arr("[31:0]", "AEM_DMAP_PNMAPS_C", dm["PNMAPS"])
        a("// A STATIC port (input or output) is served from the shared")
        a("// AEM_SMAP_* tables above - one generated source for \"what map")
        a("// does this port serve\", static and dynamic shapes alike.")
        a("// Per-STREAM_INPUT mappability + reset channel count: a mapping")
        a("// names any STREAM_INPUT (Table 7-33) and 5.4.2.27 rejects a")
        a("// channel absent from THAT stream's current format.")
        a(f"localparam int unsigned AEM_DMAP_NSTRIN_C = {dm['NSTRIN']};")
        arr("bit", "AEM_DMAP_SAAF_C", dm["SAAF"],
            lambda v: "1'b1" if v else "1'b0")
        arr("[9:0]", "AEM_DMAP_SCH_C", dm["SCH"], lambda v: f"10'd{v}")
        a("")
    od = M.get("ODMAP", {"EMIT": False})
    if od["EMIT"]:
        a("// Talker-side dynamic audio-map engine (USER 08-01). Key = the")
        a("// port's STREAM channel (8 per port, ch[2:0] fabric bound);")
        a("// Milan 5.4.2.26's output partition is over Stream Output")
        a("// channels, <= 8, so number_of_maps is 1 for every port.")
        a("// CSRC = per-output-cluster capture-source template")
        a("// {valid, half, src[2:0], idxh[3:0], idx[3:0]}; INIT = the")
        a("// power-on identity image per key {v, cluster_offset[4:0]}.")
        a("`define AEM_ODYNMAP")
        a(f"localparam int unsigned AEM_ODMAP_KEYS_C   = {od['KEYS']};")
        a(f"localparam int unsigned AEM_ODMAP_NPORTS_C = {od['NPORTS']};")
        arr("bit", "AEM_ODMAP_PDYN_C", od["PDYN"],
            lambda v: "1'b1" if v else "1'b0")
        arr("[31:0]", "AEM_ODMAP_PCLS_C", od["PCLS"])
        arr("[31:0]", "AEM_ODMAP_PCBASE_C", od["PCBASE"])
        arr("[31:0]", "AEM_ODMAP_PSTR_C", od["PSTR"])
        arr("[31:0]", "AEM_ODMAP_SLOTB_C", od["SLOTB"])
        arr("[9:0]", "AEM_ODMAP_SCH_C", od["SCH"], lambda v: f"10'd{v}")
        arr("[12:0]", "AEM_ODMAP_CSRC_C", od["CSRC"],
            lambda s: "13'h{:04X}".format(
                ((1 if s.get("valid", True) else 0) << 12)
                | ((s.get("half", 0) & 1) << 11)
                | ((s["src"] & 7) << 8)
                | ((s.get("idxh", 0) & 0xF) << 4)
                | (s.get("idx", 0) & 0xF)))
        arr("[5:0]", "AEM_ODMAP_INIT_C", od["INIT"],
            lambda e: "6'h{:02X}".format(
                ((1 if e["v"] else 0) << 5) | (e["co"] & 0x1F)))
        a("")
    return "\n".join(lines)

# emit_c_golden() is GONE (2026-08-12).  It wrote tb/verilator/aecp/aem_golden.h,
# the byte-exact image the aecp Verilator suite compared the RTL against; that
# suite and the RTL it exercised are both deleted, so the emitter had exactly
# zero consumers left.  Kept as a note rather than as dead code: a golden image
# with no harness is a file that goes stale silently and then gets believed.

def emit_json(M, path):
    with open(path, "w") as f:
        json.dump({
            "rom_hex": M["rom"].hex(),
            "directory": [
                {"type": t, "index": i, "base": b, "len": l}
                for (t, i, b, l) in M["directory"]],
            "overlays": [
                {"addr": a_, "bytes": n, "source": s}
                for (a_, n, s) in M["OVERLAYS"]],
            "writeback": M["WB"],
            "named": [
                {"type": t, "index": i, "name_index": n, "addr": a_}
                for (t, i, n, a_) in M["NAMED"]],
            "rates": M["RATES"],
            "formats": M["FORMATS"],
            "crf_formats": M["CRF_FMTS"],
        }, f, indent=1)

def self_test():
    """Negative control for the AUDIO_MAP bounds gate (methodology R2: a check
    that cannot fail is not a check). Every vector below is a model that used
    to build silently, and the deployed model passing is not evidence that the
    gate bites - only a refused model is."""
    ok = [True]

    def refuses(name, mutate):
        spec = builtin_spec()
        mutate(spec)
        try:
            build_model(spec)
        except ValueError as e:
            print(f"  [ok  ] {name}\n         -> {str(e)[:150]}")
            return
        ok[0] = False
        print(f"  [FAIL] {name}: built without complaint")

    def accepts(name, mutate=lambda s: None):
        spec = builtin_spec()
        mutate(spec)
        try:
            build_model(spec)
            print(f"  [ok  ] {name}")
        except ValueError as e:
            ok[0] = False
            print(f"  [FAIL] {name}: refused - {e}")

    print("=== gen_aem_store AUDIO_MAP bounds gate self-test ===")
    # POSITIVE control first: the gate must not refuse what ships.
    accepts("the deployed model still builds")

    def global_index(s):
        #! THE defect A shape at the model tier: a global AUDIO_CLUSTER index
        #! written where 7.2.19 wants an offset from the port's base_cluster.
        #! The output port's clusters are 8..15 globally and 0..7 relative.
        s["audio_maps"][1] = [[0, c, 8 + c, 0] for c in range(8)]
    refuses("global cluster index where 7.2.19 wants a port-relative offset",
            global_index)
    refuses("base_map naming an AUDIO_MAP the model does not define",
            lambda s: s["ports_out"][0].update(base_map=7))
    refuses("number_of_maps != 1 on a static port (pages it cannot answer)",
            lambda s: s["ports_out"][0].update(maps=2))
    refuses("cluster_channel past the cluster's channel_count (7.2.16)",
            lambda s: s["audio_maps"][0].__setitem__(0, [0, 0, 0, 1]))
    refuses("stream_index past the descriptors this direction has (7.2.13)",
            lambda s: s["audio_maps"][0].__setitem__(0, [9, 0, 0, 0]))
    refuses("INPUT: two mappings onto the SAME cluster channel (7.2.19)",
            lambda s: s["audio_maps"][0].__setitem__(1, [0, 0, 0, 0]))
    refuses("a mapping onto the CRF sink, which carries no audio channels",
            lambda s: s["audio_maps"][0].__setitem__(0, [1, 0, 0, 0]))
    #! 7.2.19's two directions are DIFFERENT rules, and this pair is the
    #! negative control for that: the first version of this gate applied the
    #! INPUT rule to both and would have refused the second model, which the
    #! OUTPUT paragraph explicitly permits.
    refuses("OUTPUT: the same (stream_index, stream_channel) twice (7.2.19 "
            "\"across the entire Configuration\")",
            lambda s: s["audio_maps"].__setitem__(
                1, [[0, 0, 0, 0], [0, 0, 1, 0]]))
    accepts("OUTPUT: the same cluster_offset twice IS allowed (7.2.19 "
            "\"there may be multiple entries for each mapping_cluster_"
            "offset\")",
            lambda s: s["audio_maps"].__setitem__(
                1, [[0, 0, 0, 0], [0, 1, 0, 0]]))
    refuses("more mappings in one AUDIO_MAP than Table 7-32 allows (62)",
            lambda s: s["audio_maps"].__setitem__(
                0, [[0, c % 8, c, 0] for c in range(63)]))

    # ...and the recorded deviation is exactly the recorded one, no more.
    M = build_model(builtin_spec())
    got = M["SMAP"]["DEVIATIONS"]
    try:
        assert_no_map_deviations(M)
        print(f"  [ok  ] the {len(got)} open stream_channel deviation(s) are "
              "exactly the recorded ones")
    except ValueError as e:
        ok[0] = False
        print(f"  [FAIL] a NEW deviation appeared: {e}")
    # ...and that allowlist is not vacuous either: drop it and it must fail.
    try:
        assert_no_map_deviations(M, allow=set())
        ok[0] = False
        print("  [FAIL] the deviation allowlist is not asserting anything")
    except ValueError:
        print("  [ok  ] with an empty allowlist the deviation FAILS "
              "(the list is load-bearing)")

    # Two-level directory gate: every vector is a layout the direct-indexed
    # accessor would silently mis-serve, so each MUST be a refusal (a check
    # that cannot fail is not a check).
    print("\n=== two-level directory gate self-test ===")

    def dir_refuses(name, tamper):
        d = list(build_model(builtin_spec())["directory"])
        tamper(d)
        try:
            l1t = two_level_directory(d)
            check_two_level(l1t, d)
        except ValueError as e:
            print(f"  [ok  ] {name}\n         -> {str(e)[:150]}")
            return
        ok[0] = False
        print(f"  [FAIL] {name}: accepted without complaint")

    def swap(d, x, y):
        d[x], d[y] = d[y], d[x]
    # row 0 is ENTITY, rows 3/4 the STREAM_INPUT run: parking SI[0] at row 0
    # splits that run around the descriptors between them
    dir_refuses("a shuffled directory entry (contiguity)",
                lambda d: swap(d, 0, 3))
    # STREAM_INPUT[0]/[1] swapped: contiguous but not ascending
    dir_refuses("same-type entries out of index order",
                lambda d: swap(d, 3, 4))
    # ...and the equivalence check itself bites on a corrupt level-1 row
    # base even when the directory is pristine (the "shuffle one entry"
    # bite at the TABLE tier)
    Mtl = build_model(builtin_spec())
    l1b = dict(Mtl["L1"], ROW=list(Mtl["L1"]["ROW"]))
    l1b["ROW"][STREAM_INPUT] += 1
    try:
        check_two_level(l1b, Mtl["directory"])
        ok[0] = False
        print("  [FAIL] an off-by-one level-1 row base was accepted")
    except ValueError as e:
        print(f"  [ok  ] an off-by-one level-1 row base is refused\n"
              f"         -> {str(e)[:150]}")
    # name split: a mask bit on an unnamed type claims names that do not
    # exist - the 1:1 gate must catch it
    try:
        check_named(Mtl["L1"], Mtl["directory"], Mtl["NAMED"],
                    Mtl["NAME_MASK"] | (1 << STRINGS), Mtl["NAME_EXC"])
        ok[0] = False
        print("  [FAIL] a mask bit on the unnamed STRINGS type was accepted")
    except ValueError as e:
        print(f"  [ok  ] a mask bit on an unnamed type is refused\n"
              f"         -> {str(e)[:150]}")

    # Milan v1.2 6.4 over the BUILTIN model's own FORMATS constant, which no
    # config and no overlay reaches: the config-driven path has its family
    # derived (endstation_builder.base_format_complete) and gated by
    # test_builder gate 29, so the constants in this file are the one
    # advertised formats list in the tree with no owner but this check.
    print("\n=== Milan 6.4 Base format family (builtin model) ===")
    for label, fmts in (("FORMATS (STREAM_INPUT)", FORMATS),):
        missing = sorted(set(MILAN_BASE_CHANNELS) - base_channel_cover(fmts))
        if missing:
            ok[0] = False
            print(f"  [FAIL] {label}: 48 kHz Base channel count(s) {missing} "
                  f"unadvertised - Milan 6.4 wants the whole family")
        else:
            print(f"  [ok  ] {label}: all {len(MILAN_BASE_CHANNELS)} 48 kHz "
                  f"Base channel counts {list(MILAN_BASE_CHANNELS)} covered "
                  f"by {len(fmts)} entries (6.5's ut string does the family)")
    # negative control: the ut entry is what carries the family, so dropping
    # it must be REPORTED and not shrugged at
    short = sorted(set(MILAN_BASE_CHANNELS) - base_channel_cover(FORMATS[:1]))
    if short:
        print(f"  [ok  ] without the ut entry the family check REPORTS "
              f"{short} missing")
    else:
        ok[0] = False
        print("  [FAIL] the family check passes without the ut entry - it has "
              "stopped being able to say no")

    print("\ngen_aem_store self-test:", "PASS" if ok[0] else "FAIL")
    return 0 if ok[0] else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="generate the HW AEM descriptor store")
    ap.add_argument("--self-test", action="store_true",
                    help="prove the AUDIO_MAP bounds gate refuses "
                         "out-of-bounds models, and exit (no files written)")
    ap.add_argument("--overlay", default=None,
                    help="build the model from a builder-emitted "
                         "aem_overlay.json instead of the builtin shape")
    ap.add_argument("--out-dir", default=None,
                    help="write aecp_aem_rom.svh + aem_rom.json into this "
                         "SCRATCH directory instead of avdecc/aem_rom.json. "
                         "Nothing is installed into an RTL tree: the AEM plane "
                         "this ROM described is deleted (see the module "
                         "docstring), so the .svh is a readable rendering of "
                         "the declarative model, not a build input")
    args = ap.parse_args()
    if args.self_test:
        raise SystemExit(self_test())
    if args.overlay:
        with open(args.overlay) as f:
            M = build_model(spec_from_overlay(json.load(f)))
    else:
        M = _M
    # The tracked-RTL destinations (hdl/ieee17221/aecp/gen/aecp_aem_rom.svh and
    # tb/verilator/aecp/aem_golden.h) are DELETED along with the plane that
    # compiled them.  Only --out-dir renders the .svh now, and only into a
    # directory the caller names.
    if args.out_dir:
        os.makedirs(args.out_dir, exist_ok=True)
        p_svh = os.path.join(args.out_dir, "aecp_aem_rom.svh")
        p_json = os.path.join(args.out_dir, "aem_rom.json")
        emit_svh(M, p_svh)
    else:
        p_json = os.path.join(HERE, "aem_rom.json")
    emit_json(M, p_json)
    print(f"[gen_aem_store] {len(M['directory'])} descriptors, "
          f"ROM {M['ROM_SIZE']} B"
          + (f" (overlay {args.overlay})" if args.overlay else "")
          + (f" -> {args.out_dir}" if args.out_dir
             else " -> avdecc/aem_rom.json (no RTL target: the AEM plane is "
                  "deleted)"))
    for t, i, b, l in M["directory"]:
        print(f"  type 0x{t:04X} idx {i}: base {b:4d} len {l}")
