#!/usr/bin/env python3
"""R266-1 mutation probes for the #532 slot code in scripts/act_ci.py.

Each mutant replaces one exact source fragment (it must occur exactly once)
in a private copy of the exact-head tree. The mutated runner is executed ONLY
inside a disposable, network-less rootless container (the bootstrap rule), with
read-only recording stubs for sudo, gh and docker. A mutant is KILLED when the
offline --selftest exits non-zero (or times out), SURVIVED when it passes.

usage: slot_mutants.py BASE_TREE WORK_DIR STUB_DIR IMAGE [JOBS]
"""
import concurrent.futures
import pathlib
import shutil
import subprocess
import sys

MUTANTS = [
    ("control-trailing-comment", "if __name__ == \"__main__\":\n",
     "# r266 control\nif __name__ == \"__main__\":\n"),
    ("slot-root-validation-unwired",
     "    validate_slot_root(slot.root, inspect=host.inspect_root)\n    lease.lock = host.lock(slot)\n",
     "    lease.lock = host.lock(slot)\n"),
    ("cpu-range-boundary",
     "    if last >= host_cpus:\n", "    if last > host_cpus:\n"),
    ("nft-query-error-reads-absent",
     "    if \"no such file or directory\" in (result.stderr or \"\").lower():\n        return False\n"
     "    require_host_success(result, f\"replay slot {slot.number} firewall query\")\n    return True\n",
     "    return False\n"),
    ("runtime-dir-absence-dropped",
     "        errors += require_slot_path_absent(slot.runtime_directory, host)\n", ""),
    ("uplink-pidfile-absence-dropped",
     "        errors += require_slot_path_absent(slot.uplink_pidfile, host)\n", ""),
    ("slice-cgroup-absence-dropped",
     "    errors += require_slot_path_absent(CGROUP_ROOT / slot.slice_unit, host)\n", ""),
    ("slot-teardown-signals-unblocked",
     "            with blocked_cleanup_signals():\n                release_replay_slot(lease, host=host)\n",
     "            release_replay_slot(lease, host=host)\n"),
    ("slice-residue-only-active",
     "    if slice_state != \"inactive\":\n", "    if slice_state == \"active\":\n"),
    ("unit-state-query-failure-reads-absent",
     "        except Refusal as exc:\n            return [str(exc)]\n",
     "        except Refusal:\n            return []\n"),
    ("dropin-query-failure-ignored",
     "            errors.append(f\"{slot.slice_unit} kept its runtime memory cap\")\n    except Refusal as exc:\n        errors.append(str(exc))\n",
     "            errors.append(f\"{slot.slice_unit} kept its runtime memory cap\")\n    except Refusal:\n        pass\n"),
    ("path-present-ignores-dangling-symlink",
     "    return path.is_symlink() or path.exists()\n", "    return path.exists()\n"),
    ("interrupt-selftest-outside-slot",
     "        with replay_slot(slot, context=context, scratch=layout.temporary):\n            prefix = require_runtime(act_binary, use_sudo, layout, env)\n",
     "        with contextlib.nullcontext():\n            prefix = require_runtime(act_binary, use_sudo, layout, env)\n"),
    ("identity-labels-unchecked",
     "        or not expected.issubset(labels)\n", ""),
    ("live-selftest-inherited-refusal-dropped",
     "        refuse_inherited_docker_endpoint(os.environ)\n        slot = select_slot(args.slot, args.slot_root, use_sudo=args.sudo)\n        if args.boundary_selftest and slot.isolated:\n",
     "        slot = select_slot(args.slot, args.slot_root, use_sudo=args.sudo)\n        if args.boundary_selftest and slot.isolated:\n"),
    ("pr-run-inherited-refusal-dropped",
     "        refuse_inherited_docker_endpoint(os.environ)\n        slot = select_slot(args.slot, args.slot_root, use_sudo=args.sudo)\n        validate_bootstrap_options(\n",
     "        slot = select_slot(args.slot, args.slot_root, use_sudo=args.sudo)\n        validate_bootstrap_options(\n"),
    ("lock-blocking",
     "        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)\n",
     "        fcntl.flock(descriptor, fcntl.LOCK_EX)\n"),
    ("lock-follows-symlink",
     "            slot.lock_path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC\n",
     "            slot.lock_path, os.O_RDONLY | os.O_CLOEXEC\n"),
    ("firewall-reject-loopback-only",
     "        \"fib daddr type local counter reject\\n\"\n",
     "        \"ip daddr 127.0.0.0/8 counter reject\\n\"\n"),
    ("uplink-maps-gateway",
     "        \"--no-map-gw\",\n        \"--pid\",\n", "        \"--pid\",\n"),
    ("slot-endpoint-range-unchecked",
     "    if match is None or int(match.group(1)) > SLOT_LIMIT:\n", "    if match is None:\n"),
    ("teardown-daemon-after-slice",
     "    if \"daemon\" in lease.attempted:\n        errors += stop_slot_unit(\n",
     "    if False:\n        errors += stop_slot_unit(\n"),
]

TIMEOUT = 240


def run(base: pathlib.Path, work: pathlib.Path, stubs: pathlib.Path, image: str,
        label: str, old: str, new: str) -> tuple[str, str]:
    tree = work / label
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(base, tree, symlinks=True)
    target = tree / "scripts" / "act_ci.py"
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        return label, f"NOT-APPLIED (fragment occurs {count} times)"
    target.write_text(text.replace(old, new, 1), encoding="utf-8")
    logdir = work / f"{label}.stublog"
    logdir.mkdir(exist_ok=True)
    logdir.chmod(0o777)
    command = [
        "timeout", str(TIMEOUT), "podman", "run", "--rm", "--network", "none",
        "--cpus", "4", "--memory", "4g",
        "-v", f"{tree}:/src:ro",
        "-v", f"{stubs}/sudo:/usr/local/bin/sudo:ro",
        "-v", f"{stubs}/gh:/usr/local/bin/gh:ro",
        "-v", f"{stubs}/docker:/usr/local/bin/docker:ro",
        "-v", f"{logdir}:/stublog",
        image, "sh", "-c",
        "cp -a /src /tmp/work && cd /tmp/work && python3 scripts/act_ci.py --selftest",
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    (work / f"{label}.log").write_text(result.stdout + result.stderr, encoding="utf-8")
    failed = [line.strip() for line in (result.stdout + result.stderr).splitlines()
              if line.startswith("  FAIL")]
    if result.returncode == 124:
        verdict = "KILLED (selftest timed out)"
    elif result.returncode == 0:
        verdict = "SURVIVED (selftest PASS)"
    else:
        verdict = f"KILLED rc={result.returncode}: " + ("; ".join(failed[:3]) or
                  (result.stdout + result.stderr).strip().splitlines()[-1][:200])
    shutil.rmtree(tree)
    return label, verdict


def main() -> int:
    base, work, stubs = (pathlib.Path(a).resolve() for a in sys.argv[1:4])
    image = sys.argv[4]
    jobs = int(sys.argv[5]) if len(sys.argv) > 5 else 6
    work.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(jobs, 8)) as pool:
        futures = [pool.submit(run, base, work, stubs, image, *m) for m in MUTANTS]
        results = dict(f.result() for f in futures)
    for label, _old, _new in MUTANTS:
        print(f"{label}: {results[label]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
