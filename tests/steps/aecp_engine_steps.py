# SPDX-FileCopyrightText: 2026 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Steps for aecp_read_descriptor.feature and aecp_response_contract.feature -
# the AECP answers this device really gives again.
#
# WHY THIS EXISTS AGAIN.  On 2026-08-12 this repository's own AECP/AEM RTL was
# deleted and the whole AECP tier of this suite went with it, on the premise
# "this device answers no AECP command at all".  That premise expired when the
# protocol-processor submodule landed its AECP uCPU. The device serves the
# inventory gated below against the RTL opcode table, applies command-specific
# refusals, and returns a conformant NOT_IMPLEMENTED response for the remainder.
# These steps cover that offline response contract, and only that.
#
# WHAT THIS LAYER IS.  An OFFLINE model, in the manner of the rest of the
# suite (tests/README.md T1): a Python mirror of the shipped command path -
# the dispatch decision, the modeled response forms, the response
# builder and the frame assembler - which emits a WHOLE Ethernet frame.  Every
# Then decodes that frame.  Nothing here talks to RTL, a simulator or a DUT,
# and nothing asserts a status that did not come out of the model.
#
# WHAT THIS LAYER CANNOT PROVE.  That the gateware matches this model.  The
# model is written FROM the submodule sources named below and re-derives their
# arithmetic rather than restating their outputs, so it catches a change in
# intent, a mis-stated clause and a drifting conformance claim - not a Verilog
# typo.  The submodule owns its own benches for that (its tb/ucpu, tb/pp_top);
# testing through them is explicitly not this suite's job.
#
# Sources mirrored (READ-ONLY, never edited from here):
#   protocol-processor/hdl/aecp/KL_aecp_engine.sv     dispatch, echo pre-load,
#                                                     header synthesis, drops
#   protocol-processor/hdl/aecp/ucode/gen_ucode.py    E_RDESC / E_RDSTUB /
#                                                     E_NOTIMPL / E_BADARG
#   protocol-processor/hdl/aecp/KL_aecp_ucpu.sv       status semantics
#   protocol-processor/hdl/aecp/KL_aecp_desc_store.sv locate, region 0xD
#   protocol-processor/hdl/aecp/desc/example_milan_8.json  the image shape
#   protocol-processor/docs/architecture/06_aecp_engine.md F06.14 master table
#
# Clauses used:
#   IEEE 1722.1-2021 7.4.5    - READ_DESCRIPTOR; "On failure the descriptor
#                               field is four octets in length, and contains
#                               the descriptor_type and descriptor_index.
#                               These are in the same location as in the
#                               command frame."  Reading is permitted even
#                               when the Entity is locked or acquired.
#   IEEE 1722.1-2021 7.4.39.2 - "IDENTIFY_NOTIFICATION is only ever sent as an
#                               unsolicited response ... If an ATDECC Entity
#                               ever receives this as a command then it shall
#                               return a response with the status code
#                               BAD_ARGUMENTS."  Opcode-specific, so it wins
#                               over the 9.3.5.3.3 fallback.
#   IEEE 1722.1-2021 9.2.2    - AECPDU common header: h = 0, version = 0,
#                               message_type per Table 9-1, status/cdl split
#                               across octet 2, command_type at @22[5:0],@23
#                               under the u and cr bits.
#   IEEE 1722.1-2021 9.3.5.3.3- "Any command that is received and not
#                               implemented shall be responded to with a
#                               correctly sized response and a status of
#                               NOT_IMPLEMENTED."
#   IEEE 1722.1-2021 9.4.2.1  - ADDRESS_ACCESS AECPDU: tlv_count at @22,
#                               tlv_data from @24.
#   IEEE 1722.1-2021 9.2.1    - responses are unicast back to the Controller
#                               that sent the command.
#   Milan v1.2 Delta 7        - ACQUIRE_ENTITY never succeeds (NOT_SUPPORTED,
#                               owner_id 0).

import json
import os
import struct
import sys

from behave import given, when, then

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#! the submodule test vector this model's descriptor LENGTHS are taken from
DESC_VECTOR = os.path.join(ROOT, "protocol-processor", "hdl", "aecp", "desc",
                           "example_milan_8.json")

# ---------------------------------------------------------------------------
# AECP constants (IEEE 1722.1-2021 9.2, Table 9-1, Table 9-2)
# ---------------------------------------------------------------------------

ETHERTYPE_AVTP = 0x22F0
SUBTYPE_AECP = 0xFB

MT_AEM_COMMAND = 0
MT_AEM_RESPONSE = 1
MT_AA_COMMAND = 2
MT_AA_RESPONSE = 3
MT_VU_COMMAND = 6
MT_VU_RESPONSE = 7

ST_SUCCESS = 0
ST_NOT_IMPLEMENTED = 1
ST_NO_SUCH_DESCRIPTOR = 2
ST_BAD_ARGUMENTS = 7
ST_NOT_SUPPORTED = 11

OP_ACQUIRE_ENTITY = 0x0000
OP_READ_DESCRIPTOR = 0x0004
OP_IDENTIFY_NOTIFICATION = 0x0026

