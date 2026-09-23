import fcntl, os, sys, time
args = sys.argv[1:]
locks = os.environ.get("FAKE_LOCKS", "/tmp")
if "--interrupt-selftest" in args:
    print("interrupt-selftest: PASS"); sys.exit(0)
slot = args[args.index("--slot") + 1] if "--slot" in args else "0"
pr = args[args.index("--pr") + 1]
fd = os.open(f"{locks}/slot-{slot}", os.O_RDWR | os.O_CREAT)
time.sleep(2)  # materialization before the slot is taken
try:
    if os.environ.get("FAKE_BREAK") != "nolock":
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
except BlockingIOError:
    print(f"act-ci: REFUSED: replay slot {slot} is in use by another runner invocation" if slot != "0"
          else "act-ci: REFUSED: shared Docker volume 'act-toolcache' already exists", file=sys.stderr)
    sys.exit(2)
if slot != "0":
    print(f"act-ci: slot {slot}: own daemon unix:///run/milan-act-slot-{slot}/docker.sock", flush=True)
print("act-ci: running docs (.github/workflows/docs.yml)", flush=True)
time.sleep(6)
broken = os.environ.get("FAKE_BREAK") == "parallel" and slot == "1"
verdict = "FAILED (1)" if pr == "22" or broken else "PASS at " + "a" * 40
print(f"act-ci: docs: {verdict}", flush=True)
sys.exit(1 if pr == "22" or broken else 0)
