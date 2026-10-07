"""Remove local compiler installation prefixes without changing diagnostics."""
import re

def toolchain_paths(data: bytes) -> bytes:
    return re.sub(rb"/home/[^\s'\"<>]+?/usr/share/verilator", b"$VERILATOR_ROOT", data)
