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
# WHERE IT LIVES.  The mechanism - the descriptor store, the command path, the
# command frames and the response decoder - is `aecp_engine_model.py`, beside
# this file.  What stays HERE is the pair of things that are not mechanism:
# the SERVED inventory below, which is this suite's declaration of what the
# device answers and is read as source by the step that compares it to the
# engine RTL and by scripts/check_feature_status.py, and the scenarios.  The
# standing recorded in this header governs both files.
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

from __future__ import annotations

import struct
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from behave import given, when, then

if TYPE_CHECKING:  # behave is a test-only dependency; the annotation is lazy
    from behave.runner import Context

#! The model this file judges lives beside it. behave puts the steps
#! directory on sys.path itself, but the insert is spelled out so the module
#! also imports under a plain `python3 -c "import aecp_engine_steps"`.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from aecp_engine_model import (  # noqa: E402
    ROOT,
    AecpEngineModel,
    DescriptorImage,
    D_ENTITY,
    FRAME_HDR,
    MILAN_PROTOCOL_ID,
    MT_AA_RESPONSE,
    MT_AEM_COMMAND,
    MT_AEM_RESPONSE,
    MT_VU_COMMAND,
    MT_VU_RESPONSE,
    OP_GET_DYNAMIC_INFO,
    OP_IDENTIFY_NOTIFICATION,
    OP_READ_DESCRIPTOR,
    OP_SET_NAME,
    ST_BAD_ARGUMENTS,
    ST_NOT_IMPLEMENTED,
    ST_NOT_SUPPORTED,
    ST_SUCCESS,
    build_acquire_entity,
    build_address_access,
    build_aem_command,
    build_command,
    build_get_dynamic_info,
    build_mvu_command,
    build_read_descriptor,
    complaints,
    decode,
    decode_command,
)

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
    #! The two setters answer the SWEEP's 8-byte READ_DESCRIPTOR-shaped
    #! command with BAD_ARGUMENTS at their response's own length: both are
    #! value-carrying commands whose floor the sweep's cdl-20 shape never
    #! reaches, and a refusal has to be the size of the response it refuses.
    #! SET_STREAM_INFO's shape is 1722.1-2021 Figure 7-40 - Milan v1.2
    #! references the 2021 edition, so its complete body is 84 payload bytes
    #! and the refusal answers at cdl 96 (the 2013 60-byte shape is itself a
    #! truncated command on the real engine; pp_top W24g pins that). The
    #! rich payload-keyed behavior (per-descriptor STREAM_IS_RUNNING, the
    #! format verdict, the exact-flag rule, the bit-31 range) moves state
    #! this model does not carry; pp_top W23/W24/W25 and milan_dp own it on
    #! the real engine.
    0x0008: dict(name="SET_STREAM_FORMAT", clause="Milan 5.4.2.7",
                 verdict=ST_BAD_ARGUMENTS, cdl=24),
    0x0009: dict(name="GET_STREAM_FORMAT", clause="Milan 5.4.2.8",
                 verdict=ST_SUCCESS, cdl=24),
    0x000E: dict(name="SET_STREAM_INFO", clause="Milan 5.4.2.9",
                 verdict=ST_BAD_ARGUMENTS, cdl=96),
    0x000F: dict(name="GET_STREAM_INFO", clause="Milan 5.4.2.10",
                 verdict=ST_SUCCESS, cdl=68),     # the Milan 80-byte form
    0x0010: dict(name="SET_NAME", clause="Milan 5.4.2.11",
                 verdict=ST_SUCCESS, cdl=84),
    0x0011: dict(name="GET_NAME", clause="Milan 5.4.2.12",
                 verdict=ST_SUCCESS, cdl=84),
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
    #! NOT MODELLED for these two, and deliberately: the RTL also answers
    #! NO_SUCH_DESCRIPTOR for a STREAM_INPUT index the image does not hold,
    #! ENTITY_LOCKED for a different controller under lock, and BAD_ARGUMENTS
    #! below cdl 16. This model answers SUCCESS for a STREAM_INPUT at ANY
    #! index and models neither refusal, because it carries no descriptor
    #! image and no lock state. No scenario sweeps index or lock today, so
    #! nothing is falsely green - but anyone adding such a sweep must teach
    #! the model those arms first, or it will disagree with the gateware and
    #! the RTL will be the one that looks wrong. pp_top W21o/W21x/W21q grade
    #! all three on the real engine.
    #!
    #! Milan narrows IEEE 7.4.35/7.4.36 to Stream Inputs, so the verdict the
    #! SWEEP sees is NOT_SUPPORTED: its payload is READ_DESCRIPTOR-shaped
    #! zeros, which puts descriptor_type 0x0000 (ENTITY) at @24, and anything
    #! that is not a STREAM_INPUT takes the refusal arm. A bound Stream Input
    #! answers SUCCESS at the same cdl - Figure 7-59 gives command and
    #! response one shape - and pp_top's W21 grades that byte-exactly.
    0x0022: dict(name="START_STREAMING", clause="Milan 5.4.2.19",
                 verdict=ST_NOT_SUPPORTED, cdl=16),
    0x0023: dict(name="STOP_STREAMING", clause="Milan 5.4.2.20",
                 verdict=ST_NOT_SUPPORTED, cdl=16),
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
    0x002C: dict(name="ADD_AUDIO_MAPPINGS", clause="Milan 5.4.2.27",
                 verdict=ST_SUCCESS, cdl=None),   # 20 + 8 x mappings
    0x002D: dict(name="REMOVE_AUDIO_MAPPINGS", clause="Milan 5.4.2.28",
                 verdict=ST_SUCCESS, cdl=None),   # 20 + 8 x mappings
    0x004B: dict(name="GET_DYNAMIC_INFO", clause="Milan 5.4.2.29",
                 verdict=ST_SUCCESS, cdl=None),   # 12 + packed records
}

