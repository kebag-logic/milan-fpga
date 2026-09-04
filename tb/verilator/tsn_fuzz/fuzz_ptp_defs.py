#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""fuzz_ptp_defs.py - what the gPTP campaign is written against: the
`state_dump()` word order, the bench identities, the model list and the
model-availability probe.

The word order here MUST match cosim_ptp.cpp and is APPEND ONLY: a reordered
index does not fail the build, it silently grades the wrong word.  Shared by
`fuzz_ptp.py` and its three section modules so there is one copy of it."""
import sys
from pathlib import Path
from typing import Protocol

import cosim
import tsn_model
import wire


class FieldModel(Protocol):
    """The whole model surface the grader touches: `.fields`, in wire order.

    The campaign passes `tsn_model.Message`; `test_grade_tx.py` passes a
    one-field stand-in built for the fixture. Narrowing the grader to Message
    would make the self-test's own fixtures disagree with the signature, and
    the self-test is what proves the grader fails closed.
    """

    @property
    def fields(self) -> list[tuple[str, int, dict[str, object]]]:
        """[(name, bits, constraint)] in wire order."""


def require_ptp_models(rep: cosim.Report) -> bool:
    """Skip cleanly when tsn-gen is present but lacks the 802.1AS models.

    The `protocols/data_link/ptp/8021as_*.yaml` models are a newer tsn-gen
    addition; a pinned rev (the CI one) can have `packet_gen` and the 1722.1
    models but not these. tsn_model.available() is TRUE there, so
    require_tsn_gen passes -- but every gPTP model load would fail and the
    campaign would crash on the first `models[...]` lookup. This is the same
    honest skip as require_tsn_gen: report why the total is smaller and exit 0,
    with NO pass/fail numbers (a "0 pass, 0 fail" would read as a campaign that
    ran and checked nothing). The AAF campaign, whose models ARE in every rev,
    is unaffected.
    """
    # `tsn_model.PTP_DIR` is that module's str; it is wrapped here and the
    # message below still prints tsn_model's own spelling of it.
    probe = Path(tsn_model.PTP_DIR) / "8021as_sync.yaml"
    if probe.is_file():
        return True
    print("  SKIP: tsn-gen has no 802.1AS models at %s" % tsn_model.PTP_DIR)
    print("        this rev predates protocols/data_link/ptp/ -- update the "
          "TSN_GEN pin to enable the gPTP field campaign")
    print("SUITE-SKIP: gPTP/802.1AS field campaign (tsn-gen lacks the 802.1AS "
          "models)")
    rep.note("campaign skipped (tsn-gen 802.1AS models absent), not a failure")
    sys.exit(0)

# state_dump() word order — must match cosim_ptp.cpp (APPEND ONLY)
(S_FLAGS, S_GM_HI, S_GM_LO, S_PAR_HI, S_PAR_LO, S_PDELAY, S_OFFSET,
 S_TAPDROP, S_RXDROP, S_PHC_HI, S_PHC_LO, S_TXCNT, S_TXTSSEQ, S_TXTSCNT,
 S_PDEXP, S_PROGRUN) = range(16)

FL_PRESENT, FL_AMGM, FL_ASCAP, FL_SYNCOK = 1, 2, 4, 8

#: bench identities (mirror cosim_ptp.cpp / tb/verilator/gptp_shadow)
OUR_CID = wire.GPTP_OUR_CID
PEER_CID = wire.GPTP_PEER_CID
PEER2_CID = wire.GPTP_PEER2_CID
GMID = 0x00AACCFFFE010203
D_NOM = 600

#: one CTRL_TICK block = 10,000 cycles = 5 ms of bench time (2 MHz);
#: the engine's second — the pdelay/announce interval — is 2,000,000 cycles
MS = 2000
SECOND = 1000 * MS

MODELS = [
    ("sync",     "8021as_sync.yaml"),
    ("follow_up", "8021as_follow_up.yaml"),
    ("pdelay_req", "8021as_pdelay_req.yaml"),
    ("pdelay_resp", "8021as_pdelay_resp.yaml"),
    ("pdelay_resp_fu", "8021as_pdelay_resp_follow_up.yaml"),
    ("announce", "8021as_announce.yaml"),
]

BUILD = {
    "sync": wire.ptp_sync,
    "follow_up": wire.ptp_follow_up,
    "pdelay_req": wire.ptp_pdelay_req,
    "pdelay_resp": wire.ptp_pdelay_resp,
    "pdelay_resp_fu": wire.ptp_pdelay_resp_fu,
    "announce": wire.ptp_announce,
}

PTP_TYPE = {
    "sync": wire.PTP_SYNC, "follow_up": wire.PTP_FOLLOW_UP,
    "pdelay_req": wire.PTP_PDELAY_REQ, "pdelay_resp": wire.PTP_PDELAY_RESP,
    "pdelay_resp_fu": wire.PTP_PDELAY_RESP_FU, "announce": wire.PTP_ANNOUNCE,
}

#: header fields every builder accepts by the model's own name
HDR_FIELDS = ("transport_specific", "reserved0", "version_ptp",
              "message_length", "domain_number", "reserved1", "flags",
              "correction_field", "reserved2", "source_clock_identity",
              "source_port_number", "sequence_id", "control",
              "log_message_interval")


def extract_fields(model: FieldModel, frame: bytes) -> dict[str, int]:
    """Walk the model's field list over the frame's PDU bits (from byte 14).

    The 8021as_* models declare the FULL layout in wire order, so the walk
    IS the decode — the cross-decode section proves the premise every run.
    """
    pdu = bytes(frame[14:])
    nbits = len(pdu) * 8
    val = int.from_bytes(pdu, "big")
    out, pos = {}, 0
    for name, bits, _con in model.fields:
        if pos + bits > nbits:
            break
        out[name] = (val >> (nbits - pos - bits)) & ((1 << bits) - 1)
        pos += bits
    return out