# ---- THE SERVED-OPCODE INVENTORY -------------------------------------------
# The one place this suite records which AECP opcodes the protocol processor
# answers for real, and the Milan v1.2 clause that makes each one a SHALL.
#
# WHY IT EXISTS: this file is an OFFLINE MODEL, so it can only ever be as
# current as somebody remembered to make it - and it was not. Between the
# 2026-08-13 substitution and 2026-08-16 the engine gained twelve commands
# while every scenario here went on asserting NOT_IMPLEMENTED for them, and
# the suite stayed 100 % green the whole time. A model that mirrors RTL fails
# silently in exactly one direction: the RTL moves and the model does not.
#
# So the inventory is GATED AGAINST THE RTL TEXT (see
# `step_inventory_matches_rtl`): the opcode constants in
# protocol-processor/hdl/aecp/KL_aecp_engine.sv are parsed and compared to
# the keys below. Add a command to the engine without adding it here and this
# suite goes RED - which is the only property that makes the table worth
# trusting. `verdict` is what a well-formed command for an EXISTING target
# draws; `cdl` is the response's control_data_length per the cited clause,
# which is the size law la_avdecc's checkResponsePayload enforces.
SERVED = {
    0x0000: dict(name="ACQUIRE_ENTITY", clause="Milan 5.4.2.1",
                 verdict=ST_NOT_SUPPORTED, cdl=28),
    0x0001: dict(name="LOCK_ENTITY", clause="Milan 5.4.2.2",
                 verdict=ST_SUCCESS, cdl=28),
    0x0002: dict(name="ENTITY_AVAILABLE", clause="Milan 5.4.2.3",
                 verdict=ST_SUCCESS, cdl=32),
    0x0004: dict(name="READ_DESCRIPTOR", clause="Milan 5.4.2.4",
                 verdict=ST_SUCCESS, cdl=None),   # 16 + descriptor length
    0x0006: dict(name="SET_CONFIGURATION", clause="Milan 5.4.2.5",
                 verdict=ST_SUCCESS, cdl=16),
    0x0007: dict(name="GET_CONFIGURATION", clause="Milan 5.4.2.6",
                 verdict=ST_SUCCESS, cdl=16),
    0x0009: dict(name="GET_STREAM_FORMAT", clause="Milan 5.4.2.8",
                 verdict=ST_SUCCESS, cdl=24),
    0x000F: dict(name="GET_STREAM_INFO", clause="Milan 5.4.2.10",
                 verdict=ST_SUCCESS, cdl=68),     # the Milan 80-byte form
    0x0015: dict(name="GET_SAMPLING_RATE", clause="Milan 5.4.2.14",
                 verdict=ST_SUCCESS, cdl=20),
    0x0014: dict(name="SET_SAMPLING_RATE", clause="Milan 5.4.2.13",
                 verdict=ST_SUCCESS, cdl=20),
    0x0016: dict(name="SET_CLOCK_SOURCE", clause="Milan 5.4.2.15",
                 verdict=ST_SUCCESS, cdl=20),
    0x0017: dict(name="GET_CLOCK_SOURCE", clause="Milan 5.4.2.16",
                 verdict=ST_SUCCESS, cdl=20),
    0x0018: dict(name="SET_CONTROL", clause="Milan 5.4.2.17",
                 verdict=ST_SUCCESS, cdl=17),     # one LINEAR_UINT8 value
    0x0019: dict(name="GET_CONTROL", clause="Milan 5.4.2.18",
                 verdict=ST_SUCCESS, cdl=17),
    0x0024: dict(name="REGISTER_UNSOLICITED_NOTIFICATION",
                 clause="Milan 5.4.2.21", verdict=ST_SUCCESS, cdl=16),
    0x0025: dict(name="DEREGISTER_UNSOLICITED_NOTIFICATION",
                 clause="Milan 5.4.2.22", verdict=ST_SUCCESS, cdl=12),
    0x0026: dict(name="IDENTIFY_NOTIFICATION", clause="IEEE 7.4.39.2",
                 verdict=ST_BAD_ARGUMENTS, cdl=None),  # echoed at command size
    0x0027: dict(name="GET_AVB_INFO", clause="Milan 5.4.2.23",
                 verdict=ST_SUCCESS, cdl=None),   # 32 + 4 x mappings
    0x0028: dict(name="GET_AS_PATH", clause="Milan 5.4.2.24",
                 verdict=ST_SUCCESS, cdl=None),   # 16 + 8 x count
    0x0029: dict(name="GET_COUNTERS", clause="Milan 5.4.2.25",
                 verdict=ST_SUCCESS, cdl=148),
    0x002B: dict(name="GET_AUDIO_MAP", clause="Milan 5.4.2.26",
                 verdict=ST_SUCCESS, cdl=None),   # 24 + 8 x mappings
}

#! the engine's own path to the RTL, resolved from this file so the gate works
#! from any working directory behave is launched in
_ENGINE_SV = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "protocol-processor", "hdl", "aecp", "KL_aecp_engine.sv")

#! Milan v1.2 vendor-unique protocol_id, on the wire at AECPDU @22..@27
MILAN_PROTOCOL_ID = bytes((0x00, 0x1B, 0xC5, 0x0A, 0xC1, 0x00))
MVU_GET_MILAN_INFO = 0x0000

# ---- geometry (KL_aecp_engine.sv localparams) ------------------------------
ETH_HDR = 14                       # ETH_HDR_C
AECP_HDR = 24                      # AECP_HDR_C
FRAME_HDR = ETH_HDR + AECP_HDR     # FRAME_HDR_C = 38
ETH_MIN = 60                       # ETH_MIN_C
LINE_BYTES = 576                   # LINE_BYTES_P: the longest servable descriptor
TX_STD_BYTES = 576                 # TX_STD_BYTES_P: above this needs the Delta 8 slot
RESP_BUF = ((16 + LINE_BYTES) + 15) & ~15   # RESP_BUF_C
PLD_MAX = RESP_BUF - 12                     # PLD_MAX_C

#! the identity of the worked example the submodule ships
ENTITY_ID = 0x001B92FFFE001122
OWN_MAC = bytes.fromhex("001b92001122")
CONTROLLER_MAC = bytes.fromhex("0203040506ff")
CONTROLLER_EID = 0x0011223344556677

# ---- descriptor types used here (IEEE 1722.1-2021 Table 7-1) ---------------
D_ENTITY = 0x0000
D_CONFIGURATION = 0x0001
D_AUDIO_UNIT = 0x0002
D_STREAM_INPUT = 0x0005
D_STREAM_OUTPUT = 0x0006
D_AVB_INTERFACE = 0x0009
D_CLOCK_SOURCE = 0x000A
D_CLOCK_DOMAIN = 0x0024


# ---------------------------------------------------------------------------
# the descriptor image + its index map (KL_aecp_desc_store.sv)
# ---------------------------------------------------------------------------

def _vector_lengths():
    """`(count, length)` per (configuration, type) as the VECTOR packs it.

    This is the agreement gate between the two fixtures, not the model's
    source.  This file's contract (see the header) is to re-derive the
    submodule's arithmetic rather than restate its outputs, so `MILAN_8`
    below writes the sizing out longhand; calling the packer to obtain it
    would make the model depend on the code it exists to check independently.
    What the packer IS good for is catching drift: two fixtures modelling one
    image and disagreeing about it is indefensible whichever layout they use,
    so the numbers are compared and a mismatch is fatal at import.

    The lengths come from `gen_desc_image.descriptor_bytes()` - the same
    function that writes tb/desc_store's image.bin - and `_type_code()`, its
    own type resolver, so this side of the comparison restates nothing
    either.  Returns None when the submodule is not checked out.
    """
    if not os.path.exists(DESC_VECTOR):
        return None
    desc_dir = os.path.dirname(DESC_VECTOR)
    if desc_dir not in sys.path:
        sys.path.insert(0, desc_dir)
    import gen_desc_image as gdi
    with open(DESC_VECTOR, encoding="utf-8") as fh:
        doc = json.load(fh)
    out = {}
    for d in doc["descriptors"]:
        key = (int(d.get("configuration", 0)), gdi._type_code(d["type"]))
        n = len(gdi.descriptor_bytes(d))
        count, length = out.get(key, (0, n))
        #! one (count, length) pair per type is all this model carries, so a
        #! vector whose members differ in length would collapse here.  The
        #! store itself does NOT have that limit (its index map splits such a
        #! type into runs, tb/desc_store S4), so say so rather than silently
        #! model something the RTL does not do.
        assert length == n, (
            "%s carries type 0x%04X at two lengths (%d and %d); this model "
            "holds one length per type" % (DESC_VECTOR, key[1], length, n))
        out[key] = (count + 1, n)
    return out


