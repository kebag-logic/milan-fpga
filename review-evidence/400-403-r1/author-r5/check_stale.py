"""Require the reviewed stale wording and unread values to be absent."""
import subprocess

for pattern in (r"let it be pruned\|what both boards ship",
                r"RX_ADDRESS_FILTERS\|stream_dmac_alloc"):
    result = subprocess.run(["git", "grep", "-n", pattern],
                            capture_output=True, text=True, timeout=120)
    assert result.returncode == 1 and not result.stdout and not result.stderr, result
    print("PASS: git grep -n", repr(pattern), "returned no matches (rc 1)")
