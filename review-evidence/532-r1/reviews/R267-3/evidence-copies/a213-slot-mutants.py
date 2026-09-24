#!/usr/bin/env python3
"""[A213] Mutation run for the #532 slot code: both reviewers' mutants plus new ones.

Each mutant is one exact substitution that must apply exactly once to the
stage clone's scripts/act_ci.py. The mutated runner's offline --selftest runs
ONLY inside the network-less, unprivileged sandbox of run-selftest-sandbox.sh
(the runner-change bootstrap rule). KILLED means the self-test failed (or timed
out); SURVIVED means it passed. The stage bytes are restored after every
mutant and verified by SHA-256 at the end.

Usage: slot-mutants.py STAGE SANDBOX_SCRIPT [root]
"""

import hashlib
import pathlib
import subprocess
import sys

MUTANTS = [
    # --- control: must SURVIVE (proves the harness does not kill everything)
    ("control trailing comment", 'if __name__ == "__main__":\n',
     '# a213 control\nif __name__ == "__main__":\n'),
    # --- R266-1 probes/slot_mutants.py, verbatim fragments
    ("R266 slot-root-validation-unwired",
     "    validate_slot_root(slot.root, inspect=host.inspect_root)\n    lease.lock = host.lock(slot)\n",
     "    lease.lock = host.lock(slot)\n"),
    ("R266 cpu-range-boundary", "    if last >= host_cpus:\n", "    if last > host_cpus:\n"),
    ("R266 nft-query-error-reads-absent",
     '    if "no such file or directory" in (result.stderr or "").lower():\n        return False\n'
     '    require_host_success(result, f"replay slot {slot.number} firewall query")\n    return True\n',
     "    return False\n"),
    ("R266 runtime-dir-absence-dropped",
     "        errors += require_slot_path_absent(slot.runtime_directory, host)\n", ""),
    ("R266 uplink-pidfile-absence-dropped",
     "        errors += require_slot_path_absent(slot.uplink_pidfile, host)\n", ""),
    ("R266 slice-cgroup-absence-dropped",
     "    errors += require_slot_path_absent(CGROUP_ROOT / slot.slice_unit, host)\n", ""),
    ("R266 slot-teardown-signals-unblocked",
     "            with blocked_cleanup_signals():\n                release_replay_slot(lease, host=host)\n",
     "            release_replay_slot(lease, host=host)\n"),
    ("R266 slice-residue-only-active",
     '    if slice_state != "inactive":\n', '    if slice_state == "active":\n'),
    ("R266 unit-state-query-failure-reads-absent",
     "        except Refusal as exc:\n            return [str(exc)]\n",
     "        except Refusal:\n            return []\n"),
    ("R266 dropin-query-failure-ignored",
     '            errors.append(f"{slot.slice_unit} kept its runtime memory cap")\n'
     "    except Refusal as exc:\n        errors.append(str(exc))\n",
     '            errors.append(f"{slot.slice_unit} kept its runtime memory cap")\n'
     "    except Refusal:\n        pass\n"),
    ("R266 path-present-ignores-dangling-symlink",
     "    return path.is_symlink() or path.exists()\n", "    return path.exists()\n"),
    ("R266 interrupt-selftest-outside-slot",
     "        with replay_slot(slot, context=context, scratch=layout.temporary):\n"
     "            prefix = require_runtime(act_binary, use_sudo, layout, env)\n",
     "        with contextlib.nullcontext():\n"
     "            prefix = require_runtime(act_binary, use_sudo, layout, env)\n"),
    ("R266 identity-labels-unchecked", "        or not expected.issubset(labels)\n", ""),
    ("R266 live-selftest-inherited-refusal-dropped",
     "        refuse_inherited_docker_endpoint(os.environ)\n"
     "        slot = select_slot(args.slot, args.slot_root, use_sudo=args.sudo)\n"
     "        if args.boundary_selftest and slot.isolated:\n",
     "        slot = select_slot(args.slot, args.slot_root, use_sudo=args.sudo)\n"
     "        if args.boundary_selftest and slot.isolated:\n"),
    ("R266 pr-run-inherited-refusal-dropped",
     "        refuse_inherited_docker_endpoint(os.environ)\n"
     "        slot = select_slot(args.slot, args.slot_root, use_sudo=args.sudo)\n"
     "        validate_bootstrap_options(\n",
     "        slot = select_slot(args.slot, args.slot_root, use_sudo=args.sudo)\n"
     "        validate_bootstrap_options(\n"),
    ("R266 lock-blocking", "        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)\n",
     "        fcntl.flock(descriptor, fcntl.LOCK_EX)\n"),
    ("R266 lock-follows-symlink",
     "            slot.lock_path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC\n",
     "            slot.lock_path, os.O_RDONLY | os.O_CLOEXEC\n"),
    ("R266 firewall-reject-loopback-only", '        "fib daddr type local counter reject\\n"\n',
     '        "ip daddr 127.0.0.0/8 counter reject\\n"\n'),
    ("R266 uplink-maps-gateway", '        "--no-map-gw",\n        "--pid",\n', '        "--pid",\n'),
    ("R266 slot-endpoint-range-unchecked",
     "    if match is None or int(match.group(1)) > SLOT_LIMIT:\n", "    if match is None:\n"),
    ("R266 teardown-daemon-after-slice",
     '    if "daemon" in lease.attempted:\n        errors += stop_slot_unit(\n',
     "    if False:\n        errors += stop_slot_unit(\n"),
    # --- R267-1 mutation-probes.py, verbatim fragments
    ("R267 R01 live interrupt self-test silently runs in slot 0",
     "            lambda: interrupt_selftest(act_binary, args.sudo, slot)\n",
     "            lambda: interrupt_selftest(act_binary, args.sudo, ReplaySlot(0))\n"),
    ("R267 R02 interrupt self-test never enters its slot",
     "        with replay_slot(slot, context=context, scratch=layout.temporary):\n"
     "            prefix = require_runtime(act_binary, use_sudo, layout, env)\n\n"
     "            planted = new_planted_volumes()",
     "        with contextlib.nullcontext():\n"
     "            prefix = require_runtime(act_binary, use_sudo, layout, env)\n\n"
     "            planted = new_planted_volumes()"),
    ("R267 R03 daemon runtime directory absence not proved",
     "        errors += require_slot_path_absent(slot.runtime_directory, host)\n", ""),
    ("R267 R04 uplink pidfile absence not proved",
     "        errors += require_slot_path_absent(slot.uplink_pidfile, host)\n", ""),
    ("R267 R05 uplink unload not proved",
     "        errors += stop_slot_unit(\n            slot.uplink_unit, host, timeout=SLOT_COMMAND_TIMEOUT_SECONDS\n        )\n",
     "        stop_slot_unit(\n            slot.uplink_unit, host, timeout=SLOT_COMMAND_TIMEOUT_SECONDS\n        )\n"),
    ("R267 R06 slice inactivity not proved",
     '    errors += await_slot_state(slot.slice_unit, "ActiveState", "inactive", host)\n', ""),
    ("R267 R07 slice cgroup absence not proved",
     "    errors += require_slot_path_absent(CGROUP_ROOT / slot.slice_unit, host)\n", ""),
    ("R267 R08 an unanswerable nft query is read as table absent",
     '    if "no such file or directory" in (result.stderr or "").lower():\n        return False\n',
     "    if True:\n        return False\n"),
    ("R267 R09 slot root never validated on acquisition",
     "    validate_slot_root(slot.root, inspect=host.inspect_root)\n", ""),
    ("R267 R10 production lock accepts the invoking user's file",
     "    owner: int = 0,\n) -> int:\n    \"\"\"Hold `slot`'s host-wide lock",
     "    owner: int = os.getuid(),\n) -> int:\n    \"\"\"Hold `slot`'s host-wide lock"),
    ("R267 R11 privileged host commands may prompt (no -n)",
     '            [require_tool("sudo"), "-n", "--", *command],\n',
     '            [require_tool("sudo"), "--", *command],\n'),
    ("R267 R12 slot teardown without blocked cleanup signals",
     "        if not lease.released:\n            with blocked_cleanup_signals():\n"
     "                release_replay_slot(lease, host=host)\n",
     "        if not lease.released:\n            release_replay_slot(lease, host=host)\n"),
    ("R267 R13 residue ignores an active slice", '    if slice_state != "inactive":\n', "    if False:\n"),
    ("R267 R14 residue ignores the uplink pidfile",
     "        for path in (slot.netns_path, slot.runtime_directory, slot.uplink_pidfile)\n",
     "        for path in (slot.netns_path, slot.runtime_directory)\n"),
    ("R267 R15 residue counts only units in state loaded",
     '        if state != "not-found":\n', '        if state == "loaded":\n'),
    ("R267 R16 firewall table deleted before the uplink stops",
     '    if "uplink" in lease.attempted:\n        errors += stop_slot_unit(\n'
     "            slot.uplink_unit, host, timeout=SLOT_COMMAND_TIMEOUT_SECONDS\n        )\n"
     "        errors += require_slot_path_absent(slot.uplink_pidfile, host)\n"
     '    if "slice" in lease.attempted:\n        errors += release_slot_slice(slot, host)\n'
     '    if "firewall" in lease.attempted:\n        errors += remove_slot_firewall(slot, host)\n',
     '    if "firewall" in lease.attempted:\n        errors += remove_slot_firewall(slot, host)\n'
     '    if "uplink" in lease.attempted:\n        errors += stop_slot_unit(\n'
     "            slot.uplink_unit, host, timeout=SLOT_COMMAND_TIMEOUT_SECONDS\n        )\n"
     "        errors += require_slot_path_absent(slot.uplink_pidfile, host)\n"
     '    if "slice" in lease.attempted:\n        errors += release_slot_slice(slot, host)\n'),
    ("R267 R17 firewall rule matches only IPv4 loopback",
     '"fib daddr type local counter reject\\n"', '"ip daddr 127.0.0.0/8 counter reject\\n"'),
    ("R267 R18 identity accepts either label",
     "        or not expected.issubset(labels)\n", "        or not expected.intersection(labels)\n"),
    # --- A213: the protections this round adds
    ("A213 F1 uplink-only rule dropped",
     '        f"add rule {table} output {selector} oifname != {{ {allowed} }} counter reject\\n"\n', ""),
    ("A213 F1 uplink rule inverted to accept only",
     "oifname != {{ {allowed} }} counter reject", "oifname == {{ {allowed} }} counter reject"),
    ("A213 F1 discovered uplinks ignored",
     "    lease.uplinks = slot_uplink_interfaces(host)\n", '    lease.uplinks = ("eth0",)\n'),
    ("A213 F1 unreachable default taken as an uplink",
     '            if route.get("type", "unicast") != "unicast":\n                continue\n', ""),
    ("A213 F1 failed route query read as no route",
     "        )\n        require_host_success(result, description)\n        try:\n            routes = json.loads(",
     "        )\n        try:\n            routes = json.loads("),
    ("A213 F1 loopback accepted as an uplink",
     '        or any(not UPLINK_INTERFACE_RE.fullmatch(name) or name == "lo" for name in names)\n',
     "        or any(not UPLINK_INTERFACE_RE.fullmatch(name) for name in names)\n"),
    ("A213 F1 unquotable uplink name accepted",
     "        or any(not UPLINK_INTERFACE_RE.fullmatch(name) or name == \"lo\" for name in names)\n",
     "        or any(name == \"lo\" for name in names)\n"),
    ("A213 F1 empty uplink set accepted", "        not names\n        or len(set(names))",
     "        False\n        or len(set(names))"),
    ("A213 F6 ancestors not inspected",
     "    for depth in range(1, len(root.parts) + 1):\n",
     "    for depth in (len(root.parts),):\n"),
    ("A213 F6 ancestor owner unchecked", "            or info.st_uid != 0\n            or info.st_mode & (stat.S_IWGRP | stat.S_IWOTH)\n        ):\n            raise Refusal(\n                f\"slot root {root}: {component}",
     "            or (info.st_uid != 0 and component == root)\n            or info.st_mode & (stat.S_IWGRP | stat.S_IWOTH)\n        ):\n            raise Refusal(\n                f\"slot root {root}: {component}"),
    ("A213 F4 slot memory cap never checked",
     "        yield\n        print(\n            f\"act-ci: slot {slot.number}: {require_slot_memory_cap_unexhausted(slot, host)}\",\n"
     "            flush=True,\n        )\n",
     "        yield\n"),
    ("A213 F4 cap exhaustion ignored", "    if exhausted:\n", "    if False:\n"),
    ("A213 F4 missing oom count read as zero",
     '        exhausted = int(events["oom"])\n', '        exhausted = int(events.get("oom", 0))\n'),
    ("A213 F4 hierarchical events read (container limits counted)",
     'host.read_text(cgroup / "memory.events.local")', 'host.read_text(cgroup / "memory.events")'),
]


