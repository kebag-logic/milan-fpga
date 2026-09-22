    if not hasattr(os, "pidfd_open") or not Path("/proc/self/stat").is_file():
The target requires /proc
