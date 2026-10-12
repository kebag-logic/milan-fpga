#!/usr/bin/env python3
"""Deliver a first signal at monitor cleanup entry using exact AST definitions.

Run only in the packet's disposable namespace. The event stream and command
collaborators are inert. A real Python worker models a reader held in a move.
No host runner import, command execution, daemon or source edit is performed.
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

root = Path(sys.argv[1])
raw = (root / 'scripts/act_ci.py').read_bytes()
tree = ast.parse(raw)
names = {
    'Refusal', 'TerminationRequest', '_CleanupSignalLatch',
    'cleanup_termination_signals', 'blocked_cleanup_signals',
    'start_cleanup_safe_thread', 'start_cleanup_thread_or_refuse',
    'deferred_cleanup_signal_delivery', 'run_with_cleanup_signals',
    'JobCpuRanges', 'read_job_cpu_events', 'join_job_cpu_reader',
    'stop_job_cpu_range_monitor', 'job_cpu_range_monitor',
}
definitions = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
assert {n.name for n in definitions} == names
monitor = next(n for n in definitions if n.name == 'job_cpu_range_monitor')
outer_try = next(n for n in monitor.body if isinstance(n, ast.Try) and n.finalbody)
entry_line = outer_try.finalbody[0].lineno
m = ModuleType('exact_cleanup_entry')
sys.modules[m.__name__] = m
m.__dict__.update(vars(typing))
m.__dict__.update(contextlib=contextlib, dataclass=dataclass, field=field, json=json,
    re=re, signal=signal, subprocess=subprocess, sys=sys, threading=threading,
    time=time, ProcessSeams=SimpleNamespace, DOCKER_COMMAND_TIMEOUT=1,
    DOCKER_OWNER_LABEL='test.owner', DOCKER_ID_RE=re.compile(r'[0-9a-f]{64}'),
    JOB_CPU_RANGE_EVENTS=('create','update','start','die','destroy'),
    CLEANUP_SIGNALS=(signal.SIGINT, signal.SIGTERM, signal.SIGHUP),
    RC_OK=0, RC_FAILED=1, RC_REFUSED=2,
    docker_prefix=lambda *args: ['INERT_ONLY'])
unit = ast.Module(body=[ast.ImportFrom(module='__future__', names=[ast.alias(name='annotations')], level=0), *definitions], type_ignores=[])
exec(compile(ast.fix_missing_locations(unit), 'exact-head-selected-definitions', 'exec'), m.__dict__)

def exercise(signum, inject_at_entry):
    contained = threading.Event()
    moving = threading.Event()
    reader_finished = threading.Event()
    trail = []
    threads = []
    config = {}
    event = json.dumps({'Type':'container','Action':'create','Actor':{
        'ID':'a'*64,'Attributes':{m.DOCKER_OWNER_LABEL:'1'*32}}}) + '\n'
    class Pipe:
        closed = False
        def __iter__(self):
            try:
                yield event
                assert contained.wait(5), 'probe stream deadline'
                trail.append('stream ended')
            finally:
                reader_finished.set()
        def close(self):
            self.closed = True
    pipe = Pipe()
    proc = SimpleNamespace(pid=424242, stdout=pipe, returncode=None, poll=lambda:None)
    def terminate(*args, **kwargs):
        trail.append('contained')
        contained.set()
    def command(args, **kwargs):
        if args[:2] == ['container','update']:
            threads.append(threading.current_thread())
            moving.set()
            assert contained.wait(5), 'probe move deadline'
            config[args[-1]] = args[2].split('=',1)[1]
            trail.append('moved')
            return subprocess.CompletedProcess([],0,'','')
        return subprocess.CompletedProcess([],0,config.get(args[-1],'0-3'),'')
    m.run_docker = command
    fired = False
    def trace(frame, event_kind, arg):
        nonlocal fired
        if (inject_at_entry and not fired and event_kind == 'line'
            and frame.f_code.co_name == 'job_cpu_range_monitor' and frame.f_lineno == entry_line):
            fired = True
            trail.append('first signal at cleanup entry')
            signal.raise_signal(signum)
        return trace
    snapshot = {}
    def action():
        try:
            with m.job_cpu_range_monitor(SimpleNamespace(token='1'*32), ('4-7',),
                    context=SimpleNamespace(use_sudo=False, env={}, cwd=Path('.')),
                    seams=SimpleNamespace(popen=lambda *a,**k:proc, terminate_group=terminate)):
                assert moving.wait(5), 'reader did not enter move'
                trail.append('body ended')
                if not inject_at_entry:
                    trail.append('first signal in body')
                    signal.raise_signal(signum)
        finally:
            trail.append('outer boundary teardown entry')
            snapshot.update(contained=contained.is_set(),
                reader_alive=any(t.is_alive() for t in threads),
                pipe_closed=pipe.closed, reader_finished=reader_finished.is_set())
        return 0
    diagnostic = io.StringIO()
    try:
        sys.settrace(trace)
        with contextlib.redirect_stderr(diagnostic):
            rc = m.run_with_cleanup_signals(action)
    finally:
        sys.settrace(None)
        # Reviewer cleanup follows the recorded boundary observation.
        contained.set()
        for thread in threads:
            thread.join(5)
            assert not thread.is_alive(), 'reviewer cleanup leaked a thread'
    return {'signal':signal.Signals(signum).name,
        'delivery':'cleanup entry' if inject_at_entry else 'body',
        'line':entry_line if inject_at_entry else None, 'rc':rc,
        'boundary_observation':snapshot, 'trail':trail,
        'diagnostic':diagnostic.getvalue().strip(),
        'invariant':snapshot == {'contained':True, 'reader_alive':False, 'pipe_closed':True, 'reader_finished':True}}

rows = [exercise(sig, at_entry) for sig in m.CLEANUP_SIGNALS for at_entry in (False, True)]
print(json.dumps({'source_sha256':hashlib.sha256(raw).hexdigest(), 'cases':rows}, indent=2))
sys.exit(0 if all(row['invariant'] for row in rows) else 1)
