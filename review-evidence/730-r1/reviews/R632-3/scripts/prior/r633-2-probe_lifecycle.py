#!/usr/bin/env python3
"""Inert allocation probes with independently modeled daemon state.

Usage: python3 probe_lifecycle.py CHECKOUT
Only selected definitions execute; no runner import or entrypoint.
"""
from __future__ import annotations
import ast
from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
import random
import re
import subprocess
import sys
from types import ModuleType, SimpleNamespace
import typing

source=(Path(sys.argv[1])/'scripts/act_ci.py').read_text()
m=ModuleType('allocation_only')
sys.modules[m.__name__]=m
m.__dict__.update(vars(typing))
m.__dict__.update(dataclass=dataclass,field=field,re=re,json=json,subprocess=subprocess,
    os=SimpleNamespace(cpu_count=lambda:1280),ReplaySlot=lambda x:SimpleNamespace(number=x),
    CONTAINER_CPU_LIMIT=4,SLOT_JOB_RANGES=4,CONCURRENT_JOB_LIMIT=1,ACT_DEFAULT_MAX_PARALLEL=4,
    DOCKER_ID_RE=re.compile(r'[0-9a-f]{64}'),DOCKER_OWNER_LABEL='owner',
    JOB_CPU_RANGE_EVENTS=('create','update','start','die','destroy'))
names={'Refusal','JobCpuRanges','job_cpu_ranges','slot_cpu_base','container_cpuset','cpu_range_overlaps'}
nodes=[x for x in ast.parse(source).body if isinstance(x,(ast.FunctionDef,ast.ClassDef)) and x.name in names]
assert {x.name for x in nodes}==names
unit=ast.Module(body=[ast.ImportFrom(module='__future__',names=[ast.alias(name='annotations')],level=0),*nodes],type_ignores=[])
exec(compile(ast.fix_missing_locations(unit),'selected-allocation-definitions','exec'),m.__dict__)
print('source_sha256='+hashlib.sha256(source.encode()).hexdigest())
token='1'*32
boundary=SimpleNamespace(token=token)

def line(action,cid):
    return json.dumps({'Type':'container','Action':action,'Actor':{'ID':cid,'Attributes':{'owner':token}}})

class Daemon:
    def __init__(self, seed, mode):
        self.rng=random.Random(seed)
        self.mode=mode
        self.config={}
        self.pending={}
        self.queue=[]
        self.serial=0
        self.record=m.JobCpuRanges(boundary,('4-7','8-11','12-15','16-19'),self.assign,self.read)
    def assign(self,cid,target):
        if cid not in self.config:
            return subprocess.CompletedProcess([],1,'','No such container')
        if self.mode in ('late','unreadable') and int(cid,16)%3==0:
            self.pending[cid]=target
            raise m.Refusal('move timed out')
        self.config[cid]=target
        self.queue.append(('update',cid))
        if self.mode=='applied-timeout' and int(cid,16)%3==0:
            raise m.Refusal('response lost after application')
        return subprocess.CompletedProcess([],0,'','')
    def read(self,cid):
        if cid in self.config:
            if self.mode=='unreadable' and int(cid,16)%3==0:
                raise m.Refusal('inspect timed out')
            return subprocess.CompletedProcess([],0,self.config[cid],'')
        return subprocess.CompletedProcess([],1,'','No such container')
    def check(self):
        allocations=[(cid,cpu) for cid,cpu in self.config.items() if cpu in self.record.ranges]
        assert not m.cpu_range_overlaps(allocations), allocations
        for cid,target in [*self.config.items(),*self.pending.items()]:
            if target in self.record.ranges:
                assert cid in self.record.held, (cid,target,self.record.held)
                assert self.record.ranges[self.record.held[cid]]==target
    def step(self):
        # The daemon changes before an event is consumed. Events can be delayed,
        # duplicated or delivered out of order. IDs are never reused.
        choice=self.rng.randrange(6)
        if choice==0 and len(self.config)<4:
            self.serial+=1
            cid=f'{self.serial:064x}'
            self.config[cid]='0-3'
            self.queue.extend([('create',cid),('start',cid)])
        elif choice in (1,2) and self.config:
            cid=self.rng.choice(list(self.config))
            self.queue.append(('die' if choice==1 else 'start',cid))
        elif choice==3 and self.config:
            cid=self.rng.choice(list(self.config))
            del self.config[cid]
            self.pending.pop(cid,None)
            if self.rng.randrange(3):
                self.queue.append(('destroy',cid))
        elif choice==4 and self.pending:
            cid=self.rng.choice(list(self.pending))
            self.config[cid]=self.pending.pop(cid)
            self.queue.append(('update',cid))
        elif self.queue:
            i=self.rng.randrange(len(self.queue))
            event=self.queue.pop(i)
            self.record.observe(line(*event))
            if self.rng.randrange(8)==0:
                self.record.observe(line(*event))
        self.check()

for mode in ('ordinary','applied-timeout','late','unreadable'):
    for seed in range(64):
        daemon=Daemon(seed,mode)
        for _ in range(300):daemon.step()
    print('PASS',mode,': 64 seeds x 300 daemon/event transitions; reservations cover configured and pending job ranges')
for cpus in (1,3,4,7,8,19,20,21,39,40,128):
    m.os.cpu_count=lambda:cpus
    for slot in (0,1,3,6):
        for width in (1,4):
            expected=cpus>=20*slot+4*(width+1)
            try:
                ranges=m.job_cpu_ranges(slot,width)
                assert expected,(cpus,slot,width,ranges)
                assert len(ranges)==width
            except m.Refusal:
                assert not expected,(cpus,slot,width)
print('PASS capacity: 88 combinations, exact boundary and insufficient-capacity refusals')
print('PASS: all inert allocation probes')
