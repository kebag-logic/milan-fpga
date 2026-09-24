#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Live proof for parallel act replay slots (#532). Run it with an AUDITED
# runner install, never with a candidate worktree's own copy of the runner:
# see "Parallel replay slots" in docs/testing/CI_WORKFLOWS.md.
#
# In order, it proves:
#   1. per-slot interruption cleanup: --interrupt-selftest in slot A passes
#      and prints the runner's own teardown line for slot A;
#   2. the serial references: PR A, then PR B, in the serial slot (default 0,
#      today's replay); each must complete (see `complete`);
#   3. isolation: PR A in slot A and PR B in slot B, started together. Both
#      must hold their slots at the same time and each must complete with the
#      verdict of its serial reference;
#   4. the isolation control, run from inside each slot while its replay
#      holds it: a listener container on a new bridge network of the default
#      daemon, and the port it publishes on that network's gateway, must both
#      be refused, while a public name resolves and answers on 443. The same
#      probe from the host's own namespace must reach both targets, so the
#      refusal is the slot firewall's and not a dead target's;
#   5. the collision control with isolation: PR A and PR B in slot A at once;
#      the second must be refused on the slot lock while the first still
#      holds the slot and then completes with its serial verdict;
#   6. the collision control without isolation: the same on slot 0, the one
#      shared default daemon, where the second must be refused on act's
#      global tool-cache or job-volume names. This is the collision the slots
#      exist to remove, so it is always part of the proof.
#
# A run completes only with exit 0 and a PASS line for every selected
# workflow in order, or exit 1 with PASS lines up to the first workflow that
# FAILED and that FAILED line (the runner stops at the first failure). A
# refusal or a signal never completes, so a proof built on runs that never
# executed a workflow fails. PROVED is printed, with exit 0, only when all ten
# checks recorded PASS. Each run's log, status and verdict land in --logs,
# with a summary in --logs/SUMMARY and the probe answers in isolation.log.
#
# `--selftest` grades these checks offline against a stand-in runner and a
# stand-in sudo (Docker CLI, namespace entry and probes) in a scratch
# directory: no Docker, no privilege, no network. It passes only when the
# honest case PROVES, each broken case FAILS on the check meant to catch it,
# and a bad slot pair, runner install or log directory is refused (exit 2)
# before any check runs.
set -euo pipefail

PROOF_LABEL=org.kebag-logic.milan-act-slot-proof
# The workflows the runner selects by default, in its own order (WORKFLOWS in
# scripts/act_ci.py); a runner that adds one fails this proof until it is here.
DEFAULT_WORKFLOWS=(docs elaborate rtl-fast rtl-full)
# A connect probe: one `NAME=reached|refused` line per NAME,HOST,PORT; a name
# that does not resolve, a refusal and a timeout are all `refused`.
PROBE='import socket, sys
for spec in sys.argv[1:]:
    name, host, port = spec.split(",")
    try:
        socket.create_connection((host, int(port)), timeout=10).close()
        print(f"{name}=reached")
    except OSError:
        print(f"{name}=refused")'
LISTENER='import socket
server = socket.create_server(("0.0.0.0", 8080))
while True:
    server.accept()[0].close()'

usage() {
  cat <<'EOF'
usage: act_slot_proof.sh --runner ABS --sha256 HEX --act-bin ABS --logs DIR
         --pr-a N --worktree-a DIR --pr-b N --worktree-b DIR
         [--slot-a N] [--slot-root-a DIR] [--slot-b N] [--slot-root-b DIR]
         [--serial-slot N] [--repo OWNER/REPO] [--workflow NAME]...
         [--probe-image IMAGE] [--probe-name HOST] [--poll-seconds S]
       act_slot_proof.sh --selftest
EOF
}

runner="" sha="" act_bin="" logs="" repo="kebag-logic/milan-fpga"
pr_a="" worktree_a="" pr_b="" worktree_b=""
slot_a=1 slot_b=2 serial_slot=0 poll_seconds=5
slot_root_a=/var/lib/milan-act-ci slot_root_b=/var/lib/milan-act-ci
probe_image=catthehacker/ubuntu:full-latest probe_name=github.com
workflow_args=() workflows=()
target="" target_ip="" target_gateway="" target_port=""