class DescriptorImage:
    """The static AEM image as the store sees it.

    Only three of the store's regions matter to the one microprogram that
    reads it: region 0xD (configurations_count), region 0xF (LOCATE) and
    region 0x0 (the located descriptor's bytes).  An image whose magic,
    layout version or checksum has not been validated reports NOTHING - the
    store answers 0 from region 0xD and a miss from every locate.
    """

    #! The docs/architecture/07 section 3.1 tree at one configuration, one in,
    #! one out, sized the way `desc/example_milan_8.json` sizes it.  Written
    #! longhand per this file's contract, then checked against that vector by
    #! `_vector_lengths()` at import: the two fixtures model one image, so a
    #! disagreement between them is fatal here rather than latent.
    #!
    #! NOT A DESCRIPTOR LAYOUT, AND MUST NOT BE READ AS ONE.  This model emits
    #! no real AEM field: `descriptor_bytes()` below is a deterministic fill,
    #! so only LENGTHS are modelled here.  The stream rows are 136 + 8*2
    #! because the vector uses Milan v1.2 Annex C Table C.1 (`formats_offset`
    #! 136, no `timing` field) on purpose, and that is NOT the layout this
    #! project ships.  Shipping descriptors come out of avdecc/gen_aem_store.py
    #! in the IEEE 1722.1-2021 Table 7-8 layout, `formats_offset` 138 and
    #! 138 + 8*N + 2*R octets: Milan v1.2 5.3.3.4 binds this descriptor to
    #! "[ATDECC, Clause 7.2.6]", and Milan v1.2 clause 2 (References) defines
    #! [ATDECC] as IEEE Std 1722.1-2021.  Annex C is a "may" there and a
    #! "shall" only "for the Streams that are part of the redundant pair",
    #! which this entity declares none of.  The shipping 138 is pinned by
    #! sw/builder/test_builder.py gate 16, not here.
    MILAN_8 = {
        (0, D_ENTITY): (1, 312),
        (0, D_CONFIGURATION): (1, 74 + 4 * 6),
        (0, D_AUDIO_UNIT): (1, 144 + 4 * 2),
        (0, D_STREAM_INPUT): (1, 136 + 8 * 2),
        (0, D_STREAM_OUTPUT): (1, 136 + 8 * 2),
        (0, D_AVB_INTERFACE): (1, 102),
        (0, D_CLOCK_SOURCE): (1, 86),
        (0, D_CLOCK_DOMAIN): (1, 76 + 2 * 1),
    }
    _FROM_VECTOR = _vector_lengths()
    assert _FROM_VECTOR is None or _FROM_VECTOR == MILAN_8, (
        "MILAN_8 and %s disagree about the same image: %r vs %r.  Move both "
        "or neither." % (DESC_VECTOR, MILAN_8, _FROM_VECTOR))
    del _FROM_VECTOR

    def __init__(self, entries=None, configurations_count=1, valid=True):
        self.valid = valid
        self._n_config = configurations_count
        self.entries = dict(self.MILAN_8 if entries is None else entries)

    def configurations_count(self):
        """Region 0xD.  `img_valid_r ? hdr_n_config_r : 64'd0`."""
        return self._n_config if self.valid else 0

    def locate(self, cfg, dtype, index):
        """Region 0xF.  Descriptor length on a hit, None on a MISS.

        The store scans its cached index map for the (configuration, type)
        entry and takes the hit only when the index is inside that entry's
        count and the entry is usable.  A descriptor longer than the line
        buffer is refused rather than truncated.

        The `self.valid` arm below is UNREACHABLE through READ_DESCRIPTOR and
        no scenario can assert it: an unvalidated image also reports zero
        configurations, and the microprogram range-checks the configuration
        BEFORE it locates, so it never gets here.  It is kept because it is
        what the store does, and because it is the arm that would start
        mattering the moment a second microprogram locates without that
        check.  See the unloaded-image scenario in
        features/aecp_read_descriptor.feature for the path that IS observable.
        """
        if not self.valid:
            return None
        entry = self.entries.get((cfg, dtype))
        if entry is None:
            return None
        count, length = entry
        if index >= count:
            return None
        if length > LINE_BYTES:
            return None
        return length

    @staticmethod
    def descriptor_bytes(dtype, index, length):
        """Region 0x0, in wire order.

        IEEE 1722.1-2021 7.2.1 opens EVERY descriptor with descriptor_type
        then descriptor_index; the rest is a deterministic fill so a short,
        shifted or missing COPY_BUFFER is visible rather than plausible.
        """
        body = bytearray(length)
        body[0:2] = struct.pack(">H", dtype)
        body[2:4] = struct.pack(">H", index)
        for k in range(4, length):
            body[k] = (dtype * 31 + index * 7 + k * 13) & 0xFF
        return bytes(body)


# ---------------------------------------------------------------------------
# the command path (KL_aecp_engine.sv + the microprograms it dispatches to)
# ---------------------------------------------------------------------------

