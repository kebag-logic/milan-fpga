Run from a clean detached clone of 79571006b803a4ab4af65358f0d87bc3af73180e, with its history available. Supply an empty packet directory and the scoped 5.050 executable. No remote write is required.

1. Run `python3 focused.py --repo SOURCE --packet PACKET --simulator EXECUTABLE`. It extracts base/head under scratch, runs the expected red reproduction, the head golden and six controls, and focused documentation gates. Its generated wrapper limits compiler parallelism to two; the campaign uses four workers.
2. Run `python3 plant_check.py --repo SOURCE --packet PACKET` for the 476 + 96 planting check.
3. Run `python3 extra_boundaries.py --packet PACKET --simulator EXECUTABLE` after step 1. It builds only a disposable copy, with extra identity and boundary assertions.
4. Run `python3 identity_and_area.py --repo SOURCE --packet PACKET --simulator EXECUTABLE` to verify source/index identity, merge equivalence and the public area table arithmetic.
5. For the complete documentation check, create a dependency environment under PACKET/scratch, install wavedrom==2.0.3.post3 there, place it first in PATH, and run `TMPDIR=PACKET/scratch make -j16 check` in SOURCE. The diagram CLI must also be available. No global install is needed.

Run all coordinators in the foreground. Red unit rc 2 and mutant rc 2 are expected only with their completed check tallies and named failures. The campaign, planting, extended golden, identity and documentation coordinators must return zero. Raw reviewer setup attempts are excluded from the publication manifest.
