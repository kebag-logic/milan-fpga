# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The saved-state store's cases on the split CPU (#665): each boot's image, journal and script.

Every case boots the split image on the service-budget harness's test SoC
(tb/verilator/ctrl_service_budget), whose flash port runs on the split SoC's
own LiteSPI map. A case names the image it boots (an ARM: the fixture as
linked, or a labelled test-code edit of it; a PLANT: a planted defect in the
saved-state store's tree), the journal the flash holds when it boots, and the
stimulus it runs.

The journals are built from the one the target wrote itself. The `commit`
case boots blank flash with every record of the shape marked changed, renames
the entity and binds sink 0 through AECP and ACMP, and lets the store commit:
the capture it measures latches the whole container from its owners. Its
journal is then the `valid` case's, and the reference codec
(scripts/nvm_klj2.py) derives the `torn` journal (a newer container renaming
the entity, its last page never programmed, beside the committed one) and the
`version` one (the committed container under another major version, the other
slot blank).
"""
from __future__ import annotations

import struct
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BUDGET = ROOT / 'tb/verilator/ctrl_service_budget'
for path in (BUDGET, ROOT / 'scripts', ROOT / 'sw/firmware/ctrl_nvm/test'):
    sys.path.insert(0, str(path))

import build  # noqa: E402  the service-budget harness's build, read only
import frames as f  # noqa: E402
import scenario  # noqa: E402
from nvm_contract import KLJ2_FMT_VER, Key  # noqa: E402
from nvm_klj2 import erased_record, frame_record, rid_of_key  # noqa: E402

MS = scenario.MS
SAVED_NAME = b'saved by the target'.ljust(64, b'\0')
NEWER_NAME = b'newer, torn'.ljust(64, b'\0')
#: The sequence_ids of the AECP and ACMP commands the cases send.
SEQ = dict(set_name=0x5401, read_entity=0x5402, bind=0x5403, rx_state=0x5404)
#: One page of the flash (nvm_shape.h NVM_FLASH_PAGE): a torn container's last page is never programmed.
PAGE = 256

#: Every record of the shape marked changed once the boot has released, so the store's first
#: capture latches the whole container from its owners.
CAPTURE_ALL = build.Variant('nvm-capture-all', ((
    '    nvm_store_boot(&nvm_flash_litespi,&image_binding.port);\n',
    '    nvm_store_boot(&nvm_flash_litespi,&image_binding.port);\n'
    '    // Every record changed: the first capture latches the whole container (#665).\n'
    '    for (struct nvm_rec r = nvm_rec_first(); r.ok; r = nvm_rec_next(r))\n'
    '        nvm_store_changed(r.group, r.index);\n'),))
#: After the boot, the port is asked to program and erase outside the journal and to erase one
#: block inside it; unless it refuses every outside call and takes the inside one, main returns
#: and the hart parks before the mailbox opens (#665, the flash region guard).
GUARD_PROBE = build.Variant('nvm-guard-probe', ((
    '    nvm_store_boot(&nvm_flash_litespi,&image_binding.port);\n',
    '    nvm_store_boot(&nvm_flash_litespi,&image_binding.port);\n'
    '    {\n'
    '        // The guard: every program and erase outside the journal refused, one inside taken (#665).\n'
    '        static const uint8_t page[NVM_FLASH_PAGE];\n'
    '        const struct nvm_flash *p = &nvm_flash_litespi;\n'
    '        const uint32_t j = MILAN_FLASH_JOURNAL_OFFSET, end = j + MILAN_FLASH_JOURNAL_SIZE;\n'
    '        if (!p->erase(p->ctx, 0u) || !p->erase(p->ctx, j - 1u) || !p->erase(p->ctx, end) ||\n'
    '            !p->erase(p->ctx, end + MILAN_FLASH_JOURNAL_SIZE) ||\n'
    '            !p->program(p->ctx, j - NVM_FLASH_PAGE, page, NVM_FLASH_PAGE) ||\n'
    '            !p->program(p->ctx, end, page, 1u) || !p->program(p->ctx, 0u, page, 1u) ||\n'
    '            p->erase(p->ctx, j)) return 9;\n'
    '        while (p->busy(p->ctx) > 0) {\n'
    '        }\n'
    '    }\n'),))
#: The probe's calls into the port, outside the journal and inside it.
GUARD_CALLS = dict(erase_outside=4, program_outside=3, erase_inside=1)
#: The arms a case boots, by name: the fixture as linked, or a labelled edit of it.
ARMS = {'fixture': 'none', 'capture-all': CAPTURE_ALL, 'guard-probe': GUARD_PROBE}

#: Planted defects in the saved-state store's tree, each a scratch copy (build.Plant).
PLANTS = {
    # The D3 walk settles after the names: the settle step's own test is removed, so the walk's
    # closing settle runs once the names are applied.
    'settle-after-names': build.Plant(
        'settle-after-names', 'ctrl_nvm/nvm_store.c', '\t\tif (r.group == NVM_G_NAME && !settled) {\n',
        '\t\tif (0 && r.group == NVM_G_NAME && !settled) {\n'),
    # The binding walk runs after the D3 walk instead of before it.
    'bindings-after-d3': build.Plant(
        'bindings-after-d3', 'ctrl_nvm/nvm_store.c',
        '\t\tnvm.st.bind_terminal = nvm_walk_bind();\n\t}\n\tif (nvm.st.bind_terminal == NVM_T_CLOSED) {\n'
        '\t\tnvm.st.terminal = NVM_T_CLOSED;\n\t\treturn;\n\t}\n'
        '\t/* blank media too: nothing is released over an unproven model */\n'
        '\tif (nvm_model_proven() && chosen != NVM_NONE)\n\t\tnvm.st.terminal = nvm_walk_d3();\n',
        '\t\tnvm.st.bind_terminal = NVM_T_COMPLETE;\n\t}\n'
        '\tif (nvm_model_proven() && chosen != NVM_NONE) {\n\t\tnvm.st.terminal = nvm_walk_d3();\n'
        '\t\tnvm.st.bind_terminal = nvm_walk_bind();\n\t}\n'),
    # The port's guard passes every address.
    'guard-removed': build.Plant(
        'guard-removed', 'ctrl_nvm/plat/nvm_flash_litespi.c',
        '\treturn addr >= MILAN_FLASH_JOURNAL_OFFSET &&\n'
        '\t       len <= MILAN_FLASH_JOURNAL_SIZE &&\n'
        '\t       addr - MILAN_FLASH_JOURNAL_OFFSET <= MILAN_FLASH_JOURNAL_SIZE - len;\n',
        '\t(void)addr;\n\t(void)len;\n\treturn 1;\n'),
}


@dataclass(frozen=True)
class Case:
    """One boot: its name, the arm and plant its image is built with, its journal, and what it asks.

    journal: 'blank' (erased flash), or 'saved', 'torn' or 'version', built from the commit
    case's journal (journals()). commit: the case lets a capture of every record commit.
    control: the case is a planted defect that must be caught, with the words its grade needs.
    """
    name: str
    arm: str
    plant: str
    journal: str
    commit: bool = False
    control: str = ''


CASES = (
    Case('commit', 'capture-all', 'none', 'blank', commit=True),
    Case('valid', 'fixture', 'none', 'saved'),
    Case('absent', 'fixture', 'none', 'blank'),
    Case('torn', 'fixture', 'none', 'torn'),
    Case('version', 'fixture', 'none', 'version'),
    Case('guard', 'guard-probe', 'none', 'blank'),
    Case('reorder-settle', 'fixture', 'settle-after-names', 'saved', control='apply order'),
    Case('reorder-bindings', 'fixture', 'bindings-after-d3', 'saved', control='apply order'),
    Case('guard-removed', 'guard-probe', 'guard-removed', 'blank', control='flash write escaped the journal'),
)


def build_key(case: Case) -> str:
    """The build directory a case's image is in: its arm, and its plant when it has one."""
    return case.arm if case.plant == 'none' else f'{case.arm}+{case.plant}'


def commit_ms(point: scenario.Point, records: int, pages: int) -> int:
    """The simulated time a capture of every record and its commit take after the boot, with room.

    The store waits 1,000 ms after the first change (DR2a), then takes one step a 10 ms tick: a
    capture step per record and one to seal, a CRC step per page, the erase and its poll, a blank
    check, a program and its poll per page and a verify per page."""
    steps = records + 1 + pages + 2 + pages + 2 * pages + pages
    return 1000 + 10 * steps + 500 + 100 * point.interfaces


def ready(steps: list[str], point: scenario.Point) -> None:
    """Boot to the open mailbox and raise every link, as the budget's groups do (scenario.ready)."""
    steps += ['wait ready within 300000000', 'mark booted', f'wait cycles {50 * MS}',
              'wait quiet 3 within 2000000', *[f'link {i} 1' for i in range(point.interfaces)],
              f'wait cycles {300 * MS}', 'mark settled']


def questions(point: scenario.Point) -> list[str]:
    """READ_DESCRIPTOR of the ENTITY (its entity_name) and GET_RX_STATE of sink 0 (its binding)."""
    aecp, acmp = scenario.CH['aecp'], scenario.CH['acmp']
    read = f.read_descriptor(f.Aem(point.entity_id, scenario.CTL1, scenario.CTL_MAC, point.mac,
                                   SEQ['read_entity']), 0, 0)
    state = scenario.acmp_cmd(point, 'GET_RX_STATE', 0, SEQ['rx_state'])
    return [f'frame 0 {read.hex()} ask.entity', f'wait tx {aecp} 1 within {50 * MS}',
            f'frame 0 {state.hex()} ask.rx_state', f'wait tx {acmp} 1 within {50 * MS}']


def script(case: Case, point: scenario.Point, records: int, pages: int) -> str:
    """The stimulus a case runs: boot, then for the commit its changes and the commit's wait, then the
    two questions."""
    steps: list[str] = []
    if case.control == 'flash write escaped the journal':
        # The planted guard sends the probe's first erase to the device, which refuses it.
        steps += ['wait ready within 300000000']
        return '\n'.join([*steps, 'end']) + '\n'
    ready(steps, point)
    if case.commit:
        aecp, acmp = scenario.CH['aecp'], scenario.CH['acmp']
        rename = f.aem_command(f.Aem(point.entity_id, scenario.CTL2, scenario.CTL_MAC, point.mac, SEQ['set_name']),
                               0x0010, bytes(8) + SAVED_NAME)
        bind = scenario.acmp_cmd(point, 'BIND_RX', 0, SEQ['bind'])
        steps += [f'frame 0 {rename.hex()} change.name', f'wait tx {aecp} 1 within {50 * MS}',
                  f'frame 0 {bind.hex()} change.bind', f'wait tx {acmp} 1 within {50 * MS}',
                  'mark committing', f'wait cycles {commit_ms(point, records, pages) * MS}', 'mark committed']
    steps += questions(point)
    return '\n'.join([*steps, f'wait cycles {50 * MS}', 'end']) + '\n'


def shape_bench(shape: str, work: Path) -> tuple[object, int, int]:
    """The shape's reference side (nvm_bench.Bench), its record count and its container's length in bytes."""
    import nvm_bench
    bench = nvm_bench.make_bench(nvm_bench.shape_inputs(ROOT / 'configs' / f'{shape}.yaml', work))
    return bench, len(bench.expect), len(bench.assemble(bench.frames, 1))


def payload_lengths(bench: object) -> tuple[int, ...]:
    """Each record's payload length, the shape's records in ascending id: the order a capture walks them."""
    ordered = sorted(bench.expect.items(), key=lambda kv: rid_of_key(kv[0], bench.donor.base))
    return tuple(plen for _key, plen in ordered)


def frames_of(applied: dict[Key, bytes], expect: dict[Key, int], donor: object) -> dict[int, bytes]:
    """Every record of a decoded container framed again by the reference codec: an applied record's
    payload, an erased record's span."""
    return {rid_of_key(key, donor.base): frame_record(rid_of_key(key, donor.base), applied[key], donor.layout)
            if key in applied else erased_record(plen) for key, plen in expect.items()}


def journals(saved: bytes, bench: object, slot: int) -> dict[str, bytes]:
    """The journals the boots read, from the commit case's: 'saved' as written, 'torn' (a newer
    container renaming the entity in the other slot, its last page erased) and 'version' (the
    container under the next major version, the other slot blank). bench is nvm_bench's Bench of the
    shape; slot the bytes of one slot."""
    verdict, applied = bench.decode(saved[:struct.unpack_from('<I', saved, 16)[0]])
    if verdict != 0:
        raise RuntimeError(f'the committed journal does not decode: verdict {verdict}')
    named = [k for k, v in applied.items() if k[0] == 'NAME' and v == SAVED_NAME]
    if len(named) != 1:
        raise RuntimeError(f'the committed journal holds the saved name in {named}, not in one NAME record')
    seq = struct.unpack_from('<I', saved, 8)[0]
    newer = bench.assemble(frames_of({**applied, named[0]: NEWER_NAME}, bench.expect, bench.donor), seq + 1)
    torn = newer[:len(newer) - (len(newer) % PAGE or PAGE)].ljust(len(newer), b'\xff')
    blank = b'\xff' * slot
    container = saved[:slot]
    wrong = bytearray(container)
    struct.pack_into('<I', wrong, 4, KLJ2_FMT_VER + 0x1_0000)
    return {'saved': saved, 'torn': container + torn.ljust(slot, b'\xff'),
            'version': bytes(wrong) + blank, 'blank': blank + blank}
