#!/usr/bin/env python3
"""model_plants.py <checkout> <workdir> <out>: plant one defect at a time in the host mailbox model
(sw/firmware/ctrl/host/mbx_model.c, a copy in <workdir>), build the mailbox suite on the model at two interfaces
as tb/verilator/mbx/Makefile's run-if2 does, run it, and record whether the held-frame checks B7, B8 and B9 fail by
name. The checkout is never written. Plant "none" is the positive control."""
import subprocess
import sys
from pathlib import Path

PLANTS = {
    'none': None,
    # B7: the free space read from RX_HEAD alone, not past the held record
    'model-space-from-the-committed-head': (
        '\tuint32_t used = (uint16_t)(ch->rx_head + ch->rx_held_words - ch->rx_tail);',
        '\tuint32_t used = (uint16_t)(ch->rx_head - ch->rx_tail);', 'B7 '),
    # B8: a frame the filter's rule refuses behind a held one counted in RATE_DROP
    'model-refused-behind-held-counted': (
        '\tif (!rule_passes(m, c, frame, len, interface)) {\n\t\treturn false;',
        '\tif (!rule_passes(m, c, frame, len, interface)) {\n'
        '\t\tif (m->ch[c].tokens == 0u && m->ch[c].rx_held_words != 0u) {\n'
        '\t\t\tm->ch[c].rate_drop = sat16(m->ch[c].rate_drop);\n\t\t\tm->err = true;\n\t\t}\n\t\treturn false;',
        'B8 '),
    # B9: the held record's commit gated on an open channel
    'model-release-gated-on-open': (
        '\t\t\tif (ch->rx_held_words != 0u) {\n\t\t\t\t// the held record takes',
        '\t\t\tif (ch->rx_held_words != 0u && ((m->filter_en >> c) & 1u) != 0u) {\n\t\t\t\t// the held record takes',
        'B9 '),
}


def sh(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def main() -> int:
    root, work, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
    fw = root / 'sw/firmware/ctrl'
    gen = work / 'gen'
    work.mkdir(parents=True, exist_ok=True)
    r = sh(['python3', '-I', '-B', str(root / 'sw/mailbox/gen_mailbox.py'), '--variant-interfaces', '2', '--out',
            str(gen)])
    lines = [f'gen if2 rc={r.returncode}']
    inc = [f'-I{fw}/{d}' for d in ('mbx', 'host', 'port', 'loop', 'adp', 'maap', 'acmp', 'app')]
    inc += [f'-I{root}/third_party/tsn-c-stack/include', f'-I{root}/sw/firmware/ctrl_nvm']
    src = (fw / 'host/mbx_model.c').read_text()
    for name, plant in PLANTS.items():
        text, tag = src, None
        if plant:
            old, new, tag = plant
            if src.count(old) != 1:
                lines.append(f'{name}: anchor found {src.count(old)} times, not planted')
                continue
            text = src.replace(old, new)
        d = work / name
        d.mkdir(exist_ok=True)
        (d / 'mbx_model.c').write_text(text)
        cc = sh(['cc', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror', '-pedantic', f'-I{gen}', f'-I{fw}/host',
                 *inc, '-c', str(d / 'mbx_model.c'), '-o', str(d / 'mbx_model.o')])
        cx = sh(['c++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Werror', f'-I{gen}', f'-I{root}/tb/verilator/mbx',
                 f'-I{fw}/test', *inc, str(root / 'tb/verilator/mbx/model_main.cpp'), str(d / 'mbx_model.o'), '-o',
                 str(d / 'Vmbx_model')]) if cc.returncode == 0 else cc
        if cx.returncode != 0:
            lines.append(f'{name}: build failed: {(cc.stderr + cx.stderr)[-400:]}')
            continue
        run = sh([str(d / 'Vmbx_model')])
        (d / 'run.log').write_text(run.stdout + run.stderr)
        fails = [ln for ln in run.stdout.splitlines() if '[FAIL]' in ln]
        summary = [ln for ln in run.stdout.splitlines() if 'checks:' in ln]
        held = [ln for ln in fails if any(t in ln for t in ('B7 ', 'B8 ', 'B9 '))]
        lines.append(f'{name}: rc={run.returncode} {summary[-1].strip() if summary else "no summary"}; '
                     f'{len(fails)} failed, {len(held)} of them B7/B8/B9')
        for ln in (held if plant else fails)[:6]:
            lines.append('    ' + ln.strip())
        if plant:
            lines.append(f'    caught by its own check ({tag.strip()}): {any(tag in ln for ln in held)}')
    out.write_text('\n'.join(lines) + '\n')
    print('\n'.join(lines))
    return 0


if __name__ == '__main__':
    sys.exit(main())
