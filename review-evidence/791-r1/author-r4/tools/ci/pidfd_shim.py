"""sitecustomize for the replay's venvs ([A746c], not part of the tree): the standalone CPython 3.12.3 on this
host was built without os.pidfd_open and signal.pidfd_send_signal, which the runner image's 3.12.3 has and the
suite driver's owned_process.py requires. Both are thin wrappers over a Linux syscall (x86_64: 434 and 424);
they are provided here with CPython's signatures and its OSError mapping (ESRCH is ProcessLookupError)."""
import ctypes
import os
import signal

_libc = ctypes.CDLL(None, use_errno=True)
_libc.syscall.restype = ctypes.c_long


def _check(result: int) -> int:
    if result < 0:
        err = ctypes.get_errno()
        raise OSError(err, os.strerror(err))
    return result


if not hasattr(os, "pidfd_open"):
    def pidfd_open(pid: int, flags: int = 0, /) -> int:
        """os.pidfd_open: pidfd_open(2)."""
        return _check(_libc.syscall(ctypes.c_long(434), ctypes.c_int(pid), ctypes.c_uint(flags)))
    os.pidfd_open = pidfd_open

if not hasattr(signal, "pidfd_send_signal"):
    def pidfd_send_signal(pidfd: int, sig: int, siginfo: None = None, flags: int = 0, /) -> None:
        """signal.pidfd_send_signal: pidfd_send_signal(2), siginfo NULL as CPython passes it."""
        _check(_libc.syscall(ctypes.c_long(424), ctypes.c_int(pidfd), ctypes.c_int(int(sig)), None,
                             ctypes.c_uint(flags)))
    signal.pidfd_send_signal = pidfd_send_signal