parse_arguments() {
  while [ "$#" -gt 0 ]; do
    if [ "$#" -lt 2 ]; then usage >&2; exit 2; fi
    case "$1" in
      --runner) runner=$2 ;;
      --sha256) sha=$2 ;;
      --act-bin) act_bin=$2 ;;
      --logs) logs=$2 ;;
      --repo) repo=$2 ;;
      --pr-a) pr_a=$2 ;;
      --worktree-a) worktree_a=$2 ;;
      --pr-b) pr_b=$2 ;;
      --worktree-b) worktree_b=$2 ;;
      --slot-a) slot_a=$2 ;;
      --slot-b) slot_b=$2 ;;
      --slot-root-a) slot_root_a=$2 ;;
      --slot-root-b) slot_root_b=$2 ;;
      --serial-slot) serial_slot=$2 ;;
      --probe-image) probe_image=$2 ;;
      --probe-name) probe_name=$2 ;;
      --poll-seconds) poll_seconds=$2 ;;
      --workflow) workflow_args+=(--workflow "$2"); workflows+=("$2") ;;
      *) usage >&2; exit 2 ;;
    esac
    shift 2
  done
  for required in "$runner" "$sha" "$act_bin" "$logs" "$pr_a" "$worktree_a" \
    "$pr_b" "$worktree_b"; do
    if [ -z "$required" ]; then usage >&2; exit 2; fi
  done
  for number in "$slot_a" "$slot_b" "$serial_slot"; do
    case "$number" in ''|*[!0-9]*) echo "slots are numbers: $number" >&2; exit 2 ;; esac
  done
  if [ "$slot_a" -eq "$slot_b" ] || [ "$slot_a" -eq 0 ] || [ "$slot_b" -eq 0 ]; then
    echo "slots A and B must be two distinct isolated slots" >&2
    exit 2
  fi
}

verify_runner() {
  local actual
  actual=$(sha256sum "$runner" | cut -d' ' -f1)
  if [ "$actual" != "$sha" ] || [ -n "$(find "$runner" -maxdepth 0 -perm /0222)" ] \
    || { [ "$(id -u)" -ne 0 ] && [ -w "$runner" ]; }; then
    echo "runner $runner is not the audited read-only install $sha" >&2
    exit 2
  fi
  mkdir -p "$logs"
  if [ -n "$(ls -A "$logs")" ]; then
    echo "log directory $logs is not empty" >&2
    exit 2
  fi
}

record() {
  printf '%s %s\n' "$1" "$2" | tee -a "$logs/SUMMARY"
}

# slot_root SLOT: the slot root the command line gave that slot.
slot_root() {
  if [ "$1" -eq "$slot_a" ]; then echo "$slot_root_a"; else echo "$slot_root_b"; fi
}

# selected_workflows: the workflows every run executes, in the runner's order.
selected_workflows() {
  if [ "${#workflows[@]}" -eq 0 ] || [ "${workflows[*]}" = all ]; then
    printf '%s\n' "${DEFAULT_WORKFLOWS[@]}"
  else
    printf '%s\n' "${workflows[@]}" | awk '!seen[$0]++'
  fi
}

# replay LABEL PR WORKTREE SLOT: one PR run; its log, status and verdict.
replay() {
  local label=$1 pr=$2 worktree=$3 slot=$4 status
  local -a slot_args=()
  if [ "$slot" -ne 0 ]; then slot_args=(--slot "$slot" --slot-root "$(slot_root "$slot")"); fi
  if (cd "$worktree" && python3 -I "$runner" --pr "$pr" --repo "$repo" \
    --worktree "$worktree" --trusted-install-sha256 "$sha" --act-bin "$act_bin" \
    --sudo "${workflow_args[@]}" "${slot_args[@]}") >"$logs/$label.log" 2>&1; then
    status=0
  else
    status=$?
  fi
  {
    printf 'exit %s\n' "$status"
    sed -n -E 's/^act-ci: ([a-z-]+): (PASS|FAILED).*/\1 \2/p' "$logs/$label.log"
  } >"$logs/$label.verdict"
  printf '%s\n' "$status" >"$logs/$label.status"
}

# complete LABEL: whether run LABEL executed its workflows: exit 0 with a PASS
# for every selected workflow in order, or exit 1 with PASS for those before
# the first failure and FAILED for it. A refusal or a signal never completes.
complete() {
  local actual expected="" name
  actual=$(cat "$logs/$1.verdict")
  while IFS= read -r name; do
    if [ "$actual" = "exit 1$expected"$'\n'"$name FAILED" ]; then return 0; fi
    expected+=$'\n'"$name PASS"
  done < <(selected_workflows)
  [ "$actual" = "exit 0$expected" ]
}