#! the engine's own path to the RTL, resolved from this file so the gate works
#! from any working directory behave is launched in
_ENGINE_SV = (ROOT / "protocol-processor" / "hdl" / "aecp"
              / "KL_aecp_engine.sv")


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
def step_engine_milan8(context: Context) -> None:
    """A validated store holding the worked example: one configuration, eight descriptors."""
    context.aecp = AecpEngineModel(SERVED, DescriptorImage())
    context.aecp_rsp = None
    context.aecp_cmd = None


@given('the protocol-processor AECP engine before software loads the image')
def step_engine_unloaded(context: Context) -> None:
    """The store validates magic + layout version + checksum before it serves
    anything; until then region 0xD reads zero and every locate misses."""
    context.aecp = AecpEngineModel(SERVED, DescriptorImage(valid=False))
    context.aecp_rsp = None
    context.aecp_cmd = None


@given('the AECP image declares {n:d} configurations')
def step_engine_nconfig(context: Context, n: int) -> None:
    """Re-declare region 0xD's count, leaving the descriptor entries in place.

    The locate has to stay able to succeed, or a scenario cannot tell a
    configuration_index refused by the range check from one that missed.
    """
    context.aecp.image = DescriptorImage(configurations_count=n)


# ---------------------------------------------------------------------------
# Steps - commands
# ---------------------------------------------------------------------------

@when('the controller reads descriptor type {dtype:d} index {index:d} '
      'in configuration {cfg:d}')
def step_read_descriptor(context: Context, dtype: int, index: int, cfg: int) -> None:
    """A complete READ_DESCRIPTOR for one descriptor, delivered to the engine."""
    _send(context, build_read_descriptor(cfg, dtype, index))


@when('the controller sends a READ_DESCRIPTOR of control_data_length {cdl:d}')
def step_read_descriptor_short(context: Context, cdl: int) -> None:
    """A command whose declared cdl cannot carry the 8 operand octets."""
    payload = b"\x00" * max(cdl - 12, 0)
    _send(context, build_command(MT_AEM_COMMAND, OP_READ_DESCRIPTOR, payload,
                                 cdl=cdl))


@when('the controller sends AEM opcode {opcode:d} to the AECP engine')
def step_send_aem(context: Context, opcode: int) -> None:
    """One AEM command for a bare opcode, so the dispatch decision is what is graded."""
    _send(context, build_aem_command(opcode))


@when('the controller sends AEM opcode {opcode:d} naming descriptor type '
      '{dtype:d} to the AECP engine')
def step_send_aem_dtype(context: Context, opcode: int, dtype: int) -> None:
    """IEEE Figure 7-59's four bytes: {descriptor_type, descriptor_index}.

    START/STOP_STREAMING carry the descriptor type at @24, not at @28 like
    the READ_DESCRIPTOR shape, so the payload is built here rather than
    reusing `build_aem_command`'s eight-byte default - which would put the
    type in the wrong field and make every row pass for the wrong reason
    (a zero at @24 is ENTITY, which is refused too).
    """
    payload = bytes((dtype >> 8, dtype & 0xFF, 0x00, 0x00))
    _send(context, build_command(MT_AEM_COMMAND, opcode, payload))


