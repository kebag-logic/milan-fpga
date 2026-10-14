#!/usr/bin/env python3
"""Read exact-head hosted jobs and measure first-start to last-end when available."""
import datetime
import json
from pathlib import Path
import subprocess

packet = Path(__file__).resolve().parent
repo = 'kebag-logic/milan-fpga'
head = 'cf9c936697a06e44c41681bcc12dc612a3242eb2'
def gh(*args):
    return json.loads(subprocess.check_output(['gh', *args], text=True))
runs = gh('run', 'list', '-R', repo, '--commit', head, '--limit', '100', '--json',
          'databaseId,workflowName,status,conclusion,headSha,event,createdAt')
(packet / 'hosted-runs.json').write_text(json.dumps(runs, indent=2) + '\n')
checks = gh('pr', 'view', '739', '-R', repo, '--json', 'headRefOid,statusCheckRollup')
(packet / 'hosted-pr-checks.json').write_text(json.dumps(checks, indent=2) + '\n')
rows = []
for run in runs:
    data = gh('run', 'view', str(run['databaseId']), '-R', repo, '--json',
              'jobs,headSha,event,status,conclusion,workflowName')
    assert data['headSha'] == head
    (packet / ('hosted-jobs-' + str(run['databaseId']) + '.json')).write_text(json.dumps(data, indent=2) + '\n')
    jobs = data['jobs']
    executed = [j for j in jobs if j.get('conclusion') != 'skipped' and j.get('startedAt')]
    complete = executed and all(j.get('completedAt') and not j['completedAt'].startswith('0001') for j in executed)
    row = dict(workflow=run['workflowName'], run=run['databaseId'], conclusion=data['conclusion'],
               executed_jobs=len(executed), skipped_jobs=sum(j.get('conclusion') == 'skipped' for j in jobs))
    if complete:
        parse = lambda value: datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
        start = min(parse(j['startedAt']) for j in executed)
        end = max(parse(j['completedAt']) for j in executed)
        row.update(first_start=start.isoformat(), last_end=end.isoformat(), seconds=int((end-start).total_seconds()))
    rows.append(row)
print(json.dumps({'head': head, 'queried_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'runs': rows, 'timing_status': 'available' if rows else 'NOT AVAILABLE: no exact-head runs returned',
                  'acceptance_owner': 'manager'}, indent=2))
