# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Link the split image, export the test SoC and compile its native model.

The image is ctrl_srp_image.py --with-aecp --layout split, unmodified, on
the runtime ctrl_image_runtime.py builds (through runtime_ssp.py, #723).
Every input of the native model is hashed into build.json, so a reused
build is refused when any of them changed.
"""
from __future__ import annotations

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
#: make's parallelism for the native model (the lane's -j16).
JOBS = 16


def run(argv: list[str], log: Path, cwd: Path | None = None) -> None:
    """Run one build step in the foreground; its whole output goes to its log."""
    print('COMMAND', shlex.join(argv), flush=True)
    with log.open('w') as sink:
        result = subprocess.run(argv, cwd=cwd, stdout=sink, stderr=subprocess.STDOUT, check=False)
    if result.returncode:
        raise RuntimeError(f'{argv[0]} exited {result.returncode}; see {log.name}')


#: Planted firmware defects for the controls: each is (source file, unique anchor, replacement).
MUTATIONS = {
    # #665 S2's planted over-budget path: ADP's receive handler spins before it hands the
    # record to the core, so every ADP record's service exceeds T_svc = 10 ms.
    'slow-adp-rx': ('adp/adp_mbx.c', '\tadp_rx(&i->adp, f->bytes, f->len);\n}',
                    '\tfor (volatile uint32_t n = 0; n < 16000u; ++n) {\n\t}\n'
                    '\tadp_rx(&i->adp, f->bytes, f->len);\n}'),
}


#: The labelled second arm (#665 S2): the size fixture's four observation callbacks
#: (ctrl_aecp_image.c) answer zeroed values instead of 'unavailable'. With the
#: unmodified fixture, AECP retries each pending change notice 1 ms later forever
#: (aecp.c, retry_at = now + 1); this arm separates that retry from each path's cost.
#: It changes test code only, in a scratch copy, and is never the formal measurement.
VARIANTS = {
    'answering-ports': [
        ('#include "wire.h"\n', '#include "wire.h"\n#include <string.h>\n'),
        ('{ (void)ctx; (void)i; (void)t; (void)n; (void)v; return false; }\nstatic bool a_avb',
         '{ (void)ctx; (void)i; (void)t; (void)n; memset(v, 0, sizeof *v); return true; }\nstatic bool a_avb'),
        ('{ (void)ctx; (void)i; (void)n; (void)v; return false; }\nstatic bool a_path',
         '{ (void)ctx; (void)i; (void)n; memset(v, 0, sizeof *v); return true; }\nstatic bool a_path'),
        ('{ (void)ctx; (void)i; (void)n; (void)v; (void)cap; (void)count; return false; }',
         '{ (void)ctx; (void)i; (void)n; (void)v; (void)cap; *count = 0; return true; }'),
        ('{ (void)ctx; (void)i; (void)t; (void)n; (void)v; return false; }\nstatic void a_changed',
         '{ (void)ctx; (void)i; (void)t; (void)n; memset(v, 0, sizeof *v); return true; }\nstatic void a_changed'),
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
    for anchor, replacement in VARIANTS[variant]:
        if source.count(anchor) != 1:
            raise RuntimeError(f'variant {variant}: an anchor is not unique in ctrl_aecp_image.c: {anchor!r}')
        source = source.replace(anchor, replacement)
    path.write_text(source)
    return scratch


def mutated_source(out: Path, mutation: str) -> Path:
    """A scratch copy of the control firmware with one planted defect, never the tree."""
    import shutil
    path, anchor, replacement = MUTATIONS[mutation]
    tree = out / 'ctrl-mutant'
    shutil.rmtree(tree, ignore_errors=True)
    shutil.copytree(ROOT / 'sw/firmware/ctrl', tree, ignore=shutil.ignore_patterns('__pycache__'))
    source = (tree / path).read_text()
    if source.count(anchor) != 1:
        raise RuntimeError(f'mutation {mutation}: its anchor is not unique in {path}')
    (tree / path).write_text(source.replace(anchor, replacement))
    return tree


def firmware(out: Path, shape: str, n_if: int, mutation: str = 'none', variant: str = 'none') -> Path:
    """The runtime archives, then the linked split image (a planted copy for a control,
    or the labelled variant arm)."""
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
    run([sys.executable, '-B', *entry,
         '--config', str(ROOT / 'configs' / (shape + '.yaml')), '--interfaces', str(n_if),
         '--with-aecp', '--layout', 'split', '--output', str(image), *source,
         '--libc', str(runtime / 'libc.a'), '--compiler-runtime', str(runtime / 'libcompiler_rt.a')],
        out / 'image.log', cwd=ROOT)
    return image / 'ctrl_app.elf'


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
    lines += [f"constexpr std::uint32_t pass_pc = 0x{table['ctrl_loop_service']:x}u;",
              f"constexpr unsigned filter_en_word = 0x{spec['filter_en'] // 4:x}u;",
              f"constexpr unsigned tmr_cmd_word = 0x{spec['tmr_cmd'] // 4:x}u;",
              'constexpr unsigned tx_head_word(unsigned ch) {',
              f"    return (0x{spec['ch_base']:x}u + ch * 0x{spec['ch_stride']:x}u + 0x{spec['tx_head']:x}u) / 4u;",
              '}']
    for name, ctype, module, var in ACCESSORS:
        path, prefix = paths[module]
        mask = ' & 1u' if name.endswith('_id') else ''
        lines.append(f'inline {ctype} {name}(const Vsim& dut) {{ return {path}->{prefix}{var}{mask}; }}')
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
    config_header(build_dir, spec, table, member_paths(native),
                  code_modules(Path(spec['elf']).with_name('ctrl_app.map')))
    run(['make', f'-j{jobs}', '-C', str(native), '-f', 'Vsim.mk', 'Vsim'], build_dir / 'make.log')


def digest(paths: list[Path]) -> dict[str, str]:
    """The sha256 of every input, by its path relative to the checkout where it has one."""
    out = {}
    for path in paths:
        key = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else path.name
        out[key] = hashlib.sha256(path.read_bytes()).hexdigest()
    return out


def build(build_dir: Path, shape: str, n_if: int, cpu_regions: str = 'cover',
          mutation: str = 'none', variant: str = 'none') -> dict:
    """The whole build at one point; returns build.json's contents."""
    import split_soc
    build_dir.mkdir(parents=True, exist_ok=True)
    elf = firmware(build_dir, shape, n_if, mutation, variant)
    table = symbols(elf)
    spec = split_soc.build(build_dir, shape, elf, n_if, cpu_regions)
    spec['elf'] = str(elf)
    sys.path.insert(0, str(ROOT / 'sw/mailbox'))
    from mailbox_model import load
    contract = load()
    regs = {r.name: r.offset for r in contract.registers}
    spec.update(channels=len(contract.channels), filter_en=regs['FILTER_EN'], tmr_cmd=regs['TMR_CMD'],
                ch_base=contract.ch_base, ch_stride=contract.ch_stride,
                tx_head={r.name: r.offset for r in contract.ch_registers}['TX_HEAD'])
    verilate(build_dir, spec, table, JOBS)
    inputs = [elf, HERE / 'sim_main.cpp', HERE / 'observe.vlt', SIBLING / 'flash.hpp',
              *[Path(s) for s in spec['sources']]]
    spec['inputs'] = digest(inputs)
    spec['symbols'] = {name: table[name] for name in ('ctrl_loop_service', 'main')}
    spec['mutation'] = mutation
    spec['variant'] = variant
    spec['executable_sha256'] = hashlib.sha256((build_dir / 'native/Vsim').read_bytes()).hexdigest()
    (build_dir / 'build.json').write_text(json.dumps(spec, indent=2) + '\n')
    return spec


def reused(build_dir: Path) -> dict:
    """A previous build, refused unless every recorded input still has its digest."""
    spec = json.loads((build_dir / 'build.json').read_text())
    paths = [ROOT / key if not Path(key).is_absolute() and (ROOT / key).exists() else None
             for key in spec['inputs']]
    for key, path in zip(spec['inputs'], paths):
        if path is not None and hashlib.sha256(path.read_bytes()).hexdigest() != spec['inputs'][key]:
            raise RuntimeError(f'reused build is stale: {key} changed')
    if hashlib.sha256((build_dir / 'native/Vsim').read_bytes()).hexdigest() != spec['executable_sha256']:
        raise RuntimeError('reused build is stale: the native model changed')
    return spec


if __name__ == '__main__':
    sys.path.insert(0, str(HERE))
    os.environ.setdefault('PYTHONHASHSEED', '0')
    print(json.dumps(build(Path(sys.argv[1]).resolve(), sys.argv[2], int(sys.argv[3]),
                           cpu_regions=sys.argv[4] if len(sys.argv) > 4 else 'cover'), indent=2)[:2000])
