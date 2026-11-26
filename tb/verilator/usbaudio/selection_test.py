#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Check bus ownership before board imports, and decode the audio format."""
from __future__ import annotations

import contextlib
import importlib.util
import io
from pathlib import Path
import yaml


def main() -> None:
    root = Path(__file__).resolve().parents[3]
    spec = importlib.util.spec_from_file_location("audio_selection", root / "sw/litex/usbaudio_build.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for board in ("arty", "ax7101"):
        args = ["--board", board, "--full", "--some-existing-option", "unchanged"]
        assert module.selection(args) == (False, args), "disabled selection must preserve every argument"
    args = ["--board", "arty", "--usb-net"]
    assert module.selection(args) == (False, args), "network selection must remain independently available"
    assert module.selection(["--board", "arty", "--usb-audio"]) == (True, ["--board", "arty"])
    for args in (["--board", "arty", "--usb-net", "--usb-audio"],
                 ["--board", "ax7101", "--usb-audio"], ["--usb-audio"]):
        with contextlib.redirect_stderr(io.StringIO()):
            try:
                module.selection(args)
            except SystemExit as error:
                assert error.code == 2
            else:
                raise AssertionError("conflicting or unsupported board selection was accepted")
    cfg = yaml.safe_load((root / "configs/endstation_arty_usbaudio.yaml").read_text())
    assert cfg["clocking"]["sampling_rate_hz"] == 48000
    assert cfg["usb_audio"] == {"feedback_window_log2": 13, "digest": 0x84ff}
    for direction in ("listeners", "talkers"):
        streams = cfg["streams"][direction]
        assert len(streams) == 1 and streams[0]["channels"] == 8
        for value in streams[0].get("formats", []):
            # IEEE 1722.1 AAF format channels_per_frame field, independent
            # of the human-readable channels declaration beside it.
            assert (int(value, 0) >> 22) & 0x3ff == 8, "wire format must encode all eight channels"
    header = (root / "configs/generated/endstation_arty_usbaudio/gen/adp_shape_defaults.svh").read_text()
    assert "ADP_DMAP_IN_SCH_C [0:1] = '{10'd8, 10'd0}" in header
    assert "ADP_DMAP_OUT_SCH_C [0:0] = '{10'd8}" in header
    assert cfg["srp"]["rtl_table"] is False, "optional profile must not own shared reset defaults"
    print("PASS build selection: audio/network exclusive, Arty-only, disabled delegation and 8x8 descriptor geometry")


if __name__ == "__main__":
    main()