class AecpEngineModel:
    """One AECP command in, one Ethernet frame or nothing out.

    READ_DESCRIPTOR carrying its operands runs the descriptor microprogram,
    IDENTIFY_NOTIFICATION and a truncated READ_DESCRIPTOR run the
    BAD_ARGUMENTS echo, declared commands enter the served inventory, and the
    remainder runs the NOT_IMPLEMENTED echo. A response arriving as input and
    a command for another entity are freed without a reply.
    """

    def __init__(self, image=None, entity_id=ENTITY_ID, own_mac=OWN_MAC):
        self.image = image if image is not None else DescriptorImage()
        self.entity_id = entity_id
        self.own_mac = own_mac
        self.cmd_count = 0
        self.resp_count = 0
        self.drop_count = 0
        self.last_oversize = False

    # -- the pop face -------------------------------------------------------
    def deliver(self, frame):
        """Hand the engine one received Ethernet frame.

        Returns the response frame, or None when the engine refuses silently.
        """
        pdu = frame[ETH_HDR:]            # an RX slot holds the AVTPDU, not the frame
        req_mac = frame[6:12]
        msg_type = pdu[1] & 0x0F
        cdl = ((pdu[2] & 0x07) << 8) | pdu[3]
        target_eid = int.from_bytes(pdu[4:12], "big")
        ctlr_eid = bytes(pdu[12:20])
        seq = bytes(pdu[20:22])
        raw_ct = bytes(pdu[22:24])
        opcode = ((pdu[22] & 0x3F) << 8) | pdu[23]

        # F06.2 MATCHED arc, plus the response-storm guard: an AECP RESPONSE
        # arriving as input (message_type odd) is freed without a reply, and so
        # is a command whose target_entity_id is not ours.  Counted, not lost.
        if (msg_type & 1) or (target_eid != self.entity_id):
            self.drop_count += 1
            return None
        self.cmd_count += 1

        # cdl is the offset-from-@12 length, so the command payload is
        # cdl - 12, capped by the response buffer and by the committed slot.
        cdl_pld = cdl - 12 if cdl > 12 else 0
        slot_pld = max(len(pdu) - AECP_HDR, 0)
        pld_cmd = min(cdl_pld, PLD_MAX, slot_pld)
        cmd_payload = bytes(pdu[AECP_HDR:AECP_HDR + pld_cmd])

        # the operand latch: only the payload bytes the walk actually reached
        cfg_ix = _be16(cmd_payload, 0)
        desc_ty = _be16(cmd_payload, 4)
        desc_ix = _be16(cmd_payload, 6)

        # the dispatch decision.  A READ_DESCRIPTOR too short to carry
        # configuration_index + reserved + type + index is BAD_ARGUMENTS, never
        # a locate of whatever zeros happened to be there.
        short = cdl < 20
        #! the served row the SERVED program reads its response form from.
        #! The dispatch arm that uses it is guarded on MT_AEM_COMMAND for the
        #! reason the engine guards every discriminator on PP_PROTO_AEM: on an
        #! ADDRESS_ACCESS PDU the @22..@23 word is tlv_count (IEEE 9.4.2.1)
        #! and on a VENDOR_UNIQUE one it is the first half of a 48-bit
        #! protocol_id - neither is a command_type, and reading either as one
        #! turns an unrelated count into a served opcode.
        self.opcode_served = opcode
        #! ...and the guard belongs on THESE TWO ARMS as well, which is where
        #! the paragraph above was written and not applied. The model mirrored
        #! the engine's own defect (issue #83): a VENDOR_UNIQUE protocol_id
        #! beginning 00-04 was dispatched to READ_DESCRIPTOR by both, so the
        #! contract suite and the gateware agreed on the wrong answer and no
        #! gate could see it. A model that reproduces the bug it exists to
        #! catch is worse than no model.
        aem = (msg_type == MT_AEM_COMMAND)
        if aem and opcode == OP_READ_DESCRIPTOR and not short:
            program, echo = "RDESC", False
        elif aem and (opcode == OP_IDENTIFY_NOTIFICATION or (
                opcode == OP_READ_DESCRIPTOR and short)):
            program, echo = "BADARG", True
        elif (msg_type == MT_AEM_COMMAND) and (opcode in SERVED):
            #! a command this engine answers for real. This model does NOT
            #! reproduce its payload - that would be re-implementing the
            #! microprograms in Python, which is how the model went stale in
            #! the first place, and pp_top already grades every one of them
            #! byte-exactly against the wire. What the model owns here is the
            #! PARTITION: a served opcode must not fall to the
            #! NOT_IMPLEMENTED echo, and it is graded as SERVED, not guessed.
            program, echo = "SERVED", False
        else:
            program, echo = "NOTIMPL", True

        # the echo pre-load: the command payload is copied into the response
        # buffer BEFORE the microprogram runs, so an echoed answer is the
        # command's own bytes at the command's own length.
        buf = bytearray(RESP_BUF)
        buf[12:12 + pld_cmd] = cmd_payload

        status, resp_len = self._run(program, buf, cfg_ix, desc_ty, desc_ix)
        pld = pld_cmd if echo else min(max(resp_len - 12, 0), PLD_MAX)

        self.resp_count += 1
        return self._assemble(req_mac, msg_type, status, raw_ct, ctlr_eid,
                              seq, buf, pld)

    # -- the microprograms --------------------------------------------------
    def _run(self, program, buf, cfg_ix, desc_ty, desc_ix):
        """Return (status, resp_len).  resp_len counts the microCPU's own 12
        header bytes, so the emitted payload is resp_len - 12."""
        if program == "NOTIMPL":
            return ST_NOT_IMPLEMENTED, 12       # E_NOTIMPL
        if program == "BADARG":
            return ST_BAD_ARGUMENTS, 12         # E_BADARG
        if program == "SERVED":
            #! the response FORM from the inventory's clause. A None cdl is a
            #! variable-length response (READ_DESCRIPTOR's descriptor,
            #! GET_AVB_INFO's mapping list, GET_AS_PATH's path, an audio-map
            #! page) whose length this model has no business predicting.
            row = SERVED[self.opcode_served]
            return row["verdict"], (12 if row["cdl"] is None else row["cdl"])
        return self._read_descriptor(buf, cfg_ix, desc_ty, desc_ix)

    def _read_descriptor(self, buf, cfg_ix, desc_ty, desc_ix):
        """E_RDESC.  The configuration range check runs BEFORE the locate, so
        a bad configuration_index is BAD_ARGUMENTS and only a real locate miss
        is NO_SUCH_DESCRIPTOR."""
        if not cfg_ix < self.image.configurations_count():
            return self._stub(buf, cfg_ix, desc_ty, desc_ix, ST_BAD_ARGUMENTS)
        length = self.image.locate(cfg_ix, desc_ty, desc_ix)
        if length is None:
            return self._stub(buf, cfg_ix, desc_ty, desc_ix,
                              ST_NO_SUCH_DESCRIPTOR)
        cur = 12
        buf[cur:cur + 2] = struct.pack(">H", cfg_ix)          # @24
        cur += 2
        buf[cur:cur + 2] = b"\x00\x00"                        # @26 reserved
        cur += 2
        buf[cur:cur + length] = self.image.descriptor_bytes(  # @28..
            desc_ty, desc_ix, length)
        cur += length
        return ST_SUCCESS, cur

    @staticmethod
    def _stub(buf, cfg_ix, desc_ty, desc_ix, status):
        """E_RDSTUB - the IEEE 7.4.5 four-octet failure descriptor, carrying
        descriptor_type and descriptor_index at the offsets the command used."""
        cur = 12
        buf[cur:cur + 2] = struct.pack(">H", cfg_ix)          # @24
        cur += 2
        buf[cur:cur + 2] = b"\x00\x00"                        # @26 reserved
        cur += 2
        buf[cur:cur + 4] = struct.pack(">HH", desc_ty, desc_ix)   # @28..@31
        cur += 4
        return status, cur

    # -- the frame ----------------------------------------------------------
    def _assemble(self, req_mac, cmd_msg_type, status, raw_ct, ctlr_eid, seq,
                  buf, pld):
        cdl = 12 + pld
        f = bytearray()
        f += req_mac                       # unicast back to the requester
        f += self.own_mac
        f += struct.pack(">H", ETHERTYPE_AVTP)
        f.append(SUBTYPE_AECP)
        f.append((cmd_msg_type | 1) & 0x0F)          # sv=0, version=0, mt+1
        f.append(((status & 0x1F) << 3) | ((cdl >> 8) & 0x07))
        f.append(cdl & 0xFF)
        f += struct.pack(">Q", self.entity_id)
        f += ctlr_eid
        f += seq
        #! The u bit exists only on an AEM command_type (IEEE 1722.1-2021
        #! 9.3.2.1). Masking it for EVERY message type is the same defect the
        #! engine records at KL_aecp_engine.sv's u-bit banner and that
        #! tb/pp_top fixed with `aem_like`: on a VENDOR_UNIQUE PDU these two
        #! bytes are the head of a 48-bit protocol_id, so clearing bit 7 of
        #! byte 0 corrupts any OUI with that bit set -- and made every such
        #! protocol_id untestable, because the model could not put one on the
        #! wire to disagree about.
        f.append(raw_ct[0] & 0x7F if cmd_msg_type == MT_AEM_COMMAND
                 else raw_ct[0])
        f.append(raw_ct[1])
        f += bytes(buf[12:12 + pld])
        while len(f) < ETH_MIN:                      # zero pad to the 802.3 minimum
            f.append(0)
        self.last_oversize = len(f) > TX_STD_BYTES
        return bytes(f)


