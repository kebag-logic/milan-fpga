#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The REBOOT simulation (#871): an AECP REBOOT on the split CPU, the reset, and the boot after it.

The split platform image runs on the split SoC of reboot_soc.py: the CPU, its
memory, the mailbox, the flash and the AECP REBOOT's reset port. The
testbench (sim_main.cpp) drives the mailbox's datapath side from a script and
stands for KL_reboot_ctrl on the reset port. A run that reaches the
configuration reload writes the flash's journal, and the next run boots from
it, since the reload boots the same flash (docs/design/REBOOT_RESET.md).

The runs, all at the shipping shape endstation_ax7101_1x1_tdm8, one interface:
  reboot  from a blank flash. A REBOOT of every other target is refused. A
          second controller registers. Every item is read at its default, set
          away from it where the shape allows, and read again. The journal
          write that saves them starts, and inside it controller 1's REBOOT of
          the ENTITY. Then the reset; frames given after the reset port fired
          must not be taken.
  after   from that journal: every item is read again, and the run waits for
          ADP's first ENTITY_AVAILABLE.
  cut     from that journal: two names change, and the run is cut after the
          first page program of the write that saves them.
  replay  from the cut's journal: the names are read again.
Each is graded from its log:
  NATIVE   the model's exit status and its checker's tally;
  REFUSE   (#871 item 5) each refused REBOOT's status as IEEE 1722.1-2021
           7.4.43 states, at cdl 16, notifying no one, with no reset and the
           entity still answering;
  ORDER    (item 2) the SUCCESS, its notification (7.5.2) and ENTITY_DEPARTING
           (Milan v1.2 5.6.3.3) leave the mailbox before the reset port fires.
           No command is answered after the SUCCESS, and no frame given after
           the port fired is taken;
  JOURNAL  (item 4) the REBOOT came inside the write, the drain ended because
           the state was durable, and the write completed: after the reset
           every item reads back as before it. The cut's replay reads back one
           whole snapshot, never a mix;
  RESTORE  (item 1) Milan's eight saved items and the binding, by the #396
           release grader (tb/tools/torture_campaign.py,
           check_release_state_restored);
  ADP      (item 1) ADP advertises again within its valid time, from the
           REBOOT command (Milan v1.2 5.6.2, Table 5.50);
  BOUND    the measured request-to-reset cycles.
--self-test also builds each planted image (PLANTS) and requires its finding,
and plants each grader control (CONTROLS) into a clean log.

Exit 0 is a pass, 1 a finding and 2 a refusal.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BUDGET = ROOT / 'tb/verilator/ctrl_service_budget'
SIBLING = ROOT / 'tb/verilator/fw_service_budget'
BOOT = ROOT / 'tb/verilator/ctrl_split_boot'
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(BUDGET))
sys.path.insert(0, str(ROOT / 'tb/tools'))
import frames  # noqa: E402  the CPU budget harness's frame builders, read only
import torture_campaign  # noqa: E402  the #396 release grader, read only


def _module(name: str, path: Path) -> object:
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


boot = _module('ctrl_split_boot_run', BOOT / 'run.py')  # the split boot simulation's build steps, read only

SHAPE = 'endstation_ax7101_1x1_tdm8'
POINT = (SHAPE, 1)
JOBS = 4
#: KL_reboot_ctrl at the AX7101 (docs/design/REBOOT_RESET.md section 3): the drain's deadline, the egress
#: wait's bound with its tick, and the PHY hold
DRAIN_MS, EGRESS_MS, HOLD_MS = 10_000, 3, 3_500
#: The simulation's own limits: the drain is stopped here (its write completes in milliseconds), and the hold runs
#: this long before the run ends at the reload
DRAIN_CAP_MS, HOLD_WINDOW_MS = 1_000, 50
#: The flash's erase and page program times, in milliseconds: a write spans ticks, so a REBOOT can land inside it
ERASE_MS, PROGRAM_MS = 20, 0.5
SIM_LIMIT_S = 8
#: Milan v1.2 5.6.2: valid_time 10, in IEEE 1722.1-2021 6.2.1.6's units of two seconds
VALID_TIME_MS = 20_000
STATUS = 'sim.status'

CTL1 = (0x0011223344556677, 0x020000000081)
CTL2 = (0x0099AABBCCDDEEFF, 0x020000000082)
TALKER, LATE_TALKER = 0x00221100AABBCCDD, 0x00221100AABBCCEE
#: AEM command_types (IEEE 1722.1-2021 Table 7-126)
GET_CONFIGURATION, SET_STREAM_FORMAT, GET_STREAM_FORMAT = 0x0007, 0x0008, 0x0009
SET_STREAM_INFO, GET_STREAM_INFO, SET_NAME, GET_NAME = 0x000E, 0x000F, 0x0010, 0x0011
GET_SAMPLING_RATE, SET_CLOCK_SOURCE, GET_CLOCK_SOURCE = 0x0015, 0x0016, 0x0017
REGISTER_UNSOLICITED, REBOOT, GET_AUDIO_MAP, REMOVE_AUDIO_MAPPINGS = 0x0024, 0x002A, 0x002B, 0x002D
#: descriptor types (Table 7-1)
ENTITY, AUDIO_UNIT, STREAM_INPUT, STREAM_OUTPUT, STREAM_PORT_INPUT = 0x0000, 0x0002, 0x0005, 0x0006, 0x000E
MEMORY_OBJECT, CLOCK_DOMAIN = 0x000B, 0x0024
#: AECP statuses (Table 7-127)
SUCCESS, NOT_IMPLEMENTED, NO_SUCH_DESCRIPTOR, ENTITY_LOCKED = 0, 1, 2, 3
BAD_ARGUMENTS, NOT_SUPPORTED = 7, 11
#: the mailbox channels (sw/mailbox/mailbox.yaml)
CH_ADP, CH_ACMP, CH_AECP = 0, 1, 2
#: The items a #396 power cycle restores (tb/tools/torture_campaign.py RELEASE_PERSISTED_ITEMS), with the reason
#: an item this shape cannot set away from its default is read, never graded
UNSETTABLE = {'configuration': 'the builder ships one configuration',
              'sampling_rate': 'the shape advertises one AUDIO_UNIT rate, 48 kHz'}
