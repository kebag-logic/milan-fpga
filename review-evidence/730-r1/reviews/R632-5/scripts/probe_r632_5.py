"""R632-5 independent probe of the CPU-range monitor's signal mask (#730, PR #731).

Usage (inside scripts/sandbox.sh only; no network, no Docker socket):
    python3 -I probe_r632_5.py <tree-root> record
    python3 -I probe_r632_5.py <tree-root> masks
    python3 -I probe_r632_5.py <tree-root> sweep <shard> <shards> <steps.json>
    python3 -I probe_r632_5.py <tree-root> precedence
    python3 -I probe_r632_5.py <tree-root> realrace

The real job_cpu_range_monitor, execute_act_boundary, run_act_process,
terminate_act_process_group and run_with_cleanup_signals run. Only the Docker
CLI (run_docker), the live-PR query and the integrity check are stood in. The
event stream is a real child in its own session that prints one owned
``create`` line, then sleeps; "act" is a real child that records its own
signal mask, then sleeps briefly. Nothing reaches a daemon.

`masks`: the blocked sets of the main thread, the reader thread, the event
stream child and the act child, read from /proc, at each phase.
`record`: the distinct traced steps (file:function:line) from just before the
monitor is entered until it has exited, in a run with no signal.
`precedence`: the act boundary's closing integrity check raises a Refusal
(rc 2 when nothing else happens). From that raise until the monitor has
exited, a first cleanup signal is sent at each traced step, to the main
thread and to the whole process. Each run records whether the Refusal or the
signal decided the exit, and whether containment, the reader's end and the
pipe close still held. This mode reports; it asserts only containment.
`realrace`: no tracer. The closing integrity check fails inside one long C
call (str.index over 400 MB), and a helper thread with the cleanup signals
blocked sends SIGTERM to the main thread while that call runs, so the C-level
handler trips with no Python checkpoint before the boundary's restoring
call. Records the exit and the main thread's mask when the monitor's cleanup
starts, which shows whether the boundary's restore ran before the handler.
`sweep`: for each step of this shard, a first cleanup signal sent there, to
the main thread and to the whole process. Each run must exit 128 + signal
with the interrupt diagnostic; at the monitor's exit the stream must be
contained, the reader ended and the pipe closed (if the stream had started);
and no cleanup signal may stay blocked or pending.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import pathlib
import signal
import subprocess
import sys
import threading
import time
from types import SimpleNamespace
from unittest import mock

ROOT = pathlib.Path(sys.argv[1]).resolve()
MODE = sys.argv[2]
SOURCE = ROOT / "scripts" / "act_ci.py"
spec = importlib.util.spec_from_file_location("act_ci_probe", SOURCE)
m = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["act_ci_probe"] = m
spec.loader.exec_module(m)

CLEAN = set(m.CLEANUP_SIGNALS)
BITS = 0
for _s in m.CLEANUP_SIGNALS:
    BITS |= 1 << (int(_s) - 1)
TOKEN = "t" * 32
CID = "a" * 64
SCRATCH = pathlib.Path(os.environ.get("TMPDIR", "/tmp")) / f"probe-r632-5-{os.getpid()}"
SCRATCH.mkdir(parents=True, exist_ok=True)


def sigblk(path: str) -> int:
    for line in pathlib.Path(path).read_text().splitlines():
        if line.startswith("SigBlk:"):
            return int(line.split()[1], 16)
    raise RuntimeError("no SigBlk")


def thread_blocked(ident_native: int) -> bool:
    return sigblk(f"/proc/self/task/{ident_native}/status") & BITS == BITS


def child_script(kind: str, out: pathlib.Path) -> list[str]:
    record = (
        "import pathlib,time,sys\n"
        "s=pathlib.Path('/proc/self/status').read_text()\n"
        "b=[l.split()[1] for l in s.splitlines() if l.startswith('SigBlk:')][0]\n"
        f"pathlib.Path({str(out)!r}).write_text(b)\n"
    )
    if kind == "stream":
        line = json.dumps({"Type": "container", "Action": "create",
                           "Actor": {"ID": CID, "Attributes": {m.DOCKER_OWNER_LABEL: TOKEN}}})
        body = f"sys.stdout.write({line!r}+'\\n');sys.stdout.flush()\ntime.sleep(60)\n"
    else:
        body = "time.sleep(0.2)\n"
    return [sys.executable, "-I", "-c", record + body]


class World:
    """One run's collaborators and observations."""

    def __init__(self) -> None:
        self.stream: subprocess.Popen | None = None
        self.reader: threading.Thread | None = None
        self.moves: list[str] = []
        self.phase_masks: dict[str, object] = {}
        self.at_exit: dict[str, object] = {}
        self.fail_integrity = False
        self.real_race = False
        self.stop_entry_blocked: bool | None = None
        self.integrity_calls = 0
        self.raised = False
        self.stream_mask = SCRATCH / "stream.mask"
        self.act_mask = SCRATCH / "act.mask"
        for p in (self.stream_mask, self.act_mask):
            p.unlink(missing_ok=True)

    def popen(self, _command, **kwargs):
        self.stream = subprocess.Popen(child_script("stream", self.stream_mask), **kwargs)
        return self.stream

    def run_docker(self, arguments, **_kwargs):
        if arguments[:2] == ["container", "update"]:
            time.sleep(0.2)  # a move in flight when the body ends
            self.moves.append(arguments[2])
            return subprocess.CompletedProcess(arguments, 0, "", "")
        if arguments[:2] == ["container", "inspect"]:
            cpus = self.moves[-1].split("=", 1)[1] if self.moves else "0-3"
            return subprocess.CompletedProcess(arguments, 0, cpus + "\n", "")
        raise AssertionError(f"unexpected docker call {arguments}")

    def find_reader(self) -> threading.Thread | None:
        for each in threading.enumerate():
            if each.name == "act-ci-cpu-range-monitor":
                self.reader = each
        return self.reader

    def masks(self, phase: str) -> None:
        reader = self.find_reader()
        self.phase_masks[phase] = {
            "main_blocked": thread_blocked(threading.main_thread().native_id),
            "reader_blocked": None if reader is None or not reader.is_alive()
            else thread_blocked(reader.native_id),
        }


