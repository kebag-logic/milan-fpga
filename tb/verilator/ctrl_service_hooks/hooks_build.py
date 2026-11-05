# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Link the split platform's image, export the hook harness's SoC and compile its native model (#665).

The image is the split platform's (ctrl_plat_image.py), linked unmodified as
the split boot simulation links it: first against the platform's fixture
map, then against the SoC's own csr.csv, which an export with the first
image gives, and the second export's map must equal the first's. At 8x8
with two interfaces it is the ledgered point platform-8x8-two-interfaces,
and the SoC's memory plan is held to it; no other point names one. A plant
links a scratch copy of the firmware's tree with one planted defect, never
the checkout's.

The native model is the CPU budget harness's testbench
(tb/verilator/ctrl_service_budget/sim_main.cpp) with TESTBENCH's additions
applied to a copy in the build directory: the counter-change event's pads
and the script's `ctrchg` step that pulses them. Each addition's anchor must
occur exactly once, or the build is refused by name. Its observers and the
build's configuration header are that harness's (build.py, imported read
only). Every input of the model and its run is hashed into build.json, and a
reused build is refused when any of them changed (reused()).
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BUDGET = ROOT / 'tb/verilator/ctrl_service_budget'
BOOT = ROOT / 'tb/verilator/ctrl_split_boot'
FIRMWARE = ROOT / 'sw/firmware/ctrl'
IMAGE = FIRMWARE / 'test/ctrl_plat_image.py'
#: The platform's fixture map, the first link's (the split boot simulation's PROVISIONAL).
PROVISIONAL = FIRMWARE / 'test/ctrl_plat_csr.csv'
POINTS = {'1x1': ('endstation_ax7101_1x1_tdm8', 1), '8x8': ('endstation_ax7101_8x8', 2)}
#: The one point the planner's ledger lets the platform image plan past 56 RAMB36 (ctrl_memory.LEDGERED, the
#: ruling of 2026-10-29 on #665): its name for the image and the SoC's memory plan, at that point only.
LEDGERED_POINTS = {('endstation_ax7101_8x8', 2): 'platform-8x8-two-interfaces'}
#: The CPU clocks (hooks_soc.py), the product's first: `sys`, the SoC's system clock, 100 MHz, the product's split
#: CPU clock by the owner's decision of 2026-10-30 on #665; `milan`, the shape's Milan clock, 50 MHz, which this
#: base's MilanSoC still drives the CPU from.
CPU_CLOCKS = ('sys', 'milan')
#: make's parallelism for the native model.
JOBS = 16
#: The testbench's additions: (anchor in the CPU budget harness's sim_main.cpp, its replacement). The
#: counter-change event (contract 2.3's ctr_chg_p_i, with its descriptor) is a one-cycle pulse per interface,
#: cleared each cycle as the grandmaster pulse is, and logged CTRCHG <bus cycle> <if> <type> <index>.
TESTBENCH = (
    ('        put(dut.mbx_gm_change, std::uint8_t(gm_pulse_));\n',
     '        put(dut.mbx_gm_change, std::uint8_t(gm_pulse_));\n'
     '        put(dut.hook_ctr_chg, std::uint8_t(ctr_pulse_));\n'
     '        put(dut.hook_ctr_type, ctr_type_);\n'
     '        put(dut.hook_ctr_index, ctr_index_);\n'),
    ('        gm_pulse_ = 0;\n', '        gm_pulse_ = 0;\n        ctr_pulse_ = 0;\n'),
    ('            } else if (s.op == "txready") {\n',
     '            } else if (s.op == "ctrchg") {\n'
     '                // ctrchg <if> <descriptor_type> <descriptor_index>: the datapath\'s counter-change event\n'
     '                const unsigned i = std::stoul(s.args.at(0));\n'
     '                const std::uint32_t type = std::stoul(s.args.at(1), nullptr, 16);\n'
     '                const std::uint32_t index = std::stoul(s.args.at(2), nullptr, 16);\n'
     '                ctr_type_ = (ctr_type_ & ~(0xffffu << (16 * i))) | (type << (16 * i));\n'
     '                ctr_index_ = (ctr_index_ & ~(0xffffu << (16 * i))) | (index << (16 * i));\n'
     '                ctr_pulse_ |= 1u << i;\n'
     '                std::printf("CTRCHG %llu %u %x %x\\n", ull(sys_), i, type, index);\n'
     '            } else if (s.op == "txready") {\n'),
    ('    bool gm_dirty_ = true;\n',
     '    bool gm_dirty_ = true;\n    unsigned ctr_pulse_ = 0;\n'
     '    std::uint32_t ctr_type_ = 0;\n    std::uint32_t ctr_index_ = 0;\n'),
    ('    dut.mbx_gm_change = 0;\n', '    dut.mbx_gm_change = 0;\n    dut.hook_ctr_chg = 0;\n'),
)
#: The CSR window's addition, completed with the window's base and size: each CPU store into the Milan CSR
#: window, logged CSRW <bus cycle> <offset>, as the CPU's load/store bus presents it.
CSR_STORES = ('            (write ? pass_.store : pass_.load)[r] += 1;\n',
              '            (write ? pass_.store : pass_.load)[r] += 1;\n'
              '            if (write && lsu_address(dut) - {base:#x}u < {size:#x}u)\n'
              '                std::printf("CSRW %llu %x\\n", ull(sys_), unsigned(lsu_address(dut) - {base:#x}u));\n')