# same_verdict LABEL REFERENCE: whether two runs reached identical verdicts.
same_verdict() {
  cmp -s "$logs/$1.verdict" "$logs/$2.verdict"
}

# reference LABEL: record whether serial reference LABEL completed.
reference() {
  if complete "$1"; then
    record PASS "$1 completed: $(tr '\n' ' ' <"$logs/$1.verdict")"
  else
    record FAIL "$1 did not complete its workflows: $(tr '\n' ' ' <"$logs/$1.verdict")"
  fi
}

# compare LABEL REFERENCE: record whether LABEL completed with REFERENCE's verdict.
compare() {
  if ! complete "$1"; then
    record FAIL "$1 did not complete its workflows: $(tr '\n' ' ' <"$logs/$1.verdict")"
  elif same_verdict "$1" "$2"; then
    record PASS "$1 = $2"
  else
    record FAIL "$1 != $2"
  fi
}

# ended LABEL: whether run LABEL has printed a verdict or a refusal. A run that
# completes prints every verdict before its slot or Docker boundary is torn
# down, so a run whose marker is printed and which has not ended holds its slot.
ended() {
  grep -q -E '^act-ci: ([a-z-]+: (PASS|FAILED)|REFUSED)' "$logs/$1.log" 2>/dev/null
}

# await_holder LABEL SLOT: block until run LABEL holds SLOT; fail once it has ended.
await_holder() {
  local label=$1 slot=$2 marker="act-ci: running " polls=0
  if [ "$slot" -ne 0 ]; then marker="act-ci: slot $slot: own daemon"; fi
  while [ "$polls" -lt 720 ]; do
    if grep -q -F "$marker" "$logs/$label.log" 2>/dev/null; then return 0; fi
    if [ -e "$logs/$label.status" ]; then return 1; fi
    sleep "$poll_seconds"
    polls=$((polls + 1))
  done
  return 1
}

# interrupt_gate: the live interruption gate in slot A, torn down by the runner itself.
interrupt_gate() {
  local log=$logs/interrupt-$slot_a.log
  if (cd "$logs" && python3 -I "$runner" --interrupt-selftest --act-bin "$act_bin" \
    --sudo --slot "$slot_a" --slot-root "$slot_root_a") >"$log" 2>&1 \
    && grep -q '^interrupt-selftest: PASS ' "$log" \
    && grep -q "^interrupt-selftest: slot $slot_a: " "$log"; then
    record PASS "interrupt self-test in slot $slot_a, whose slot the runner then tore down and proved absent"
  else
    record FAIL "interrupt self-test in slot $slot_a: see interrupt-$slot_a.log"
  fi
}

# start_target: the isolation target, a listener container on a new bridge
# network of the default daemon with a port published on that network's
# gateway only; false when any step fails.
start_target() {
  target=milan-act-slot-proof-$(od -An -N6 -tx1 /dev/urandom | tr -d ' \n')
  sudo -n docker network create --driver bridge --label "$PROOF_LABEL=$target" "$target" \
    >/dev/null || return 1
  target_gateway=$(sudo -n docker network inspect \
    --format '{{range .IPAM.Config}}{{.Gateway}}{{end}}' "$target") || return 1
  sudo -n docker run --detach --pull never --name "$target" --network "$target" \
    --label "$PROOF_LABEL=$target" --publish "$target_gateway::8080" \
    --entrypoint python3 "$probe_image" -c "$LISTENER" >/dev/null || return 1
  target_ip=$(sudo -n docker inspect \
    --format "{{(index .NetworkSettings.Networks \"$target\").IPAddress}}" "$target") || return 1
  target_port=$(sudo -n docker port "$target" 8080/tcp | sed -n '1s/.*://p') || return 1
  printf 'target %s: container %s:8080, published %s:%s\n' "$target" "$target_ip" \
    "$target_gateway" "$target_port" >>"$logs/isolation.log"
  [ -n "$target_gateway" ] && [ -n "$target_ip" ] && [ -n "$target_port" ]
}

