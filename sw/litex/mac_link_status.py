# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The reset of the MAC link-status word, milan_mac_link_status (MAC_STATUS 0x110).

[`milan_soc.py`](milan_soc.py)'s MilanMAC resets the word's fields from here.
The word's link_up bit is the datapath's i_link_up, a factor of its effective
link (eff_link_w in hdl/milan/milan_datapath.sv). Every consumer of that link
reads it: the gPTP plane's port enable, the fabric MAAP engine, the mailbox's
LINK level and the AVB_INTERFACE link counters.

#972: where firmware owns the PHY, the word resets to link down. That is the
split placement (--ctrl-mailbox) with an MDIO pair. Its firmware publishes the
PHY's verified link (sw/firmware/ctrl/plat/ctrl_plat_phy.h). So from the
datapath's reset to that publication, nothing transmits on the link. This holds
after a reload that kept the PHY's link, and on a boot that firmware refuses
before its PHY poll starts.

Without firmware PHY management, the word keeps its reset at link up, the
constant it replaced. That is the all-fabric placement, and any board without
an MDIO pair. Nothing publishes the link there.

Nothing here imports LiteX, so a harness reads the same reset without it
(tb/verilator/milan_dp's linkreset leg, the split boot simulation).
"""

#: The word's fields: (name, bit offset, width).
FIELDS = (("link_up", 0, 1), ("speed", 1, 2), ("full_duplex", 3, 1))


def link_up_reset(fw_link_owner: bool) -> int:
    """MAC_STATUS[0]'s reset: link down where firmware owns the PHY (#972), else link up."""
    return 0 if fw_link_owner else 1


def speed_reset(phy_model: str) -> int:
    """MAC_STATUS[2:1]'s reset, the board's PHY wiring: mii 100 Mb/s (1), gmii 1000 Mb/s (2)."""
    return 0b01 if phy_model == "mii" else 0b10


def full_duplex_reset() -> int:
    """MAC_STATUS[3]'s reset: full duplex."""
    return 1


def word_reset(phy_model: str, fw_link_owner: bool) -> int:
    """The whole word's reset, its fields at their offsets."""
    values = {"link_up": link_up_reset(fw_link_owner), "speed": speed_reset(phy_model),
              "full_duplex": full_duplex_reset()}
    return sum(values[name] << offset for name, offset, _width in FIELDS)


if __name__ == "__main__":
    import sys
    # the reset a harness elaborates: `mac_link_status.py <phy_model> <owner 0|1>` prints link_up's, then the word's
    model, owner = sys.argv[1], sys.argv[2] == "1"
    print(link_up_reset(owner), word_reset(model, owner))
