"""Review guard, on PYTHONPATH for the review's LiteX runs only: the shared CPU netlist cache is never written.
LiteX's VexiiRiscv generates an uncached netlist by running the generator through subprocess.check_call; any
command that runs the generator is refused by name instead."""
import subprocess

_check_call = subprocess.check_call


def _guarded(cmd, *args, **kwargs):
    text = cmd if isinstance(cmd, str) else ' '.join(map(str, cmd))
    if 'SocGen' in text or 'sbt' in text.split():
        raise RuntimeError('REVIEW GUARD: the CPU netlist is not cached; generation refused: ' + text[:200])
    return _check_call(cmd, *args, **kwargs)


subprocess.check_call = _guarded
