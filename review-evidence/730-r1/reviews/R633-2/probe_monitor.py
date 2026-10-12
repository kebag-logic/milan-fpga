#!/usr/bin/env python3
"""Inert extraction of the allocator, monitor and workflow-return path.

Usage: python3 probe_monitor.py CHECKOUT
No runner import, entrypoint, self-test, host command, or daemon is executed.
Threads below are ordinary in-process probes and are joined before return.
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
import signal
import subprocess
import sys
import threading
import time
from types import ModuleType, SimpleNamespace
import typing

NAMES = {'Refusal', 'TerminationRequest', 'JobCpuRanges', 'read_job_cpu_events',
         'join_job_cpu_reader', 'stop_job_cpu_range_monitor', 'job_cpu_range_monitor',
         'report_job_cpu_ranges', 'execute_workflows', 'run_with_cleanup_signals',
         'joined_before_exit'}
root = Path(sys.argv[1]).resolve()
source = (root/'scripts/act_ci.py').read_text()

def load(remove_join=False):
    tree = ast.parse(source)
    definitions = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))
                   and n.name in NAMES]
    assert {n.name for n in definitions} == NAMES
    if remove_join:
        stop = next(n for n in definitions if n.name == 'stop_job_cpu_range_monitor')
        matches = [n for n in ast.walk(stop) if isinstance(n, ast.If)
                   and ast.unparse(n.test) == 'reader is not None and reader.ident is not None']
        assert len(matches) == 1
        matches[0].test = ast.Constant(False)
    m = ModuleType('inert_monitor_mutant' if remove_join else 'inert_monitor_clean')
    sys.modules[m.__name__] = m
    m.__dict__.update(vars(typing))
    m.__dict__.update(contextlib=contextlib, dataclass=dataclass, field=field,
        json=json, re=re, signal=signal, subprocess=subprocess, sys=sys,
        threading=threading, time=time, ProcessSeams=SimpleNamespace,
        blocked_cleanup_signals=contextlib.nullcontext,
        deferred_cleanup_signal_delivery=contextlib.nullcontext,
        cleanup_termination_signals=contextlib.nullcontext,
        start_cleanup_thread_or_refuse=lambda thread, description: thread.start(),
        docker_prefix=lambda *args: ['INERT_ONLY'], DOCKER_COMMAND_TIMEOUT=1,
        DOCKER_OWNER_LABEL='test.owner', DOCKER_ID_RE=re.compile(r'[0-9a-f]{64}'),
        JOB_CPU_RANGE_EVENTS=('create','update','start','die','destroy'),
        RC_OK=0, RC_FAILED=1, RC_REFUSED=2,
        WORKFLOWS={'docs':'.github/workflows/docs.yml'})
    unit = ast.Module(body=[ast.ImportFrom(module='__future__',
        names=[ast.alias(name='annotations')], level=0), *definitions], type_ignores=[])
    exec(compile(ast.fix_missing_locations(unit), 'selected-exact-head-definitions', 'exec'), m.__dict__)
    return m

def lifecycle(m, body_kind='return', reap_failure=False):
    contained = threading.Event()
    moving = threading.Event()
    trail = []
    config = {}
    token = '1'*32
    event = json.dumps({'Type':'container','Action':'create','Actor':{
        'ID':'a'*64,'Attributes':{m.DOCKER_OWNER_LABEL:token}}})+'\n'
    class Pipe:
        closed = False
        def __iter__(self):
            yield event
            assert contained.wait(2), 'probe containment deadline'
            trail.append('stream ended')
        def close(self):
            self.closed = True
    pipe = Pipe()
    proc = SimpleNamespace(pid=424242, stdout=pipe, returncode=None, poll=lambda: None)
    def terminate(*args, **kwargs):
        trail.append('contained')
        contained.set()
        if reap_failure:
            raise m.Refusal('cannot reap interrupted host process leader')
    def inert_command(args, **kwargs):
        if args[:2] == ['container','update']:
            moving.set()
            assert contained.wait(2), 'probe containment deadline'
            time.sleep(0.05)
            config[args[-1]] = args[2].split('=',1)[1]
            trail.append('moved')
            return subprocess.CompletedProcess([],0,'','')
        return subprocess.CompletedProcess([],0,config.get(args[-1],'0-3'),'')
    m.run_docker = inert_command
    primary = None
    if body_kind == 'signal':
        primary = m.TerminationRequest(signal.SIGTERM)
    elif body_kind == 'error':
        primary = RuntimeError('original body failure')
    boundary = SimpleNamespace(token=token)
    context = SimpleNamespace(use_sudo=False, env={}, cwd=Path('.'))
    seams = SimpleNamespace(popen=lambda *a,**k:proc, terminate_group=terminate)
    record = None
    surfaced = None
    def action():
        nonlocal record
        with m.job_cpu_range_monitor(boundary, ('4-7','8-11'), context=context, seams=seams) as record:
            assert moving.wait(2), 'probe reader never entered move'
            trail.append('body ended')
            if primary:
                raise primary
        return 0
    text = io.StringIO()
    rc = None
    try:
        with contextlib.redirect_stderr(text):
            rc = m.run_with_cleanup_signals(action)
    except BaseException as exc:
        surfaced = exc
        rc = 2 if isinstance(exc,m.Refusal) else None
    trail.append('monitor exited')
    alive_at_exit = any(t.name=='act-ci-cpu-range-monitor' for t in threading.enumerate())
    # Probe cleanup is outside the candidate boundary. It cannot repair the observation above.
    for thread in threading.enumerate():
        if thread.name == 'act-ci-cpu-range-monitor':
            thread.join(3)
            assert not thread.is_alive(), 'probe leaked worker'
    return {'body':body_kind,'reap_failure':reap_failure, 'rc':rc,
        'exception':type(surfaced).__name__ if surfaced else None,
        'message':str(surfaced) if surfaced else None,
        'prior_exception_in_context':str(surfaced.__context__) if surfaced and surfaced.__context__ else None,
        'trail':trail, 'alive_at_boundary_exit':alive_at_exit,
        'pipe_closed':pipe.closed, 'joined_before_exit_predicate':m.joined_before_exit(trail),
        'primary_is_propagated':surfaced is primary if primary else surfaced is None,
        'diagnostic':text.getvalue().strip()}

def workflow_warning(m, rc):
    trail=[]
    boundary=SimpleNamespace(token='1'*32,job_volume_prefixes=('act-docs-',))
    @contextlib.contextmanager
    def monitor(*args,**kwargs):
        trail.append('monitor-enter')
        rec=m.JobCpuRanges(boundary,('4-7',),None,None)
        rec.outcome['a'*64]='staging'
        rec.problems=['container stays on staging','stream ended early']
        yield rec
        trail.append('monitor-exit')
    m.job_cpu_range_monitor=monitor
    m.inspect_docker_boundary=lambda *a,**k:None
    m.allocate_tcp_port=lambda:1
    m.build_act_command=lambda *a,**k:['INERT_ONLY']
    m.execute_act_boundary=lambda *a,**k:rc
    m.cleanup_owned_containers=lambda *a,**k:trail.append('containers') or 0
    m.cleanup_act_job_volumes=lambda *a,**k:trail.append('volumes') or []
    m.require_live_pull_request=lambda *a,**k:None
    m.check_run_integrity=lambda *a,**k:None
    m.SpawnSeams=SimpleNamespace
    run=SimpleNamespace(pr=SimpleNamespace(head_sha='5ba8313a3f036f34aac1a6bfbfcec0e0efd8c646'),repository='inert')
    plan=SimpleNamespace(workflows=['docs'],job_volume_scope={'docs':'act-docs-'},
                         prefix=[],dry_run=False,cpu_ranges=('4-7',))
    output=io.StringIO()
    with contextlib.redirect_stdout(output),contextlib.redirect_stderr(output):
        answer=m.execute_workflows(run,None,plan,boundary,context=None)
    return {'workflow_exit':rc,'runner_exit':answer,'trail':trail,'output':output.getvalue().splitlines()}

print('source_sha256='+hashlib.sha256(source.encode()).hexdigest())
print('No runner import or self-test; selected definitions with inert collaborators only.')
rows=[]
for body,fault in [('return',False),('return',True),('error',False),('error',True),('signal',False),('signal',True)]:
    row=lifecycle(load(),body,fault)
    print('LIFECYCLE '+json.dumps(row,sort_keys=True))
    rows.append(row)
mutant=lifecycle(load(remove_join=True))
print('NO_JOIN_MUTANT '+json.dumps(mutant,sort_keys=True))
for rc in (0,3):
    print('WARNING '+json.dumps(workflow_warning(load(),rc),sort_keys=True))
assert all(row['joined_before_exit_predicate'] and row['pipe_closed'] and not row['alive_at_boundary_exit'] for row in rows)
assert not mutant['joined_before_exit_predicate'] and mutant['alive_at_boundary_exit']
lost=next(row for row in rows if row['body']=='signal' and row['reap_failure'])
print('SIGNAL_PRESERVATION '+('PASS' if lost['rc']==143 else 'FAIL')+
      ': expected 143, observed '+str(lost['rc']))
raise SystemExit(0 if lost['rc']==143 else 1)
