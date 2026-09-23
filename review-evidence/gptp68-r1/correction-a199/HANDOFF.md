# A199 handoff: FPGA-gPTP #68 / PR #74, correction round

| Item | Value |
|---|---|
| Role | author, cleared context, correction round |
| Assignment | https://github.com/Mister-M-alt/FPGA-gPTP/issues/68#issuecomment-5794740482 |
| Policy implemented | https://github.com/Mister-M-alt/FPGA-gPTP/issues/68#issuecomment-5794731372 |
| Findings addressed | R258-1 F1 (BLOCKER), F2 (MAJOR), S1; R259-1 F1 (BLOCKER), both suggestions; the manager validation's two parent failures |
| Lane checkout | `$LANES/gptp68-step-policy`, branch `68-step-policy` |
| Head | `cbccf226068c107fb30764891c98b8d70c54d775`, tree `e8b9fa23fe5e1d5e3bd3ab1dd3c09196760a5063` |
| Parent of head | `77c34e904eba2446755d13e1bf4763d1652c3ca7` (the reviewed head; `origin/68-step-policy` still points there) |
| Commit | one-line subject, no trailers |
| Pushed | NO. No PR edit, no merge |
| Working tree | clean (`git status --porcelain` empty); only ignored build products present |
| Packet | `$REVIEWS/gptp68-a199-packet`: `PR-BODY.md` (proposed PR text), this file, `receipts/`, `scripts/`, `MANIFEST.sha256`. The output directory `$MANAGEMENT/2026-09-23/gptp68-a199` is a link to it |
| Scratch | deleted after the runs (the private parent clone and its disposable copies) |

## State in one paragraph

The SERVO leg:

- steps above 20 us at link-up and above 100 us once locked;
- keeps the servo locked across a grandmaster identity change;
- clamps the whole written trim to the +-200 ppm envelope, derived with the parent's own `PHC_ADJ_MAX_C` expression.

A new scratch cell `S_LOCK` holds the lock. It is re-armed to link-up by the asCapable rise (warm-reset safe), the Sync receipt timeout and becoming grandmaster.

Results at this head:

- The full donor gate passes, including the 26-mutant engine arm.
- In a private parent clone with the gitlink staged here, `gptp_shadow` (default target, run plus mutation arm) and `gptp_plane` are green, and the builder test passes, with one arm not run for environment only.
- The first review's wedge probes, and two new locked-slew probes, show zero PHC-history refusals and asCapable held. The trim rides exactly the envelope.

## Where each claim is proved

| Claim | Receipt |
|---|---|
| Simulator identity (wrapper and binary sha256, 5.050; system 5.052 not used) | `receipts/identity.log` |
| Full donor gate at head, exit 0, tree clean before and after | `receipts/gate-head.log`, `gate-head.segments`, `gate-head.exit` |
| Each required test fails when its rule is removed (matrix) | `receipts/policy-mutation-evidence-head.log` |
| The ROM is the documented rule, bit-identical in band where the old trim stayed in the envelope, and only SERVO/PDPAIR/SRTO/BECOME change content; the clamp equals the parent expression at 2 to 125 MHz | `receipts/rom-differential-head.log` |
| Old and new SHA-256 of every tracked and test-time image; changed word ranges | `receipts/rom-digests-head.log` |
| Why the slew input is no longer saturated | `receipts/slew-variants-model.log` |
| Parent `gptp_shadow` default target at head: 309/309 and arm PASS | `receipts/parent-gptp_shadow-default-head.log` |
| Parent `gptp_shadow` run at base and reviewed (contrast) | `receipts/parent-gptp_shadow-run-{base,reviewed}.log` |
| Parent `gptp_plane` at base, reviewed, head | `receipts/parent-gptp_plane-{base,reviewed,head}.log` |
| Parent builder test at head | `receipts/parent-test_builder-head.log` |
| Parent-bench probes at head (10 ms, 900 ms first, +-90 us locked, and +90 us continuing into the suite) and the +90 us probe at reviewed | `receipts/parent-probe-*-head.log`, `receipts/parent-probe-slewplus90us-reviewed.log` |
| Lane state, commit shape, diff stats | `receipts/lane-state-head.log` |

## Reproduce

```sh
. $REVIEWS/gptp68-a199-packet/scripts/env.sh   # pinned simulator first on PATH
S=$REVIEWS/gptp68-a199-packet/scripts
sh $S/identity.sh
for s in begin contract ucpu parser engine-run engine-mutants gaskets tsngen bench lint docs end; do sh $S/gate.sh <label> $s; done
(cd $A199_LANE/tb/verilator/engine && python3 $S/policy_mutation_evidence.py)
python3 $S/rom_differential.py --n 20000
python3 $S/rom_digests.py
python3 $S/slew_variants_model.py
```

Parent runs need a private clone first. The scratch clone was deleted, so recreate it:

1. `git clone --no-hardlinks $LANES/gptp68-parent-consumer $A199_PACKET/scratch/parent`.
2. Initialise `third_party/verilog-axis` and `protocol-processor` from that checkout's own submodules. Use `-c submodule.<name>.url=<local path>` and `-c protocol.file.allow=always`.
3. Initialise `gptp-processor` from `$A199_LANE`, then check out the head and `git add gptp-processor`.

After that:

- `make -C tb/verilator/gptp_shadow` in the clone;
- `scripts/parent_probe.sh <label> <rev> [patch]`;
- `scripts/parent_suite.sh <label> <rev> gptp_plane`.

## Decisions taken in this round, for the reviewers

1. **The link-up reading.** A link-up is the pair that raises the sync verdict, except after a grandmaster identity change clears it: the owner keeps that case locked. So a receipt timeout with asCapable held, and a return from mastership, both re-arm the link-up. Only an asCapable rise may be meant instead. In that case remove the SRTO leg's `S_LOCK` write; the matrix row "a receipt timeout keeps the lock" shows the tests that would change.
2. **No input saturation.** Every slewed offset is at most 100 us, so MULS is exact without it. The ROM had no room for both it and the whole-trim clamp, and the model shows a comparable settle.
3. **The PDPAIR verdict** now writes `S_PDGOT` ahead of the compare. That is behaviour-neutral: proved by executing both images.
4. **Leg relocation.** Eight legs moved by the packer (list in `PR-BODY.md`). Their content is identical to base.

## Pending, for the manager

- Push `68-step-policy` to `cbccf226`, and update the PR #74 body from `PR-BODY.md`.
- Route to R258 and R259 for re-review of all five lenses at the new head.
- The parent adoption lane (#387) owns:
  - the pin;
  - the per-configuration ROM digests;
  - the other parent consumer gates (idiom, xvlog, source lists, `milan_dp` gPTP-ON). These were not run here.
- For #387:
  - The phase-4 1 ms scenarios pass unchanged but no longer distinguish 20 from 100 us.
  - The `gptp_shadow` reconstruction law flags in-envelope trims near the clamp in that bench's 8 ns / 2 MHz shape. Measured: 1 result during an injected 90 us locked slew, with 0 refusals.

## Limits

- No hardware, no synthesis, no physical calibration.
- The product clock is analysed, not simulated. The parent bench runs 2 MHz servo gains on an 8 ns counter.
- The parent builder's gate 11 did not run: it needs a hardware build tree that is not on this host.
- Parent runs used a private clone of the parent checkout at `574c29fa`; that checkout itself was not modified. The `external` submodule was not initialised; no suite run here needs it.
- The engine mutation arm ran as four parallel slices of its own list, with its C++ builds at `-j 2` instead of `-j 4`.