#: SET_STREAM_FORMAT's other format for STREAM_INPUT 0 at this shape (the builder's AEM overlay, 8 channels)
OTHER_FORMAT = 0x0215022002006000
REFUSALS = (('refuse-short', b'\0\0', BAD_ARGUMENTS), ('refuse-input', bytes(4), NOT_SUPPORTED),
            ('refuse-memory', bytes(4), NOT_SUPPORTED), ('refuse-index', bytes(4), NO_SUCH_DESCRIPTOR))


def be(value: int, size: int) -> bytes:
    """Big-endian."""
    return value.to_bytes(size, 'big')


def target(descriptor_type: int, index: int) -> bytes:
    """{descriptor_type, descriptor_index}, Figure 7-68's body and every read's first four bytes."""
    return be(descriptor_type, 2) + be(index, 2)


@dataclass(frozen=True)
class Entity:
    """The entity under test, from the image's generated identity (adp_entity_gen.h)."""
    entity_id: int
    mac: int


def entity_of(image: Path) -> Entity:
    """The entity's ID and MAC as the image was generated with them."""
    text = (image / 'adp_entity_gen.h').read_text()
    eid = int(re.search(r'\.entity_id = (0x[0-9A-Fa-f]+)ull', text)[1], 16)
    mac = int(re.search(r'\.mac = (0x[0-9A-Fa-f]+)ull', text)[1], 16)
    return Entity(eid, mac)


class Script:
    """A run's script and the tag each frame was sent under, by its sequence_id."""

    def __init__(self, entity: Entity) -> None:
        self.entity = entity
        self.lines: list[str] = []
        self.seq = 0x100
        self.tags: dict[int, str] = {}

    def step(self, line: str) -> None:
        """One script step, as sim_main.cpp reads it."""
        self.lines.append(line)

    def aem(self, tag: str, command: int, body: bytes, ctl: tuple[int, int] = CTL1, pause: int = 5) -> None:
        """An AEM command (IEEE 1722.1-2021 9.2.1.2) from a controller, then a pause for its answer."""
        self.seq += 1
        self.tags[self.seq] = tag
        to = frames.Aem(self.entity.entity_id, ctl[0], ctl[1], self.entity.mac, self.seq)
        self.step(f'send {tag} {frames.aem_command(to, command, body).hex()}')
        if pause:
            self.step(f'wait {pause}')

    def acmp(self, tag: str, message: str, talker: int, pause: int = 5) -> None:
        """An ACMP command to the entity's sink 0 (IEEE 1722.1-2021 8.2.1) from controller 1."""
        self.seq += 1
        self.tags[self.seq] = tag
        fields = frames.Acmp(controller=CTL1[0], talker=talker, listener=self.entity.entity_id, sequence=self.seq)
        self.step(f'send {tag} {frames.acmp(frames.ACMP[message], CTL1[1], fields).hex()}')
        if pause:
            self.step(f'wait {pause}')

    def text(self) -> str:
        """The script's text."""
        return '\n'.join(self.lines) + '\n'


#: Each item's read: (tag, AEM command_type or None for ACMP's GET_RX_STATE, body)
READS = {
    'configuration': (GET_CONFIGURATION, bytes(4)),
    'sampling_rate': (GET_SAMPLING_RATE, target(AUDIO_UNIT, 0)),
    'stream_format': (GET_STREAM_FORMAT, target(STREAM_INPUT, 0)),
    'presentation_time_offset': (GET_STREAM_INFO, target(STREAM_OUTPUT, 0)),
    'channel_mappings': (GET_AUDIO_MAP, target(STREAM_PORT_INPUT, 0) + bytes(4)),
    'clock_source': (GET_CLOCK_SOURCE, target(CLOCK_DOMAIN, 0)),
    'entity_names': ((GET_NAME, target(ENTITY, 0) + be(0, 2) + bytes(2)),
                     (GET_NAME, target(ENTITY, 0) + be(1, 2) + bytes(2))),
    'object_names': (GET_NAME, target(STREAM_INPUT, 0) + bytes(4)),
    'stream_binding': (None, b''),
}


def name_body(descriptor_type: int, index: int, name_index: int, name: str) -> bytes:
    """SET_NAME's body (7.4.17.1): the target, name_index, configuration 0 and the 64-byte name."""
    return target(descriptor_type, index) + be(name_index, 2) + bytes(2) + name.encode().ljust(64, b'\0')


def read_all(s: Script, prefix: str) -> None:
    """Every item's read, each tagged prefix-item[-k]."""
    for item, read in READS.items():
        reads = read if isinstance(read[0], tuple) else (read,)
        for k, (command, body) in enumerate(reads):
            tag = f'{prefix}-{item}' + (f'-{k}' if len(reads) > 1 else '')
            if command is None:
                s.acmp(tag, 'GET_RX_STATE', 0)
            else:
                s.aem(tag, command, body)


