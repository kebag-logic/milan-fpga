#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The region-decode simulation (#791): the split CPU fetches and loads at the edges of its control regions.

Builds, all outside the checkout under --build-dir:
  1. the probe image: probe.S and the probe table run.py writes
     (probe_data.S), linked by the script run.py writes (probe.ld), with the
     RV32 compiler (sw/firmware/gtest/fw_rv32.py);
  2. the test SoC (region_soc.py) with the shipping split region list, or a
     planted decode (--mutant), and its native model (sim_main.cpp).
Then it runs the model, saves its exit status beside its log (sim.status),
and grades the log by name, for `rom` and `sram` (ctrl_memory.ROM, RAM):

  - a load at the region's last word reads its word from memory: the load
    reaches the bus, answers without err, and is the image's word (rom) or
    the word the probe stored (sram); and no trap;
  - a fetch at the last word executes it: the word is `ret`, it commits,
    and no trap;
  - a load and a fetch at each seam of the region's decode pieces
    (ctrl_memory.decode_pieces: the last word of a piece, the first of the
    next) read and execute its word;
  - a load one word past the region's end takes a load access fault
    (cause 5) whose mtval is that address, and no data command for it
    reaches the bus;
  - a fetch one word past the end takes an instruction access fault
    (cause 1) whose mtval and mepc are that address, and no fetch command
    for its line reaches the bus;
  - the probe ran every probe and stored its end word;
  - DECODE: the netlist's own fetch and load decode admit exactly the SoC's
    regions of their modes at every 32-bit address (decode.py).

The test SoC's banks fill each region's whole power-of-two window
(region_soc.full_plan), so the last word is memory and so is the word past
the end: a fault at either can only be the CPU's decode, and the
past-the-end checks also require the CPU to refuse the access before its bus.

--mutant builds a planted decode (region_soc.MUTANTS): single-mask hands the
generator the whole regions, the decode of #791; cover hands it each region's
power-of-two cover, the boot harness's old workaround. --self-test builds the
shipping decode and both mutants, each in its own directory under
--build-dir, and requires the shipping one to pass and each mutant to fail
exactly the checks KILLS names for it, in a run that reached its end word.
--regrade grades the log and status a run left in --build-dir.

Exit 0 = pass, 1 = a finding, 2 = refused.
"""
from __future__ import annotations

import argparse
import contextlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BUDGET = ROOT / 'tb/verilator/ctrl_service_budget'
sys.path.insert(0, str(ROOT / 'sw/litex'))
sys.path.insert(0, str(ROOT / 'sw/firmware/gtest'))
sys.path.insert(0, str(HERE))
import ctrl_memory  # noqa: E402
import decode  # noqa: E402

#: make's parallelism for the native model.
JOBS = 16
#: The simulated time the probe may take, in ms; it ends in well under one.
SIM_LIMIT_MS = 5
#: The report word (sram's first word) and the words the probe stores to it at its end.
REPORT = ctrl_memory.RAM.origin
DONE_WORD, HALT_WORD = 0x444F4E45, 0x48414C54
#: `ret` (jalr x0, 0(ra)), the word at every address probed inside a region.
RET = 0x00008067
#: The file a run saves the native model's exit status in, beside its log.
STATUS = 'sim.status'
K_END, K_LOAD, K_FETCH, K_STORE = 0, 1, 2, 3


class Probe(NamedTuple):
    """One access of the probe: its kind, its address, a store's value, and the check it serves."""

    kind: int
    address: int
    value: int
    check: str


def seams(region: ctrl_memory.Region) -> list[int]:
    """The words on either side of each seam between the region's decode pieces."""
    pieces = ctrl_memory.decode_pieces(region.origin, region.size)
    return [w for origin, _ in pieces[1:] for w in (origin - 4, origin)]


