"""Summarize the merge-head sweep from raw reports; copies no large artifact.

Per seed: WNS/TNS/WHS/THS at every #395 declared corner, read from the in-build
`kl_timing_grade_reports` signoff reports and cross-checked against the read-only
acceptance reports; Ethernet crossing slack against 8 ns; `report_clock_interaction`
rows for the Ethernet pairs; implementation-log warning census; hook order in the
emitted Tcl; build-gate acceptance; and artifact sizes/hashes.
"""
import csv
import hashlib
import json
from pathlib import Path
import re

out = Path(__file__).resolve().parent
root = Path('$LANES/607-xdc-clock-names')
runs = json.loads((out / 'sweep-results.json').read_text())
pin = 'c951a9ff0cb5851fb159d33e966e5a2a9a188fe3'
CORNERS = [(corner, temp) for temp in (0, 85) for corner in ('Slow', 'Fast')]
summary, artifacts = [], []


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def timing_row(path):
    section = path.read_text().split('| Design Timing Summary', 1)[1]
    line = next(line for line in section.splitlines()
                if re.match(r'^\s*-?\d+\.\d+\s+-?\d+\.\d+\s+\d+', line))
    c = line.split()
    return dict(WNS=float(c[0]), TNS=float(c[1]), WHS=float(c[4]), THS=float(c[5]))


def eth_rows(report, pairs):
    matched, all_eth = [], []
    for line in report.read_text().splitlines():
        words = line.split()
        if len(words) >= 2 and 'eth_clocks0_rx' in words[:2]:
            assert 'unsafe' not in line.lower(), line
            all_eth.append(line.strip())
        if len(words) >= 2 and (words[0], words[1]) in pairs:
            assert 'Max Delay Datapath Only' in line, line
            matched.append(line.strip())
    assert len(matched) == 4, (report, matched)
    return dict(report=str(report), pairs=matched, all_eth_pairs=all_eth)


roms = {}
for line in (root / 'syn/yosys/rom_digests.tsv').read_text().splitlines():
    fields = line.split('\t')
    if len(fields) == 3 and fields[0] == pin:
        roms[fields[1]] = fields[2]
rom_check = {name: dict(expected=roms[name], actual=digest(root / 'configs/generated' / name))
             for name in ('ltn_rom.hex', 'ucode.hex')}
assert all(v['expected'] == v['actual'] for v in rom_check.values()), rom_check

