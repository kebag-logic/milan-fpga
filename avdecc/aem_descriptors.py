#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Descriptor BYTES: the IEEE 1722.1-2021 clause 7.2 field layouts.

Split out of `gen_aem_store.py` when that module passed a thousand lines
(Rule 12 in docs/development/CODE_QUALITY.md). The seam is what the code
PRODUCES: everything here turns a handful of numbers into the exact octets
one descriptor occupies, and nothing here knows what a model is, how
descriptors are ordered in the ROM, or how any of it is rendered.

It also owns the gateware version the ENTITY descriptor carries, because
`firmware_version_string()` is the value of a Table 7-2 FIELD and belongs
with the layout that places it, not with the assembly that calls it.

`gen_aem_store` re-exports every name here, so an importer that has always
said `gen_aem_store.d_entity` or `gen_aem_store.FORMATS` still gets it.
"""
import dataclasses
import re
import struct
from collections.abc import Sequence
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

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
#: defect as the ADP shape registers (docs/ENDSTATION_BUILDER.md):
#: a hand-typed declaration that no gate could compare against the fabric.
MILAN_CSR_SV = ROOT / "hdl/common/csr/milan_csr.sv"

_VERSION_RE = re.compile(
    r"parameter\s+logic\s*\[31:0\]\s+VERSION\s*=\s*32'h([0-9A-Fa-f_]+)")


def rtl_version(path: str | Path | None = None) -> tuple[int, int]:
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
    src = Path(path) if path else MILAN_CSR_SV
    m = _VERSION_RE.search(src.read_text())
    if not m:
        raise ValueError(
            f"{src}: no `parameter logic [31:0] VERSION = 32'h...` - the "
            "gateware version has no single source of truth any more")
    v = int(m.group(1).replace("_", ""), 16)
    return (v >> 16) & 0xFFFF, v & 0xFFFF


def firmware_version_string(rev: int = 0,
                            path: str | Path | None = None) -> str:
    """The ENTITY descriptor's firmware_version value: `major.minor.rev`.

    IEEE 1722.1-2021 7.2.1 Table 7-2 offset 116: "64-octet UTF-8 string
    containing the firmware version of the ATDECC Entity" - the standard
    fixes the size and the encoding and says nothing about the syntax, and
    Milan compliance tooling (enumeration checks) reads the
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
# AAF PCM 32-bit 8ch stream formats for the compatibility model
#! 8ch default restored (2026-07-20, the internal compliance suite expects the classic
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
#! 2ch-first: an
#! 8ch default + reboot + pure-ACMP bind starved the render at 1/4 rate);
#! the ut entry keeps the full Milan 6.4 1..8ch family coverage.
FORMATS = [0x0205022000806000, 0x0215022002006000]
#! talker truth (2026-07-18): the framer is a STEREO 48k device (Pmod I2S2 /
#! tone path both 2ch, fs fixed by the divider chain) - STREAM_OUTPUT must
#! DECLARE exactly what the wire carries or format-matching controllers
#! strand every listener (user bugs 5/6)
OUT_FORMATS = [0x0205022000806000]
# CRF AUDIO_SAMPLE media-clock format for the compatibility model
#! 48k only (the CRF engine validates base 48000/pull 0 - advertising
#! unlockable rates is the same honesty violation)
CRF_FORMATS = [0x041060010000BB80]
# IDENTIFY control (byte-exact)
CTRL_TYPE_IDENTIFY = 0x90E0F00000000001
CTRL_LINEAR_UINT8 = 0x0001

def cstr(s: str, n: int = 64) -> bytes:
    """A fixed-size AEM string field: UTF-8, truncated at `n`, zero-padded.

    1722.1-2021 7.2: "The 64-octet strings do not include the NULL terminator
    when they are 64-octets long. If the string is shorter than 64-octets then
    the remainder of the field shall be zero (0) padded." Truncation is on the
    ENCODED bytes, so an over-long name shortens the field rather than
    overrunning the descriptor and moving every field after it.
    """
    b = s.encode()[: n]
    return b + bytes(n - len(b))


