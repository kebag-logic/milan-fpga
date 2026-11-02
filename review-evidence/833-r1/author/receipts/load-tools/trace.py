from pathlib import Path
import sys
p = Path(sys.argv[1]) / "scripts/owned_process.py"
t = p.read_text()
# One JSON document per cleanup; each pass carries every descendant's state. Scratch only.
t = t.replace('''        while True:
            pass_started = time.monotonic()
            self._reap()
            owned = self._descendants()
            passes += 1
            if not owned:
                return
''', '''        trace = dict(owner=os.getpid(), root=self.process.pid if self.process is not None else None, notified=self.root_notified, sent=[], passes=[], load=(PROC / "loadavg").read_text().split()[0])
        def flush(outcome):
            import json
            target = os.environ.get("OWNED_TRACE")
            if target:
                trace.update(outcome=outcome, elapsed=round(time.monotonic() - started, 3), resumed=None if resumed is None else round(resumed - started, 3))
                with open(target, "a") as f:
                    f.write(json.dumps(trace) + "\\n")
        def states(pids):
            out = {}
            for p in pids:
                try:
                    s = (PROC / str(p) / "stat").read_text()
                    w = "?"
                    try: w = (PROC / str(p) / "wchan").read_text().strip()
                    except OSError: pass
                    r = s.rsplit(")", 1)[1].split()
                    out[str(p)] = [s[s.index("(")+1:s.rindex(")")], r[0], int(r[1]), w]
                except OSError:
                    out[str(p)] = None
            return out
        while True:
            pass_started = time.monotonic()
            self._reap()
            owned = self._descendants()
            passes += 1
            trace["passes"].append([round(pass_started - started, 3), round(time.monotonic() - pass_started, 3), states(owned)])
            if not owned:
                flush("clean")
                return
''')
t = t.replace('''                first = dict(initial)
                remaining = "; ".join(''', '''                flush("FAILED")
                first = dict(initial)
                remaining = "; ".join(''')
t = t.replace('''                        notified.add(key)
                        if signum == signal.SIGKILL:''', '''                        notified.add(key)
                        trace["sent"].append([round(time.monotonic() - started, 3), pid, int(signum)])
                        if signum == signal.SIGKILL:''')
t = t.replace('''                self._signal(self.root_fd, signal.SIGCONT)
                resumed = now
''', '''                self._signal(self.root_fd, signal.SIGCONT)
                resumed = now
                trace["sent"].append([round(time.monotonic() - started, 3), self.process.pid, "RESUME"])
''')
p.write_text(t)