def names(region: ctrl_memory.Region) -> dict[str, str]:
    """The region's checks by role."""
    last, end = region.end - 4, region.end
    return {
        'last load': f'{region.name}: a load at its last word, 0x{last:08x}, reads its word from memory',
        'last fetch': f'{region.name}: a fetch at its last word, 0x{last:08x}, executes it',
        'seam load': f'{region.name}: a load at each seam of its decode pieces reads its word from memory',
        'seam fetch': f'{region.name}: a fetch at each seam of its decode pieces executes it',
        'end load': f'{region.name}: a load one word past its end, 0x{end:08x}, takes a load access fault '
                    '(cause 5) before its bus',
        'end fetch': f'{region.name}: a fetch one word past its end, 0x{end:08x}, takes an instruction access '
                     'fault (cause 1) before its bus',
    }


def probes() -> list[Probe]:
    """Every probe, in order: rom's, then sram's, each of whose words the probe stores first. Every word
    probed inside a region is `ret`, so a fetch there returns and a load reads it."""
    out = []
    for region in (ctrl_memory.ROM, ctrl_memory.RAM):
        check, last, end = names(region), region.end - 4, region.end
        if region is ctrl_memory.RAM:
            out += [Probe(K_STORE, w, RET, check['seam load']) for w in seams(region)]
            out.append(Probe(K_STORE, last, RET, check['last load']))
        out += [p for w in seams(region) for p in (Probe(K_LOAD, w, 0, check['seam load']),
                                                   Probe(K_FETCH, w, 0, check['seam fetch']))]
        out += [Probe(K_LOAD, last, 0, check['last load']), Probe(K_FETCH, last, 0, check['last fetch']),
                Probe(K_LOAD, end, 0, check['end load']), Probe(K_FETCH, end, 0, check['end fetch'])]
    return out


#: The checks every run grades, in order.
CHECKS = [*[n for r in (ctrl_memory.ROM, ctrl_memory.RAM) for n in names(r).values()],
          'the probe ran every probe and stored its end word',
          *[f'DECODE the {port} decode admits exactly the SoC regions it may {port}' for port in decode.PORTS]]
_ROM, _RAM = names(ctrl_memory.ROM), names(ctrl_memory.RAM)
_DECODE = {c for c in CHECKS if c.startswith('DECODE ')}
#: The checks each planted decode must fail, and no other. single-mask: (address & 0xfffc8000) == 0 refuses
#: every rom address with bit 15 set, so rom's seam words 0x1fffc and 0x2fffc, while its last word 0x37ffc
#: (bit 15 clear) and every sram word stay admitted (decode.py on that netlist: its sram terms are exact).
#: cover: the word past each region's end reaches the bus and the memory there answers.
KILLS = {
    'single-mask': {_ROM['seam load'], _ROM['seam fetch'], *_DECODE},
    'cover': {_ROM['end load'], _ROM['end fetch'], _RAM['end load'], _RAM['end fetch'], *_DECODE},
}


def run(argv: list[str], log: Path, cwd: Path | None = None) -> None:
    """One build step in the foreground, its whole output in its log."""
    print('COMMAND', ' '.join(argv), flush=True)
    with log.open('w') as sink:
        result = subprocess.run(argv, cwd=cwd, stdout=sink, stderr=subprocess.STDOUT, check=False)
    if result.returncode:
        raise RuntimeError(f'{Path(argv[0]).name} exited {result.returncode}; see {log}')


def sources(out: Path) -> None:
    """The probe table and the rom words it reads (probe_data.S), and their link script (probe.ld)."""
    table = [f'\t.word {p.kind}, 0x{p.address:08x}, 0x{p.value:08x}\t/* {p.check} */' for p in probes()]
    words = sorted({p.address for p in probes() if ctrl_memory.ROM.holds(p.address, p.address + 4)})
    data = ['/* GENERATED by tb/verilator/ctrl_region_decode/run.py; DO NOT EDIT. */',
            '\t.section .rodata.probes, "a"', '\t.balign 4', '\t.globl probes', 'probes:', *table,
            f'\t.word {K_END}, 0, 0']
    for w in words:
        data += [f'\t.section .rom.at.{w:08x}, "ax"', '\t.balign 4', f'\t.word 0x{RET:08x}\t/* ret */']
    (out / 'probe_data.S').write_text('\n'.join(data) + '\n')
    link = ['/* GENERATED by tb/verilator/ctrl_region_decode/run.py; DO NOT EDIT. */', 'ENTRY(_start)',
            'SECTIONS', '{', f'\t.text 0x{ctrl_memory.ROM.origin:08x} : {{ KEEP(*(.text.start)) *(.text .text.*) '
            '*(.rodata .rodata.*) }']
    link += [f'\t.rom.at.{w:08x} 0x{w:08x} : {{ KEEP(*(.rom.at.{w:08x})) }}' for w in words]
    link += ['\t/DISCARD/ : { *(.comment) *(.note .note.*) }', '}']
    (out / 'probe.ld').write_text('\n'.join(link) + '\n')