def set_all(s: Script) -> None:
    """Every item the shape lets a controller set, away from its default."""
    s.aem('set-entity-name', SET_NAME, name_body(ENTITY, 0, 0, 'after the reboot'))
    s.aem('set-group-name', SET_NAME, name_body(ENTITY, 0, 1, 'reboot group'))
    s.aem('set-object-name', SET_NAME, name_body(STREAM_INPUT, 0, 0, 'reboot input'))
    s.aem('set-stream-format', SET_STREAM_FORMAT, target(STREAM_INPUT, 0) + be(OTHER_FORMAT, 8))
    # Milan v1.2 5.3.7.6: MSRP_ACC_LAT_VALID with the presentation time offset (Figure 7-40)
    info = bytearray(84)
    info[0:4] = target(STREAM_OUTPUT, 0)
    info[4:8] = be(0x20000000, 4)
    info[24:28] = be(1_500_000, 4)
    s.aem('set-presentation-time-offset', SET_STREAM_INFO, bytes(info))
    # REMOVE_AUDIO_MAPPINGS (7.4.46.1): one mapping, stream channel 7 to cluster 7
    s.aem('set-channel-mappings', REMOVE_AUDIO_MAPPINGS,
          target(STREAM_PORT_INPUT, 0) + be(1, 2) + bytes(2) + be(0, 2) + be(7, 2) + be(7, 2) + be(0, 2))
    s.aem('set-clock-source', SET_CLOCK_SOURCE, target(CLOCK_DOMAIN, 0) + be(1, 2) + bytes(2))
    s.acmp('set-stream-binding', 'BIND_RX', TALKER)


def reboot_script(entity: Entity, full: bool = True) -> Script:
    """The reboot run's script; `full` False keeps the refusals, the registration and the REBOOT alone."""
    s = Script(entity)
    s.step('ready')
    s.step('wait 5')
    for tag, body, _ in REFUSALS:
        kind = {'refuse-input': target(STREAM_INPUT, 0), 'refuse-memory': target(MEMORY_OBJECT, 0),
                'refuse-index': target(ENTITY, 1)}.get(tag, body)
        s.aem(tag, REBOOT, kind)
    s.aem('in-service', GET_CONFIGURATION, bytes(4))
    s.aem('register', REGISTER_UNSOLICITED, bytes(4), CTL2)
    if full:
        read_all(s, 'default')
        set_all(s)
        read_all(s, 'pre')
        s.step('erase')
    s.aem('reboot', REBOOT, target(ENTITY, 0), pause=2)
    s.aem('after-success', GET_CONFIGURATION, bytes(4), pause=0)
    s.step('request 300')
    s.aem('after-port', GET_CONFIGURATION, bytes(4), pause=0)
    s.acmp('after-port-bind', 'BIND_RX', LATE_TALKER, pause=0)
    s.step(f'reset {DRAIN_CAP_MS + 500}')
    return s


def after_script(entity: Entity) -> Script:
    """The boot after the reset: every item, then ADP's first ENTITY_AVAILABLE (Table 5.50: TMR_DELAY to 4 s)."""
    s = Script(entity)
    s.step('ready')
    s.step('wait 5')
    read_all(s, 'post')
    s.step('adp 4100')
    return s


def cut_script(entity: Entity) -> Script:
    """Two names change; the run is cut after the first page program of the write that saves them."""
    s = Script(entity)
    s.step('ready')
    s.step('wait 5')
    s.aem('cut-entity-name', SET_NAME, name_body(ENTITY, 0, 0, 'cut entity'))
    s.aem('cut-object-name', SET_NAME, name_body(STREAM_INPUT, 0, 0, 'cut input'))
    s.step('erase')
    s.step('program 1')
    s.step('cut')
    return s


def replay_script(entity: Entity) -> Script:
    """The two names after the cut."""
    s = Script(entity)
    s.step('ready')
    s.step('wait 5')
    s.aem('replay-entity-name', GET_NAME, target(ENTITY, 0) + bytes(4))
    s.aem('replay-object-name', GET_NAME, target(STREAM_INPUT, 0) + bytes(4))
    return s


# ---- the build ---------------------------------------------------------------------------------------------

def exported(out: Path, name: str, elf: Path, flash_map: Path) -> dict:
    """reboot_soc's export for one image, in a child process (the CPU generator patches its class)."""
    code = ('import json, sys; from pathlib import Path; sys.path.insert(0, sys.argv[1]); import reboot_soc; '
            'print(json.dumps(reboot_soc.build(Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4]), 1, '
            'Path(sys.argv[5]))))')
    boot.run([sys.executable, '-B', '-c', code, str(HERE), str(out / name), SHAPE, str(elf), str(flash_map)],
             out / f'{name}.log', cwd=ROOT)
    return json.loads((out / name / 'soc.json').read_text())


