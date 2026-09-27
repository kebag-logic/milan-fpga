#!/usr/bin/env python3
"""Recompute every published table cell of docs/findings/397_SERVICE_BUDGET.md
from the committed receipts' integer system cycles (independent arithmetic).
usage: check_tables.py <repo>"""
import json, math, re, sys
from pathlib import Path
repo = Path(sys.argv[1])
doc = (repo / 'docs/findings/397_SERVICE_BUDGET.md').read_text()
NAME = {'Boot to entity enabled': 'boot_to_entity_enabled', 'AEM copy/CRC, enclosed by boot': 'aem_copy_crc_enclosed_by_boot',
        'Binding restore walk': 'restore_walk', 'Journal erase envelope': 'erase_enclosed_to_first_program',
        'Journal START-to-ACK': 'journal_commit_bracket', 'Maximum heartbeat gap': 'maximum_heartbeat_gap',
        '`milan_status`': 'milan_status', '`milan_gettime`': 'milan_gettime', '`milan_settime`, maximum tested case': 'milan_settime',
        '`milan_utc`, maximum tested case': 'milan_utc', '`milan_nvm` status': 'milan_nvm', '`milan_nvm commit`': 'milan_nvm commit',
        '`milan_nvm wipe`, whole command': 'milan_nvm wipe', 'Wipe erase envelope, maximum of two': 'wipe_erase_envelope',
        '`milan_nvm invalid`': 'milan_nvm invalid'}
bad = 0
sections = re.split(r'\*\*(1x1|8x8): populated', doc)
for shape, body in ((sections[1], sections[2]), (sections[3], sections[4])):
    rec = json.loads((repo / f'docs/findings/397_SERVICE_BUDGET_{shape.upper()}.json').read_text())
    rows = rec['rows']
    for line in body.split('\n\n**')[0].splitlines():
        m = re.match(r'\| (.+?) \| ([\d,]+) \| ([\d.]+) \| ([\d,N/A]+) \| ([-\d.N/A]+) \|', line)
        if not m:
            continue
        duty, cyc, ms, bud, mar = m.groups()
        key = NAME[duty]
        cands = [r for r in rows if r['duty'] == key or (key == 'milan_settime' and r['duty'].startswith('milan_settime'))
                 or (key == 'milan_utc' and r['duty'].startswith('milan_utc'))]
        if key == 'milan_nvm':
            cands = [r for r in rows if r['duty'] == 'milan_nvm']
        if key == 'milan_status':
            cands = [r for r in rows if r['duty'] == 'milan_status']
        worst = max(cands, key=lambda r: r['sys_cycles'])
        s = worst['sys_cycles']
        exp_cyc = math.ceil(s / 2); exp_ms = s / 100_000
        b = worst['budget_ms']
        ok = (int(cyc.replace(',', '')) == exp_cyc and abs(float(ms) - exp_ms) < 5e-6 and
              (bud == 'N/A' if b is None else int(bud.replace(',', '')) == b) and
              (mar == 'N/A' if b is None else abs(float(mar) - (b - exp_ms)) < 5e-6))
        bad += not ok
        print(f"{shape} {'OK ' if ok else 'BAD'} {duty:40s} sys={s} cpu={exp_cyc} ms={exp_ms:.5f} n={len(cands)}")
# device projection table
for line in doc.splitlines():
    m = re.match(r'\| (1x1|8x8) (.+?) \| ([\d.]+) \| (\d+) \| ([\d,]+) \| ([\d.]+) \|', line)
    if not m:
        continue
    shape, op, svc, wip, dev, tot = m.groups()
    rec = json.loads((repo / f'docs/findings/397_SERVICE_BUDGET_{shape.upper()}.json').read_text())
    key = {'journal START-to-ACK': 'journal_commit_bracket', 'whole console commit': 'milan_nvm commit',
           'journal erase envelope': 'erase_enclosed_to_first_program', 'whole wipe': 'milan_nvm wipe'}[op]
    r = max((r for r in rec['rows'] if r['duty'] == key), key=lambda r: r['sys_cycles'])
    img = rec['media']['image_bytes']; pages = math.ceil(img / 256)
    devmax = {'journal START-to-ACK': 3000 + 5 * pages, 'whole console commit': 3000 + 5 * pages,
              'journal erase envelope': 3000, 'whole wipe': 6000}[op]
    ok = (abs(float(svc) - r['service_ms']) < 5e-6 and abs(float(wip) - r['device_wait_ms']) < 5e-3
          and int(dev.replace(',', '')) == devmax and abs(float(tot) - (r['service_ms'] + devmax)) < 5e-6)
    bad += not ok
    print(f"{shape} {'OK ' if ok else 'BAD'} projection {op:24s} svc={r['service_ms']:.5f} wip={r['device_wait_ms']} devmax={devmax}")
print('mismatches:', bad)
sys.exit(1 if bad else 0)