def integrity(world: World) -> None:
    """The boundary's integrity check: the second (post-act) call fails when asked to."""
    world.integrity_calls += 1
    if world.fail_integrity and world.integrity_calls == 2:
        world.raised = True
        raise m.Refusal("original integrity failure")
    if world.real_race and world.integrity_calls == 2:
        haystack = "a" * 400_000_000
        main_ident = threading.main_thread().ident

        def send() -> None:
            time.sleep(0.02)
            signal.pthread_kill(main_ident, signal.SIGTERM)

        helper = threading.Thread(target=send, daemon=True)
        m.start_cleanup_safe_thread(helper)
        haystack.index("ab")  # a C-level ValueError after the signal has tripped


def act_process(world: World):
    def run(command, **kwargs):
        world.masks("act window")
        return m.run_act_process(child_script("act", world.act_mask), **kwargs)
    return run


def one_run(world: World, tracer=None) -> tuple[int, str]:
    context = m.CommandContext(use_sudo=False, cwd=ROOT, env={"PATH": "/usr/bin"})
    boundary = SimpleNamespace(token=TOKEN)
    fake_run = SimpleNamespace(pr=SimpleNamespace(number=1), repository="o/r")

    def action() -> int:
        try:
            if tracer is not None:
                sys.settrace(tracer)
            with m.job_cpu_range_monitor(
                boundary, ("4-7",), context=context, seams=m.ProcessSeams(popen=world.popen)
            ) as record:
                world.masks("body before act")
                time.sleep(0.05)  # let the reader take the create and start its move
                m.execute_act_boundary(
                    ["act"], run=fake_run, context=context, integrity_check=lambda: integrity(world),
                    seams=m.SpawnSeams(query=lambda *_a: None, run_process=act_process(world)),
                )
                world.masks("body after act")
        finally:
            sys.settrace(None)
            s = world.stream
            r = world.find_reader()
            world.at_exit = {
                "stream_started": s is not None,
                "stream_contained": s is None or s.poll() is not None,
                "pipe_closed": s is None or s.stdout is None or s.stdout.closed,
                "reader_alive": bool(r is not None and r.is_alive()),
                "blocked_now": sorted(int(x) for x in CLEAN & signal.pthread_sigmask(signal.SIG_BLOCK, ())),
            }
        return 0

    original_stop = m.stop_job_cpu_range_monitor

    def stop_spy(*args, **kwargs):
        world.stop_entry_blocked = CLEAN <= signal.pthread_sigmask(signal.SIG_BLOCK, ())
        return original_stop(*args, **kwargs)

    err = io.StringIO()
    with mock.patch.multiple(m, run_docker=world.run_docker, stop_job_cpu_range_monitor=stop_spy,
                             require_live_pull_request=lambda *_a, **_k: None), \
            contextlib.redirect_stderr(err):
        try:
            rc = m.run_with_cleanup_signals(action)
        except m.Refusal as exc:
            rc = 2
            print(f"act-ci: REFUSED: {exc}", file=err)
    # Anything left pending or blocked is a failure; consume it so the next run starts clean.
    signal.pthread_sigmask(signal.SIG_BLOCK, m.CLEANUP_SIGNALS)
    pending = sorted(int(x) for x in CLEAN & signal.sigpending())
    while signal.sigtimedwait(m.CLEANUP_SIGNALS, 0) is not None:
        pass
    signal.pthread_sigmask(signal.SIG_SETMASK, [])
    for item in m.CLEANUP_SIGNALS:
        signal.signal(item, signal.SIG_DFL if item != signal.SIGINT else signal.default_int_handler)
    if world.stream is not None and world.stream.poll() is None:
        world.stream.kill()
        world.stream.wait()
    world.at_exit["pending_after"] = pending
    return rc, err.getvalue()


