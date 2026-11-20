#!/usr/bin/env python3
"""cdc_summary.py DIR: RULING-1118e item 3's check of u_fcdc's storage-to-read-register crossing, from cdc.tcl's
reports in DIR, per routed checkpoint: fcdc-TAG-cdc.txt (report_cdc's summary and every detail row naming u_fcdc,
counted by rule beside u_tcdc's), fcdc-TAG-methodology.txt (report_methodology's summary, the rows naming u_fcdc, and
the clock-group rules' details), and fcdc-summary.txt, one verdict block per image."""
import re
import sys
from collections import Counter
from pathlib import Path

D = Path(sys.argv[1])
TAGS = [('release', "p11's release image (all-fabric), ExtraTimingOpt, the selected route"),
        ('split-1x1', "p11's 1x1/1if split image, ExtraPostPlacementOpt, its best of three"),
        ('split-8x8-1if', "p11's 8x8/1if split image, ExtraPostPlacementOpt, its best of three"),
        ('candidate-release-c8ff391a', "the candidate c8ff391a's release image (before #927, block RAM), "
                                       "ExtraPostPlacementOpt, for comparison")]


def body(path: Path) -> list[str]:
    """The report's lines below its header block (which names the host and the command's paths)."""
    lines = path.read_text(errors='replace').splitlines()
    for i, line in enumerate(lines):
        if line.startswith('| Design State'):
            return lines[i + 2:]
    return lines


def rows(path: Path, needle: str) -> list[str]:
    return [l for l in body(path) if re.match(r'^\s*\d+\s+CDC-\d+', l) and needle in l]


def by_rule(rs: list[str]) -> Counter:
    return Counter(' '.join(r.split()[1:3]) for r in rs)


summary = ['# u_fcdc\'s storage-to-read-register crossing (RULING-1118e item 3), from existing routed checkpoints;',
           '# read only: report_cdc, report_timing and report_exceptions on the path, report_methodology. No route made.', '']
for tag, what in TAGS:
    cells = (D / f'fcdc-{tag}-cells.txt').read_text().rstrip('\n')
    full, summ, meth = D / f'cdc-full-{tag}.rpt', D / f'cdc-summary-{tag}.rpt', D / f'methodology-full-{tag}.rpt'
    f_rows, t_rows = rows(full, 'u_fcdc'), rows(full, 'u_tcdc')
    s_lines = [l for l in body(summ) if l.strip()]
    header = [l for l in body(full) if l.startswith('Row  ID') or l.startswith('---  ')][:2]
    out = [f'# {what}', '# report_cdc -summary:', *s_lines, '',
           f'# report_cdc -details: the {len(f_rows)} row(s) naming u_fcdc (the whole design\'s report, filtered)',
           *header, *f_rows, '',
           '# by rule: u_fcdc ' + (', '.join(f'{k} x{v}' for k, v in sorted(by_rule(f_rows).items())) or 'none')
           + '; u_tcdc (the TDM capture\'s, default branch, unchanged) '
           + (', '.join(f'{k} x{v}' for k, v in sorted(by_rule(t_rows).items())) or 'none')]
    (D / f'fcdc-{tag}-cdc.txt').write_text('\n'.join(out) + '\n')
    m = body(meth)
    m_sum = [l for l in m[:60] if l.startswith('|') or l.startswith('+') or 'Checks found' in l]
    m_fcdc = [l for l in m if 'u_fcdc' in l]
    detail, keep = [], False
    for l in m:
        if re.match(r'^(TIMING-47|TIMING-10)#\d+', l):
            keep = True
        elif re.match(r'^[A-Z]+-\d+#\d+', l):
            keep = False
        if keep:
            detail.append(l)
    (D / f'fcdc-{tag}-methodology.txt').write_text('\n'.join(
        [f'# {what}', '# report_methodology summary:', *m_sum, '',
         f'# lines naming u_fcdc: {len(m_fcdc)}', *m_fcdc, '', '# TIMING-47 and TIMING-10 details:', *detail]) + '\n')
    sm = re.search(r'storage leaf cells: (\d+)', cells)
    pair = [l for l in s_lines if 'milansoc_crg_clkout1' in l and 'audio' in l]
    timing = D / f'fcdc-{tag}-timing.txt'
    tex = sorted(set(re.findall(r'Timing Exception:\s+(.*)', timing.read_text()))) if timing.is_file() else []
    slack = sorted(set(re.findall(r'^Slack[^:]*:\s+(\S+)', timing.read_text(), re.M))) if timing.is_file() else []
    summary += [f'== {tag}: {what}', cells, *(['report_cdc summary, the two clocks: ' + ' / '.join(' '.join(p.split()) for p in pair)] if pair else []),
                f'u_fcdc rows in report_cdc: {dict(sorted(by_rule(f_rows).items())) or "none"}; '
                f'u_tcdc rows: {dict(sorted(by_rule(t_rows).items())) or "none"}',
                f'report_timing storage -> read register: exception {tex or "n/a"}, slack {slack or "n/a"}',
                f'report_methodology lines naming u_fcdc: {len(m_fcdc)}', '']
(D / 'fcdc-summary.txt').write_text('\n'.join(summary) + '\n')
print((D / 'fcdc-summary.txt').read_text())
