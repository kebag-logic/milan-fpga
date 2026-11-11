# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The wire-timing harness's build (#665, #868), all outside the checkout under one build directory.

In order:
  1. the shape's flash port map, from the split SoC's export (the CPU budget
     harness's build.flash_map);
  2. the bare-metal runtime archives and the platform image, linked twice as
     the split boot simulation links it (its run.runtime, and run.image's
     command): first against the fixture map, then against the CPU half's own
     csr.csv, and the two exports' rows must be equal; at 8x8 with two
     interfaces the image is the ledgered point (LEDGERED), planned to its
     ledgered tiles in the link and in the CPU half's memory;
  3. the CPU half's export (wire_soc.py), each in a child process, since the
     CPU generator patches its class;
  4. the split top, by milan_dp's own split recipe (make build-split, its
     SPLIT_MDIR in this build directory, its SPLIT_SHAPE, SPLIT_STREAMS and
     SPLIT_IF the point's), whose model archive is linked here; at two
     interfaces its mailbox variant must equal the CPU half's, file by file;
  5. the native model: the CPU half's export with wire_main.cpp, linked with
     the split top's archive.
Every input the model is built from, or reads when it runs, is recorded in
build.json with its digest, so a reused build is refused when any changed
(#868): the image, the ROM files and the generated headers; this harness's
model, export and build; the build's tools elsewhere (TOOLS, milan_dp's split
recipe among them); the split recipe's own source list (milan_dp's
print-split-srcs: the datapath's, KL_mbx's and the split top's); every file a
Verilator run or the native compile read, from the dependency lists they
leave; the checkout's modules the CPU half's export imported; the shape's
config; and the firmware's source trees, the TSN stack's among them
(FIRMWARE_TREES), by one digest.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BUDGET = ROOT / 'tb/verilator/ctrl_service_budget'
BOOT = ROOT / 'tb/verilator/ctrl_split_boot'
MILAN_DP = ROOT / 'tb/verilator/milan_dp'
SIBLING = ROOT / 'tb/verilator/fw_service_budget'
#: The points, the CPU budget harness's (its run.py POINTS): the shipping shape with one interface, and 8x8 with
#: two, whose interface 1 the split top gives to the bench (tb_split_top.sv). Each shape's datapath streams are the
#: builder's (endstation_builder.datapath_params, N_STREAMS).
POINTS = {'1x1': ('endstation_ax7101_1x1_tdm8', 1), '8x8': ('endstation_ax7101_8x8', 2)}
#: The one point whose platform image the planner's ledger lets plan past the 56-RAMB36 budget, by its name
#: (ctrl_memory.LEDGERED; docs/design/SPLIT_CONTROL_MEMORY.md section 5, ledgered at 59.0 by the owner's ruling of
#: 2026-10-29 on #665): the link (ctrl_plat_image.py --ledgered-point) and the CPU half's memory plan
#: (split_soc.ledgered_plan) both name it. Every other point names none.
LEDGERED = {('endstation_ax7101_8x8', 2): 'platform-8x8-two-interfaces'}
JOBS = int(os.environ.get('WIRE_JOBS', '16'))
#: The split top's model, as milan_dp's split recipe names it (--top-module tb_split_top).
SPLIT_ARCHIVE = 'Vtb_split_top__ALL.a'


def module(name: str, path: Path) -> object:
    """A sibling harness's module, loaded read only under a name of its own."""
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    sys.modules[name] = loaded
    spec.loader.exec_module(loaded)
    return loaded


boot = module('wire_boot_run', BOOT / 'run.py')
sys.path.insert(0, str(BUDGET))
import build as budget_build  # noqa: E402  the CPU budget harness's build, read only
sys.path.insert(0, str(ROOT / 'sw/mailbox'))
from mailbox_model import load as load_contract  # noqa: E402
sys.path.insert(0, str(ROOT / 'sw/builder'))
import endstation_builder as eb  # noqa: E402  the builder's datapath parameters, read only

#: The source trees the platform image is compiled from, bound to a build by one digest of every file in them: the
#: CPU budget harness's list (its build.FIRMWARE_TREES: the control firmware and its image tools, the saved-state
#: store, the RV32 toolchain pin's harness, the mailbox contract, the TSN stack's cores and lwSRP).
FIRMWARE_TREES = budget_build.FIRMWARE_TREES
#: The build's tools outside this directory, each by digest: the split boot simulation's link and runtime build,
#: the CPU budget harness's flash map and runtime archives, and milan_dp's split recipe.
TOOLS = (BOOT / 'run.py', BUDGET / 'build.py', BUDGET / 'runtime_ssp.py', MILAN_DP / 'Makefile')


def image(out: Path, name: str, point: tuple[str, int], maps: object, archives: tuple[Path, Path]) -> Path:
    """The platform image of one point against one map: the split boot simulation's link (run.image's command),
    naming the point's ledger where it has one."""
    shape, n_if = point
    ledger = LEDGERED.get(point)
    boot.run([sys.executable, '-B', str(boot.FIRMWARE_TEST / 'ctrl_plat_image.py'), '--config',
              str(ROOT / 'configs' / f'{shape}.yaml'), '--interfaces', str(n_if), '--csr-csv', str(maps.csr_csv),
              '--flash-map', str(maps.flash_map), '--output', str(out / name), '--libc', str(archives[0]),
              '--compiler-runtime', str(archives[1]), *(['--ledgered-point', ledger] if ledger else [])],
             out / f'{name}.log', cwd=ROOT)
    return out / name / 'ctrl_app.elf'


def export(out: Path, name: str, shape: str, elf: Path, n_if: int, flash_map: Path) -> dict:
    """The CPU half's export for one image, in a child process; its spec."""
    boot.run([sys.executable, '-B', str(HERE / 'wire_soc.py'), str(out / name), shape, str(elf), str(n_if),
              str(flash_map), LEDGERED.get((shape, n_if), '-')], out / f'{name}.log', cwd=ROOT)
    return json.loads((out / name / 'soc.json').read_text())


def streams(shape: str) -> int:
    """The shape's datapath streams, as the builder binds them on milan_datapath (N_STREAMS)."""
    return eb.datapath_params(eb.load_config(str(ROOT / 'configs' / (shape + '.yaml'))))['N_STREAMS']


def split_vars(shape: str, n_if: int) -> dict[str, str]:
    """The split recipe's variables at one point: its shape, the shape's streams and the interfaces."""
    return {'SPLIT_SHAPE': shape, 'SPLIT_STREAMS': str(streams(shape)), 'SPLIT_IF': str(n_if)}


def split_top(out: Path, variables: dict[str, str]) -> Path:
    """The split top's model, by milan_dp's split recipe at the point's variables, its Mdir in the build
    directory."""
    mdir = out / 'split'
    boot.run(['make', '-C', str(MILAN_DP), f'-j{JOBS}', 'build-split', f'SPLIT_MDIR={mdir}',
              *[f'{k}={v}' for k, v in variables.items()]], out / 'split.log')
    archive = mdir / SPLIT_ARCHIVE
    if not archive.is_file():
        raise RuntimeError(f'the split recipe left no {SPLIT_ARCHIVE} in {mdir}')
    return mdir


def split_sources(out: Path, spec: dict) -> list[Path]:
    """The split recipe's own source list (milan_dp's print-split-srcs) at the build's variables, or at the
    recipe's defaults where the build recorded none."""
    argv = ['make', '-s', '--no-print-directory', '-C', str(MILAN_DP), 'print-split-srcs',
            f'SPLIT_MDIR={out / "split"}', *[f'{k}={v}' for k, v in spec.get('split_vars', {}).items()]]
    listed = subprocess.run(argv, capture_output=True, text=True, env=dict(os.environ, MAKEFLAGS=''))
    if listed.returncode or not listed.stdout.split():
        raise RuntimeError(f"the reused build is stale: the split recipe's source list cannot be read "
                           f'({(listed.stderr.strip().splitlines() or ["no output"])[-1]})')
    return [(MILAN_DP / word).resolve() for word in listed.stdout.split()]


def dependencies(path: Path, base: Path) -> list[Path]:
    """The prerequisites one make dependency file names (Verilator's __ver.d, a compiler's -MMD file), each
    relative to the directory its tool ran in."""
    out = []
    for line in path.read_text().replace('\\\n', ' ').splitlines():
        _, colon, prerequisites = line.partition(': ')
        out += [(base / word).resolve() for word in prerequisites.split()] if colon else []
    return out


def read_by_tools(out: Path) -> list[Path]:
    """Every file a Verilator run or the native compile read, from the dependency lists they left (each run's
    __ver.d, each object's .d), but the Mdirs' own generated C++: the split top's Verilator run in milan_dp, the
    native model's in the export's gateware, each compile in its Mdir."""
    found = []
    for mdir, verilated_in in ((out / 'split', MILAN_DP), (out / 'native', out / 'soc/gateware')):
        for listing in sorted(mdir.glob('*.d')) if mdir.is_dir() else []:
            found += dependencies(listing, verilated_in if listing.name.endswith('__ver.d') else mdir)
    own = {(out / 'split').resolve(), (out / 'native').resolve()}
    return [p for p in found if p.parent not in own]


def same_mailbox(spec: dict, mdir: Path, n_if: int) -> None:
    """At two interfaces, the split top's mailbox variant (the recipe's SPLIT_VARIANT) is the CPU half's, file by
    file, so KL_mbx_wb and KL_mbx are built from one contract variant."""
    if n_if == 1:
        return
    for source in map(Path, spec['mailbox_sources']):
        if source.name in ('KL_mbx_pkg.sv', 'KL_mbx.sv'):
            other = mdir / f'mbx-if{n_if}' / source.name
            if not other.is_file() or digest(other) != digest(source):
                raise RuntimeError(f"the split top's {source.name} is not the CPU half's variant ({other})")


def contract_words() -> dict:
    """The mailbox contract's word addresses the testbench decodes: each channel's TX_HEAD, TMR_CMD and
    TMR_DEADLINE (sw/mailbox/mailbox.yaml)."""
    c = load_contract()
    regs = {r.name: r.offset for r in c.registers}
    tx_head = {r.name: r.offset for r in c.ch_registers}['TX_HEAD']
    return dict(channels=[ch.name for ch in c.channels],
                tx_head=[(c.ch_base + i * c.ch_stride + tx_head) // 4 for i in range(len(c.channels))],
                tmr_cmd=regs['TMR_CMD'] // 4, tmr_deadline=regs['TMR_DEADLINE'] // 4)


def config_header(out: Path, spec: dict, words: dict) -> Path:
    """wire_config.hpp: the clock, the window and the contract's words, generated, never restated."""
    ready = boot.BANNER.splitlines(keepends=True)[-1].replace('\r', '\\r').replace('\n', '\\n')
    path = out / 'wire_config.hpp'
    path.write_text('\n'.join([
        '// GENERATED by tb/verilator/ctrl_wire_timing/wire_build.py; DO NOT EDIT.', '#pragma once',
        '#include <cstdint>',
        f'constexpr std::uint64_t sys_hz = {spec["sys_hz"]}ULL;',
        f'constexpr std::uint32_t ms_div = {spec["sys_hz"] // 1000}u;',
        f'constexpr std::uint32_t csr_size = {spec["csr_size"]}u;',
        f'constexpr unsigned n_if = {spec["interfaces"]}u;',
        f'constexpr unsigned n_channels = {len(words["channels"])}u;',
        f'constexpr std::uint32_t tx_head_word[n_channels] = {{{", ".join(f"{w}u" for w in words["tx_head"])}}};',
        f'constexpr std::uint32_t tmr_cmd_word = {words["tmr_cmd"]}u;',
        f'constexpr std::uint32_t tmr_deadline_word = {words["tmr_deadline"]}u;',
        f'constexpr const char* ready_line = "{ready}";', '']))
    return path


def verilate(out: Path, spec: dict, mdir: Path) -> Path:
    """The native model: the CPU half's export and wire_main.cpp, linked with the split top's archive."""
    native = out / 'native'
    flags = f'-O3 -std=c++17 -Wall -Wextra -I{ROOT}/tb/common -I{out} -I{SIBLING} -I{mdir}'
    boot.run(['verilator', '--cc', '--exe', '-Wno-fatal', '-Werror-USERERROR', '-Wno-BLKANDNBLK', '-Wno-WIDTH',
              '-Wno-COMBDLY', '-Wno-CASEINCOMPLETE', '--top-module', 'sim', '--Mdir', str(native), '-O3',
              '--output-split', '5000', '--output-split-cfuncs', '500', '-CFLAGS', flags,
              *['-I' + str(i) for i in spec['includes']], *spec['sources'], str(HERE / 'wire_main.cpp'),
              str(mdir / SPLIT_ARCHIVE)], out / 'verilate.log', cwd=out / 'soc/gateware')
    boot.run(['make', f'-j{JOBS}', '-C', str(native), '-f', 'Vsim.mk', 'Vsim'], out / 'make.log')
    return native / 'Vsim'


def digest(path: Path) -> str:
    """One file's sha256."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inputs(out: Path, spec: dict) -> dict[str, str]:
    """Every input the native model is built from or reads when it runs (see the module's docstring), by a key
    relative to its root; a file listed and gone is recorded as missing."""
    out = out.resolve()
    files = [Path(spec['elf']), *sorted((out / 'soc/gateware').glob('*.init')), out / 'wire_config.hpp',
             HERE / 'wire_main.cpp', HERE / 'wire_soc.py', HERE / 'wire_build.py', out / 'split' / SPLIT_ARCHIVE,
             SIBLING / 'flash.hpp', *TOOLS, *[Path(s) for s in spec['sources']], *split_sources(out, spec),
             *map(Path, spec.get('generator_modules', ())), *read_by_tools(out),
             *([ROOT / 'configs' / (spec['shape'] + '.yaml')] if 'shape' in spec else [])]
    found = {}
    for f in dict.fromkeys(p.resolve() for p in files):
        key = str(f.relative_to(ROOT)) if ROOT in f.parents else 'build:' + str(f.relative_to(out)) \
            if out in f.parents else str(f)
        found[key] = digest(f) if f.is_file() else 'missing'
    found['tree:firmware'] = budget_build.tree_digest([ROOT / t for t in FIRMWARE_TREES])
    return found


def build(out: Path, point: str) -> dict:
    """Every build step at one point; build.json's contents."""
    shape, n_if = POINTS[point]
    out.mkdir(parents=True, exist_ok=True)
    flash_map = budget_build.flash_map(out / 'split-soc/flash-map', shape)
    archives = boot.runtime(out)
    first = image(out, 'image-provisional', (shape, n_if), boot.ImageMaps(boot.PROVISIONAL, flash_map), archives)
    export(out, 'soc-provisional', shape, first, n_if, flash_map)
    csr_csv = out / 'soc-provisional/csr.csv'
    elf = image(out, 'image', (shape, n_if), boot.ImageMaps(csr_csv, flash_map), archives)
    spec = export(out, 'soc', shape, elf, n_if, flash_map)
    if boot.rows(out / 'soc/csr.csv') != boot.rows(csr_csv):
        raise RuntimeError("the CPU half's csr.csv depends on the image; the map cannot be generated from it")
    spec.update(elf=str(elf), point=point, split_vars=split_vars(shape, n_if))
    config_header(out, spec, contract_words())
    mdir = split_top(out, spec['split_vars'])
    same_mailbox(spec, mdir, n_if)
    executable = verilate(out, spec, mdir)
    spec['inputs'] = inputs(out, spec)
    spec['executable_sha256'] = digest(executable)
    (out / 'build.json').write_text(json.dumps(spec, indent=2) + '\n')
    return spec


def reused(out: Path) -> dict:
    """A previous build, refused unless every recorded input still has its digest and the model is the one built."""
    spec = json.loads((out / 'build.json').read_text())
    if not spec.get('inputs'):
        raise RuntimeError('the reused build is stale: build.json records no inputs')
    now = inputs(out, spec)
    changed = sorted(k for k in set(spec['inputs']) | set(now) if spec['inputs'].get(k) != now.get(k))
    if changed:
        raise RuntimeError(f'the reused build is stale: {changed[:5]} changed, missing or never recorded')
    if digest(out / 'native/Vsim') != spec['executable_sha256']:
        raise RuntimeError('the reused build is stale: the native model changed')
    return spec
