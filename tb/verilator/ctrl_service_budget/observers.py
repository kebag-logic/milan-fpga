# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The testbench's observed modules and where the generated model keeps them (build.py binds sim_main.cpp to them),
and the MRP participants' registry the testbench keeps from the CPU's register file (#665, PR #934).

Each MRP timer's expiry is reported with the participant that owns it, read at the expiry itself: the callback's
argument, a0 at its entry, is its participant's timer_arg, which lwSRP registers with shlan_timer_init inside
msrp_app_create or mvrp_app_create, and the SRP adapter then publishes that interface's Domain
(mbx_pub_domain(index, false, ...); srp_mbx.c, create_participants). sim_main.cpp binds each argument there to its
interface and application (note_owner), and names the owner at every timer's entry (owner_of)."""
from __future__ import annotations

import re
from pathlib import Path

#: Each observed module, the instance name it has inside the mailbox, and one of its observed variables; the CPU's
#: integer register file among them, its asMem_ram public in VexiiRiscv's netlist.
OBSERVED = {'VexiiRiscv': ('vexiis_0_logic_core', 'WhiteboxerPlugin_logic_commits_ports_0_valid'),
            'KL_mbx_rx': ('u_rx', 'commit_w'), 'KL_mbx_evt': ('u_evt', 'wr_en_o'),
            'RegFileMem': ('integer_RegFilePlugin_logic_regfile_fpga', 'asMem_ram')}
#: The entries whose expiry the testbench reports with the participant that owns it: the MRP timers' callbacks
#: (mrpdu_grade.TIMERS).
OWNED_ENTRIES = ('on_join_timer', 'on_pt_timer', 'on_la_timer')
#: The functions the participants' registry reads the CPU's registers at (sim_main.cpp, note_owner), by the constant
#: that names each: each application's creation, the timers' registration, the LeaveAll timer's callback the
#: registration names, and the Domain's publication that ends an interface's creation.
OWNER_HOOKS = (('msrp_create_pc', 'msrp_app_create'), ('mvrp_create_pc', 'mvrp_app_create'),
               ('timer_init_pc', 'shlan_timer_init'), ('la_timer_pc', 'on_la_timer'),
               ('pub_domain_pc', 'mbx_pub_domain'))


def owner_lines(entries: tuple[str, ...], table: dict[str, int], paths: dict[str, tuple[str, str]]) -> list[str]:
    """budget_config.hpp's lines for the registry: which entries carry their owner, each hook's pc, and the
    register file's reader."""
    path, prefix = paths['RegFileMem']
    return ['inline constexpr bool entry_owned[n_entries] = {'
            + ', '.join('true' if name in OWNED_ENTRIES else 'false' for name in entries) + '};',
            *[f'constexpr std::uint32_t {const} = 0x{table[name]:x}u;' for const, name in OWNER_HOOKS],
            f'inline std::uint32_t reg(const Vsim& dut, unsigned n) {{ return {path}->{prefix}asMem_ram[n]; }}']


def member_paths(native: Path) -> dict[str, tuple[str, str]]:
    """Each observed module's C++ path from the root, and the prefix of its variables there.

    Verilator keeps a module as its own class or inlines it into its parent,
    whose members then carry the instance path (KL_mbx__DOT__u_rx__DOT__x);
    both forms are read off the generated headers, never assumed.
    """
    edges: dict[str, list[tuple[str, str]]] = {}
    members: dict[str, str] = {}
    for header in [native / 'Vsim___024root.h', *native.glob('Vsim_*.h')]:
        text = header.read_text()
        members[header.stem] = text
        for target, name in re.findall(r'^\s*(Vsim_\w+)\*\s+(\w+);', text, re.M):
            edges.setdefault(header.stem, []).append((target, name))
    paths = {'Vsim___024root': 'dut.rootp'}
    frontier = ['Vsim___024root']
    while frontier:
        cls = frontier.pop()
        for target, name in edges.get(cls, []):
            if target not in paths:
                paths[target] = f'{paths[cls]}->{name}'
                frontier.append(target)
    found: dict[str, tuple[str, str]] = {}
    for module, (instance, var) in OBSERVED.items():
        cls = 'Vsim_' + module
        if cls in paths and re.search(rf'\b{var};', members[cls]):
            found[module] = (paths[cls], '')
            continue
        hits = [(c, m.group(1)) for c in paths if c in members
                for m in re.finditer(rf'\b(\w*__DOT__{instance}__DOT__){var};', members[c])]
        if len(hits) != 1:
            raise RuntimeError(f'observed module {module} is not reachable once from the root: {hits}')
        found[module] = (paths[hits[0][0]], hits[0][1])
    return found
