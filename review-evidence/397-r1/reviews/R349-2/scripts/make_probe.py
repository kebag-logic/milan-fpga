#!/usr/bin/env python3
"""Build a probe variant of the service-budget native driver, head files untouched.

Usage: make_probe.py <repo> <reused-build-dir> <probe-dir> <variant>
variant 'uart_paced': RX bytes and TX ready at one byte per 115,200-baud 8N1 frame.
variant 'wip_split' : 5th argv = page-program wait us (erase wait stays argv[4]).
The generated gateware, BIOS and firmware of the reused build are used read-only.
"""
import json, subprocess, sys
from pathlib import Path

repo, build, probe, variant = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
src = (repo / 'tb/verilator/fw_service_budget/sim_main.cpp').read_text()

def sub(old, new):
    global src
    assert src.count(old) == 1, old
    src = src.replace(old, new)

if variant == 'uart_paced':
    frame = '(sys_hz / 11520)'  # 10 bit times at 115,200 baud
    sub('        dut.serial_sink_valid = sending_ && send_offset_ < commands_.at(command_).size();',
        '        dut.serial_sink_valid = sending_ && send_offset_ < commands_.at(command_).size() && cycle_ >= next_rx_;\n'
        '        dut.serial_source_ready = cycle_ >= next_tx_;')
    sub('            ++send_offset_;', f'            ++send_offset_;\n            next_rx_ = cycle_ + {frame};')
    sub('        const char ch = static_cast<char>(dut.serial_source_data);',
        f'        next_tx_ = cycle_ + {frame};\n        const char ch = static_cast<char>(dut.serial_source_data);')
    sub('    std::uint64_t response_at_ = 0;', '    std::uint64_t response_at_ = 0;\n    std::uint64_t next_rx_ = 0;\n    std::uint64_t next_tx_ = 0;')
    sub('    void drive(Vsim& dut) const {', '    void drive(Vsim& dut) {')
elif variant == 'wip_split':
    sub('    Devices(const char* aem, const char* slots, const char* commands, unsigned wait_us)\n'
        '        : flash_(wait_us * (sys_hz / 1000000), wait_us * (sys_hz / 1000000)) {',
        '    Devices(const char* aem, const char* slots, const char* commands, unsigned wait_us, unsigned page_us)\n'
        '        : flash_(wait_us * (sys_hz / 1000000), page_us * (sys_hz / 1000000)) {')
    sub('if (argc != 5)', 'if (argc != 6)')
    sub('std::stoul(argv[4]));', 'std::stoul(argv[4]), std::stoul(argv[5]));')
else:
    sys.exit('unknown variant')
probe.mkdir(parents=True, exist_ok=True)
(probe / 'sim_main.cpp').write_text(src)
(probe / 'flash.hpp').write_text((repo / 'tb/verilator/fw_service_budget/flash.hpp').read_text())
spec = json.loads((build / 'service_spec.json').read_text())
(probe / 'probe_config.hpp').write_text('#pragma once\n#include <cstdint>\n' + ''.join(
    f'constexpr std::uint64_t {n} = {spec[n]};\n' for n in ('sys_hz', 'cpu_hz', 'tdm_hz')))
argv = ['verilator', '--cc', '--exe', '--build', '-j', '4', '-Wno-fatal', '-Werror-USERERROR',
        '-Wno-BLKANDNBLK', '-Wno-WIDTH', '-Wno-COMBDLY', '-Wno-CASEINCOMPLETE',
        '--top-module', 'sim', '--Mdir', str(probe / 'native'), '-O3',
        '--output-split', '5000', '--output-split-cfuncs', '500',
        '-CFLAGS', f'-O3 -std=c++17 -Wall -Wextra -I{repo}/tb/common -I{probe}',
        *['-I' + str(i) for i in spec['includes']], *spec['sources'], str(probe / 'sim_main.cpp')]
subprocess.run(argv, cwd=build / 'gateware', check=True, stdout=subprocess.DEVNULL)
print('built', probe / 'native/Vsim')
