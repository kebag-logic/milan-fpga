# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Build selector for mutually exclusive audio and network Arty attachments.

The standard board entry point remains untouched. With audio absent this
entry point delegates directly, including for every ALINX recipe.
"""
from __future__ import annotations

import argparse
import sys


def selection(argv: list[str]) -> tuple[bool, list[str]]:
    """Validate ownership before importing or constructing any board objects."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--usb-audio", action="store_true")
    parser.add_argument("--usb-net", action="store_true")
    parser.add_argument("--board", default="ax7101")
    selected, _ = parser.parse_known_args(argv)
    if selected.usb_audio and selected.usb_net:
        parser.error("USB audio and network are exclusive until the extra address line is wired")
    if selected.usb_audio and selected.board != "arty":
        parser.error("USB audio is supported only on Arty")
    return selected.usb_audio, [arg for arg in argv if arg != "--usb-audio"]


def main() -> None:
    """Attach the selected bus owner without editing the network build files."""
    audio, remaining = selection(sys.argv[1:])
    import milan_soc
    if audio:
        from usbaudio_soc import UsbAudio
        original = milan_soc.add_milan_datapath

        def audio_datapath(host: object, platform: object, axil: object, **kwargs: object) -> None:
            if (kwargs.get("num_streams") != 1 or kwargs.get("talker_wire_chans") != 8
                    or kwargs.get("audio_if_slots") != 8 or not kwargs.get("audio_if_master")):
                raise ValueError("USB audio needs one eight-channel stream and a TDM8 master media grid")
            host.usbaudio = UsbAudio(platform, milan_soc.REPO_ROOT, kwargs["milan_cd"])
            ports = dict(kwargs.get("extra_ports") or {})
            ports.update(host.usbaudio.ports)
            ports["p_USBAUDIO_P"] = 1
            kwargs["extra_ports"] = ports
            original(host, platform, axil, **kwargs)

        milan_soc.add_milan_datapath = audio_datapath
        # The public audio harness owns JB, JC and JD. The media oscillator
        # and grid remain internal; no legacy TDM header is requested.
        milan_soc._board_audio_ports = lambda platform: ({}, None)
    sys.argv = [sys.argv[0], *remaining]
    milan_soc.main()


if __name__ == "__main__":
    main()
