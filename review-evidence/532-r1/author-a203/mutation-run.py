#!/usr/bin/env python3
"""[A203] Mutation controls for the #532 slot arms, run only inside a disposable container.

Each mutation is one exact substitution in the candidate scripts/act_ci.py. The
candidate's own --selftest runs inside a network-less container on the scratch
daemon; a mutation is KILLED when the self-test exits non-zero, and the arms
that failed are listed. Nothing here executes the candidate on the host.
"""

import pathlib
import subprocess
import sys
import tempfile

LANE = pathlib.Path("$LANES/532-act-parallel-slots")
SCRATCH = pathlib.Path("$REVIEWS/532-a203-packet/scratch")
DOCKER = ["sudo", "-n", "docker", "-H", "unix:///run/a203-exp/docker.sock"]
NAME = "a203-mutation"

MUTATIONS = [
    ("uplink maps the gateway to host loopback", '        "--no-map-gw",\n', ""),
    ("uplink forwards inbound TCP ports", '        "--tcp-ports",\n        "none",', '        "--tcp-ports",\n        "auto",'),
    ("daemon attaches to the system containerd", 'f"--property=NetworkNamespacePath={slot.netns_path}",\n        "--property=TemporaryFileSystem=/run/containerd",\n', 'f"--property=NetworkNamespacePath={slot.netns_path}",\n'),
    ("daemon leaves the slot namespace", '        f"--property=NetworkNamespacePath={slot.netns_path}",\n', ""),
    ("daemon reads the host daemon.json", '        "--config-file",\n        "/dev/null",', '        "--config-file",\n        "/etc/docker/daemon.json",'),
    ("daemon shares the default containerd namespace", '        "--containerd-namespace",\n        slot.name,\n', ""),
    ("slice memory cap removed", '                slot.slice_unit,\n                f"MemoryMax={SLOT_MEMORY_MAX}",', '                slot.slice_unit,\n                "MemoryMax=infinity",'),
    ("firewall rule not restricted to the slot cgroup", 'socket cgroupv2 level 1 "{slot.slice_unit}" ', ""),
    ("inherited endpoint no longer refused on the PR path", "        refuse_inherited_docker_endpoint(os.environ)\n        slot = select_slot(args.slot, args.slot_root, use_sudo=args.sudo)\n        validate_bootstrap_options(", "        slot = select_slot(args.slot, args.slot_root, use_sudo=args.sudo)\n        validate_bootstrap_options("),
    ("inherited endpoint no longer refused on the live path", "    try:\n        refuse_inherited_docker_endpoint(os.environ)\n        slot = select_slot(", "    try:\n        slot = select_slot("),
    ("lease recorded only after the create succeeds", "        if resource not in lease.attempted:\n            lease.attempted.append(resource)\n        description = f\"replay slot {slot.number} {resource} setup\"\n        require_host_success(\n            host.run(command, description=description, timeout=timeout), description\n        )\n", "        description = f\"replay slot {slot.number} {resource} setup\"\n        require_host_success(\n            host.run(command, description=description, timeout=timeout), description\n        )\n        if resource not in lease.attempted:\n            lease.attempted.append(resource)\n"),
    ("residue probe ignores the firewall table", "    if nft_table_present(slot, host):\n        found.append(", "    if False and nft_table_present(slot, host):\n        found.append("),
    ("residue refusal removed", "    if residue:\n        raise Refusal(\n            f\"replay slot {slot.number} holds", "    if False:\n        raise Refusal(\n            f\"replay slot {slot.number} holds"),
    ("slot CPUs ignored in act options", "--cpuset-cpus={container_cpuset(boundary.slot)} ", "--cpuset-cpus={container_cpuset()} "),
    ("boundary created through another slot's daemon", "    if planned.slot != slot_of_environment(context.env):\n", "    if False:\n"),
    ("slot lock not taken", "    lease.lock = host.lock(slot)\n", "    lease.lock = None\n"),
    ("slot lock never released", "            host.unlock(lease.lock)\n", "            pass\n"),
    ("teardown swallows unproved absence", "    lease.released = True\n    if errors:\n", "    lease.released = True\n    if False:\n"),
    ("slot 0 environment carries an endpoint", "    if selected.isolated:\n        environment[\"DOCKER_HOST\"]", "    if selected.number >= 0:\n        environment[\"DOCKER_HOST\"]"),
    ("isolated prefix does not enter the namespace", "        if slot\n        else []\n", "        if False\n        else []\n"),
    ("slice not stopped at teardown", '    for action in ("stop", "revert"):\n', '    for action in ("revert",):\n'),
    ("uplink not stopped at teardown", "    if \"uplink\" in lease.attempted:\n        errors += stop_slot_unit(", "    if False:\n        errors += stop_slot_unit("),
    ("namespace not deleted at teardown", "    if \"netns\" in lease.attempted:\n        errors += remove_slot_netns(slot, host)\n", ""),
    ("daemon identity not verified", "    verify_slot_daemon_identity(\n        slot, lease.token, context=context, docker_command=host.docker_command\n    )\n", ""),
    ("isolated slot accepted without sudo", "    if not use_sudo:\n        raise Refusal(\n            f\"replay slot {slot.number} runs its own Docker daemon and requires --sudo\"", "    if False:\n        raise Refusal(\n            f\"replay slot {slot.number} runs its own Docker daemon and requires --sudo\""),
    ("slot root may be group-writable", "or info.st_mode & (stat.S_IWGRP | stat.S_IWOTH)", "or info.st_mode & stat.S_IWOTH"),
    ("slot lock follows a symlink", "os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC", "os.O_RDONLY | os.O_CLOEXEC"),
    ("slot lock is not exclusive", "        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)\n", ""),
    ("boundary self-test allowed in an isolated slot", "        if args.boundary_selftest and slot.isolated:\n", "        if False:\n"),
    ("slot endpoint above the limit accepted", "    if match is None or int(match.group(1)) > SLOT_LIMIT:\n", "    if match is None:\n"),
    ("slot number above the limit accepted", "            or not 0 <= self.number <= SLOT_LIMIT\n", "            or not 0 <= self.number\n"),
    ("slot 0 enters the slot lifecycle", "    if not slot.isolated:\n        yield\n        return\n", ""),
    ("slot CPUs overlap slot 0", "    first = slot * CONTAINER_CPU_LIMIT\n", "    first = (slot - 1) * CONTAINER_CPU_LIMIT\n"),
    ("CPU availability not checked", "    if last >= host_cpus:\n        raise Refusal(", "    if False:\n        raise Refusal("),
    ("slice kept top-level check removed", "    if cgroup != f\"/{slot.slice_unit}\":\n", "    if False:\n"),
    ("table absence skipped when its delete fails", "    except Refusal as exc:\n        errors.append(str(exc))\n    try:\n        if nft_table_present(slot, host):", "        if nft_table_present(slot, host):"),
    ("rules write failure escapes as a raw error", "    try:\n        rules.write_text(slot_firewall_rules(slot), encoding=\"utf-8\")\n    except OSError as exc:\n        raise Refusal(f\"cannot write replay slot {slot.number} firewall rules: {exc}\") from exc\n", "    rules.write_text(slot_firewall_rules(slot), encoding=\"utf-8\")\n"),
    ("slot-root allowed for slot 0", "        if root is not None:\n            raise Refusal(\n                \"--slot-root applies only", "        if False:\n            raise Refusal(\n                \"--slot-root applies only"),
]


