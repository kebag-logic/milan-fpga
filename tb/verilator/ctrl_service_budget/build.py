# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Link the split image, export the test SoC and compile its native model.

The image is ctrl_srp_image.py --with-aecp --layout split, unmodified, on
the runtime ctrl_image_runtime.py builds (through runtime_ssp.py, #723).
Every input of the native model and of its run is hashed into build.json:
the checkout's sources, the firmware source trees the image is compiled
from, the image, its runtime archives and the ROM files the model reads at
run time, the exported SoC Verilog and the CPU netlist. A reused or
regraded build is refused when any of them changed, is missing, or is
recorded under a key that does not resolve (reused()).
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SIBLING = ROOT / 'tb/verilator/fw_service_budget'
SIM_LIMIT_S = 60
#: make's parallelism for the native model (-j16).
JOBS = 16


def run(argv: list[str], log: Path, cwd: Path | None = None) -> None:
    """Run one build step in the foreground; its whole output goes to its log."""
    print('COMMAND', shlex.join(argv), flush=True)
    with log.open('w') as sink:
        result = subprocess.run(argv, cwd=cwd, stdout=sink, stderr=subprocess.STDOUT, check=False)
    if result.returncode:
        raise RuntimeError(f'{argv[0]} exited {result.returncode}; see {log.name}')


#: Planted firmware defects for the controls: each is (source file, unique anchor, replacement),
#: the control group its control paths are in, and the variant it needs.
MUTATIONS = {
    # #665's planted over-budget path: ADP's receive handler spins before it hands the
    # record to the core, so every ADP record's service exceeds its 20 ms budget, min(T_svc,
    # 200 ms) (FR_NFR.md 3.4.1), on the cacheless CPU the controls run on (README, Controls).
    'slow-adp-rx': ('adp/adp_mbx.c', '\tadp_rx(&i->adp, f->bytes, f->len);\n}',
                    '\tfor (volatile uint32_t n = 0; n < 32000u; ++n) {\n\t}\n'
                    '\tadp_rx(&i->adp, f->bytes, f->len);\n}', 'control', 'none'),
    # The SHUTDOWN path's planted defect (MAILBOX_SPLIT.md:523): disabling ADP spins before
    # each interface's ENTITY_DEPARTING, so the path exceeds its 20 ms budget.
    'slow-adp-shutdown': ('adp/adp_mbx.c', '\tfor (unsigned k = 0; k < MBX_N_IF; ++k) {\n\t\tadp_set_enable(',
                          '\tfor (volatile uint32_t n = 0; !enable && n < 32000u; ++n) {\n\t}\n'
                          '\tfor (unsigned k = 0; k < MBX_N_IF; ++k) {\n\t\tadp_set_enable(',
                          'control-shutdown', 'shutdown-entry'),
}


#: Labelled test-code arms, each a scratch copy of the size fixture (ctrl_aecp_image.c), never
#: the formal measurement. answering-ports: the four observation ports answer zeroed values
#: instead of 'unavailable'. Three are contract 2.3's face block (aecp_face.c: stream, avb and
#: counters, each a bounded window read that the datapath, held idle here, never answers);
#: the arm replaces those three in the face's ports, before the core takes them, and makes the
#: fixture's own path port answer an empty sequence. With the unmodified fixture, AECP retries
#: each pending change notice 1 ms later forever (aecp.c, retry_at = now + 1), and this arm
#: separates that retry from each path's cost. shutdown-entry: the linked image never
#: disables ADP, so a poll does it once at NOW_MS scenario.SHUTDOWN_MS, the only input of
#: the SHUTDOWN path (MAILBOX_SPLIT.md:523); it costs one NOW_MS read a pass.
VARIANTS = {
    'answering-ports': [
        ('#include "wire.h"\n', '#include "wire.h"\n#include <string.h>\n'),
        ('{ (void)ctx; (void)i; (void)n; (void)v; (void)cap; (void)count; return false; }',
         '{ (void)ctx; (void)i; (void)n; (void)v; (void)cap; *count = 0; return true; }'),
        ('static struct aecp_face image_face;\n',
         'static struct aecp_face image_face;\n'
         'static bool b_stream(void *ctx, unsigned i, uint16_t t, uint16_t n, struct aecp_stream_info *v)\n'
         '{ (void)ctx; (void)i; (void)t; (void)n; memset(v, 0, sizeof *v); return true; }\n'
         'static bool b_avb(void *ctx, unsigned i, uint16_t n, struct aecp_avb_info *v)\n'
         '{ (void)ctx; (void)i; (void)n; memset(v, 0, sizeof *v); return true; }\n'
         'static bool b_counters(void *ctx, unsigned i, uint16_t t, uint16_t n, struct aecp_counters *v)\n'
         '{ (void)ctx; (void)i; (void)t; (void)n; memset(v, 0, sizeof *v); return true; }\n'),
        ('    aecp_face_init(&image_face,&image_platform);\n',
         '    aecp_face_init(&image_face,&image_platform);\n'
         '    image_face.ports.stream=b_stream;\n'
         '    image_face.ports.avb=b_avb;\n'
         '    image_face.ports.counters=b_counters;\n'),
    ],
    'shutdown-entry': [
        ('int main(void)\n{',
         '// The SHUTDOWN path\'s test-only input (#665; MAILBOX_SPLIT.md:523): ADP is disabled once.\n'
         'static bool shutdown_entry(void *ctx)\n{\n    static bool fired;\n    (void)ctx;\n'
         '    if (!fired && mbx_now_ms() >= SHUTDOWN_MS) {\n        fired = true;\n'
         '        adp_mbx_set_enable(&image_app.adp, false);\n    }\n    return false;\n}\n\n'
         'int main(void)\n{'),
        ('    ctrl_loop_run(&image_app.loop);',
         '    if (!ctrl_loop_add_poll(&image_app.loop, shutdown_entry, NULL)) return 7;\n'
         '    ctrl_loop_run(&image_app.loop);'),
    ],
}


def variant_fixture(out: Path, variant: str) -> Path:
    """A scratch copy of the fixture's test directory files with the variant's edits."""
    test = ROOT / 'sw/firmware/ctrl/test'
    scratch = out / 'fixture-variant'
    scratch.mkdir(parents=True, exist_ok=True)
    for name in ('ctrl_aecp_image.c', 'ctrl_image.c', 'ctrl_image.ld'):
        (scratch / name).write_bytes((test / name).read_bytes())
    path = scratch / 'ctrl_aecp_image.c'
    source = path.read_text()
    import scenario
    for anchor, replacement in VARIANTS[variant]:
        if source.count(anchor) != 1:
            raise RuntimeError(f'variant {variant}: an anchor is not unique in ctrl_aecp_image.c: {anchor!r}')
        source = source.replace(anchor, replacement.replace('SHUTDOWN_MS', f'{scenario.SHUTDOWN_MS}u'))
    path.write_text(source)
    return scratch


def mutated_source(out: Path, mutation: str) -> Path:
    """A scratch copy of the control firmware with one planted defect, never the tree."""
    import shutil
    path, anchor, replacement, _, _ = MUTATIONS[mutation]
    tree = out / 'ctrl-mutant'
    shutil.rmtree(tree, ignore_errors=True)
    shutil.copytree(ROOT / 'sw/firmware/ctrl', tree, ignore=shutil.ignore_patterns('__pycache__'))
    source = (tree / path).read_text()
    if source.count(anchor) != 1:
        raise RuntimeError(f'mutation {mutation}: its anchor is not unique in {path}')
    (tree / path).write_text(source.replace(anchor, replacement))
    return tree


#: The one point the planner's ledger lets plan past the 56-RAMB36 budget (ctrl_memory.LEDGERED),
#: by its name, which this harness gives only its measurement of that point: the image
#: (ctrl_srp_image.py --ledgered-point) and the SoC plan (split_soc.ledgered_plan). The product SoC
#: build names none (#665; docs/design/SPLIT_CONTROL_MEMORY.md section 5).
LEDGERED_POINTS = {('endstation_ax7101_8x8', 2): '8x8-two-interfaces'}


def ledgered_point(shape: str, n_if: int) -> str | None:
    """The ledgered point's name when this build is that point, else None."""
    return LEDGERED_POINTS.get((shape, n_if))


def firmware(out: Path, shape: str, n_if: int, mutation: str = 'none', variant: str = 'none') -> Path:
    """The runtime archives, then the linked split image (a planted copy for a control,
    or the labelled variant arm), planned as the ledgered point at that point only."""
    import pythondata_software_picolibc as picolibc
    import pythondata_software_compiler_rt as compiler_rt
    import litex
    runtime = out / 'runtime'
    run([sys.executable, '-B', str(HERE / 'runtime_ssp.py'), '--picolibc', picolibc.data_location,
         '--compiler-rt', compiler_rt.data_location,
         '--litex-software', str(Path(litex.__file__).parent / 'soc/software'),
         '--output', str(runtime)], out / 'runtime.log', cwd=ROOT)
    image = out / 'image'
    source = [] if mutation == 'none' else ['--ctrl-source', str(mutated_source(out, mutation))]
    entry = [str(ROOT / 'sw/firmware/ctrl/test/ctrl_srp_image.py')]
    if variant != 'none':
        entry = [str(HERE / 'fixture_variant.py'), str(variant_fixture(out, variant))]
    ledgered = ledgered_point(shape, n_if)
    run([sys.executable, '-B', *entry,
         '--config', str(ROOT / 'configs' / (shape + '.yaml')), '--interfaces', str(n_if),
         '--with-aecp', '--layout', 'split', '--output', str(image), *source,
         *([] if ledgered is None else ['--ledgered-point', ledgered]),
         '--libc', str(runtime / 'libc.a'), '--compiler-runtime', str(runtime / 'libcompiler_rt.a')],
        out / 'image.log', cwd=ROOT)
    return image / 'ctrl_app.elf'


#: The labelled hybrid-XIP arm (#665, decision D3): the anchor in plat/ctrl_split.ld that
#: places all code in rom, and what replaces it. Every other function executes from the QSPI
#: flash window behind the instruction cache. rom keeps the reset entry, the saved-state flash
#: driver (nvm_flash_litespi.c), .rodata and the initial values of .data, which the core reads
#: through its cacheless data bus. The driver stays in block RAM as D3 requires: a CPU fetching
#: from the flash cannot also hold the flash's command master, so the driver's own fetches would
#: wait behind its chip select.
XIP_TEXT = ('\t.text :\n\t{\n\t\tKEEP(*(.text.start))\n',
            '\t.entry : { KEEP(*(.text.start)) *-nvm_flash_litespi.o(.text .text.*) } > rom\n'
            '\t.text : ALIGN(4)\n\t{\n')
#: The close of that placement and what replaces it: the service loop's hot code, which the script
#: places ahead of the rest (#665), moves to flash with it, in the same order.
XIP_END = ('\t\t*(.text .text.*)\n\t} > rom\n', '\t\t*(.text .text.*)\n\t} > flash\n')


def xip_offset() -> int:
    """The flash offset of the arm's code: the first erase block past the product's AEM slot."""
    sys.path.insert(0, str(ROOT / 'sw/litex'))
    import milan_soc
    aem = milan_soc.FLASHBOOT_LAYOUT['aem']
    return -(-(aem['offset'] + aem['size']) // milan_soc.FLASH_ERASE_BLOCK) * milan_soc.FLASH_ERASE_BLOCK


def xip_script(script: str, flash: int, end: int) -> str:
    """plat/ctrl_split.ld with its code past the reset entry in a flash region from flash to end."""
    if (script.count(XIP_TEXT[0]) != 1 or script.count(XIP_END[0]) != 1 or
            script.count('INCLUDE regions.ld\n') != 1):
        raise RuntimeError('xip: plat/ctrl_split.ld no longer has its rom code placement')
    return script.replace(XIP_TEXT[0], XIP_TEXT[1]).replace(XIP_END[0], XIP_END[1]).replace(
        'INCLUDE regions.ld\n', f'INCLUDE regions.ld\nMEMORY {{ flash (rx) : ORIGIN = 0x{flash:08x}, '
        f'LENGTH = 0x{end - flash:x} }}\n')


def xip_image(out: Path, elf: Path, window: int) -> tuple[Path, Path, Path]:
    """Relink the image's own objects with its code in the flash window, through ctrl_srp_image.link.

    Returns the relinked ELF (its symbols and link map), the ELF rom is built
    from (the relinked one without its flash code) and the flash device's
    image (erased bytes, then the code at xip_offset()).
    """
    import shutil
    sys.path[:0] = [str(ROOT / 'sw/firmware/ctrl/test'), str(ROOT / 'sw/firmware/gtest')]
    import ctrl_srp_image
    import fw_rv32
    cc = fw_rv32.compiler()
    src = out / 'xip-source'
    (src / 'plat').mkdir(parents=True, exist_ok=True)
    plat = ROOT / 'sw/firmware/ctrl/plat'
    (src / 'plat/ctrl_split.ld').write_text(xip_script((plat / 'ctrl_split.ld').read_text(), window + xip_offset(),
                                                       window + 0x1000000))
    shutil.copy(plat / 'ctrl_split_start.S', src / 'plat/ctrl_split_start.S')
    objects = sorted(elf.parent.glob('[0-9]*-*.o'), key=lambda p: int(p.name.split('-', 1)[0]))
    linked = out / 'xip'
    linked.mkdir(exist_ok=True)
    # The scenario reads the image's generated entity headers beside the ELF it is given.
    for header in elf.parent.glob('*_gen.h'):
        shutil.copy(header, linked / header.name)
    xip_elf, _ = ctrl_srp_image.link(cc, src, linked, objects,
                                     [out / 'runtime/libc.a', out / 'runtime/libcompiler_rt.a'], 'split')
    objcopy = cc.removesuffix('gcc') + 'objcopy'
    rom_elf = linked / 'ctrl_app_rom.elf'
    run([objcopy, '--remove-section=.text', str(xip_elf), str(rom_elf)], linked / 'rom.log')
    code = linked / 'code.bin'
    run([objcopy, '-O', 'binary', '--only-section=.text', str(xip_elf), str(code)], linked / 'code.log')
    image = out / 'flash.bin'
    image.write_bytes(b'\xff' * xip_offset() + code.read_bytes())
    return xip_elf, rom_elf, image


def symbols(elf: Path) -> dict[str, int]:
    """The linked image's text symbols, each defined once."""
    sys.path.insert(0, str(ROOT / 'sw/firmware/gtest'))
    import fw_rv32
    cc = fw_rv32.compiler()
    if cc is None:
        raise RuntimeError('the pinned RV32 compiler is required')
    listing = subprocess.check_output([cc.removesuffix('gcc') + 'nm', '-S', str(elf)], text=True)
    table: dict[str, int] = {}
    functions = []
    for line in listing.splitlines():
        fields = line.split()
        if len(fields) == 4 and fields[2] in 'tT':
            functions.append([fields[3], int(fields[0], 16), int(fields[1], 16)])
            if fields[2] == 'T':
                if fields[3] in table:
                    raise RuntimeError(f'global text symbol {fields[3]} is defined twice')
                table[fields[3]] = int(fields[0], 16)
    (elf.parent / 'functions.json').write_text(json.dumps(sorted(functions, key=lambda f: f[1])) + '\n')
    return table


#: Each observed module, the instance name it has inside the mailbox, and one of its observed variables.
OBSERVED = {'VexiiRiscv': ('vexiis_0_logic_core', 'WhiteboxerPlugin_logic_commits_ports_0_valid'),
            'KL_mbx_rx': ('u_rx', 'commit_w'), 'KL_mbx_evt': ('u_evt', 'wr_en_o')}


def code_modules(mapfile: Path) -> tuple[list[str], list[tuple[int, int, int]]]:
    """Each linked text input section and the source module it came from, off the link map.

    A module is the object's source stem (ctrl_srp_image.py names objects
    <index>-<stem>.o); a runtime archive member is rt_<member>.
    """
    text = mapfile.read_text()
    body = text[text.index('Linker script and memory map'):]
    # One input section: its name, then (on the same line or the next) address, size, object.
    rows = re.findall(r'^ \.text(?:\.\S+)?\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)\s+(\S+)$', body, re.M)
    names: list[str] = []
    spans = []
    for start, size, path in rows:
        if not int(size, 16):
            continue
        stem = Path(path).name
        match = re.fullmatch(r'\d+-(.+)\.o', stem)
        member = re.fullmatch(r'lib\w+\.a\((\w+)\.o\)', stem)
        label = match.group(1) if match else f'rt_{member.group(1)}' if member else Path(stem).stem
        if label not in names:
            names.append(label)
        spans.append((int(start, 16), int(start, 16) + int(size, 16), names.index(label)))
    spans.sort()
    for (_, end, _), (start, _, _) in zip(spans, spans[1:]):
        if start < end:
            raise RuntimeError('overlapping text sections in the link map')
    return names, spans


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


#: The testbench's observers: accessor name, its C++ type, the module and the variable it reads.
ACCESSORS = (
    ('commit_valid', 'bool', 'VexiiRiscv', 'WhiteboxerPlugin_logic_commits_ports_0_valid'),
    ('commit_pc', 'std::uint32_t', 'VexiiRiscv', 'WhiteboxerPlugin_logic_commits_ports_0_pc'),
    ('trap_valid', 'bool', 'VexiiRiscv', 'WhiteboxerPlugin_logic_trap_ports_0_valid'),
    ('trap_interrupt', 'bool', 'VexiiRiscv', 'WhiteboxerPlugin_logic_trap_ports_0_interrupt'),
    ('trap_cause', 'unsigned', 'VexiiRiscv', 'WhiteboxerPlugin_logic_trap_ports_0_cause'),
    ('fetch_cmd_valid', 'bool', 'VexiiRiscv', 'FetchCachelessPlugin_logic_bus_cmd_valid'),
    ('fetch_cmd_ready', 'bool', 'VexiiRiscv', 'FetchCachelessPlugin_logic_bus_cmd_ready'),
    ('fetch_cmd_id', 'unsigned', 'VexiiRiscv', 'FetchCachelessPlugin_logic_bus_cmd_payload_id'),
    ('fetch_address', 'std::uint32_t', 'VexiiRiscv', 'FetchCachelessPlugin_logic_bus_cmd_payload_address'),
    ('fetch_rsp_valid', 'bool', 'VexiiRiscv', 'FetchCachelessPlugin_logic_bus_rsp_valid'),
    ('fetch_rsp_id', 'unsigned', 'VexiiRiscv', 'FetchCachelessPlugin_logic_bus_rsp_payload_id'),
    ('fetch_rsp_error', 'bool', 'VexiiRiscv', 'FetchCachelessPlugin_logic_bus_rsp_payload_error'),
    ('lsu_cmd_valid', 'bool', 'VexiiRiscv', 'LsuCachelessPlugin_logic_bus_cmd_valid'),
    ('lsu_cmd_ready', 'bool', 'VexiiRiscv', 'LsuCachelessPlugin_logic_bus_cmd_ready'),
    ('lsu_cmd_id', 'unsigned', 'VexiiRiscv', 'LsuCachelessPlugin_logic_bus_cmd_payload_id'),
    ('lsu_write', 'bool', 'VexiiRiscv', 'LsuCachelessPlugin_logic_bus_cmd_payload_write'),
    ('lsu_address', 'std::uint32_t', 'VexiiRiscv', 'LsuCachelessPlugin_logic_bus_cmd_payload_address'),
    ('lsu_rsp_valid', 'bool', 'VexiiRiscv', 'LsuCachelessPlugin_logic_bus_rsp_valid'),
    ('lsu_rsp_id', 'unsigned', 'VexiiRiscv', 'LsuCachelessPlugin_logic_bus_rsp_payload_id'),
    ('lsu_rsp_error', 'bool', 'VexiiRiscv', 'LsuCachelessPlugin_logic_bus_rsp_payload_error'),
    ('rx_commit', 'bool', 'KL_mbx_rx', 'commit_w'),
    ('rx_channel', 'unsigned', 'KL_mbx_rx', 'ch_r'),
    ('evt_write', 'bool', 'KL_mbx_evt', 'wr_en_o'),
    ('evt_addr', 'unsigned', 'KL_mbx_evt', 'wr_addr_o'),
    ('evt_data', 'std::uint32_t', 'KL_mbx_evt', 'wr_data_o'),
)


def fetch_bus(spec: dict) -> tuple[list[tuple[str, str, str, str]], int]:
    """The observers of this build's fetch bus, and the words each fetch command carries.

    The cacheless CPU fetches one word a command, with ids in flight. The
    instruction cache (#665) refills one line a command, one refill at a
    time and without an id, so its ids read 0; its line is read off the
    netlist's refill address, never restated.
    """
    if not spec.get('fetch_l1_geometry'):
        return list(ACCESSORS), 1
    netlist = next(Path(s) for s in spec['sources'] if Path(s).name == spec['netlist'] + '.v')
    text = netlist.read_text()
    lines = re.findall(r"assign FetchL1Plugin_logic_bus_cmd_payload_address = "
                       r"\{\w+\[31 : (\d+)\],\d+'h0\};", text)
    if len(lines) != 1:
        raise RuntimeError('the fetch L1 refill address is not one line-aligned assignment')
    rows = [(name, ctype, module, var.replace('FetchCachelessPlugin', 'FetchL1Plugin'))
            for name, ctype, module, var in ACCESSORS if name not in ('fetch_cmd_id', 'fetch_rsp_id')]
    return lsu_bus(rows, text), (1 << int(lines[0])) // 4


def lsu_bus(rows: list[tuple[str, str, str, str]], netlist: str) -> list[tuple[str, str, str, str]]:
    """The observers of this build's load/store bus, from the netlist's own plugin.

    The split CPU's data cache (#665, milan_soc.CTRL_LSU_L1) replaces the
    cacheless LSU. Its uncached accesses, every mailbox access among them,
    travel LsuPlugin's IO bus one at a time and without an id, so its ids read
    0; cached accesses and refills never reach that bus and are not counted.
    """
    cacheless = 'LsuCachelessPlugin_logic_bus_cmd_valid' in netlist
    cached = 'LsuPlugin_logic_bus_cmd_valid' in netlist and 'LsuL1Plugin_' in netlist
    if cacheless == cached:
        raise RuntimeError('the netlist has neither or both of the cacheless LSU and the data cache')
    if cacheless:
        return rows
    return [(name, ctype, module, var.replace('LsuCachelessPlugin', 'LsuPlugin'))
            for name, ctype, module, var in rows if name not in ('lsu_cmd_id', 'lsu_rsp_id')]


#: Functions whose entry the testbench reports (ENTRY lines): a probe's entry:<symbol> start.
ENTRY_SYMBOLS = ('adp_mbx_set_enable',)


def cpu_region(spec: dict, origin: int) -> list:
    """The SoC region at origin, exactly one."""
    rows = [r for r in spec['memory_regions'] if r[0] == origin]
    if len(rows) != 1:
        raise RuntimeError(f'no single CPU region at 0x{origin:08x}')
    return rows[0]


def config_header(build_dir: Path, spec: dict, table: dict[str, int],
                  paths: dict[str, tuple[str, str]], modules: tuple[list[str], list]) -> None:
    """Bind the testbench to this build: clocks, regions, the pass PC and the observers."""
    rom, sram, csr = (cpu_region(spec, o) for o in (0, 0x1000_0000, 0xf000_0000))
    addresses = spec['addresses']
    headers = sorted(h.name for h in (build_dir / 'native').glob('Vsim_*.h')
                     if not h.name.startswith(('Vsim__', 'Vsim_KL_mbx_pkg')))
    lines = ['#pragma once', '// Generated by build.py for one build; never edited or committed.',
             '#include <cstdint>', '#include "Vsim.h"', '#include "Vsim___024root.h"',
             *[f'#include "{h}"' for h in headers],
             f"constexpr std::uint64_t sys_hz = {spec['sys_hz']};",
             f"constexpr std::uint64_t cpu_hz = {spec['cpu_hz']};",
             f"constexpr unsigned n_if = {spec['interfaces']};",
             f"constexpr unsigned n_ch = {spec['channels']};",
             f'constexpr std::uint64_t sim_limit_ps = {SIM_LIMIT_S}ULL * 1000000000000ULL;']
    for name, base, size in (('rom', rom[0], rom[1]), ('sram', sram[0], sram[1]),
                             ('mbx', addresses['mailbox'], spec['window_bytes']),
                             ('flash', addresses['flash'], addresses['flash_size']), ('csr', csr[0], csr[1])):
        lines += [f'constexpr std::uint32_t {name}_base = 0x{base:x}u;',
                  f'constexpr std::uint32_t {name}_size = 0x{size:x}u;']
    lines += [f'constexpr unsigned n_entries = {len(ENTRY_SYMBOLS)};',
              'inline constexpr std::uint32_t entry_pc[n_entries] = {'
              + ', '.join(f'0x{table[name]:x}u' for name in ENTRY_SYMBOLS) + '};',
              'inline const char* const entry_name[n_entries] = {'
              + ', '.join(f'"{name}"' for name in ENTRY_SYMBOLS) + '};']
    lines += [f"constexpr std::uint32_t pass_pc = 0x{table['ctrl_loop_service']:x}u;",
              f"constexpr unsigned filter_en_word = 0x{spec['filter_en'] // 4:x}u;",
              f"constexpr unsigned tmr_cmd_word = 0x{spec['tmr_cmd'] // 4:x}u;",
              'constexpr unsigned tx_head_word(unsigned ch) {',
              f"    return (0x{spec['ch_base']:x}u + ch * 0x{spec['ch_stride']:x}u + 0x{spec['tx_head']:x}u) / 4u;",
              '}']
    rows, beats = fetch_bus(spec)
    lines.append(f'constexpr unsigned fetch_beats = {beats}u;')
    for name, ctype, module, var in rows:
        path, prefix = paths[module]
        mask = ' & 1u' if name.endswith('_id') else ''
        lines.append(f'inline {ctype} {name}(const Vsim& dut) {{ return {path}->{prefix}{var}{mask}; }}')
    if beats > 1:
        lines += ['inline unsigned fetch_cmd_id(const Vsim&) { return 0u; }',
                  'inline unsigned fetch_rsp_id(const Vsim&) { return 0u; }']
    if not any(name == 'lsu_cmd_id' for name, *_ in rows):
        lines += ['inline unsigned lsu_cmd_id(const Vsim&) { return 0u; }',
                  'inline unsigned lsu_rsp_id(const Vsim&) { return 0u; }']
    lines.append('inline void set_gm(Vsim& dut, unsigned i, std::uint64_t id, unsigned domain) {')
    if spec['interfaces'] == 1:
        lines += ['    dut.mbx_gm_id = id;', '    dut.mbx_domain = domain;', '    (void)i;']
    else:
        lines += ['    dut.mbx_gm_id[2 * i] = static_cast<std::uint32_t>(id);',
                  '    dut.mbx_gm_id[2 * i + 1] = static_cast<std::uint32_t>(id >> 32);',
                  '    dut.mbx_domain = (dut.mbx_domain & ~(0xffu << (8 * i))) | ((domain & 0xffu) << (8 * i));']
    names, spans = modules
    lines += ['}', 'struct CodeSpan { std::uint32_t start, end; unsigned module; };',
              f'constexpr unsigned n_modules = {len(names)};',
              'inline const char* const module_name[n_modules] = {' + ', '.join(f'"{n}"' for n in names) + '};',
              'inline constexpr CodeSpan code_spans[] = {',
              *[f'    {{0x{a:x}u, 0x{e:x}u, {m}u}},' for a, e, m in spans], '};']
    (build_dir / 'budget_config.hpp').write_text('\n'.join(lines) + '\n')


#: The mailbox's modules, each of whose instances must connect every port it declares.
MAILBOX_MODULES = ('KL_mbx', 'KL_mbx_wb')


def mailbox_pins_missing(log: str, cwd: Path) -> list[str]:
    """Each mailbox port Verilator reports an instance leaves unconnected (PINMISSING, which
    -Wno-fatal lets pass), as module.port; the instance is the module named at the line it cites."""
    found = set()
    for path, line, pin in re.findall(r'PINMISSING: (\S+?):(\d+):\d+: \w+ has missing pin: \'(\w+)\'', log):
        words = (cwd / path).read_text().splitlines()[int(line) - 1].split()
        if words and words[0] in MAILBOX_MODULES:
            found.add(f'{words[0]}.{pin}')
    return sorted(found)


def verilate(build_dir: Path, spec: dict, table: dict[str, int], jobs: int) -> None:
    """Verilate the exported top, bind the observers, then compile the native model."""
    native = build_dir / 'native'
    flags = f'-O3 -std=c++17 -Wall -Wextra -I{ROOT}/tb/common -I{build_dir} -I{SIBLING}'
    argv = ['verilator', '--cc', '--exe', '-Wno-fatal', '-Werror-USERERROR',
            '-Wno-BLKANDNBLK', '-Wno-WIDTH', '-Wno-COMBDLY', '-Wno-CASEINCOMPLETE',
            '--top-module', 'sim', '--Mdir', str(native), '-O3',
            '--output-split', '5000', '--output-split-cfuncs', '500', '-CFLAGS', flags,
            *['-I' + str(i) for i in spec['includes']], str(HERE / 'observe.vlt'),
            *spec['sources'], str(HERE / 'sim_main.cpp')]
    run(argv, build_dir / 'verilate.log', cwd=build_dir / 'gateware')
    missing = mailbox_pins_missing((build_dir / 'verilate.log').read_text(), build_dir / 'gateware')
    if missing:
        raise RuntimeError(f'the mailbox instances leave ports unconnected (verilate.log, PINMISSING): {missing}')
    config_header(build_dir, spec, table, member_paths(native),
                  code_modules(Path(spec['elf']).with_name('ctrl_app.map')))
    run(['make', f'-j{jobs}', '-C', str(native), '-f', 'Vsim.mk', 'Vsim'], build_dir / 'make.log')


#: The source trees the image is compiled from (ctrl_srp_image.py: the control firmware and
#: its fixture, the saved-state store, the RV32 toolchain pin, the mailbox contract, the TSN
#: stack's cores and lwSRP), bound to a build by one digest of every file in them.
FIRMWARE_TREES = ('sw/firmware/ctrl', 'sw/firmware/ctrl_nvm', 'sw/firmware/gtest', 'sw/mailbox',
                  'third_party/tsn-c-stack', 'third_party/lwSRP', 'sw/litex/ctrl_memory.py')


def tree_digest(roots: list[Path]) -> str:
    """One sha256 over every file under the roots: each path (relative to the checkout) and its bytes."""
    h = hashlib.sha256()
    for root in roots:
        files = [root] if root.is_file() else sorted(
            q for q in root.rglob('*') if q.is_file() and '.git' not in q.parts and '__pycache__' not in q.parts)
        for q in files:
            name = q.relative_to(ROOT) if q.is_relative_to(ROOT) else q
            h.update(str(name).encode() + b'\0' + hashlib.sha256(q.read_bytes()).digest())
    return h.hexdigest()


def input_key(path: Path, build_dir: Path) -> str:
    """An input's key: checkout:<path>, build:<path> or external:<absolute path>."""
    path = path.resolve()
    if path.is_relative_to(build_dir):
        return f'build:{path.relative_to(build_dir)}'
    if path.is_relative_to(ROOT):
        return f'checkout:{path.relative_to(ROOT)}'
    return f'external:{path}'


def resolve(key: str, build_dir: Path) -> Path:
    """The file an input key names; a key in no known namespace is refused, never skipped."""
    space, _, name = key.partition(':')
    if space == 'build':
        return build_dir / name
    if space == 'checkout':
        return ROOT / name
    if space == 'external' and Path(name).is_absolute():
        return Path(name)
    raise RuntimeError(f'reused build is stale: input key {key!r} does not resolve')


def digest(paths: list[Path], build_dir: Path) -> dict[str, str]:
    """The sha256 of every input, by its key (input_key)."""
    return {input_key(path, build_dir): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}


def run_inputs(build_dir: Path, spec: dict) -> list[Path]:
    """Every file the native model is built from or reads when it runs."""
    gateware = build_dir / 'gateware'
    return [Path(spec['elf']), *([Path(spec['flash_image'])] if spec.get('flash_image') else []),
            *sorted((build_dir / 'runtime').glob('*.a')), *sorted(gateware.glob('*.init')),
            build_dir / 'budget_config.hpp', HERE / 'sim_main.cpp', HERE / 'observe.vlt', SIBLING / 'flash.hpp',
            *[Path(s) for s in spec['sources']]]


@dataclasses.dataclass(frozen=True)
class Core:
    """The CPU a build runs on and where its code executes from.

    cpu_regions: the generator's region set (split_soc.build); fetch_l1: its
    instruction cache (split_soc.fetch_l1_geometry); xip: the labelled
    hybrid-XIP arm, the code past the reset entry in the flash window;
    cpu_hz: None for the product's split CPU clock, or the labelled option's
    clock (split_soc.build; clock_line names it).
    """
    cpu_regions: str = 'cover'
    fetch_l1: str = 'split'
    xip: bool = False
    cpu_hz: int | None = None


def clock_line(spec: dict) -> str:
    """A build's CPU clock as every table and run line names it (#665): the product's split CPU
    clock, or a labelled option that is not. A build recorded before the label names its clock only."""
    mhz = lambda hz: f'{hz / 1e6:g} MHz'
    bus = f"bus {mhz(spec['sys_hz'])}"
    if 'cpu_clock' not in spec:
        return f"CPU {mhz(spec['cpu_hz'])} (recorded before the CPU clock was labelled), {bus}"
    if spec['cpu_clock'] == 'product':
        return f"CPU {mhz(spec['cpu_hz'])}, the product's split CPU clock (the Milan clock), {bus}"
    return (f"CPU {mhz(spec['cpu_hz'])}, a labelled option: not the product's split CPU clock, "
            f"{mhz(spec['product_cpu_hz'])}, {bus}")


def build(build_dir: Path, shape: str, n_if: int, mutation: str = 'none', variant: str = 'none',
          core: Core = Core()) -> dict:
    """The whole build at one point; returns build.json's contents."""
    import split_soc
    build_dir.mkdir(parents=True, exist_ok=True)
    elf = firmware(build_dir, shape, n_if, mutation, variant)
    rom_elf, flash_image = elf, None
    if core.xip:
        elf, rom_elf, flash_image = xip_image(build_dir, elf, split_soc.fixture_addresses()['flash'])
    table = symbols(elf)
    with split_soc.ledgered_plan(ledgered_point(shape, n_if)):
        spec = split_soc.build(build_dir, shape, rom_elf, n_if, core)
    spec['elf'] = str(elf)
    spec['xip'] = core.xip
    spec['cpu_clock'] = 'product' if spec['cpu_hz'] == spec['product_cpu_hz'] else 'option'
    spec['flash_image'] = str(flash_image) if flash_image else None
    sys.path.insert(0, str(ROOT / 'sw/mailbox'))
    from mailbox_model import load
    contract = load()
    regs = {r.name: r.offset for r in contract.registers}
    spec.update(channels=len(contract.channels), filter_en=regs['FILTER_EN'], tmr_cmd=regs['TMR_CMD'],
                ch_base=contract.ch_base, ch_stride=contract.ch_stride,
                tx_head={r.name: r.offset for r in contract.ch_registers}['TX_HEAD'])
    verilate(build_dir, spec, table, JOBS)
    spec['inputs'] = digest(run_inputs(build_dir, spec), build_dir)
    spec['inputs']['tree:firmware'] = tree_digest([ROOT / t for t in FIRMWARE_TREES])
    spec['inputs']['tree:config'] = tree_digest([ROOT / 'configs' / (shape + '.yaml')])
    spec['symbols'] = {name: table[name] for name in ('ctrl_loop_service', 'main', *ENTRY_SYMBOLS)}
    spec['mutation'] = mutation
    spec['variant'] = variant
    spec['executable_sha256'] = hashlib.sha256((build_dir / 'native/Vsim').read_bytes()).hexdigest()
    (build_dir / 'build.json').write_text(json.dumps(spec, indent=2) + '\n')
    return spec


def reused(build_dir: Path) -> dict:
    """A previous build, refused unless every recorded input still exists with its digest.

    Every key must resolve: the checkout's files, the build directory's (the
    image, its runtime, the ROM files, the generated SoC and mailbox Verilog),
    the external CPU netlist and RAM models, and the firmware source trees.
    The ROM .init files and the runtime archives found now must be exactly
    those recorded, and the native model must be the one built.
    """
    spec = json.loads((build_dir / 'build.json').read_text())
    inputs = spec.get('inputs') or {}
    for key, want in inputs.items():
        if key == 'tree:firmware':
            got = tree_digest([ROOT / t for t in FIRMWARE_TREES])
        elif key == 'tree:config':
            got = tree_digest([ROOT / 'configs' / (spec['shape'] + '.yaml')])
        else:
            path = resolve(key, build_dir)
            if not path.is_file():
                raise RuntimeError(f'reused build is stale: {key} is missing')
            got = hashlib.sha256(path.read_bytes()).hexdigest()
        if got != want:
            raise RuntimeError(f'reused build is stale: {key} changed')
    present = {input_key(p, build_dir) for p in run_inputs(build_dir, spec)}
    if present - set(inputs) or not {'tree:firmware', 'tree:config'} <= set(inputs):
        raise RuntimeError(f'reused build is stale: inputs never recorded: {sorted(present - set(inputs))}')
    executable = build_dir / 'native/Vsim'
    if not executable.is_file() or hashlib.sha256(executable.read_bytes()).hexdigest() != spec['executable_sha256']:
        raise RuntimeError('reused build is stale: the native model changed')
    return spec


if __name__ == '__main__':
    sys.path.insert(0, str(HERE))
    os.environ.setdefault('PYTHONHASHSEED', '0')
    print(json.dumps(build(Path(sys.argv[1]).resolve(), sys.argv[2], int(sys.argv[3]),
                           core=Core(cpu_regions=sys.argv[4] if len(sys.argv) > 4 else 'cover')), indent=2)[:2000])
