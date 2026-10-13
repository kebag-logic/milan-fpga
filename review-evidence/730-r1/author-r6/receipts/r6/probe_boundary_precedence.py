#!/usr/bin/env python3
"""Inert collaborators, real monitor and act boundary; signal at the boundary mask restoration."""
import ast,contextlib,importlib.util,io,json,signal,subprocess,sys,threading
from pathlib import Path
from unittest import mock
root=Path(sys.argv[1]).resolve();source=root/'scripts/act_ci.py'
spec=importlib.util.spec_from_file_location('review_boundary',source)
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
fn=next(n for n in ast.parse(source.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='execute_act_boundary')
entry=next(n for n in fn.body if isinstance(n,ast.Try) and n.finalbody).finalbody[0].lineno
monitor=next(n for n in ast.parse(source.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='job_cpu_range_monitor')
monitor_entry=next(n for n in monitor.body if isinstance(n,ast.Try) and n.finalbody).finalbody[0].lineno
rows=[]
for signum in m.CLEANUP_SIGNALS:
 for inject in ('none','boundary_restore','monitor_cleanup'):
  fixture=m.selftest_fixture();run=m.ValidatedRun(fixture.pr,fixture.repository,fixture.base)
  trail=[];contained=threading.Event();reader_started=threading.Event();reader_finished=threading.Event()
  earlier=m.Refusal('original integrity failure')
  class Pipe:
   closed=False
   def __iter__(self):
    reader_started.set()
    assert contained.wait(5)
    reader_finished.set();trail.append('reader ended')
    return iter(())
   def close(self): self.closed=True;trail.append('pipe closed')
  pipe=Pipe();proc=type('Stream',(),{'pid':424242,'stdout':pipe,'poll':lambda self:None,'returncode':None})()
  def contain(*a,**k):trail.append('contained');contained.set()
  def fail():
   assert reader_started.wait(5)
   trail.append('original failure raised')
   raise earlier
  fired=[]
  def trace(frame,event,arg):
   if not fired and event=='line' and ((inject=='boundary_restore' and frame.f_code.co_name=='execute_act_boundary' and frame.f_lineno==entry) or (inject=='monitor_cleanup' and frame.f_code.co_name=='job_cpu_range_monitor' and frame.f_lineno==monitor_entry)):
    fired.append({'active_exception':str(sys.exception()),'mask_before_signal':sorted(int(s) for s in signal.pthread_sigmask(signal.SIG_BLOCK,()))})
    trail.append('signal at '+inject)
    signal.raise_signal(signum)
   return trace
  outcome={};diagnostic=io.StringIO();incoming=signal.pthread_sigmask(signal.SIG_BLOCK,())
  def action():
   try:
    with m.job_cpu_range_monitor(type('Boundary',(),{'token':'1'*32})(),('4-7',),
     context=m.CommandContext(False,root,{}),seams=m.ProcessSeams(popen=lambda *a,**k:proc,terminate_group=contain)):
     m.execute_act_boundary(['INERT'],run=run,context=m.CommandContext(False,root,{}),integrity_check=fail,
      seams=m.SpawnSeams(query=lambda *a:fixture.pr,run_process=lambda *a,**k:subprocess.CompletedProcess([],0)))
   finally:
    outcome.update(contained=contained.is_set(),reader_finished=reader_finished.is_set(),pipe_closed=pipe.closed)
    trail.append('outer teardown')
   return 0
  with mock.patch.object(m,'require_tool',m.fake_host_tool),contextlib.redirect_stderr(diagnostic):
   try:
    sys.settrace(trace)
    try: outcome['rc']=m.run_with_cleanup_signals(action)
    except BaseException as e:
     outcome.update(raised=type(e).__name__,message=str(e),original_preserved=e is earlier)
     if isinstance(e,m.Refusal):
      outcome['rc']=m.RC_REFUSED
      print(f'act-ci: REFUSED: {e}',file=sys.stderr)
   finally:
    sys.settrace(None);contained.set();signal.pthread_sigmask(signal.SIG_SETMASK,incoming)
  rows.append({'signal':signal.Signals(signum).name,'inject':inject,'line':monitor_entry if inject=='monitor_cleanup' else entry,'fired':fired,'outcome':outcome,'diagnostic':diagnostic.getvalue(),'trail':trail})
print(json.dumps(rows,indent=2))
sys.exit(0 if all(r['outcome'].get('original_preserved',False) for r in rows) else 1)
