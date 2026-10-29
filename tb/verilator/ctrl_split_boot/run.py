#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The split boot simulation (#665): the platform image from reset to ready, its CSR trace and its UART.

Builds, in order, all outside the checkout under --build-dir:
  1. the bare-metal runtime archives (the CPU budget harness's runtime_ssp.py);
  2. the platform image (ctrl_plat_image.py), first against the fixture map
     (ctrl_plat_csr.csv), then against the boot SoC's own csr.csv, which an export with the
     first image gives (the map does not depend on the image: the two
     exports' csr.csv rows must be identical, or the run is refused);
  3. the boot SoC (boot_soc.py) and its native model (sim_main.cpp).
Then it runs the model, saves its exit status beside its log (sim.status), and grades the log:
  - NATIVE: the model's own verdict, which no observation before it discharges:
    its saved exit status is 0, and its checker's tally (verilator_harness.hpp),
    read as the sweep reads a suite log (scripts/suite_tally.py), completed with
    no failure; a regrade reads the same saved status, and refuses a run that
    saved none;
  - BOOT: the ready line, one banner, and the boot-to-ready time against the
    20 s ADP valid time (Milan v1.2 5.6.2/5.6.3, ARCHITECTURE_HW_SW_SPLIT.md);
  - TRACE: the CSR window's writes up to ready: the first fifteen are
    milan_baremetal.c's configure_fabric() for the same config, compiled on
    the host as builder gate 35 runs it on the same seeded register file
    (sw/firmware/ctrl/test/plat_trace.py), then MAAP's one-owner report;
    no write sets ADP_CTRL[0] or PP_CTRL[0];
  - UART: scripts/baremetal_uart_smoke.py's own parse and grade on the
    transcript, each check's verdict printed; and each command's duty against
    #397's 500 ms tick rule and T_svc = 10 ms: its span, and its longest gap
    between two response bytes, which bounds the loop pass that sends them.
--native-controls grades the native controls (NATIVE_CONTROLS), with no
build: a stand-in for the model prints a valid boot's observations, then ends
as each control says, and each must be graded as it requires, on its run and
on its regrade. --self-test grades them first, then builds and runs each
planted control (PLANTS) and requires the grade to report it as a finding of
its own kind: a CSR write skipped as TRACE, a console that holds the loop past
the tick rule as UART.

Exit 0 when NATIVE, BOOT and TRACE pass, every UART duty is within its bounds,
the grader's firmware checks pass and its one listed difference
(fabric-enabled) fails as listed; the checks whose words are the stand-in
register file's are printed with their verdicts and never counted. 1 = a
finding; 2 = refused.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BUDGET = ROOT / 'tb/verilator/ctrl_service_budget'
SIBLING = ROOT / 'tb/verilator/fw_service_budget'
FIRMWARE_TEST = ROOT / 'sw/firmware/ctrl/test'
#: make's parallelism for the native model.
JOBS = 16
#: The simulated time the boot and the commands may take, in ms.
SIM_LIMIT_MS = 2000
#: Milan v1.2 5.6.2/5.6.3: an entity advertises within its 20 s valid time.
READY_BOUND_MS = 20000.0
#: #397's one-hart tick rule, and the control service bound (FR_NFR.md 3.4.1).
TICK_RULE_MS = 500.0
T_SVC_MS = 10.0
#: The grader's check whose verdict on a split image differs by design, and why: a difference for a ruling.
DIFFERS = {
    'fabric-enabled': 'the split never sets ADP_CTRL[0] or PP_CTRL[0], because the core owns ADP and AECP '
                      '(ARCHITECTURE_HW_SW_SPLIT.md section 1): a split image fails this check on any board',
}
#: The grader's checks whose words come from the testbench's stand-in register file, not a datapath and a
#: gPTP peer, and why: each verdict is printed and none is evidence, pass or fail.
STAND_IN = {
    'id-miln': 'ID is the datapath\'s reset value, which the testbench answers',
    'version-gptp-publication': 'VERSION is the datapath\'s reset value, 0x0002_0060 (decision D2), which '
                                'the testbench answers',
    'gptp-identities': 'no gPTP peer and no datapath: GM and parent are the stand-in register file\'s words',
    'gptp-path': 'no gPTP peer and no datapath: AS_PATH_CMD is the stand-in register file\'s word',
    'gptp-pdelay': 'no gPTP peer and no datapath: PDELAY_NS is the stand-in register file\'s word',
    'clkv-fabric-owner': 'no datapath: CLKV_STAT is the stand-in register file\'s word',
    'gptp-locked': 'no gPTP peer and no datapath: CLKV_STAT is the stand-in register file\'s word',
}
#: The planted controls of --self-test: (source file, unique anchor, replacement), and the finding's first word
#: the grade must give, in a run the model completes. A CSR write skipped is caught by the trace; a console that
#: holds the loop past #397's tick rule by the UART duty, its span measured: a spin of 700,000 turns before
#: milan_status's response, about 0.7 s, each turn a load and a store of the counter in sram, about 1 us; the
#: two milan_gettime answers do not spin, so the run ends inside SIM_LIMIT_MS.
PLANTS = {
    'csr-write-skipped': ('plat/ctrl_plat_csr.c', '\twr(csr, CTRL_PLAT_CSR_LWSRP_VID, p->sr_vid);\n', '', 'TRACE'),
    'console-blocks': ('plat/ctrl_plat_console.c', '\tif (is(c, "milan_status")) {\n\t\tstatus(c);',
                       '\tif (is(c, "milan_status")) {\n\t\tfor (volatile uint32_t n = 0; n < 700000u; ++n) {\n\t\t}'
                       '\n\t\tstatus(c);', 'UART'),
}
#: The first link's map: the platform's fixture, at placeholder addresses.
PROVISIONAL = FIRMWARE_TEST / 'ctrl_plat_csr.csv'
#: The file a run saves the native model's exit status in, beside its log, so that a regrade grades it too.
STATUS = 'sim.status'
#: The model's checker's last lines (verilator_harness.hpp), as a native control's stand-in ends its log: a pass,
#: and the failure sim_main.cpp prints when the simulation passes its time limit.
PASSED = '== ctrl_split_boot: checks: 1   failures: 0 ==\nRESULT: PASS\n'
FAILED = ('FAIL: simulation exceeded its time limit\n  [FAIL] simulation completed without boundary failures\n'
          '== ctrl_split_boot: checks: 1   failures: 1 ==\nRESULT: FAIL\n')


class Control(NamedTuple):
    """A native control: how its stand-in ends (its exit status and its log's end), whether the run's saved status
    is kept for the regrade, and the verdicts the run and the regrade must give."""

    status: int
    ending: str
    kept: bool
    run: str
    regrade: str


#: The native controls. Each stand-in's observations before its end are a valid boot's, so the only finding a
#: control may give is NATIVE: the passing control none; a nonzero exit, a failed or an incomplete tally one, on
#: the run and on its regrade; a run whose saved status is gone (an older build directory) one on its regrade.
NATIVE_CONTROLS = {
    'native-passes': Control(0, PASSED, True, 'PASS', 'PASS'),
    'native-exits-nonzero': Control(1, PASSED, True, 'NATIVE', 'NATIVE'),
    'native-tally-failed': Control(0, FAILED, True, 'NATIVE', 'NATIVE'),
    'native-incomplete': Control(0, '', True, 'NATIVE', 'NATIVE'),
    'native-fails-and-exits-nonzero': Control(1, FAILED, True, 'NATIVE', 'NATIVE'),
    'native-status-not-saved': Control(0, PASSED, False, 'PASS', 'NATIVE'),
}
#: A boot's lines and the answers the smoke grader passes, as the stand-in prints them.
BANNER = 'Milan split control firmware: boot\r\nMilan split control firmware: ready\r\n'
ANSWERS = (('milan_status', 'ID=4d494c4e VERSION=00020060 PTP_CTRL=00000001 ADP_CTRL=00000000 PP_CTRL=00000000 '
                            'PP_STAT=00000000 AEM=loaded\r\nGPTP_GM=001bc5fffe001122 GPTP_PARENT=001bc5fffe334455 '
                            'PDELAY_NS=600 AS_PATH_COUNT=3 AS_PATH_GEN=7 CLKV_STAT=00010002 SYNC=1 ASCAPABLE=1 '
                            'TU=0 GPTP_LAT=029000db\r\nTAI_NS=0x0000000000001000\r\n'),
           ('milan_gettime', 'TAI_NS=0x0000000000002000\r\n'), ('milan_gettime', 'TAI_NS=0x0000000000003000\r\n'))


def run(argv: list[str], log: Path, cwd: Path | None = None) -> None:
    """One build step in the foreground, its whole output in its log."""
    print('COMMAND', ' '.join(argv), flush=True)
    with log.open('w') as sink:
        result = subprocess.run(argv, cwd=cwd, stdout=sink, stderr=subprocess.STDOUT, check=False)
    if result.returncode:
        raise RuntimeError(f'{Path(argv[0]).name} exited {result.returncode}; see {log}')


def runtime(out: Path) -> tuple[Path, Path]:
    """The bare-metal runtime archives, as the CPU budget harness builds them."""
    import litex
    import pythondata_software_compiler_rt as compiler_rt
    import pythondata_software_picolibc as picolibc
    run([sys.executable, '-B', str(BUDGET / 'runtime_ssp.py'), '--picolibc', picolibc.data_location,
         '--compiler-rt', compiler_rt.data_location, '--litex-software',
         str(Path(litex.__file__).parent / 'soc/software'), '--output', str(out / 'runtime')], out / 'runtime.log')
    return out / 'runtime/libc.a', out / 'runtime/libcompiler_rt.a'


def image(out: Path, name: str, point: tuple[str, int], csr_csv: Path, archives: tuple[Path, Path],
          source: Path | None = None) -> Path:
    """The platform image of one point (shape, interfaces) against one map, from the checkout's tree or a
    planted copy."""
    shape, n_if = point
    run([sys.executable, '-B', str(FIRMWARE_TEST / 'ctrl_plat_image.py'), '--config',
         str(ROOT / 'configs' / f'{shape}.yaml'), '--interfaces', str(n_if), '--csr-csv', str(csr_csv),
         '--output', str(out / name), '--libc', str(archives[0]), '--compiler-runtime', str(archives[1]),
         *([] if source is None else ['--ctrl-source', str(source)])], out / f'{name}.log', cwd=ROOT)
    return out / name / 'ctrl_app.elf'


def export(out: Path, name: str, shape: str, elf: Path, n_if: int) -> dict:
    """The boot SoC's export for one image, in a child process (the CPU generator patches its class)."""
    code = ('import json, sys; from pathlib import Path; sys.path.insert(0, sys.argv[1]); import boot_soc; '
            'print(json.dumps(boot_soc.build(Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4]), int(sys.argv[5]))))')
    run([sys.executable, '-B', '-c', code, str(HERE), str(out / name), shape, str(elf), str(n_if)],
        out / f'{name}.log', cwd=ROOT)
    return json.loads((out / name / 'soc.json').read_text())


def verilate(out: Path, spec: dict) -> Path:
    """The native model of the exported top and this testbench."""
    native = out / 'native'
    (out / 'boot_config.hpp').write_text('\n'.join([
        '// GENERATED by tb/verilator/ctrl_split_boot/run.py; DO NOT EDIT.', '#pragma once', '#include <cstdint>',
        f'constexpr std::uint64_t sys_hz = {spec["sys_hz"]}ULL;',
        f'constexpr std::uint64_t cpu_hz = {spec["cpu_hz"]}ULL;',
        f'constexpr std::uint32_t csr_size = {spec["csr_size"]}u;',
        f'constexpr std::uint64_t sim_limit_ps = {SIM_LIMIT_MS}ULL * 1000000000ULL;',
        'constexpr const char* ready_line = "Milan split control firmware: ready\\r\\n";',
        'constexpr const char* stop_prefix = "Milan split: ";', '']))
    flags = f'-O3 -std=c++17 -Wall -Wextra -I{ROOT}/tb/common -I{out} -I{SIBLING}'
    run(['verilator', '--cc', '--exe', '-Wno-fatal', '-Werror-USERERROR', '-Wno-BLKANDNBLK', '-Wno-WIDTH',
         '-Wno-COMBDLY', '-Wno-CASEINCOMPLETE', '--top-module', 'sim', '--Mdir', str(native), '-O3',
         '--output-split', '5000', '--output-split-cfuncs', '500', '-CFLAGS', flags,
         *['-I' + str(i) for i in spec['includes']], *spec['sources'], str(HERE / 'sim_main.cpp')],
        out / 'verilate.log', cwd=out / 'soc/gateware')
    run(['make', f'-j{JOBS}', '-C', str(native), '-f', 'Vsim.mk', 'Vsim'], out / 'make.log')
    return native / 'Vsim'


def rows(csr_csv: Path) -> list[str]:
    """A csr.csv's rows, without its banner (which carries the export's time)."""
    return [ln for ln in csr_csv.read_text().splitlines() if not ln.startswith('#')]


def planted(out: Path, plant: str) -> Path:
    """A copy of the firmware's tree with one plant written into it."""
    import shutil
    path, old, new, _ = PLANTS[plant]
    copy = out / 'ctrl'
    shutil.copytree(ROOT / 'sw/firmware/ctrl', copy, ignore=shutil.ignore_patterns('__pycache__'))
    text = (copy / path).read_text()
    if text.count(old) != 1:
        raise RuntimeError(f'plant {plant}: its anchor occurs {text.count(old)} times in {path}')
    (copy / path).write_text(text.replace(old, new))
    return copy


def build(out: Path, shape: str, n_if: int, plant: str | None = None) -> tuple[Path, dict]:
    """Every build step; the native model and the boot SoC's spec."""
    out.mkdir(parents=True, exist_ok=True)
    archives = runtime(out)
    first = image(out, 'image-provisional', (shape, n_if), PROVISIONAL, archives)
    export(out, 'soc-provisional', shape, first, n_if)
    csr_csv = out / 'soc-provisional/csr.csv'
    elf = image(out, 'image', (shape, n_if), csr_csv, archives, None if plant is None else planted(out, plant))
    spec = export(out, 'soc', shape, elf, n_if)
    if rows(out / 'soc/csr.csv') != rows(csr_csv):
        raise RuntimeError('the boot SoC\'s csr.csv depends on the image; the map cannot be generated from it')
    spec['elf'] = str(elf)
    return verilate(out, spec), spec


def lines(log: str, tag: str) -> list[list[str]]:
    """The log's lines of one tag, split."""
    return [ln.split()[1:] for ln in log.splitlines() if ln.startswith(tag + ' ')]


def expected_writes(shape: str, work: Path) -> list[tuple[int, int]]:
    """configure_fabric()'s writes for the shape (gate 35's host run), then MAAP's one-owner report."""
    sys.path.insert(0, str(FIRMWARE_TEST))
    sys.path.insert(0, str(ROOT / 'sw/firmware/gtest'))
    import plat_trace
    want = plat_trace.baremetal_writes(ROOT / 'configs' / f'{shape}.yaml', work)
    words = dict(want)
    return want + [(0x654, words[0x654] & ~1), (0x750, words[0x750] & ~1), (0x6CC, words[0x6CC] & ~1)]


def native(log: str, status: int | None) -> tuple[list[str], str]:
    """The model's own verdict: its saved exit status, and its checker's tally read as the sweep reads a suite log
    (suite_tally.scan, is_nocount, log_reports_failure), so a tally that is missing or measured nothing is a run
    that did not complete. Its findings, and its report line."""
    import suite_tally
    findings = []
    if status is None:
        findings.append(f'NATIVE: the run saved no exit status ({STATUS}), so how the model ended is unknown')
    elif status != 0:
        findings.append(f'NATIVE: the model exited {status}')
    checks, failures, matched, unparsed, skipped = suite_tally.scan(log)
    errors = [ln.strip() for ln in log.splitlines() if ln.startswith('FAIL:')]
    reason, failed = suite_tally.log_reports_failure(log)
    if suite_tally.is_nocount(checks, failures, matched, skipped):
        findings.append('NATIVE: the model printed no tally: it did not complete')
    elif unparsed:
        findings.append(f'NATIVE: a tally line the sweep cannot read: {unparsed[0]}')
    elif failed:
        findings.append(f'NATIVE: the model\'s log reports a failure: {reason}{"; " if errors else ""}'
                        f'{"; ".join(errors)}')
    tally = matched[-1][3] if matched else 'no tally'
    return findings, f'NATIVE exit status {"not saved" if status is None else status}; {tally}'


def grade(log: str, transcript: str, spec: dict, work: Path, status: int | None) -> tuple[list[str], list[str]]:
    """The findings and the report lines; `status` is the model's saved exit status, None when there is none."""
    sys.path.insert(0, str(ROOT / 'scripts'))
    import baremetal_uart_smoke as smoke
    findings, line = native(log, status)
    report = [line]
    to_ms = 1000.0 / spec['sys_hz']
    ready = lines(log, 'READY')
    if not ready:
        stopped = lines(log, 'STOPPED')
        findings.append(f'BOOT: no ready line{" (a stage refused)" if stopped else ""}; transcript {transcript!r}')
        return findings, report
    ready_at = int(ready[0][0])
    boot_ms = ready_at * to_ms
    banner = transcript.count('Milan split control firmware: boot')
    report.append(f'BOOT ready at bus cycle {ready_at} ({ready_at * spec["cpu_hz"] // spec["sys_hz"]} CPU cycles): '
                  f'{boot_ms:.3f} ms against {READY_BOUND_MS:.0f} ms; banners {banner}')
    if boot_ms > READY_BOUND_MS or banner != 1:
        findings.append(f'BOOT: {boot_ms:.3f} ms, {banner} banner(s)')
    writes = [(int(c), int(o, 16), int(v, 16)) for c, o, v in lines(log, 'CSRW') if int(c) <= ready_at]
    want = expected_writes(spec['shape'], work)
    got = [(o, v) for _, o, v in writes[:len(want)]]
    same = got == want
    report.append(f'TRACE {len(writes)} window writes before ready; the first {len(want)} '
                  f'{"equal" if same else "DIFFER FROM"} configure_fabric()\'s {len(want) - 3} and MAAP\'s one-owner 3')
    if not same:
        findings.append(f'TRACE: {[(hex(o), hex(v)) for o, v in got]} != {[(hex(o), hex(v)) for o, v in want]}')
    enables = [(o, v) for _, o, v in writes if o in (0x600, 0x920) and v & 1]
    if enables:
        findings.append(f'TRACE: a compatibility enable set: {enables}')
    uart = [(int(c), int(b, 16)) for c, b in lines(log, 'UART')]
    commands = [(int(c), name) for c, name in lines(log, 'IN')]
    answers = []
    for k, (start, name) in enumerate(commands):
        end = commands[k + 1][0] if k + 1 < len(commands) else uart[-1][0] + 1
        sent = [(c, b) for c, b in uart if start <= c < end]
        text = bytes(b for _, b in sent).decode('ascii', 'replace')
        answers.append(text)
        span = (sent[-1][0] - start) * to_ms if sent else float('inf')
        gap = max((b[0] - a[0] for a, b in zip(sent, sent[1:])), default=0) * to_ms
        first = (sent[0][0] - start) * to_ms if sent else float('inf')
        report.append(f'UART {name}: {len(sent)} bytes; span {span:.3f} ms; to the first byte {first:.3f} ms; '
                      f'longest gap between bytes {gap:.3f} ms; '
                      f'against {TICK_RULE_MS:.0f} ms and T_svc {T_SVC_MS:.0f} ms')
        if span > TICK_RULE_MS or gap > T_SVC_MS or first > T_SVC_MS:
            findings.append(f'UART: {name} holds the loop past its bound ({span:.3f} / {gap:.3f} / {first:.3f} ms)')
    if len(answers) != 3:
        findings.append(f'UART: {len(answers)} commands answered of 3')
        return findings, report
    try:
        checks = smoke.grade(answers[0], answers[1], answers[2])
    except ValueError as error:
        findings.append(f'UART: the grader refused the transcript: {error}')
        return findings, report
    for name, ok, detail in checks:
        why = (f'; a difference by design: {DIFFERS[name]}' if name in DIFFERS and not ok else
               f'; not evidence: {STAND_IN[name]}' if name in STAND_IN else '')
        report.append(f'GRADER {name}: {"PASS" if ok else "FAIL"} ({detail}){why}')
        if ok == (name in DIFFERS) and name not in STAND_IN:
            findings.append(f'GRADER: {name} {"passes, against its listed difference" if ok else "fails"} ({detail})')
    return findings, report


def saved_status(out: Path) -> int | None:
    """The model's exit status a run saved in `out`, or None when it saved none."""
    try:
        return int((out / STATUS).read_text())
    except (OSError, ValueError):
        return None


def point(out: Path, shape: str, n_if: int, regrade: bool, plant: str | None = None,
          model: tuple[Path, dict] | None = None) -> tuple[list[str], list[str]]:
    """Build (unless regrading, or given the model and its spec: a native control's stand-in), run and grade one
    point; its findings and report."""
    if regrade:
        spec = json.loads((out / 'soc/soc.json').read_text())
    else:
        exe, spec = build(out, shape, n_if, plant) if model is None else model
        (out / STATUS).unlink(missing_ok=True)
        # the model reads the image's ROM banks from the export's .init files
        with (out / 'sim.log').open('w') as sink:
            result = subprocess.run([str(exe), str(out / 'transcript.txt')], stdout=sink,
                                    stderr=subprocess.STDOUT, check=False, cwd=out / 'soc/gateware')
        (out / STATUS).write_text(f'{result.returncode}\n')
        print(f'COMMAND Vsim exited {result.returncode}')
    return grade((out / 'sim.log').read_text(), (out / 'transcript.txt').read_text(), spec, out / 'baremetal',
                 saved_status(out))


def stand_in(out: Path, shape: str, n_if: int, control: Control) -> tuple[Path, dict]:
    """A native control's model, and the spec its export would give: a program that writes a boot's transcript and
    prints a valid boot's observations as sim_main.cpp prints them (configure_fabric()'s writes and MAAP's
    one-owner report, the ready line, and the three commands answered as the grader passes them), then ends its log
    and exits as the control says."""
    spec = {'sys_hz': 100_000_000, 'cpu_hz': 50_000_000, 'shape': shape, 'interfaces': n_if}
    rows = [f'CSRW {k + 1} {o:03x} {v:08x}' for k, (o, v) in enumerate(expected_writes(shape, out / 'oracle'))]
    rows.append('READY 10000')
    for k, (command, answer) in enumerate(ANSWERS):
        start = 20000 + 100000 * k
        rows += [f'IN {start} {command}', *(f'UART {start + 100 * (j + 1)} {b:02x}'
                                             for j, b in enumerate(answer.encode()))]
    log = '\n'.join(rows) + '\n' + control.ending
    transcript = BANNER + ''.join(answer for _, answer in ANSWERS)
    (out / 'soc/gateware').mkdir(parents=True, exist_ok=True)
    (out / 'soc/soc.json').write_text(json.dumps(spec))
    exe = out / 'stand-in'
    exe.write_text(f'#!{sys.executable}\nimport pathlib, sys\npathlib.Path(sys.argv[1]).write_bytes('
                   f'{transcript.encode()!r})\nsys.stdout.write({log!r})\nsys.exit({control.status})\n')
    exe.chmod(0o755)
    return exe, spec


def verdict(findings: list[str]) -> str:
    """PASS for none; NATIVE when every finding is the model's own verdict; OTHER when the observations failed."""
    return 'PASS' if not findings else 'NATIVE' if all(f.startswith('NATIVE:') for f in findings) else 'OTHER'


def native_controls(out: Path, shape: str, n_if: int) -> int:
    """Each native control graded on its run and on its regrade; the number not graded as they require."""
    wrong = 0
    for name, control in NATIVE_CONTROLS.items():
        where = out / name
        where.mkdir(parents=True, exist_ok=True)
        ran, _ = point(where, shape, n_if, False, model=stand_in(where, shape, n_if, control))
        if not control.kept:
            (where / STATUS).unlink(missing_ok=True)
        regraded, _ = point(where, shape, n_if, True)
        got = (verdict(ran), verdict(regraded))
        ok = got == (control.run, control.regrade)
        wrong += not ok
        print(f'NATIVE-CONTROL {name}: {"as required" if ok else "WRONG"} (run {got[0]}, regrade {got[1]}; '
              f'required {control.run}, {control.regrade}); findings: {ran} / {regraded}')
    print(f'ctrl_split_boot native controls: {len(NATIVE_CONTROLS) - wrong} of {len(NATIVE_CONTROLS)} as required')
    return wrong


def self_test(out: Path, shape: str, n_if: int) -> int:
    """Every native control graded as it requires, then every plant graded a finding of its own kind in a run the
    model completed (no NATIVE finding), so its observations are a whole run's; 0 when each is."""
    wrong = native_controls(out / 'native', shape, n_if)
    escaped = 0
    for plant, (_, _, _, kind) in PLANTS.items():
        findings, _ = point(out / f'plant-{plant}', shape, n_if, False, plant)
        completed = not any(f.startswith('NATIVE:') for f in findings)
        caught = completed and any(f.startswith(kind + ':') for f in findings)
        escaped += not caught
        print(f'PLANT {plant}: {"caught" if caught else "ESCAPED"} ({kind}; '
              f'{"the run completed" if completed else "the model did not complete its run"}); findings: {findings}')
    print(f'ctrl_split_boot self-test: {len(NATIVE_CONTROLS) - wrong} of {len(NATIVE_CONTROLS)} native controls as '
          f'required; {len(PLANTS) - escaped} of {len(PLANTS)} plants caught')
    return 1 if escaped or wrong else 0


def main() -> int:
    """Build, run and grade one point."""
    parser = argparse.ArgumentParser(description=__doc__.split('\n', 1)[0])
    parser.add_argument('--build-dir', type=Path, required=True)
    parser.add_argument('--shape', default='endstation_ax7101_1x1_tdm8')
    parser.add_argument('--interfaces', type=int, choices=(1, 2), default=1)
    parser.add_argument('--regrade', action='store_true', help='grade the log of an earlier run in --build-dir')
    parser.add_argument('--native-controls', action='store_true',
                        help='grade every native control (NATIVE_CONTROLS) under --build-dir, with no build')
    parser.add_argument('--self-test', action='store_true',
                        help='grade every native control, then build and run every planted control (PLANTS) under '
                             '--build-dir; each must be graded as it requires')
    args = parser.parse_args()
    out = args.build_dir.resolve()
    try:
        if args.native_controls:
            return 1 if native_controls(out, args.shape, args.interfaces) else 0
        if args.self_test:
            return self_test(out, args.shape, args.interfaces)
        findings, report = point(out, args.shape, args.interfaces, args.regrade)
    except (RuntimeError, OSError, ValueError, KeyError) as error:
        print(f'REFUSED: {error}')
        return 2
    print('\n'.join(report))
    for finding in findings:
        print(f'FINDING: {finding}')
    print(f'ctrl_split_boot: {"FAIL" if findings else "PASS"} ({len(findings)} finding(s))')
    return 1 if findings else 0


if __name__ == '__main__':
    raise SystemExit(main())
