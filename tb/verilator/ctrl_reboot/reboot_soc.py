# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The REBOOT simulation's SoC (#871): the split boot simulation's SoC, with the reset port's level and the GSI
window on pads.

boot_soc.py (tb/verilator/ctrl_split_boot, imported read only) builds the
split CPU, its firmware memory, the mailbox with its datapath on pads, the
flash, timer0, the Milan CSR window and the UART. Its devices come from
split_soc.add_devices (tb/verilator/ctrl_service_budget), which adds the split
SoC's own AECP REBOOT reset port, milan_soc.add_ctrl_reboot. This SoC adds two
pad groups, and nothing else differs:

  - `reboot`, that port's CSR level, so the testbench sees the firmware's
    request where the product crosses it into KL_reboot_ctrl;
  - `gsi`, the face block's GSI window (contract 2.3): its open request with
    its tag, kind and selector out, and its answer in. split_soc holds every
    window answer idle, so a read of the window finds none, and the AECP
    owner then refuses SET_STREAM_FORMAT and SET_STREAM_INFO, which read the
    datapath through it (aecp_face.c). The testbench answers as a datapath
    whose stream runs no traffic would: every GET_STREAM_INFO word 0, and the
    format verdict 3, supported (sim_main.cpp).

The build is boot_soc's, with platform_for, add_devices and face_ports
wrapped for the pads.
"""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'tb/verilator/ctrl_split_boot'))
import boot_soc  # noqa: E402  the split boot simulation's SoC, read only
from litex.build.generic_platform import Pins, Subsignal  # noqa: E402

split_soc = boot_soc.split_soc
#: The GSI window's pads, one interface: (name, width).
GSI_FIELDS = (('req', 1), ('tag', 4), ('kind', 2), ('sel', 4), ('ans_p', 1), ('ans_tag', 4), ('ans_data', 64))


def build(build_dir: Path, shape: str, elf: Path, n_if: int, flash_map: Path) -> dict:
    """boot_soc.build, with the reset port's level on `reboot` and the GSI window on `gsi`."""
    if n_if != 1:
        raise RuntimeError('the REBOOT simulation answers one interface\'s GSI window')
    platform_for, add_devices, face_ports = split_soc.platform_for, split_soc.add_devices, split_soc.face_ports

    def with_pads(contract: object, interfaces: int) -> object:
        """split_soc's platform with the two pad groups."""
        platform = platform_for(contract, interfaces)
        platform.add_extension([('reboot', 0, Pins(1)),
                                ('gsi', 0, *[Subsignal(n, Pins(w)) for n, w in GSI_FIELDS])])
        return platform

    def wired(soc: object, platform: object, addresses: dict, contract: object, interfaces: int) -> None:
        """split_soc's devices, the GSI window and the reset port's level on their pads."""
        pads = platform.request('gsi')

        def answered(contract_: object, interfaces_: int) -> dict:
            """split_soc's face ports, the GSI window's request out and its answer in."""
            ports = face_ports(contract_, interfaces_)
            soc.comb += [pads.req.eq(ports['o_gsi_req_o']), pads.tag.eq(ports['o_gsi_tag_o']),
                         pads.kind.eq(ports['o_gsi_kind_o']), pads.sel.eq(ports['o_gsi_sel_o'])]
            return {**ports, 'i_gsi_ans_p_i': pads.ans_p, 'i_gsi_ans_tag_i': pads.ans_tag,
                    'i_gsi_ans_data_i': pads.ans_data}

        with patch.object(split_soc, 'face_ports', answered):
            add_devices(soc, platform, addresses, contract, interfaces)
        soc.comb += platform.request('reboot').eq(soc.ctrl_reboot.req.storage)

    with patch.object(split_soc, 'platform_for', with_pads), patch.object(split_soc, 'add_devices', wired):
        return boot_soc.build(build_dir, shape, elf, n_if, flash_map)
