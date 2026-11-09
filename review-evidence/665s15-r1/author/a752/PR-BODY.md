[A752]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

BLOCKED after item 1: the census is committed and gated; items 2 to 5 wait on the decisions the census names. `665-s15-32x32` -> `dev-soft-core`.

Local gates at the head, every rc 0: every `run:` step of the four workflows a pull request to `dev-soft-core` triggers (136 ran, 221 not run with a reason, 0 bad); the full sweep, 65 of 65 suites and 2,192,828 checks (`milan_dp` re-run alone after a wall-clock timeout under host contention); the firmware self-test, coverage and every mutant campaign; the builder bank; behave; the split CPU budget harness at 1x1/1if and 8x8/2if. The 32x32/2if point cannot be built yet.

## Linked Issue / roles

Relates to #859
Relates to #665

Executor: `[A752]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

One commit on `dev-soft-core` `a9d69c77`: item 1 of the assignment on #859, the census of every per-shape limit a 32x32 shape on two AVB interfaces crosses.

| File | Change |
|---|---|
| `docs/design/SHAPE_32X32_CENSUS.md` (new) | The shape (32 AAF talker and 32 AAF listener streams of eight channels plus the CRF pair, stream n on interface n mod 2, everything else the 8x8 config's); nine tables, one per area the assignment lists, each limit with where it is stated, what bounds it, its rule and the figure at 1x1/1if, 8x8/2if and 32x32/2if; the rule for each limit that states none; and the three limits that need a decision |
| `docs/README.md` | One index row linking the page |

What the census finds, in short:

- **The saved-state record space and slot (#823) blocks the shape.** The builder's 16 streams per direction is the record space's 16-id blocks. At 32x32 the model has 395 writable names against 128 NAME ids, 596 records against the 256 ids of `record_id[7:0]`, and a 99,080 B image against one 64 KiB slot. The builder, the firmware's F1 store (`nvm_shape.h:132-133`) and the fabric backend (`KL_nvm_backend.sv:285-295`) each refuse it. #823 owns that format.
- **The mailbox contract's per-interface tables are full at 16.** Bound-talker, publication and face entries, and the bit-per-source fields. The firmware writes sink k into entry k, so 33 entries are needed; per-interface ordinals would still need 17 on the primary, where both CRF streams are. Growth moves fields, a major change.
- **The datapath stops on five elaboration guards at 32 streams**, among them the render crossbar's 3-bit stream field (at most 8 streams) and two 4-bit talker indices.
- Also measured: ACMP's 16 sinks and sources in tsn-c-stack, the SRP pool's 144,832 B at 32x32/2if from its own formula, the 69,488 B descriptor image against the 64 KiB `aem` flash slot, and the 224 KiB `sram` region against at least 243,920 B from two objects.

Every figure was taken on a scratch clone of the base, lifting one reported limit at a time; no lift is in the tree.

## Authoritative references

- #859 and its assignment; #640 (the 32x32 Mark II target, the 56-RAMB36 budget); #823 (the saved-state format at 32x32); #394 (Milan v1.2 clause 8 redundancy, out of scope).
- `sw/mailbox/mailbox.yaml` (the contract and its rules for change), [MAILBOX_SPLIT.md](docs/design/MAILBOX_SPLIT.md), [SPLIT_CONTROL_MEMORY.md](docs/design/SPLIT_CONTROL_MEMORY.md).
- Milan v1.2 Table 5.22 (the counter notification period); IEEE 1722-2016 Annex B (MAAP) and 4.4.4.8 (stream_id).

## How to get into the same state

```sh
git fetch origin 665-s15-32x32
git checkout --detach 6857012df33f51aa6e3cb6eafff26c4f82f0ea77
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

## How to validate

The page's gates:

```sh
python3 scripts/docs_check.py
python3 scripts/check_doc_paths.py
python3 scripts/gen_toc.py --check
python3 scripts/check_doc_style.py
git diff --check a9d69c774d HEAD
```

The census's first refusals, on a scratch copy of the 8x8 config with 32 rows of each direction:

```sh
S15=$(mktemp -d)
S15="$S15" python3 - <<'EOF'
import os
import re
s = open("configs/endstation_ax7101_8x8.yaml").read()
li = "\n".join(f'    - {{ name: "Stream In {i}", channels: 8, map_mode: dynamic }}' for i in range(32))
ta = "\n".join(f'    - {{ name: "Stream Out {i}", channels: 8, map_mode: dynamic, clusters: 2 }}' for i in range(32))
s = re.sub(r'(    - \{ name: "Stream In \d+".*\n)+', li + "\n", s)
s = re.sub(r'(    - \{ name: "Stream Out \d+".*\n)+', ta + "\n", s)
s = s.replace('name: "Milan FPGA 8x8"', 'name: "Milan FPGA 32x32"').replace("    last: 7\n", "    last: 31\n")
open(os.environ["S15"] + "/endstation_ax7101_32x32.yaml", "w").write(s)
EOF
python3 sw/builder/endstation_builder.py "$S15/endstation_ax7101_32x32.yaml" -o "$S15/out"
python3 scripts/check_nvm_record_space.py --config configs/endstation_ax7101_8x8.yaml
```

Expected result / pass criteria: each gate exits 0; the builder refuses the 32x32 config with `streams.listeners: 32 streams (max 16 per direction)`; the 8x8 record-space line reads `names=107 records=164 ... image= 13256 B (20% of a slot)`.

## Known limitations / out of scope

- Items 2 to 5 of #859 (the simulation-only config and its two gates, the contract's sizing, the firmware link, the Verilator legs and the harness rows at 32x32/2if) are not done: each needs the decisions in the census's section 4 first.
- No source, generated file, config or test changes, so no existing shape's output moves.
- Milan v1.2 clause 8 redundancy (#394), any route, and `sw/firmware/ctrl/loop/` are out of scope.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (item 1 only; items 2 to 5 blocked)
- [x] New or changed behavior has self-checking tests (no behavior changes)
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