# remove_target: remove the isolation target and prove it absent.
remove_target() {
  local containers networks
  if [ -z "$target" ]; then return 0; fi
  sudo -n docker rm --force "$target" >/dev/null 2>&1 || true
  sudo -n docker network rm "$target" >/dev/null 2>&1 || true
  containers=$(sudo -n docker ps --all --quiet --filter "label=$PROOF_LABEL=$target") \
    || containers=unknown
  networks=$(sudo -n docker network ls --quiet --filter "label=$PROOF_LABEL=$target") \
    || networks=unknown
  if [ -n "$containers$networks" ]; then
    record FAIL "isolation target not proved absent after its removal: $target"
  fi
  target=""
}

# isolation SLOT: the isolation control from inside SLOT, set against the host.
isolation() {
  local slot=$1 inside outside
  local -a targets=("container,$target_ip,8080" "published,$target_gateway,$target_port")
  inside=$(sudo -n nsenter "--net=/run/netns/milan-act-slot-$slot" -- env -i PATH=/usr/bin:/bin \
    python3 -I -c "$PROBE" "${targets[@]}" "internet,$probe_name,443" 2>&1 | tr '\n' ' ') || true
  outside=$(sudo -n env -i PATH=/usr/bin:/bin python3 -I -c "$PROBE" "${targets[@]}" 2>&1 \
    | tr '\n' ' ') || true
  printf 'slot %s: %s\nhost: %s\n' "$slot" "$inside" "$outside" >>"$logs/isolation.log"
  if [ "$inside" = "container=refused published=refused internet=reached " ] \
    && [ "$outside" = "container=reached published=reached " ]; then
    record PASS "isolation slot $slot: the default daemon's container and published port were refused, $probe_name:443 answered, and the host reached both targets"
  else
    record FAIL "isolation slot $slot: slot saw '$inside', host saw '$outside' (see isolation.log)"
  fi
}

# parallel: PR A in slot A and PR B in slot B together, with the isolation control.
parallel() {
  local pid_a pid_b slot
  replay parallel-a "$pr_a" "$worktree_a" "$slot_a" &
  pid_a=$!
  replay parallel-b "$pr_b" "$worktree_b" "$slot_b" &
  pid_b=$!
  if await_holder parallel-a "$slot_a" && await_holder parallel-b "$slot_b" \
    && ! ended parallel-a && ! ended parallel-b; then
    record PASS "overlap: slots $slot_a and $slot_b were held at the same time"
    for slot in "$slot_a" "$slot_b"; do
      if [ -n "$target" ]; then isolation "$slot"; else record FAIL "isolation slot $slot: no target"; fi
    done
  else
    record FAIL "overlap: the parallel runs never held slots $slot_a and $slot_b at the same time"
  fi
  wait "$pid_a" "$pid_b"
  compare parallel-a serial-a
  compare parallel-b serial-b
}

# collide SLOT REFUSAL: A holds SLOT, B arrives while A holds it and must be refused.
collide() {
  local slot=$1 refusal=$2 holder rival_early rival_status
  replay "collide-$slot-holder" "$pr_a" "$worktree_a" "$slot" &
  holder=$!
  if ! await_holder "collide-$slot-holder" "$slot"; then
    wait "$holder"
    record FAIL "collision slot $slot: the holder never held the slot"
    return
  fi
  replay "collide-$slot-rival" "$pr_b" "$worktree_b" "$slot"
  rival_early=1
  if ended "collide-$slot-holder"; then rival_early=0; fi
  wait "$holder"
  rival_status=$(cat "$logs/collide-$slot-rival.status")
  if [ "$rival_early" -eq 1 ] && [ "$rival_status" = 2 ] \
    && grep -q -E "$refusal" "$logs/collide-$slot-rival.log" \
    && complete "collide-$slot-holder" && same_verdict "collide-$slot-holder" serial-a; then
    record PASS "collision slot $slot: the rival was refused while the holder held the slot, and the holder kept its serial verdict"
  else
    record FAIL "collision slot $slot: see collide-$slot-*.log"
  fi
}

prove() {
  verify_runner
  trap remove_target EXIT
  interrupt_gate
  replay serial-a "$pr_a" "$worktree_a" "$serial_slot"
  reference serial-a
  replay serial-b "$pr_b" "$worktree_b" "$serial_slot"
  reference serial-b
  if ! start_target; then
    record FAIL "isolation target: it could not be started on the default daemon (see isolation.log)"
  fi
  parallel
  remove_target
  collide "$slot_a" "is in use by another runner invocation"
  collide 0 "act-toolcache|already exist"
  if grep -q '^FAIL' "$logs/SUMMARY" || [ "$(grep -c '^PASS' "$logs/SUMMARY")" -ne 10 ]; then
    exit 1
  fi
  record PROVED "every slot proof held"
}