def verilate(out: Path, spec: dict, flash_map: Path) -> Path:
    """The native model of the exported top and this testbench."""
    native = out / 'native'
    journal = json.loads((flash_map / 'flash_port.json').read_text())['journal']
    cyc = spec['sys_hz'] // 1000
    (out / 'reboot_config.hpp').write_text('\n'.join([
        '// GENERATED by tb/verilator/ctrl_reboot/run.py; DO NOT EDIT.', '#pragma once', '#include <cstdint>',
        '#include <string>',
        f'constexpr std::uint64_t sys_hz = {spec["sys_hz"]}ULL;',
        f'constexpr std::uint64_t cpu_hz = {spec["cpu_hz"]}ULL;',
        f'constexpr std::uint32_t csr_size = {spec["csr_size"]}u;',
        f'constexpr std::uint64_t sim_limit_ps = {SIM_LIMIT_S}ULL * 1000000000000ULL;',
        f'constexpr std::uint32_t journal_offset = 0x{journal["offset"]:x}u;',
        f'constexpr std::uint32_t journal_size = 0x{journal["size"]:x}u;',
        f'constexpr std::uint64_t erase_cycles = {int(ERASE_MS * cyc)}ULL;',
        f'constexpr std::uint64_t program_cycles = {int(PROGRAM_MS * cyc)}ULL;',
        f'constexpr unsigned drain_ms = {DRAIN_MS}u, drain_cap_ms = {DRAIN_CAP_MS}u;',
        f'constexpr unsigned egress_ms = {EGRESS_MS}u, hold_window_ms = {HOLD_WINDOW_MS}u;',
        'inline const std::string ready_line = "Milan split control firmware: ready\\r\\n";', '']))
    flags = f'-O3 -std=c++17 -Wall -Wextra -I{ROOT}/tb/common -I{out} -I{SIBLING} -I{ROOT}/sw/firmware/ctrl/mbx'
    boot.run(['verilator', '--cc', '--exe', '-Wno-fatal', '-Werror-USERERROR', '-Wno-BLKANDNBLK', '-Wno-WIDTH',
              '-Wno-COMBDLY', '-Wno-CASEINCOMPLETE', '--top-module', 'sim', '--Mdir', str(native), '-O3',
              '--output-split', '5000', '--output-split-cfuncs', '500', '-CFLAGS', flags,
              *['-I' + str(i) for i in spec['includes']], *spec['sources'], str(HERE / 'sim_main.cpp')],
             out / 'verilate.log', cwd=out / 'soc/gateware')
    boot.run(['make', f'-j{JOBS}', '-C', str(native), '-f', 'Vsim.mk', 'Vsim'], out / 'make.log')
    return native / 'Vsim'


def common(out: Path) -> tuple[Path, tuple[Path, Path], Path]:
    """What every image shares: the flash map, the runtime archives and the test SoC's csr.csv, from an export
    with the checkout's image against the fixture map (the map does not depend on the image)."""
    import build as budget_build
    flash_map = budget_build.flash_map(out / 'split-soc/flash-map', SHAPE)
    archives = boot.runtime(out)
    first = boot.image(out, 'image-provisional', POINT, boot.ImageMaps(boot.PROVISIONAL, flash_map), archives)
    exported(out, 'soc-provisional', first, flash_map)
    return flash_map, archives, out / 'soc-provisional/csr.csv'


def build(out: Path, shared: tuple[Path, tuple[Path, Path], Path], source: Path | None = None) -> tuple[Path, dict]:
    """One image (the checkout's, or a planted tree's), its export and its model."""
    flash_map, archives, csr_csv = shared
    out.mkdir(parents=True, exist_ok=True)
    elf = boot.image(out, 'image', POINT, boot.ImageMaps(csr_csv, flash_map), archives, source)
    spec = exported(out, 'soc', elf, flash_map)
    if boot.rows(out / 'soc/csr.csv') != boot.rows(csr_csv):
        raise RuntimeError("the SoC's csr.csv depends on the image; the image's map cannot be generated from it")
    spec['elf'] = str(elf)
    return verilate(out, spec, flash_map), spec


def run(exe: Path, where: Path, name: str, script: Script, journal_in: Path | None) -> Path:
    """One run of the model; its log, beside its script, transcript, exit status and journal."""
    where.mkdir(parents=True, exist_ok=True)
    (where / f'{name}.script').write_text(script.text())
    (where / f'{name}.tags.json').write_text(json.dumps(script.tags))
    env = {**os.environ, 'REBOOT_JOURNAL_OUT': str(where / f'{name}.journal')}
    if journal_in is not None:
        env['REBOOT_JOURNAL_IN'] = str(journal_in)
    else:
        env.pop('REBOOT_JOURNAL_IN', None)
    log = where / f'{name}.log'
    with log.open('w') as sink:
        result = subprocess.run([str(exe), str(where / f'{name}.script'), str(where / f'{name}.transcript')],
                                stdout=sink, stderr=subprocess.STDOUT, check=False, cwd=exe.parents[1] / 'soc/gateware',
                                env=env)
    (where / f'{name}.{STATUS}').write_text(f'{result.returncode}\n')
    return log


# ---- reading a log -----------------------------------------------------------------------------------------

@dataclass
class Frame:
    """A frame the mailbox sent: its last byte's cycle, channel and bytes."""
    cycle: int
    channel: int
    data: bytes


@dataclass
class Log:
    """One run's observations."""
    text: str
    tags: dict[int, str]
    status: int | None
    tx: list[Frame]
    rx_end: dict[str, int]
    events: dict[str, list[list[str]]]

    def first(self, tag: str) -> list[str] | None:
        """The first line of one kind, without its tag; None when the log holds none."""
        rows = self.events.get(tag, [])
        return rows[0] if rows else None


