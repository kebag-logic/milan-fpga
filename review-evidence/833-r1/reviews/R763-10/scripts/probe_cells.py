"""Reviewer cell probe for #833 cleanup timing: every resume class x new-descendant liveness x shell.

Usage: python3 -I probe_cells.py <tree>   (tree holds scripts/owned_process.py)
Runs OwnedProcesses._cleanup over fake listings on a dense, explicit pass schedule (every key time, a tick
before and after it, and a 0.25 s grid), with expectations written from the stated rows of the cleanup
table in docs/testing/TESTING.md, not from the product. Prints one line per failing cell; rc 1 if any.
"""
import os
import signal
import subprocess
import sys
from types import SimpleNamespace

sys.path.insert(0, os.path.join(sys.argv[1], "scripts"))
import owned_process  # noqa: E402

T = 2.0 ** -20
INF = float("inf")
FAKE = iter(range(2 ** 22 + 100, 2 ** 22 + 200))


def schedule(keys):
    times = {0.0}
    for k in keys:
        if k != INF:
            times |= {k - T, k, k + T, k - 2 * T}
    times |= {i * 0.25 for i in range(0, 4 * 80)}
    return sorted(t for t in times if t >= 0)


def run(listing, keys, root):
    passes = schedule(keys)
    it = iter(passes[1:])
    clock = [0.0]
    events = []
    names = {}

    def pause(_s):
        clock[0] = next(it)

    def census():
        return listing(clock[0])

    def send(pid, _start, signum):
        events.append((clock[0], signal.Signals(signum).name, pid))
        return True

    owner = owned_process.OwnedProcesses()
    owner.process = SimpleNamespace(pid=root) if root else None
    owner.root_notified = bool(root)
    owner.root_fd = None
    real = owned_process.time
    owned_process.time = SimpleNamespace(monotonic=lambda: clock[0], sleep=pause)
    owner._descendants, owner._reap, owner._send = census, lambda: set(), send
    owner._signal = lambda _fd, signum: events.append((clock[0], signal.Signals(signum).name, root))
    try:
        owner._cleanup()
        events.append((clock[0], "no verdict", 0))
    except RuntimeError:
        events.append((clock[0], "verdict", 0))
    except StopIteration:
        events.append((clock[0], "schedule exhausted", 0))
    finally:
        owned_process.time = real
    del names
    return events


def norm(events):
    return sorted(events, key=lambda e: (e[0], e[1] == "verdict", repr(e)))