# fake_runner_source: the stand-in runner --selftest grades the proof against.
fake_runner_source() {
  cat <<'EOF'
#!/usr/bin/env python3
"""Stand-in runner: takes slots with real flocks, prints the runner's lines, reaches scripted verdicts."""
import fcntl, os, pathlib, signal, sys, time
args = sys.argv[1:]
state = pathlib.Path(os.environ["FAKE_STATE"])
faults = os.environ.get("FAKE_FAULTS", "").split(",")
summary = state.parent / "logs" / "SUMMARY"  # the graded proof's, beside FAKE_STATE
def value(flag, default):
    return args[args.index(flag) + 1] if flag in args else default
def await_judgment():
    """Wait until the proof has failed the overlap or recorded both slots' isolation controls."""
    for _ in range(1200):
        lines = summary.read_text().splitlines() if summary.exists() else []
        if any(line.startswith("FAIL overlap") for line in lines) or sum(
                line.startswith(("PASS isolation slot ", "FAIL isolation slot ")) for line in lines) >= 2:
            return
        time.sleep(0.05)
slot = value("--slot", "0")
if "--interrupt-selftest" in args:
    if "interrupt-no-pass" not in faults:
        print("interrupt-selftest: PASS (stand-in)")
    if "interrupt-no-slot" not in faults:
        print(f"interrupt-selftest: slot {slot}: its daemon, uplink, firewall table, slice "
              "and namespace were then torn down and proved absent")
    if "interrupt-refused" in faults:
        print("act-ci: REFUSED: replay slot teardown failed", file=sys.stderr)
        sys.exit(2)
    sys.exit(0)
workflows = [args[i + 1] for i, word in enumerate(args) if word == "--workflow"]
workflows = workflows or ["docs", "elaborate", "rtl-fast", "rtl-full"]
pr, hold = value("--pr", "0"), float(os.environ.get("FAKE_HOLD", "3"))
with open(state / f"runs-{slot}-{pr}", "a+") as runs:
    fcntl.flock(runs, fcntl.LOCK_EX)
    runs.write("x")
    runs.seek(0)
    run_number = len(runs.read())
if pr == "23" and slot == "1" and "rival-other-refusal" in faults:
    print("act-ci: REFUSED: act version check failed", file=sys.stderr)
    sys.exit(2)
if pr == "23" and slot == "0" and run_number == 2 and "rival0-other-refusal" in faults:
    print("act-ci: REFUSED: action clone failed", file=sys.stderr)
    sys.exit(2)
if pr == "23" and slot == "1" and "late-refusal" in faults:
    time.sleep(hold + 1)
    print("act-ci: REFUSED: replay slot 1 is in use by another runner invocation", file=sys.stderr)
    sys.exit(2)
time.sleep(0.2)
# The parallel runs: A is PR 21's first run in slot 1, and B the only run in slot 2.
run_a, run_b = pr == "21" and slot == "1" and run_number == 1, slot == "2"
if (run_a and "a-never-holds" in faults) or (run_b and "b-never-holds" in faults):
    os.kill(os.getpid(), signal.SIGKILL)
for waits, first in ((run_b, "a-refused-first"), (run_a, "b-refused-first")):
    if waits and first in faults:
        for _ in range(600):
            if (state / first).exists():
                break
            time.sleep(0.05)
if "serialize" in faults:
    queue = open(state / "queue.lock", "w")
    fcntl.flock(queue, fcntl.LOCK_EX)
lock = open(state / f"lock-{slot}", "w")
unlocked = "nolock" in faults or ("nolock0" in faults and slot == "0")
try:
    if not unlocked:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
except BlockingIOError:
    print("act-ci: REFUSED: " + (f"replay slot {slot} is in use by another runner invocation"
          if slot != "0" else "shared Docker volume 'act-toolcache' already exists"), file=sys.stderr)
    sys.exit(1 if "rival-wrong-status" in faults else 2)
if slot != "0":
    (state / f"netns-{slot}").touch()
    if "slot-unannounced" not in faults:
        print(f"act-ci: slot {slot}: own daemon unix:///run/milan-act-slot-{slot}/docker.sock", flush=True)
try:
    for refuses, first in ((run_a, "a-refused-first"), (run_b, "b-refused-first")):
        if refuses and first in faults:
            # Refused before the other run takes its slot, and alive until judged,
            # so the proof sees this run's marker before its exit status.
            print("act-ci: REFUSED: action clone failed", file=sys.stderr, flush=True)
            (state / first).touch()
            await_judgment()
            sys.exit(2)
    print(f"act-ci: running {workflows[0]} (stand-in)", flush=True)
    # A run that announced its isolated slot holds it until the proof has judged
    # the parallel runs, so no check races its end. Serialized runs cannot overlap
    # and hold for FAKE_HOLD alone; the collisions come after the judgment.
    if slot != "0" and "slot-unannounced" not in faults and "serialize" not in faults:
        await_judgment()
    time.sleep(hold)
    if "refuse" in faults:
        print("act-ci: REFUSED: action clone failed", file=sys.stderr)
        sys.exit(2)
    broken = "parallel-break" in faults or ("holder-break" in faults and run_number == 2)
    for index, name in enumerate(workflows):
        if "partial" in faults and index == 1:
            sys.exit(0)
        if (pr == "22" and index == 1) or (broken and slot == "1") or (
                run_b and "parallel-break-b" in faults):
            print(f"act-ci: {name}: FAILED (1)", file=sys.stderr, flush=True)
            sys.exit(2 if "failed-refused" in faults else 1)
        print(f"act-ci: {name}: PASS at {'a' * 40}", flush=True)
    if "pass-then-refuse" in faults:
        print("act-ci: REFUSED: replay slot teardown failed", file=sys.stderr)
        sys.exit(2)
finally:
    (state / f"netns-{slot}").unlink(missing_ok=True)
EOF
}