def parse(log: Path, tags: dict[int, str] | None = None, text: str | None = None) -> Log:
    """A run's log, its tags and its saved exit status."""
    text = log.read_text() if text is None else text
    if tags is None:
        tags = {int(k): v for k, v in json.loads(log.with_suffix('.tags.json').read_text()).items()}
    status_file = log.parent / log.name.replace('.log', f'.{STATUS}')
    status = int(status_file.read_text()) if status_file.exists() else None
    tx, rx_end, events = [], {}, {}
    for line in text.splitlines():
        words = line.split()
        if not words:
            continue
        if words[0] == 'TX':
            tx.append(Frame(int(words[1]), int(words[3]), bytes.fromhex(words[4])))
        elif words[0] == 'RXE':
            rx_end.setdefault(words[2], int(words[1]))
        elif words[0] in ('READY', 'REQ', 'DRAIN', 'EGRESS', 'HOLD', 'RELOAD', 'CUT', 'NOREQ', 'NOADP', 'FLASH',
                          'NVM', 'SUMMARY', 'STEP'):
            events.setdefault(words[0], []).append(words[1:])
    return Log(text, tags, status, tx, rx_end, events)


@dataclass(frozen=True)
class Answer:
    """A response the mailbox sent to a tagged command."""
    cycle: int
    status: int
    cdl: int
    command: int
    payload: bytes


def answers(log: Log) -> dict[str, Answer]:
    """Each tagged command's response: an AEM_RESPONSE (9.2.1.1, u clear) or an ACMP response (8.2.1), by its
    sequence_id."""
    out: dict[str, Answer] = {}
    for f in log.tx:
        d = f.data
        if len(d) < 38 or d[12:14] != b'\x22\xf0':
            continue
        if f.channel == CH_AECP and d[14] == 0xFB and d[15] & 0x0F == 1 and not d[36] & 0x80:
            tag = log.tags.get(int.from_bytes(d[34:36], 'big'))
            if tag and int.from_bytes(d[26:34], 'big') in (CTL1[0], CTL2[0]):
                out.setdefault(tag, Answer(f.cycle, d[16] >> 3, ((d[16] & 7) << 8) | d[17],
                                           int.from_bytes(d[36:38], 'big'), d[38:]))
        elif f.channel == CH_ACMP and d[14] == 0xFC and d[15] & 0x0F in (7, 11) and len(d) >= 70:
            tag = log.tags.get(int.from_bytes(d[62:64], 'big'))
            if tag:
                out.setdefault(tag, Answer(f.cycle, d[16] >> 3, ((d[16] & 7) << 8) | d[17], d[15] & 0x0F, d[18:70]))
    return out


def notifications(log: Log, command: int) -> list[Frame]:
    """The unsolicited AEM responses of a command_type (u set; 7.5.2)."""
    return [f for f in log.tx if f.channel == CH_AECP and len(f.data) >= 38 and f.data[14] == 0xFB
            and int.from_bytes(f.data[36:38], 'big') == 0x8000 | command]


def adp(log: Log, message: int) -> list[Frame]:
    """The ADPDUs of one message_type the entity sent (IEEE 1722.1-2021 6.2.1)."""
    return [f for f in log.tx if f.channel == CH_ADP and len(f.data) > 15 and f.data[15] & 0x0F == message]


def value(item: str, got: dict[str, Answer], prefix: str) -> object:
    """An item's value as its read answered it, None when unanswered or refused."""
    def one(tag: str) -> Answer | None:
        """A tagged read's answer when it was SUCCESS."""
        a = got.get(tag)
        return a if a is not None and a.status == SUCCESS else None
    if item == 'entity_names':
        names = [one(f'{prefix}-{item}-{k}') for k in (0, 1)]
        return None if None in names else tuple(a.payload[8:72].rstrip(b'\0').decode(errors='replace') for a in names)
    a = one(f'{prefix}-{item}')
    if a is None:
        return None
    p = a.payload
    return {'configuration': lambda: int.from_bytes(p[2:4], 'big'),
            'sampling_rate': lambda: int.from_bytes(p[4:8], 'big'),
            'stream_format': lambda: p[4:12].hex(),
            'presentation_time_offset': lambda: int.from_bytes(p[24:28], 'big'),
            'channel_mappings': lambda: p[12:12 + 8 * int.from_bytes(p[8:10], 'big')].hex(),
            'clock_source': lambda: int.from_bytes(p[4:6], 'big'),
            'object_names': lambda: p[8:72].rstrip(b'\0').decode(errors='replace'),
            # GET_RX_STATE_RESPONSE: talker_entity_id and talker_unique_id (8.2.1)
            'stream_binding': lambda: (hex(int.from_bytes(p[16:24], 'big')), int.from_bytes(p[32:34], 'big'))}[item]()


def snapshot(got: dict[str, Answer], prefix: str) -> dict[str, object]:
    """Every item's value as one round of reads (its tag prefix) answered it."""
    return {item: value(item, got, prefix) for item in READS}


# ---- the grades --------------------------------------------------------------------------------------------

def ms(cycles: int, spec: dict) -> float:
    """Bus cycles as milliseconds."""
    return cycles * 1000 / spec['sys_hz']