def _be16(buf, off):
    """Big-endian halfword, zero where the walk never reached."""
    hi = buf[off] if off < len(buf) else 0
    lo = buf[off + 1] if off + 1 < len(buf) else 0
    return (hi << 8) | lo


# ---------------------------------------------------------------------------
# command frames a controller would put on the wire
# ---------------------------------------------------------------------------

def build_command(msg_type, ct_word, payload, target_eid=ENTITY_ID,
                  ctlr_eid=CONTROLLER_EID, seq=0x1234, cdl=None,
                  src_mac=CONTROLLER_MAC, dst_mac=OWN_MAC):
    """One AECP command frame.  `ct_word` is the raw 16-bit field at @22."""
    pdu = bytearray()
    pdu.append(SUBTYPE_AECP)
    pdu.append(msg_type & 0x0F)                 # sv = 0, h = 0, version = 0
    real_cdl = (12 + len(payload)) if cdl is None else cdl
    pdu.append(((0 & 0x1F) << 3) | ((real_cdl >> 8) & 0x07))
    pdu.append(real_cdl & 0xFF)
    pdu += struct.pack(">Q", target_eid)
    pdu += struct.pack(">Q", ctlr_eid)
    pdu += struct.pack(">H", seq)
    pdu += struct.pack(">H", ct_word)
    pdu += payload
    frame = bytearray(dst_mac + src_mac + struct.pack(">H", ETHERTYPE_AVTP) + pdu)
    while len(frame) < ETH_MIN:
        frame.append(0)
    # KL_pp_rx_validator V1: a PDU claiming more than it carries never reaches
    # the engine at all.  Guard the fixture, not the device.
    assert real_cdl + 12 <= len(frame) - ETH_HDR, \
        "fixture builds a V1-illegal frame the validator would drop"
    return bytes(frame)


def build_read_descriptor(cfg, dtype, index, **kw):
    payload = struct.pack(">HHHH", cfg, 0, dtype, index)
    return build_command(MT_AEM_COMMAND, OP_READ_DESCRIPTOR, payload, **kw)


def build_aem_command(opcode, payload=None, **kw):
    if payload is None:
        payload = struct.pack(">HHHH", 0, 0, D_ENTITY, 0)
    return build_command(MT_AEM_COMMAND, opcode, payload, **kw)


def build_acquire_entity(owner_id=0, **kw):
    """IEEE 7.4.1: flags, owner_id, descriptor_type, descriptor_index - the
    16-octet acquire form, so the response is the 40-octet AECPDU of F06.14.
    The command carries owner_id zero. Milan Delta 7 requires the response to
    remain unowned and return NOT_SUPPORTED."""
    payload = struct.pack(">IQHH", 0, owner_id, D_ENTITY, 0)
    return build_command(MT_AEM_COMMAND, OP_ACQUIRE_ENTITY, payload, **kw)


def build_address_access(tlv_count=1, **kw):
    """IEEE 9.4.2: tlv_count at @22, tlv_data from @24.  One READ TLV is
    mode+length (2 octets) and address (8), with no memory_data."""
    tlv = struct.pack(">HQ", (0 << 12) | 0, 0x0000_0000_DEAD_BEEF)
    return build_command(MT_AA_COMMAND, tlv_count, tlv * tlv_count, **kw)


def build_mvu_command(mvu_command_type=MVU_GET_MILAN_INFO, **kw):
    """F06.11: protocol_id spans @22..@27, so its first two octets ride the
    header field the engine echoes and its last four ride the payload."""
    ct_word = (MILAN_PROTOCOL_ID[0] << 8) | MILAN_PROTOCOL_ID[1]
    payload = MILAN_PROTOCOL_ID[2:6] + struct.pack(">HH", mvu_command_type, 0)
    return build_command(MT_VU_COMMAND, ct_word, payload, **kw)


# ---------------------------------------------------------------------------
# response decoding + well-formedness
# ---------------------------------------------------------------------------

def decode(frame):
    cdl = ((frame[16] & 0x07) << 8) | frame[17]
    return {
        "dst_mac": bytes(frame[0:6]),
        "src_mac": bytes(frame[6:12]),
        "ethertype": int.from_bytes(frame[12:14], "big"),
        "subtype": frame[14],
        "sv_version": frame[15] >> 4,
        "message_type": frame[15] & 0x0F,
        "status": frame[16] >> 3,
        "control_data_length": cdl,
        "target_entity_id": int.from_bytes(frame[18:26], "big"),
        "controller_entity_id": int.from_bytes(frame[26:34], "big"),
        "sequence_id": int.from_bytes(frame[34:36], "big"),
        "u": frame[36] >> 7,
        "cr": (frame[36] >> 6) & 1,
        "command_type": ((frame[36] & 0x3F) << 8) | frame[37],
        "payload": bytes(frame[FRAME_HDR:FRAME_HDR + max(cdl - 12, 0)]),
        "frame_len": len(frame),
    }


def complaints(frame, cmd_frame, entity_id=ENTITY_ID):
    """Everything that makes this response MALFORMED against its command.

    Empty list = well formed.  The list is what "never malformed" means here,
    and every entry is a rule from IEEE 9.2.2 or 9.2.1.
    """
    bad = []
    if frame is None:
        return ["no response at all"]
    if len(frame) < ETH_MIN:
        bad.append("frame %d octets, below the 802.3 minimum %d"
                   % (len(frame), ETH_MIN))
    r = decode(frame)
    c = decode_command(cmd_frame)
    if r["ethertype"] != ETHERTYPE_AVTP:
        bad.append("ethertype %#06x" % r["ethertype"])
    if r["subtype"] != SUBTYPE_AECP:
        bad.append("subtype %#04x" % r["subtype"])
    if r["sv_version"] != 0:
        bad.append("sv/version nibble %#x, 9.2.2.2/.3 require zero"
                   % r["sv_version"])
    if r["message_type"] != (c["message_type"] | 1):
        bad.append("message_type %d for a command of type %d"
                   % (r["message_type"], c["message_type"]))
    if r["control_data_length"] < 12:
        bad.append("control_data_length %d below the 12-octet header"
                   % r["control_data_length"])
    carried = len(frame) - FRAME_HDR
    if r["control_data_length"] - 12 > carried:
        bad.append("control_data_length claims %d payload octets, the frame "
                   "carries %d" % (r["control_data_length"] - 12, carried))
    if r["target_entity_id"] != entity_id:
        bad.append("target_entity_id %#018x is not ours" % r["target_entity_id"])
    if r["controller_entity_id"] != c["controller_entity_id"]:
        bad.append("controller_entity_id not echoed")
    if r["sequence_id"] != c["sequence_id"]:
        bad.append("sequence_id %d, command sent %d"
                   % (r["sequence_id"], c["sequence_id"]))
    #! ...on an AEM response. Only an AEM command_type has a `u` bit (IEEE
    #! 1722.1-2021 9.3.2.1); on a VENDOR_UNIQUE PDU that bit is part of the
    #! 48-bit protocol_id and on an ADDRESS_ACCESS one it belongs to
    #! tlv_count. Asserting it unconditionally made every OUI with the top bit
    #! set "malformed" -- the well-formedness check enforcing the same
    #! misreading of @22..@23 that issue #83 is about, one level up.
    if r["message_type"] == MT_AEM_RESPONSE and r["u"] != 0:
        bad.append("u set on a solicited response")
    if r["dst_mac"] != c["src_mac"]:
        bad.append("not unicast back to the requester")
    return bad