def main():
    cats = [subprocess.Popen(["cat"], stdin=subprocess.PIPE) for _ in range(3)]
    LIVE_C, LIVE_N, LIVE_S = (c.pid for c in cats)
    SHELL, OWNER, FAKE_N, FAKE_S = (next(FAKE) for _ in range(4))
    failures = []

    def check(name, listing, keys, expected, root):
        got = norm(run(listing, keys, root))
        want = norm(expected)
        if got != want:
            failures.append(f"CELL {name}: got {got} want {want}")

    resumes = [("first", 0.0), ("second", T), ("half", 0.5), ("one", 1.0), ("one-half", 1.5),
               ("next-to-last-in-grace", 2 - 2 * T), ("last-in-grace", 2 - T), ("first-past", 2.0),
               ("second-past", 2 + T), ("two-half", 2.5), ("three", 3.0), ("four-tick", 4 - T), ("four", 4.0),
               ("five-half", 5.5), ("ten", 10.0), ("last-pass", 14 - T)]
    kinds = [("none", None), ("fake", FAKE_N), ("live", LIVE_N)]
    for rname, r in resumes:
        for kname, n in kinds:
            def listing(clock, r=r, n=n):
                d = {SHELL: (OWNER, "2")}
                if clock < r:
                    d[LIVE_C] = (SHELL, "4")
                if n is not None and clock > r:
                    d[n] = (SHELL, "3")
                return d
            win = [SHELL] + ([n] if n else [])
            exp = ([(0.0, "SIGTERM", LIVE_C)] if r > 0 else []) + ([(2.0, "SIGKILL", LIVE_C)] if r > 2 else [])
            exp += [(r, "SIGCONT", SHELL)] + [(r + 10, "SIGKILL", p) for p in win]
            exp += [(r + 20, "SIGKILL", p) for p in win] + [(r + 20, "verdict", 0)]
            check(f"shell resume={rname} new={kname}", listing, [r, r + 10, r + 20, 2, 4, 14], exp, SHELL)
    # Never resumed: the child stays; its trap's command, new, is listed from pass 2.
    for kname, n in kinds:
        def listing(clock, n=n):
            d = {SHELL: (OWNER, "2"), LIVE_C: (SHELL, "4")}
            if n is not None and clock > 0:
                d[n] = (LIVE_C, "7")
            return d
        exp = [(0.0, "SIGTERM", LIVE_C)]
        if n == LIVE_N:
            exp += [(2.0, "SIGKILL", n), (4.0, "SIGKILL", LIVE_C)]
        else:
            exp += [(2.0, "SIGKILL", LIVE_C)] + ([(2.0, "SIGKILL", n)] if n else [])
        exp += [(14.0, "SIGKILL", p) for p in [SHELL, LIVE_C] + ([n] if n else [])] + [(14.0, "verdict", 0)]
        check(f"shell never new={kname}", listing, [2, 4, 14], exp, SHELL)
    # A live new descendant beside a stopped shell, the child gone after pass 1; the shell resumes once it is gone.
    for gname, g in [("1", 1.0), ("2-tick", 2 - T), ("2", 2.0), ("3", 3.0), ("4", 4.0), ("5.5", 5.5),
                     ("last-pass", 14 - T)]:
        def listing(clock, g=g):
            d = {SHELL: (OWNER, "2")}
            if not clock:
                d[LIVE_C] = (SHELL, "4")
            if 0 < clock < g:
                d[LIVE_N] = (SHELL, "8")
            return d
        exp = [(0.0, "SIGTERM", LIVE_C)] + ([(2.0, "SIGKILL", LIVE_N)] if g > 2 else [])
        exp += [(g, "SIGCONT", SHELL), (g + 10, "SIGKILL", SHELL), (g + 20, "SIGKILL", SHELL), (g + 20, "verdict", 0)]
        check(f"shell live-new-holds gone={gname}", listing, [g, g + 10, g + 20, 2, 4, 14], exp, SHELL)
    # A live new descendant beside a stopped shell that never goes: the shell is never resumed.
    def listing(clock):
        d = {SHELL: (OWNER, "2")}
        if not clock:
            d[LIVE_C] = (SHELL, "4")
        else:
            d[LIVE_N] = (SHELL, "8")
        return d
    check("shell live-new-holds gone=never", listing, [2, 4, 14],
          [(0.0, "SIGTERM", LIVE_C), (2.0, "SIGKILL", LIVE_N), (14.0, "SIGKILL", SHELL), (14.0, "SIGKILL", LIVE_N),
           (14.0, "verdict", 0)], SHELL)
    # No cancelled shell: a survivor leaf from the first census, its new child listed from pass 2.
    for sname, s in [("live", LIVE_S), ("fake", FAKE_S)]:
        for kname, n in kinds:
            def listing(clock, s=s, n=n):
                d = {s: (OWNER, "1")}
                if n is not None and clock > 0:
                    d[n] = (s, "9")
                return d
            exp = [(0.0, "SIGTERM", s)]
            if n == LIVE_N:
                exp += [(2.0, "SIGKILL", n), (4.0, "SIGKILL", s)]
            else:
                exp += [(2.0, "SIGKILL", s)] + ([(2.0, "SIGKILL", n)] if n else [])
            exp += [(14.0, "SIGKILL", p) for p in [s] + ([n] if n else [])] + [(14.0, "verdict", 0)]
            check(f"noshell survivor={sname} new={kname}", listing, [2, 4, 14], exp, None)
    for c in cats:
        c.stdin.close()
        c.wait()
    for line in failures:
        print(line[:600])
    total = len(resumes) * 3 + 3 + 7 + 1 + 6
    print(f"probe_cells: {'FAIL' if failures else 'PASS'} {len(failures)} of {total} cells failed")
    return 1 if failures else 0


sys.exit(main())