@when('the controller sends ACQUIRE_ENTITY to the AECP engine')
def step_send_acquire(context: Context) -> None:
    """ACQUIRE_ENTITY in its 16-octet form, the command Milan Delta 7 never grants."""
    _send(context, build_acquire_entity())


@when('the controller sends an ADDRESS_ACCESS command to the AECP engine')
def step_send_aa(context: Context) -> None:
    """An ADDRESS_ACCESS command, whose @22 word is a tlv_count and not a command_type."""
    _send(context, build_address_access())


@when('the controller sends the Milan MVU command to the AECP engine')
def step_send_mvu(context: Context) -> None:
    """The Milan vendor-unique command, whose protocol_id straddles @22 and the payload."""
    _send(context, build_mvu_command())


@when('the controller sends a VENDOR_UNIQUE command whose protocol_id '
      'starts {oui_hi} to the AECP engine')
def step_send_vu_oui(context: Context, oui_hi: str) -> None:
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


@when('the controller sends a message_type {mt:d} command whose word at 22 '
      'is {word} to the AECP engine')
def step_send_non_aem(context: Context, mt: int, word: str) -> None:
    """A non-AEM message whose @22..@23 collides with an AEM opcode.

    VENDOR_UNIQUE is not the only type with something other than a
    command_type there: AVC_COMMAND carries an `avc_length` (Figure 9-9),
    ADDRESS_ACCESS a `tlv_count` (9.4.2.1), and the RX validator files every
    type it does not recognise into the AEM bucket.
    """
    payload = struct.pack(">IHH", 0xAABBCCDD, 0, 0)
    context.vu_oui_payload = payload
    _send(context, build_command(mt, int(word, 0), payload))


@then('the AECP response protocol_id is echoed whole')
def step_vu_protocol_id_whole(context: Context) -> None:
    """Both halves of the 48-bit protocol_id came back unaltered, head and tail."""
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
def step_send_foreign(context: Context, eid: str) -> None:
    """A command addressed to another entity, which this one must free unanswered."""
    _send(context, build_aem_command(OP_READ_DESCRIPTOR,
                                     target_eid=int(eid, 0)))


@when('an AECP {kind} arrives at the AECP engine as input')
def step_send_response_as_input(context: Context, kind: str) -> None:
    """An AECP RESPONSE fed in as if received - the response-storm case, per type."""
    mt = {"AEM response": MT_AEM_RESPONSE,
          "VENDOR_UNIQUE response": MT_VU_RESPONSE,
          "ADDRESS_ACCESS response": MT_AA_RESPONSE}[kind]
    _send(context, build_command(mt, OP_READ_DESCRIPTOR,
                                 struct.pack(">HHHH", 0, 0, D_ENTITY, 0)))


@when('the controller sweeps AEM opcodes {lo:d} to {hi:d} plus {extra:d}')
def step_sweep(context: Context, lo: int, hi: int, extra: int) -> None:
    """One valid command per opcode across the complete dispatch partition.

    The generic eight-byte selector is valid for every served row except
    SET_NAME, whose command includes the complete 64-byte replacement name.
    """
    context.aecp_sweep = []
    for op in list(range(lo, hi + 1)) + [extra]:
        if op == OP_GET_DYNAMIC_INFO:
            cmd = build_get_dynamic_info()
        elif op == OP_SET_NAME:
            cmd = build_aem_command(op, bytes(72))
        else:
            cmd = build_aem_command(op)
        context.aecp_sweep.append((op, cmd, context.aecp.deliver(cmd)))


# ---------------------------------------------------------------------------
# Steps - the answer
# ---------------------------------------------------------------------------

@then('the AECP response status is {status:d}')
def step_status(context: Context, status: int) -> None:
    """The status the engine actually put on the wire, decoded back off the frame."""
    got = _rsp(context)["status"]
    assert got == status, "AECP status %d, expected %d" % (got, status)


@then('the AECP response message_type is {mt:d}')
def step_message_type(context: Context, mt: int) -> None:
    """The response's message_type nibble, as IEEE Table 9-1 numbers it."""
    got = _rsp(context)["message_type"]
    assert got == mt, "AECP message_type %d, expected %d" % (got, mt)


@then('the AECP response message_type is the command type plus one')
def step_message_type_plus_one(context: Context) -> None:
    """A response is its command's type plus one, whatever that type was.

    Stated as the relation and not as a number, so an ADDRESS_ACCESS or
    VENDOR_UNIQUE command is graded by the same rule instead of by a
    constant that only happens to be right for AEM.
    """
    got = _rsp(context)["message_type"]
    want = decode_command(context.aecp_cmd)["message_type"] + 1
    assert got == want, "AECP message_type %d, expected %d" % (got, want)


