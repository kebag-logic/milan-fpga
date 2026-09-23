#!/usr/bin/env python3
"""[R267] Independent mutation probes for the #532 slot code at the reviewed head.

Each probe is one exact substitution (it must apply exactly once) in a copy of
scripts/act_ci.py inside a disposable scratch clone. The candidate's offline
--selftest then runs ONLY inside the network-less, unprivileged sandbox of
run-selftest-sandbox.sh. A probe is KILLED when the self-test exits non-zero
(failing check labels are listed) and SURVIVED when it passes. The exact head
bytes are restored after every probe and verified by SHA-256 at the end.

Usage: mutation-probes.py STAGE_CLONE SANDBOX_SCRIPT
"""

import hashlib
import pathlib
import subprocess
import sys

HEAD_SHA256 = "e1d614342e30162aae19a5ca8df7fe631784b61212e30dfa7f5ec6b034be276c"

PROBES = [
    # --- wiring of the live proof's per-slot interruption gate
    ("R01 live interrupt self-test silently runs in slot 0",
     "            lambda: interrupt_selftest(act_binary, args.sudo, slot)\n",
     "            lambda: interrupt_selftest(act_binary, args.sudo, ReplaySlot(0))\n"),
    ("R02 interrupt self-test never enters its slot",
     "        with replay_slot(slot, context=context, scratch=layout.temporary):\n"
     "            prefix = require_runtime(act_binary, use_sudo, layout, env)\n\n"
     "            planted = new_planted_volumes()",
     "        with contextlib.nullcontext():\n"
     "            prefix = require_runtime(act_binary, use_sudo, layout, env)\n\n"
     "            planted = new_planted_volumes()"),
    # --- teardown absence proofs
    ("R03 daemon runtime directory absence not proved",
     "        errors += require_slot_path_absent(slot.runtime_directory, host)\n", ""),
    ("R04 uplink pidfile absence not proved",
     "        errors += require_slot_path_absent(slot.uplink_pidfile, host)\n", ""),
    ("R05 uplink unload not proved (stop still runs)",
     "        errors += stop_slot_unit(\n            slot.uplink_unit, host, timeout=SLOT_COMMAND_TIMEOUT_SECONDS\n        )\n",
     "        stop_slot_unit(\n            slot.uplink_unit, host, timeout=SLOT_COMMAND_TIMEOUT_SECONDS\n        )\n"),
    ("R06 slice inactivity not proved",
     '    errors += await_slot_state(slot.slice_unit, "ActiveState", "inactive", host)\n', ""),
    ("R07 slice cgroup absence not proved",
     "    errors += require_slot_path_absent(CGROUP_ROOT / slot.slice_unit, host)\n", ""),
    ("R08 an unanswerable nft query is read as table absent (fail-open)",
     '    if "no such file or directory" in (result.stderr or "").lower():\n        return False\n',
     "    if True:\n        return False\n"),
    # --- acquisition wiring
    ("R09 slot root never validated on acquisition",
     "    validate_slot_root(slot.root, inspect=host.inspect_root)\n", ""),
    ("R10 production lock accepts a lock file owned by the invoking user",
     "    owner: int = 0,\n) -> int:\n    \"\"\"Hold `slot`'s host-wide lock",
     "    owner: int = os.getuid(),\n) -> int:\n    \"\"\"Hold `slot`'s host-wide lock"),
    ("R11 privileged host commands may prompt (sudo without -n)",
     '            [require_tool("sudo"), "-n", "--", *command],\n',
     '            [require_tool("sudo"), "--", *command],\n'),
    ("R12 slot teardown runs without blocked cleanup signals",
     "        if not lease.released:\n            with blocked_cleanup_signals():\n                release_replay_slot(lease, host=host)\n",
     "        if not lease.released:\n            release_replay_slot(lease, host=host)\n"),
    # --- residue detection
    ("R13 residue ignores an active slice",
     '    if slice_state != "inactive":\n', "    if False:\n"),
    ("R14 residue ignores the uplink pidfile",
     "        for path in (slot.netns_path, slot.runtime_directory, slot.uplink_pidfile)\n",
     "        for path in (slot.netns_path, slot.runtime_directory)\n"),
    ("R15 residue counts only units in state loaded",
     '        if state != "not-found":\n', '        if state == "loaded":\n'),
    # --- ordering controls (expected KILLED: the order is security relevant)
    ("R16 firewall table deleted before the uplink stops",
     '    if "uplink" in lease.attempted:\n        errors += stop_slot_unit(\n            slot.uplink_unit, host, timeout=SLOT_COMMAND_TIMEOUT_SECONDS\n        )\n        errors += require_slot_path_absent(slot.uplink_pidfile, host)\n'
     '    if "slice" in lease.attempted:\n        errors += release_slot_slice(slot, host)\n'
     '    if "firewall" in lease.attempted:\n        errors += remove_slot_firewall(slot, host)\n',
     '    if "firewall" in lease.attempted:\n        errors += remove_slot_firewall(slot, host)\n'
     '    if "uplink" in lease.attempted:\n        errors += stop_slot_unit(\n            slot.uplink_unit, host, timeout=SLOT_COMMAND_TIMEOUT_SECONDS\n        )\n        errors += require_slot_path_absent(slot.uplink_pidfile, host)\n'
     '    if "slice" in lease.attempted:\n        errors += release_slot_slice(slot, host)\n'),
    ("R17 firewall rule matches only IPv4 loopback instead of every host-local address",
     '"fib daddr type local counter reject\\n"', '"ip daddr 127.0.0.0/8 counter reject\\n"'),
    ("R18 identity accepts either label instead of both",
     "        or not expected.issubset(labels)\n", "        or not expected.intersection(labels)\n"),
]


