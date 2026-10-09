[A572]

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)

## Status

REVIEW READY: implementation committed and all local command families return 0.
The existing physical calibration arm is explicitly NOT RUN.
`665-f5-aecp` -> `dev`. Head `1e68d1b62ef2facdf0e8dbad28a202297d433c61`.
66 new named tests, 59 caught source defects, eight new production C units at raw
100% line and branch coverage, with no exclusion.

## Linked Issue / roles

Relates to #665

Executor: `[A572]`
Internal cleared-context reviewer: `[R564]`
External reviewer: `[R565]`

## Description

Add the opt-in bare-metal AECP owner and mailbox adapter beside the existing
ADP, ACMP, MAAP and SRP owners. The portable core serves every generated
descriptor and the mandatory Milan AEM/MVU commands, manages per-interface
controller registrations and notifications, and shares entity-wide locks and
saved values through typed environment ports.

The application bridge defers START/STOP, prevents late completion from applying
an expired request, holds MEDIA_UNLOCKED behind its owed UNBIND_RX response, and
restores saved channel maps atomically with the required format rollback.
Image parsing, mailbox access and persistence remain separate adapters.

The complete F0-F5/F1 linked fixture spans 139072/151728 bytes for the shipping
shape and 192240/219744 bytes for the largest shape at one/two interfaces,
including the 8192-byte stack. The largest case is below the revised 224 KB
threshold. Its nominal count is 48 RAMB36 tiles at 4608 bytes per tile;
32-bit data packing would require 54 and remains a routing obligation.
The packet lists all static pools and reduction options for the five largest
BSS consumers. No non-AECP reduction is implemented.

## Authoritative references

- #665 assignment comment 6081266905 and budget ruling 6081705916.
- REQUIREMENTS section 1; `docs/reference/FR_NFR.md`, NFR-SCOUT-02/03/08.
- `docs/design/MAILBOX_SPLIT.md` and `sw/mailbox/README.md`.
- IEEE 1722.1-2021 7.4, 7.5, 9.3.2.6; Milan v1.2 5.4 and Table 5.22.
- #653 response-before-notification ordering; #637 saved-map restore and rollback.
- #678 deferred callback contract; #697 portability boundary.
- Processor issues 69 (interface index) and 73 (future command model).
- `sw/firmware/ctrl/aecp/README.md` for API, boot order and measured limits.

## How to get into the same state

Use the local branch or a subsequently authorized publication of the exact head.
Dependencies must be at the repository pins. Before a command inside a
submodule, check that its reported top level is that directory.

```sh
git switch 665-f5-aecp
git rev-parse HEAD
export TMPDIR="$F5_SCRATCH"
export PYTHONDONTWRITEBYTECODE=1
export VERILATOR_JOBS=2
```

`REPRODUCE.md` in the handoff packet defines dependency selectors, runtime
source fingerprints, the second interface reference and foreground partitions.
All generated files and build products go to disk-backed scratch.

## How to validate

```sh
python3 -B sw/mailbox/gen_mailbox.py --check
python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py \
  --require-rv32 --jobs 4 --build-dir "$F5_SCRATCH/firmware-bank"
python3 -B sw/firmware/gtest/fw_coverage.py \
  --check --jobs 4 --keep "$F5_SCRATCH/coverage" --lwsrp third_party/lwSRP
python3 -B sw/firmware/ctrl/test/aecp_mutants.py \
  --shard 0 2 --output "$F5_SCRATCH/mutants-zero"
python3 -B sw/firmware/ctrl/test/aecp_mutants.py \
  --shard 1 2 --output "$F5_SCRATCH/mutants-one"
python3 -B sw/firmware/ctrl/test/aecp_wire.py \
  --reference protocol-processor --interfaces 1 \
  --output "$F5_SCRATCH/wire-one" --verilator "$PINNED_VERILATOR"
python3 -B sw/firmware/ctrl/test/aecp_wire.py \
  --reference "$PROCESSOR_69_REFERENCE" --interfaces 2 \
  --output "$F5_SCRATCH/wire-two" --verilator "$PINNED_VERILATOR"
python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --with-aecp \
  --config configs/endstation_ax7101_8x8.yaml --interfaces 2 \
  --output "$F5_SCRATCH/largest-two" \
  --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a"
```

Expected result: every gate returns 0; all new source plants fail their named
assertions; raw new-file coverage is 100%; all four linked cases pass ABI,
no-heap and retained-symbol checks. Run the complete mailbox, firmware
mutation, saved-state, builder and documentation banks using the packet's
recorded foreground partitions; each original table must be covered exactly
once. The existing physical calibration arm is explicitly NOT RUN because no
calibration report is available and hardware access is outside this lane.

The wire differential passes 123 observations for one interface and 128 on each
two-interface ingress. Its six observation controls per ingress all fail as
intended. Four exact differences are recorded in the AECP contract: mandatory
system ID support (Milan 5.4.4.2/3), first saved-default override notifications
(5.4.5.2), the additional started-state GET_STREAM_INFO notification (Table
5.22), and permitted unlock-flag alternatives (IEEE 7.4.2.1). No other difference
is accepted.

## Known limitations / out of scope

- Default all-fabric behavior, the shipping image, RTL and register maps are unchanged.
- The link fixture uses explicit unavailable physical observers and is not a board image.
- Desk service bounds include explicit access/CPU allowances: maximum command body
  1.0770 ms, full fanout 1.1573 ms, one-millisecond TX stall 2.0069 ms and deferred
  failure 9.0061 ms. Target CPU timing, full call-chain stack proof and physical
  transmit timing remain integration work.
- The two-interface reference exposes ingress but no physical egress index;
  registration isolation and the core egress index are checked separately.
- Processor issue 73 is open; future shared command-model adoption is owed.
  System unique ID is volatile pending its saved-record decision.
- The default flip still owes routed resource use and the 10% reserve.
- No hosted CI, independent review, merge-candidate or post-merge evidence is claimed.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes (physical calibration arm explicitly NOT RUN)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
