#!/usr/bin/env python3
"""Restate ctrl_loop.h's and aecp.h's measured figures from this head's legs (#665, round 16 item 4).

usage: restate_headers.py CHECKOUT FIGURES.json
FIGURES.json keys: heaviest_ms (8x8/2if, any pass), heaviest_cycles, margin_ms and margin_row (the least row
margin, 8x8/2if, with an aged step at its worst placement measured), build_cycles (the heaviest pass that carries an
MRPDU build, 8x8/2if), classes (a list of [class, words, cycles_8x8, cycles_1x1]), notice_8x8 and notice_1x1 (the
retried notice's range, ms), srp_ms (the 8x8 notice groups' longest held SRP record).
"""
import json
import sys
from pathlib import Path

root, figures = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
loop_h = root / 'sw/firmware/ctrl/loop/ctrl_loop.h'
aecp_h = root / 'sw/firmware/ctrl/aecp/aecp.h'


def edit(path: Path, pairs: list[tuple[str, str]]) -> None:
    text = path.read_text()
    for old, new in pairs:
        if text.count(old) != 1:
            raise SystemExit(f'{path.name}: {text.count(old)} sites for {old[:60]!r}')
        text = text.replace(old, new)
    path.write_text(text)


f = figures
edit(loop_h, [
    ('// pass the other slices make (1.99 ms at 8x8/2if), and in a pass that takes',
     f"// pass the other slices make ({f['heaviest_ms']:.2f} ms at 8x8/2if), and in a pass that takes"),
    ('// (srp_mbx.c, transmit), up to 95,258 CPU cycles a build at 8x8/2if. Built in',
     f"// (srp_mbx.c, transmit): a pass that carries one takes up to {f['build_cycles']:,} CPU\n"
     '// cycles at 8x8/2if. Built in'),
    ('// margin 0.10 ms (8x8/2if) against a step of up to 0.97 ms; at three a',
     f"// margin {f['margin_ms']:.2f} ms (8x8/2if, {f['margin_row']}) against a step of up to\n"
     '// 0.97 ms; at three a'),
])
classes = '\n'.join(f'//   * {name}: {words}, {c8:,} cycles at 8x8/2if, {c1:,} at 1x1/1if;'
                    for name, words, c8, c1 in f['classes'])
edit(loop_h, [
    ('//   * the saved-state store: one service step, taken only in a pass that\n'
     '//     took no input and has room for it, or as the whole of a pass once it\n'
     '//     has waited past its age limit (THE STEP, nvm_store.h).\n',
     '//   * the saved-state store: one service step, taken only in a pass that\n'
     '//     took no input and has room for it, or as the whole of a pass once it\n'
     '//     has waited past its age limit (THE STEP, nvm_store.h).\n'
     '// So each kind of pass has its worst case, the heaviest each measured at\n'
     '// this head across every group the CPU budget harness stages, both arms,\n'
     '// with and without the drafts (docs/design/SPLIT_CONTROL_MEMORY.md\n'
     '// section 13), each at least 6,490 cycles, the data layout\'s measured\n'
     '// swing, under THE SHARE:\n' + classes + '\n'),
])
edit(aecp_h, [
    ('// builds no notice at all. GET_COUNTERS keeps its one-second spacing, and the',
     f"// builds no notice at all. Measured from the port's answer under input that\n"
     f"// leaves no pass empty (notice_window.py): {f['notice_1x1']} ms at 1x1/1if,\n"
     f"// {f['notice_8x8']} ms at 8x8/2if. GET_COUNTERS keeps its one-second spacing, and the"),
])
print('restated', loop_h.relative_to(root), aecp_h.relative_to(root))