# fake_sudo_source: the stand-in `sudo -n` for the Docker CLI, namespace entry and probes.
fake_sudo_source() {
  cat <<'EOF'
#!/usr/bin/env python3
"""Stand-in sudo -n: answers the proof's Docker, nsenter and probe commands from a state directory."""
import os, pathlib, sys
state = pathlib.Path(os.environ["FAKE_STATE"])
faults = os.environ.get("FAKE_FAULTS", "").split(",")
args = sys.argv[1:]
if args[:1] != ["-n"]:
    sys.exit("stand-in sudo: only non-interactive -n is expected")
args = args[1:]
live = state / "target"
def answers(specs, inside, slot=""):
    """What a probe of the given specs sees from inside a slot or from the host."""
    alive = live.exists() and "target-dead" not in faults
    for spec in specs:
        name, host, port = spec.split(",")
        known = {("container", "172.30.0.2", "8080"), ("published", "172.30.0.1", "32768")}
        leaks = {f"slot-reaches-{name}", f"slot{slot}-reaches-{name}"}
        if name == "internet":
            reached = host == "github.com" and port == "443" and "slot-misses-internet" not in faults
        elif inside:
            reached = alive and not leaks.isdisjoint(faults) and (name, host, port) in known
        else:
            reached = alive and f"host-misses-{name}" not in faults and (name, host, port) in known
        print(f"{name}={'reached' if reached else 'refused'}")
if args[0] == "docker":
    verb = " ".join(args[1:3])
    if verb == "network create":
        (state / "network").touch()
        print("n" * 64)
    elif verb == "network inspect":
        print("172.30.0.1")
    elif args[1] == "run":
        assert "--publish" in args and "172.30.0.1::8080" in args and "never" in args
        if "target-unstartable" in faults:
            sys.exit("docker: Error response from daemon: stand-in refuses the listener")
        live.touch()
        print("c" * 64)
    elif args[1] == "inspect":
        print("172.30.0.2")
    elif args[1] == "port":
        print("172.30.0.1:32768")
    elif args[1] == "rm" and "target-survives" not in faults:
        live.unlink(missing_ok=True)
    elif verb == "network rm" and "network-survives" not in faults:
        (state / "network").unlink(missing_ok=True)
    elif args[1] == "ps":
        if "container-query-fails" in faults:
            sys.exit("docker: Cannot connect to the Docker daemon (stand-in)")
        print("c" * 12 if live.exists() else "", end="")
    elif verb == "network ls":
        if "network-query-fails" in faults:
            sys.exit("docker: Cannot connect to the Docker daemon (stand-in)")
        print("n" * 12 if (state / "network").exists() else "", end="")
    sys.exit(0)
if args[0] == "nsenter":
    slot = args[1].rsplit("-", 1)[1]
    if not (state / f"netns-{slot}").exists():
        sys.exit(f"nsenter: cannot open {args[1]}: No such file or directory")
    answers(args[args.index("-c") + 2:], inside=True, slot=slot)
    sys.exit(0)
if args[0] == "env":
    answers(args[args.index("-c") + 2:], inside=False)
    sys.exit(0)
sys.exit(f"stand-in sudo: unexpected command {args}")
EOF
}

