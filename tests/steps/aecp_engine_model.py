# SPDX-FileCopyrightText: 2026 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The offline AECP model the `aecp_engine_steps` scenarios judge.

This is the mechanism half of that step module, lifted out whole when the
file passed a thousand lines: the descriptor store, the command path, the
command frames a controller would put on the wire, and the response decoder
with its well-formedness rules. `aecp_engine_steps.py` keeps the two things
that are NOT mechanism - the served-opcode inventory, which is this suite's
declaration of what the device answers for real, and the scenarios - and
imports what is here.

WHY THE SPLIT IS THIS ONE. The inventory is data with a gate on it: it is
compared against the engine RTL's own opcode constants by the steps, and
against docs/reference/milan_feature_status.json by
scripts/check_feature_status.py, which AST-parses `SERVED` out of the step
module. It therefore stays where those two readers look for it, and reaches
the engine as a CONSTRUCTOR ARGUMENT (`AecpEngineModel(served, ...)`) rather
than as a module global this file would have to import back.

The sources mirrored, the clauses used and the standing of this layer are
recorded in the header of `aecp_engine_steps.py`; they govern this file too.

PATHS ARE `Path` HERE, all of them. The one string crossing is `sys.path`,
which takes strings, and it is spelled `str(...)` where it happens.
"""

from __future__ import annotations

import json
import struct
import sys
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[2]
#! the submodule test vector this model's descriptor LENGTHS are taken from
DESC_VECTOR = (ROOT / "protocol-processor" / "hdl" / "aecp" / "desc"
               / "example_milan_8.json")

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
OP_SET_NAME = 0x0010
OP_IDENTIFY_NOTIFICATION = 0x0026
OP_GET_DYNAMIC_INFO = 0x004B
OP_START_STREAMING = 0x0022
OP_STOP_STREAMING = 0x0023
#! 1722.1-2021 Table 7-1. Milan 5.4.2.19/.20 serve these two per Stream
#! INPUT and require NOT_SUPPORTED for a Stream Output; every other type
#! takes the same refusal, which is what keeps a locate on a descriptor that
#! EXISTS (ENTITY[0] does) away from the started/stopped write.
DT_STREAM_INPUT = 0x0005

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
    if not DESC_VECTOR.exists():
        return None
    desc_dir = str(DESC_VECTOR.parent)
    if desc_dir not in sys.path:
        sys.path.insert(0, desc_dir)
    import gen_desc_image as gdi
    doc = json.loads(DESC_VECTOR.read_text(encoding="utf-8"))
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

    def configurations_count(self) -> int:
        """Region 0xD.  `img_valid_r ? hdr_n_config_r : 64'd0`."""
        return self._n_config if self.valid else 0

    def locate(self, cfg: int, dtype: int, index: int) -> int | None:
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
    def descriptor_bytes(dtype: int, index: int, length: int) -> bytes:
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

class _Echoed(NamedTuple):
    """The command fields the response sends straight back: the requester's
    address, its message type, the raw @22 word, the controller id and the
    sequence id.  They travel together because IEEE 9.2.1 says the response
    echoes them together, and splitting them into six adjacent arguments is
    how a caller swaps two of the same type without the reader noticing."""

    req_mac: bytes
    msg_type: int
    raw_ct: bytes
    ctlr_eid: bytes
    seq: bytes


class AecpEngineModel:
    """One AECP command in, one Ethernet frame or nothing out.

    READ_DESCRIPTOR carrying its operands runs the descriptor microprogram,
    IDENTIFY_NOTIFICATION and a truncated READ_DESCRIPTOR run the
    BAD_ARGUMENTS echo, declared commands enter the served inventory, and the
    remainder runs the NOT_IMPLEMENTED echo. A response arriving as input and
    a command for another entity are freed without a reply.

    `served` is the opcode inventory this engine answers for real, keyed by
    opcode - `aecp_engine_steps.SERVED`. It is a CONSTRUCTOR ARGUMENT and not
    a module constant here on purpose: that table is the suite's declaration,
    gated against the engine RTL by the steps and against the feature ledger
    by scripts/check_feature_status.py, so it lives where those readers look
    and the mechanism is handed it.
    """

    def __init__(self, served, image=None, entity_id=ENTITY_ID,
                 own_mac=OWN_MAC):
        self.served = served
        self.image = image if image is not None else DescriptorImage()
        self.entity_id = entity_id
        self.own_mac = own_mac
        self.cmd_count = 0
        self.resp_count = 0
        self.drop_count = 0
        self.last_oversize = False

    # -- the pop face -------------------------------------------------------
    def deliver(self, frame: bytes) -> bytes | None:
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
        elif (msg_type == MT_AEM_COMMAND) and (opcode in self.served):
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
        echoed = _Echoed(req_mac, msg_type, raw_ct, ctlr_eid, seq)
        return self._assemble(echoed, status, buf, pld)

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
            row = self.served[self.opcode_served]
            #! START/STOP_STREAMING are the one served pair whose verdict is
            #! keyed on the PAYLOAD, so the inventory's single verdict cannot
            #! be the whole answer: Milan 5.4.2.19/.20 serve a Stream Input
            #! and refuse every other target with NOT_SUPPORTED. Without this
            #! the model answered NOT_SUPPORTED for a STREAM_INPUT too, and a
            #! scenario sweeping descriptor types passed on every row - the
            #! expected value was a constant, so the check could not fail.
            #! The SUCCESS arm's payload is not modelled (it moves state in
            #! the ACMP binding record); pp_top W21 and milan_dp own that.
            #!
            #! `cfg_ix` is the @24 WORD, named for READ_DESCRIPTOR's meaning
            #! of it - which is exactly the register the engine compares
            #! (`cfg_ix_r != DT_STREAM_INPUT_C`), so the model and the RTL
            #! read the same field of the same command.
            if self.opcode_served in (OP_START_STREAMING, OP_STOP_STREAMING):
                verdict = (ST_SUCCESS if cfg_ix == DT_STREAM_INPUT
                           else ST_NOT_SUPPORTED)
                return verdict, 16
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
    def _assemble(self, echoed, status, buf, pld):
        req_mac, cmd_msg_type, raw_ct, ctlr_eid, seq = echoed
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

class FrameEnvelope(NamedTuple):
    """Who a command frame is addressed to, and how it is sized and numbered.

    Every field is what a controller would use unless a scenario says
    otherwise, so a fixture names only the one it is varying.
    """

    target_eid: int = ENTITY_ID
    ctlr_eid: int = CONTROLLER_EID
    seq: int = 0x1234
    cdl: int = None
    src_mac: bytes = CONTROLLER_MAC
    dst_mac: bytes = OWN_MAC


def build_command(msg_type: int, ct_word: int, payload: bytes,
                  **envelope: int | bytes | None) -> bytes:
    """One AECP command frame.  `ct_word` is the raw 16-bit field at @22, and
    the keywords are `FrameEnvelope`'s: any the caller does not name keep the
    address, sequence and length a controller would have used."""
    target_eid, ctlr_eid, seq, cdl, src_mac, dst_mac = FrameEnvelope(**envelope)
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


def build_read_descriptor(cfg: int, dtype: int, index: int,
                          **kw: int | bytes | None) -> bytes:
    """A READ_DESCRIPTOR carrying the whole eight-octet operand block.

    configuration_index, reserved, descriptor_type, descriptor_index - the
    shape a control_data_length below 20 cannot hold, which is what makes
    the short form BAD_ARGUMENTS instead of a locate of whatever zeros
    happened to be there.
    """
    payload = struct.pack(">HHHH", cfg, 0, dtype, index)
    return build_command(MT_AEM_COMMAND, OP_READ_DESCRIPTOR, payload, **kw)


def build_aem_command(opcode: int, payload: bytes | None = None,
                      **kw: int | bytes | None) -> bytes:
    """An AEM command for one opcode, carrying the sweep's generic operands.

    Those eight default octets are READ_DESCRIPTOR's selector for
    ENTITY[0].  The inventory records what each served opcode answers to
    exactly this shape - including the two setters whose value-carrying
    command it never reaches, which is why their row is a refusal.
    """
    if payload is None:
        payload = struct.pack(">HHHH", 0, 0, D_ENTITY, 0)
    return build_command(MT_AEM_COMMAND, opcode, payload, **kw)


def build_get_dynamic_info(**kw: int | bytes | None) -> bytes:
    """One legal fixed-size record requesting GET_CONFIGURATION.

    The contract model owns the served-opcode partition, not the packet-level
    record encoder. The real response records are graded byte-exactly by the
    protocol processor pp_top suite.
    """
    record = struct.pack(">HHBBH", 0, 0, ST_SUCCESS, 0, 0x0007)
    return build_command(MT_AEM_COMMAND, OP_GET_DYNAMIC_INFO, record, **kw)


def build_acquire_entity(owner_id: int = 0,
                         **kw: int | bytes | None) -> bytes:
    """IEEE 7.4.1: flags, owner_id, descriptor_type, descriptor_index - the
    16-octet acquire form, so the response is the 40-octet AECPDU of F06.14.
    The command carries owner_id zero. Milan Delta 7 requires the response to
    remain unowned and return NOT_SUPPORTED."""
    payload = struct.pack(">IQHH", 0, owner_id, D_ENTITY, 0)
    return build_command(MT_AEM_COMMAND, OP_ACQUIRE_ENTITY, payload, **kw)


def build_address_access(tlv_count: int = 1,
                         **kw: int | bytes | None) -> bytes:
    """IEEE 9.4.2: tlv_count at @22, tlv_data from @24.  One READ TLV is
    mode+length (2 octets) and address (8), with no memory_data."""
    tlv = struct.pack(">HQ", (0 << 12) | 0, 0x0000_0000_DEAD_BEEF)
    return build_command(MT_AA_COMMAND, tlv_count, tlv * tlv_count, **kw)


def build_mvu_command(mvu_command_type: int = MVU_GET_MILAN_INFO,
                      **kw: int | bytes | None) -> bytes:
    """F06.11: protocol_id spans @22..@27, so its first two octets ride the
    header field the engine echoes and its last four ride the payload."""
    ct_word = (MILAN_PROTOCOL_ID[0] << 8) | MILAN_PROTOCOL_ID[1]
    payload = MILAN_PROTOCOL_ID[2:6] + struct.pack(">HH", mvu_command_type, 0)
    return build_command(MT_VU_COMMAND, ct_word, payload, **kw)


# ---------------------------------------------------------------------------
# response decoding + well-formedness
# ---------------------------------------------------------------------------

def decode(frame: bytes) -> dict[str, int | bytes]:
    """Every field of a RESPONSE frame, at the offsets IEEE 9.2.2 fixes.

    Read positionally and never searched for: the AECP header is fixed
    layout, so a field the engine placed one octet out arrives here as a
    wrong value rather than as a decode that quietly gives up.
    """
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


def complaints(frame: bytes | None, cmd_frame: bytes,
               entity_id: int = ENTITY_ID) -> list[str]:
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


def decode_command(frame: bytes) -> dict[str, int | bytes]:
    """The command's own AECPDU fields, the reference a response is judged against.

    Deliberately not `decode`: a command carries no status and no `u` bit,
    so this stops at the fields that mean something on the way in.
    """
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