def grade_reboot(log: Log, spec: dict, full: bool = True) -> tuple[list[str], list[str]]:
    """REFUSE, ORDER, JOURNAL (its first half) and BOUND on the reboot run."""
    findings, report = [], []
    got = answers(log)
    req, hold = log.first('REQ'), log.first('HOLD')
    reboot_at = log.rx_end.get('reboot')
    # REFUSE: 7.4.43's routes; the processor's order (protocol-processor 06_aecp_engine.md 6.11)
    for tag, _, status in REFUSALS:
        a = got.get(tag)
        if a is None:
            findings.append(f'REFUSE: {tag} was not answered')
            continue
        if a.status != status or a.cdl != 16:
            findings.append(f'REFUSE: {tag} answered status {a.status} at cdl {a.cdl}, not {status} at cdl 16')
        if req and int(req[0]) < a.cycle:
            findings.append(f'REFUSE: the reset port fired before {tag} was answered')
    if got.get('in-service') is None or got['in-service'].status != SUCCESS:
        findings.append('REFUSE: after the refusals the entity no longer answers')
    early = [f for f in notifications(log, REBOOT) if reboot_at is None or f.cycle < reboot_at]
    if early:
        findings.append(f'REFUSE: a refused REBOOT notified {len(early)} controller(s)')
    if req and (reboot_at is None or int(req[0]) < reboot_at):
        findings.append('REFUSE: the reset port fired before the REBOOT of the ENTITY')
    # ORDER
    ok = got.get('reboot')
    if ok is None or ok.status != SUCCESS or ok.payload[:4] != target(ENTITY, 0):
        findings.append(f'ORDER: the REBOOT of the ENTITY was not answered SUCCESS with its target '
                        f'({None if ok is None else (ok.status, ok.payload[:4].hex())})')
    note = [f for f in notifications(log, REBOOT) if reboot_at is not None and f.cycle > reboot_at]
    departing = [f for f in adp(log, frames.ADP_DEPARTING) if reboot_at is not None and f.cycle > reboot_at]
    if req is None:
        findings.append('ORDER: the reset port never fired' + (' (NOREQ)' if log.first('NOREQ') else ''))
    else:
        at = int(req[0])
        if ok is not None and ok.cycle >= at:
            findings.append('ORDER: the REBOOT\'s SUCCESS left the mailbox after the reset port fired')
        if len(note) != 1 or note[0].cycle >= at:
            findings.append(f'ORDER: the REBOOT notified the other registered controller '
                            f'{len(note)} time(s) before the reset port fired, not once')
        if not departing or departing[0].cycle >= at or (note and departing[0].cycle < note[0].cycle):
            findings.append('ORDER: ENTITY_DEPARTING did not leave between the notification and the reset port')
        report.append(f'ORDER REBOOT received at cycle {reboot_at}; SUCCESS at {ok.cycle if ok else None}; '
                      f'notification at {note[0].cycle if note else None}; ENTITY_DEPARTING at '
                      f'{departing[0].cycle if departing else None}; the reset port at {at}')
    if 'after-success' in got:
        findings.append('ORDER: a command after the REBOOT\'s SUCCESS was answered')
    if 'after-port' in got or 'after-port-bind' in got:
        findings.append('ORDER: a frame given after the reset port fired was taken')
    # BOUND
    if req and reboot_at is not None:
        cycles = int(req[0]) - reboot_at
        report.append(f'BOUND the REBOOT command\'s last byte to the reset port: {cycles} bus cycles, '
                      f'{cycles * spec["cpu_hz"] // spec["sys_hz"]} CPU cycles, {ms(cycles, spec):.3f} ms')
        if hold:
            report.append(f'BOUND the reset port to the PHY hold: {ms(int(hold[0]) - int(req[0]), spec):.3f} ms '
                          f'(drain {log.first("DRAIN")[1]}, egress {log.first("EGRESS")[1]}); then the RTL\'s '
                          f'{HOLD_MS} ms hold, 3 ms and 8 clocks to the IPROG word')
    # JOURNAL, the first half
    if full:
        erases = [int(r[0]) for r in log.events.get('FLASH', []) if r[1] == 'd8']
        programs = [int(r[0]) for r in log.events.get('FLASH', []) if r[1] == '02']
        drain = log.first('DRAIN')
        if not erases or reboot_at is None or erases[0] > reboot_at or not any(p > reboot_at for p in programs):
            findings.append('JOURNAL: the REBOOT did not come inside the journal write that saves the items')
        if drain is None or drain[1] != 'durable':
            findings.append(f'JOURNAL: the drain ended {drain[1] if drain else "never"}, not because the state was '
                            'durable: the write in progress did not complete')
        report.append(f'JOURNAL the write\'s erase at {erases[0] if erases else None}, the REBOOT at {reboot_at}, '
                      f'{sum(p > (reboot_at or 0) for p in programs)} page program(s) after it; the drain '
                      f'{drain[1] if drain else None}')
    return findings, report