@then('the AECP response control_data_length is {cdl:d}')
def step_cdl(context: Context, cdl: int) -> None:
    """The response's control_data_length, the size law a controller checks a payload against."""
    got = _rsp(context)["control_data_length"]
    assert got == cdl, "control_data_length %d, expected %d" % (got, cdl)


@then('the AECP response control_data_length counts its own payload')
def step_cdl_counts_payload(context: Context) -> None:
    """control_data_length is never a claim about octets the frame does not carry."""
    r = _rsp(context)
    carried = len(context.aecp_rsp) - FRAME_HDR
    assert r["control_data_length"] - 12 <= carried, \
        "control_data_length claims %d payload octets, the frame carries %d" \
        % (r["control_data_length"] - 12, carried)
    assert r["control_data_length"] == 12 + len(r["payload"]), \
        "control_data_length %d does not equal 12 + payload %d" \
        % (r["control_data_length"], len(r["payload"]))


@then('the AECP response AECPDU is {n:d} octets')
def step_aecpdu_len(context: Context, n: int) -> None:
    """The whole AECPDU, cdl + 12, which the F06.14 master table fixes per command."""
    got = _rsp(context)["control_data_length"] + 12
    assert got == n, "AECPDU %d octets (cdl + 12), expected %d" % (got, n)


@then('the AECP response carries the command payload verbatim')
def step_echo_verbatim(context: Context) -> None:
    """The answer replayed the command's own payload, at the command's own length.

    That is what the echo pre-load buys: a refusal is the command
    reflected, not a body this engine had to invent a size for.
    """
    r = _rsp(context)
    want = decode_command(context.aecp_cmd)["payload"]
    assert r["payload"] == want, \
        "echo payload %s, command carried %s" % (r["payload"].hex(), want.hex())


@then('the AECP response echoes command_type {op:d} with u clear')
def step_echo_command_type(context: Context, op: int) -> None:
    """The command_type came back, with u clear - the mark of a solicited response."""
    r = _rsp(context)
    assert r["command_type"] == op, \
        "command_type %#06x, expected %#06x" % (r["command_type"], op)
    assert r["u"] == 0, "u set on a solicited response"


@then('the AECP response is unicast back to the requester from our own MAC')
def step_unicast(context: Context) -> None:
    """IEEE 9.2.1: the answer goes back to the requester alone, from our own MAC."""
    r = _rsp(context)
    c = decode_command(context.aecp_cmd)
    assert r["dst_mac"] == c["src_mac"], \
        "destination %s, requester was %s" % (r["dst_mac"].hex(),
                                              c["src_mac"].hex())
    assert r["src_mac"] == context.aecp.own_mac, \
        "source %s, our MAC is %s" % (r["src_mac"].hex(),
                                      context.aecp.own_mac.hex())


@then('the AECP response echoes the sequence_id and the controller_entity_id')
def step_echo_identity(context: Context) -> None:
    """sequence_id and controller_entity_id came back unchanged, so the controller can pair the two."""
    r = _rsp(context)
    c = decode_command(context.aecp_cmd)
    assert r["sequence_id"] == c["sequence_id"], \
        "sequence_id %d, command sent %d" % (r["sequence_id"], c["sequence_id"])
    assert r["controller_entity_id"] == c["controller_entity_id"], \
        "controller_entity_id %#018x, command sent %#018x" \
        % (r["controller_entity_id"], c["controller_entity_id"])


@then('the AECP response target_entity_id is our own')
def step_target_is_ours(context: Context) -> None:
    """The response names this entity as the target, not the controller that asked."""
    got = _rsp(context)["target_entity_id"]
    assert got == context.aecp.entity_id, \
        "target_entity_id %#018x, ours is %#018x" % (got, context.aecp.entity_id)


@then('the AECP response is well formed against its command')
def step_wellformed(context: Context) -> None:
    """`complaints` is empty: every 9.2.1/9.2.2 rule at once, not a sampled few."""
    bad = complaints(context.aecp_rsp, context.aecp_cmd,
                     context.aecp.entity_id)
    assert not bad, "malformed response: " + "; ".join(bad)


@then('the AECP response configuration_index is {cfg:d} and the reserved '
      'halfword is zero')
def step_cfg_and_reserved(context: Context, cfg: int) -> None:
    """The 7.4.5 prefix: configuration_index echoed back, reserved halfword zero."""
    p = _rsp(context)["payload"]
    assert len(p) >= 4, "payload %d octets, too short for the 7.4.5 prefix" % len(p)
    got = struct.unpack(">H", p[0:2])[0]
    assert got == cfg, "configuration_index %d, expected %d" % (got, cfg)
    assert p[2:4] == b"\x00\x00", "reserved halfword %s" % p[2:4].hex()


