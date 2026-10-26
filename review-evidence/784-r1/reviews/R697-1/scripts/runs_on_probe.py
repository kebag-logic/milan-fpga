"""Drive the head's real validate_workflow_sandbox with edge-case runs-on YAML values.

Usage: python3 -I runs_on_probe.py <checkout> <scratch-dir>
Loads <checkout>/scripts/act_ci.py by path (no copy), writes one docs workflow per
probe under <scratch-dir>, and prints ACCEPT or REFUSE with the refusal text.
"""
import importlib.util
import pathlib
import sys

checkout, scratch = (pathlib.Path(arg).resolve() for arg in sys.argv[1:3])
spec = importlib.util.spec_from_file_location("act_ci_probe", checkout / "scripts" / "act_ci.py")
act_ci = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = act_ci
spec.loader.exec_module(act_ci)

PROBES = [
    ("literal ubuntu-latest", "ubuntu-latest", True),
    ("literal ubuntu-24.04", "ubuntu-24.04", True),
    ("single-quoted ubuntu-24.04", "'ubuntu-24.04'", True),
    ("double-quoted ubuntu-24.04", '"ubuntu-24.04"', True),
    ("ubuntu-22.04", "ubuntu-22.04", False),
    ("ubuntu-26.04", "ubuntu-26.04", False),
    ("ubuntu-20.04", "ubuntu-20.04", False),
    ("empty value", "", False),
    ("empty quoted string", '""', False),
    ("null", "null", False),
    ("matrix expression", "${{ matrix.os }}", False),
    ("one-label list", "[ubuntu-24.04]", False),
    ("two-label list", "[ubuntu-latest, ubuntu-24.04]", False),
    ("group mapping", "{group: hosted, labels: ubuntu-24.04}", False),
    ("trailing space quoted", "'ubuntu-24.04 '", False),
    ("upper-case", "UBUNTU-LATEST", False),
    ("windows-latest", "windows-latest", False),
    ("macos-latest", "macos-latest", False),
    ("number 24.04", "24.04", False),
    ("self-hosted", "self-hosted", False),
]

failures = 0
for index, (name, value, want_accept) in enumerate(PROBES):
    root = scratch / f"probe-{index:02d}"
    message = act_ci.runs_on_refusal(root, value)
    accepted = message == ""
    ok = accepted == want_accept
    failures += not ok
    print(f"{'ok  ' if ok else 'BAD '} {'ACCEPT' if accepted else 'REFUSE'} {name!r}: {message}")
print(f"probes {len(PROBES)}, unexpected {failures}")
sys.exit(1 if failures else 0)
