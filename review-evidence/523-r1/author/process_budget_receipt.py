"""Measure bounded actual sweep cleanup after explicit command readiness."""
import signal,sys,tempfile,time
from pathlib import Path
sys.path.insert(0,"scripts")
from test_suite_cancellation import fixture,start
from process_test_support import assert_reaped,identity
from owned_process import OwnedProcesses
with tempfile.TemporaryDirectory() as scratch, OwnedProcesses():
    for signum in (signal.SIGINT,signal.SIGTERM):
        root,probe=fixture(Path(scratch),"bounded-"+signum.name)
        probe.env["PROBE_MODE"]="command"
        start(probe);data=probe.ready()
        began=time.monotonic();probe.signal(signum);code,output=probe.finish();elapsed=time.monotonic()-began
        assert code==128+signum and elapsed<5.5,(code,elapsed,output)
        assert_reaped(data)
        after={pid:identity(int(pid)) for pid in data["identities"]}
        probe.save(dict(exit=code,signal=signum.name,cleanup_seconds=elapsed,
                        before=data["identities"],after=after,
                        next_suite=(probe.control/"next-suite").exists(),
                        completed_summary="\nsuites:" in output))