def grade_after(reboot: Log, after: Log, spec: dict) -> tuple[list[str], list[str]]:
    """RESTORE, JOURNAL (its second half) and ADP on the boot after the reset."""
    findings, report = [], []
    first, after_got = answers(reboot), answers(after)
    defaults, pre, post = snapshot(first, 'default'), snapshot(first, 'pre'), snapshot(after_got, 'post')
    graded = tuple(i for i in READS if i not in UNSETTABLE)
    verdict, detail = torture_campaign.check_release_state_restored(pre, post, defaults, items=graded,
                                                                    phase='soft_reset')
    report.append(f'RESTORE {verdict} over {", ".join(graded)}: {detail}')
    if verdict != 'PASS':
        findings.append(f'RESTORE: the #396 grader says {verdict}: {detail}')
    for item, why in UNSETTABLE.items():
        if pre[item] is None or post[item] != pre[item]:
            findings.append(f'RESTORE: {item} reads {post[item]!r} after the reset, {pre[item]!r} before')
        report.append(f'RESTORE {item} NOT RUN: {why}; it reads {post[item]!r} before and after')
    if verdict != 'PASS' and any(post[i] != pre[i] for i in graded):
        findings.append('JOURNAL: the write in progress at the REBOOT did not complete: an item reverted')
    hold, ready = reboot.first('HOLD'), after.first('READY')
    available = adp(after, frames.ADP_AVAILABLE)
    reboot_at = reboot.rx_end.get('reboot')
    if not available or hold is None or reboot_at is None:
        findings.append('ADP: no ENTITY_AVAILABLE after the reset')
    else:
        before = ms(int(hold[0]) - reboot_at, spec)
        boot_ms = ms(available[0].cycle, spec)
        total = before + HOLD_MS + 3 + boot_ms
        ready_ms = ms(int(ready[0]), spec) if ready else None
        report.append(f'ADP the REBOOT to the PHY hold {before:.3f} ms, the hold {HOLD_MS} ms and the IPROG word '
                      f'3 ms, the reset to ready {ready_ms} ms and to the first ENTITY_AVAILABLE '
                      f'{boot_ms:.3f} ms: {total:.3f} ms of {VALID_TIME_MS} ms, {VALID_TIME_MS - total:.3f} ms left '
                      'for the configuration load, which the simulation does not model')
        if total >= VALID_TIME_MS:
            findings.append(f'ADP: {total:.3f} ms from the REBOOT to the first ENTITY_AVAILABLE, past the valid time')
    return findings, report


def grade_cut(reboot: Log, replay: Log) -> tuple[list[str], list[str]]:
    """JOURNAL's cut: the replay reads one whole snapshot, the saved one or the cut write's, never a mix."""
    got = answers(replay)
    first = snapshot(answers(reboot), 'pre')
    entity = got.get('replay-entity-name')
    obj = got.get('replay-object-name')
    read = tuple(None if a is None or a.status != SUCCESS else a.payload[8:72].rstrip(b'\0').decode(errors='replace')
                 for a in (entity, obj))
    saved = (first['entity_names'][0] if first['entity_names'] else None, first['object_names'])
    cut = ('cut entity', 'cut input')
    report = [f'JOURNAL the cut\'s replay reads {read}; the saved snapshot {saved}, the cut write\'s {cut}']
    if read not in (saved, cut):
        return [f'JOURNAL: the cut\'s replay reads {read}, neither the saved snapshot {saved} nor the cut write {cut}: '
                'a write half applied'], report
    return [], report


def native(log: Log) -> list[str]:
    """The model's own verdict (the split boot simulation's reader)."""
    return boot.native(log.text, log.status)[0]


# ---- the plants and the grader controls --------------------------------------------------------------------

@dataclass(frozen=True)
class Plant:
    """A planted image: a firmware edit, the reboot run it is driven by, and the grade that must find it."""
    path: str
    old: str
    new: str
    full: bool
    kind: str


PLANTS = {
    # item 2: the reset port fired at the REBOOT's acceptance, before its frames leave
    'reset-before-the-response': Plant(
        'plat/ctrl_plat.c', '\t\tif (!aecp_reboot_due(&p->aecp.core)) {\n',
        '\t\tif (p->aecp.core.reboot != 0u) {\n\t\t\tctrl_plat_io_write32(p->env->reboot, 1u);\n\t\t}\n'
        '\t\tif (!aecp_reboot_due(&p->aecp.core)) {\n', False, 'ORDER'),
    # item 3: the request answered and never fired
    'request-ignored': Plant('plat/ctrl_plat.c', '\tctrl_plat_io_write32(p->env->reboot, 1u);\n', '', False,
                             'ORDER'),
    # item 4: the store stopped at the reset port, which tears the write in progress
    'write-torn': Plant('plat/ctrl_plat.c', '\t\tnvm_store_service();\n', '', True, 'JOURNAL'),
    # item 5: a REBOOT of another descriptor type accepted
    'any-descriptor-type': Plant(
        'aecp/aecp_commands.c',
        '\tif (wire_be16(in) != 0u) {\n\t\treturn AECP_NOT_SUPPORTED;\n\t}\n\tif (wire_be16(in + 2) != 0u) {\n',
        '\tif (wire_be16(in + 2) != 0u) {\n', False, 'REFUSE'),
}


def planted(out: Path, plant: Plant) -> Path:
    """A copy of the firmware's tree with the plant written into it."""
    copy = out / 'ctrl'
    shutil.rmtree(copy, ignore_errors=True)
    shutil.copytree(ROOT / 'sw/firmware/ctrl', copy, ignore=shutil.ignore_patterns('__pycache__'))
    text = (copy / plant.path).read_text()
    if text.count(plant.old) != 1:
        raise RuntimeError(f'a plant\'s anchor occurs {text.count(plant.old)} times in {plant.path}')
    (copy / plant.path).write_text(text.replace(plant.old, plant.new))
    return copy


def _early_port(text: str) -> str:
    """The reset port's rise moved to the cycle after the REBOOT's last byte, before its SUCCESS leaves."""
    arrived = int(re.search(r'^RXE (\d+) reboot$', text, flags=re.M)[1])
    return re.sub(r'^REQ \d+$', f'REQ {arrived + 1}', text, flags=re.M)