def watched(frame) -> str | None:
    name = frame.f_code.co_filename
    if name == str(SOURCE) or name.endswith("contextlib.py"):
        return f"{pathlib.Path(name).name}:{frame.f_code.co_name}:{frame.f_lineno}"
    return None


class Recorder:
    def __init__(self, gate=None) -> None:
        self.steps: list[str] = []
        self.gate = gate

    def __call__(self, frame, event, arg):
        if threading.current_thread() is not threading.main_thread():
            return None
        if self.gate is not None and not self.gate():
            return self
        if event == "line":
            label = watched(frame)
            if label is not None and label not in self.steps:
                self.steps.append(label)
        return self


class Injector:
    def __init__(self, target: str, signum: int, process_wide: bool, gate=None) -> None:
        self.target, self.signum, self.process_wide = target, signum, process_wide
        self.sent = False
        self.gate = gate

    def __call__(self, frame, event, arg):
        if self.sent or threading.current_thread() is not threading.main_thread():
            return None
        if self.gate is not None and not self.gate():
            return self
        if event == "line" and watched(frame) == self.target:
            self.sent = True
            if self.process_wide:
                os.kill(os.getpid(), self.signum)
            else:
                signal.pthread_kill(threading.main_thread().ident, self.signum)
            return None
        return self


