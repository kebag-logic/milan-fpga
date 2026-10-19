#!/usr/bin/env python3
"""Fetch public scope and pinned parent authorities, without fetching review reports."""
import concurrent.futures
import json
import pathlib
import subprocess

P = pathlib.Path(__file__).resolve().parent
OUT = P / 'public-authorities'
OUT.mkdir(exist_ok=True)
PARENT = 'e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f'
HEAD = '2022d363fc622f6bbf4c312239fc3db741b4d29a'
FILES = ['hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv',
         'hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv', 'hdl/milan/milan_datapath.sv',
         'tb/verilator/milan_dp/sim_gptp.cpp', 'tb/verilator/milan_dp/sim_ax1x1gptp.cpp',
         'tb/verilator/gptp_shadow/sim_main.cpp', 'docs/design/GPTP_PLANE.md']

def api(path, raw=False):
    return subprocess.check_output(['gh', 'api', path] + (['-H', 'Accept: application/vnd.github.raw+json'] if raw else []))

def fetch(path):
    data = api(f'repos/kebag-logic/milan-fpga/contents/{path}?ref={PARENT}', True)
    (OUT / pathlib.Path(path).name).write_bytes(data)
    return path

with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
    for path in pool.map(fetch, FILES): print('Fetched parent authority:', path)

for n in [82, 84, 85]:
    obj = json.loads(api(f'repos/Mister-M-alt/FPGA-gPTP/issues/{n}'))
    (OUT / f'issue{n}.md').write_text(obj['html_url'] + '\n\n' + obj['body'] + '\n')
for cid in [6257168490,6259159680,6259958948,6263973943,6264025745,6264069827]:
    obj = json.loads(api(f'repos/Mister-M-alt/FPGA-gPTP/issues/comments/{cid}'))
    (OUT / f'comment-{cid}.md').write_text(obj['html_url'] + '\n\n' + obj['body'] + '\n')
pr = json.loads(api('repos/Mister-M-alt/FPGA-gPTP/pulls/86'))
(OUT / 'PR86.md').write_text(pr['html_url'] + '\n\n' + pr['body'] + '\n')
for name, suffix in [('hosted-runs', f'actions/runs?head_sha={HEAD}'),
                     ('hosted-checks', f'commits/{HEAD}/check-runs'),
                     ('hosted-status', f'commits/{HEAD}/status'),
                     ('source-commit', f'commits/{HEAD}')]:
    (OUT / (name + '.json')).write_bytes(api('repos/Mister-M-alt/FPGA-gPTP/' + suffix))
tree = json.loads(api(f'repos/kebag-logic/milan-fpga/git/trees/{PARENT}?recursive=1'))
pins = {x['path']: x['sha'] for x in tree['tree'] if x['mode'] == '160000'}
(OUT / 'parent-gitlinks.json').write_text(json.dumps(pins, indent=2) + '\n')
print('Fetched public scope, source signature metadata, hosted metadata, and parent dependency pins.')