def docker(*arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Run one scratch-daemon Docker command."""
    return subprocess.run([*DOCKER, *arguments], text=True, capture_output=True, check=check)


def stage() -> pathlib.Path:
    """A scratch clone of the lane HEAD carrying the exact working-tree diff."""
    source = SCRATCH / "mutation-src"
    subprocess.run(["rm", "-rf", str(source)], check=True)
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", str(LANE), str(source)], check=True)
    diff = subprocess.run(["git", "-C", str(LANE), "diff", "HEAD", "--binary"],
                          check=True, capture_output=True).stdout
    subprocess.run(["git", "-C", str(source), "apply", "--index", "--allow-empty"],
                   input=diff, check=True)
    subprocess.run(["git", "-C", str(source), "-c", "user.name=a203", "-c",
                    "user.email=a203@invalid", "commit", "-q", "--allow-empty", "-m", "candidate"],
                   check=True)
    return source


def selftest() -> tuple[int, list[str]]:
    """The container self-test's status and its FAIL lines."""
    result = docker("exec", "-w", "/work", NAME, "python3", "scripts/act_ci.py", "--selftest",
                    check=False)
    output = result.stdout + result.stderr
    fails = [line.strip() for line in output.splitlines() if line.lstrip().startswith("FAIL")]
    if result.returncode != 0 and not fails:
        fails = ["(no FAIL line) " + (output.strip().splitlines() or ["?"])[-1]]
    return result.returncode, fails


def main() -> int:
    """Run the baseline and every mutation; exit 0 only when the baseline passes and every mutation is killed."""
    source = stage()
    original = (source / "scripts/act_ci.py").read_text(encoding="utf-8")
    docker("rm", "-f", NAME, check=False)
    docker("run", "-d", "--name", NAME, "--network", "none", "--cpuset-cpus=32-39",
           "--memory=8g", "--memory-swap=8g",
           "--label", "org.kebag-logic.milan-act-ci.owner=a203-selftest",
           "a203-selftest:ubuntu24", "tail", "-f", "/dev/null")
    docker("cp", str(source), f"{NAME}:/work")
    survived = 0
    try:
        rc, fails = selftest()
        print(f"baseline rc={rc} fails={len(fails)}")
        if rc != 0:
            print("\n".join(fails))
            return 1
        for index, (label, old, new) in enumerate(MUTATIONS, 1):
            if original.count(old) != 1:
                print(f"M{index:02d} SETUP-ERROR {label}: pattern count {original.count(old)}")
                survived += 1
                continue
            with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as handle:
                handle.write(original.replace(old, new))
            docker("cp", handle.name, f"{NAME}:/work/scripts/act_ci.py")
            pathlib.Path(handle.name).unlink()
            rc, fails = selftest()
            verdict = "KILLED" if rc != 0 else "SURVIVED"
            survived += rc == 0
            print(f"M{index:02d} {verdict} rc={rc} {label}")
            for line in fails[:6]:
                print(f"      {line}")
            if len(fails) > 6:
                print(f"      ... {len(fails) - 6} more")
        docker("cp", str(source / "scripts/act_ci.py"), f"{NAME}:/work/scripts/act_ci.py")
        rc, fails = selftest()
        print(f"restored rc={rc} fails={len(fails)}")
    finally:
        docker("rm", "-f", NAME, check=False)
    print(f"mutations={len(MUTATIONS)} survived={survived}")
    return 0 if survived == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