def module(name: str, path: Path) -> object:
    """A sibling harness's module, imported read only under its own name."""
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    sys.modules[name] = loaded
    spec.loader.exec_module(loaded)
    return loaded


sys.path.insert(0, str(BUDGET))
s2build = module('budget_build', BUDGET / 'build.py')
boot = module('split_boot_run', BOOT / 'run.py')


def ledgered_point(shape: str, n_if: int) -> str | None:
    """The ledgered point's name when this build is that point, else None."""
    return LEDGERED_POINTS.get((shape, n_if))


def plant_text(source: Path, edits: tuple[tuple[str, str, str], ...]) -> dict[str, str]:
    """Each file a plant edits, as the plant leaves it: every edit (file, unique anchor, replacement) applied in
    order, each anchor found exactly once in the text its earlier edits left."""
    texts: dict[str, str] = {}
    for path, anchor, replacement in edits:
        text = texts.get(path, (source / path).read_text())
        if text.count(anchor) != 1:
            raise RuntimeError(f'plant: an anchor occurs {text.count(anchor)} times in {path}: {anchor[:60]!r}')
        texts[path] = text.replace(anchor, replacement)
    return texts


def planted(out: Path, edits: tuple[tuple[str, str, str], ...]) -> Path:
    """A scratch copy of the firmware's tree with one plant's edits written in, never the checkout's."""
    copy = out / 'ctrl-planted'
    shutil.rmtree(copy, ignore_errors=True)
    shutil.copytree(FIRMWARE, copy, ignore=shutil.ignore_patterns('__pycache__'))
    for path, text in plant_text(FIRMWARE, edits).items():
        (copy / path).write_text(text)
    return copy


def image(out: Path, name: str, point: tuple[str, int], csr_csv: Path, source: Path | None) -> Path:
    """The platform image of one point against one map, from the checkout's tree or a planted copy."""
    shape, n_if = point
    ledgered = ledgered_point(shape, n_if)
    boot.run([sys.executable, '-B', str(IMAGE), '--config', str(ROOT / 'configs' / f'{shape}.yaml'),
              '--interfaces', str(n_if), '--csr-csv', str(csr_csv), '--output', str(out / name),
              '--libc', str(out / 'runtime/libc.a'), '--compiler-runtime', str(out / 'runtime/libcompiler_rt.a'),
              *([] if ledgered is None else ['--ledgered-point', ledgered]),
              *([] if source is None else ['--ctrl-source', str(source)])], out / f'{name}.log', cwd=ROOT)
    return out / name / 'ctrl_app.elf'


