[A594]

## Contents

- **[Status](#status)** — STOP at the memory-fit proof; no change; `640-m8a` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — The fit table, as mapped, the reuse census, the ledger and the missing prerequisites.
- **[Authoritative references](#authoritative-references)** — Rulings, plan sections and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout and environment.
- **[How to validate](#how-to-validate)** — The commands that reproduce every figure.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What was not done, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from CONTRIBUTING.md.

## Status

STOP. The assignment's own condition fired: "A shape that does not fit is a STOP with the table".
No commit: the branch head is its base, dev `e8454e2751d05b02ee8e5a571857589ab358ab86`. Ten evidence commands, all rc 0; one optional mapping variant was not run.
There is nothing to merge. This body records the evidence for the decision.

## Linked Issue / roles

Relates to #640

Executor: `[A594]`
Internal cleared-context reviewer: `[R606]`
External reviewer: `[R607]`

Assignment: #640 comment 6100371426. TAKEN: #640 comment 6100426002. STOP: #640 comment 6101473717.

## Description

**Memory fit.** The firmware was linked at this base with `sw/firmware/ctrl/test/ctrl_srp_image.py --with-aecp`: the full F0-F5/F1 composition, with an 8,192-byte stack reservation. The span already holds:

- the descriptor image (`aecp_entity_image`, 7,512 / 19,520 B, CRC-identical to the fabric's `aem_desc.bin`);
- the shape-sized stage (`nvm_stage`, 3,344 / 13,264 B);
- the lwSRP pool.

| Point | Linked span, B | Floor RAMB36 (4,096 B each) | As mapped, ROM + RAM | As mapped, unified | Against 50 RAMB36 |
|---|---:|---:|---:|---:|---|
| 1x1, one interface (shipping) | 140,400 | 35 | 48 | 64 | fits as ROM + RAM |
| 1x1, two interfaces | 153,056 | 38 | 48 | 64 | fits as ROM + RAM |
| 8x8, one interface | 194,224 | 48 | 64 | 64 | over as mapped; fits only at the floor |
| **8x8, two interfaces** | **221,728** | **55** | **64** | **64** | **over: 16,928 B past the ceiling** |

A RAMB36 exposes 4,096 byte-addressable bytes. The 224 KB / 50-tile figure assumed 4.5 KB per tile, which counts parity bits that a byte-addressed bus cannot use, so 224,000 B needs 55 RAMB36. The floor counts no boot code.

**As mapped.** Each memory is LiteX's own `wishbone.SRAM`, emitted by LiteX, with the ROM initialised from the linked image. It was synthesised out of context at the shipping part and `AreaOptimized_high`. Vivado's default inference rounds every memory to a power-of-two depth:

- 50 x 4,096 B = 204,800 B, the whole 50-tile ceiling, maps to **64 RAMB36**;
- every unified image maps to 64;
- ROMs of 23,736-27,492 words map to 32;
- RAMs map to 16 (1x1) or 32 (8x8).

Reaching the floor needs a 1K x 32-per-tile decomposition. A `ram_decomp` variant was prepared but not run, so whether that attribute achieves it is unmeasured.

**BIOS ROM and SRAM reuse at `e8454e27`:** 16 RAMB36 ROM (53,116 B of content) + 2 RAMB36 SRAM = **18 RAMB36, 0 RAMB18**. The ledger's extra RAMB18 is the 49-byte SoC identifier memory, which stays in either placement. With the BIOS retained (about 38-40 KB), both 8x8 points exceed 50 tiles.

**Ledger:** with the measured reuse, `87.5 - 6.5 + 6 - 18 + 55 + 2 = 126` tiles at the floor and `... + 64 + 2 = 135` as mapped. Both are over the 121.5 ceiling before the conditional 11-tile release (115 and 124 after it).

**Prerequisites absent at this base** (needed by the service and route proofs):

- `--ctrl-mailbox` keeps the wrapper (`hdl/milan/milan_datapath.sv:8003`) and holds the mailbox idle (`sw/litex/milan_soc.py:2548-2553`).
- No SoC build links the control application (`sw/litex/milan_soc.py:3990-3993`), so no split image can boot to its ready state.
- M0s has no split figure (`docs/design/MARK_II_AREA_PLAN.md:644-648`), and the `f0-f4` census refuses a wrapper-retaining export (`syn/ooc/pp_placement.py:41-48`).

The switch that removes the wrapper is F-INT PR 2 (#665), not yet assigned.

**All-fabric without DDR3 (measurement only):** DDR3 holds only the processor window. Compacted, it is 14,792 B at 1x1 (4 RAMB36) and 46,640 B at 8x8 (12 RAMB36): the descriptor image, the 592-byte response buffer and two containers. Dropping DDR3 would also need:

- a compacted window and its compile-time bases;
- an on-chip memory on the DMA bus;
- a pinned `spiflash` CSR location.

**Decisions needed:**

1. Raise the allocation, reduce the firmware (the five largest consumers are tabled in the handoff), or bound the largest shape's interface count.
2. Keep the BIOS or give the control firmware its own reset entry.
3. Sequence M8a's proofs after F-INT PR 2.

**Observation for a separate Issue:** the comment at `sw/litex/milan_soc.py:3005-3006` gives the 8x8 descriptor image as 23,216 bytes. It is 19,520 B at this base.

## Authoritative references

- #640 assignment 6100371426; owner decisions 5991591637 (D4) and 6081706413 (224 KB); manager rulings 5990755268 (D3, D7).
- #665 F5 size ruling 6081705916 and F5 spans 6086832557; F-INT ruling 6088423771 (PR 2 carries the split switch).
- `docs/design/MARK_II_AREA_PLAN.md`, "L11 The SoC side" and "Firmware and block RAM ledger".
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, "Selected-placement measurements".
- `sw/firmware/ctrl/README.md`, "Linked size"; `sw/firmware/ctrl/aecp/README.md`, "Verification and limits".

## How to get into the same state

```sh
git fetch origin
git checkout -b 640-m8a e8454e2751d05b02ee8e5a571857589ab358ab86
git submodule update --init
python3 scripts/ci_rv32_sdk.py --destination "$SDK" --verify-only
export MILAN_RV32_CC="$SDK/bin/riscv32-linux-gcc"
```

The runtime archives need `-fno-stack-protector`, because the SDK's compiler defaults to the stack protector. Build them with `MILAN_RV32_CC` naming a compiler wrapper that adds that flag.

## How to validate

```sh
python3 sw/firmware/ctrl/test/ctrl_image_runtime.py --picolibc "$PICOLIBC" \
  --compiler-rt "$COMPILER_RT" --litex-software "$LITEX_SOFTWARE" --output "$RUNTIME"
for shape in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
  for ifs in 1 2; do
    python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config "configs/$shape.yaml" \
      --interfaces "$ifs" --with-aecp --output "$IMAGE/$shape-if$ifs" \
      --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a"
  done
done
python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32
python3 syn/ooc/pp_baseline.py --selftest
```

Expected result: every command exits 0; `ram_span` reads 140400, 153056, 194224 and 221728; the image self-test prints `33 checks PASS`.
The as-mapped figures come from the mapping script and Tcl in the handoff's evidence, run with Vivado at the shipping part and directive.

## Known limitations / out of scope

- No implementation: the STOP condition fired before any change, and the split build that the service and route proofs need is absent.
- No planted controls, service checks, simulation boot or route were run, for the same reasons.
- The as-mapped figures are out-of-context synthesis of each memory alone, not a placed SoC.
- The `ram_decomp` mapping variant was not run.
- The BIOS-retained figures are estimates from the base link map, not a linked image.
- The reuse census comes from the base route of `e8454e27` measured by lane M2, whose gate check passed against `route-1x1`.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (STOP: memory fit fails at 8x8 with two interfaces)
- [ ] New or changed behavior has self-checking tests (no change)
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
