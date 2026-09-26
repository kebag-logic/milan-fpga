# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The generated words the bare-metal firmware programs at boot (#398).

``configure_fabric()`` in
[`sw/firmware/milan_baremetal/milan_baremetal.c`](../firmware/milan_baremetal/milan_baremetal.c)
writes the entity identity, the station MAC, the talker count, the lwSRP words
and the CRF talker's control word from ``generated/soc.h`` constants, and
[`sw/litex/milan_soc.py`](milan_soc.py) publishes every entry of
``fabric_constants()`` with ``add_constant``. The inputs are the two files the
end-station builder writes for one config, ``aem_overlay.json`` and
``lwsrp_table.json``. Nothing here imports LiteX, so the builder gate that
runs ``configure_fabric()`` on a host (gate 35) compiles the firmware against
the values a real build hands it rather than a second reading of the config.
"""
from typing import Any

#: ``CRFT_CTRL`` (``0x750``): ``[0]`` enables the CRF talker, ``[1]`` declares
#: and tags its stream as SR class A (Milan v1.2 7.3.3). See
#: docs/reference/REGISTER_MAP.md.
CRFT_TALKER_ENABLE = 0x1
CRFT_CLASS_A_DECLARE = 0x2


def crf_output_declared(overlay: dict[str, Any]) -> bool:
    """Whether the config declares a CRF Media Clock Output.

    ``clocking.crf_output.enabled`` reaches the overlay as exactly one
    STREAM_OUTPUT of kind ``crf``, appended after the AAF talkers, and as
    nothing at all when the key is false or absent.
    """
    return any(s.get("kind") == "crf" for s in overlay["stream_outputs"])


def fabric_constants(overlay: dict[str, Any],
                     lwsrp: dict[str, Any]) -> dict[str, int]:
    """Every generated ``MILAN_*`` word ``configure_fabric()`` writes, by name,
    in the order ``milan_soc.py`` emits them."""
    eid = int(overlay["adp"]["entity_id"], 16)
    mid = int(overlay["entity"]["entity_model_id"], 16)
    mac = bytes.fromhex(overlay["adp"]["mac_address"].replace(":", ""))
    reset_words = lwsrp["reset_words"]
    return {
        "MILAN_ENTITY_ID_LO": eid & 0xFFFF_FFFF,
        "MILAN_ENTITY_ID_HI": eid >> 32,
        "MILAN_MODEL_ID_LO": mid & 0xFFFF_FFFF,
        "MILAN_MODEL_ID_HI": mid >> 32,
        "MILAN_STATION_MAC_LO": int.from_bytes(mac[:4], "little"),
        "MILAN_STATION_MAC_HI": int.from_bytes(mac[4:], "little"),
        "MILAN_N_TALKERS": sum(s.get("kind", "aaf") == "aaf"
                               for s in overlay["stream_outputs"]),
        "MILAN_SR_VID": int(reset_words["LWSRP_VID"], 16),
        "MILAN_LWSRP_CTRL_RESET": int(reset_words["LWSRP_CTRL"], 16),
        # Neutral hardware resets; firmware supplies this shape's policy.
        "MILAN_AAF_CTRL_BOOT": (int(reset_words["LWSRP_VID"], 16) << 16) | 1,
        "MILAN_MAAP_CTRL_BOOT": (len(overlay["stream_outputs"]) << 8) | 1,
        # Existing accept-all posture, even with the filter hardware present.
        "MILAN_MAC_CTRL_SET": 1 << 3,
        "MILAN_TCAM_CTRL_BOOT": 1,
        # clocking.crf_output.enabled owns the CRF talker: a declared output
        # runs as a class-A stream, and an undeclared one leaves CRFT_CTRL[0]
        # clear and declares nothing.
        "MILAN_CRF_TX_CTRL_BOOT": (
            CRFT_TALKER_ENABLE | CRFT_CLASS_A_DECLARE
            if crf_output_declared(overlay) else 0),
    }