def export(out: Path, name: str, selection: dict) -> dict:
    """The SoC's export for one image, in a child process (the CPU generator patches its class)."""
    code = ('import json, sys; from pathlib import Path; sys.path.insert(0, sys.argv[1]); import hooks_soc; '
            's = json.loads(sys.argv[3]); s["elf"] = Path(s["elf"]); '
            'hooks_soc.build(Path(sys.argv[2]), hooks_soc.Build(**s))')
    boot.run([sys.executable, '-B', '-c', code, str(HERE), str(out / name), json.dumps(selection)],
             out / f'{name}.log', cwd=ROOT)
    return json.loads((out / name / 'soc.json').read_text())


def additions(spec: dict) -> tuple[tuple[str, str], ...]:
    """TESTBENCH, then CSR_STORES at the build's CSR window."""
    anchor, replacement = CSR_STORES
    return (*TESTBENCH, (anchor, replacement.format(base=spec['csr_base'], size=spec['csr_size'])))


def testbench(out: Path, spec: dict) -> Path:
    """The CPU budget harness's testbench with its additions, written into the build directory."""
    text = (BUDGET / 'sim_main.cpp').read_text()
    for anchor, replacement in additions(spec):
        if text.count(anchor) != 1:
            raise RuntimeError(f'the testbench addition\'s anchor occurs {text.count(anchor)} times in '
                               f'ctrl_service_budget/sim_main.cpp: {anchor.strip()!r}')
        text = text.replace(anchor, replacement)
    path = out / 'sim_main.cpp'
    path.write_text(text)
    return path


def verilate(out: Path, spec: dict, table: dict[str, int]) -> None:
    """Verilate the exported top with the observers, bind them (the CPU budget harness's configuration header),
    then compile the native model."""
    native = out / 'native'
    flags = f'-O3 -std=c++17 -Wall -Wextra -I{ROOT}/tb/common -I{out} -I{s2build.SIBLING}'
    argv = ['verilator', '--cc', '--exe', '-Wno-fatal', '-Werror-USERERROR', '-Wno-BLKANDNBLK', '-Wno-WIDTH',
            '-Wno-COMBDLY', '-Wno-CASEINCOMPLETE', '--top-module', 'sim', '--Mdir', str(native), '-O3',
            '--output-split', '5000', '--output-split-cfuncs', '500', '-CFLAGS', flags,
            *['-I' + str(i) for i in spec['includes']], str(BUDGET / 'observe.vlt'), *spec['sources'],
            str(testbench(out, spec))]
    s2build.run(argv, out / 'verilate.log', cwd=out / 'soc/gateware')
    missing = s2build.mailbox_pins_missing((out / 'verilate.log').read_text(), out / 'soc/gateware')
    if missing:
        raise RuntimeError(f'the mailbox instances leave ports unconnected (verilate.log, PINMISSING): {missing}')
    s2build.config_header(out, spec, table, s2build.member_paths(native),
                          s2build.code_modules(Path(spec['elf']).with_name('ctrl_app.map')))
    s2build.run(['make', f'-j{JOBS}', '-C', str(native), '-f', 'Vsim.mk', 'Vsim'], out / 'make.log')


def contract_fields() -> dict:
    """The mailbox contract's offsets the configuration header binds (the CPU budget harness's build)."""
    sys.path.insert(0, str(ROOT / 'sw/mailbox'))
    from mailbox_model import load
    contract = load()
    regs = {r.name: r.offset for r in contract.registers}
    return dict(channels=len(contract.channels), filter_en=regs['FILTER_EN'], tmr_cmd=regs['TMR_CMD'],
                ch_base=contract.ch_base, ch_stride=contract.ch_stride,
                tx_head={r.name: r.offset for r in contract.ch_registers}['TX_HEAD'])


