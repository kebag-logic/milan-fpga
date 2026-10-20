[A656] REVIEW READY (round 2, PR #768)
Commit: `8000520cc12ec5d107a2a67f8ba3d6134b87d2b5` (branch `637-map-records`, local, not pushed; dev `e26f1816` merged by merge commit `8a7e6beb`, then 8 commits; processor pin `2cbed0a9` unchanged)

Answers R669-1 and R670-1 under the round-2 assignment (PR #768 comment 6269988820).

Changed:
- Status (R670-F1, R669-F1, R669-S2): PP_STAT `[1]` busy, `[2]` done, `[3]` fail and `[7]` blank are composed in the parent with the map restore (`milan_datapath.sv` `pp_stat_*_w`). Busy covers it, done waits for its end, fail adds its roll-back, and blank needs it to have validated no record and failed nowhere. The processor's interface is unchanged.
- Cross-port ownership, fixed per the ruling (R670-F2, R669-F5): the restore runs in three stages. Stage 0 takes down every dynamic port's reset set, stage 1 reads each record once and ADDs the saved set, and stage 2 puts back the reset sets of erased, unframed or refused ports. A refused take-down or put-back rolls every map back (Milan v1.2 5.3.10.1; D3 6.2, 8.6).
- One-pass transaction, per the ruling (R670-F6): D3 section 3 rule 7 carries the amendment. 18.4 states the transaction, its map-only boundary, and its validation obligation for one pass and its deadlines.
- Restore arms (R670-F3, R669-F2): committed checks on the real restore path, with a killing control each, for put-back, holes, layout, id, ranges and conflicting keys (both directions where the field exists), a D3 pass-0 abort, the legal maximum, and conflicting keys across ports. Two new `milan_dp` legs: `maprec8` covers transfers between the 8x8's output ports in both port orders and a cyclic swap, graded on GET_AUDIO_MAP, key ownership and the capture RAM. `maprec4` covers the 4x4's first, last and emptied input ports and a put-back under a narrower format.
- Gates (R670-F4, R669-F3/F4): the `mrec_offset_i` literal carries its rationale; the `[MAPREC]` code is split into functions under 100 lines; no ratchet moved. `sw/firmware/ctrl/README.md` states the boundary's 165 pin controls (the two new legs add four).
- Docs (R670-F5, R669-F6): REGISTER_MAP PP_STAT `[4]` names the parent map writer (#637), with three attempts 500 ms apart and reset-sticky. `[1]`, `[2]`, `[3]` and `[7]` describe the composition.
- Residue: R669-R1 to R3 applied; R669-S1 is one sentence in 18.4.
- No processor register-map, top-level port or parameter change (`git diff 63a187e1 8000520c -- hdl` adds or removes no port or parameter line).

Validation (all rc 0, unpiped, clean clones):
- `scripts/run_all_suites.sh` at `8000520c`, as the runner's four shards run one after another (`--shard <i>/4`, i = 0 to 3; a host reset had cut the single run): rc 0 each, 63 of 63 suites, 2,187,192 checks, 0 failures, the four declared `tsn_fuzz` skips; inside it dynmap 589/0, maprec8 219/0, maprec4 137/0.
- `make -C tb/verilator/milan_dp dynmap-mutants DYNMAP_MUTANT_JOBS=4` at `af5eefc6` (`tb/` and `hdl/` equal the head's): 60 of 60 planted controls caught (23 new) and the five clean legs pass: dynmap 589/0, maprec8 219/0 and maprec4 137/0. The listener leg needs `make -C tb/verilator/milan_dp_render tdm8render-build` first, as on dev.
- Both reviews' probes rerun at `af5eefc6`: R670's status probe 131/0 (3 failures at round 1); R670's two controls each fail exactly their three targeted checks; R669's six restore-arm probes, all of which survived at round 1, are all caught.
- docs.yml: 95 commands at the head plus both builder legs. rtl-fast: both firmware-boundary legs at the head; lint, bdd, yosys-elaboration, census, firmware-unit and the three firmware mutation campaigns at `af5eefc6` (which differs from the head by one README line, read only by the boundary gate).
- `syn/yosys/run.sh` rc 0 (`af5eefc6`); `xvlog_gate.py --check` and `--selftest` rc 0 (`887b6bf2`, whose `hdl/` equals the head's).
- route-1x1 at `887b6bf2`: LUT +260, FF +258 over base (DR4 maps ceiling 1,250 / 600), WNS +0.065 ns, WHS +0.036 ns, route complete. ooc-1x1 +52 / +2; ooc-8x8 +71 / 0.
- The PR body separates executed, skipped and cancelled work.

Acceptance criteria:
- Assignment items 1 to 6, the merge and the gate reruns: met (HANDOFF and PR body map each to its evidence).
- Issue items 1 to 4 and #763's empty and non-default lists: met.
- NOT met: the on-board cold cycle. This lane has no bench access, so the PR says "Relates to #637".

Open risks/questions:
- At 8x8 (non-shipping) the three stages hold the faces about 13,700 clocks, past the processor's 4,096-clock gather watchdog. A command held there is answered by the watchdog, never with a half-restored map. This stays open with D3 18.4's other 8x8 obligations.
- The 1x1 hold is 598 to 672 clocks on a zero-latency window model; DDR latency on the board adds to it.
- `dynmap-mutants` does not build the render suite its listener leg reads, as on dev. Making the target build it is proposed, not done.
- Interpreters: the sweep and the boundary legs ran under CPython 3.14.8 (`os.pidfd_open`; `migen`), the other Python gates under 3.12.3.