# selftest_case SCRATCH NAME FAULTS PR_B STATUS LINE: one graded run of this proof.
# LINE is looked for in the SUMMARY, or for STATUS 2 in the proof's own output,
# since a status-2 case must be refused before any check records anything.
selftest_case() {
  local scratch=$1 name=$2 faults=$3 pr_b_case=$4 want_status=$5 want_line=$6 status=0
  local case_dir=$scratch/$name runner=$scratch/runner.py digest slot_a_case=1 slot_b_case=2
  local graded=$case_dir/logs/SUMMARY
  mkdir -p "$case_dir/state" "$case_dir/wt-a" "$case_dir/wt-b"
  digest=$(sha256sum "$runner" | cut -d' ' -f1)
  case ",$faults," in
    *,wrong-digest,*)
      digest=$(printf 'another runner' | sha256sum | cut -d' ' -f1) ;;
    *,writable-runner,*)
      runner=$case_dir/runner.py
      cp "$scratch/runner.py" "$runner"
      chmod 0464 "$runner" ;;
    *,logs-not-empty,*) mkdir "$case_dir/logs" && : >"$case_dir/logs/stale.log" ;;
    *,slot-a-word,*) slot_a_case=one ;;
    *,same-slots,*) slot_b_case=1 ;;
    *,slot-a-zero,*) slot_a_case=0 ;;
    *,slot-b-zero,*) slot_b_case=0 ;;
  esac
  FAKE_STATE=$case_dir/state FAKE_FAULTS=$faults PATH="$scratch/bin:$PATH" \
    bash "$0" --runner "$runner" --sha256 "$digest" \
    --act-bin /nonexistent/act --logs "$case_dir/logs" --pr-a 21 --worktree-a "$case_dir/wt-a" \
    --pr-b "$pr_b_case" --worktree-b "$case_dir/wt-b" --slot-a "$slot_a_case" \
    --slot-b "$slot_b_case" --poll-seconds 0.05 >"$case_dir/out" 2>&1 || status=$?
  if [ "$want_status" = 2 ]; then graded=$case_dir/out; fi
  if [ "$status" = "$want_status" ] && grep -q -F -- "$want_line" "$graded" \
    && { [ "$want_status" != 0 ] || [ "$(grep -c '^PASS' "$graded")" -eq 10 ]; } \
    && { [ "$want_status" != 2 ] || [ ! -e "$case_dir/logs/SUMMARY" ]; }; then
    echo "  ok   $name: exit $status with '$want_line'"
  else
    echo "  FAIL $name: exit $status, wanted $want_status with '$want_line'"
    sed 's/^/       | /' "$case_dir/logs/SUMMARY" 2>/dev/null || true
    return 1
  fi
}