for run in runs:
    assert run['rc'] == run['report_rc'] == 0, run
    directory = Path(run['directory'])
    gateware = directory / 'gateware'
    reports = directory / 'acceptance'
    timing = []
    for corner, temp in CORNERS:
        signoff = timing_row(gateware / f'alinx_ax7101_signoff_{corner}_{temp}C_timing.rpt')
        acceptance = timing_row(reports / f'seed_{corner}_{temp}C_timing.rpt')
        assert signoff == acceptance, (corner, temp, signoff, acceptance)
        operating = (gateware / f'alinx_ax7101_signoff_{corner}_{temp}C_operating.rpt').read_text()
        assert re.search(r'Junction Temp\s*\|\s*' + str(temp), operating) or f'{temp}' in operating
        negative = (gateware / f'alinx_ax7101_signoff_{corner}_{temp}C_negative.rpt').read_text()
        negative_paths = len(re.findall(r'^Slack \(VIOLATED\)', negative, re.M))
        timing.append(dict(corner=corner, temperature_C=temp, **signoff, negative_paths=negative_paths))
    grade = (gateware / 'alinx_ax7101_signoff_grade.txt').read_text()
    with (reports / 'seed_crossings.tsv').open() as stream:
        crossings = list(csv.DictReader(stream, delimiter='\t'))
    assert len(crossings) == 16
    for row in crossings:
        for key in ('slack_ns', 'requirement_ns', 'datapath_ns'):
            row[key] = float(row[key])
        assert row['requirement_ns'] == 8.0, row
    pairs = {(row['from'], row['to']) for row in crossings}
    interaction_reports = [reports / 'seed_interaction.rpt', *sorted(reports.glob('seed_*C_interaction.rpt')),
                           gateware / 'alinx_ax7101_clock_interaction.rpt',
                           gateware / 'alinx_ax7101_signoff_clock_interaction.rpt']
    interactions = [eth_rows(report, pairs) for report in interaction_reports]
    log_lines = (gateware / 'vivado.log').read_text(errors='replace').splitlines()
    application = [dict(line=n, text=line) for n, line in enumerate(log_lines, 1) if line.startswith('CONSTRAINTS:')]
    assert any(re.search(r'quasi_static cells=[1-9]\d* setup=4 hold=3', row['text']) for row in application)
    severity = {s: sum(line.startswith(s + ':') for line in log_lines)
                for s in ('WARNING', 'CRITICAL WARNING', 'ERROR')}
    critical = [dict(line=n, text=line) for n, line in enumerate(log_lines, 1)
                if line.startswith('CRITICAL WARNING:')]
    codes = {code: sum(bool(re.match(r'^(?:CRITICAL WARNING|WARNING|ERROR):\s+\[(?:Vivado|Designutils) ' + code + r'\]', line))
                       for line in log_lines) for code in ('12-4739', '20-1307', '12-5201')}
    assert codes == {'12-4739': 0, '20-1307': 0, '12-5201': 0}, codes
    tcl = (gateware / 'alinx_ax7101.tcl').read_text().splitlines()

    def at(pattern):
        hits = [n for n, line in enumerate(tcl, 1) if re.match(pattern, line)]
        assert len(hits) == 1, (pattern, hits)
        return hits[0]
    order = dict(synth_design=at(r'synth_design '), milan_eth_constraints=at(r'milan_eth_constraints '),
                 opt_design=at(r'opt_design '), kl_timing_grade_configure=at(r'kl_timing_grade_configure '),
                 place_design=at(r'place_design '), route_design=at(r'route_design '),
                 kl_timing_grade_reports=at(r'kl_timing_grade_reports '),
                 report_clock_interaction=at(r'report_clock_interaction '),
                 write_bitstream=at(r'write_bitstream '))
    assert order['synth_design'] < order['milan_eth_constraints'] < order['opt_design']
    assert order['opt_design'] < order['kl_timing_grade_configure'] < order['place_design']
    assert order['route_design'] < order['kl_timing_grade_reports'] < order['write_bitstream']
    launch = Path(run['log']).read_text(errors='replace')
    gate_line = [line for line in launch.splitlines() if line.startswith('[constraints] ')]
    assert any('no 12-4739, 20-1307 or 12-5201 diagnostics' in line for line in gate_line), gate_line
    bits = sorted(p.name for p in gateware.glob('*.bit*'))
    assert (gateware / 'alinx_ax7101.bit').is_file() and not list(gateware.glob('*.bit.rejected')), bits
    assert (directory / 'flashboot_layout.json').is_file()
    margin_ok = all(r['WNS'] >= 0.03 and r['WHS'] >= 0 and r['TNS'] == r['THS'] == 0 and r['negative_paths'] == 0
                    for r in timing)
    bound_ok = all(row['slack_ns'] >= 0 for row in crossings)
    summary.append(dict(seed=run['seed'], directive=run['directive'], head=run['head'],
                        build_seconds=run['elapsed_s'], timing=timing, grade=grade, crossings=crossings,
                        interactions=interactions, application=application, emitted_severity_counts=severity,
                        critical_warnings=critical, diagnostic_counts=codes, tcl_order=order,
                        build_gate=gate_line, bitstreams=bits, margin_ok=margin_ok, bound_ok=bound_ok))
    selected = [*reports.glob('*'), *gateware.glob('alinx_ax7101_signoff*'),
                gateware / 'alinx_ax7101_clock_interaction.rpt', gateware / 'alinx_ax7101_exceptions.rpt',
                gateware / 'vivado.log', Path(run['log']), gateware / 'alinx_ax7101_route.dcp',
                gateware / 'alinx_ax7101.bit', gateware / 'alinx_ax7101.xdc', gateware / 'alinx_ax7101.tcl',
                directory / 'flashboot_layout.json', directory / 'aem_desc.bin']
    for path in selected:
        if path.is_file():
            artifacts.append(dict(path=str(path), size=path.stat().st_size, sha256=digest(path)))
(out / 'sweep-summary.json').write_text(json.dumps(dict(rom_check=rom_check, seeds=summary), indent=2) + '\n')
(out / 'sweep-artifacts.json').write_text(json.dumps(artifacts, indent=2) + '\n')
for row in summary:
    print(row['seed'], 'margin', row['margin_ok'], 'bound', row['bound_ok'],
          'worst WNS', min(v['WNS'] for v in row['timing']), 'worst WHS', min(v['WHS'] for v in row['timing']),
          'worst crossing slack', min(v['slack_ns'] for v in row['crossings']),
          'CW', row['emitted_severity_counts']['CRITICAL WARNING'])
assert len(summary) == 3 and all(row['margin_ok'] and row['bound_ok'] for row in summary)
print('COLLECT OK')