def decode_command(frame):
    pdu = frame[ETH_HDR:]
    cdl = ((pdu[2] & 0x07) << 8) | pdu[3]
    return {
        "src_mac": bytes(frame[6:12]),
        "message_type": pdu[1] & 0x0F,
        "control_data_length": cdl,
        "target_entity_id": int.from_bytes(pdu[4:12], "big"),
        "controller_entity_id": int.from_bytes(pdu[12:20], "big"),
        "sequence_id": int.from_bytes(pdu[20:22], "big"),
        "command_type": ((pdu[22] & 0x3F) << 8) | pdu[23],
        "payload": bytes(pdu[AECP_HDR:AECP_HDR + max(cdl - 12, 0)]),
    }


# ---------------------------------------------------------------------------
# helpers shared by the steps
# ---------------------------------------------------------------------------

def _send(context, frame):
    context.aecp_cmd = frame
    before = (context.aecp.cmd_count, context.aecp.resp_count,
              context.aecp.drop_count)
    context.aecp_before = before
    context.aecp_rsp = context.aecp.deliver(frame)
    return context.aecp_rsp


def _rsp(context):
    assert context.aecp_rsp is not None, \
        "the engine produced NO response - there is nothing to decode"
    return decode(context.aecp_rsp)


# ---------------------------------------------------------------------------
# Steps - the engine under test
# ---------------------------------------------------------------------------

@given('the protocol-processor AECP engine with the 8-descriptor Milan image')
def step_engine_milan8(context):
    context.aecp = AecpEngineModel(DescriptorImage())
    context.aecp_rsp = None
    context.aecp_cmd = None


@given('the protocol-processor AECP engine before software loads the image')
def step_engine_unloaded(context):
    """The store validates magic + layout version + checksum before it serves
    anything; until then region 0xD reads zero and every locate misses."""
    context.aecp = AecpEngineModel(DescriptorImage(valid=False))
    context.aecp_rsp = None
    context.aecp_cmd = None


@given('the AECP image declares {n:d} configurations')
def step_engine_nconfig(context, n):
    context.aecp.image = DescriptorImage(configurations_count=n)


# ---------------------------------------------------------------------------
# Steps - commands
# ---------------------------------------------------------------------------

@when('the controller reads descriptor type {dtype:d} index {index:d} '
      'in configuration {cfg:d}')
def step_read_descriptor(context, dtype, index, cfg):
    _send(context, build_read_descriptor(cfg, dtype, index))


@when('the controller sends a READ_DESCRIPTOR of control_data_length {cdl:d}')
def step_read_descriptor_short(context, cdl):
    """A command whose declared cdl cannot carry the 8 operand octets."""
    payload = b"\x00" * max(cdl - 12, 0)
    _send(context, build_command(MT_AEM_COMMAND, OP_READ_DESCRIPTOR, payload,
                                 cdl=cdl))


@when('the controller sends AEM opcode {opcode:d} to the AECP engine')
def step_send_aem(context, opcode):
    _send(context, build_aem_command(opcode))


@when('the controller sends ACQUIRE_ENTITY to the AECP engine')
def step_send_acquire(context):
    _send(context, build_acquire_entity())


@when('the controller sends an ADDRESS_ACCESS command to the AECP engine')
def step_send_aa(context):
    _send(context, build_address_access())


@when('the controller sends the Milan MVU command to the AECP engine')
def step_send_mvu(context):
    _send(context, build_mvu_command())


@when('the controller sends a VENDOR_UNIQUE command whose protocol_id '
      'starts {oui_hi} to the AECP engine')
def step_send_vu_oui(context, oui_hi):
    """A vendor command whose OUI head collides with an AEM opcode.

    The engine and this model both read AECPDU @22..@23 as `opcode`, and on a
    VENDOR_UNIQUE PDU those two bytes are the first half of a 48-bit
    protocol_id.  Issue #83: a vendor whose OUI began 00-04 was dispatched to
    READ_DESCRIPTOR by BOTH, so the contract suite agreed with the gateware
    about the wrong answer and nothing could see it.
    """
    ct_word = int(oui_hi, 0)
    payload = struct.pack(">IHH", 0xAABBCCDD, 0, 0)
    context.vu_oui_payload = payload
    _send(context, build_command(MT_VU_COMMAND, ct_word, payload))


@then('the AECP response protocol_id is echoed whole')
def step_vu_protocol_id_whole(context):
    r = _rsp(context)
    sent = context.aecp_cmd
    #! @22..@23 rides the header field the engine echoes; @24..@27 rides the
    #! payload it copies back. Both halves, or the check misses the exact
    #! corruption issue #83 produced -- READ_DESCRIPTOR overwriting @24..@27
    #! with configuration_index and reserved while the head looked right.
    head_got, head_sent = bytes(context.aecp_rsp[36:38]), bytes(sent[36:38])
    assert head_got == head_sent, \
        "protocol_id head came back %s, sent %s" % (head_got.hex(),
                                                    head_sent.hex())
    tail_sent = bytes(context.vu_oui_payload[0:4])
    tail_got = r["payload"][0:4]
    assert tail_got == tail_sent, \
        "protocol_id tail came back %s, sent %s" % (tail_got.hex(),
                                                    tail_sent.hex())


@when('a command for entity {eid} reaches the AECP engine')
def step_send_foreign(context, eid):
    _send(context, build_aem_command(OP_READ_DESCRIPTOR,
                                     target_eid=int(eid, 0)))