#: Grader controls: (the run they edit, the edit, the grade that must find it)
CONTROLS: dict[str, tuple[str, Callable[[str], str], str]] = {
    'response-after-the-port': ('reboot', _early_port, 'ORDER'),
    'drain-at-its-cap': ('reboot', lambda t: re.sub(r'^DRAIN (\d+) durable$', r'DRAIN \1 cap', t, flags=re.M),
                         'JOURNAL'),
    'no-advertisement': ('after', lambda t: '\n'.join(ln for ln in t.splitlines()
                                                      if not re.match(r'TX \d+ \d+ 0 ', ln)) + '\n', 'ADP'),
    'name-reverted': ('after', lambda t: t.replace('after the reboot'.encode().hex(),
                                                   'Milan FPGA 1x1 TDM8'.encode().hex().ljust(32, '0')[:32]),
                      'RESTORE'),
    'binding-lost': ('after', lambda t: t.replace(f'{TALKER:016x}', f'{0:016x}'), 'RESTORE'),
}


# ---- the points ---------------------------------------------------------------------------------------------

def clean(out: Path, shared: tuple, jobs: int) -> tuple[list[str], list[str], dict[str, Log], dict]:
    """The checkout's image: the four runs and their grades."""
    exe, spec = build(out / 'clean', shared)
    entity = entity_of(out / 'clean/image')
    runs = out / 'clean/runs'
    reboot_log = run(exe, runs, 'reboot', reboot_script(entity), None)
    with ThreadPoolExecutor(max_workers=min(jobs, 2)) as pool:
        after_f = pool.submit(run, exe, runs, 'after', after_script(entity), runs / 'reboot.journal')
        cut_f = pool.submit(run, exe, runs, 'cut', cut_script(entity), runs / 'reboot.journal')
        after_log, cut_log = after_f.result(), cut_f.result()
    replay_log = run(exe, runs, 'replay', replay_script(entity), runs / 'cut.journal')
    logs = {n: parse(p) for n, p in (('reboot', reboot_log), ('after', after_log), ('cut', cut_log),
                                     ('replay', replay_log))}
    findings, report = [], []
    for name, log in logs.items():
        findings += [f'{f} ({name})' for f in native(log)]
    for f, r in (grade_reboot(logs['reboot'], spec), grade_after(logs['reboot'], logs['after'], spec),
                 grade_cut(logs['reboot'], logs['replay'])):
        findings += f
        report += r
    return findings, report, logs, spec


def plant_point(out: Path, shared: tuple, name: str, plant: Plant) -> tuple[bool, str]:
    """One planted image, its reboot run and its grade: caught when the grade it names finds it."""
    where = out / f'plant-{name}'
    exe, spec = build(where, shared, planted(where, plant))
    log = parse(run(exe, where / 'runs', 'reboot', reboot_script(entity_of(where / 'image'), plant.full), None))
    findings, _ = grade_reboot(log, spec, plant.full)
    caught = any(f.startswith(plant.kind + ':') for f in findings)
    return caught, f'PLANT {name}: {"caught" if caught else "ESCAPED"} ({plant.kind}); findings: {findings}'


def control(logs: dict[str, Log], spec: dict, name: str) -> tuple[bool, str]:
    """One grader control on the clean logs: caught when its grade finds it."""
    which, edit, kind = CONTROLS[name]
    edited = dict(logs)
    edited[which] = parse(Path(f'{which}.log'), logs[which].tags, edit(logs[which].text))
    edited[which].status = logs[which].status
    findings = grade_reboot(edited['reboot'], spec)[0] + grade_after(edited['reboot'], edited['after'], spec)[0]
    caught = any(f.startswith(kind + ':') for f in findings)
    return caught, f'CONTROL {name}: {"caught" if caught else "ESCAPED"} ({kind}); findings: {findings}'


def main() -> int:
    """Build, run and grade the checkout's image; with --self-test, every plant and control too."""
    parser = argparse.ArgumentParser(description=__doc__.split('\n', 1)[0])
    parser.add_argument('--build-dir', type=Path, required=True)
    parser.add_argument('--self-test', action='store_true',
                        help='also build and run every planted image (PLANTS) and plant every grader control '
                             '(CONTROLS)')
    parser.add_argument('--jobs', type=int, default=JOBS, help='runs and builds at once')
    args = parser.parse_args()
    out = args.build_dir.resolve()
    try:
        out.mkdir(parents=True, exist_ok=True)
        shared = common(out)
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            done = pool.submit(clean, out, shared, args.jobs)
            planted_runs = ({name: pool.submit(plant_point, out, shared, name, p) for name, p in PLANTS.items()}
                            if args.self_test else {})
            findings, report, logs, spec = done.result()
            plants = {name: f.result() for name, f in planted_runs.items()}
    except (RuntimeError, OSError, ValueError, KeyError) as error:
        print(f'REFUSED: {error}')
        return 2
    print('\n'.join(report))
    for finding in findings:
        print(f'FINDING: {finding}')
    wrong = 0
    if args.self_test:
        for caught, line in plants.values():
            wrong += not caught
            print(line)
        for name in CONTROLS:
            caught, line = control(logs, spec, name)
            wrong += not caught
            print(line)
        print(f'ctrl_reboot self-test: {len(PLANTS) + len(CONTROLS) - wrong} of {len(PLANTS) + len(CONTROLS)} '
              'plants and controls caught')
    print(f'ctrl_reboot: {"FAIL" if findings or wrong else "PASS"} ({len(findings)} finding(s))')
    return 1 if findings or wrong else 0


if __name__ == '__main__':
    raise SystemExit(main())