def inputs(out: Path, spec: dict) -> list[Path]:
    """Every file the native model is built from or reads when it runs."""
    gateware = out / 'soc/gateware'
    return [Path(spec['elf']), *sorted((out / 'runtime').glob('*.a')), *sorted(gateware.glob('*.init')),
            out / 'budget_config.hpp', out / 'sim_main.cpp', BUDGET / 'sim_main.cpp', BUDGET / 'observe.vlt',
            s2build.SIBLING / 'flash.hpp', HERE / 'hooks_soc.py', HERE / 'hooks_build.py',
            *[Path(s) for s in spec['sources']]]


def digests(out: Path, spec: dict) -> dict[str, str]:
    """Every input's sha256 by its key, and the source trees the image is compiled from."""
    found = s2build.digest(inputs(out, spec), out)
    found['tree:firmware'] = s2build.tree_digest([ROOT / t for t in s2build.FIRMWARE_TREES])
    found['tree:config'] = s2build.tree_digest([ROOT / 'configs' / (spec['shape'] + '.yaml')])
    return found


def build(out: Path, point: str, arm: str, cpu_clock: str,
          plant: tuple[tuple[str, str, str], ...] | None) -> dict:
    """Every build step at one point and CPU clock (CPU_CLOCKS); returns build.json's contents."""
    if cpu_clock not in CPU_CLOCKS:
        raise RuntimeError(f'unknown CPU clock {cpu_clock!r}')
    shape, n_if = POINTS[point]
    out.mkdir(parents=True, exist_ok=True)
    boot.runtime(out)
    selection = dict(shape=shape, n_if=n_if, arm=arm, cpu_clock=cpu_clock, ledgered=ledgered_point(shape, n_if))
    first = image(out, 'image-provisional', (shape, n_if), PROVISIONAL, None)
    export(out, 'soc-provisional', {**selection, 'elf': str(first)})
    csr_csv = out / 'soc-provisional/csr.csv'
    elf = image(out, 'image', (shape, n_if), csr_csv, None if plant is None else planted(out, plant))
    spec = export(out, 'soc', {**selection, 'elf': str(elf)})
    if boot.rows(out / 'soc/csr.csv') != boot.rows(csr_csv):
        raise RuntimeError('the SoC\'s csr.csv depends on the image; the map cannot be generated from it')
    spec.update(elf=str(elf), point=point, plant=[list(e) for e in plant] if plant else None, **contract_fields())
    table = s2build.symbols(elf)
    verilate(out, spec, table)
    spec['symbols'] = {name: table[name] for name in ('ctrl_loop_service', 'main', *s2build.ENTRY_SYMBOLS)}
    spec['inputs'] = digests(out, spec)
    spec['executable_sha256'] = hashlib.sha256((out / 'native/Vsim').read_bytes()).hexdigest()
    (out / 'build.json').write_text(json.dumps(spec, indent=2) + '\n')
    return spec


def reused(out: Path) -> dict:
    """A previous build, refused unless every recorded input still exists with its digest, every input found now
    was recorded, and the native model is the one built."""
    spec = json.loads((out / 'build.json').read_text())
    recorded = spec.get('inputs') or {}
    now = digests(out, spec)
    changed = sorted(k for k in set(recorded) | set(now) if recorded.get(k) != now.get(k))
    if changed:
        raise RuntimeError(f'reused build is stale: {changed[:5]} changed, missing or never recorded')
    executable = out / 'native/Vsim'
    if not executable.is_file() or hashlib.sha256(executable.read_bytes()).hexdigest() != spec['executable_sha256']:
        raise RuntimeError('reused build is stale: the native model changed')
    return spec


if __name__ == '__main__':
    os.environ.setdefault('PYTHONHASHSEED', '0')
    print(json.dumps(build(Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else 'idle',
                           sys.argv[4] if len(sys.argv) > 4 else 'sys', None), indent=2)[:3000])
