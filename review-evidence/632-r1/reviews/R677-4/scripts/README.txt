Scripts used by round R677-4 (run from the packet root, against a disposable copy of the head):
- merge_hunks.py <repo> d40e2ee8 e5b480a3 > receipts/merge/diff3_hunks.txt
  Lists every diff3 conflict region of the dev merge, with the words each side changed against the base.
- gmstep_delay_probe.py <tree> <out> 777
  Builds the clean gmstep leg and the control "the grandmaster change stops the talker for good" planted alone,
  through gmstep_mutants.py's own plant and recipe, and runs both at feed delay 777.
- launch.sh <name> <workdir> <command...>
  Runs one probe detached with its own log, rc and stamps (VERILATOR = the pinned Verilator 5.050 wrapper).
Commands run through launch.sh in the copy of 417ec528:
  rq_suite:     make -C tb/verilator/render_queue run odd
  rq_mutants:   make -C tb/verilator/render_queue mutants
  gmstep_delay: python3 -I scripts/gmstep_delay_probe.py <tree> <scratch>/gmdelay 777
Own gate run in the clone: python3 syn/ooc/pp_resource_gate.py check-baseline (receipts/resource/).
