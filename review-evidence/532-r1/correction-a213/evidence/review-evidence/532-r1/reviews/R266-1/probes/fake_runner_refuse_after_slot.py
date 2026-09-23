# R266-1 fake runner for scripts/act_slot_proof.sh: every PR run REFUSES
# (exit 2, no workflow verdict line) after it has taken its slot, as a run
# would when an action clone or image pull fails; slots are real flocks so the
# same-slot rival is refused exactly as the audited runner refuses it.
import fcntl, os, sys, time
args = sys.argv[1:]
if "--interrupt-selftest" in args:
    print("interrupt-selftest: PASS"); sys.exit(0)
slot = args[args.index("--slot") + 1] if "--slot" in args else "0"
fd = os.open(f"/tmp/fake-slot-{slot}.lock", os.O_RDWR | os.O_CREAT)
try:
    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
except BlockingIOError:
    print(f"act-ci: REFUSED: replay slot {slot} is in use by another runner invocation", file=sys.stderr)
    sys.exit(2)
if slot != "0":
    print(f"act-ci: slot {slot}: own daemon unix:///run/milan-act-slot-{slot}/docker.sock", flush=True)
time.sleep(8)
print("act-ci: REFUSED: action clone of actions/checkout@v4 failed", file=sys.stderr)
sys.exit(2)
