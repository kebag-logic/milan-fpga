# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ts_pads.py - the testbench's binding of contract 2.5's timestamp pads (#884, #665 F6), which build.config_header
writes into the build's header: set_ts drives one timestamp unit's record onto interface i's ts_* inputs of KL_mbx,
and ts_take reads its take pulse. A contract without the TIMESTAMP event has no such pads, and both are stubs."""
from __future__ import annotations

#: One record's bits an interface: {EGRESS, OK, MSG_TYPE, SEQ, NS}, NS lowest (KL_mbx_pkg.sv, MBX_TS_REC_BITS).
REC_BITS = 86


def cpp(has_ts: bool) -> list[str]:
    """The C++ lines of set_ts and ts_take for a contract with (has_ts) or without the TIMESTAMP event."""
    if not has_ts:
        return ['inline void set_ts(Vsim&, unsigned, bool, bool, bool, unsigned, unsigned, std::uint64_t) {}',
                'inline bool ts_take(const Vsim&, unsigned) { return false; }']
    return ['inline void set_ts(Vsim& dut, unsigned i, bool valid, bool egress, bool ok, unsigned type, '
            'unsigned seq, std::uint64_t ns) {',
            f'    const unsigned b = {REC_BITS}u * i;',
            '    auto put = [&](unsigned at, unsigned n, std::uint64_t v) {',
            '        for (unsigned k = 0; k < n; ++k) {',
            '            const unsigned bit = b + at + k;',
            '            const std::uint32_t one = static_cast<std::uint32_t>((v >> k) & 1u);',
            '            auto& w = dut.mbx_ts_data[bit / 32u];',
            '            w = (w & ~(1u << (bit % 32u))) | (one << (bit % 32u));',
            '        }',
            '    };',
            '    put(0, 64, ns); put(64, 16, seq); put(80, 4, type); put(84, 1, ok); put(85, 1, egress);',
            '    dut.mbx_ts_valid = (dut.mbx_ts_valid & ~(1u << i)) | (static_cast<unsigned>(valid) << i);',
            '}',
            'inline bool ts_take(const Vsim& dut, unsigned i) { return (dut.mbx_ts_take >> i) & 1u; }']
