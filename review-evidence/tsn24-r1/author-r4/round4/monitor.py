from pathlib import Path
import time
root = Path('/sys/fs/cgroup') / Path('/proc/self/cgroup').read_text().split('::', 1)[1].strip().lstrip('/')
work = Path(__file__).resolve().parent
with (work / 'memory.csv').open('w', buffering=1) as log:
    log.write('time,memory_current,memory_peak\n')
    while not (work / 'monitor.stop').exists():
        current = int((root / 'memory.current').read_text())
        peak = int((root / 'memory.peak').read_text())
        log.write(f'{time.time():.3f},{current},{peak}\n')
        if current >= 9000000000:
            (work / 'memory-limit-exceeded').write_text(str(current) + '\n')
        time.sleep(5)