def image(out: Path) -> Path:
    """The probe image, linked against the table and script sources() writes."""
    import fw_rv32
    cc = fw_rv32.compiler()
    if cc is None:
        raise RuntimeError('no RV32 compiler (sw/firmware/gtest/fw_rv32.py)')
    sources(out)
    elf = out / 'probe.elf'
    run([cc, '-march=rv32i_zicsr', '-mabi=ilp32', '-nostdlib', '-nostartfiles', '-ffreestanding', '-static',
         f'-DREPORT_ADDRESS=0x{REPORT:08x}', f'-DDONE_WORD=0x{DONE_WORD:08x}', f'-DHALT_WORD=0x{HALT_WORD:08x}',
         '-T', str(out / 'probe.ld'), '-Wl,--no-relax', '-o', str(elf), str(HERE / 'probe.S'),
         str(out / 'probe_data.S')], out / 'probe.log')
    return elf


def symbols(elf: Path) -> dict[str, int]:
    """The image's global symbols."""
    import fw_rv32
    nm = Path(fw_rv32.compiler()).with_name(Path(fw_rv32.compiler()).name.replace('gcc', 'nm'))
    text = subprocess.run([str(nm), str(elf)], capture_output=True, text=True, check=True).stdout
    return {name: int(value, 16) for value, _, name in (ln.split() for ln in text.splitlines() if len(ln.split()) == 3)}


def export(out: Path, shape: str, elf: Path, mutant: str) -> dict:
    """The test SoC's export, in a child process (the CPU generator patches its class)."""
    soc = out / 'soc'
    soc.mkdir(parents=True, exist_ok=True)
    run([sys.executable, '-B', str(HERE / 'region_soc.py'), str(soc), shape, str(elf), mutant], out / 'soc.log',
        cwd=ROOT)
    return json.loads((soc / 'soc.json').read_text())


#: The testbench's observers: accessor, C++ type and the VexiiRiscv variable it reads.
ACCESSORS = (
    ('commit_valid', 'bool', 'WhiteboxerPlugin_logic_commits_ports_0_valid'),
    ('commit_pc', 'std::uint32_t', 'WhiteboxerPlugin_logic_commits_ports_0_pc'),
    ('trap_valid', 'bool', 'WhiteboxerPlugin_logic_trap_ports_0_valid'),
    ('trap_interrupt', 'bool', 'WhiteboxerPlugin_logic_trap_ports_0_interrupt'),
    ('trap_cause', 'unsigned', 'WhiteboxerPlugin_logic_trap_ports_0_cause'),
    ('fetch_cmd_valid', 'bool', 'FetchL1Plugin_logic_bus_cmd_valid'),
    ('fetch_cmd_ready', 'bool', 'FetchL1Plugin_logic_bus_cmd_ready'),
    ('fetch_address', 'std::uint32_t', 'FetchL1Plugin_logic_bus_cmd_payload_address'),
    ('fetch_rsp_valid', 'bool', 'FetchL1Plugin_logic_bus_rsp_valid'),
    ('fetch_rsp_error', 'bool', 'FetchL1Plugin_logic_bus_rsp_payload_error'),
    ('lsu_cmd_valid', 'bool', 'LsuCachelessPlugin_logic_bus_cmd_valid'),
    ('lsu_cmd_ready', 'bool', 'LsuCachelessPlugin_logic_bus_cmd_ready'),
    ('lsu_cmd_id', 'unsigned', 'LsuCachelessPlugin_logic_bus_cmd_payload_id'),
    ('lsu_write', 'bool', 'LsuCachelessPlugin_logic_bus_cmd_payload_write'),
    ('lsu_address', 'std::uint32_t', 'LsuCachelessPlugin_logic_bus_cmd_payload_address'),
    ('lsu_wdata', 'std::uint32_t', 'LsuCachelessPlugin_logic_bus_cmd_payload_data'),
    ('lsu_rsp_valid', 'bool', 'LsuCachelessPlugin_logic_bus_rsp_valid'),
    ('lsu_rsp_id', 'unsigned', 'LsuCachelessPlugin_logic_bus_rsp_payload_id'),
    ('lsu_rsp_data', 'std::uint32_t', 'LsuCachelessPlugin_logic_bus_rsp_payload_data'),
    ('lsu_rsp_error', 'bool', 'LsuCachelessPlugin_logic_bus_rsp_payload_error'),
)