def be16(v: int) -> bytes:
    """`v` as the two-octet network-order field every AEM u16 is on the wire."""
    return struct.pack(">H", v & 0xFFFF)


def be32(v: int) -> bytes:
    """`v` as the four-octet network-order field every AEM u32 is on the wire."""
    return struct.pack(">I", v & 0xFFFFFFFF)


def be64(v: int) -> bytes:
    """`v` as the eight-octet network-order field every AEM u64 is on the wire."""
    return struct.pack(">Q", v & 0xFFFFFFFFFFFFFFFF)


def d_entity(e: dict[str, str]) -> bytes:
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

def d_configuration(n_inputs: int, n_outputs: int, n_clk_sources: int) -> bytes:
    """CONFIGURATION descriptor (7.2.2): the top-level descriptor_counts list.

    These counts are what a controller enumerates the tree from, so a type
    missing here is a subtree it never reads however complete the ROM is.
    """
    # Top-level compatibility-model counts. STREAM_PORT, AUDIO_CLUSTER,
    # AUDIO_MAP, and STRINGS are reached through their parents.
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

def d_audio_unit(rates: list[int], current_rate: int, n_in_ports: int,
                 n_out_ports: int) -> bytes:
    """AUDIO_UNIT descriptor (7.2.3): the sampling rates this unit offers.

    `rates` are Table 7-5 encoded words (pull 0, so the word IS the Hz value)
    and `current_rate` is the one SET_SAMPLING_RATE currently selects; it is
    written verbatim, so a rate absent from `rates` would advertise a state no
    controller could ask for.
    """
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

def d_stream(dtype: int, index: int, name: str, flags: int,
             formats: list[int], buffer_len: int = 0) -> bytes:
    """STREAM_INPUT/STREAM_OUTPUT descriptor in the 1722.1-**2021** layout.

    `dtype` picks the direction and `formats[0]` becomes current_format. The
    2021 layout is not interchangeable with 2013's: see the CONSTRAINT note
    below on why emitting the older one hands a 2021 controller the first two
    octets of formats[0] as `timing`.
    """
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