@when('an AECP {kind} arrives at the AECP engine as input')
def step_send_response_as_input(context, kind):
    mt = {"AEM response": MT_AEM_RESPONSE,
          "VENDOR_UNIQUE response": MT_VU_RESPONSE,
          "ADDRESS_ACCESS response": MT_AA_RESPONSE}[kind]
    _send(context, build_command(mt, OP_READ_DESCRIPTOR,
                                 struct.pack(">HHHH", 0, 0, D_ENTITY, 0)))


@when('the controller sweeps AEM opcodes {lo:d} to {hi:d} plus {extra:d}')
def step_sweep(context, lo, hi, extra):
    """One READ_DESCRIPTOR-shaped command per opcode, so a single payload
    exercises all three dispatch arms and the partition is exact."""
    context.aecp_sweep = []
    for op in list(range(lo, hi + 1)) + [extra]:
        cmd = build_aem_command(op)
        context.aecp_sweep.append((op, cmd, context.aecp.deliver(cmd)))


# ---------------------------------------------------------------------------
# Steps - the answer
# ---------------------------------------------------------------------------

@then('the AECP response status is {status:d}')
def step_status(context, status):
    got = _rsp(context)["status"]
    assert got == status, "AECP status %d, expected %d" % (got, status)


@then('the AECP response message_type is {mt:d}')
def step_message_type(context, mt):
    got = _rsp(context)["message_type"]
    assert got == mt, "AECP message_type %d, expected %d" % (got, mt)


@then('the AECP response message_type is the command type plus one')
def step_message_type_plus_one(context):
    got = _rsp(context)["message_type"]
    want = decode_command(context.aecp_cmd)["message_type"] + 1
    assert got == want, "AECP message_type %d, expected %d" % (got, want)


@then('the AECP response control_data_length is {cdl:d}')
def step_cdl(context, cdl):
    got = _rsp(context)["control_data_length"]
    assert got == cdl, "control_data_length %d, expected %d" % (got, cdl)


@then('the AECP response control_data_length counts its own payload')
def step_cdl_counts_payload(context):
    r = _rsp(context)
    carried = len(context.aecp_rsp) - FRAME_HDR
    assert r["control_data_length"] - 12 <= carried, \
        "control_data_length claims %d payload octets, the frame carries %d" \
        % (r["control_data_length"] - 12, carried)
    assert r["control_data_length"] == 12 + len(r["payload"]), \
        "control_data_length %d does not equal 12 + payload %d" \
        % (r["control_data_length"], len(r["payload"]))


@then('the AECP response AECPDU is {n:d} octets')
def step_aecpdu_len(context, n):
    got = _rsp(context)["control_data_length"] + 12
    assert got == n, "AECPDU %d octets (cdl + 12), expected %d" % (got, n)


@then('the AECP response carries the command payload verbatim')
def step_echo_verbatim(context):
    r = _rsp(context)
    want = decode_command(context.aecp_cmd)["payload"]
    assert r["payload"] == want, \
        "echo payload %s, command carried %s" % (r["payload"].hex(), want.hex())


@then('the AECP response echoes command_type {op:d} with u clear')
def step_echo_command_type(context, op):
    r = _rsp(context)
    assert r["command_type"] == op, \
        "command_type %#06x, expected %#06x" % (r["command_type"], op)
    assert r["u"] == 0, "u set on a solicited response"


@then('the AECP response is unicast back to the requester from our own MAC')
def step_unicast(context):
    r = _rsp(context)
    c = decode_command(context.aecp_cmd)
    assert r["dst_mac"] == c["src_mac"], \
        "destination %s, requester was %s" % (r["dst_mac"].hex(),
                                              c["src_mac"].hex())
    assert r["src_mac"] == context.aecp.own_mac, \
        "source %s, our MAC is %s" % (r["src_mac"].hex(),
                                      context.aecp.own_mac.hex())


@then('the AECP response echoes the sequence_id and the controller_entity_id')
def step_echo_identity(context):
    r = _rsp(context)
    c = decode_command(context.aecp_cmd)
    assert r["sequence_id"] == c["sequence_id"], \
        "sequence_id %d, command sent %d" % (r["sequence_id"], c["sequence_id"])
    assert r["controller_entity_id"] == c["controller_entity_id"], \
        "controller_entity_id %#018x, command sent %#018x" \
        % (r["controller_entity_id"], c["controller_entity_id"])


@then('the AECP response target_entity_id is our own')
def step_target_is_ours(context):
    got = _rsp(context)["target_entity_id"]
    assert got == context.aecp.entity_id, \
        "target_entity_id %#018x, ours is %#018x" % (got, context.aecp.entity_id)


@then('the AECP response is well formed against its command')
def step_wellformed(context):
    bad = complaints(context.aecp_rsp, context.aecp_cmd,
                     context.aecp.entity_id)
    assert not bad, "malformed response: " + "; ".join(bad)


@then('the AECP response configuration_index is {cfg:d} and the reserved '
      'halfword is zero')
def step_cfg_and_reserved(context, cfg):
    p = _rsp(context)["payload"]
    assert len(p) >= 4, "payload %d octets, too short for the 7.4.5 prefix" % len(p)
    got = struct.unpack(">H", p[0:2])[0]
    assert got == cfg, "configuration_index %d, expected %d" % (got, cfg)
    assert p[2:4] == b"\x00\x00", "reserved halfword %s" % p[2:4].hex()


@then('the AECP response descriptor is {n:d} octets opening with type {dtype:d} '
      'index {index:d}')
def step_descriptor(context, n, dtype, index):
    p = _rsp(context)["payload"]
    desc = p[4:]
    assert len(desc) == n, "descriptor %d octets, expected %d" % (len(desc), n)
    assert desc[0:4] == struct.pack(">HH", dtype, index), \
        "descriptor opens %s, expected type %d index %d" \
        % (desc[0:4].hex(), dtype, index)
    assert desc == DescriptorImage.descriptor_bytes(dtype, index, n), \
        "the served descriptor is not the image's bytes"


@then('the AECP response carries the 7.4.5 stub for type {dtype:d} index {index:d}')
def step_stub(context, dtype, index):
    """On failure the descriptor field is FOUR octets and contains
    descriptor_type and descriptor_index, at the command's own offsets."""
    r = _rsp(context)
    p = r["payload"]
    assert len(p) == 8, \
        "failure payload %d octets, 7.4.5 wants 4 prefix + 4 stub" % len(p)
    stub = p[4:8]
    assert stub == struct.pack(">HH", dtype, index), \
        "stub %s, expected type %d index %d" % (stub.hex(), dtype, index)
    cmd_p = decode_command(context.aecp_cmd)["payload"]
    assert stub == cmd_p[4:8], \
        "the stub is not at the command's own offsets: %s vs %s" \
        % (stub.hex(), cmd_p[4:8].hex())


# ---------------------------------------------------------------------------
# Steps - the refusals
# ---------------------------------------------------------------------------

@then('the AECP engine emits no frame at all')
def step_no_frame(context):
    assert context.aecp_rsp is None, \
        "the engine answered %d octets where it must stay silent: %s" \
        % (len(context.aecp_rsp), context.aecp_rsp[:24].hex())