def verilate(out: Path, spec: dict) -> Path:
    """The native model of the exported top and this testbench, its observers bound by the generated header."""
    sys.path.insert(0, str(BUDGET))
    import build as budget_build
    native = out / 'native'
    flags = f'-O3 -std=c++17 -Wall -Wextra -I{ROOT}/tb/common -I{out}'
    run(['verilator', '--cc', '--exe', '-Wno-fatal', '-Werror-USERERROR', '-Wno-BLKANDNBLK', '-Wno-WIDTH',
         '-Wno-COMBDLY', '-Wno-CASEINCOMPLETE', '--top-module', 'sim', '--Mdir', str(native), '-O3',
         '--output-split', '5000', '--output-split-cfuncs', '500', '-CFLAGS', flags,
         *['-I' + str(i) for i in spec['includes']], str(HERE / 'observe.vlt'), *spec['sources'],
         str(HERE / 'sim_main.cpp')], out / 'verilate.log', cwd=out / 'soc/gateware')
    observed = {'VexiiRiscv': budget_build.OBSERVED['VexiiRiscv']}
    with patch.dict(budget_build.OBSERVED, observed, clear=True):
        path, prefix = budget_build.member_paths(native)['VexiiRiscv']
    lines = ['// GENERATED by tb/verilator/ctrl_region_decode/run.py; DO NOT EDIT.', '#pragma once',
             '#include <cstdint>', '#include "Vsim.h"', '#include "Vsim___024root.h"',
             *[f'#include "{h.name}"' for h in sorted(native.glob('Vsim_*.h'))
               if not h.name.startswith('Vsim__')],
             f'constexpr std::uint64_t sys_hz = {spec["sys_hz"]}ULL;',
             f'constexpr std::uint64_t cpu_hz = {spec["cpu_hz"]}ULL;',
             f'constexpr std::uint64_t sim_limit_ps = {SIM_LIMIT_MS}ULL * 1000000000ULL;',
             f'constexpr std::uint32_t report_address = 0x{REPORT:08x}u;',
             f'constexpr std::uint32_t done_word = 0x{DONE_WORD:08x}u;',
             f'constexpr std::uint32_t halt_word = 0x{HALT_WORD:08x}u;']
    lines += [f'inline {ctype} {name}(const Vsim& dut) {{ return {path}->{prefix}{var}; }}'
              for name, ctype, var in ACCESSORS]
    (out / 'region_config.hpp').write_text('\n'.join(lines) + '\n')
    run(['make', f'-j{JOBS}', '-C', str(native), '-f', 'Vsim.mk', 'Vsim'], out / 'make.log')
    return native / 'Vsim'


def simulate(out: Path, model: Path) -> None:
    """Run the model where its memories' init files are; keep its log and its exit status."""
    with (out / 'sim.log').open('w') as sink:
        status = subprocess.run([str(model)], cwd=out / 'soc/gateware', stdout=sink, stderr=subprocess.STDOUT,
                                check=False).returncode
    (out / STATUS).write_text(f'{status}\n')


class Segment(NamedTuple):
    """One probe's observations: from its mark to the next."""

    lines: list[list[str]]

    def tagged(self, tag: str) -> list[list[str]]:
        """The segment's lines of one tag, without the tag."""
        return [ln[1:] for ln in self.lines if ln[0] == tag]

    def reports(self, offset: int) -> list[int]:
        """The words stored to the report word + offset."""
        return [int(d, 16) for _, rw, a, d in self.tagged('LSU') if rw == 'W' and int(a, 16) == REPORT + offset]