def selftest(stage: pathlib.Path, sandbox: pathlib.Path, label: str) -> tuple[int, str]:
    """Run the sandboxed self-test; (exit status, its combined output)."""
    result = subprocess.run(
        [str(sandbox), str(stage), "scripts/act_ci.py", label],
        capture_output=True, text=True, timeout=1800, check=False,
    )
    return result.returncode, result.stdout + result.stderr


def main() -> int:
    stage = pathlib.Path(sys.argv[1]).resolve()
    sandbox = pathlib.Path(sys.argv[2]).resolve()
    runner = stage / "scripts/act_ci.py"
    original = runner.read_bytes()
    if hashlib.sha256(original).hexdigest() != HEAD_SHA256:
        print("stage runner is not the reviewed head bytes", file=sys.stderr)
        return 2
    text = original.decode("utf-8")
    try:
        for label, before, after in PROBES:
            count = text.count(before)
            if count != 1:
                print(f"{label}: NOT APPLIED (pattern occurs {count} times)", flush=True)
                continue
            runner.write_text(text.replace(before, after, 1), encoding="utf-8")
            status, output = selftest(stage, sandbox, label.split()[0])
            failed = [line.strip() for line in output.splitlines()
                      if line.startswith("  FAIL") or line.startswith("FAIL")]
            verdict = "KILLED" if status != 0 else "SURVIVED"
            print(f"{label}: {verdict} rc={status}", flush=True)
            for line in failed[:6]:
                print(f"    {line}", flush=True)
            if status != 0 and not failed:
                tail = [line for line in output.splitlines() if line.strip()][-3:]
                for line in tail:
                    print(f"    | {line}", flush=True)
    finally:
        runner.write_bytes(original)
    restored = hashlib.sha256(runner.read_bytes()).hexdigest()
    print(f"restored scripts/act_ci.py sha256={restored} "
          f"{'EXACT' if restored == HEAD_SHA256 else 'MISMATCH'}")
    return 0 if restored == HEAD_SHA256 else 2


if __name__ == "__main__":
    raise SystemExit(main())