# selftest: grade every check of this proof against the stand-ins, in parallel.
selftest() {
  local scratch failures=0 name faults pr_b_case want_status want_line
  local -a pids=() names=()
  scratch=$(mktemp -d "${TMPDIR:-/tmp}/act-slot-proof-selftest.XXXXXX")
  mkdir "$scratch/bin"
  fake_runner_source >"$scratch/runner.py"
  fake_sudo_source >"$scratch/bin/sudo"
  chmod 0555 "$scratch/runner.py" "$scratch/bin/sudo"
  while IFS='|' read -r name faults pr_b_case want_status want_line; do
    selftest_case "$scratch" "$name" "$faults" "$pr_b_case" "$want_status" "$want_line" \
      >"$scratch/$name.result" 2>&1 &
    pids+=("$!")
    names+=("$name")
  done <<'EOF'
honest, where PR B fails its second workflow||22|0|PROVED every slot proof held
slot A is not a number|slot-a-word|23|2|slots are numbers: one
slots A and B are the same slot|same-slots|23|2|slots A and B must be two distinct isolated slots
slot A is slot 0|slot-a-zero|23|2|slots A and B must be two distinct isolated slots
slot B is slot 0|slot-b-zero|23|2|slots A and B must be two distinct isolated slots
the runner is not the recorded digest|wrong-digest|23|2|is not the audited read-only install
the runner install is group-writable|writable-runner|23|2|is not the audited read-only install
the log directory is not empty|logs-not-empty|23|2|is not empty
every run refuses after taking its slot|refuse|23|1|FAIL serial-a did not complete
a run stops before its last workflow|partial|23|1|FAIL serial-a did not complete
a run passes every workflow and is then refused|pass-then-refuse|23|1|FAIL serial-a did not complete
a run fails a workflow and is then refused|failed-refused|22|1|FAIL serial-b did not complete
a parallel run refuses like its serial reference|refuse|23|1|FAIL parallel-a did not complete
the interrupt gate ignores its slot|interrupt-no-slot|23|1|FAIL interrupt self-test in slot 1
the interrupt gate prints no PASS line|interrupt-no-pass|23|1|FAIL interrupt self-test in slot 1
the interrupt gate passes and is then refused|interrupt-refused|23|1|FAIL interrupt self-test in slot 1
slot A changes a verdict|parallel-break|23|1|FAIL parallel-a != serial-a
slot B changes a verdict|parallel-break-b|23|1|FAIL parallel-b != serial-b
the parallel runs never overlap|serialize|23|1|FAIL overlap
neither run reports its own slot daemon|slot-unannounced|23|1|FAIL overlap
run A dies before taking slot A while run B holds slot B|a-never-holds|23|1|FAIL overlap
run B dies before taking slot B while run A holds slot A|b-never-holds|23|1|FAIL overlap
run A is refused after taking slot A, before run B takes slot B|a-refused-first|23|1|FAIL overlap
run B is refused after taking slot B, before run A takes slot A|b-refused-first|23|1|FAIL overlap
the isolation target cannot be started|target-unstartable|23|1|FAIL isolation target: it could not be started
a slot reaches the default daemon's container|slot-reaches-container|23|1|FAIL isolation slot 1
only slot B reaches the default daemon's container|slot2-reaches-container|23|1|FAIL isolation slot 2
a slot reaches the container's published port|slot-reaches-published|23|1|FAIL isolation slot 1
a slot cannot reach the probe name|slot-misses-internet|23|1|FAIL isolation slot 1
the isolation target is dead|target-dead|23|1|FAIL isolation slot 1
the host cannot reach the container|host-misses-container|23|1|FAIL isolation slot 1
the host cannot reach the published port while the container answers|host-misses-published|23|1|FAIL isolation slot 1
the isolation container survives removal|target-survives|23|1|FAIL isolation target not proved absent
the isolation network survives removal|network-survives|23|1|FAIL isolation target not proved absent
the isolation container cannot be queried after removal|container-query-fails|23|1|FAIL isolation target not proved absent
the isolation network cannot be queried after removal|network-query-fails|23|1|FAIL isolation target not proved absent
the slot lock is missing|nolock|23|1|FAIL collision slot 1
the rival is refused only after the holder left|late-refusal|23|1|FAIL collision slot 1
the rival is refused for another reason|rival-other-refusal|23|1|FAIL collision slot 1
the rival names the slot lock but exits 1|rival-wrong-status|23|1|FAIL collision slot 1
the collision holder changes its verdict|holder-break|23|1|FAIL collision slot 1
a collision holder refuses like its serial reference|refuse|23|1|FAIL collision slot 1
the shared daemon does not collide|nolock0|23|1|FAIL collision slot 0
the slot-0 rival is refused for neither the tool cache nor a job volume|rival0-other-refusal|23|1|FAIL collision slot 0
EOF
  for index in "${!pids[@]}"; do
    if ! wait "${pids[$index]}"; then failures=$((failures + 1)); fi
    cat "$scratch/${names[$index]}.result"
  done
  rm -rf "$scratch"
  if [ "$failures" -ne 0 ]; then
    echo "act_slot_proof selftest: $failures FAILURE(S)"
    return 1
  fi
  echo "act_slot_proof selftest: PASS (${#names[@]} cases)"
}

main() {
  if [ "$#" -eq 1 ] && [ "$1" = --selftest ]; then
    selftest
    return
  fi
  parse_arguments "$@"
  prove
}

main "$@"
