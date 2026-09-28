"""Summarize exact-head sweep reports without copying large artifacts."""
import csv
import hashlib
import json
from pathlib import Path
import re

out = Path(__file__).resolve().parent
runs = json.loads((out/'sweep-results.json').read_text())
summary = []
artifacts = []

def timing_row(path):
    section = path.read_text().split('| Design Timing Summary',1)[1]
    line = next(line for line in section.splitlines()
                if re.match(r'^\s*-?\d+\.\d+\s+-?\d+\.\d+\s+\d+',line))
    columns = line.split()
    return dict(WNS=float(columns[0]),TNS=float(columns[1]),
                WHS=float(columns[4]),THS=float(columns[5]))

for run in runs:
    assert run['rc'] == run['report_rc'] == 0, run
    directory = Path(run['directory'])
    reports = directory/'acceptance'
    rows = []
    for temperature in (0,85):
        for corner in ('Slow','Fast'):
            name = f'seed_{corner}_{temperature}C'
            values = timing_row(reports/(name+'_timing.rpt'))
            rows.append(dict(temperature_C=temperature,corner=corner,**values))
    with (reports/'seed_crossings.tsv').open() as stream:
        crossings = list(csv.DictReader(stream,delimiter='\t'))
    assert len(crossings)==16
    for row in crossings:
        row['slack_ns']=float(row['slack_ns'])
        row['requirement_ns']=float(row['requirement_ns'])
        row['datapath_ns']=float(row['datapath_ns'])
        assert row['requirement_ns']==8.0,row
    pairs = {(row['from'],row['to']) for row in crossings}
    interactions = []
    for report in [reports/'seed_interaction.rpt', *sorted(reports.glob('seed_*C_interaction.rpt'))]:
        matched = []
        all_eth_pairs = []
        for line in report.read_text().splitlines():
            words = line.split()
            if len(words)>=2 and 'eth_clocks0_rx' in words[:2]:
                assert 'unsafe' not in line.lower(),line
                all_eth_pairs.append(line.strip())
            if len(words)>=2 and (words[0],words[1]) in pairs:
                assert 'unsafe' not in line.lower(),line
                assert 'Max Delay Datapath Only' in line,line
                matched.append(line.strip())
        assert len(matched)==4,(report,matched)
        interactions.append(dict(report=str(report),pairs=matched,all_eth_pairs=all_eth_pairs))
    log = directory/'gateware/vivado.log'
    application_lines = [dict(line=n,text=line) for n,line in enumerate(log.read_text().splitlines(),1)
                         if line.startswith('CONSTRAINTS:')]
    assert len(application_lines)==3, application_lines
    assert any(re.search(r'quasi_static cells=[1-9][0-9]* setup=4 hold=3', row['text'])
               for row in application_lines), application_lines
    severity_counts = {severity:sum(line.startswith(severity+':') for line in log.read_text().splitlines())
                       for severity in ('WARNING','CRITICAL WARNING','ERROR')}
    warning_lines = [dict(line=n,text=line) for n,line in enumerate(log.read_text().splitlines(),1)
                     if line.startswith('CRITICAL WARNING:')]
    counts = {code:sum(code in line['text'] for line in warning_lines)
              for code in ('12-4739','20-1307','12-5201')}
    assert counts['12-4739']==counts['20-1307']==0
    margin_ok = all(row['WNS']>=0.03 and row['WHS']>=0 and row['TNS']==row['THS']==0 for row in rows)
    bound_ok = all(row['slack_ns']>=0 for row in crossings)
    summary.append(dict(seed=run['seed'],directive=run['directive'],head=run['head'],
                        timing=rows,crossings=crossings,interactions=interactions,
                        critical_warnings=warning_lines,warning_counts=counts,application=application_lines,
                        emitted_severity_counts=severity_counts,
                        margin_ok=margin_ok,bound_ok=bound_ok))
    selected = list(reports.glob('*'))+[log,Path(run['log']),
        directory/'gateware/alinx_ax7101_route.dcp',directory/'gateware/alinx_ax7101.bit',
        directory/'gateware/alinx_ax7101.xdc',directory/'gateware/alinx_ax7101.tcl',
        directory/'flashboot_layout.json',directory/'aem_desc.bin']
    for path in selected:
        if path.is_file():
            with path.open('rb') as stream:
                digest=hashlib.file_digest(stream,'sha256').hexdigest()
            artifacts.append(dict(path=str(path),size=path.stat().st_size,sha256=digest))
(out/'sweep-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(out/'sweep-artifacts.json').write_text(json.dumps(artifacts,indent=2)+'\n')
for row in summary:
    print(row['seed'],'margin',row['margin_ok'],'bound',row['bound_ok'],
          'worst WNS',min(v['WNS'] for v in row['timing']),
          'worst WHS',min(v['WHS'] for v in row['timing']),
          'worst crossing slack',min(v['slack_ns'] for v in row['crossings']))
assert all(row['margin_ok'] and row['bound_ok'] for row in summary)
