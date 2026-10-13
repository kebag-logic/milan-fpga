"""Run a command; write each output line prefixed with seconds since start; final line has rc and total."""
import subprocess, sys, time
log = open(sys.argv[1], "w", buffering=1)
t0 = time.monotonic()
p = subprocess.Popen(sys.argv[2:], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
for line in p.stdout:
    log.write(f"{time.monotonic() - t0:8.1f} {line}")
rc = p.wait()
log.write(f"{time.monotonic() - t0:8.1f} == rc {rc}\n")
sys.exit(rc)