@then('the AECP response descriptor is {n:d} octets opening with type {dtype:d} '
      'index {index:d}')
def step_descriptor(context: Context, n: int, dtype: int, index: int) -> None:
    """The served descriptor is the image's own bytes, whole and at the stated length.

    Compared against `descriptor_bytes` rather than against its first four
    octets, which is what makes a short, shifted or missing copy visible
    instead of plausible.
    """
    p = _rsp(context)["payload"]
    desc = p[4:]
    assert len(desc) == n, "descriptor %d octets, expected %d" % (len(desc), n)
    assert desc[0:4] == struct.pack(">HH", dtype, index), \
        "descriptor opens %s, expected type %d index %d" \
        % (desc[0:4].hex(), dtype, index)
    assert desc == DescriptorImage.descriptor_bytes(dtype, index, n), \
        "the served descriptor is not the image's bytes"


@then('the AECP response carries the 7.4.5 stub for type {dtype:d} index {index:d}')
def step_stub(context: Context, dtype: int, index: int) -> None:
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
def step_no_frame(context: Context) -> None:
    """The engine stayed silent; a refusal that answers is a storm, not a refusal."""
    assert context.aecp_rsp is None, \
        "the engine answered %d octets where it must stay silent: %s" \
        % (len(context.aecp_rsp), context.aecp_rsp[:24].hex())


@then('the AECP engine counted a drop and no command')
def step_counted_drop(context: Context) -> None:
    """A refused frame moved the drop counter and left the command counter alone.

    Silence is only defensible when it is counted: an uncounted drop cannot
    be told apart from a frame that never arrived.
    """
    cmd0, _resp0, drop0 = context.aecp_before
    assert context.aecp.drop_count == drop0 + 1, \
        "drop counter %d, was %d" % (context.aecp.drop_count, drop0)
    assert context.aecp.cmd_count == cmd0, \
        "command counter advanced to %d on a refused frame" % context.aecp.cmd_count


@then('the AECP engine counted a command and a response')
def step_counted_command(context: Context) -> None:
    """An answered command moved the command and response counters, and no drop."""
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
def step_sweep_answered(context: Context) -> None:
    """No swept opcode was met with silence, so the dispatch partition is total."""
    silent = [op for op, _c, r in context.aecp_sweep if r is None]
    assert not silent, \
        "%d opcodes were met with silence: %s" % (len(silent), silent[:8])


@then('every swept answer is well formed against its command')
def step_sweep_wellformed(context: Context) -> None:
    """Every swept answer meets the rules the single-command case is held to."""
    bad = []
    for op, cmd, rsp in context.aecp_sweep:
        for c in complaints(rsp, cmd):
            bad.append("opcode %#06x: %s" % (op, c))
    assert not bad, "%d malformed answers: %s" % (len(bad), "; ".join(bad[:5]))


@then('the swept opcodes partition into the served set and the '
      'NOT_IMPLEMENTED remainder')
def step_sweep_partition(context: Context) -> None:
    """The sweep splits into the served inventory and the NOT_IMPLEMENTED remainder, and records both sizes."""
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
def step_inventory_matches_rtl(context: Context) -> None:
    """The anti-staleness gate: parse the engine's own opcode localparams and
    compare them to SERVED.  This is the check that would have caught the
    twelve commands this suite went on calling NOT_IMPLEMENTED for three days
    after they landed."""
    import re
    assert _ENGINE_SV.exists(), \
        "the engine RTL is not readable at %s - the submodule is probably " \
        "not checked out, and an unreadable gate is a SKIP, never a PASS" \
        % _ENGINE_SV
    text = _ENGINE_SV.read_text(encoding="utf-8", errors="replace")
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
def step_sweep_echo(context: Context) -> None:
    """Only the echo paths replay the command bytes; a served opcode builds its own body."""
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
def step_protocol_id(context: Context) -> None:
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
def step_owner_id(context: Context) -> None:
    """7.4.1 puts owner_id at payload offset 4, right after the 4-octet flags.
    Milan Delta 7: the entity never grants an acquisition, so it answers zero
    there."""
    p = _rsp(context)["payload"]
    assert len(p) >= 12, \
        "payload %d octets, too short for the 16-octet ACQUIRE form" % len(p)
    owner = int.from_bytes(p[4:12], "big")
    assert owner == 0, \
        "owner_id %#018x, Milan Delta 7 wants zero" % owner
