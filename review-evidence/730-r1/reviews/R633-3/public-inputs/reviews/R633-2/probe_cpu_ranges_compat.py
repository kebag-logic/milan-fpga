#!/usr/bin/env python3
"""Offline, inert probes of selected exact-head definitions; no runner import.

Usage: python3 probe_cpu_ranges.py /path/to/review/checkout
Exit 1 reports reproduced contract violations; exit 2 is a probe setup error.
No daemon, process-group command, signal handler, or runner self-test executes.
"""
from __future__ import annotations

import ast
import contextlib
from dataclasses import dataclass, field
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
from types import ModuleType, SimpleNamespace
import typing

import yaml

NAMES = {
    'Refusal', 'job_container_width', 'replay_container_concurrency',
    'slot_cpu_base', 'container_cpuset', 'cpu_range_overlaps', 'job_cpu_ranges',
    'describe_job_cpu_ranges', 'JobCpuRanges', 'stop_job_cpu_range_monitor',
    'join_job_cpu_reader',
}
CONSTANTS = {
    'CONTAINER_CPU_LIMIT', 'CONCURRENT_JOB_LIMIT', 'ACT_DEFAULT_MAX_PARALLEL',
    'JOB_CPU_RANGE_EVENTS', 'DOCKER_OWNER_LABEL', 'DOCKER_COMMAND_TIMEOUT',
    'WORKFLOWS',
}


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    source = (root / 'scripts/act_ci.py').read_bytes()
    print('source_sha256=' + hashlib.sha256(source).hexdigest())
    tree = ast.parse(source)
    definitions = [node for node in tree.body
                   if isinstance(node, (ast.FunctionDef, ast.ClassDef))
                   and node.name in NAMES]
    assert {node.name for node in definitions} == NAMES
    m = ModuleType('review_inert_definitions')
    sys.modules[m.__name__] = m
    m.__dict__.update(vars(typing))
    m.__dict__.update(dataclass=dataclass, field=field, re=re, json=json,
                      subprocess=subprocess, pathlib=__import__('pathlib'),
                      os=SimpleNamespace(cpu_count=lambda: 128),
                      ReplaySlot=lambda number: SimpleNamespace(number=number),
                      blocked_cleanup_signals=contextlib.nullcontext)
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name) and target.id in CONSTANTS:
                m.__dict__[target.id] = ast.literal_eval(node.value)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.target.id in CONSTANTS:
                m.__dict__[node.target.id] = ast.literal_eval(node.value)
    assert CONSTANTS <= m.__dict__.keys()
    m.SLOT_JOB_RANGES = m.CONCURRENT_JOB_LIMIT * m.ACT_DEFAULT_MAX_PARALLEL
    m.DOCKER_ID_RE = re.compile(r'[0-9a-f]{64}')
    # Read shipping workflow bytes. The runner's no-follow YAML reader is not
    # executed here; these pristine files are independently byte-verified.
    m.load_workflow = lambda root, relative: yaml.load(
        (root / relative).read_text(), Loader=yaml.BaseLoader)
    unit = ast.Module(body=[ast.ImportFrom(module='__future__',
                      names=[ast.alias(name='annotations')], level=0),
                      *definitions], type_ignores=[])
    exec(compile(ast.fix_missing_locations(unit), 'exact-head-selected-definitions', 'exec'), m.__dict__)
    print('Selected definitions: ' + ', '.join(sorted(NAMES)))
    print('All collaborators inert; no candidate module import or entrypoint.')
    failures = []

    def check(label, predicate, detail):
        print(('PASS ' if predicate else 'FAIL ') + label + ': ' + json.dumps(detail, sort_keys=True))
        if not predicate:
            failures.append(label)

    widths = {name: m.replay_container_concurrency(root, (name,)) for name in m.WORKFLOWS}
    check('shipping workflow derivation', widths == {'docs': 1, 'elaborate': 1, 'rtl-fast': 1, 'rtl-full': 4}, widths)
    m.os.cpu_count = lambda: 1280
    layout = []
    for slot in range(64):
        layout.append((f'slot-{slot}-staging', m.container_cpuset(slot)))
        layout.extend((f'slot-{slot}-job-{i}', x) for i, x in enumerate(m.job_cpu_ranges(slot, 4)))
    check('maximum static disjointness', not m.cpu_range_overlaps(layout) and len(layout) == 320, {'ranges': len(layout)})
    planted = layout + [('planted-overlap', layout[1][1])]
    check('planted overlap detected', len(m.cpu_range_overlaps(planted)) == 4, m.cpu_range_overlaps(planted))
    m.os.cpu_count = lambda: 128
    for slot in (0, 3):
        print(m.describe_job_cpu_ranges(slot, widths['rtl-full'], m.job_cpu_ranges(slot, widths['rtl-full'])))
    for raw in ('${{ inputs.width }}', '-1', '1.5', ['2'], '1234567'):
        refused = False
        try:
            m.job_container_width({'strategy': {'matrix': {'n': ['1']}, 'max-parallel': raw}}, 'probe')
        except m.Refusal:
            refused = True
        check('unreadable max-parallel refused', refused, raw)
    refused = False
    try:
        width = m.job_container_width({'strategy': {'matrix': {'n': ['1']}, 'max-parallel': '5'}}, 'probe')
        m.job_cpu_ranges(0, width)
    except m.Refusal:
        refused = True
    check('too-wide max-parallel refused', refused, '5')

    token = '1' * 32
    boundary = SimpleNamespace(token=token)
    cpus = ('4-7', '8-11', '12-15', '16-19')

    def event(action, name, owner=token):
        return json.dumps({'Type': 'container', 'Action': action,
                           'Actor': {'ID': name * 64,
                                     'Attributes': {m.DOCKER_OWNER_LABEL: owner}}})

    class Daemon:
        def __init__(self, ambiguous=False):
            self.config = {}
            self.live = set()
            self.ambiguous = ambiguous

        def assign(self, cid, cpuset):
            self.config[cid] = cpuset
            if self.ambiguous and cid == 'a' * 64:
                raise m.Refusal('job container CPU-range move timed out after server application')
            return subprocess.CompletedProcess([], 0, '', '')

        def read_cpus(self, cid):
            if cid not in self.config:
                return subprocess.CompletedProcess([], 1, '', 'No such container')
            return subprocess.CompletedProcess([], 0, self.config[cid], '')

        def deliver(self, record, action, name):
            cid = name * 64
            if action == 'create':
                self.config[cid] = '0-3'
            elif action == 'start':
                self.live.add(cid)
            elif action in ('die', 'destroy'):
                self.live.discard(cid)
            if action == 'destroy':
                self.config.pop(cid, None)
            record.observe(event(action, name))

        def snapshot(self, record):
            return {'live_cpu_ranges': {cid[0]: self.config[cid] for cid in sorted(self.live)},
                    'held': {cid[0]: index for cid, index in record.held.items()},
                    'problems': record.problems, 'summary': record.summary()}

        def disjoint(self):
            return not m.cpu_range_overlaps([(cid[0], self.config[cid]) for cid in sorted(self.live)])

    daemon = Daemon()
    record = m.JobCpuRanges(boundary, cpus, daemon.assign, daemon.read_cpus)
    for name in 'abcd':
        for action in ('create', 'update', 'start'):
            daemon.deliver(record, action, name)
    check('four ordinary live containers disjoint', daemon.disjoint(), daemon.snapshot(record))
    for action in ('die', 'destroy'):
        daemon.deliver(record, action, 'a')
    for action in ('create', 'update', 'start'):
        daemon.deliver(record, action, 'e')
    check('create/die/destroy reuse disjoint', daemon.disjoint(), daemon.snapshot(record))
    before = dict(record.held)
    record.observe(event('create', 'f', '2' * 32))
    record.observe('not-json')
    check('foreign and malformed event cannot assign', before == record.held and len(record.problems) == 2, record.problems)

    daemon = Daemon()
    record = m.JobCpuRanges(boundary, cpus, daemon.assign, daemon.read_cpus)
    sequence = [('create', 'a'), ('update', 'a'), ('start', 'a'), ('die', 'a'),
                ('create', 'b'), ('update', 'b'), ('start', 'b'), ('start', 'a')]
    for action, name in sequence:
        daemon.deliver(record, action, name)
    check('F1 restart retains exclusive range', daemon.disjoint(), {'sequence': sequence, **daemon.snapshot(record)})

    daemon = Daemon(ambiguous=True)
    record = m.JobCpuRanges(boundary, cpus, daemon.assign, daemon.read_cpus)
    sequence = [('create', 'a'), ('update', 'a'), ('start', 'a'),
                ('create', 'b'), ('update', 'b'), ('start', 'b')]
    for action, name in sequence:
        daemon.deliver(record, action, name)
    check('F2 post-accept timeout preserves exclusive range', daemon.disjoint(), {'sequence': sequence, **daemon.snapshot(record)})

    m.os.cpu_count = lambda: 19
    refused = False
    result = None
    try:
        result = m.job_cpu_ranges(0, 4)
    except m.Refusal:
        refused = True
    check('F3 insufficient slot-0 CPUs refuse', refused, {'host_cpus': 19, 'concurrency': 4, 'returned_ranges': result})
    refused = False
    try:
        m.job_cpu_ranges(1, 4)
    except m.Refusal:
        refused = True
    check('insufficient isolated-slot CPUs refuse', refused, {'host_cpus': 19})

    # Inert teardown-fault model; neither a process nor a thread is created.
    calls = []
    class Reader:
        ident = 1
        def join(self, **kwargs): calls.append('joined')
        def is_alive(self): return False
    class Process:
        pid = 424242
        stdout = io.StringIO()
        returncode = None
        def poll(self): return None
    def terminate(*args, **kwargs):
        calls.append('group-absent-but-leader-reap-failed')
        raise m.Refusal('cannot reap interrupted host process leader')
    process = Process()
    try:
        m.stop_job_cpu_range_monitor(process, Reader(), record,
                                    context=SimpleNamespace(use_sudo=False),
                                    seams=SimpleNamespace(terminate_group=terminate))
    except m.Refusal:
        calls.append('refusal-propagated')
    check('F4 shutdown refusal still joins reader', 'joined' in calls,
          {'calls': calls, 'pipe_closed': process.stdout.closed})
    print('CONTRACT VIOLATIONS=' + str(len(failures)))
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