def selftest(stage: pathlib.Path, sandbox: pathlib.Path, label: str, as_root: str) -> tuple[int, str]:
    """Run the sandboxed self-test; (exit status, combined output); a timeout kills."""
    try:
        result = subprocess.run(
            [str(sandbox), str(stage), label, as_root],
            capture_output=True, text=True, timeout=240, check=False,
        )
    except subprocess.TimeoutExpired:
        return 124, "timed out"
    return result.returncode, result.stdout + result.stderr


def main() -> int:
    """Apply, run and restore every mutant; print one verdict line each."""
    stage = pathlib.Path(sys.argv[1]).resolve()
    sandbox = pathlib.Path(sys.argv[2]).resolve()
    as_root = sys.argv[3] if len(sys.argv) > 3 else ""
    runner = stage / "scripts/act_ci.py"
    original = runner.read_bytes()
    digest = hashlib.sha256(original).hexdigest()
    text = original.decode("utf-8")
    print(f"stage act_ci.py sha256={digest} as_root={as_root or 'no'}", flush=True)
    try:
        for label, before, after in MUTANTS:
            count = text.count(before)
            if count != 1:
                print(f"{label}: NOT APPLIED (fragment occurs {count} times)", flush=True)
                continue
            runner.write_text(text.replace(before, after, 1), encoding="utf-8")
            status, output = selftest(stage, sandbox, label.split()[0], as_root)
            failed = [line.strip() for line in output.splitlines() if line.startswith("  FAIL")]
            verdict = "KILLED" if status != 0 else "SURVIVED"
            print(f"{label}: {verdict} rc={status}", flush=True)
            for line in failed[:4]:
                print(f"    {line}", flush=True)
            if status not in (0, 1) and not failed:
                tail = [line for line in output.splitlines() if line.strip()][-2:]
                for line in tail:
                    print(f"    | {line[:200]}", flush=True)
            runner.write_bytes(original)
    finally:
        runner.write_bytes(original)
    restored = hashlib.sha256(runner.read_bytes()).hexdigest()
    print(f"restored sha256={restored} {'EXACT' if restored == digest else 'MISMATCH'}")
    return 0 if restored == digest else 2


if __name__ == "__main__":
    raise SystemExit(main())
