#!/usr/bin/env python3
"""Run a foreground offline command in disposable user/PID/network namespaces."""
import os
import pathlib
import subprocess
import sys
import tempfile

packet = pathlib.Path(__file__).resolve().parent.parent
repo = pathlib.Path(sys.argv[1]).resolve()
name = sys.argv[2]
command = sys.argv[3:]
with tempfile.TemporaryDirectory(dir=packet / "scratch", prefix=name + "-") as scratch:
    args = ["bwrap", "--unshare-all", "--die-with-parent", "--new-session",
            "--cap-drop", "ALL", "--ro-bind", "/usr", "/usr",
            "--symlink", "usr/bin", "/bin", "--symlink", "usr/lib", "/lib",
            "--symlink", "usr/lib64", "/lib64", "--proc", "/proc", "--dev", "/dev",
            "--tmpfs", "/tmp", "--dir", "/etc", "--dir", "<home-path>",
            "--ro-bind", "/etc/passwd", "/etc/passwd", "--ro-bind", "/etc/group", "/etc/group",
            "--ro-bind", str(repo), "/repo", "--bind", scratch, "/work",
            "--ro-bind", str(packet / "scripts"), "/review",
            "--ro-bind", str(packet / "scratch/venv"), "/env",
            "--clearenv", "--setenv", "PATH", "/env/bin:/usr/bin:/bin",
            "--setenv", "HOME", "<home-path>", "--setenv", "LANG", "C.UTF-8",
            "--setenv", "GITHUB_WORKSPACE", "/repo", "--setenv", "PYTHONDONTWRITEBYTECODE", "1",
            "--setenv", "GIT_CONFIG_COUNT", "1", "--setenv", "GIT_CONFIG_KEY_0", "safe.directory",
            "--setenv", "GIT_CONFIG_VALUE_0", "/repo", "--chdir", "/repo", *command]
    log = packet / "receipts" / (name + ".log")
    with log.open("w") as out:
        out.write("command: " + repr(command) + "\n")
        out.write("isolation: private user/PID/network/IPC/UTS namespaces; no host home, sockets or credentials; read-only source; no capabilities\n")
        out.flush()
        result = subprocess.run(args, stdout=out, stderr=subprocess.STDOUT, timeout=580)
    (packet / "receipts" / (name + ".rc")).write_text(str(result.returncode) + "\n")
    print(name, "rc", result.returncode, flush=True)
    sys.exit(result.returncode)