def main() -> int:
    if MODE == "masks":
        world = World()
        rc, err = one_run(world)
        stream_mask = int(world.stream_mask.read_text(), 16)
        act_mask = int(world.act_mask.read_text(), 16)
        result = {
            "rc": rc, "stderr": err, "phases": world.phase_masks, "at_exit": world.at_exit,
            "moves": world.moves,
            "stream_child_blocks_cleanup": bool(stream_mask & BITS),
            "act_child_blocks_cleanup": bool(act_mask & BITS),
        }
        print(json.dumps(result, indent=1))
        ok = (
            rc == 0
            and world.phase_masks["body before act"] == {"main_blocked": True, "reader_blocked": True}
            and world.phase_masks["act window"]["main_blocked"] is False
            and world.phase_masks["act window"]["reader_blocked"] in (True, None)
            and world.phase_masks["body after act"]["main_blocked"] is True
            and not result["stream_child_blocks_cleanup"]
            and not result["act_child_blocks_cleanup"]
            and world.at_exit["stream_contained"] and world.at_exit["pipe_closed"]
            and not world.at_exit["reader_alive"] and world.at_exit["blocked_now"] == []
            and world.at_exit["pending_after"] == []
        )
        print("masks:", "PASS" if ok else "FAIL")
        return 0 if ok else 1
    if MODE == "record":
        recorder = Recorder()
        rc, err = one_run(World(), recorder)
        print(json.dumps({"rc": rc, "stderr": err, "steps": recorder.steps}, indent=1))
        return 0 if rc == 0 else 1
    if MODE == "realrace":
        results = []
        for attempt in range(5):
            world = World()
            world.real_race = True
            rc, err = one_run(world)
            results.append({"rc": rc, "stderr": err.strip().splitlines(),
                            "mask_held_at_cleanup_entry": world.stop_entry_blocked,
                            "at_exit": world.at_exit})
            print(json.dumps(results[-1]))
        contained = all(r["at_exit"]["stream_contained"] and r["at_exit"]["pipe_closed"]
                        and not r["at_exit"]["reader_alive"] for r in results)
        print(f"realrace: exits {[r['rc'] for r in results]}, mask held at cleanup entry "
              f"{[r['mask_held_at_cleanup_entry'] for r in results]}, contained {contained}")
        return 0 if contained else 1
    if MODE == "precedence":
        control = World()
        control.fail_integrity = True
        recorder = Recorder(lambda: control.raised)
        rc, err = one_run(control, recorder)
        print(json.dumps({"control_rc": rc, "control_stderr": err.strip().splitlines(),
                          "control_at_exit": control.at_exit, "steps": recorder.steps}))
        contained_everywhere = rc == 2 and control.at_exit["stream_contained"]
        flipped = []
        for index, step in enumerate(recorder.steps):
            signum = m.CLEANUP_SIGNALS[index % len(m.CLEANUP_SIGNALS)]
            for process_wide in (False, True):
                world = World()
                world.fail_integrity = True
                injector = Injector(step, signum, process_wide, lambda w=world: w.raised)
                rc, err = one_run(world, injector)
                e = world.at_exit
                kept = rc == 2 and "original integrity failure" in err
                contained = e["stream_contained"] and e["pipe_closed"] and not e["reader_alive"] \
                    and e["blocked_now"] == [] and e["pending_after"] == []
                contained_everywhere &= contained
                if not kept:
                    flipped.append(step)
                print(json.dumps({"step": step, "signal": signal.Signals(signum).name,
                                  "process_wide": process_wide, "sent": injector.sent, "rc": rc,
                                  "refusal_kept": kept, "contained": contained,
                                  "stderr": err.strip().splitlines()}))
        print(f"precedence: steps {len(recorder.steps)}, runs {2 * len(recorder.steps)}, "
              f"refusal replaced at {sorted(set(flipped))}, containment held in every run: "
              f"{contained_everywhere}")
        return 0 if contained_everywhere else 1
    shard, shards = int(sys.argv[3]), int(sys.argv[4])
    steps = json.loads(pathlib.Path(sys.argv[5]).read_text())["steps"]
    failures = 0
    runs = 0
    for index, step in enumerate(steps):
        if index % shards != shard:
            continue
        signum = m.CLEANUP_SIGNALS[index % len(m.CLEANUP_SIGNALS)]
        for process_wide in (False, True):
            world = World()
            injector = Injector(step, signum, process_wide)
            rc, err = one_run(world, injector)
            runs += 1
            name = signal.Signals(signum).name
            e = world.at_exit
            ok = (
                injector.sent
                and rc == 128 + signum
                and f"act-ci: interrupted by {name} after cleanup" in err
                and e["stream_contained"] and e["pipe_closed"] and not e["reader_alive"]
                and e["blocked_now"] == [] and e["pending_after"] == []
            )
            if not ok:
                failures += 1
            print(json.dumps({"step": step, "signal": name, "process_wide": process_wide,
                              "sent": injector.sent, "rc": rc, "at_exit": e,
                              "stderr": err.strip().splitlines()[-3:], "ok": ok}))
    print(f"shard {shard}/{shards}: runs {runs}, failures {failures}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