def segments(log: str, table: int, count: int) -> tuple[list[Segment | None], str | None]:
    """Each probe's segment, by the mark (its table address) stored before it, and the run's end word."""
    found: list[Segment | None] = [None] * count
    current, end = None, None
    for raw in log.splitlines():
        line = raw.split()
        if not line or line[0] not in ('COMMIT', 'TRAP', 'FETCH', 'FETCHERR', 'LSU', 'RSP', 'END'):
            continue
        if line[0] == 'END':
            end = line[2]
            current = None
            continue
        if line[0] == 'LSU' and line[2] == 'W' and int(line[3], 16) == REPORT:
            mark = int(line[4], 16) - table
            current = None
            if 0 <= mark < 12 * count and mark % 12 == 0:
                current = found[mark // 12] = Segment([])
            continue
        if current is not None:
            current.lines.append(line)
    return found, end


def judge(probe: Probe, seg: Segment | None, want: int | None) -> str | None:
    """Why one probe's segment fails its check, or None when it passes."""
    if seg is None:
        return f'0x{probe.address:08x}: the probe never reached it'
    traps = seg.tagged('TRAP')
    at = f'0x{probe.address:08x}'
    if probe.kind == K_STORE:
        stored = [ln for ln in seg.tagged('LSU') if ln[1] == 'W' and int(ln[2], 16) == probe.address]
        return None if stored and not traps else f'{at}: the store did not reach the bus ({len(traps)} trap(s))'
    if probe.kind == K_LOAD and want is not None:
        rsp = [ln for ln in seg.tagged('RSP') if int(ln[1], 16) == probe.address]
        if traps:
            return f'{at}: trap cause {traps[0][2]}'
        if not rsp or rsp[0][3] != '0' or int(rsp[0][2], 16) != want or seg.reports(4) != [want]:
            return f'{at}: read {rsp[0][2] if rsp else "nothing"} (err {rsp[0][3] if rsp else "-"}), want {want:08x}'
        return None
    if probe.kind == K_FETCH and want is not None:
        if traps:
            return f'{at}: trap cause {traps[0][2]}'
        commits = [int(pc, 16) for _, pc in seg.tagged('COMMIT')]
        return None if probe.address in commits else f'{at}: never committed'
    cause = 5 if probe.kind == K_LOAD else 1
    reported = (seg.reports(8), seg.reports(12), seg.reports(16))
    bus = ([ln for ln in seg.tagged('LSU') if int(ln[2], 16) == probe.address] if probe.kind == K_LOAD
           else [ln for ln in seg.tagged('FETCH') if int(ln[1], 16) == probe.address & ~63])
    wrong = []
    if [int(t[2]) for t in traps] != [cause] or reported[0] != [cause] or reported[1] != [probe.address]:
        wrong.append(f'traps {[t[2] for t in traps]}, mcause {reported[0]}, mtval {[hex(v) for v in reported[1]]}')
    if probe.kind == K_FETCH and reported[2] != [probe.address]:
        wrong.append(f'mepc {[hex(v) for v in reported[2]]}')
    if bus:
        wrong.append(f'{len(bus)} command(s) for it on the bus')
    return f'{at}: ' + '; '.join(wrong) if wrong else None


def expected(probe: Probe, rom: list[int]) -> int | None:
    """The word a load at an address inside a region reads, or a fetch there executes; None past the ends."""
    a = probe.address
    if ctrl_memory.ROM.holds(a, a + 4):
        return rom[(a - ctrl_memory.ROM.origin) // 4]
    if ctrl_memory.RAM.holds(a, a + 4):
        stores = [p.value for p in probes() if p.kind == K_STORE and p.address == a]
        return stores[-1] if stores else None
    return None


def grade(out: Path) -> tuple[dict[str, str | None], list[str]]:
    """Each check's failure (None for a pass), and the report lines."""
    spec = json.loads((out / 'soc/soc.json').read_text())
    elf = out / 'probe.elf'
    status_path = out / STATUS
    status = int(status_path.read_text()) if status_path.exists() else None
    log = (out / 'sim.log').read_text()
    rom = ctrl_memory.rom_words(ctrl_memory.read_elf(elf))
    table = symbols(elf)['probes']
    plan = probes()
    found, end = segments(log, table, len(plan))
    failures: dict[str, list[str]] = {c: [] for c in CHECKS}
    for probe, seg in zip(plan, found):
        reason = judge(probe, seg, expected(probe, rom))
        if reason:
            failures[probe.check].append(reason)
    ending = 'the probe ran every probe and stored its end word'
    if end != 'DONE' or status != 0 or any(s is None for s in found):
        failures[ending].append(f'end {end}, model exit status {status}, '
                                f'{sum(s is None for s in found)} probe(s) never reached')
    netlist = next(Path(s) for s in spec['sources'] if Path(s).name == spec['netlist'] + '.v')
    report = [f'NETLIST {spec["netlist"]} ({spec["mutant"]}); the generator was handed '
              + ', '.join(f'[0x{o:08x}, +0x{s:x}) {m}' for o, s, m, _ in spec['cpu_memory_regions'])]
    for name, ok, detail in decode.check(netlist, spec['memory_regions'] + spec['cpu_devices']):
        report.append(f'DECODE {"PASS" if ok else "FAIL"} {name}: {detail}')
        if not ok:
            failures[f'DECODE {name}'].append(detail)
    verdict = {c: ('; '.join(r) if r else None) for c, r in failures.items()}
    report += [f'{"FAIL" if v else "PASS"} {c}{": " + v if v else ""}' for c, v in verdict.items()]
    return verdict, report


def build_and_run(out: Path, shape: str, mutant: str) -> None:
    """Every step of one run."""
    out.mkdir(parents=True, exist_ok=True)
    elf = image(out)
    spec = export(out, shape, elf, mutant)
    simulate(out, verilate(out, spec))


def one(out: Path, shape: str, mutant: str, regrade: bool) -> int:
    """One run, graded: 0 when every check passes."""
    if not regrade:
        build_and_run(out, shape, mutant)
    verdict, report = grade(out)
    print('\n'.join(report))
    failed = [c for c, v in verdict.items() if v]
    print(f'ctrl_region_decode: {"PASS" if not failed else "FAIL"} ({len(failed)} finding(s))')
    return 1 if failed else 0


def self_test(out: Path, shape: str) -> int:
    """The shipping decode must pass; each planted decode must fail exactly its KILLS, in a run that ended."""
    results = []
    for mutant in ('none', *KILLS):
        build_and_run(out / mutant, shape, mutant)
        verdict, report = grade(out / mutant)
        print(f'== {mutant}', *report, sep='\n')
        failed = {c for c, v in verdict.items() if v}
        want = KILLS.get(mutant, set())
        ended = 'the probe ran every probe and stored its end word' not in failed
        ok = failed == want and ended
        results.append(ok)
        print(f'SELF-TEST {"PASS" if ok else "FAIL"} {mutant}: fails {len(failed)} check(s), '
              f'wants {len(want)}' + ('' if ok else f'; unexpected {sorted(failed - want)}, '
                                                    f'escaped {sorted(want - failed)}'))
    print(f'ctrl_region_decode self-test: {"PASS" if all(results) else "FAIL"}')
    return 0 if all(results) else 1


def main() -> int:
    """Parse the options and run."""
    parser = argparse.ArgumentParser(description=__doc__.split('\n', 1)[0])
    parser.add_argument('--build-dir', type=Path, required=True)
    parser.add_argument('--shape', default='endstation_ax7101_1x1_tdm8')
    parser.add_argument('--mutant', choices=('none', *KILLS), default='none')
    parser.add_argument('--regrade', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    out = args.build_dir.resolve()
    if out.is_relative_to(ROOT):
        parser.error('keep the build directory outside the checkout')
    try:
        if args.self_test:
            return self_test(out, args.shape)
        return one(out, args.shape, args.mutant, args.regrade)
    except (RuntimeError, decode.Unreadable, ctrl_memory.Refusal) as error:
        print(f'ctrl_region_decode: REFUSED: {error}')
        return 2


if __name__ == '__main__':
    with contextlib.suppress(BrokenPipeError):
        sys.exit(main())