@then('the AECP engine counted a drop and no command')
def step_counted_drop(context):
    cmd0, _resp0, drop0 = context.aecp_before
    assert context.aecp.drop_count == drop0 + 1, \
        "drop counter %d, was %d" % (context.aecp.drop_count, drop0)
    assert context.aecp.cmd_count == cmd0, \
        "command counter advanced to %d on a refused frame" % context.aecp.cmd_count


@then('the AECP engine counted a command and a response')
def step_counted_command(context):
    cmd0, resp0, drop0 = context.aecp_before
    assert context.aecp.cmd_count == cmd0 + 1, \
        "command counter %d, was %d" % (context.aecp.cmd_count, cmd0)
    assert context.aecp.resp_count == resp0 + 1, \
        "response counter %d, was %d" % (context.aecp.resp_count, resp0)
    assert context.aecp.drop_count == drop0, \
        "drop counter advanced to %d on an answered command" \
        % context.aecp.drop_count


# ---------------------------------------------------------------------------
# Steps - the sweep
# ---------------------------------------------------------------------------

@then('every swept opcode was answered and none was met with silence')
def step_sweep_answered(context):
    silent = [op for op, _c, r in context.aecp_sweep if r is None]
    assert not silent, \
        "%d opcodes were met with silence: %s" % (len(silent), silent[:8])


@then('every swept answer is well formed against its command')
def step_sweep_wellformed(context):
    bad = []
    for op, cmd, rsp in context.aecp_sweep:
        for c in complaints(rsp, cmd):
            bad.append("opcode %#06x: %s" % (op, c))
    assert not bad, "%d malformed answers: %s" % (len(bad), "; ".join(bad[:5]))


@then('the swept opcodes partition into the served set and the '
      'NOT_IMPLEMENTED remainder')
def step_sweep_partition(context):
    wrong = []
    served = 0
    others = 0
    for op, _cmd, rsp in context.aecp_sweep:
        got = decode(rsp)["status"]
        if op in SERVED:
            want = SERVED[op]["verdict"]
            served += 1
        else:
            want = ST_NOT_IMPLEMENTED
            others += 1
        if got != want:
            wrong.append("opcode %#06x (%s): status %d, expected %d"
                         % (op, SERVED.get(op, {}).get("name", "unserved"),
                            got, want))
    assert not wrong, "%d opcodes answered wrong: %s" % (len(wrong),
                                                         "; ".join(wrong[:5]))
    #! the sweep must actually have covered the inventory: a sweep range that
    #! stopped short of the served opcodes would report a clean partition
    #! having proved nothing about them
    missed = sorted(set(SERVED) - {op for op, _c, _r in context.aecp_sweep})
    assert not missed, "the sweep never reached served opcodes %s" \
        % ", ".join("%#06x" % o for o in missed)
    assert served == len(SERVED), \
        "%d served opcodes swept, the inventory holds %d" % (served,
                                                             len(SERVED))
    assert others > 0, "the sweep found no unserved opcode to refuse"
    context.sweep_counts = (served, others)


@then('the served inventory matches the opcodes the engine RTL decodes')
def step_inventory_matches_rtl(context):
    """The anti-staleness gate: parse the engine's own opcode localparams and
    compare them to SERVED.  This is the check that would have caught the
    twelve commands this suite went on calling NOT_IMPLEMENTED for three days
    after they landed."""
    import re
    assert os.path.exists(_ENGINE_SV), \
        "the engine RTL is not readable at %s - the submodule is probably " \
        "not checked out, and an unreadable gate is a SKIP, never a PASS" \
        % _ENGINE_SV
    with open(_ENGINE_SV, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    #! the opcode constants, but NOT the descriptor-type ones: both are 16-bit
    #! localparams in the same block and only the OP_ prefix separates them
    rtl = {int(m, 16) for m in
           re.findall(r"localparam\s+logic\s*\[15:0\]\s+OP_[A-Z0-9_]+_C\s*=\s*"
                      r"16'h([0-9A-Fa-f]{4})\s*;", text)}
    assert rtl, "no OP_*_C opcode constants parsed out of %s" % _ENGINE_SV
    missing = sorted(rtl - set(SERVED))
    extra = sorted(set(SERVED) - rtl)
    assert not missing, \
        "the engine decodes %s but this suite's SERVED inventory does not " \
        "list them - add the row (with its Milan clause) or the model is " \
        "asserting behaviour the RTL no longer has" \
        % ", ".join("%#06x" % o for o in missing)
    assert not extra, \
        "this suite claims %s are served but the engine decodes no such " \
        "opcode" % ", ".join("%#06x" % o for o in extra)


@then('every swept answer carries the command payload verbatim except '
      'the served set')
def step_sweep_echo(context):
    #! only the ECHO path replays the command bytes. A served opcode builds
    #! its own response body, so it is excluded here and graded byte-exactly
    #! by protocol-processor/tb/pp_top instead - the layer that drives the
    #! real RTL. IDENTIFY_NOTIFICATION stays in the echo set: its
    #! BAD_ARGUMENTS answer IS the reflected command (IEEE 7.4.39.2).
    bad = []
    for op, cmd, rsp in context.aecp_sweep:
        if op in SERVED and op != OP_IDENTIFY_NOTIFICATION:
            continue
        want = decode_command(cmd)["payload"]
        got = decode(rsp)["payload"]
        if got != want:
            bad.append("opcode %#06x echoed %s, command carried %s"
                       % (op, got.hex(), want.hex()))
    assert not bad, "%d opcodes did not echo: %s" % (len(bad), "; ".join(bad[:5]))


# ---------------------------------------------------------------------------
# Steps - the MVU protocol_id
# ---------------------------------------------------------------------------

@then('the Milan protocol_id survives the AECP echo whole')
def step_protocol_id(context):
    """protocol_id spans @22..@27: two octets in the field the engine echoes
    from the wire and four in the payload it copies back."""
    r = _rsp(context)
    on_wire = bytes(context.aecp_rsp[36:38]) + r["payload"][0:4]
    assert on_wire == MILAN_PROTOCOL_ID, \
        "protocol_id came back %s, sent %s" % (on_wire.hex(),
                                               MILAN_PROTOCOL_ID.hex())


# ---------------------------------------------------------------------------
# Steps - the Milan Delta 7 ACQUIRE_ENTITY refusal
# ---------------------------------------------------------------------------

@then('the AECP response owner_id is zero, not the acquiring controller')
def step_owner_id(context):
    """7.4.1 puts owner_id at payload offset 4, right after the 4-octet flags.
    Milan Delta 7: the entity never grants an acquisition, so it answers zero
    there."""
    p = _rsp(context)["payload"]
    assert len(p) >= 12, \
        "payload %d octets, too short for the 16-octet ACQUIRE form" % len(p)
    owner = int.from_bytes(p[4:12], "big")
    assert owner == 0, \
        "owner_id %#018x, Milan Delta 7 wants zero" % owner
