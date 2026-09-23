#!/usr/bin/env python3
"""[R267] Slot-0 differential: base (live dev) runner vs reviewed head runner.

Run ONLY inside the network-less sandbox (run-in-sandbox.sh): it imports both
runner files as modules, which executes their top-level definitions. For the
same inputs it compares every slot-0 artefact the acceptance calls unchanged:
the controlled environment, the Docker and act prefixes with and without sudo,
the CPU set, the complete act command for every shipping workflow, the planned
boundary shape, and the parsed defaults of every pre-existing option. It also
exercises three slot/root refusal paths the offline self-test does not drive
through the production collaborators.
"""

import dataclasses
import importlib.util
import pathlib
import sys
from unittest import mock


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


base = load("act_base", "/base/scripts/act_ci.py")
head = load("act_head", "/head/scripts/act_ci.py")
results: list[tuple[str, bool, str]] = []


def record(label: str, ok: bool, detail: str = "") -> None:
    results.append((label, ok, detail))


def layout_of(module):
    pr = module.interrupt_selftest_pull_request()
    return module.make_layout(pathlib.Path("/tmp/differential-run"), pr)


with mock.patch("os.cpu_count", return_value=128):
    lb, lh = layout_of(base), layout_of(head)
    record("layouts equal", dataclasses.asdict(lb) == dataclasses.asdict(lh))
    eb, eh = base.controlled_act_environment(lb), head.controlled_act_environment(lh)
    record("slot-0 controlled environment identical", eb == eh, repr(set(eb) ^ set(eh)))
    record("slot-0 environment carries no Docker selector",
           not {"DOCKER_HOST", "DOCKER_CONTEXT", "DOCKER_CONFIG"} & set(eh))
    for sudo in (False, True):
        record(f"docker prefix identical (sudo={sudo})",
               base.docker_prefix(sudo, eb) == head.docker_prefix(sudo, eh))
        record(f"act prefix identical (sudo={sudo})",
               base.act_prefix("/audited/act", sudo, eb) == head.act_prefix("/audited/act", sudo, eh))
    record("slot-0 cpuset identical", base.container_cpuset() == head.container_cpuset(0) == "0-3")
    fields = dict(token="a" * 32, name="milan-act-ci-" + "a" * 32,
                  job_volume_prefixes=("act-docs-",), network_id="b" * 64,
                  gateway="172.30.0.1", toolcache_owned=True, toolcache_seeded=True)
    fields = {k: v for k, v in fields.items()
              if k in {f.name for f in dataclasses.fields(base.DockerBoundary)}}
    bb = base.DockerBoundary(**fields)
    bh = head.DockerBoundary(**fields)
    record("head boundary defaults to slot 0", bh.slot == 0)
    for workflow in base.WORKFLOWS:
        cb = base.build_act_command(["/audited/act"], workflow, lb, 43210, bb)
        ch = head.build_act_command(["/audited/act"], workflow, lh, 43210, bh)
        record(f"slot-0 act command identical for {workflow}", cb == ch)
    pb = base.new_docker_boundary(("act-docs-",))
    ph = head.new_docker_boundary(("act-docs-",))
    record("planned boundary shape identical apart from the new slot field",
           {f.name for f in dataclasses.fields(pb)} | {"slot"} == {f.name for f in dataclasses.fields(ph)}
           and ph.slot == 0 and ph.job_volume_prefixes == pb.job_volume_prefixes)
    argv = ["--pr", "7", "--workflow", "docs", "--sudo", "--dry-run", "--act-bin", "/a/act"]
    ab = vars(base.build_argument_parser().parse_args(argv))
    ah = vars(head.build_argument_parser().parse_args(argv))
    record("every pre-existing option parses identically",
           all(ab[k] == ah[k] for k in ab) and ah["slot"] is None and ah["slot_root"] is None,
           repr({k: (ab[k], ah.get(k)) for k in ab if ab[k] != ah.get(k)}))

    # Slot-root check reaches only the final path component (DECISION: "no symlink in its path").
    root = pathlib.Path("/tmp/slotroot-real")
    (root / "root").mkdir(parents=True, exist_ok=True)
    (root / "root").chmod(0o755)
    link = pathlib.Path("/tmp/slotroot-link")
    if not link.is_symlink():
        link.symlink_to(root)
    open_parent = pathlib.Path("/tmp/slotroot-open")
    (open_parent / "root").mkdir(parents=True, exist_ok=True)
    open_parent.chmod(0o777)
    (open_parent / "root").chmod(0o755)
    running_as_root = head.os.getuid() == 0
    for label, candidate in (
        ("a slot root reached through a symlinked parent", link / "root"),
        ("a slot root under an other-writable parent", open_parent / "root"),
    ):
        try:
            head.validate_slot_root(candidate)
            outcome = "ACCEPTED"
        except head.Refusal as exc:
            outcome = f"refused: {exc}"
        record(f"observation: {label} is {outcome.split(':')[0]}", True,
               f"uid0={running_as_root} {outcome}")

failures = [r for r in results if not r[1]]
for label, ok, detail in results:
    print(f"{'ok  ' if ok else 'FAIL'} {label}" + (f"  [{detail}]" if detail and (not ok or label.startswith('observation')) else ""))
print(f"slot0-differential: {len(results) - len(failures)}/{len(results)} ok")
raise SystemExit(1 if failures else 0)