def d_avb_interface(gp: dict[str, int] | None = None) -> bytes:
    """gp = the builder-RESOLVED `gptp:` dataset (overlay key "gptp").
    Since [R-parallel] on #228 the builder derives every field the fabric
    engine does not consume (priority2, clockQuality, the log intervals)
    from the constants in gptp-processor/hdl/ucode/gen_gptp_ucode.py and
    refuses a config that states anything else, so these bytes are the
    wire Announce dataset, not a free claim. Absent (legacy overlays /
    builtin spec) keeps the historical constants BYTE-EXACTLY:
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

def clock_source_shape(
        clock_sources: Sequence[dict[str, Any]]) -> tuple[int, int | None]:
    """The two CLOCK_SOURCE facts the RTL needs: (count, CRF index or None).

    One rule for every emitter. The model's spec rows carry the config type
    under 'raw_type' (cs_type is already the 1722.1 encoding, where CRF and
    INPUT_STREAM are both 0x0002 and cannot be told apart); the builder's
    overlay rows carry it under 'type'. Both name the CRF row "crf". The
    generator banner above AEM_N_CLKSRC_C records why this is derived and
    never mirrored: the literals "3"/"2" were only right for a 1-listener
    shape (an 8-listener shape has 10 sources with CRF at 9)."""
    crf_ix = next((i for i, c in enumerate(clock_sources)
                   if c.get("raw_type", c.get("type")) == "crf"), None)
    return len(clock_sources), crf_ix


def d_clock_source(index: int, name: str, cs_type: int, loc_type: int,
                   loc_index: int) -> bytes:
    """CLOCK_SOURCE descriptor (7.2.9): one selectable media-clock reference.

    `cs_type` is the 1722.1 encoding (INTERNAL=0 / INPUT_STREAM=2), which is
    why CRF and a stream clock are indistinguishable here and the config's own
    word has to travel separately - see clock_source_shape().
    """
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

def d_clock_domain(n_sources: int) -> bytes:
    """CLOCK_DOMAIN descriptor (7.2.32) listing sources 0..n_sources-1.

    The list is the identity permutation on purpose: clock_sources_offset
    entries are CLOCK_SOURCE descriptor indices, and this model defines them
    densely, so the domain can select any of them by its own index.
    """
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

def d_control_identify() -> bytes:
    """The IDENTIFY CONTROL descriptor (7.2.22), byte-exact.

    signal_type/index are INVALID/zero because 7.2.22 says so for a control
    that acts on no signal: IDENTIFY acts on the PAAD. Its parent is the
    CONFIGURATION, never the AVB_INTERFACE - see d_avb_interface().
    """
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

def d_locale() -> bytes:
    """The single LOCALE descriptor (7.2.11): en-EN, one STRINGS child."""
    b = be16(LOCALE) + be16(0)
    b += cstr("en-EN")                  # locale_identifier
    b += be16(1)                        # number_of_strings (STRINGS descriptors)
    b += be16(0)                        # base_strings
    assert len(b) == 72
    return b

def d_strings(strs: Sequence[str]) -> bytes:
    """STRINGS descriptor (7.2.12): the seven localized strings, 64 B each.

    Seven is the descriptor's fixed width, not this model's choice, so the
    assert is what stops a caller silently shortening every string index the
    other descriptors reference by localized_description.
    """
    assert len(strs) == 7
    b = be16(STRINGS) + be16(0)
    for s in strs:
        b += cstr(s)
    assert len(b) == 452
    return b

@dataclasses.dataclass(frozen=True)
class PortMapBounds:
    """The four 7.2.13 fields that say what a STREAM_PORT owns.

    They travel together everywhere - a cluster run (`clusters` from
    `base_cluster`) and a map run (`maps` from `base_map`) - and each pair is
    meaningless without its other half, so they are ONE argument. A dynamic
    port passes maps=0, base_map=0: 7.2.13 "These Entities set the
    number_of_maps field to zero (0) and the base_map field is ignored".
    """
    clusters: int
    base_cluster: int
    maps: int
    base_map: int


def d_stream_port(dtype: int, index: int, flags: int,
                  bounds: PortMapBounds) -> bytes:
    """STREAM_PORT_INPUT/OUTPUT descriptor (7.2.13), 20 octets.

    Everything a controller needs to address this port's clusters and maps is
    in `bounds`; the two runs it names are what static_map_tables() checks
    every AUDIO_MAP mapping against.
    """
    b = be16(dtype) + be16(index)
    b += be16(0)                        # clock_domain_index
    b += be16(flags)                    # port_flags
    b += be16(0) + be16(0)              # controls
    b += be16(bounds.clusters) + be16(bounds.base_cluster)
    b += be16(bounds.maps) + be16(bounds.base_map)
    assert len(b) == 20
    return b

def d_audio_cluster(index: int, name: str, signal_type: int) -> bytes:
    """AUDIO_CLUSTER descriptor (7.2.16) in the 2021 90-octet layout.

    channel_count is fixed at 1 for every cluster this model emits, which is
    the bound SMAP_CLUSTER_CHANNELS records for the map gate. The two
    aes3_* fields past offset 86 are 2021's, not padding - see the note below
    on why truncating to the 2013 length was a compliance defect.
    """
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

def d_audio_map(index: int, rows: Sequence[Sequence[int]]) -> bytes:
    """AUDIO_MAP descriptor (7.2.19): `rows` as `(stream, ch, offset, ch)`.

    cluster_offset is PORT-RELATIVE (Table 7-33), so the same row means a
    different global cluster on a different port; static_map_tables() is what
    bounds it against the owning port rather than against the model.
    """
    b = be16(AUDIO_MAP) + be16(index)
    b += be16(8)                        # mappings_offset (fixed, from desc start)
    b += be16(len(rows))
    assert len(b) == 8
    for (stream, ch, cluster_off, cluster_ch) in rows:
        # cluster_offset RELATIVE to the owning port's base_cluster
        # (1722.1-2021 7.2.19)
        b += be16(stream) + be16(ch) + be16(cluster_off) + be16(cluster_ch)
    return b
