#!/usr/bin/env python3
"""Reviewer probe on a disposable copy of tb/aecp_notify (never the clone).

usage: probe_midround.py TREE

Adds section PROBE-MR to the default build's run: C and D registered, X takes
then releases the lock with flags UNLOCK (1); while the UNLOCK round's first job
is presented, Y takes the lock (a solicited LOCK the block serves by withdrawal);
the round's remaining job and the next round are printed with their arguments.
The engine's E_LOCKUNS emits the job's arguments as flags @24 and reads
locked_id live from the registry (RG_STATE), so a job carrying 0000/0001 after
Y's LOCK becomes a frame with flags UNLOCK and locked_id Y.
Each edit must match exactly once, or the probe refuses.
"""
import sys
from pathlib import Path


def edit(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    n = text.count(old)
    if n != 1:
        sys.exit(f"REFUSED {path}: anchor occurs {n} times: {old[:60]!r}")
    path.write_text(text.replace(old, new, 1))


PROBE = r'''
void Harness::probe_midround() {
  constexpr uint64_t EID_X = 0x8888000000000008ull;
  constexpr uint64_t EID_Y = 0x9999000000000009ull;
  constexpr uint64_t EID_D2 = 0x4444000000000004ull;
  constexpr uint64_t MAC_D2 = 0x020000000004ull;
  warm_reset();
  d->uns_done_i = 0;
  now = 50000;
  register_row(EID_C, MAC_C, false);
  register_row(EID_D2, MAC_D2, false);
  auto show = [&](const char* tag, const UnsJob& j) {
    printf("PROBE-MR %s: ms %u kind %u mac %012llx args %04x/%04x\n", tag, j.ms,
           unsigned(j.kind), static_cast<unsigned long long>(j.mac), unsigned(j.arg1),
           unsigned(j.arg0));
  };
  const bool took = lock_op(EID_X, false, 0x00000000u);
  for (int k = 0; k < 2; ++k) {
    const UnsJob j = job_presented(now + WALK_MS);
    show("lock-round", j);
    if (j.ms != 0) (void)retire();
  }
  const bool released = lock_op(EID_X, true, 0x00000001u);
  const UnsJob u1 = job_presented(now + WALK_MS);
  show("unlock-round job 1 presented", u1);
  const bool ytook = lock_op(EID_Y, false, 0x00000000u);
  const UnsJob u1b = job_presented(now + WALK_MS);
  show("unlock-round job 1 after Y's LOCK", u1b);
  if (u1b.ms != 0) (void)retire();
  for (int k = 0; k < 4; ++k) {
    const UnsJob j = job_presented(now + WALK_MS);
    show("next", j);
    if (j.ms == 0) break;
    (void)retire();
  }
  printf("PROBE-MR premises: X took %d, X released %d, Y took %d\n", int(took),
         int(released), int(ytook));
  d->uns_done_i = 1;
}
'''


def main() -> None:
    sim = Path(sys.argv[1]) / "tb/aecp_notify/sim_main.cpp"
    edit(sim, "  void lock_flags();\n", "  void lock_flags();\n  void probe_midround();\n")
    edit(sim, "  lock_flags();\n  command_queue();\n",
         "  lock_flags();\n  probe_midround();\n  command_queue();\n")
    edit(sim, "// SC1: both rows have live probes.", PROBE + "\n// SC1: both rows have live probes.")
    print(f"probe midround planted in {sim}")


if __name__ == "__main__":
    main()
