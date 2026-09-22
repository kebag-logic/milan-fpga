
import fcntl, json, os, resource, signal, subprocess, sys

FRAME_VAR = "MILAN_COUNTER_FRAME_OUT"


def record(path, **fields):
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        os.write(fd, (json.dumps(fields) + "\n").encode())
    finally:
        os.close(fd)


def live_children(ppid):
    """Children of `ppid` that are not zombies, read from /proc."""
    alive = 0
    for entry in os.listdir("/proc"):
        if not entry.isdigit():
            continue
        try:
            with open("/proc/" + entry + "/stat", "rb") as fh:
                raw = fh.read()
        except OSError:
            continue
        fields = raw[raw.rfind(b")") + 2:].split()
        if int(fields[1]) == ppid and fields[0] != b"Z":
            alive += 1
    return alive


def status(name):
    with open("/proc/self/status") as fh:
        for line in fh:
            if line.startswith(name + ":"):
                return line.split()[1]
    return None


def hold(path):
    """Block until the arm writes a byte or lets go of the FIFO."""
    fd = os.open(path, os.O_RDONLY)
    try:
        os.read(fd, 1)
    finally:
        os.close(fd)


def write_chunks(chunks):
    for stream, text in chunks:
        os.write(1 if stream == "out" else 2, text.encode("latin-1"))


def main(cfg):
    name = cfg["name"]
    ppid = os.getppid()
    siblings = live_children(ppid)
    descendant = None
    if cfg.get("descendant_hold"):
        ready_read, ready_write = os.pipe()
        code = ("import os, sys, json\n"
                "os.write(int(sys.argv[3]), b'r')\n"
                "os.close(int(sys.argv[3]))\n"
                "fd = os.open(sys.argv[1], os.O_RDONLY)\n"
                "os.read(fd, 1)\n"
                "out = os.open(sys.argv[2], os.O_WRONLY | os.O_APPEND)\n"
                "os.write(out, (json.dumps({'event': 'survived', 'pid': os.getpid()})"
                " + chr(10)).encode())\n")
        descendant = subprocess.Popen([sys.executable, "-S", "-c", code,
                                       cfg["descendant_hold"], cfg["ledger"], str(ready_write)],
                                      pass_fds=(ready_write,),
                                      start_new_session=cfg.get("descendant_session", False)).pid
        os.close(ready_write)
        assert os.read(ready_read, 1) == b'r'
        os.close(ready_read)
    environ = dict(os.environ)
    record(cfg["ledger"], event="start", leg=name, pid=os.getpid(), ppid=ppid,
           argv=sys.argv, cwd=os.getcwd(), stdin=os.readlink("/proc/self/fd/0"),
           sid=os.getsid(0), pgid=os.getpgid(0), siblings=siblings,
           sigblk=status("SigBlk"), sigign=status("SigIgn"), environ=environ,
           descendant=descendant)
    shared = None
    if cfg.get("shared"):
        shared = os.open(cfg["shared"], os.O_WRONLY | os.O_CREAT, 0o644)
        try:
            fcntl.flock(shared, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            record(cfg["ledger"], event="contention", leg=name)
            cfg["exit"] = 4
    write_chunks(cfg.get("out", []))
    fd = os.open(cfg["announce"], os.O_WRONLY)
    os.write(fd, (json.dumps({"leg": name, "pid": os.getpid(), "holds": bool(cfg.get("hold")),
                              "descendant": descendant}) + "\n").encode())
    os.close(fd)
    if cfg.get("hold"):
        hold(cfg["hold"])
        record(cfg["ledger"], event="survived" if cfg.get("killed") else "released",
               leg=name, pid=os.getpid())
    if cfg.get("dump") and FRAME_VAR in os.environ:
        try:
            with open(os.environ[FRAME_VAR], "wb") as dump:
                dump.write(name.encode())
        except OSError:
            write_chunks([["out", "  [FAIL] optional reference frame dump\n"]])
            record(cfg["ledger"], event="end", leg=name)
            sys.exit(1)
    write_chunks(cfg.get("after", []))
    record(cfg["ledger"], event="end", leg=name)
    if cfg.get("crash"):
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        os.kill(os.getpid(), getattr(signal, cfg["crash"]))
    sys.exit(cfg.get("exit", 0))
