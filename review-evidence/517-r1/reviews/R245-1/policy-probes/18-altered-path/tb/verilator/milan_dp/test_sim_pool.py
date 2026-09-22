    if not hasattr(os, "pidfd_open") or not Path("/proc/foreign/self/stat").is_file():
